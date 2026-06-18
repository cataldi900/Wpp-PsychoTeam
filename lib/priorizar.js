// ============================================================================
//  Priorização LOCAL (sem internet) — decide o que é mais importante responder.
//  Tudo roda no seu computador; nenhum conteúdo de paciente sai daqui.
// ============================================================================

const { normalizar } = require("./util");

// Recebe os "dados" de uma conversa e devolve { nivel, pontos, motivos }.
//   dados = {
//     texto: string (mensagens recebidas, juntas),
//     horasEsperando: number,
//     naoLidas: number,
//     contatoSalvo: boolean,   // false = número desconhecido (possível novo cliente)
//   }
function pontuarConversa(dados, cfg) {
  let pontos = 0;
  const motivos = [];

  const texto = normalizar(dados.texto);
  const contem = (lista) =>
    lista.some((p) => texto.includes(normalizar(p)));

  // 1) Urgência (peso máximo — no seu ramo, crise vem sempre primeiro)
  if (contem(cfg.palavrasUrgencia)) {
    pontos += 9;
    motivos.push("⚠️ palavras de urgência/crise");
  }

  // 2) Temas importantes: agenda, pagamento, dúvidas
  if (contem(cfg.palavrasImportantes)) {
    pontos += 3;
    motivos.push("agenda/pagamento/dúvida");
  }

  // 3) Tempo de espera
  if (dados.horasEsperando >= 24) {
    pontos += 5;
    motivos.push("esperando há mais de 1 dia");
  } else if (dados.horasEsperando >= cfg.horasParaSubirPrioridade) {
    pontos += 3;
    motivos.push("esperando há horas");
  }

  // 4) Contato desconhecido (possível novo cliente / consultoria)
  if (!dados.contatoSalvo) {
    pontos += 2;
    motivos.push("contato novo");
  }

  // 5) Volume de mensagens não lidas
  if (dados.naoLidas >= 3) {
    pontos += 1;
    motivos.push(`${dados.naoLidas} mensagens não lidas`);
  }

  // 6) Pergunta em aberto
  if (texto.includes("?")) {
    pontos += 1;
    motivos.push("fez uma pergunta");
  }

  // Classificação final
  let nivel;
  if (pontos >= 7) nivel = "urgente";
  else if (pontos >= 3) nivel = "importante";
  else nivel = "pode_esperar";

  return { nivel, pontos, motivos };
}

module.exports = { pontuarConversa };
