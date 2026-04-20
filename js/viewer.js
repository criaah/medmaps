/* ============ MEDMAPS VIEWER v2 — JS ============ */

// Mapas hardcoded (legacy, sólo si están presentes para compat)
const LEGACY_MAPS = { fa: window.MAP_FA, inph: window.MAP_INPH };
let MAP = null;  // se asigna en init() — asíncrono desde data-loader o legacy

const $ = (s, p = document) => p.querySelector(s);
const $$ = (s, p = document) => Array.from(p.querySelectorAll(s));

// URL params
function getParam(name) {
  const m = location.search.match(new RegExp('[?&]' + name + '=([^&]+)'));
  return m ? decodeURIComponent(m[1]) : null;
}

// Resuelve el mapa a cargar: prioridad URL > localStorage > default
async function resolveMap() {
  const urlId = getParam('id');
  const lsId = localStorage.getItem('medmaps.map');
  const target = urlId || lsId;

  // Caso legacy (fa / inph hardcoded)
  if (target && LEGACY_MAPS[target] && !target.startsWith('map_')) {
    return LEGACY_MAPS[target];
  }

  // Caso dinámico: cargar vía data-loader
  if (target && window.MedMapsData) {
    try {
      return await window.MedMapsData.loadMap(target);
    } catch (e) {
      console.warn('No se pudo cargar', target, e);
    }
  }

  // Fallback: primer legacy disponible
  return LEGACY_MAPS.fa || LEGACY_MAPS.inph;
}

// Expose section body renderer for mindmap cards
window.renderSectionBody = function(sec) {
  const dummy = renderSection(sec, 0);
  // extract body (strip outer <section>..<header>..</header>)
  const m = dummy.match(/<\/header>\s*([\s\S]*)<\/section>/);
  return m ? m[1] : dummy;
};

// ============ RENDER FICHA ============
function renderFicha() {
  const c = $('#fichaContent');
  let html = '';

  // HERO
  const related = MAP.related || [];
  const sources = MAP.sources || [];
  const metaBits = [];
  metaBits.push(`<span class="hero-tag">${esc(MAP.specialty || 'General')}</span>`);
  if (related.length) metaBits.push(related.map(r => `<span>${esc(r)}</span>`).join('<span class="sep">·</span>'));
  if (sources.length) metaBits.push(`<span>${sources.join(' · ')}</span>`);
  if (MAP.reading_min) metaBits.push(`<span>${MAP.reading_min} min lectura</span>`);
  html += `
    <header class="hero">
      <div class="hero-meta">${metaBits.join('<span class="sep">·</span>')}</div>
      <h1>${esc(MAP.title)}</h1>
      ${MAP.subtitle ? `<p class="hero-subtitle">${esc(MAP.subtitle)}</p>` : ''}
      ${MAP.one_liner ? `<div class="hero-oneliner">${esc(MAP.one_liner)}</div>` : ''}
    </header>
  `;

  // RED FLAGS — sólo si tienen contenido real (no placeholder)
  const rf = MAP.redflags || [];
  const rfReal = rf.length && !(rf.length === 1 && /sin red flags/i.test(rf[0].t || ''));
  if (rfReal) {
    html += `
      <section class="redflags" id="sec-redflags">
        <div class="redflags-head">Red flags · urgencias</div>
        <ul class="redflags-list">
          ${rf.map(r => `<li><div><b>${esc(r.t)}</b> — ${esc(r.d)}</div></li>`).join('')}
        </ul>
      </section>
    `;
  }

  // SECTIONS
  (MAP.sections || []).forEach((sec, i) => {
    html += renderSection(sec, i + 1);
  });

  c.innerHTML = html;
}

