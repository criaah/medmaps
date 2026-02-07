#!/usr/bin/env python3
"""
Procesamiento Masivo de Archivos SMMX y PDF para MedMaps

Este script:
1. Escanea todos los archivos .smmx y .pdf en Dropbox
2. Identifica los que no están en el índice
3. Los procesa usando la estructura de carpetas para clasificar
4. Genera enlaces a mapas relacionados
5. Actualiza el índice

Uso:
    python bulk_process.py --scan              # Solo escanear y reportar
    python bulk_process.py --process           # Procesar todos los nuevos .smmx
    python bulk_process.py --process -n 50     # Procesar solo 50
    python bulk_process.py --process-pdf       # Procesar PDFs
    python bulk_process.py --cleanup           # Reporte de limpieza
"""

import json
import argparse
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import re
import subprocess
import sys

# Configuración
DROPBOX_ESQUEMAS = Path("/sessions/bold-jolly-cerf/mnt/Dropbox/- Esquemas")
MAPS_DIR = Path("data/maps")
INDEX_FILE = Path("data/maps_index.json")

# Mapeo de carpetas a especialidades
FOLDER_TO_SPECIALTY = {
    "geriatría": "Geriatría",
    "cardiología": "Cardiología",
    "neurología": "Neurología",
    "nefrología": "Nefrología",
    "endocrinología": "Endocrinología",
    "uci-medicina crítica": "UCI-Medicina Crítica",
    "uci": "UCI-Medicina Crítica",
    "infectología": "Infectología",
    "hematología": "Hematología",
    "hematología y oncología": "Hematología",
    "gastroenterología": "Gastroenterología",
    "neumología": "Neumología",
    "reumatología": "Reumatología",
    "psiquiatría": "Psiquiatría",
    "ortogeriatría": "Ortogeriatría",
    "pediatría": "Pediatría",
    "dermatología": "Dermatología",
    "oftalmología": "General",
    "otorrinolaringología": "General",
    "cirugía": "General",
    "medicina interna": "General",
    "atención primaria": "General",
    "bioestadística": "General",
    "paliativos": "Geriatría",
    "transversales": "General",
    "continuum": "Continuum",
    "estudios pivotales": "Estudios Pivotales",
    "mksap": "General",
}

# Palabras clave para TAG
TAG_KEYWORDS = {
    "⭐ Estudio Pivotal": ["trial", "study", "ensayo", "sprint", "paradigm", "dapa", "empa", "sglt2", "rct", "horizon"],
    "📋 Guía Clínica": ["guía", "guideline", "aha", "esc", "acc", "nice", "consenso"],
    "🔬 Fisiopatología": ["fisiopatología", "mecanismo", "patogenia", "pathophysiology"],
    "💊 Farmacología": ["fármaco", "drug", "medicamento", "farmacología", "tratamiento"],
    "🏥 Caso Clínico": ["caso", "case", "clinical case"],
    "📄 Paper": ["paper", "artículo", "article", "review"],
}

