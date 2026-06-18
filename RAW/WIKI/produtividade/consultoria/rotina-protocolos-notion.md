# Rotina — Cadastro de Protocolos de Alunos no Notion

> Capacidade fixa do segundo treinador (PsychoTeam). Dois caminhos para registrar
> um aluno no Notion. Sempre no **mesmo formato** das páginas `Aluno: ...` que já
> existem no workspace.

---

## Caminho 1 — COM PDF (transcrição fiel)

Quando o Guilherme manda o **PDF de um plano pronto**:

1. Ler o PDF integralmente.
2. Abrir uma página `Aluno: ...` existente no Notion como **referência de formato**
   (cores, toggles, tabelas, ordem das seções).
3. Transcrever **fiel** — sem reinterpretar conteúdo. Só estruturar no padrão Notion.
4. Criar a página `Aluno: [Nome]` no mesmo data source das demais.

Regra: no caminho 1 **não se gera nada novo** — só se transcreve o que está no PDF.

---

## Caminho 2 — COM ANAMNESE (gerar do zero)

Quando o Guilherme manda **só os dados do aluno** (sem PDF):

1. Conferir a anamnese. **O que faltar, perguntar** (campos abaixo).
2. **Ler os conceitos do método** antes de montar:
   - Canônico (vault local): `RAW/WIKI/conceitos/` (periodização, RPE, top set e
     back-off, progressão, deload, supino/agacho/terra, dieta e nutrição).
   - Espelho sincronizado (GitHub): `segundo-cerebro/06-PsychoTeam/Protocolos/Padroes-de-Progressao/`
     (notas 01–18, incl. verbatim e base de evidências).
3. **Derivar a paleta de alimentos** mais usada:
   - Canônico (vault local): `RAW/planos/`.
   - Espelho acessível: páginas `Aluno: ...` do Notion (mesmo conteúdo dos planos).
4. **Gerar o protocolo completo** (treino + dieta + fitoterápicos) no método.
5. **Mostrar o rascunho para o Guilherme aprovar.** ⚠️ NÃO criar no Notion antes da aprovação.
6. Após aprovação, criar a página `Aluno: [Nome]`.

### Dados da anamnese a coletar
- **Geral:** objetivo, nível e tempo de treino, dias disponíveis + horas/sessão, equipamento.
- **Força:** PRs (squat/bench/deadlift) **e em quantas reps** (define se é 1RM ou submáximo).
- **Saúde:** lesões/limitações (atenção redobrada a lesões de coluna/nervo), medicamentos, sono.
- **Dieta:** peso, altura, idade, sexo, direção do peso (cutting/manutenção/bulking),
  nº de refeições, preferências/alergias, restrições, condição financeira, suplementos.
- Se faltar qualquer item **que mude a prescrição** (sobretudo **peso** para a dieta), perguntar antes.

### Regra de substituição de alimentos
Sempre por alimento **já preparado (cozido)**, com **mesma caloria e macro aproximado**.

---

## Estrutura EXATA da página `Aluno: [Nome]`

Ordem das seções e formatação (Notion-flavored Markdown):

1. `# 🥗 Dieta {color="orange"}`
   - Callout com o **formato** da dieta (ex.: `> 🍃 **Dieta Linear**`; jejum se houver).
2. `## 🍽️ Refeições {color="orange"}`
   - Refeições numeradas: `### 🌅 1ª Refeição`, `### 🍱 2ª Refeição`, `### 🥗 3ª Refeição`, `### 🌙 4ª Refeição`.
   - Variações em toggle: `<details><summary>**Opção A (...)**</summary> ... </details>`.
   - "Carbo de fruta (55g)" em toggle com **tabela** de opções.
3. `## 📋 Diretrizes da Dieta {color="orange"}`
   - Callouts: `> 💧 Beber no mínimo **4L de água por dia**`, `> 🥦 ... 2 legumes`.
   - **Observações gerais** (lista): café preto antes das 18h, chá à vontade,
     refri zero evitar, vinagre de maçã p/ indigestão, pode juntar refeições,
     ordem é sugestão, folhas à vontade, avisar se custo alto / se não come algo.
4. `# Recursos Fitoterápicos e Manipulados {color="purple"}`
   - `### Nootrópicos` e `### Fitoterápicos` (cada item: nome + dose + função).
   - Callout da farmácia de manipulação (indicação Guilherme Moreti, sem parceria).
5. `# 🏋️ Sugestão de Treino — Nª semana {color="red"}`
   - `**PRs:**` + **tabela** (Exercício | Carga) + Obs sobre anotar cargas dos vídeos.
6. `## 💪 Treino A {color="orange"}` … B, C, D, E
   - Exercício em **negrito** (+ link de exemplo `([ex](url))` quando útil).
   - Séries em lista: `- 1x6 — RPE 5`, `- 1x3 — RPE 7`, `- 2x4 a 8 — RPE 8`.
   - Top set + back-off nos principais; observações em itálico `*(Gravar)*`.
7. `## 🏃 Cardio {color="red"}`
8. `# 📋 Diretrizes Gerais do Treino {color="purple"}`
   - `🎯 Objetivo desta fase`; subseções `{color="blue"}`: 📹 Sobre as gravações,
     ⚖️ Sobre o RPE e as cargas, ⏱️ Tempo de descanso, 💬 Feedback e dúvidas.

### Padrão de prescrição (séries)
- 1ª série = aquecimento (RPE 5–6), prepara o SNC.
- Acessórios: `1x6 RPE5 → 1x3 RPE7 → 2x(4 a 8) RPE8/10`.
- Principais: top set no RPE-alvo + back-off −10% (ver nota 18 verbatim).
- Carga = anilhas + barra (sempre contar a barra). "10kg-10kg" = por lado.

---

## Paleta de alimentos PsychoTeam (mais frequentes)

Derivada dos planos `Aluno: ...`. Usar como vocabulário padrão de prescrição.

- **Proteínas:** filé de frango (base), patinho + costela/acém/músculo (corte gordo
  3x/semana), ovos, whey, iogurte natural/kefir, queijo muçarela/prato, requeijão light.
- **Carboidratos:** arroz branco/parboilizado, macarrão (ou macarrão de arroz),
  pão de forma (fermentação natural), tapioca, aveia/floco de arroz, maizena,
  pão de hambúrguer (brioche), granola.
- **Carbo de fruta (55g):** melancia/melão (600–750g), banana (2un), manga (400g),
  abacaxi/mamão (400g), uva verde (300g), água de coco (600ml).
- **Gorduras:** azeite, castanha do Pará, coco ralado.
- **Fibra/digestão:** psyllium, biomassa de banana verde, crucíferos (brócolis,
  couve, couve-flor, couve de bruxelas, repolho), folhas à vontade, vinagre de maçã.

---

## Referências
- Método: `segundo-cerebro/06-PsychoTeam/Protocolos/Padroes-de-Progressao/` (notas 01–18)
- Voz/comunicação: nota 15 · Cues técnicos: nota 16 · Dieta: nota 17 · Núcleo verbatim: nota 18
- Onboarding: `segundo-cerebro/06-PsychoTeam/Protocolos/Onboarding-Cliente-Novo.md`
- Privacidade/LGPD: `segundo-cerebro/06-PsychoTeam/Protocolos/Privacidade-e-LGPD.md`
