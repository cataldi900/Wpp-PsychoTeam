# Rotina: Protocolos de aluno no Notion (autossuficiente)

> Playbook COMPLETO pra criar/atualizar o protocolo de um aluno no Notion. Tudo que precisa está aqui dentro (método, paleta de alimentos, formato, mecânica), então funciona mesmo sem acesso ao resto do cofre. Dois caminhos que terminam na MESMA estrutura: a partir de um PDF, ou a partir de uma anamnese.

## Regra de ouro
No caminho da anamnese (sem PDF), gere um rascunho e mostre pro Guilherme aprovar antes de finalizar no Notion. Com PDF, é transcrição fiel.

## Voz e travessão
Texto que o aluno lê: como áudio do Guilherme transcrito, sem cara de IA. Travessão: nunca na prosa. Exceção única: a notação das séries do treino usa "—" (ex: 1x6 — RPE 5).

---

## CAMINHO A — a partir de PDF (transcrever)
1. Ler o PDF (se não renderizar, extrair texto via Python: pdfplumber/pypdf → .txt).
2. Identificar o tipo (só dieta / só treino / completo) e extrair tudo.
3. Montar a página no formato da seção ESTRUTURA, fiel ao PDF.
4. Criar no Notion (seção MECÂNICA).

## CAMINHO B — a partir de anamnese (gerar do zero)

### B.1 Dados de entrada (perguntar ao Guilherme o que faltar)
- Treino: objetivo (powerlifting/powerbuilding/estética/força/emagrecer), nível e tempo de treino, dias disponíveis/semana + tempo por sessão, equipamento, PRs atuais, lesões/limitações, domínio dos lifts.
- Dieta: completo ou só treino; peso, altura, idade, sexo; direção do peso (ganhar/manter/perder); nº de refeições viável; preferências e alergias (ex: lactose); restrições (vegetariano etc.); condição financeira (monta conforme o bolso); suplementos.
- Saúde/rotina: exames, condições (diabetes etc.), ergogênicos/hormônios, ansiedade/sono/foco (decide fitoterápico), trabalho, sono, estresse.

### B.2 Método do Guilherme (gerar com base nisto)
Treino:
- Esporte de frequência: distribuir agacho/supino/terra em vários dias vale mais que socar tudo num dia.
- Fase inicial moderada: aprender o movimento, fortalecer pontos fracos, intensidade controlada.
- Top set + back-off: top set é a série mais pesada (referência); back-offs acumulam volume (tirar ~10% e manter o esforço, ou repetir a mesma carga como workset quando o corpo responde).
- RPE guia a carga: a 1ª série de cada exercício é aquecimento (RPE 5–6) e prepara o SN; a série principal vai num RPE mais alto; perto de 10 = perto da falha.
- Progressão pequena e constante (não pulo grande). Diminuir repetições abre espaço pra mais carga no mesmo esforço.
- Deload quando a fadiga pede (semana leve é onde o PR se constrói). Single controlado (RPE ~7) como termômetro de PR.
- Carga = anilhas + barra (sempre conta a barra). Marcar "Gravar" nos exercícios complexos.
- Split: definir A/B/C/D conforme os dias disponíveis, com SBD distribuído + acessórios pros pontos fracos. Cardio (média intensidade e/ou HIIT) conforme objetivo, sem tirar sono.
Dieta:
- Acompanha o treino: calorias sobem com a intensidade, caem no deload/cutting. Déficit forte atrapalha a recuperação.
- Linear (iniciante, mais aderência) ou ciclo de carbo (carbo alto nos dias de treino, baixo no descanso).
- Aderência medida toda semana (peso + foto + relato). Ajuste fino por refeição. Montar conforme o bolso.
- Estrutura: 3–4 refeições (+ intra-treino se aplicável), com opções em toggle onde precisa variar.