def load_index():
    """Carga el índice existente"""
    if not INDEX_FILE.exists():
        return []
    with open(INDEX_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_index(data):
    """Guarda el índice"""
    with open(INDEX_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_specialty_from_path(file_path):
    """Determina la especialidad basándose en la ruta del archivo"""
    path_str = str(file_path).lower()

    # Verificar primero si está en Estudios Pivotales
    if "estudios pivotales" in path_str:
        return "Estudios Pivotales"

    if "continuum" in path_str:
        return "Continuum"

    # Buscar en la ruta completa
    for folder, specialty in FOLDER_TO_SPECIALTY.items():
        if folder in path_str:
            return specialty

    return "General"

def get_tag_from_content(title, text=""):
    """Determina el TAG basándose en el contenido"""
    combined = (title + " " + text).lower()

    for tag, keywords in TAG_KEYWORDS.items():
        for kw in keywords:
            if kw in combined:
                return tag

    return "📚 Revisión"  # Default

def parse_smmx(file_path):
    """Extrae el contenido de un archivo .smmx (SimpleMind)"""
    try:
        with zipfile.ZipFile(file_path, 'r') as z:
            # Probar diferentes rutas de XML
            xml_paths = ['document/mindmap.xml', 'document.xml', 'mindmap.xml']
            xml_content = None

            for xml_path in xml_paths:
                try:
                    xml_content = z.read(xml_path)
                    break
                except KeyError:
                    continue

            if xml_content is None:
                return None

        root = ET.fromstring(xml_content)

        # Buscar el elemento mindmap
        mindmap = root.find('mindmap')
        if mindmap is None:
            mindmap = root  # Puede que sea la raíz directamente

        # Obtener topics
        topics_elem = mindmap.find('topics')
        if topics_elem is None:
            return None

        topics_list = list(topics_elem)
        if not topics_list:
            return None

        # Construir diccionario de topics
        topics_dict = {}
        for topic in topics_list:
            topic_id = topic.attrib.get('id', '')
            text = topic.attrib.get('text', '')
            parent = topic.attrib.get('parent', '')
            topics_dict[topic_id] = {
                'text': text,
                'parent': parent,
                'children': []
            }

        # Construir árbol basado en parent
        root_nodes = []
        for topic_id, topic_data in topics_dict.items():
            parent_id = topic_data['parent']
            if parent_id and parent_id in topics_dict:
                topics_dict[parent_id]['children'].append(topic_data)
            elif not parent_id or parent_id not in topics_dict:
                root_nodes.append(topic_data)

        # Limpiar parent references
        def clean_node(node):
            result = {'text': node['text'], 'children': []}
            for child in node['children']:
                result['children'].append(clean_node(child))
            return result

        # Usar el primer root o crear uno
        if root_nodes:
            root_node = clean_node(root_nodes[0])
            # Si hay múltiples roots, agregarlos como children
            if len(root_nodes) > 1:
                for r in root_nodes[1:]:
                    root_node['children'].append(clean_node(r))
        else:
            return None

        title = root_node['text'] or file_path.stem

        # Contar nodos
        def count_nodes(node):
            return 1 + sum(count_nodes(c) for c in node.get('children', []))

        node_count = count_nodes(root_node)

        # Texto completo para búsqueda
        def get_all_text(node):
            text = node.get('text', '')
            for c in node.get('children', []):
                text += ' ' + get_all_text(c)
            return text

        full_text = get_all_text(root_node)

        return {
            'title': title,
            'root': root_node,
            'node_count': node_count,
            'full_text': full_text
        }

    except Exception as e:
        return None

def find_related_maps(text, index, exclude_id=None, max_related=5):
    """Encuentra mapas relacionados basándose en términos médicos"""
    text_lower = text.lower()
    scores = []

    # Términos médicos relevantes
    medical_terms = [
        "delirium", "demencia", "fragilidad", "sarcopenia", "caídas",
        "insuficiencia cardíaca", "fibrilación", "hipertensión", "diabetes",
        "erc", "diálisis", "anemia", "anticoagulación", "polifarmacia",
        "depresión", "parkinson", "alzheimer", "stroke", "acv",
        "neumonía", "sepsis", "shock", "ventilación", "iam", "sca",
        "osteoporosis", "fractura", "cadera", "deglución", "disfagia",
        "incontinencia", "deterioro cognitivo", "agitación"
    ]

    for m in index:
        if m['id'] == exclude_id:
            continue

        score = 0
        m_title = m.get('title', '').lower()

        # Coincidencia de términos
        for term in medical_terms:
            if term in text_lower and term in m_title:
                score += 3

        # Penalizar mapas genéricos
        if m.get('specialty') == 'General':
            score -= 1

        if score > 0:
            scores.append((m['id'], m['title'], score))

    # Ordenar por score
    scores.sort(key=lambda x: x[2], reverse=True)

    return [{'id': s[0], 'title': s[1]} for s in scores[:max_related]]

def scan_smmx_files():
    """Escanea todos los archivos .smmx en Dropbox"""
    all_files = list(DROPBOX_ESQUEMAS.rglob("*.smmx"))

    # Excluir backups y duplicados
    filtered = [f for f in all_files if "_Backup" not in str(f) and "_Duplicados" not in str(f)]

    return filtered

def scan_pdf_files():
    """Escanea PDFs en la carpeta principal de Dropbox"""
    return list(DROPBOX_ESQUEMAS.glob("*.pdf"))

def get_existing_titles(index):
    """Obtiene set de títulos existentes para detectar duplicados"""
    return {m['title'].lower().strip() for m in index}

def scan_and_report():
    """Escanea y genera reporte sin procesar"""
    print("\n📊 ESCANEO DE ARCHIVOS EN DROPBOX\n")
    print("="*60)

    index = load_index()
    existing_titles = get_existing_titles(index)

    # SMMX files
    smmx_files = scan_smmx_files()
    pdf_files = scan_pdf_files()

    print(f"Total archivos .smmx encontrados: {len(smmx_files)}")
    print(f"Total archivos .pdf encontrados: {len(pdf_files)}")
    print(f"Mapas ya en portal: {len(index)}")

    # Clasificar SMMX por estado
    new_files = []
    duplicates = []
    errors = []
    by_specialty = defaultdict(list)

    for f in smmx_files:
        parsed = parse_smmx(f)
        if parsed is None:
            errors.append(f)
            continue

        title_lower = parsed['title'].lower().strip()
        if title_lower in existing_titles:
            duplicates.append((f, parsed['title']))
        else:
            specialty = get_specialty_from_path(f)
            new_files.append((f, parsed, specialty))
            by_specialty[specialty].append(f.name)

    print(f"\n📁 ARCHIVOS SMMX:")
    print(f"  Nuevos para procesar: {len(new_files)}")
    print(f"  Ya existentes: {len(duplicates)}")
    print(f"  Con errores de lectura: {len(errors)}")

    print("\n📊 DISTRIBUCIÓN POR ESPECIALIDAD (nuevos):\n")
    for spec, files in sorted(by_specialty.items(), key=lambda x: -len(x[1])):
        print(f"  {spec}: {len(files)}")

    # Mostrar ejemplos
    print("\n📝 EJEMPLOS DE NUEVOS MAPAS:\n")
    for f, parsed, spec in new_files[:10]:
        print(f"  [{spec}] {parsed['title'][:50]}")

    if len(new_files) > 10:
        print(f"  ... y {len(new_files) - 10} más")

    # PDFs
    print(f"\n📄 ARCHIVOS PDF ({len(pdf_files)}):\n")
    for p in pdf_files[:10]:
        print(f"  {p.stem[:60]}")
    if len(pdf_files) > 10:
        print(f"  ... y {len(pdf_files) - 10} más")

    return new_files, duplicates, errors, pdf_files

def process_smmx_files(new_files, limit=None):
    """Procesa archivos SMMX nuevos y los agrega al portal"""
    index = load_index()

    # Determinar próximo ID
    max_id = 0
    for m in index:
        match = re.search(r'map_(\d+)', m['id'])
        if match:
            max_id = max(max_id, int(match.group(1)))

    next_id = max_id + 1
    processed = 0

    files_to_process = new_files[:limit] if limit else new_files

    print(f"\n🔄 PROCESANDO {len(files_to_process)} ARCHIVOS SMMX...\n")

    for f, parsed, specialty in files_to_process:
        map_id = f"map_{next_id:04d}"

        # Determinar TAG
        tag = get_tag_from_content(parsed['title'], parsed['full_text'])

        # Encontrar mapas relacionados
        related = find_related_maps(parsed['full_text'], index, map_id)

        # Crear estructura del mapa
        map_data = {
            'id': map_id,
            'title': parsed['title'],
            'specialty': specialty,
            'tag': tag,
            'node_count': parsed['node_count'],
            'root': parsed['root'],
            'related_maps': related,
            'source_file': f.name,
            'created': datetime.now().isoformat()
        }

        # Guardar archivo JSON
        map_file = MAPS_DIR / f"{map_id}.json"
        with open(map_file, 'w', encoding='utf-8') as out:
            json.dump(map_data, out, ensure_ascii=False, indent=2)

        # Agregar al índice
        index.append({
            'id': map_id,
            'title': parsed['title'],
            'specialty': specialty,
            'tag': tag,
            'node_count': parsed['node_count'],
            'related_maps': related,
            'access': 'free'
        })

        print(f"  ✅ {map_id}: {parsed['title'][:40]}... [{specialty}]")

        next_id += 1
        processed += 1

    # Guardar índice actualizado
    save_index(index)

    print(f"\n✅ PROCESADOS: {processed} mapas")
    print(f"📊 Total en portal: {len(index)} mapas")

    return processed

def extract_pdf_text(pdf_path):
    """Extrae texto de un PDF usando pdftotext o PyPDF2"""
    try:
        # Intentar con pdftotext (más rápido)
        result = subprocess.run(
            ['pdftotext', '-layout', str(pdf_path), '-'],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout
    except:
        pass

    # Fallback a PyPDF2
    try:
        import PyPDF2
        with open(pdf_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            text = ''
            for page in reader.pages[:20]:  # Limitar a 20 páginas
                text += page.extract_text() + '\n'
            return text
    except:
        pass

    return None

def pdf_to_mindmap(pdf_path, text):
    """Convierte texto de PDF a estructura de mapa mental"""
    lines = text.split('\n')

    # Limpiar líneas
    lines = [l.strip() for l in lines if l.strip()]

    # Extraer título del nombre del archivo
    title = pdf_path.stem
    # Limpiar prefijos comunes
    for prefix in ['Bronco.', 'Cardio', 'Dermato.', 'Endocrino.', 'Hemato Onco.']:
        if title.startswith(prefix):
            title = title.replace(prefix, '').strip()
            break

    # Crear estructura básica
    root = {
        'text': title,
        'children': []
    }

    current_section = None

    for line in lines[:100]:  # Procesar primeras 100 líneas
        # Detectar secciones (mayúsculas, números, etc.)
        if line.isupper() and len(line) > 3 and len(line) < 50:
            current_section = {'text': line.title(), 'children': []}
            root['children'].append(current_section)
        elif current_section and len(line) > 10:
            # Agregar como contenido de la sección
            if len(current_section['children']) < 10:
                current_section['children'].append({'text': line[:100], 'children': []})

    # Si no se encontraron secciones, crear estructura básica
    if not root['children']:
        for i, line in enumerate(lines[:20]):
            if len(line) > 10:
                root['children'].append({'text': line[:100], 'children': []})

    return root, title

def process_pdf_files(pdf_files, limit=None):
    """Procesa archivos PDF y los convierte a mapas mentales"""
    index = load_index()
    existing_titles = get_existing_titles(index)

    # Determinar próximo ID
    max_id = 0
    for m in index:
        match = re.search(r'map_(\d+)', m['id'])
        if match:
            max_id = max(max_id, int(match.group(1)))

    next_id = max_id + 1
    processed = 0

    files_to_process = pdf_files[:limit] if limit else pdf_files

    print(f"\n🔄 PROCESANDO {len(files_to_process)} ARCHIVOS PDF...\n")

    for pdf_path in files_to_process:
        # Verificar que no exista ya
        title_check = pdf_path.stem.lower()
        if title_check in existing_titles:
            print(f"  ⏭️ Ya existe: {pdf_path.stem[:40]}")
            continue

        # Extraer texto
        text = extract_pdf_text(pdf_path)
        if not text:
            print(f"  ❌ No se pudo leer: {pdf_path.stem[:40]}")
            continue

        # Convertir a mapa mental
        root, title = pdf_to_mindmap(pdf_path, text)

        # Determinar especialidad del nombre
        specialty = get_specialty_from_path(pdf_path)

        # Detectar especialidad del prefijo
        name_lower = pdf_path.stem.lower()
        if 'bronco' in name_lower or 'ira' in name_lower:
            specialty = 'Neumología'
        elif 'cardio' in name_lower:
            specialty = 'Cardiología'
        elif 'dermato' in name_lower:
            specialty = 'General'
        elif 'endocrino' in name_lower:
            specialty = 'Endocrinología'
        elif 'hemato' in name_lower:
            specialty = 'Hematología'
        elif 'neuro' in name_lower:
            specialty = 'Neurología'
        elif 'nefro' in name_lower:
            specialty = 'Nefrología'

        map_id = f"map_{next_id:04d}"

        # Contar nodos
        def count_nodes(node):
            return 1 + sum(count_nodes(c) for c in node.get('children', []))

        node_count = count_nodes(root)
        tag = get_tag_from_content(title, text[:500])

        # Encontrar mapas relacionados
        related = find_related_maps(text[:1000], index, map_id)

        # Crear estructura del mapa
        map_data = {
            'id': map_id,
            'title': title,
            'specialty': specialty,
            'tag': tag,
            'node_count': node_count,
            'root': root,
            'related_maps': related,
            'source_file': pdf_path.name,
            'source_type': 'pdf',
            'created': datetime.now().isoformat()
        }

        # Guardar archivo JSON
        map_file = MAPS_DIR / f"{map_id}.json"
        with open(map_file, 'w', encoding='utf-8') as out:
            json.dump(map_data, out, ensure_ascii=False, indent=2)

        # Agregar al índice
        index.append({
            'id': map_id,
            'title': title,
            'specialty': specialty,
            'tag': tag,
            'node_count': node_count,
            'related_maps': related,
            'access': 'free'
        })

        print(f"  ✅ {map_id}: {title[:40]}... [{specialty}]")

        next_id += 1
        processed += 1

        # Actualizar títulos existentes
        existing_titles.add(title.lower())

    # Guardar índice actualizado
    save_index(index)

    print(f"\n✅ PROCESADOS: {processed} PDFs convertidos a mapas")
    print(f"📊 Total en portal: {len(index)} mapas")

    return processed

def cleanup_report():
    """Genera reporte de archivos que pueden limpiarse"""
    print("\n🧹 ANÁLISIS DE LIMPIEZA\n")
    print("="*60)

    # Archivos en la carpeta principal
    all_files = list(DROPBOX_ESQUEMAS.glob("*"))

    pdfs = [f for f in all_files if f.is_file() and f.suffix == '.pdf']
    images = [f for f in all_files if f.is_file() and f.suffix.lower() in ['.png', '.jpg', '.jpeg']]
    others = [f for f in all_files if f.is_file() and not f.name.startswith('.')
              and f.suffix not in ['.pdf', '.png', '.jpg', '.jpeg', '.smmx', '.md']]

    print(f"\n📄 PDFs en carpeta raíz: {len(pdfs)}")
    total_pdf_size = sum(f.stat().st_size for f in pdfs) / (1024*1024)
    print(f"   Tamaño total: {total_pdf_size:.1f} MB")

    print(f"\n🖼️ Imágenes: {len(images)}")
    print(f"📁 Otros archivos: {len(others)}")
    for o in others[:5]:
        print(f"    {o.name}")

    # Carpeta de backups
    backup_path = DROPBOX_ESQUEMAS / "_Backup_Duplicados"
    if backup_path.exists():
        backup_files = list(backup_path.rglob("*"))
        backup_size = sum(f.stat().st_size for f in backup_files if f.is_file()) / (1024*1024)
        print(f"\n💾 Carpeta _Backup_Duplicados: {len(backup_files)} archivos ({backup_size:.1f} MB)")

    print("\n💡 RECOMENDACIONES:")
    print("  1. Los PDFs pueden convertirse a mapas con --process-pdf")
    print("  2. La carpeta _Backup_Duplicados puede eliminarse después de verificar")
    print("  3. Los archivos .smmx ya procesados permanecen como fuente")

def main():
    parser = argparse.ArgumentParser(description='Procesamiento masivo de mapas')
    parser.add_argument('--scan', action='store_true', help='Solo escanear y reportar')
    parser.add_argument('--process', action='store_true', help='Procesar archivos SMMX nuevos')
    parser.add_argument('--process-pdf', action='store_true', help='Procesar archivos PDF')
    parser.add_argument('-n', '--limit', type=int, help='Limitar cantidad a procesar')
    parser.add_argument('--cleanup', action='store_true', help='Reporte de limpieza')
    parser.add_argument('--auto', action='store_true', help='Procesar sin confirmación')

    args = parser.parse_args()

    if args.scan:
        scan_and_report()
    elif args.process:
        new_files, _, _, _ = scan_and_report()
        if new_files:
            if args.auto:
                process_smmx_files(new_files, args.limit)
            else:
                confirm = input(f"\n¿Procesar {args.limit or len(new_files)} mapas? (s/n): ")
                if confirm.lower() == 's':
                    process_smmx_files(new_files, args.limit)
    elif args.process_pdf:
        _, _, _, pdf_files = scan_and_report()
        if pdf_files:
            if args.auto:
                process_pdf_files(pdf_files, args.limit)
            else:
                confirm = input(f"\n¿Procesar {args.limit or len(pdf_files)} PDFs? (s/n): ")
                if confirm.lower() == 's':
                    process_pdf_files(pdf_files, args.limit)
    elif args.cleanup:
        cleanup_report()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
