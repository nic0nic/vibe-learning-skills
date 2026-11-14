#!/usr/bin/env node
/* baue.js – Übung für vibe learning prüfen und als Datei, ByCS-Paket oder Pull-Request-Dateien bauen.
 *
 * Eingabe: Aufgaben-JSON (.json, Standardbausteine) oder eigene Seite (.html, geschrieben wie eine Seite in
 * pb_public/<Fach>/<Bereich>/ mit relativen Pfaden ../../lib/aufgaben.js usw., siehe references/eigene-seite.md).
 * Die Bausteine liegen in assets/vl/ (Kopie von pb_public, werkzeuge/vibe-learning-holen.py) – nicht lesen, nur einbetten.
 *
 *   node scripts/baue.js pruefe  uebung.json                     Fehlerliste (Regeln von lib/seite.js) – wie die Webseite
 *   node scripts/baue.js html    uebung.json|seite.html -o x.html Eine HTML-Datei, läuft per Doppelklick (alles eingebettet)
 *   node scripts/baue.js bycs    uebung.json|seite.html -o x.zip  SCORM-Paket für ByCS/Moodle („Lernpaket“)
 *   node scripts/baue.js repo    uebung.json|seite.html --pfad BWR/9II/finanzierung -o ordner [--katalog katalog.js] [--text "Kurztext"]
 *        → ordner/pb_public/<pfad>/<id>.html, ordner/pb_public/katalog.js (Eintrag in EINREICHUNGEN), ordner/PR.md
 *        Dieselben Dateien wie „Einreichen“ auf der Webseite (pb_hooks/einreichen.pb.js). --katalog: aktuelle
 *        katalog.js aus dem Repo (sonst der Stand in assets/vl).
 *   node scripts/baue.js bereiche                                Bereiche (pfad für --pfad) mit Namen
 * Optionen: --stufen n (ByCS: Stufen für die Prozentzahl, Standard 0), --design id (nur JSON, statt json.design)
 */
'use strict';
const fs = require('fs'), path = require('path');
const VL = path.join(__dirname, '..', 'assets', 'vl');
const Seite = require(path.join(VL, 'lib', 'seite.js'));
const lies = p => fs.readFileSync(path.join(VL, p), 'utf8');
const stop = text => { console.error(text); process.exit(1); };

// ---------- Aufruf ----------
const argv = process.argv.slice(2), befehl = argv[0];
const opt = {}, frei = [];
for (let i = 1; i < argv.length; i++) {
  if (argv[i].startsWith('--') || argv[i] === '-o') opt[argv[i].replace(/^-+/, '')] = argv[++i];
  else frei.push(argv[i]);
}

function katalog(datei) {
  const text = datei ? fs.readFileSync(datei, 'utf8') : lies('katalog.js');
  const fenster = {};
  new Function('window', text)(fenster);
  return {text, K: fenster.KATALOG};
}
const bereiche = K => K.bereiche.filter(b => !b.fachweit);

function eingabe() {
  const datei = frei[0];
  if (!datei) stop('Datei fehlt (Aufgaben-JSON oder eigene Seite .html).');
  const text = fs.readFileSync(datei, 'utf8');
  if (/\.html?$/i.test(datei)) return {art: 'eigen', html: text, datei};
  let daten;
  try { daten = JSON.parse(text); } catch (e) { stop('Das JSON ist nicht gültig: ' + e.message); }
  const f = Seite.pruefe(daten);
  if (f.length) stop('Bitte korrigieren:\n- ' + f.join('\n- '));
  return {art: 'json', daten, datei};
}

// ---------- Eigene Seite: Bausteine einbetten (wie werkzeuge/einzeldateien.py in vibe learning) ----------
const EINBINDEN = /<script\s+src="([^"]+)"\s*>\s*<\/script>|<link\s+rel="stylesheet"\s+href="([^"]+)"\s*\/?>|<script\s+type="application\/json"\s+data-einbetten="([^"]+)"\s*>\s*<\/script>/g;
const tiefe = html => { const m = html.match(/src="((?:\.\.\/)*)katalog\.js"/); return m ? m[1].length / 3 : null; };

