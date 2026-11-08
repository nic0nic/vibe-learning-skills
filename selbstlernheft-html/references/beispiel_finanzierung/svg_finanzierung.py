"""Schwarz-weiß-taugliche SVG-Grafiken für das Finanzierungsheft."""
_n = [0]


def _id():
    _n[0] += 1
    return f"g{_n[0]}"


def defs(i):
    return f'''<defs>
<marker id="{i}a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#000"/></marker>
<pattern id="{i}h" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="7" height="7" fill="#fff"/><line x1="0" y1="0" x2="0" y2="7" stroke="#000" stroke-width="1.6"/></pattern>
<pattern id="{i}d" width="5" height="5" patternUnits="userSpaceOnUse"><rect width="5" height="5" fill="#fff"/><circle cx="2.5" cy="2.5" r="0.9" fill="#000"/></pattern>
</defs>'''


T = 'font-family="Arial,Helvetica,sans-serif"'


def guitar(w="34mm"):
    i = _id()
    return f'''<svg viewBox="0 0 160 60" style="width:{w}" xmlns="http://www.w3.org/2000/svg">
<g transform="rotate(-18 80 30)">
<rect x="58" y="25" width="78" height="9" fill="#555" stroke="#000"/>
<path d="M136,22 L156,18 L158,40 L136,37 z" fill="#000"/>
<g fill="#fff" stroke="#000">{''.join(f'<circle cx="{142+k*5}" cy="{17+k*0.4}" r="2"/><circle cx="{142+k*5}" cy="{41-k*0.4}" r="2"/>' for k in range(3))}</g>
<path d="M60,30 C60,10 42,8 34,14 C26,5 4,6 4,30 C4,54 26,55 34,46 C42,52 60,50 60,30 z" fill="#fff" stroke="#000" stroke-width="2.5"/>
<circle cx="40" cy="30" r="7" fill="#000"/>
<rect x="14" y="24" width="5" height="12" fill="#000"/>
{''.join(f'<line x1="16" y1="{27+k*2}" x2="156" y2="{27+k*2}" stroke="#999" stroke-width="0.4"/>' for k in range(4))}
</g></svg>'''


def bilanz_schema():
    i = _id()
    return f'''<svg viewBox="0 0 620 250" style="width:100%" xmlns="http://www.w3.org/2000/svg" {T}>{defs(i)}
<text x="310" y="20" text-anchor="middle" font-size="17" font-weight="bold">Bilanz</text>
<line x1="60" y1="30" x2="560" y2="30" stroke="#000" stroke-width="2"/><line x1="310" y1="30" x2="310" y2="150" stroke="#000" stroke-width="2"/>
<text x="65" y="25" font-size="13" font-weight="bold">AKTIVA</text><text x="555" y="25" font-size="13" font-weight="bold" text-anchor="end">PASSIVA</text>
<rect x="70" y="40" width="230" height="45" fill="#e6e6e6" stroke="#000"/><text x="185" y="68" text-anchor="middle" font-size="15" font-weight="bold">Anlagevermögen</text>
<rect x="70" y="92" width="230" height="45" fill="#fff" stroke="#000"/><text x="185" y="120" text-anchor="middle" font-size="15" font-weight="bold">Umlaufvermögen</text>
<rect x="320" y="40" width="230" height="45" fill="#ddd" stroke="#000"/><text x="435" y="68" text-anchor="middle" font-size="15" font-weight="bold">Eigenkapital</text>
<rect x="320" y="92" width="230" height="45" fill="#fff" stroke="#000"/><text x="435" y="120" text-anchor="middle" font-size="15" font-weight="bold">Fremdkapital</text>
<path d="M435,140 L435,175 L185,175 L185,145" fill="none" stroke="#000" stroke-width="2.5" marker-end="url(#{i}a)"/>
<text x="310" y="168" text-anchor="middle" font-size="12" font-style="italic">das beschaffte Kapital wird im Vermögen angelegt</text>
<rect x="20" y="190" width="285" height="55" rx="6" fill="#fff" stroke="#000" stroke-width="1.5"/>
<text x="162" y="210" text-anchor="middle" font-size="14" font-weight="bold">INVESTIERUNG = Mittelverwendung</text>
<text x="162" y="230" text-anchor="middle" font-size="12.5">„Wofür wird das Geld verwendet?“</text>
<rect x="315" y="190" width="285" height="55" rx="6" fill="#eee" stroke="#000" stroke-width="1.5"/>
<text x="457" y="210" text-anchor="middle" font-size="14" font-weight="bold">FINANZIERUNG = Mittelherkunft</text>
<text x="457" y="230" text-anchor="middle" font-size="12.5">„Woher kommt das Geld?“</text>
</svg>'''