function renderSection(sec, num) {
  const n = String(num).padStart(2, '0');
  let body = '';
  switch (sec.kind) {
    case 'text-grid':
      body = `<div class="tgrid">${sec.items.map(it =>
        `<div class="tgrid-item"><div class="tgrid-h">${esc(it.h)}</div><div class="tgrid-b">${esc(it.b)}</div></div>`
      ).join('')}</div>`;
      break;
    case 'two-col':
      body = `<div class="twocol">
        <div class="twocol-col"><h4>${esc(sec.left.h)}</h4><ul>${sec.left.items.map(i => `<li>${esc(i)}</li>`).join('')}</ul></div>
        <div class="twocol-col"><h4>${esc(sec.right.h)}</h4><ul>${sec.right.items.map(i => `<li>${esc(i)}</li>`).join('')}</ul></div>
      </div>`;
      break;
    case 'score':
      body = `
        ${sec.intro ? `<p class="score-intro">${esc(sec.intro)}</p>` : ''}
        <table class="score-table">
          <thead><tr><th>Letra</th><th>Criterio</th><th>Puntos</th></tr></thead>
          <tbody>${sec.rows.map(r => `<tr><td>${esc(r[0])}</td><td>${esc(r[1])}</td><td>${esc(r[2])}</td></tr>`).join('')}</tbody>
        </table>
        <div class="score-bands">
          ${sec.bands.map((b, i) => `<div class="score-band b${i}">
            <div class="score-band-range">${esc(b.range)}</div>
            <div class="score-band-risk">Riesgo: ${esc(b.risk)}</div>
            <div class="score-band-action">${esc(b.action)}</div>
          </div>`).join('')}
        </div>`;
      break;
    case 'steps':
      body = `<div class="steps">${sec.steps.map(s =>
        `<div class="step"><div class="step-n">${esc(s.n)}</div><div><div class="step-h">${esc(s.h)}</div><p class="step-b">${esc(s.b)}</p></div></div>`
      ).join('')}</div>`;
      break;
    case 'framework':
      body = `${sec.intro ? `<p class="framework-intro">${esc(sec.intro)}</p>` : ''}
        <div class="pillars">${sec.pillars.map(p =>
          `<div class="pillar"><div class="pillar-letter">${esc(p.letter)}</div><div class="pillar-title">${esc(p.title)}</div><div class="pillar-sub">${esc(p.sub)}</div></div>`
        ).join('')}</div>`;
      break;
    case 'drugs':
      body = `<div class="drugs">
        ${sec.drugs.map(d => `<div class="drug-row">
          <div class="drug-cell drug-name">${esc(d.name)}<small>${esc(d.class)}</small></div>
          <div class="drug-cell drug-dose">${esc(d.dose)}${d.adjust && d.adjust !== '—' ? `<small>Ajuste: ${esc(d.adjust)}</small>` : ''}</div>
          <div class="drug-cell drug-notes">${esc(d.notes)}</div>
        </div>`).join('')}
        ${sec.warning ? `<div class="drug-warning">⚠ ${esc(sec.warning)}</div>` : ''}
      </div>`;
      break;
    case 'algorithm':
      body = `<div class="algo">
        <div class="algo-start">${esc(sec.start)}</div>
        ${sec.steps.map(s => `<div class="algo-step">
          <div class="algo-q">${esc(s.q)}</div>
          <div class="algo-arrow">→</div>
          <div class="algo-yes"><b>Sí:</b> ${esc(s.yes)}</div>
        </div>`).join('')}
        ${sec.pharma_cv ? `<div class="algo-pharma">
          <h4>Cardioversión farmacológica</h4>
          ${sec.pharma_cv.map(d => `<div class="algo-drug"><b>${esc(d.name)}</b><div><div class="algo-drug-dose">${esc(d.dose)}</div><div class="algo-drug-note">${esc(d.note)}</div></div></div>`).join('')}
        </div>` : ''}
      </div>`;
      break;
    case 'pearls':
      body = `<div class="pearls">${sec.items.map(p =>
        `<div class="pearl"><div class="pearl-t">${esc(p.t)}</div><div class="pearl-d">${esc(p.d)}</div></div>`
      ).join('')}</div>`;
      break;
    case 'studies':
      body = `<div class="studies">${sec.items.map(s =>
        `<div class="study"><div class="study-yr">${esc(s.yr)}</div><div class="study-name">${esc(s.name)}<small>${esc(s.trial)}</small></div><div><div class="study-q">${esc(s.q)}</div><div class="study-res">${esc(s.res)}</div></div></div>`
      ).join('')}</div>`;
      break;
  }
  return `<section class="section" id="sec-${sec.id}">
    <header class="section-head">
      <span class="section-num">${n}</span>
      <span class="section-icon">${sec.icon}</span>
      <h2>${esc(sec.title)}</h2>
    </header>
    ${body}
  </section>`;
}

