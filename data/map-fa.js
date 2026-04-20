// ============ FIBRILACIÓN AURICULAR — FICHA DE ESTUDIO ============
// Dataset hardcodeado estilo AMBOSS, denso, con cross-links a otros mapas
window.MAP_FA = {
  id: "fa",
  title: "Fibrilación auricular",
  subtitle: "Taquiarritmia supraventricular · Prevalencia 2–4% adultos · CIE-10 I48",
  specialty: "Cardiología",
  related: ["Medicina Interna", "Urgencias"],
  sources: ["ESC 2024", "AHA/ACC/HRS 2023", "Lancet 2022"],
  reading_min: 12,

  one_liner: "Taquiarritmia auricular rápida e irregular, sin ondas P, con riesgo tromboembólico dependiente de CHA₂DS₂-VASc. Manejo: anticoagular + control de ritmo o frecuencia.",

  redflags: [
    { t: "Inestabilidad hemodinámica", d: "hipoTA, shock, SCA, EAP → CVE inmediata" },
    { t: "FA + WPW (pre-excitación)", d: "NO dar BB / CA / digoxina / adenosina → FV. Usar procainamida o CVE" },
    { t: "FC > 150 + dolor torácico + elevación troponina", d: "SCA concomitante" },
    { t: "FA de inicio < 48h con signos focales", d: "Descartar ACV cardioembólico" },
    { t: "HASBLED ≥ 3 sin corregir factores modificables", d: "Revisar TA, INR, OH, AINES antes de escalar ACO" },
  ],

  sections: [
    {
      id: "def",
      icon: "◉",
      title: "Definición y clasificación",
      kind: "text-grid",
      items: [
        { h: "Definición", b: "Taquiarritmia supraventricular con activación auricular desorganizada (350–600 lpm) → pérdida de sístole auricular efectiva y respuesta ventricular irregular." },
        { h: "ECG", b: "Ausencia de ondas P · ondas f irregulares · R-R irregularmente irregular · QRS estrecho (salvo aberrancia o pre-excitación)." },
        { h: "FA paroxística", b: "Termina espontáneamente o con intervención en < 7 días. Típicamente < 48h." },
        { h: "FA persistente", b: "> 7 días o requiere cardioversión. Persistente de larga data: > 1 año." },
        { h: "FA permanente", b: "Aceptada por paciente + médico, no se intenta restaurar ritmo sinusal." },
        { h: "FA valvular", b: "Estenosis mitral moderada-severa o prótesis mecánica → warfarina obligada, no DOAC." },
      ]
    },
    {
      id: "epi",
      icon: "◉",
      title: "Epidemiología & factores",
      kind: "two-col",
      left: {
        h: "Prevalencia",
        items: [
          "2–4% población adulta · ↑ con edad",
          "≥ 75 años: 10–17%",
          "Hombres > mujeres (pero ACV ↑ en ♀)",
          "Proyección 2050: duplicación de casos"
        ]
      },
      right: {
        h: "Factores de riesgo",
        items: [
          "HTA (factor #1, 60% casos)",
          "Edad avanzada",
          "Insuficiencia cardíaca",
          "Obesidad · IMC ≥ 30 (RR 1.5)",
          "SAHOS · alcohol · tabaco",
          "Hipertiroidismo · DM2 · ERC",
          "Valvulopatía · cirugía cardíaca reciente"
        ]
      }
    },
    {
      id: "score-cha",
      icon: "▦",
      title: "CHA₂DS₂-VASc",
      kind: "score",
      intro: "Estima riesgo anual de ACV/embolia sistémica en FA no valvular. Define indicación de ACO.",
      rows: [
        ["C", "IC / disfunción VI (FEVI ≤ 40%)", "1"],
        ["H", "Hipertensión arterial", "1"],
        ["A₂", "Edad ≥ 75 años", "2"],
        ["D", "Diabetes mellitus", "1"],
        ["S₂", "ACV / AIT / tromboembolia previa", "2"],
        ["V", "Enfermedad vascular (IAM, EAP, placa Ao)", "1"],
        ["A", "Edad 65–74 años", "1"],
        ["Sc", "Sexo femenino (solo si otro factor presente)", "1"],
      ],
      bands: [
        { range: "0 ♂ / 1 ♀", risk: "0.2%/año", action: "No anticoagular" },
        { range: "1 ♂", risk: "0.6%/año", action: "Considerar ACO (clase IIa)" },
        { range: "≥ 2", risk: "2.2–15%/año", action: "ACO indicada (clase I)" },
      ]
    },
    {
      id: "score-has",
      icon: "▦",
      title: "HAS-BLED",
      kind: "score",
      intro: "Riesgo de sangrado mayor anual. ≥ 3 = alto riesgo; NO contraindica ACO, sino exige corregir factores modificables.",
      rows: [
        ["H", "Hipertensión no controlada (TAS > 160)", "1"],
        ["A", "Función renal o hepática anormal", "1+1"],
        ["S", "Stroke previo", "1"],
        ["B", "Bleeding previo o predisposición", "1"],
        ["L", "INR lábil (TTR < 60%)", "1"],
        ["E", "Edad > 65 años", "1"],
        ["D", "Drogas (AAS/AINE) o alcohol (≥8/sem)", "1+1"],
      ],
      bands: [
        { range: "0–2", risk: "Bajo (< 2%/año)", action: "ACO sin reparos" },
        { range: "≥ 3", risk: "Alto (> 4%/año)", action: "Corregir modificables · vigilar · NO suspender ACO" },
      ]
    },
    {
      id: "dx",
      icon: "◉",
      title: "Diagnóstico",
      kind: "steps",
      steps: [
        { n: "01", h: "ECG 12 derivaciones", b: "Confirma FA (ausencia P + R-R irregular). Si episodio breve: Holter 24–72h, event-recorder o dispositivo implantable." },
        { n: "02", h: "Eco TT", b: "FEVI, tamaño AI (> 45 mm predice recurrencia), valvulopatías, cardiopatía estructural." },
        { n: "03", h: "Labs", b: "TSH, hemograma, creatinina (eGFR para dosis DOAC), ionograma, perfil hepático, NT-proBNP opcional." },
        { n: "04", h: "Eco TE si CVE o ablación", b: "Descartar trombo en orejuela izquierda si no ha completado 3 sem de ACO o inicio FA > 48h." },
        { n: "05", h: "Búsqueda etiología secundaria", b: "SAHOS (poligrafía), tirotoxicosis, abuso OH, hipokalemia, hipoMg." },
      ]
    },
    {
      id: "tx-frame",
      icon: "⚕",
      title: "Estrategia — framework ABC",
      kind: "framework",
      intro: "ESC 2024: 'AF-CARE' pathway. Simplificado a 3 pilares obligatorios.",
      pillars: [
        { letter: "A", title: "Anticoagulación", sub: "Prevenir ACV · CHA₂DS₂-VASc ≥ 2 ♂ / ≥ 3 ♀ → ACO. DOAC > warfarina salvo FA valvular." },
        { letter: "B", title: "Better symptom control", sub: "Control FC (< 110 permisivo; < 80 estricto si sintomático) y/o control ritmo (ablación/CVE/antiarrítmicos)." },
        { letter: "C", title: "Comorbilidades", sub: "HTA, IC, DM, obesidad, SAHOS, OH. Agresivo: reduce recurrencia 40–50%." },
      ]
    },
    {
      id: "tx-aco",
      icon: "💊",
      title: "Anticoagulación — fármacos y dosis",
      kind: "drugs",
      drugs: [
        { name: "Apixabán", dose: "5 mg c/12h VO", adjust: "2.5 mg c/12h si ≥ 2 de: ≥ 80 años · ≤ 60 kg · Cr ≥ 1.5", class: "DOAC · Xa", notes: "Menor sangrado GI. Preferido en ERC (hasta ClCr 15)." },
        { name: "Rivaroxabán", dose: "20 mg c/24h con comida", adjust: "15 mg si ClCr 15–49", class: "DOAC · Xa", notes: "1 toma/día favorece adherencia." },
        { name: "Dabigatrán", dose: "150 mg c/12h VO", adjust: "110 mg si ≥ 80 a o ClCr 30–49", class: "DOAC · IIa", notes: "Antídoto: idarucizumab. Evitar si ClCr < 30." },
        { name: "Edoxabán", dose: "60 mg c/24h", adjust: "30 mg si ClCr 15–50 o ≤ 60 kg", class: "DOAC · Xa", notes: "No usar si ClCr > 95 (eficacia ↓)." },
        { name: "Warfarina", dose: "Ajuste por INR 2–3", adjust: "INR 2.5–3.5 si prótesis mecánica mitral", class: "AVK", notes: "Obligada en FA valvular. TTR ≥ 70% para ser efectiva." },
      ],
      warning: "NO combinar DOAC con AAS/clopidogrel salvo SCA reciente. Reevaluar función renal cada 6–12 meses."
    },
    {
      id: "tx-rate",
      icon: "💊",
      title: "Control de frecuencia",
      kind: "drugs",
      drugs: [
        { name: "Metoprolol", dose: "25–200 mg/día VO · 5 mg IV lento", adjust: "Repetir IV c/5 min × 3 si precisa", class: "β-bloqueante", notes: "1ra línea. Preferido si IC, HTA, SCA previo." },
        { name: "Bisoprolol", dose: "2.5–10 mg/día VO", adjust: "—", class: "β-bloqueante", notes: "Buena tolerancia, 1 toma/día." },
        { name: "Diltiazem", dose: "120–360 mg/día VO · 0.25 mg/kg IV", adjust: "—", class: "CA no-dihidropiridínico", notes: "Si β-bloqueante contraindicado (asma). EVITAR si FEVI < 40%." },
        { name: "Verapamilo", dose: "120–480 mg/día", adjust: "—", class: "CA no-dihidropiridínico", notes: "Igual que diltiazem. Constipación frecuente." },
        { name: "Digoxina", dose: "0.125–0.25 mg/día VO", adjust: "↓ en ERC y edad avanzada", class: "Glucósido", notes: "Adyuvante. Útil en IC con FEVI ↓. No monoterapia en paciente activo." },
        { name: "Amiodarona", dose: "150 mg IV bolo + 1 mg/min × 6h", adjust: "Luego 0.5 mg/min × 18h", class: "Clase III", notes: "Último recurso para control FC agudo si IC severa o hipoTA." },
      ],
    },
    {
      id: "tx-rhythm",
      icon: "⚡",
      title: "Control de ritmo — algoritmo agudo",
      kind: "algorithm",
      start: "FA aguda sintomática",
      steps: [
        { q: "¿Inestable? (hipoTA, shock, SCA, EAP)", yes: "CVE sincronizada 120–200 J", no: "siguiente" },
        { q: "¿WPW / pre-excitación?", yes: "Procainamida 10 mg/kg IV o CVE. NO BB/CA/digoxina/adenosina", no: "siguiente" },
        { q: "¿Inicio < 48h O anticoagulado ≥ 3 sem O ETE sin trombo?", yes: "Cardioversión farmacológica o eléctrica electiva", no: "Anticoagular 3 sem → CVE → ACO ≥ 4 sem post" },
      ],
      pharma_cv: [
        { name: "Flecainida", dose: "200–300 mg VO (pill-in-pocket) o 2 mg/kg IV", note: "Solo si no hay cardiopatía estructural." },
        { name: "Propafenona", dose: "450–600 mg VO", note: "Idem flecainida. Combinar con β-bloq para evitar flutter 1:1." },
        { name: "Amiodarona", dose: "150 mg IV + 1 mg/min × 6h", note: "Preferida si cardiopatía estructural o IC." },
        { name: "Vernakalant", dose: "3 mg/kg IV × 10 min", note: "Rápido (< 10 min). No si hipoTA, SCA, IC NYHA III-IV." },
      ]
    },
    {
      id: "ablation",
      icon: "⚕",
      title: "Ablación & intervenciones",
      kind: "text-grid",
      items: [
        { h: "Ablación con catéter (AVP)", b: "Aislamiento venas pulmonares. Clase I en FA paroxística sintomática refractaria a ≥1 antiarrítmico. Eficacia: 70–80% a 1 año." },
        { h: "EAST-AFNET 4 (2020)", b: "Control ritmo temprano (< 1 año del dx) reduce eventos CV vs manejo convencional. Indicación ampliada." },
        { h: "Crioablación vs radiofrecuencia", b: "Similares en eficacia. CRYO más rápida, RF más versátil en anatomías complejas." },
        { h: "Cierre orejuela izq (WATCHMAN, Amulet)", b: "Alternativa a ACO si contraindicación absoluta (sangrado mayor recurrente). PROTECT-AF, PREVAIL." },
        { h: "Cirugía maze / ablación concomitante", b: "En cirugía cardíaca por otra indicación." },
      ]
    },
    {
      id: "pearls",
      icon: "✦",
      title: "Perlas clínicas · errores frecuentes",
      kind: "pearls",
      items: [
        { t: "No dar digoxina monoterapia en paciente activo", d: "Solo controla FC en reposo, no en ejercicio. Combinar con β-bloq." },
        { t: "FA + WPW: jamás BB/CA/digoxina/adenosina", d: "Bloquean el nodo AV → conducción preferente por vía accesoria → FV. Procainamida o CVE." },
        { t: "FA rápida en IC descompensada: la taquicardia NO es el enemigo inicial", d: "La IC causa la FA rápida, no al revés. Trata la IC primero (diuréticos); la FC cae sola." },
        { t: "Anticoagular antes de CVE si > 48h o duración desconocida", d: "Mínimo 3 sem previo + 4 sem post. O ETE sin trombo → CVE inmediata + ACO ≥ 4 sem." },
        { t: "Mujer joven con FA sin FR: descarta tirotoxicosis y OH", d: "Causas reversibles frecuentes. TSH + historia dirigida." },
        { t: "CHA₂DS₂-VASc es para NO-valvular", d: "Si estenosis mitral moderada-severa o prótesis mecánica → warfarina directamente, sin score." },
        { t: "Un HASBLED alto NO contraindica ACO", d: "Identifica factores corregibles: TA, OH, AINES, INR lábil." },
        { t: "DOAC y ERC: apixabán es el más permisivo", d: "Aprobado hasta ClCr 15. Rivaroxabán/edoxabán requieren ajuste. Dabigatrán evitar < 30." },
      ]
    },
    {
      id: "studies",
      icon: "📚",
      title: "Estudios pivotales",
      kind: "studies",
      items: [
        { yr: "2009", name: "RE-LY", q: "Dabigatrán vs warfarina en FA no valvular", res: "Dabi 150 mg: ↓ 35% ACV vs warfarina. Dabi 110 mg: no inferior, menor sangrado.", trial: "18.113 pts" },
        { yr: "2011", name: "ROCKET-AF", q: "Rivaroxabán vs warfarina", res: "No inferior para ACV/embolia. Menor HIC.", trial: "14.264 pts" },
        { yr: "2011", name: "ARISTOTLE", q: "Apixabán vs warfarina", res: "↓ 21% ACV · ↓ 31% sangrado mayor · ↓ mortalidad total.", trial: "18.201 pts · landmark" },
        { yr: "2013", name: "ENGAGE AF-TIMI 48", q: "Edoxabán vs warfarina", res: "Dosis altas no inferiores, menor sangrado.", trial: "21.105 pts" },
        { yr: "2020", name: "EAST-AFNET 4", q: "Control ritmo temprano vs convencional", res: "↓ eventos CV en pts dx hace < 1 año.", trial: "2.789 pts" },
        { yr: "2021", name: "EARLY-AF", q: "Crioablación 1ra línea vs antiarrítmico", res: "Menos recurrencias con ablación directa.", trial: "303 pts" },
      ]
    }
  ],

  // Red de conexiones — este mapa ↔ otros
  connections: [
    { to: "anticoagulacion", label: "Anticoagulación", via: "ACO · DOAC · warfarina", strength: 3 },
    { to: "acv", label: "ACV isquémico", via: "Cardioembolia · CHA₂DS₂-VASc", strength: 3 },
    { to: "icc", label: "Insuficiencia cardíaca crónica", via: "Comorbilidad frecuente · ABC pathway", strength: 3 },
    { to: "flutter", label: "Flutter auricular", via: "Manejo agudo similar · ablación istmo", strength: 2 },
    { to: "wpw", label: "Síndrome WPW", via: "⚠️ Contraindicación BB/CA/digoxina", strength: 2 },
    { to: "hta", label: "Hipertensión arterial", via: "Factor de riesgo #1", strength: 2 },
    { to: "sahos", label: "SAHOS", via: "Factor modificable · recurrencia", strength: 2 },
    { to: "erc", label: "Enfermedad renal crónica", via: "Ajuste de DOAC", strength: 2 },
    { to: "tiroides", label: "Hipertiroidismo", via: "Causa reversible", strength: 1 },
    { to: "sca", label: "Síndrome coronario agudo", via: "Triple terapia · ajuste ACO", strength: 2 },
  ]
};
