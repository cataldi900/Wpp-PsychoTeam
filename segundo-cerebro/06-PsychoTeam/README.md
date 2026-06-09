---
tipo: indice
tags: [psychoteam]
---

# 💬 06 — PsychoTeam

Operação de atendimento: receber clientes novos pelo WhatsApp, enviar saudações
e PDFs, e registrar o acompanhamento. Conecta o segundo cérebro ao trabalho real
descrito no `CLAUDE.md` da raiz ("Responder clientes novos com PDF e mensagens
de saudações").

## Subpastas
- 👥 [[Clientes]] — uma nota por cliente. Template: [[Templates/Template-Cliente]].
- 💬 **Modelos-Saudacao** — mensagens prontas. Ex.: [[Saudacao-Padrao]].
- 📋 **Protocolos** — passo a passo do atendimento. Ex.: [[Onboarding-Cliente-Novo]], [[Privacidade-e-LGPD]].
- 📎 **PDFs** — materiais enviados aos clientes (e notas sobre eles).

## Fluxo de cliente novo (resumo)
1. Cliente chega no WhatsApp → cria nota em `Clientes/` (template).
2. Envia [[Saudacao-Padrao]] + PDF de apresentação.
3. Registra o histórico na nota do cliente.
4. Segue [[Onboarding-Cliente-Novo]].

> ⚠️ Dados de clientes são sensíveis. Veja [[Privacidade-e-LGPD]] antes de
> registrar qualquer informação pessoal.
