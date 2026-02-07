# 🗺️ Workflow de Creación de Mapas Mentales MedMaps

## Flujo Obligatorio (5 pasos)

Al recibir solicitud de mapa mental sobre un tema:

### 1️⃣ REVISAR MAPAS EXISTENTES (PRIMERO)

Antes de crear cualquier mapa nuevo, buscar en el índice de MedMaps:

```bash
cd /sessions/bold-jolly-cerf/medmaps_repo
python -c "
import json
TERM = 'TEMA_A_BUSCAR'  # Reemplazar con término de búsqueda
with open('data/maps_index.json') as f:
    index = json.load(f)
term_lower = TERM.lower()
related = [m for m in index if term_lower in m.get('title','').lower()]
print(f'Mapas relacionados con {TERM}:')
for m in related[:10]:
    print(f\"  - {m['id']}: {m['title'][:60]}... [{m.get('specialty')}]\")
"
```

**Mapas encontrados →** Usar como fuente adicional:
- Leer contenido del mapa: `cat data/maps/{map_id}.json | python -m json.tool`
- Extraer conceptos clave, perlas clínicas
- Evitar duplicar contenido ya existente, mejor complementar
- Identificar mapas para enlazar en la sección final

### 2️⃣ BUSCAR EN GOOGLE DRIVE

- Buscar Docs, PDFs, PPTs relacionados con el tema
- Revisar contenido detallado y extenso
- Incluir tablas, diagramas, imágenes

### 3️⃣ COMPLEMENTAR CON PUBMED

- Buscar evidencia actualizada
- Priorizar revisiones sistemáticas y guías clínicas
- Incluir estudios pivotales relevantes

### 4️⃣ GENERAR MAPA MENTAL

Formato de salida:

```
Tema Principal
	Subtema 1
		**Concepto clave**
		Detalle → consecuencia
		Dato estadístico (OR 2.5, IC 95% 1.2-4.1)
	Subtema 2
		Elemento X
			Sub-elemento
		Elemento Y (~aproximado)
	Perlas Clínicas ⭐
		[Implicación práctica 1]
		[Precaución o atajo diagnóstico/terapéutico]
		[Recomendación implícita detectada]

🔗 Mapas Relacionados
	→ [map_XXXX] Nombre del mapa relacionado 1
	→ [map_YYYY] Nombre del mapa relacionado 2
	→ [map_ZZZZ] Nombre del mapa relacionado 3

Referencias
	1. Autor. Título. Revista. Año;vol(num):pág.
	2. ...
```

### 5️⃣ AGREGAR A MEDMAPS (Opcional)

```bash
# Guardar en inbox para revisión
cp mapa_nuevo.txt /sessions/bold-jolly-cerf/mnt/Dropbox/MedMaps/inbox/

# O procesar directamente
python text_to_map.py --input mapa_nuevo.txt --specialty "Geriatría" --tag "📚 Revisión"
```

---

## 🔗 Tabla de Relaciones Temáticas

| Si el tema es... | Buscar también... |
|------------------|-------------------|
| Delirium | Demencia, Polifarmacia, Fragilidad, UCI, CAM |
| Fragilidad | Sarcopenia, Caídas, Polifarmacia, CFS |
| Insuficiencia cardíaca | SGLT2, Diuréticos, Cardiorrenal, BNP |
| Diabetes | ERC, Neuropatía, SGLT2, Hipoglicemia |
| Demencia | Delirium, DCL, Parkinson, Alzheimer, Lewy |
| ACV/Stroke | Fibrilación auricular, Anticoagulación, NIHSS |
| Sepsis | Shock, UCI, Antimicrobianos, SOFA |
| Fractura cadera | Osteoporosis, Caídas, Ortogeriatría, VTE |
| Parkinson | Demencia, Lewy, Diskinesia, Temblor |
| ERC | Diálisis, Anemia, Hipertensión, KDIGO |
| Fibrilación auricular | Anticoagulación, ACV, CHA2DS2-VASc |
| Neumonía | Sepsis, Antimicrobianos, CURB-65 |
| Osteoporosis | Caídas, Fractura, Vitamina D, Bifosfonatos |
| Incontinencia | Polifarmacia, Deterioro funcional, Vejiga |

---

## 📊 Estadísticas Actuales del Portal

- **Total mapas**: 489
- **Por especialidad**:
  - General: ~287
  - Estudios Pivotales: ~37
  - Continuum: ~30
  - UCI-Medicina Crítica: ~32
  - Cardiología: ~25
  - Neurología: ~26
  - Infectología: ~23
  - Hematología: ~27
  - Endocrinología: ~18
  - Nefrología: ~18
  - Geriatría: ~12

---

## 🔍 Búsqueda Rápida de Mapas

```bash
# Buscar por término en título
python review_maps.py --search "delirium"

# Listar por especialidad
python review_maps.py --specialty "Geriatría"

# Ver todos
python review_maps.py --list
```

---

*Última actualización: 7 de Febrero 2026*
