#!/usr/bin/env python3
"""
Procesador de Recursos - MedMaps

Agrega guías de estudio, presentaciones (PDF + audio) y documentos al portal
de recursos (recursos.html). Copia los archivos a resources/ y actualiza
data/resources_index.json.

Uso:
    # Guía de estudio (markdown)
    python process_resources.py add guia_epoc.md --type guia \
        --title "Guía de estudio: EPOC" --specialty "Neumología"

    # Presentación PDF con audio
    python process_resources.py add clase_ic.pdf --type presentacion \
        --title "Insuficiencia cardíaca" --specialty "Cardiología" \
        --audio parte1.mp3 parte2.mp3

    # Documento suelto (PDF)
    python process_resources.py add paper.pdf --type documento --title "Paper X"

    # Rellenar un recurso pendiente del catálogo (ej: Rotación UCI)
    python process_resources.py fill res_uci_g05 clase.pdf --audio p1.mp3 p2.mp3

    # Presentación sincronizada (diapositivas que avanzan con el audio)
    python process_resources.py pack res_uci_g24 --pdf G24.pdf --audio g24.mp3

    # Emparejar en lote una carpeta de PDFs con el catálogo (por código G)
    python process_resources.py import-folder ~/Desktop/presentaciones \
        --audio-dir ~/Desktop/audios

    # Listar recursos existentes (o solo los pendientes)
    python process_resources.py list [--pending]

    # Eliminar un recurso (borra la entrada del índice, no los archivos)
    python process_resources.py remove res_guia_epoc
"""

import argparse
import json
import re
import shutil
import subprocess
import sys
import unicodedata
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
INDEX_FILE = BASE_DIR / "data" / "resources_index.json"
RESOURCES_DIR = BASE_DIR / "resources"

TYPE_DIRS = {
    "guia": RESOURCES_DIR / "guias",
    "presentacion": RESOURCES_DIR / "presentaciones",
    "documento": RESOURCES_DIR / "documentos",
}
AUDIO_DIR = RESOURCES_DIR / "audio"

AUDIO_EXTS = {".mp3", ".m4a", ".wav", ".ogg", ".aac", ".opus"}


def slugify(text: str) -> str:
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^a-zA-Z0-9]+", "_", text).strip("_").lower()
    return text[:60] or "recurso"


def load_index() -> list:
    if INDEX_FILE.exists():
        with open(INDEX_FILE, encoding="utf-8") as f:
            return json.load(f)
    return []


def save_index(index: list):
    INDEX_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)
        f.write("\n")


def unique_id(index: list, base: str) -> str:
    existing = {r["id"] for r in index}
    rid = f"res_{base}"
    n = 2
    while rid in existing:
        rid = f"res_{base}_{n}"
        n += 1
    return rid


def copy_into(src: Path, dest_dir: Path) -> Path:
    """Copia src a dest_dir evitando sobrescribir; retorna la ruta destino."""
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / src.name
    n = 2
    while dest.exists() and dest.stat().st_size != src.stat().st_size:
        dest = dest_dir / f"{src.stem}_{n}{src.suffix}"
        n += 1
    if not dest.exists():
        shutil.copy2(src, dest)
    return dest


def guess_type(filepath: Path) -> str:
    if filepath.suffix.lower() in (".md", ".markdown", ".txt"):
        return "guia"
    return "documento"


def build_files(src: Path, rtype: str, audio: list) -> dict:
    """Copia el archivo principal y las pistas de audio; retorna el dict `files`."""
    files = {}
    is_markdown = src.suffix.lower() in (".md", ".markdown", ".txt")
    dest = copy_into(src, TYPE_DIRS[rtype])
    rel = dest.relative_to(BASE_DIR).as_posix()
    if is_markdown:
        files["content"] = rel
    else:
        files["pdf"] = rel  # PDF u otro archivo incrustable

    audio_entries = []
    for i, a in enumerate(audio or [], 1):
        apath = Path(a).expanduser()
        if not apath.exists():
            sys.exit(f"❌ Audio no encontrado: {apath}")
        if apath.suffix.lower() not in AUDIO_EXTS:
            print(f"⚠️  {apath.name}: extensión poco común para audio, se incluye igual")
        adest = copy_into(apath, AUDIO_DIR)
        audio_entries.append({
            "title": f"Parte {i}",
            "src": adest.relative_to(BASE_DIR).as_posix(),
        })
    if audio_entries:
        files["audio"] = audio_entries
    return files


