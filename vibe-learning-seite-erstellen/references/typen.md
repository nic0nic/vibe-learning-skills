# Aufgabentypen von vibe learning (Stand: lib/aufgaben.js, November 2026)

Alle Typen kennen zusätzlich: `nr`, `frage`, `erinnerung`, `erinnerungZu`, `material`, `ok` (Text bei Erfolg), `danach` (Folgeaufgabe).
Vollständiges Beispiel einer Reihe: `beispiel.json`.
Formel mit Bruchstrich in jedem HTML-Text: `<span class=\"bruch\"><span>Restschuld · Zinssatz</span><span>100</span></span>`.

## mc – Multiple Choice
`options` (Texte), `correct` (Indizes ab 0; mehrere = Mehrfachauswahl), `why` (Erklärung je falscher Antwort, Schlüssel = Index als Text), `after` (Text nach Erfolg). Optional `multi: true` (Mehrfachauswahl, auch wenn nur eine richtig ist), `mischen: false` (Reihenfolge behalten, z. B. bei „alle …“).
Bei genau einer richtigen Antwort wird beim Antippen sofort geprüft.
```json
{"typ": "mc", "frage": "Was bedeutet Kreditfähigkeit?", "options": ["rechtliche Fähigkeit, einen Kreditvertrag abzuschließen", "Fähigkeit, den Kredit zurückzuzahlen"], "correct": [0], "why": {"1": "Das ist die Kreditwürdigkeit."}}
```

## zahlen – Zahleneingabe (Formular)
`felder`: je `t` (Beschriftung), `l` (Lösung als Zahl), `e` (Einheit), `h` (Hinweis bei Fehler), `tol` (Toleranz, Standard 0.005). Eingaben wie „11.900,00 €“ werden verstanden. Optional `knopf` (Text des Prüfknopfs).
```json
{"typ": "zahlen", "frage": "Berechne das Disagio und den Auszahlungsbetrag.", "felder": [{"t": "Disagio", "l": 1000, "e": "€", "h": "Kreditbetrag · 2 : 100"}, {"t": "Auszahlungsbetrag", "l": 49000, "e": "€"}]}
```

## luecken – Lückentext mit Auswahllisten oder Wortbank
`text` mit Lücken `[[richtig|falsch|falsch]]` – die **erste** Antwort ist richtig (Anzeige gemischt). HTML im Text erlaubt (`<br>`, `<b>`).
```json
{"typ": "luecken", "frage": "Vervollständige.", "text": "Der Kontokorrentkredit ist [[kurzfristig|langfristig]] und vergleichsweise [[teuer|günstig]]."}
```
**Wortbank zum Ziehen** statt Auswahllisten: `"ziehen": true`. Die Bank enthält je Lücke das richtige Wort, die falschen Antworten aller Lücken und `extra` (weitere Ablenker, optional). `[[Wort]]` ohne `|` reicht hier.
```json
{"typ": "luecken", "ziehen": true, "frage": "Ziehe die Wörter in die Lücken.", "text": "Die Bank prüft die [[Kreditwürdigkeit]] und verlangt [[Sicherheiten|Skonto]].", "extra": ["Rabatt"]}
```

## zuordnen – Karten in Felder ziehen
`felder`: `[["id", "Überschrift"], …]` (mind. 2), `karten`: `[{"t": "Text", "z": "id"}]`. Ziehen oder antippen; richtige bleiben liegen. Auch für Reihenfolgen (Felder „1.“, „2.“ …) und Paare.
```json
{"typ": "zuordnen", "frage": "Ordne zu.", "felder": [["f", "Kreditfähigkeit"], ["w", "Kreditwürdigkeit"]], "karten": [{"t": "Lea ist 17 und will ohne Eltern einen Kredit.", "z": "f"}, {"t": "Die SCHUFA meldet offene Rechnungen.", "z": "w"}]}
```

## freitext – Begriffe eingeben
`felder` (Beschriftungen, je ein Eingabefeld), `antworten`: Liste von Einträgen, jeder Eintrag = Liste gleichwertiger Schreibweisen. Ein Feld ist richtig, wenn ein Begriff darin vorkommt; jedes Feld braucht einen anderen Eintrag. Tippfehler gelten als „fast richtig“ (`"tippfehler": "ok"` zählt sie als richtig). `h` = Hinweis bei falscher Antwort.
```json
{"typ": "freitext", "frage": "Nenne zwei Sicherheiten.", "felder": ["1. Sicherheit", "2. Sicherheit"], "antworten": [["Bürgschaft"], ["Grundschuld"], ["Zession", "Abtretung von Forderungen"]]}
```

