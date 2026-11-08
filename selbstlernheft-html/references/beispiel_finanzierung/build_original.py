"""Erzeugt Heft (Schüler), Heft (Lösung) und Lösungsblätter L1–L9."""
import svg as S

MODE = 's'
LSG = {}      # L-Nr -> Liste von HTML-Teilen (nur im Lösungsmodus gesammelt)
LTITEL = {}

# ---------- Bausteine ----------
def a(t, w=None):
    st = f' style="min-width:{w}"' if w else ''
    lang = ' lang' if len(t) > 28 else ''
    return f'<span class="a{lang}"{st}>{t}</span>'

def ab(t, n, keep=False):
    """Ohne keep: Bearbeitung auf dem Blockblatt -> im Schülerheft kein Platz, in der Lösung nur der Text."""
    if keep:
        return f'<div class="ab" style="height:{n*7.5}mm"><span class="at">{t}</span></div>'
    return f'<div class="lt"><span class="at">{t}</span></div>' if (MODE == 'l' and t) else ''

def karo(t, n, keep=False):
    if keep:
        W, H = 180, n*5
        d = ''.join(f'M0 {y}H{W}' for y in range(0, H+1, 5)) + ''.join(f'M{x} 0V{H}' for x in range(0, W+1, 5))
        g = f'<svg class="grid" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" style="width:{W}mm;height:{H}mm"><path d="{d}" stroke="#8a8a8a" stroke-width="0.18" fill="none"/></svg>'
        return f'<div class="karo" style="height:{n*5}mm">{g}<span class="at">{t}</span></div>'
    return f'<div class="lt"><span class="at">{t}</span></div>' if MODE == 'l' else ''

def frac(z, n):
    return f'<span class="frac"><span>{z}</span><span>{n}</span></span>'

def lsg(nr, html):
    if MODE == 'l':
        LSG.setdefault(nr, []).append(html)
    return html

def ueb(nr, titel, inner):
    return lsg(nr, f'<div class="ueb"><div class="uebt">ÜBERBLICK · {titel} <span>– ergänze die Lücken</span></div>{inner}</div>')

def alltag(titel, inner, label='AUS DEM ALLTAG'):
    return f'<div class="alltag"><div class="allt">{label} · {titel}</div>{inner}</div>'

def aufg(nr, html):
    return lsg(nr, f'<div class="aufgaben">{html}</div>')

def aufg_kopf():
    return '<div class="ak">✎ Aufgaben</div>'

def task(n, text, body=''):
    return f'<div class="task"><b class="tn">{n}</b> {text}{body}</div>'

def check(nr, extra=''):
    return f'<div class="check"><span class="cl">✔ L{nr}</span> Vergleiche jetzt deine Lösungen mit dem <b>Lösungsblatt L{nr}</b> (hinten im Klassenzimmer). Korrigiere mit einer anderen Farbe. {extra}</div>'

KAPSEITE={}
def kap(n, t, pb=False):
    KAPSEITE[n]=len(PAGES)+1
    return f'<h2 class="kap{" pb" if pb else ""}"><span class="kn">{n}</span>{t}</h2>'

def info(html, cols=False):
    return f'<div class="info{" cols" if cols else ""}">{html}</div>'

PAGES = []
def page(html):
    PAGES.append(html)

