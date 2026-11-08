---
name: selbstlernheft-html
description: Erstellt druckfertige Selbstlernhefte (A4, HTML+PDF) für den Unterricht im Layout „Saitgig/Finanzierung“ – Szenario-Einstieg, Infotexte, Alltagsvergleiche, s/w-Grafiken, Überblickskästen zum Ergänzen, Aufgaben fürs Blockblatt, nummerierte Lösungsblätter L1…Ln und platzoptimierte Paginierung. Nutzen, wenn eine Lehrkraft ein Heft, Arbeitsheft oder eine Sequenz zur Selbsterarbeitung mit Lösungen zum Auslegen möchte.
---

# Selbstlernheft (HTML → A4/PDF)

Erzeugt aus **einer** Python-Inhaltsdatei:
- Schülerheft (Lücken unsichtbar) und Lehrkraftfassung (Lösungen blau, Monospace)
- je eine **Kompaktfassung** (platzoptimiert auf A4, Fußzeile „Seite x von n“)
- **Lösungsblätter L1…Ln** (ein A4-Blatt pro Kapitel, große Nummer oben rechts) zum Auslegen im Klassenzimmer
- Export: ZIP `<Titel>/html/*.html` und `<Titel>/pdf/*.pdf`

Dateien:
- `scripts/heft_lib.py` – Bausteine + `build()` (siehe Docstrings)
- `scripts/svg_kit.py` – s/w-Grafikbausteine (Kasten, Pfeil, gestapelte Säulen, Zeitstrahl)
- `scripts/paginate.py` – Kompaktfassung (wird von `build()` aufgerufen)
- `scripts/pruefen.py` – Überlauf-Check + Miniaturvorschau (PNG)
- `scripts/export.py` – PDFs + ZIP
- `assets/style.css` – komplettes Layout (nicht inline neu erfinden)
- `references/vorlage_inhalt.py` – lauffähige Minimalvorlage, **Ausgangspunkt für jedes neue Heft**
- `references/beispiel_finanzierung/` – vollständiges Referenzheft (BwR 9, Finanzierung) mit allen Grafiken; ältere Einzeldatei-Fassung, nur als Ideen- und Formulierungsquelle verwenden

## Ablauf

1. **Klären** (nur was fehlt): Fach/Jgst., Thema + Lehrplanbezug, was ausdrücklich *nicht* selbst erarbeitet wird, Modellunternehmen/Szenario, Kapitelzahl, ob ein Teil als separate Ergänzung ausgegliedert wird.
2. **Fachlich vorbereiten:** Bei BwR Aufgaben mit `bwr-aufgabenstellungen-afb` formulieren (Operator am Satzanfang, Du-Form), Fachkonventionen nach `bwr-uebungsaufgaben`. **Keine Punkte** im Heft. Alle Zahlen per Python nachrechnen. **Zahlenformat in Lösungen:** Euro-Beträge immer mit zwei Nachkommastellen und Tausenderpunkt, auch in Nebenrechnungen und Vergleichen (`420.000,00 + 260.000,00 = 680.000,00 €`, nicht `420.000 + 260.000`); Ergebnisse kaufmännisch auf zwei Nachkommastellen runden (DIN 1333), also `11,11 %` statt `11,1 %`. Nur glatte Prozentsätze (z. B. `30 %`, `2,5 %`) ohne zweite Stelle. Vor der Auslieferung alle Lösungstexte auf Beträge ohne `,00` prüfen. Vorlagen der Lehrkraft (Verlagsblätter) inhaltlich nutzen, Thesen aber kritisch prüfen und Abweichungen in der Antwort begründen.
3. **Inhalt schreiben:** `references/vorlage_inhalt.py` ins Arbeitsverzeichnis kopieren, `SKILL_DIR` setzen, Kapitel füllen (Bausteine unten).
4. **Bauen:** `SKILL_DIR=<skillpfad> python3 inhalt.py` → `out/`.
5. **Prüfen:** `python3 <skill>/scripts/pruefen.py out/*_kompakt.html out/Loesungsblaetter_*.html`, dann die `*_vorschau.png` mit Read ansehen. Überlauf muss „keiner“ sein; Lücken, Grafiken, Umbrüche optisch kontrollieren.
6. **Ausliefern:** Zuerst die Lehrkraftfassung zur Durchsicht, nach Freigabe alles. Final per `export.py` als ZIP.

## Kapitelaufbau (Bausteine aus heft_lib)

