"""Validate the required order: natural dialogue training, then automatic inference."""
from pathlib import Path
from datetime import datetime,timezone
import json,sys
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
    check('learning is the initial phase',page.evaluate("Journey.mode==='train'&&Journey.model.updates===0"))
    check('inference disabled before learned weights',page.locator('#j-infer').is_disabled())
    text=page.locator('#j-dataset').input_value();check('daily-life sentences supplied',all(s in text for s in ['Bonjour ! Comment vas-tu ?','Tu veux un café ?','On va marcher au parc ?']))
    check('plain text keeps speaker turns and paragraph breaks','\nR:Je vais bien, merci.\nQ:Tu veux un café ?' in text and '\n\nQ:' in text)
    page.screenshot(path=str(ROOT/'validation/daily-learning-first.png'))
    page.locator('#open-conversation').click()
    check('complete dialogues displayed',page.locator('.daily-dialogue').count()==3 and page.locator('.daily-turn').count()==12)
    check('original examples distinguished from DailyDialog','ne sont pas des extraits' in page.locator('#chat-examples').inner_text())
    check('response form locked before training',page.locator('#chat-question').is_disabled())
    # An interrupted run must not be presented as completed learning.
    page.locator('#chat-train').click();page.wait_for_function("Number(document.querySelector('#chat-training').textContent.split('/')[0])>=2000",timeout=120000)
    page.locator('#chat-stop').click();page.wait_for_function("document.querySelector('#chat-stop').disabled",timeout=30000)
    check('cancelled run does not launch inference',page.evaluate("Journey.mode==='train'&&!Conversation.pendingAutomatic&&Conversation.result===null"))
    check('cancellation explicitly stated','interruption' in page.locator('#chat-state').inner_text())
    # Complete the actual browser learning run from fresh weights.
    page.locator('#j-speed').select_option('2');page.locator('#chat-train').click();page.wait_for_function("document.querySelector('#chat-stop').disabled",timeout=240000)
    check('24000 real corrections completed',page.evaluate('Conversation.model.updates')==24000)
    check('completion automatically switches to inference',page.evaluate("Journey.mode==='infer'&&Conversation.pendingAutomatic"))
    check('3D simulation automatically starts',page.evaluate('Journey.running'))
    check('identical learned weights used in inference',page.evaluate('JSON.stringify(Journey.model.weights)===JSON.stringify(Conversation.model.weights)'))
    check('speaker newline preserved in actual model input','\nR:' in page.locator('#j-input').input_value())
    check('inference form unlocked after completion',not page.locator('#chat-question').is_disabled())
    # No click after learning: the entire first inference cycle must run itself.
    page.wait_for_function('Conversation.result!==null&&!Conversation.generating',timeout=90000)
    check('natural answer generated without extra send click',page.evaluate('Conversation.result.answer')=='Je vais bien, merci.')
    check('answer visible next to simulation','Je vais bien, merci.' in page.locator('#j-live-dialogue .live-answer').inner_text())
    check('3D probabilities exactly match the response calculation',page.evaluate('JSON.stringify(Journey.trace.probabilities)===JSON.stringify(Conversation.result.trace[0].probabilities)'))
    report['automatic_reply']=page.evaluate('({question:Conversation.result.question,answer:Conversation.result.answer,updates:Conversation.model.updates,type:Conversation.model.type})')
    page.screenshot(path=str(ROOT/'validation/daily-automatic-inference.png'),full_page=True)
    with page.expect_download() as pending:page.locator('#chat-export').click()
    csv=Path(pending.value.path()).read_text(encoding='utf-8');check('full training measurements exported','24000,' in csv)
    (ROOT/'validation/conversation-browser-training.csv').write_text(csv,encoding='utf-8')
    for width in [390,768,1280]:
        page.set_viewport_size({'width':width,'height':1000});check('learning-first layout fits '+str(width),page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'))
    check('no runtime errors',not report['errors']);report['browser']=b.version;b.close()
(ROOT/'validation/daily-flow.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(str(len(report['checks']))+' learning-to-inference checks passed')