## chat – Lern-Chat (wie LearningSnacks)
`name`, `bild` (Emoji), `nachrichten`: Text (Bot spricht, HTML erlaubt) oder Frage `{"bot": "…", …}` mit **einer** Antwortform:
- `antworten`: `[{"t": "mehr", "ok": true, "r": "Genau!"}, {"t": "weniger", "r": "Nein, weil …"}]`
- `zahl`: `{"l": 11900, "e": "€"}` mit `r` (bei richtig) und `rFalsch` (Erklärung)
- `freitext`: `{"antworten": [["UST"]]}` mit `r`, `rFalsch`
Bei Fehlern erklärt der Bot und macht weiter; am Ende Punkte. Gut für Buchungssätze Schritt für Schritt.
```json
{"typ": "chat", "name": "BWR-Coach", "bild": "🧑‍🏫", "nachrichten": ["Wir buchen einen Verkauf.", {"bot": "Wird das Bankkonto mehr oder weniger?", "antworten": [{"t": "mehr", "ok": true, "r": "Genau!"}, {"t": "weniger", "r": "Nein, der Kunde überweist uns Geld."}]}, {"bot": "Welcher Betrag?", "zahl": {"l": 11900, "e": "€"}, "r": "Richtig!", "rFalsch": "10.000,00 € + 19 % = 11.900,00 €."}]}
```

## buchungssatz – Buchungssatz bilden
`konten` (Auswahlliste, auch Ablenker), `soll` / `haben`: `[["Konto", Betrag], …]` (Konto aus `konten`, Soll = Haben), `steuer` (Steuerkonten für den Hinweis „Denke an …“), `nebenrechnung` (HTML, wird nach Lösung gezeigt). Prüft Konten, vertauschtes Soll/Haben, fehlende Steuer, Beträge.
```json
{"typ": "buchungssatz", "frage": "Bilde den Buchungssatz.", "konten": ["0700 MA", "2600 VORST", "2800 BK", "4400 VE"], "soll": [["0700 MA", 40000], ["2600 VORST", 7600]], "haben": [["4400 VE", 47600]], "steuer": ["2600 VORST"], "nebenrechnung": "Vorsteuer: 40.000,00 € · 19 % = 7.600,00 €"}
```
Jgst. 7: Konten ohne Nummer, z. B. `"konten": ["BK", "UEFE", "UST", "VORST"]`.

## tabelle – Tabelle ausfüllen (z. B. Tilgungsplan, Abschreibung)
`spalten` (Spaltenköpfe), `zeilen`: je Zeile eine Liste mit genau so vielen Zellen. Text oder Zahl = vorgegeben (Zahlen werden mit 2 Nachkommastellen angezeigt, Jahreszahlen daher als Text `"1"`), `{"l": Lösung}` = Eingabefeld. Optional `einheit` (z. B. `"€"`, im Kopf ab Spalte 2), `hinweise` (`{"Spaltenindex": "Rechenregel"}`, erscheint bei Fehlern in dieser Spalte), `tol`.
```json
{"typ": "tabelle", "frage": "Vervollständige den Tilgungsplan.", "einheit": "€", "spalten": ["Jahr", "Restschuld am Jahresanfang", "Zinsen (5 %)", "Tilgung", "Rate", "Restschuld am Jahresende"], "zeilen": [["1", 40000, {"l": 2000}, 10000, {"l": 12000}, {"l": 30000}], ["2", {"l": 30000}, {"l": 1500}, 10000, {"l": 11500}, {"l": 20000}]], "hinweise": {"2": "Zinsen = Restschuld am Jahresanfang · 5 : 100", "4": "Rate = Zinsen + Tilgung"}}
```

## wahrheit – ja/nein-Tabelle (z. B. Wahrheitstabelle UND/ODER)
`spalten` (Spaltenköpfe, HTML erlaubt), `zeilen`: je Zeile genau so viele Zellen. `true`/`false` = vorgegeben (wird als „ja“/„nein“ angezeigt), Text oder Zahl = vorgegeben, `{"l": true}` bzw. `{"l": false}` = Feld zum Anklicken (leer → ja → nein → ja …). Optional `werte` (zwei Wörter statt `["ja", "nein"]`, z. B. `["WAHR", "FALSCH"]`), `hinweise` (`{"Spaltenindex": "Regel"}`, erscheint bei Fehlern in dieser Spalte).
```json
{"typ": "wahrheit", "frage": "Fülle die Tabelle für UND und ODER aus.", "spalten": ["Bedingung 1", "Bedingung 2", "UND", "ODER"], "zeilen": [[true, true, {"l": true}, {"l": true}], [true, false, {"l": false}, {"l": true}], [false, true, {"l": false}, {"l": true}], [false, false, {"l": false}, {"l": false}]], "hinweise": {"2": "UND: nur ja, wenn beide erfüllt sind.", "3": "ODER: ja, sobald eine erfüllt ist."}}
```
