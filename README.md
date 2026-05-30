# Wpp-PsychoTeam 🤖💜

Robô que **responde automaticamente** no seu WhatsApp quem entra em contato
perguntando sobre a **consultoria**. Ele manda uma saudação educada conforme o
horário (_"Oi, bom dia! Tudo bem?"_) e envia **2 PDFs** com as informações.

Funciona com o seu número normal do WhatsApp (igual ao WhatsApp Web) — **não
precisa de API paga**. Você conecta uma vez escaneando um QR Code e ele cuida
do resto sozinho.

---

## ⚙️ Como funciona

1. Alguém te manda uma mensagem como _"oi, gostaria de mais informações sobre a consultoria"_.
2. O robô detecta palavras-chave (consultoria, plano, valores, preço...).
3. Ele responde: **"Oi, bom dia! Tudo bem? 😊"** (a saudação muda com o horário).
4. Manda uma mensagem de apresentação + os **2 PDFs** da pasta `pdfs/`.
5. Anti-spam: não responde a mesma pessoa de novo nas próximas 12h (ajustável).

---

## 🚀 Passo a passo para usar

### 1. Instale o Node.js (só na primeira vez)
Baixe e instale em: https://nodejs.org (versão LTS).

### 2. Coloque seus 2 PDFs
Arraste seus arquivos para dentro da pasta **`pdfs/`**. Nomeie assim para
garantir a ordem de envio:
```
pdfs/1-apresentacao.pdf
pdfs/2-planos-e-valores.pdf
```

### 3. Instale o robô (só na primeira vez)
Abra o terminal **nesta pasta** e rode:
```bash
npm install
```

### 4. Ligue o robô
```bash
npm start
```
Vai aparecer um **QR Code** no terminal. No celular:
**WhatsApp → Aparelhos conectados → Conectar um aparelho** → aponte para o QR.

Pronto! Quando aparecer **"🤖 Robô conectado e funcionando!"**, ele já está
respondendo sozinho. Deixe o terminal aberto / o computador ligado para ele
continuar funcionando.

---

## ✏️ Como personalizar

Abra o arquivo **`config.js`** — está tudo comentado e fácil de editar:

| O que mudar | Onde |
|---|---|
| Palavras que ativam a resposta | `palavrasChave` |
| Texto da saudação | `mensagemSaudacao` |
| Texto que acompanha os PDFs | `mensagemApresentacao` |
| Tempo do anti-spam (em horas) | `horasEntreRespostas` (use `0` para responder sempre) |
| Responder em grupos ou não | `responderEmGrupos` |
| Faixas de horário do "bom dia/tarde/noite" | `faixasHorario` |

Para trocar os PDFs, é só substituir os arquivos na pasta `pdfs/`. Não precisa
reiniciar.

---

## ❓ Dúvidas comuns

- **Preciso deixar o computador ligado?** Sim. Enquanto o robô estiver rodando
  ele responde. Se fechar o terminal, ele para (é só rodar `npm start` de novo).
- **Vou ter que escanear o QR toda vez?** Não. A sessão fica salva; só pede o QR
  de novo se você desconectar o aparelho pelo celular.
- **Ele responde minhas conversas antigas?** Não. Só reage a mensagens **novas**
  que chegarem depois que ele estiver ligado e que contenham as palavras-chave.

---

## ⚠️ Importante / segurança

- A pasta `.wwebjs_auth/` guarda o acesso à sua conta — **nunca** compartilhe
  nem suba para o GitHub (já está no `.gitignore`).
- Use com bom senso e respeitando as regras do WhatsApp (não use para envio em
  massa / spam). Aqui ele só **responde** quem **te procurou primeiro**.
