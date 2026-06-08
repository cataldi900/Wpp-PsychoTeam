#!/usr/bin/env python3
# Gera um PDF do roteiro de apresentação (formato vertical, leitura no celular),
# no padrão visual PsychoTeam. Uso: python3 slides/build-roteiro-pdf.py
import re, markdown, pathlib
from weasyprint import HTML

src = pathlib.Path(__file__).parent / "roteiro-apresentacao.md"
out = pathlib.Path(__file__).parent / "roteiro-apresentacao.pdf"
text = src.read_text(encoding="utf-8")

body = markdown.markdown(text, extensions=["tables", "sane_lists"])

# realça os marcadores de slide ("Slide N — Título.") dentro dos parágrafos em negrito
body = body.replace("<strong>Slide", '<strong class="slidemark">Slide')

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Anton&family=Inter:wght@400;500;600;700&family=Lora:ital@0;1&display=swap');
@page {
  size: A4; margin: 20mm 18mm 18mm;
  background: #0c0b08;
  @bottom-center { content: counter(page) " / " counter(pages); color:#5d574a; font-family:'Inter'; font-size:9px; letter-spacing:.2em; }
  @top-right { content: "PSYCHOTEAM · ENGENHARIA DO SUPINO"; color:#5d574a; font-family:'Inter'; font-size:8px; letter-spacing:.25em; }
}
* { box-sizing:border-box; }
html { background:#0c0b08; }
body { font-family:'Inter',sans-serif; color:#d9d3c4; font-size:11.5pt; line-height:1.6; }
h1 { font-family:'Anton'; font-weight:400; text-transform:uppercase; color:#ece6d8; font-size:30pt; line-height:1.02; letter-spacing:.5px; margin:0 0 4pt; }
h1 + p { color:#e6c463; font-family:'Lora'; font-style:italic; font-size:12pt; }
h2 { font-family:'Anton'; font-weight:400; text-transform:uppercase; color:#c8a24a; font-size:17pt; letter-spacing:.4px;
     margin:22pt 0 8pt; padding-bottom:5pt; border-bottom:1px solid #2a2519; }
h3 { font-family:'Anton'; font-weight:400; text-transform:uppercase; color:#b9b1a0; font-size:12pt; letter-spacing:.3px; margin:18pt 0 6pt; }
p { margin:0 0 9pt; }
strong { color:#ece6d8; font-weight:700; }
em { color:#cdbf9a; }
hr { border:0; border-top:1px solid #2a2519; margin:16pt 0; }
/* marcador do slide: vira um selo dourado */
.slidemark { display:inline-block; color:#15110a; background:linear-gradient(145deg,#e6c463,#b8862f);
  padding:2pt 8pt; border-radius:4pt; font-family:'Inter'; font-weight:700; font-size:9.5pt;
  text-transform:uppercase; letter-spacing:.04em; }
/* o parágrafo que contém o marcador (linha do slide) */
p > .slidemark:first-child { }
blockquote { margin:10pt 0; padding:9pt 14pt; background:rgba(255,255,255,.03);
  border-left:3px solid #c8a24a; color:#cdbf9a; font-family:'Lora'; font-style:italic; font-size:10.5pt; }
blockquote p { margin:0; }
ul { margin:0 0 9pt; padding-left:18pt; }
li { margin-bottom:4pt; }
em.vid, .vid { color:#c8a24a; }
/* a fala (parágrafo logo após a linha de marcador) ganha respiro de leitura */
"""

html = f"""<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8">
<style>{CSS}</style></head><body>{body}</body></html>"""

(pathlib.Path("/tmp/roteiro.html")).write_text(html, encoding="utf-8")
HTML(string=html).write_pdf(str(out))
print("PDF gerado:", out)