def cmd_add(args):
    src = Path(args.file).expanduser()
    if not src.exists():
        sys.exit(f"❌ Archivo no encontrado: {src}")

    rtype = args.type or guess_type(src)
    if rtype not in TYPE_DIRS:
        sys.exit(f"❌ Tipo inválido: {rtype}. Usa: {', '.join(TYPE_DIRS)}")

    title = args.title or src.stem.replace("_", " ").replace("-", " ").strip()
    index = load_index()
    rid = unique_id(index, slugify(args.id or title))

    files = build_files(src, rtype, args.audio)

    entry = {
        "id": rid,
        "type": rtype,
        "title": title,
        "specialty": args.specialty,
        "description": args.description or "",
        "author": args.author,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "tags": args.tags or [],
        "access": args.access,
        "files": files,
        "related_maps": args.related or [],
    }
    index.append(entry)
    save_index(index)

    print(f"\n✅ Recurso agregado: {rid}")
    print(f"   Título: {title}")
    print(f"   Tipo: {rtype} · Especialidad: {args.specialty}")
    for k, v in files.items():
        if k == "audio":
            for a in v:
                print(f"   Audio: {a['src']}")
        else:
            print(f"   {k}: {v}")
    print(f"\n   URL: recurso.html?id={rid}")
    print("   Recuerda hacer commit + push para publicarlo.")


def cmd_fill(args):
    """Rellena un recurso pendiente (del catálogo) con sus archivos reales."""
    src = Path(args.file).expanduser()
    if not src.exists():
        sys.exit(f"❌ Archivo no encontrado: {src}")

    index = load_index()
    entry = next((r for r in index if r["id"] == args.id), None)
    if entry is None:
        sys.exit(f"❌ No existe el recurso: {args.id}  (usa 'list' para ver los ids)")

    rtype = entry.get("type", guess_type(src))
    if rtype not in TYPE_DIRS:
        rtype = guess_type(src)
    entry["files"] = build_files(src, rtype, args.audio)
    entry.pop("pending", None)
    if args.description:
        entry["description"] = args.description
    elif entry.get("description", "").endswith("Pendiente de subir los archivos."):
        entry["description"] = entry["description"].replace(
            " Pendiente de subir los archivos.", "").strip()
    entry["date"] = datetime.now().strftime("%Y-%m-%d")
    save_index(index)

    print(f"\n✅ Recurso completado: {entry['id']}")
    print(f"   Título: {entry['title']}")
    for k, v in entry["files"].items():
        if k == "audio":
            for a in v:
                print(f"   Audio: {a['src']}")
        else:
            print(f"   {k}: {v}")
    print(f"\n   URL: recurso.html?id={entry['id']}")
    print("   Recuerda hacer commit + push para publicarlo.")


SLIDES_DIR = RESOURCES_DIR / "presentaciones"
IMG_EXTS = {".png", ".jpg", ".jpeg", ".webp"}


def parse_timestamp(s: str) -> float:
    """'1:23' -> 83.0 ; '1:02:03' -> 3723.0 ; '42' -> 42.0"""
    s = s.strip()
    if not s:
        return 0.0
    parts = s.split(":")
    try:
        parts = [float(p) for p in parts]
    except ValueError:
        return 0.0
    sec = 0.0
    for p in parts:
        sec = sec * 60 + p
    return sec


def audio_duration(path: Path):
    """Duración en segundos vía ffprobe; None si no está disponible."""
    try:
        out = subprocess.run(
            ["ffprobe", "-v", "quiet", "-show_entries", "format=duration",
             "-of", "default=nk=1:nw=1", str(path)],
            capture_output=True, text=True, timeout=30)
        return float(out.stdout.strip())
    except Exception:
        return None


