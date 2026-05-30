// Funções auxiliares compartilhadas.

// Remove acentos e deixa minúsculo, para comparar texto sem erro.
function normalizar(texto) {
  return (texto || "")
    .toLowerCase()
    .normalize("NFD")
    .replace(/[̀-ͯ]/g, "");
}

// "bom dia" / "boa tarde" / "boa noite" conforme a hora e as faixas do config.
function saudacaoDoHorario(faixas) {
  const hora = new Date().getHours();
  const { bomDia, boaTarde } = faixas;
  if (hora >= bomDia.inicio && hora <= bomDia.fim) return "bom dia";
  if (hora >= boaTarde.inicio && hora <= boaTarde.fim) return "boa tarde";
  return "boa noite";
}

// Transforma horas em texto amigável: "há 3h", "há 2 dias", "há poucos minutos".
function tempoEspera(horas) {
  if (horas < 1) return "há poucos minutos";
  if (horas < 24) return `há ${Math.round(horas)}h`;
  const dias = Math.floor(horas / 24);
  return dias === 1 ? "há 1 dia" : `há ${dias} dias`;
}

module.exports = { normalizar, saudacaoDoHorario, tempoEspera };