const eigenPruefen = html => Seite.eigeneSeite(html, {}).fehler;   // gleiche Prüfung wie beim Einreichen auf der Webseite

function einbetten(html, bycs) {
  const t = tiefe(html), basis = path.join(VL, ...Array(t).fill('x'));   // gedachter Ordner pb_public/<…>/ in gleicher Tiefe
  const fehlt = [];
  html = html.replace(EINBINDEN, (m, js, css, text) => {
    const url = js || css || text;
    if (/^[a-z]+:|^\/\//i.test(url)) return m;                                   // externe Adresse bleibt
    let datei = path.resolve(basis, url);
    if (bycs && path.basename(url) === 'sync.js') datei = path.join(VL, 'scorm.js');
    if (!datei.startsWith(VL) || !fs.existsSync(datei)) { fehlt.push(url); return m; }
    const code = fs.readFileSync(datei, 'utf8');
    if (text) return `<script type="application/json" data-einbetten="${url}">${JSON.stringify(code).replace(/</g, '\\u003c')}</script>`;
    if (js) return `<script>/* ${url} */\n${code.replace(/<\/script/g, '<\\/script')}\n</script>`;
    return `<style>/* ${url} */\n${code.replace(/<\/style/g, '<\\/style')}\n</style>`;
  });
  if (fehlt.length) stop('Nicht gefunden (Pfad falsch oder kein Baustein von vibe learning): ' + fehlt.join(', '));
  const vorne = 'window.PF_EINZELDATEI = true;' + (bycs ? ` window.PF_BYCS = {stufen: ${+opt.stufen || 0}};` : '');
  return html.replace(/<head>/, `<head>\n<script>${vorne}</script>`);
}

const titelVon = html => { const m = html.match(/<title>([\s\S]*?)<\/title>/); return m ? m[1].trim().replace(/\s*[–-]\s*vibe learning$/, '').replace(/&amp;/g, '&') : 'Übung'; };
const kennungVon = html => { const m = html.match(/data-trainer="([^"]*)"/); return m ? m[1] : null; };
const dateiname = titel => Seite.toolId(titel, 'x').replace(/-x$/, '');
const zufall = () => Array.from({length: 4}, () => 'abcdefghijklmnopqrstuvwxyz0123456789'[Math.floor(Math.random() * 36)]).join('');
function mitKennung(html, id) {   // <html … data-trainer="id"> setzen (Speicherstand, Auswertung, ByCS)
  if (/data-trainer="[^"]*"/.test(html)) return html.replace(/data-trainer="[^"]*"/, `data-trainer="${id}"`);
  return html.replace(/<html\b/, `<html data-trainer="${id}"`);
}

// ---------- JSON-Seiten wie „Übung erstellen“ (IT/tools/uebung-erstellen.html) ----------
function libObjekt() {
  return {aufgabenJs: lies('lib/aufgaben.js'), aufgabenCss: lies('lib/aufgaben.css'), bwrCss: lies('BWR/bwr.css'),
    formelJs: lies('lib/formel.js'), scormJs: lies('scorm.js')};
}

// ---------- ZIP (unkomprimiert, wie werkzeuge/bycs-pakete.py) ----------
const CRC = Array.from({length: 256}, (_, n) => { let c = n; for (let k = 0; k < 8; k++) c = c & 1 ? 0xEDB88320 ^ (c >>> 1) : c >>> 1; return c >>> 0; });
const crc32 = b => { let c = 0xFFFFFFFF; for (const x of b) c = CRC[(c ^ x) & 255] ^ (c >>> 8); return (c ^ 0xFFFFFFFF) >>> 0; };
function zip(eintraege) {
  const teile = [], zentral = []; let pos = 0;
  const zeit = 0, datum = ((2026 - 1980) << 9) | (1 << 5) | 1;
  for (const [name, text] of eintraege) {
    const n = Buffer.from(name), d = Buffer.from(text, 'utf8'), crc = crc32(d);
    const kopf = Buffer.alloc(30); kopf.writeUInt32LE(0x04034b50, 0); kopf.writeUInt16LE(20, 4); kopf.writeUInt16LE(0x0800, 6);
    kopf.writeUInt16LE(0, 8); kopf.writeUInt16LE(zeit, 10); kopf.writeUInt16LE(datum, 12); kopf.writeUInt32LE(crc, 14);
    kopf.writeUInt32LE(d.length, 18); kopf.writeUInt32LE(d.length, 22); kopf.writeUInt16LE(n.length, 26); kopf.writeUInt16LE(0, 28);
    const z = Buffer.alloc(46); z.writeUInt32LE(0x02014b50, 0); z.writeUInt16LE(0x0314, 4); z.writeUInt16LE(20, 6); z.writeUInt16LE(0x0800, 8);
    z.writeUInt16LE(0, 10); z.writeUInt16LE(zeit, 12); z.writeUInt16LE(datum, 14); z.writeUInt32LE(crc, 16); z.writeUInt32LE(d.length, 20);
    z.writeUInt32LE(d.length, 24); z.writeUInt16LE(n.length, 28); z.writeUInt32LE((0o100644 << 16) >>> 0, 38); z.writeUInt32LE(pos, 42);
    teile.push(kopf, n, d); zentral.push(z, n); pos += 30 + n.length + d.length;
  }
  const zg = Buffer.concat(zentral), ende = Buffer.alloc(22);
  ende.writeUInt32LE(0x06054b50, 0); ende.writeUInt16LE(eintraege.length, 8); ende.writeUInt16LE(eintraege.length, 10);
  ende.writeUInt32LE(zg.length, 12); ende.writeUInt32LE(pos, 16);
  return Buffer.concat([...teile, zg, ende]);
}
const xml = s => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&#x27;');

function schreibe(datei, inhalt) {
  fs.mkdirSync(path.dirname(path.resolve(datei)), {recursive: true});
  fs.writeFileSync(datei, inhalt);
  console.log(`${datei}  (${Math.round(fs.statSync(datei).size / 1024)} KB)`);
}

// ---------- Befehle ----------
if (befehl === 'bereiche') {
  const {K} = katalog(opt.katalog);
  bereiche(K).forEach(b => console.log(`${b.pfad}  –  ${b.titel}`));
} else if (befehl === 'pruefe') {
  const e = eingabe();
  if (e.art === 'eigen') { const f = eigenPruefen(e.html); if (f.length) stop('- ' + f.join('\n- ')); einbetten(e.html, false); }
  console.log('OK: ' + (e.art === 'json' ? `„${e.daten.titel}“, ${Seite.normalisiere(e.daten).schritte.length} Schritte` : `eigene Seite „${titelVon(e.html)}“, Bausteine gefunden`));
} else if (befehl === 'html' || befehl === 'bycs') {
  const e = eingabe(), bycs = befehl === 'bycs';
  let html, titel, id;
  if (e.art === 'json') {
    titel = e.daten.titel; id = Seite.toolId(titel);
    const L = libObjekt();
    html = Seite.seiteHTML(e.daten, {pfad: opt.pfad || '', toolId: bycs ? id : 'vorschau', einzeln: true, lib: L, design: opt.design,
      bycs: bycs ? {scormJs: L.scormJs, stufen: +opt.stufen || 0} : undefined});
  } else {
    const f = eigenPruefen(e.html); if (f.length) stop('- ' + f.join('\n- '));
    titel = titelVon(e.html); id = kennungVon(e.html) || Seite.toolId(titel);
    html = einbetten(mitKennung(e.html, id), bycs);
  }
  const ziel = opt.o || dateiname(titel) + (bycs ? '.zip' : '.html');
  if (!bycs) schreibe(ziel, html);
  else schreibe(ziel, zip([['imsmanifest.xml', lies('lib/scorm-manifest.xml').replace(/\{kennung\}/g, id).replace(/\{t\}/g, xml(titel))], ['index.html', html]]));
} else if (befehl === 'repo') {
  const e = eingabe(), pfad = opt.pfad || '';
  const {text, K} = katalog(opt.katalog);
  const b = bereiche(K).find(x => x.pfad === pfad);
  if (!b) stop(`Bereich „${pfad}“ gibt es nicht. Möglich:\n` + bereiche(K).map(x => `  ${x.pfad}  –  ${x.titel}`).join('\n'));
  const m = text.match(/\/\* EINREICHUNGEN-ANFANG \*\/([\s\S]*?)\/\* EINREICHUNGEN-ENDE \*\//);
  if (!m) stop('katalog.js: Markierungen EINREICHUNGEN-ANFANG/-ENDE fehlen');
  let html, titel, kurz, id;
  if (e.art === 'json') {
    titel = e.daten.titel; kurz = opt.text != null ? opt.text : e.daten.kurztext || '';
    id = Seite.toolId(titel, zufall());
    html = Seite.seiteHTML(e.daten, {pfad, toolId: id, design: opt.design});
  } else {
    const f = eigenPruefen(e.html); if (f.length) stop('- ' + f.join('\n- '));
    titel = titelVon(e.html); kurz = opt.text || '';
    id = Seite.toolId(titel, zufall());
    html = Seite.eigeneSeite(e.html, {pfad, toolId: id}).html;   // relative Pfade an die Tiefe des Bereichs, data-trainer
    einbetten(html, false);   // nur prüfen, ob alle Bausteine gefunden werden
  }
  const liste = JSON.parse(m[1]);
  const eintrag = {bereich: b.id, tool: {id, datei: id + '.html', titel, text: kurz}};
  liste.push(eintrag);
  const neu = text.replace(m[0], '/* EINREICHUNGEN-ANFANG */ ' + JSON.stringify(liste, null, 2) + ' /* EINREICHUNGEN-ENDE */');
  const aus = opt.o || 'einreichung', seitePfad = `pb_public/${pfad}/${id}.html`;
  schreibe(path.join(aus, seitePfad), html);
  schreibe(path.join(aus, 'pb_public/katalog.js'), neu);
  const eigen = e.art === 'eigen', p = eigen ? Seite.eigeneSeite(e.html, {}) : null;
  schreibe(path.join(aus, 'PR.md'), `# ${eigen ? '⚠️ Eigener Code – ' : ''}Neue Übung: ${titel}\n\n`
    + (eigen ? `> [!WARNING]\n> **Eigener Code:** Diese Seite enthält eigenes JavaScript (${p.skripte} Script-Blöcke, ${p.zeilen} Zeilen). Geprüft wurde nur, dass sie ausschließlich Bausteine von vibe learning einbindet – den Code vor dem Mergen lesen und die Seite ausprobieren.\n\n` : '')
    + `Erstellt mit dem Skill vibe-learning-seite-erstellen (${eigen ? 'eigene Seite' : 'Standardbausteine, Aufgaben-JSON'}).\n\n`
    + `- **Bereich:** ${pfad} (${b.titel})\n- **Datei:** \`${seitePfad}\`\n- **Kurztext:** ${kurz || '–'}\n\n`
    + `Nach dem Mergen: \`python3 werkzeuge/einzeldateien.py\` und \`python3 werkzeuge/bycs-pakete.py\` laufen lassen und mit \`git push origin main:live\` freigeben.\n`);
  console.log('\nEintrag in katalog.js (EINREICHUNGEN, zum Einfügen von Hand):\n' + JSON.stringify(eintrag));
} else {
  stop('Befehle: pruefe | html | bycs | repo | bereiche (Kopfkommentar von scripts/baue.js)');
}
