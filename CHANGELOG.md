# MedMaps - Registro de Cambios

## Sesión: 6 de Febrero 2026

### ✅ CAMBIOS COMPLETADOS

#### 1. Portal de Pagos (`planes.html`)
- Página completa de planes y precios
- Tres planes: Estudiante (gratis), Premium ($9.990), Institucional ($49.990)
- Integración preparada con MercadoPago SDK
- Modal de pago con opciones: tarjeta y transferencia bancaria
- Datos de transferencia configurados (Banco Estado, Cuenta RUT)
- FAQ interactivo
- Garantía de 7 días
- Diseño responsive

#### 2. Sistema de Revisión de Mapas (`admin.html`)
- Panel de administración protegido con contraseña
- Cola de revisión con estados: pendiente, aprobado, rechazado, publicado
- Visualizador de mapas en árbol jerárquico
- Notas de revisión por mapa
- Estadísticas en tiempo real
- Filtros: todos, pendientes, aprobados
- Formulario para subir nuevos mapas manualmente
- Estructura JSON en `data/review_queue.json`
- Directorio `data/review/` para mapas en cola

#### 3. Sistema de TAGS para Clasificación
- Tags implementados en `explorar.html`:
  - 📄 Paper
  - 📚 Revisión
  - ⭐ Estudio Pivotal
  - 📋 Guía Clínica
  - 🔬 Fisiopatología
  - 💊 Farmacología
  - 🏥 Caso Clínico

#### 4. Mejoras en `explorar.html`
- ❌ Eliminado botón de "Copiar contenido"
- ✅ Mapas siempre colapsados por defecto (solo título raíz visible)
- ✅ Expandir/Colapsar funcional
- ✅ Configuración expandida de especialidades (17 especialidades con emojis)
- ✅ Sistema de TAGS configurado

#### 5. Estructura del Repositorio
```
medmaps_repo/
├── index.html          # Página principal
├── explorar.html       # Explorador de mapas (actualizado)
├── planes.html         # Planes y precios (NUEVO)
├── admin.html          # Panel de administración (NUEVO)
├── data/
│   ├── maps/           # 254 mapas en JSON
│   ├── maps_index.json # Índice de mapas
│   ├── specialties.json
│   ├── stats.json
│   ├── review_queue.json (NUEVO)
│   └── review/         # Cola de revisión (NUEVO)
│       └── README.md
└── CHANGELOG.md        # Este archivo
```

---

### ⏳ TAREAS PENDIENTES

#### PRIORIDAD ALTA - Para dejar operativo

1. **Integración con Notion** (solicitado por usuario)
   - Crear base de datos en Notion para gestión de mapas
   - Campos: título, especialidad, TAG, estado (no subido/gratis/pagado), fecha actualización
   - Sincronización bidireccional con el portal
   - Webhook para actualizar página cuando se modifica Notion

2. **Optimizar página de inicio (`index.html`)**
   - Mejorar hero section
   - Agregar estadísticas dinámicas
   - CTAs claros hacia planes y explorar

3. **Push a GitHub**
   - Commit con todos los cambios
   - Verificar que el sitio funcione en GitHub Pages

4. **Configurar MercadoPago**
   - Obtener credenciales de producción
   - Configurar webhook para confirmar pagos
   - Implementar backend para crear preferencias de pago

#### PRIORIDAD MEDIA

5. **Sistema de autenticación de usuarios**
   - Login/registro
   - Verificar plan activo
   - Restringir mapas según plan

6. **Extraer fechas de creación de mapas**
   - Leer metadatos de archivos .smmx originales
   - Agregar campo `created_at` a cada mapa

7. **SEO y optimización**
   - Meta tags para cada página
   - Open Graph para compartir
   - Sitemap.xml
   - robots.txt

#### PRIORIDAD BAJA

8. **Integración del skill `mapa-mental`**
   - El skill está en sistema de solo lectura
   - Documentar flujo manual: generar mapa → copiar a admin → aprobar → publicar
   - Considerar crear script de automatización

9. **Exportar a PDF**
   - Funcionalidad para usuarios Premium
   - Diseño de PDF con logo y formato profesional

10. **Modo offline (PWA)**
    - Service worker
    - Cache de mapas frecuentes

---

### 🔐 CREDENCIALES Y CONFIGURACIÓN

#### Admin Panel
- URL: `/admin.html`
- Contraseña: `medmaps2026` (cambiar en producción)

#### Transferencia Bancaria
- Banco: Banco Estado
- Cuenta RUT: 17700400-6
- Nombre: Cristian Acevedo
- Email: criaah@gmail.com

#### MercadoPago (pendiente)
- Public Key: `[CONFIGURAR]`
- Access Token: `[CONFIGURAR]`

---

### 📝 NOTAS PARA EL USUARIO

1. **Flujo de revisión actual:**
   - Generar mapa con skill `mapa-mental`
   - Copiar contenido a admin.html → "Subir Mapa"
   - Revisar y aprobar
   - Publicar (requiere script de sincronización)

2. **Integración Notion (próximo paso):**
   - Cuando se implemente, podrás gestionar todo desde Notion
   - Los cambios en Notion se reflejarán automáticamente en el portal
   - Recomendación: usar Notion API + webhook

3. **GitHub Token:**
   - Token creado: `github_pat_11BNRUMJY0...` (guardado en sesión anterior)
   - Repositorio: criaah/medmaps

---

*Última actualización: 6 de Febrero 2026*
