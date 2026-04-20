// ============ HIDROCEFALIA NORMOTENSIVA (iNPH) — FICHA ============
window.MAP_INPH = {
  id: "inph",
  title: "Hidrocefalia normotensiva (iNPH)",
  subtitle: "Síndrome de Hakim · Hidrocefalia crónica comunicante del adulto mayor · PIC 5–18 mmHg",
  specialty: "Neurología",
  related: ["Neurocirugía", "Geriatría"],
  sources: ["Hamilton 2025", "Nakajima 2021", "PENS trial"],
  reading_min: 10,

  one_liner: "Hidrocefalia comunicante crónica del adulto mayor con PIC normal. Tríada de Hakim-Adams: marcha magnética + deterioro cognitivo subcortical + incontinencia. Tratamiento: derivación ventriculoperitoneal (NNT 1.79, PENS).",

  redflags: [
    { t: "Tríada de Hakim-Adams en >65 años", d: "Marcha magnética + disfunción ejecutiva + urgencia urinaria → pensar iNPH, no 'envejecimiento'" },
    { t: "Evolución <2 años", d: "Ventana terapéutica óptima — deterioro puede volverse irreversible" },
    { t: "Evans >0.3 + DESH en RM", d: "Indicación quirúrgica alta — referir a neurocirugía" },
    { t: "Tap test negativo", d: "NO descarta iNPH — considerar drenaje lumbar externo o test de infusión" },
    { t: "Caídas recurrentes en AM con marcha magnética", d: "Riesgo-beneficio favorece evaluación quirúrgica (caídas ↓ 24% vs 46%)" },
  ],

  sections: [
    {
      id: "def", icon: "◉", title: "Definición y clasificación", kind: "text-grid",
      items: [
        { h: "Definición", b: "Hidrocefalia crónica comunicante del adulto mayor con PIC normal o levemente elevada (5–18 mmHg / 70–245 mmH₂O). Tipton 2023 propone llamarla Síndrome de Hakim." },
        { h: "Primaria (idiopática)", b: ">40 años, inicio insidioso 3–6 meses, sin causa identificable. Más frecuente con edad." },
        { h: "Secundaria", b: "HSA, meningitis, cirugía cerebral, radiación, TCE. Inicio agudo o gradual." },
        { h: "Epidemiología", b: "Prevalencia 1.5% a 65–70 años → 7.7% >86 años. Subdiagnosticada: solo 10–20% identificados. Edad media dx 70–80 años." },
      ]
    },
    {
      id: "fisio", icon: "◉", title: "Fisiopatología",
      kind: "two-col",
      left: {
        h: "Dinámica LCR",
        items: [
          "Producción normal ~500 mL/día (plexos coroideos)",
          "Reabsorción deficiente en granulaciones aracnoideas",
          "Compliance intracraneal reducida",
          "Ondas B de Lundberg en monitoreo PIC"
        ]
      },
      right: {
        h: "Teoría two-hit & glinfático",
        items: [
          "1ª noxa: infección/hemorragia perinatal → altera glía",
          "2ª noxa: enfermedad pequeño vaso → gliosis",
          "Drenaje glinfático perivascular alterado",
          "Acumulación Aβ y tau (solapa con EA)",
          "Linfáticos durales: nueva vía alterada"
        ]
      }
    },
    {
      id: "triada", icon: "◉", title: "Tríada de Hakim-Adams",
      kind: "steps",
      steps: [
        { n: "1º", h: "Alteración de la marcha (la primera)", b: "Marcha magnética: pies pegados al suelo, base amplia, pasos cortos arrastrados, giros en bloque, inestabilidad postural con caídas. MEJOR predictor de respuesta al shunt." },
        { n: "2º", h: "Deterioro cognitivo subcortical-frontal", b: "Disfunción ejecutiva predominante, enlentecimiento psicomotor, apatía, memoria corto plazo (menos severa que Alzheimer). No mejora significativamente a 3 meses post-shunt (PENS)." },
        { n: "3º", h: "Incontinencia urinaria", b: "Secuencia temporal: frecuencia → urgencia → incontinencia franca (tardía). Disfunción frontal del control vesical." },
      ]
    },
    {
      id: "dx", icon: "◉", title: "Diagnóstico — criterios de Relkin 2005",
      kind: "text-grid",
      items: [
        { h: "Probable", b: "Tríada completa + neuroimagen compatible + tap test positivo." },
        { h: "Posible", b: "Tríada incompleta (marcha + ≥1 adicional) + neuroimagen compatible." },
        { h: "Improbable", b: "Sin ventriculomegalia o sin síntomas cardinales." },
        { h: "NPH primaria — requisitos", b: "Marcha + ≥1 tríada, inicio gradual 3–6 meses en >40 años, sin causa secundaria ni otra etiología." },
        { h: "Guías japonesas 3ª ed (Nakajima 2021)", b: "Distingue iNPH de NPH congénita/adquirida. Rol esencial del DESH en decisión quirúrgica." },
      ]
    },
    {
      id: "imagen", icon: "◉", title: "Neuroimagen",
      kind: "text-grid",
      items: [
        { h: "Evans index >0.3", b: "Ancho cuernos frontales / diámetro biparietal. Primera aproximación. NO es específico aislado." },
        { h: "DESH (clave)", b: "Disproportionately Enlarged Subarachnoid-space Hydrocephalus. Surcos estrechos en vertex + cisuras Silvio ensanchadas. HALLAZGO CLAVE para shunt." },
        { h: "Ángulo callosal", b: "≤90° en corte coronal a nivel comisura posterior." },
        { h: "Cuernos temporales", b: "Ensanchados en ventrículos laterales." },
        { h: "Edema transependimario", b: "Hiperintensidad periventricular T2/FLAIR." },
        { h: "Flow void acueductal", b: "Signo de hiperdinamia del LCR en RM." },
        { h: "Dx diferencial imagenológico", b: "Atrofia ex vacuo = surcos difusamente ensanchados. iNPH = surcos estrechos en vertex + DESH." },
      ]
    },
    {
      id: "pruebas", icon: "⚕", title: "Pruebas complementarias",
      kind: "drugs",
      drugs: [
        { name: "Tap test (PL alto volumen)", dose: "Extracción 30–50 mL LCR por punción lumbar", adjust: "10-meter walk test pre/post. Velocidad máxima > confortable.", class: "1ª línea", notes: "Sensibilidad 50–80% · Especificidad 60–90%. Negativo NO descarta." },
        { name: "Drenaje lumbar externo (ELD)", dose: "150–200 mL/día continuo × 3–5 días", adjust: "—", class: "Alta sensibilidad", notes: "Sensibilidad ~90% · Especificidad ~80%. Riesgo: infección, cefalea, neumoencéfalo." },
        { name: "Test de infusión", dose: "Evalúa compliance y resistencia absorción", adjust: "Rout >18 mmHg/mL/min sugiere iNPH", class: "Dinámico", notes: "Menos invasivo que ELD. Buena correlación con respuesta." },
        { name: "Monitoreo PIC continuo", dose: "Invasivo", adjust: "—", class: "Reservado", notes: "Ondas B de Lundberg sugieren iNPH. Uso limitado." },
        { name: "Biomarcadores LCR", dose: "P-Tau · T-Tau · Aβ1-42", adjust: "—", class: "Pronóstico", notes: "P-Tau bajo → buen pronóstico post-shunt (Migliorati 2020). Ayuda a distinguir de EA." },
      ]
    },
    {
      id: "ddx", icon: "◉", title: "Diagnóstico diferencial",
      kind: "two-col",
      left: {
        h: "Neurodegenerativas",
        items: [
          "Alzheimer → memoria episódica, MTA elevado",
          "Demencia cuerpos Lewy → alucinaciones, fluctuaciones",
          "PSP, MSA → signos parkinsonianos específicos",
          "Deterioro cognitivo vascular → leucoencefalopatía"
        ]
      },
      right: {
        h: "Motoras / otras",
        items: [
          "Parkinson → temblor, rigidez, bradicinesia asimétrica",
          "Estenosis espinal lumbar → claudicación neurógena",
          "Atrofia ex vacuo (sin DESH)",
          "Trastornos psiquiátricos"
        ]
      }
    },
    {
      id: "tx", icon: "⚕", title: "Tratamiento quirúrgico",
      kind: "framework",
      intro: "Derivación = único tratamiento modificador. Decisión multidisciplinaria con predictores positivos (DESH, tap test+, marcha predominante, <2 años).",
      pillars: [
        { letter: "DVP", title: "Ventrículo-peritoneal", sub: "GOLD STANDARD. Válvula programable (Codman Certas Plus, Hakim, Miethke). Presión inicial 110 mmH₂O (PENS). Mecanismo antisifón." },
        { letter: "DVA", title: "Ventrículo-atrial", sub: "Alternativa si patología peritoneal. Mayor riesgo cardíaco." },
        { letter: "ETV", title: "Tercerventriculostomía endoscópica", sub: "Casos seleccionados. Sin material protésico. Menor evidencia en iNPH vs obstructiva." },
      ]
    },
    {
      id: "pens", icon: "⚡", title: "Estudio PENS — evidencia nivel 1",
      kind: "algorithm",
      start: "Primer RCT doble ciego controlado con placebo en iNPH",
      steps: [
        { q: "Diseño", yes: "N=99 pacientes · shunt abierto (49) vs placebo (50) · edad media 75 años", no: "" },
        { q: "Resultado primario — marcha", yes: "Velocidad +0.23 m/s (p<0.001) · Δ tratamiento 0.21 m/s (IC 0.12–0.31) · 80% superó MCID · NNT 1.79" },
        { q: "Resultados secundarios", yes: "Tinetti +2.9 (p=0.003) · Caídas ↓ 24% vs 46% (p=0.03) · MoCA y vejiga: sin diferencia a 3 meses" },
      ],
      pharma_cv: [
        { name: "Interpretación", dose: "NNT 1.79", note: "Uno de los tratamientos más efectivos en neurología." },
        { name: "Limitación", dose: "Seguimiento 3 meses", note: "Cognición/vejiga mejoran más lentamente; puede requerir 6–12 meses." },
      ]
    },
    {
      id: "complic", icon: "💊", title: "Complicaciones del shunt",
      kind: "drugs",
      drugs: [
        { name: "Hematoma subdural", dose: "12% (PENS)", adjust: "3/49 requirieron cirugía", class: "Más frecuente grave", notes: "Manejo inicial: ajustar válvula a presión mayor." },
        { name: "Cefalea postural", dose: "59% (PENS)", adjust: "Hipotensión LCR", class: "Frecuente leve", notes: "Manejo: ajuste de válvula programable." },
        { name: "Infección del shunt", dose: "3–6%", adjust: "S. epidermidis, S. aureus", class: "Grave", notes: "Retiro + ATB + reimplante diferido." },
        { name: "Obstrucción catéter", dose: "Tardía frecuente", adjust: "—", class: "Falla mecánica", notes: "Revisión quirúrgica." },
        { name: "Higroma / derrame subdural", dose: "Variable", adjust: "—", class: "Por sobredrenaje", notes: "Ajuste válvula." },
        { name: "Convulsiones perioperatorias", dose: "Raras", adjust: "—", class: "Agudo", notes: "Manejo estándar." },
      ]
    },
    {
      id: "pronostico", icon: "✦", title: "Factores de buena respuesta",
      kind: "pearls",
      items: [
        { t: "Marcha predominante", d: "Mejor predictor de beneficio. Mejora +0.21 m/s velocidad (PENS)." },
        { t: "Evolución <2 años", d: "Ventana terapéutica. Deterioro prolongado → menor respuesta." },
        { t: "DESH presente en RM", d: "Hallazgo imagenológico con mayor valor predictivo." },
        { t: "Tap test o ELD positivos", d: "Respuesta predice beneficio quirúrgico." },
        { t: "P-Tau bajo en LCR", d: "Biomarcador pronóstico — buena respuesta a 2 años." },
        { t: "Sin neurodegeneración severa", d: "Comorbilidad Alzheimer atenúa respuesta cognitiva." },
        { t: "Edad NO es contraindicación absoluta", d: "Evaluar funcionalidad y fragilidad, no cronología." },
        { t: "Ventana: no demorar derivación", d: "Deterioro puede volverse irreversible." },
      ]
    },
    {
      id: "pearls", icon: "✦", title: "Perlas clínicas",
      kind: "pearls",
      items: [
        { t: "Diagnóstico tardío frecuente", d: "Pensar iNPH ante tríada en AM — no atribuir a 'envejecimiento'." },
        { t: "Evans >0.3 solo NO confirma", d: "Buscar DESH y obliteración de surcos en vertex." },
        { t: "Marcha magnética + cognición subcortical", d: "Sospecha alta, iniciar estudio." },
        { t: "Tap test (–) NO descarta iNPH", d: "Considerar ELD o test de infusión si alta sospecha clínica." },
        { t: "NNT 1.79 (PENS)", d: "Uno de los tratamientos más efectivos en neurología — no dejar de referir." },
        { t: "Shunt reduce caídas", d: "24% vs 46% placebo (PENS) — impacto en funcionalidad independiente de marcha." },
        { t: "Cognición/vejiga mejoran lento", d: "No evaluar 'fracaso' a 3 meses — revalorar a 6–12 meses." },
        { t: "Sobreposición con Alzheimer", d: "Biomarcadores LCR (P-Tau, Aβ) ayudan a diferenciar." },
        { t: "Válvula programable", d: "Permite manejo de sobredrenaje/subdrenaje sin reintervenir." },
        { t: "Two-hit theory", d: "Enfermedad pequeño vaso + factor predisponente temprano." },
      ]
    },
    {
      id: "refs", icon: "📚", title: "Referencias clave",
      kind: "studies",
      items: [
        { yr: "2025", name: "Hamilton et al", q: "Guidelines for Diagnosis and Management of iNPH", res: "Neurosurg Clin N Am 36(2):199-205", trial: "Guía actual" },
        { yr: "2023", name: "Tipton et al", q: "NPH (Hakim syndrome): review and update", res: "Neurol Neurochir Pol 58(1):8-20", trial: "Terminología" },
        { yr: "2021", name: "Nakajima et al", q: "Guidelines for Management of iNPH (3rd Ed)", res: "Neurol Med Chir 61(2):63-97", trial: "Guía japonesa" },
        { yr: "2025", name: "Bluett et al", q: "Standardizing the tap test for iNPH", res: "J Neurosurg Sci 69(1):46-63 · MDS Study Group", trial: "Systematic review" },
        { yr: "2021", name: "Migliorati et al", q: "P-Tau as prognostic marker in shunted iNPH", res: "Neurol Res 43(1):78-85", trial: "Biomarcador" },
        { yr: "—", name: "PENS trial", q: "Placebo-controlled shunt for iNPH", res: "Primer RCT doble ciego. NNT 1.79. Velocidad marcha +0.21 m/s.", trial: "NEJM" },
      ]
    }
  ],

  connections: [
    { to: "alzheimer", label: "Alzheimer", via: "Dx diferencial · biomarcadores LCR", strength: 3 },
    { to: "parkinson", label: "Parkinson", via: "Dx diferencial · marcha", strength: 2 },
    { to: "demencia-vascular", label: "Demencia vascular", via: "Teoría two-hit · pequeño vaso", strength: 3 },
    { to: "marcha-am", label: "Trastornos de marcha en AM", via: "Marcha magnética · evaluación", strength: 3 },
    { to: "caidas", label: "Caídas en adulto mayor", via: "Prevención · shunt reduce 24% vs 46%", strength: 2 },
    { to: "hsa", label: "Hemorragia subaracnoidea", via: "Causa de NPH secundaria", strength: 2 },
    { to: "meningitis", label: "Meningitis", via: "Causa de NPH secundaria", strength: 1 },
    { to: "incontinencia", label: "Incontinencia urinaria AM", via: "Dx diferencial · disfunción frontal", strength: 2 },
    { to: "neuroimagen", label: "Neuroimagen dx", via: "Evans · DESH · ángulo callosal", strength: 3 },
  ]
};
