"""Bausteine und Build-Pipeline für Selbstlernhefte (A4, HTML -> PDF).

Benutzung in einer eigenen Inhaltsdatei (z. B. inhalt.py):

    import sys; sys.path.insert(0, '<skill>/scripts')
    from heft_lib import *
    import svg_kit as S

    TITEL = {1: 'Thema 1', 2: 'Thema 2'}
    def inhalt():
        page(titelseite(...))
        page(kap(1, TITEL[1]) + info('...') + ueb(1, 'Thema 1', '...') + aufg(1, aufg_kopf() + task('1.1', '...', ab('Lösung', 3))) + check(1))
    if __name__ == '__main__':
        build(inhalt, TITEL, teile=[('Heft', [1, 2])], out='out', prefix='Thema', fuss='Thema · Modellunternehmen')

Modi: 's' = Schülerfassung (Antworten unsichtbar), 'l' = Lösung (Antworten blau, Monospace).
"""
import os, re, glob

HERE = os.path.dirname(os.path.abspath(__file__))
CSS = open(os.path.join(HERE, '..', 'assets', 'style.css'), encoding='utf-8').read()

MODE = 's'
LSG = {}        # Lösungsblatt-Nr -> HTML-Teile (nur im Modus 'l' gesammelt)
PAGES = []
KAPSEITE = {}

# ---------------------------------------------------------------- Bausteine
def a(t, w=None):
    """Lücke im Fließtext oder in Tabellen. Lange Antworten (>28 Zeichen) bekommen in Tabellen Schreiblinien."""
    st = f' style="min-width:{w}"' if w else ''
    lang = ' lang' if len(t) > 28 else ''
    return f'<span class="a{lang}"{st}>{t}</span>'

def ab(t, n, keep=False):
    """Freie Antwort. Standard: Bearbeitung auf Blockblatt (Schülerheft ohne Platz).
    keep=True: n Schreiblinien (7,5 mm) im Heft – nur für Merkteile."""
    if keep:
        return f'<div class="ab" style="height:{n*7.5}mm"><span class="at">{t}</span></div>'
    return f'<div class="lt"><span class="at">{t}</span></div>' if (MODE == 'l' and t) else ''

def karo(t, n, keep=False):
    """Rechenaufgabe. keep=True: n Kästchenzeilen (5 mm, Vektorlinien) im Heft."""
    if keep:
        W, H = 180, n * 5
        d = ''.join(f'M0 {y}H{W}' for y in range(0, H + 1, 5)) + ''.join(f'M{x} 0V{H}' for x in range(0, W + 1, 5))
        g = (f'<svg class="grid" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" style="width:{W}mm;height:{H}mm">'
             f'<path d="{d}" stroke="#8a8a8a" stroke-width="0.18" fill="none"/></svg>')
        return f'<div class="karo" style="height:{n*5}mm">{g}<span class="at">{t}</span></div>'
    return f'<div class="lt"><span class="at">{t}</span></div>' if MODE == 'l' else ''

def frac(z, n):
    return f'<span class="frac"><span>{z}</span><span>{n}</span></span>'

def formel(html):
    return f'<div class="formel">{html}</div>'

def lsg(nr, html):
    """Markiert einen Teil, der auf Lösungsblatt L<nr> erscheint."""
    if MODE == 'l':
        LSG.setdefault(nr, []).append(html)
    return html

def ueb(nr, titel, inner):
    """Eingerahmter Merkteil mit Lücken (a(...)). Landet auf dem Lösungsblatt."""
    return lsg(nr, f'<div class="ueb"><div class="uebt">ÜBERBLICK · {titel} <span>– ergänze die Lücken</span></div>{inner}</div>')

def alltag(titel, inner, label='AUS DEM ALLTAG'):
    """Nur bei echtem Alltagsbezug 'AUS DEM ALLTAG', sonst label='BEISPIEL'."""
    return f'<div class="alltag"><div class="allt">{label} · {titel}</div>{inner}</div>'

def beispiel(titel, inner):
    return alltag(titel, inner, 'BEISPIEL')

def aufg(nr, html):
    return lsg(nr, f'<div class="aufgaben">{html}</div>')

def aufg_kopf():
    return '<div class="ak">✎ Aufgaben</div>'

def task(n, text, body=''):
    return f'<div class="task"><b class="tn">{n}</b> {text}{body}</div>'

