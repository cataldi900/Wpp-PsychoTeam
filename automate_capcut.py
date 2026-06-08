#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
automate_capcut.py  —  Automação de edição com VectCutAPI + CapCut (Windows)

Faz:
  1) Baixa IMG_7844.mov do Google Drive -> C:\\Users\\moret\\VectCutAPI\\input\\
  2) Cria draft 1080x1920
  3) Adiciona o vídeo
  4) Título grande no topo (branco, bold, centralizado, SEM fundo)
  5) Legenda com FUNDO LARANJA no rodapé (SRT gerado por faster-whisper, se disponível)
  6) (opcional) trilha de suspense baixa
  7) save_draft + move automático para a pasta do CapCut

Zooms/overlays o Gui finaliza no CapCut. Detecção de silêncios = função opcional no fim.

Requisitos:  pip install requests gdown
Opcionais :  pip install faster-whisper   (legenda automática)
             pip install pydub            (corte de silêncios — função no fim)
             (ffmpeg no PATH para faster-whisper/pydub)

Servidor VectCutAPI precisa estar rodando:  python capcut_server.py  (porta 9001)
"""

import os
import sys
import shutil
import subprocess
import requests

# ============================== CONFIG ==============================
API_BASE      = "http://127.0.0.1:9001"
DRIVE_FILE_ID = "18ECBxthBbpCkidwUtSPRgEZp49Y1BQQe"   # IMG_7844.mov

VECTCUT_DIR   = r"C:\Users\moret\VectCutAPI"
INPUT_DIR     = os.path.join(VECTCUT_DIR, "input")
CAPCUT_DRAFTS = r"C:\Users\moret\AppData\Local\CapCut\User Data\Projects\com.lveditor.draft"

VIDEO_NAME    = "IMG_7844.mov"
WIDTH, HEIGHT = 1080, 1920

# ---- Título (topo) ----
TITLE_TEXT   = "ESFORÇO x RESULTADO"      # <- ajuste
TITLE_FONT   = "Source Han Sans"          # veja opções em GET /get_font_types
TITLE_COLOR  = "#FFFFFF"
TITLE_SIZE   = 15.0                       # escala da API (padrão 8.0); título maior
TITLE_Y      = 0.80                       # topo. Se aparecer embaixo, troque p/ -0.80
TITLE_START, TITLE_END = 0.0, 5.0         # quando o título aparece (s)

# ---- Legenda (rodapé, fundo laranja) ----
SUB_FONT     = "Source Han Sans"
SUB_COLOR    = "#FFFFFF"
SUB_SIZE     = 7.0
SUB_BG_COLOR = "#FF6600"                  # laranja
SUB_Y        = -0.80                      # rodapé. Se inverter, use 0.80
SRT_PATH     = os.path.join(INPUT_DIR, "IMG_7844.srt")  # usado se existir; senão tenta gerar
WHISPER_MODEL = "small"                   # tiny/base/small/medium (qualidade x velocidade)

# ---- Trilha de suspense (opcional) ----
MUSIC_PATH   = ""                         # caminho local .mp3/.wav; "" = pula
MUSIC_VOLUME = 0.15                        # bem baixo

MOVE_DRAFT   = True                       # mover automaticamente p/ a pasta do CapCut
# ===================================================================


def api(endpoint, payload):
    """POST no VectCutAPI; retorna o objeto 'output' (ou o JSON inteiro)."""
    url = f"{API_BASE}/{endpoint}"
    r = requests.post(url, json=payload, timeout=900)
    r.raise_for_status()
    data = r.json()
    if isinstance(data, dict) and data.get("success") is False:
        raise RuntimeError(f"[{endpoint}] falhou: {data.get('error') or data}")
    return data.get("output", data) if isinstance(data, dict) else data


def get_draft_id(out):
    """Extrai draft_id de respostas em formatos variados."""
    for key in ("draft_id", "draftId", "id"):
        if isinstance(out, dict) and out.get(key):
            return out[key]
        if isinstance(out, dict) and isinstance(out.get("output"), dict) and out["output"].get(key):
            return out["output"][key]
    raise RuntimeError(f"Não achei draft_id na resposta: {out}")


def download_drive(file_id, out_path):
    if os.path.exists(out_path):
        print(f"[download] já existe: {out_path}")
        return out_path
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    try:
        import gdown
    except ImportError:
        print("[download] instalando gdown...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "gdown"])
        import gdown
    print("[download] baixando do Google Drive...")
    gdown.download(id=file_id, output=out_path, quiet=False)
    if not os.path.exists(out_path):
        raise RuntimeError("Falha no download do Drive. Verifique o compartilhamento do arquivo.")
    return out_path


def maybe_make_srt(video_path, srt_path):
    """Gera SRT com faster-whisper se não existir. Retorna o caminho ou None."""
    if os.path.exists(srt_path):
        print(f"[srt] usando existente: {srt_path}")
        return srt_path
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        print("[srt] faster-whisper não instalado -> pulando legenda.")
        print("      Instale (pip install faster-whisper) ou coloque um arquivo em:", srt_path)
        return None

    def fmt(t):
        h = int(t // 3600); m = int((t % 3600) // 60); s = t % 60
        return f"{h:02d}:{m:02d}:{s:06.3f}".replace(".", ",")

    print(f"[srt] transcrevendo ({WHISPER_MODEL}) — pode demorar...")
    model = WhisperModel(WHISPER_MODEL, device="cpu", compute_type="int8")
    segments, _ = model.transcribe(video_path, language="pt", vad_filter=True)
    blocks = []
    for i, seg in enumerate(segments, 1):
        blocks.append(f"{i}\n{fmt(seg.start)} --> {fmt(seg.end)}\n{seg.text.strip()}\n")
    with open(srt_path, "w", encoding="utf-8") as f:
        f.write("\n".join(blocks))
    print(f"[srt] gerado: {srt_path}")
    return srt_path


def move_to_capcut(draft_id):
    src = os.path.join(VECTCUT_DIR, draft_id)
    dst = os.path.join(CAPCUT_DRAFTS, draft_id)
    if os.path.isdir(dst):
        print(f"[move] já está no CapCut: {dst}")
        return
    if not os.path.isdir(src):
        print(f"[move] não achei {src}. (Talvez o save_draft já tenha salvo em {CAPCUT_DRAFTS}.)")
        return
    os.makedirs(CAPCUT_DRAFTS, exist_ok=True)
    shutil.move(src, dst)
    print(f"[move] {src}  ->  {dst}")


def main():
    # 1) baixar vídeo
    video_path = download_drive(DRIVE_FILE_ID, os.path.join(INPUT_DIR, VIDEO_NAME))

    # 2) criar draft
    out = api("create_draft", {"width": WIDTH, "height": HEIGHT})
    draft_id = get_draft_id(out)
    print(f"[draft] id = {draft_id}")

    # 3) adicionar vídeo (faixa principal, caminho LOCAL absoluto)
    api("add_video", {
        "draft_id": draft_id,
        "video_url": video_path,
        "width": WIDTH, "height": HEIGHT,
        "track_name": "video_main",
        "volume": 1.0,
    })
    print("[ok] vídeo adicionado")

    # 4) título no topo (sem fundo => NÃO passamos background_*)
    api("add_text", {
        "draft_id": draft_id,
        "text": TITLE_TEXT,
        "start": TITLE_START, "end": TITLE_END,
        "font": TITLE_FONT,
        "font_color": TITLE_COLOR,
        "font_size": TITLE_SIZE,
        "transform_x": 0.0,
        "transform_y": TITLE_Y,
        "track_name": "title",
    })
    print("[ok] título adicionado")

    # 5) legenda com fundo laranja (precisa de SRT)
    srt = maybe_make_srt(video_path, SRT_PATH)
    if srt:
        api("add_subtitle", {
            "draft_id": draft_id,
            "srt": srt,
            "font": SUB_FONT,
            "font_size": SUB_SIZE,
            "font_color": SUB_COLOR,
            "transform_x": 0.0,
            "transform_y": SUB_Y,
            # fundo laranja sólido:
            "background_color": SUB_BG_COLOR,
            "background_alpha": 1.0,
            "background_style": 1,      # 1 = caixa sólida (confirme no README/get_* se preciso)
            "track_name": "subtitle",
        })
        print("[ok] legenda (fundo laranja) adicionada")

    # 6) trilha de suspense baixa (opcional)
    if MUSIC_PATH and os.path.exists(MUSIC_PATH):
        api("add_audio", {
            "draft_id": draft_id,
            "audio_url": MUSIC_PATH,
            "volume": MUSIC_VOLUME,
            "track_name": "music",
        })
        print("[ok] trilha adicionada")

    # 7) salvar (passando draft_folder do CapCut) + mover como rede de segurança
    save_out = api("save_draft", {"draft_id": draft_id, "draft_folder": CAPCUT_DRAFTS})
    print(f"[save] {save_out}")
    if MOVE_DRAFT:
        move_to_capcut(draft_id)

    print("\n✅ PRONTO. Abra o CapCut e finalize zooms/overlays.")
    print(f"   draft_id: {draft_id}")


# =====================================================================
# OPCIONAL — corte de silêncios (precisa: pip install pydub + ffmpeg)
# Em vez de add_video único, divide a fala em trechos e adiciona sem as
# pausas (re-temporizando target_start). Zooms/overlays continuam manuais.
# =====================================================================
def build_speech_segments(video_path, silence_thresh_db=-38, min_silence_ms=500, keep_pad_ms=120):
    """Retorna lista de (start_s, end_s) de FALA, com silêncios removidos."""
    from pydub import AudioSegment, silence
    audio = AudioSegment.from_file(video_path)
    nonsilent = silence.detect_nonsilent(
        audio, min_silence_len=min_silence_ms, silence_thresh=silence_thresh_db
    )
    segs = []
    for a, b in nonsilent:
        a = max(0, a - keep_pad_ms); b = min(len(audio), b + keep_pad_ms)
        segs.append((a / 1000.0, b / 1000.0))
    return segs


def add_video_with_silence_removal(draft_id, video_path):
    """Adiciona o vídeo já cortado nos silêncios (chame no lugar do add_video do passo 3)."""
    segs = build_speech_segments(video_path)
    timeline = 0.0
    for (s, e) in segs:
        dur = e - s
        api("add_video", {
            "draft_id": draft_id,
            "video_url": video_path,
            "start": s, "end": e,          # trecho do material
            "target_start": timeline,      # onde entra na timeline final
            "width": WIDTH, "height": HEIGHT,
            "track_name": "video_main",
            "volume": 1.0,
        })
        timeline += dur
    print(f"[silence] {len(segs)} trechos de fala adicionados (silêncios removidos)")
    return timeline


if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("ERRO: não consegui falar com a API. O servidor está rodando?")
        print("      cd C:\\Users\\moret\\VectCutAPI && venv-capcut\\Scripts\\activate && python capcut_server.py")
        sys.exit(1)
    except Exception as e:
        print("ERRO:", e)
        sys.exit(1)
