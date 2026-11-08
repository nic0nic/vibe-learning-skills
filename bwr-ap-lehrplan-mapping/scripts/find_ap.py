#!/usr/bin/env python3
"""AP-Teilaufgaben nach Lernbereich, Stichwort, Konto, Typ oder Prüfung filtern.
Beispiele:
  find_ap.py --lb 8.2                 # Haupt- und Nebenzuordnung zu Jgst 8 LB2
  find_ap.py --lb 8.2 --haupt         # nur Schwerpunkt
  find_ap.py --stichwort skonto --typ BS
  find_ap.py --konto 6730
  find_ap.py --lb 9.5 --pruefung 2025
  find_ap.py --uebersicht             # Anzahl je LB und Prüfung
"""
import argparse, csv, os, collections
p = argparse.ArgumentParser()
p.add_argument('--lb', help='Code Jgst.LB, z. B. 8.2; mehrere mit Komma')
p.add_argument('--haupt', action='store_true', help='nur lb_haupt')
p.add_argument('--stichwort', help='Teilstring im Thema (case-insensitive)')
p.add_argument('--konto', help='Kontonummer oder -kürzel in Spalte konten')
p.add_argument('--typ', choices=['BS', 'BE', 'TX', 'MC'])
p.add_argument('--pruefung', help='z. B. 2024 oder 2024/HT')
p.add_argument('--uebersicht', action='store_true')
a = p.parse_args()
f = os.path.join(os.path.dirname(__file__), '..', 'references', 'ap_mapping.csv')
rows = list(csv.DictReader(open(f, encoding='utf-8')))
if a.uebersicht:
    c = collections.defaultdict(collections.Counter)
    for r in rows:
        c[r['lb_haupt']][r['pruefung']] += 1
    pr = sorted({r['pruefung'] for r in rows})
    print('LB    ' + ' '.join(x for x in pr) + '  Σ')
    for lb in sorted(c, key=lambda x: tuple(map(int, x.split('.')))):
        print(f"{lb:5} " + ' '.join(f"{c[lb][x]:7}" for x in pr) + f"  {sum(c[lb].values())}")
    raise SystemExit
def ok(r):
    if a.lb:
        want = set(a.lb.split(','))
        have = {r['lb_haupt']} if a.haupt else {r['lb_haupt']} | set(r['lb_neben'].split())
        if not want & have: return False
    if a.stichwort and a.stichwort.lower() not in r['thema'].lower(): return False
    if a.konto and a.konto.lower() not in r['konten'].lower(): return False
    if a.typ and r['typ'] != a.typ: return False
    if a.pruefung and not r['pruefung'].startswith(a.pruefung): return False
    return True
res = [r for r in rows if ok(r)]
for r in res:
    n = f" (+{r['lb_neben']})" if r['lb_neben'] else ''
    print(f"{r['pruefung']} {r['aufgabe']:6} [{r['lb_haupt']}{n}] {r['typ']} {r['thema']}" + (f"  | {r['konten']}" if r['konten'] else ''))
print(f"-- {len(res)} Treffer")
