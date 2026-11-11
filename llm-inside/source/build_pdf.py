"""Render the same SVG/HTML scenes to a vector PDF with source links."""
from pathlib import Path
import json
import fitz
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
CHROME=r'C:\Program Files\Google\Chrome\Application\chrome.exe'

def main():
    checks=[];outputs={}
    with sync_playwright() as p:
        browser=p.chromium.launch(executable_path=CHROME,headless=True)
        for audience,name in [('discovery','course.pdf'),('engineer','engineering.pdf')]:
            output=fitz.open()
            page=browser.new_page(viewport={'width':1600,'height':900},reduced_motion='reduce')
            page.goto((ROOT/'index.html').as_uri()+'?print=1&audience='+audience)
            page.wait_for_function('document.documentElement.dataset.ready === "true"')
            count=page.evaluate('Deck.slides.length')
            for index in range(count):
                page.evaluate('(i)=>Deck.go(i,true)',index)
                page.wait_for_timeout(40)
                metrics=page.evaluate('''()=>{
              const root=document.querySelector('#slide').getBoundingClientRect();
              const footer=document.querySelector('.slide-footer').getBoundingClientRect();
              const copy=document.querySelector('.copy').getBoundingClientRect();
              const visual=document.querySelector('.visual').getBoundingClientRect();
              return {id:Deck.slides[Deck.state.index].id,copyBottom:copy.bottom-root.top,footerTop:footer.top-root.top,
                visualBottom:Deck.slides[Deck.state.index].reading?0:visual.bottom-root.top,
                slideWidth:root.width,slideHeight:root.height};
                }''')
                metrics['audience']=audience;checks.append(metrics)
                assert metrics['copyBottom']<metrics['footerTop']-12,metrics
                assert metrics['visualBottom']<metrics['footerTop']-12,metrics
                pdf=page.pdf(width='1600px',height='900px',print_background=True,prefer_css_page_size=True)
                part=fitz.open(stream=pdf,filetype='pdf')
                assert len(part)==1,(index,len(part))
                output.insert_pdf(part,links=True);part.close()
            titles=page.evaluate('Deck.slides.map(s=>s.title.replace(/<[^>]+>/g," ").replace(/\\s+/g," "))')
            output.set_metadata({'title':'Dans la mémoire d’un modèle — '+('Découverte' if audience=='discovery' else 'Parcours ingénieur complet'),'author':'Roland Cédric TAYO','subject':'Mini-cours INEM · modèles de langage et IA embarquée'})
            output.set_toc([[1,title,i+1] for i,title in enumerate(titles)])
            output.save(ROOT/name,garbage=4,deflate=True);output.close();page.close();outputs[name]=count
        browser.close()
    target=ROOT/'verification';target.mkdir(exist_ok=True)
    (target/'pdf-layout.json').write_text(json.dumps(checks,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'pdf_pages':outputs,'layout_checks':'passed'}))

if __name__=='__main__':main()
