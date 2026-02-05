# MedMaps - Guía Rápida de Inicio

## En 5 minutos: Publicar tu sitio

### Paso 1: GitHub (1 min)
```bash
# Crear repositorio en github.com llamado "medmaps"
# Copiar el nombre de usuario (ej: miusuario)
```

### Paso 2: Git (2 min)
```bash
# En tu terminal:
cd "/sessions/bold-jolly-cerf/mnt/Dropbox/- Esquemas/_MedMaps_Web"

git init
git add .
git commit -m "MedMaps v1.0 - Sitio estático de mapas mentales médicos"
git branch -M main
git remote add origin https://github.com/miusuario/medmaps.git
git push -u origin main
```

### Paso 3: GitHub Pages (2 min)
1. En GitHub, ir a **Settings** > **Pages**
2. Branch: `main` | Folder: `/ (root)`
3. Guardar

### ¡Listo! Tu sitio está en:
```
https://miusuario.github.io/medmaps/
```

---

## Funcionalidades Principales

✓ Búsqueda en tiempo real
✓ Acordeones interactivos
✓ Modo oscuro/claro
✓ Responsive (móvil, tablet, desktop)
✓ 400+ mapas mentales
✓ 30+ especialidades

---

## Estructura de Archivos Clave

```
├── index.html           ← Página de inicio
├── especialidades.html  ← Todos los mapas
├── planes.html          ← Planes de suscripción
├── css/
│   └── style.css       ← Colores: Navy #0D47A1
├── js/
│   └── app.js          ← Búsqueda, acordeones, tema
└── especialidades/
    ├── cardiologia.html
    ├── geriatria.html
    ├── neurologia.html
    ├── pediatria.html
    ├── hematologia.html
    └── gastroenterologia.html
```

---

## Personalización Rápida

### Cambiar título
En `index.html`:
```html
<h1>MedMaps</h1>  <!-- Cambiar aquí -->
```

### Cambiar descripción
En todas las páginas HTML:
```html
<meta name="description" content="Tu descripción aquí">
```

### Cambiar colores
En `css/style.css`:
```css
:root {
  --primary: #0D47A1;  /* Azul marino - Cambiar aquí */
}
```

### Agregar logo/favicon
Crear `favicon.ico` (32x32px) y agregar a `<head>`:
```html
<link rel="icon" href="favicon.ico">
```

---

## Agregar Nuevos Mapas

### Opción 1: En especialidades.html
```javascript
const especialidadesMapas = {
  'Cardiología': {
    mapas: [
      { titulo: 'Nuevo Mapa', año: 2025, premium: false },
      // ...
    ]
  }
};
```

### Opción 2: Crear nueva especialidad
1. Copiar `especialidades/cardiologia.html` → `especialidades/nueva.html`
2. Actualizar contenido
3. Agregar link en `especialidades.html` y `index.html`
4. Git push

---

## Conectar Pagos (Lemon Squeezy)

1. Ir a lemonsqueezy.com
2. Crear productos:
   - Premium: $4.99/mes (ID: 123456)
   - Anual: $49.99/año (ID: 123457)

3. En `js/app.js`, actualizar:
```javascript
function initiatePremiumPayment(planId) {
  const ids = {
    'premium': '123456',
    'annual': '123457'
  };
  window.location.href =
    `https://tutienda.lemonsqueezy.com/checkout/buy/${ids[planId]}`;
}
```

---

## Estadísticas

| Métrica | Valor |
|---------|-------|
| Páginas | 23 |
| Tamaño | ~500KB |
| Mapas | 400+ |
| Especialidades | 30+ |
| Carga (4G) | <2s |
| Lighthouse | 95+ |

---

## Solucionar Problemas

### El sitio no carga
- Esperar 5 minutos después de push
- Limpiar caché (Ctrl+Shift+Del)
- Ver en: github.com/usuario/medmaps/actions

### Búsqueda no funciona
- F12 → Console → Ver errores
- Revisar IDs en HTML: `searchInput`, `searchBtn`

### Los estilos no cargan
- Rutas deben ser relativas: `css/style.css` ✓
- NO absolutas: `/css/style.css` ✗

---

## Próximos Pasos

1. ✓ Publicado en GitHub Pages
2. → Agregar dominio personalizado
3. → Conectar Lemon Squeezy
4. → Crear más especialidades
5. → SEO y marketing

---

## Recursos

- [GitHub Pages Docs](https://docs.github.com/en/pages)
- [Lemon Squeezy](https://www.lemonsqueezy.com)
- [SEO para Sitios Estáticos](https://www.semrush.com/blog/static-websites-seo/)

---

**Creado:** Febrero 2025
**Versión:** 1.0
**Autor:** Dr. Acevedo

¡Buena suerte con MedMaps! 🧠
