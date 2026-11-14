---
name: vibe-learning-seite-erstellen
description: Erstellt Übungen für die Lernplattform vibe learning (vl.nimals.de) – als Aufgaben-JSON für den Editor auf vl.nimals.de/IT/tools/uebung-erstellen.html, als fertige HTML-Datei oder ByCS-Paket (SCORM-ZIP) direkt im Chat, oder als Pull Request ins Repo nic0nic/vibe-learning. Auch eigene Seiten mit eigener Interaktion über die Standardbausteine hinaus. Nutzen, wenn eine Lehrkraft eine interaktive Übung, Aufgabenreihe, Erarbeitung oder einen Drill für vibe learning möchte (Multiple Choice, Zahlen, Lückentext, Zuordnen, Freitext, Lern-Chat, Buchungssatz, Tabelle, Training auf Zeit) – auch wenn nur „Übung für vibe learning“, „für ByCS“ oder „Aufgaben für die Plattform“ gesagt wird. Fehlt ein Aufgabentyp, prüft der Skill die Umsetzbarkeit und bereitet ein GitHub-Issue vor.
---

# Übung für vibe learning

Ziel: mit **wenig Text** (die Lehrkraft hat evtl. nur wenige Credits) eine Übung aus den **vorhandenen Bausteinen**.
Die Bausteine (Kopie der Plattform) liegen in `assets/vl/` – **nicht lesen**, `scripts/baue.js` bettet sie ein.

## Ablauf

1. **Klären (höchstens eine Rückfrage):** Fach, Jahrgangsstufe, Thema, Umfang – und der **Weg** (Tabelle unten), falls
   nicht gesagt. Ohne Angabe: Weg A. Was schon gesagt oder hochgeladen ist, nicht erneut fragen; Kleines sinnvoll annehmen.
2. **Bausteine wählen** – zuerst immer Aufgaben-JSON (Typen unten, Felder in `references/typen.md`, nur bei Bedarf lesen).
   Nur wenn das Ziel damit nicht geht und die Lehrkraft eine eigene Interaktion will: **eigene Seite**
   (`references/eigene-seite.md`) – auch dort so viele Standardbausteine wie möglich, eigener Code nur für das Fehlende.
   Soll daraus ein neuer Standardbaustein werden: „Fehlender Aufgabentyp“.
3. **Prüfen:** `node scripts/baue.js pruefe datei` (gleiche Regeln wie die Webseite; ohne Node: `python3 scripts/pruefe.py datei.json`;
   ohne Code-Ausführung die Regeln unten selbst einhalten). Fehler beheben, dann ausgeben.
4. **Änderungswünsche:** Datei ändern und neu bauen bzw. den **vollständigen** JSON-Block neu ausgeben, Erklärungen nicht wiederholen.

## Wege

| Weg | Ergebnis | Aufgaben-JSON | eigene Seite |
|---|---|---|---|
| **A Webseite – Editor** | JSON-Block → Lehrkraft fügt ihn in „Übung erstellen“ ein, testet, lädt herunter oder reicht ein | ✓ | – |
| **B Webseite – Pull Request direkt** | Seite + Eintrag in `katalog.js` als Pull Request in nic0nic/vibe-learning | ✓ | ✓ |
| **C Datei im Chat** | eine HTML-Datei (läuft per Doppelklick) oder ein ByCS-Paket (SCORM-ZIP) | ✓ | ✓ |
| **D JSON exportieren** | `.json`-Datei zum Öffnen im Editor (Knopf „Öffnen“) oder zum Aufheben | ✓ | – |

**A:** genau **ein** Codeblock ```json …```, davor höchstens ein Satz, danach kurz:
> Kopiere den Block auf **https://vl.nimals.de/IT/tools/uebung-erstellen.html** (Ansicht „JSON“), klicke „Im Editor öffnen“ und bearbeite die Übung dort bei Bedarf weiter. „▶ Vorschau“ zeigt sie so, wie Schüler sie sehen. Als angemeldete Lehrkraft kannst du sie einem Bereich zuordnen und einreichen (ohne GitHub-Konto) – oder als Datei bzw. für ByCS herunterladen.

