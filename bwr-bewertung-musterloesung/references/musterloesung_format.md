# Format des Lösungsvorschlags (Musterlösung)

Ziel: Der Lösungsvorschlag ist zugleich Korrekturgrundlage. Jeder Punkt muss einem Schritt oder Teilergebnis eindeutig zuordenbar sein. Layout und Konventionen sind identisch mit dem Skill `bwr-uebungsaufgaben` (Markdown, Typora).

## Aufbau der Datei

```
# Lösung – <Titel>

**Gesamtpunktzahl: N P**

## Aufgabe 1 – <Thema> (X P)

1.1 <Kurztitel> (Y P)

Nebenrechnung: ...

<Buchungssatz im Codeblock>

1.2 ...
```

- Überschrift je Aufgabe mit Summe `(X P)`; Teilaufgaben mit `N.M Titel (Y P)` oder nur `N.M (Y P)`.
- Summe der Teilaufgaben = Aufgabenpunkte; Summe der Aufgaben = Gesamtpunktzahl (prüft `scripts/umfang_check.py`).
- Seitenumbruch zwischen Aufgaben nach Bedarf: `<div style="page-break-after: always; break-after: page;"></div>`

## Buchungssätze

- Codeblock; je Konto eine Zeile `Nr KÜRZEL Betrag €`; Habenseite nach `an` in derselben Zeile der ersten Sollbuchung bzw. darunter.
- Punkte des Buchungssatzes als `(N)` am Ende der letzten Zeile des Blocks (Konto-mit-Betrag = 1 P je Konto).
- Ab Jgst. 8 mit Kontonummer und Kürzel (aus dem Kontenplan), in Jgst. 7 nur Kürzel/Bezeichnung.
- Nebenrechnung (Brutto→Netto, USt, Anschaffungskosten, Abgrenzungsbetrag …) **vor** dem Block als Zeile `Nebenrechnung: …`; ihre Punkte nur dort, wo `punktevergabe_grundregeln.md` einen Extrapunkt vorsieht (z. B. Jgst. 7 Netto aus Brutto, Anschaffungskosten, Abgrenzungsbetrag, Bruttoausfall, Kurswert). Der Punkt steht in der Teilaufgaben-Summe, nicht im `(N)` des Blocks – dann in der Zeile vermerken: `Nebenrechnung (1 P): …`.
- Doppik beachten: Soll = Haben.
- Bei mehreren richtigen Lösungswegen: Alternative nennen („Alternativ: …“), gleiche Punkte.

## Schemata und Berechnungen

- Tabelle mit Spalten Bezeichnung | Betrag | %-Spalte (falls Prozentschema); Zielwert fett.
- Punkte: je Zwischenergebnis 1 P, Ergebnis mit Einheit; Extrapunkt für das Schema, wenn Handreichung 3.11 greift (Tabelle in `punktevergabe_grundregeln.md`, Abschnitt 8).
- Rechenweg angeben (Formel, eingesetzte Werte), Rundung nennen.

## Textaufgaben

- Mit „z. B.:“ einleiten, wenn mehrere Antworten möglich sind; Punkte je Teilantwort als Haken-Liste: `- Aspekt (1 P)`.
- Erwartete Anzahl Nennungen steht in der Aufgabe (z. B. „Nenne zwei …“) → Lösungsvorschlag enthält mind. diese Anzahl plus ggf. weitere Alternativen, gekennzeichnet als „weitere mögliche Antworten“.
- Punkte je Operator: siehe `operatoren_punkte.md`.

## Bewertungshinweis (je Aufgabentyp einmal, bei neuem Typ wiederholen)

Muster: *„Die maximal erreichbare Punktzahl beträgt vier Punkte. Ein Punkt wird für die Berechnung des Anschaffungswerts angesetzt. Drei Punkte sind für den Buchungssatz (jeweils Konto mit Betrag) vorgesehen.“*

## Checkliste vor Abgabe

1. Jede Zahl der Musterlösung nachgerechnet (Python, nicht im Kopf), Doppik geprüft.
2. Konten/Nummern gegen Kontenplan geprüft.
3. Punkte je Block = Anzahl Konten (+ Extrapunkte nach Katalog).
4. `python3 scripts/umfang_check.py <lösung.md> --art <art>` ohne Warnung.
5. Folgefehler: Teilaufgaben möglichst unabhängig; wo nicht, im Hinweis „Folgefehler werden berücksichtigt“.
