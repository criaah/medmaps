#!/usr/bin/env python3
"""
Búsqueda Rápida de Mapas MedMaps

Uso:
    python search_maps.py "término"
    python search_maps.py --related "delirium"
    python search_maps.py --stats
"""

import json
import sys
from pathlib import Path

MAPS_DIR = Path("data/maps")
INDEX_FILE = Path("data/maps_index.json")

# Relaciones temáticas predefinidas
RELATED_TOPICS = {
    "delirium": ["demencia", "polifarmacia", "fragilidad", "uci", "cam", "agitación"],
    "fragilidad": ["sarcopenia", "caídas", "polifarmacia", "cfs", "deterioro funcional"],
    "insuficiencia cardíaca": ["sglt2", "diuréticos", "cardiorrenal", "bnp", "fevi"],
    "diabetes": ["erc", "neuropatía", "sglt2", "hipoglicemia", "hba1c"],
    "demencia": ["delirium", "dcl", "parkinson", "alzheimer", "lewy", "dft"],
    "acv": ["fibrilación", "anticoagulación", "nihss", "stroke", "isquémico"],
    "stroke": ["fibrilación", "anticoagulación", "nihss", "acv", "isquémico"],
    "sepsis": ["shock", "uci", "antimicrobianos", "sofa", "qsofa"],
    "fractura": ["osteoporosis", "caídas", "ortogeriatría", "cadera", "vte"],
    "parkinson": ["demencia", "lewy", "diskinesia", "temblor", "bradicinesia"],
    "erc": ["diálisis", "anemia", "hipertensión", "kdigo", "nefropatía"],
    "fibrilación": ["anticoagulación", "acv", "cha2ds2", "ablación", "cardioversión"],
    "neumonía": ["sepsis", "antimicrobianos", "curb", "nac", "respiratorio"],
    "osteoporosis": ["caídas", "fractura", "vitamina d", "bifosfonatos", "dexa"],
}

def load_index():
    with open(INDEX_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def search(term, index):
    """Búsqueda simple por término"""
    term_lower = term.lower()
    results = []

    for m in index:
        title_lower = m.get('title', '').lower()
        if term_lower in title_lower:
            results.append(m)

    return results

def search_related(term, index):
    """Búsqueda incluyendo términos relacionados"""
    term_lower = term.lower()
    all_terms = [term_lower]

    # Agregar términos relacionados
    for key, related in RELATED_TOPICS.items():
        if key in term_lower or term_lower in key:
            all_terms.extend(related)

    all_terms = list(set(all_terms))
    results = []
    seen_ids = set()

    for t in all_terms:
        for m in index:
            if m['id'] in seen_ids:
                continue
            title_lower = m.get('title', '').lower()
            if t in title_lower:
                results.append((m, t))
                seen_ids.add(m['id'])

    return results

def print_stats(index):
    """Muestra estadísticas del portal"""
    from collections import Counter

    specs = Counter(m.get('specialty', 'N/A') for m in index)
    tags = Counter(m.get('tag', 'N/A') for m in index)

    print(f"\n📊 ESTADÍSTICAS MEDMAPS")
    print("="*50)
    print(f"\nTotal mapas: {len(index)}")

    print("\n📁 Por especialidad:")
    for spec, count in specs.most_common():
        print(f"  {spec}: {count}")

    print("\n🏷️ Por TAG:")
    for tag, count in tags.most_common():
        print(f"  {tag}: {count}")

def main():
    index = load_index()

    if len(sys.argv) < 2:
        print("Uso: python search_maps.py <término>")
        print("     python search_maps.py --related <término>")
        print("     python search_maps.py --stats")
        return

    if sys.argv[1] == "--stats":
        print_stats(index)
        return

    if sys.argv[1] == "--related" and len(sys.argv) > 2:
        term = sys.argv[2]
        results = search_related(term, index)

        print(f"\n🔗 BÚSQUEDA RELACIONADA: '{term}'")
        print("="*50)

        if not results:
            print("No se encontraron mapas relacionados.")
            return

        print(f"Encontrados: {len(results)} mapas\n")

        for m, matched_term in results[:20]:
            print(f"  [{m['id']}] {m['title'][:50]}...")
            print(f"      Especialidad: {m.get('specialty')} | Match: {matched_term}")

        if len(results) > 20:
            print(f"\n  ... y {len(results) - 20} más")

    else:
        term = sys.argv[1]
        results = search(term, index)

        print(f"\n🔍 BÚSQUEDA: '{term}'")
        print("="*50)

        if not results:
            print("No se encontraron mapas.")
            # Sugerir búsqueda relacionada
            print(f"\n💡 Intenta: python search_maps.py --related \"{term}\"")
            return

        print(f"Encontrados: {len(results)} mapas\n")

        for m in results[:20]:
            tag = m.get('tag', '')
            spec = m.get('specialty', '')
            nodes = m.get('node_count', 0)
            print(f"  [{m['id']}] {m['title'][:50]}...")
            print(f"      {spec} | {tag} | {nodes} nodos")

        if len(results) > 20:
            print(f"\n  ... y {len(results) - 20} más")

if __name__ == "__main__":
    main()
