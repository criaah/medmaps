#!/usr/bin/env python3
"""
Herramienta de Revisión de Mapas - MedMaps

Permite:
- Ver mapas por especialidad
- Reclasificar mapas
- Actualizar TAGs y acceso
- Agregar enlaces a mapas relacionados
- Buscar mapas por contenido

Uso:
    python review_maps.py --list              # Ver todos los mapas
    python review_maps.py --specialty General # Ver mapas de una especialidad
    python review_maps.py --reclassify        # Modo reclasificación interactivo
    python review_maps.py --update MAP_ID     # Actualizar un mapa específico
    python review_maps.py --search "término"  # Buscar en contenido
    python review_maps.py --add-links         # Agregar enlaces automáticos a todos
"""

import json
import argparse
import re
from pathlib import Path
from text_to_map import find_related_maps, load_existing_maps

MAPS_DIR = Path("data/maps")
INDEX_FILE = Path("data/maps_index.json")

SPECIALTIES = [
    "Geriatría", "Cardiología", "Neurología", "Nefrología", 
    "Endocrinología", "UCI-Medicina Crítica", "Infectología",
    "Hematología", "Gastroenterología", "Neumología", 
    "Reumatología", "Psiquiatría", "Ortogeriatría", 
    "Pediatría", "General", "Continuum", "Estudios Pivotales"
]

TAGS = [
    "📄 Paper", "📚 Revisión", "⭐ Estudio Pivotal", 
    "📋 Guía Clínica", "🔬 Fisiopatología", "💊 Farmacología", 
    "🏥 Caso Clínico"
]

