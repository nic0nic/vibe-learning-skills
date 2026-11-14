# Skills für Claude – Schule (BwR, IT, vibe learning)

Skills für [claude.ai](https://claude.ai) für Lehrkräfte an bayerischen Realschulen, u. a. für die Übungsplattform **vibe learning** ([vl.nimals.de](https://vl.nimals.de), Quellcode: [nic0nic/vibe-learning](https://github.com/nic0nic/vibe-learning)).

| Skill | Wofür |
|---|---|
| [`vibe-learning-seite-erstellen`](vibe-learning-seite-erstellen/SKILL.md) | Übungen für vibe learning aus den Standardbausteinen: als Aufgaben-JSON für den Editor („Übung erstellen“), als HTML-Datei oder ByCS-Paket direkt im Chat, oder als Pull Request ins Repo. Auch eigene Seiten mit eigener Interaktion (nur Datei, ByCS oder Pull Request). Fehlende Aufgabentypen werden als Issue vorgeschlagen. |
| [`selbstlernheft-html`](selbstlernheft-html/SKILL.md) | Druckfertige Selbstlernhefte (A4, HTML + PDF) mit Infotexten, s/w-Grafiken, Überblickskästen und Lösungsblättern L1…Ln. |
| [`bwr-uebungsaufgaben`](bwr-uebungsaufgaben/SKILL.md) | BwR-Übungsaufgaben (Angabe + Lösung) nach ISB-Handreichung: Buchungssätze, Belege, Operatoren, Punkte. |
| [`bwr-aufgabenstellungen-afb`](bwr-aufgabenstellungen-afb/SKILL.md) | Operationalisierte BwR-Aufgabenstellungen nach Anforderungsbereichen I–III, AP-nah, je Jahrgangsstufe. |
| [`bwr-bewertung-musterloesung`](bwr-bewertung-musterloesung/SKILL.md) | Punktevergabe, Umfang (1 Punkt ≈ 1 Minute) und Musterlösungen für BwR-Leistungsnachweise. |
| [`bwr-ap-lehrplan-mapping`](bwr-ap-lehrplan-mapping/SKILL.md) | Ordnet Aufgaben der BwR-Abschlussprüfungen 2023–2025 den Lernbereichen der Jgst. 7–10 zu. |
| [`it-aufgaben-operationalisieren`](it-aufgaben-operationalisieren/SKILL.md) | Operationalisierte Aufgabenstellungen für IT/Informatik mit rotierenden Operatoren. |
| [`gruppen-arbeitsblaetter`](gruppen-arbeitsblaetter/SKILL.md) | Arbeitsblätter mit Gruppenvarianten, die beim Austeilen automatisch ausgeglichene Gruppen ergeben. |
| [`praesentation-zu-mkslides`](praesentation-zu-mkslides/SKILL.md) | Wandelt .pdf/.pptx in eine mkslides-`slides.md` mit Bildern, Arbeitsaufträgen und Gruppen-Direktiven um. |
| [`typora-arbeitsblatt-layout`](typora-arbeitsblatt-layout/SKILL.md) | Setzt Antwortfelder und Seitenumbrüche in Markdown-Arbeitsblätter für Typora (pruefung.css). |

## Installieren in claude.ai

1. Dieses Repo als ZIP herunterladen (*Code → Download ZIP*) und entpacken.
2. Den Ordner des Skills (z. B. `vibe-learning-seite-erstellen`) **für sich** wieder als ZIP packen – im ZIP muss der Ordner mit `SKILL.md` liegen.
3. In claude.ai: *Einstellungen → Fähigkeiten* (Capabilities) → Skill hochladen. Dafür muss dort „Code-Ausführung und Dateierstellung“ eingeschaltet sein.
4. Im Chat einfach schreiben, z. B.: „Erstelle eine Übung für vibe learning zu Abschreibungen, BWR Jahrgangsstufe 9, mit Lückentext und Buchungssatz.“

Wer keine Skills nutzen kann (je nach Tarif), kopiert den Inhalt von `SKILL.md` und `references/typen.md` zu Beginn in den Chat oder in die Anweisungen eines Projekts – dann gibt es nur den JSON-Weg.

## Ablauf `vibe-learning-seite-erstellen`

- **Webseite, Editor:** Chat → JSON-Block → auf [vl.nimals.de/IT/tools/uebung-erstellen.html](https://vl.nimals.de/IT/tools/uebung-erstellen.html) einfügen und testen → als Lehrkraft einreichen (es entsteht ein Pull Request, der nach Freigabe auf der Seite erscheint) oder herunterladen.
- **Webseite, Pull Request direkt:** der Skill baut Seite und Katalog-Eintrag (`scripts/baue.js repo`) und stellt den Pull Request mit einem GitHub-Werkzeug – oder erklärt das Hochladen auf github.com.
- **Datei im Chat:** fertige HTML-Datei oder ByCS-Paket (`scripts/baue.js html|bycs`). Braucht „Code-Ausführung und Dateierstellung“.
- **JSON exportieren:** `.json`-Datei, im Editor über „Öffnen“ zu laden.

Eigene Seiten (eigener Code über die Bausteine hinaus) gehen nur als Datei, ByCS-Paket oder Pull Request direkt, nicht über den Editor.

**Bausteine aktuell halten:** Der Skill enthält in `assets/vl/` eine Kopie der Bibliotheken von vibe learning. Nach Änderungen dort (lib/, katalog.js, nav.js, sync.js, scorm.js) im Ordner dieses Repos `python3 werkzeuge/vibe-learning-holen.py` laufen lassen und committen; das Skript meldet auch, wenn `DESIGNS` in `scripts/pruefe.py` nicht mehr passt.

## Abschlussprüfungen für `bwr-ap-lehrplan-mapping` ergänzen

Die Volltexte der Abschlussprüfungen sind urheberrechtlich geschützt und deshalb **nicht** in diesem Repo. Ohne sie findet der Skill die passenden AP-Aufgaben (Prüfung, Nummer, Thema, Typ), kann sie aber nicht wörtlich zitieren. Wer die AP-PDFs hat (z. B. über Schule/ISB), legt sie für sich selbst so ab:

1. Je Prüfung eine Datei `bwr-ap-lehrplan-mapping/references/ap/AP_JJJJ_HT.md` bzw. `AP_JJJJ_NT.md` anlegen (z. B. `AP_2025_HT.md`).
2. Text aus dem PDF holen: `pdftotext -layout AP_2025_HT.pdf -` (oder in claude.ai das PDF hochladen und Claude bitten, die Datei im folgenden Format zu erstellen).
3. Aufbau der Datei – jeder Block in einem Codeblock `text`, damit das Layout erhalten bleibt:
   ````
   # Abschlussprüfung BwR 2025 Haupttermin (2025/HT)

   ## Angabe

   ### Unternehmensinformationen und formale Vorgaben

   ```text
   …Text…
   ```

   ### Aufgabe 1

   ```text
   …Angabe von Aufgabe 1 mit 1.1, 1.2 …
   ```

   ## Lösungsvorschlag

   ### Aufgabe 1

   ```text
   …Lösung von Aufgabe 1…
   ```
   ````
4. Testen: `python3 scripts/show_ap.py 2025/HT 1.1 --loesung` (im Ordner `bwr-ap-lehrplan-mapping`).
5. Für claude.ai den Ordner `bwr-ap-lehrplan-mapping` **samt** `references/ap/` als ZIP packen und als Skill hochladen (nur für dich, nicht weitergeben).

Der Ordner `references/ap/` steht in `.gitignore` und wird nicht mit hochgeladen, auch wenn du in diesem Repo arbeitest. Neue Prüfungsjahrgänge zusätzlich in `references/ap_mapping.csv` eintragen (siehe `SKILL.md`, „Neue AP-Jahrgänge ergänzen“).

## Pflege

vibe learning: Die Aufgabentypen kommen aus `pb_public/lib/aufgaben.js` in vibe-learning; Format und Prüfregeln aus `pb_public/lib/seite.js`. Kommt dort ein Typ dazu oder ändert sich ein Feld, `references/typen.md`, `SKILL.md` (Typenliste) und `scripts/pruefe.py` hier anpassen.
