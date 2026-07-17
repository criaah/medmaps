# Portal de Recursos de Estudio

Además de los mapas mentales, MedMaps incluye un portal de recursos
(`recursos.html`) para guías de estudio, presentaciones en PDF con audio y
documentos, pensado para estudiar y compartir con compañeros.

## Tipos de recurso

| Tipo | Archivo principal | Extras | Se ve como |
|------|-------------------|--------|------------|
| `guia` | Markdown (`.md`, `.txt`) | — | Guía formateada y legible |
| `presentacion` | PDF | Pistas de audio (`.mp3`, `.m4a`, `.wav`…) | PDF incrustado + reproductor con playlist |
| `presentacion` (sincronizada) | Diapositivas PNG | Audio + cues de tiempo | **Visor sincronizado**: la diapositiva avanza sola con el audio |
| `documento` | PDF | — | PDF incrustado |

## Cómo subir un recurso

Todo es estático: "subir" = agregar los archivos al repo y actualizar el índice.
El script `process_resources.py` hace ambas cosas:

```bash
# Guía de estudio
python process_resources.py add mi_guia.md --type guia \
    --title "Guía de estudio: EPOC" --specialty "Neumología" \
    --description "Diagnóstico GOLD, escalones de tratamiento y exacerbaciones" \
    --tags epoc gold --related map_123

# Presentación PDF con audio narrado (las pistas en orden)
python process_resources.py add clase_ic.pdf --type presentacion \
    --title "Insuficiencia cardíaca con FE reducida" --specialty "Cardiología" \
    --audio parte1.mp3 parte2.mp3 parte3.mp3

# Ver lo que hay
python process_resources.py list

# Quitar un recurso del índice
python process_resources.py remove res_guia_epoc
```

Después, publicar:

```bash
git add data/resources_index.json resources/
git commit -m "recurso: Guía de estudio EPOC"
git push
```

En 1–2 minutos GitHub Pages lo publica.

## Catálogo pre-cargado y recursos "pendientes"

El portal ya trae pre-cargado el catálogo de la **Rotación UCI** (50 presentaciones,
G00–G37) como recursos *pendientes*: aparecen en el listado con la etiqueta
**⏳ Pendiente**, agrupados en la especialidad "Medicina Intensiva", pero todavía sin
PDF ni audio. La estructura del curso ya está publicada; solo falta subir los archivos.

Para completar un pendiente cuando tengas su PDF (y audio) a mano:

```bash
# Ver qué falta por subir
python process_resources.py list --pending

# Rellenar uno concreto (copia los archivos y quita el estado pendiente)
python process_resources.py fill res_uci_g05 \
    G05_shock_hemorragico.pdf --audio g05_parte1.mp3 g05_parte2.mp3
```

`fill` reutiliza la entrada existente del catálogo (mantiene título, especialidad,
tags y URL), así que el enlace `recurso.html?id=res_uci_g05` es estable desde el
primer momento: puedes compartirlo aunque el recurso todavía esté pendiente, y en
cuanto lo rellenes empezará a mostrar el PDF y el audio.

### Subir muchas presentaciones de una vez (desde tu computador)

Si tienes los PDFs juntos en una carpeta (por ejemplo, el escritorio del Mac), el
comando `import-folder` los empareja **automáticamente** con el catálogo por su
código G en el nombre del archivo (`G05…`, `G24_…`, `g06a - …`, etc.):

```bash
# 1. En tu Mac: clona o actualiza el repo
git clone https://github.com/criaah/medmaps.git   # (o git pull si ya lo tienes)
cd medmaps

# 2. Previsualiza el emparejamiento sin escribir nada
python process_resources.py import-folder ~/Desktop/presentaciones --dry-run

# 3. Si se ve bien, ejecútalo de verdad (con audios opcionales en otra carpeta)
python process_resources.py import-folder ~/Desktop/presentaciones \
    --audio-dir ~/Desktop/audios

# 4. Publica
git add -A && git commit -m "presentaciones Rotación UCI" && git push
```

- El nombre del PDF solo necesita contener el código G (`G05`, `G24`, `G06a`…);
  el resto del nombre da igual.
- Los audios se emparejan igual, por código G; varios audios del mismo código se
  ordenan alfabéticamente y quedan como pistas 1, 2, 3…
- Los PDFs sin código G reconocible se **reportan** (no se pierden) para que los
  subas a mano con `add` o `fill`.
- `--dry-run` muestra el plan sin tocar nada; `--force` sobrescribe recursos que
  ya tuvieran archivos.

> **Por qué en tu computador y no aquí:** este asistente corre en un entorno
> remoto aislado y **no puede ver los archivos de tu Mac**. Los PDFs tienen que
> pasar por el repositorio (git) para llegar al portal; por eso el emparejamiento
> se corre localmente y luego se hace `push`.

