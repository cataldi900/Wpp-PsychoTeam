#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
automate_capcut.py — 1 COMANDO faz tudo (VectCutAPI + CapCut, Windows)

Solte o vídeo em  C:\\Users\\moret\\VectCutAPI\\input\\  e rode:
    python automate_capcut.py
(se não houver vídeo local, baixa o IMG_7844.mov do Drive)

O script RECONHECE e aplica automaticamente:
  • detecção e REMOÇÃO de silêncios
  • melhor TRANSIÇÃO (auto-selecionada via /get_transition_types)
  • EFEITO de cena discreto (via /get_video_scene_effect_types)
  • TRILHA de expectativa que cresce até o final (gerada em Python puro)
  • SFX glitch/whoosh nos cortes
  • título no topo + legenda fundo laranja (re-sincronizada) + zoom por keyframe
  • save_draft + move automático pra pasta do CapCut

Requisitos :  pip install requests gdown
Recomendado:  pip install faster-whisper pydub   (legenda + corte de silêncio)
              ffmpeg no PATH
"""

import os, sys, math, wave, struct, random, shutil, subprocess
from collections import deque
import requests

# ============================== CONFIG ==============================
API_BASE      = "http://127.0.0.1:9001"
DRIVE_FILE_ID = "18ECBxthBbpCkidwUtSPRgEZp49Y1BQQe"   # fallback se não houver vídeo local

VECTCUT_DIR   = r"C:\Users\moret\VectCutAPI"
INPUT_DIR     = os.path.join(VECTCUT_DIR, "input")
CAPCUT_DRAFTS = r"C:\Users\moret\AppData\Local\CapCut\User Data\Projects\com.lveditor.draft"
DEFAULT_NAME  = "IMG_7844.mov"
WIDTH, HEIGHT = 1080, 1920

# título
TITLE_TEXT, TITLE_FONT = "ESFORÇO ≠ RESULTADO", "SourceHanSansCN_Bold"
TITLE_COLOR, TITLE_SIZE, TITLE_Y = "#FFFFFF", 15.0, 0.80
TITLE_START, TITLE_END = 0.0, 5.0
# legenda (fundo laranja)
SUB_FONT, SUB_COLOR, SUB_SIZE, SUB_BG, SUB_Y = "SourceHanSansCN_Regular", "#FFFFFF", 7.0, "#FF6600", -0.80
WHISPER_MODEL = "small"
# silêncios
REMOVE_SILENCES, SIL_THRESH_DB, MIN_SIL_MS, KEEP_PAD_MS = True, -35, 350, 120
# transição / efeito (auto-selecionados; ordem de preferência por substring)
APPLY_TRANSITIONS = True
TRANS_DURATION    = 0.2
TRANS_PREFER = ["dissolve", "叠化", "fade", "渐", "mix", "zoom", "拉", "pull", "blur", "模糊"]
APPLY_EFFECTS  = True
EFFECT_DURATION = 0.4
EFFECT_PREFER = ["shake", "抖", "glitch", "故障", "rgb", "信号", "light", "光", "blur", "虚化", "zoom", "缩放"]
# zoom
KEYWORDS = ["RECORDE","ESFORÇAM","ESFORÇO","MUSCULAÇÃO","NATAÇÃO","CORRIDA","CARGAS","DIRECIONAMENTO","EVOLUEM"]
AUTO_ZOOM_ON_KEYWORDS, ZOOM_FROM, ZOOM_TO = True, 1.0, 1.10
ZOOM_MOMENTS = []
# overlays  [{path,start,end,scale,x,y}]
IMAGE_OVERLAYS = []
# trilha de expectativa (gerada se MUSIC_PATH vazio)
MUSIC_PATH, MUSIC_VOLUME = "", 0.16
# SFX
SFX_TRANSITIONS, SFX_VOLUME = True, 0.33
MOVE_DRAFT = True
VIDEO_EXTS = (".mov", ".mp4", ".mkv", ".m4v", ".avi")
# ===================================================================


def api(endpoint, payload):
    r = requests.post(f"{API_BASE}/{endpoint}", json=payload, timeout=900)
    r.raise_for_status(); data = r.json()
    if isinstance(data, dict) and data.get("success") is False:
        raise RuntimeError(f"[{endpoint}] {data.get('error') or data}")
    return data.get("output", data) if isinstance(data, dict) else data


def get_types(endpoint):
    """GET de listas (transições/efeitos/fontes). Retorna lista de nomes."""
    try:
        r = requests.get(f"{API_BASE}/{endpoint}", timeout=30); r.raise_for_status()
        data = r.json()
        items = data.get("output", data) if isinstance(data, dict) else data
        return [(it.get("name") if isinstance(it, dict) else it) for it in items]
    except Exception as e:
        print(f"[types] {endpoint} indisponível ({e})"); return []


def pick(names, prefer):
    for p in prefer:
        for n in names:
            if n and p.lower() in str(n).lower():
                return n
    return names[0] if names else None


def safe(label, fn):
    """Executa um passo opcional; se falhar, avisa e segue (não derruba o draft)."""
    try:
        fn(); return True
    except Exception as e:
        msg = str(e)
        print(f"[aviso] '{label}' pulado: {msg[:180]}")
        return False


def get_draft_id(out):
    for k in ("draft_id", "draftId", "id"):
        if isinstance(out, dict) and out.get(k): return out[k]
        if isinstance(out, dict) and isinstance(out.get("output"), dict) and out["output"].get(k):
            return out["output"][k]
    raise RuntimeError(f"sem draft_id: {out}")


def ffprobe_duration(path):
    try:
        r = subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",path],
                           capture_output=True, text=True); return float(r.stdout.strip())
    except Exception: return None


# ---------- input: pega vídeo local mais recente, senão baixa do Drive ----------
def resolve_video():
    os.makedirs(INPUT_DIR, exist_ok=True)
    vids = [os.path.join(INPUT_DIR, f) for f in os.listdir(INPUT_DIR)
            if f.lower().endswith(VIDEO_EXTS)]
    if vids:
        v = max(vids, key=os.path.getmtime)
        print(f"[input] usando vídeo local: {v}"); return v
    out = os.path.join(INPUT_DIR, DEFAULT_NAME)
    try:
        import gdown
    except ImportError:
        subprocess.check_call([sys.executable,"-m","pip","install","gdown"]); import gdown
    print("[input] nenhum vídeo local — baixando do Drive...")
    gdown.download(id=DRIVE_FILE_ID, output=out, quiet=False)
    return out


# ---------- silêncios ----------
def speech_segments(video_path):
    from pydub import AudioSegment, silence
    audio = AudioSegment.from_file(video_path)
    parts = silence.detect_nonsilent(audio, min_silence_len=MIN_SIL_MS, silence_thresh=SIL_THRESH_DB)
    segs = [(max(0,a-KEEP_PAD_MS)/1000.0, min(len(audio),b+KEEP_PAD_MS)/1000.0) for a,b in parts]
    return segs or [(0.0, len(audio)/1000.0)]


def mapper_for(kept):
    starts=[]; acc=0.0
    for s,e in kept: starts.append(acc); acc+=(e-s)
    def m(t):
        for (s,e),st in zip(kept,starts):
            if s<=t<=e: return st+(t-s)
        for (s,e),st in zip(kept,starts):
            if t<s: return st
        return acc
    return m, acc


# ---------- transcrição / SRT ----------
def transcribe(video_path):
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        print("[asr] faster-whisper ausente — sem legenda/zoom auto."); return None
    print(f"[asr] transcrevendo ({WHISPER_MODEL})...")
    model = WhisperModel(WHISPER_MODEL, device="cpu", compute_type="int8")
    segs,_ = model.transcribe(video_path, language="pt", vad_filter=True)
    return [{"start":s.start,"end":s.end,"text":s.text.strip()} for s in segs]


def write_srt(segments, mapper, path):
    def f(t):
        h=int(t//3600); m=int(t%3600//60); s=t%60; return f"{h:02d}:{m:02d}:{s:06.3f}".replace(".",",")
    out=[]; i=1
    for s in segments:
        a,b=mapper(s["start"]),mapper(s["end"])
        if b-a<0.2: continue
        out.append(f"{i}\n{f(a)} --> {f(b)}\n{s['text']}\n"); i+=1
    open(path,"w",encoding="utf-8").write("\n".join(out)); return path


# ---------- áudio gerado (Python puro) ----------
def _wav(path, samples, sr=44100):
    with wave.open(path,"w") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes(b"".join(struct.pack("<h",int(max(-1,min(1,s))*32767)) for s in samples))

def gen_glitch(path, dur=0.18, sr=44100):
    n=int(sr*dur); _wav(path,[random.uniform(-1,1)*(1.0 if int((i/n)*90)%2==0 else 0.15)*math.exp(-(i/n)*9)*0.5 for i in range(n)],sr)

def gen_whoosh(path, dur=0.30, sr=44100):
    n=int(sr*dur); dq=deque(); acc=0.0; sm=[]; k=22
    for x in (random.uniform(-1,1) for _ in range(n)):
        dq.append(x); acc+=x
        if len(dq)>k: acc-=dq.popleft()
        sm.append(acc/len(dq))
    _wav(path,[s*(math.sin(math.pi*i/n)**1.5)*0.5 for i,s in enumerate(sm)],sr)

def gen_anticipation(path, dur, sr=44100):
    """Trilha de tensão que CRESCE até o final + impacto no fim."""
    n=int(sr*dur); out=[0.0]*n
    for i in range(n):
        t=i/sr; p=i/n; vol=0.16+0.55*(p**1.6)
        out[i]=(math.sin(2*math.pi*55*t)+0.5*math.sin(2*math.pi*82.5*t)+0.3*math.sin(2*math.pi*110*t))/1.8*vol
    tcur=0.0
    while tcur<dur-0.1:                       # pulso que acelera
        p=tcur/dur; base=int(tcur*sr)
        for j in range(int(sr*0.08)):
            idx=base+j
            if idx<n:
                te=j/sr; out[idx]+=math.sin(2*math.pi*70*te)*math.exp(-te*30)*(0.25+0.45*p)
        tcur+=0.75-0.46*p
    sw=max(0,int((dur-2.5)*sr))               # swell final
    for i in range(sw,n):
        out[i]+=random.uniform(-1,1)*0.16*((i-sw)/(n-sw+1))
    b0=int((dur-1.0)*sr)                       # boom no fim
    for j in range(int(sr*1.0)):
        idx=b0+j
        if 0<=idx<n:
            te=j/sr; out[idx]+=math.sin(2*math.pi*(45+30*math.exp(-te*20))*te)*math.exp(-te*3)*0.6
    mx=max(1e-6,max(abs(x) for x in out))
    _wav(path,[x/mx*0.85 for x in out],sr)


# ---------- API: vídeo + transição/efeito/zoom/sfx/overlay ----------
def add_video_segments(draft_id, path, kept, transition):
    timeline=0.0; cuts=[]
    for i,(s,e) in enumerate(kept):
        payload={"draft_id":draft_id,"video_url":path,"start":s,"end":e,"target_start":timeline,
                 "width":WIDTH,"height":HEIGHT,"track_name":"video_main","volume":1.0}
        if i>0 and transition:
            payload["transition"]=transition; payload["transition_duration"]=TRANS_DURATION
        api("add_video", payload)
        timeline+=(e-s); cuts.append(timeline)
    return cuts[:-1], timeline

def add_zoom(draft_id,t0,t1):
    api("add_video_keyframe",{"draft_id":draft_id,"track_name":"video_main",
        "property_types":["scale_x","scale_y","scale_x","scale_y"],
        "times":[t0,t0,t1,t1],"values":[str(ZOOM_FROM),str(ZOOM_FROM),str(ZOOM_TO),str(ZOOM_TO)]})

def add_effects_at(draft_id, cuts, effect):
    if not (APPLY_EFFECTS and effect and cuts): return
    for ct in cuts:
        try:
            api("add_effect",{"draft_id":draft_id,"effect_type":effect,"effect_category":"scene",
                "start":max(0,ct-EFFECT_DURATION/2),"end":ct+EFFECT_DURATION/2,
                "track_name":"effect_main","width":WIDTH,"height":HEIGHT})
        except Exception as e:
            print(f"[effect] pulando ({e})"); break

def add_sfx(draft_id, cuts):
    g=os.path.join(INPUT_DIR,"glitch.wav"); w=os.path.join(INPUT_DIR,"whoosh.wav")
    if not os.path.exists(g): gen_glitch(g)
    if not os.path.exists(w): gen_whoosh(w)
    for i,ct in enumerate(cuts):
        api("add_audio",{"draft_id":draft_id,"audio_url":(g if i%2==0 else w),
            "target_start":max(0,ct-0.06),"volume":SFX_VOLUME,"track_name":"sfx"})

def add_overlays(draft_id, ovs):
    for ov in ovs:
        if not os.path.exists(ov["path"]): print(f"[overlay] sem arquivo: {ov['path']}"); continue
        api("add_image",{"draft_id":draft_id,"image_url":ov["path"],"start":ov["start"],"end":ov["end"],
            "scale_x":ov.get("scale",1.0),"scale_y":ov.get("scale",1.0),
            "transform_x":ov.get("x",0.0),"transform_y":ov.get("y",0.0),
            "width":WIDTH,"height":HEIGHT,"track_name":"image_main"})

def move_to_capcut(draft_id):
    src=os.path.join(VECTCUT_DIR,draft_id); dst=os.path.join(CAPCUT_DRAFTS,draft_id)
    if os.path.isdir(dst): print(f"[move] já no CapCut"); return
    if not os.path.isdir(src): print(f"[move] {src} não existe (talvez já salvo no CapCut)"); return
    os.makedirs(CAPCUT_DRAFTS,exist_ok=True); shutil.move(src,dst); print(f"[move] -> {dst}")


def main():
    video = resolve_video()

    # reconhecer recursos disponíveis na API
    transition = pick(get_types("get_transition_types"), TRANS_PREFER) if APPLY_TRANSITIONS else None
    effect     = pick(get_types("get_video_scene_effect_types"), EFFECT_PREFER) if APPLY_EFFECTS else None
    fonts = get_types("get_font_types")
    title_font = pick(fonts, ["SourceHanSansCN_Bold","SourceHanSansTW_Bold","思源黑体","SourceHanSans","Bold"]) or TITLE_FONT
    sub_font   = pick(fonts, ["SourceHanSansCN_Regular","SourceHanSansCN_Medium","SourceHanSansCN_Normal","思源黑体","SourceHanSans"]) or SUB_FONT
    print(f"[auto] transição='{transition}' efeito='{effect}' fonte='{title_font}'/'{sub_font}'")

    out=api("create_draft",{"width":WIDTH,"height":HEIGHT}); draft_id=get_draft_id(out)
    print(f"[draft] {draft_id}")

    # vídeo + corte de silêncios + transições
    kept=None; cuts=[]
    if REMOVE_SILENCES:
        try: kept=speech_segments(video)
        except ImportError: print("[silence] pydub ausente -> vídeo inteiro")
    if kept:
        cuts,total=add_video_segments(draft_id,video,kept,transition)
        print(f"[ok] {len(kept)} trechos (silêncios removidos) | {total:.2f}s")
    else:
        api("add_video",{"draft_id":draft_id,"video_url":video,"width":WIDTH,"height":HEIGHT,
                         "track_name":"video_main","volume":1.0})
        dur=ffprobe_duration(video) or 0.0; kept=[(0.0,dur)]; total=dur
    mapper,total=mapper_for(kept)

    # título (não derruba o draft se a fonte/campo falhar)
    safe("título", lambda: api("add_text",{"draft_id":draft_id,"text":TITLE_TEXT,
        "start":TITLE_START,"end":TITLE_END,"font":title_font,"font_color":TITLE_COLOR,
        "font_size":TITLE_SIZE,"transform_x":0.0,"transform_y":TITLE_Y,"track_name":"title"}))

    # legenda + zoom por palavra-chave
    segments=transcribe(video)
    if segments:
        srt=write_srt(segments,mapper,os.path.join(INPUT_DIR,"legenda.srt"))
        safe("legenda", lambda: api("add_subtitle",{"draft_id":draft_id,"srt":srt,"font":sub_font,
            "font_size":SUB_SIZE,"font_color":SUB_COLOR,"transform_x":0.0,"transform_y":SUB_Y,
            "background_color":SUB_BG,"background_alpha":1.0,"background_style":1,"track_name":"subtitle"}))

    zwin=list(ZOOM_MOMENTS)
    if AUTO_ZOOM_ON_KEYWORDS and segments:
        for s in segments:
            if any(kw in s["text"].upper() for kw in KEYWORDS):
                a,b=mapper(s["start"]),mapper(s["end"])
                if b-a>=0.4: zwin.append((a,b))
    if zwin: safe("zoom", lambda: [add_zoom(draft_id,a,b) for a,b in zwin])

    # efeitos + SFX + overlays
    safe("efeitos", lambda: add_effects_at(draft_id,cuts,effect))
    if SFX_TRANSITIONS and cuts: safe("sfx", lambda: add_sfx(draft_id,cuts))
    safe("overlays", lambda: add_overlays(draft_id,IMAGE_OVERLAYS))

    # trilha de expectativa
    music=MUSIC_PATH
    if not music:
        music=os.path.join(INPUT_DIR,"trilha_expectativa.wav")
        print("[music] gerando trilha de expectativa..."); gen_anticipation(music,total)
    if os.path.exists(music):
        safe("trilha", lambda: api("add_audio",{"draft_id":draft_id,"audio_url":music,
            "volume":MUSIC_VOLUME,"track_name":"music"}))

    # salvar + mover
    print(f"[save] {api('save_draft',{'draft_id':draft_id,'draft_folder':CAPCUT_DRAFTS})}")
    if MOVE_DRAFT: move_to_capcut(draft_id)
    print(f"\n✅ PRONTO. draft_id={draft_id} | {total:.2f}s — abra o CapCut.")


if __name__=="__main__":
    try: main()
    except requests.exceptions.ConnectionError:
        print("ERRO: API offline? Rode: python capcut_server.py (porta 9001)"); sys.exit(1)
    except Exception as e:
        print("ERRO:", e); sys.exit(1)
