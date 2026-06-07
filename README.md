# Wpp-PsychoTeam
Responder clientes novos com PDF e mensagens de saudações.

---

## 📋 Formulário de Indicação (`index.html`)

Formulário web onde os alunos da consultoria indicam até **3 pessoas** (nome +
WhatsApp). As respostas ficam salvas para sempre numa **Planilha Google sua** —
nada é perdido e você vê tudo em um só lugar.

### Regras de desconto exibidas no formulário
- **Indicado que fechar:** R$ 50 nos planos **mensais** e R$ 100 nos **trimestrais**.
- **Quem indicou:** R$ 50 de desconto a **cada** indicação que fechar.

O formulário já mostra as regras e calcula em tempo real a estimativa de desconto
de quem está indicando.

---

## 🚀 Como colocar no ar (passo a passo, ~10 min)

Você só precisa de uma **conta Google**. Não precisa de servidor nem pagar nada.

### 1) Crie a Planilha + o robô que recebe os dados
1. Crie uma **Planilha Google** nova em <https://sheets.new>.
2. No menu da planilha, vá em **Extensões → Apps Script**.
3. Apague o código que aparecer e **cole todo o conteúdo** do arquivo
   [`apps-script/Codigo.gs`](apps-script/Codigo.gs).
4. Clique em **Salvar** (ícone do disquete).
5. Clique em **Implantar → Nova implantação**.
   - Em **"Selecionar tipo"** (engrenagem) escolha **App da Web**.
   - **Executar como:** *Eu mesmo*.
   - **Quem pode acessar:** *Qualquer pessoa*.
   - Clique em **Implantar** e **autorize** o acesso (é a sua própria conta).
6. Copie a **URL do app da Web** que aparecer (algo como
   `https://script.google.com/macros/s/AKfyc.../exec`).

### 2) Conecte o formulário à planilha
1. Abra o arquivo [`index.html`](index.html).
2. No início do `<script>`, troque:
   ```js
   const ENDPOINT = "COLE_AQUI_A_URL_DO_APPS_SCRIPT";
   ```
   pela URL que você copiou no passo anterior.
3. Salve.

### 3) Publique o formulário (escolha uma opção)
- **GitHub Pages:** ative em *Settings → Pages* do repositório e use o link gerado.
- **Netlify / Vercel:** arraste o `index.html` ou conecte o repositório.
- **Google Sites:** incorpore o `index.html`.
- **Direto:** você pode até enviar o arquivo `index.html` e abrir no navegador
  (mas para o aluno enviar de qualquer lugar, hospede em um dos serviços acima).

Pronto! Cada envio vira **uma linha por indicado** na aba **"Indicações"** da sua planilha.

---

## ✅ Marcando quem fechou (e calculando descontos)

Na planilha, a coluna **Status** começa como `Aguardando`. Quando uma indicação
fechar plano:
1. Troque o **Status** daquela linha para **`Fechou`**.
2. No menu da planilha, clique em **Indicações → Recalcular descontos**.

O sistema preenche automaticamente:
- **Desconto indicado:** R$ 50 (mensal) ou R$ 100 (trimestral).
- **Desconto p/ quem indicou:** R$ 50 por fechamento.

Assim você acompanha facilmente quanto cada aluno acumulou de desconto.

---

## 🔧 Personalização rápida
No `index.html` você pode mudar:
- `NUM_INDICADOS` — quantidade de indicações (padrão 3).
- `DESC_INDICADOR_POR_FECHAMENTO` — quanto quem indica ganha por fechamento.
- `PLANOS` — valores de desconto por tipo de plano.

(Se mudar os valores aqui, ajuste também as constantes no `apps-script/Codigo.gs`.)

---

## Skill: video-use
Veja instruções em [`CLAUDE.md`](CLAUDE.md).
