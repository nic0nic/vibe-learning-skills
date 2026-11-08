---
name: "bwr-ap-lehrplan-mapping"
description: 'Ordnet Abschlussprüfungsaufgaben BwR Realschule Bayern (WPFG II, 2023–2025 HT/NT) den Lehrplan-Lernbereichen der Jgst. 7–10 zu. Nutzen, um für ein Thema (z. B. Skonto, Gewerbesteuer, Abschreibung, Kennzahlen) die passenden AP-Aufgaben zu finden oder Unterricht, Förderplan und Übungen an der AP auszurichten.'
---

# BwR: Lehrplan ↔ Abschlussprüfung

Mapping von 278 Teilaufgaben der Abschlussprüfungen BwR (2023, 2024, 2025, je Haupt- und Nachtermin) auf die Lernbereiche (LB) des LehrplanPLUS Realschule, Wahlpflichtfächergruppe II. IIIa ist ausgeschlossen.

## Dateien

- `references/lehrplan_katalog.md`: Code-Schema `Jgst.LB` (z. B. `8.2`), Inhalte, Anzahl Teilaufgaben je LB
- `references/ap_mapping.csv`: eine Zeile je Teilaufgabe (pruefung, aufgabe, lb_haupt, lb_neben, thema, typ, konten)
- `references/index_nach_lb.md`: fertiger Rückwärtsindex je LB und Prüfung
- `references/ap/AP_JJJJ_HT.md` bzw. `_NT.md`: Volltext der Prüfungen, je Aufgabe ein Block, erst Angabe, dann Lösungsvorschlag. **Nicht im öffentlichen Repo** (Urheberrecht); wer die AP-PDFs hat, legt die Dateien lokal an (siehe „Neue AP-Jahrgänge ergänzen“). Fehlen sie, funktionieren Mapping und `find_ap.py` trotzdem.
- `scripts/find_ap.py`: Filter nach LB, Stichwort, Konto, Typ, Prüfung
- `scripts/show_ap.py`: gibt eine Teilaufgabe (mit `--loesung` samt Lösungsvorschlag) aus dem Volltext aus (nur, wenn `references/ap/` vorhanden ist)

## Vorgehen: AP-Aufgaben zu einem Thema finden

1. Thema auf LB abbilden: `references/lehrplan_katalog.md` lesen (Spalte Inhalte). Bei mehreren möglichen LB alle prüfen.
2. Abfragen, z. B.:
   - `python3 scripts/find_ap.py --lb 8.2` (Haupt- und Nebenzuordnung)
   - `python3 scripts/find_ap.py --lb 9.5 --haupt --typ BS`
   - `python3 scripts/find_ap.py --stichwort gewerbesteuer`
   - `python3 scripts/find_ap.py --konto 6730`
   - `python3 scripts/find_ap.py --uebersicht` (Häufigkeit je LB und Prüfung)
3. Treffer sichten. Das Mapping enthält nur Kurzthemen. Den Originaltext holt `scripts/show_ap.py` (Nummer = Spalte `pruefung` + `aufgabe`).
4. Auf Nachfrage Aufgaben ausgeben (siehe nächster Abschnitt). Ergebnis nach Prüfungsjahr gruppiert ausgeben, Typ (BS/BE/TX/MC) nennen. Nicht belegte LB ausdrücklich so benennen (kein Treffer = in 2023–2025 nicht geprüft).

## Aufgaben im Chat ausgeben

Nur möglich, wenn die Volltexte in `references/ap/` liegen. Fehlen sie: Fundstellen aus dem Mapping nennen (Prüfung, Aufgabe, Thema, Typ) und die Lehrkraft bitten, das AP-PDF hochzuladen; daraus zitieren.

Wird nach einer AP-Aufgabe gefragt (z. B. „zeig mir alle Skonto-Buchungssätze“, „2025 HT Aufgabe 3.3“):

1. Treffer mit `find_ap.py` bestimmen.
2. Text je Teilaufgabe mit `python3 scripts/show_ap.py 2025/HT 3.3.2` ausgeben. `--loesung` ergänzt den Lösungsvorschlag mit Punkten, `--ganz` die gesamte Aufgabe, `--kopf` die Unternehmensinformationen und formalen Vorgaben (für Kontext zu „DAZE“ etc.). Alternativ direkt in `references/ap/AP_JJJJ_HT.md` nachlesen.
3. Im Chat wortgetreu wiedergeben (Angabe, auf Wunsch Lösung), mit Prüfungsangabe in der Überschrift. Buchungssätze und Rechenschemata in Codeblöcken lassen, damit das Layout erhalten bleibt. Nichts ergänzen oder umformulieren; Punkte nur aus der Lösung übernehmen.
4. Ohne Wunsch nach Lösung nur die Angabe zeigen und die Lösung anbieten.
5. Der Volltext stammt aus der PDF-Textextraktion. Grafiken, Infografiken und Bildbelege (Rechnungen, Kontoauszüge) fehlen teils oder sind unvollständig, Wörter mit Silbentrennung stehen getrennt. Fehlt etwas Entscheidendes, darauf hinweisen und das AP-PDF verlangen.

## Grenzen (offen benennen)

- Die Zuordnung ist eine fachliche Einschätzung, keine amtliche Zuordnung. Bei Grenzfällen steht der Schwerpunkt in `lb_haupt`, Berührungen in `lb_neben`.
- Jede Teilaufgabe hat genau einen Schwerpunkt. Grundlagen aus Jgst. 7 (Beleg, Konten, UST/VORST) sind Voraussetzung vieler Buchungssätze, werden aber nur selten als `7.x` geführt. Wer „Stoff bis Klasse 8“ sucht, soll deshalb 7.x und 8.x zusammen abfragen und Buchungssätze mit Beleg (Typ BS) mitnehmen.
- Kontenangaben in `konten` sind Hinweise aus dem Kontenplan (IKR Bayern Realschule), nicht die Musterlösung. Für exakte Buchungssätze die Lösungsvorschläge der AP verwenden.
- Einzelne Zeilen sind aus Aufgabenstamm und Überschrift abgeleitet (z. B. Belegauszüge); bei Nutzung im Unterricht die Originalangabe prüfen.

## Neue AP-Jahrgänge ergänzen

1. PDF mit `pdftotext -layout` extrahieren und im Format der vorhandenen `references/ap/AP_*.md` ablegen (Abschnitte `## Angabe` und `## Lösungsvorschlag`, je Aufgabe `### Aufgabe N` mit Codeblock `text`). Angabeteil lesen.
2. Je Teilaufgabe eine Zeile an `references/ap_mapping.csv` anhängen: `pruefung` als `JJJJ/HT|NT`, `aufgabe` wie im Heft, `lb_haupt` und optional `lb_neben` (Leerzeichen getrennt), Kurzthema, `typ`, ggf. Konten.
3. `references/lehrplan_katalog.md` (Zähler) und `references/index_nach_lb.md` neu erzeugen: Zähl- und Listenlogik folgt dem vorhandenen Format (Haupt je Prüfung gruppiert, Neben als Liste).
4. `python3 scripts/find_ap.py --uebersicht` als Plausibilitätscheck.

## Typische Verwendung

- Förderplan oder Übungsblatt an AP ausrichten: LB abfragen, `--typ BS` für Buchungssätze, `--typ BE` für Rechenaufgaben, Häufigkeit mit `--uebersicht` gewichten.
- Skill `bwr-uebungsaufgaben`: Aufgaben im AP-Stil bauen, Operatoren und Punkte aus den gefundenen Originalaufgaben übernehmen.
