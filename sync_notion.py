#!/usr/bin/env python3
"""
MedMaps - Sincronización con Notion
====================================
Este script sincroniza los mapas mentales con una base de datos de Notion.

Uso:
    python sync_notion.py --setup      # Crear base de datos en Notion
    python sync_notion.py --sync       # Sincronizar mapas existentes
    python sync_notion.py --status     # Ver estado de sincronización
"""

import os
import json
import argparse
from pathlib import Path
from datetime import datetime

try:
    from notion_client import Client
    from dotenv import load_dotenv
except ImportError:
    print("Instalando dependencias...")
    os.system("pip install notion-client python-dotenv -q")
    from notion_client import Client
    from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")

# Configuración de TAGs y Estados
TAGS = [
    "📄 Paper",
    "📚 Revisión", 
    "⭐ Estudio Pivotal",
    "📋 Guía Clínica",
    "🔬 Fisiopatología",
    "💊 Farmacología",
    "🏥 Caso Clínico"
]

ESTADOS = [
    {"name": "No Subido", "color": "gray"},
    {"name": "En Revisión", "color": "yellow"},
    {"name": "Gratis", "color": "green"},
    {"name": "Premium", "color": "blue"},
    {"name": "Archivado", "color": "red"}
]

ESPECIALIDADES = [
    "Geriatría", "Cardiología", "Neurología", "Nefrología",
    "Endocrinología", "UCI-Medicina Crítica", "Infectología",
    "Hematología", "Gastroenterología", "Neumología",
    "Reumatología", "Psiquiatría", "Ortogeriatría", 
    "Pediatría", "General", "Continuum", "Estudios Pivotales"
]


def get_notion_client():
    """Obtener cliente de Notion"""
    if not NOTION_TOKEN:
        print("❌ Error: NOTION_TOKEN no configurado en .env")
        return None
    return Client(auth=NOTION_TOKEN)


def setup_database(notion, parent_page_id):
    """Crear base de datos de MedMaps en Notion"""
    print("🔧 Creando base de datos de MedMaps en Notion...")
    
    try:
        database = notion.databases.create(
            parent={"type": "page_id", "page_id": parent_page_id},
            title=[{"type": "text", "text": {"content": "📚 MedMaps - Gestión de Mapas Mentales"}}],
            icon={"type": "emoji", "emoji": "🧠"},
            properties={
                "Título": {"title": {}},
                "Especialidad": {
                    "select": {
                        "options": [{"name": s, "color": "default"} for s in ESPECIALIDADES]
                    }
                },
                "TAG": {
                    "select": {
                        "options": [{"name": t, "color": "default"} for t in TAGS]
                    }
                },
                "Estado": {
                    "select": {
                        "options": ESTADOS
                    }
                },
                "Nodos": {"number": {"format": "number"}},
                "Fecha Creación": {"date": {}},
                "Última Actualización": {"date": {}},
                "ID Mapa": {"rich_text": {}},
                "URL Portal": {"url": {}},
                "Notas": {"rich_text": {}}
            }
        )
        
        db_id = database["id"]
        print(f"✅ Base de datos creada exitosamente!")
        print(f"📋 Database ID: {db_id}")
        print(f"\n⚠️  Agrega este ID a tu archivo .env:")
        print(f"   NOTION_DATABASE_ID={db_id}")
        
        # Actualizar .env automáticamente
        env_path = Path(__file__).parent / ".env"
        if env_path.exists():
            content = env_path.read_text()
            content = content.replace("NOTION_DATABASE_ID=", f"NOTION_DATABASE_ID={db_id}")
            env_path.write_text(content)
            print(f"\n✅ .env actualizado automáticamente")
        
        return db_id
        
    except Exception as e:
        print(f"❌ Error creando base de datos: {e}")
        return None


