# 📚 Guía de Operaciones MedMaps
## Manual Completo de Gestión y Mantenimiento

---

## 🔧 CONFIGURACIÓN INICIAL

### 1. Configurar Notion (Una sola vez)

✅ **COMPLETADO**: La base de datos de MedMaps ya fue creada en tu página "MedMaps Dashboard".

**Propiedades configuradas:**
- ✅ Nombre (título)
- ✅ Especialidad (selector)
- ✅ TAG (selector)

**Propiedades pendientes de agregar manualmente:**

Para agregar cada propiedad, haz clic en el "+" al final de las columnas:

| Propiedad | Tipo | Opciones/Descripción |
|-----------|------|---------------------|
| Estado | Estado | No Subido (gris), En Revisión (amarillo), Gratis (verde), Premium (azul), Archivado (rojo) |
| Nodos | Número | Cantidad de nodos del mapa |
| ID Mapa | Texto | Identificador único (ej: map_0001) |
| URL Portal | URL | Link al mapa en el portal |
| Notas | Texto | Observaciones |

**Opciones para Especialidad:**
Geriatría, Cardiología, Neurología, Nefrología, Endocrinología, UCI-Medicina Crítica,
Infectología, Hematología, Gastroenterología, Neumología, Reumatología, Psiquiatría,
Ortogeriatría, Pediatría, General, Continuum, Estudios Pivotales

**Opciones para TAG:**
📄 Paper, 📚 Revisión, ⭐ Estudio Pivotal, 📋 Guía Clínica, 🔬 Fisiopatología,
💊 Farmacología, 🏥 Caso Clínico

### 2. Sincronización API

⚠️ **NOTA**: La API de Notion no está disponible desde Cowork (proxy bloqueado).
Para sincronizar automáticamente, ejecuta el script desde tu terminal local:

```bash
cd medmaps_repo
python sync_notion.py --sync
```

Alternativamente, puedes agregar mapas manualmente en Notion copiando los datos.

---

## 📤 FLUJO PARA SUBIR NUEVOS MAPAS

### Opción A: Desde el Skill mapa-mental (Recomendado)

1. **Generar el mapa**
   - Usa el skill: "Hazme un mapa mental sobre [TEMA]"
   - Claude buscará en tu Drive + PubMed
   - Generará el mapa con referencias Vancouver

2. **Copiar al sistema de revisión**
   - Abre `admin.html` (contraseña: medmaps2026)
   - Clic en "📤 Subir Mapa"
   - Pega el contenido del mapa
   - Selecciona especialidad y TAG
   - Clic en "Agregar a Cola"

3. **Revisar y aprobar**
   - En admin.html, selecciona el mapa
   - Revisa el contenido
   - Agrega notas si es necesario
   - Clic en "✅ Aprobar"

4. **Publicar**
   - Una vez aprobado, clic en "🚀 Publicar"
   - Esto moverá el mapa a `data/maps/`

5. **Subir a GitHub**
   ```bash
   cd medmaps_repo
   git add .
   git commit -m "Add: [nombre del mapa]"
   git push
   ```

6. **Sincronizar con Notion**
   ```bash
   python sync_notion.py --sync
   ```

### Opción B: Subida manual directa

1. Crear archivo JSON en `data/maps/map_XXXX.json`:
```json
{
  "id": "map_XXXX",
  "title": "Título del Mapa",
  "specialty": "Geriatría",
  "tag": "📚 Revisión",
  "node_count": 25,
  "root": {
    "text": "Tema Principal",
    "children": [
      {
        "text": "Subtema 1",
        "children": [
          {"text": "Detalle 1.1"},
          {"text": "Detalle 1.2"}
        ]
      }
    ]
  }
}
```

2. Actualizar `data/maps_index.json`:
```bash
python update_index.py  # Si existe, o agregar manualmente
```

---

## 🔄 MANTENIMIENTO REGULAR

### Diario
- [ ] Revisar cola de mapas pendientes en admin.html
- [ ] Aprobar/rechazar mapas revisados

### Semanal
- [ ] Sincronizar con Notion: `python sync_notion.py --sync`
- [ ] Verificar que GitHub Pages esté funcionando
- [ ] Revisar estadísticas de visitas (Google Analytics)

### Mensual
- [ ] Actualizar mapas con nueva evidencia
- [ ] Revisar mapas más visitados
- [ ] Agregar nuevos temas solicitados por usuarios
- [ ] Backup de la base de datos

---

## 📊 DASHBOARD EN NOTION

### Estructura recomendada de la página principal:

```
📊 MedMaps Dashboard
├── 📈 Métricas (embed Google Analytics)
├── 📚 Base de Datos de Mapas
│   ├── Vista: Todos los mapas
│   ├── Vista: Pendientes de revisión
│   ├── Vista: Por especialidad
│   └── Vista: Más populares
├── 👥 Clientes (base de datos separada)
│   ├── Nombre
│   ├── Email
│   ├── Plan (Gratis/Premium/Institucional)
│   ├── Fecha suscripción
│   └── Estado pago
├── 💰 Finanzas
│   ├── Ingresos mensuales
│   └── Pagos pendientes
└── 📝 Tareas pendientes
```

### Cómo agregar Google Analytics a Notion:
1. Ve a [Google Analytics](https://analytics.google.com)
2. Crea una propiedad para medmaps
3. Obtén el ID de medición (G-XXXXXXXXX)
4. Agrega el script a `index.html` y `explorar.html`:
```html
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXX');
</script>
```
5. En Notion, usa embed para mostrar el dashboard de Analytics

---

## 🏷️ SISTEMA DE TAGS

| TAG | Uso | Ejemplo |
|-----|-----|---------|
| 📄 Paper | Análisis de artículo | "SPRINT Trial Analysis" |
| 📚 Revisión | Tema amplio | "Manejo de HTA" |
| ⭐ Estudio Pivotal | Ensayo que cambió práctica | "PARADIGM-HF" |
| 📋 Guía Clínica | Resumen de guías | "ACC/AHA HF 2024" |
| 🔬 Fisiopatología | Ciencia básica | "Sarcopenia: mecanismos" |
| 💊 Farmacología | Fármacos | "IECA en ERC" |
| 🏥 Caso Clínico | Casos | "Delirium en UCI" |

---

## 🚨 SOLUCIÓN DE PROBLEMAS

### Error: "403 Forbidden" en Notion
- La integración no tiene acceso a la página
- Solución: Compartir la página con la integración

### Error: "Map not found" al abrir mapa
- El ID en maps_index.json no coincide con el archivo
- Solución: Regenerar índice o verificar nombres de archivos

### El mapa no aparece en explorar.html
- No está en maps_index.json
- Solución: Agregar al índice y hacer push

### Pago no se procesa
- MercadoPago requiere configuración backend
- Solución temporal: Usar transferencia bancaria

---

## 📞 CONTACTO Y SOPORTE

- **Admin Panel**: `/admin.html` (pass: medmaps2026)
- **GitHub**: https://github.com/criaah/medmaps
- **Portal**: https://criaah.github.io/medmaps

---

## 🔐 CREDENCIALES (NO COMPARTIR)

| Servicio | Ubicación |
|----------|-----------|
| Notion Token | `.env` |
| GitHub Token | Configurado en git |
| MercadoPago | Pendiente en `.env` |
| Admin Password | admin.html (medmaps2026) |

---

*Última actualización: 6 de Febrero 2026*
