# Cola de Revisión MedMaps

Este directorio contiene los mapas mentales pendientes de revisión antes de ser publicados en el portal.

## Flujo de Trabajo

1. **Generación**: El skill `mapa-mental` genera un mapa y lo guarda aquí
2. **Revisión**: El administrador revisa en `admin.html`
3. **Aprobación**: Si se aprueba, se mueve a `data/maps/`
4. **Publicación**: Se actualiza `maps_index.json` y se hace push

## Formato de archivos

Cada mapa se guarda como JSON con la siguiente estructura:

```json
{
  "id": "review_timestamp",
  "title": "Título del Mapa",
  "specialty": "Geriatría",
  "tag": "📚 Revisión",
  "status": "pending",
  "content": "Contenido del mapa...",
  "references": "Referencias Vancouver...",
  "created_at": "2026-02-06T00:00:00Z",
  "source": "skill_mapa_mental"
}
```

## TAGS Disponibles

- `📄 Paper` - Artículos científicos
- `📚 Revisión` - Síntesis de temas
- `⭐ Estudio Pivotal` - Ensayos que cambiaron la práctica
- `📋 Guía Clínica` - Guías y consensos
- `🔬 Fisiopatología` - Ciencia básica
- `💊 Farmacología` - Fármacos
- `🏥 Caso Clínico` - Casos
