/* ============ MEDMAPS DATA LOADER ============
 *
 * Puente entre el JSON crudo del pipeline (medmaps_sync.py) y el formato
 * rico que espera el viewer.
 *
 * Input: { title, specialty, folder, root: { id, text, children:[...] } }
 *   — el árbol SimpleMind genérico, con `\n` y `\\N` como separadores intra-nodo.
 *
 * Output: { id, title, subtitle, specialty, related, sources, reading_min,
 *           one_liner, redflags, sections, connections }
 *   — el shape que renderFicha() y MindMap.render() esperan.
 *
 * Filosofía: el mapa rico (map-fa.js) tiene `kind` por sección (drugs, score,
 * steps…). El mapa genérico no sabe su tipo — le damos `kind: "text-grid"` y
 * tratamos cada hijo directo del root como una sección, cada nieto como item.
 *
 * Detecciones heurísticas opt-in:
 *   - Sección cuyo título incluye "red flag" / "urgenc" / "alerta" → redflags
 *   - Sección cuyo título incluye "dosis" / "fármac" / "drug" / "trat"
 *     con items de estructura `Nombre: Dosis` → drugs (simplificada)
 *   - Por defecto: text-grid
 */

(function () {
  'use strict';

  const SEP_CAP = String.fromCharCode(92) + 'N';
  const SEP_LOW = String.fromCharCode(92) + 'n';
  const SEP_CR = String.fromCharCode(92) + 'r';

  function cleanText(raw) {
    if (!raw) return '';
    let t = String(raw);
    t = t.split(SEP_CAP).join('\n')
         .split(SEP_LOW).join('\n')
         .split(SEP_CR).join('\n');
    t = t.replace(/\r\n?/g, '\n');
    t = t.split('\n').map(l => l.replace(/\s+$/, '')).join('\n');
    t = t.replace(/^\n+|\n+$/g, '');
    return t;
  }

  function firstLine(text) {
    const c = cleanText(text);
    const nl = c.indexOf('\n');
    return nl < 0 ? c : c.slice(0, nl);
  }

  function restLines(text) {
    const c = cleanText(text);
    const nl = c.indexOf('\n');
    return nl < 0 ? '' : c.slice(nl + 1).trim();
  }

  // Aplana sub-árbol a texto plano (para items hoja con detalle anidado)
  function flattenBranch(node, depth = 0) {
    if (!node) return '';
    const out = [];
    const text = cleanText(node.text || '');
    if (text) out.push(text);
    (node.children || []).forEach(c => {
      const sub = flattenBranch(c, depth + 1);
      if (sub) {
        // indent para estructura
        const lines = sub.split('\n').map(l => (depth === 0 ? '— ' : '  ') + l);
        out.push(lines.join('\n'));
      }
    });
    return out.join('\n');
  }

  // Derivación de kind basado en título de sección
  function inferKind(title) {
    const t = title.toLowerCase();
    if (/red\s*flag|urgenc|alerta|alarm/.test(t)) return 'redflags-like';
    if (/dosi|f[aá]rmac|drug|tratam/.test(t)) return 'drugs-like';
    if (/paso|step|algorit|flujo/.test(t)) return 'steps-like';
    if (/score|puntaje|escala|cha|has|grace|tims/.test(t)) return 'score-like';
    if (/perla|pearl|clave|clinical|tip/.test(t)) return 'pearls-like';
    if (/estudio|trial|stud|evidencia/.test(t)) return 'studies-like';
    return 'generic';
  }

  // Transforma un item (hijo de sección) a estructura text-grid
  function itemToTextGrid(child) {
    const text = cleanText(child.text || '');
    const header = firstLine(text);
    const rest = restLines(text);
    const childDetails = (child.children || [])
      .map(c => flattenBranch(c))
      .filter(Boolean)
      .join('\n\n');
    const body = [rest, childDetails].filter(Boolean).join('\n\n');
    return {
      h: header || '(sin título)',
      b: body || header
    };
  }

  // Transforma una sección (hijo directo del root)
  function buildSection(sectionNode, sectionIdx) {
    const secTitle = firstLine(sectionNode.text || '') || `Sección ${sectionIdx + 1}`;
    const kind = inferKind(secTitle);
    const id = 'sec-' + sectionIdx;

    // redflags → lista compacta de t/d
    if (kind === 'redflags-like') {
      const items = (sectionNode.children || []).map(c => {
        const tx = cleanText(c.text || '');
        const header = firstLine(tx);
        const rest = restLines(tx);
        const subs = (c.children || []).map(cc => flattenBranch(cc)).filter(Boolean).join(' · ');
        return { t: header, d: [rest, subs].filter(Boolean).join(' — ') };
      });
      return null; // redflags se extraen aparte (ver buildRedflags)
    }

    // Default: text-grid genérico
    const items = (sectionNode.children || []).map(itemToTextGrid);

    // Ícono por kind
    const icon = {
      'redflags-like': '⚠',
      'drugs-like': '💊',
      'steps-like': '◉',
      'score-like': '▦',
      'pearls-like': '✦',
      'studies-like': '🔬',
      'generic': '◉'
    }[kind] || '◉';

    return {
      id,
      icon,
      title: secTitle,
      kind: 'text-grid',
      items: items.length ? items : [{ h: secTitle, b: restLines(sectionNode.text || '') || '(vacío)' }]
    };
  }

  // Extrae redflags del árbol (primera sección con título "red flag/urgencia/alarma")
  function buildRedflags(root) {
    const match = (root.children || []).find(c => {
      const t = firstLine(c.text || '').toLowerCase();
      return /red\s*flag|urgenc|alerta|alarm/.test(t);
    });
    if (!match) return [];
    return (match.children || []).map(c => {
      const tx = cleanText(c.text || '');
      const header = firstLine(tx);
      const rest = restLines(tx);
      const subs = (c.children || []).map(cc => flattenBranch(cc)).filter(Boolean).join(' · ');
      return {
        t: header || '(sin título)',
        d: [rest, subs].filter(Boolean).join(' — ') || ''
      };
    });
  }

  // Transformación principal
  function transformRawMap(raw) {
    if (!raw || !raw.root) {
      throw new Error('Mapa sin root: ' + JSON.stringify(raw).slice(0, 200));
    }

    const root = raw.root;
    const rootText = cleanText(root.text || '');
    const title = raw.title || firstLine(rootText) || '(sin título)';
    const subtitle = restLines(rootText) || '';

    // Red flags primero (si existen, se excluyen de las secciones normales)
    const redflags = buildRedflags(root);
    const redflagIdx = redflags.length
      ? (root.children || []).findIndex(c => /red\s*flag|urgenc|alerta|alarm/.test(firstLine(c.text || '').toLowerCase()))
      : -1;

    const sectionChildren = (root.children || []).filter((_, i) => i !== redflagIdx);
    const sections = sectionChildren.map((c, i) => buildSection(c, i)).filter(Boolean);

    const specialty = raw.specialty || 'General';
    const folder = raw.folder || '';
    const nodeCount = raw.node_count || 0;
    const readingMin = Math.max(3, Math.round(nodeCount / 30));

    return {
      id: raw.id || raw.filename || 'map',
      title,
      subtitle: subtitle.split('\n')[0] || `${specialty} · ${nodeCount} nodos`,
      specialty,
      related: folder && folder !== specialty ? [folder] : [],
      sources: raw.resolved_references && raw.resolved_references.length
        ? raw.resolved_references.slice(0, 3).map(r => r.short || r.title || r.id).filter(Boolean)
        : [],
      reading_min: readingMin,
      one_liner: subtitle || `Mapa mental de ${specialty}. ${nodeCount} conceptos.`,
      redflags: redflags.length ? redflags : [
        { t: 'Sin red flags explícitas', d: 'Revisar sección correspondiente en el mapa original' }
      ],
      sections,
      connections: (raw.cross_references || []).slice(0, 8).map(cr => ({
        label: cr.title || cr.id || cr,
        via: cr.via || 'Cross-reference',
        strength: 2,
        to: cr.id || ''
      }))
    };
  }

  // === PUBLIC API ===

  async function fetchJSON(path) {
    const url = `data/${path}`;
    const r = await fetch(url);
    if (!r.ok) throw new Error(`HTTP ${r.status} al cargar ${url}`);
    return await r.json();
  }

  async function loadIndex() {
    return await fetchJSON('maps_index.json');
  }

  async function loadSpecialties() {
    try { return await fetchJSON('specialties.json'); }
    catch (e) { return null; }
  }

  async function loadMap(mapId) {
    const raw = await fetchJSON(`maps/${mapId}.json`);
    return transformRawMap(raw);
  }

  // Para testing local: permite pasar un mapa ya cargado
  function fromRaw(rawMap) {
    return transformRawMap(rawMap);
  }

  window.MedMapsData = {
    loadIndex,
    loadSpecialties,
    loadMap,
    fromRaw,
    transformRawMap,
    _utils: { cleanText, firstLine, restLines, flattenBranch, inferKind }
  };
})();
