# Aufgabentypen von vibe learning (Stand: lib/aufgaben.js, November 2026)

Alle Typen kennen zusätzlich: `nr`, `frage`, `erinnerung`, `erinnerungZu`, `material`, `ok` (Text bei Erfolg). Mehrere Aufgaben, die nacheinander erscheinen sollen: Typ `kombi` (unten).
Vollständiges Beispiel einer Reihe: `beispiel.json`.
Formel mit Bruchstrich in jedem HTML-Text: `<span class=\"bruch\"><span>Restschuld · Zinssatz</span><span>100</span></span>`.

## mc – Multiple Choice
`options` (Texte), `correct` (Indizes ab 0; mehrere = Mehrfachauswahl), `why` (Erklärung je falscher Antwort, Schlüssel = Index als Text), `after` (Text nach Erfolg). Optional `multi: true` (Mehrfachauswahl, auch wenn nur eine richtig ist), `mischen: false` (Reihenfolge behalten, z. B. bei „alle …“). Antworten sind reiner Text (ein `<` bleibt ein `<`). Für Brüche oder Formatierung in den Antworten `"html": true` setzen, dann sind sie HTML wie die anderen Texte, z. B. `{"typ": "mc", "html": true, "options": ["<span class=\"bruch\"><span>1</span><span>3</span></span>", "…"], …}`.
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
**Szenario (verzweigter Chat):** alles optional, alte Chats laufen unverändert. Eine Nachricht als Objekt kann `"id": "kredit"` (Sprungziel), `"weiter": "id"` (danach dorthin statt zur nächsten) und `"ende": true` (Chat endet hier) haben; reiner Text mit Marke: `{"bot": "…", "id": "kk"}`. Antwort-Knöpfe können `"weiter": "id"` oder `"ende": true` haben (gilt vor `weiter`/`ende` der Frage). Hat kein Knopf `"ok": true`, ist die Frage eine **Entscheidung**: Sie zählt nicht als Frage, `r` erscheint neutral (dafür `weiter` an den Knöpfen oder `"entscheidung": true` an der Frage). Jeder Zweig braucht ein Ende: letzte Nachricht des Zweigs mit `"ende": true` oder `"weiter"` zu einem gemeinsamen Schluss.
```json
{"typ": "chat", "name": "Bankberaterin", "bild": "🏦", "nachrichten": ["Du brauchst 5.000 € für eine Maschine.",
  {"bot": "Wie finanzierst du?", "antworten": [{"t": "Kontokorrent", "weiter": "kk"}, {"t": "Darlehen", "weiter": "dar"}]},
  {"id": "kk", "bot": "Der Kontokorrentkredit ist flexibel, aber teuer."},
  {"bot": "Passt er zu einer Maschine?", "antworten": [{"t": "ja", "r": "Nein, er ist kurzfristig."}, {"t": "nein", "ok": true, "r": "Genau."}], "weiter": "schluss"},
  {"id": "dar", "bot": "Ein Darlehen passt zur langen Nutzung."},
  {"bot": "Wie hoch sind die Zinsen bei 4 % im ersten Jahr?", "zahl": {"l": 200, "e": "€"}, "rFalsch": "5.000 € · 4 : 100 = 200 €"},
  {"id": "schluss", "bot": "Damit ist die Finanzierung geklärt.", "ende": true}]}
```
```json
{"typ": "chat", "name": "BWR-Coach", "bild": "🧑‍🏫", "nachrichten": ["Wir buchen einen Verkauf.", {"bot": "Wird das Bankkonto mehr oder weniger?", "antworten": [{"t": "mehr", "ok": true, "r": "Genau!"}, {"t": "weniger", "r": "Nein, der Kunde überweist uns Geld."}]}, {"bot": "Welcher Betrag?", "zahl": {"l": 11900, "e": "€"}, "r": "Richtig!", "rFalsch": "10.000,00 € + 19 % = 11.900,00 €."}]}
```

