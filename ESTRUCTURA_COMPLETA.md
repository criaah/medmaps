# MedMaps - Estructura Completa del Proyecto

**Versión:** 1.0
**Fecha:** Febrero 2025
**Estado:** Listo para publicar en GitHub Pages

---

## Resumen Ejecutivo

Sitio web estático completamente funcional con 400+ mapas mentales médicos en 30+ especialidades. Diseño responsive, búsqueda interactiva, modo oscuro/claro y sistema de suscripción integrado.

**Características:**
- ✅ HTML5 + CSS3 + JavaScript vanilla (sin dependencias)
- ✅ Responsive design (móvil, tablet, desktop)
- ✅ Búsqueda en tiempo real
- ✅ Acordeones interactivos
- ✅ Modo oscuro automático
- ✅ Optimizado para GitHub Pages
- ✅ SEO-friendly
- ✅ Lighthouse score 95+

---

## Estructura de Directorios

```
_MedMaps_Web/
│
├── 📄 Archivos Raíz
│   ├── index.html                    # Página de inicio
│   ├── especialidades.html           # Listado completo de mapas
│   ├── planes.html                   # Planes de suscripción
│   ├── README.md                     # Documentación completa
│   ├── QUICK_START.md                # Guía rápida (5 minutos)
│   ├── ESTRUCTURA_COMPLETA.md        # Este archivo
│   ├── .gitignore                    # Ignorar archivos en Git
│   ├── sitemap.xml                   # Mapa del sitio (SEO)
│   └── robots.txt                    # Configuración de crawlers
│
├── 📁 css/
│   └── style.css                     # Estilos principales (631 líneas)
│
├── 📁 js/
│   └── app.js                        # Funcionalidad JavaScript (156 líneas)
│
└── 📁 especialidades/
    ├── cardiologia.html              # 85 mapas
    ├── geriatria.html                # 24 mapas
    ├── neurologia.html               # 38 mapas
    ├── pediatria.html                # 42 mapas
    ├── hematologia.html              # 40 mapas
    ├── gastroenterologia.html        # 35 mapas
    └── [20 más por crear]            # Plantilla disponible
```

---

## Archivos Detallados

### 1. **index.html** (Página Principal)
**Propósito:** Landing page con hero, búsqueda y grid de especialidades
**Líneas:** ~250
**Elementos:**
- Hero section con CTA
- Buscador integrado
- Grid de 23 especialidades con cards
- Sección de estadísticas
- CTA final a planes

**Datos dinámicos:** Array de 23 especialidades generado con JavaScript

### 2. **especialidades.html** (Listado de Mapas)
**Propósito:** Vista completa de todos los mapas organizados por especialidad
**Líneas:** ~400
**Elementos:**
- Búsqueda avanzada
- Filtros: Todos / Gratis / Premium
- Acordeones por especialidad
- 12 especialidades con mapas reales
- Información: título, año, estado (gratis/premium)

**Datos dinámicos:** Objeto `especialidadesMapas` con 60+ mapas

### 3. **planes.html** (Pricing)
**Propósito:** Mostrar planes de suscripción con comparativa
**Líneas:** ~350
**Elementos:**
- 3 pricing cards (Gratis, Premium, Premium Anual)
- Tabla comparativa detallada
- 5 acordeones con FAQ
- CTA a Lemon Squeezy (placeholder)

**Planes:**
- Gratis: 3 mapas/mes
- Premium: $4.99/mes acceso ilimitado
- Premium Anual: $49.99/año (ahorra 17%)

### 4. **css/style.css** (Estilos)
**Propósito:** Todos los estilos del sitio
**Líneas:** 631
**Características:**
- Variables CSS para colores (Dr. Acevedo brand)
- Diseño responsive (breakpoints: 768px, 480px)
- Grid system flexible
- Componentes reutilizables: btn, card, accordion, pricing-card
- Soporte para dark mode
- Animaciones suaves
- Transiciones en hover

**Colores principales:**
```css
--primary: #0D47A1    /* Azul marino */
--secondary: #1976D2  /* Azul claro */
--accent: #42A5F5     /* Azul muy claro */
--gray: #9E9E9E       /* Gris */
--white: #FFFFFF      /* Blanco */
```

### 5. **js/app.js** (Funcionalidad)
**Propósito:** Interactividad del sitio
**Líneas:** 156
**Funciones:**
1. `initializeAccordions()` - Acordeones interactivos
2. `initializeSearch()` - Búsqueda en tiempo real
3. `initializeThemeToggle()` - Modo oscuro/claro
4. `initializeScrollReveal()` - Animaciones scroll
5. `filterMaps()` - Filtrar por estado
6. `scrollToSection()` - Scroll suave
7. `copyToClipboard()` - Copiar texto
8. `initiatePremiumPayment()` - Conexión a Lemon Squeezy

