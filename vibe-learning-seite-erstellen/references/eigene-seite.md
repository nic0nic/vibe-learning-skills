# Eigene Seite (über die Standardbausteine hinaus)

Nur wenn das Ziel mit Aufgaben-JSON **nicht** geht: eigene Interaktion (z. B. Lampen zum Anklicken, Grafik, Simulation)
oder Aufgaben, die der Code jedes Mal neu erzeugt. Alles andere bleibt Standardbaustein – auch auf der eigenen Seite.

## Grundsatz: so wenig eigener Code wie möglich

- Die Seite ist ein **Gerüst + `Aufgaben.sequenz`**. Die Schritte schreibst du wie im Aufgaben-JSON (gleiche Typen und
  Felder, als JavaScript-Objekt). Eigener Code nur für das, was fehlt:
  - `nach(el)` an einem Schritt: eigenes Element in `html` füllen (z. B. `<div class="bitbox"></div>`)
  - `training: {stufen: [{name, antwort: 'mc' | 'eingabe', zeit, neu: fn}]}`: Endlos-Drill mit selbst erzeugten Aufgaben,
    `neu({mc})` → `{frage (HTML), loesung (Text), optionen (bei mc: [{t, ok}], genau eine ok), pruefe(text) → 'ok' | 'fast' | 'falsch'}`
  - `Aufgaben.endlos({el, key, stufen: [{name, neu() → Aufgabe}]})`: Endlos mit beliebigen Aufgabentypen
  - `Aufgaben.baue(el, aufgabe, {fertig})`: eine einzelne Aufgabe irgendwo einsetzen
- API und alle Felder: **nur den Kopfkommentar lesen**: `sed -n "1,/^ \*\//p" assets/vl/lib/aufgaben.js`. Den Rest von
  `assets/vl/` nicht lesen (kostet nur Tokens) – `scripts/baue.js` bettet die Dateien ein.
- Aussehen: Klassen aus `lib/basis.css` (`.wrap .bar .brand .karte .btn .btn.haupt .btn.klein .feld .muted`) und
  Farbvariablen (`--bg --panel --panel2 --text --muted --border --accent --ok --err --mono`), die im hellen und
  dunklen Modus stimmen. Eigenes CSS kurz halten und nur diese Variablen verwenden.
- Kein Server, keine externen Skripte/Schriften/Bilder (läuft auch als Datei und in ByCS). Bilder höchstens als
  kleines Inline-SVG. Keine personenbezogenen Daten.

## Gerüst

Die Seite liegt gedacht in `pb_public/<Fach>/<Bereich>/` (Tiefe 2, `../../`); für einen Bereich mit Jahrgangsstufe
(z. B. `BWR/9II/finanzierung`) passt `scripts/baue.js repo` die Pfade selbst an.

```html
<!doctype html>
<html lang="de" data-trainer="kennung">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Titel – vibe learning</title>
<script src="../../katalog.js"></script>
<script src="../../nav.js"></script>
<script src="../../sync.js"></script>
<script>
(function(){var t=null;try{t=localStorage.getItem('wenn-theme');}catch(e){}
document.documentElement.dataset.theme=t||(matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light');})();
</script>
<link rel="stylesheet" href="../../lib/basis.css">
<link rel="stylesheet" href="../../lib/aufgaben.css">
<script src="../../lib/aufgaben.js"></script>
<style>
/* nur das Nötigste, mit den Farbvariablen */
</style>
</head>
<body>
<div class="wrap">
  <div class="bar"><div class="brand">Wort<span>teil</span></div><div class="muted">Untertitel</div></div>
  <div id="app"></div>
</div>
<script>
'use strict';
function eigenesBauen(el){ /* füllt z. B. el.querySelector('.box') */ }

Aufgaben.sequenz({el:'#app', key:'kennung', schritte:[
  {id:'info', kurz:'Einführung', html:'<h2>…</h2><p>…</p><div class="box"></div>', nach: eigenesBauen},
  {id:'ueb1', kurz:'1 Üben', erinnerung:'<p>Regel</p>', aufgaben:[
    {typ:'mc', nr:'1.1', frage:'…', options:['richtig', 'falsch'], correct:[0], why:{1:'…'}}]},
  {id:'endlos', kurz:'Endlos', titel:'Training', html:'<h2>…</h2>',
   training:{stufen:[{name:'Auswählen', antwort:'mc', neu:neueAufgabe}, {name:'Eintippen', antwort:'eingabe', neu:neueAufgabe}]}}
]});
</script>
</body>
</html>
```

- `data-trainer` und `key` = dieselbe Kennung (a–z, 0–9, -). Beim Pull Request setzt `baue.js` eine neue, eindeutige.
- `<title>` endet auf „ – vibe learning“ (wird für Paket- und Menünamen abgeschnitten).
- Vorbild mit allem (Bits zum Anklicken, Training mit eigenen Aufgaben und Schaltern): `IT/grundlagen/zahlensysteme.html`
  im Repo nic0nic/vibe-learning – nur ansehen, wenn ein Muster wirklich gebraucht wird.

## Prüfen und bauen

```
node scripts/baue.js pruefe seite.html          # Gerüst da, alle Bausteine gefunden
node scripts/baue.js html   seite.html -o …     # Datei zum Herunterladen
node scripts/baue.js bycs   seite.html -o …     # ByCS-Paket (--stufen n bei Stufen)
node scripts/baue.js repo   seite.html --pfad IT/grundlagen -o einreichung
```

Wenn möglich die fertige Datei im Browser öffnen bzw. mit einem Headless-Browser auf JavaScript-Fehler prüfen.
Eigene Seiten gehen **nicht** über „Übung erstellen“ auf der Webseite (dort nur Aufgaben-JSON ohne Code), sondern nur als
Datei, ByCS-Paket oder Pull Request direkt im Repo – der Code wird dort vor dem Freigeben geprüft.