def car_old():
    i = _id()
    return f'''<svg viewBox="0 0 220 110" style="width:100%" xmlns="http://www.w3.org/2000/svg" {T}>{defs(i)}
<path d="M12,75 L12,52 Q14,44 34,41 L62,20 L132,18 Q146,19 160,40 L196,45 Q206,47 206,62 L206,75 z" fill="#fff" stroke="#000" stroke-width="2.5"/>
<path d="M68,25 L128,23 Q138,25 148,40 L52,41 z" fill="#ddd" stroke="#000" stroke-width="1.5"/><line x1="99" y1="23" x2="99" y2="41" stroke="#000" stroke-width="2"/>
<line x1="99" y1="44" x2="99" y2="73" stroke="#000"/><rect x="104" y="50" width="12" height="3" fill="#000"/>
<g fill="#000"><circle cx="40" cy="56" r="2.2"/><circle cx="46" cy="61" r="1.5"/><circle cx="178" cy="66" r="2"/></g>
<path d="M140,58 q6,-4 10,1 q4,5 9,0" fill="none" stroke="#000"/>
<rect x="198" y="52" width="9" height="6" fill="#fff" stroke="#000"/>
<g><circle cx="52" cy="78" r="16" fill="#000"/><circle cx="52" cy="78" r="7" fill="#999"/><circle cx="168" cy="78" r="16" fill="#000"/><circle cx="168" cy="78" r="7" fill="#999"/></g>
<path d="M6,95 q4,-6 8,0 q4,6 8,0" fill="none" stroke="#000"/><text x="110" y="106" text-anchor="middle" font-size="11" font-style="italic">Baujahr 2010 · 180.000 km</text>
</svg>'''


def car_new():
    i = _id()
    return f'''<svg viewBox="0 0 240 110" style="width:100%" xmlns="http://www.w3.org/2000/svg" {T}>{defs(i)}
<path d="M6,72 L6,56 Q10,46 44,43 L82,24 Q118,15 152,22 Q170,28 184,42 L224,47 Q236,50 236,64 L236,72 z" fill="#555" stroke="#000" stroke-width="2.5"/>
<path d="M88,28 Q118,19 148,25 Q160,30 170,42 L64,43 z" fill="#ddd" stroke="#000" stroke-width="1.5"/><line x1="122" y1="22" x2="118" y2="43" stroke="#000" stroke-width="3"/>
<path d="M30,52 L220,54" stroke="#fff" stroke-width="2" opacity="0.8"/><path d="M60,40 Q120,30 175,40" stroke="#fff" stroke-width="1" fill="none" opacity="0.6"/>
<rect x="224" y="52" width="12" height="5" fill="#fff" stroke="#000"/>
{''.join(f'<g transform="translate({cx},76)"><circle r="17" fill="#000"/><circle r="10" fill="#fff"/>' + ''.join(f'<line x1="0" y1="0" x2="{9*__import__("math").cos(k*1.2566):.1f}" y2="{9*__import__("math").sin(k*1.2566):.1f}" stroke="#000" stroke-width="2.5"/>' for k in range(5)) + '<circle r="2.5" fill="#000"/></g>' for cx in (56, 190))}
<g stroke="#000" stroke-width="1.3"><line x1="200" y1="10" x2="206" y2="4"/><line x1="210" y1="14" x2="218" y2="10"/><line x1="192" y1="8" x2="193" y2="1"/></g>
<text x="120" y="106" text-anchor="middle" font-size="11" font-style="italic">Neuwagen · 0 km · Vollausstattung</text>
</svg>'''


