"""Run desktop/mobile layout checks and the actual slide interactions."""
from pathlib import Path
from datetime import datetime,timezone
import sys,json
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parent
OUTPUT=Path(sys.argv[2]) if len(sys.argv)>2 else ROOT/'verification'
OUTPUT.mkdir(exist_ok=True,parents=True)
URL=sys.argv[1] if len(sys.argv)>1 else (ROOT/'index.html').as_uri()
report={'executed_utc':datetime.now(timezone.utc).isoformat(),'url':URL,'checks':[],'errors':[],'layout_issues':[]}
def check(name,ok):
    assert ok,name
    report['checks'].append({'name':name,'passed':True})
with sync_playwright() as p:
    b=p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True)
    page=b.new_page(viewport={'width':1440,'height':900},reduced_motion='reduce')
    page.on('pageerror',lambda e:report['errors'].append(str(e)))
    page.goto(URL);page.wait_for_function('window.Course&&Course.ready')
    check('63 concepts and four activities loaded',page.evaluate('Course.total')==67)
    check('left/right keyboard controls explanation before changing topic',page.evaluate('Course.step')==0)
    page.keyboard.press('ArrowRight');check('one logical explanation advanced',page.evaluate('Course.step')==1)
    page.evaluate("Course.goId('etape-13')")
    before=page.evaluate('Composition.stats()')
    page.keyboard.press('ArrowRight')
    after=page.evaluate('Composition.stats()')
    check('diagram adds elements with the explanation',after['visible']>before['visible'])
    page.locator('#build-position').evaluate('(e)=>{e.value=3;e.dispatchEvent(new Event("input"))}')
    final=page.evaluate('Composition.stats()')
    check('last explanation builds the complete diagram',final['visible']==final['total'])
    page.locator('#build-position').evaluate('(e)=>{e.value=0;e.dispatchEvent(new Event("input"))}')
    check('rewinding removes later elements',page.evaluate('Composition.stats().visible')==before['visible'])
    check('chapter names are visible','Données' in page.locator('#journey').inner_text() and 'Chercher' in page.locator('#journey').inner_text())
    expected=[{'person','speech'},{'person','speech','compute','heard'},{'person','speech','compute','heard','lamp'},{'person','speech','compute','heard','lamp','command','offline'}]
    for phase,objects in enumerate(expected):
        page.evaluate(f"Course.goId('etape-1',{phase})")
        actual=page.evaluate('Composition.stats()')
        check(f'intro phase {phase+1} shows complete intended objects',set(actual['objects'])==objects)
        page.screenshot(path=str(OUTPUT/f'intro-phase-{phase+1}.png'))
    audit=page.evaluate('''()=>{const errors=[];let phases=0;for(let i=0;i<Course.total;i++){Course.show(i);if(Course.current.activity)continue;for(let j=0;j<Course.current.steps.length;j++){Course.show(i,j);const s=Composition.stats();phases++;if(s.missing||s.dangling.length)errors.push({id:s.id,phase:j,missing:s.missing,dangling:s.dangling});}const s=Composition.stats();if(s.visible!==s.total)errors.push({id:s.id,reason:'incomplete final diagram'})}return{errors,phases}}''')
    report['orchestration_audit']=audit
    check('every scene phase is authored and all connections have endpoints',not audit['errors'])
    for width,height in [(1440,900),(1280,720),(1024,768),(1920,1080),(390,844),(768,1024),(844,390)]:
        page.set_viewport_size({'width':width,'height':height})
        issues=page.evaluate('''()=>{const issues=[];for(let i=0;i<Course.total;i++){Course.show(i);for(let j=0;j<Course.current.steps.length;j++){Course.show(i,j);const c=document.querySelector('.copy');if(c.scrollHeight>c.clientHeight+2)issues.push({i:i+1,j:j+1,type:'copy',height:c.scrollHeight,available:c.clientHeight});}const s=document.querySelector('#slide').getBoundingClientRect(),v=document.querySelector('#viewport').getBoundingClientRect();if(s.left<v.left-2||s.right>v.right+2||s.top<v.top-2||s.bottom>v.bottom+2)issues.push({i:i+1,type:'canvas'});}return issues}''')
        report['layout_issues'] += [{'viewport':[width,height],**i} for i in issues]
        check(f'no page scroll at {width}x{height}',page.evaluate('document.documentElement.scrollWidth<=innerWidth+1&&document.documentElement.scrollHeight<=innerHeight+1'))
    if report['layout_issues']:(OUTPUT/'layout-issues.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    check('every explanation fits its authored area',not report['layout_issues'])
    for width,height in [(1440,900),(390,844),(768,1024),(844,390)]:
        page.set_viewport_size({'width':width,'height':height})
        over=page.evaluate('''()=>{let a=[];for(let i=0;i<Course.total;i++){Course.show(i);if(Course.current.widget)Course.manipulate();let e=document.querySelector('#scene .lab'),s=document.querySelector('#scene');if(e){const x=e.getBoundingClientRect(),y=s.getBoundingClientRect();if(x.top<y.top-2||x.bottom>y.bottom+2)a.push({i:i+1,top:y.top-x.top,bottom:x.bottom-y.bottom})}}return a}''')
        report['layout_issues'] += [{'viewport':[width,height],'type':'interactive-scene',**i} for i in over]
        check(f'interactive scenes fit at {width}x{height}',not over)
    page.set_viewport_size({'width':1440,'height':900})
    page.evaluate("Course.goId('etape-18');Course.manipulate()")
    page.locator('#gradient-step').click();check('real gradient produces loss .2048','0,2048' in page.locator('#gradient-out').inner_text())
    page.locator('#gradient-reset').click();check('weights can be reset','0,32' in page.locator('#gradient-out').inner_text())
    page.evaluate("Course.goId('etape-13');Course.manipulate()")
    page.locator('#x1').evaluate('(e)=>{e.value=2;e.dispatchEvent(new Event("input"))}')
    check('neuron control changes the computed score','z = −0,1' in page.locator('#neuron-out').inner_text() or 'z = -0,1' in page.locator('#neuron-out').inner_text())
    page.evaluate("Course.goId('etape-21');Course.manipulate()")
    page.locator('#conv-next').click();check('filter movement changes actual dot product','Position 2 : 2 × 1 − 0 = 2' in page.locator('#conv-out').inner_text())
    page.screenshot(path=str(OUTPUT/'slides-convolution.png'))
    page.evaluate("Course.goId('etape-24');Course.manipulate()")
    page.locator('#token-input').fill('la');one=page.locator('#token-cells .cell').nth(1).inner_text();page.locator('#token-input').fill('al');two=page.locator('#token-cells .cell').nth(0).inner_text();check('character IDs remain fixed between phrases',one==two)
    page.locator('#token-input').fill('<b>été</b>');check('typed text is literal, never HTML',page.locator('#token-cells .cell').count()==10)
    page.evaluate("Course.goId('etape-31');Course.manipulate()")
    page.locator('#memory-bits').select_option('8');check('835 int8 values occupy ideal 835 bytes','835 octets' in page.locator('#memory-out').inner_text())
    page.evaluate("Course.goId('etape-38');Course.manipulate()")
    page.locator('#quant-bits').select_option('2');check('simulated 2-bit quantization computes error .175','0,175' in page.locator('#quant-out').inner_text())
    page.evaluate("Course.goId('etape-42');Course.manipulate()")
    page.locator('#quality-min').evaluate('(e)=>{e.value=93;e.dispatchEvent(new Event("input"))}');check('constraint experiment detects no feasible candidate','aucune' in page.locator('#pareto-out').inner_text())
    # Assemble by clicks and by actual browser drag-and-drop.
    page.evaluate("Course.goId('assembler')")
    page.locator('#check-assembly').click();check('incorrect assembly has explanatory feedback','Pas encore' in page.locator('#assembly-result').inner_text())
    page.locator('[data-brick="0"]').drag_to(page.locator('[data-slot="0"]'))
    check('drag-and-drop places the chosen brick',page.evaluate('Course.state.assembly[0]')==0)
    for i in range(1,5):
        page.locator(f'[data-brick="{i}"]').click();page.locator(f'[data-slot="{i}"]').click()
    page.locator('#check-assembly').click();check('correct assembly validated','Chaîne cohérente' in page.locator('#assembly-result').inner_text())
    page.locator('#run-assembly').click();page.wait_for_function("document.querySelector('#assembly-result').textContent.includes('commandée')",timeout=7000)
    check('logical data flow reaches the actuator','commandée' in page.locator('#assembly-result').inner_text())
    page.screenshot(path=str(OUTPUT/'slides-assembly.png'))
    page.evaluate("Course.goId('objet-3d')")
    page.locator('[data-part="RAM"]').click();page.locator('#isolate').click();check('selected component isolates in 3D',page.locator('.board').evaluate("e=>e.classList.contains('isolated')"))
    page.locator('#yaw').evaluate('(e)=>{e.value=35;e.dispatchEvent(new Event("input"))}');check('rotation control changes real 3D transform','35deg' in page.locator('.board').get_attribute('style'))
    page.screenshot(path=str(OUTPUT/'slides-object-3d.png'))
    page.locator('#front').click();check('reassembly and frontal reset work',page.evaluate('Course.state.yaw===0&&!Course.state.isolated'))
    page.locator('#spin').click();check('continuous rotation can be activated',page.locator('.board-wrap').evaluate("e=>e.classList.contains('spinning')"));page.locator('#spin').click()
    page.evaluate("Course.goId('table-memoire')")
    check('memory example starts over budget','Dépassement : 12' in page.locator('#packing-out').inner_text())
    page.locator('#temp-memory').evaluate('(e)=>{e.value=48;e.dispatchEvent(new Event("input"))}');check('changing temporary memory changes budget to 96 bytes','96 octets' in page.locator('#packing-out').inner_text() and 'Marge restante : 4' in page.locator('#packing-out').inner_text())
    page.evaluate("Course.goId('aller-retour')")
    page.locator('#run-deploy').click();page.wait_for_function("document.querySelector('#deploy-out').textContent.includes('non mesuré')",timeout=5000)
    check('virtual deployment returns actual score and declares unmeasured time','-0,3' in page.locator('#deploy-out').inner_text() and 'non mesuré' in page.locator('#deploy-out').inner_text())
    page.evaluate("Course.goId('etape-39')");page.locator('#question').click()
    page.locator('[data-answer="0"]').click();check('quiz explains wrong answer','À revoir' in page.locator('.feedback').inner_text())
    page.locator('[data-answer="1"]').click();check('quiz explains right answer','Oui.' in page.locator('.feedback').inner_text());page.locator('#close-panel').click()
    quizzes=page.evaluate('COURSE_DATA.slides.map((s,i)=>({i,id:s.id,q:s.quiz})).filter(s=>s.q)')
    for width,height in [(1440,900),(390,844),(844,390)]:
        page.set_viewport_size({'width':width,'height':height})
        for quiz in quizzes:
            for answer in [0,1]:
                page.evaluate(f"Course.show({quiz['i']})");page.locator('#question').click()
                check(f"{quiz['id']} continue waits for response {width} answer {answer}",page.locator('#quiz-continue').is_disabled())
                page.locator(f'[data-answer="{answer}"]').click()
                check(f"{quiz['id']} response enables continue {width} answer {answer}",not page.locator('#quiz-continue').is_disabled())
                fits=page.evaluate('''()=>{const c=document.querySelector('#panel-content'),b=document.querySelector('#quiz-continue').getBoundingClientRect(),p=document.querySelector('#panel').getBoundingClientRect(),f=document.querySelector('.feedback').getBoundingClientRect();return c.scrollHeight<=c.clientHeight+2&&b.bottom<=p.bottom&&f.bottom<=b.top+2}''')
                check(f"{quiz['id']} correction and continue fit {width} answer {answer}",fits)
                page.locator('#quiz-continue').click()
                check(f"{quiz['id']} continue advances once {width} answer {answer}",page.evaluate('Course.position')==quiz['i']+1 and not page.locator('#panel').evaluate('e=>e.open'))
    page.set_viewport_size({'width':1440,'height':900})
    for tool in ['plan','lexicon','references']:
        page.locator('#'+tool).click();check(tool+' opens without scrolling',page.locator('#panel').evaluate('e=>e.open&&e.scrollHeight<=e.clientHeight+1'));page.keyboard.press('Escape')
    for width,height in [(1440,900),(390,844),(844,390)]:
        page.set_viewport_size({'width':width,'height':height})
        modal_issues=[]
        for tool in ['plan','lexicon','references']:
            page.locator('#'+tool).click();n=0
            while True:
                if page.locator('#panel-content').evaluate('e=>e.scrollHeight>e.clientHeight+2'):modal_issues.append([tool,n])
                if page.locator('#panel-next').is_disabled():break
                page.locator('#panel-next').click();n+=1
                assert n<100
            page.keyboard.press('Escape')
        check(f'plan glossary and sources fit at {width}x{height}',not modal_issues)
    page.set_viewport_size({'width':1440,'height':900})
    page.locator('#fullscreen').click();page.wait_for_function('!!document.fullscreenElement');check('native fullscreen works',page.evaluate('!!document.fullscreenElement'));page.locator('#fullscreen').click()
    page.evaluate("Course.goId('etape-1')");page.screenshot(path=str(OUTPUT/'slides-entry.png'))
    page.set_viewport_size({'width':390,'height':844});page.screenshot(path=str(OUTPUT/'slides-mobile.png'))
    moving=b.new_page(viewport={'width':1440,'height':900},reduced_motion='no-preference')
    moving.on('pageerror',lambda e:report['errors'].append(str(e)))
    moving.goto(URL);moving.wait_for_function('window.Course&&Course.ready')
    moving.evaluate("Course.goId('etape-1')");moving.locator('#build-speed').select_option('4');moving.locator('#animate').click()
    for phase,objects in enumerate(expected):
        moving.wait_for_function(f'Course.step==={phase}',timeout=12000)
        check(f'intro autoplay phase {phase+1} follows authored order',set(moving.evaluate('Composition.stats().objects'))==objects)
        moving.wait_for_timeout(1050)
        moving.screenshot(path=str(OUTPUT/f'intro-autoplay-{phase+1}.png'))
    moving.locator('#animate').click()
    moving.evaluate("Course.goId('etape-13')");moving.locator('#next').click()
    check('construction uses real browser animations',moving.evaluate("document.querySelector('#scene').getAnimations({subtree:true}).length>0"))
    moving.locator('#build-speed').select_option('4');moving.locator('#animate').click();moving.wait_for_timeout(250);moving.locator('#animate').click()
    frozen=moving.evaluate('Course.step');moving.wait_for_timeout(moving.evaluate('Course.autoplayDelay')+100)
    check('pause freezes the timeline',moving.evaluate('Course.step')==frozen)
    moving.locator('#build-position').evaluate('(e)=>{e.value=3;e.dispatchEvent(new Event("input"))}')
    moving.wait_for_timeout(700);moving.screenshot(path=str(OUTPUT/'slides-neuron-built.png'))
    moving.evaluate("Course.goId('objet-3d')");moving.locator('#spin').click();a=moving.locator('.board').evaluate('e=>getComputedStyle(e).transform');moving.wait_for_timeout(350);bb=moving.locator('.board').evaluate('e=>getComputedStyle(e).transform')
    check('3D spin changes the rendered transformation',a!=bb);moving.locator('#spin').click();moving.close()
    check('no JavaScript runtime errors',not report['errors']);report['browser']=b.version;b.close()
(OUTPUT/'slides-validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'checks_passed':len(report['checks']),'layout_issues':len(report['layout_issues']),'errors':report['errors']}))