def load_index():
    with open(INDEX_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_index(data):
    with open(INDEX_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_map(map_id):
    map_file = MAPS_DIR / f"{map_id}.json"
    if not map_file.exists():
        return None
    with open(map_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_map(map_data):
    map_file = MAPS_DIR / f"{map_data['id']}.json"
    with open(map_file, 'w', encoding='utf-8') as f:
        json.dump(map_data, f, ensure_ascii=False, indent=2)

def get_map_text(node, depth=0):
    """Extrae todo el texto de un mapa para búsqueda"""
    text = node.get('text', '')
    for child in node.get('children', []):
        text += ' ' + get_map_text(child, depth+1)
    return text

def list_maps(specialty=None, show_content=False):
    """Lista mapas, opcionalmente filtrados por especialidad"""
    index = load_index()
    
    if specialty:
        index = [m for m in index if m.get('specialty') == specialty]
    
    print(f"\n{'='*60}")
    print(f"📚 MAPAS {'en ' + specialty if specialty else 'TOTALES'}: {len(index)}")
    print('='*60)
    
    for m in index[:50]:  # Limitar a 50
        tag = m.get('tag', '')
        access = '🔒' if m.get('access') == 'premium' else '🆓'
        related = len(m.get('related_maps', []))
        print(f"\n{m['id']}: {m['title'][:50]}")
        print(f"   {m.get('specialty', '?')} | {tag} | {m.get('node_count', 0)} nodos | {related} enlaces | {access}")
    
    if len(index) > 50:
        print(f"\n... y {len(index) - 50} más")

def search_maps(term):
    """Busca mapas por contenido"""
    index = load_index()
    results = []
    
    term_lower = term.lower()
    
    for m in index:
        # Buscar en título
        if term_lower in m.get('title', '').lower():
            results.append((m, 'título'))
            continue
        
        # Buscar en contenido
        map_data = load_map(m['id'])
        if map_data:
            text = get_map_text(map_data.get('root', {}))
            if term_lower in text.lower():
                results.append((m, 'contenido'))
    
    print(f"\n🔍 Búsqueda: '{term}' - {len(results)} resultados\n")
    
    for m, where in results[:20]:
        print(f"{m['id']}: {m['title'][:50]} ({where})")
    
    return results

def reclassify_interactive():
    """Modo interactivo para reclasificar mapas"""
    index = load_index()
    general_maps = [m for m in index if m.get('specialty') == 'General']
    
    print(f"\n📋 Hay {len(general_maps)} mapas en 'General' para reclasificar")
    print("Presiona Enter para saltar, 'q' para salir\n")
    
    for i, s in enumerate(SPECIALTIES, 1):
        print(f"  {i}. {s}")
    print()
    
    updated = 0
    
    for m in general_maps:
        map_data = load_map(m['id'])
        if not map_data:
            continue
        
        # Mostrar preview del mapa
        print(f"\n{'='*50}")
        print(f"📄 {m['id']}: {m['title']}")
        print(f"   Nodos: {m.get('node_count', 0)}")
        
        # Mostrar primeros nodos
        root = map_data.get('root', {})
        print(f"   Raíz: {root.get('text', '')[:60]}")
        for child in root.get('children', [])[:3]:
            print(f"     → {child.get('text', '')[:50]}")
        
        choice = input("\nEspecialidad (número/Enter/q): ").strip()
        
        if choice.lower() == 'q':
            break
        
        if choice.isdigit() and 1 <= int(choice) <= len(SPECIALTIES):
            new_specialty = SPECIALTIES[int(choice) - 1]
            
            # Actualizar mapa
            map_data['specialty'] = new_specialty
            save_map(map_data)
            
            # Actualizar índice
            for idx_m in index:
                if idx_m['id'] == m['id']:
                    idx_m['specialty'] = new_specialty
                    break
            
            print(f"✅ Cambiado a: {new_specialty}")
            updated += 1
    
    save_index(index)
    print(f"\n✅ Actualizados: {updated} mapas")

def add_links_to_all():
    """Agrega enlaces relacionados a todos los mapas"""
    index = load_index()
    updated = 0
    
    print("\n🔗 Agregando enlaces a todos los mapas...")
    
    for m in index:
        map_data = load_map(m['id'])
        if not map_data:
            continue
        
        # Obtener texto del mapa
        text = get_map_text(map_data.get('root', {}))
        
        # Encontrar relacionados
        related = find_related_maps(text, index, m['id'])
        
        if related and related != map_data.get('related_maps', []):
            map_data['related_maps'] = related
            save_map(map_data)
            
            # Actualizar índice
            for idx_m in index:
                if idx_m['id'] == m['id']:
                    idx_m['related_maps'] = related
                    break
            
            updated += 1
            print(f"  {m['id']}: +{len(related)} enlaces")
    
    save_index(index)
    print(f"\n✅ Actualizados: {updated} mapas con enlaces")

def update_map(map_id):
    """Actualiza un mapa específico interactivamente"""
    map_data = load_map(map_id)
    if not map_data:
        print(f"❌ Mapa no encontrado: {map_id}")
        return
    
    print(f"\n📄 Editando: {map_data['title']}")
    print(f"   Especialidad actual: {map_data.get('specialty', 'N/A')}")
    print(f"   TAG actual: {map_data.get('tag', 'N/A')}")
    print(f"   Acceso actual: {map_data.get('access', 'free')}")
    
    # Especialidad
    print("\nEspecialidades:")
    for i, s in enumerate(SPECIALTIES, 1):
        marker = "→" if s == map_data.get('specialty') else " "
        print(f"  {marker} {i}. {s}")
    
    choice = input("\nNueva especialidad (número/Enter para mantener): ").strip()
    if choice.isdigit() and 1 <= int(choice) <= len(SPECIALTIES):
        map_data['specialty'] = SPECIALTIES[int(choice) - 1]
    
    # TAG
    print("\nTAGs:")
    for i, t in enumerate(TAGS, 1):
        marker = "→" if t == map_data.get('tag') else " "
        print(f"  {marker} {i}. {t}")
    
    choice = input("\nNuevo TAG (número/Enter para mantener): ").strip()
    if choice.isdigit() and 1 <= int(choice) <= len(TAGS):
        map_data['tag'] = TAGS[int(choice) - 1]
    
    # Acceso
    choice = input("\nAcceso (f=free, p=premium, Enter para mantener): ").strip().lower()
    if choice == 'f':
        map_data['access'] = 'free'
    elif choice == 'p':
        map_data['access'] = 'premium'
    
    # Guardar
    save_map(map_data)
    
    # Actualizar índice
    index = load_index()
    for m in index:
        if m['id'] == map_id:
            m['specialty'] = map_data.get('specialty')
            m['tag'] = map_data.get('tag')
            m['access'] = map_data.get('access', 'free')
            break
    save_index(index)
    
    print(f"\n✅ Mapa actualizado: {map_id}")

def main():
    parser = argparse.ArgumentParser(description='Revisar y actualizar mapas MedMaps')
    parser.add_argument('--list', '-l', action='store_true', help='Listar todos los mapas')
    parser.add_argument('--specialty', '-s', help='Filtrar por especialidad')
    parser.add_argument('--reclassify', '-r', action='store_true', help='Modo reclasificación')
    parser.add_argument('--update', '-u', help='Actualizar mapa específico')
    parser.add_argument('--search', help='Buscar en contenido')
    parser.add_argument('--add-links', action='store_true', help='Agregar enlaces a todos')
    
    args = parser.parse_args()
    
    if args.list or args.specialty:
        list_maps(args.specialty)
    elif args.reclassify:
        reclassify_interactive()
    elif args.update:
        update_map(args.update)
    elif args.search:
        search_maps(args.search)
    elif args.add_links:
        add_links_to_all()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
