#!/usr/bin/env python3
"""
extract_pdf.py — Extrahiert Text und Original-Bilder aus einer .pdf-Datei
(z.B. eine als PDF exportierte Folienpräsentation).

Bilder werden als eingebettete Original-Objekte gezogen (keine Screenshots/
Rendering der Seite), Text pro Seite als Rohtext (Reihenfolge kann bei
komplexen Layouts abweichen -> Claude ordnet das beim Erstellen der .md
inhaltlich sinnvoll ein).

Verwendung:
    python extract_pdf.py input.pdf --out-dir ./extrahiert

Erzeugt:
    ./extrahiert/assets/img_01.png, ...
    ./extrahiert/inhalt.json

JSON-Struktur:
[
  {"seite": 1, "text": "...", "bilder": ["img_01.png", ...]},
  ...
]
"""

import argparse
import json
import sys
from pathlib import Path

import fitz  # PyMuPDF


def extrahiere(pdf_pfad: Path, out_dir: Path) -> list[dict]:
    assets_dir = out_dir / "assets"
    assets_dir.mkdir(parents=True, exist_ok=True)

    doc = fitz.open(str(pdf_pfad))
    ergebnis = []
    bild_zaehler = 0

    for seiten_index in range(len(doc)):
        seite = doc[seiten_index]
        text = seite.get_text("text").strip()

        bilder = []
        for img in seite.get_images(full=True):
            xref = img[0]
            try:
                base = doc.extract_image(xref)
            except Exception:
                continue
            bild_zaehler += 1
            ext = base["ext"]
            dateiname = f"img_{bild_zaehler:02d}.{ext}"
            (assets_dir / dateiname).write_bytes(base["image"])
            bilder.append(dateiname)

        ergebnis.append({
            "seite": seiten_index + 1,
            "text": text,
            "bilder": bilder,
        })

    doc.close()
    return ergebnis


def main():
    p = argparse.ArgumentParser(description="Text + Bilder aus PDF extrahieren.")
    p.add_argument("pdf_datei")
    p.add_argument("--out-dir", required=True)
    args = p.parse_args()

    pdf_pfad = Path(args.pdf_datei)
    out_dir = Path(args.out_dir)
    if not pdf_pfad.exists():
        sys.exit(f"Datei nicht gefunden: {pdf_pfad}")

    daten = extrahiere(pdf_pfad, out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "inhalt.json").write_text(
        json.dumps(daten, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    n_bilder = sum(len(s["bilder"]) for s in daten)
    print(f"{len(daten)} Seiten, {n_bilder} Bilder extrahiert -> {out_dir}")


if __name__ == "__main__":
    main()
