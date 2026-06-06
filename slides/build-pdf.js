// Gera uma versão estática (print/PDF) a partir dos mesmos dados do deck interativo.
// Uso: node slides/build-pdf.js  ->  escreve /tmp/print.html (renderizado com WeasyPrint).
const fs = require('fs');
const path = require('path');

const file = path.join(__dirname, 'supino-engenharia.html');
const html = fs.readFileSync(file, 'utf8');

// extrai SEC + SLIDES do próprio deck (sem duplicar conteúdo)
const start = html.indexOf('const SEC =');
const end = html.indexOf('/* ============== RENDER');
const code = html.slice(start, end);
const { SEC, SLIDES } = new Function(code + '\nreturn {SEC,SLIDES};')();

const esc = s => s;
const ytURL = id => 'https://www.youtube.com/watch?v=' + id;
const drURL = id => 'https://drive.google.com/file/d/' + id + '/view';

function videoBox(v) {
  const url = v.type === 'yt' ? ytURL(v.id) : drURL(v.id);
  const tag = v.type === 'yt' ? 'YouTube' : 'Vídeo (Google Drive)';
  return `<a class="vbox ${v.type}" href="${url}">
    <span class="vico">▶</span>
    <span class="vtxt"><b>${v.label}</b><small>${tag} · toque para assistir</small></span>
  </a>`;
}

function slidePage(s, i, total) {
  const counter = (i + 1).toString().padStart(2, '0') + ' / ' + total;
  let cls = 'page', inner = '';
  if (s.kind === 'cover') {
    cls += ' cover';
    inner = `<div class="body-wrap">
      <div class="eyebrow">P S Y C H O T E A M</div>
      <h1 class="big">A ENGENHARIA<br>DO <span class="g">SUPINO</span></h1>
      <div class="lead">Técnica, regras da IPF e variações com propósito — o porquê de cada detalhe, não só o como.</div>
      <div class="cfoot"><span>Treinamento de Força · Powerlifting · Hipertrofia</span><span>por Guilherme Moreti · Coach PsychoTeam</span></div>
    </div>`;
  } else if (s.kind === 'cta') {
    cls += ' cover';
    inner = `<div class="body-wrap center">
      <div class="eyebrow">P S Y C H O T E A M</div>
      <h2 class="title big2">ISSO É UM PONTO<br>DE <span class="g">PARTIDA</span></h2>
      <p class="disc">Essas diretrizes servem pra maioria, mas não substituem a avaliação individual. Histórico, ponto fraco, alavanca e recuperação mudam tudo. Na PsychoTeam todo aluno começa com avaliação completa — treino e ajuste do começo ao fim.</p>
      <a class="btn" href="https://wa.me/message/546BBW7RMFXRB1">Fale comigo no WhatsApp →</a>
      <div class="wa">wa.me/message/546BBW7RMFXRB1</div>
    </div>`;
  } else if (s.kind === 'divider') {
    cls += ' divider';
    inner = `<div class="head"><span>${SEC}</span><span class="r">${counter}</span></div><div class="rule"></div>
      <div class="body-wrap"><div class="part">${s.part}</div><h2 class="title big2">${s.title}</h2><div class="lead">${s.lead}</div></div>
      <div class="foot"><span>PsychoTeam · ${s.section}</span><span>Material exclusivo. Reprodução proibida.</span></div>`;
  } else {
    let media = '';
    if (s.videos) media = `<div class="vwrap">` + s.videos.map(videoBox).join('') + `</div>`;
    const main = (s.kind === 'video')
      ? `<div class="split"><div>${s.html}</div><div>${media}</div></div>`
      : (s.html || '');
    inner = `<div class="head"><span>${SEC} · ${s.section}</span><span class="r">${counter}</span></div><div class="rule"></div>
      <div class="body-wrap"><h2 class="title">${s.title}</h2>${s.lead ? `<div class="lead">${s.lead}</div>` : ''}${main}</div>
      <div class="foot"><span>PsychoTeam · Engenharia do Supino</span><span>${s.section}</span></div>`;
  }
  return `<section class="${cls}">${inner}</section>`;
}

const pages = SLIDES.map((s, i) => slidePage(s, i, SLIDES.length)).join('\n');