def ek_balken(ek, mode, label):
    """Senkrechter 100-%-Balken; im Lösungsmodus ist der EK-Anteil schraffiert."""
    i = _id()
    H, y0 = 160, 20
    ticks = ''.join(f'<line x1="58" y1="{y0+H-k*H/10:.1f}" x2="66" y2="{y0+H-k*H/10:.1f}" stroke="#000"/><text x="54" y="{y0+H-k*H/10+4:.1f}" font-size="10" text-anchor="end">{k*10}</text>' for k in range(0, 11, 2))
    fill = ''
    if mode == 'l':
        h = H * ek / 100
        fill = (f'<rect class="ans" x="66" y="{y0+H-h:.1f}" width="70" height="{h:.1f}" fill="url(#{i}h)" stroke="#000"/>'
                f'<line class="ans" x1="66" y1="{y0+H-h:.1f}" x2="136" y2="{y0+H-h:.1f}" stroke="#1565c0" stroke-width="2.5"/>'
                f'<text class="ans" x="142" y="{y0+H-h/2+4:.1f}" font-size="13" fill="#1565c0" font-family="Courier New,monospace" font-weight="bold">EK {str(round(ek,1)).replace(".",",")} %</text>')
    return f'''<svg viewBox="0 0 230 210" style="width:100%" xmlns="http://www.w3.org/2000/svg" {T}>{defs(i)}
<rect x="66" y="{y0}" width="70" height="{H}" fill="#fff" stroke="#000" stroke-width="2"/>{fill}{ticks}
<text x="20" y="12" font-size="10">%</text>
<text x="101" y="{y0+H+22}" text-anchor="middle" font-size="13" font-weight="bold">{label}</text>
</svg>'''


def goldene_regel():
    i = _id()
    return f'''<svg viewBox="0 0 620 270" style="width:100%" xmlns="http://www.w3.org/2000/svg" {T}>{defs(i)}
<text x="210" y="18" text-anchor="middle" font-size="13" font-weight="bold">AKTIVA (Vermögen)</text>
<text x="410" y="18" text-anchor="middle" font-size="13" font-weight="bold">PASSIVA (Kapital)</text>
<rect x="140" y="28" width="140" height="140" fill="url(#{i}h)" stroke="#000" stroke-width="2"/>
<rect x="140" y="168" width="140" height="80" fill="#fff" stroke="#000" stroke-width="2"/>
<rect x="340" y="28" width="140" height="70" fill="url(#{i}h)" stroke="#000" stroke-width="2"/>
<rect x="340" y="98" width="140" height="90" fill="url(#{i}h)" stroke="#000" stroke-width="2"/>
<rect x="340" y="188" width="140" height="60" fill="#fff" stroke="#000" stroke-width="2"/>
<g font-weight="bold" font-size="14" text-anchor="middle">
<rect x="150" y="86" width="120" height="24" fill="#fff"/><text x="210" y="103">Anlagevermögen</text>
<text x="210" y="213">Umlaufvermögen</text>
<rect x="350" y="52" width="120" height="22" fill="#fff"/><text x="410" y="68">Eigenkapital</text>
<rect x="345" y="130" width="130" height="38" fill="#fff"/><text x="410" y="146">langfristiges</text><text x="410" y="163">Fremdkapital</text>
<text x="410" y="215">kurzfristiges</text><text x="410" y="232">Fremdkapital</text></g>
<path d="M130,30 L118,30 L118,166 L130,166" fill="none" stroke="#000" stroke-width="2"/>
<text x="110" y="92" text-anchor="end" font-size="12.5">lange gebunden</text><text x="110" y="108" text-anchor="end" font-size="12.5">(Gebäude,</text><text x="110" y="123" text-anchor="end" font-size="12.5">Maschinen)</text>
<path d="M130,170 L118,170 L118,246 L130,246" fill="none" stroke="#000" stroke-width="2"/>
<text x="110" y="205" text-anchor="end" font-size="12.5">kurz gebunden</text><text x="110" y="221" text-anchor="end" font-size="12.5">(Vorräte, Bank)</text>
<path d="M490,30 L502,30 L502,186 L490,186" fill="none" stroke="#000" stroke-width="2"/>
<text x="510" y="102" font-size="12.5">steht lange</text><text x="510" y="118" font-size="12.5">zur Verfügung</text>
<path d="M490,190 L502,190 L502,246 L490,246" fill="none" stroke="#000" stroke-width="2"/>
<text x="510" y="215" font-size="12.5">muss bald</text><text x="510" y="231" font-size="12.5">zurück</text>
<line x1="282" y1="100" x2="338" y2="100" stroke="#000" stroke-width="2.5" marker-start="url(#{i}a)" marker-end="url(#{i}a)"/>
<line x1="282" y1="225" x2="338" y2="225" stroke="#000" stroke-width="2.5" marker-start="url(#{i}a)" marker-end="url(#{i}a)"/>
<text x="310" y="264" text-anchor="middle" font-size="11.5" font-style="italic">schraffiert = langfristig</text>
</svg>'''


