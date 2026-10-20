"""Check real slide geometry, interactive maths, navigation and PDF completeness."""
from pathlib import Path
from collections import Counter
import json
import fitz
from PIL import Image, ImageOps, ImageDraw
from playwright.sync_api import sync_playwright
from content import SLIDES,REFERENCES
from build_course import CHROME

ROOT=Path(__file__).resolve().parents[1]
VERIFY=ROOT/'verification';VERIFY.mkdir(exist_ok=True)

GEOMETRY='''() => {
 const s=document.querySelector('.slide.active');const scale=s.getBoundingClientRect().width/1600;
 const f=s.querySelector('footer').getBoundingClientRect();const errors=[];
 const within=(element,parent,label)=>{if(!element||!parent)return;const a=element.getBoundingClientRect(),b=parent.getBoundingClientRect();
  if(a.bottom>b.bottom+2*scale||a.top<b.top-2*scale||a.right>b.right+2*scale||a.left<b.left-2*scale)
   errors.push({label,bottom:Math.round((a.bottom-b.bottom)/scale),right:Math.round((a.right-b.right)/scale)});
 };
 const content=s.querySelector('.content');
 if(content){within(s.querySelector('.points'),content,'points');within(s.querySelector('.visual'),content,'visual');
  within(s.querySelector('.quiz-options'),content,'quiz-options');}
 s.querySelectorAll('.visual,.interactive-panel,.reference-list,.glossary-grid').forEach(el=>{
  if(el.scrollHeight>el.clientHeight+3||el.scrollWidth>el.clientWidth+3)errors.push({label:el.className,scrollH:el.scrollHeight-el.clientHeight,scrollW:el.scrollWidth-el.clientWidth});
 });
 const last=s.querySelector('.content,.reference-list,.glossary-grid,.answer-list,.hero-grid');
 if(last&&last.getBoundingClientRect().bottom>f.top+2*scale)errors.push({label:'footer-overlap'});
 s.querySelectorAll('svg.diagram').forEach(svg=>{const vb=svg.viewBox.baseVal;
  svg.querySelectorAll('text').forEach(t=>{const b=t.getBBox();if(b.x<-3||b.y<-3||b.x+b.width>vb.width+3||b.y+b.height>vb.height+3)errors.push({label:'svg-text',text:t.textContent,bbox:[b.x,b.y,b.width,b.height]});});
 });
 return errors;
}'''