### B.3 Paleta de alimentos (os que o Guilherme MAIS usa, por frequência real)
- Proteínas: filé de frango, ovos, whey, patinho/músculo/acém/costela, coração de frango, atum, tilápia/peixe, iogurte natural, kefir, queijo muçarela/prato, leite (zero lactose), peito de peru.
- Carboidratos: arroz branco/parboilizado, macarrão de arroz (substituto), tapioca, aveia, maizena, pão de forma (fermentação natural), batata inglesa/doce/mandioca, pão de hambúrguer (brioche).
- Frutas: banana, abacaxi, mamão, melão, melancia, manga, uva, morango, água de coco.
- Gorduras: azeite, pasta de amendoim/amendoim, castanhas, abacate, coco/leite de coco/coco ralado, azeitona.
- Legumes/verduras: brócolis, couve-flor, couve, repolho, cenoura, abobrinha, chuchu, pepino, vagem, alface/tomate/cebola, folhas à vontade.

### B.4 Substituições de alimento
Sempre por alimento já preparado (cozido), com a mesma caloria e macro aproximado (base TACO). Trocar dentro da mesma família (carbo com carbo, proteína com proteína, gordura com gordura) mantém o macro perto.

---

## ESTRUTURA da página (igual pros dois caminhos)
Título: "Aluno: {Nome}". Página standalone (sem parent). Ordem:
- Completo: Dieta → Fitoterápicos → Treino → Diretrizes Gerais do Treino
- Só treino: começa em "# 🏋️ Sugestão de Treino"
- Só dieta: Dieta → Fitoterápicos → Diretrizes da Dieta

Dieta:
# 🥗 Dieta {color="orange"}
> 🍃 **Dieta Linear**
---
## 🍽️ Refeições {color="orange"}
### 🌅 1ª Refeição
- alimento
### 🍌 Qualquer horário do dia
- 55g carbo de frutas, opções (toggle com tabela)
### 🍱 2ª Refeição
- ...
### 🥗 3ª Refeição  (alternativas SEMPRE em toggle <details>, itens indentados por TAB)
<details>
<summary>**Opção A (...)**</summary>
	- alimento
</details>
### 🌙 4ª Refeição
- ...
### ⚡ Ref intra-treino  (só se aplicável)

Ciclo de carbo (quando for o caso) troca o cabeçalho por:
> 🍃 **Ciclo de Carbo — Dieta Linear**
> 📅 Carbo alto nos dias de treino · Carbo baixo nos dias de descanso
## 🔥 Carbo Alto — Dias de Treino {color="orange"}
## 🧊 Carbo Baixo — Dias de Descanso {color="blue"}

Fecha a dieta com:
## 📋 Diretrizes da Dieta {color="orange"}
> 💧 Beber no mínimo **4L de água por dia**
> 🥦 Que seu dia tenha pelo menos a variedade de **2 legumes**
> ⚠️ Durante essa primeira semana, tente **não fazer refeição livre**, assim teremos mais parâmetro para ajustes
**Observações gerais:**
- 🚽 Me informar no feedback se sua constância de defecar está em 1x por dia
- ☕ **Café preto:** somente antes das 18:00
- 🍵 Chá à vontade
- 🥤 Refri zero: evitar para não gerar compulsão
- 🤢 Indigestão: uma colher de vinagre de maçã na comida/salada ajuda
- Custo alto da dieta? Me avise
- 🔀 Pode juntar as refeições, o importante é comer tudo até o fim do dia
- ⏰ Não precisa comer de 3 em 3 horas, e sim realizar todas as refeições até o fim do dia
- 📅 A ordem das refeições é sugestão, se não encaixar me avise
- 🔄 Alimento que não come, me avise pra eu trocar (aderência vem antes)
- 🥬 Folhas à vontade
- **Usar a lista de substituição e variar ajuda a manter a dieta**

Fitoterápicos:
# Recursos Fitoterápicos e Manipulados {color="purple"}
### Nootrópicos
- **Nome Xmg** — posologia
	Efeito.
### Fitoterápicos
- 🌙 **Nome Xmg** — posologia
	Efeito.
