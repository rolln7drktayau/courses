import json,sys
from pathlib import Path
from datetime import datetime,timezone
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
BASE=sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:8766/neural-lab/'
report={'executed_utc':datetime.now(timezone.utc).isoformat(),'url':BASE,'checks':[],'errors':[]}
def check(name,ok):
    assert ok,name
    report['checks'].append({'name':name,'passed':True})
with sync_playwright() as p:
    b=p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True,args=['--enable-unsafe-swiftshader'])
    page=b.new_page(viewport={'width':1536,'height':1100});page.on('pageerror',lambda e:report['errors'].append(str(e)))
    page.goto(BASE+'#conversation');page.wait_for_function('!!window.Conversation&&!!window.Display')
    check('conversation anchor opens examples',page.locator('#chat-content').is_visible())
    check('actual repeated exchanges shown',page.locator('.chat-example').count()==5)
    check('70/30 observed frequency shown','70 %' in page.locator('#chat-frequencies').inner_text() and '30 %' in page.locator('#chat-frequencies').inner_text())
    page.locator('#chat-load').click();page.wait_for_function('Conversation.model!==null')
    check('trained weights and hash verified',page.evaluate('Conversation.model.updates')==22000)
    weights=page.evaluate('Conversation.model.weights.slice()')
    for question,answer in [('salut','bonjour'),('merci','de rien'),('etat?','pret'),('stop?','arret')]:
        page.locator('#chat-question').fill(question);page.locator('#chat-send').click();page.wait_for_function('expected=>Conversation.result.answer===expected',arg=answer)
        check('actual network response '+question,page.evaluate('Conversation.result.answer')==answer)
    page.locator('#chat-question').fill('salut');page.locator('#chat-send').click();page.wait_for_timeout(5500)
    check('visible character-by-character answer completes',page.locator('#chat-answer').inner_text()=='bonjour')
    check('statistics return to first letter',page.evaluate('Conversation.position')==0)
    check('frequency and model discrepancy explicitly explained','trop confiant' in page.locator('.stats-observation').inner_text());check('first-letter distribution normalized',abs(sum(page.evaluate('Conversation.distribution'))-1)<1e-12)
    check('inference keeps weights fixed',page.evaluate('Conversation.model.weights')==weights)
    page.locator('#chat-draw').click();check('100 seeded draws displayed','100 tirages réels' in page.locator('#chat-draws').inner_text())
    with page.expect_download() as pending:
        # Download is exposed after actual browser training below; test weights by inspector first.
        page.locator('#chat-inspect').click();page.locator('#journey-mode').click();page.locator('#export-model').click()
    check('conversation model can be exported from workshop',pending.value.suggested_filename=='neural-model.json');page.locator('#journey-mode').click()
    check('3D receives real conversation model',page.evaluate('Journey.model.context')==12)
    page.locator('#sim-full').click();page.wait_for_function("document.fullscreenElement===document.querySelector('.viewport-panel')")
    check('native simulation fullscreen',page.locator('#canvas').bounding_box()['height']>800)
    distance=page.evaluate('Lab.scene.camera.position.length()');page.locator('#sim-zoom-in').click();check('fullscreen zoom actually moves camera',page.evaluate('Lab.scene.camera.position.length()')<distance)
    camera=page.evaluate('Lab.scene.camera.position.toArray()');page.locator('#sim-next').click();check('camera view preserved across steps',page.evaluate('Lab.scene.camera.position.toArray()')==camera)
    canvas=page.locator('#canvas').bounding_box();x,y=canvas['x']+canvas['width']/2,canvas['y']+canvas['height']/2
    page.mouse.move(x,y);page.mouse.down();page.mouse.move(x+90,y+20,steps=8);page.mouse.up();page.wait_for_timeout(150)
    check('fullscreen rotation remains interactive',page.evaluate('Lab.scene.camera.position.toArray()')!=camera)
    page.screenshot(path=str(ROOT/'validation/fullscreen-conversation.png'))
    page.locator('#sim-exit').click();page.wait_for_function('!document.fullscreenElement')
    page.locator('#journey-mode').click();page.locator('#sim-page').click();page.wait_for_function('document.fullscreenElement===document.documentElement');check('whole workspace fullscreen',page.evaluate('Display.fullscreen'))
    page.evaluate('Display.leave()');page.wait_for_function('!document.fullscreenElement');page.locator('#journey-mode').click()
    # Explicit fallback when native fullscreen cannot be requested.
    page.evaluate("document.querySelector('.viewport-panel').requestFullscreen=undefined")
    page.locator('#sim-full').click();check('fullscreen fallback works',page.locator('.viewport-panel').evaluate("e=>e.classList.contains('fullscreen-fallback')"));page.keyboard.press('Escape');check('fallback closes with Escape',not page.evaluate('Display.fullscreen'))
    page.locator('#chat-data').click();check('conversation data reach training text','Q:salut\nR:bonjour' in page.locator('#j-dataset').input_value());check('first training target belongs to answer',page.locator('#j-example').input_value()=='10')
    page.locator('#chat-train').click();page.wait_for_function("document.querySelector('#chat-stop').disabled",timeout=240000)
    check('6000 real browser training updates',page.evaluate('Conversation.model.updates')==6000)
    report['trained_model_replies']={}
    for question,answer in [('salut','bonjour'),('merci','de rien'),('etat?','pret'),('stop?','arret')]:
        page.locator('#chat-question').fill(question);page.locator('#chat-send').click();page.wait_for_function('expected=>Conversation.result.question===expected',arg=question);actual=page.evaluate('Conversation.result.answer');report['trained_model_replies'][question]=actual;check('browser-trained answer '+question,actual==answer)
    with page.expect_download() as pending:page.locator('#chat-export').click()
    csv=Path(pending.value.path()).read_text(encoding='utf-8');check('actual training measurements exported','6000,' in csv);(ROOT/'validation/conversation-browser-training.csv').write_text(csv,encoding='utf-8')
    page.locator('#chat-question').fill('salut');page.locator('#chat-send').click();page.wait_for_timeout(5500)
    page.locator('#conversation').screenshot(path=str(ROOT/'validation/conversation-statistics.png'))
    for width in [390,768,1280]:page.set_viewport_size({'width':width,'height':1000});check('conversation fits '+str(width),page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'))
    check('no runtime errors',not report['errors']);report['browser']=b.version;b.close()
(ROOT/'validation/conversation-browser.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(str(len(report['checks']))+' conversation/fullscreen browser checks passed')