def render_pdf_to_pngs(pdf: Path, out_dir: Path, dpi: int = 130):
    """Renderiza cada página del PDF a PNG. Prefiere PyMuPDF; cae a pdftoppm."""
    out_dir.mkdir(parents=True, exist_ok=True)
    # 1) PyMuPDF
    try:
        import fitz  # type: ignore
        doc = fitz.open(str(pdf))
        pngs = []
        for i, page in enumerate(doc, 1):
            pix = page.get_pixmap(dpi=dpi)
            dest = out_dir / f"slide-{i:03d}.png"
            pix.save(str(dest))
            pngs.append(dest)
        doc.close()
        return pngs
    except ImportError:
        pass
    # 2) pdftoppm (poppler)
    if shutil.which("pdftoppm"):
        prefix = out_dir / "slide"
        subprocess.run(["pdftoppm", "-png", "-r", str(dpi), str(pdf), str(prefix)],
                       check=True)
        pngs = sorted(out_dir.glob("slide-*.png")) or sorted(out_dir.glob("slide*.png"))
        # normalizar a slide-001.png
        norm = []
        for i, p in enumerate(sorted(pngs), 1):
            dest = out_dir / f"slide-{i:03d}.png"
            if p != dest:
                p.rename(dest)
            norm.append(dest)
        return norm
    sys.exit("❌ No hay renderizador de PDF. Instala PyMuPDF (`pip install pymupdf`) "
             "o poppler (`brew install poppler`), o pasa --slides-dir con los PNG ya exportados.")


GCODE_RE = re.compile(r'[Gg]\s*0*(\d{1,2})\s*[-_ ]?\s*([ABab])?')


def parse_gcode(name: str):
    """Extrae (num, letra) de un nombre de archivo o id. Ej: 'G06a' -> (6, 'a')."""
    m = GCODE_RE.search(name)
    if not m:
        return None
    return (int(m.group(1)), (m.group(2) or "").lower())