> Farmácia de confiança: **(11)94565-4164 — WhatsApp** · falar que veio por indicação de **Guilherme Moreti**.
Se não houver: "- Não coloquei nada por não ver necessidade de acordo com a anamnese".

Treino:
# 🏋️ Sugestão de Treino — Xª semana {color="red"}
**PRs:** (tabela <table header-row="true"> com Exercício/Carga; só os que o aluno tem, resto "—")
Obs: Aqui vou anotar sua carga máxima a partir dos vídeos e cargas que me enviar.
---
## 💪 Treino A {color="orange"}
**Nome do exercício** *(observação se houver)* ([ex](link))
- 1x6 — RPE 5
- 1x3 — RPE 7
- 2x4 a 8 — RPE 8
---
(demais treinos B/C/D iguais, divisor "---" após cada um)
## 🏃 Cardio {color="red"}
**🚶 X dias na semana — Cardio de média intensidade** (Bicicleta, Caminhada ou Escada)
- Total: **Xmin por dia**
> 😴 Fazer cardio só se não precisar perder horas de sono.
> ☀️ Se expor à luz solar durante o cardio seria importante.
---
Regras das séries: nome do exercício em negrito em linha própria; séries logo abaixo em lista sem linha em branco; travessão "—" (nunca hífen); observação em itálico entre parênteses; link como ([ex](url)); divisor "---" após a tabela de PRs e após cada treino.

Diretrizes Gerais do Treino:
# 📋 Diretrizes Gerais do Treino {color="purple"}
> 🎯 **Objetivo desta fase:** aprender movimentos básicos, fortalecer regiões enfraquecidas e atingir a musculatura alvo com intensidade moderada.
## 📹 Sobre as gravações {color="blue"}
- É muito importante gravar os exercícios pra eu ver como você treina, suas limitações e cargas.
- Exercícios com "Gravar" pedem atenção pela complexidade. Grave 1 série com o celular apoiado.
- Posso te enviar um vídeo antes pra explicar. Pode gravar e perguntar sobre qualquer exercício.
## ⚖️ Sobre o RPE e as cargas {color="blue"}
- **RPE:** sua base pra se localizar na carga de cada exercício.
- A 1ª série de cada exercício é aquecimento (RPE 5 ou 6) e prepara o SN pra série principal.
- **A carga é a soma das anilhas + barra. Sempre conte a barra.** No formato "10kg-10kg", é por lado.
## ⏱️ Tempo de descanso {color="blue"}
- Multiarticulares: 3 a 5 min. Isolados: 2 a 3 min. Parâmetro, não regra: descanse o suficiente pra não baixar a carga.
## 📅 Organização da semana {color="blue"}
- [nº de treinos e descansos; preferir descanso em dias alternados]
## 💬 Feedback e dúvidas {color="blue"}
> 💬 Manda todas as dúvidas e faz tudo sem se lesionar. Pode perguntar pelo WhatsApp a hora que quiser!

Formatação Notion: cores {color="orange|red|purple|blue"}; toggles <details><summary>**...**</summary> com itens indentados por TAB; tabelas <table header-row="true"> com <tr>/<td> em linhas; não repetir o título no corpo.

---

## MECÂNICA
1. Criar a página: ferramenta notion-create-pages (MCP Notion), sem parent (standalone), properties.title = "Aluno: {Nome}", content = markdown acima.
2. Registrar: adicionar "{Nome}": "{page-id}", no dicionário ALUNOS do gerar_planos.py (projeto local periodizacao).
3. Gerar HTML (passo LOCAL): py gerar_planos.py "{Nome completo}" → sai em planos_gerados\{nome}.html. Roda na máquina local do Guilherme, não na nuvem.
4. Token do Notion: usar o configurado no ambiente.

## ENTREGA
Informar: nome do aluno, URL da página no Notion, caminho do HTML (se gerado localmente), e no caminho B confirmar que o Guilherme aprovou o rascunho.
