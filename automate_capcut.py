#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
automate_capcut.py  —  Automação COMPLETA de edição com VectCutAPI + CapCut (Windows)

Padrão do vídeo de referência (tudo automatizado):
  1) Baixa IMG_7844.mov do Google Drive -> VectCutAPI\\input\\
  2) Cria draft 1080x1920
  3) Adiciona o vídeo  (com CORTE DE SILÊNCIOS por padrão)
  4) Título grande no topo (branco, bold, centralizado, SEM fundo)
  5) Legenda com FUNDO LARANJA no rodapé  (SRT RE-SINCRONIZADO à timeline cortada)
  6) Trilha de suspense baixa (opcional)
  7) ZOOM por keyframe em momentos-chave (segmentos com palavra-chave + lista manual)
  8) Overlays de IMAGEM em momentos específicos
  9) SFX de transição (glitch/whoosh) discretos nos cortes  (gerados em Python puro)
 10) save_draft + move automático para a pasta do CapCut

Requisitos :  pip install requests gdown
Recomendado:  pip install faster-whisper pydub   (legenda + corte de silêncio)
              ffmpeg no PATH
"""

import os
import sys
import math
import wave
import struct
import random
import shutil
import subprocess
from collections import deque

import requests

# ============================== CONFIG ==============================
API_BASE      = "http://127.0.0.1:9001"
DRIVE_FILE_ID = "18ECBxthBbpCkidwUtSPRgEZp49Y1BQQe"   # IMG_7844.mov

VECTCUT_DIR   = r"C:\Users\moret\VectCutAPI"
INPUT_DIR     = os.path.join(VECTCUT_DIR, "input")
CAPCUT_DRAFTS = r"C:\Users\moret\AppData\Local\CapCut\User Data\Projects\com.lveditor.draft"

VIDEO_NAME    = "IMG_7844.mov"
WIDTH, HEIGHT = 1080, 1920

# ---- Título (topo, sem fundo) ----
TITLE_TEXT   = "ESFORÇO x RESULTADO"      # <- ajuste
TITLE_FONT   = "Source Han Sans"          # veja GET /get_font_types (precisa de acento PT)
TITLE_COLOR  = "#FFFFFF"
TITLE_SIZE   = 15.0
TITLE_Y      = 0.80                       # topo. Se inverter, use -0.80
TITLE_START, TITLE_END = 0.0, 5.0

# ---- Legenda (rodapé, fundo laranja) ----
SUB_FONT     = "Source Han Sans"
SUB_COLOR    = "#FFFFFF"
SUB_SIZE     = 7.0
SUB_BG_COLOR = "#FF6600"
SUB_Y        = -0.80                      # rodapé. Se inverter, use 0.80
WHISPER_MODEL = "small"                   # tiny/base/small/medium

# ---- Corte de silêncios ----
REMOVE_SILENCES   = True
SILENCE_THRESH_DB = -38                   # mais negativo = corta menos
MIN_SILENCE_MS    = 500                   # pausa mínima p/ cortar
KEEP_PAD_MS       = 120                   # respiro mantido nas bordas

# ---- Zoom por keyframe ----
KEYWORDS = ["RECORDE", "ESFORÇAM", "ESFORÇO", "MUSCULAÇÃO", "NATAÇÃO",
            "CORRIDA", "CARGAS", "DIRECIONAMENTO", "EVOLUEM"]
AUTO_ZOOM_ON_KEYWORDS = True
ZOOM_FROM, ZOOM_TO = 1.0, 1.10            # escala inicial/final do zoom
ZOOM_MOMENTS = []                         # extra manual: [(t_ini, t_fim), ...] na timeline final

# ---- Overlays de imagem ----  [{path, start, end, scale, x, y}]  (tempos na timeline final)
IMAGE_OVERLAYS = [
    # {"path": r"C:\Users\moret\VectCutAPI\input\print1.png", "start": 6.0, "end": 9.0,
    #  "scale": 0.7, "x": 0.0, "y": 0.2},
]

# ---- Trilha de suspense (opcional) ----
MUSIC_PATH   = ""                         # .mp3/.wav local; "" = pula
MUSIC_VOLUME = 0.15

# ---- SFX de transição ----
SFX_TRANSITIONS = True
SFX_VOLUME      = 0.35
SFX_DIR         = INPUT_DIR               # onde gerar glitch.wav / whoosh.wav

MOVE_DRAFT   = True
# ===================================================================


def api(endpoint, payload):
    r = requests.post(f"{API_BASE}/{endpoint}", json=payload, timeout=900)
    r.raise_for_status()
    data = r.json()
    if isinstance(data, dict) and data.get("success") is False:
        raise RuntimeError(f"[{endpoint}] falhou: {data.get('error') or data}")
    return data.get("output", data) if isinstance(data, dict) else data


def get_draft_id(out):
    for key in ("draft_id", "draftId", "id"):
        if isinstance(out, dict) and out.get(key):
            return out[key]
        if isinstance(out, dict) and isinstance(out.get("output"), dict) and out["output"].get(key):
            return out["output"][key]
    raise RuntimeError(f"Não achei draft_id na resposta: {out}")


def ffprobe_duration(path):
    try:
        r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                            "-of", "csv=p=0", path], capture_output=True, text=True)
        return float(r.stdout.strip())
    except Exception:
        return None


# ---------------------------------------------------------------- download
def download_drive(file_id, out_path):
    if os.path.exists(out_path):
        print(f"[download] já existe: {out_path}"); return out_path
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    try:
        import gdown
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "gdown"])
        import gdown
    print("[download] baixando do Drive...")
    gdown.download(id=file_id, output=out_path, quiet=False)
    if not os.path.exists(out_path):
        raise RuntimeError("Falha no download do Drive.")
    return out_path


# ---------------------------------------------------------------- silêncios
def build_speech_segments(video_path):
    """Retorna lista de (src_start, src_end) em segundos, com silêncios removidos."""
    from pydub import AudioSegment, silence
    audio = AudioSegment.from_file(video_path)
    nonsilent = silence.detect_nonsilent(audio, min_silence_len=MIN_SILENCE_MS,
                                          silence_thresh=SILENCE_THRESH_DB)
    segs = []
    for a, b in nonsilent:
        a = max(0, a - KEEP_PAD_MS); b = min(len(audio), b + KEEP_PAD_MS)
        segs.append((a / 1000.0, b / 1000.0))
    return segs or [(0.0, len(audio) / 1000.0)]


def make_mapper(kept):
    """kept = [(s,e),...] -> função src_time->timeline_time e duração total."""
    starts = []; acc = 0.0
    for (s, e) in kept:
        starts.append(acc); acc += (e - s)
    def m(t):
        for (s, e), st in zip(kept, starts):
            if s <= t <= e:
                return st + (t - s)
        for (s, e), st in zip(kept, starts):
            if t < s:
                return st
        return acc
    return m, acc


# ---------------------------------------------------------------- transcrição
def transcribe(video_path):
    """Retorna lista de segmentos [{start,end,text}] (PT) ou None se faster-whisper ausente."""
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        print("[asr] faster-whisper não instalado -> sem legenda/zoom automático.")
        return None
    print(f"[asr] transcrevendo ({WHISPER_MODEL})...")
    model = WhisperModel(WHISPER_MODEL, device="cpu", compute_type="int8")
    segments, _ = model.transcribe(video_path, language="pt", vad_filter=True)
    return [{"start": s.start, "end": s.end, "text": s.text.strip()} for s in segments]


def write_srt(segments, mapper, srt_path):
    def fmt(t):
        h = int(t // 3600); m = int((t % 3600) // 60); s = t % 60
        return f"{h:02d}:{m:02d}:{s:06.3f}".replace(".", ",")
    lines = []; idx = 1
    for seg in segments:
        st = mapper(seg["start"]); en = mapper(seg["end"])
        if en - st < 0.2:
            continue
        lines.append(f"{idx}\n{fmt(st)} --> {fmt(en)}\n{seg['text']}\n")
        idx += 1
    with open(srt_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"[srt] {idx-1} blocos -> {srt_path}")
    return srt_path


# ---------------------------------------------------------------- SFX (Python puro)
def _save_wav(path, samples, sr=44100):
    with wave.open(path, "w") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes(b"".join(struct.pack("<h", int(max(-1, min(1, s)) * 32767)) for s in samples))


def gen_whoosh(path, dur=0.30, sr=44100):
    n = int(sr * dur); noise = [random.uniform(-1, 1) for _ in range(n)]
    dq = deque(); acc = 0.0; sm = []; k = 22
    for x in noise:
        dq.append(x); acc += x
        if len(dq) > k:
            acc -= dq.popleft()
        sm.append(acc / len(dq))
    out = [s * (math.sin(math.pi * i / n) ** 1.5) * 0.5 for i, s in enumerate(sm)]
    _save_wav(path, out, sr)


def gen_glitch(path, dur=0.18, sr=44100):
    n = int(sr * dur)
    out = [random.uniform(-1, 1) * (1.0 if (int((i/n) * 90) % 2 == 0) else 0.15)
           * math.exp(-(i/n) * 9) * 0.5 for i in range(n)]
    _save_wav(path, out, sr)


def ensure_sfx():
    g = os.path.join(SFX_DIR, "glitch.wav"); w = os.path.join(SFX_DIR, "whoosh.wav")
    os.makedirs(SFX_DIR, exist_ok=True)
    if not os.path.exists(g):
        gen_glitch(g)
    if not os.path.exists(w):
        gen_whoosh(w)
    return g, w


# ---------------------------------------------------------------- API helpers
def add_video_full(draft_id, video_path):
    api("add_video", {"draft_id": draft_id, "video_url": video_path,
                      "width": WIDTH, "height": HEIGHT, "track_name": "video_main", "volume": 1.0})


def add_video_cut(draft_id, video_path, kept):
    timeline = 0.0; cuts = []
    for (s, e) in kept:
        api("add_video", {"draft_id": draft_id, "video_url": video_path,
                          "start": s, "end": e, "target_start": timeline,
                          "width": WIDTH, "height": HEIGHT, "track_name": "video_main", "volume": 1.0})
        timeline += (e - s)
        cuts.append(timeline)        # fronteira entre trechos
    print(f"[silence] {len(kept)} trechos | timeline final = {timeline:.2f}s")
    return cuts[:-1], timeline        # ignora a última fronteira (= fim do vídeo)


def add_zoom(draft_id, t0, t1, z0=ZOOM_FROM, z1=ZOOM_TO):
    """Zoom suave entre t0 e t1 (timeline) na faixa video_main, via keyframes scale_x/scale_y."""
    api("add_video_keyframe", {
        "draft_id": draft_id, "track_name": "video_main",
        "property_types": ["scale_x", "scale_y", "scale_x", "scale_y"],
        "times":          [t0, t0, t1, t1],
        "values":         [str(z0), str(z0), str(z1), str(z1)],
    })


def add_transition_sfx(draft_id, cut_times, glitch, whoosh):
    for i, ct in enumerate(cut_times):
        sfx = glitch if i % 2 == 0 else whoosh
        api("add_audio", {"draft_id": draft_id, "audio_url": sfx,
                          "target_start": max(0.0, ct - 0.06), "volume": SFX_VOLUME,
                          "track_name": "sfx"})
    print(f"[sfx] {len(cut_times)} transições (glitch/whoosh)")


def add_overlays(draft_id, overlays):
    for ov in overlays:
        if not os.path.exists(ov["path"]):
            print(f"[overlay] arquivo não encontrado, pulando: {ov['path']}"); continue
        api("add_image", {"draft_id": draft_id, "image_url": ov["path"],
                          "start": ov["start"], "end": ov["end"],
                          "scale_x": ov.get("scale", 1.0), "scale_y": ov.get("scale", 1.0),
                          "transform_x": ov.get("x", 0.0), "transform_y": ov.get("y", 0.0),
                          "width": WIDTH, "height": HEIGHT,
                          "intro_animation": "渐显", "outro_animation": "渐隐",  # fade in/out
                          "track_name": "image_main"})
    if overlays:
        print(f"[overlay] {len(overlays)} imagens")


def move_to_capcut(draft_id):
    src = os.path.join(VECTCUT_DIR, draft_id); dst = os.path.join(CAPCUT_DRAFTS, draft_id)
    if os.path.isdir(dst):
        print(f"[move] já no CapCut: {dst}"); return
    if not os.path.isdir(src):
        print(f"[move] {src} não existe (talvez save_draft já salvou em {CAPCUT_DRAFTS})."); return
    os.makedirs(CAPCUT_DRAFTS, exist_ok=True)
    shutil.move(src, dst)
    print(f"[move] {src} -> {dst}")


# ---------------------------------------------------------------- main
def main():
    video_path = download_drive(DRIVE_FILE_ID, os.path.join(INPUT_DIR, VIDEO_NAME))

    out = api("create_draft", {"width": WIDTH, "height": HEIGHT})
    draft_id = get_draft_id(out)
    print(f"[draft] {draft_id}")

    # ---- vídeo (com/sem corte de silêncio) ----
    kept = None; cut_times = []
    if REMOVE_SILENCES:
        try:
            kept = build_speech_segments(video_path)
            cut_times, total = add_video_cut(draft_id, video_path, kept)
        except ImportError:
            print("[silence] pydub ausente -> vídeo inteiro. (pip install pydub)")
            kept = None
    if kept is None:
        add_video_full(draft_id, video_path)
        dur = ffprobe_duration(video_path) or 0.0
        kept = [(0.0, dur)]
    mapper, total = make_mapper(kept)
    print("[ok] vídeo adicionado")

    # ---- título ----
    api("add_text", {"draft_id": draft_id, "text": TITLE_TEXT,
                     "start": TITLE_START, "end": TITLE_END,
                     "font": TITLE_FONT, "font_color": TITLE_COLOR, "font_size": TITLE_SIZE,
                     "transform_x": 0.0, "transform_y": TITLE_Y, "track_name": "title"})
    print("[ok] título")

    # ---- transcrição (legenda + zoom por palavra-chave) ----
    segments = transcribe(video_path)
    if segments:
        srt = write_srt(segments, mapper, os.path.join(INPUT_DIR, "IMG_7844.srt"))
        api("add_subtitle", {"draft_id": draft_id, "srt": srt,
                             "font": SUB_FONT, "font_size": SUB_SIZE, "font_color": SUB_COLOR,
                             "transform_x": 0.0, "transform_y": SUB_Y,
                             "background_color": SUB_BG_COLOR, "background_alpha": 1.0,
                             "background_style": 1, "track_name": "subtitle"})
        print("[ok] legenda (fundo laranja)")

    # ---- música ----
    if MUSIC_PATH and os.path.exists(MUSIC_PATH):
        api("add_audio", {"draft_id": draft_id, "audio_url": MUSIC_PATH,
                          "volume": MUSIC_VOLUME, "track_name": "music"})
        print("[ok] trilha")

    # ---- zoom por keyframe ----
    zoom_windows = list(ZOOM_MOMENTS)
    if AUTO_ZOOM_ON_KEYWORDS and segments:
        for seg in segments:
            up = seg["text"].upper()
            if any(kw in up for kw in KEYWORDS):
                a, b = mapper(seg["start"]), mapper(seg["end"])
                if b - a >= 0.4:
                    zoom_windows.append((a, b))
    for (a, b) in zoom_windows:
        add_zoom(draft_id, a, b)
    if zoom_windows:
        print(f"[ok] {len(zoom_windows)} zooms por keyframe")

    # ---- overlays de imagem ----
    add_overlays(draft_id, IMAGE_OVERLAYS)

    # ---- SFX de transição ----
    if SFX_TRANSITIONS and cut_times:
        glitch, whoosh = ensure_sfx()
        add_transition_sfx(draft_id, cut_times, glitch, whoosh)

    # ---- salvar + mover ----
    save_out = api("save_draft", {"draft_id": draft_id, "draft_folder": CAPCUT_DRAFTS})
    print(f"[save] {save_out}")
    if MOVE_DRAFT:
        move_to_capcut(draft_id)

    print(f"\n✅ PRONTO. draft_id: {draft_id}  | timeline: {total:.2f}s")
    print("   Abra o CapCut e ajuste o que quiser (zooms/overlays já entram automáticos).")


if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("ERRO: API offline? Rode: python capcut_server.py (porta 9001)")
        sys.exit(1)
    except Exception as e:
        print("ERRO:", e)
        sys.exit(1)