function esc(s) {
  return String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
}

// ============ TOC ============
function renderToc() {
  const list = $('#tocList');
  const rf = MAP.redflags || [];
  const rfReal = rf.length && !(rf.length === 1 && /sin red flags/i.test(rf[0].t || ''));
  const items = (rfReal ? [{ id: 'sec-redflags', title: 'Red flags · urgencias' }] : [])
    .concat((MAP.sections || []).map(s => ({ id: 'sec-' + s.id, title: s.title })));
  list.innerHTML = items.map(it =>
    `<li class="toc-item"><a class="toc-link" href="#${it.id}" data-sec="${it.id}">${esc(it.title)}</a></li>`
  ).join('');
  list.addEventListener('click', e => {
    const a = e.target.closest('.toc-link');
    if (!a) return;
    e.preventDefault();
    const id = a.getAttribute('data-sec');
    document.getElementById(id)?.scrollIntoView({ behavior: 'smooth', block: 'start' });
    closeDrawers();
  });
}

// Scroll-spy
let scrollSpyFn = null;
function setupScrollSpy() {
  if (scrollSpyFn) window.removeEventListener('scroll', scrollSpyFn);
  const sections = [document.getElementById('sec-redflags'), ...(MAP.sections || []).map(s => document.getElementById('sec-' + s.id))].filter(Boolean);
  const links = $$('.toc-link');
  const linkById = Object.fromEntries(links.map(l => [l.getAttribute('data-sec'), l]));

  function onScroll() {
    const y = window.scrollY + 100;
    let active = sections[0];
    for (const s of sections) if (s.offsetTop <= y) active = s;
    links.forEach(l => l.classList.remove('active'));
    if (active) linkById[active.id]?.classList.add('active');

    // progress
    const docH = document.documentElement.scrollHeight - window.innerHeight;
    const pct = Math.min(100, Math.max(0, (window.scrollY / docH) * 100));
    $('#tocBar').style.width = pct + '%';
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  scrollSpyFn = onScroll;
  onScroll();
}

// ============ CONEXIONES ============
function renderConn() {
  const connections = MAP.connections || [];
  const related = MAP.related || [];
  const sources = MAP.sources || [];
  $('#connList').innerHTML = connections.length
    ? connections.map(c =>
        `<div class="conn-item" data-to="${esc(c.to || '')}">
          <div><div class="conn-item-name">${esc(c.label)}</div><div class="conn-item-via">${esc(c.via || '')}</div></div>
          <div class="conn-strength s${c.strength || 2}"><i></i><i></i><i></i></div>
        </div>`
      ).join('')
    : '<div class="conn-empty" style="color:#888;padding:.5rem 0;font-size:.85rem">Sin cross-references detectadas en este mapa.</div>';
  $('#connSpec').innerHTML = [
    `<span class="conn-chip primary">${esc(MAP.specialty || 'General')}</span>`,
    ...related.map(r => `<span class="conn-chip">${esc(r)}</span>`),
    ...sources.map(s => `<span class="conn-chip">${esc(s)}</span>`)
  ].join('');
}

// ============ DRAWERS ============
const backdrop = $('#backdrop');
const tocPanel = $('#tocPanel');
const connPanel = $('#connPanel');

function closeDrawers() {
  tocPanel.classList.remove('visible');
  connPanel.classList.remove('visible');
  backdrop.classList.remove('visible');
}
backdrop.addEventListener('click', closeDrawers);

function toggleToc() {
  const v = tocPanel.classList.toggle('visible');
  connPanel.classList.remove('visible');
  backdrop.classList.toggle('visible', v);
}
function toggleConn() {
  const v = connPanel.classList.toggle('visible');
  tocPanel.classList.remove('visible');
  backdrop.classList.toggle('visible', v);
}
$('#mnToc').onclick = toggleToc;
$('#mnConn').onclick = toggleConn;
$('#mnBiblio').onclick = () => location.href = 'index.html';

// ============ CARD MODE ============
function toggleCards() {
  const on = document.body.classList.toggle('cards-on');
  $$('.mnav-btn')[2]?.classList.toggle('active', on);
  $$('[class*="blur"]').forEach(el => el.classList.remove('revealed'));
  tweakState.cards = on ? 'on' : 'off';
  applyTweaks(tweakState);
  // wire reveal on click
  if (on) {
    document.body.addEventListener('click', revealOnClick);
  } else {
    document.body.removeEventListener('click', revealOnClick);
    $$('.revealed').forEach(el => el.classList.remove('revealed'));
  }
}
function revealOnClick(e) {
  const selectors = ['.drug-dose','.drug-notes','.tgrid-b','.score-bands','.step-b','.pearl-d','.study-res','.algo-yes','.algo-drug-dose','.algo-drug-note'];
  for (const s of selectors) {
    const el = e.target.closest(s);
    if (el) { el.classList.toggle('revealed'); return; }
  }
}
$('#btnCardTop').onclick = toggleCards;
$('#tocCard').onclick = toggleCards;
$('#mnCard').onclick = toggleCards;
$('#tocPrint').onclick = () => window.print();

// ============ SEARCH ============
const palette = $('#palette');
const pInput = $('#paletteInput');
const pResults = $('#paletteResults');

function openPalette() {
  palette.classList.add('visible');
  pInput.value = '';
  pInput.focus();
  renderPaletteResults('');
  // clear prior highlights
  $$('mark.hit').forEach(m => { const t = document.createTextNode(m.textContent); m.replaceWith(t); });
}
function closePalette() {
  palette.classList.remove('visible');
}
$('#btnSearchTop').onclick = openPalette;
$('#mnSearch').onclick = openPalette;
palette.addEventListener('click', e => { if (e.target === palette) closePalette(); });

// Build searchable index
function buildIndex() {
  const idx = [];
  const rf = MAP.redflags || [];
  const rfReal = rf.length && !(rf.length === 1 && /sin red flags/i.test(rf[0].t || ''));
  if (rfReal) idx.push({ kind: 'Sección', text: 'Red flags · urgencias', id: 'sec-redflags' });
  (MAP.sections || []).forEach(s => {
    idx.push({ kind: 'Sección', text: s.title, id: 'sec-' + s.id });
    if (s.kind === 'drugs') (s.drugs || []).forEach(d => idx.push({ kind: 'Fármaco', text: d.name, sub: d.dose, id: 'sec-' + s.id }));
    if (s.kind === 'studies') (s.items || []).forEach(it => idx.push({ kind: 'Estudio', text: it.name + ' (' + it.yr + ')', sub: it.q, id: 'sec-' + s.id }));
    if (s.kind === 'pearls') (s.items || []).forEach(it => idx.push({ kind: 'Perla', text: it.t, sub: (it.d || '').slice(0, 80), id: 'sec-' + s.id }));
    // Para text-grid genérico, indexamos los headers
    if (s.kind === 'text-grid') (s.items || []).forEach(it => idx.push({ kind: 'Concepto', text: it.h, sub: (it.b || '').slice(0, 80), id: 'sec-' + s.id }));
  });
  (MAP.connections || []).forEach(c => idx.push({ kind: 'Mapa relacionado', text: c.label, sub: c.via, id: null }));
  return idx;
}
const searchIndex = [];

function renderPaletteResults(q) {
  const query = q.toLowerCase().trim();
  if (!query) {
    pResults.innerHTML = `
      <div class="pal-group-title">Secciones</div>
      ${searchIndex.filter(i => i.kind === 'Sección').map(i =>
        `<a class="pal-item" data-id="${i.id || ''}"><div class="pal-item-t">${esc(i.text)}</div><div class="pal-item-s">${i.kind}</div></a>`
      ).join('')}
    `;
    wirePaletteItems();
    return;
  }
  const hits = searchIndex.filter(i =>
    i.text.toLowerCase().includes(query) || (i.sub && i.sub.toLowerCase().includes(query))
  ).slice(0, 20);
  if (!hits.length) {
    pResults.innerHTML = `<div class="pal-empty">Sin resultados para "${esc(q)}"</div>`;
    return;
  }
  pResults.innerHTML = hits.map(i =>
    `<a class="pal-item" data-id="${i.id || ''}"><div class="pal-item-t">${highlight(i.text, query)}</div><div class="pal-item-s">${i.kind}${i.sub ? ' · ' + highlight(i.sub, query) : ''}</div></a>`
  ).join('');
  wirePaletteItems();
  // highlight in body
  highlightInBody(query);
}
function wirePaletteItems() {
  $$('.pal-item').forEach(a => a.onclick = () => {
    const id = a.getAttribute('data-id');
    if (id) document.getElementById(id)?.scrollIntoView({ behavior: 'smooth', block: 'start' });
    closePalette();
  });
}
function highlight(text, q) {
  const esced = esc(text);
  const re = new RegExp('(' + q.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + ')', 'ig');
  return esced.replace(re, '<mark class="hit">$1</mark>');
}
function highlightInBody(q) {
  $$('mark.hit').forEach(m => { const t = document.createTextNode(m.textContent); m.replaceWith(t); m.parentNode?.normalize(); });
  if (q.length < 2) return;
  const re = new RegExp('(' + q.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + ')', 'ig');
  const walker = document.createTreeWalker($('#fichaContent'), NodeFilter.SHOW_TEXT, null);
  const toWrap = [];
  let node;
  while (node = walker.nextNode()) {
    if (node.parentElement.closest('script, style')) continue;
    if (re.test(node.textContent)) toWrap.push(node);
    re.lastIndex = 0;
  }
  toWrap.forEach(n => {
    const span = document.createElement('span');
    span.innerHTML = n.textContent.replace(re, '<mark class="hit">$1</mark>');
    n.replaceWith(...span.childNodes);
  });
}

pInput.addEventListener('input', e => renderPaletteResults(e.target.value));

// Keybinds
document.addEventListener('keydown', e => {
  if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') {
    e.preventDefault(); openPalette();
  } else if (e.key === 'Escape') {
    if (palette.classList.contains('visible')) closePalette();
    else closeDrawers();
  }
});