def cmd_pack(args):
    """Empaqueta una presentación sincronizada: slides PNG + audio + cues de tiempo."""
    index = load_index()
    entry = next((r for r in index if r["id"] == args.id), None)
    creating = entry is None

    # 1) Obtener las diapositivas como PNG
    slug = slugify(args.id.replace("res_uci_", "").replace("res_", "") or (entry and entry["title"]) or "deck")
    out_dir = SLIDES_DIR / slug
    if args.slides_dir:
        sdir = Path(args.slides_dir).expanduser()
        if not sdir.is_dir():
            sys.exit(f"❌ No es una carpeta de slides: {sdir}")
        srcs = sorted(p for p in sdir.iterdir() if p.suffix.lower() in IMG_EXTS)
        if not srcs:
            sys.exit(f"❌ No hay imágenes en {sdir}")
        out_dir.mkdir(parents=True, exist_ok=True)
        slide_paths = []
        for i, p in enumerate(srcs, 1):
            dest = out_dir / f"slide-{i:03d}{p.suffix.lower()}"
            shutil.copy2(p, dest)
            slide_paths.append(dest)
    elif args.pdf:
        pdf = Path(args.pdf).expanduser()
        if not pdf.exists():
            sys.exit(f"❌ PDF no encontrado: {pdf}")
        print(f"🖼️  Renderizando {pdf.name} a PNG (dpi={args.dpi})…")
        slide_paths = render_pdf_to_pngs(pdf, out_dir, dpi=args.dpi)
    else:
        sys.exit("❌ Indica --pdf archivo.pdf  o  --slides-dir carpeta_con_pngs")

    n = len(slide_paths)
    print(f"   {n} diapositivas.")

    # 2) Audio
    apath = Path(args.audio).expanduser()
    if not apath.exists():
        sys.exit(f"❌ Audio no encontrado: {apath}")
    adest = copy_into(apath, AUDIO_DIR)
    audio_rel = adest.relative_to(BASE_DIR).as_posix()

    # 3) Cues de tiempo
    approx = False
    if args.cues:
        cfile = Path(args.cues).expanduser()
        if not cfile.exists():
            sys.exit(f"❌ Archivo de cues no encontrado: {cfile}")
        cues = [parse_timestamp(l) for l in cfile.read_text(encoding="utf-8").splitlines() if l.strip()]
        if len(cues) < n:
            print(f"⚠️  {len(cues)} cues para {n} slides; el resto se estima proporcionalmente.")
            approx = True
    else:
        cues = []

    if len(cues) < n:
        dur = args.duration or audio_duration(adest)
        if dur:
            if not cues:
                # spread proporcional uniforme: slide i empieza en dur*i/n
                cues = [dur * i / n for i in range(n)]
            else:
                # completar los que faltan tras el último cue explícito
                base = cues[-1]
                remaining = n - len(cues)
                span = max(0.0, dur - base)
                for i in range(1, remaining + 1):
                    cues.append(base + span * i / (remaining + 1))
            approx = approx or not args.cues
        else:
            print("⚠️  Sin duración de audio (instala ffmpeg o pasa --duration SEG). "
                  "Los cues quedan en 0; la diapositiva no avanzará sola.")
            cues = (cues + [0.0] * n)[:n]

    slides_manifest = [
        {"img": p.relative_to(BASE_DIR).as_posix(), "start": round(cues[i], 2)}
        for i, p in enumerate(slide_paths)
    ]

    files = {
        "audio": [{"title": "Narración", "src": audio_rel}],
        "slides": slides_manifest,
    }
    if args.pdf:
        pdf_dest = copy_into(Path(args.pdf).expanduser(), TYPE_DIRS["presentacion"])
        files["pdf"] = pdf_dest.relative_to(BASE_DIR).as_posix()

    if creating:
        entry = {
            "id": args.id,
            "type": "presentacion",
            "title": args.title or args.id,
            "specialty": args.specialty,
            "description": args.description or "",
            "author": args.author,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "tags": args.tags or [],
            "access": "free",
            "files": files,
            "related_maps": [],
        }
        index.append(entry)
    else:
        entry["files"] = files
        entry.pop("pending", None)
        if args.title:
            entry["title"] = args.title
        desc = entry.get("description", "")
        if desc.endswith("Pendiente de subir los archivos."):
            entry["description"] = desc.replace(" Pendiente de subir los archivos.", "").strip()
        entry["date"] = datetime.now().strftime("%Y-%m-%d")
    if approx:
        entry["sync_approx"] = True
    else:
        entry.pop("sync_approx", None)

    save_index(index)
    print(f"\n✅ Presentación sincronizada lista: {entry['id']}")
    print(f"   {n} slides · audio {audio_rel}{' · ≈ sincronía aproximada' if approx else ''}")
    print(f"   URL: recurso.html?id={entry['id']}")
    print("   Recuerda hacer commit + push para publicarla.")


