"""Exercise live phrase/data ingestion, real token mapping and controllable motion."""
from pathlib import Path
from datetime import datetime,timezone
import json,sys,hashlib
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
BASE=sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:8766/neural-lab/'
report={'executed_utc':datetime.now(timezone.utc).isoformat(),'url':BASE,'checks':[],'errors':[]}
def check(name,ok):
    assert ok,name
    report['checks'].append({'name':name,'passed':True})
with sync_playwright() as p:
    browser=p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True,args=['--enable-unsafe-swiftshader'])
    page=browser.new_page(viewport={'width':1536,'height':1100})
    page.on('pageerror',lambda e:report['errors'].append(str(e)))
    page.goto(BASE);page.wait_for_function('!!window.Journey')
    page.locator('#open-conversation').click();page.locator('#chat-load').click();page.wait_for_function("Journey.mode==='infer'");page.evaluate('Journey.pause()')
    phrase='la lampe est allumee'
    page.locator('#j-input').fill(phrase)
    weights=page.evaluate('Journey.model.weights.slice()')
    page.locator('#j-run').click();page.wait_for_timeout(500)
    check('phrase playback really advances',0<page.evaluate('Journey.progress')<1)
    page.locator('#j-auto').click();progress=page.evaluate('Journey.progress');page.wait_for_timeout(250)
    check('pause freezes timeline',page.evaluate('Journey.progress')==progress)
    page.evaluate('Journey.seek(.1)');before=page.evaluate("Lab.scene.lessonCards.find(x=>x.card.key==='sentence').container.position.x")
    page.evaluate('Journey.seek(.85)');after=page.evaluate("Lab.scene.lessonCards.find(x=>x.card.key==='sentence').container.position.x")
    check('the phrase physically moves into the scene',before<after)
    check('input buffer reflects actual phrase count','17 / 20' in page.locator('#j-live').inner_text())
    page.locator('#j-next').click();page.evaluate('Journey.seek(.12)')
    early=page.evaluate("Lab.scene.lessonCards.filter(x=>x.card.key.startsWith('part')).map(x=>x.card.subtitle)")
    page.evaluate('Journey.seek(.88)')
    late=page.evaluate("Lab.scene.lessonCards.filter(x=>x.card.key.startsWith('part')).map(x=>x.card.subtitle)")
    check('tokenization follows the whole phrase, not only its tail',early[0]=='token n°0' and late[0]=='token n°16')
    check('token receipt has visibly separate tiles',page.locator('#j-receipt .j-buffer').get_attribute('class').find('tokens')>=0)
    page.screenshot(path=str(ROOT/'validation/phrase-in-motion.png'),full_page=True)
    page.locator('#j-next').click();page.evaluate('Journey.seek(.4)')
    check('IDs are actual vocabulary lookups',page.evaluate("Lab.scene.lessonCards.find(x=>x.card.key==='id0').card.title===String(Journey.model.vocab.indexOf(Array.from(document.querySelector('#j-input').value)[8]))"))
    page.locator('#j-next').click();page.evaluate('Journey.seek(1)')
    check('context restriction is explicitly visible','hors de la fenêtre' in page.locator('#j-receipt').inner_text())
    check('inference has not modified any weight',page.evaluate('Journey.model.weights')==weights)
    # Verify automatic traversal, not merely the manual next button.
    page.locator('#j-run').click();page.locator('#j-speed').select_option('2');page.wait_for_function('Journey.index>=1',timeout=12000);page.locator('#j-auto').click()
    check('playback automatically reaches tokenization',page.evaluate('Journey.index')==1)
    page.locator('#j-train').click()
    corpus=('capteur rouge. arret moteur. signal vert. avance lente. ')*4
    page.locator('#j-datafile').set_input_files({'name':'atelier.txt','mimeType':'text/plain','buffer':corpus.encode('utf-8')})
    page.wait_for_function("document.querySelector('#j-data-info').textContent.includes('atelier.txt lu')")
    check('UTF8 file is actually read',page.locator('#j-dataset').input_value()==corpus)
    page.locator('#j-example').fill('12');page.locator('#j-ingest').click();page.wait_for_timeout(150);page.locator('#j-auto').click()
    check('new model uses exactly the supplied dataset',page.evaluate('Journey.model.corpus')==corpus)
    check('source filename and sample count recorded','atelier.txt' in page.locator('#j-data-info').inner_text() and str(len(corpus)-1)+' exemples' in page.locator('#j-data-info').inner_text())
    check('training vocabulary comes from these data',page.evaluate('Journey.model.vocab.slice(2)')==sorted(set(corpus)))
    page.evaluate('Journey.seek(.5)');check('dataset receipt count is real',str(len(corpus)//2)+' / '+str(len(corpus)) in page.locator('#j-live').inner_text())
    page.locator('#j-next').click();page.evaluate('Journey.seek(.9)')
    check('training tokenizes the entire dataset',str(len(corpus))+' caractères découpés' in page.locator('#j-live').inner_text())
    page.locator('#j-next').click();page.evaluate('Journey.seek(1)')
    page.locator('#j-next').click();check('context and expected answer are visibly separated',page.locator('.j-training-pair').count()==1)
    pair=page.evaluate('Journey.pair')
    check('training sample is extracted without invented examples',pair['text']==corpus[:12] and pair['next']==corpus[12])
    page.screenshot(path=str(ROOT/'validation/dataset-to-example.png'),full_page=True)
    for _ in range(7):page.locator('#j-next').click()
    check('real update on the supplied data',page.evaluate('Journey.model.updates')==1 and page.evaluate('Journey.after.tape.v[Journey.after.loss]<Journey.trace.tape.v[Journey.trace.loss]'))
    report['dataset']={'file':'atelier.txt','characters':len(corpus),'sha256':hashlib.sha256(corpus.encode()).hexdigest(),'pair':{'text':pair['text'],'next':pair['next'],'at':pair['at']}}
    # Malformed input must not silently replace the accepted data/model.
    page.locator('#j-editdata').click()
    page.locator('#j-datafile').set_input_files({'name':'invalid.txt','mimeType':'text/plain','buffer':b'\xff\xfe\xff'})
    page.wait_for_function("document.querySelector('#j-data-info').textContent.includes('Lecture impossible')")
    check('invalid UTF8 rejected without changing the model',page.evaluate('Journey.model.corpus')==corpus)
    for width in [390,768,1280]:
        page.set_viewport_size({'width':width,'height':1000});check('ingestion controls fit '+str(width),page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'))
    check('no runtime errors',not report['errors']);report['browser']=browser.version;browser.close()
(ROOT/'validation/ingestion.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(str(len(report['checks']))+' ingestion checks passed')