def kredit_ablauf():
    i = _id()
    return f'''<svg viewBox="0 0 620 255" style="width:100%" xmlns="http://www.w3.org/2000/svg" {T}>{defs(i)}
<rect x="10" y="70" width="170" height="120" rx="8" fill="#fff" stroke="#000" stroke-width="2"/>
<text x="95" y="95" text-anchor="middle" font-size="14" font-weight="bold">Kreditnehmer</text><text x="95" y="112" text-anchor="middle" font-size="12">(Schuldner, z. B. Saitgig)</text>
<text x="95" y="140" text-anchor="middle" font-size="12">stellt Kreditantrag,</text><text x="95" y="156" text-anchor="middle" font-size="12">legt Unterlagen vor,</text><text x="95" y="172" text-anchor="middle" font-size="12">bietet Sicherheiten</text>
<rect x="390" y="70" width="220" height="120" rx="8" fill="#eee" stroke="#000" stroke-width="2"/>
<text x="500" y="95" text-anchor="middle" font-size="14" font-weight="bold">Kreditgeber (Bank)</text><text x="500" y="112" text-anchor="middle" font-size="12">(Gläubiger)</text>
<text x="500" y="140" text-anchor="middle" font-size="12">prüft Kreditfähigkeit</text><text x="500" y="156" text-anchor="middle" font-size="12">und Kreditwürdigkeit,</text><text x="500" y="172" text-anchor="middle" font-size="12">verlangt Sicherheiten</text>
<rect x="420" y="2" width="160" height="40" rx="6" fill="#fff" stroke="#000" stroke-dasharray="5 3"/>
<text x="500" y="19" text-anchor="middle" font-size="12" font-weight="bold">Auskunftei (z. B. SCHUFA)</text><text x="500" y="35" text-anchor="middle" font-size="11">sammelt Daten zur Zahlungsmoral</text>
<line x1="500" y1="44" x2="500" y2="68" stroke="#000" stroke-dasharray="4 3" marker-end="url(#{i}a)"/>
<line x1="182" y1="90" x2="388" y2="90" stroke="#000" stroke-width="2" marker-end="url(#{i}a)"/><text x="285" y="83" text-anchor="middle" font-size="12.5">① Kreditantrag</text>
<line x1="388" y1="130" x2="182" y2="130" stroke="#000" stroke-width="3" marker-end="url(#{i}a)"/><text x="285" y="123" text-anchor="middle" font-size="12.5" font-weight="bold">② Kredit (Geld)</text>
<line x1="182" y1="172" x2="388" y2="172" stroke="#000" stroke-width="3" marker-end="url(#{i}a)"/><text x="285" y="165" text-anchor="middle" font-size="12.5" font-weight="bold">③ Zinsen + Tilgung</text>
<rect x="190" y="200" width="190" height="48" rx="6" fill="#fff" stroke="#000" stroke-width="1.5"/>
<text x="285" y="220" text-anchor="middle" font-size="13" font-weight="bold">= Schuldendienst</text><text x="285" y="238" text-anchor="middle" font-size="11.5">Zinsen = Preis · Tilgung = Rückzahlung</text>
<line x1="285" y1="176" x2="285" y2="198" stroke="#000"/>
</svg>'''


