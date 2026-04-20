/* ============ MIND MAP RENDERER ============ */
/* Vertical tree. Branch pill → toggles list of leaves.
   Each leaf shows: title + short synthetic summary. Tap → expands inline with full detail. */

// Color by content type — consistent across all maps
const KIND_COLOR = {
  redflags:    '#c53030', // red — alertas
  'text-grid': '#0072c6', // blue — contexto/definiciones
  'two-col':   '#0072c6',
  steps:       '#0a7248', // green — procedimiento
  algorithm:   '#0a7248',
  score:       '#b45309', // amber — scores/estratificación
  drugs:       '#6d28d9', // purple — farmacología
  framework:   '#0891b2', // teal — estrategia/abordaje
  pearls:      '#a16207', // ochre — perlas
  studies:     '#4f46e5'  // indigo — evidencia
};

// Keep summary line short & information-dense.
const SUMMARY_MAX = 90;

function shortSummary(txt) {
  if (!txt) return '';
  let s = String(txt).replace(/\s+/g, ' ').trim();
  // Take up to first sentence or until max length
  const firstStop = s.search(/[.;]\s/);
  if (firstStop > 20 && firstStop < SUMMARY_MAX + 10) s = s.slice(0, firstStop);
  if (s.length > SUMMARY_MAX) s = s.slice(0, SUMMARY_MAX).replace(/\s\S*$/, '') + '…';
  return s;
}

