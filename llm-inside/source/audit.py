"""Check both routes, analytical calculations, controls and illustrative data."""
from pathlib import Path
import csv,hashlib,json,math,statistics
import fitz
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
CHROME=r'C:\Program Files\Google\Chrome\Application\chrome.exe'

def main():
    errors=[];requests=[];report={}
    with sync_playwright() as p:
        browser=p.chromium.launch(executable_path=CHROME,headless=True)
        page=browser.new_page(viewport={'width':1600,'height':1000})
        page.on('pageerror',lambda e:errors.append(str(e)))
        page.on('request',lambda r:requests.append(r.url))
        page.goto((ROOT/'index.html').as_uri());page.wait_for_function('window.Deck')
        def go(sid,full=True):page.evaluate('([id,full])=>Deck.goTo(id,full)',[sid,full])
        def audience(name):page.evaluate('(name)=>Deck.setAudience(name)',name)
        assert page.evaluate('Deck.state.audience')=='discovery'
        assert page.evaluate('Deck.slides.length')==18
        assert page.evaluate('Deck.slides.filter(s=>!s.reading).length')==15
        assert page.evaluate('Deck.allSlides.every(s=>s.reading||(s.steps.length===3&&s.phase>=1&&s.phase<=5))')
        core=page.evaluate('Deck.slides.map(s=>s.id)')
        assert not set(core)&{'distributed','attention-math','architectures','q-hash','bitnet','speculative'}
        for sid in core:
            go(sid);assert page.locator('#body .equation').count()==0,sid
        go('attention');assert 'Q :' not in page.locator('#art').text_content()
        go('quantize');assert 'wᵢxᵢ' not in page.locator('#art').text_content()
        go('embedding',False)
        assert page.locator('#scene-steps button').count()==3
        assert page.locator('#scene-steps button.current').get_attribute('data-scene-step')=='0'
        assert page.locator('[data-key="embedding-result"]').evaluate('(e)=>e.style.opacity')=='0'
        page.locator('[data-scene-step="1"]').click()
        assert page.locator('[data-key="embedding-table"]').evaluate('(e)=>e.style.opacity')=='1'
        assert page.locator('[data-key="embedding-result"]').evaluate('(e)=>e.style.opacity')=='0'
        page.locator('[data-scene-step="2"]').click()
        assert page.locator('[data-key="embedding-result"]').evaluate('(e)=>e.style.opacity')=='1'
        assert 'Une ligne' not in page.locator('#art').text_content()
        page.locator('[data-embedding="2"]').click()
        assert '[ 0,6 ; 0,1 ; −0,2 ]' in page.locator('[data-key="embedding-result"]').text_content()
        go('embedded-constraints');assert 'Énergie et chaleur' in page.locator('#art').text_content()
        assert page.locator('#journey button.current').get_attribute('data-phase')=='1'
        go('optimization-levers');page.locator('[data-lever="1"]').click()
        assert 'Coder les poids avec moins de bits' in page.locator('#art').text_content()
        go('research');page.locator('#prepare-research').click()
        for name in ['brick','change','mechanism','constraints','protocol','falsification']:
            page.locator(f'textarea[name="{name}"]').fill('Test pédagogique : '+name)
        with page.expect_download() as pending:page.locator('#download-research').click()
        hypothesis=json.loads(Path(pending.value.path()).read_text(encoding='utf-8'))
        assert hypothesis['kind']=='hypothesis_not_results' and hypothesis['falsification']
        page.locator('#close-modal').click()
        report['teaching_stages']={'steps_per_diagram':3,'selected_embedding':'dort','five_part_path':True,'hypothesis_download':'checked; no measurements claimed'}
        values=page.evaluate('''()=>{
          const m=MathLab,q=m.quantize([-.9,-.32,.18,.76],4);
          return {weights16:m.weightBytes(7e9,16),weights4:m.weightBytes(7e9,4),cacheBytes:m.kvBytes(32,8192,8,128,2),roof:m.roofline(7e9,4,50e9,2e12),computeLimited:m.roofline(7e9,4,50e9,1e11),quant:q,before:m.dot([-.9,-.32,.18,.76],[1,.5,-1,.25]),after:m.dot(q.codes.map(v=>v*q.scale),[1,.5,-1,.25]),budget8:m.memoryBudget(7e9,4,32,8192,8,128,2,1,8),budget4:m.memoryBudget(7e9,4,32,8192,8,128,2,1,4)};
        }''')
        assert values['weights16']==14_000_000_000 and values['weights4']==3_500_000_000
        assert values['cacheBytes']==2**30
        assert math.isclose(values['roof']['bound'],.07) and math.isclose(values['computeLimited']['bound'],.14)
        assert values['quant']['codes']==[-7,-2,1,6]
        assert math.isclose(values['before'],-1.05) and math.isclose(values['after'],-.9642857142857144)
        assert math.isclose(values['budget8']['total'],5.573741824)
        assert values['budget8']['margin']>0>values['budget4']['margin']
        report['analytical_examples']=values
        go('weights');page.locator('[data-bits="4"]').click();assert '3,50 Go' in page.locator('#art').text_content()
        go('cache');assert page.locator('#heads').count()==0
        page.locator('#cache-size').select_option('32768');assert '4,29 Go' in page.locator('#art').text_content()
        go('memory-total');page.evaluate('Deck.state.cache=8192;Deck.draw()');assert '5,57 Go' in page.locator('#art').text_content()
        page.locator('#budget-cap').click();assert 'Dépassement' in page.locator('#art').text_content()
        page.locator('#budget-bits').click();assert '16,07 Go' in page.locator('#art').text_content()
        go('roofline');page.locator('#compute').click();assert '140,0 ms' in page.locator('#art').text_content()
        page.locator('#compute').click();page.locator('#bandwidth').fill('100');assert '35,0 ms' in page.locator('#art').text_content()
        go('attention');page.locator('[data-context="1"]').click();assert 'Un mois' in page.locator('#art').text_content()
        page.locator('[data-detail="attention-math"]').click();assert page.evaluate('Deck.state.audience')=='engineer'
        assert page.locator('#body .equation').count()==1 and 'Q :' in page.locator('#art').text_content()
        page.locator('#audience').click();assert page.evaluate('Deck.slides[Deck.state.index].id')=='attention'
        audience('engineer');assert page.evaluate('Deck.slides.length')==33
        go('cache-math');page.locator('#cache-size').select_option('32768');small=page.locator('[data-key="kv"] rect').count()-1
        page.locator('#heads').click();assert page.locator('[data-key="kv"] rect').count()-1==4*small
        assert '17,18 Go' in page.locator('#art').text_content()
        order=page.evaluate('Deck.slides.map(s=>s.id)');assert order.index('q-hash')==order.index('architectures')+1
        for sid in ['q-memory','q-bandwidth','q-hash']:
            go(sid,False);a=page.evaluate('Deck.slides[Deck.state.index].answer');wrong=(a+1)%3
            page.locator(f'[data-answer="{wrong}"]').click()
            assert 'incorrect' in page.locator(f'[data-answer="{wrong}"]').get_attribute('class')
            assert 'correct' in page.locator(f'[data-answer="{a}"]').get_attribute('class')
        go('q-hash');assert 'voisin' in page.locator('#feedback').inner_text()
        with (ROOT/'assets/comparison-example.csv').open(newline='') as f:sample=list(csv.DictReader(f))
        assert len(sample)==2 and all(r['kind']=='illustrative_not_measured' for r in sample)
        assert all(r['prompt_tokens']=='128' and r['generated_tokens']=='20' and r['model_loading_included']=='false' for r in sample)
        assert float(sample[1]['median_ms'])<float(sample[0]['median_ms']) and int(sample[1]['correct'])<47<=int(sample[0]['correct'])
        with (ROOT/'assets/comparison-timing-samples.csv').open(newline='') as f:raw=list(csv.DictReader(f))
        for summary in sample:
            timings=[float(r['elapsed_ms']) for r in raw if r['version']==summary['version']]
            assert len(timings)==5 and statistics.median(timings)==float(summary['median_ms'])
            assert min(timings)==float(summary['min_ms']) and max(timings)==float(summary['max_ms'])
        go('measurement-example');assert '46 / 50' in page.locator('#art').text_content()
        report['comparison_example']={'kind':'illustrative_not_measured','source':'assets/comparison-example.csv','rows':sample,'decision':'variant fails quality threshold'}
        go('embedding');page.locator('[data-term="token"]').first.click();assert 'Unité traitée' in page.locator('#modal-content').inner_text();page.locator('#close-modal').click()
        page.locator('[data-term="token"]').first.focus();page.keyboard.press('Space');assert page.locator('#modal').get_attribute('open') is not None;page.locator('#close-modal').click()
        glossary=page.evaluate('KEYWORDS');assert all(k['definition'].strip() for k in glossary);report['defined_keywords']=len(glossary)
        go('opening',False);page.keyboard.press('ArrowRight');assert page.evaluate('Deck.state.step')==1
        page.keyboard.press('ArrowRight');assert page.evaluate('Deck.state.step')==2
        page.keyboard.press('ArrowRight');assert page.evaluate('Deck.slides[Deck.state.index].id')=='embedded-constraints'
        page.keyboard.press('ArrowLeft');assert page.evaluate('Deck.state.step')==2
        go('opening');page.wait_for_timeout(1000);before=page.locator('[data-key="model"]').evaluate('(e)=>getComputedStyle(e).transform')
        go('learn');page.wait_for_timeout(200);during=page.locator('[data-key="model"]').evaluate('(e)=>getComputedStyle(e).transform')
        page.wait_for_timeout(1000);after=page.locator('[data-key="model"]').evaluate('(e)=>getComputedStyle(e).transform');assert len({before,during,after})==3
        report['observed_transition']={'before':before,'during':during,'after':after};report['viewports']={}
        for route in ['discovery','engineer']:
            audience(route);count=page.evaluate('Deck.slides.length')
            for width,height in [(1920,1080),(1366,768),(1024,768),(768,1024),(390,844)]:
                page.set_viewport_size({'width':width,'height':height});page.wait_for_timeout(40);failures=[]
                for i in range(count):
                    page.evaluate('(i)=>Deck.go(i,true)',i)
                    ok=page.evaluate('''()=>{
                      const a=document.querySelector('#slide').getBoundingClientRect(),f=document.querySelector('.slide-footer').getBoundingClientRect(),c=document.querySelector('.copy').getBoundingClientRect(),v=document.querySelector('.visual').getBoundingClientRect();
                      return a.left>=-1&&a.right<=innerWidth+1&&a.top>=50&&a.bottom<=innerHeight-65&&c.bottom<f.top-2&&(Deck.slides[Deck.state.index].reading||v.bottom<f.top-2)&&document.documentElement.scrollWidth<=innerWidth&&document.documentElement.scrollHeight<=innerHeight;
                    }''')
                    if not ok:failures.append(i+1)
                assert not failures,(route,width,height,failures);report['viewports'][f'{route}/{width}x{height}']=failures
            page.locator('#reader-toggle').click();assert page.locator('#reader section').count()==count
            assert page.evaluate('document.documentElement.scrollWidth<=innerWidth');page.locator('#reader-toggle').click()
        page.set_viewport_size({'width':1366,'height':768});audience('discovery');go('q-memory',False);page.locator('#play').click();assert not page.evaluate('Deck.state.auto')
        references=page.evaluate('REFERENCES');assert len(references)==19 and not [u for u in requests if u.startswith('http')];browser.close()
        b=p.chromium.launch(executable_path=CHROME,headless=True);page=b.new_page(reduced_motion='reduce');page.goto((ROOT/'index.html').as_uri());assert page.evaluate('getComputedStyle(document.querySelector(".node")).transitionDuration')=='0s';b.close()
    assert not errors,errors
    report.update(console_errors=errors,external_runtime_requests=[],reduced_motion='respected',discovery_scenes=15,discovery_pages=18,engineer_pages=33,pdfs={})
    for name,pages in [('course.pdf',18),('engineering.pdf',33)]:
        with fitz.open(ROOT/name) as doc:
            assert len(doc)==pages and doc.metadata['author']=='Roland Cédric TAYO'
            report['pdfs'][name]={'pages':len(doc),'links':sum(len(p.get_links()) for p in doc),'sha256':hashlib.sha256((ROOT/name).read_bytes()).hexdigest()}
    (ROOT/'verification/browser-and-math.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    (ROOT/'references.json').write_text(json.dumps(references,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    lines=['# Sources du mini-cours','Roland Cédric TAYO · INEM. Sources originales. Comptes analytiques ; tableau de comparaison fictif. Aucun débit de LLM sur carte revendiqué.']
    for r in references:lines.extend([f'## {r["id"]} — {r["title"]}',f'{r["authors"]}. {r["year"]}. **{r["type"]}.**',f'[Source originale]({r["url"]})',r['use']])
    lines.extend(['## Inspiration visuelle','Nerdy Kings, [vidéo indiquée par l’enseignant](https://www.youtube.com/watch?v=gYG4J6Do0UU). Référence de rythme ; schémas et code originaux.'])
    (ROOT/'SOURCES.md').write_text('\n\n'.join(lines)+'\n',encoding='utf-8')
    print(json.dumps({'passed':True,'discovery_pages':18,'engineer_pages':33,'viewports':10,'references':len(references)}))
if __name__=='__main__':main()
