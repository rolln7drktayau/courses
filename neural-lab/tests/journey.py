"""Verify manual learning first, then inference with the same model."""
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
    page=b.new_page(viewport={'width':1536,'height':1000});page.on('pageerror',lambda e:report['errors'].append(str(e)))
    page.goto(BASE);page.wait_for_function('!!window.Conversation')
    check('learning first by default',page.evaluate("Journey.mode==='train'&&Journey.model.updates===0"))
    check('inference initially locked',page.locator('#j-infer').is_disabled())
    check('natural text provided','Bonjour ! Comment vas-tu ?' in page.locator('#j-dataset').input_value())
    check('daily data are original examples','Exemples originaux' in page.locator('#chat-examples').inner_text())
    page.locator('#j-ingest').click();page.locator('#j-auto').click();original=page.evaluate('Journey.model.weights.slice()')
    check('real ingestion initializes the model',page.evaluate('Journey.dataAccepted&&Journey.model.type===\'mlp\''))
    page.locator('#j-next').click();page.evaluate('Journey.seek(.2)')
    check('tokenization visible and controllable','tokenisation' in page.locator('#j-title').inner_text() and page.evaluate('Journey.progress')==.2)
    page.locator('#scene').screenshot(path=str(ROOT/'validation/guided-tokenization.png'))
    page.locator('#j-next').click();check('vocabulary conversion visible','identifiant' in page.locator('#j-explain').inner_text())
    page.locator('#j-next').click();page.locator('[data-token="0"]').click();check('embedding selection is actual token ID',page.evaluate('Journey.selected')==0)
    page.locator('#scene').screenshot(path=str(ROOT/'validation/guided-lookup.png'))
    page.locator('#j-next').click();check('MLP hidden layer explained honestly','MLP' in page.locator('#j-take').inner_text() and 'attention' in page.locator('#j-take').inner_text())
    page.locator('#j-next').click();check('probabilities normalized',abs(sum(page.evaluate('Journey.trace.probabilities'))-1)<1e-12)
    page.locator('#j-next').click();check('real argmax selected',page.evaluate('Journey.chosen===Journey.trace.probabilities.indexOf(Math.max(...Journey.trace.probabilities))'))
    page.locator('#j-next').click();check('known answer used as target',page.evaluate("Journey.model.vocab[Journey.trace.target]==='J'"))
    check('weights fixed before correction',page.evaluate('Journey.model.weights')==original)
    page.locator('#j-next').click();check('gradients calculated',page.evaluate('Journey.trace.gradientComputed'))
    page.locator('#j-next').click();check('real parameter update',page.evaluate('Journey.model.updates')==1 and page.evaluate('Journey.model.weights')!=original)
    learned=page.evaluate('Journey.model.weights.slice()');page.locator('#j-prev').click();page.locator('#j-next').click()
    check('replay never doubles the update',page.evaluate('Journey.model.weights')==learned and page.evaluate('Journey.model.updates')==1)
    page.locator('#j-next').click();check('same-example improvement measured',page.evaluate('Journey.after.tape.v[Journey.after.loss]<Journey.trace.tape.v[Journey.trace.loss]'))
    check('inference unlocked after correction',not page.locator('#j-infer').is_disabled())
    page.screenshot(path=str(ROOT/'validation/guided-learning.png'),full_page=True)
    page.locator('#j-infer').click();check('inference reuses learned weights',page.evaluate('Journey.model.weights')==learned and page.evaluate('Journey.mode')=='infer')
    # Reference weights come from an executed learning campaign, not a fake answer table.
    page.locator('#j-ready').click();page.wait_for_function('Journey.model.updates===24000')
    prefix='Q:Bonjour ! Comment vas-tu ?\nR:';page.locator('#j-input').fill(prefix)
    check('speaker newline preserved',page.locator('#j-input').input_value()==prefix)
    fixed=page.evaluate('Journey.model.weights.slice()')
    for _ in range(7):page.locator('#j-next').click()
    check('inference does not change weights',page.evaluate('Journey.model.weights')==fixed)
    check('expected first character predicted',page.evaluate("Journey.model.vocab[Journey.chosen]==='J'"))
    page.locator('#j-again').click();check('continuation returns to input',page.evaluate('Journey.index')==0 and page.locator('#j-input').input_value()==prefix+'J')
    page.locator('#j-flat').click();check('2D alternative available',page.locator('#fallback').is_visible())
    page.locator('#j-input').fill('🙂 inconnu');page.locator('#j-next').click();page.locator('#j-next').click();check('unknown token explicit',page.evaluate('Journey.trace.tokens.includes(1)'))
    for width in [390,768,1280]:page.set_viewport_size({'width':width,'height':1000});check('no horizontal overflow '+str(width),page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'))
    check('no runtime errors',not report['errors']);report['browser']=b.version;b.close()
(ROOT/'validation/journey.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(str(len(report['checks']))+' guided checks passed')
