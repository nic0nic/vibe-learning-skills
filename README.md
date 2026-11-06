# vibe learning – Skills für Claude

Skills für [claude.ai](https://claude.ai), mit denen Lehrkräfte Inhalte für die Übungsplattform **vibe learning** ([vl.nimals.de](https://vl.nimals.de), Quellcode: [nic0nic/vibe-learning](https://github.com/nic0nic/vibe-learning)) erstellen.

| Skill | Wofür |
|---|---|
| [`vibe-learning-seite-erstellen`](vibe-learning-seite-erstellen/SKILL.md) | Übungen und Aufgabenreihen als kurzen Aufgaben-JSON-Block erstellen; auf [vl.nimals.de/vorlage.html](https://vl.nimals.de/vorlage.html) testen, herunterladen oder einreichen. Fehlende Aufgabentypen werden als Issue vorgeschlagen. |

## Installieren in claude.ai

1. Dieses Repo als ZIP herunterladen (*Code → Download ZIP*) und entpacken.
2. Den Ordner des Skills (z. B. `vibe-learning-seite-erstellen`) **für sich** wieder als ZIP packen – im ZIP muss der Ordner mit `SKILL.md` liegen.
3. In claude.ai: *Einstellungen → Fähigkeiten* (Capabilities) → Skill hochladen. Dafür muss dort „Code-Ausführung und Dateierstellung“ eingeschaltet sein.
4. Im Chat einfach schreiben, z. B.: „Erstelle eine Übung für vibe learning zu Abschreibungen, BWR Jahrgangsstufe 9, mit Lückentext und Buchungssatz.“

Wer keine Skills nutzen kann (je nach Tarif), kopiert den Inhalt von `SKILL.md` und `references/typen.md` zu Beginn in den Chat oder in die Anweisungen eines Projekts – das Ergebnis ist dasselbe JSON.

## Ablauf

Chat → JSON-Block → [vl.nimals.de/vorlage.html](https://vl.nimals.de/vorlage.html) einfügen und testen → als Lehrkraft einreichen (es entsteht ein Pull Request in vibe-learning, der nach Freigabe auf der Seite erscheint) oder als Datei herunterladen.

## Pflege

Die Aufgabentypen kommen aus `pb_public/lib/aufgaben.js` in vibe-learning; Format und Prüfregeln aus `pb_public/lib/seite.js`. Kommt dort ein Typ dazu oder ändert sich ein Feld, `references/typen.md`, `SKILL.md` (Typenliste) und `scripts/pruefe.py` hier anpassen.