def cmd_import_folder(args):
    """Empareja PDFs (y audios) de una carpeta con los recursos del catálogo por código G."""
    pdf_dir = Path(args.dir).expanduser()
    if not pdf_dir.is_dir():
        sys.exit(f"❌ No es una carpeta: {pdf_dir}")
    audio_dir = Path(args.audio_dir).expanduser() if args.audio_dir else None
    if audio_dir and not audio_dir.is_dir():
        sys.exit(f"❌ No es una carpeta de audio: {audio_dir}")

    index = load_index()
    # Mapa (num, letra) -> entrada del catálogo (solo recursos res_uci_*)
    catalog = {}
    for r in index:
        if not r["id"].startswith("res_uci_"):
            continue
        gc = parse_gcode(r["id"].replace("res_uci_", ""))
        if gc:
            catalog[gc] = r

    # Indexar audios disponibles por código G
    audio_by_gc = {}
    if audio_dir:
        for a in sorted(audio_dir.iterdir()):
            if a.is_file() and a.suffix.lower() in AUDIO_EXTS:
                gc = parse_gcode(a.name)
                if gc:
                    audio_by_gc.setdefault(gc, []).append(a)

    pdfs = sorted(p for p in pdf_dir.iterdir() if p.is_file() and p.suffix.lower() == ".pdf")
    if not pdfs:
        sys.exit(f"📭 No hay PDFs en {pdf_dir}")

    filled, skipped, unmatched = [], [], []
    for pdf in pdfs:
        gc = parse_gcode(pdf.name)
        if gc is None or gc not in catalog:
            unmatched.append(pdf.name)
            continue
        entry = catalog[gc]
        if entry.get("files") and not args.force:
            skipped.append((entry["id"], pdf.name))
            continue
        audios = audio_by_gc.get(gc, [])
        if args.dry_run:
            filled.append((entry["id"], pdf.name, [a.name for a in audios]))
            continue
        entry["files"] = build_files(pdf, "presentacion", [str(a) for a in audios])
        entry.pop("pending", None)
        desc = entry.get("description", "")
        if desc.endswith("Pendiente de subir los archivos."):
            entry["description"] = desc.replace(" Pendiente de subir los archivos.", "").strip()
        entry["date"] = datetime.now().strftime("%Y-%m-%d")
        filled.append((entry["id"], pdf.name, [a.name for a in audios]))

    if not args.dry_run and filled:
        save_index(index)

    tag = "[dry-run] " if args.dry_run else ""
    print(f"\n{tag}✅ {len(filled)} presentación(es) {'se rellenarían' if args.dry_run else 'rellenadas'}:")
    for rid, pdf, auds in filled:
        extra = f"  +{len(auds)} audio(s)" if auds else "  (sin audio)"
        print(f"   {rid}  ←  {pdf}{extra}")
    if skipped:
        print(f"\n⏭️  {len(skipped)} ya tenían archivos (usa --force para sobrescribir):")
        for rid, pdf in skipped:
            print(f"   {rid}  (venía con: {pdf})")
    if unmatched:
        print(f"\n⚠️  {len(unmatched)} PDF(s) sin código G reconocible — rellénalos a mano con 'fill':")
        for name in unmatched:
            print(f"   {name}")
    still = [r["id"] for r in index if r["id"].startswith("res_uci_") and (r.get("pending") or not r.get("files"))]
    if still and not args.dry_run:
        print(f"\n📌 Quedan {len(still)} presentaciones del catálogo aún pendientes.")
    if not args.dry_run and filled:
        print("\n   Recuerda: git add -A && git commit -m 'presentaciones UCI' && git push")


def cmd_list(args):
    index = load_index()
    if not index:
        print("📭 No hay recursos todavía.")
        return
    if getattr(args, "pending", False):
        index = [r for r in index if r.get("pending") or not r.get("files")]
    print(f"\n📚 {len(index)} recursos{' pendientes' if getattr(args, 'pending', False) else ''}:\n")
    for r in index:
        icon = {"guia": "📖", "presentacion": "🎧", "documento": "📄"}.get(r["type"], "📄")
        audio = r.get("files", {}).get("audio", [])
        pending = r.get("pending") or not r.get("files")
        extra = " · ⏳ pendiente" if pending else (f" · {len(audio)} pista(s) de audio" if audio else "")
        print(f"  {icon} [{r['id']}] {r['title']} — {r.get('specialty', 'General')}{extra}")


def cmd_remove(args):
    index = load_index()
    before = len(index)
    index = [r for r in index if r["id"] != args.id]
    if len(index) == before:
        sys.exit(f"❌ No existe el recurso: {args.id}")
    save_index(index)
    print(f"✅ Recurso {args.id} eliminado del índice (los archivos quedan en resources/).")


