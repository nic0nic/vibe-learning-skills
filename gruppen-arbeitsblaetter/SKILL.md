---
name: "gruppen-arbeitsblaetter"
description: "Arbeitsblätter mit Gruppenvarianten als Markdown-Einzelseiten (1_, A_, i_, 001_ …) erstellen und per Skript so zusammenfügen, dass Austeilen automatisch ausgeglichene, wechselnde Gruppen ergibt."
---

# Gruppen-Arbeitsblätter (automatische Gruppeneinteilung)

Jeder Schüler bekommt ein Blatt mit mehreren Seiten. Jede Seite gehört zu einer anderen Gruppierung (z. B. Vorderseite Gruppe 1–6, Rückseite Gruppe A–C). Die Lehrkraft druckt nur so viele Blätter, wie sie Schüler hat, und teilt den Stapel aus. Die Reihenfolge der Blätter sorgt bei jeder Schülerzahl für gleich große Gruppen (±1) und dafür, dass möglichst wenige Schüler in mehreren Phasen zusammensitzen.

## Ablauf

1. **Klären, nur falls nicht aus dem Chat ersichtlich:**
   - Wie viele Seiten (= Gruppierungen) hat ein Schülerblatt, und wie viele Gruppen gibt es je Seite?
   - Schülerzahl: Standard 35, das genügt für alle kleineren Klassen.
2. **Einzelseiten schreiben** in den Ordner `einzelseiten/`, eine `.md` pro Gruppe:
   - Seite 1: `1_<info>.md`, `2_<info>.md`, … (Zahlen)
   - Seite 2: `A_<info>.md`, `B_<info>.md`, … (Großbuchstaben)
   - Seite 3: `i_<info>.md`, `ii_<info>.md`, … (römisch, klein)
   - Seite 4: `001_<info>.md`, `010_<info>.md`, `011_<info>.md`, `100_<info>.md` (binär, mind. 3 Stellen)
   - `<info>` beschreibt den Inhalt, z. B. `3_entscheiden.md`.
   - Erst alle Einzelseiten zur Durchsicht zeigen und die Gesamtdatei erst bauen, wenn die Lehrkraft zustimmt.
3. **Skript ablegen:** den Inhalt aus dem Abschnitt „Skript“ unverändert als `gruppen_zusammenfuegen.py` neben den Ordner `einzelseiten/` speichern.
4. **Ausführen:** `python gruppen_zusammenfuegen.py` (Optionen siehe unten). Es entsteht `<ordnername>_gesamt_35.md` mit Typora-Seitenumbrüchen. Die Konsolenausgabe (Druckmodus, Gruppengrößen) an die Lehrkraft weitergeben.
5. **Export:** Die Lehrkraft exportiert die Gesamtdatei in Typora als PDF. Seitengröße in den Typora-Einstellungen: Export → PDF → **A5**. Nur falls im Chat gewünscht, erzeugt Claude das PDF selbst (siehe unten).

## Gestaltung der Einzelseiten (A5)

- **Aufbau:** Alle Varianten einer Seite haben denselben Aufbau und denselben Arbeitsauftrag, nur der Inhalt wechselt. Die Gruppe steht gut sichtbar oben rechts.
- **Umfang:** Eine Seite muss auf A5 passen, also etwa 150–250 Wörter Text plus Arbeitsauftrag und Schreibfeld. Lieber Platz lassen als überlaufen.
- **Hervorhebung:** Die Stellen, aus denen die Schüler die Lösung ableiten, im Text **fett** setzen.
- **Format:** Typora rendert Markdown in HTML-Blöcken nicht zuverlässig. Innerhalb von `<div>` deshalb reines HTML verwenden.
- **Druckfreundlich:** keine farbigen Flächen. Gruppenkennzeichen in Schwarz mit Rahmen, Arbeitsauftrag mit gelbem Strich links.

Vorlage:

```markdown
<div style="float:right;border:1.5px solid #000;padding:2px 12px;font-weight:bold;">Gruppe 2</div>

## Titel der Seite

<div style="border-left:5px solid #FFC000;padding:2px 0 2px 10px;margin:10px 0;">
<b>Arbeitsauftrag</b>
<ol style="margin:4px 0 0 0;">
<li>Lies den Text zu …</li>
<li>Notiere …</li>
</ol>
</div>

Fließtext mit **fett hervorgehobenen Schlüsselstellen** …

<div style="border:1px solid #000;padding:6px 10px;margin-top:12px;">
<b>Überschrift des Kastens</b>
<div style="border-bottom:1px solid #999;height:2em;"></div>
<div style="border-bottom:1px solid #999;height:2em;"></div>
<div style="border-bottom:1px solid #999;height:2em;"></div>
</div>
```