**B:** Bereich wählen (`node scripts/baue.js bereiche`, Pfad wie `BWR/9II/finanzierung`), dann
`node scripts/baue.js repo datei --pfad <Bereich> -o einreichung [--katalog aktuelle-katalog.js] [--text "Kurztext"]`
→ `einreichung/pb_public/<Bereich>/<id>.html`, `einreichung/pb_public/katalog.js`, `einreichung/PR.md`.
- **Mit GitHub-Werkzeug, das schreiben darf** (z. B. `gh`): aktuelle `pb_public/katalog.js` von `main` holen und als `--katalog`
  übergeben, Zweig `einreichung/<id>`, beide Dateien committen, Pull Request gegen `main` mit Titel und Text aus `PR.md`.
- **Ohne:** Aufgaben-JSON lieber über Weg A einreichen (kein GitHub-Konto nötig). Eigene Seite: die Seite und `PR.md` ausgeben
  und erklären: auf github.com/nic0nic/vibe-learning im Ordner `pb_public/<Bereich>/` „Add file → Upload files“
  (GitHub legt Kopie und Pull Request an), dazu in `pb_public/katalog.js` den ausgegebenen Eintrag in die Liste zwischen
  `EINREICHUNGEN-ANFANG` und `-ENDE` einfügen. Braucht ein (kostenloses) GitHub-Konto.

**C:** `node scripts/baue.js html datei -o <name>.html` bzw. `node scripts/baue.js bycs datei -o <name>.zip`
(`--stufen n`, wenn ein Training n Stufen hat). Ergebnis in den Ausgabeordner legen (claude.ai: `/mnt/user-data/outputs/`) und
verlinken. ByCS: „Im Kurs Aktivität anlegen → Lernpaket, ZIP hochladen.“ Den Fortschritt speichert die Datei im Browser, das Paket in ByCS.

**D:** geprüftes JSON als `<name>.json` in den Ausgabeordner, Hinweis: „Übung erstellen → Öffnen“.

Ohne Code-Ausführung gehen nur A und D (als Codeblock).

## Aufgaben-JSON

```json
{"titel": "Kredite bei der Bank", "kurztext": "Ein Satz für die Übersicht",
 "schritte": [
  {"kurz": "Kredit", "titel": "Was ist ein Kredit?", "html": "<h2>…</h2><p>Erklärung …</p>"},
  {"kurz": "1.1", "titel": "…", "erinnerung": "<p>kurze Regel/Formel</p>", "material": "<p>alle nötigen Werte</p>",
   "aufgaben": [{"typ": "mc", "nr": "1.1", "frage": "…", "options": ["richtig", "falsch"], "correct": [0], "why": {"1": "Warum falsch"}}]}
 ]}
```
- **Typen:** `mc` Multiple Choice · `zahlen` Zahleneingabe · `luecken` Lückentext mit Auswahllisten oder Wortbank · `zuordnen` Karten in Felder ziehen · `freitext` Begriffe eingeben (mit Tippfehlererkennung) · `chat` Lern-Chat · `buchungssatz` · `tabelle` Tabelle ausfüllen (z. B. Tilgungsplan) · `wahrheit` Tabelle mit ja/nein (z. B. UND/ODER) · `kombi` Aufgaben nacheinander (`{"typ": "kombi", "teile": [Aufgabe, …]}`).
- `schritte` = Knöpfe oben (Erarbeitung). Ein Schritt hat Erklärung (`html`) und/oder `aufgaben`. Für eine einfache Liste genügt `"aufgaben": [...]` statt `schritte`.
- Je Aufgabe optional: `nr`, `frage`, `erinnerung`, `erinnerungZu: true` (zugeklappt, wenn sie die Lösung verraten würde), `material`, `ok` (Text bei Erfolg).
- Drill auf Zeit und/oder endlos (Kopfrechnen, Vokabeln): Schritt mit `"training"` statt `"aufgaben"`, Stufen mit eigener Antwortform und Zeit (`typen.md`).
- Andere Optik nur auf Wunsch: oben `"design": "…"` – `kommandozeile` (schwarz, grüne Monospace-Schrift), `comic`, `titelkarte-pink`/`-rosa`/`-mint`/`-senf`/`-himmelblau`/`-bordeaux` (Punkte oder Raster in der Farbe – umschaltbar –, gestreifte Karte, fette Versalien, Briefmarke), `secondhand` (Sakko-Karo, Preisetiketten), `trattoria` (karierte Tischdecke, Speisekarte), `chemielabor` (Laborblatt, Reagenzgläser), `kino` (Filmstreifen, Filmklappen), `candy` (Zuckerstangen, Lollipops), `musik` (Notenpapier, Noten).

