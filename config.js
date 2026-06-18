// ============================================================================
//  CONFIGURAÇÃO  —  edite só este arquivo para mudar o comportamento.
//  Tudo que está entre aspas "..." você pode trocar à vontade.
//
//  Este assistente tem 2 recursos independentes:
//   (A) RELATÓRIO DIÁRIO  -> resumo priorizado do que responder (LIGADO)
//   (B) AUTO-RESPOSTA      -> responde sozinho quem pergunta da consultoria (DESLIGADO)
//  Você liga/desliga cada um no campo "ativo".
// ============================================================================

module.exports = {
  // ==========================================================================
  //  (A) RELATÓRIO DIÁRIO
  // ==========================================================================
  relatorio: {
    ativo: true,

    // Horários (do seu computador) em que o resumo é gerado e te enviado.
    // Formato "HH:MM", 24h. Pode colocar quantos quiser.
    horarios: ["07:30", "20:00"],

    // Manda o relatório pra você mesmo no WhatsApp (conversa "Você").
    enviarParaMim: true,

    // Também salva uma cópia do relatório em arquivo, na pasta /relatorios.
    salvarArquivo: true,

    // Olha as mensagens de quantas horas pra trás ao montar o resumo.
    janelaHoras: 16,

    // Incluir conversas de GRUPOS no relatório? (normalmente não)
    incluirGrupos: false,

    // A partir de quantas horas SEM RESPOSTA uma conversa "sobe" de prioridade.
    horasParaSubirPrioridade: 6,

    // Palavras que indicam URGÊNCIA (sobem a conversa para 🔴 Urgente).
    palavrasUrgencia: [
      "urgente", "urgencia", "emergencia", "socorro", "agora", "imediato",
      "crise", "surto", "panico", "nao aguento", "nao estou bem",
      "preciso muito", "me ajuda", "ajuda por favor", "hoje ainda", "pra hoje",
    ],

    // Palavras IMPORTANTES (sobem para 🟡 Importante): agenda, dinheiro, dúvidas.
    palavrasImportantes: [
      "remarcar", "desmarcar", "cancelar", "agendar", "agenda", "horario",
      "consulta", "sessao", "atendimento", "faltei", "falta",
      "pagamento", "pagar", "pix", "boleto", "nota fiscal", "recibo",
      "valor", "valores", "preco", "duvida", "pergunta", "consultoria", "plano",
    ],
  },

  // ==========================================================================
  //  (B) AUTO-RESPOSTA DA CONSULTORIA  (desligada por padrão)
  // ==========================================================================
  autoResposta: {
    ativo: false,

    // Palavras-chave que disparam a resposta automática + envio dos PDFs.
    palavrasChave: [
      "consultoria", "consulta", "plano", "planos",
      "informacao", "informacoes", "informações", "mais informacoes",
      "valor", "valores", "preco", "preço", "quanto custa", "saber mais",
    ],

    // {saudacao} vira "bom dia" / "boa tarde" / "boa noite" conforme o horário.
    mensagemSaudacao: "Oi, {saudacao}! Tudo bem? 😊",

    mensagemApresentacao:
      "Que bom ter você por aqui! Estou te enviando dois materiais com todas as " +
      "informações sobre a nossa consultoria. Dá uma olhadinha e qualquer dúvida " +
      "é só me chamar por aqui. 💜",

    // Pasta com os PDFs a enviar (envia todos os .pdf em ordem alfabética).
    pastaPdfs: "./pdfs",

    // Horas de espera antes de responder a MESMA pessoa de novo (0 = sempre).
    horasEntreRespostas: 12,
  },

  // ==========================================================================
  //  GERAL
  // ==========================================================================
  geral: {
    // Responder/considerar grupos na auto-resposta?
    responderEmGrupos: false,

    // Faixas de horário da saudação (usado na auto-resposta).
    faixasHorario: {
      bomDia: { inicio: 5, fim: 11 },    // 05:00–11:59 -> "bom dia"
      boaTarde: { inicio: 12, fim: 17 }, // 12:00–17:59 -> "boa tarde"
      // qualquer outro horário -> "boa noite"
    },
  },
};