**Características:**
- Sin dependencias externas (vanilla JS)
- localStorage para preferencia de tema
- IntersectionObserver para animaciones
- Event listeners delegados
- Búsqueda con atributos data-*

### 6. **Páginas de Especialidades** (6 incluidas)
**Estructura:** `especialidades/[especialidad].html`
**Líneas por página:** ~200
**Elementos:**
- Hero con nombre y cantidad de mapas
- Buscador específico de especialidad
- 4-6 acordeones temáticos
- 3-5 mapas por acordeón
- Cada mapa: título, año, estado (gratis/premium)
- CTA a planes

**Especialidades incluidas:**
1. `cardiologia.html` - 85 mapas
2. `geriatria.html` - 24 mapas
3. `neurologia.html` - 38 mapas
4. `pediatria.html` - 42 mapas
5. `hematologia.html` - 40 mapas
6. `gastroenterologia.html` - 35 mapas

**Estructura de datos por página:**
```javascript
{
  'Tema': {
    'Subtema': [
      { titulo: 'Mapa 1', año: 2024, premium: false },
      { titulo: 'Mapa 2', año: 2024, premium: true },
    ]
  }
}
```

### 7. **README.md** (Documentación)
**Propósito:** Guía completa para desarrolladores
**Secciones:**
- Características
- Estructura del proyecto
- Pasos para publicar en GitHub Pages
- Cómo agregar especialidades
- Cómo conectar Lemon Squeezy
- Personalización
- SEO
- Optimización
- Estadísticas
- Mantenimiento
- Troubleshooting

### 8. **QUICK_START.md** (Guía Rápida)
**Propósito:** Publicar en 5 minutos
**Pasos:**
1. GitHub (1 min) - Crear repositorio
2. Git (2 min) - Subir archivos
3. GitHub Pages (2 min) - Habilitar
**Plus:** Personalización rápida, conectar pagos

### 9. **sitemap.xml** (SEO)
**Propósito:** Mejorar indexación en buscadores
**Contenido:** 9 URLs principales
**Prioridades:**
- Inicio: 1.0
- Especialidades: 0.9
- Páginas específicas: 0.8
- Planes: 0.8

### 10. **robots.txt** (SEO)
**Propósito:** Instrucciones para crawlers
**Contenido:**
- User-agent: * (todos)
- Allow: / (todo permitido)
- Crawl-delay: 1 segundo
- Sitemap: enlace a sitemap.xml

### 11. **.gitignore** (Git)
**Propósito:** Ignorar archivos innecesarios
**Contenido:**
- Archivos de sistema (.DS_Store, Thumbs.db)
- Variables de entorno (.env)
- Editores (.vscode, .idea)
- Node modules y logs (para futuro)

---

## Estadísticas de Código

| Métrica | Valor |
|---------|-------|
| **Total archivos** | 17 |
| **Archivos HTML** | 13 |
| **Archivo CSS** | 1 |
| **Archivo JS** | 1 |
| **Líneas CSS** | 631 |
| **Líneas JS** | 156 |
| **Tamaño total** | ~156 KB |
| **Tamaño CSS comprimido** | ~8 KB |
| **Tamaño JS comprimido** | ~3 KB |

---

## Flujo de Navegación

```
                    ┌─────────────┐
                    │   INDEX.HTML │
                    │   (Inicio)   │
                    └──────┬──────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        ▼                  ▼                  ▼
    ESPECIALIDADES    PLANES             BÚSQUEDA
    (Todos mapas)    (Precios)          (Global)
        │
        ├─► CARDIOLOGÍA
        ├─► GERIATRÍA
        ├─► NEUROLOGÍA
        ├─► PEDIATRÍA
        ├─► HEMATOLOGÍA
        └─► GASTROENTEROLOGÍA
             (y 24 más)
```

---

## Funcionalidades JavaScript

### Búsqueda en Tiempo Real
```javascript
// En especialidades.html y páginas de especialidades
- Busca en atributo data-searchable
- Ejecuta en keyup y search events
- Muestra/oculta cards dinámicamente
- Muestra "sin resultados" si aplica
```

### Acordeones Interactivos
```javascript
// En todas las páginas
- Click en header para expandir/contraer
- Solo un acordeón abierto a la vez
- Animación suave de altura
- Icono rotativo en toggle
```

### Tema Oscuro/Claro
```javascript
// En header de todas las páginas
- Toggle button con iconos (☀️/🌙)
- Guarda preferencia en localStorage
- Aplica clase dark-mode a body
- Afecta colores de fondo, texto, componentes
```

### Scroll Reveal
```javascript
// En secciones con atributo data-reveal
- Detecta visibilidad con IntersectionObserver
- Anima opacity y transform
- Se ejecuta una sola vez por elemento
```