const CSS = `
@page { size: 1280px 720px; margin: 0; }
:root{ --red:#c0563f; --gold:#c8a24a; }
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: 'Inter','Helvetica Neue',Arial,sans-serif; color:#ece6d8; background:#0c0b08; }
.page { width:1280px; height:720px; padding:54px 70px 46px; background:linear-gradient(160deg,#100d08,#0a0907);
  page-break-after: always; position:relative; overflow:hidden; display:flex; flex-direction:column; }
.page:last-child{ page-break-after:auto; }
.head{ display:flex; justify-content:space-between; font-size:11px; letter-spacing:.28em; text-transform:uppercase; color:#8a8273; }
.head .r{ color:#c8a24a; }
.rule{ height:1px; background:linear-gradient(90deg,#9c7a2e,transparent); margin-top:10px; }
.body-wrap{ flex:1; display:flex; flex-direction:column; justify-content:center; }
.body-wrap.center{ align-items:center; text-align:center; }
.eyebrow{ font-size:13px; letter-spacing:.42em; text-transform:uppercase; color:#c8a24a; font-weight:700; }
h1.big{ font-family:'Anton','Arial Narrow',sans-serif; font-weight:800; text-transform:uppercase; font-size:86px; line-height:.95; margin-top:24px; letter-spacing:1px; }
.big2{ font-size:70px !important; }
.title{ font-family:'Anton','Arial Narrow',sans-serif; font-weight:800; text-transform:uppercase; font-size:50px; line-height:1; letter-spacing:.5px; }
.g{ color:#c8a24a; }
.lead{ font-family:Georgia,'Times New Roman',serif; font-style:italic; color:#e6c463; font-size:21px; line-height:1.4; margin-top:14px; max-width:82%; }
.cover .lead{ max-width:62%; }
ul.clean{ list-style:none; margin-top:14px; }
ul.clean li{ position:relative; padding-left:26px; font-size:18px; line-height:1.45; color:#b9b1a0; margin-bottom:11px; }
ul.clean li:before{ content:""; position:absolute; left:0; top:8px; width:9px; height:9px; background:#c8a24a; transform:rotate(45deg); }
ul.clean li strong{ color:#ece6d8; }
.cards{ display:grid; gap:13px; margin-top:14px; }
.c2{ grid-template-columns:1fr 1fr; } .c3{ grid-template-columns:repeat(3,1fr); } .c4{ grid-template-columns:1fr 1fr; }
.card{ background:linear-gradient(160deg,#151209,#0e0b07); border:1px solid #2a2519; border-left:3px solid #c8a24a; border-radius:10px; padding:14px 16px; }
.card h4{ font-size:12.5px; letter-spacing:.1em; text-transform:uppercase; color:#c8a24a; margin-bottom:6px; font-weight:700; }
.card p{ font-size:15px; line-height:1.4; color:#b9b1a0; } .card p strong{ color:#ece6d8; }
.callout{ margin-top:16px; background:rgba(255,255,255,.03); border-left:3px solid #c8a24a; border-radius:6px; padding:13px 16px; }
.callout .k{ font-size:11px; letter-spacing:.2em; text-transform:uppercase; color:#c8a24a; font-weight:700; }
.callout p{ font-family:Georgia,serif; font-style:italic; color:#ece6d8; font-size:16px; line-height:1.4; margin-top:5px; }
.split{ display:grid; grid-template-columns:1.05fr .95fr; gap:24px; align-items:center; margin-top:6px; }
.judge{ display:flex; gap:12px; margin-top:10px; }
.judge .j{ flex:1; border-radius:10px; padding:11px 13px; font-weight:600; font-size:14px; }
.judge .ok{ background:#1d2614; border:1px solid #3c5226; color:#7fae57; }
.judge .no{ background:#271612; border:1px solid #532a22; color:#c0563f; }
.judge .j span{ display:block; font-size:11px; letter-spacing:.1em; text-transform:uppercase; opacity:.8; margin-bottom:3px; }
.part{ font-size:15px; letter-spacing:.4em; color:#c8a24a; text-transform:uppercase; font-weight:700; }
.divider .lead{ font-size:23px; max-width:72%; }
.foot,.cfoot{ display:flex; justify-content:space-between; font-size:10.5px; letter-spacing:.18em; text-transform:uppercase; color:#5d574a; margin-top:auto; padding-top:12px; border-top:1px solid #2a2519; }
.cfoot{ border:0; }
.disc{ max-width:64%; color:#b9b1a0; font-size:16px; line-height:1.5; margin-top:18px; }
.btn{ margin-top:22px; display:inline-block; background:linear-gradient(145deg,#e6c463,#9c7a2e); color:#140f06; font-weight:700; font-size:19px; padding:14px 36px; border-radius:10px; text-decoration:none; }
.wa{ margin-top:10px; color:#c8a24a; font-size:14px; letter-spacing:.08em; }
.vwrap{ display:flex; flex-direction:column; gap:12px; }
.vbox{ display:flex; align-items:center; gap:14px; text-decoration:none; background:radial-gradient(120% 120% at 20% 0%,#241d10,#0c0a07);
  border:1px solid #4a3c1c; border-left:4px solid #c8a24a; border-radius:12px; padding:16px 18px; }
.vbox .vico{ width:44px; height:44px; flex:none; border-radius:50%; background:#c8a24a; color:#15110a; font-size:18px;
  display:flex; align-items:center; justify-content:center; }
.vbox .vtxt{ display:flex; flex-direction:column; }
.vbox .vtxt b{ color:#ece6d8; font-size:16px; } .vbox .vtxt small{ color:#9a907a; font-size:12.5px; margin-top:3px; letter-spacing:.04em; }
`;

const out = `<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8">
<style>@import url('https://fonts.googleapis.com/css2?family=Anton&family=Inter:wght@400;600;700&display=swap');
${CSS}</style></head><body>${pages}</body></html>`;

fs.writeFileSync('/tmp/print.html', out);
console.log('print.html escrito com', SLIDES.length, 'páginas');
