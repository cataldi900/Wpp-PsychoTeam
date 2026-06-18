// ============================================================================
//  Coleta as conversas pendentes no WhatsApp e monta o relatório priorizado.
// ============================================================================

const { tempoEspera } = require("./util");
const { pontuarConversa } = require("./priorizar");

// Pega um trechinho curto e numa linha só, para o preview.
function preview(texto, limite = 90) {
  const t = (texto || "[mídia/áudio]").replace(/\s+/g, " ").trim();
  return t.length > limite ? t.slice(0, limite) + "…" : t;
}

// Varre as conversas do WhatsApp e devolve as que estão pendentes de resposta.
async function coletarConversas(client, cfg) {
  const meuId = client.info && client.info.wid ? client.info.wid._serialized : null;
  const agoraSeg = Date.now() / 1000;
  const chats = await client.getChats();
  const conversas = [];

  for (const chat of chats) {
    try {
      if (chat.isGroup && !cfg.incluirGrupos) continue;
      if (meuId && chat.id._serialized === meuId) continue; // ignora "Você"

      const ultima = chat.lastMessage;
      if (!ultima) continue;

      // Se a ÚLTIMA mensagem foi sua, então você já respondeu -> não está pendente.
      if (ultima.fromMe) continue;

      const horasEsperando = (agoraSeg - ultima.timestamp) / 3600;
      if (horasEsperando > cfg.janelaHoras) continue; // fora da janela do relatório

      // Junta o texto das últimas mensagens recebidas (para analisar palavras).
      let textoRecebido = ultima.body || "";
      try {
        const ultimas = await chat.fetchMessages({ limit: 8 });
        textoRecebido = ultimas
          .filter((m) => !m.fromMe)
          .map((m) => m.body || "")
          .join(" ");
      } catch {
        /* se não der pra buscar histórico, usa só a última mensagem */
      }

      // Contato salvo na agenda? (desconhecido = possível cliente novo)
      let nome = chat.name || (ultima.author || chat.id.user);
      let contatoSalvo = true;
      try {
        const contato = await chat.getContact();
        contatoSalvo = !!contato.isMyContact;
        nome = contato.name || contato.pushname || nome;
      } catch {
        /* mantém o nome do chat */
      }

      const dados = {
        texto: textoRecebido,
        horasEsperando,
        naoLidas: chat.unreadCount || 0,
        contatoSalvo,
      };

      const classificacao = pontuarConversa(dados, cfg);

      conversas.push({
        nome,
        horasEsperando,
        preview: preview(ultima.body),
        ...classificacao,
      });
    } catch (e) {
      // uma conversa com problema não derruba o relatório inteiro
      console.error("  (aviso) erro ao ler uma conversa:", e.message);
    }
  }

  // Mais importante primeiro
  conversas.sort((a, b) => b.pontos - a.pontos);
  return conversas;
}

// Monta o texto final do relatório a partir das conversas classificadas.
function montarRelatorio(conversas) {
  const agora = new Date();
  const data = agora.toLocaleString("pt-BR", {
    weekday: "long",
    day: "2-digit",
    month: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
  });

  const urgentes = conversas.filter((c) => c.nivel === "urgente");
  const importantes = conversas.filter((c) => c.nivel === "importante");
  const podeEsperar = conversas.filter((c) => c.nivel === "pode_esperar");

  const linhas = [];
  linhas.push(`📋 *Resumo do WhatsApp* — ${data}`);
  linhas.push("");

  if (conversas.length === 0) {
    linhas.push("✅ Tudo em dia! Nenhuma mensagem pendente de resposta. 🎉");
    return linhas.join("\n");
  }

  linhas.push(
    `Você tem *${conversas.length}* conversa(s) aguardando resposta:`
  );
  linhas.push(
    `🔴 ${urgentes.length} urgente(s)  •  🟡 ${importantes.length} importante(s)  •  🟢 ${podeEsperar.length} pode(m) esperar`
  );

  const secao = (titulo, lista) => {
    if (lista.length === 0) return;
    linhas.push("");
    linhas.push(titulo);
    for (const c of lista) {
      linhas.push(`• *${c.nome}* (${tempoEspera(c.horasEsperando)})`);
      linhas.push(`   "${c.preview}"`);
      if (c.motivos.length) {
        linhas.push(`   _↳ ${c.motivos.join(", ")}_`);
      }
    }
  };

  secao("🔴 *URGENTE — responder primeiro*", urgentes);
  secao("🟡 *IMPORTANTE*", importantes);
  secao("🟢 *Pode esperar*", podeEsperar);

  linhas.push("");
  linhas.push("_Bom trabalho! 💜 (resumo automático)_");
  return linhas.join("\n");
}

module.exports = { coletarConversas, montarRelatorio };
