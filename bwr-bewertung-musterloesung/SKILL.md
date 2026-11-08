---
name: bwr-bewertung-musterloesung
description: 'Punktevergabe, Umfang (1 Punkt ≈ 1 Minute) und Musterlösungen für BwR-Leistungsnachweise (Realschule Bayern, WPFG II) nach ISB-Handreichung zur Leistungsbewertung. Einsetzen beim Bepunkten von Aufgaben, beim Planen des Umfangs und beim Erstellen oder Korrigieren von Lösungsvorschlägen.'
---

# BwR: Bewertung und Musterlösung

Verdichtung der ISB-Handreichung „Leistungskorrektur/Leistungsbewertung im Fach BwR“ (Okt. 2024). Zweck: Aufgaben im richtigen Umfang bepunkten und Musterlösungen bauen, ohne die Handreichung im Kontext zu haben. Zusammenspiel: Aufgabenstellungen/Operatoren → `bwr-aufgabenstellungen-afb`; Aufgaben nach Lehrplan/AP suchen → `bwr-ap-lehrplan-mapping`; Layout/Übungsformat → `bwr-uebungsaufgaben`.

## Kernregeln (immer parat)

- **1 Punkt ≈ 1 Minute.** Richtwerte: Stegreifaufgabe 20–22 P (20 min), Kurzarbeit 30–32 P (30 min), Schulaufgabe 42–46 P (45 min). Jgst. 10, 2./3. Schulaufgabe: höchstens AP-Umfang.
- **Drittelung:** BWL-Fragestellungen / Rechnen / Buchführung möglichst je ein Drittel der Punkte.
- **Punkte werden den Schülern nicht angegeben**; nur die Musterlösung enthält sie.
- **Buchungssatz:** 1 P je Konto mit Betrag. Extra-Punkt nur für gesondert zu berechnende Beträge (Katalog in `references/punkte_je_aufgabentyp.md`); Brutto→Netto nur in Jgst. 7 ein Extrapunkt.
- Halbe Punkte nur bei geringfügigen Fehlern; nie negative Punktzahl je Teilaufgabe.
- Notenschlüssel: 50 % der Punkte = Untergrenze Note 4.

## Ablauf

1. **Art und Umfang festlegen** (Stegreif/Kurz/Schul/AP-Niveau), Zielpunkte = Richtwert. Aufteilung in Drittel planen. → `references/umfang_und_konzeption.md`
2. **Aufgaben bepunkten**: Aufgabentyp im Katalog suchen (Buchungssätze, Berechnungen, Kennzahlen, Text), Punkte ansetzen, Extrapunkte und Sonderfälle beachten. → `references/punkte_je_aufgabentyp.md`, `references/punktevergabe_grundregeln.md`, `references/operatoren_punkte.md`
3. **Musterlösung schreiben** im vorgegebenen Format; alle Zahlen per Code nachrechnen, Konten gegen Kontenplan prüfen. → `references/musterloesung_format.md`
4. **Check**: `python3 scripts/umfang_check.py loesung.md --art schul --kategorien "1:F,2:R,3:B"` (Summen Teile = Aufgabe = Gesamt; Umfang im Richtwert; Drittel). Bei Warnung korrigieren, bis „OK“.
5. Bei Korrektur von Schülerlösungen oder für Bewertungshinweise: `references/korrektur_schuelerloesungen.md`.

## Kennzeichnung in der Antwort

Nenne am Ende kurz: Gesamtpunkte, Verteilung B/R/F, veranschlagte Minuten, und Stellen, an denen die Punktvergabe eine Ermessensentscheidung ist.

## Grenzen

- Der Typ-Katalog stammt aus den Beispielen der Handreichung und ist nicht vollständig; für neue Aufgabentypen nach dem Prinzip „Konto mit Betrag = 1 P, eigens zu berechnender Betrag = +1 P“ ableiten und die Lehrkraft darauf hinweisen.
- Die AP-Punktzahlen (Teil A 80 P, Nachtermine 110 P, Teil-B-Aufgaben 15 P) sind aus den Lösungsvorschlägen 2023–2025 ausgezählt; die Wahlregel für Teil B steht nicht in den Quellen und ist erschlossen.
- Regeln, die nicht in der Handreichung stehen (z. B. Umgang mit überzähligen Nennungen), legt die Lehrkraft fest.
