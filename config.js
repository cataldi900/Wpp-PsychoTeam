// ============================================================================
//  CONFIGURAÇÃO DO ROBÔ  —  edite só este arquivo para mudar o comportamento.
//  Tudo que está entre aspas "..." você pode trocar à vontade.
// ============================================================================

module.exports = {
  // --------------------------------------------------------------------------
  // 1) PALAVRAS-CHAVE QUE ATIVAM A RESPOSTA AUTOMÁTICA
  //    Se a mensagem que a pessoa enviar contiver QUALQUER uma destas palavras,
  //    o robô responde com a saudação + envia os 2 PDFs.
  //    (não diferencia maiúscula/minúscula nem acento)
  // --------------------------------------------------------------------------
  palavrasChave: [
    "consultoria",
    "consulta",
    "plano",
    "planos",
    "informacao",
    "informacoes",
    "informaçoes",
    "informações",
    "mais informacoes",
    "valor",
    "valores",
    "preco",
    "preço",
    "quanto custa",
    "saber mais",
  ],

  // --------------------------------------------------------------------------
  // 2) TEXTO DA SAUDAÇÃO
  //    {saudacao} é trocado automaticamente por "bom dia", "boa tarde" ou
  //    "boa noite", conforme o horário em que a pessoa mandou a mensagem.
  // --------------------------------------------------------------------------
  mensagemSaudacao: "Oi, {saudacao}! Tudo bem? 😊",

  // Mensagem enviada logo depois da saudação, junto com os PDFs.
  mensagemApresentacao:
    "Que bom ter você por aqui! Estou te enviando dois materiais com todas as " +
    "informações sobre a nossa consultoria. Dá uma olhadinha e qualquer dúvida " +
    "é só me chamar por aqui. 💜",

  // --------------------------------------------------------------------------
  // 3) PASTA DOS PDFs
  //    Coloque seus 2 arquivos PDF dentro da pasta "pdfs".
  //    O robô envia TODOS os PDFs que encontrar nessa pasta (em ordem alfabética).
  //    Dica: nomeie como "1-apresentacao.pdf" e "2-planos.pdf" para garantir a ordem.
  // --------------------------------------------------------------------------
  pastaPdfs: "./pdfs",

  // --------------------------------------------------------------------------
  // 4) ANTI-SPAM
  //    Tempo (em horas) que o robô espera antes de responder a MESMA pessoa de novo.
  //    Assim, se a pessoa mandar 5 mensagens seguidas, ela recebe os PDFs só 1 vez.
  //    Coloque 0 se quiser que responda SEMPRE, em toda mensagem.
  // --------------------------------------------------------------------------
  horasEntreRespostas: 12,

  // --------------------------------------------------------------------------
  // 5) RESPONDER EM GRUPOS?
  //    false = ignora mensagens de grupos (recomendado).
  //    true  = também responde dentro de grupos.
  // --------------------------------------------------------------------------
  responderEmGrupos: false,

  // --------------------------------------------------------------------------
  // 6) FAIXAS DE HORÁRIO DA SAUDAÇÃO (horário do seu computador)
  // --------------------------------------------------------------------------
  faixasHorario: {
    bomDia: { inicio: 5, fim: 11 },    // 05:00 às 11:59 -> "bom dia"
    boaTarde: { inicio: 12, fim: 17 }, // 12:00 às 17:59 -> "boa tarde"
    // qualquer outro horário -> "boa noite"
  },
};
