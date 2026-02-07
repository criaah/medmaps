#!/usr/bin/env python3
"""
Procesador de Inbox - MedMaps

Lee archivos de la carpeta inbox (Dropbox) y los convierte a JSON para el portal.
Soporta:
- .smmx (SimpleMind Pro)
- .txt (formato texto tabulado)

Uso:
    python process_inbox.py                    # Procesar todo el inbox
    python process_inbox.py --file archivo.txt # Procesar archivo específico
    python process_inbox.py --watch            # Modo observador (futuro)
"""

import os
import sys
import json
import zipfile
import xml.etree.ElementTree as ET
import shutil
import argparse
from pathlib import Path
from datetime import datetime

# Importar funciones del conversor de texto
from text_to_map import parse_tabbed_text, count_nodes, extract_references, \
    find_related_maps, load_existing_maps, save_map, get_next_map_id

# Configuración de rutas
DROPBOX_BASE = Path(os.path.expanduser("~/Dropbox/MedMaps"))
INBOX_DIR = DROPBOX_BASE / "inbox"
TEXTOS_DIR = DROPBOX_BASE / "textos"
PUBLICADOS_DIR = DROPBOX_BASE / "publicados"
MAPS_DIR = Path("data/maps")

# Intentar rutas alternativas si no existe
if not DROPBOX_BASE.exists():
    DROPBOX_BASE = Path("/sessions/bold-jolly-cerf/mnt/Dropbox/MedMaps")
    INBOX_DIR = DROPBOX_BASE / "inbox"
    TEXTOS_DIR = DROPBOX_BASE / "textos"
    PUBLICADOS_DIR = DROPBOX_BASE / "publicados"

def parse_smmx_file(filepath: Path) -> dict:
    """Parsea un archivo .smmx de SimpleMind Pro"""
    
    with zipfile.ZipFile(filepath, 'r') as zf:
        # Buscar el archivo XML principal
        xml_file = None
        for name in zf.namelist():
            if name.endswith('.xml') and not name.startswith('__'):
                xml_file = name
                break
        
        if not xml_file:
            raise ValueError(f"No se encontró XML en {filepath}")
        
        with zf.open(xml_file) as f:
            tree = ET.parse(f)
            root = tree.getroot()
    
    # Parsear la estructura del mapa
    def parse_node(element):
        text = ""
        children = []
        
        # Buscar texto del nodo
        for child in element:
            if child.tag == 'text':
                text = child.text or ""
            elif child.tag == 'node' or child.tag == 'children':
                if child.tag == 'children':
                    for subchild in child:
                        if subchild.tag == 'node':
                            children.append(parse_node(subchild))
                else:
                    children.append(parse_node(child))
        
        return {"text": text.strip(), "children": children}
    
    # Encontrar el nodo raíz
    root_node = None
    for elem in root.iter():
        if elem.tag == 'mindmap' or elem.tag == 'map':
            for child in elem:
                if child.tag == 'node':
                    root_node = parse_node(child)
                    break
    
    if not root_node:
        # Intento alternativo de parsing
        for elem in root.iter('node'):
            root_node = parse_node(elem)
            break
    
    return root_node or {"text": "Sin contenido", "children": []}

def process_smmx(filepath: Path, specialty: str = "General", 
                 tag: str = "📚 Revisión", access: str = "free") -> dict:
    """Procesa un archivo .smmx y retorna datos del mapa"""
    
    root = parse_smmx_file(filepath)
    existing_maps = load_existing_maps()
    map_id = get_next_map_id()
    
    # Extraer título del nombre del archivo o del nodo raíz
    title = root.get("text", filepath.stem)
    
    # Buscar mapas relacionados
    content_text = json.dumps(root, ensure_ascii=False)
    related = find_related_maps(content_text, existing_maps, map_id)
    
    map_data = {
        "id": map_id,
        "title": title,
        "specialty": specialty,
        "tag": tag,
        "access": access,
        "node_count": count_nodes(root),
        "created_date": datetime.now().strftime("%Y-%m-%d"),
        "source_file": filepath.name,
        "related_maps": related,
        "references": [],
        "root": root
    }
    
    return map_data

def process_txt(filepath: Path, specialty: str = "General",
                tag: str = "📚 Revisión", access: str = "free") -> dict:
    """Procesa un archivo de texto tabulado"""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    
    root = parse_tabbed_text(text)
    references = extract_references(text)
    existing_maps = load_existing_maps()
    map_id = get_next_map_id()
    
    title = root.get("text", filepath.stem)
    content_text = text
    related = find_related_maps(content_text, existing_maps, map_id)
    
    map_data = {
        "id": map_id,
        "title": title,
        "specialty": specialty,
        "tag": tag,
        "access": access,
        "node_count": count_nodes(root),
        "created_date": datetime.now().strftime("%Y-%m-%d"),
        "source_file": filepath.name,
        "related_maps": related,
        "references": references,
        "root": root
    }
    
    return map_data

