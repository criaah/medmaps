# 🚀 Cómo Publicar MedMaps en GitHub Pages

## Pasos para Subir tu Sitio Web

### 1. Crear el Repositorio en GitHub

1. Ve a [github.com](https://github.com) e inicia sesión
2. Haz clic en el botón verde **"New"** (o el **+** en la esquina superior derecha)
3. Nombre del repositorio: `medmaps` (o `medmaps.github.io` si quieres URL personalizada)
4. Descripción: "Mapas mentales médicos interactivos"
5. Selecciona **Public**
6. **NO** marques "Add a README file"
7. Haz clic en **Create repository**

### 2. Subir los Archivos

#### Opción A: Desde la web de GitHub (más fácil)
1. En la página del repositorio vacío, haz clic en **"uploading an existing file"**
2. Arrastra toda la carpeta `_MedMaps_Web` a la ventana
3. Escribe un mensaje de commit: "Versión inicial de MedMaps"
4. Haz clic en **Commit changes**

#### Opción B: Usando Terminal (más profesional)
```bash
# En tu computadora, navega a la carpeta
cd ~/Dropbox/- Esquemas/_MedMaps_Web

# Inicializa git
git init

# Agrega todos los archivos
git add .

# Crea el primer commit
git commit -m "Versión inicial de MedMaps"

# Conecta con GitHub (reemplaza TU_USUARIO)
git remote add origin https://github.com/TU_USUARIO/medmaps.git

# Sube los archivos
git branch -M main
git push -u origin main
```

### 3. Activar GitHub Pages

1. En tu repositorio, ve a **Settings** (⚙️ engranaje)
2. En el menú lateral, busca **Pages**
3. En "Source", selecciona:
   - Branch: `main`
   - Folder: `/ (root)`
4. Haz clic en **Save**
5. ¡Espera 1-2 minutos!

### 4. Tu URL será:
```
https://TU_USUARIO.github.io/medmaps/
```

---

## 📁 Estructura de Archivos para Subir

```
_MedMaps_Web/
├── index.html          ← Página principal
├── especialidades.html ← Lista de mapas
├── planes.html         ← Planes de suscripción
├── css/
│   └── style.css       ← Estilos
└── js/
    └── app.js          ← JavaScript
```

---

## 🎨 Personalización Posterior

### Cambiar dominio personalizado
1. Compra un dominio (ej: medmaps.cl)
2. En Settings > Pages > Custom domain, ingresa tu dominio
3. Configura DNS en tu proveedor:
   - CNAME: `www` → `tu-usuario.github.io`
   - A records: Apuntar a IPs de GitHub Pages

### Agregar Google Analytics
Agrega antes de `</head>` en cada HTML:
```html
<script async src="https://www.googletagmanager.com/gtag/js?id=TU-ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'TU-ID');
</script>
```

---

## 💳 Para Activar Pagos (Lemon Squeezy)

1. Crea cuenta en [lemonsqueezy.com](https://lemonsqueezy.com)
2. Crea un producto "MedMaps Premium" ($4.990 CLP/mes)
3. Obtén el link de checkout
4. Reemplaza el botón de suscripción en `planes.html`

---

## ✅ Checklist Final

- [ ] Repositorio creado en GitHub
- [ ] Archivos subidos
- [ ] GitHub Pages activado
- [ ] URL funcionando
- [ ] Probado en móvil
- [ ] Dark mode funcionando
- [ ] Búsqueda funcionando

---

**¿Problemas?** El sitio puede tardar hasta 10 minutos en estar disponible después de activar GitHub Pages.

*Última actualización: Febrero 2026*