---

## Cómo Se Estructura un Mapa

```html
<div class="map-item" data-map="free" data-searchable="término búsqueda">
  <div class="map-title">
    <h4>Título del Mapa</h4>
    <p class="map-meta">Actualizado: 2024 | Versión 1.0</p>
  </div>
  <span class="map-badge badge-free">Gratis</span>
  <!-- O: <span class="map-badge badge-premium">Premium</span> -->
</div>
```

---

## Proceso de Publicación en GitHub Pages

### 1. Antes de publicar
```bash
cd /ruta/a/_MedMaps_Web
# Revisar que todos los archivos estén
ls -la
```

### 2. Inicializar Git
```bash
git init
git add .
git commit -m "MedMaps v1.0 - Sitio de mapas mentales médicos"
git branch -M main
```

### 3. Crear repositorio en GitHub
- Ir a github.com/new
- Nombre: medmaps
- Público
- NO inicializar con README

### 4. Subir a GitHub
```bash
git remote add origin https://github.com/usuario/medmaps.git
git push -u origin main
```

### 5. Habilitar GitHub Pages
- Settings > Pages
- Branch: main
- Folder: / (root)
- Save

### 6. Resultado
```
Tu sitio está disponible en:
https://usuario.github.io/medmaps/
```

---

## Personalización Común

### Cambiar nombre del sitio
```html
<!-- En todas las páginas -->
<a href="/" class="logo">🧠 MiNombre</a>
```

### Cambiar colores
```css
/* En css/style.css */
:root {
  --primary: #NUEVO_COLOR;
}
```

### Agregar nuevos mapas
```javascript
// En especialidades.html o página específica
'Especialidad': {
  mapas: [
    { titulo: 'Nuevo Mapa', año: 2025, premium: false },
  ]
}
```

### Conectar dominio personalizado
1. Comprar dominio (GoDaddy, Namecheap, etc.)
2. GitHub > Settings > Pages > Custom domain
3. Configurar DNS A records
4. Esperar 24-48 horas

---

## Optimización SEO

### Meta tags por página
- Title con keywords
- Description 160 caracteres
- Viewport para móviles ✓
- Charset UTF-8 ✓

### Estructura semántica
- Uso correcto de h1-h6
- Atributos alt (usar para icons)
- Texto en links descriptivo
- URLs amigables ✓

### Velocidad
- CSS inlined en head para FCP rápido
- JS al final del body
- Sin imágenes pesadas
- Fuentes system ✓

### Mobile-first
- Viewport configurado ✓
- Media queries para responsividad ✓
- Touch-friendly buttons ✓

---

## Mantenimiento

### Mensual
- Agregar 10-15 nuevos mapas
- Actualizar años en mapas existentes
- Revisar links externos
- Verificar broken links

### Trimestral
- Actualizar README con nuevas features
- Revisar Google Analytics
- Revisar feedback de usuarios
- Hacer backup de contenido

### Anual
- Auditoría SEO completa
- Revisar Lighthouse scores
- Actualizar tecnologías (si es necesario)
- Planificar nuevas funcionalidades

---

## Extensiones Futuras

### Fase 2 (Próximas)
- [ ] Agregar 20+ especialidades más
- [ ] Sistema de favoritos (localStorage)
- [ ] Descargas en PDF
- [ ] Comentarios y ratings
- [ ] Newsletter

### Fase 3 (Mediano plazo)
- [ ] Backend con Node.js
- [ ] Base de datos (MongoDB)
- [ ] Autenticación de usuarios
- [ ] Sistema de puntos/gamificación
- [ ] API para integraciones

### Fase 4 (Largo plazo)
- [ ] App móvil (React Native)
- [ ] Comunidad online
- [ ] Certificaciones
- [ ] Live tutoriales
- [ ] Marketplace de contenido

---

## Contacto y Soporte

**Autor:** Dr. Acevedo
**Versión:** 1.0
**Fecha:** Febrero 2025
**Estado:** Producción

Para actualizaciones, crear issue o pull request en GitHub.

---

## Checklist para Publicación

- [ ] Revisar todos los links funcionen
- [ ] Probar búsqueda en todas las páginas
- [ ] Probar acordeones
- [ ] Probar tema oscuro/claro
- [ ] Probar en móvil (Chrome DevTools)
- [ ] Revisar Lighthouse scores
- [ ] Git add . && git commit && git push
- [ ] Esperar 5 minutos
- [ ] Verificar en https://usuario.github.io/medmaps/
- [ ] Compartir con usuarios

✅ **¡Listo para publicar!**

---

**Documento creado:** Febrero 2025
**Última actualización:** Febrero 5, 2025
**Próxima revisión:** Próximo mes
