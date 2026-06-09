# 🧠 Segundo Cérebro — Wpp-PsychoTeam

Vault [Obsidian](https://obsidian.md) híbrido: combina o método **PARA** e
**Zettelkasten** para gestão de conhecimento com pastas específicas do fluxo de
atendimento do **PsychoTeam** (clientes novos via WhatsApp, saudações e PDFs).

## Como abrir

1. Instale o Obsidian: https://obsidian.md/download
2. `Abrir pasta como vault` → selecione a pasta **`segundo-cerebro/`** deste
   repositório.
3. O Obsidian já vem configurado (core plugins, notas diárias e templates) via
   a pasta `.obsidian/`.

> O vault é só markdown + uma pasta de config. Tudo é versionado no git, então
> dá para sincronizar pelo próprio repositório (ou por Obsidian Sync, se preferir).

## Estrutura

| Pasta | Para quê |
| ----- | -------- |
| `00-Inbox` | Captura rápida. Tudo entra aqui antes de ser processado. |
| `01-Projetos` | **P**ARA — esforços com objetivo e prazo definidos. |
| `02-Areas` | P**A**RA — responsabilidades contínuas (sem data de fim). |
| `03-Recursos` | PA**R**A — temas de interesse e material de referência. |
| `04-Arquivo` | PAR**A** — projetos/áreas inativos. |
| `05-Notas-Permanentes` | Zettelkasten — notas atômicas e interligadas. |
| `06-PsychoTeam` | Operação: clientes, saudações, protocolos, PDFs. |
| `Diario` | Notas diárias. |
| `Mapas` | MOCs (Maps of Content) — pontos de entrada do conhecimento. |
| `Templates` | Modelos para novas notas. |

Comece por [[Mapas/000 - Mapa Central]].

## Fluxo de trabalho sugerido

1. **Capture** qualquer ideia em `00-Inbox` (ou na nota diária).
2. **Processe** o inbox: vire nota permanente, anexe a um projeto/área, ou
   descarte.
3. **Conecte** com `[[wikilinks]]` — o valor está nas ligações, não nas pastas.
4. **Navegue** pelos MOCs em `Mapas/` e pelo grafo (ícone de grafo na lateral).

## Convenções

- Uma nota permanente = **uma ideia**, escrita com suas palavras.
- Use `[[wikilinks]]` generosamente para criar conexões.
- Tags em `tipo:` no frontmatter (`projeto`, `cliente`, `nota-permanente`, …).
- Dados sensíveis de clientes: siga [[06-PsychoTeam/Protocolos/Privacidade-e-LGPD]].
