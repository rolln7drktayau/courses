"""Execute the public UI in Chrome. No fabricated benchmark or Pi result."""
import json,sys,time
from datetime import datetime,timezone
from pathlib import Path
from playwright.sync_api import sync_playwright
sys.stdout.reconfigure(encoding='utf-8')
ROOT=Path(__file__).resolve().parents[1]
BASE=sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:8766/neural-lab/?advanced'
report={'executed_utc':datetime.now(timezone.utc).isoformat(),'load':'not controlled','rendering':'Chrome headless with --enable-unsafe-swiftshader; not a GPU performance test','url':BASE,'checks':[],'errors':[],'network_requests':[]}
def checked(name,condition):
    assert condition,name
    report['checks'].append({'name':name,'passed':True})
with sync_playwright() as p:
    browser=p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True,args=['--enable-unsafe-swiftshader'])
    page=browser.new_page(viewport={'width':1536,'height':1000},accept_downloads=True)
    page.on('pageerror',lambda e:report['errors'].append(str(e)))
    page.on('request',lambda r:report['network_requests'].append(r.url))
    page.goto(BASE);page.wait_for_function('!!window.Lab')
    checked('WebGL initialized',page.evaluate('!!Lab.renderer'))
    checked('all three model choices',page.locator('#model option').count()==3)
    page.locator('#guide').click();checked('guided start',page.locator('#dialog').is_visible());page.locator('#tour-start').click()
    page.locator('#slow-train').click();page.wait_for_timeout(1600);page.locator('#slow-train').click();count=page.evaluate('Lab.trace.tape.v.length');page.wait_for_timeout(1600);checked('slow real computation can pause',page.evaluate('Lab.trace.tape.v.length')==count);page.locator('#initialize').click()
    original=page.evaluate('Lab.model.weights.slice()')
    for selector in ['#forward','#loss','#backward']:page.locator(selector).click()
    checked('no weight change before update',page.evaluate('Lab.model.weights')==original)
    page.locator('#update').click();checked('manual update changes weights',page.evaluate('Lab.model.weights')!=original)
    checked('updated trace has no fake zero gradient',page.evaluate('Lab.trace.gradientComputed===false'));checked('manual correction values visible','La dernière correction' in page.locator('#inspector').inner_text());checked('manual update trace matches new weights',page.evaluate('Lab.trace.target !== null && Lab.trace.tape.v[0]===Lab.model.weights[0]'))
    page.locator('#initialize').click()
    page.locator('#train').click();page.wait_for_function('!Lab.busy',timeout=90000)
    checked('actual 300 updates',page.evaluate('Lab.model.updates')==300)
    history=page.evaluate('Lab.model.history');report['training_history']=history
    checked('training/validation curves recorded',len(history)>=13)
    page.locator('[data-tab=infer]').click();page.locator('#prompt').fill('al');page.locator('#predict').click();fixed=page.evaluate('Lab.model.weights.slice()');page.locator('#generate-one').click();page.locator('#generate-one').click()
    checked('inference keeps weights fixed',page.evaluate('Lab.model.weights')==fixed)
    checked('cache actually reused','réutilisés' in page.locator('#cache-status').inner_text())
    page.locator('#inference-bits').select_option('4');page.locator('#predict').click();checked('quantized inference visible','4 bits' in page.locator('#cache-status').inner_text())
    page.locator('#prompt').fill('🙂');page.locator('#predict').click();checked('unknown token explicitly shown','absent' in page.locator('#cache-status').inner_text())
    page.evaluate("Lab.openMatrix('Q')");checked('matrix drill down',page.evaluate("Lab.level==='matrix'"))
    page.locator('#matrix-grid button').first.click();checked('weight precise value',page.locator('#weight-detail').inner_text().find('∂L/∂θ')>=0)
    page.locator('#open-weight-node').click();checked('scalar leaf visible','feuille' in page.locator('#inspector').inner_text().lower())
    page.locator('#home').click();page.locator('[data-block=logits]').click();page.locator('#values button').first.click();checked('operation drill down',page.evaluate("Lab.level==='operation'"));page.locator('#replay').click();checked('algorithm replay',page.locator('#op-next').is_visible());page.locator('#op-next').click();page.locator('#op-inside').click()
    page.screenshot(path=str(ROOT/'validation/exploration.png'),full_page=False)
    page.locator('#home').click();page.locator('#toggle-2d').click();checked('2D fallback visible',page.locator('#fallback').is_visible());page.locator('#fallback [data-flat=attention]').click();checked('2D accessible inspector','Choisir où regarder' in page.locator('#inspector').inner_text());page.locator('#toggle-2d').click()
    page.locator('[data-tab=research]').click();page.locator('#hypothesis').fill('Je prévois que 2 bits augmentent la perte de validation de plus de 0,1 nat par rapport à 32 bits.')
    page.locator('#compare').click();page.wait_for_function('!Lab.busy',timeout=90000);checked('four precision measurements',page.evaluate('Lab.comparison.length')==4)
    report['comparison']=page.evaluate('Lab.comparison');report['timing']=page.evaluate('Lab.timing')
    checked('timing repetitions and calibration',len(report['timing'])==10 and all(r['calibration_ms']>=100 or r['k']==65536 for r in report['timing']))
    saved=page.evaluate('({hypothesis:Lab.comparisonProtocol.hypothesis,mode:Lab.comparisonProtocol.scale_mode,bits:Lab.comparisonProtocol.timing_bits})');page.locator('#hypothesis').fill('Changed AFTER measurement');page.locator('#scale-mode').select_option('global');page.locator('#bits').select_option('2')
    downloads=[];page.on('download',lambda d:downloads.append(d));page.locator('#export-results').click();page.wait_for_timeout(500)
    checked('all experiment files exported',len(downloads)==5)
    protocol=json.loads(Path(next(d for d in downloads if d.suggested_filename=='protocol.json').path()).read_text(encoding='utf-8'))
    checked('immutable experiment provenance',protocol['hypothesis']==saved['hypothesis'] and protocol['scale_mode']==saved['mode'] and protocol['timing_bits']==saved['bits'])
    page.locator('#tab-research details summary').click();page.locator('#wrong-sign').check();page.locator('#check-gradient').click();checked('update sign bug detected','ALERTE' in page.locator('#gradient-result').inner_text());report['gradient_check']=page.locator('#gradient-result').inner_text()
    page.locator('#unmask').check();page.locator('#check-mask').click();checked('mask bug detected','masque manque' in page.locator('#mask-result').inner_text());checked('mask explanation follows actual state','masque retiré' in page.locator('#inspector').inner_text().lower())
    with page.expect_download() as d:page.locator('#export-model').click()
    destination=ROOT/'validation/.roundtrip.json';d.value.save_as(str(destination));page.locator('#import-model').set_input_files(str(destination));page.wait_for_function("document.querySelector('#status').textContent.includes('importés')")
    checked('weight export import SHA256',page.evaluate('Lab.model.weights')==fixed);destination.unlink()
    # Run the two other public model paths, not just engine-level tests.
    for model in ['bigram','mlp']:
        page.locator('#model').select_option(model);page.locator('#initialize').click();page.locator('[data-tab=train]').click();page.locator('#steps').select_option('100');page.locator('#train').click();page.wait_for_function('!Lab.busy',timeout=90000);checked(model+' browser training',page.evaluate('Lab.model.updates')==100)
    for width,height in [(390,844),(768,1024),(1280,800)]:
        page.set_viewport_size({'width':width,'height':height});page.wait_for_timeout(100);checked('no horizontal overflow '+str(width),page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'))
    page.set_viewport_size({'width':1536,'height':1000});page.locator('#model').select_option('transformer');page.locator('#initialize').click();page.evaluate("Lab.openMatrix('Q')");page.wait_for_timeout(500);page.locator('#scene').screenshot(path=str(ROOT/'validation/matrix.png'))
    page.locator('#load-example').click();page.wait_for_function('!Lab.busy');checked('verified trained example loads',page.evaluate('Lab.model.updates')==2000)
    page.locator('#home').click();page.wait_for_timeout(700)
    point=page.evaluate('''()=>{const s=Lab.scene,p=s.items[0].position.clone().project(s.camera),r=s.canvas.getBoundingClientRect();return {x:r.x+(p.x+1)*r.width/2,y:r.y+(1-p.y)*r.height/2};}''')
    page.mouse.move(point['x'],point['y']);checked('real 3D hover tooltip',page.locator('#tooltip').is_visible())
    page.mouse.click(point['x'],point['y']);checked('3D picking selects real block', 'texte devient' in page.locator('#inspector').inner_text().lower())
    page.locator('#scene').screenshot(path=str(ROOT/'validation/network.png'))
    # Generation can be paused without changing weights or leaving a runaway timer.
    page.locator('[data-tab=infer]').click();page.locator('#prompt').fill('al');page.locator('#generate').click();page.wait_for_timeout(600);page.locator('#generate').click();checked('generation pause',page.locator('#generate').inner_text().startswith('▶'))
    fallback=browser.new_page();fallback.add_init_script("const original=HTMLCanvasElement.prototype.getContext;HTMLCanvasElement.prototype.getContext=function(type,...rest){if(type.startsWith('webgl'))return null;return original.call(this,type,...rest);};");fallback.goto(BASE);fallback.wait_for_function('!!window.Lab');checked('automatic 2D fallback without WebGL',fallback.locator('#fallback').is_visible() and fallback.evaluate('!Lab.renderer'));fallback.locator('[data-flat=logits]').click();checked('fallback provides actual values',fallback.locator('#values button').count()>0);fallback.close()
    checked('no JavaScript errors',not report['errors'])
    from urllib.parse import urlparse
    checked('no external runtime requests',all(urlparse(u).netloc==urlparse(BASE).netloc for u in report['network_requests']))
    report['browser']=browser.version
    browser.close()
(ROOT/'validation/browser.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(str(len(report['checks']))+' browser checks passed')
