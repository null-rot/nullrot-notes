(() => {
'use strict';
const D = window.DATA;
const ELEMS = D.elems, CROPS = D.crops;
const $ = (s, r = document) => r.querySelector(s);
const tmp = document.createElement('div');
const dec = h => { tmp.innerHTML = h; return tmp.textContent; };
const norm = s => dec(String(s)).toUpperCase().replace(/[\s ]+/g, '');
const chips = s => s.replace(/\[\[(.+?)\]\]/g, (m, k) => `<b class="k" tabindex="0" role="button" data-k="${k.replace(/"/g, '&quot;')}">${k}</b>`);
const ELBYNORM = {};
ELEMS.forEach(e => { const l = e.kind === 'pad' ? 'PAD' + e.label : norm(e.label); ELBYNORM[l] = e.id; });
const ELLABEL = {}; ELEMS.forEach(e => ELLABEL[e.id] = e.kind === 'pad' ? 'pad ' + e.label : e.label.replace(/\n/g, ' '));

/* ---------- panel renderer (port of panel.py) ---------- */
const esc = s => s.replace(/&/g, '&amp;');
const st = (f, s, w) => `style="fill:${f};${s ? `stroke:${s};stroke-width:${w}` : ''}"`;
const tf = c => `style="fill:${c}"`;
function textLines(label, cx, cy, size, fill) {
  const lines = label.split('\n'), off = (lines.length - 1) * size * 0.55;
  return lines.map((ln, i) => `<text x="${cx}" y="${(cy - off + i * size * 1.1 + size * 0.35).toFixed(1)}" text-anchor="middle" font-size="${size}" font-weight="700" ${tf(fill)}>${esc(ln)}</text>`).join('');
}
function panelSVG(hl, crop, o = {}) {
  hl = hl || {};
  const fs = 1, bigfs = 1, dispSub = o.dispSub || '';
  let x, y, w, h;
  if (crop === 'auto') {
    const mg = { btn: 6, pad: 4.5, pad2: 4.5, knob: 14, disp: 10 };
    const ys = ELEMS.filter(e => hl[e.id]).map(e => [e.cy - e.h / 2 - mg[e.kind], e.cy + e.h / 2 + mg[e.kind]]);
    const y0 = Math.max(0, Math.min(...ys.map(a => a[0]))), y1 = Math.min(750, Math.max(...ys.map(a => a[1])));
    x = 60; y = y0; w = 880; h = Math.max(y1 - y0, 60);
  } else [x, y, w, h] = CROPS[crop];
  const dim = Object.keys(hl).length > 0;
  const P = [];
  P.push(`<rect x="${x - 20}" y="${y - 20}" width="${w + 40}" height="${h + 40}" ${st('var(--pbg)')}/>`);
  P.push(`<rect x="52" y="4" width="896" height="738" rx="26" ${st('var(--pbody)', 'var(--pbodystroke)', 3)}/>`);
  for (const e of ELEMS) {
    const role = hl[e.id], r = role ? role[0] : null;
    const op = (r || !dim) ? 1 : 0.42;
    const stroke = r ? 'var(--phlstroke)' : 'var(--pstroke)', tx = r ? 'var(--phltxt)' : 'var(--ptxt)';
    const fill = r ? `var(--${r})` : 'var(--pbtn)';
    const { cx, cy, w: ew, h: eh, label: lab, sub } = e;
    const g = [`<g opacity="${op}"${o.interactive ? ` class="el" data-id="${e.id}" tabindex="0" role="button" aria-label="${ELLABEL[e.id]}"` : ''}>`];
    if (e.kind === 'disp') {
      g.push(`<circle cx="${cx}" cy="${cy}" r="${ew}" ${st('var(--pdisp)', 'var(--pdispstroke)', 3)}/>`);
      g.push(`<text x="${cx}" y="${cy - 4}" text-anchor="middle" font-size="22" font-weight="800" letter-spacing="1" ${tf('var(--pdispfg)')}>DISPLAY</text>`);
      if (dispSub) g.push(`<text x="${cx}" y="${cy + 20}" text-anchor="middle" font-size="15" ${tf('var(--pdispsub)')}>${dispSub}</text>`);
    } else if (e.kind === 'knob') {
      g.push(`<circle cx="${cx}" cy="${cy}" r="${ew * 0.62}" ${st(fill, stroke, r ? 4 : 2.5)}/>`);
      g.push(`<line x1="${cx}" y1="${cy}" x2="${cx}" y2="${cy - ew * 0.55}" style="stroke:${r ? 'var(--phlring)' : 'var(--ptxt)'};stroke-width:3.5;stroke-linecap:round"/>`);
      if (['vol', 'c1', 'c2', 'c3'].includes(e.id))
        g.push(`<text x="${cx + ew * 0.62 + 8}" y="${cy + 6}" font-size="17" font-weight="800" ${tf('var(--ptxt)')}>${lab}</text>`);
      else
        g.push(`<text x="${cx - ew * 0.62 - 8}" y="${cy + 6}" text-anchor="end" font-size="17" font-weight="800" ${tf('var(--ptxt)')}>${lab}</text>`);
    } else if (e.kind === 'btn') {
      g.push(`<rect x="${cx - ew / 2}" y="${cy - eh / 2}" width="${ew}" height="${eh}" rx="7" ${st(fill, stroke, r === 'hold' ? 4 : r ? 3 : 2)}/>`);
      if (r === 'hold') g.push(`<rect x="${cx - ew / 2 + 5}" y="${cy - eh / 2 + 5}" width="${ew - 10}" height="${eh - 10}" rx="4" style="fill:none;stroke:var(--phlring);stroke-width:1.6"/>`);
      let fsz = (!lab.includes('\n') && lab.length < 8 ? 15 : 14) * fs;
      if (lab === 'SHIFT') fsz = 17;
      if (r) { const mx = Math.max(...lab.split('\n').map(t => t.length)); fsz = Math.max(fsz, Math.min(21, 72 / (mx * 0.64))) * bigfs; }
      g.push(textLines(lab, cx, cy, fsz, tx));
    } else {
      g.push(`<rect x="${cx - ew / 2}" y="${cy - eh / 2}" width="${ew}" height="${eh}" rx="9" ${st(fill, stroke, r === 'hold' ? 4 : r ? 3 : 2)}/>`);
      if (r === 'hold') g.push(`<rect x="${cx - ew / 2 + 6}" y="${cy - eh / 2 + 6}" width="${ew - 12}" height="${eh - 12}" rx="5" style="fill:none;stroke:var(--phlring);stroke-width:1.6"/>`);
      if (e.kind === 'pad') g.push(`<text x="${cx}" y="${cy - 2}" text-anchor="middle" font-size="${r ? 42 : 34}" font-weight="800" ${tf(tx)}>${lab}</text>`);
      else g.push(textLines(lab, cx, cy - 8, lab.includes('\n') ? 17 : 20, tx));
      if (sub) {
        g.push(`<rect x="${cx - ew / 2 + 8}" y="${cy + eh / 2 - 23}" width="${ew - 16}" height="17" rx="3" ${st('var(--pshbar)')}/>`);
        g.push(`<text x="${cx}" y="${cy + eh / 2 - 10}" text-anchor="middle" font-size="12.5" font-weight="800" letter-spacing=".3" ${tf('var(--pshtxt)')}>${sub}</text>`);
      }
    }
    if (role && role[1]) {
      const bx = cx - ew / 2 + 2, by = cy - eh / 2 + 2;
      g.push(`<circle cx="${bx}" cy="${by}" r="12" ${st('var(--pbadge)', 'var(--pbadgest)', 2)}/>`);
      g.push(`<text x="${bx}" y="${by + 5}" text-anchor="middle" font-size="15" font-weight="800" ${tf('var(--pbadgetxt)')}>${role[1]}</text>`);
    }
    g.push('</g>');
    P.push(g.join(''));
  }
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="${x} ${y} ${w} ${h}" role="img" aria-label="${(o.aria || 'SP-404MKII panel').replace(/"/g, '&quot;')}" font-family="Inter,Helvetica,Arial,sans-serif">${P.join('')}</svg>`;
}