def prompt_metadata():
    """Pide al usuario los metadatos del mapa"""
    
    specialties = [
        "Geriatría", "Cardiología", "Neurología", "Nefrología", 
        "Endocrinología", "UCI-Medicina Crítica", "Infectología",
        "Hematología", "Gastroenterología", "Neumología", 
        "Reumatología", "Psiquiatría", "Ortogeriatría", "General"
    ]
    
    tags = [
        "📄 Paper", "📚 Revisión", "⭐ Estudio Pivotal", 
        "📋 Guía Clínica", "🔬 Fisiopatología", "💊 Farmacología", 
        "🏥 Caso Clínico"
    ]
    
    print("\n📋 Especialidades:")
    for i, s in enumerate(specialties, 1):
        print(f"  {i}. {s}")
    
    try:
        choice = int(input("Selecciona (número): "))
        specialty = specialties[choice - 1]
    except:
        specialty = "General"
    
    print("\n🏷️ TAGs:")
    for i, t in enumerate(tags, 1):
        print(f"  {i}. {t}")
    
    try:
        choice = int(input("Selecciona (número): "))
        tag = tags[choice - 1]
    except:
        tag = "📚 Revisión"
    
    access = input("\n🔐 Acceso (free/premium) [free]: ").strip().lower()
    if access not in ["free", "premium"]:
        access = "free"
    
    return specialty, tag, access

def process_inbox(interactive: bool = True):
    """Procesa todos los archivos en la carpeta inbox"""
    
    if not INBOX_DIR.exists():
        print(f"❌ No existe la carpeta inbox: {INBOX_DIR}")
        print("   Créala en Dropbox/MedMaps/inbox/")
        return
    
    # Buscar archivos procesables
    files = []
    for ext in ['*.smmx', '*.txt']:
        files.extend(INBOX_DIR.glob(ext))
    
    if not files:
        print("📭 Inbox vacío - no hay archivos para procesar")
        return
    
    print(f"\n📥 Encontrados {len(files)} archivos en inbox:\n")
    
    for i, f in enumerate(files, 1):
        print(f"  {i}. {f.name}")
    
    for filepath in files:
        print(f"\n{'='*50}")
        print(f"📄 Procesando: {filepath.name}")
        print('='*50)
        
        try:
            # Pedir metadatos
            if interactive:
                specialty, tag, access = prompt_metadata()
            else:
                specialty, tag, access = "General", "📚 Revisión", "free"
            
            # Procesar según tipo
            if filepath.suffix.lower() == '.smmx':
                map_data = process_smmx(filepath, specialty, tag, access)
            else:
                map_data = process_txt(filepath, specialty, tag, access)
            
            # Mostrar preview
            print(f"\n📋 Preview:")
            print(f"   ID: {map_data['id']}")
            print(f"   Título: {map_data['title']}")
            print(f"   Nodos: {map_data['node_count']}")
            print(f"   Relacionados: {len(map_data['related_maps'])}")
            
            # Confirmar
            if interactive:
                confirm = input("\n¿Guardar? (s/n): ").strip().lower()
            else:
                confirm = 's'
            
            if confirm == 's':
                # Guardar mapa
                save_map(map_data)
                
                # Mover archivo a publicados
                dest = PUBLICADOS_DIR / filepath.name
                shutil.move(str(filepath), str(dest))
                print(f"📦 Archivo movido a: {dest}")
                
                print(f"✅ Mapa {map_data['id']} creado exitosamente")
            else:
                print("⏭️ Saltado")
                
        except Exception as e:
            print(f"❌ Error procesando {filepath.name}: {e}")
            import traceback
            traceback.print_exc()

def main():
    parser = argparse.ArgumentParser(description='Procesar inbox de MedMaps')
    parser.add_argument('--file', '-f', help='Archivo específico a procesar')
    parser.add_argument('--batch', '-b', action='store_true', 
                        help='Modo batch (sin preguntas)')
    parser.add_argument('--specialty', '-s', default='General')
    parser.add_argument('--tag', '-t', default='📚 Revisión')
    parser.add_argument('--access', '-a', default='free')
    
    args = parser.parse_args()
    
    print("\n" + "="*50)
    print("📥 PROCESADOR DE INBOX - MedMaps")
    print("="*50)
    
    if args.file:
        filepath = Path(args.file)
        if not filepath.exists():
            filepath = INBOX_DIR / args.file
        
        if not filepath.exists():
            print(f"❌ Archivo no encontrado: {args.file}")
            return
        
        # Procesar archivo específico
        if filepath.suffix.lower() == '.smmx':
            map_data = process_smmx(filepath, args.specialty, args.tag, args.access)
        else:
            map_data = process_txt(filepath, args.specialty, args.tag, args.access)
        
        save_map(map_data)
        print(f"✅ Mapa creado: {map_data['id']}")
    else:
        process_inbox(interactive=not args.batch)

if __name__ == "__main__":
    main()
