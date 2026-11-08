#!/usr/bin/env python3
"""
extract_pptx.py — Extrahiert Text und Original-Bilder aus einer .pptx-Datei.

PPTX ist ein ZIP-Container. Bilder werden 1:1 aus dem Media-Ordner kopiert
(kein Rendering/Screenshot), Text wird pro Folie samt grober Layout-Rolle
(Titel vs. Fließtext) und Sprechernotizen extrahiert.

Verwendung:
    python extract_pptx.py input.pptx --out-dir ./extrahiert

Erzeugt:
    ./extrahiert/assets/img_01.png, img_02.jpg, ...
    ./extrahiert/inhalt.json   (strukturierte Beschreibung, siehe unten)

JSON-Struktur:
[
  {
    "folie": 1,
    "titel": "...",
    "textbloecke": ["...", "..."],
    "notizen": "...",
    "bilder": ["img_01.png", ...]
  },
  ...
]
"""

import argparse
import json
import sys
from pathlib import Path

from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE


def extrahiere(pptx_pfad: Path, out_dir: Path) -> list[dict]:
    assets_dir = out_dir / "assets"
    assets_dir.mkdir(parents=True, exist_ok=True)

    prs = Presentation(str(pptx_pfad))
    ergebnis = []
    bild_zaehler = 0

    for i, slide in enumerate(prs.slides, start=1):
        titel = None
        textbloecke = []
        bilder = []

        for shape in slide.shapes:
            if shape.shape_type == MSO_SHAPE_TYPE.PICTURE:
                bild_zaehler += 1
                image = shape.image
                ext = image.ext  # z.B. 'png', 'jpeg'
                dateiname = f"img_{bild_zaehler:02d}.{ext}"
                (assets_dir / dateiname).write_bytes(image.blob)
                bilder.append(dateiname)
                continue

            if not shape.has_text_frame:
                continue
            text = shape.text_frame.text.strip()
            if not text:
                continue

            ist_titel = (
                shape == slide.shapes.title
                if slide.shapes.title is not None
                else False
            )
            if ist_titel and titel is None:
                titel = text
            else:
                textbloecke.append(text)

        notizen = ""
        if slide.has_notes_slide and slide.notes_slide.notes_text_frame:
            notizen = slide.notes_slide.notes_text_frame.text.strip()

        ergebnis.append({
            "folie": i,
            "titel": titel,
            "textbloecke": textbloecke,
            "notizen": notizen,
            "bilder": bilder,
        })

    return ergebnis


def main():
    p = argparse.ArgumentParser(description="Text + Bilder aus PPTX extrahieren.")
    p.add_argument("pptx_datei")
    p.add_argument("--out-dir", required=True)
    args = p.parse_args()

    pptx_pfad = Path(args.pptx_datei)
    out_dir = Path(args.out_dir)
    if not pptx_pfad.exists():
        sys.exit(f"Datei nicht gefunden: {pptx_pfad}")

    daten = extrahiere(pptx_pfad, out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "inhalt.json").write_text(
        json.dumps(daten, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    n_bilder = sum(len(f["bilder"]) for f in daten)
    print(f"{len(daten)} Folien, {n_bilder} Bilder extrahiert -> {out_dir}")


if __name__ == "__main__":
    main()
