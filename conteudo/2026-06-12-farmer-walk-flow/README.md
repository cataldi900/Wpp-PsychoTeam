# take 00 — Farmer Walk (Reels/Shorts/TikTok) · fluxo gemini-omni

- **Vídeo fonte:** pasta Drive "Farmer walk" → `IMG_7946.mov`, `IMG_7950.mov`, `IMG_7956.mov` (+ `copy_…AAF.mov`)
- **Formato:** VERTICAL **9:16** (gravado 2160×3840) → saída alvo **1080×1920**
- **Duração total:** TODO (definir após transcrição)
- **Takes:** 4 clips, cortados em fim de frase / na pausa
- **Estilo de motion:** **Apple-clean** — *frosted glass, SF Pro, easing leve, asterisco laranja como acento; credibilidade premium institucional* (exatamente o estilo descrito nos prints do fluxo gemini-omni)
- **Status:** SCAFFOLD. Falas e ranges marcados `TODO` — preencher quando os vídeos chegarem e a transcrição (Whisper) rodar.

> ⚠️ Este é o esqueleto montado **sem o footage** (os .mov de 50 MB não passaram pelo conector do Drive nem pela rede do ambiente). Os prompts já estão pasteáveis no Google Flow; ranges e falas exatas entram depois.

## Tabela de takes (proposta — refinar com a transcrição)

| # | Range | Layout | Tema |
|---|-------|--------|------|
| 01 | 0:00–0:0X | Motion-only | HOOK — keyword gigante "FARMER WALK" / parar o scroll |
| 02 | 0:0X–0:XX | Overlay | BENEFÍCIOS nas laterais (PEGADA · CORE · POSTURA · CARDIO) |
| 03 | 0:XX–0:XX | Overlay | ERRO riscado + ✓ CERTO — cues de técnica |
| 04 | 0:XX–0:XX | Motion-only | CTA "SALVA ESSE TREINO" + assinatura |

## Base visual unificada (atualizada)

- **Fundo de todos os takes:** parede branca minimalista com ar-condicionado split no alto — `frames/ac-background.png`. Anexar como **imagem de referência / primeiro frame** no Flow.
- **Hélice do ar girando** continuamente em todos os takes (no T4 ela desacelera junto com o "silêncio visual").
- **Talking head** (você) composto na frente dessa parede nos takes de corpo (T2/T3).
- **Montagem animada do farmer walk:** o footage real do exercício é costurado no ritmo da fala (subir como *ingrediente de vídeo* no Flow).
- **Apple-clean** mantido: frosted glass, SF Pro, easing leve, asterisco laranja como único acento.

> **Como o "Flow identifica as palavras" de fato funciona:** o Google Flow **não escuta o seu áudio**. Quem identifica as palavras é a **transcrição (Whisper, rodada aqui)** — ela gera os timestamps e o texto, que eu embuto nos prompts pra cada animação cair na palavra certa. O Flow então **gera o visual** a partir do prompt. Por isso ainda preciso dos vídeos (mesmo comprimidos) pra rodar o Whisper e travar a sincronia.

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

### Apple-clean — regras herdadas dos prints

- **Frosted glass mais opaco nos overlays (T2/T3)** pra garantir legibilidade do texto sobre o footage de alta resolução.
- **Acento de cor único = laranja** (asterisco/risco/check/linha). Todo o resto neutro: grafite + branco, SF Pro.
- **Easing leve** em tudo — movimento premium e contido, nunca snap agressivo.
- **T4 fecha com "silêncio visual"**: os elementos recuam e sobra só o asterisco laranja sumindo com fade ("silence before reset").
