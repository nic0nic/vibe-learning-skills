---
name: "typora-arbeitsblatt-layout"
description: "Setzt Antwortfelder (Linien/Kästchen) und Seitenumbrüche in Markdown-Arbeitsblätter und Leistungsnachweise für Typora mit dem pruefung.css-Theme. Nur Layout, kein Inhalt."
---

# Typora-Arbeitsblatt-Layout

Ziel: Aus vorhandenen Aufgaben ein druckfertiges Typora-Markdown machen, mit passend großen Schreibfeldern und sinnvollen Seitenumbrüchen. **Nur Layout.** Aufgabentexte, Punkte und Reihenfolge werden nicht verändert, gekürzt oder ergänzt. Fehlt Inhalt, wird nichts erfunden: Ein Platzhalter `<!-- TODO: … -->` bleibt stehen.

Ausgabe: eine `.md`-Datei, die mit dem Theme `pruefung.css` in Typora gerendert wird.

## Bausteine (pruefung.css)

| Baustein | Code | Höhe pro Einheit |
|---|---|---|
| Schreiblinien | `<div class="lines-N"></div>` | 10,6 mm (2,5em) |
| Enge Linien | `<div class="lines-sm-N"></div>` | 6,8 mm (1,6em) |
| Karo 5 mm | `<div class="grid-N"></div>` | 5 mm (+ Abschlusslinie) |
| Seitenumbruch | `<div style="page-break-after: always; break-after: page;"></div>` | – |

`N` liegt zwischen 1 und 40. Andere Klassen gibt es nicht, also keine erfinden (z. B. kein `grid-50`, kein `box-`). Wird mehr gebraucht, zwei Felder untereinander setzen.

### Typora-Syntaxregeln

- Jedes `<div>` steht **allein auf einer Zeile** und hat davor und danach **eine Leerzeile**. Sonst behandelt Typora es als Inline-HTML oder zieht den folgenden Markdown-Text mit hinein.
- Kein Inhalt zwischen `<div …>` und `</div>`.
- Ein Seitenumbruch steht nie am Dokumentende, sonst entsteht eine leere letzte Seite.
- Ein Seitenumbruch steht nie direkt vor einer Überschrift, auf die nichts folgt.

## Feldtyp wählen

| Aufgabenart | Feld |
|---|---|
| Buchungssätze, Schemata (Kalkulation, Abschreibung, Bilanz, GuV …), Rechnungen, T-Konten, Tabellen zum Selberzeichnen, Skizzen | `grid-N` |
| Textantworten (beschreiben, erläutern, begründen, beurteilen) | `lines-N` |
| Kurze Stichworte, Einzelwerte, Aufzählungen (nennen) | `lines-sm-N` |
| Ankreuzen, Zuordnen, Lückentext im Text, Tabelle zum Ausfüllen vorgegeben | kein Feld (Tabelle/Checkboxen direkt in Markdown) |

Wenn die Lehrkraft einen Feldtyp vorgibt, gilt ihre Vorgabe.

## Feldgröße bestimmen

Die Größe richtet sich nach dem **Umfang der erwarteten Lösung**, nicht nach der Punktzahl. Deshalb zuerst intern die Lösung skizzieren (sie wird nicht ausgegeben) und dann die Zeilen zählen.

### Karo: 2 Kästchen pro Zeile

Jede geschriebene Zeile der Lösung bekommt **2 Kästchenreihen**.

- **Buchungssatz:** Jede Kontozeile (Soll- und Habenkonten einzeln gezählt) ist eine Zeile.
  - `Bank an Kasse`: 2 Zeilen, also `grid-4`
  - `Maschinen / Vorsteuer an Verbindlichkeiten`: 3 Zeilen, also `grid-6`
  - Mehrere Buchungssätze in einer Aufgabe: Zeilen addieren, dazu 1 Leerzeile (2 Kästchen) zwischen den Sätzen.
  - Ist eine Nebenrechnung nötig (z. B. Brutto zu Netto: Netto, USt), deren Rechenzeilen ebenfalls × 2.
- **Schema:** Jede Schemazeile ist eine Zeile, einschließlich Zwischen- und Endsummen. Beispiel Handelskalkulation mit 12 Schemazeilen: `grid-24`.
- **Rechnung:** Jeder Rechenschritt ist eine Zeile.
- **T-Konto:** Kopfzeile + Anzahl der Buchungen auf der längeren Seite + Summenzeile, je × 2.
- **Reserve:** +2 Kästchen (1 Zeile) pro Feld. Bei langen Schemata (über 10 Zeilen) +4.

Formel: `N = 2 × Lösungszeilen + Reserve`. Ergibt das mehr als 40, das Feld aufteilen.

### Linien

