"""Vorlage für ein neues Selbstlernheft. Kopieren, Inhalte ersetzen, ausführen:
    python3 inhalt.py
Erzeugt in ./out/ Schüler-, Lehrkraft- und Kompaktfassungen sowie Lösungsblätter."""
import sys, os
import glob
SKILL = os.environ.get('SKILL_DIR') or (glob.glob('/mnt/skills/**/selbstlernheft-html', recursive=True) or ['.'])[0]
sys.path.insert(0, os.path.join(SKILL, 'scripts'))
from heft_lib import *
import svg_kit as S

TITEL = {1: 'Begriff und Bedeutung', 2: 'Kennzahl berechnen'}

def inhalt():
    page(titelseite(
        'BwR · Jahrgangsstufe 9 · Selbstlernheft', 'Beispielthema',
        S.svg(S.box(10, 10, 140, 40, 'LOGO'), 160, 60, style='width:40mm'),
        '<p>Szenario: Eine Bekannte führt ein Unternehmen und bittet dich um Rat. Du arbeitest dich mit diesem Heft selbstständig ein und schreibst ihr am Ende eine Beratungs-E-Mail.</p>',
        [('Firma', 'Muster GmbH'), ('Inhaberin', 'Erika Muster'), ('Rechtsform', 'Einzelunternehmen')],
        TITEL))

    page(kap(1, TITEL[1])
         + alltag('Taschengeld', '<p>Echter Alltagsvergleich – nur dann „Aus dem Alltag“, sonst beispiel(...).</p>')
         + info('<p>Längerer Infotext mit <b>Fachbegriffen</b> …</p><p>Zweiter Absatz …</p>', cols=True)
         + fig(S.svg(S.box(20, 20, 200, 60, 'Kasten A', 'Unterzeile') + S.pfeil(222, 50, 398, 50, 'Beziehung')
                     + S.box(400, 20, 200, 60, 'Kasten B', fill='url(#§h)'), 620, 100))
         + ueb(1, TITEL[1], f'<p><b>Begriff</b> = {a("Definition, die die Schüler ergänzen", "60mm")}</p>'
                            + tabelle(['Merkmal', 'A', 'B'], [['Kosten', a('niedrig'), a('hoch')],
                                                             ['Vorteil', a('lange Antwort bekommt automatisch Linien'), a('zweite lange Antwort mit Linien')]]))
         + aufg(1, aufg_kopf()
                + task('1.1', 'Nenne zwei Merkmale von …', ab('z. B. Merkmal 1; Merkmal 2', 2))
                + task('1.2', 'Ordne zu …', tabelle(['Vorgang', 'X / Y'], [['a) …', a('X')], ['b) …', a('Y')]], [None, '20mm'])))
         + check(1))

    page(kap(2, TITEL[2], pb=True)
         + keep(info(f'<p>Formel:</p>{formel("Quote in % = " + frac("Teil · 100", "Ganzes"))}')
                + aufg(2, aufg_kopf() + task('2.1', 'Berechne die Quote (Merkteil, daher Kästchen im Heft).', karo('30 · 100 : 120 = 25 %', 3, keep=True))))
         + aufg(2, task('2.2', 'Beurteile das Ergebnis.', ab('Musterlösung …', 3)))
         + check(2))

if __name__ == '__main__':
    build(inhalt, TITEL, teile=[('Heft', [1, 2])], out='out', prefix='Beispiel', fuss='Beispielthema · Muster GmbH')
