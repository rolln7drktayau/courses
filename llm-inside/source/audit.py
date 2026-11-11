"""Check the teaching calculations, interactions and layout in a real browser."""
from pathlib import Path
import json, math
import fitz
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
CHROME=r'C:\Program Files\Google\Chrome\Application\chrome.exe'

def main():
    errors=[];report={};references=[]
    with sync_playwright() as p:
        browser=p.chromium.launch(executable_path=CHROME,headless=True)
        page=browser.new_page(viewport={'width':1600,'height':1000})
        page.on('pageerror',lambda e:errors.append(str(e)))
        requests=[];page.on('request',lambda r:requests.append(r.url))
        page.goto((ROOT/'index.html').as_uri())
        page.wait_for_function('document.documentElement.dataset.ready === "true"')
        values=page.evaluate('''()=>{
          const m=MathLab,q=m.quantize([-.9,-.32,.18,.76],4);
          const z=m.quantize([0,0],2),r=m.roofline(7e9,4,50e9,2e12);
          return {weights16:m.weightBytes(7e9,16),weights4:m.weightBytes(7e9,4),
            kv8:m.kvBytes(32,8192,8,128,2),kv32:m.kvBytes(32,8192,32,128,2),
            roofline:r,quant:q,quantOutput:m.dot(q.codes.map(x=>x*q.scale),[1,.5,-1,.25]),
            quantOriginal:m.dot([-.9,-.32,.18,.76],[1,.5,-1,.25]),zero:z,
            halfAway:m.quantize([1,.5,-.5],2),collisions:32000*32*16};
        }''')
        assert values['weights16']==14_000_000_000
        assert values['weights4']==3_500_000_000
        assert values['kv8']==2**30 and values['kv32']==4*2**30
        assert math.isclose(values['roofline']['memory'],.07)
        assert math.isclose(values['roofline']['calculation'],.007)
        assert values['quant']['codes']==[-7,-2,1,6]
        assert math.isclose(values['quantOutput'],-.9642857142857144)
        assert math.isclose(values['quantOriginal'],-1.05)
        assert values['zero']['scale']==1 and values['zero']['codes']==[0,0]
        assert values['halfAway']['codes']==[1,1,-1]
        assert values['collisions']==16_384_000
        report['calculated_examples']=values
        # Actual control changes must update the SVG, not just the labels.
        page.evaluate('Deck.go(7,true)');page.locator('[data-bits="4"]').click()
        assert '3,50 Go' in page.locator('#art').text_content()
        page.evaluate('Deck.go(8,true)');page.locator('#cache-size').select_option('32768')
        assert '4,00 Gio' in page.locator('#art').text_content()
        page.locator('#heads').click();assert '16,00 Gio' in page.locator('#art').text_content()
        page.evaluate('Deck.go(9,true)');page.locator('#bandwidth').fill('100')
        assert '35,0 ms' in page.locator('#art').text_content()
        page.evaluate('Deck.go(11,true)');page.locator('[data-quant="2"]').click()
        assert page.evaluate('Deck.state.quantBits')==2
        page.evaluate('Deck.go(4,true)');page.locator('[data-context="1"]').click()
        assert 'Un mois' in page.locator('#art').text_content()
        for index in [5,10,17]:
            page.evaluate('(i)=>Deck.go(i)',index)
            page.locator('[data-answer="0"]').click()
            assert page.locator('[data-answer="0"]').get_attribute('class')=='incorrect'
            assert page.locator('[data-answer="1"]').get_attribute('class')=='correct'
            assert page.locator('#feedback').inner_text()
        page.evaluate('Deck.go(0)');page.keyboard.press('ArrowRight')
        assert page.evaluate('Deck.state.index===0 && Deck.state.step===1')
        page.keyboard.press('ArrowRight');assert page.evaluate('Deck.state.index')==1
        page.keyboard.press('ArrowLeft');assert page.evaluate('Deck.state.index')==0
        page.locator('#toc').click();page.locator('[data-jump="8"]').click()
        assert page.evaluate('Deck.state.index')==8
        page.locator('[data-ref="R6"]').click();assert page.locator('#modal').get_attribute('open') is not None
        assert page.locator('#ref-R6').is_visible();page.locator('#close-modal').click()
        # The same SVG object is retained across scenes; movement is not only a fade.
        shared=page.evaluate('''()=>{Deck.go(0);window._node=document.querySelector('[data-key="model"]');
          const before=_node.style.transform;Deck.go(1);return {retained:_node===document.querySelector('[data-key="model"]'),
          moved:before!==_node.style.transform,transition:getComputedStyle(_node).transitionDuration};}''')
        assert shared['retained'] and shared['moved'] and '.95' in shared['transition']
        report['shared_object_transition']=shared
        page.evaluate('Deck.go(0,true)');page.wait_for_timeout(1000)
        before=page.locator('[data-key="model"]').evaluate('(e)=>getComputedStyle(e).transform')
        page.evaluate('Deck.go(1,true)');page.wait_for_timeout(200)
        during=page.locator('[data-key="model"]').evaluate('(e)=>getComputedStyle(e).transform')
        page.wait_for_timeout(1000)
        after=page.locator('[data-key="model"]').evaluate('(e)=>getComputedStyle(e).transform')
        assert len({before,during,after})==3,(before,during,after)
        report['observed_transition']={'before':before,'during':during,'after':after}
        viewports={}
        for width,height in [(1920,1080),(1366,768),(1024,768),(768,1024),(390,844)]:
            page.set_viewport_size({'width':width,'height':height});page.wait_for_timeout(40)
            failures=[]
            for index in range(23):
                page.evaluate('(i)=>Deck.go(i,true)',index)
                metrics=page.evaluate('''()=>{
                  const a=document.querySelector('#slide').getBoundingClientRect(),
                    f=document.querySelector('.slide-footer').getBoundingClientRect(),
                    c=document.querySelector('.copy').getBoundingClientRect(),v=document.querySelector('.visual').getBoundingClientRect();
                  return {fits:a.left>=-1&&a.right<=innerWidth+1&&a.top>=50&&a.bottom<=innerHeight-65,
                    copyFits:c.bottom<f.top-2,visualFits:Deck.slides[Deck.state.index].reading||v.bottom<f.top-2,
                    noScroll:document.documentElement.scrollWidth<=innerWidth&&document.documentElement.scrollHeight<=innerHeight};
                }''')
                if not all(metrics.values()):failures.append({'slide':index+1,**metrics})
            assert not failures,(width,height,failures)
            viewports[f'{width}x{height}']=failures
        report['viewports']=viewports
        page.locator('#reader-toggle').click()
        assert page.locator('#reader section').count()==23
        assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
        assert page.locator('#reader').is_visible()
        page.locator('#reader-toggle').click()
        page.set_viewport_size({'width':1366,'height':768})
        page.evaluate('Deck.go(0)');page.locator('#play').click()
        assert page.locator('#play').get_attribute('aria-pressed')=='true'
        page.evaluate('Deck.pause();Deck.go(5);document.querySelector("#play").click()')
        assert page.locator('#play').get_attribute('aria-pressed')=='false'
        report['interaction_checks']=['memory and KV controls','bandwidth bound','quantization controls',
          'context switch','three questions and feedback','keyboard navigation','outline','per-scene citations',
          'continuous mobile reading','auto-play stops at a question']
        references=page.evaluate('REFERENCES')
        assert len({r['id'] for r in references})==15
        assert not [u for u in requests if u.startswith('http')],requests
        browser.close()
        reduced=p.chromium.launch(executable_path=CHROME,headless=True)
        page=reduced.new_page(reduced_motion='reduce');page.goto((ROOT/'index.html').as_uri())
        assert page.evaluate('getComputedStyle(document.querySelector(".node")).transitionDuration')=='0s'
        reduced.close()
    assert not errors,errors
    report['console_errors']=errors;report['external_runtime_requests']=[];report['reduced_motion']='respected'
    with fitz.open(ROOT/'course.pdf') as doc:
        assert len(doc)==23
        assert doc.metadata['author']=='Roland Cédric TAYO'
        report['pdf_pages']=len(doc);report['pdf_links']=sum(len(p.get_links()) for p in doc)
        assert report['pdf_links']>=40
    (ROOT/'verification/browser-and-math.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    (ROOT/'references.json').write_text(json.dumps(references,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    lines=['# Sources du mini-cours','', 'Roland Cédric TAYO · INEM. Sources originales des notions et méthodes. Les démonstrations chiffrées sont analytiques ; aucun débit de LLM sur carte n’est revendiqué.','']
    for r in references:
        lines.extend([f'## {r["id"]} — {r["title"]}',f'{r["authors"]}. {r["year"]}. **{r["type"]}.**',f'[Source originale]({r["url"]})',r['use'],''])
    lines.extend(['## Inspiration visuelle','Nerdy Kings, [vidéo indiquée par l’enseignant](https://www.youtube.com/watch?v=gYG4J6Do0UU). Référence de rythme et de construction visuelle uniquement ; schémas et code du support originaux.',''])
    (ROOT/'SOURCES.md').write_text('\n\n'.join(lines).rstrip()+'\n',encoding='utf-8')
    print(json.dumps({'passed':True,'slides':23,'references':len(references),'viewports':len(viewports),'pdf_links':report['pdf_links']}))

if __name__=='__main__':main()
