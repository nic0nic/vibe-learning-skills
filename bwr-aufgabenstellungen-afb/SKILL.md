---
name: "bwr-aufgabenstellungen-afb"
description: 'Formuliert operationalisierte Aufgabenstellungen für BwR (Realschule Bayern, WPFG II) nach Anforderungsbereichen I–III, orientiert an Aufgabentypen und Niveau der Abschlussprüfungen 2023–2025, angepasst an die Jahrgangsstufe. Nutzen für Leistungsnachweise, Schulaufgaben, Stegreifaufgaben und Übungen, bei Fragen nach passenden Operatoren, AFB-Verteilung oder AP-nahen Aufgaben.'
---

# BwR: Operationalisierte Aufgabenstellungen nach AFB

Einsatz: Leistungsnachweise und Übungen im Fach BwR, wahlweise AP-nah, in der Schwierigkeit an die Jahrgangsstufe angepasst. Der Skill legt fest, welcher Operator in welchem Anforderungsbereich steht, welche Aufgabentypen die APs verwenden und wie ein Dokument aufgebaut wird. Für Format, Buchungssatz-Syntax, Belege und Punktevergabe gilt der Skill `bwr-uebungsaufgaben`. Passende AP-Vorbilder liefert `bwr-ap-lehrplan-mapping`.

## Dateien

- `references/afb_operatoren.md`: 47 Operatoren nach AFB I–III mit Synonymgruppen, Du- und Sie-Form, Häufigkeit in den APs
- `references/operatoren.json`: dieselben Operatoren maschinenlesbar
- `references/aufgabentypen_ap.md`: 26 Aufgabentypen der APs (T1–T26) mit Musterformulierung, AFB, Jahrgangsstufe, Fundstellen
- `references/jahrgangsstufen.md`: Stoff und Stellschrauben für Jgst. 7–10 (AFB-Anteile, Rechenschritte, Hilfen)
- `references/aufbau_leistungsnachweis_uebung.md`: Bauplan, Reihenfolge, Qualitätscheck
- `scripts/pruefe_operatoren.py`: prüft eine fertige Angabe (Operatoren, AFB-Verteilung, Wiederholungen)

## Vorgehen

1. **Klären** (nur was fehlt): Leistungsnachweis oder Übung, Jgst., Lernbereich/Thema, Umfang (einzelne Teilaufgaben oder ganzes Dokument), Dauer und Gesamtpunkte, AP-Nähe (frei, angelehnt, AP-nah), Anrede. Standard: Du-Form; Sie-Form nur auf Wunsch (AP-Wortlaut). Standard: einzelne Aufgabe(n) oder Bauplan; ein vollständiges Dokument nur auf ausdrückliche Bitte.
2. **Typen wählen:** Zum Lernbereich passende Typen aus `references/aufgabentypen_ap.md` auswählen (Spalte „ab Jgst.“ beachten). Vorbilder suchen und im Wortlaut lesen: `bwr-ap-lehrplan-mapping`, `find_ap.py --lb 8.2 --typ BS` und `show_ap.py 2025/HT 1.3.2 --loesung`.
3. **Bauplan** als Tabelle ausgeben und bei einem ganzen Dokument kurz zur Freigabe vorlegen: Teilaufgabe | Typ | AFB | Operator | AP-Vorbild | Punkte.
4. **Formulieren:** Pro Teilaufgabe ein Operator am Satzanfang, eine Handlung, Zielgröße benennen. Schwierigkeit über die Stellschrauben in `references/jahrgangsstufen.md` einstellen.
5. **Rotation:** Innerhalb eines AFB und eines Dokuments Operatoren derselben Synonymgruppe wechseln (nennen / angeben / aufzählen; erläutern / erklären; berechnen / ermitteln / bestimmen). Ausnahme: „den Buchungssatz bilden“ und „berechnen“ dürfen sich wiederholen, weil sie den Aufgabentyp tragen. Ist eine Gruppe erschöpft, die Wiederholung offen benennen statt einen unpassenden Operator zu nehmen.
6. **Prüfen:** `python3 scripts/pruefe_operatoren.py angabe.md` (bei Sie-Form `--sie`). AFB-Verteilung mit dem Zielbereich abgleichen, Wiederholungen und Sätze ohne Operator klären.
7. **Lösung** nach `bwr-uebungsaufgaben` mit Punkten, Gesamtpunkte als Summe der Teilpunkte. Umfang (1 P ≈ 1 min, Richtwerte, Drittelung) und Punktevergabe: Skill `bwr-bewertung-musterloesung`. Punkte nie in der Angabe nennen.