# ---------- Inhalt ----------
def inhalt():
    PAGES.clear()
    # ===== Seite 1: Titel / Szenario =====
    page(f'''
<div class="kopf"><span>Name: ______________________________</span><span>Klasse: ______</span><span>Datum: ______________</span></div>
<div class="titel"><div><div class="tsub">BwR · Jahrgangsstufe 9 · Selbstlernheft</div><h1>Möglichkeiten der Finanzierung</h1></div>{S.guitar("42mm")}</div>
<div class="szenario"><div class="szt">Dein Auftrag</div>
<p>Beim Grillen erzählt <b>Jakob Seite</b>, ein guter Freund deines Vaters, von seiner Firma: Seine handgefertigten Gitarren verkaufen sich so gut, dass er neue Maschinen braucht. „Die Bank bietet mir einen Kredit an, mein Steuerberater redet ständig von <i>Eigenkapitalquote</i>, und ein Bekannter will sich an meiner Firma beteiligen – ich blicke da nicht mehr durch. Du hast doch BwR in der Schule. Kannst du mir ein paar Tipps geben?“</p>
<p>Du sagst zu. Damit deine Tipps Hand und Fuß haben, arbeitest du dich mit diesem Heft <b>selbstständig</b> in das Thema Finanzierung ein. Am Ende schreibst du Jakob eine <b>Beratungs-E-Mail</b>.</p></div>
<h3 class="h3">Das Unternehmen</h3>
<table class="steck"><tr><td>Firma</td><td>Jakob Seite Saitgig e. K. („Saitgig“)</td></tr>
<tr><td>Inhaber</td><td>Jakob Seite</td></tr><tr><td>Rechtsform</td><td>Einzelunternehmen</td></tr>
<tr><td>Zweck des Unternehmens</td><td>Saitgig stellt Gitarren her.</td></tr>
<tr><td>Fertigerzeugnisse</td><td>E-Gitarren, Akustikgitarren, E-Bässe</td></tr>
<tr><td>Geschäftsjahr</td><td>1. Januar bis 31. Dezember</td></tr></table>
<h3 class="h3">Dein Arbeitsplan</h3>
<table class="plan"><tr><th>Nr.</th><th>Thema</th><th>Seite</th><th>Lösungsblatt</th><th>erledigt</th></tr>
{''.join(f'<tr><td>{n}</td><td>{t}</td><td>{s}</td><td>L{n}</td><td class="cb">☐</td></tr>' for n,t,s in [
 (k,TITEL[k],'§S%d§'%k) for k in range(1,7)])}</table>
<h3 class="h3">So arbeitest du</h3>
<div class="block">✎ Bearbeite alle Aufgaben auf einem <b>eigenen Blockblatt</b> (Aufgabennummer davor schreiben). <b>Ausnahme:</b> Lücken, Tabellen und Kästchen, die im Heft vorgegeben sind, füllst du direkt im Heft aus.</div>
<div class="legende">
<div><span class="mini mi">INFO</span> Lies den Text genau und markiere Fachbegriffe.</div>
<div><span class="mini ma">ALLTAG</span> Vergleich mit dem echten Leben – hilft beim Verstehen.</div>
<div><span class="mini mu">ÜBERBLICK</span> Ergänze die Lücken. Das ist dein Merkkasten zum Lernen.</div>
<div><span class="mini mk">✎ AUFGABEN</span> Bearbeite sie selbstständig auf deinem Blockblatt.</div>
<div><span class="mini mc">✔ L1</span> Hole dir das Lösungsblatt, vergleiche und korrigiere.</div>
</div>''')

    # ===== Kapitel 1 =====
    page(f'''{kap(1,'Finanzierung und Liquidität')}
{info('''<p>Jakob braucht ständig Geld: für neue Maschinen, Tonhölzer, Saiten, Löhne und die Miete der Werkstatt. Wie ein Unternehmen an dieses Geld (<b>Kapital</b>) kommt und wofür es eingesetzt wird, zeigt die <b>Bilanz</b>. Sie hat zwei Seiten, die immer gleich groß sind:</p>''')}
<div class="fig">{S.bilanz_schema()}</div>
{info('''<p><b>Finanzierung</b> ist die <b>Beschaffung von Kapital</b>. Sie ist auf der <b>Passivseite</b> der Bilanz sichtbar (Mittel<b>herkunft</b>): Das Kapital stammt entweder vom Eigentümer (<b>Eigenkapital</b>) oder von Gläubigern wie der Bank (<b>Fremdkapital</b>).<br>
<b>Investierung</b> ist die <b>Anlage von Kapital im Vermögen</b> des Unternehmens. Sie ist auf der <b>Aktivseite</b> sichtbar (Mittel<b>verwendung</b>), z. B. als Maschine oder Holzvorrat.<br>
Weil laufend investiert und bezahlt wird, ist Finanzierung eine <b>laufende</b> Aufgabe jedes Unternehmens.</p>
<p>Ganz entscheidend für das Überleben eines Unternehmens ist die <b>Liquidität</b> (Zahlungsfähigkeit): die Fähigkeit, alle <b>Zahlungsverpflichtungen termingerecht</b> zu erfüllen. Wer Rechnungen, Löhne oder Kreditraten nicht pünktlich bezahlen kann, ist <b>zahlungsunfähig</b> – das kann zur <b>Insolvenz</b> (Pleite) führen.</p>''', True)}
{alltag('Reich, aber pleite?','''<p>Lena besitzt eine alte Vintage-Gitarre im Wert von 3.000 €. Auf ihrem Konto liegen aber nur 20 €. Morgen muss sie 150 € für die Klassenfahrt überweisen. Ist Lena reich? Vielleicht. Ist sie <b>liquide</b>? Nein! Ihr Vermögen steckt in der Gitarre und lässt sich nicht von heute auf morgen in Geld umwandeln.<br>
Genauso kann ein Unternehmen Gewinn machen und trotzdem zahlungsunfähig werden – zum Beispiel, wenn Kunden spät bezahlen, die eigenen Rechnungen aber sofort fällig sind.</p>''')}
''')
    page(f'''{ueb(1,'Finanzierung und Liquidität',f'''
<p><b>Finanzierung</b> = {a('Beschaffung','30mm')} von Kapital →<br>sichtbar auf der {a('Passivseite','30mm')} der Bilanz (Mittel{a('herkunft','22mm')})</p>
<p><b>Investierung</b> = {a('Anlage','22mm')} von Kapital im {a('Vermögen','24mm')} →<br>sichtbar auf der {a('Aktivseite','26mm')} der Bilanz (Mittel{a('verwendung','26mm')})</p>
<p><b>Liquidität</b> = Fähigkeit, alle {a('Zahlungsverpflichtungen','50mm')} {a('termingerecht','32mm')} zu erfüllen.</p>
<p>Folge dauerhafter Zahlungsunfähigkeit: {a('Insolvenz','30mm')}</p>''')}
{aufg(1, aufg_kopf() + task('1.1','Ordne die Vorgänge bei Saitgig der Investierung (I) oder der Finanzierung (F) zu.',f'''
<table class="t"><tr><th>Vorgang</th><th style="width:20mm">I / F</th></tr>
<tr><td>a) Kauf einer Lackieranlage</td><td>{a('I')}</td></tr>
<tr><td>b) Aufnahme eines Bankdarlehens</td><td>{a('F')}</td></tr>
<tr><td>c) Jakob Seite legt 20.000,00 € aus seinem Privatvermögen ein.</td><td>{a('F')}</td></tr>
<tr><td>d) Einkauf von Tonhölzern auf Lager</td><td>{a('I')}</td></tr>
<tr><td>e) Ein Bekannter beteiligt sich mit 30.000,00 € am Unternehmen.</td><td>{a('F')}</td></tr></table>''')
+ task('1.2','Definiere den Begriff Liquidität.', ab('Liquidität ist die Fähigkeit eines Unternehmens, alle Zahlungsverpflichtungen termingerecht (fristgerecht) zu erfüllen.',3))
+ task('1.3','Erläutere, warum ein Unternehmen trotz Gewinn zahlungsunfähig werden kann.', ab('Gewinn ist nicht automatisch Geld auf dem Konto: z. B. zahlen Kunden erst später (Forderungen) oder das Geld steckt in Vorräten und Maschinen. Werden gleichzeitig Rechnungen, Löhne oder Kreditraten fällig, fehlt das Geld → Zahlungsunfähigkeit.',4))
+ task('1.4','Am 03.11. hat Saitgig 5.000,00 € auf dem Bankkonto. Am 04.11. ist eine Rechnung über 8.000,00 € fällig. Ein Kunde wird Saitgig in 30 Tagen 12.000,00 € überweisen. Begründe, ob Saitgig am 04.11. liquide ist.', ab('Nein: Am 04.11. stehen nur 5.000,00 € zur Verfügung, fällig sind aber 8.000,00 €. Die Zahlung des Kunden kommt zu spät – die Rechnung kann nicht termingerecht bezahlt werden (obwohl Saitgig insgesamt genug Geld bekommt).',4)))}
{check(1)}''')

    # ===== Kapitel 2 =====
    page(f'''{kap(2,'Eigenkapitalquote')}
{alltag('Klaus und Peter kaufen sich ein Auto','''<p>Klaus und Peter sind beide 19 und haben gerade ihre Ausbildung abgeschlossen.</p>''')}
<div class="autos"><div class="auto">{S.car_old()}<p><b>Klaus</b> fährt einen alten Golf. Er hat ihn für <b>4.000 €</b> gekauft und <b>komplett aus seinem Ersparten</b> (Ferienjobs) bezahlt.</p></div>
<div class="auto">{S.car_new()}<p><b>Peter</b> fährt einen neuen BMW für <b>45.000 €</b>. Er hat <b>5.000 €</b> Erspartes angezahlt, den Rest (<b>40.000 €</b>) finanziert er über einen <b>Autokredit</b>.</p></div></div>
<div class="keep">{info(f'''<p>Beide fahren ein Auto – aber wem gehört das Auto wirklich? Bei Klaus steckt nur <b>eigenes Geld</b> (Eigenkapital) im Auto. Bei Peter stammt der größte Teil von der Bank (Fremdkapital). Wie groß der eigene Anteil ist, zeigt die <b>Eigenkapitalquote</b>:</p>
<div class="formel">Eigenkapitalquote in % = {frac('Eigenkapital · 100','Gesamtkapital')}</div>
<p>Das Gesamtkapital ist dabei der gesamte Wert, der finanziert wurde (Eigenkapital + Fremdkapital).</p>''')}
{aufg(2, aufg_kopf() + task('2.1','Berechne die Eigenkapitalquote von Klaus und von Peter.', karo('Klaus: 4.000 · 100 : 4.000 = 100 %<br>Peter: 5.000 · 100 : 45.000 = 11,1 %',4, keep=True)))}</div>
{aufg(2, task('2.2','Beide verlieren ein halbes Jahr nach dem Autokauf ihre Arbeitsstelle. Erläutere, wer finanziell besser dasteht.', ab('Klaus: Er hat keine Schulden und muss keine Kreditraten zahlen – er ist unabhängig. Peter muss weiter Zinsen und Tilgung für 40.000 € zahlen, obwohl ihm das Einkommen fehlt. Kann er nicht zahlen, verliert er das Auto. → Klaus steht besser da.',4)))}''')

    page(f'''{info('''<p><b>Und im Unternehmen?</b> Banken, Lieferer und Geschäftspartner schauen sich die Eigenkapitalquote eines Unternehmens sehr genau an. Eine <b>hohe</b> Eigenkapitalquote bedeutet:</p>
<ul><li><b>finanzielle Unabhängigkeit</b> – das Unternehmen ist weniger von Gläubigern abhängig,</li><li><b>Kreditwürdigkeit</b> – Banken vergeben leichter und günstiger Kredite,</li><li><b>Krisenfestigkeit</b> – Verluste in schlechten Jahren können besser aufgefangen werden.</li></ul>
<p>Ob eine Quote gut ist, erkennt man nur im <b>Branchenvergleich</b>: Anlagenintensive Unternehmen (viele Maschinen und Gebäude) brauchen eine höhere Eigenkapitalausstattung. <i>Aber Vorsicht:</i> „Je höher, desto besser“ stimmt nur bedingt – auch Eigenkapital ist nicht kostenlos, denn die Eigentümer wollen am Gewinn beteiligt werden.</p>''', True)}
{ueb(2,'Eigenkapitalquote',f'''<p><b>Eigenkapitalquote</b> = Anteil des {a('Eigenkapitals','30mm')} am {a('Gesamtkapital','30mm')}</p>
<p>Formel: Eigenkapitalquote in % = {a('Eigenkapital · 100 : Gesamtkapital','70mm')}</p>
<p>Vorteile einer hohen Eigenkapitalquote: {a('finanzielle Unabhängigkeit','45mm')}, {a('Kreditwürdigkeit','32mm')}, {a('Krisenfestigkeit','32mm')}</p>
<p>Beurteilung nur sinnvoll durch {a('Branchenvergleich','36mm')}</p>''')}
<div class="mat"><div class="matt">Material: Bilanz von Saitgig zum 31.12. (in €)</div>
<table class="bil"><tr><th colspan="2">Aktiva</th><th colspan="2">Passiva</th></tr>
<tr><td><b>Anlagevermögen</b></td><td></td><td><b>Eigenkapital</b></td><td>312.000,00</td></tr>
<tr><td>Betriebs- und Verwaltungsgebäude</td><td>420.000,00</td><td><b>Fremdkapital</b></td><td></td></tr>
<tr><td>Maschinen und Anlagen</td><td>260.000,00</td><td>Langfristige Bankverbindlichkeiten</td><td>520.000,00</td></tr>
<tr><td>Fuhrpark</td><td>60.000,00</td><td>Kurzfristige Bankverbindlichkeiten</td><td>98.000,00</td></tr>
<tr><td>Büromöbel und Geschäftsausstattung</td><td>40.000,00</td><td>Verbindlichkeiten aus L. u. L.</td><td>110.000,00</td></tr>
<tr><td><b>Umlaufvermögen</b></td><td></td><td></td><td></td></tr>
<tr><td>Rohstoffe (Tonhölzer)</td><td>95.000,00</td><td></td><td></td></tr>
<tr><td>Forderungen aus L. u. L.</td><td>110.000,00</td><td></td><td></td></tr>
<tr><td>Bank</td><td>48.000,00</td><td></td><td></td></tr>
<tr><td>Kasse</td><td>7.000,00</td><td></td><td></td></tr>
<tr class="sum"><td>Summe</td><td>1.040.000,00</td><td>Summe</td><td>1.040.000,00</td></tr></table>
<p class="klein">Durchschnittliche Eigenkapitalquote im Musikinstrumentenbau: 38 %. Diese Bilanz brauchst du auch in Kapitel 3 und 9.</p></div>
{aufg(2, task('2.3','Berechne die Eigenkapitalquote von Saitgig.', karo('312.000,00 · 100 : 1.040.000,00 = 30,0 %',2))
+ task('2.4','Beurteile die Eigenkapitalquote von Saitgig mithilfe des Branchendurchschnitts.', ab('Mit 30,0 % liegt Saitgig unter dem Branchendurchschnitt von 38 %. Saitgig ist stärker von Gläubigern abhängig und gilt als weniger kreditwürdig und krisenfest → die Eigenkapitalbasis sollte gestärkt werden.',4)))}
{check(2)}''')

    # ===== Kapitel 3 =====
    page(f'''{kap(3,'Goldene Finanzierungsregel')}
{alltag('Das geliehene Moped','''<p>Du möchtest ein Moped für 2.000 € kaufen und es drei Jahre lang fahren. Dein Bruder leiht dir das Geld – will es aber <b>in vier Wochen</b> zurück. Das Moped ist dann noch da, das Geld aber nicht. Du müsstest das Moped verkaufen oder dir schnell neues Geld leihen. Besser wäre ein Geldgeber, der dir genauso lange Zeit lässt, wie du das Moped nutzt.</p>''')}
{info('''<p>Genau so denkt die <b>Goldene Finanzierungsregel</b>: Kapital soll mindestens so lange zur Verfügung stehen, wie es im Vermögen gebunden ist – <b>Grundsatz der Fristengleichheit</b>.</p>
<ul><li><b>Langfristiges Vermögen</b> (Anlagevermögen: Gebäude, Maschinen) wird mit <b>langfristigem Kapital</b> finanziert (Eigenkapital und langfristiges Fremdkapital).</li>
<li><b>Kurzfristiges Vermögen</b> (Umlaufvermögen: Vorräte, Forderungen, Bank) darf mit <b>kurzfristigem Fremdkapital</b> finanziert werden.</li></ul>''')}
<div class="fig fig80">{S.goldene_regel()}</div>
{info('''<p>Wer gegen die Regel verstößt, muss Kredite zurückzahlen, bevor die Maschine das Geld „erwirtschaftet“ hat → es drohen <b>Liquiditätsschwierigkeiten</b>.</p>
<p><b>Langfristiges Fremdkapital</b> (Laufzeit über ein Jahr): z. B. <b>4250 LBKV</b> – langfristige Bankverbindlichkeiten (Darlehen).<br>
<b>Kurzfristiges Fremdkapital</b> (Laufzeit bis ein Jahr): z. B. <b>4200 KBKV</b> – kurzfristige Bankverbindlichkeiten und <b>4400 VE</b> – Verbindlichkeiten aus Lieferungen und Leistungen.</p>''')}
{ueb(3,'Goldene Finanzierungsregel',f'''<p>Grundsatz der {a('Fristengleichheit','40mm')}: Kapital soll so lange verfügbar sein, wie es im {a('Vermögen','26mm')} gebunden ist.</p>
<table class="t ut"><tr><td>langfristiges Vermögen → {a('langfristiges','28mm')} Kapital</td><td>{a('Anlagevermögen','34mm')} ≤ {a('Eigenkapital + langfristiges Fremdkapital','78mm')}</td></tr>
<tr><td>kurzfristiges Vermögen → {a('kurzfristiges','28mm')} Kapital</td><td>{a('Umlaufvermögen','34mm')} ≥ {a('kurzfristiges Fremdkapital','58mm')}</td></tr></table>
<p>Bei Verstoß drohen {a('Liquiditätsschwierigkeiten','52mm')}.</p>''')}
''')

    page(f'''{aufg(3, aufg_kopf() + task('3.1','Überprüfe mithilfe der Bilanz von Saitgig (Kapitel 2, S. §S5§), ob Saitgig die Goldene Finanzierungsregel einhält.', karo('AV: 420.000 + 260.000 + 60.000 + 40.000 = 780.000,00 €<br>EK + langfr. FK: 312.000 + 520.000 = 832.000,00 €<br>UV: 95.000 + 110.000 + 48.000 + 7.000 = 260.000,00 €<br>kurzfr. FK: 98.000 + 110.000 = 208.000,00 €<br>780.000 ≤ 832.000 und 260.000 ≥ 208.000<br>→ Die Goldene Finanzierungsregel wird eingehalten.',9))
+ task('3.2','Jakob möchte eine neue CNC-Fräse für 80.000,00 € kaufen und sie mit einem kurzfristigen Bankkredit bezahlen. Begründe, ob die Goldene Finanzierungsregel danach noch eingehalten wird.', ab('Nein: Das Anlagevermögen steigt auf 860.000,00 €, das langfristige Kapital bleibt bei 832.000,00 € → 860.000 &gt; 832.000. Ein Teil des langfristigen Vermögens wäre kurzfristig finanziert.',4))
+ task('3.3','Gib an, ob es sich um langfristiges (L) oder kurzfristiges (K) Kapital handelt.', f'''<table class="t"><tr><th>Kapital</th><th style="width:20mm">L / K</th></tr>
<tr><td>a) Bankdarlehen mit 10 Jahren Laufzeit</td><td>{a('L')}</td></tr><tr><td>b) Rechnung eines Holzlieferanten, zahlbar in 30 Tagen</td><td>{a('K')}</td></tr>
<tr><td>c) Kredit über 6 Monate zur Überbrückung eines Zahlungsengpasses</td><td>{a('K')}</td></tr><tr><td>d) Eigenkapital von Jakob Seite</td><td>{a('L')}</td></tr></table>'''))}
{check(3)}''')

    # ===== Kapitel 4 =====
    page(f"""{kap(4,'Eigenfinanzierung und Fremdfinanzierung')}
{alltag('Noch einmal Klaus und Peter','''<p>Klaus hat sein Auto mit <b>eigenem Geld</b> bezahlt – er musste niemanden fragen und zahlt keine Zinsen. Peter hat sich das meiste Geld <b>geliehen</b>: Er muss den Kredit mit Zinsen zurückzahlen, darf aber alleine entscheiden, wohin er fährt – die Bank redet nicht mit.</p>''')}
{info('''<div class="zwei"><div><p><b>Wer gibt das Kapital?</b></p>
<p><b>Eigenfinanzierung:</b> Das Kapital kommt von den <b>Eigentümern</b> und erhöht das <b>Eigenkapital</b>. Es steht <b>unbefristet</b> zur Verfügung; es fallen <b>keine Zinsen und keine Tilgung</b> an. Die Eigentümer wollen aber am Gewinn beteiligt werden und tragen das Verlustrisiko.</p>
<p><b>Fremdfinanzierung (Kreditfinanzierung):</b> Das Kapital kommt von <b>Gläubigern</b> (Bank, Lieferer) und erhöht das <b>Fremdkapital</b>. Es steht nur <b>befristet</b> zur Verfügung, kostet <b>Zinsen</b> und muss <b>getilgt</b> werden. Der Gläubiger hat <b>kein Mitspracherecht</b>.</p>
</div><div><p><b>Woher kommt das Geld?</b></p>
<p><b>Innenfinanzierung:</b> Das Geld stammt aus dem Unternehmen selbst, z. B. einbehaltener Gewinn.<br><b>Außenfinanzierung:</b> Das Geld fließt von außen zu, z. B. Inhaber legt privates Geld ein, neuer Gesellschafter, Bankkredit.</p>
</div></div>''')}
{info('''<p><b>Formen der Eigenfinanzierung:</b></p>
<ul><li><b>Selbstfinanzierung:</b> Gewinne werden nicht entnommen, sondern im Unternehmen einbehalten (<b>Thesaurierung</b>).</li>
<li><b>Einlagenfinanzierung</b> (Einzelunternehmen): Der Inhaber legt privates Geld ein oder ein <b>stiller Gesellschafter</b> beteiligt sich.</li>
<li><b>Beteiligungsfinanzierung</b> (Aktiengesellschaft): Die AG gibt <b>junge Aktien</b> aus (<b>Kapitalerhöhung</b>).</li></ul>''')}
{ueb(4,'Finanzierungsformen als Matrix',f'''<table class="matrix"><tr><th></th><th>{a('Eigenfinanzierung','40mm')}<small>Kapital von den Eigentümern</small></th><th>{a('Fremdfinanzierung','40mm')}<small>Kapital von Gläubigern</small></th></tr>
<tr><th>{a('Innenfinanzierung','34mm')}<small>Geld aus dem Unternehmen selbst</small></th><td>{a('Selbstfinanzierung','40mm')}<small>Beispiel:</small>{a('Gewinn wird einbehalten','50mm')}</td><td class="grau"><small>kommt in diesem Heft nicht vor</small></td></tr>
<tr><th>{a('Außenfinanzierung','34mm')}<small>Geld fließt von außen zu</small></th><td>{a('Einlagen- bzw. Beteiligungsfinanzierung','58mm')}<small>Beispiele:</small>{a('Einlage des Inhabers, stiller Gesellschafter, junge Aktien','62mm')}</td><td>{a('Kreditfinanzierung','40mm')}<small>Beispiel:</small>{a('Bankkredit, Lieferantenkredit','50mm')}</td></tr></table>''')}
<p class="vnt"><b>Vor- und Nachteile der Formen der Eigenfinanzierung</b></p>
<table class="t vn"><tr><th style="width:22%">Form</th><th>Vorteile</th><th>Nachteile / Risiken</th></tr>
<tr><td><b>Selbstfinanzierung</b></td><td>Kapital unbefristet; keine Zinsen, keine Tilgung; Eigenkapitalquote und Kreditwürdigkeit steigen</td><td>nur möglich, wenn Gewinn erzielt wurde; Inhaber kann den Gewinn nicht privat verwenden; Gefahr von Fehlinvestitionen, weil keine Bank das Vorhaben prüft</td></tr>
<tr><td><b>stiller Gesellschafter</b><br><small>(Einzelunternehmen)</small></td><td><i>Unternehmen:</i> Kapital ohne Änderung der Rechtsform; Eigenkapital steigt; Inhaber bleibt alleiniger Chef<br><i>Gesellschafter:</i> anonym, keine Pflicht zur Mitarbeit, Gewinnanteil</td><td><i>Unternehmen:</i> Gewinn muss geteilt werden; Gesellschafter erwartet oft mehr als Bankzinsen; Einlage muss bei Kündigung zurückgezahlt werden<br><i>Gesellschafter:</i> kaum Einfluss; Einlage kann verloren gehen</td></tr>
<tr><td><b>junge Aktien</b><br><small>(Aktiengesellschaft)</small></td><td>sehr hohe Beträge möglich; Kapital unbefristet; keine Zinsen; Kreditwürdigkeit steigt</td><td>gelingt nur bei guten Zukunftsaussichten; Mehrheitsverhältnisse können sich ändern; Gewinn verteilt sich auf mehr Aktien</td></tr></table>
""")

    page(f"""{alltag('Der stille Gesellschafter','''<p>Deine Cousine eröffnet einen Imbisswagen. Euer Onkel gibt ihr 10.000 € und bekommt dafür jedes Jahr einen Anteil am Gewinn. Im Imbiss steht er nie – die Kunden wissen nicht einmal, dass er beteiligt ist. Läuft der Imbiss schlecht, ist sein Geld im schlimmsten Fall weg.</p>''', 'BEISPIEL')}
{aufg(4, aufg_kopf() + task('4.1','Vervollständige die Tabelle.', f'''<table class="t"><tr><th>Vorgang</th><th style="width:34mm">Eigen- oder Fremd&shy;finanzierung?</th><th style="width:34mm">Innen- oder Außen&shy;finanzierung?</th></tr>
<tr><td>a) Der Gewinn des Vorjahres bleibt im Unternehmen.</td><td>{a('Eigenfinanzierung')}</td><td>{a('Innenfinanzierung')}</td></tr>
<tr><td>b) Die Bank gewährt Saitgig ein Darlehen über 50.000,00 €.</td><td>{a('Fremdfinanzierung')}</td><td>{a('Außenfinanzierung')}</td></tr>
<tr><td>c) Ein stiller Gesellschafter beteiligt sich mit 40.000,00 €.</td><td>{a('Eigenfinanzierung')}</td><td>{a('Außenfinanzierung')}</td></tr>
<tr><td>d) Ein Instrumentenkonzern (AG) gibt junge Aktien aus.</td><td>{a('Eigenfinanzierung')}</td><td>{a('Außenfinanzierung')}</td></tr></table>''')
+ task('4.2','Unterscheide Eigen- und Fremdfinanzierung anhand von zwei Merkmalen.', ab('z. B.: Verfügbarkeit: Eigenkapital unbefristet – Fremdkapital befristet; Kosten: Eigenkapital keine Zinsen/Tilgung – Fremdkapital Zinsen und Tilgung. (Auch möglich: Kapitalgeber Eigentümer – Gläubiger; Mitsprache ja – nein)',4))
+ task('4.3','Gib an, zu welcher Form der Eigenfinanzierung die Aussagen passen: Selbstfinanzierung (S), stiller Gesellschafter (G) oder junge Aktien (A).', f'''<table class="t"><tr><th>Aussage</th><th style="width:20mm">S / G / A</th></tr>
<tr><td>a) Die Mehrheitsverhältnisse im Unternehmen können sich verschieben.</td><td>{a('A')}</td></tr>
<tr><td>b) Der Kapitalgeber tritt nach außen nicht in Erscheinung.</td><td>{a('G')}</td></tr>
<tr><td>c) Diese Finanzierung ist nur möglich, wenn Gewinn erzielt wurde.</td><td>{a('S')}</td></tr></table>''')
+ task('4.4','Ein Bekannter möchte sich mit 60.000,00 € als stiller Gesellschafter an Saitgig beteiligen. Erläutere je einen Vorteil und einen Nachteil für Jakob Seite.', ab('Vorteil, z. B.: Das Eigenkapital steigt (Eigenkapitalquote über 30 %), es fallen keine festen Zinsen an und Jakob bleibt alleiniger Chef.<br>Nachteil, z. B.: Jakob muss den Gewinn teilen; kündigt der Bekannte, muss die Einlage zurückgezahlt werden.',5)))}
{check(4)}""")

    # ===== Kapitel 5 =====
    page(f'''{kap(5,'Kredite bei der Bank')}
{info('''<p><b>Kredit</b> kommt vom lateinischen <i>credere</i> = vertrauen. Ein Kredit ist die <b>zeitweilige Überlassung von Geld</b> durch den <b>Kreditgeber</b> (Gläubiger) an den <b>Kreditnehmer</b> (Schuldner) gegen die Zahlung von <b>Zinsen</b> – sie sind der Preis für das geliehene Geld. Kredite mit hohen Beträgen und langen Laufzeiten nennt man <b>Darlehen</b>.</p>''')}
<div class="fig">{S.kredit_ablauf()}</div>
{info('''<p><b>Die Bank prüft vor der Kreditvergabe:</b></p><ul>
<li><b>Kreditfähigkeit</b> = rechtliche Fähigkeit, einen Kreditvertrag abzuschließen (z. B. volljährig, Firma im Handelsregister).</li>
<li><b>Kreditwürdigkeit</b> = Fähigkeit, den Kredit zurückzuzahlen (Gewinn, Eigenkapitalquote, bisherige Zahlungsmoral).</li></ul>
<p><b>Sicherheiten</b> schützen die Bank, falls der Kredit nicht zurückgezahlt wird: <b>Bürgschaft</b> (eine andere Person haftet), <b>Sicherungsübereignung</b> (z. B. ein Lieferwagen), <b>Grundschuld</b> (auf ein Grundstück), <b>Zession</b> (Abtretung von Forderungen an die Bank).</p>''', True)}
{alltag('SCHUFA und Handyvertrag','''<p>Wenn du mit 18 deinen ersten Handyvertrag abschließt, fragt der Anbieter bei der <b>SCHUFA</b> nach, ob du bisher Rechnungen pünktlich bezahlt hast. Mit 17 bekommst du ohne Eltern gar keinen Vertrag – dir fehlt die <b>Kreditfähigkeit</b>. Wer ständig Rechnungen offen lässt, gilt als nicht <b>kreditwürdig</b> und bekommt später schwerer einen Kredit, eine Wohnung oder einen Vertrag.</p>''')}''')

    page(f'''{info('''<p><b>Disagio – ein Abzug vorab:</b> Manche Banken zahlen nicht den vollen Kreditbetrag aus, sondern behalten einen Prozentsatz ein (<b>Disagio</b> = Abschlag, „vorausbezahlter Zins“). Der Kreditnehmer erhält nur den <b>Auszahlungsbetrag</b>, muss aber den <b>vollen Kreditbetrag</b> verzinsen und zurückzahlen.</p>''')}
<table class="t schema"><tr><td>Kreditbetrag</td><td>40.000,00 €</td><td>100,0 %</td></tr><tr><td>– Disagio</td><td>200,00 €</td><td>0,5 %</td></tr><tr class="sum"><td>= Auszahlungsbetrag</td><td>39.800,00 €</td><td>99,5 %</td></tr></table>
{info('''<p>Ein Angebot mit niedrigem Zinssatz ist deshalb nicht automatisch das günstigste: Ein hohes Disagio oder zusätzliche Gebühren können es teurer machen. Wie man Angebote richtig vergleicht (effektiver Zinssatz), lernst du im Unterricht.</p>''')}
{ueb(5,'Kredite bei der Bank',f'''<p><b>Kredit</b> = {a('zeitweilige Überlassung von Geld','64mm')} gegen Zahlung von {a('Zinsen','20mm')}</p>
<p><b>Kreditfähigkeit</b> = {a('rechtliche Fähigkeit, einen Kreditvertrag abzuschließen','108mm')}</p>
<p><b>Kreditwürdigkeit</b> = {a('Fähigkeit, den Kredit zurückzuzahlen','80mm')}</p>
<p><b>Sicherheiten:</b> {a('Bürgschaft','24mm')}, {a('Sicherungsübereignung','42mm')}, {a('Grundschuld','26mm')}, {a('Zession','18mm')}</p>
<p><b>Schuldendienst</b> = {a('Zinsen','18mm')} + {a('Tilgung','18mm')}</p>
<p><b>Disagio</b> = {a('Abzug vom Kreditbetrag bei der Auszahlung (vorausbezahlter Zins)','120mm')}</p>''')}
{aufg(5, aufg_kopf() + task('5.1','Grenze Kreditfähigkeit und Kreditwürdigkeit voneinander ab.', ab('Kreditfähigkeit: rechtliche Fähigkeit, einen Kreditvertrag abzuschließen.<br>Kreditwürdigkeit: wirtschaftliche Fähigkeit, Zinsen und Tilgung zu zahlen.',3))
+ task('5.2','Nenne zwei Sicherheiten, die Saitgig der Bank anbieten könnte.', ab('z. B. Grundschuld auf das Betriebsgrundstück; Sicherungsübereignung des Lieferwagens/einer Maschine (auch: Bürgschaft, Zession von Forderungen)',3))
+ task('5.3','Saitgig nimmt ein Darlehen über 50.000,00 € auf. Die Bank behält 2 % Disagio ein. Berechne den Auszahlungsbetrag.', karo('Disagio: 50.000,00 · 2 : 100 = 1.000,00 €<br>Auszahlungsbetrag: 50.000,00 – 1.000,00 = 49.000,00 €',3))
+ task('5.4','Gib den Betrag an, den Saitgig bei diesem Darlehen insgesamt tilgen muss.', ab('50.000,00 € (der volle Kreditbetrag)',1)))}
{check(5)}''')

    # ===== Kapitel 6 =====
    page(f'''{kap(6,'Darlehensarten', pb=True)}
{alltag('Der Hauskredit deiner Eltern','''<p>Viele Familien bezahlen ihr Haus über 20 bis 30 Jahre ab – jeden Monat mit der <b>gleichen Rate</b>. Am Anfang steckt in dieser Rate viel Zins und wenig Tilgung, am Ende ist es umgekehrt. Das ist ein <b>Annuitätendarlehen</b>.</p>''')}
{info('''<p>Langfristige Darlehen für Maschinen oder Gebäude unterscheiden sich vor allem darin, <b>wie getilgt</b> wird. Wichtig: Die Zinsen werden immer auf die <b>Restschuld</b> berechnet – je schneller getilgt wird, desto weniger Zinsen fallen insgesamt an.</p>
<ul><li><b>Abzahlungsdarlehen:</b> jedes Jahr wird der <b>gleiche Betrag getilgt</b>. Die Restschuld sinkt gleichmäßig, damit sinken die Zinsen – und die Rate wird jedes Jahr kleiner.</li>
<li><b>Annuitätendarlehen:</b> die <b>Rate</b> (Zinsen + Tilgung) ist jedes Jahr <b>gleich hoch</b>. Weil die Zinsen sinken, steigt der Tilgungsanteil.</li>
<li><b>Festdarlehen</b> (Fälligkeitsdarlehen): während der Laufzeit werden <b>nur Zinsen</b> gezahlt, getilgt wird <b>einmalig am Ende</b>. Da die Schuld voll bestehen bleibt, sind die Zinsen jedes Jahr gleich hoch.</li></ul>
<p>Beispiel: Darlehen über 40.000 €, Laufzeit 4 Jahre, 8 % Zinsen p. a.</p>''', True)}
<div class="dgrp"><div class="fig">{S.legende_darlehen()}</div>
<div class="drei"><div>{S.darlehen_chart('Abzahlungsdarlehen')}</div><div>{S.darlehen_chart('Annuitätendarlehen')}</div><div>{S.darlehen_chart('Festdarlehen')}</div></div></div>
{ueb(6,'Darlehensarten',f'''<p class="klein">Trage ein: gleich · steigend · sinkend · einmalig am Ende</p>
<table class="t ut3"><tr><th></th><th>Abzahlungsdarlehen</th><th>Annuitätendarlehen</th><th>Festdarlehen</th></tr>
<tr><td><b>Tilgung</b></td><td>{a('gleich')}</td><td>{a('steigend')}</td><td>{a('einmalig am Ende')}</td></tr>
<tr><td><b>Zinsen</b></td><td>{a('sinkend')}</td><td>{a('sinkend')}</td><td>{a('gleich')}</td></tr>
<tr><td><b>Rate</b></td><td>{a('sinkend')}</td><td>{a('gleich')}</td><td>{a('gleich (nur Zinsen), am Ende sehr hoch')}</td></tr>
<tr><td><b>Vorteil</b></td><td>{a('geringste Zinskosten; Belastung sinkt mit der Zeit')}</td><td>{a('gut planbar durch gleiche Rate')}</td><td>{a('geringe Belastung während der Laufzeit, schont Liquidität')}</td></tr>
<tr><td><b>Nachteil</b></td><td>{a('hohe Belastung am Anfang')}</td><td>{a('höhere Zinskosten als Abzahlungsdarlehen')}</td><td>{a('höchste Zinskosten; große Summe am Ende nötig')}</td></tr></table>''')}''')

    def plan(n, rows):
        return (f'<div class="plan1"><b>Plan {n}</b><table class="t pl"><tr><th>Jahr</th><th>Restschuld</th><th>Zinsen</th><th>Tilgung</th><th>Rate</th></tr>'
                + ''.join(f'<tr><td>{k+1}</td>' + ''.join(f'<td>{v}</td>' for v in r) + '</tr>' for k, r in enumerate(rows)) + '</table></div>')
    page(f'''<div class="mat"><div class="matt">Material: Drei Angebote der Hausbank für ein Darlehen von Saitgig über 60.000,00 €, Laufzeit 4 Jahre, 5 % Zinsen p. a. (Beträge in €)</div>
<div class="plaene">{plan('A',[('60.000,00','3.000,00','0,00','3.000,00')]*3+[('60.000,00','3.000,00','60.000,00','63.000,00')])}
{plan('B',[('60.000,00','3.000,00','13.920,71','16.920,71'),('46.079,29','2.303,96','14.616,75','16.920,71'),('31.462,54','1.573,13','15.347,58','16.920,71'),('16.114,96','805,75','16.114,96','16.920,71')])}
{plan('C',[('60.000,00','3.000,00','15.000,00','18.000,00'),('45.000,00','2.250,00','15.000,00','17.250,00'),('30.000,00','1.500,00','15.000,00','16.500,00'),('15.000,00','750,00','15.000,00','15.750,00')])}</div></div>
{aufg(6, aufg_kopf() + task('6.1','Ordne die Pläne A, B und C der passenden Darlehensart zu. Begründe jeweils mit einem Merkmal aus dem Plan.', ab('A: Festdarlehen – getilgt wird erst einmalig am Ende, die Zinsen bleiben gleich.<br>B: Annuitätendarlehen – die Rate ist jedes Jahr gleich, die Tilgung steigt.<br>C: Abzahlungsdarlehen – die Tilgung ist jedes Jahr gleich, die Rate sinkt.',4))
+ task('6.2','Ermittle für jeden Plan die gesamten Zinskosten.', karo('A: 4 · 3.000,00 = 12.000,00 €<br>B: 3.000,00 + 2.303,96 + 1.573,13 + 805,75 = 7.682,84 €<br>C: 3.000,00 + 2.250,00 + 1.500,00 + 750,00 = 7.500,00 €',4))
+ task('6.3','Erkläre, warum beim Festdarlehen die höchsten Zinskosten entstehen.', ab('Die Restschuld bleibt bis zum Ende in voller Höhe (60.000,00 €) bestehen. Da die Zinsen auf die Restschuld berechnet werden, sinken sie nie.',3))
+ task('6.4','Jakob möchte jedes Jahr mit einer gleich hohen Belastung planen können. Entscheide dich für einen Plan und begründe deine Entscheidung.', ab('Plan B (Annuitätendarlehen), weil die Rate jedes Jahr gleich hoch ist (16.920,71 €) und Jakob damit sicher planen kann.',3)))}
{check(6)}''')

    # ===== Kapitel 7 =====
    page(f'''{kap(7,'Kontokorrent-, Dispositions- und Lieferantenkredit')}
{info('''<p>Nicht jeder Kredit ist ein großes Darlehen. Für den <b>laufenden Geschäftsverkehr</b> nutzen Unternehmen kurzfristige Kredite.</p>
<p><b>Kontokorrentkredit</b> (ital. <i>conto corrente</i> = laufendes Konto): Die Bank erlaubt dem Unternehmen, sein <b>Geschäftsbankkonto</b> bis zu einer <b>Kreditlinie</b> (Kreditlimit = Obergrenze) zu überziehen – <b>ohne weitere Rücksprache</b>. Er dient zur <b>Finanzierung</b> des laufenden Geschäftsverkehrs, zur <b>Sicherung der Liquidität</b> und zur <b>Überbrückung</b> kurzfristiger Zahlungsengpässe.</p>''')}
<div class="fig">{S.kontokorrent_chart()}</div>
{info('''<ul><li>kurzfristiger Kredit; Zinsen nur für die <b>tatsächlich beanspruchte Höhe und Dauer</b></li>
<li>vergleichsweise <b>teure</b> Kreditart; wird das Limit überschritten (geduldete Überziehung), fallen noch höhere <b>Überziehungszinsen</b> an</li>
<li><b>Tilgung</b> automatisch durch Zahlungseingänge (z. B. Kunden überweisen); die Bank kann die Kreditlinie jederzeit anpassen</li>
<li>zusätzlich können <b>Kontoführungsgebühren</b> anfallen → Konto 6750 KGV (Kosten des Geldverkehrs); Zinsen → 7510 ZAW</li></ul>
<p><b>Dispositionskredit</b> („Dispo“): funktioniert genauso, wird aber <b>Privatkunden</b> auf dem <b>Girokonto</b> eingeräumt. Die Höhe hängt von der Kreditwürdigkeit und den regelmäßigen Geldeingängen (z. B. Gehalt) ab. Vorteil: hohe <b>Flexibilität</b>. Nachteil: sehr <b>hohe Zinsen</b> → nur in Ausnahmefällen nutzen!</p>''')}
{alltag('Der Dispo auf deinem ersten Girokonto','''<p>Mit dem ersten Ausbildungsgehalt bietet dir die Bank vielleicht einen Dispo von 1.000 € an. Bequem – aber teuer: Dispozinsen liegen oft bei über 10 % im Jahr. Wer dauerhaft „im Minus“ lebt, zahlt jeden Monat drauf.</p>''')}''')

    page(f'''{info('''<p><b>Lieferantenkredit:</b> Gibt ein Lieferer ein <b>Zahlungsziel</b> (z. B. „zahlbar innerhalb von 30 Tagen“), gewährt er seinem Kunden einen Kredit. Bietet er zusätzlich <b>Skonto</b> an (z. B. „2 % Skonto bei Zahlung innerhalb von 10 Tagen“), gilt:</p>''')}
<div class="fig">{S.lieferanten_zeitstrahl()}</div>
{info('''<p>Bis zum Ende der Skontofrist ist der Lieferantenkredit <b>zinslos</b>. Wer später zahlt, verzichtet auf das Skonto – der entgangene <b>Nettoskonto</b> ist der Preis für die restlichen Tage. Rechnet man 2 % für 20 Tage auf ein ganzes Jahr hoch, entspricht das einem Zinssatz von etwa <b>36 %</b>! Ein Kontokorrentkredit kostet meist nur 8–12 %. Deshalb gilt: <b>Skonto nutzen – notfalls mit dem Kontokorrentkredit.</b></p>''')}
{ueb(7,'Kurzfristige Kredite',f'''<p><b>Kontokorrentkredit</b>: Überziehung des {a('Geschäftsbankkontos','40mm')} bis zur {a('Kreditlinie','24mm')}; Zinsen nur für {a('beanspruchte Höhe und Dauer','56mm')}; Tilgung durch {a('Zahlungseingänge','36mm')}</p>
<p><b>Dispositionskredit</b>: wie Kontokorrentkredit, aber für {a('Privatkunden','28mm')} auf dem {a('Girokonto','24mm')}</p>
<p><b>Lieferantenkredit</b>: bis zum Ende der {a('Skontofrist','24mm')} kostenlos, danach sehr {a('teuer','14mm')}, weil der {a('Nettoskonto','26mm')} verloren geht → {a('Skonto ausnutzen','36mm')}</p>''')}
<div class="mat"><div class="matt">Material: Eingangsrechnung eines Holzlieferanten (Auszug)</div>
<table class="t rech"><tr><td>Rechnungsdatum</td><td>02.11.</td></tr><tr><td>20 Hälse aus Ahorn, Warenwert netto</td><td>10.000,00 €</td></tr><tr><td>+ 19 % Umsatzsteuer</td><td>1.900,00 €</td></tr><tr class="sum"><td>Rechnungsbetrag</td><td>11.900,00 €</td></tr></table>
<p class="klein"><i>Zahlungsbedingungen: Zahlbar innerhalb von 30 Tagen ohne Abzug; bei Zahlung innerhalb von 10 Tagen 2 % Skonto.</i><br>Saitgig hat zurzeit kein Guthaben. Nutzt Jakob das Skonto, muss er den Überweisungsbetrag mit dem Kontokorrentkredit bezahlen. Die Bank verlangt dafür für die 20 Tage <b>58,31 € Zinsen</b>.</p></div>''')

    page(f'''{aufg(7, aufg_kopf() + task('7.1','Nenne zwei Merkmale des Kontokorrentkredits.', ab('z. B.: Überziehung bis zur Kreditlinie ohne Rücksprache; Zinsen nur für beanspruchte Höhe und Dauer (auch: kurzfristig, teuer, Tilgung durch Zahlungseingänge)',3))
+ task('7.2','Unterscheide Kontokorrentkredit und Dispositionskredit.', ab('Kontokorrentkredit: für Unternehmen auf dem Geschäftsbankkonto – Dispositionskredit: für Privatkunden auf dem Girokonto.',3))
+ task('7.3','Berechne den Bruttoskonto, den Nettoskonto und den Überweisungsbetrag, wenn Jakob innerhalb der Skontofrist zahlt.', karo('Bruttoskonto: 11.900,00 · 2 : 100 = 238,00 €<br>Nettoskonto: 238,00 : 1,19 = 200,00 € (Steuerberichtigung 38,00 €)<br>Überweisungsbetrag: 11.900,00 – 238,00 = 11.662,00 €',5))
+ task('7.4','Weise rechnerisch nach, dass der Kontokorrentkredit hier günstiger ist als der Lieferantenkredit. Entscheide, wie Jakob zahlen sollte.', karo('Kosten Lieferantenkredit = entgangener Nettoskonto: 200,00 €<br>Kosten Kontokorrentkredit = Zinsen: 58,31 €<br>Vorteil: 200,00 – 58,31 = 141,69 €<br>→ innerhalb der Skontofrist mit dem Kontokorrentkredit zahlen und Skonto abziehen.',6))
+ task('7.5','Begründe, warum Jakob die Rechnung nicht dauerhaft über den Kontokorrentkredit finanzieren sollte.', ab('Der Kontokorrentkredit ist eine teure, kurzfristige Kreditart. Er soll nur kurzfristige Engpässe überbrücken; dauerhaft beansprucht kosten die Zinsen viel Geld und die Kreditlinie fehlt für andere Zahlungen.',4)))}
{check(7)}''')

    # ===== Kapitel 8 =====
    page(f'''{kap(8,'Leasing, Factoring und Förderprogramme')}
{info('''<p>Neben Eigenkapital und klassischen Krediten gibt es weitere Möglichkeiten, an Geld oder Maschinen zu kommen.</p>
<p><b>Leasing</b> = Überlassung von <b>Anlagegütern</b> (Maschinen, Fahrzeuge) gegen Zahlung einer <b>Leasinggebühr</b> (Leasingrate) für die Nutzung.</p>''')}
<div class="fig">{S.leasing_ablauf()}</div>
{info('''<p><b>Vorteile:</b> kein hoher Kapitalbedarf beim Kauf → <b>Liquidität</b> wird geschont; feste Raten → <b>Kostensicherheit</b>; Austausch gegen <b>neueste Technik</b> nach Vertragsende.<br>
<b>Nachteile:</b> <b>kein Eigentum</b>; insgesamt meist <b>teurer als ein Kauf</b>; Bindung an den Vertrag.</p>''')}
{alltag('Leasing kennst du schon','''<p>Viele Arbeitnehmer fahren ein <b>Dienstrad</b>: Der Arbeitgeber least ein E-Bike, die Rate wird vom Gehalt abgezogen, nach drei Jahren wird es zurückgegeben oder abgelöst. Auch viele Autos auf der Straße gehören gar nicht ihren Fahrern, sondern einer Leasinggesellschaft.</p>''')}
{info('''<p><b>Factoring</b> = Verkauf von <b>Forderungen</b> gegenüber Kunden vor ihrer Fälligkeit an ein Finanzierungsinstitut (<b>Factor</b>). Der Factor zahlt den Gegenwert (abzüglich einer Gebühr) <b>sofort</b> aus – die <b>Liquidität</b> verbessert sich. Oft übernimmt er auch das Mahnwesen und das Risiko, dass der Kunde nicht zahlt.</p>''')}
<div class="fig fig80">{S.factoring_ablauf()}</div>
{info('''<p><b>Öffentliche Förderprogramme:</b> Der Staat unterstützt Unternehmen mit <b>Förderkrediten, Zuschüssen und Bürgschaften</b> – in Bayern vor allem über die <b>LfA Förderbank Bayern</b>, bundesweit über die <b>KfW-Bankengruppe</b>. Vorteile: <b>niedrigere Zinsen, längere Laufzeiten</b>, günstigere Rückzahlungsbedingungen. Wichtig: Der Antrag läuft über die <b>Hausbank</b> und muss <b>vor Beginn</b> des Vorhabens gestellt werden.</p>''')}''')

    page(f'''{ueb(8,'Alternative Finanzierungsmöglichkeiten',f'''<table class="t ut3"><tr><th style="width:22%"></th><th>Leasing</th><th>Factoring</th><th>Förderprogramme</th></tr>
<tr><td><b>Was ist das?</b></td><td>{a('Überlassung von Anlagegütern gegen Leasingrate')}</td><td>{a('Verkauf von Forderungen an einen Factor')}</td><td>{a('staatliche Förderkredite, Zuschüsse, Bürgschaften')}</td></tr>
<tr><td><b>Vorteil</b></td><td>{a('schont Liquidität, Kostensicherheit, neueste Technik')}</td><td>{a('sofort Geld → bessere Liquidität')}</td><td>{a('niedrige Zinsen, lange Laufzeiten')}</td></tr>
<tr><td><b>Nachteil / Beachte</b></td><td>{a('kein Eigentum, meist teurer als Kauf')}</td><td>{a('Gebühr mindert den Erlös')}</td><td>{a('Antrag über Hausbank vor Beginn des Vorhabens')}</td></tr></table>''')}
{aufg(8, aufg_kopf() + task('8.1','Ordne den Situationen die passende Finanzierungsmöglichkeit zu: Leasing (L), Factoring (F) oder Förderprogramm (P).', f'''<table class="t"><tr><th>Situation</th><th style="width:20mm">L / F / P</th></tr>
<tr><td>a) Saitgig möchte seine Lieferwagen alle drei Jahre gegen neue Modelle tauschen, ohne sie zu kaufen.</td><td>{a('L')}</td></tr>
<tr><td>b) Ein Musikhaus zahlt erst in 90 Tagen; Jakob braucht das Geld aber sofort.</td><td>{a('F')}</td></tr>
<tr><td>c) Für eine neue, energiesparende Werkhalle sucht Jakob einen besonders zinsgünstigen Kredit.</td><td>{a('P')}</td></tr></table>''')
+ task('8.2','Nenne je einen Vorteil und einen Nachteil des Leasings für Saitgig.', ab('Vorteil, z. B.: Liquidität wird geschont / feste Raten / neueste Technik<br>Nachteil, z. B.: Saitgig wird nicht Eigentümer / insgesamt meist teurer als ein Kauf',3))
+ task('8.3','Jakob hat die neue Werkhalle bereits beim Bauunternehmen in Auftrag gegeben. Erläutere, warum er jetzt keinen Förderkredit mehr bekommt.', ab('Förderkredite müssen über die Hausbank vor Beginn des Vorhabens beantragt werden. Ein bereits begonnenes Vorhaben wird nicht mehr gefördert.',3))
+ task('8.4','Erkläre, wie Factoring die Liquidität von Saitgig verbessert.', ab('Saitgig verkauft die Forderung an den Factor und erhält das Geld sofort statt erst nach 90 Tagen. Damit stehen schneller Mittel zur Verfügung, um eigene Rechnungen termingerecht zu bezahlen.',4)))}
{check(8)}''')

    # ===== Kapitel 9 =====
    page(f'''{kap(9,'Abschluss: Deine Beratung für Saitgig')}
<div class="szenario"><div class="szt">Jakobs Anfrage</div>
<p>„Ich will eine <b>CNC-Fräse für 80.000 €</b> kaufen, damit wir Gitarrenhälse schneller und genauer fräsen können. Die Maschine soll mindestens <b>acht Jahre</b> laufen. Ich habe drei Möglichkeiten – was rätst du mir?“</p></div>
<table class="t opt"><tr><th></th><th>Möglichkeit 1</th><th>Möglichkeit 2</th><th>Möglichkeit 3</th></tr>
<tr><td><b>Art</b></td><td>Kontokorrentkredit</td><td>Annuitätendarlehen, Laufzeit 8 Jahre</td><td>Leasing, Vertrag über 5 Jahre</td></tr>
<tr><td><b>Kosten</b></td><td>9,5 % Zinsen p. a.</td><td>5,2 % Zinsen p. a., kein Disagio</td><td>Leasingrate 1.650,00 € monatlich</td></tr>
<tr><td><b>Besonderheit</b></td><td>sofort verfügbar</td><td>Bank verlangt eine Grundschuld auf das Betriebsgrundstück</td><td>Maschine bleibt Eigentum des Leasinggebers</td></tr></table>
<p class="klein">Nutze auch die Bilanz von Saitgig (Heft, Kapitel 2) und deine Ergebnisse aus den Kapiteln 2, 3 und 6.</p>
{aufg(9, aufg_kopf() + task('9.1','Begründe, warum Möglichkeit 1 für diese Investition nicht geeignet ist.', ab('Die Fräse ist langfristig im Anlagevermögen gebunden, der Kontokorrentkredit ist kurzfristig → Verstoß gegen die Goldene Finanzierungsregel (vgl. 3.2). Außerdem ist er mit 9,5 % teuer und die Kreditlinie fehlt dann für den laufenden Geschäftsverkehr.',4))
+ task('9.2','Ermittle die gesamten Leasingzahlungen bei Möglichkeit 3 und vergleiche sie mit dem Kaufpreis.', karo('1.650,00 · 12 · 5 = 99.000,00 €<br>99.000,00 – 80.000,00 = 19.000,00 € mehr als der Kaufpreis – und die Fräse gehört Saitgig danach trotzdem nicht.',4))
+ task('9.3','Die Bank zögert wegen der niedrigen Eigenkapitalquote. Nenne zwei Möglichkeiten, wie Jakob die Eigenkapitalquote erhöhen kann.', ab('z. B.: Gewinne im Unternehmen lassen (Selbstfinanzierung); privates Geld einlegen; einen stillen Gesellschafter aufnehmen',3)))}''')

    page(f'''{aufg(9, task('9.4','Schreibe Jakob eine Beratungs-E-Mail. Nimm darin begründet Stellung, welche Möglichkeit du ihm empfiehlst. Gehe auf mindestens drei Gesichtspunkte aus diesem Heft ein (z. B. Goldene Finanzierungsregel, Kosten, Liquidität, Eigentum, Eigenkapitalquote, Förderprogramme).', f'''<div class="mail"><div class="mailk"><b>An:</b> jakob.seite@saitgig.example &nbsp;·&nbsp; <b>Betreff:</b> Meine Empfehlung zur Finanzierung der CNC-Fräse</div>
{ab('Hallo Jakob,<br>ich empfehle dir Möglichkeit 2, das Annuitätendarlehen. Die Fräse nutzt du acht Jahre, und das Darlehen läuft genauso lange – damit hältst du die Goldene Finanzierungsregel ein. Mit 5,2 % ist es deutlich günstiger als der Kontokorrentkredit (9,5 %), den du für kurzfristige Engpässe frei halten solltest. Die Rate ist jedes Jahr gleich hoch, du kannst also gut planen. Anders als beim Leasing gehört dir die Fräse am Ende; Leasing würde allein in fünf Jahren 99.000 € kosten. Als Sicherheit kannst du die Grundschuld auf dein Grundstück anbieten.<br>Zwei Tipps noch: Frag deine Hausbank vor dem Kauf nach einem Förderkredit der LfA – der könnte noch günstiger sein. Und lass einen Teil deines Gewinns im Unternehmen, damit deine Eigenkapitalquote (30 %, Branche 38 %) steigt.<br>Viele Grüße<br><i>(Auch vertretbar: Leasing, wenn Liquidität und neueste Technik wichtiger sind – dann müssen höhere Kosten und fehlendes Eigentum abgewogen werden.)</i>',17)}</div>'''))}
{check(9,'Vergleiche deine E-Mail mit der Muster-E-Mail: Hast du eine klare Empfehlung gegeben und sie mit mindestens drei Argumenten begründet?')}
<div class="ende">Geschafft! Du bist jetzt bereit, Jakob zu beraten.</div>''')


