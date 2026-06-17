---
tags: [top-set, backoff, estrutura-sessao, progressao]
criado: 2026-06-17
---

# 02 — Top Set + Backoff

## Conceito

Cada sessão principal é estruturada em dois momentos:

1. **Top Set** — série mais pesada do dia, feita em RPE controlado. É o dado de progressão real.
2. **Backoff** — séries após o top set, com 10% menos de carga. Acumulam volume sem competir com a recuperação.

---

## Estrutura padrão

```
TOP SET:
  1x[reps] — RPE [alvo da semana]  ← gravar sempre

BACKOFF:
  Nx[reps] — [top set - 10%]
```

**Exemplo — Deadlift Sumo (semana 4 de acumulação):**
```
Top Set:  1x3 — 228kg — RPE 8,5   ← gravar
Backoff:  2x4 — 205kg             (≈10% abaixo)
```

**Exemplo — Bench Press (semana 1):**
```
Top Set:  1x1 — RPE 6,5   ← gravar e informar carga
Backoff:  5x5 — [carga -15%]   (primeira semana, margem maior)
```

---

## Variações de backoff por levantamento

| Levantamento | Backoff padrão | Obs |
|---|---|---|
| Agachamento | Carga fixa × séries | Manter carga, fazer séries diretas |
| Supino | Carga fixa × séries | Mesma lógica |
| Terra | Cascata descendente | Tirar 10% em cada série sequencial |

No terra a cascata funciona bem porque é o levantamento de maior custo sistêmico — reduzir progressivamente evita overshoot no volume.

---

## Por que o top set em RPE controlado (não máximo)

- Dados de progressão real só existem se o RPE é consistente semana a semana
- Um top set feito no RPE 8 na semana 1 e RPE 10 na semana 2 são incomparáveis
- O objetivo é que o mesmo peso saia com RPE menor nas semanas seguintes → esse é o sinal de progressão

**Indicador de progressão real:**
> Quando a carga do top set começa a sair 0,5 RPE mais fácil que na semana anterior, o bloco está funcionando.
> Quando 94-98% do 1RM começa a sair no RPE 6, o pico está próximo.

---

## Sem top set → sem dado

Se o aluno treina sem diferenciar top set de backoff (tudo saindo com o mesmo esforço), não há dado de progressão. É treino no escuro.

A gravação do top set é obrigatória porque:
1. Permite verificar qualidade técnica na carga mais alta
2. Registra a progressão visual ao longo das semanas
3. Permite recalibrar RPE quando o feedback verbal diverge do que aparece no vídeo

---

## Referência cruzada

- [[01 - Escala RPE e Estrutura da Sessão]]
- [[04 - Progressão de 0.5 RPE por Semana]]
- [[06 - Volume e Intensidade Nunca Sobem Juntos]]