## AFB-Zuordnung

| AFB | Kern | Typische Operatoren |
|---|---|---|
| I Reproduktion | Wiedergeben aus Gelerntem oder Material, ohne Erklärung | nennen, angeben, beschreiben, definieren, zuordnen, vervollständigen |
| II Reorganisation und Transfer | Bekanntes selbstständig anwenden, erklären, rechnen, buchen, entscheiden | berechnen, ermitteln, den Buchungssatz bilden, erläutern, begründen, abgrenzen, prüfen, ableiten, entscheiden |
| III Reflexion und Problemlösung | Urteil bilden, abwägen, begründet Stellung nehmen | beurteilen, bewerten, Stellung nehmen, diskutieren |

Zuordnungsregeln:

- Der AFB ergibt sich aus Operator **und** Aufwand. „Gib die Zuschlagsgrundlage an“ ist I; „Berechne den Zuschlagssatz“ ist II; „Berechne und beurteile die Anlagendeckung II“ enthält einen III-Anteil.
- Ein Operator allein legt den AFB nicht fest. Wird er mit einer neuen Situation oder mit mehreren Schritten verknüpft, steigt der AFB.
- Rechen- und Buchungsoperatoren zählen nach der Handreichung zu II; das Ablesen oder Einsetzen eines einzigen Werts ist inhaltlich I.
- Richtwerte aus den APs 2023–2025 (Anzahl der Teilaufgaben): AFB I ca. 28 %, II ca. 67 %, III ca. 5 %. Je Prüfung I zwischen 19 und 36 %, III zwischen 3 und 7 %. Für Jgst. 8 bis 10 abgestufte Zielwerte stehen in `references/jahrgangsstufen.md`.

## Formulierungsregeln

- Beginn mit Operator, kein „Was ist …?“ oder „Wie funktioniert …?“.
- Mehrere geforderte Aspekte ausdrücklich nennen („Nenne zwei Vorteile“), weil die Punktzahl daran hängt.
- Bei Entscheidungen Entscheidung und Begründung getrennt fordern („Entscheide … und begründe“).
- Bei Berechnung mit Beurteilung beide Operatoren nennen („Berechne und beurteile“).
- Brutto/Netto und USt-Satz ausdrücklich angeben (Standard 19 % im Kopf des Dokuments, abweichend 7 % an der Teilaufgabe).
- Zuordnungs- und Lückenaufgaben: Kennbuchstaben verwenden, keine Begriffsliste, die die Lösung vorwegnimmt.
- Konten nur dort vorgeben, wo es die Jgst. verlangt (siehe `jahrgangsstufen.md`).

## Grenzen

- Die AFB-Zuordnung einzelner Operatoren ist eine Einschätzung; die Handreichung ordnet nicht jeden Operator verbindlich zu.
- Die AFB-Anteile der APs sind nach Anzahl der Teilaufgaben gezählt, nicht nach Punkten.
- Richtwerte für Jahrgangsstufen und Bearbeitungszeit sind didaktische Vorschläge, keine amtlichen Vorgaben.
- AP-Fundstellen stammen aus dem Mapping des Skills `bwr-ap-lehrplan-mapping`; Grafiken und Bildbelege sind dort nur im Text enthalten.