# ---------- Rahmen ----------
CSS = open('style.css').read()

def zeilen(html):
    import re
    def tr(m):
        t = m.group(0)
        tds = re.findall(r'<td[^>]*>.*?</td>', t, flags=re.S)
        if 'class="a lang"' not in t and not any(x.count('class="a') >= 2 for x in tds):
            return t
        return re.sub(r'(<td[^>]*>)((?:(?!</td>).)*class="a(?: lang)?"(?:(?!</td>).)*)(</td>)', r'\1<div class="zl">\2</div>\3', t, flags=re.S)
    return re.sub(r'<tr>.*?</tr>', tr, html, flags=re.S)

def doc(title, body, cls):
    body = zeilen(body)
    return f'''<!doctype html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title><style>{CSS}</style></head><body class="{cls}">{body}</body></html>'''

def heft(mode):
    global MODE
    MODE = mode
    LSG.clear()
    inhalt()
    for k,v in KAPSEITE.items():
        PAGES[0]=PAGES[0].replace('§S%d§'%k,str(v))
    b5=str(KAPSEITE[2]+1)
    PAGES[:]=[p.replace('§S5§',b5) for p in PAGES]
    for k in LSG: LSG[k]=[x.replace('§S5§',b5) for x in LSG[k]]
    cut = KAPSEITE[7]-1
    return render(PAGES[:cut],'Möglichkeiten der Finanzierung · Saitgig'), render(PAGES[cut:],'Möglichkeiten der Finanzierung · Saitgig · Ergänzung Kap. 7–9')

