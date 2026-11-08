# Aufbau von Leistungsnachweis und Übung

## Gemeinsame Regeln

- Ein fiktives Unternehmen je Dokument, wie in der AP: Name, Ort, Branche, Rechtsform, Geschäftsjahr, Werkstoffe. Bei Übungsreihen dasselbe Unternehmen wiederverwenden (siehe `bwr-uebungsaufgaben`).
- Einstieg mit kurzer Situation, dann Teilaufgaben. Nummerierung 1.1, 1.2 …, Material (Beleg, Konto, Grafik) direkt an der Teilaufgabe.
- Pro Teilaufgabe eine Handlung und ein Operator am Satzanfang. Zielgröße nennen (Buchungssatz, Betrag in Euro, Prozent, Fachbegriff).
- Innerhalb eines AFB Operatoren aus derselben Synonymgruppe rotieren (z. B. nennen / angeben / aufzählen), außer bei Buchungssatz und Berechnen, wo Wiederholung zum Aufgabentyp gehört.
- Teilaufgaben unabhängig lösbar halten (Folgefehler).
- Zahlen stehen im Material; Werte, die Schüler selbst berechnen können, nicht vorgeben.
- Format, Buchungssatz-Syntax und Punkteregeln: Skill `bwr-uebungsaufgaben`. Layout für Typora: Skill `typora-arbeitsblatt-layout`.

## Leistungsnachweis

Vorgehen:

1. Klären: Jgst., Lernbereiche, Dauer, Gesamtpunkte, Du/Sie, Form (Schulaufgabe/Kurzarbeit/Stegreifaufgabe), AP-Nähe.
2. Bauplan als Tabelle erstellen: Aufgabe | Teilaufgabe | Typ (T-Nr.) | AFB | Operator | AP-Vorbild | Punkte.
3. AFB-Anteil nach `jahrgangsstufen.md` einstellen und mit `pruefe_operatoren.py` kontrollieren.
4. Typen je Lernbereich aus `aufgabentypen_ap.md` wählen, passende AP-Vorbilder mit `bwr-ap-lehrplan-mapping` (`find_ap.py --lb …`) suchen und im Wortlaut lesen (`show_ap.py … --loesung` für die Punkteverteilung).
5. Vorbild nicht kopieren: Unternehmen, Zahlen und Belegdetails ändern, Struktur und Operator beibehalten.
6. Reihenfolge: Beleg-/Einstiegsaufgabe zuerst, innerhalb der Aufgabe von AFB I über II zu III.
7. Lösung mit Punkten (Skill `bwr-uebungsaufgaben`), Gesamtpunkte aus den Teilpunkten summieren.
8. Umfang prüfen: ein Punkt ≈ eine Minute (ISB-Handreichung). Richtwerte: Stegreifaufgabe 20–22 P, Kurzarbeit 30–32 P, Schulaufgabe 42–46 P; Jgst. 10 (2./3. Schulaufgabe) höchstens AP-Umfang. Drittelung: BWL-Fragestellungen / Rechnen / Buchführung möglichst je ein Drittel der Punkte. Details und Prüfskript: Skill `bwr-bewertung-musterloesung`.

Die Punkte je Teilaufgabe und die Gesamtpunktzahl werden den Schülern **nicht** in der Angabe genannt (Handreichung); sie stehen nur im Lösungsvorschlag.

## Übung

Unterschiede zum Leistungsnachweis:

- Höherer AFB-I-Anteil (Begriffe, Zuordnen), kleinschrittige Teilaufgaben mit einem Lerngedanken je Aufgabe.
- Hilfen erlaubt (Kontenliste, Schema, Beispiel), je Jgst. nach `jahrgangsstufen.md`.
- Steigerung: Grundaufgabe → Variation (andere Konten, 7 % USt, Skonto) → AP-nahe Transferaufgabe am Ende.
- Typisches Muster: 2–3 gleichartige Belege nacheinander (gleicher Typ, wechselnde Konten), dann eine gemischte Aufgabe, dann Begründen/Prüfen.
- Optional eine Original-AP-Teilaufgabe zum Schluss („AP-Aufgabe“), Wortlaut aus `show_ap.py`.

## Qualitätscheck vor der Ausgabe

1. Jede Teilaufgabe beginnt mit einem Operator aus `operatoren.json`.
2. `scripts/pruefe_operatoren.py angabe.md` ausführen: AFB-Verteilung im Zielbereich, keine unnötigen Wiederholungen, keine Sätze ohne Operator.
3. Keine Lösungsvorwegnahme in Angabe oder Begriffslisten.
4. Gefragtes ist im Material auffindbar; Zahlen konsistent (Netto/Brutto, USt-Satz).
5. Alle Teilaufgaben haben einen Lösungsvorschlag; Punkte in der Lösung ergeben die Gesamtsumme.
6. Bei AP-Vorbildern: Quelle (Jahr/Termin, Nr.) im Bauplan notiert, Text nicht wörtlich übernommen.