def tabelle(kopf, zeilen, breiten=None):
    """kopf: Liste Spaltenköpfe; zeilen: Liste von Listen (Zellen-HTML, Lücken mit a())."""
    br = breiten or [None] * len(kopf)
    th = ''.join(f'<th{f" style=\'width:{b}\'" if b else ""}>{k}</th>' for k, b in zip(kopf, br))
    tr = ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in z) + '</tr>' for z in zeilen)
    return f'<table class="t"><tr>{th}</tr>{tr}</table>'

def check(nr, extra=''):
    return (f'<div class="check"><span class="cl">✔ L{nr}</span> Vergleiche jetzt deine Lösungen mit dem '
            f'<b>Lösungsblatt L{nr}</b> (hinten im Klassenzimmer). Korrigiere mit einer anderen Farbe. {extra}</div>')

def kap(n, t, pb=False):
    """Kapitelüberschrift. pb=True erzwingt auch in der Kompaktfassung eine neue Seite."""
    KAPSEITE[n] = len(PAGES) + 1
    return f'<h2 class="kap{" pb" if pb else ""}"><span class="kn">{n}</span>{t}</h2>'

def info(html, cols=False):
    """Infotext (9,6 pt). cols=True: zweispaltiger Fluss für längere Abschnitte."""
    return f'<div class="info{" cols" if cols else ""}">{html}</div>'

def zwei(links, rechts):
    """Zwei feste Spalten mit gezieltem Spaltenumbruch (z. B. 'Wer?' | 'Woher?')."""
    return f'<div class="zwei"><div>{links}</div><div>{rechts}</div></div>'

def keep(html):
    """Gruppe, die in der Kompaktfassung nie getrennt wird (z. B. Erklärung + zugehörige Aufgabe)."""
    return f'<div class="keep">{html}</div>'

def fig(svg, schmal=False):
    return f'<div class="fig{" fig80" if schmal else ""}">{svg}</div>'

def material(titel, html):
    return f'<div class="mat"><div class="matt">Material: {titel}</div>{html}</div>'

def szenario(titel, html):
    return f'<div class="szenario"><div class="szt">{titel}</div>{html}</div>'

def seitenref(sel):
    """Platzhalter für 'siehe S. x': wird in der Kompaktfassung durch die Seite des ersten Elements mit CSS-Selektor sel ersetzt."""
    return f'<span class="sref" data-sel="{sel}">?</span>'

def page(html):
    PAGES.append(html)

def titelseite(fach_zeile, titel, logo_svg, auftrag_html, steckbrief, titel_dict, legende_extra=''):
    """Titelseite mit Kopfzeile, Szenario, Steckbrief, Arbeitsplan und Arbeitshinweisen."""
    st = ''.join(f'<tr><td>{k}</td><td>{v}</td></tr>' for k, v in steckbrief)
    plan = ''.join(f'<tr><td>{n}</td><td>{t}</td><td>§S{n}§</td><td>L{n}</td><td class="cb">☐</td></tr>' for n, t in titel_dict.items())
    return f'''
<div class="kopf"><span>Name: ______________________________</span><span>Klasse: ______</span><span>Datum: ______________</span></div>
<div class="titel"><div><div class="tsub">{fach_zeile}</div><h1>{titel}</h1></div>{logo_svg}</div>
{szenario('Dein Auftrag', auftrag_html)}
<h3 class="h3">Das Unternehmen</h3><table class="steck">{st}</table>
<h3 class="h3">Dein Arbeitsplan</h3>
<table class="plan"><tr><th>Nr.</th><th>Thema</th><th>Seite</th><th>Lösungsblatt</th><th>erledigt</th></tr>{plan}</table>
<h3 class="h3">So arbeitest du</h3>
<div class="block">✎ Bearbeite alle Aufgaben auf einem <b>eigenen Blockblatt</b> (Aufgabennummer davor schreiben). <b>Ausnahme:</b> Lücken, Tabellen und Kästchen, die im Heft vorgegeben sind, füllst du direkt im Heft aus.</div>
<div class="legende">
<div><span class="mini mi">INFO</span> Lies den Text genau und markiere Fachbegriffe.</div>
<div><span class="mini ma">ALLTAG</span> Vergleich mit dem echten Leben – hilft beim Verstehen.</div>
<div><span class="mini mu">ÜBERBLICK</span> Ergänze die Lücken. Das ist dein Merkkasten zum Lernen.</div>
<div><span class="mini mk">✎ AUFGABEN</span> Bearbeite sie selbstständig auf deinem Blockblatt.</div>
<div><span class="mini mc">✔ L1</span> Hole dir das Lösungsblatt, vergleiche und korrigiere.</div>{legende_extra}
</div>'''

