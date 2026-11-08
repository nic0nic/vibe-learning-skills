---
name: praesentation-zu-mkslides
description: Konvertiert eine bestehende Präsentation (.pdf oder .pptx) in eine mkslides-kompatible slides.md samt Original-Bildern als assets/. Erkennt dabei inhaltlich Arbeitsaufträge (Aufgabenstellungen an Schüler) und verpackt sie in die passende styled div-Box, und erkennt Gruppenarbeits-Aufträge, um automatisch eine GRUPPEN-Direktive für die Zufallsgruppen-Zuordnung einzufügen. IMMER verwenden, wenn eine .pdf- oder .pptx-Datei hochgeladen wird und der Nutzer sie "zu Folien machen", "in mkslides umwandeln", "als slides.md" haben möchte, oder generell eine bestehende Präsentation/ein Foliensatz in dieses Markdown-Format überführt werden soll — auch wenn "mkslides" nicht explizit erwähnt wird, aber der Kontext (Lehrkraft, Unterrichtsstunde, Foliensatz) erkennbar ist.
---

# Präsentation zu mkslides konvertieren

Wandelt eine PDF- oder PPTX-Datei in eine `slides.md` (mkslides/reveal.js-
Format) samt zugehörigem `assets/`-Ordner mit den Original-Bildern um.
Ergebnis wird am Ende als ZIP bereitgestellt (fertig entpackbar neben
`build_stunde.py`).

## Ablauf

### 1. Format erkennen und Bilder + Text extrahieren

Je nach Dateityp eines der Extraktionsskripte aufrufen (liegen unter
`scripts/` relativ zu diesem SKILL.md):

```bash
python scripts/extract_pptx.py "<pfad-zur-datei>.pptx" --out-dir /tmp/extrahiert
# oder
python scripts/extract_pdf.py "<pfad-zur-datei>.pdf" --out-dir /tmp/extrahiert
```

Das erzeugt `/tmp/extrahiert/assets/` (Original-Bilder, unverändert aus der
Quelldatei) und `/tmp/extrahiert/inhalt.json` (Text pro Folie/Seite + welche
Bilddateien dazugehören).

**Wichtig:** Die Bilder sind bereits die echten Originaldaten aus dem
Container (kein Screenshot/Rendering) — nicht erneut versuchen, Bilder aus
gerendeten Seiten zu exportieren.

### 2. `inhalt.json` lesen und inhaltlich strukturieren

`inhalt.json` mit `view` öffnen und für jede Folie/Seite entscheiden:

- **Ist das eine normale Inhaltsfolie?** -> Abschnitt 3 der Vorlage.
- **Enthält der Text eine Aufgabenstellung an Schüler** (Formulierungen wie
  "Lest...", "Notiert...", "Diskutiert...", "Findet euch in Gruppen...",
  Fragen die zum Bearbeiten auffordern)? -> Arbeitsauftrag-Box, Abschnitt 4
  der Vorlage.
- **Ist die Aufgabenstellung erkennbar Gruppenarbeit** (mehrere Themen
  parallel, "in eurer Gruppe", "jede Gruppe bearbeitet...")? -> zusätzlich
  GRUPPEN-Direktive, Abschnitt 5 der Vorlage.

Bei Unsicherheit lieber als normale Inhaltsfolie behandeln und den Nutzer
am Ende kurz auf die Unsicherheit hinweisen, statt zu raten.

**Vor dem Schreiben der `slides.md` immer `references/vorlage.md` lesen** —
dort stehen die exakten Formatvorlagen (Frontmatter, CSS-Block, Folientrenner,
Arbeitsauftrag-Syntax, GRUPPEN-Direktiven-Syntax inkl. Regeln für
`klasse`/`gruppen`/`namen`/`seed`).

### 3. Bilder bei Bedarf zuschneiden/skalieren

Falls ein extrahiertes Bild unnötige Ränder hat, zu groß ist, oder aus
optischen Gründen angepasst werden sollte:

```bash
python scripts/bild_bearbeiten.py /tmp/extrahiert/assets/img_03.png --crop 20 20 780 580 --width 800
```

Schreibt eine neue Datei (Standard-Suffix `_bearbeitet`), Original bleibt
erhalten. Bei Unsicherheit über Zuschnitt-Koordinaten: Bild zuerst mit `view`
ansehen, um die Pixelgrenzen abzuschätzen.

### 4. `slides.md` schreiben

Neue Datei in einem Arbeitsordner erstellen, z.B.:

```
/tmp/ausgabe/<name-der-stunde>/slides.md
/tmp/ausgabe/<name-der-stunde>/assets/...
```

Bilder aus `/tmp/extrahiert/assets/` (bzw. die bearbeiteten Varianten) in
diesen `assets/`-Ordner kopieren. Nur die Bilder übernehmen, die tatsächlich
in der `slides.md` referenziert werden (keine unbenutzten Dateien mitschleppen).

Inhalt gemäß `references/vorlage.md` aufbauen — Frontmatter + CSS-Block einmal
zu Beginn, dann Folie für Folie mit `---` getrennt.

### 5. Ergebnis als ZIP bereitstellen

```bash
cd /tmp/ausgabe && zip -r <name-der-stunde>.zip <name-der-stunde>/
```

ZIP mit `present_files` bereitstellen. Der Ordner im ZIP ist so aufgebaut,
dass er direkt als `quellordner` für `build_stunde.py build ...`
funktioniert (`slides.md` + `assets/` auf gleicher Ebene).

## Am Ende immer erwähnen

- Wie viele Folien/Arbeitsaufträge erkannt wurden, und ob irgendwo
  Unsicherheit bestand (z.B. "Folie 7 sah wie ein Arbeitsauftrag aus, war mir
  aber nicht sicher genug").
- Dass bei jeder GRUPPEN-Direktive `klasse` noch manuell gesetzt werden muss
  (Platzhalter `"KLASSE_ANPASSEN"`) und `seed`/`gruppen`/`namen` bei Bedarf
  angepasst werden können.
- Dass Bildzuschnitte (falls gemacht) stichprobenartig geprüft werden sollten.
