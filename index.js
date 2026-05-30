// ============================================================================
//  Wpp-PsychoTeam  —  Robô de atendimento automático do WhatsApp
//
//  O que ele faz:
//   1. Conecta ao seu WhatsApp via QR Code (uma vez só).
//   2. Fica "ouvindo" as mensagens que chegam.
//   3. Quando alguém manda uma mensagem perguntando sobre a consultoria
//      (detectado pelas palavras-chave do config.js), ele responde com uma
//      saudação educada de acordo com o horário ("oi, bom dia, tudo bem?")
//      e envia os 2 PDFs da pasta /pdfs.
//
//  Para iniciar:  npm start
// ============================================================================

const fs = require("fs");
const path = require("path");
const qrcode = require("qrcode-terminal");
const { Client, LocalAuth, MessageMedia } = require("whatsapp-web.js");

const config = require("./config");

// --- Memória de quem já foi respondido (para o anti-spam) -------------------
const ARQUIVO_MEMORIA = path.join(__dirname, "respondidos.json");

function carregarMemoria() {
  try {
    return JSON.parse(fs.readFileSync(ARQUIVO_MEMORIA, "utf8"));
  } catch {
    return {};
  }
}

function salvarMemoria(memoria) {
  try {
    fs.writeFileSync(ARQUIVO_MEMORIA, JSON.stringify(memoria, null, 2));
  } catch (e) {
    console.error("⚠️  Não consegui salvar a memória anti-spam:", e.message);
  }
}

let respondidos = carregarMemoria();

// --- Funções auxiliares -----------------------------------------------------

// Remove acentos e deixa minúsculo, para comparar palavras-chave sem erro.
function normalizar(texto) {
  return (texto || "")
    .toLowerCase()
    .normalize("NFD")
    .replace(/[̀-ͯ]/g, "");
}

// Decide "bom dia" / "boa tarde" / "boa noite" pelo horário atual.
function saudacaoDoHorario() {
  const hora = new Date().getHours();
  const { bomDia, boaTarde } = config.faixasHorario;
  if (hora >= bomDia.inicio && hora <= bomDia.fim) return "bom dia";
  if (hora >= boaTarde.inicio && hora <= boaTarde.fim) return "boa tarde";
  return "boa noite";
}

// Verifica se a mensagem contém alguma das palavras-chave.
function mensagemPedeInfo(texto) {
  const t = normalizar(texto);
  return config.palavrasChave.some((p) => t.includes(normalizar(p)));
}

// Verifica se já respondemos essa pessoa dentro do período anti-spam.
function jaRespondidoRecentemente(idContato) {
  if (config.horasEntreRespostas <= 0) return false;
  const ultima = respondidos[idContato];
  if (!ultima) return false;
  const horasPassadas = (Date.now() - ultima) / (1000 * 60 * 60);
  return horasPassadas < config.horasEntreRespostas;
}

// Carrega os PDFs da pasta configurada.
function carregarPdfs() {
  const pasta = path.resolve(__dirname, config.pastaPdfs);
  if (!fs.existsSync(pasta)) {
    console.error(`⚠️  A pasta de PDFs não existe: ${pasta}`);
    return [];
  }
  return fs
    .readdirSync(pasta)
    .filter((nome) => nome.toLowerCase().endsWith(".pdf"))
    .sort()
    .map((nome) => path.join(pasta, nome));
}

// --- Cliente do WhatsApp ----------------------------------------------------
const client = new Client({
  authStrategy: new LocalAuth(), // salva a sessão para não pedir QR toda hora
  puppeteer: {
    headless: true,
    args: ["--no-sandbox", "--disable-setuid-sandbox"],
  },
});

client.on("qr", (qr) => {
  console.log("\n📱 Escaneie o QR Code abaixo com o WhatsApp do seu celular:");
  console.log("   (WhatsApp > Aparelhos conectados > Conectar um aparelho)\n");
  qrcode.generate(qr, { small: true });
});

client.on("authenticated", () => {
  console.log("✅ Autenticado com sucesso!");
});

client.on("ready", () => {
  const pdfs = carregarPdfs();
  console.log("\n🤖 Robô conectado e funcionando!");
  console.log(`📄 PDFs encontrados na pasta: ${pdfs.length}`);
  pdfs.forEach((p) => console.log(`   - ${path.basename(p)}`));
  if (pdfs.length === 0) {
    console.log(
      "⚠️  ATENÇÃO: nenhum PDF na pasta /pdfs. Coloque seus arquivos lá!"
    );
  }
  console.log("\n⏳ Aguardando mensagens...\n");
});

client.on("message", async (mensagem) => {
  try {
    // Ignora mensagens de status/transmissão
    if (mensagem.from === "status@broadcast") return;

    // Ignora grupos, se configurado
    const ehGrupo = mensagem.from.endsWith("@g.us");
    if (ehGrupo && !config.responderEmGrupos) return;

    // A mensagem pede informações sobre a consultoria?
    if (!mensagemPedeInfo(mensagem.body)) return;

    // Anti-spam: já respondemos essa pessoa há pouco tempo?
    if (jaRespondidoRecentemente(mensagem.from)) {
      console.log(`⏭️  Ignorado (anti-spam): ${mensagem.from}`);
      return;
    }

    console.log(`💬 Pedido de info recebido de: ${mensagem.from}`);

    // 1) Saudação educada conforme o horário
    const saudacao = config.mensagemSaudacao.replace(
      "{saudacao}",
      saudacaoDoHorario()
    );
    await client.sendMessage(mensagem.from, saudacao);

    // 2) Mensagem de apresentação
    if (config.mensagemApresentacao) {
      await client.sendMessage(mensagem.from, config.mensagemApresentacao);
    }

    // 3) Envia os PDFs
    const pdfs = carregarPdfs();
    for (const caminhoPdf of pdfs) {
      const media = MessageMedia.fromFilePath(caminhoPdf);
      await client.sendMessage(mensagem.from, media);
      console.log(`   📎 Enviado: ${path.basename(caminhoPdf)}`);
    }

    // Marca como respondido (anti-spam)
    respondidos[mensagem.from] = Date.now();
    salvarMemoria(respondidos);

    console.log(`✅ Resposta completa enviada para: ${mensagem.from}\n`);
  } catch (erro) {
    console.error("❌ Erro ao processar mensagem:", erro.message);
  }
});

client.on("disconnected", (motivo) => {
  console.log("🔌 Desconectado do WhatsApp:", motivo);
});

console.log("🚀 Iniciando o robô... (pode demorar alguns segundos)");
client.initialize();
