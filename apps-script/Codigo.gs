/**
 * PsychoTeam — Programa de Indicação
 * Recebe as indicações enviadas pelo index.html e grava numa Planilha Google.
 *
 * COMO USAR (passo a passo no README.md):
 *  1. Crie uma Planilha Google nova.
 *  2. Menu Extensões > Apps Script.
 *  3. Apague o conteúdo padrão e cole TODO este arquivo.
 *  4. Implantar > Nova implantação > tipo "App da Web".
 *       - Executar como: Eu mesmo
 *       - Quem pode acessar: Qualquer pessoa
 *  5. Copie a URL gerada e cole na constante ENDPOINT do index.html.
 *
 * Cada envio do formulário vira UMA linha por indicado (fica fácil de filtrar
 * e marcar quem fechou). Uma coluna "Status" e "Desconto" ficam prontas pra você.
 */

// Nome da aba onde os dados serão gravados (criada automaticamente).
const ABA = 'Indicações';

// Cabeçalho da planilha.
const CABECALHO = [
  'Data/Hora',
  'Quem indicou (nome)',
  'Quem indicou (WhatsApp)',
  'Indicado nº',
  'Indicado (nome)',
  'Indicado (WhatsApp)',
  'Interesse de plano',
  'Status',            // você preenche: Aguardando / Fechou / Não fechou
  'Desconto indicado', // calculado quando você marcar "Fechou"
  'Desconto p/ quem indicou'
];

// Regras de desconto (em R$).
const DESCONTO_INDICADO = { mensal: 50, trimestral: 100, indeciso: 0 };
const DESCONTO_INDICADOR_POR_FECHAMENTO = 50;

function doPost(e) {
  try {
    const dados = JSON.parse(e.postData.contents);
    const aba = obterAba_();

    const dataHora = formatarData_(dados.enviado_em);
    const indicador = dados.indicador_nome || '';
    const indicadorWhats = dados.indicador_whatsapp || '';
    const indicados = Array.isArray(dados.indicados) ? dados.indicados : [];

    const linhas = indicados.map(function (ind) {
      return [
        dataHora,
        indicador,
        indicadorWhats,
        ind.posicao || '',
        ind.nome || '',
        ind.whatsapp || '',
        rotuloPlano_(ind.plano_interesse),
        'Aguardando',
        '', // desconto do indicado (preenchido quando marcar "Fechou")
        ''  // desconto de quem indicou
      ];
    });

    if (linhas.length === 0) {
      return resposta_({ ok: false, erro: 'Nenhum indicado recebido.' });
    }

    aba.getRange(aba.getLastRow() + 1, 1, linhas.length, CABECALHO.length).setValues(linhas);

    return resposta_({ ok: true, gravados: linhas.length });
  } catch (err) {
    return resposta_({ ok: false, erro: String(err) });
  }
}

// Endpoint de teste no navegador (GET) — confirma que o app está no ar.
function doGet() {
  return resposta_({ ok: true, mensagem: 'PsychoTeam — endpoint de indicações ativo.' });
}

/**
 * Recalcula os descontos com base na coluna "Status".
 * Rode este menu sempre que marcar alguém como "Fechou":
 *   - Para um indicado que fechou: desconto do indicado vem do plano,
 *     e quem indicou ganha +R$50 por aquele fechamento.
 * Você pode rodar manualmente em Executar > recalcularDescontos,
 * ou usar o menu "Indicações" que aparece ao abrir a planilha.
 */
function recalcularDescontos() {
  const aba = obterAba_();
  const ultima = aba.getLastRow();
  if (ultima < 2) return;

  const valores = aba.getRange(2, 1, ultima - 1, CABECALHO.length).getValues();

  valores.forEach(function (linha) {
    const plano = String(linha[6] || '').toLowerCase();
    const status = String(linha[7] || '').toLowerCase();
    const fechou = status.indexOf('fechou') !== -1 && status.indexOf('não') === -1 && status.indexOf('nao') === -1;

    if (fechou) {
      var dInd = 0;
      if (plano.indexOf('trimestral') !== -1) dInd = DESCONTO_INDICADO.trimestral;
      else if (plano.indexOf('mensal') !== -1) dInd = DESCONTO_INDICADO.mensal;
      linha[8] = dInd ? 'R$ ' + dInd : '';
      linha[9] = 'R$ ' + DESCONTO_INDICADOR_POR_FECHAMENTO;
    } else {
      linha[8] = '';
      linha[9] = '';
    }
  });

  aba.getRange(2, 1, valores.length, CABECALHO.length).setValues(valores);
  SpreadsheetApp.getActive().toast('Descontos recalculados!', 'PsychoTeam', 4);
}

// Cria o menu "Indicações" ao abrir a planilha.
function onOpen() {
  SpreadsheetApp.getUi()
    .createMenu('Indicações')
    .addItem('Recalcular descontos', 'recalcularDescontos')
    .addToUi();
}

/* ------------------------------- helpers ------------------------------- */

function obterAba_() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  let aba = ss.getSheetByName(ABA);
  if (!aba) {
    aba = ss.insertSheet(ABA);
  }
  if (aba.getLastRow() === 0) {
    aba.getRange(1, 1, 1, CABECALHO.length).setValues([CABECALHO]).setFontWeight('bold');
    aba.setFrozenRows(1);
  }
  return aba;
}

function rotuloPlano_(id) {
  switch (String(id || '')) {
    case 'mensal': return 'Mensal';
    case 'trimestral': return 'Trimestral';
    case 'indeciso': return 'Ainda não sabe';
    default: return id || '';
  }
}

function formatarData_(iso) {
  const d = iso ? new Date(iso) : new Date();
  return Utilities.formatDate(d, 'America/Sao_Paulo', 'dd/MM/yyyy HH:mm');
}

function resposta_(obj) {
  return ContentService
    .createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}
