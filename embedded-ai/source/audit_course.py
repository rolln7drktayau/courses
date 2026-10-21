"""Check real slide geometry, interactive maths, navigation and PDF completeness."""
from pathlib import Path
from collections import Counter
import json
import fitz
from PIL import Image, ImageOps, ImageDraw
from playwright.sync_api import sync_playwright
from content import SLIDES,REFERENCES,CORE_COUNT
from build_course import CHROME,build_appendices

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
  within(s.querySelector('.story-copy'),content,'story-copy');
  within(s.querySelector('.quiz-options'),content,'quiz-options');}
 s.querySelectorAll('.visual,.interactive-panel,.reference-list,.glossary-grid,.opening-grid,.opening-card,.quiz-prompt').forEach(el=>{
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
    import csv
    import io
    _,extra=build_appendices();total=CORE_COUNT+len(extra)
    results={'oral_slides':CORE_COUNT,'annexes':len(extra),'minutes':sum(s['minutes'] for s in SLIDES),'references':len(REFERENCES),
             'viewports':{},'console_errors':[],'external_requests':[],'interactive_checks':[]}
    with sync_playwright() as p:
        browser=p.chromium.launch(executable_path=str(CHROME) if CHROME.exists() else None,headless=True)
        page=browser.new_page()
        page.on('pageerror',lambda e:results['console_errors'].append(str(e)))
        page.on('request',lambda r:results['external_requests'].append(r.url) if r.url.startswith('http') else None)
        page.goto((ROOT/'index.html').as_uri())
        page.wait_for_function('window.Course && document.documentElement.dataset.ready === "true"')
        page.evaluate('document.body.classList.add("no-motion")')
        images=page.locator('.scene-picture')
        assert images.count()>=8
        assert images.evaluate_all('els=>els.every(e=>getComputedStyle(e).backgroundImage.startsWith(\'url("data:image/png;base64,\'))')
        results['embedded_artwork']='all narrative panels contain their offline image'
        history_images=page.locator('.history-picture')
        assert history_images.count()==2
        assert history_images.evaluate_all('els=>els.every(e=>getComputedStyle(e).backgroundImage.startsWith(\'url("data:image/png;base64,\'))')
        for w,h in [(1920,1080),(1366,768),(1280,720),(1024,768),(768,1024)]:
            page.set_viewport_size({'width':w,'height':h});page.evaluate('window.Course.fit()')
            problems=[]
            for i in range(total):
                page.evaluate("(i)=>window.Course.show(i,true,'all')",i)
                errors=page.evaluate(GEOMETRY)
                if errors:problems.append({'slide':i+1,'errors':errors})
            results['viewports'][f'{w}x{h}']=problems
        page.set_viewport_size({'width':1600,'height':1000});page.evaluate('window.Course.fit()')
        def go(i):page.evaluate("(i)=>window.Course.show(i,true,'all')",i)
        def visual(name):
            go(next(i for i,item in enumerate(SLIDES+extra) if item.get('visual')==name))
        assert sum(item['minutes'] for item in SLIDES)==180
        page.evaluate('window.Course.show(1,true)')
        assert page.locator('.slide.active .opening-card').count()==4
        assert page.locator('.slide.active [data-answer]').count()==0
        for count in range(1,5):
            page.keyboard.press('ArrowRight')
            assert page.locator('.slide.active .opening-card:not(.fragment-hidden)').count()==count
        results['opening_questions']='four unscored prompts, revealed separately before the story'
        visual('forward_lab')
        assert page.locator('.slide.active [data-forward-value="y"]').inner_text()=='1,5'
        page.locator('.slide.active [data-forward="x1"]').fill('3')
        assert page.locator('.slide.active [data-forward-value="y"]').inner_text()=='4,5'
        results['interactive_checks'].append('Complete network: initial output 1.5; x1=3 gives 4.5')
        visual('learning_step')
        assert page.locator('.slide.active [data-learning-value="loss"]').inner_text()=='0,075625'
        page.locator('.slide.active [data-learning="eta"]').fill('1')
        assert 'augmente' in page.locator('.slide.active [data-learning-value="verdict"]').inner_text()
        page.locator('.slide.active [data-learning="eta"]').fill('0.1')
        results['interactive_checks'].append('One-weight gradient step reduces loss; a large step increases it')
        visual('memory');page.locator('.slide.active [data-weight-bits="8"]').click()
        assert page.locator('.slide.active [data-output="weights"]').inner_text()=='100 Ko'
        assert '120 Ko' in page.locator('.slide.active .memory-columns').inner_text()
        results['interactive_checks'].append('Weight-only quantisation leaves stated SRAM example unchanged')
        visual('quant');page.locator('.slide.active [data-control="quant"]').fill('8')
        assert page.locator('.slide.active [data-output="step"]').inner_text()=='0,0079'
        results['interactive_checks'].append('INT8 symmetric example uses scale 1/127')
        visual('amdahl')
        assert page.locator('.slide.active [data-output="speedup"]').inner_text()=='1,11'
        page.locator('.slide.active [data-control="fraction"]').fill('100')
        page.locator('.slide.active [data-control="speed"]').fill('10')
        assert page.locator('.slide.active [data-output="speedup"]').inner_text()=='10'
        page.locator('.slide.active [data-control="fraction"]').fill('0')
        assert page.locator('.slide.active [data-output="speedup"]').inner_text()=='1'
        results['interactive_checks'].append('Amdahl boundary cases and initial 1.11x verified')
        visual('benchmark_lab')
        assert 'Pas encore mesuré' in page.locator('.slide.active .benchmark-status').inner_text()
        page.locator('.slide.active [data-action="benchmark"]').click()
        page.wait_for_function("document.querySelector('.benchmark-lab [data-action=\"benchmark-csv\"]').disabled === false",timeout=60000)
        with page.expect_download() as event:page.locator('.slide.active [data-action="benchmark-csv"]').click()
        download=event.value
        rows=list(csv.DictReader(Path(download.path()).read_text(encoding='utf-8').splitlines()))
        assert len(rows)==14 and {r['implementation'] for r in rows}=={'loop','reduce'}
        for campaign in range(1,8):
            pair=[r for r in rows if int(r['campaign'])==campaign]
            assert len(pair)==2 and pair[0]['implementation']==('loop' if campaign%2 else 'reduce')
            assert all(float(r['elapsed_ms'])>0 for r in pair)
            assert all(int(r['values'])==4096 for r in pair)
            assert pair[0]['output']==pair[1]['output']
        results['interactive_checks'].append('Live browser benchmark: 7 alternating pairs, equal sums, positive times and downloadable raw CSV')
        results['browser_benchmark_rows']=len(rows)
        quiz_overflow=[]
        for i,item in enumerate(SLIDES):
            if not item['quiz']:continue
            go(i)
            assert page.locator('.slide.active .quiz-followup').is_hidden()
            page.locator(f'.slide.active [data-answer="{item["quiz"]["correct"]}"]').click()
            assert page.locator('.slide.active .quiz-followup').is_visible()
            assert page.locator('.slide.active .quiz-feedback').inner_text().startswith('Oui.')
            for choice in range(len(item['quiz']['options'])):
                page.locator(f'.slide.active [data-answer="{choice}"]').click()
                feedback=page.locator('.slide.active .quiz-feedback').inner_text()
                expected='Oui.' if choice==item['quiz']['correct'] else 'À revoir.'
                assert feedback.startswith(expected)
                assert item['quiz']['feedback'][choice] in feedback
                assert page.locator('.slide.active .quiz-choice.correct').count()==1
                errors=page.evaluate(GEOMETRY)
                if errors:quiz_overflow.append({'slide':i+1,'choice':choice,'errors':errors})
            page.locator(f'.slide.active [data-answer="{item["quiz"]["correct"]}"]').click()
            if item['quiz'].get('decision'):
                assert page.locator('.slide.active .decision-table').is_visible()
            page.locator('[data-action="toc"]').click()
            page.locator(f'#quiz-list button[data-go="{i}"]').click()
            assert page.locator('.slide.active').get_attribute('data-index')==str(i)
        results['quiz_feedback_overflow']=quiz_overflow
        results['interactive_checks'].append('Six end-of-act question breaks: open questions, numerical choices and explanations')
        visual('story_alvinn');page.locator('.slide.active [data-ref="R01"]').click()
        assert page.locator('#reader').evaluate('d=>d.open');page.locator('[data-action="close"]').click()
        page.locator('[data-action="sources"]').click()
        page.get_by_role('button',name='Voir la bibliographie dans la présentation').click()
        assert 'Sources et limites' in page.locator('.slide.active h1').inner_text()
        page.locator('[data-action="toc"]').click();page.locator('.toc-search').fill('Howard')
        page.locator('#slide-list .toc-entry').first.click()
        assert 'Howard' in page.locator('.slide.active h1').inner_text()
        # A scene advances through its layers before the next scene; history restores its layer.
        page.evaluate('window.Course.show(1,true)')
        assert page.evaluate('window.Course.step')==0
        assert page.locator('.slide.active .fragment-hidden').count()>0
        page.keyboard.press('ArrowRight');assert page.evaluate('window.Course.step')==1
        assert page.locator('.slide.active').get_attribute('data-index')=='1'
        page.keyboard.press('a');assert page.locator('.slide.active .fragment-hidden').count()==0
        page.keyboard.press('ArrowRight');assert page.locator('.slide.active').get_attribute('data-index')=='2'
        page.keyboard.press('ArrowLeft');assert page.locator('.slide.active').get_attribute('data-index')=='1'
        assert page.evaluate('window.Course.step')==page.evaluate('window.Course.maxStep')
        page.evaluate('window.Course.show(1,true,2)');page.reload();page.wait_for_function('window.Course')
        assert page.evaluate('window.Course.step')==2
        visual('story_outage')
        assert 'offline' in page.locator('.slide.active .network-scene').get_attribute('class')
        page.locator('.slide.active [data-action="network-toggle"]').click()
        assert 'online' in page.locator('.slide.active .network-scene').get_attribute('class')
        results['interactive_checks'].append('Progressive reveals, reverse navigation, saved step URL and network schematic toggle')
        results['mobile_navigation_fits']=True
        for width in [1366,1100,1024,960,950,900,850,768,701,700,600,560,390,360]:
            page.set_viewport_size({'width':width,'height':844})
            nav=page.locator('.controls').bounding_box()
            assert nav['x']>=0 and nav['x']+nav['width']<=width,(width,nav)
        page.set_viewport_size({'width':1600,'height':1000})
        go(0);page.screenshot(path=str(VERIFY/'presentation_accueil.png'))
        visual('forward_lab');page.screenshot(path=str(VERIFY/'presentation_reseau.png'))
        browser.close()
    pdf=fitz.open(ROOT/'course.pdf')
    results['pdf_pages']=len(pdf);assert len(pdf)==total
    assert pdf.metadata['author']=='Roland Cédric TAYO'
    assert all(len(p.get_text())>150 for p in pdf)
    assert all(abs(p.rect.width/p.rect.height-16/9)<.001 for p in pdf)
    text='\n'.join(p.get_text() for p in pdf)
    for ref in REFERENCES:assert ref['id'] in text,ref['id']
    assert 'Futurs ingénieurs en systèmes embarqués' not in pdf[0].get_text()
    assert 'Alice' in pdf[0].get_text()
    for i,item in enumerate(SLIDES):
        if item['visual'] in {'story_cover','story_request','story_voices','story_shakey','story_alvinn','story_remote','story_outage','story_pause','story_robustness','story_epilogue'}:
            assert pdf[i].get_images(),f'Missing printed scene art at {i+1}'
    assert all(ref in text for ref in ['Pomerleau','Howard','Jacob','Wei-Ming Chen'])
    assert 'Sans Internet' not in pdf[1].get_text()
    assert 'Une IA peut-elle fonctionner sans Internet' in pdf[1].get_text()
    assert 'La lampe' in pdf[2].get_text()
    assert sum(bool(item['quiz']) for item in SLIDES)==6
    results['pdf_links']=sum(len(p.get_links()) for p in pdf)
    selected=[0,1,2,4,5,8,13,20,21,25,31,34]
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
    assert not any(results['viewports'].values()),results['viewports']
    assert not results['quiz_feedback_overflow'],results['quiz_feedback_overflow']
    assert not results['console_errors'] and not results['external_requests']

if __name__=='__main__':main()
