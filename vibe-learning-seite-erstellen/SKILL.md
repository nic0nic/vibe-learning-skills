---
name: vibe-learning-seite-erstellen
description: Erstellt Übungen für die Lernplattform vibe learning (vl.nimals.de) als kurzen Aufgaben-JSON-Block, den Lehrkräfte auf vl.nimals.de/vorlage.html einfügen, testen und einreichen. Nutzen, wenn eine Lehrkraft eine interaktive Übung, Aufgabenreihe oder Erarbeitung für vibe learning möchte (Multiple Choice, Zahlen, Lückentext, Zuordnen, Freitext, Lern-Chat, Buchungssatz, Tabelle ausfüllen) – auch wenn nur „Übung für vibe learning“ oder „Aufgaben für die Plattform“ gesagt wird. Fehlt ein Aufgabentyp, prüft der Skill die Umsetzbarkeit und bereitet ein GitHub-Issue vor.
---

# Übung für vibe learning als Aufgaben-JSON

Ziel: mit **wenig Text** (die Lehrkraft hat evtl. nur wenige Credits) einen **gültigen JSON-Block** erzeugen. Keine HTML-Seite, kein Artefakt, keine langen Erklärungen – die Seite baut vl.nimals.de daraus.

## Ablauf

1. **Klären (höchstens eine Rückfrage):** Fach, Jahrgangsstufe, Thema, ungefährer Umfang. Was die Lehrkraft schon gesagt oder hochgeladen hat, nicht erneut fragen. Fehlt nur Kleines, sinnvoll annehmen.
2. **Aufgabentypen wählen** – nur diese gibt es (Felder und Beispiele: `references/typen.md`, nur bei Bedarf lesen):
   `mc` Multiple Choice · `zahlen` Zahleneingabe · `luecken` Lückentext mit Auswahllisten · `zuordnen` Karten in Felder ziehen · `freitext` Begriffe eingeben (mit Tippfehlererkennung) · `chat` Lern-Chat Schritt für Schritt · `buchungssatz` Buchungssatz bilden · `tabelle` Tabelle ausfüllen (z. B. Tilgungsplan)
   Passt nichts davon: siehe „Fehlender Aufgabentyp“.
3. **JSON ausgeben:** genau **ein** Codeblock ```json …```, davor höchstens ein Satz, danach diese Hinweise (kurz):
   > Kopiere den Block auf **https://vl.nimals.de/vorlage.html**, klicke „Prüfen und Vorschau“ und probiere die Übung aus. Als Lehrkraft kannst du sie dort einem Bereich zuordnen und einreichen – oder als Datei herunterladen.
4. **Änderungswünsche:** den **vollständigen** JSON-Block neu ausgeben (er wird komplett eingefügt), ohne Wiederholung der Erklärungen.
5. **Wenn Code-Ausführung verfügbar ist:** vor der Ausgabe `python3 scripts/pruefe.py datei.json` laufen lassen und Fehler beheben. Sonst die Regeln unten selbst einhalten.

## Format

```json
{"titel": "Kredite bei der Bank", "kurztext": "Ein Satz für die Übersicht",
 "schritte": [
  {"kurz": "Kredit", "titel": "Was ist ein Kredit?", "html": "<h2>…</h2><p>Erklärung …</p>"},
  {"kurz": "1.1", "titel": "…", "erinnerung": "<p>kurze Regel/Formel</p>", "material": "<p>alle nötigen Werte</p>",
   "aufgaben": [{"typ": "mc", "nr": "1.1", "frage": "…", "options": ["richtig", "falsch"], "correct": [0], "why": {"1": "Warum falsch"}}]}
 ]}
```
- `schritte` = Knöpfe oben auf der Seite (Erarbeitung). Ein Schritt hat Erklärung (`html`) und/oder `aufgaben` (mehrere möglich). Für eine einfache Aufgabenliste genügt statt `schritte` auch `"aufgaben": [...]`.
- Je Aufgabe optional: `nr` (z. B. „5.1“), `frage`, `erinnerung`, `erinnerungZu: true` (Erinnerung startet zugeklappt, wenn sie die Lösung verraten würde), `material`, `ok` (Text bei Erfolg), `danach` (Folgeaufgabe, erscheint nach richtiger Lösung).