def render(pages, fuss):
    n=len(pages)
    return ''.join(f'<div class="page">{p}<div class="foot"><span>{fuss}</span><span>Seite {k+1} von {n}</span></div></div>' for k,p in enumerate(pages))

TITEL = {1:'Finanzierung und Liquidität',2:'Eigenkapitalquote',3:'Goldene Finanzierungsregel',4:'Eigen- und Fremdfinanzierung',5:'Kredite bei der Bank',6:'Darlehensarten',7:'Kontokorrent-, Dispo- und Lieferantenkredit',8:'Leasing, Factoring, Förderprogramme',9:'Abschluss: Beratung für Saitgig'}

def blaetter(ks):
    return ''.join(f'<div class="page lsheet"><div class="lnr">L{k}</div><div class="lkopf">Lösungsblatt {k} · {TITEL[k]}</div><div class="lhinw">Nicht hineinschreiben – bitte zurücklegen!</div>{"".join(LSG[k])}</div>' for k in ks)

FLOW_CSS='''
@page{size:A4;margin:10mm 12mm 10mm}
body.flow{background:#fff}
.flow .page{width:auto;max-width:186mm;height:auto;padding:0;margin:0 auto;overflow:visible;break-after:auto;page-break-after:auto}
.flow .foot{display:none}
.flow .kap{margin-top:5mm;break-after:avoid;page-break-after:avoid}
.flow .task,.flow .fig,.flow .ueb,.flow .alltag,.flow .check,.flow .t,.flow .steck,.flow .plan,.flow .plan1,.flow .autos,.flow .drei,.flow .formel,.flow .info p,.flow li{break-inside:avoid;page-break-inside:avoid}
.flow .ak{break-after:avoid}
.flow .plan th:nth-child(3),.flow .plan td:nth-child(3){display:none}
@media screen{.flow .page{padding:0 4mm}}
'''
def flow(html):
    import re
    html=re.sub(r', S\. \d+\)',')',html)
    return html.replace('</style>',FLOW_CSS+'</style>',1).replace('<body class="s">','<body class="s flow">').replace('<body class="l">','<body class="l flow">')

