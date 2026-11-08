---
name: "bwr-uebungsaufgaben"
description: 'Erstellt Übungsaufgaben (Angabe + Lösung) für Betriebswirtschaftslehre/Rechnungswesen (BwR) an bayerischen Realschulen, konform mit der ISB-Handreichung "Leistungskorrektur/Leistungsbewertung im Fach BwR". Diesen Skill IMMER nutzen bei Wiederholungsaufgaben, Übungsblättern, Buchungssatz-Aufgaben, Belegen (Rechnung, Gutschrift, Kontoauszug, Gehaltsliste, Gebührenbescheid), Skontoschemata oder Lösungsvorschlägen mit Punktevergabe für BwR/Rechnungswesen - auch wenn "Handreichung", "Punkteschema" oder "Operator" nicht explizit genannt werden. Der Skill legt fest, wie Angabe und Lösung strukturiert werden, wie Buchungssätze formatiert und bepunktet werden (Skontoschema-Punkte über bwr-bewertung-musterloesung) und welche Operatoren für Aufgabenstellungen zu verwenden sind.'
---

# BwR-Übungsaufgaben erstellen (Bayern, Realschule)

Dieser Skill fasst zusammen, wie Übungsaufgaben für BwR/Rechnungswesen so erstellt werden, dass sie fachlich korrekt formuliert und exakt nach der ISB-Handreichung bepunktet sind. Er basiert auf einer iterativen Abstimmung mit einer Lehrkraft anhand konkreter Aufgabenbeispiele – die hier festgehaltenen Regeln sind keine Vermutungen, sondern bestätigte Konventionen.

## 1. Grundstruktur einer Übungsreihe

