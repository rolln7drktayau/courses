"""Check simulator prominence, upright geometry and scene-only enlargement."""
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
    browser=p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True,args=['--enable-unsafe-swiftshader'])
    page=browser.new_page(viewport={'width':1536,'height':900});page.on('pageerror',lambda e:report['errors'].append(str(e)))
    page.goto(BASE);page.wait_for_function('!!window.Display&&!!window.Conversation');page.wait_for_timeout(150)
    for width,height in [(1536,900),(1280,800),(1920,1080)]:
        page.set_viewport_size({'width':width,'height':height});page.evaluate('scrollTo(0,0)');page.wait_for_timeout(150);rect=page.locator('#scene').bounding_box()
        check('entire scene visible at entry '+str(width),rect['y']+rect['height']<=height+2 and rect['height']>=250)
        check('simulation is the dominant column '+str(width),rect['width']>width*.6)
    check('conversation no longer precedes simulation',page.locator('#conversation').bounding_box()['y']>page.locator('#scene').bounding_box()['y'])
    check('cards are standing in a vertical plane',page.evaluate('Math.abs(Lab.scene.content.rotation.x-Math.PI/2)<1e-9'))
    check('camera looks straight at fronts',page.evaluate('Math.abs(Lab.scene.camera.position.y-Lab.scene.controls.target.y)<1e-9&&Lab.scene.camera.position.z>0'))
    check('link geometry remains finite',page.evaluate('Lab.scene.lessonLinks.every(l=>l.arrow.position.toArray().every(Number.isFinite))'))
    page.screenshot(path=str(ROOT/'validation/simulation-entry.png'))
    # A click must not be mistaken for a camera rotation.
    rect=page.locator('#canvas').bounding_box();page.mouse.click(rect['x']+rect['width']/2,rect['y']+rect['height']/2)
    check('selection click does not lock camera',page.evaluate('!Lab.scene.keepLessonView'))
    page.locator('#workspace-fullscreen').click();page.wait_for_timeout(150)
    check('header enlarges only simulation',page.evaluate('Display.spotlight&&!document.fullscreenElement'))
    check('spotlight has its own backdrop',page.locator('#simulation-scrim').is_visible())
    rect=page.locator('.viewport-panel').bounding_box();check('spotlight occupies viewport',rect['width']>1800 and rect['height']>1000)
    page.locator('#sim-next').click();check('steps work in spotlight',page.evaluate('Journey.index')==1)
    page.locator('#sim-full').click();page.wait_for_function("document.fullscreenElement===document.querySelector('.viewport-panel')")
    check('spotlight transitions to native scene fullscreen',page.evaluate('!Display.spotlight'))
    before=page.evaluate('Lab.scene.camera.position.toArray()');rect=page.locator('#canvas').bounding_box();x,y=rect['x']+rect['width']/2,rect['y']+rect['height']/2
    page.mouse.move(x,y);page.mouse.down();page.mouse.move(x+60,y+20,steps=8);page.mouse.up();page.wait_for_timeout(200)
    check('rotation works on upright blocks',page.evaluate('Lab.scene.camera.position.toArray()')!=before)
    check('actual manipulation locks viewing angle',page.evaluate('Lab.scene.keepLessonView'))
    page.locator('#sim-home').click();check('recenter restores a frontal view',page.evaluate('!Lab.scene.keepLessonView&&Math.abs(Lab.scene.camera.position.y-Lab.scene.controls.target.y)<1e-9'))
    page.screenshot(path=str(ROOT/'validation/simulation-upright-fullscreen.png'))
    page.locator('#sim-exit').click();page.wait_for_function('!document.fullscreenElement');page.locator('#sim-spotlight').click();page.keyboard.press('Escape');check('Escape leaves spotlight',page.evaluate('!Display.spotlight'))
    for width in [390,768,1280]:page.set_viewport_size({'width':width,'height':1000});check('no horizontal overflow '+str(width),page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'))
    check('no runtime errors',not report['errors']);report['browser']=browser.version;browser.close()
(ROOT/'validation/presentation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(str(len(report['checks']))+' presentation checks passed')
