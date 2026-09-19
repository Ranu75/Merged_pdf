#!/usr/bin/env python3
"""
merge_pdfs.py
Fusionne plusieurs fichiers PDF en un seul fichier de sortie et vérifie
que le résultat contient exactement 12 pages.
Usage:
  python merge_pdfs.py --output resultat.pdf file1.pdf file2.pdf ...
  python merge_pdfs.py --dir ./mes_pdfs --output resultat.pdf
"""
import argparse
import glob
import os
import re
import sys
from pypdf import PdfReader, PdfWriter


def natural_key(s):
    # clé de tri « naturelle » : sépare chiffres et texte
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r"(\d+)", s)]


def collect_files_from_dir(directory):
    pats = glob.glob(os.path.join(directory, "*.pdf"))
    pats_sorted = sorted(pats, key=lambda p: natural_key(os.path.basename(p)))
    return pats_sorted


def merge_pdfs(file_paths, output_path):
    writer = PdfWriter()
    total_pages = 0
    for p in file_paths:
        try:
            reader = PdfReader(p)
        except Exception as e:
            print(f"Erreur en ouvrant '{p}': {e}", file=sys.stderr)
            return None
        for pg in reader.pages:
            writer.add_page(pg)
        total_pages += len(reader.pages)
    try:
        with open(output_path, "wb") as f_out:
            writer.write(f_out)
    except Exception as e:
        print(f"Erreur en écrivant '{output_path}': {e}", file=sys.stderr)
        return None
    return total_pages


def main():
    parser = argparse.ArgumentParser(description="Fusionne PDFs et vérifie 12 pages.")
    parser.add_argument("--dir", help="Dossier contenant les PDFs à fusionner (ordre naturel).")
    parser.add_argument("--output", "-o", default="merged.pdf", help="Fichier PDF de sortie.")
    parser.add_argument("files", nargs="*", help="Fichiers PDF à fusionner (si fournis, ignorent --dir).")
    args = parser.parse_args()

    if args.files:
        inputs = args.files
    elif args.dir:
        inputs = collect_files_from_dir(args.dir)
    else:
        print("Erreur: fournissez des fichiers ou utilisez --dir", file=sys.stderr)
        sys.exit(2)

    if not inputs:
        print("Aucun fichier PDF trouvé.", file=sys.stderr)
        sys.exit(3)

    print(f"Fusion de {len(inputs)} fichiers en '{args.output}'...")
    pages = merge_pdfs(inputs, args.output)
    if pages is None:
        print("La fusion a échoué.", file=sys.stderr)
        sys.exit(4)

    print(f"Fusion terminée. Pages totales: {pages}")
    if pages == 12:
        print("✅ Le PDF de sortie contient exactement 12 pages.")
        sys.exit(0)
    else:
        print("⚠️ Le PDF de sortie ne contient pas 12 pages.", file=sys.stderr)
        sys.exit(5)


if __name__ == "__main__":
    main()