/* ---------- index ---------- */
const GUIDES = D.guides;
GUIDES.forEach(g => g.sections.forEach(s => {
  s.name = dec(s.title);
  s.entries.forEach(e => {
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
    });
  });
}));

/* ---------- state ---------- */
const S = { g: GUIDES[0].id, s: 'all', q: '', key: null, both: false };
function readHash() {
  const p = new URLSearchParams(location.hash.slice(1));
  if (GUIDES.some(g => g.id === p.get('g'))) S.g = p.get('g');
  if (p.get('s')) S.s = p.get('s') === 'all' ? 'all' : +p.get('s');
  S.q = p.get('q') || ''; S.both = p.get('b') === '1';
  const k = p.get('k'); S.key = k ? { text: k, id: ELBYNORM[norm(k)] || null } : null;
}
function writeHash() {
  const p = new URLSearchParams({ g: S.g, s: S.s });
  if (S.q) p.set('q', S.q); if (S.key) p.set('k', S.key.text); if (S.both) p.set('b', '1');
  history.replaceState(null, '', '#' + p.toString());
}
const guide = () => GUIDES.find(g => g.id === S.g);

/* ---------- matching ---------- */
const tokens = () => S.q.toLowerCase().split(/\s+/).filter(Boolean);
const active = () => tokens().length > 0 || !!S.key;
function keyMatchEntry(e) {
  if (!S.key) return true;
  const nk = norm(S.key.text);
  if (S.key.id && e.hl && e.hl[S.key.id]) return true;
  return e._c.has(nk) || (S.key.id && e._c.has(norm(ELLABEL[S.key.id])));
}
function keyMatchRow(r) {
  if (!S.key) return true;
  return r._c.has(norm(S.key.text)) || (S.key.id && r._c.has(norm(ELLABEL[S.key.id])));
}
const tokMatch = (t, tk) => tk.every(w => t.includes(w));
function filterEntry(e) {
  const tk = tokens();
  if (e.type === 'group') {
    if (!tk.length && !S.key) return e;
    const titleHit = tk.length && tokMatch(e._t.split(' ').slice(0, 6).join(' '), tk) && tokMatch(dec(e.title).toLowerCase(), tk);
    const rows = e.rows.filter(r => (!tk.length || titleHit || tokMatch(r._t, tk)) && keyMatchRow(r));
    return rows.length ? Object.assign({}, e, { rows }) : null;
  }
  if (tk.length && !tokMatch(e._t, tk)) return null;
  if (!keyMatchEntry(e)) return null;
  return e;
}