- `lines-sm`: 1 Linie pro erwartetem Stichwort oder Wert, dazu 1 Reserve.
- `lines`: Den erwarteten Antworttext abschätzen: Wie viele Aspekte bzw. Sätze verlangt der Operator? Mit ca. 1 Linie pro kurzem Satz rechnen (Schülerhandschrift: ca. 60–70 Zeichen pro Linie), dazu 1–2 Reserve.

Lieber etwas großzügiger: Handschrift von Schülern ist größer als erwartet. Nach dem ersten Druck übernimmt die Lehrkraft gemeldete Anpassungen.

## Seitenumbrüche planen

Grundsatz: Eine Aufgabe (Aufgabentext + Feld) wird nicht über eine Seite hinweg getrennt. Das CSS verhindert nur, dass ein **Feld** geteilt wird. Den Aufgabentext darüber kann es nicht festhalten. Ein Umbruch wird deshalb **vor** der Aufgabe gesetzt, die nicht mehr vollständig auf die Seite passt.

### Höhenbudget (A4, ca. 2 cm Rand ergibt ca. 255 mm nutzbare Höhe)

| Element | ca. Höhe inkl. Abstände |
|---|---|
| `#` Überschrift | 20 mm |
| `##` Überschrift | 15 mm |
| `###` Überschrift | 11 mm |
| Absatz, 1 Zeile (ca. 90 Zeichen) | 12 mm, jede weitere Zeile +7 mm |
| Listenpunkt | 7 mm |
| Tabellenzeile | 9 mm |
| `lines-N` | N × 10,6 mm |
| `lines-sm-N` | N × 6,8 mm |
| `grid-N` | N × 5 mm |

Vorgehen:

1. Seite für Seite die Höhen aufsummieren.
2. Würde die nächste Aufgabe (Text + Feld) das Budget überschreiten, den Seitenumbruch davor setzen.
3. Bleibt dabei auf der alten Seite mehr als ca. 60 mm frei, lieber das Feld der letzten Aufgabe vergrößern, als Leerraum zu lassen, sofern das fachlich vertretbar ist. Sonst so lassen.
4. Kopf- und Deckblattbereich (Name, Klasse, Datum, Punktetabelle) mitrechnen.
5. Die Schätzung ist grob (Bilder, lange Tabellen und Formeln weichen ab). In der Antwort darauf hinweisen, dass die Umbrüche nach dem ersten PDF-Export in Typora geprüft werden sollten.

Weitere Regeln:

- Teilaufgaben, die sich auf eine gemeinsame Ausgangssituation, Tabelle oder Abbildung beziehen, möglichst auf derselben Seite oder Doppelseite halten wie diese.
- Eine Überschrift nie allein am Seitenende stehen lassen: Der Umbruch kommt vor die Überschrift.
- Ein Feld über ca. 200 mm (z. B. `grid-40`, `lines-20`) bekommt eine eigene Seite.
- Beim Leistungsnachweis mit Deckblatt folgt nach dem Deckblatt immer ein Umbruch.

## Grundgerüst

```markdown
# Titel

Name: ____________________   Klasse: ______   Datum: __________

## 1. Buchungssätze

1.1 Bargeldeinzahlung von 4.000,00 € auf das Geschäftsbankkonto. (2)

<div class="grid-6"></div>

1.2 Einkauf einer Fertigungsmaschine im Wert von 12.000,00 € netto auf Ziel. (3)

<div class="grid-8"></div>

<div style="page-break-after: always; break-after: page;"></div>

## 2. Abschnitt

…
```

(1.1: 2 Zeilen × 2 + 2 Reserve = 6. 1.2: 3 Zeilen × 2 + 2 Reserve = 8.)

## Ablauf

1. Inhalt übernehmen, ohne ihn zu verändern. Vorhandene Punktangaben `(n)` bleiben stehen.
2. Je Aufgabe intern die Lösung skizzieren, Lösungszeilen zählen und Feldtyp und Größe bestimmen.
3. Seitenbudget durchrechnen und Umbrüche setzen.
4. Syntax prüfen: Leerzeilen um jedes `<div>`, N zwischen 1 und 40, kein Umbruch am Ende.
5. `.md` ausgeben. Danach knapp auflisten:
   - die Seitenaufteilung (Seite 1: Aufgaben 1.1–1.4, …),
   - Felder, bei denen die Zeilenzahl unsicher war (z. B. wenn mehrere Lösungswege unterschiedlich lang sind),
   - fachliche Auffälligkeiten in den Aufgaben (z. B. fehlende Angaben, mehrdeutige Formulierung). Die nur **nennen**, nicht ändern.

## Kritisch prüfen

- Ist eine Aufgabe mit Feld überhaupt sinnvoll, oder wäre ein vorgegebenes Schema bzw. ein Ankreuzformat besser? Als Vorschlag nennen.
- Gibt die Lehrkraft eine Feldgröße vor, die nach der Zeilenzählung nicht reicht (z. B. `grid-4` für einen Buchungssatz mit Vorsteuer), darauf hinweisen und ihre Vorgabe trotzdem übernehmen.