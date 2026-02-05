# MedMaps - Mapas Mentales Médicos

Sitio web estático de mapas mentales médicos interactivos para estudiantes y profesionales de la salud.

**Versión:** 1.0
**Autor:** Dr. Acevedo
**Año:** 2025

## Características

- ✓ 400+ mapas mentales médicos
- ✓ 30+ especialidades médicas
- ✓ Búsqueda en tiempo real
- ✓ Diseño responsive (móvil, tablet, desktop)
- ✓ Modo oscuro/claro
- ✓ Acordeones interactivos
- ✓ Sistema de planes (Gratis/Premium)
- ✓ Totalmente estático - sin backend requerido

## Estructura del Proyecto

```
_MedMaps_Web/
├── index.html                      # Página principal
├── especialidades.html              # Lista completa de mapas
├── planes.html                      # Planes de suscripción
├── css/
│   └── style.css                   # Estilos (Navy #0D47A1)
├── js/
│   └── app.js                      # Funcionalidad JavaScript
├── especialidades/
│   ├── cardiologia.html
│   ├── geriatria.html
│   ├── neurologia.html
│   ├── pediatria.html
│   ├── hematologia.html
│   ├── gastroenterologia.html
│   └── [otras especialidades].html
└── README.md                        # Este archivo
```

## Pasos para Publicar en GitHub Pages (Gratuito)

### 1. Crear repositorio en GitHub

