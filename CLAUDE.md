# Wpp-PsychoTeam

Responder clientes novos com PDF e mensagens de saudações.

## Capacidade fixa: cadastrar protocolos de alunos no Notion

Dois caminhos para registrar um aluno no Notion, sempre no formato das páginas
`Aluno: ...` já existentes. A rotina completa (campos da anamnese, estrutura exata
da página, mecânica, paleta de alimentos, regra de substituição) está em
**`RAW/WIKI/produtividade/consultoria/rotina-protocolos-notion.md`** — ler antes
de executar.

- **Com PDF:** transcrever fiel para o Notion (não reinterpretar).
- **Com anamnese (sem PDF):** gerar o protocolo do zero pelo método
  (`segundo-cerebro/06-PsychoTeam/Protocolos/Padroes-de-Progressao/` notas 01–18) e
  pela paleta de alimentos dos planos. **Mostrar o rascunho para aprovação antes de
  criar no Notion.** O que faltar na anamnese (sobretudo o **peso**), perguntar.

## Skill: video-use

The repository vendors the [video-use](https://github.com/browser-use/video-use)
skill (MIT) under `.claude/skills/video-use/`. It edits video by conversation
(transcribe, cut, color grade, subtitles, overlay animations).

**Before using any of its `helpers/` scripts, run the runtime setup** — the
skill files persist in git, but the runtime deps (ffmpeg + Python libs) do not
survive an ephemeral container:

```bash
bash .claude/skills/video-use/setup.sh
```

The script is idempotent (safe to re-run; it skips anything already installed),
so only run it when a video task actually comes up — there is no need to run it
for non-video work.

**ElevenLabs API key** (needed only for transcription): the most secure option
is to set `ELEVENLABS_API_KEY` as an environment variable in the Claude Code
environment settings. `setup.sh` will mirror it into a git-ignored `.env`
automatically. Never commit the key. Get one at
https://elevenlabs.io/app/settings/api-keys