// ============ TWEAKS ============
const TWEAK_DEFAULTS = /*EDITMODE-BEGIN*/{
  "theme": "amboss",
  "density": "comfortable",
  "bodyfont": "sans",
  "cards": "off"
}/*EDITMODE-END*/;
let tweakState = { ...TWEAK_DEFAULTS };

function applyTweaks(s) {
  document.body.setAttribute('data-theme', s.theme);
  document.body.setAttribute('data-density', s.density);
  document.body.setAttribute('data-bodyfont', s.bodyfont);
  document.body.classList.toggle('cards-on', s.cards === 'on');
  $$('.tweak-opt').forEach(b => {
    const group = b.parentElement.getAttribute('data-group');
    b.classList.toggle('active', b.getAttribute('data-value') === s[group]);
  });
}

window.addEventListener('message', e => {
  if (e.data?.type === '__activate_edit_mode') $('#tweaks').classList.add('visible');
  else if (e.data?.type === '__deactivate_edit_mode') $('#tweaks').classList.remove('visible');
});
window.parent.postMessage({ type: '__edit_mode_available' }, '*');

$$('.tweak-opt').forEach(btn => {
  btn.addEventListener('click', () => {
    const group = btn.parentElement.getAttribute('data-group');
    tweakState[group] = btn.getAttribute('data-value');
    applyTweaks(tweakState);
    window.parent.postMessage({ type: '__edit_mode_set_keys', edits: { [group]: tweakState[group] } }, '*');
  });
});