if __name__ == '__main__':
    import os, glob
    for f in glob.glob('out/*'): os.remove(f)
    s1,s2 = heft('s')
    l1,l2 = heft('l')
    W=lambda n,t,b,c: open('out/'+n,'w').write(doc(t,b,c))
    W('Heft_Finanzierung_Kap1-6_Schueler.html','Finanzierung – Selbstlernheft',s1,'s')
    W('Heft_Finanzierung_Kap1-6_Lehrkraft.html','Finanzierung – Selbstlernheft (Lösung)',l1,'l')
    W('Loesungsblaetter_L1-L6.html','Finanzierung – Lösungsblätter L1–L6',blaetter(range(1,7)),'l')
    W('Ergaenzung_Kap7-9_Schueler.html','Finanzierung – Ergänzung Kap. 7–9',s2,'s')
    W('Ergaenzung_Kap7-9_Lehrkraft.html','Finanzierung – Ergänzung Kap. 7–9 (Lösung)',l2,'l')
    W('Loesungsblaetter_L7-L9.html','Finanzierung – Lösungsblätter L7–L9',blaetter(range(7,10)),'l')
    for n in ['Heft_Finanzierung_Kap1-6_Schueler','Heft_Finanzierung_Kap1-6_Lehrkraft','Ergaenzung_Kap7-9_Schueler','Ergaenzung_Kap7-9_Lehrkraft']:
        h=open('out/'+n+'.html').read()
        open('out/'+n+'_ohne_Seitenumbrueche.html','w').write(flow(h))
    print('ok', KAPSEITE)
