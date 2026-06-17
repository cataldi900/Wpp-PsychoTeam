---
tags: [psychoteam, base-de-dados, evidencia, loom, pr]
criado: 2026-06-17
fonte: vault local do Guilherme (planos .md + export Loom)
---

# 🗃️ Base de Dados — PsychoTeam

Dados reais da consultoria, usados como **evidência empírica** para validar e
refinar os [[00 - Índice dos Padrões|padrões de progressão]]. Não é teoria: é o
que de fato aconteceu com os alunos ao longo de ~3 anos.

## Arquivos

| Arquivo | O que é |
|---|---|
| [[Timeline-Forca-por-Aluno]] | Curva de PR (Squat/Bench/Dead) no tempo, por aluno. 59 alunos · 6050 planos · 2023→2026. |
| [[Dossie-Alunos (PR + Loom)]] | PR **+** feedbacks do Loom na **mesma linha do tempo**, por aluno. |
| [[Feedbacks-Loom-por-Aluno]] | Todos os feedbacks do Loom agrupados por aluno (nº e títulos). |
| `loom_meta.json` | Metadados crus dos 849 vídeos do Loom (id, título, data). |

## Cobertura

- **59 alunos** com curva de PR documentada (linhas `PR:` dos planos)
- **849 vídeos** de Loom (08/2025 → 06/2026)
- Janela total dos planos: **2023-04-14 → 2026-06-02**

## Limitações conhecidas

- Os arquivos trazem **títulos e datas** dos Looms, não a transcrição verbatim do
  áudio. O conteúdo falado é inferido pelo título + contexto da curva de PR.
- PRs só aparecem onde o plano trazia a linha `PR:` (nem todo plano traz).
- Quando **não há Loom nem protocolo** numa data, normalmente é porque a
  progressão era simples ou não houve tempo de comentar (regra do Guilherme).

> Síntese analítica desta base: [[14 - Base de Evidências (59 Alunos · 849 Looms)]]
