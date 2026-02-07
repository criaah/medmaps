#!/usr/bin/env python3
"""
Conversor de Mapa Mental: Texto Tabulado → JSON para MedMaps

Uso:
    python text_to_map.py --input mapa.txt --specialty "Geriatría" --tag "📚 Revisión"
    python text_to_map.py --interactive
    
El script también detecta términos que podrían enlazar a otros mapas existentes.
"""

import json
import re
import argparse
import os
from pathlib import Path
from datetime import datetime

# Configuración de rutas
MAPS_DIR = Path("data/maps")
INDEX_FILE = Path("data/maps_index.json")

def load_existing_maps():
    """Carga el índice de mapas existentes para buscar enlaces"""
    if not INDEX_FILE.exists():
        return []
    with open(INDEX_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def find_related_maps(content: str, existing_maps: list, current_id: str = None) -> list:
    """
    Encuentra mapas relacionados basándose en términos comunes.
    Retorna lista de IDs de mapas relacionados.
    """
    related = []
    content_lower = content.lower()
    
    # Términos de enlace comunes en medicina
    link_terms = {
        'delirium': ['demencia', 'deterioro cognitivo', 'sedación', 'benzodiacepinas'],
        'fragilidad': ['sarcopenia', 'caídas', 'polifarmacia', 'dependencia funcional'],
        'insuficiencia cardíaca': ['cardiología', 'diuréticos', 'ieca', 'betabloqueadores'],
        'diabetes': ['nefropatía', 'neuropatía', 'pie diabético', 'insulina'],
        'hipertensión': ['sprint', 'cardiovascular', 'ieca', 'ara-ii'],
        'demencia': ['alzheimer', 'deterioro cognitivo', 'delirium', 'neurología'],
        'caídas': ['fragilidad', 'osteoporosis', 'fractura', 'ortogeriatría'],
        'polifarmacia': ['stopp/start', 'deprescripción', 'interacciones', 'anticolinérgicos'],
    }
    
    for map_data in existing_maps:
        if current_id and map_data.get('id') == current_id:
            continue
            
        map_title = map_data.get('title', '').lower()
        map_specialty = map_data.get('specialty', '').lower()
        
        # Buscar coincidencias directas en el título
        title_words = re.findall(r'\w+', map_title)
        for word in title_words:
            if len(word) > 4 and word in content_lower:
                if map_data['id'] not in related:
                    related.append(map_data['id'])
                break
        
        # Buscar términos relacionados
        for term, related_terms in link_terms.items():
            if term in content_lower:
                for rt in related_terms:
                    if rt in map_title:
                        if map_data['id'] not in related:
                            related.append(map_data['id'])
    
    return related[:5]  # Máximo 5 mapas relacionados

def parse_tabbed_text(text: str) -> dict:
    """
    Convierte texto con tabulaciones a estructura de árbol.
    
    Formato de entrada:
        Tema Principal
            Subtema 1
                Detalle 1.1
                Detalle 1.2
            Subtema 2
                **Concepto clave**
    """
    lines = text.strip().split('\n')
    if not lines:
        return {"text": "Sin contenido", "children": []}
    
    # Encontrar la raíz (primera línea no vacía)
    root_line = None
    start_idx = 0
    for i, line in enumerate(lines):
        if line.strip():
            root_line = line.strip()
            start_idx = i + 1
            break
    
    if not root_line:
        return {"text": "Sin contenido", "children": []}
    
    root = {"text": root_line, "children": []}
    
    # Stack para mantener la jerarquía: [(nivel, nodo)]
    stack = [(0, root)]
    
    for line in lines[start_idx:]:
        if not line.strip():
            continue
        
        # Contar tabulaciones para determinar nivel
        tabs = 0
        for char in line:
            if char == '\t':
                tabs += 1
            elif char == ' ':
                # Considerar 4 espacios como 1 tab
                tabs += 0.25
            else:
                break
        
        level = int(tabs) + 1  # +1 porque la raíz es nivel 0
        text = line.strip()
        
        # Procesar formato especial
        # Convertir **negrita** a formato especial
        text = re.sub(r'\*\*(.+?)\*\*', r'⚡\1', text)
        
        new_node = {"text": text, "children": []}
        
        # Encontrar el padre correcto
        while stack and stack[-1][0] >= level:
            stack.pop()
        
        if stack:
            parent = stack[-1][1]
            parent["children"].append(new_node)
        
        stack.append((level, new_node))
    
    return root

def count_nodes(node: dict) -> int:
    """Cuenta el total de nodos en el árbol"""
    count = 1
    for child in node.get("children", []):
        count += count_nodes(child)
    return count

def extract_references(text: str) -> list:
    """Extrae referencias Vancouver del texto"""
    references = []
    lines = text.split('\n')
    in_refs = False
    
    for line in lines:
        line_lower = line.lower().strip()
        if 'referencia' in line_lower or 'bibliography' in line_lower:
            in_refs = True
            continue
        if in_refs and line.strip():
            # Limpiar número inicial si existe
            ref = re.sub(r'^\d+\.\s*', '', line.strip())
            if ref and len(ref) > 10:
                references.append(ref)
    
    return references

def get_next_map_id() -> str:
    """Obtiene el siguiente ID disponible para un mapa"""
    existing = load_existing_maps()
    max_num = 0
    for m in existing:
        match = re.search(r'map_(\d+)', m.get('id', ''))
        if match:
            num = int(match.group(1))
            if num > max_num:
                max_num = num
    return f"map_{max_num + 1:04d}"

def convert_to_json(text: str, specialty: str, tag: str, access: str = "free", 
                    title: str = None) -> dict:
    """Convierte texto tabulado a estructura JSON completa"""
    
    root = parse_tabbed_text(text)
    references = extract_references(text)
    existing_maps = load_existing_maps()
    map_id = get_next_map_id()
    
    # Usar título de la raíz si no se proporciona
    if not title:
        title = root.get("text", "Sin título")
    
    # Encontrar mapas relacionados
    related = find_related_maps(text, existing_maps, map_id)
    
    map_data = {
        "id": map_id,
        "title": title,
        "specialty": specialty,
        "tag": tag,
        "access": access,
        "node_count": count_nodes(root),
        "created_date": datetime.now().strftime("%Y-%m-%d"),
        "related_maps": related,
        "references": references,
        "root": root
    }
    
    return map_data

def save_map(map_data: dict, update_index: bool = True):
    """Guarda el mapa en data/maps/ y actualiza el índice"""
    
    # Crear directorio si no existe
    MAPS_DIR.mkdir(parents=True, exist_ok=True)
    
    # Guardar archivo del mapa
    map_file = MAPS_DIR / f"{map_data['id']}.json"
    with open(map_file, 'w', encoding='utf-8') as f:
        json.dump(map_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Mapa guardado: {map_file}")
    
    if update_index:
        update_maps_index(map_data)
    
    return map_file

def update_maps_index(map_data: dict):
    """Actualiza el archivo maps_index.json"""
    
    existing = load_existing_maps()
    
    # Crear entrada para el índice (sin el árbol completo)
    index_entry = {
        "id": map_data["id"],
        "title": map_data["title"],
        "specialty": map_data["specialty"],
        "tag": map_data["tag"],
        "access": map_data.get("access", "free"),
        "node_count": map_data["node_count"],
        "created_date": map_data.get("created_date"),
        "related_maps": map_data.get("related_maps", [])
    }
    
    # Verificar si ya existe y actualizar
    found = False
    for i, m in enumerate(existing):
        if m["id"] == map_data["id"]:
            existing[i] = index_entry
            found = True
            break
    
    if not found:
        existing.append(index_entry)
    
    # Ordenar por ID
    existing.sort(key=lambda x: x["id"])
    
    with open(INDEX_FILE, 'w', encoding='utf-8') as f:
        json.dump(existing, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Índice actualizado: {INDEX_FILE}")

def interactive_mode():
    """Modo interactivo para crear mapas"""
    print("\n" + "="*60)
    print("📚 CREADOR DE MAPAS MENTALES - MedMaps")
    print("="*60)
    
    print("\nPega el contenido del mapa mental (formato tabulado).")
    print("Cuando termines, escribe 'FIN' en una línea nueva:\n")
    
    lines = []
    while True:
        try:
            line = input()
            if line.strip().upper() == 'FIN':
                break
            lines.append(line)
        except EOFError:
            break
    
    text = '\n'.join(lines)
    
    if not text.strip():
        print("❌ No se proporcionó contenido")
        return
    
    # Especialidades disponibles
    specialties = [
        "Geriatría", "Cardiología", "Neurología", "Nefrología", 
        "Endocrinología", "UCI-Medicina Crítica", "Infectología",
        "Hematología", "Gastroenterología", "Neumología", 
        "Reumatología", "Psiquiatría", "Ortogeriatría", "General"
    ]
    
    print("\n📋 Especialidades disponibles:")
    for i, s in enumerate(specialties, 1):
        print(f"  {i}. {s}")
    
    try:
        choice = int(input("\nSelecciona número de especialidad: "))
        specialty = specialties[choice - 1]
    except:
        specialty = "General"
    
    # TAGs disponibles
    tags = [
        "📄 Paper", "📚 Revisión", "⭐ Estudio Pivotal", 
        "📋 Guía Clínica", "🔬 Fisiopatología", "💊 Farmacología", 
        "🏥 Caso Clínico"
    ]
    
    print("\n🏷️ TAGs disponibles:")
    for i, t in enumerate(tags, 1):
        print(f"  {i}. {t}")
    
    try:
        choice = int(input("\nSelecciona número de TAG: "))
        tag = tags[choice - 1]
    except:
        tag = "📚 Revisión"
    
    # Acceso
    access = input("\n🔐 Acceso (free/premium) [free]: ").strip().lower()
    if access not in ["free", "premium"]:
        access = "free"
    
    # Título personalizado
    title = input("\n📝 Título (Enter para usar el del mapa): ").strip()
    
    # Convertir
    map_data = convert_to_json(text, specialty, tag, access, title or None)
    
    # Mostrar preview
    print("\n" + "="*60)
    print("📋 PREVIEW DEL MAPA")
    print("="*60)
    print(f"ID: {map_data['id']}")
    print(f"Título: {map_data['title']}")
    print(f"Especialidad: {map_data['specialty']}")
    print(f"TAG: {map_data['tag']}")
    print(f"Acceso: {map_data['access']}")
    print(f"Nodos: {map_data['node_count']}")
    
    if map_data['related_maps']:
        print(f"Mapas relacionados: {', '.join(map_data['related_maps'])}")
    
    if map_data['references']:
        print(f"Referencias: {len(map_data['references'])}")
    
    # Confirmar
    confirm = input("\n¿Guardar mapa? (s/n): ").strip().lower()
    if confirm == 's':
        save_map(map_data)
        print(f"\n🎉 Mapa creado exitosamente!")
        print(f"   URL: https://criaah.github.io/medmaps/explorar.html?map={map_data['id']}")
    else:
        print("❌ Cancelado")

def main():
    parser = argparse.ArgumentParser(description='Convertir mapa mental de texto a JSON')
    parser.add_argument('--input', '-i', help='Archivo de texto con el mapa')
    parser.add_argument('--specialty', '-s', default='General', help='Especialidad médica')
    parser.add_argument('--tag', '-t', default='📚 Revisión', help='TAG del mapa')
    parser.add_argument('--access', '-a', default='free', choices=['free', 'premium'], 
                        help='Nivel de acceso')
    parser.add_argument('--title', help='Título personalizado')
    parser.add_argument('--interactive', action='store_true', help='Modo interactivo')
    parser.add_argument('--output', '-o', help='Archivo de salida (opcional)')
    
    args = parser.parse_args()
    
    if args.interactive:
        interactive_mode()
        return
    
    if not args.input:
        print("Uso: python text_to_map.py --input archivo.txt --specialty 'Geriatría'")
        print("     python text_to_map.py --interactive")
        return
    
    # Leer archivo
    with open(args.input, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # Convertir
    map_data = convert_to_json(text, args.specialty, args.tag, args.access, args.title)
    
    # Guardar
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(map_data, f, ensure_ascii=False, indent=2)
        print(f"✅ Guardado en: {args.output}")
    else:
        save_map(map_data)

if __name__ == "__main__":
    main()