def darlehen_chart(art):
    """Gestapelte Säulen: Tilgung grau, Zinsen schraffiert. 40.000 €, 4 Jahre, 8 %."""
    i = _id()
    data = {
        'Abzahlungsdarlehen': [(10000, 3200), (10000, 2400), (10000, 1600), (10000, 800)],
        'Annuitätendarlehen': [(8876.83, 3200), (9586.98, 2489.85), (10353.94, 1722.90), (11182.25, 894.58)],
        'Festdarlehen': [(0, 3200), (0, 3200), (0, 3200), (40000, 3200)],
    }[art]
    sc, base = 7.5 / 1000, 135
    out = []
    for k, (t, z) in enumerate(data):
        x = 28 + k * 38
        if t > 15000:  # gekappte Säule
            ht = 105
            out.append(f'<rect x="{x}" y="{base-ht}" width="30" height="{ht}" fill="#999" stroke="#000"/>')
            out.append(f'<rect x="{x}" y="{base-ht-z*sc:.1f}" width="30" height="{z*sc:.1f}" fill="url(#{i}h)" stroke="#000"/>')
            out.append(f'<path d="M{x-3},{base-60} l12,-6 l12,6 l12,-6" stroke="#fff" stroke-width="5" fill="none"/><path d="M{x-3},{base-60} l12,-6 l12,6 l12,-6" stroke="#000" fill="none"/>')
        else:
            ht = t * sc
            if ht:
                out.append(f'<rect x="{x}" y="{base-ht:.1f}" width="30" height="{ht:.1f}" fill="#999" stroke="#000"/>')
            out.append(f'<rect x="{x}" y="{base-ht-z*sc:.1f}" width="30" height="{z*sc:.1f}" fill="url(#{i}h)" stroke="#000"/>')
        out.append(f'<text x="{x+15}" y="{base+14}" text-anchor="middle" font-size="11">{k+1}</text>')
    return f'''<svg viewBox="0 0 200 175" style="width:100%" xmlns="http://www.w3.org/2000/svg" {T}>{defs(i)}
<line x1="22" y1="10" x2="22" y2="{base}" stroke="#000" marker-start="url(#{i}a)"/><line x1="22" y1="{base}" x2="195" y2="{base}" stroke="#000"/>
<text x="4" y="12" font-size="10">€</text><text x="199" y="{base+14}" font-size="10" text-anchor="end">Jahr</text>
{''.join(out)}
<text x="100" y="168" text-anchor="middle" font-size="12.5" font-weight="bold">{art}</text>
</svg>'''


def legende_darlehen():
    i = _id()
    return f'''<svg class="leg" viewBox="0 0 330 22" style="width:85mm" xmlns="http://www.w3.org/2000/svg" {T}>{defs(i)}
<rect x="2" y="4" width="16" height="13" fill="#999" stroke="#000"/><text x="24" y="15" font-size="12">Tilgung</text>
<rect x="100" y="4" width="16" height="13" fill="url(#{i}h)" stroke="#000"/><text x="122" y="15" font-size="12">Zinsen</text>
<text x="190" y="15" font-size="11" font-style="italic">Säule = Rate eines Jahres</text></svg>'''