## buchungssatz – Buchungssatz bilden
`konten` (Auswahlliste, auch Ablenker), `soll` / `haben`: `[["Konto", Betrag], …]` (Konto aus `konten`, Soll = Haben), `steuer` (Steuerkonten für den Hinweis „Denke an …“), `nebenrechnung` (HTML, wird nach Lösung gezeigt), `betraege` (optional: `[["Rechnungsbetrag", 11900], ["", 238], …]` – Beträge zum Ziehen, Bezeichnung darf leer sein auf die Betragsfelder, auch Ablenker; passt als Teil 2 einer `kombi` nach einer Rechenaufgabe), `jgst: 7` (optional: 7. Jahrgangsstufe, Konten nur mit Kürzel ohne Nummer, z. B. `["BK", "UEFE", "UST"]`). Die Schüler suchen Konten per Nummer oder Kürzel; „an“ steht wie im Heft auf der Zeile des letzten Soll-Kontos. Prüft Konten, vertauschtes Soll/Haben, fehlende Steuer, Beträge.
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

## kombi – Kombinierte Aufgabe (Teile nacheinander)
`teile`: Liste von mindestens zwei Aufgaben beliebigen Typs (keine `kombi` darin). Teil 2 erscheint erst, wenn Teil 1 richtig gelöst ist, Teil 3 nach Teil 2 usw. Die Kombi kann selbst `nr`, `frage` (Einleitung über allen Teilen), `erinnerung`, `material` und `ok` (wenn alle Teile gelöst sind) haben; jeder Teil hat zusätzlich seine eigenen. Typisch: erst rechnen, dann buchen (Beträge der Rechnung als `betraege`), dann Handlungsempfehlung (mc). Das frühere `danach` an einer Aufgabe wird noch gelesen, ist aber veraltet.
```json
{"typ": "kombi", "nr": "7.3", "teile": [
  {"typ": "zahlen", "frage": "Berechne Bruttoskonto und Überweisungsbetrag.", "felder": [{"t": "Bruttoskonto", "l": 238, "e": "€"}, {"t": "Überweisungsbetrag", "l": 11662, "e": "€"}]},
  {"typ": "buchungssatz", "frage": "Buche die Zahlung mit Skonto.", "konten": ["2600 VORST", "2800 BK", "4400 VE", "6002 NR"],
   "soll": [["4400 VE", 11900]], "haben": [["2800 BK", 11662], ["6002 NR", 200], ["2600 VORST", 38]], "steuer": ["2600 VORST"],
   "betraege": [["Rechnungsbetrag", 11900], ["Bruttoskonto", 238], ["Nettoskonto", 200], ["Steuerberichtigung", 38], ["Überweisungsbetrag", 11662]]}]}
```

## Training-Schritt – Aufgaben auf Zeit und/oder endlos (Kopfrechnen, Vokabeln)
Kein Aufgabentyp, sondern ein **Schritt** mit `"training"` statt `"aufgaben"`. Eine Aufgabe nach der anderen, Antwort eintippen (`"antwort": "eingabe"`) oder auswählen (`"mc"`, 4 Antworten, falsche automatisch).
- `anzahl`: Aufgaben pro Runde (Ergebnis + Bestleistung). **Weglassen = endlos**: ein Fehler beendet die Serie, gezählt wird die Bestleistung.
- `zeit`: `{"start": 5, "schritt": -0.1, "min": 1.5}` – Sekunden für die erste Aufgabe, Änderung je richtiger Antwort, Untergrenze. Weglassen = ohne Zeit.
- `versuche: true`: Bei einem Fehler darf man es nochmal versuchen (sonst sofort Fehler, Lösung wird gezeigt). `ziel`: so viele richtige zählen den Schritt als erledigt (Standard: Runde beendet bzw. Serie ab 10).
- Inhalt: `szenarien` (Zahlen) **oder** `woerterbuch` (Vokabeln) – oder `stufen: [{"name": "bis 20", "szenarien": […]}, {"name": "Lektion 2", "woerterbuch": {…}}]` (Flammen zum Wählen).
- Eine Stufe kann eigene `antwort` und `zeit` haben (`"zeit": null` = ohne Zeit), z. B. dieselben Aufgaben in vier Stufen: Auswählen, Auswählen auf Zeit, Eintippen, Eintippen auf Zeit.
- **Szenario**: `frage` mit `{a}` (Wert) oder `{=a*10}` (Ausdruck), `werte`: `[von, bis]`, `[von, bis, Schritt]`, `{"aus": [2, 5, 10]}` oder Formel aus früheren Werten (`"c": "a*b"`), `loesung` (Formel), optional `bedingung` (z. B. `"b <= a"`, es wird neu gewürfelt), `runden` (Nachkommastellen), `einheit`, `falsch` (typische falsche Antworten als Formeln, für mc). Formeln: `+ - * / ( ) ^`, Vergleiche, `und`/`oder`, `runden(x, 2)`, `abs`, `min`, `max`, `wurzel`, `ganz`, `rest`; Kommazahlen mit Punkt.
- **Wörterbuch**: `sprachen` (zwei Namen), `richtung` `"a-b"` | `"b-a"` | `"beide"`, `eintraege` `[["house", "Haus|Gebäude"], …]` (`|` = mehrere richtige Antworten), `tippfehler: true` (fast richtig zählt). Für mc mindestens 4 Einträge.
```json
{"kurz": "Kopfrechnen", "titel": "Addition bis 20", "html": "<p>Rechne so schnell du kannst.</p>",
 "training": {"antwort": "eingabe", "anzahl": 20, "zeit": {"start": 5, "schritt": -0.1, "min": 1.5},
   "stufen": [{"name": "bis 10", "szenarien": [{"frage": "{a} + {b} =", "werte": {"a": [0, 10], "b": [0, 10]}, "bedingung": "a + b <= 10", "loesung": "a + b"}]},
              {"name": "bis 20", "szenarien": [{"frage": "{a} + {b} =", "werte": {"a": [1, 19], "b": [1, 19]}, "bedingung": "a + b <= 20", "loesung": "a + b"},
                                                {"frage": "{a} − {b} =", "werte": {"a": [2, 20], "b": [1, 20]}, "bedingung": "b <= a", "loesung": "a - b", "falsch": ["a + b"]}]}]}}
```
```json
{"kurz": "Vokabeln", "titel": "Unit 3", "training": {"antwort": "mc", "woerterbuch": {"sprachen": ["Englisch", "Deutsch"], "richtung": "beide",
   "eintraege": [["house", "Haus"], ["to go", "gehen"], ["tired", "müde"], ["cheese", "Käse"], ["bird", "Vogel"]]}}}
```
Im Editor („Übung erstellen“): Baustein „⏱ Training“; Vokabeln lassen sich aus Excel/CSV/Quizlet/Anki importieren.


