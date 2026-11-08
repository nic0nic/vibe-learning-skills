"""Exportiert die finalen HTML-Dateien als PDF und packt alles in eine ZIP:
<Ordnername>/html/*.html  und  <Ordnername>/pdf/*.pdf
Aufruf: python3 export.py "<Ordnername>" ziel.zip quelle1.html=1_Neuer_Name quelle2.html=2_Name ..."""
import sys, os, shutil, zipfile
from playwright.sync_api import sync_playwright

name, zipf, *paare = sys.argv[1:]
base = os.path.join(os.path.dirname(os.path.abspath(zipf)), name)
shutil.rmtree(base, ignore_errors=True)
os.makedirs(os.path.join(base, 'html')); os.makedirs(os.path.join(base, 'pdf'))
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page()
    for paar in paare:
        src, ziel = paar.split('=') if '=' in paar else (paar, os.path.basename(paar)[:-5])
        shutil.copy(src, os.path.join(base, 'html', ziel + '.html'))
        pg.goto('file://' + os.path.abspath(src)); pg.emulate_media(media='print')
        pg.pdf(path=os.path.join(base, 'pdf', ziel + '.pdf'), prefer_css_page_size=True, print_background=True)
    b.close()
with zipfile.ZipFile(zipf, 'w', zipfile.ZIP_DEFLATED) as z:
    for root, _, files in os.walk(base):
        for f in files:
            full = os.path.join(root, f)
            z.write(full, os.path.relpath(full, os.path.dirname(base)))
print('ZIP:', zipf)