def kontokorrent_chart():
    i = _id()
    # Kontostand in Tsd. €; y = 70 - wert*1.5
    pts = [(0, 25), (60, 25), (60, -20), (140, -20), (140, -45), (230, -45), (230, 10), (300, 10), (300, -60), (360, -60), (360, -82), (410, -82), (410, -35), (480, -35), (480, 15), (560, 15)]
    def y(v): return 70 - v * 1.5
    poly = ' '.join(f'{40+x},{y(v):.1f}' for x, v in pts)
    neg = f'M40,{y(0)} ' + ' '.join(f'L{40+x},{y(min(v,0)):.1f}' for x, v in pts) + f' L600,{y(0)} z'
    return f'''<svg viewBox="0 0 620 225" style="width:100%" xmlns="http://www.w3.org/2000/svg" {T}>{defs(i)}
<path d="{neg}" fill="url(#{i}h)" stroke="none"/>
<line x1="40" y1="{y(0)}" x2="605" y2="{y(0)}" stroke="#000" stroke-width="1.5" marker-end="url(#{i}a)"/><text x="600" y="{y(0)-6}" text-anchor="end" font-size="11">Zeit</text>
<line x1="40" y1="200" x2="40" y2="5" stroke="#000" stroke-width="1.5" marker-end="url(#{i}a)"/><text x="8" y="14" font-size="11">Konto-</text><text x="8" y="27" font-size="11">stand</text>
<text x="35" y="{y(0)+4}" text-anchor="end" font-size="11">0 €</text>
<line x1="40" y1="{y(-70)}" x2="600" y2="{y(-70)}" stroke="#000" stroke-width="2" stroke-dasharray="9 5"/>
<text x="230" y="{y(-70)-6}" text-anchor="middle" font-size="12" font-weight="bold">Kreditlinie (Limit) – 70.000 €</text>
<polyline points="{poly}" fill="none" stroke="#000" stroke-width="2.5"/>
<rect x="58" y="186" width="14" height="11" fill="url(#{i}h)" stroke="#000"/><text x="78" y="196" font-size="12">schraffiert = Kontokorrentkredit beansprucht → Zinsen</text>
<line x1="452" y1="{y(-78)}" x2="470" y2="{y(-70)+8}" stroke="#000"/><text x="472" y="{y(-70)+18}" font-size="11.5">geduldete Überziehung</text><text x="472" y="{y(-70)+31}" font-size="11.5">(noch teurer!)</text>
<text x="100" y="{y(25)-6}" text-anchor="middle" font-size="11">Guthaben</text>
<text x="270" y="{y(10)-6}" text-anchor="middle" font-size="11">Kunde zahlt ein</text>
</svg>'''


def lieferanten_zeitstrahl():
    i = _id()
    return f'''<svg viewBox="0 0 620 125" style="width:100%" xmlns="http://www.w3.org/2000/svg" {T}>{defs(i)}
<rect x="40" y="30" width="170" height="40" fill="#fff" stroke="#000" stroke-width="2"/>
<rect x="210" y="30" width="370" height="40" fill="url(#{i}h)" stroke="#000" stroke-width="2"/>
<text x="125" y="48" text-anchor="middle" font-size="12.5" font-weight="bold">10 Tage Skontofrist</text><text x="125" y="63" text-anchor="middle" font-size="11.5">Lieferantenkredit kostenlos</text>
<rect x="250" y="35" width="290" height="30" fill="#fff"/>
<text x="395" y="48" text-anchor="middle" font-size="12.5" font-weight="bold">20 Tage bis zum Zahlungsziel</text><text x="395" y="62" text-anchor="middle" font-size="11.5">Preis des Kredits = entgangenes Skonto</text>
<line x1="20" y1="90" x2="605" y2="90" stroke="#000" stroke-width="1.5" marker-end="url(#{i}a)"/>
<g stroke="#000" stroke-width="2"><line x1="40" y1="84" x2="40" y2="96"/><line x1="210" y1="84" x2="210" y2="96"/><line x1="580" y1="84" x2="580" y2="96"/></g>
<g font-size="12" text-anchor="middle"><text x="40" y="112">02.11. Rechnung</text><text x="210" y="112">12.11. Ende Skontofrist</text><text x="560" y="112">02.12. Zahlungsziel</text></g>
<text x="40" y="20" font-size="11.5" font-style="italic">Zahlung mit 2 % Skonto möglich</text><text x="580" y="20" text-anchor="end" font-size="11.5" font-style="italic">Zahlung „rein netto“ ohne Abzug</text>
</svg>'''


