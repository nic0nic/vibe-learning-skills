"""Prüft fertige HTML-Hefte: Überlauf je A4-Seite, abgeschnittene Antwortfelder, Seitenzahl.
Erzeugt zusätzlich eine Miniaturübersicht (PNG) zum Ansehen mit dem Read-Tool.
Aufruf: python3 pruefen.py datei1.html [datei2.html ...]  (Ausgabe-PNGs neben den Dateien: *_vorschau.png)"""
import sys, os, subprocess, glob, tempfile
from playwright.sync_api import sync_playwright
from PIL import Image

JS = '''()=>[...document.querySelectorAll('.page')].map((e,i)=>{let last=0;
 const box=e.querySelector('.pc')||e;
 for(const c of box.children){if(c.classList.contains('foot'))continue;
   last=Math.max(last,c.getBoundingClientRect().bottom-e.getBoundingClientRect().top)}
 const lim=e.clientHeight-(e.classList.contains('lsheet')?40:58);return [i+1,Math.round(last-lim)]})'''

def pruefe(f):
    tmp = tempfile.mkdtemp()
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page()
        pg.goto('file://' + os.path.abspath(f)); pg.emulate_media(media='print')
        over = [x for x in pg.evaluate(JS) if x[1] > 2]
        ab = pg.evaluate("[...document.querySelectorAll('.ab,.karo')].filter(e=>e.scrollHeight>e.clientHeight+2).map(e=>e.innerText.slice(0,40))")
        pdf = os.path.join(tmp, 'x.pdf')
        pg.pdf(path=pdf, prefer_css_page_size=True, print_background=True)
        b.close()
    subprocess.run(['pdftoppm', '-r', '40', '-png', pdf, os.path.join(tmp, 'p')], check=True)
    ims = [Image.open(x) for x in sorted(glob.glob(os.path.join(tmp, 'p-*.png')))]
    w, h = ims[0].size; cols = min(6, len(ims)); rows = (len(ims) + cols - 1) // cols
    c = Image.new('RGB', (w * cols, h * rows), 'white')
    for i, im in enumerate(ims):
        c.paste(im, ((i % cols) * w, (i // cols) * h))
    png = f.replace('.html', '_vorschau.png'); c.save(png)
    print(f'{os.path.basename(f)}: {len(ims)} Seiten | Überlauf: {over or "keiner"} | zu kleine Antwortfelder: {ab or "keine"} | Vorschau: {png}')

for f in sys.argv[1:]:
    pruefe(f)