## Regeln

- **JSON gültig halten:** nur doppelte Anführungszeichen; keine Kommas vor `]`/`}`; Zahlen ohne Tausenderpunkt (`"l": 11900`, Komma als Punkt: `58.31`); Anführungszeichen in HTML als `\"`; keine Zeilenumbrüche in Texten (stattdessen `<br>` oder `<p>`).
- **HTML nur für Text** (Erlaubtliste, sonst lehnt die Prüfung ab): `p br b strong i em u s sub sup small mark span div hr ul ol li h2 h3 h4 table thead tbody tr th td code pre blockquote`, als Attribut nur `class="…"` (bei `td`/`th` auch `colspan`, `rowspan`). Keine Links, Bilder, Styles, kein JavaScript – das gibt es nur auf eigenen Seiten.
- **Didaktik:** Vor neuen Aufgaben eine kurze Erklärung (Schritt mit `html`) oder `erinnerung`. Aufgabenstellungen beginnen mit einem **Operator** (nenne, berechne, ordne zu, bilde den Buchungssatz …). **Alle nötigen Werte stehen im selben Schritt** (`material`). Bei MC zu jeder falschen Antwort ein `why`. Richtige Antwort darf zuerst stehen (wird gemischt).
- **BWR (Bayern):** Beträge im Text „11.900,00 €“; Konten ab Jgst. 8 mit Nummer und Kürzel („2800 BK“), **in Jgst. 7 nur Kürzel** („BK“). Gibt es die Skills `bwr-uebungsaufgaben` oder `bwr-aufgabenstellungen-afb`, deren Schreibweise und Operatoren übernehmen.
- **Datenschutz:** keine echten Namen von Schülerinnen und Schülern, keine personenbezogenen Daten.
- **Kleinigkeiten** (Tabellen, Hervorhebungen, Formel im Text) gehen über HTML. Bruch: `<span class=\"bruch\"><span>Zähler</span><span>Nenner</span></span>`.
- **Tokens sparen:** `assets/vl/` nicht lesen; Ergebnisdateien nicht in den Chat kopieren, sondern verlinken; bei eigenen Seiten nur den Kopfkommentar von `aufgaben.js`.

## Fehlender Aufgabentyp

1. **Erst umformen:** Reihenfolge → `zuordnen` mit Feldern „1.“, „2.“ …; Wahr/Falsch → `mc`; Tabelle ausfüllen → `tabelle`/`zahlen`; Begriffe nennen → `freitext`. Wenn das reicht: so umsetzen und kurz sagen.
2. **Nur für diese Übung gebraucht:** eigene Seite anbieten (Wege B und C).
3. **Für viele Übungen nützlich** (alle müssen zutreffen: läuft im Browser ohne Server · Antwort automatisch eindeutig prüfbar · keine neuen Schülerdaten · mit Daten beschreibbar · in mehreren Fächern oder Übungen nützlich): Issue in **nic0nic/vibe-learning** vorbereiten:
   - Mit GitHub-Werkzeug dort anlegen, sonst Link mit URL-kodiertem Titel und Text (unter 6000 Zeichen):
     `https://github.com/nic0nic/vibe-learning/issues/new?title=Neuer%20Aufgabentyp%3A%20…&body=…`
   - Inhalt: **Wofür** (Fach, Jgst., Beispiel) · **Bedienung** · **Prüfregel** · **Vorschlag für die Daten** (kleines JSON) · Ergebnis der Prüfung.
   - Hinweis: Zum Absenden braucht die Lehrkraft ein (kostenloses) GitHub-Konto; bis dahin vorhandene Typen oder eine eigene Seite.
4. **Sonst:** in 1–2 Sätzen begründen und die beste Lösung mit vorhandenen Typen anbieten.
