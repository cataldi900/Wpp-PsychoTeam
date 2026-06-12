# take 00 — Farmer Walk (Reels/Shorts/TikTok) · fluxo gemini-omni

- **Vídeo fonte:** pasta Drive "Farmer walk" → `IMG_7946.mov`, `IMG_7950.mov`, `IMG_7956.mov` (+ `copy_…AAF.mov`)
- **Formato:** VERTICAL **9:16** (gravado 2160×3840) → saída alvo **1080×1920**
- **Duração total:** TODO (definir após transcrição)
- **Takes:** 4 clips, cortados em fim de frase / na pausa
- **Estilo de motion:** Híbrido energético (estrutura clean + tipografia UPPERCASE + acento laranja) — trocável por Apple-clean
- **Status:** SCAFFOLD. Falas e ranges marcados `TODO` — preencher quando os vídeos chegarem e a transcrição (Whisper) rodar.

> ⚠️ Este é o esqueleto montado **sem o footage** (os .mov de 50 MB não passaram pelo conector do Drive nem pela rede do ambiente). Os prompts já estão pasteáveis no Google Flow; ranges e falas exatas entram depois.

## Tabela de takes (proposta — refinar com a transcrição)

| # | Range | Layout | Tema |
|---|-------|--------|------|
| 01 | 0:00–0:0X | Motion-only | HOOK — keyword gigante "FARMER WALK" / parar o scroll |
| 02 | 0:0X–0:XX | Overlay | BENEFÍCIOS nas laterais (PEGADA · CORE · POSTURA · CARDIO) |
| 03 | 0:XX–0:XX | Overlay | ERRO riscado + ✓ CERTO — cues de técnica |
| 04 | 0:XX–0:XX | Motion-only | CTA "SALVA ESSE TREINO" + assinatura |

## Divisão de trabalho

1. **Aqui (skill):** transcrição Whisper → `splits.json` → corte dos takes → estes prompts → README.
2. **Você (Google Flow / créditos Gemini Pro):** gerar os takes animados a partir de `prompts/take-0X.md`.
3. **Aqui (montagem final):** juntar os clipes do Flow + seus takes reais em um reel 9:16 com transições e som.

## Calibrações 9:16 (≠ do exemplo 16:9)

- **Safe areas verticais:** topo **12%** (não cobrir com texto-chave), base **18–20%** (UI do TikTok/Reels: legenda + botões). Texto de CTA sempre ACIMA da base 18%.
- **Coluna sagrada:** terço central vertical, onde você/o haltere aparece — motion não invade.
- **Stack vertical:** hook no terço superior, keyword no centro, CTA no terço inferior (acima da safe zone).
- **Áudio:** passa byte-for-byte do original; nada de re-encode do áudio nos cortes (fades de 30 ms nas bordas).
- **Correções de transcrição:** termos técnicos ("farmer walk", "grip") conferidos manualmente antes de virar texto na tela.