# Experimentelle Typen (Branch `beta` von vibe learning)

Diese Typen gibt es bisher nur im Branch `beta` (noch nicht auf vl.nimals.de). Format und Bedienung können sich noch ändern – der Lehrkraft das dazusagen. Im Editor stehen sie unter „Experimentell (β)“. Reiner Text heißt: kein HTML, ein `<p>` wird als Zeichen angezeigt (gut für Code).

## reihenfolge – Karten ordnen
`karten`: Texte in der **richtigen** Reihenfolge (HTML erlaubt), werden gemischt. Ziehen, ▲ ▼ oder antippen. `"mono": true` → reiner Text in Schreibmaschinenschrift, Einrückung bleibt (Codezeilen ordnen). `h` (Hinweis bei Fehler). Gleiche Texte sind austauschbar.
```json
{"typ": "reihenfolge", "frage": "Ordne das Kalkulationsschema.", "karten": ["Listeneinkaufspreis", "− Liefererrabatt", "= Zieleinkaufspreis", "− Liefererskonto", "= Bareinkaufspreis"]}
```

## offen – freie Antwort mit Selbstkontrolle (AFB II/III)
`muster` (Musterlösung, HTML), `kriterien` (Liste zum Abhaken, optional), `zeilen` (Höhe des Textfelds, Standard 5), `min` (Mindestzahl Zeichen). Ablauf: schreiben → „Musterlösung zeigen“ → Kriterien abhaken → abschließen. Gilt dann als gelöst, unabhängig von den Haken; nichts wird automatisch bewertet oder gespeichert.
```json
{"typ": "offen", "frage": "Begründe, warum ein Unternehmen Skonto nutzen sollte.", "min": 20, "muster": "<p>Skonto ist ein Preisnachlass für schnelle Zahlung. Wer darauf verzichtet, nimmt einen sehr teuren Lieferantenkredit in Anspruch.</p>", "kriterien": ["nennt den Preisnachlass", "vergleicht mit einem Kredit"]}
```

## markieren – Stellen im Text anklicken
`text` (reiner Text, Zeilen mit `\n`): gesuchte Stellen in `[[…]]`. Angeklickt werden Wörter (Satzzeichen nicht; mehrere Wörter in einer Klammer zusammen) oder mit `"einheit": "zeile"` ganze Zeilen (gesucht ist jede Zeile, in der `[[` vorkommt). `"mono": true` (Code, Trennung nur an Leerzeichen), `"anzahl": false` (Anzahl nicht verraten), `h`.
```json
{"typ": "markieren", "frage": "Markiere alle Aufwandskonten.", "text": "Auf dem Tisch liegen Belege zu [[AWR]], BK, [[AWF]], UEFE und [[AWB]]."}
```

