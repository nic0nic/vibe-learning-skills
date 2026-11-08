#!/usr/bin/env python3
"""Gibt eine AP-Aufgabe (Angabe, optional Lösungsvorschlag) aus.
  show_ap.py 2025/HT 3.3.2            # Angabe der Teilaufgabe 3.3.2
  show_ap.py 2025/HT 3.3 --loesung    # Angabe + Lösungsvorschlag von 3.3 inkl. 3.3.1, 3.3.2
  show_ap.py 2025/HT 3 --ganz         # gesamte Aufgabe 3 (Angabe; mit --loesung auch Lösung)
  show_ap.py 2025/HT --kopf           # Unternehmensinformationen/formale Vorgaben
Die Zeilen der Teilaufgabe werden per Nummer am Zeilenanfang gesucht; bei Auffälligkeiten --ganz nutzen.
"""
import re, sys, os, argparse
p = argparse.ArgumentParser()
p.add_argument('pruefung'); p.add_argument('nr', nargs='?')
p.add_argument('--loesung', action='store_true'); p.add_argument('--ganz', action='store_true')
p.add_argument('--kopf', action='store_true')
a = p.parse_args()
y, t = a.pruefung.upper().split('/')
f = os.path.join(os.path.dirname(__file__), '..', 'references', 'ap', f'AP_{y}_{t}.md')
if not os.path.exists(f):
    sys.exit(f'Volltext fehlt: references/ap/AP_{y}_{t}.md\n'
             'Die Prüfungstexte sind urheberrechtlich geschützt und nicht im Repo. AP-PDF selbst besorgen (z. B. ISB/Schule), '
             'mit pdftotext -layout extrahieren und im Format aus SKILL.md („Neue AP-Jahrgänge ergänzen“) dort ablegen. '
             'Ohne Volltext: Lehrkraft um das AP-PDF bitten.')
md = open(f, encoding='utf-8').read()
ang, los = md.split('## Lösungsvorschlag')
def blocks(part):
    d = {}
    for m in re.finditer(r'### (.+?)\n\n```text\n(.*?)\n```', part, re.S):
        d[m.group(1)] = m.group(2)
    return d
A, L = blocks(ang), blocks(los)
if a.kopf:
    print(A['Unternehmensinformationen und formale Vorgaben']); sys.exit()
if not a.nr: sys.exit('Nummer fehlt')
top = a.nr.split('.')[0]
key = f'Aufgabe {top}'
def sub(text, nr):
    ls = text.split('\n'); lab = re.compile(r'^\s*([1-8](?:\.\d{1,2}){1,3})(?=\s)')
    out = []; on = False
    for l in ls:
        m = lab.match(l)
        if m:
            n = m.group(1)
            if n == nr or n.startswith(nr + '.'): on = True
            elif on and not n.startswith(nr + '.'): break
        if on: out.append(l)
    return '\n'.join(out) if out else None
def get(d, title):
    txt = d[key]
    if a.ganz or '.' not in a.nr: return txt
    r = sub(txt, a.nr)
    return r if r else f'[Teilaufgabe {a.nr} nicht gefunden – gesamte {key}:]\n' + txt
print(f'=== {y}/{t} {a.nr} – Angabe ===\n' + get(A, 'A'))
if a.loesung:
    print(f'\n=== {y}/{t} {a.nr} – Lösungsvorschlag ===\n' + get(L, 'L'))