Name/Klasse/Datum nur auf Seite 1, z. B. als graue Zeile ganz oben.

## Druck (wählt das Skript automatisch nach Seitenzahl pro Schüler)

| Seiten pro Schüler | Druck | Drucken: erste … Seiten |
|---|---|---|
| 1 | A4, 2 Seiten pro Blatt, einseitig, in der Mitte schneiden | Schülerzahl (ungerade: +1) |
| 2 | A4, 2 Seiten pro Blatt, doppelseitig, **kurze Kante**, in der Mitte schneiden (Skript sortiert dafür um) | Schülerzahl × 2 (ungerade: +2) |
| 3–4 | A4, 2 Seiten pro Blatt, doppelseitig, 1 A4-Blatt pro Schüler (bei 3 Seiten bleibt eine Hälfte leer) | Schülerzahl × 4 |
| mit `--a5` | direkt auf A5, doppelseitig, keine Umsortierung | Schülerzahl × Seiten |

- **Druckerprobe:** Vor dem Druck die Lehrkraft auf einen Probedruck von 2 Blättern hinweisen. Passen bei 2 Seiten die Rückseiten nicht, mit `--lange-kante` neu erzeugen.

## Optionen

- `-n 28`: nur 28 Schülerblätter erzeugen (Standard 35)
- `--a5`: für A5-Papier, ohne Umsortierung
- `--lange-kante`: Umsortierung für Drucker, die an der langen Kante wenden
- `--nummer`: „Blatt k“ klein unter jede Seite setzen
- `-o name.md`: eigener Dateiname
- `--ordner`: anderer Unterordner als `einzelseiten`

## PDF im Chat erzeugen (nur auf Wunsch)

1. Skript mit `--a5` ausführen, sodass die Seiten nicht umsortiert werden.
2. Markdown → HTML (pandoc), dann HTML → PDF im Format A5 (z. B. headless Chromium oder weasyprint). Die Seitenumbruch-Divs werden dabei übernommen.
3. Für A4 die A5-Seiten selbst mit pypdf auf A4 quer setzen:
   - **2 Seiten pro Schüler:** Vorderseite = Vorderseite Schüler k | Schüler k+1. Rückseite = Rückseite Schüler k+1 | Schüler k. Gedruckt wird mit Wenden an der kurzen Kante.
   - **3–4 Seiten pro Schüler:** Die Seiten werden einfach nacheinander auf die A4-Blätter verteilt.
4. Das Ergebnis vor der Übergabe als Bild prüfen: Gruppenlabels, Seitenumbrüche und dass jede Seite auf A5 passt.

## Skript