/* ---------- rendering ---------- */
function renderEntry(e, g) {
  if (e.type === 'card') {
    const svgs = e.crops.map(c => panelSVG(e.hl, c, { aria: dec(e.title), dispSub: g.id === 'doom' ? 'DOOM OS grid' : '' })).join('');
    return `<section class="card"><h3>${e.title}</h3>${svgs}<div class="cb">${chips(e.body)}</div></section>`;
  }
  if (e.type === 'group') {
    const rows = e.rows.map(r => `<div class="row${r.result ? '' : ' no-r'}"><div class="n">${chips(r.name)}</div><div class="i">${chips(r.input)}</div>${r.result ? `<div class="r">${chips(r.result)}</div>` : ''}</div>`).join('');
    return `<section class="grp"><h3>${e.title}</h3><div class="rows">${rows}</div></section>`;
  }
  if (e.type === 'pads') {
    const cells = e.labels.map((t, i) => `<div class="pc${e.used.includes(i + 1) ? ' u' : ''}" data-k="pad ${i + 1}" tabindex="0" role="button"><b>${i + 1}</b><span>${t}</span></div>`).join('');
    return `<section class="padbox grp"><h3>${e.title}</h3><div class="padgrid">${cells}</div>${e.used.length ? '<p class="cb" style="color:var(--mut)">Outlined = pad shortcuts DOOM OS refers to.</p>' : ''}<p class="cb" style="color:var(--mut)">Labels are Roland’s printed SHIFT functions; tap a pad to filter.</p></section>`;
  }
  return `<section class="box"><h3>${e.title}</h3><div class="cb">${chips(e.body)}</div></section>`;
}
const legend = '<div class="legend"><span><i style="background:var(--hold)"></i>hold</span><span><i style="background:var(--press)"></i>press</span><span><i style="background:var(--turn)"></i>turn</span><span>numbered badge = order</span></div>';
function mapBox(g) {
  return `<section class="mapbox"><h3 style="margin:0 0 6px">Panel map</h3>${legend}${panelSVG({}, 'all', { interactive: true, dispSub: g.id === 'doom' ? 'DOOM OS grid' : '', aria: 'SP-404MKII panel map' })}<p class="hint">Tap any control to list everything that uses it.</p></section>`;
}
function sectionHTML(g, s, entries, showGuide) {
  if (!entries.length) return '';
  return `<h2 class="sec">${s.title}${showGuide ? `<span class="gtag">${g.name}</span>` : ''}<small>${entries.length} item${entries.length > 1 ? 's' : ''}</small></h2><div class="grid">${entries.map(e => renderEntry(e, g)).join('')}</div>`;
}
function highlight(root) {
  const tk = tokens(); if (!tk.length) return;
  const re = new RegExp('(' + tk.map(t => t.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')).join('|') + ')', 'gi');
  const w = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, { acceptNode: n => n.parentElement.closest('svg,mark,script') || !re.test(n.nodeValue) ? NodeFilter.FILTER_REJECT : NodeFilter.FILTER_ACCEPT });
  const nodes = []; while (w.nextNode()) nodes.push(w.currentNode);
  nodes.forEach(n => {
    re.lastIndex = 0;
    const f = document.createDocumentFragment(); let last = 0, m; const t = n.nodeValue; re.lastIndex = 0;
    while ((m = re.exec(t))) { f.append(t.slice(last, m.index)); const k = document.createElement('mark'); k.textContent = m[0]; f.append(k); last = m.index + m[0].length; if (!m[0].length) re.lastIndex++; }
    f.append(t.slice(last)); n.replaceWith(f);
  });
}
function render() {
  const main = $('#main'); let html = '';
  const act = active();
  if (act) {
    const gs = S.both ? GUIDES : [guide()];
    let n = 0;
    gs.forEach(g => g.sections.forEach(s => {
      const es = s.entries.map(filterEntry).filter(Boolean); n += es.length;
      html += sectionHTML(g, s, es, S.both);
    }));
    html = html || `<div class="empty">No matches${S.both ? '' : ' in this guide'}. ${S.both ? '' : 'Try “both guides”.'}</div>`;
  } else {
    const g = guide();
    const secs = S.s === 'all' ? g.sections : g.sections.filter(s => s.n === S.s);
    if (S.s === 'all' || S.s === 1) html += '<div class="grid">' + mapBox(g) + '</div>';
    secs.forEach(s => html += sectionHTML(g, s, s.entries, false));
  }
  main.innerHTML = html;
  highlight(main);
  renderPills(); renderTabs(); writeHash();
}
function renderTabs() {
  const g = guide(), tabs = $('#tabs'), act = active();
  tabs.hidden = act && true;
  tabs.innerHTML = [`<button role="tab" data-s="all" aria-selected="${S.s === 'all'}">All</button>`]
    .concat(g.sections.map(s => `<button role="tab" data-s="${s.n}" aria-selected="${S.s === s.n}">${s.n}. ${s.name}</button>`)).join('');
}
function renderPills() {
  $('#pills').innerHTML = S.key ? `<span class="pill">Control: <b>${S.key.text}</b><button aria-label="Clear control filter" data-clear="key">×</button></span>` : '';
}
function renderSeg() {
  $('#guideSeg').innerHTML = GUIDES.map(g => `<button role="tab" data-g="${g.id}" aria-selected="${S.g === g.id}">${g.name}</button>`).join('');
}