## Presentaciones sincronizadas (diapositiva + audio) — comando `pack`

Es el formato "clase": cada diapositiva se muestra como imagen y **avanza sola a
medida que corre el audio**, con miniaturas para saltar a cualquier momento. Es
el equivalente al visor de Biblioteca Geriatría, reconstruido aquí.

`pack` renderiza el PDF a PNG, copia el audio y calcula los tiempos (cues) de cada
diapositiva:

```bash
# A partir de un PDF + audio; los tiempos se estiman proporcionalmente
python process_resources.py pack res_uci_g24 --pdf G24.pdf --audio g24.mp3

# Con tiempos exactos: un archivo de texto, un timestamp por línea (mm:ss)
python process_resources.py pack res_uci_g24 --pdf G24.pdf --audio g24.mp3 --cues g24_cues.txt

# Si ya tienes las diapositivas exportadas como PNG (sin PDF)
python process_resources.py pack res_uci_g24 --slides-dir ./g24_slides --audio g24.mp3
```

- **Render PDF→PNG**: usa PyMuPDF (`pip install pymupdf`) o poppler
  (`brew install poppler`). Si no tienes ninguno, exporta los PNG a mano y usa
  `--slides-dir`.
- **Cues**: con `--cues` pones los tiempos exactos (uno por diapositiva). Sin
  `--cues`, se reparten proporcionalmente a lo largo del audio (para saber la
  duración usa `ffmpeg`/`ffprobe`, o pásala con `--duration SEGUNDOS`); en ese
  caso el visor muestra un aviso de "sincronía aproximada".
- Funciona igual sobre un id del catálogo (`res_uci_g24`) o uno nuevo.
- El PDF, si lo pasas, queda disponible como descarga ("⬇ PDF completo") dentro
  del visor.

> Este es el punto 1 del handoff de Biblioteca Geriatría (portal de clases con
> diapositiva + audio sincronizado), pero para el portal público de medmaps.

## Cómo compartir con compañeros

Cada recurso tiene URL propia y estable:

```
https://TU_USUARIO.github.io/medmaps/recurso.html?id=res_guia_epoc
```

En `recursos.html` y dentro de cada recurso hay botones:

- **🔗 Copiar enlace** — copia la URL al portapapeles
- **📤 Compartir** — abre el menú de compartir del sistema (móvil) o WhatsApp Web

## Estructura de archivos

```
recursos.html                 # Portal: listado, búsqueda y filtros
recurso.html                  # Visor de un recurso (?id=res_...)
process_resources.py          # CLI para agregar/listar/quitar recursos
data/resources_index.json     # Índice (equivalente a maps_index.json)
resources/
├── guias/                    # Markdown de guías de estudio
├── presentaciones/           # PDFs de presentaciones
├── documentos/               # Otros PDFs
└── audio/                    # Pistas de audio de las presentaciones
```

## Formato del índice

Cada entrada de `data/resources_index.json`:

```json
{
  "id": "res_guia_epoc",
  "type": "guia",
  "title": "Guía de estudio: EPOC",
  "specialty": "Neumología",
  "description": "…",
  "author": "Dr. Acevedo",
  "date": "2026-07-17",
  "tags": ["epoc"],
  "access": "free",
  "files": {
    "content": "resources/guias/mi_guia.md",
    "pdf": "resources/presentaciones/clase.pdf",
    "audio": [ { "title": "Parte 1", "src": "resources/audio/parte1.mp3" } ]
  },
  "related_maps": ["map_123"]
}
```

`files` admite cualquier combinación: una guía puede además llevar PDF y audio.
`related_maps` enlaza el recurso con mapas del visor (`viewer.html?id=…`).

## Notas y límites

- **Tamaño**: GitHub recomienda archivos < 50 MB y repos < 1 GB. Para audios
  largos usa `.m4a`/`.mp3` a 64–96 kbps (una clase de 40 min ≈ 20–30 MB).
  Si el volumen crece mucho, considerar Git LFS o un bucket externo.
- **Audio por partes**: dividir la narración en pistas cortas (una por sección
  o diapositiva) mejora la navegación; el reproductor avanza solo a la
  siguiente pista.
- **PDF en móvil**: algunos navegadores móviles no incrustan PDFs; el visor
  siempre ofrece el botón "Abrir en pestaña nueva".
- **Acceso**: el campo `access` (`free`/`premium`) queda registrado para
  integrarse con el sistema de planes existente.

## Migrar contenido desde otro proyecto

Si ya tienes guías/presentaciones en otro repo o carpeta:

```bash
# Guías markdown en lote
for f in /ruta/al/otro/proyecto/guias/*.md; do
  python process_resources.py add "$f" --type guia --specialty "General"
done
```

Luego edita `data/resources_index.json` para ajustar títulos, especialidades y
descripciones (es JSON simple, se puede editar a mano sin miedo).