def main():
    parser = argparse.ArgumentParser(description="Procesar recursos de estudio de MedMaps")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_add = sub.add_parser("add", help="Agregar un recurso")
    p_add.add_argument("file", help="Archivo principal (.md/.txt para guías, .pdf para presentaciones/documentos)")
    p_add.add_argument("--type", "-t", choices=list(TYPE_DIRS), help="guia | presentacion | documento (se infiere si se omite)")
    p_add.add_argument("--title", help="Título del recurso (por defecto, el nombre del archivo)")
    p_add.add_argument("--specialty", "-s", default="General")
    p_add.add_argument("--description", "-d", default="")
    p_add.add_argument("--author", default="Dr. Acevedo")
    p_add.add_argument("--audio", nargs="+", help="Archivos de audio (en orden) para presentaciones")
    p_add.add_argument("--tags", nargs="+", help="Etiquetas")
    p_add.add_argument("--related", nargs="+", help="IDs de mapas relacionados (ej: map_12 fa)")
    p_add.add_argument("--access", "-a", default="free", choices=["free", "premium"])
    p_add.add_argument("--id", help="Forzar un id específico (se slugifica)")
    p_add.set_defaults(func=cmd_add)

    p_fill = sub.add_parser("fill", help="Rellenar un recurso pendiente del catálogo con sus archivos")
    p_fill.add_argument("id", help="ID del recurso pendiente (ej: res_uci_g05)")
    p_fill.add_argument("file", help="Archivo principal (.pdf para presentaciones, .md para guías)")
    p_fill.add_argument("--audio", nargs="+", help="Archivos de audio (en orden)")
    p_fill.add_argument("--description", "-d", default="", help="Descripción (opcional; reemplaza la del catálogo)")
    p_fill.set_defaults(func=cmd_fill)

    p_pack = sub.add_parser("pack",
                            help="Empaquetar una presentación sincronizada (slides PNG + audio + cues)")
    p_pack.add_argument("id", help="ID del recurso (existente del catálogo, ej: res_uci_g24, o uno nuevo)")
    p_pack.add_argument("--pdf", help="PDF del deck (se renderiza a PNG)")
    p_pack.add_argument("--slides-dir", help="Carpeta con los PNG ya exportados (alternativa a --pdf)")
    p_pack.add_argument("--audio", required=True, help="Archivo de audio de la narración")
    p_pack.add_argument("--cues", help="Archivo de texto con un tiempo por línea (mm:ss) por diapositiva")
    p_pack.add_argument("--duration", type=float, help="Duración del audio en segundos (si no hay ffmpeg)")
    p_pack.add_argument("--dpi", type=int, default=130, help="Resolución del render PDF→PNG (def. 130)")
    p_pack.add_argument("--title", help="Título (para recursos nuevos)")
    p_pack.add_argument("--specialty", "-s", default="Medicina Intensiva")
    p_pack.add_argument("--description", "-d", default="")
    p_pack.add_argument("--author", default="Dr. Acevedo")
    p_pack.add_argument("--tags", nargs="+")
    p_pack.set_defaults(func=cmd_pack)

    p_imp = sub.add_parser("import-folder",
                           help="Emparejar PDFs de una carpeta con el catálogo por código G (G05, G24…)")
    p_imp.add_argument("dir", help="Carpeta con los PDFs (ej: ~/Desktop/presentaciones)")
    p_imp.add_argument("--audio-dir", help="Carpeta con los audios (se emparejan por código G)")
    p_imp.add_argument("--dry-run", action="store_true", help="Mostrar qué se rellenaría sin escribir nada")
    p_imp.add_argument("--force", action="store_true", help="Sobrescribir recursos que ya tienen archivos")
    p_imp.set_defaults(func=cmd_import_folder)

    p_list = sub.add_parser("list", help="Listar recursos")
    p_list.add_argument("--pending", "-p", action="store_true", help="Solo los pendientes de subir")
    p_list.set_defaults(func=cmd_list)

    p_rm = sub.add_parser("remove", help="Quitar un recurso del índice")
    p_rm.add_argument("id", help="ID del recurso (ej: res_guia_epoc)")
    p_rm.set_defaults(func=cmd_remove)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
