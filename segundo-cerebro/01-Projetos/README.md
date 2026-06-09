---
tipo: indice
---

# 🎯 01 — Projetos

Esforços com **objetivo claro e prazo definido** (têm linha de chegada).
Ex.: "Criar PDF de boas-vindas v2", "Configurar fluxo de saudação automática".

Use o template [[Templates/Template-Projeto]] para cada projeto novo.

## Projetos ativos
```dataview
LIST
FROM "segundo-cerebro/01-Projetos"
WHERE tipo = "projeto" AND status = "ativo"
```
> O bloco acima funciona se você instalar o plugin **Dataview**. Sem ele, basta
> listar os projetos manualmente abaixo.

-
