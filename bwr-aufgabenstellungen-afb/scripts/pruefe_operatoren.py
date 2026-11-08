#!/usr/bin/env python3
"""Prüft eine Angabe (Markdown) auf Operatoren, AFB-Verteilung und Wiederholungen.
  pruefe_operatoren.py angabe.md [--sie]
Erkannt werden Operatoren am Satzanfang (nach Nummer wie 2.1, a) oder Aufzählungszeichen) sowie nach 'und'
('Berechne und beurteile'). Beleg-Zitate (Zeilen mit >) und Codeblöcke werden übersprungen.
Ausgabe: Operatoren je Teilaufgabe, Anteil AFB I/II/III, Wiederholungen je AFB und Synonymgruppe,
Sätze ohne erkannten Operator (Prüfhinweis, kein Fehler)."""
import json, re, sys, os, collections
args = [a for a in sys.argv[1:] if not a.startswith('--')]
sie = '--sie' in sys.argv
if not args: sys.exit(__doc__)
ops = json.load(open(os.path.join(os.path.dirname(__file__), '..', 'references', 'operatoren.json'), encoding='utf-8'))['operatoren']
key = 'sie' if sie else 'du'
def find_ops(sentence):
    found = []
    for o in sorted(ops, key=lambda o: -len(o[key])):
        stem = o[key]
        for m in re.finditer(r'(?:(?<=^)|(?<=\s))' + re.escape(stem) + r'\b', sentence, re.I):
            tail = sentence[m.end():]
            if 'enthalten' in o and o['enthalten'].lower() not in (stem + ' ' + tail).lower(): continue
            # nur am Satzanfang oder nach 'und'/'sowie'/'oder'/Komma
            pre = sentence[:m.start()].strip().lower()
            if pre == '' or re.search(r'(und|sowie|oder|,|;)$', pre):
                found.append(o)
    out = []
    for o in found:
        if o['lemma'] not in [x['lemma'] for x in out]: out.append(o)
    return out
text = open(args[0], encoding='utf-8').read()
text = re.sub(r'```.*?```', '', text, flags=re.S)
rows = []; unknown = []
for line in text.split('\n'):
    s = line.strip()
    if not s or s.startswith('>') or s.startswith('#') or s.startswith('<') or s.startswith('|'): continue
    s = re.sub(r'^(\*\*)?(\d+(?:\.\d+)*\.?|[a-z]\)|[-*])(\*\*)?\s*', '', s)
    for sent in re.split(r'(?<=[.:?!])\s+', s):
        if not sent: continue
        got = find_ops(sent)
        if got: rows.append((sent[:90], got))
        elif re.match(r'^[A-ZÄÖÜ]\w+e\b', sent) and len(sent) < 160 and not sent.startswith(('Soweit', 'Name', 'Unternehmen')): unknown.append(sent[:90])
afb = collections.Counter(); per = collections.defaultdict(list)
for sent, got in rows:
    top = max(got, key=lambda o: ['I', 'II', 'III'].index(o['afb']))
    afb[top['afb']] += 1
    for o in got: per[o['afb']].append(o)
    print(f"[{top['afb']:>3}] {'+'.join(o['lemma'] for o in got):28} {sent}")
n = sum(afb.values())
print(f"\nAFB-Verteilung nach Anzahl Teilaufgaben ({n}): " + ', '.join(f"{k}: {afb[k]} ({100*afb[k]/n:.0f} %)" for k in ('I', 'II', 'III')) if n else 'Keine Operatoren erkannt.')
for k in ('I', 'II', 'III'):
    c = collections.Counter(o['lemma'] for o in per[k])
    rep = [f"{l} ×{v}" for l, v in c.items() if v > 1]
    if rep: print(f"Wiederholt in AFB {k}: " + ', '.join(rep) + '  → Synonym derselben Gruppe prüfen (Gruppen in references/operatoren.json); bei Buchungssatz/Berechnen ist Wiederholung üblich.')
if unknown:
    print('\nSätze ohne erkannten Operator (prüfen):'); [print('  -', u) for u in unknown[:15]]