def main():
    results={'oral_slides':44,'annexes':10,'minutes':sum(s['minutes'] for s in SLIDES),'references':len(REFERENCES),
             'viewports':{},'console_errors':[],'external_requests':[],'interactive_checks':[]}
    with sync_playwright() as p:
        browser=p.chromium.launch(executable_path=str(CHROME) if CHROME.exists() else None,headless=True)
        page=browser.new_page()
        page.on('pageerror',lambda e:results['console_errors'].append(str(e)))
        page.on('request',lambda r:results['external_requests'].append(r.url) if r.url.startswith('http') else None)
        page.goto((ROOT/'index.html').as_uri())
        page.wait_for_function('window.Course && document.documentElement.dataset.ready === "true"')
        page.evaluate('document.body.classList.add("no-motion")')
        for w,h in [(1920,1080),(1366,768),(1280,720),(1024,768),(768,1024)]:
            page.set_viewport_size({'width':w,'height':h});page.evaluate('window.Course.fit()')
            problems=[]
            for i in range(54):
                page.evaluate('(i)=>window.Course.show(i,true)',i)
                errors=page.evaluate(GEOMETRY)
                if errors:problems.append({'slide':i+1,'errors':errors})
            results['viewports'][f'{w}x{h}']=problems
        page.set_viewport_size({'width':1600,'height':1000});page.evaluate('window.Course.fit()')
        def go(i):page.evaluate('(i)=>window.Course.show(i,true)',i)
        go(15)
        page.locator('.slide.active [data-control="kv"]').fill('4096')
        assert page.locator('.slide.active [data-output="kv"]').inner_text()=='64'
        results['interactive_checks'].append('KV: 4096 tokens -> 64 Mio in stated example')
        go(19);page.locator('.slide.active [data-weight-bits="8"]').click()
        assert page.locator('.slide.active [data-output="weights"]').inner_text()=='100 Ko'
        assert '120 Ko' in page.locator('.slide.active .memory-columns').inner_text()
        results['interactive_checks'].append('Weight-only quantisation leaves SRAM example unchanged')
        go(27);page.locator('.slide.active [data-control="quant"]').fill('8')
        step=page.locator('.slide.active [data-output="step"]').inner_text();assert step=='0,0079',step
        results['interactive_checks'].append('INT8 symmetric quantisation step = 1/127')
        go(32)
        assert page.locator('.slide.active [data-output="speedup"]').inner_text()=='1,11'
        page.locator('.slide.active [data-control="fraction"]').fill('100')
        page.locator('.slide.active [data-control="speed"]').fill('10')
        assert page.locator('.slide.active [data-output="speedup"]').inner_text()=='10'
        page.locator('.slide.active [data-control="fraction"]').fill('0')
        assert page.locator('.slide.active [data-output="speedup"]').inner_text()=='1'
        results['interactive_checks'].append('Global speedup: 20%/2x -> 1.11x; 100%/10x -> 10x; 0% -> 1x')
        quiz_overflow=[]
        for i,s in enumerate(SLIDES):
            if not s['quiz']:continue
            go(i);page.locator('.slide.active [data-answer="0"]').click()
            page.locator(f'.slide.active [data-answer="{s["quiz"]["correct"]}"]').click()
            assert page.locator('.slide.active .quiz-feedback').inner_text().startswith('Oui.')
            errors=page.evaluate(GEOMETRY)
            if errors:quiz_overflow.append({'slide':i+1,'errors':errors})
        results['quiz_feedback_overflow']=quiz_overflow
        results['interactive_checks'].append('Five quizzes: feedback and correct answers available')
        go(4);page.locator('.slide.active [data-ref="R01"]').click();assert page.locator('#reader').evaluate('d=>d.open')
        page.locator('[data-action="close"]').click()
        page.locator('[data-action="toc"]').click();page.locator('.toc-search').fill('Quantifier')
        assert page.locator('.toc-entry').count()>=1;page.locator('.toc-entry').first.click()
        assert 'Quantifier' in page.locator('.slide.active h1').inner_text()
        page.keyboard.press('ArrowRight');assert 'Calibrer' in page.locator('.slide.active h1').inner_text()
        results['interactive_checks'].append('Sources, searchable contents and keyboard navigation')
        go(0);page.screenshot(path=str(VERIFY/'presentation_accueil.png'))
        go(15);page.screenshot(path=str(VERIFY/'presentation_cache_kv.png'))
        browser.close()
    pdf=fitz.open(ROOT/'course.pdf')
    results['pdf_pages']=len(pdf);assert len(pdf)==54
    assert pdf.metadata['author']=='Roland Cédric TAYO'
    assert all(len(p.get_text())>150 for p in pdf)
    assert all(abs(p.rect.width/p.rect.height-16/9)<.001 for p in pdf)
    text='\n'.join(p.get_text() for p in pdf)
    for r in REFERENCES:assert r['id'] in text,r['id']
    results['pdf_links']=sum(len(p.get_links()) for p in pdf)
    selected=[0,4,10,12,15,19,20,27,32,40,44,50]
    thumbs=[]
    for i in selected:
        pix=pdf[i].get_pixmap(matrix=fitz.Matrix(.4,.4))
        img=Image.frombytes('RGB',[pix.width,pix.height],pix.samples)
        canvas=Image.new('RGB',(480,297),'#d8e2e8');canvas.paste(img,(0,0));ImageDraw.Draw(canvas).text((12,277),f'Slide {i+1}',fill='#163a4e')
        thumbs.append(canvas)
    sheet=Image.new('RGB',(480*3,297*4),'white')
    for i,img in enumerate(thumbs):sheet.paste(img,((i%3)*480,(i//3)*297))
    sheet.save(VERIFY/'planche_verification.png')
    (VERIFY/'checks.json').write_text(json.dumps(results,indent=2,ensure_ascii=False),encoding='utf-8')
    print(json.dumps(results,ensure_ascii=True))


if __name__=='__main__':main()
