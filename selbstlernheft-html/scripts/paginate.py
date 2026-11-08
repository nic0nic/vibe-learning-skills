"""Platzoptimierte Paginierung: packt Blöcke auf feste A4-Seiten statt je Kapitel neue Seite.
Regeln: .kap/.ak/.vnt nie allein am Seitenende; .pb erzwingt neue Seite; .info wird absatzweise geteilt;
.aufgaben wird in Einzelaufgaben aufgelöst; alles andere (inkl. .keep) bleibt ganz.
Aufruf: python3 paginate.py "eingabe.html|ausgabe.html|Fußzeile" ..."""
import sys, os
from playwright.sync_api import sync_playwright

JS = r'''
(fuss) => {
  document.querySelectorAll('tr').forEach(tr=>{const z=[...tr.querySelectorAll('.zl')]; if(!z.length) return;
    const mm=3.7795; let h=Math.max(...z.map(e=>e.getBoundingClientRect().height)); h=Math.ceil(h/(6*mm)-0.05)*6*mm;
    z.forEach(e=>e.style.minHeight=h+'px');});
  const old=[...document.querySelectorAll('body > .page')];
  const hasTitle = !!old[0].querySelector('.titel');
  const blocks=[];
  old.forEach((p,i)=>{ if(hasTitle && i===0) return;
    [...p.children].forEach(c=>{ if(c.classList.contains('foot')) return;
      if(c.classList.contains('aufgaben')) [...c.children].forEach(x=>blocks.push(x)); else blocks.push(c);});});
  const body=document.body; const titlePage = hasTitle? old[0] : null;
  old.forEach((p,i)=>{ if(!(hasTitle&&i===0)) p.remove(); });
  if(titlePage) titlePage.querySelector('.foot')?.remove();
  const pages = titlePage? [titlePage] : [];
  let pc=null;
  const newPage=()=>{const p=document.createElement('div');p.className='page';pc=document.createElement('div');pc.className='pc';p.appendChild(pc);body.appendChild(p);pages.push(p);return pc;};
  const over=()=>pc.scrollHeight>pc.clientHeight+1;
  newPage();
  for(let k=0;k<blocks.length;k++){
    const b=blocks[k];
    if(b.classList.contains('pb') && pc.children.length>0){ newPage(); }
    pc.appendChild(b);
    // Kapitelüberschrift nie allein am Seitenende: mit nächstem Block testen
    if((b.classList.contains('kap')||b.classList.contains('ak')||b.classList.contains('vnt')) && k+1<blocks.length){
      const nx=blocks[k+1]; pc.appendChild(nx);
      const bad=over(); nx.remove();
      if(bad && pc.children.length>1){ b.remove(); newPage(); pc.appendChild(b); }
      continue;
    }
    if(!over()) continue;
    // teilbare Infotexte absatzweise aufteilen
    if(b.classList.contains('info') && b.children.length>1){
      const rest=b.cloneNode(false);
      while(over() && b.children.length>0){ rest.insertBefore(b.lastElementChild, rest.firstChild); }
      if(b.children.length===0){ b.remove(); }
      newPage(); pc.appendChild(rest);
      continue;
    }
    if(pc.children.length>1){ b.remove(); newPage(); pc.appendChild(b); }
  }
  const n=pages.length;
  pages.forEach((p,i)=>{const f=document.createElement('div');f.className='foot';f.innerHTML=`<span>${fuss}</span><span>Seite ${i+1} von ${n}</span>`;p.appendChild(f);});
  // Arbeitsplan-Seitenzahlen und Bilanz-Verweis aktualisieren
  const seite={};
  pages.forEach((p,i)=>p.querySelectorAll('.kap .kn').forEach(e=>{seite[e.textContent.trim()]=i+1;}));
  document.querySelectorAll('.plan tr').forEach(tr=>{const td=tr.children; if(td.length>3 && seite[td[0].textContent.trim()]) td[2].textContent=seite[td[0].textContent.trim()];});
  document.querySelectorAll('.sref').forEach(r=>{const sel=r.dataset.sel; let s='?';
    pages.forEach((p,i)=>{ if(s==='?' && p.querySelector(sel)) s=String(i+1); }); r.textContent=s;});
  return [n, seite];
}
'''

CSS = '<style>.fig:not(.fig80)>svg:not(.leg){width:84%!important}.fig80>svg{width:92%}.autos .auto svg{max-height:21mm}.pc{height:calc(297mm - 26mm);overflow:hidden}.pc>.kap:not(:first-child){margin-top:5mm}.pc>.ak:first-child{margin-top:0}</style>'


def paginate(jobs):
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page()
        for src, dst, fuss in jobs:
            pg.goto('file://' + os.path.abspath(src)); pg.emulate_media(media='print')
            pg.evaluate("css=>document.head.insertAdjacentHTML('beforeend',css)", CSS)
            print(os.path.basename(dst), pg.evaluate(JS, fuss))
            open(dst, 'w', encoding='utf-8').write(pg.content())
        b.close()

if __name__ == '__main__':
    paginate([a.split('|') for a in sys.argv[1:]])