# ---------------------------------------------------------------- Ausgabe
def _zeilen(html):
    """Tabellenzeilen mit mehrzeiligen Einträgen bekommen Schreiblinien (alle Antwortzellen der Zeile)."""
    def tr(m):
        t = m.group(0)
        tds = re.findall(r'<td[^>]*>.*?</td>', t, flags=re.S)
        if 'class="a lang"' not in t and not any(x.count('class="a') >= 2 for x in tds):
            return t
        return re.sub(r'(<td[^>]*>)((?:(?!</td>).)*class="a(?: lang)?"(?:(?!</td>).)*)(</td>)', r'\1<div class="zl">\2</div>\3', t, flags=re.S)
    return re.sub(r'<tr>.*?</tr>', tr, html, flags=re.S)

def doc(title, body, cls):
    return (f'<!doctype html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{title}</title><style>{CSS}</style></head><body class="{cls}">{_zeilen(body)}</body></html>')

def _render(pages, fuss):
    n = len(pages)
    return ''.join(f'<div class="page">{p}<div class="foot"><span>{fuss}</span><span>Seite {k+1} von {n}</span></div></div>' for k, p in enumerate(pages))

def _blaetter(titel_dict, ks):
    return ''.join(f'<div class="page lsheet"><div class="lnr">L{k}</div><div class="lkopf">Lösungsblatt {k} · {titel_dict[k]}</div>'
                   f'<div class="lhinw">Nicht hineinschreiben – bitte zurücklegen!</div>{"".join(LSG.get(k, []))}</div>' for k in ks)

def _lauf(inhalt_fn, mode):
    global MODE
    MODE = mode
    LSG.clear(); PAGES.clear(); KAPSEITE.clear()
    inhalt_fn()
    for k, v in KAPSEITE.items():
        PAGES[:] = [p.replace(f'§S{k}§', str(v)) for p in PAGES]
    return list(PAGES)

def build(inhalt_fn, titel_dict, teile, out='out', prefix='Heft', fuss='', kompakt=True):
    """teile: [(Name, [Kapitelnummern]), ...] – jeder Teil wird ein eigenes Heft mit eigenen Lösungsblättern.
    Erzeugt je Teil: <prefix>_<Name>_Schueler/_Lehrkraft.html (je Kapitel neue Seite),
    *_kompakt.html (platzoptimiert) und Loesungsblaetter_L<a>-L<b>.html."""
    os.makedirs(out, exist_ok=True)
    for f in glob.glob(os.path.join(out, '*.html')):
        os.remove(f)
    erzeugt = []
    for mode in ('s', 'l'):
        pages = _lauf(inhalt_fn, mode)
        for i, (name, kaps) in enumerate(teile):
            start = KAPSEITE[kaps[0]] - 1
            if i == 0:
                start = 0  # Titelseite gehört zum ersten Teil
            ende = KAPSEITE[teile[i + 1][1][0]] - 1 if i + 1 < len(teile) else len(pages)
            f_teil = fuss + ('' if i == 0 else f' · {name}')
            fn = f'{prefix}_{name}_{"Schueler" if mode == "s" else "Lehrkraft"}.html'
            open(os.path.join(out, fn), 'w', encoding='utf-8').write(doc(f'{prefix} – {name}', _render(pages[start:ende], f_teil), mode))
            erzeugt.append((fn, f_teil))
            if mode == 'l':
                bn = f'Loesungsblaetter_L{kaps[0]}-L{kaps[-1]}.html'
                open(os.path.join(out, bn), 'w', encoding='utf-8').write(doc(f'{prefix} – Lösungsblätter', _blaetter(titel_dict, kaps), 'l'))
    if kompakt:
        from paginate import paginate
        paginate([(os.path.join(out, fn), os.path.join(out, fn.replace('.html', '_kompakt.html')), f) for fn, f in erzeugt])
    print('Kapitelseiten:', KAPSEITE)
