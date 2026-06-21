#!/usr/bin/env python3
"""
Extrai o texto de TODOS os PDFs de periodizacao para um unico JSONL compactado.

Por que: 20 mil PDFs nao devem ser movidos crus (varios GB, inviavel de ler um a
um). Este script roda na maquina do Guilherme (onde os PDFs estao, ex: Downloads),
extrai o texto de cada um e gera um unico arquivo .jsonl.gz pequeno (texto
comprime muito), que e o que sobe pro Google Drive.

Cada linha do JSONL e um PDF:
  {"i": ordem, "path": caminho relativo, "name": nome do arquivo,
   "chars": tamanho do texto, "dup": True se for duplicata de conteudo, "text": ...}

O "path" e o "name" carregam o nome do aluno e a ordem numerica (a sequencia da
periodizacao), entao a estrutura de pastas/nomes e preservada.

USO (Windows):
    pip install pdfplumber
    python extrair_periodizacoes.py "C:\\Users\\SEU_USUARIO\\Downloads\\PASTA_DAS_PERIODIZACOES" periodizacoes.jsonl.gz

USO (Mac/Linux):
    pip3 install pdfplumber
    python3 extrair_periodizacoes.py "/caminho/da/pasta" periodizacoes.jsonl.gz

Depois: suba o arquivo periodizacoes.jsonl.gz no seu Google Drive e me avise o nome.
"""
import sys
import os
import json
import gzip
import hashlib

try:
    import pdfplumber
except ImportError:
    sys.exit("Falta a biblioteca. Rode primeiro:  pip install pdfplumber")

root = sys.argv[1] if len(sys.argv) > 1 else "."
out = sys.argv[2] if len(sys.argv) > 2 else "periodizacoes.jsonl.gz"

pdfs = []
for dirpath, _, files in os.walk(root):
    for f in files:
        if f.lower().endswith(".pdf"):
            pdfs.append(os.path.join(dirpath, f))
pdfs.sort()
total = len(pdfs)
print(f"{total} PDFs encontrados em {root}\nExtraindo texto...")

seen = set()
n_ok = n_dup = n_err = n_empty = 0
with gzip.open(out, "wt", encoding="utf-8") as gz:
    for i, path in enumerate(pdfs, 1):
        rel = os.path.relpath(path, root).replace("\\", "/")
        text = ""
        try:
            parts = []
            with pdfplumber.open(path) as pdf:
                for page in pdf.pages:
                    parts.append(page.extract_text() or "")
            text = "\n".join(parts).strip()
        except Exception:
            n_err += 1
        if not text:
            n_empty += 1
        h = hashlib.md5(text.encode("utf-8")).hexdigest() if text else None
        dup = bool(h and h in seen)
        if h:
            seen.add(h)
        if dup:
            n_dup += 1
        elif text:
            n_ok += 1
        rec = {
            "i": i,
            "path": rel,
            "name": os.path.basename(path),
            "chars": len(text),
            "dup": dup,
            "text": text,
        }
        gz.write(json.dumps(rec, ensure_ascii=False) + "\n")
        if i % 500 == 0:
            print(f"  {i}/{total}...")

print(
    f"\nPronto -> {out}\n"
    f"  {n_ok} unicos com texto · {n_dup} duplicados · "
    f"{n_empty} vazios (sem camada de texto) · {n_err} com erro de leitura\n"
    f"Se 'vazios' for alto, os PDFs podem ser imagem/escaneados e precisariam de OCR."
)