// ============ VIEW TOGGLE + MAP PICKER ============
function setView(v) {
  document.body.classList.toggle('view-mapa', v === 'mapa');
  $$('.vt-btn').forEach(b => b.classList.toggle('active', b.getAttribute('data-view') === v));
  localStorage.setItem('medmaps.view', v);
  if (v === 'mapa' && window.MindMap) {
    window.MindMap.render(MAP);
  }
}
$$('.vt-btn').forEach(b => b.onclick = () => setView(b.getAttribute('data-view')));

const picker = $('#mapPicker');
if (picker) {
  picker.onchange = async () => {
    const val = picker.value;
    localStorage.setItem('medmaps.map', val);
    // Si es legacy hardcoded, cambio sin recargar página
    if (LEGACY_MAPS[val]) {
      MAP = LEGACY_MAPS[val];
    } else if (window.MedMapsData) {
      try {
        MAP = await window.MedMapsData.loadMap(val);
      } catch (e) {
        console.error('Error cargando', val, e);
        return;
      }
    }
    // Actualizar URL sin recargar (para deep-linking)
    const newURL = location.pathname + '?id=' + encodeURIComponent(val);
    history.replaceState(null, '', newURL);
    updateCrumbs();
    renderFicha();
    $('#tocList').innerHTML = '';
    renderToc();
    renderConn();
    setupScrollSpy();
    searchIndex.length = 0;
    searchIndex.push(...buildIndex());
    if (document.body.classList.contains('view-mapa')) window.MindMap.render(MAP);
  };
}

