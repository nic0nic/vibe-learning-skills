# Vorlage & Syntax-Konventionen für mkslides-Folien

Diese Referenz beschreibt das Ziel-Format. Beim Erstellen der `slides.md`
orientiere dich exakt an diesen Mustern (Frontmatter, Folientrenner,
Arbeitsauftrag-Box, Gruppenübersicht-Direktive).

## 1. Frontmatter (Kopf der Datei)

Immer als YAML-Frontmatter zu Beginn, `author` und `date` an die Quelle
anpassen, Rest kann übernommen werden:

```yaml
---
author: "<Name der Lehrkraft, falls bekannt, sonst weglassen>"
date: "<Jahr>--"
slides:
    title: "<Thema der Stunde>"
    theme: "solarized"
revealjs:
    height: 1080
    width: 1920
    transition:
---
```

Direkt danach folgt IMMER der CSS-Block für die Arbeitsauftrag-Boxen (siehe
Abschnitt 3) — unverändert übernehmen:

```html
<style>
div.arbeitsauftrag {
    background-color: #ffe699 !important;
    color: #504e45 !important;
    padding: 40px !important;
    border-radius: 15px !important;
    border: 3px solid #2b2a50 !important;
    margin: 30px 0 !important;
}
div.arbeitsauftrag h2 {
    color: #2b2a50 !important;
    border-bottom: 2px solid #2b2a50 !important;
    padding-bottom: 15px !important;
}
div.arbeitsauftrag strong {
    color: #4f4f4f !important;
}
</style>
```

## 2. Folien trennen

Jede neue Folie wird durch eine Zeile mit drei Bindestrichen getrennt:

```
---
```

## 3. Normale Inhaltsfolie

```
# <Haupttitel, nur auf der ersten Inhaltsfolie>
## <Untertitel, z.B. Lernbaustein/Kapitel>

---

<Fließtext oder Überschrift der Folie>

![<beschreibender alt-Text>](./assets/<bilddatei>)

Quelle: <URL oder Quellenangabe, falls im Original vorhanden>
```

Bilder werden IMMER relativ aus `./assets/` eingebunden, nie mit absoluten
Pfaden. Verwende die tatsächlichen Dateinamen aus der Extraktion
(`img_01.png` etc.) — nicht umbenennen, außer es verbessert die Lesbarkeit
und du passt den Verweis konsistent an.

## 4. Arbeitsauftrag-Folie (Einzelarbeit / ohne Gruppenzuordnung)

Wird verwendet, wenn die Quelle eine Aufgabenstellung an die Schüler enthält
(erkennbar an Formulierungen wie "Lies...", "Notiere...", "Bearbeite...",
Fragen an die Lernenden, Arbeitsanweisungen). Icon-Kürzel nach Kontext wählen:
`:bust_in_silhouette:` für Einzelarbeit, `:busts_in_silhouette:` für
Partner-/Gruppenarbeit.

```html
<div class="arbeitsauftrag">

## Arbeitsauftrag :bust_in_silhouette:

<Aufgabenstellung aus der Quelle, so wörtlich wie möglich übernehmen>

</div>
```

Falls die Quellfolie ein unterstützendes Bild enthält (z.B. Screenshot einer
App, Diagramm), wird es eingebunden:

```html
<div class="arbeitsauftrag">

## Arbeitsauftrag :bust_in_silhouette:

<Aufgabenstellung>

<img src="./assets/<bilddatei>" alt="<alt-Text>" style="zoom: 67%;" />

</div>
```

## 5. Arbeitsauftrag mit Gruppenarbeit -> GRUPPEN-Direktive

Wenn die Aufgabenstellung erkennbar Gruppenarbeit ist (z.B. "Findet euch in
Gruppen zusammen", "Diskutiert in eurer Gruppe", "jede Gruppe bearbeitet ein
Thema"), wird ZUSÄTZLICH zur Arbeitsauftrag-Box eine GRUPPEN-Direktive
eingefügt (direkt danach, als eigener HTML-Kommentar):

```html
<div class="arbeitsauftrag">

## Arbeitsauftrag :busts_in_silhouette:

<Aufgabenstellung aus der Quelle>

</div>

<!-- GRUPPEN: {"klasse": "KLASSE_ANPASSEN", "gruppen": <ANZAHL_ANPASSEN>, "seed": <ZUFALLSZAHL>} -->
```

Regeln für die Werte:
- `klasse`: IMMER Platzhalter `"KLASSE_ANPASSEN"` — wird vom Nutzer manuell
  gesetzt (Skript weiß nicht, für welche Klasse gebaut wird).
- `gruppen`: Anzahl aus dem Kontext ableiten, falls erkennbar (z.B. Anzahl
  genannter Unterthemen in der Quelle -> jedes Unterthema wird eine Gruppe,
  dann zusätzlich `"namen"` mit den Themen befüllen). Sonst plausiblen
  Standardwert (z.B. 4) setzen und im Chat kurz darauf hinweisen.
- `namen`: NUR setzen, wenn die Quelle klar benannte Teilthemen/Gruppen
  vorgibt (z.B. "Gruppe A bearbeitet X, Gruppe B bearbeitet Y"). Sonst
  weglassen (Skript nummeriert dann automatisch "Gruppe 1", "Gruppe 2", ...).
- `seed`: eine feste, zufällig gewählte Ganzzahl (z.B. per Zufallsgenerator
  bestimmt) — wichtig, damit die Zuordnung bei jedem Build gleich bleibt.
  NICHT bei jedem Lauf neu würfeln, sondern einmal pro Arbeitsauftrag fest
  vergeben.

Beispiel mit benannten Themen (aus einer Quelle mit 3 Teilthemen):

```html
<!-- GRUPPEN: {"klasse": "KLASSE_ANPASSEN", "gruppen": 3, "namen": ["Überschuldung", "buy now pay later", "Raus aus den Schulden"], "seed": 17} -->
```

## 6. Bild-only Folie (z.B. Titelbild, Logo, Quelle als Fußzeile)

```
![<alt-Text>](./assets/<bilddatei>)

<Quelle/Beschriftung als einfacher Text darunter, falls vorhanden>
```

## 7. Allgemeine Regeln

- Reihenfolge der Folien aus der Quelle beibehalten.
- Text so nah wie möglich am Original übernehmen (nicht umformulieren),
  außer offensichtliche Tippfehler/Encoding-Artefakte aus der Extraktion.
- Leere/inhaltslose Folien (nur Seitenzahl, Übergangsfolie ohne Text) können
  übersprungen werden — im Zweifel lieber übernehmen und der Nutzer entfernt
  sie händisch.
- Sprechernotizen (aus PPTX) NICHT automatisch in die Folie übernehmen,
  sondern nur erwähnen, falls sie wichtigen Kontext für die Aufgabenerkennung
  liefern (z.B. "Notiz: hier Gruppenarbeit machen").
- Bilder nicht umbenennen/verschieben ohne Grund — Referenzen in der .md
  müssen exakt zu den Dateinamen in `assets/` passen.