```python
#!/usr/bin/env python3
"""
Fügt Gruppen-Arbeitsblätter (Markdown) zu einer druckfertigen Gesamtdatei zusammen.

Ordnerstruktur:
    <ordner>/gruppen_zusammenfuegen.py
    <ordner>/einzelseiten/1_ziele.md, 2_planen.md, ..., A_gesellschaft.md, B_..., i_..., 001_...

Präfix = Gruppe, jede Präfix-Art ist eine Seite des Schülerblatts:
    Seite 1: 1, 2, 3, ...          (Zahlen)
    Seite 2: A, B, C, ...          (Großbuchstaben)
    Seite 3: i, ii, iii, iv, ...   (römisch, klein)
    Seite 4: 001, 010, 011, 100... (binär, mind. 3 Stellen)

Die Reihenfolge der Schülerblätter ist so gewählt, dass für JEDE Schülerzahl
(die ersten N Blätter) alle Gruppen gleich groß sind (±1) und möglichst wenige
Schüler mehrfach zusammen in einer Gruppe landen.

Druckmodi (automatisch nach Seitenzahl pro Schüler):
    1 Seite : A4, 2 Seiten pro Blatt, einseitig, schneiden
    2 Seiten: A4, 2 Seiten pro Blatt, doppelseitig (kurze Kante), schneiden
              -> Seiten werden passend umsortiert
    3/4 Seiten: A4, 2 Seiten pro Blatt, doppelseitig, 1 A4-Blatt pro Schüler
              (bei 3 Seiten wird eine Leerseite ergänzt)
Mit --a5 wird nicht umsortiert (Druck direkt auf A5, doppelseitig).

Aufruf:
    python gruppen_zusammenfuegen.py                 # 35 Schüler
    python gruppen_zusammenfuegen.py -n 28           # nur 28 Blätter
    python gruppen_zusammenfuegen.py --a5            # für A5-Papier
    python gruppen_zusammenfuegen.py --lange-kante   # falls Drucker anders wendet
    python gruppen_zusammenfuegen.py --nummer        # "Blatt k" auf jede Seite
"""
import argparse
import re
import sys
from itertools import combinations, product
from pathlib import Path

PAGEBREAK = '<div style="page-break-after: always; break-after: page;"></div>'
LEERSEITE = " "
ROEMISCH = {"i": 1, "ii": 2, "iii": 3, "iv": 4, "v": 5, "vi": 6, "vii": 7, "viii": 8,
            "ix": 9, "x": 10, "xi": 11, "xii": 12}


def gruppe_erkennen(praefix):
    """-> (dimension, sortierwert) oder None"""
    if re.fullmatch(r"[01]{3,}", praefix):
        return 3, int(praefix, 2)
    if re.fullmatch(r"[1-9][0-9]*", praefix):
        return 0, int(praefix)
    if re.fullmatch(r"[A-Z]", praefix):
        return 1, ord(praefix)
    if praefix in ROEMISCH:
        return 2, ROEMISCH[praefix]
    return None


def dateien_einlesen(ordner):
    dims = {}
    for f in sorted(ordner.glob("*.md")):
        praefix = f.stem.split("_", 1)[0].strip()
        g = gruppe_erkennen(praefix)
        if g is None:
            print(f"! übersprungen (Präfix unbekannt): {f.name}")
            continue
        dims.setdefault(g[0], []).append((g[1], praefix, f))
    if not dims:
        sys.exit(f"Keine passenden .md-Dateien in {ordner}")
    ergebnis = []
    for d in sorted(dims):
        eintraege = sorted(dims[d])
        werte = [w for w, _, _ in eintraege]
        if len(set(werte)) != len(werte):
            sys.exit(f"Doppelte Gruppe in Seite {d + 1}: {[p for _, p, _ in eintraege]}")
        ergebnis.append([(p, f) for _, p, f in eintraege])
    return ergebnis


def seite_laden(pfad, ordnername):
    text = pfad.read_text(encoding="utf-8")
    # YAML-Frontmatter entfernen
    text = re.sub(r"\A---\n.*?\n---\n", "", text, flags=re.S)
    # relative Bildpfade auf den Unterordner umbiegen
    def fix(p):
        if re.match(r"^([a-z]+:|/|#|data:)", p, flags=re.I):
            return p
        return f"{ordnername}/{p[2:] if p.startswith('./') else p}"
    text = re.sub(r"(!\[[^\]]*\]\()([^)\s]+)", lambda m: m.group(1) + fix(m.group(2)), text)
    text = re.sub(r'(<img[^>]*\bsrc=")([^"]+)', lambda m: m.group(1) + fix(m.group(2)), text)
    return text.strip()


def reihenfolge(gruppenzahlen, n):
    """Greedy: pro Seite immer eine der aktuell kleinsten Gruppen,
    darunter die Kombination mit den wenigsten Mehrfach-Begegnungen."""
    zaehler = [[0] * g for g in gruppenzahlen]
    blaetter = []
    for _ in range(n):
        erlaubt = [[i for i in range(g) if zaehler[d][i] == min(zaehler[d])]
                   for d, g in enumerate(gruppenzahlen)]
        bestes = None
        for t in product(*erlaubt):
            kosten = 0
            for s in blaetter:
                m = sum(a == b for a, b in zip(s, t))
                kosten += m * (m - 1) // 2
            if bestes is None or (kosten, t) < bestes:
                bestes = (kosten, t)
        t = bestes[1]
        blaetter.append(t)
        for d, i in enumerate(t):
            zaehler[d][i] += 1
    return blaetter


def mehrfach(blaetter):
    return sum(max(0, sum(a == b for a, b in zip(x, y)) - 1) for x, y in combinations(blaetter, 2))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("-n", "--anzahl", type=int, default=35, help="Anzahl Schülerblätter (Standard 35)")
    ap.add_argument("-o", "--ausgabe", default=None, help="Name der Ausgabedatei (.md)")
    ap.add_argument("--ordner", default="einzelseiten")
    ap.add_argument("--a5", action="store_true", help="nicht umsortieren (Druck direkt auf A5)")
    ap.add_argument("--lange-kante", action="store_true", help="Umsortierung für Wenden an langer Kante")
    ap.add_argument("--nummer", action="store_true", help='"Blatt k" klein unter jede Seite setzen')
    args = ap.parse_args()

    basis = Path(__file__).resolve().parent
    ordner = basis / args.ordner
    dims = dateien_einlesen(ordner)
    seiten = [[seite_laden(f, args.ordner) for _, f in d] for d in dims]
    gz = [len(d) for d in dims]
    blaetter = reihenfolge(gz, args.anzahl)

    def seite(k, d):
        if k is None or d >= len(dims):
            return LEERSEITE
        inhalt = seiten[d][blaetter[k][d]]
        if args.nummer:
            inhalt += f'\n\n<p style="font-size:8pt;color:#888;text-align:right;margin:0">Blatt {k + 1}</p>'
        return inhalt

    p = len(dims)
    folge = []
    if args.a5:
        q = p + (p % 2 if p > 1 else 0)  # gerade Seitenzahl, damit doppelseitig passt
        for k in range(args.anzahl):
            folge += [seite(k, d) for d in range(q)]
        modus = f"A5 direkt, {'doppelseitig' if p > 1 else 'einseitig'}"
        druckseiten = "Schülerzahl × %d" % q
    elif p == 1:
        for k in range(args.anzahl):
            folge.append(seite(k, 0))
        modus = "A4, 2 Seiten pro Blatt, einseitig, danach in der Mitte schneiden"
        druckseiten = "Schülerzahl (bei ungerader Zahl +1)"
    elif p == 2:
        for k in range(0, args.anzahl, 2):
            k2 = k + 1 if k + 1 < args.anzahl else None
            rueck = [seite(k, 1), seite(k2, 1)] if args.lange_kante else [seite(k2, 1), seite(k, 1)]
            folge += [seite(k, 0), seite(k2, 0)] + rueck
        kante = "lange" if args.lange_kante else "kurze"
        modus = f"A4, 2 Seiten pro Blatt, doppelseitig ({kante} Kante), danach in der Mitte schneiden"
        druckseiten = "Schülerzahl × 2 (bei ungerader Zahl +2)"
    elif p in (3, 4):
        for k in range(args.anzahl):
            folge += [seite(k, d) for d in range(4)]
        modus = "A4, 2 Seiten pro Blatt, doppelseitig, 1 A4-Blatt pro Schüler (nicht schneiden)"
        druckseiten = "Schülerzahl × 4"
    else:
        sys.exit("Mehr als 4 Seiten pro Schüler wird nicht unterstützt.")

    name = args.ausgabe or f"{basis.name}_gesamt_{args.anzahl}.md"
    (basis / name).write_text(f"\n\n{PAGEBREAK}\n\n".join(folge) + "\n", encoding="utf-8")

    labels = [[pr for pr, _ in d] for d in dims]
    print(f"Geschrieben: {name}  ({len(folge)} Seiten)")
    print(f"Gruppen je Seite: " + " | ".join(", ".join(l) for l in labels))
    print(f"Druck: {modus}")
    print(f"Zu druckende Seiten: {druckseiten}")
    print("\nGruppengrößen / Mehrfach-Begegnungen je Schülerzahl:")
    for n in sorted({10, 15, 20, 25, 30, args.anzahl}):
        if n > args.anzahl:
            continue
        teil = blaetter[:n]
        groessen = []
        for d, g in enumerate(gz):
            c = [sum(1 for t in teil if t[d] == i) for i in range(g)]
            groessen.append(f"{min(c)}–{max(c)}" if min(c) != max(c) else str(min(c)))
        print(f"  {n:>3} Schüler: " + " | ".join(groessen) + f"   Mehrfach: {mehrfach(teil)}")


if __name__ == "__main__":
    main()
```