| Baustein | Zweck / Regel |
|---|---|
| `titelseite(...)` | Kopfzeile Name/Klasse/Datum, Titel + Logo-SVG, Szenario „Dein Auftrag“ (Bekannte/r bittet um Rat → am Ende Beratungs-E-Mail), Steckbrief, Arbeitsplan (Seite + Lösungsblatt + ☐), Hinweis **Blockblatt**, Legende |
| `kap(n, titel, pb=False)` | Kapitelkopf; `pb=True` = neue Seite auch in Kompaktfassung |
| `info(html, cols=True)` | Infotext 9,6 pt; bei längeren Abschnitten zweispaltig. Gezielter Spaltenumbruch: `info(zwei(links, rechts))` |
| `alltag(titel, html)` | **nur** bei echtem Alltagsbezug der Schüler (Handyvertrag, Dispo, Auto, Moped). Sonst `beispiel(titel, html)` |
| `fig(svg)` | Grafik/Schaubild, wo es sich anbietet (Abläufe, Bilanzen, Verläufe, Vergleiche). s/w: Grau, Schraffur `url(#§h)`, **kein Punktraster hinter Text** |
| `ueb(nr, titel, html)` | Eingerahmter Merkteil mit Lücken `a('Lösung','30mm')`. Zeilenumbruch so setzen, dass Zusammengehöriges (z. B. „Mittel___“) in einer Zeile steht |
| `tabelle(kopf, zeilen)` | In Tabellen keine Unterstrich-Linien; Zeilen mit mehrzeiligen Einträgen (Antwort > 28 Zeichen oder 2 Einträge in einer Zelle) bekommen automatisch Schreiblinien für alle Antwortzellen der Zeile |
| `material(titel, html)` | Bilanz, Rechnung, Tilgungsplan … |
| `aufg(nr, aufg_kopf() + task(...))` | Aufgaben ohne Schreibplatz (Blockblatt): `ab(lösung, n)` / `karo(lösung, n)` erscheinen nur in der Lösung |
| `karo(..., keep=True)` / `ab(..., keep=True)` | Ausnahme: Platz im Heft, wenn die Aufgabe zum Merkteil gehört (z. B. erste Kennzahlberechnung direkt unter der Formel) |
| `keep(html)` | Erklärung + zugehörige Aufgabe bleiben auf einer Seite |
| `check(nr)` | „✔ Ln – Vergleiche jetzt mit Lösungsblatt Ln“ am Kapitelende |
| `seitenref('.bil')` | „siehe S. x“, wird in der Kompaktfassung automatisch korrigiert |

Was auf ein Lösungsblatt kommt, steuert `lsg()` automatisch: alle `ueb(...)` und `aufg(...)` mit derselben Nummer.

## Gestaltungsregeln (aus Rückmeldungen der Lehrkraft)

- Druck schwarz-weiß; Lösungsschrift blau + Monospace nur in Lösungen.
- Mehr Bilder und Grafiken als reiner Text; Vergleiche aus dem echten Leben, wenn sie passen (z. B. EK-Quote: alter Gebrauchtwagen bar bezahlt vs. Neuwagen auf Kredit, mit Zeichnung).
- Überschriften „AUS DEM ALLTAG“ nur bei echtem Alltagsbezug, sonst „BEISPIEL“.
- Keine Notizfelder, keine leeren Schreibflächen für Blockblatt-Aufgaben; lieber weniger Seiten.
- Kompaktfassung ist Standard; Seitenumbruch nur gezielt (`pb=True`), Überschriften und „✎ Aufgaben“ nie allein am Seitenende (macht `paginate.py`).
- Grafik-Labels dürfen sich nicht überlappen und nicht abgeschnitten sein → Vorschau ansehen.
- Teile, die (noch) nicht gebraucht werden, als eigenen Teil ausgeben: `build(..., teile=[('Kap1-6',[1..6]), ('Ergaenzung_Kap7-9',[7,8,9])])` – jeder Teil bekommt eigene Lösungsblätter.

## Export

```
python3 <skill>/scripts/export.py "Thema 101" Thema_101.zip \
  out/X_Heft_Schueler_kompakt.html=1_Heft_Schueler \
  out/X_Heft_Lehrkraft_kompakt.html=2_Heft_Lehrkraft_mit_Loesungen \
  out/Loesungsblaetter_L1-L6.html=3_Loesungsblaetter_L1-L6
```
Nur die finalen Fassungen exportieren (Kompakt + Lösungsblätter), durchnummeriert. Drucken: A4, Ränder „Keine“, Hintergrundgrafiken an.

## Voraussetzungen
Python 3, `playwright` (Chromium), `Pillow`, `pdftoppm` (poppler). Fehlt Chromium: `python3 -m playwright install chromium`.