def leasing_ablauf():
    i = _id()
    return f'''<svg viewBox="0 0 620 235" style="width:100%" xmlns="http://www.w3.org/2000/svg" {T}>{defs(i)}
<rect x="10" y="10" width="170" height="60" rx="8" fill="#eee" stroke="#000" stroke-width="2"/><text x="95" y="36" text-anchor="middle" font-size="14" font-weight="bold">Leasingnehmer</text><text x="95" y="54" text-anchor="middle" font-size="12">(Saitgig)</text>
<rect x="440" y="10" width="170" height="60" rx="8" fill="#fff" stroke="#000" stroke-width="2"/><text x="525" y="36" text-anchor="middle" font-size="14" font-weight="bold">Leasinggeber</text><text x="525" y="54" text-anchor="middle" font-size="12">(Leasinggesellschaft)</text>
<rect x="225" y="165" width="170" height="60" rx="8" fill="#fff" stroke="#000" stroke-width="2"/><text x="310" y="191" text-anchor="middle" font-size="14" font-weight="bold">Hersteller</text><text x="310" y="209" text-anchor="middle" font-size="12">(z. B. Maschinenbauer)</text>
<line x1="182" y1="25" x2="438" y2="25" stroke="#000" stroke-width="2" marker-end="url(#{i}a)"/><text x="310" y="19" text-anchor="middle" font-size="12">① Leasingvertrag</text>
<line x1="438" y1="58" x2="182" y2="58" stroke="#000" stroke-width="2" marker-end="url(#{i}a)"/><text x="310" y="52" text-anchor="middle" font-size="12">④ monatliche Leasingraten</text>
<line x1="500" y1="72" x2="390" y2="163" stroke="#000" stroke-width="2" marker-end="url(#{i}a)"/><text x="470" y="125" font-size="12">② kauft und</text><text x="470" y="140" font-size="12">bezahlt Maschine</text>
<line x1="235" y1="163" x2="120" y2="72" stroke="#000" stroke-width="2" marker-end="url(#{i}a)"/><text x="40" y="125" font-size="12">③ liefert Maschine</text><text x="40" y="140" font-size="12">direkt zum Nutzer</text>
<text x="310" y="100" text-anchor="middle" font-size="12" font-style="italic">Eigentümer bleibt der Leasinggeber –</text><text x="310" y="116" text-anchor="middle" font-size="12" font-style="italic">Saitgig darf die Maschine nur nutzen</text>
</svg>'''


def factoring_ablauf():
    i = _id()
    return f'''<svg viewBox="0 0 620 175" style="width:100%" xmlns="http://www.w3.org/2000/svg" {T}>{defs(i)}
<rect x="10" y="60" width="140" height="50" rx="8" fill="#eee" stroke="#000" stroke-width="2"/><text x="80" y="90" text-anchor="middle" font-size="14" font-weight="bold">Saitgig</text>
<rect x="240" y="60" width="140" height="50" rx="8" fill="#fff" stroke="#000" stroke-width="2"/><text x="310" y="83" text-anchor="middle" font-size="14" font-weight="bold">Factor</text><text x="310" y="100" text-anchor="middle" font-size="11">(Finanzierungsinstitut)</text>
<rect x="470" y="60" width="140" height="50" rx="8" fill="#fff" stroke="#000" stroke-width="2"/><text x="540" y="90" text-anchor="middle" font-size="14" font-weight="bold">Kunde</text>
<path d="M80,58 Q310,-2 540,58" fill="none" stroke="#000" stroke-width="1.5" marker-end="url(#{i}a)"/><text x="310" y="16" text-anchor="middle" font-size="11.5">① liefert Gitarren auf Rechnung (Zahlungsziel 90 Tage)</text>
<line x1="152" y1="72" x2="238" y2="72" stroke="#000" stroke-width="2" marker-end="url(#{i}a)"/><text x="195" y="52" text-anchor="middle" font-size="11">② verkauft</text><text x="195" y="65" text-anchor="middle" font-size="11">Forderung</text>
<line x1="238" y1="98" x2="152" y2="98" stroke="#000" stroke-width="3" marker-end="url(#{i}a)"/>
<text x="195" y="128" text-anchor="middle" font-size="11.5" font-weight="bold">③ sofort Geld</text><text x="195" y="143" text-anchor="middle" font-size="11">(minus Gebühr)</text>
<line x1="468" y1="85" x2="382" y2="85" stroke="#000" stroke-width="2" marker-end="url(#{i}a)"/><text x="425" y="128" text-anchor="middle" font-size="11.5">④ zahlt nach</text><text x="425" y="143" text-anchor="middle" font-size="11.5">90 Tagen</text>
</svg>'''