/* ---------- events ---------- */
let timer;
$('#q').addEventListener('input', e => { clearTimeout(timer); timer = setTimeout(() => { S.q = e.target.value.trim(); render(); }, 120); });
$('#both').addEventListener('change', e => { S.both = e.target.checked; render(); });
$('#guideSeg').addEventListener('click', e => { const b = e.target.closest('[data-g]'); if (!b) return; S.g = b.dataset.g; S.s = 'all'; renderSeg(); render(); scrollTo(0, 0); });
$('#tabs').addEventListener('click', e => { const b = e.target.closest('[data-s]'); if (!b) return; S.s = b.dataset.s === 'all' ? 'all' : +b.dataset.s; render(); scrollTo(0, 0); });
$('#pills').addEventListener('click', e => { if (e.target.dataset.clear) { S.key = null; render(); } });
function pick(el) {
  const kEl = el.closest('[data-k]'), gEl = el.closest('g.el');
  if (kEl) { const t = kEl.dataset.k; S.key = { text: t, id: ELBYNORM[norm(t)] || (/^pad \d+$/i.test(t) ? 'p' + t.split(' ')[1] : null) }; }
  else if (gEl) { const id = gEl.dataset.id; S.key = { text: ELLABEL[id], id }; }
  else return false;
  render(); scrollTo({ top: 0, behavior: 'smooth' }); return true;
}
$('#main').addEventListener('click', e => pick(e.target));
$('#main').addEventListener('keydown', e => { if ((e.key === 'Enter' || e.key === ' ') && e.target.matches('[data-k],g.el')) { e.preventDefault(); pick(e.target); } });
addEventListener('keydown', e => { if (e.key === '/' && !/INPUT|TEXTAREA/.test(document.activeElement.tagName)) { e.preventDefault(); $('#q').focus(); } if (e.key === 'Escape') { $('#q').value = ''; S.q = ''; S.key = null; render(); } });
addEventListener('hashchange', () => { readHash(); sync(); render(); });

/* ---------- theme ---------- */
function setTheme(t, save) {
  document.documentElement.dataset.theme = t;
  $('meta[name=theme-color]').content = t === 'dark' ? '#282a36' : '#f5f4ef';
  if (save) try { localStorage.setItem('sp404-theme', t); } catch (_) {}
}
let saved = null; try { saved = localStorage.getItem('sp404-theme'); } catch (_) {}
setTheme(saved || (matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark'));
$('#themeBtn').addEventListener('click', () => setTheme(document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark', true));

function sync() { $('#q').value = S.q; $('#both').checked = S.both; renderSeg(); }
readHash(); sync(); render();
if ('serviceWorker' in navigator && /^https:|^http:\/\/localhost/.test(location.href)) navigator.serviceWorker.register('sw.js').catch(() => {});
})();
