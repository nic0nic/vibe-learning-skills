#!/usr/bin/env python3
"""
bild_bearbeiten.py — Zuschneiden und/oder Skalieren eines einzelnen Bildes.

Nützlich, wenn ein extrahiertes Bild unnötige Ränder hat oder zu groß für
die Folie ist. Überschreibt NICHT das Original, sondern schreibt eine neue
Datei (Standard: gleicher Name mit "_bearbeitet"-Suffix).

Verwendung:
    # Zuschneiden: linke, obere, rechte, untere Kante in Pixeln
    python bild_bearbeiten.py assets/img_03.png --crop 20 20 780 580

    # Auf Breite skalieren (Höhe proportional)
    python bild_bearbeiten.py assets/img_03.png --width 800

    # Beides kombiniert, mit eigenem Ausgabenamen
    python bild_bearbeiten.py assets/img_03.png --crop 20 20 780 580 --width 600 --out assets/img_03_klein.png
"""

import argparse
from pathlib import Path

from PIL import Image


def main():
    p = argparse.ArgumentParser(description="Bild zuschneiden/skalieren.")
    p.add_argument("bild")
    p.add_argument("--crop", nargs=4, type=int, metavar=("LINKS", "OBEN", "RECHTS", "UNTEN"),
                    help="Zuschneiden auf Pixel-Koordinaten (links, oben, rechts, unten)")
    p.add_argument("--width", type=int, help="Auf diese Breite skalieren (Höhe proportional)")
    p.add_argument("--out", help="Ausgabepfad (Default: <name>_bearbeitet.<ext>)")
    args = p.parse_args()

    pfad = Path(args.bild)
    img = Image.open(pfad)

    if args.crop:
        img = img.crop(tuple(args.crop))

    if args.width:
        verhaeltnis = args.width / img.width
        neue_hoehe = round(img.height * verhaeltnis)
        img = img.resize((args.width, neue_hoehe), Image.LANCZOS)

    ziel = Path(args.out) if args.out else pfad.with_stem(pfad.stem + "_bearbeitet")
    img.save(ziel)
    print(f"Gespeichert: {ziel} ({img.width}x{img.height})")


if __name__ == "__main__":
    main()