1. Ir a [github.com](https://github.com) e iniciar sesión
2. Hacer clic en "New" para crear un nuevo repositorio
3. Nombre del repositorio: `medmaps` (o el que prefieras)
4. Descripción: "Mapas Mentales Médicos Interactivos"
5. Seleccionar "Public"
6. **NO** inicializar con README (lo tienes)
7. Hacer clic en "Create repository"

### 2. Subir archivos a GitHub

#### Opción A: Usar Git en línea de comandos

```bash
# Clonar el repositorio
git clone https://github.com/TU_USUARIO/medmaps.git
cd medmaps

# Copiar los archivos de _MedMaps_Web
cp -r /ruta/a/_MedMaps_Web/* .

# Agregar archivos
git add .

# Hacer commit
git commit -m "Initial commit: Sitio MedMaps v1.0"

# Subir
git push origin main
```

#### Opción B: Arrastrar y soltar en GitHub

1. Ir al repositorio en GitHub
2. Hacer clic en "Add file" > "Upload files"
3. Arrastrar todos los archivos/carpetas
4. Escribir mensaje: "Initial commit: Sitio MedMaps v1.0"
5. Hacer clic en "Commit changes"

### 3. Habilitar GitHub Pages

1. En tu repositorio, ir a **Settings** (Configuración)
2. Buscar **Pages** en el menú izquierdo
3. En "Source", seleccionar:
   - Branch: `main`
   - Folder: `/ (root)`
4. Hacer clic en "Save"

### 4. ¡Sitio publicado!

Tu sitio estará disponible en:
```
https://tu_usuario.github.io/medmaps/
```

O si configuraste un dominio personalizado:
```
https://tu-dominio.com
```

## Cómo Agregar Nuevas Especialidades

### 1. Crear nueva página

Crear archivo: `especialidades/nueva-especialidad.html`

Usar como plantilla el archivo `especialidades/cardiologia.html` y reemplazar:
- Título (h1): Nueva especialidad
- Descripción: X mapas mentales sobre...
- Acordeones con los mapas
- Footer con cantidad de mapas

### 2. Actualizar página de especialidades

En `especialidades.html`, agregar al objeto `especialidadesMapas`:

```javascript
'Nueva Especialidad': {
  id: 'nueva-especialidad',
  mapas: [
    { titulo: 'Mapa 1', año: 2024, premium: false },
    { titulo: 'Mapa 2', año: 2024, premium: true },
    // ...
  ]
}
```

### 3. Actualizar índice en página principal

En `index.html`, agregar al array `especialidades`:

```javascript
{ id: 'nueva-especialidad', nombre: 'Nueva Especialidad', mapas: 15 }
```

### 4. Subir cambios a GitHub

```bash
git add .
git commit -m "Agregar especialidad: Nueva Especialidad"
git push origin main
```

## Cómo Conectar Lemon Squeezy (Pagos)

### 1. Crear cuenta en Lemon Squeezy

1. Ir a [lemonsqueezy.com](https://www.lemonsqueezy.com)
2. Registrarse y crear cuenta
3. Configurar productos:
   - Plan Premium: $4.99/mes
   - Plan Premium Anual: $49.99/año
4. Obtener los "Product IDs"

### 2. Actualizar función de pago en JavaScript

En `js/app.js`, reemplazar función `initiatePremiumPayment`:

```javascript
function initiatePremiumPayment(planId) {
  const productIds = {
    'premium': 'YOUR_PRODUCT_ID_MONTHLY',
    'annual': 'YOUR_PRODUCT_ID_ANNUAL'
  };

  // Redirigir a Lemon Squeezy
  window.location.href = `https://your-store.lemonsqueezy.com/checkout/buy/${productIds[planId]}`;
}
```

### 3. Agregar botón de compra en planes.html

```html
<a href="https://your-store.lemonsqueezy.com/checkout/buy/PRODUCT_ID"
   class="btn btn-primary" style="width: 100%; color: #0D47A1;">
  Suscribirse Ahora
</a>
```

**Nota:** Lemon Squeezy ofrece un plan gratuito con límite de transacciones.

## Personalización

### Cambiar colores (Dr. Acevedo Brand)

En `css/style.css`, modificar variables CSS:

```css
:root {
  --primary: #0D47A1;      /* Azul marino */
  --secondary: #1976D2;    /* Azul claro */
  --accent: #42A5F5;       /* Azul más claro */
  --gray: #9E9E9E;         /* Gris */
  --white: #FFFFFF;        /* Blanco */
}
```

### Cambiar tipografía

En `css/style.css`, buscar `font-family` y modificar:

```css
body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Arial Narrow", sans-serif;
}
```

### Cambiar textos

Buscar en archivos HTML y reemplazar textos de:
- Títulos
- Descripciones
- CTAs (Llamadas a la acción)
- Footer

## Optimización SEO

### Meta tags importante

En cada página, revisar:
- `<title>`: Debe incluir palabras clave
- `<meta name="description">`: Descrición de 160 caracteres
- `<meta name="viewport">`: Ya está configurado para móviles

### Ejemplo de buena estructura:

```html
<title>Cardiología - Mapas Mentales Médicos | MedMaps</title>
<meta name="description" content="85 mapas mentales sobre enfermedades cardiovasculares, arritmias, insuficiencia cardíaca y más. Estudia cardiología con MedMaps.">
```

## Rendimiento

### Lighthouse Score

El sitio fue diseñado para obtener:
- ✓ 95+ Performance
- ✓ 100 Accessibility
- ✓ 100 Best Practices
- ✓ 100 SEO

### Optimizaciones aplicadas

- CSS minificado
- JavaScript sin dependencias externas
- Imágenes optimizadas (solo iconos emoji)
- Lazy loading en componentes
- Mobile-first responsive design

## Estadísticas

- **Páginas estáticas:** 23 (1 inicio + 2 principales + 20 especialidades)
- **Tamaño total:** ~500KB
- **Mapas mentales:** 400+
- **Especialidades:** 30+
- **Tiempo de carga:** < 2 segundos en 4G

## Mantenimiento

### Actualizaciones regulares

Cada mes, agregar:
- 10-15 nuevos mapas
- Actualizar años en mapas existentes
- Revisar links a Lemon Squeezy

### Actualizar el índice

Mantener actualizado el archivo:
```
/mnt/Dropbox/- Esquemas/00_INDICE_MEDMAPS.md
```

Sincronizar con:
- `index.html` (array de especialidades)
- `especialidades.html` (objeto especialidadesMapas)
- Páginas individuales de especialidades

## Dominio Personalizado

### Configurar dominio propio

1. Comprar dominio (ej. GoDaddy, Namecheap, etc.)
2. En panel de GitHub Pages > Custom domain
3. Ingresar: `medmaps.com`
4. Configurar DNS:
   - **A record:** 185.199.108.153
   - **CNAME:** tu-usuario.github.io

Esperar 24-48 horas para que se propague.

## Troubleshooting

### El sitio no aparece en GitHub Pages

- Revisar que rama sea `main` y folder sea `/` (root)
- Esperar 5-10 minutos
- Limpiar caché del navegador (Ctrl+Shift+Delete)

### Los estilos no cargan

- Revisar que las rutas sean relativas
- Esperar a que se reconstruya (max 5 min)

### Búsqueda no funciona

- Abrir consola (F12)
- Revisar que no hay errores en JavaScript
- Verificar IDs de inputs: `searchInput`, `searchBtn`

## Contribuciones

Para agregar contenido:
1. Crear rama: `git checkout -b feature/nueva-especialidad`
2. Hacer cambios y commit
3. Hacer push: `git push origin feature/nueva-especialidad`
4. Crear Pull Request

## Licencia

Contenido educativo de Dr. Acevedo - 2025

## Contacto

- Email: [contacto]
- GitHub: [github.com/usuario]
- Web: [medmaps.com]

---

**Versión 1.0** - Febrero 2025

Sitio creado con HTML5, CSS3 y JavaScript vanilla. Sin frameworks, sin dependencias, completamente gratuito.