## verbessern – Fehler finden und verbessern
`text` (reiner Text, Zeilen mit `\n`) mit Fehlern `[[falsch|richtig|auch richtig]]` – **das Falsche zuerst** (wird angezeigt), danach die erlaubten Verbesserungen; `[[zu viel|]]` = Stelle löschen. Ablauf je Fehlerzeile: Zeile anklicken → alle falschen Stellen anklicken (nochmal = abwählen) → verbessern. Bei nur einer Zeile entfällt die Zeilenwahl. Stellen sind Wörter (durch Leerzeichen getrennt) und die Klammern, ein Fehler mitten im Wort also als eigene Klammer: `Titel[[</h2>|</h1>]]`. `"mono": true` (Code), `"gross": false` (Groß/klein egal), `h`.
```json
{"typ": "verbessern", "mono": true, "frage": "Finde und verbessere die Fehler.", "text": "<h1>Mouse Rat[[</h2>|</h1>]]\n<p>Die Band aus Pawnee</p>\n<img [[scr|src]]=\"band.jpg\">"}
```

## beschriften – Begriffe auf ein Bild ziehen
`bild`: eingebettet als `data:image/png|jpeg|gif|webp|svg+xml;base64,…` (höchstens 600 kB, zählt nicht zu den 150 kB; SVG mit `width` und `height`), `alt` (Bildbeschreibung), `punkte`: `[{"x": 25, "y": 40, "t": "Begriff"}]` (x, y in Prozent von links/oben), `extra` (Ablenker). Im Chat am einfachsten ein kleines SVG selbst zeichnen und mit base64 einbetten; im Editor lädt die Lehrkraft ein Bild hoch und klickt die Punkte an.

## bloecke – Blöcke zu Formel oder Ablauf zusammensetzen
`bloecke` (Vorrat, reiner Text, auch Ablenker; beliebig oft nutzbar, `"einmal": true` = jeder nur einmal), `loesung` (Blöcke in der richtigen Reihenfolge) oder `loesungen` (mehrere Listen), `start` (fester Text davor, z. B. `"Z ="`), `"gleichwertig": true` → jede rechnerisch gleichwertige Formel zählt (Blöcke werden mit `· : + − ( )` und Zahlen gerechnet, Buchstaben sind Größen), `"senkrecht": true` (untereinander, für Programmzeilen), `"mono": true`, `h`.
```json
{"typ": "bloecke", "frage": "Baue die Zinsformel.", "start": "Z =", "gleichwertig": true, "bloecke": ["K", "p", "t", "·", ":", "(", ")", "100", "360", "+"], "loesung": ["K", "·", "p", "·", "t", ":", "(", "100", "·", "360", ")"]}
```

## karteikarten – umdrehen und selbst einschätzen
`karten`: `[{"v": "Vorderseite", "r": "Rückseite"}]` (HTML), `"mischen": false`. „Gewusst“ / „Nicht gewusst“ – nicht gewusste Karten kommen wieder; gelöst, wenn alle gewusst sind.
```json
{"typ": "karteikarten", "frage": "Lerne die Begriffe.", "karten": [{"v": "Disagio", "r": "Abschlag vom Kreditbetrag"}, {"v": "Tilgung", "r": "Rückzahlung des Kredits"}]}
```

## kreuzwort – Kreuzworträtsel
`woerter`: `[{"w": "Bilanz", "t": "Hinweis"}]` (2 bis 25 Wörter, je 2 bis 20 Buchstaben A–Z, Ä, Ö, Ü; ß wird SS, Leerzeichen und Bindestriche entfallen). Das Gitter entsteht von selbst. Wörter mit gemeinsamen Buchstaben wählen, sonst stehen sie einzeln darunter. Sparsam einsetzen: viel Zeit, wenig Lernertrag.
```json
{"typ": "kreuzwort", "frage": "Löse das Rätsel.", "woerter": [{"w": "Bilanz", "t": "Gegenüberstellung von Vermögen und Kapital"}, {"w": "Inventur", "t": "Bestandsaufnahme"}, {"w": "Aktiva", "t": "linke Seite der Bilanz"}]}
```