def sync_maps_to_notion(notion, database_id):
    """Sincronizar mapas existentes a Notion"""
    print("🔄 Sincronizando mapas con Notion...")
    
    # Cargar índice de mapas
    maps_index_path = Path(__file__).parent / "data" / "maps_index.json"
    if not maps_index_path.exists():
        print("❌ No se encontró maps_index.json")
        return
    
    with open(maps_index_path) as f:
        maps = json.load(f)
    
    print(f"📊 Encontrados {len(maps)} mapas para sincronizar")
    
    # Obtener páginas existentes en Notion
    existing = {}
    try:
        results = notion.databases.query(database_id=database_id)
        for page in results.get("results", []):
            props = page.get("properties", {})
            map_id = props.get("ID Mapa", {}).get("rich_text", [])
            if map_id:
                existing[map_id[0]["text"]["content"]] = page["id"]
    except Exception as e:
        print(f"⚠️ Error consultando existentes: {e}")
    
    synced = 0
    updated = 0
    
    for map_data in maps:
        map_id = map_data.get("id", "")
        title = map_data.get("title", "Sin título")
        specialty = map_data.get("specialty", "General")
        node_count = map_data.get("node_count", 0)
        
        page_data = {
            "Título": {"title": [{"text": {"content": title[:100]}}]},
            "Especialidad": {"select": {"name": specialty if specialty in ESPECIALIDADES else "General"}},
            "Estado": {"select": {"name": "Gratis"}},  # Default a gratis
            "Nodos": {"number": node_count},
            "ID Mapa": {"rich_text": [{"text": {"content": map_id}}]},
            "URL Portal": {"url": f"https://criaah.github.io/medmaps/explorar.html?map={map_id}"},
            "Última Actualización": {"date": {"start": datetime.now().isoformat()}}
        }
        
        try:
            if map_id in existing:
                # Actualizar existente
                notion.pages.update(page_id=existing[map_id], properties=page_data)
                updated += 1
            else:
                # Crear nuevo
                notion.pages.create(parent={"database_id": database_id}, properties=page_data)
                synced += 1
                
            if (synced + updated) % 50 == 0:
                print(f"  Progreso: {synced + updated}/{len(maps)}")
                
        except Exception as e:
            print(f"  ⚠️ Error con {map_id}: {e}")
    
    print(f"\n✅ Sincronización completada!")
    print(f"   📝 Nuevos: {synced}")
    print(f"   🔄 Actualizados: {updated}")


def show_status(notion, database_id):
    """Mostrar estado de la base de datos"""
    print("📊 Estado de MedMaps en Notion\n")
    
    try:
        # Contar por estado
        results = notion.databases.query(database_id=database_id)
        pages = results.get("results", [])
        
        estados = {}
        especialidades = {}
        
        for page in pages:
            props = page.get("properties", {})
            
            estado = props.get("Estado", {}).get("select", {})
            if estado:
                name = estado.get("name", "Sin estado")
                estados[name] = estados.get(name, 0) + 1
            
            esp = props.get("Especialidad", {}).get("select", {})
            if esp:
                name = esp.get("name", "General")
                especialidades[name] = especialidades.get(name, 0) + 1
        
        print(f"Total de mapas en Notion: {len(pages)}\n")
        
        print("Por Estado:")
        for estado, count in sorted(estados.items(), key=lambda x: -x[1]):
            print(f"  {estado}: {count}")
        
        print("\nPor Especialidad (top 10):")
        for esp, count in sorted(especialidades.items(), key=lambda x: -x[1])[:10]:
            print(f"  {esp}: {count}")
            
    except Exception as e:
        print(f"❌ Error: {e}")


def main():
    parser = argparse.ArgumentParser(description="MedMaps - Sincronización con Notion")
    parser.add_argument("--setup", metavar="PAGE_ID", help="Crear base de datos (requiere ID de página padre)")
    parser.add_argument("--sync", action="store_true", help="Sincronizar mapas a Notion")
    parser.add_argument("--status", action="store_true", help="Mostrar estado")
    
    args = parser.parse_args()
    
    notion = get_notion_client()
    if not notion:
        return
    
    if args.setup:
        setup_database(notion, args.setup)
    elif args.sync:
        if not NOTION_DATABASE_ID:
            print("❌ NOTION_DATABASE_ID no configurado. Ejecuta --setup primero.")
            return
        sync_maps_to_notion(notion, NOTION_DATABASE_ID)
    elif args.status:
        if not NOTION_DATABASE_ID:
            print("❌ NOTION_DATABASE_ID no configurado.")
            return
        show_status(notion, NOTION_DATABASE_ID)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
