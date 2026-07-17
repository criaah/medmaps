# Portal de Recursos de Estudio

Además de los mapas mentales, MedMaps incluye un portal de recursos
(`recursos.html`) para guías de estudio, presentaciones en PDF con audio y
documentos, pensado para estudiar y compartir con compañeros.

## Tipos de recurso

| Tipo | Archivo principal | Extras | Se ve como |
|------|-------------------|--------|------------|
| `guia` | Markdown (`.md`, `.txt`) | — | Guía formateada y legible |
| `presentacion` | PDF | Pistas de audio (`.mp3`, `.m4a`, `.wav`…) | PDF incrustado + reproductor con playlist |
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
