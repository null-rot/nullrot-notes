(() => {
'use strict';
const D = window.DATA;
const ELEMS = D.elems, CROPS = D.crops;
const $ = (s, r = document) => r.querySelector(s);
const tmp = document.createElement('div');
const dec = h => { tmp.innerHTML = h; return tmp.textContent; };
const norm = s => dec(String(s)).toUpperCase().replace(/[\s ]+/g, '');
const attr = s => String(s).replace(/&/g, '&amp;').replace(/"/g, '&quot;');
const chips = s => s.replace(/\[\[(.+?)\]\]/g, (m, k) => `<b class="k" tabindex="-1" data-k="${attr(k)}">${k}</b>`);
const ELBYNORM = {};
ELEMS.forEach(e => { const l = e.kind === 'pad' ? 'PAD' + e.label : norm(e.label); ELBYNORM[l] = e.id; });
const ELLABEL = {}; ELEMS.forEach(e => ELLABEL[e.id] = e.kind === 'pad' ? 'pad ' + e.label : e.label.replace(/\n/g, ' '));
const ELKIND = {}; ELEMS.forEach(e => ELKIND[e.id] = e.kind);
const idFor = t => ELBYNORM[norm(t)] || (/^pad \d+$/i.test(t) ? 'p' + t.split(' ')[1] : null);
const LETTERS = 'ABCDEFGHIJ';

/* ---------- panel renderer (port of panel.py, hardware palette) ---------- */
const esc = s => s.replace(/&/g, '&amp;');
const st = (f, s, w) => `style="fill:${f};${s ? `stroke:${s};stroke-width:${w}` : ''}"`;
const tf = c => `style="fill:${c}"`;
function textLines(label, cx, cy, size, fill) {
  const lines = label.split('\n'), off = (lines.length - 1) * size * 0.55;
  return lines.map((ln, i) => `<text x="${cx}" y="${(cy - off + i * size * 1.1 + size * 0.35).toFixed(1)}" text-anchor="middle" font-size="${size}" font-weight="700" ${tf(fill)}>${esc(ln)}</text>`).join('');
}
const ROLEWORD = { hold: 'hold', press: 'press', turn: 'turn', sel: 'selected' };
function describe(hl) {
  return Object.entries(hl).filter(([, r]) => r[0] !== 'sel')
    .sort((a, b) => (a[1][1] || 99) - (b[1][1] || 99))
    .map(([id, r]) => `${r[1] ? r[1] + ' ' : ''}${ROLEWORD[r[0]]} ${ELLABEL[id]}`).join(', ');
}
function panelSVG(hl, crop, o = {}) {
  hl = hl || {};
  const dispSub = o.dispSub || '';
  let x, y, w, h;
  if (crop === 'auto') {
    const mg = { btn: 10, pad: 10, pad2: 10, knob: 18, disp: 12 };
    const ys = ELEMS.filter(e => hl[e.id]).map(e => [e.cy - e.h / 2 - Math.max(mg[e.kind], hl[e.id][1] && o.badge !== 0 ? 30 : 0), e.cy + e.h / 2 + mg[e.kind]]);
    if (!ys.length) return '';
    const y0 = Math.max(0, Math.min(...ys.map(a => a[0]))), y1 = Math.min(750, Math.max(...ys.map(a => a[1])));
    x = 60; y = y0; w = 880; h = Math.max(y1 - y0, 80);
  } else {
    [x, y, w, h] = CROPS[crop];
    if (crop !== 'all') {
      const need = Math.min(...ELEMS.filter(e => hl[e.id] && hl[e.id][1]).map(e => e.cy - e.h / 2 - 30));
      if (need < y) { h += y - need; y = need; }
    }
  }
  const inCrop = e => crop === 'all' || (e.kind === 'disp' ? e.cy + e.w : e.cy + e.h / 2) <= y + h + 2 && (e.kind === 'disp' ? e.cy - e.w : e.cy - e.h / 2) >= y - 2;
  const dim = Object.keys(hl).length > 0;
  const P = [];
  P.push(`<rect x="${x - 20}" y="${y - 20}" width="${w + 40}" height="${h + 40}" ${st('var(--pbg)')}/>`);
  P.push(`<rect x="52" y="4" width="896" height="738" rx="26" ${st('var(--pbody)', 'var(--pbodystroke)', 3)}/>`);
  const badges = [];
  for (const e of ELEMS) {
    const role = hl[e.id], r = role ? role[0] : null;
    if (!r && !inCrop(e)) continue;
    const op = (r || !dim) ? 1 : 0.4;
    const stroke = r ? 'var(--phlstroke)' : 'var(--pstroke)', tx = r ? 'var(--phltxt)' : 'var(--ptxt)';
    const fill = r === 'sel' ? 'var(--phlstroke)' : r ? `var(--l${r})` : 'var(--pbtn)';
    const { cx, cy, w: ew, h: eh, label: lab, sub } = e;
    const g = [`<g opacity="${op}"${o.interactive ? ` class="el" data-id="${e.id}" tabindex="0" role="button" aria-label="${attr(ELLABEL[e.id])}${r ? ' (lit)' : ''}"` : ''}>`];
    if (e.kind === 'disp') {
      g.push(`<circle cx="${cx}" cy="${cy}" r="${ew}" ${st(r ? fill : 'var(--pdisp)', 'var(--pdispstroke)', 3)}/>`);
      g.push(`<text x="${cx}" y="${cy - 4}" text-anchor="middle" font-size="22" font-weight="800" letter-spacing="1" ${tf(r ? 'var(--phltxt)' : 'var(--pdispfg)')}>DISPLAY</text>`);
      if (dispSub) g.push(`<text x="${cx}" y="${cy + 20}" text-anchor="middle" font-size="15" ${tf(r ? 'var(--phltxt)' : 'var(--pdispsub)')}>${dispSub}</text>`);
    } else if (e.kind === 'knob') {
      g.push(`<circle cx="${cx}" cy="${cy}" r="${ew * 0.62}" ${st(fill, stroke, r ? 4 : 2.5)}/>`);
      g.push(`<line x1="${cx}" y1="${cy}" x2="${cx}" y2="${cy - ew * 0.55}" style="stroke:${r ? 'var(--phlring)' : 'var(--ptxt)'};stroke-width:3.5;stroke-linecap:round"/>`);
      if (r === 'turn') g.push(`<path d="M${cx - ew * 0.95} ${cy + ew * 0.35} A ${ew} ${ew} 0 1 1 ${cx + ew * 0.95} ${cy + ew * 0.35}" style="fill:none;stroke:var(--lturn);stroke-width:4;stroke-linecap:round"/>`);
      const right = ['vol', 'c1', 'c2', 'c3'].includes(e.id);
      g.push(`<text x="${right ? cx + ew * 0.62 + 14 : cx - ew * 0.62 - 14}" y="${cy + 6}"${right ? '' : ' text-anchor="end"'} font-size="17" font-weight="800" ${tf('var(--ptxt)')}>${lab}</text>`);
    } else if (e.kind === 'btn') {
      g.push(`<rect x="${cx - ew / 2}" y="${cy - eh / 2}" width="${ew}" height="${eh}" rx="7" ${st(fill, stroke, r === 'hold' ? 4 : r ? 3 : 2)}/>`);
      if (r === 'hold') g.push(`<rect x="${cx - ew / 2 + 5}" y="${cy - eh / 2 + 5}" width="${ew - 10}" height="${eh - 10}" rx="4" style="fill:none;stroke:var(--phlring);stroke-width:2"/>`);
      let fsz = !lab.includes('\n') && lab.length < 8 ? 15 : 14;
      if (lab === 'SHIFT') fsz = 17;
      if (r) { const mx = Math.max(...lab.split('\n').map(t => t.length)); fsz = Math.max(fsz, Math.min(21, 72 / (mx * 0.64))); }
      g.push(textLines(lab, cx, cy, fsz, tx));
    } else {
      g.push(`<rect x="${cx - ew / 2}" y="${cy - eh / 2}" width="${ew}" height="${eh}" rx="9" ${st(fill, stroke, r === 'hold' ? 4 : r ? 3 : 2)}/>`);
      if (r === 'hold') g.push(`<rect x="${cx - ew / 2 + 6}" y="${cy - eh / 2 + 6}" width="${ew - 12}" height="${eh - 12}" rx="5" style="fill:none;stroke:var(--phlring);stroke-width:2"/>`);
      if (e.kind === 'pad') g.push(`<text x="${cx}" y="${cy - 2}" text-anchor="middle" font-size="${r ? 42 : 34}" font-weight="800" ${tf(tx)}>${lab}</text>`);
      else g.push(textLines(lab, cx, cy - 8, lab.includes('\n') ? 17 : 20, tx));
      if (sub) {
        const quiet = dim && !r;
        g.push(`<rect x="${cx - ew / 2 + 8}" y="${cy + eh / 2 - 23}" width="${ew - 16}" height="17" rx="3" ${st(quiet ? 'var(--pshdim)' : 'var(--pshbar)')}/>`);
        g.push(`<text x="${cx}" y="${cy + eh / 2 - 10}" text-anchor="middle" font-size="12.5" font-weight="800" letter-spacing=".3" ${tf(quiet ? 'var(--pshdimtxt)' : 'var(--pshtxt)')}>${sub}</text>`);
      }
    }
    g.push('</g>');
    P.push(g.join(''));
    if (role && role[1]) {
      const rad = o.badge || 25, bx = cx - ew / 2 - (e.kind === 'knob' ? 0 : rad * 0.35), by = cy - eh / 2 - rad * 0.35;
      badges.push(`<circle cx="${bx}" cy="${by}" r="${rad}" ${st('var(--pbadge)', 'var(--pbadgest)', 4)}/><text x="${bx}" y="${by + rad * 0.42}" text-anchor="middle" font-size="${rad * 1.25}" font-weight="800" ${tf('var(--pbadgetxt)')}>${role[1]}</text>`);
    }
  }
  P.push(badges.join(''));
  const vbw = w, wpct = Math.min(100, vbw / 880 * 100).toFixed(2);
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="${x} ${y} ${w} ${h}" style="width:${o.fill ? 100 : wpct}%" role="img" aria-label="${attr(o.aria || 'SP-404MKII panel')}" font-family="Barlow,Inter,Helvetica,Arial,sans-serif">${P.join('')}</svg>`;
}

/* ---------- derive a diagram from a row's [[chips]] ---------- */
function rowHL(input) {
  const hl = {}; let n = 0, last = 0; const re = /\[\[(.+?)\]\]/g; let m;
  while ((m = re.exec(input))) {
    const before = input.slice(last, m.index).toLowerCase(); last = re.lastIndex;
    const id = idFor(m[1]); if (!id || hl[id]) continue;
    const role = ELKIND[id] === 'knob' ? 'turn' : /hold/.test(before) ? 'hold' : 'press';
    hl[id] = [role, ++n];
  }
  return hl;
}

/* ---------- index ---------- */
const GUIDES = D.guides;
GUIDES.forEach(g => g.sections.forEach(s => {
  s.name = dec(s.title); s.letter = LETTERS[s.n - 1];
  let i = 0;
  s.entries.forEach(e => {
    if (e.type !== 'note') e._pos = s.letter + (++i);
    let t = [e.title || ''];
    if (e.type === 'group') e.rows.forEach(r => t.push(r.name, r.input, r.result));
    else if (e.type === 'pads') t.push(...e.labels);
    else t.push(e.body);
    if (e.hl) Object.keys(e.hl).forEach(id => t.push(ELLABEL[id]));
    e._t = dec(t.join(' ').replace(/\[\[|\]\]/g, '')).toLowerCase();
    e._c = new Set((e.chips || []).map(norm));
    if (e.type === 'group') e.rows.forEach(r => {
      r._t = dec([r.name, r.input, r.result].join(' ').replace(/\[\[|\]\]/g, '')).toLowerCase();
      r._c = new Set((r.chips || []).map(norm));
      r._hl = rowHL(r.input || '');
    });
  });
}));

/* ---------- state ---------- */
const S = { g: GUIDES[0].id, s: 'all', q: '', key: null, both: false, mode: 'dia', open: false };
try { if (localStorage.getItem('sp404-mode') === 'text') S.mode = 'text'; } catch (_) {}
function readHash() {
  const p = new URLSearchParams(location.hash.slice(1));
  if (GUIDES.some(g => g.id === p.get('g'))) S.g = p.get('g');
  S.s = p.get('s') && p.get('s') !== 'all' ? +p.get('s') : 'all';
  S.q = p.get('q') || ''; S.both = p.get('b') === '1';
  const k = p.get('k'); S.key = k ? { text: k, id: idFor(k) } : null;
}
function writeHash() {
  const p = new URLSearchParams({ g: S.g, s: S.s });
  if (S.q) p.set('q', S.q); if (S.key) p.set('k', S.key.text); if (S.both) p.set('b', '1');
  history.replaceState(null, '', '#' + p.toString());
}
const guide = () => GUIDES.find(g => g.id === S.g);
const dispSub = g => g.id === 'doom' ? 'DOOM OS grid' : '';

/* ---------- matching ---------- */
const tokens = () => S.q.toLowerCase().split(/\s+/).filter(Boolean);
const active = () => tokens().length > 0 || !!S.key;
function keyMatchEntry(e) {
  if (!S.key) return true;
  if (S.key.id && e.hl && e.hl[S.key.id]) return true;
  return e._c.has(norm(S.key.text)) || (S.key.id && e._c.has(norm(ELLABEL[S.key.id])));
}
function keyMatchRow(r) {
  if (!S.key) return true;
  if (S.key.id && r._hl[S.key.id]) return true;
  return r._c.has(norm(S.key.text)) || (S.key.id && r._c.has(norm(ELLABEL[S.key.id])));
}
const tokMatch = (t, tk) => tk.every(w => t.includes(w));
function filterEntry(e) {
  const tk = tokens();
  if (e.type === 'group') {
    if (!tk.length && !S.key) return e;
    const titleHit = tk.length && tokMatch(dec(e.title).toLowerCase(), tk);
    const rows = e.rows.filter(r => (!tk.length || titleHit || tokMatch(r._t, tk)) && keyMatchRow(r));
    return rows.length ? Object.assign({}, e, { rows }) : null;
  }
  if (S.key && e.type === 'note') return null;
  if (tk.length && !tokMatch(e._t, tk)) return null;
  if (!keyMatchEntry(e)) return null;
  return e;
}
/* rank inside a section: title hits, then diagrammed cards, then rows, then notes */
function rank(e) {
  const tk = tokens(), title = dec(e.title || '').toLowerCase();
  let s = { card: 2, pads: 3, group: 4, note: 6 }[e.type];
  if (tk.length && tokMatch(title, tk)) s -= 2;
  return s;
}

/* ---------- rendering ---------- */
function combo(hl) {
  const ks = Object.entries(hl || {});
  const stepped = ks.filter(([, r]) => r[1]);
  const use = (stepped.length ? stepped : ks).sort((a, b) => (a[1][1] || 99) - (b[1][1] || 99));
  if (!use.length) return '';
  const parts = use.map(([id, r], i) => {
    const op = i === 0 ? '' : `<span class="op">${use[i - 1][1][0] === 'hold' ? '+' : 'then'}</span>`;
    return `${op}<b class="kc ${r[0]}" tabindex="-1" data-k="${attr(ELLABEL[id])}">${r[1] ? `<span class="n">${r[1]}</span>` : ''}<svg aria-hidden="true"><use href="#m-${r[0]}"/></svg>${ELLABEL[id]}</b>`;
  });
  return `<span class="combo" aria-label="${attr(describe(Object.fromEntries(use)))}">${parts.join('')}</span>`;
}
/* a credit line: name ······ credit */
const credit = (name, tag, right) => `<div class="credit"><${tag} class="t">${name}</${tag}>${right ? `<span class="lead" aria-hidden="true"></span>${right}` : ''}</div>`;
const dia = (hl, crop, g, title) => {
  const svg = panelSVG(hl, crop, { aria: `${dec(title)}: ${describe(hl)}`, dispSub: dispSub(g) });
  return svg ? `<figure class="dia">${svg}</figure>` : '';
};
function renderEntry(e, g) {
  if (e.type === 'card') {
    const figs = e.crops.map(c => dia(e.hl, c, g, e.title)).join('');
    return `<article class="cr"><div class="pos">${e._pos}</div><div>${credit(e.title, 'h3', combo(e.hl))}<div class="cb">${chips(e.body)}</div></div>${figs}</article>`;
  }
  if (e.type === 'group') {
    const rows = e.rows.map((r, i) => `<div class="rw"><div class="pos">${i + 1}</div><div>${credit(chips(r.name), 'div', r.input ? `<span class="in">${chips(r.input)}</span>` : '')}${r.result ? `<div class="rs">${chips(r.result)}</div>` : ''}</div>${dia(r._hl, 'auto', g, dec(r.name))}</div>`).join('');
    return `<section class="grp"><h3 class="t"><span class="pos">${e._pos}</span>${e.title}</h3>${rows}</section>`;
  }
  if (e.type === 'pads') {
    const cells = e.labels.map((t, i) => `<button type="button" class="pc${e.used.includes(i + 1) ? ' u' : ''}" data-k="pad ${i + 1}"><b>${i + 1}</b><span>${t}</span></button>`).join('');
    return `<section class="pads"><h3 class="t"><span class="pos">${e._pos}</span> ${e.title}</h3><div class="padgrid">${cells}</div><p class="cb">${e.used.length ? 'Blue numbers = pads DOOM OS refers to. ' : ''}Orange labels are Roland’s printed SHIFT functions. Tap a pad to filter.</p></section>`;
  }
  return `<section class="note"><h3 class="t">${e.title}</h3><div class="cb">${chips(e.body)}</div></section>`;
}
function sectionHTML(g, s, entries, showGuide) {
  if (!entries.length) return '';
  return `<h2 class="side"><span class="letter">Side ${s.letter}</span><span>${s.title}</span>${showGuide ? `<span class="os">· ${g.name}</span>` : ''}<small>${entries.length} ${entries.length > 1 ? 'entries' : 'entry'}</small></h2>${entries.map(e => renderEntry(e, g)).join('')}`;
}
function highlight(root) {
  const tk = tokens(); if (!tk.length) return;
  const re = new RegExp('(' + tk.map(t => t.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')).join('|') + ')', 'gi');
  const w = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, { acceptNode: n => n.parentElement.closest('svg,mark,.k,.kc,.pos') || !re.test(n.nodeValue) ? NodeFilter.FILTER_REJECT : NodeFilter.FILTER_ACCEPT });
  const nodes = []; while (w.nextNode()) nodes.push(w.currentNode);
  nodes.forEach(n => {
    const f = document.createDocumentFragment(); let last = 0, m; const t = n.nodeValue; re.lastIndex = 0;
    while ((m = re.exec(t))) { f.append(t.slice(last, m.index)); const k = document.createElement('mark'); k.textContent = m[0]; f.append(k); last = m.index + m[0].length; if (!m[0].length) re.lastIndex++; }
    f.append(t.slice(last)); n.replaceWith(f);
  });
  root.querySelectorAll('b.k').forEach(b => { if (tk.some(w => b.textContent.toLowerCase().includes(w))) b.classList.add('on'); });
}
let litHL = {};
function render() {
  const list = $('#list'); let html = '', n = 0;
  litHL = {};
  if (active()) {
    const gs = S.both ? [guide(), ...GUIDES.filter(g => g.id !== S.g)] : [guide()];
    gs.forEach(g => g.sections.forEach(s => {
      const es = s.entries.map(filterEntry).filter(Boolean).sort((a, b) => rank(a) - rank(b));
      es.forEach(e => {
        n += e.type === 'group' ? e.rows.length : 1;
        const hls = e.type === 'group' ? e.rows.map(r => r._hl) : [e.hl || {}];
        hls.forEach(h => Object.entries(h).forEach(([id, r]) => { if (!litHL[id]) litHL[id] = [r[0], null]; }));
      });
      html += sectionHTML(g, s, es, S.both);
    }));
    if (S.key) litHL = S.key.id ? { [S.key.id]: ['sel', null] } : {};
    const where = S.both ? 'either guide' : guide().name;
    if (!html) html = `<div class="empty"><p>Nothing in ${where} matches ${S.q ? `“${S.q.replace(/</g, '&lt;')}”` : ''}${S.q && S.key ? ' with ' : ''}${S.key ? S.key.text : ''}.</p><div class="acts">${S.both ? '' : '<button type="button" class="go" data-act="both">Search both guides</button>'}<button type="button" data-act="clear">Clear search</button></div></div>`;
    $('#count').textContent = n ? `${n} ${n > 1 ? 'shortcuts' : 'shortcut'} in ${where}` : `No matches in ${where}`;
  } else {
    const g = guide();
    const secs = S.s === 'all' ? g.sections : g.sections.filter(s => s.n === S.s);
    secs.forEach(s => html += sectionHTML(g, s, s.entries, false));
    $('#count').textContent = '';
  }
  list.innerHTML = html;
  document.body.classList.toggle('textmode', S.mode === 'text');
  highlight(list);
  renderBoard(); renderControls(); writeHash(); markWraps();
}
/* drop the leader where the credit wraps, so it never ends in blank space */
function markWraps() {
  document.querySelectorAll('#list .credit').forEach(c => {
    c.classList.remove('wrapped');
    const t = c.firstElementChild, r = c.lastElementChild;
    if (r && r !== t && r.offsetTop > t.offsetTop + t.offsetHeight / 2) c.classList.add('wrapped');
  });
}
let rz; addEventListener('resize', () => { clearTimeout(rz); rz = setTimeout(markWraps, 120); });
document.fonts && document.fonts.ready.then(markWraps);
function renderBoard() {
  const g = guide();
  $('#map').innerHTML = panelSVG(litHL, 'all', { interactive: true, fill: true, badge: 0, dispSub: dispSub(g), aria: 'SP-404MKII panel: choose a control to list every shortcut that uses it' });
  const anyLit = Object.keys(litHL).length > 0;
  $('#mapThumb').innerHTML = panelSVG(litHL, anyLit ? 'auto' : 'all', { fill: true, badge: 0, dispSub: '', aria: anyLit ? `Lit on the panel: ${Object.keys(litHL).map(id => ELLABEL[id]).join(', ')}` : 'Panel overview' });
  $('#thumb').classList.toggle('wide', anyLit);
  const lit = $('#lit'), shut = S.open ? '<button type="button" class="shut" data-act="shut">Done</button>' : '';
  const ROLEP = { hold: 'held', press: 'pressed', turn: 'turned' };
  if (S.key) lit.innerHTML = `<span class="lbl">Lit</span><b class="kc chosen">${S.key.text}</b>${shut}<button type="button" class="clr" data-act="key"><svg aria-hidden="true"><use href="#i-close"/></svg>Clear</button>`;
  else if (tokens().length && anyLit) {
    const ids = Object.keys(litHL), shown = ids.slice(0, 4);
    lit.innerHTML = `<span class="lbl">Lit</span>${shown.map(id => `<span class="lk ${litHL[id][0]}"><svg aria-hidden="true"><use href="#m-${litHL[id][0]}"/></svg>${ELLABEL[id]} <i>${ROLEP[litHL[id][0]]}</i></span>`).join('')}${ids.length > 4 ? `<span class="more">+${ids.length - 4} more</span>` : ''}${shut}`;
  }
  else lit.innerHTML = S.open || matchMedia('(min-width:960px)').matches ? `<span>Choose a control to list every shortcut that uses it.</span>${shut}` : '';
  $('#board').classList.toggle('open', S.open); $('#deck').classList.toggle('open', S.open);
  $('#thumb').setAttribute('aria-expanded', S.open);
}
function renderControls() {
  const g = guide();
  $('#guideSeg').innerHTML = GUIDES.map(x => `<button type="button" data-g="${x.id}" aria-pressed="${S.g === x.id}">${x.name}</button>`).join('');
  $('#secSel').innerHTML = `<option value="all">All sides</option>` + g.sections.map(s => `<option value="${s.n}"${S.s === s.n ? ' selected' : ''}>${s.letter} · ${s.name}</option>`).join('');
  $('#secSel').disabled = active();
  document.querySelectorAll('[data-mode]').forEach(b => b.setAttribute('aria-pressed', b.dataset.mode === S.mode));
  $('#bothBtn').setAttribute('aria-pressed', S.both);
}

/* ---------- events ---------- */
let timer;
const top0 = () => scrollTo({ top: 0, behavior: 'smooth' });
$('#q').addEventListener('input', e => { clearTimeout(timer); timer = setTimeout(() => { S.q = e.target.value.trim(); render(); }, 120); });
$('#guideSeg').addEventListener('click', e => { const b = e.target.closest('[data-g]'); if (!b) return; S.g = b.dataset.g; S.s = 'all'; render(); scrollTo(0, 0); });
$('#secSel').addEventListener('change', e => { S.s = e.target.value === 'all' ? 'all' : +e.target.value; render(); scrollTo(0, 0); });
$('#bothBtn').addEventListener('click', () => { S.both = !S.both; render(); });
document.querySelectorAll('[data-mode]').forEach(b => b.addEventListener('click', () => {
  S.mode = b.dataset.mode; try { localStorage.setItem('sp404-mode', S.mode); } catch (_) {} render();
}));
$('#thumb').addEventListener('click', () => { S.open = true; renderBoard(); const f = $('#map g.el'); if (f) f.focus({ preventScroll: true }); });
function setKey(text, id) { S.key = { text, id: id || idFor(text) }; S.open = false; render(); top0(); }
function act(a) {
  if (a === 'key') { S.key = null; render(); }
  else if (a === 'shut') { S.open = false; renderBoard(); $('#thumb').focus(); }
  else if (a === 'both') { S.both = true; render(); }
  else if (a === 'clear') { $('#q').value = ''; S.q = ''; S.key = null; render(); $('#q').focus(); }
}
document.addEventListener('click', e => {
  const a = e.target.closest('[data-act]'); if (a) return act(a.dataset.act);
  const gEl = e.target.closest('#map g.el'); if (gEl) return setKey(ELLABEL[gEl.dataset.id], gEl.dataset.id);
  const k = e.target.closest('#list [data-k]'); if (k) return setKey(k.dataset.k);
});
$('#map').addEventListener('keydown', e => { const gEl = e.target.closest('g.el'); if (gEl && (e.key === 'Enter' || e.key === ' ')) { e.preventDefault(); setKey(ELLABEL[gEl.dataset.id], gEl.dataset.id); } });
addEventListener('keydown', e => {
  if (e.key === '/' && !/INPUT|TEXTAREA|SELECT/.test(document.activeElement.tagName)) { e.preventDefault(); $('#q').focus(); }
  if (e.key === 'Escape') { if (S.open && matchMedia('(max-width:959px)').matches) return act('shut'); $('#q').value = ''; S.q = ''; S.key = null; render(); }
});
addEventListener('hashchange', () => { readHash(); $('#q').value = S.q; render(); });

/* ---------- theme ---------- */
function setTheme(t, save) {
  document.documentElement.dataset.theme = t;
  $('meta[name=theme-color]').content = t === 'dark' ? '#161617' : '#efece4';
  const b = $('#themeBtn'); b.setAttribute('aria-pressed', t === 'light'); b.setAttribute('aria-label', t === 'dark' ? 'Switch to light theme' : 'Switch to dark theme');
  if (save) try { localStorage.setItem('sp404-theme', t); } catch (_) {}
}
let saved = null; try { saved = localStorage.getItem('sp404-theme'); } catch (_) {}
setTheme(saved === 'light' ? 'light' : 'dark');
$('#themeBtn').addEventListener('click', () => setTheme(document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark', true));

readHash(); $('#q').value = S.q; render();
if ('serviceWorker' in navigator && /^https:|^http:\/\/(localhost|127\.0\.0\.1)/.test(location.href)) navigator.serviceWorker.register('sw.js').catch(() => {});
})();