const MindMap = {
  map: null,
  root: null,
  expanded: new Set(),          // branch indices open
  expandedLeaves: new Map(),    // key "bi-li" → bool

  render(map) {
    this.map = map;
    const canvas = document.getElementById('mindmapCanvas');
    this.root = canvas;
    this.expanded.clear();
    this.expandedLeaves.clear();

    // Construye lista de secciones, anteponiendo red flags si tienen contenido real
    const sections = [];
    const rf = this.map.redflags || [];
    const rfReal = rf.length && !(rf.length === 1 && /sin red flags/i.test(rf[0].t || ''));
    if (rfReal) {
      sections.push({ id: 'redflags', title: 'Red flags', kind: 'redflags', items: rf });
    }
    sections.push(...(this.map.sections || []));

    this.branchData = sections.map(sec => ({
      sec,
      color: KIND_COLOR[sec.kind] || '#0072c6',
      leaves: this.summarize(sec)
    }));

    const branchesHtml = this.branchData.map((b, i) => `
      <div class="tree-node" data-branch="${i}" style="--branch-c:${b.color}">
        <button class="tree-branch" data-branch="${i}" aria-expanded="false">
          <span class="tree-branch-title">${esc(b.sec.title)}</span>
          <span class="tree-branch-count">${b.leaves.length}</span>
          <span class="tree-branch-chev" aria-hidden="true">▾</span>
        </button>
        <div class="tree-leaves" data-branch-leaves="${i}" hidden>
          <ul class="tree-leaves-list">
            ${b.leaves.map((l, idx) => this.renderLeaf(l, i, idx)).join('')}
          </ul>
        </div>
      </div>
    `).join('');

    canvas.innerHTML = `
      <div class="tree-layout">
        <div class="tree-root-wrap">
          <div class="tree-root">
            <div class="tree-root-tag">${esc(this.map.specialty)}</div>
            <div class="tree-root-title">${esc(this.map.title)}</div>
          </div>
        </div>
        <div class="tree-branches" id="treeBranches">
          ${branchesHtml}
        </div>
      </div>
    `;

    this.bindEvents();
  },

  renderLeaf(l, bi, li) {
    // If the summary captured essentially all of the detail, don't make it expandable
    const hasMoreThanSummary = l.detail && l.summary
      ? this.detailExceedsSummary(l.detail, l.summary)
      : !!l.detail;
    const interactive = hasMoreThanSummary;
    const summary = l.summary ? `<span class="tree-leaf-summary">${esc(l.summary)}</span>` : '';
    return `
      <li class="tree-leaf${interactive ? ' tree-leaf-interactive' : ''}"
          data-branch="${bi}" data-leaf="${li}"
          tabindex="${interactive ? 0 : -1}"
          aria-expanded="false">
        <div class="tree-leaf-head">
          <div class="tree-leaf-main">
            <span class="tree-leaf-label">${esc(l.label)}</span>
            ${summary}
          </div>
          ${interactive ? '<span class="tree-leaf-chev" aria-hidden="true">▾</span>' : ''}
        </div>
        ${interactive ? `<div class="tree-leaf-detail" hidden>${l.detail}</div>` : ''}
      </li>
    `;
  },

  detailExceedsSummary(detailHtml, summary) {
    // Strip tags and compare length
    const plain = detailHtml.replace(/<[^>]*>/g, '').replace(/&[a-z]+;/gi, ' ').replace(/\s+/g, ' ').trim();
    // If the detail is <= 10% longer than the summary, consider it redundant
    return plain.length > summary.length * 1.15 + 10;
  },

  bindEvents() {
    // Branch toggle
    this.root.querySelectorAll('.tree-branch').forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.stopPropagation();
        const i = +btn.dataset.branch;
        const leaves = this.root.querySelector(`[data-branch-leaves="${i}"]`);
        const isOpen = this.expanded.has(i);
        if (isOpen) {
          this.expanded.delete(i);
          leaves.hidden = true;
          btn.setAttribute('aria-expanded', 'false');
          btn.classList.remove('is-open');
        } else {
          this.expanded.add(i);
          leaves.hidden = false;
          btn.setAttribute('aria-expanded', 'true');
          btn.classList.add('is-open');
        }
      });
    });

    // Leaf toggle (accordion inline)
    this.root.querySelectorAll('.tree-leaf-interactive').forEach(leafEl => {
      const toggle = (e) => {
        if (e) e.stopPropagation();
        const detail = leafEl.querySelector('.tree-leaf-detail');
        if (!detail) return;
        const isOpen = !detail.hidden;
        if (isOpen) {
          detail.hidden = true;
          leafEl.setAttribute('aria-expanded', 'false');
          leafEl.classList.remove('is-open');
        } else {
          detail.hidden = false;
          leafEl.setAttribute('aria-expanded', 'true');
          leafEl.classList.add('is-open');
        }
      };
      leafEl.addEventListener('click', toggle);
      leafEl.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          toggle(e);
        }
      });
    });
  },

  summarize(sec) {
    const br = s => esc(s).replace(/\n/g, '<br>');

    if (sec.kind === 'redflags') {
      return sec.items.map(r => ({
        label: r.t,
        summary: shortSummary(r.d),
        detail: r.d ? `<p>${br(r.d)}</p>` : null
      }));
    }

    if (sec.kind === 'text-grid') {
      return sec.items.map(i => ({
        label: i.h,
        summary: shortSummary(i.b),
        detail: i.b ? `<p>${br(i.b)}</p>` : null
      }));
    }

    if (sec.kind === 'two-col') {
      const L = sec.left.items.map(t => ({ label: t, section: sec.left.h }));
      const R = sec.right.items.map(t => ({ label: t, section: sec.right.h }));
      return [...L, ...R].map(it => ({
        label: it.label,
        summary: it.section,
        detail: `<p class="mm-leaf-ctx">${esc(it.section)}</p>`
      }));
    }

    if (sec.kind === 'score') {
      return sec.rows.map(r => ({
        label: r[0],
        summary: `${r[1]} pts${r[2] ? ' · ' + shortSummary(r[2]) : ''}`,
        detail: `<p><b>Puntos:</b> ${esc(r[1])}</p>${r[2] ? `<p>${br(r[2])}</p>` : ''}`
      }));
    }

    if (sec.kind === 'steps') {
      return sec.steps.map(s => ({
        label: `${s.n}. ${s.h}`,
        summary: shortSummary(s.b),
        detail: s.b ? `<p>${br(s.b)}</p>` : null
      }));
    }

    if (sec.kind === 'framework') {
      return sec.pillars.map(p => ({
        label: `${p.letter} — ${p.title}`,
        summary: shortSummary(p.sub),
        detail: p.sub ? `<p>${br(p.sub)}</p>` : null
      }));
    }

    if (sec.kind === 'drugs') {
      return sec.drugs.map(d => ({
        label: d.name,
        summary: d.dose ? shortSummary(d.dose) : shortSummary(d.notes),
        detail: `${d.dose ? `<p class="mm-leaf-dose">${br(d.dose)}</p>` : ''}${d.notes ? `<p>${br(d.notes)}</p>` : ''}`
      }));
    }

    if (sec.kind === 'algorithm') {
      return sec.steps.map(s => {
        const yText = typeof s.y === 'string' ? s.y : (s.y && s.y.t) || '';
        return {
          label: s.q,
          summary: shortSummary(yText),
          detail: s.y ? `<p><b>Sí →</b> ${br(yText)}</p>${s.y && s.y.d ? `<p>${br(s.y.d)}</p>` : ''}` : null
        };
      });
    }

    if (sec.kind === 'pearls') {
      return sec.items.map(p => ({
        label: p.t,
        summary: shortSummary(p.d),
        detail: p.d ? `<p>${br(p.d)}</p>` : null
      }));
    }

    if (sec.kind === 'studies') {
      return sec.items.map(s => ({
        label: `${s.name} (${s.yr})`,
        summary: shortSummary(s.q || s.res),
        detail: `${s.q ? `<p class="mm-leaf-ctx"><em>${br(s.q)}</em></p>` : ''}${s.res ? `<p>${br(s.res)}</p>` : ''}`
      }));
    }

    return [];
  }
};

function esc(s) {
  return String(s == null ? '' : s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
}

window.MindMap = MindMap;