// ============ BIBLIOTECA NAVIGATION ============
function updateCrumbs() {
  if (!MAP) return;
  const cur = document.querySelector('.crumbs .current');
  if (cur) cur.textContent = MAP.title;
  const specCrumbs = document.querySelectorAll('.crumbs a');
  if (specCrumbs[1]) specCrumbs[1].textContent = MAP.specialty || '—';
  document.title = MAP.title + ' — MedMaps';
}

async function populatePicker() {
  if (!picker || !window.MedMapsData) return;
  try {
    const idx = await window.MedMapsData.loadIndex();
    // Agrupar por especialidad para el <select>
    const bySpec = {};
    idx.forEach(m => {
      (bySpec[m.specialty] = bySpec[m.specialty] || []).push(m);
    });
    const fragments = [];
    // Primero, los legacy hardcoded si existen
    if (window.MAP_FA) fragments.push(`<option value="fa">★ Fibrilación auricular (curado)</option>`);
    if (window.MAP_INPH) fragments.push(`<option value="inph">★ Hidrocefalia normotensiva (curado)</option>`);
    // Luego el resto agrupado
    Object.keys(bySpec).sort().forEach(spec => {
      fragments.push(`<optgroup label="${esc(spec)}">`);
      bySpec[spec].slice(0, 200).forEach(m => {
        fragments.push(`<option value="${esc(m.id)}">${esc(m.title)}</option>`);
      });
      fragments.push(`</optgroup>`);
    });
    picker.innerHTML = fragments.join('');
    if (MAP) picker.value = MAP.id;
  } catch (e) {
    console.warn('Picker: no pude cargar maps_index.json', e);
  }
}

// ============ INIT ============
async function init() {
  MAP = await resolveMap();
  if (!MAP) {
    document.getElementById('fichaContent').innerHTML =
      '<div style="padding:2rem;text-align:center;color:#a00">No se pudo cargar el mapa. <a href="index.html">Volver a la biblioteca</a></div>';
    return;
  }
  updateCrumbs();
  renderFicha();
  renderToc();
  renderConn();
  setupScrollSpy();
  searchIndex.push(...buildIndex());
  applyTweaks(tweakState);
  const savedView = localStorage.getItem('medmaps.view') || 'ficha';
  setView(savedView);
  await populatePicker();
}

window.addEventListener('resize', () => {
  /* mindmap handles its own resize via positionHorizontalBus */
});

init();
