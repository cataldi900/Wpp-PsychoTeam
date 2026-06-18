// ============================================================================
//  Wpp-PsychoTeam — Assistente de WhatsApp
//
//  Recurso A (LIGADO):  Relatório diário priorizado do que responder.
//  Recurso B (DESLIGADO): Auto-resposta da consultoria com 2 PDFs.
//  Ligue/desligue cada um no arquivo config.js.
//
//  Iniciar normal:        npm start
//  Gerar relatório agora:  npm run relatorio   (útil para testar)
// ============================================================================

const fs = require("fs");
const path = require("path");
const qrcode = require("qrcode-terminal");
const { Client, LocalAuth, MessageMedia } = require("whatsapp-web.js");

const config = require("./config");
const { normalizar, saudacaoDoHorario } = require("./lib/util");
const { coletarConversas, montarRelatorio } = require("./lib/relatorio");

const GERAR_AGORA = process.argv.includes("--agora");

// ============================================================================
//  Cliente do WhatsApp
// ============================================================================
const client = new Client({
  authStrategy: new LocalAuth(),
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

client.on("authenticated", () => console.log("✅ Autenticado com sucesso!"));

client.on("ready", async () => {
  console.log("\n🤖 Assistente conectado!");

  if (config.relatorio.ativo) {
    console.log(
      `📋 Relatório diário LIGADO — horários: ${config.relatorio.horarios.join(", ")}`
    );
    iniciarAgendador();
  }
  if (config.autoResposta.ativo) {
    console.log("🤝 Auto-resposta da consultoria LIGADA.");
  }

  if (GERAR_AGORA) {
    console.log("\n⚡ Gerando um relatório agora (modo teste)...\n");
    await gerarRelatorio();
    console.log("\nPronto. Encerrando.");
    process.exit(0);
  }

  console.log("\n⏳ Rodando. Deixe esta janela aberta.\n");
});

client.on("disconnected", (motivo) =>
  console.log("🔌 Desconectado do WhatsApp:", motivo)
);

// ============================================================================
//  RECURSO A — Relatório diário
// ============================================================================

async function gerarRelatorio() {
  try {
    const conversas = await coletarConversas(client, config.relatorio);
    const texto = montarRelatorio(conversas);

    // Mostra no terminal
    console.log("\n----------------------------------------");
    console.log(texto);
    console.log("----------------------------------------\n");

    // Envia para você mesmo no WhatsApp
    if (config.relatorio.enviarParaMim && client.info && client.info.wid) {
      await client.sendMessage(client.info.wid._serialized, texto);
      console.log("📤 Relatório enviado para a sua conversa 'Você'.");
    }

    // Salva em arquivo
    if (config.relatorio.salvarArquivo) {
      const pasta = path.join(__dirname, "relatorios");
      fs.mkdirSync(pasta, { recursive: true });
      const nome = `relatorio-${new Date()
        .toISOString()
        .slice(0, 16)
        .replace(/[:T]/g, "-")}.txt`;
      fs.writeFileSync(path.join(pasta, nome), texto);
      console.log(`💾 Salvo em relatorios/${nome}`);
    }
  } catch (e) {
    console.error("❌ Erro ao gerar relatório:", e.message);
  }
}

// Agendador simples: a cada minuto, vê se a hora atual bate com algum horário.
function iniciarAgendador() {
  let ultimoDisparo = "";
  setInterval(() => {
    const agora = new Date();
    const hhmm = `${String(agora.getHours()).padStart(2, "0")}:${String(
      agora.getMinutes()
    ).padStart(2, "0")}`;
    if (config.relatorio.horarios.includes(hhmm) && ultimoDisparo !== hhmm) {
      ultimoDisparo = hhmm;
      console.log(`\n⏰ ${hhmm} — gerando relatório agendado...`);
      gerarRelatorio();
    }
  }, 60 * 1000);
}

// ============================================================================
//  RECURSO B — Auto-resposta da consultoria (opcional)
// ============================================================================

function carregarPdfs() {
  const pasta = path.resolve(__dirname, config.autoResposta.pastaPdfs);
  if (!fs.existsSync(pasta)) return [];
  return fs
    .readdirSync(pasta)
    .filter((n) => n.toLowerCase().endsWith(".pdf"))
    .sort()
    .map((n) => path.join(pasta, n));
}

const respondidosPath = path.join(__dirname, "respondidos.json");
let respondidos = {};
try {
  respondidos = JSON.parse(fs.readFileSync(respondidosPath, "utf8"));
} catch {
  respondidos = {};
}

function pedeInfo(texto) {
  const t = normalizar(texto);
  return config.autoResposta.palavrasChave.some((p) => t.includes(normalizar(p)));
}

function respondidoRecentemente(id) {
  const h = config.autoResposta.horasEntreRespostas;
  if (h <= 0) return false;
  const ultima = respondidos[id];
  return ultima && (Date.now() - ultima) / 3600000 < h;
}

client.on("message", async (msg) => {
  if (!config.autoResposta.ativo) return;
  try {
    if (msg.from === "status@broadcast") return;
    if (msg.from.endsWith("@g.us") && !config.geral.responderEmGrupos) return;
    if (!pedeInfo(msg.body)) return;
    if (respondidoRecentemente(msg.from)) return;

    const saudacao = config.autoResposta.mensagemSaudacao.replace(
      "{saudacao}",
      saudacaoDoHorario(config.geral.faixasHorario)
    );
    await client.sendMessage(msg.from, saudacao);
    if (config.autoResposta.mensagemApresentacao) {
      await client.sendMessage(msg.from, config.autoResposta.mensagemApresentacao);
    }
    for (const pdf of carregarPdfs()) {
      await client.sendMessage(msg.from, MessageMedia.fromFilePath(pdf));
    }
    respondidos[msg.from] = Date.now();
    fs.writeFileSync(respondidosPath, JSON.stringify(respondidos, null, 2));
    console.log(`✅ Auto-resposta enviada para: ${msg.from}`);
  } catch (e) {
    console.error("❌ Erro na auto-resposta:", e.message);
  }
});

// ============================================================================
console.log("🚀 Iniciando o assistente... (pode demorar alguns segundos)");
client.initialize();