- **Ein fiktives Unternehmen** für die gesamte Aufgabenreihe (Name, Ort, Branche), damit alle Übungen zusammenhängen und Zahlen wiederverwendet werden können (z. B. Kontodaten einer Person in mehreren Übungen).
- **Je Übung zwei getrennte Dateien**: `Angabe.md` (was die Schüler bearbeiten) und `Lösung.md` (Lösungsvorschlag mit Punkten). Nie in einer Datei mischen.
- **Kontenplan**: Industriekontenrahmen (IKR) in der für bayerische Realschulen zugelassenen Fassung verwenden. Kontonummer **und** Kurzbezeichnung immer gemeinsam angeben (z. B. „4400 VE").
- **Belege als eigene Dateien**, keine Zahlen nur im Fließtext der Angabe verstecken, wenn ein echtes Dokument sinnvoller ist:
  - Reale Dokumente (Rechnung, Gutschrift, Kontoauszug, Gehaltsliste, Gebührenbescheid) → als HTML-Datei im Stil eines echten Geschäftsbriefs/Kontoauszugs erstellen. Die Lehrkraft öffnet die Datei im Browser, screenshottet sie und fügt den Screenshot an der markierten Stelle in die Angabe ein.
  - Diagramme/Schaubilder (z. B. Wirtschaftskreislauf) → als SVG erstellen (Vektorgrafik, verlustfrei druckbar, direkt einfügbar – kein Screenshot nötig).
  - In der Angabe an der richtigen Stelle einen Platzhalter setzen: `*(Beleg X hier einfügen)*`.
  - Eine `TODO_Belege.md` führen: welcher Beleg gehört in welche Angabe-Datei, an welche Aufgabe.

## 2. Design-Prinzipien für Aufgaben

Diese Prinzipien wurden aus konkreten Korrekturen abgeleitet und sind zentral für gute Übungsaufgaben:

- **Schüler sollen möglichst selbst rechnen, statt fertige Werte zu bekommen.** Wo ein Wert aus dem Beleg oder aus einer vorherigen Aufgabe ableitbar ist, wird er nicht direkt vorgegeben.
  - Schlecht: „Der Nettowert der Rücksendung beträgt 800,00 €."
  - Gut: Der Beleg zeigt den Stückpreis; die Schüler berechnen den Rücksendewert selbst aus Menge × Preis.
  - Schlecht: „Listeneinkaufspreis: 12.500,00 €"
  - Gut: „1.250 Meter à 10,00 €" – erfordert eine Nebenrechnung (Menge × Preis), bevor das eigentliche Kalkulationsschema beginnt.
- **Realistische Bedingungen statt vorweggenommener Ergebnisse.** Bei Skontofragen z. B. ein konkretes Zahlungsdatum angeben, sodass die Schüler selbst prüfen müssen, ob die Skontofrist überhaupt noch läuft, statt ihnen „es werden X % Skonto gewährt" vorzusetzen. Das prüft echtes Verständnis (Fristenkontrolle) statt reines Nachrechnen.
- **Keine Angaben, die die Lösung vorwegnehmen.** Eine Zuordnungs- oder Lückenaufgabe verliert ihren Sinn, wenn die Begriffsliste in der Angabe bereits exakt die Lösung ist. Bei Diagrammaufgaben (z. B. Wirtschaftskreislauf) nur die Kennbuchstaben zeigen, nicht zusätzlich die passenden Begriffe auflisten.
- **Aufgaben so konzipieren, dass Teilaufgaben möglichst unabhängig lösbar sind** (siehe Folgefehler-Regel in Abschnitt 6) – sonst lässt sich ein Fehler in Teilaufgabe 1 nicht sauber von Teilaufgabe 2 trennen.
- **Kurze, einzeilige Übungstitel** (z. B. „Wdh. 8. Jgst. – Übung 1: Einkauf mit Kalkulation" statt eines mehrzeilig umbrechenden Titels).

## 3. Angabe.md – Konventionen

- **Keine Punkteangaben** – weder pro Aufgabe noch als Gesamtpunktzahl am Anfang. Punkte gehören ausschließlich in die Lösung; eine Gesamtpunktzahl in der Angabe veraltet sofort, sobald sich an den Aufgaben etwas ändert, und wird leicht vergessen zu aktualisieren.
- Aufgabenstellungen **ausschließlich mit Operatoren aus dem Operatorenkatalog** formulieren (siehe Abschnitt 7 / `references/operatorenkatalog.md`), nicht mit umgangssprachlichen Fragen („Was ist...?", „Wie funktioniert...?").
- Wo ein Beleg die Datengrundlage liefert, den Platzhalter `*(Beleg X hier einfügen)*` direkt über der zugehörigen Aufgabe setzen.
- Ergebnis-Alternativen ausdrücklich zulassen, wo sinnvoll (z. B. „... oder zeichne alternativ den kompletten Wirtschaftskreislauf in dein Heft").

## 4. Lösung.md – Konventionen

### Buchungssätze

- Immer in einem Codeblock (monospace), damit Kontonummer, Komma und Eurozeichen untereinanderstehen.
- Soll-Konten zuerst, dann `an`, dann Haben-Konten. `an` markiert immer den Übergang von der letzten Soll-Zeile zur ersten Haben-Zeile – unabhängig davon, welche Seite mehr Konten hat (auch bei mehreren Konten auf beiden Seiten). Weitere Konten einer Seite folgen bündig darunter, ohne „an" zu wiederholen.
- Reihenfolge der Konten innerhalb einer Seite folgt dem Beleg (Hauptkonto → Nebenkosten → Steuerkonto), nicht dem Alphabet oder der Kontonummer.
- **Nie einen Schrägstrich (/) statt „an"** verwenden – für Schüler ist „an" die klarere Verbindung zwischen Soll und Haben.
- Stornobuchungen (Rücksendung u. Ä.) werden durch Vertauschen von Soll und Haben mit denselben, weiterhin positiven Beträgen dargestellt – kein Minuszeichen.
- Punktenotation: Die Punktzahl steht als `(N)` direkt am Ende der letzten Zeile des Buchungssatzblocks (nicht als separater Fließtext „je 1 P pro Konto").
- Cent-Beträge immer mit zwei Nachkommastellen, Tausenderpunkt, Komma als Dezimaltrennzeichen, Eurozeichen **hinter** dem Betrag (z. B. `14.137,20 €`). Kaufmännisch runden (DIN 1333).
- Vollständige Syntax-Regeln inkl. aller Buchungssatz-Varianten (einfach, mehrere Soll-Konten, mehrere Haben-Konten, beide Seiten mehrfach) und Beispielen: `references/buchungssatz-syntax.md`.

### Grundprinzip der Punktevergabe

Ein Punkt pro **Konto** (Kontonummer + Bezeichnung + Betrag als untrennbare Einheit) im Buchungssatz. Zusätzlich ein Punkt für jeden **gesondert zu berechnenden Betrag**, der nicht direkt aus einem gegebenen Netto- oder Bruttowert folgt (Ausnahme: reine Brutto-Netto-Umrechnung ab der 8. Jahrgangsstufe – dafür gibt es **keinen** Punkt mehr). Details und die vollständige Punktevergabe-Tabelle: `references/korrekturprinzipien.md`.

### Skontoschema

Vor dem Bepunkten eines Skontoschemas den Skill `bwr-bewertung-musterloesung` laden und `references/punktevergabe_grundregeln.md`, Abschnitt 7.1, anwenden.

## 5. Belege

- **Standard: Beleg als eigene HTML-Datei**, die Lehrkraft macht einen Screenshot und fügt ihn als Bild an der Platzhalterstelle ein (Größe im Dokument frei veränderbar).
- **Option (nur auf Wunsch): Beleg direkt als HTML in die Angabe eingebettet** (eigene Datei `…_Angabe_Belege_eingebettet.md`, die Fassung mit Platzhaltern bleibt erhalten). Regeln in `references/belege_eingebettet.md`.
- HTML-Belege im Stil eines echten Dokuments (Briefkopf, Tabelle, Zahlungsbedingungen/Hinweis) – keine verspielte Gestaltung, Belege sollen wie echte Geschäftsdokumente aussehen.
- Realistische Details verwenden (Rechnungsnummer, IBAN, Steuersatz), aber keine echten Firmen/Personen.
- Sachlich korrekt bei Steuerfragen bleiben: hoheitliche Gebühren (z. B. Müllgebühren einer Stadt) sind i. d. R. **nicht** umsatzsteuerpflichtig (Konto 6730 GEB ohne 2600 VORST); Kontoführungsgebühren einer Bank sind Kosten des Geldverkehrs (6750 KGV), nicht „Gebühren" (6730 GEB) – beide Fälle sauber auseinanderhalten, je nachdem, was die Aufgabe abfragen soll.
- Diagramme (Wirtschaftskreislauf o. Ä.) als SVG: Knoten als Boxen, Pfeile mit Marker-Arrowheads, Kennbuchstaben in kleinen Kreisen an den Pfeilen platzieren. Vor dem Einfügen in die Angabe kurz als PNG rendern und optisch prüfen (Überschneidungen, Lesbarkeit), z. B. mit `cairosvg`.

## 6. Weitere Korrekturprinzipien (Kurzfassung)

- **Keine negative Punktzahl.** Minimal 0 Punkte je (Teil-)Aufgabe, auch bei mehreren Fehlern.
- **Folgefehler:** Baut eine Teilaufgabe zwingend auf dem (fehlerhaften) Ergebnis einer vorherigen auf, werden die Punkte für den *korrekten Rechenweg* mit dem falschen Ausgangswert trotzdem gegeben – vorausgesetzt, Teilaufgaben sind wirklich voneinander abhängig konzipiert.
- **Drehfehler** (Soll/Haben vertauscht): 0 Punkte für den Buchungssatz, unabhängig von richtigen Beträgen. Kein "Korrigieren" durch Doppelpfeil zulässig.
- **Geschäftsfall nicht erfasst** (falsches Konto-Set, grundlegend falscher Ansatz): mit „NE" kennzeichnen, 0 Punkte für den betroffenen Teil.
- **Geringfügige Abweichungen** (Rundungsfehler, Übertragungsfehler, falsche Kontobezeichnung bei richtiger Nummer o. ä.): Abzug von 0,5 Punkten möglich, kein Totalausfall des Punktes.
- **Nicht geforderte, aber zusätzlich gebildete Buchungssätze/Konten:** echter Punktabzug (z. B. „– 1 P: nicht gefordert"), nicht nur „kein Punkt".
- **Fehlende Nebenrechnung, aber richtiger Betrag im Buchungssatz:** Punkt für die Nebenrechnung entfällt, Kontopunkte bleiben. Fehlt die Nebenrechnung **und** ist der Betrag falsch: auch die Kontopunkte für diesen Betrag entfallen.
- Details, Tabellen und Beispiele: `references/korrekturprinzipien.md`.

## 7. Operatorenkatalog

Aufgaben werden ausschließlich mit den Operatoren aus der Handreichung formuliert – sie signalisieren den Schülern eindeutig, welche Art und welchen Umfang von Antwort erwartet wird:

- **Anforderungsbereich I (Reproduktion):** z. B. angeben, aufzählen, beschreiben, definieren, einordnen, nennen, vervollständigen, zuordnen – Wiedergabe ohne eigene Erklärung/Begründung.
- **Anforderungsbereich II (Reorganisation):** z. B. abgrenzen, begründen, erklären/erläutern, ermitteln/berechnen/den Buchungssatz bilden/im Konto buchen, prüfen, vergleichen – erfordert selbstständiges Anwenden, Erklären oder Entscheiden.

Wichtige Operator-eigene Punkteregeln (siehe vollständige Tabelle in `references/operatorenkatalog.md`):

| Operator | Punkteregel |
|---|---|
| abgrenzen / unterscheiden | 1 P je Sachverhalt/Begriff, der abgegrenzt wird |
| begründen | i. d. R. in Kombination mit einer Entscheidung: 1 P Entscheidung + 1 P Begründung |
| vergleichen | 1 P je genanntem Merkmal |
| ermitteln / berechnen / den Buchungssatz bilden / im Konto buchen | Ergebnisorientiert: je Konto bzw. je gesondert zu berechnendem Betrag 1 P (siehe Abschnitt 4) |

Vor dem Formulieren jeder neuen Aufgabe: `references/operatorenkatalog.md` konsultieren und den passenden Operator (nicht nur ein ähnliches Wort) wählen – das bestimmt direkt, wie die Aufgabe später bepunktet wird.

## 8. Checkliste vor Fertigstellung

1. Angabe enthält keine Punkteangaben.
2. Jede Aufgabenstellung beginnt mit einem Operator aus dem Katalog.
3. Kein vorgegebener Wert, der von den Schülern selbst hätte berechnet werden können.
4. Buchungssätze: „an", nicht „/"; Konto+Betrag als Block; Punktzahl als „(N)" am Zeilenende in der Lösung.
5. Skontoschema-Punkte nach `bwr-bewertung-musterloesung`, `punktevergabe_grundregeln.md` Abschnitt 7.1.
6. Nebenrechnung vorhanden, wo laut `references/korrekturprinzipien.md` Pflicht.
7. Belege: HTML für Screenshot-Dokumente (eingebettet nur auf Wunsch), SVG für Diagramme; TODO-Liste aktuell; steuerliche Behandlung des Belegs sachlich korrekt.
8. Gesamtpunktzahl der Lösung ist die Summe der tatsächlich vergebenen Teilpunkte (nach jeder inhaltlichen Änderung neu prüfen).
