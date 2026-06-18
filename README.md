# Wpp-PsychoTeam 🤖💜

Assistente que conecta no seu WhatsApp (igual ao WhatsApp Web, via QR Code) e
te ajuda a **organizar a demanda diária**. Tem dois recursos, que você liga ou
desliga no arquivo `config.js`:

| Recurso | O que faz | Padrão |
|---|---|---|
| 📋 **Relatório diário** | De manhã e à noite, te manda um **resumo priorizado** de quem está esperando resposta (🔴 urgente / 🟡 importante / 🟢 pode esperar). | **LIGADO** |
| 🤝 **Auto-resposta** | Responde sozinho quem pergunta da consultoria, com saudação + 2 PDFs. | Desligado |

> ⚠️ **Importante sobre acesso:** ninguém "de fora" (nem eu, uma IA) consegue
> ver as notificações do seu celular ou entrar na sua conta. Quem se conecta é
> **você**, escaneando o QR Code uma vez. O programa roda **no seu computador**.

---

## 📋 Como é o relatório

Nos horários que você definir (padrão **07:30** e **20:00**), o assistente varre
suas conversas e te manda — **no seu próprio WhatsApp** (conversa "Você") — algo
assim:

```
📋 Resumo do WhatsApp — sábado, 30/05, 07:30

Você tem 3 conversa(s) aguardando resposta:
🔴 1 urgente  •  🟡 1 importante  •  🟢 1 pode esperar

🔴 URGENTE — responder primeiro
• Maria S. (há 2h)
   "preciso muito falar, estou em crise..."
   ↳ ⚠️ palavras de urgência/crise, 4 mensagens não lidas

🟡 IMPORTANTE
• João P. (há 8h)
   "gostaria de remarcar minha sessão..."
   ↳ agenda/pagamento/dúvida, fez uma pergunta

🟢 Pode esperar
• Ana (há poucos minutos)
   "obrigada!!"
```

**Como ele decide a prioridade (modo local, 100% no seu PC):** palavras de
urgência/crise, temas de agenda/pagamento/dúvida, há quanto tempo a pessoa
espera, contatos novos (possível cliente) e quantidade de mensagens não lidas.
Nenhum conteúdo de paciente sai do seu computador.

---

## 🚀 Como usar

### 1. Instale o Node.js (uma vez)
Baixe a versão LTS em https://nodejs.org

### 2. Instale o assistente (uma vez)
Abra o terminal **nesta pasta** e rode:
```bash
npm install
```

### 3. Ligue
```bash
npm start
```
Aparece um **QR Code**. No celular: **WhatsApp → Aparelhos conectados →
Conectar um aparelho** → aponte para o QR. Quando aparecer
**"🤖 Assistente conectado!"**, está funcionando. Deixe a janela aberta.

### Testar o relatório na hora (sem esperar o horário)
```bash
npm run relatorio
```
Gera um relatório imediatamente e te envia, para você ver como fica.

---

## ✏️ Personalizar (`config.js`)

**Relatório (`relatorio`):**
- `horarios` — quando receber, ex.: `["07:30", "20:00"]`
- `janelaHoras` — olhar mensagens de quantas horas pra trás
- `horasParaSubirPrioridade` — a partir de quanto tempo sem resposta "sobe" a prioridade
- `palavrasUrgencia` / `palavrasImportantes` — as palavras que classificam
- `enviarParaMim` / `salvarArquivo` — onde entregar o relatório

**Auto-resposta (`autoResposta`):** mude `ativo: true` para ligar. Configure
`palavrasChave`, mensagens e a pasta dos PDFs (`pdfs/`).

---

## ⚠️ Privacidade e segurança

- A pasta `.wwebjs_auth/` dá acesso à sua conta — **nunca** compartilhe.
- A pasta `relatorios/` contém dados de pacientes — já está protegida no
  `.gitignore` para **não** ir pro GitHub.
- Tudo roda localmente no modo padrão. Nada é enviado para a internet.
- Precisa do computador ligado e da janela aberta para funcionar.
