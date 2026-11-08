"""Schwarz-weiß-taugliche SVG-Grundbausteine (Schraffur statt Farbe, Pfeile, Kästen, Säulen, Zeitstrahl).
Konvention: viewBox-Breite 620 ≈ volle Satzbreite (182 mm), Schrift 11–15 Einheiten.
Vollständige Beispiele (Bilanz, Autos, Goldene Regel, Kreditablauf, Darlehenssäulen, Kontoverlauf,
Leasing/Factoring-Dreieck): references/beispiel_finanzierung/svg_finanzierung.py"""
_n = [0]
T = 'font-family="Arial,Helvetica,sans-serif"'

def _id():
    _n[0] += 1
    return f"g{_n[0]}"

def defs(i):
    """Pfeilspitze url(#<i>a), Schraffur url(#<i>h). Keine Punktraster hinter Text verwenden (unleserlich)."""
    return f'''<defs>
<marker id="{i}a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#000"/></marker>
<pattern id="{i}h" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="7" height="7" fill="#fff"/><line x1="0" y1="0" x2="0" y2="7" stroke="#000" stroke-width="1.6"/></pattern>
</defs>'''

def svg(inner, w=620, h=250, i=None, style='width:100%'):
    i = i or _id()
    return f'<svg viewBox="0 0 {w} {h}" style="{style}" xmlns="http://www.w3.org/2000/svg" {T}>{defs(i)}{inner.replace("§", i)}</svg>'

def box(x, y, w, h, titel, unter='', fill='#fff'):
    """Kasten mit fettem Titel und optionaler Unterzeile. fill: '#fff', '#eee' oder 'url(#§h)' (Schraffur)."""
    u = f'<text x="{x+w/2}" y="{y+h/2+16}" text-anchor="middle" font-size="12">{unter}</text>' if unter else ''
    ty = y + h/2 + (0 if unter else 5)
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{fill}" stroke="#000" stroke-width="2"/>'
            f'<text x="{x+w/2}" y="{ty}" text-anchor="middle" font-size="14" font-weight="bold">{titel}</text>{u}')

def pfeil(x1, y1, x2, y2, text='', dx=0, dy=-7, dick=2):
    t = f'<text x="{(x1+x2)/2+dx}" y="{(y1+y2)/2+dy}" text-anchor="middle" font-size="12">{text}</text>' if text else ''
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#000" stroke-width="{dick}" marker-end="url(#§a)"/>{t}'

def saeulen(werte, labels, titel='', hoehe=120, legende=('Tilgung', 'Zinsen')):
    """Gestapelte Säulen: werte = [(unten, oben), ...]; unten grau, oben schraffiert."""
    mx = max(u + o for u, o in werte) or 1
    sc = hoehe / mx; base = hoehe + 15; out = []
    for k, (u, o) in enumerate(werte):
        x = 30 + k * 38
        out.append(f'<rect x="{x}" y="{base-u*sc:.1f}" width="30" height="{u*sc:.1f}" fill="#999" stroke="#000"/>')
        out.append(f'<rect x="{x}" y="{base-(u+o)*sc:.1f}" width="30" height="{o*sc:.1f}" fill="url(#§h)" stroke="#000"/>')
        out.append(f'<text x="{x+15}" y="{base+14}" text-anchor="middle" font-size="11">{labels[k]}</text>')
    w = 40 + len(werte) * 38
    inner = (f'<line x1="22" y1="5" x2="22" y2="{base}" stroke="#000" marker-start="url(#§a)"/><line x1="22" y1="{base}" x2="{w}" y2="{base}" stroke="#000"/>'
             + ''.join(out) + f'<text x="{w/2}" y="{base+32}" text-anchor="middle" font-size="12.5" font-weight="bold">{titel}</text>')
    return svg(inner, w + 5, base + 40)

def zeitstrahl(punkte, abschnitte):
    """punkte: [(x, 'Label')], abschnitte: [(x1, x2, 'Text', schraffiert?)] in viewBox-Einheiten 0..620."""
    out = [f'<line x1="15" y1="80" x2="605" y2="80" stroke="#000" stroke-width="1.5" marker-end="url(#§a)"/>']
    for x1, x2, t, sch in abschnitte:
        out.append(f'<rect x="{x1}" y="25" width="{x2-x1}" height="40" fill="{"url(#§h)" if sch else "#fff"}" stroke="#000" stroke-width="2"/>')
        out.append(f'<rect x="{x1+15}" y="35" width="{x2-x1-30}" height="20" fill="#fff"/><text x="{(x1+x2)/2}" y="50" text-anchor="middle" font-size="12" font-weight="bold">{t}</text>')
    for x, t in punkte:
        out.append(f'<line x1="{x}" y1="74" x2="{x}" y2="86" stroke="#000" stroke-width="2"/><text x="{x}" y="102" text-anchor="middle" font-size="12">{t}</text>')
    return svg(''.join(out), 620, 110)