## Regeln

- **JSON gültig halten:** nur doppelte Anführungszeichen; keine Kommas vor `]`/`}`; Zahlen ohne Tausenderpunkt (`"l": 11900`, Komma als Punkt: `58.31`); Anführungszeichen in HTML als `\"`; keine Zeilenumbrüche in Texten (stattdessen `<br>` oder `<p>`).
- **HTML nur für Text** (Erlaubtliste, sonst lehnt die Prüfung ab): `p br b strong i em u s sub sup small mark span div hr ul ol li h2 h3 h4 table thead tbody tr th td code pre blockquote`, als Attribut nur `class="…"` (bei `td`/`th` auch `colspan`, `rowspan`). Keine Links, Bilder, Styles, kein JavaScript.
- **Didaktik:** Vor neuen Aufgaben eine kurze Erklärung (Schritt mit `html`) oder `erinnerung`. Aufgabenstellungen beginnen mit einem **Operator** (nenne, berechne, ordne zu, bilde den Buchungssatz …). **Alle nötigen Werte stehen im selben Schritt** (`material`), nie nur in einem früheren. Bei MC zu jeder falschen Antwort ein `why`. Richtige Antwort darf an erster Stelle stehen (wird gemischt).
- **BWR (Bayern):** Beträge im Text „11.900,00 €“; Konten ab Jgst. 8 mit Nummer und Kürzel („2800 BK“), **in Jgst. 7 nur Kürzel** („BK“). Gibt es die Skills `bwr-uebungsaufgaben` oder `bwr-aufgabenstellungen-afb`, deren Schreibweise und Operatoren übernehmen.
- **Datenschutz:** keine echten Namen von Schülerinnen und Schülern, keine personenbezogenen Daten.
- **„Kleinigkeiten“** (Tabellen, Hervorhebungen, eine Formel im Text) gehen über HTML. Neue Interaktion (anderes Bedienen, andere Prüfung) ist ein neuer Aufgabentyp.

## Fehlender Aufgabentyp

1. **Erst umformen:** Lässt sich das Ziel mit vorhandenen Typen erreichen? (z. B. Reihenfolge → `zuordnen` mit Feldern „1.“, „2.“ …; Wahr/Falsch → `mc`; Tabelle ausfüllen → `zahlen`; Begriffe nennen → `freitext`). Wenn ja: so umsetzen und kurz sagen.
2. **Umsetzbarkeit prüfen** (alle müssen zutreffen): läuft im Browser ohne Server · Antwort automatisch eindeutig prüfbar · speichert keine neuen Schülerdaten · mit Daten (JSON) beschreibbar · in mehreren Fächern oder Übungen nützlich.
3. **Nicht umsetzbar:** in 1–2 Sätzen begründen und die beste Lösung mit vorhandenen Typen anbieten.
4. **Umsetzbar:** ein Issue im Repo **nic0nic/vibe-learning** vorbereiten:
   - Ist ein GitHub-Werkzeug verfügbar: Issue dort anlegen.
   - Sonst einen Link ausgeben, Titel und Text URL-kodiert (gesamte Länge unter 6000 Zeichen):
     `https://github.com/nic0nic/vibe-learning/issues/new?title=Neuer%20Aufgabentyp%3A%20…&body=…`
   - Inhalt: **Wofür** (Fach, Jgst., Beispielaufgabe) · **Bedienung** · **Prüfregel** (wann richtig, welche Hinweise bei Fehlern) · **Vorschlag für die Daten** (kleines JSON-Beispiel im Stil der vorhandenen Typen) · Ergebnis der Prüfung aus Schritt 2.
   - Hinweis an die Lehrkraft: Zum Absenden braucht sie ein (kostenloses) GitHub-Konto. Bis zur Umsetzung die Übung mit vorhandenen Typen anbieten.
