"""Execute the browser exercises, export print PDF, and record validation evidence."""
from pathlib import Path
from datetime import datetime, timezone
import json, re
import fitz
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parent
V=ROOT/'verification'
V.mkdir(exist_ok=True)
data=json.loads((ROOT/'cours-source.json').read_text(encoding='utf-8'))
report={'executed_utc':datetime.now(timezone.utc).isoformat(),'checks':[],'errors':[],
        'limits':['Vérification par logiciel et personas simulés, sans essai auprès d’enfants réels.',
                  'Aucune performance matérielle IA n’est mesurée dans ce cours.']}
def check(name,condition):
    assert condition,name
    report['checks'].append({'name':name,'passed':True})
with sync_playwright() as p:
    browser=p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True)
    page=browser.new_page(viewport={'width':1440,'height':1000})
    page.on('pageerror',lambda e:report['errors'].append(str(e)))
    page.goto((ROOT/'index.html').as_uri())
    page.wait_for_function('window.Course&&Course.ready')
    check('55 original lessons loaded',page.locator('article.lesson').count()==55)
    check('one initial lesson visible',page.locator('article.lesson:visible').count()==1)
    check('previous button disabled initially',page.locator('#prev').is_disabled())
    page.keyboard.press('ArrowRight')
    check('keyboard navigation advances one step',page.evaluate('Course.position')==1)
    page.locator('#outline').select_option('2')
    check('direct navigation selects the requested lesson',page.evaluate('Course.position')==2)
    page.wait_for_timeout(400);page.screenshot(path=str(V/'01-besoin.png'),full_page=True)
    # Numeric exercises must compute, not display a prerecorded answer.
    page.evaluate('Course.readAll()')
    check('reading mode reveals all lessons',page.locator('article.lesson:visible').count()==55)
    check('paper neuron initial score is -0.3', '-0,3' in page.locator('#neuron-out').inner_text())
    page.locator('#x1').evaluate('(e)=>{e.value=2;e.dispatchEvent(new Event("input"))}')
    check('neuron output reacts to actual changed input','-0,1' in page.locator('#neuron-out').inner_text())
    page.locator('#gradient-step').click()
    g=page.locator('#gradient-out').inner_text()
    check('gradient update computes w=.28,b=.08,loss=.2048',all(x in g for x in ['0,28','0,08','0,2048']))
    for _ in range(4):page.locator('#gradient-step').click()
    check('repeated real gradient updates reduce loss','Corrections : 5' in page.locator('#gradient-out').inner_text())
    page.locator('#gradient-reset').click()
    check('gradient reset returns original numeric state','0,32' in page.locator('#gradient-out').inner_text())
    page.locator('#conv-next').click()
    check('moving filter computes second local dot product','Position 2 : 2 × 1 + 0 × (−1) = 2' in page.locator('#conv-out').inner_text())
    page.locator('#token-input').fill('<b>été</b>')
    check('token input is rendered as safe literal text',page.locator('#token-cells .cell').count()==10 and page.locator('#token-cells').inner_text().count('é')==2)
    page.locator('#token-input').fill('la lampe')
    page.locator('#token-input').fill('la');before=page.locator('#token-cells .cell').nth(1).inner_text();page.locator('#token-input').fill('al');after=page.locator('#token-cells .cell').nth(0).inner_text();check('same character keeps the same fixed vocabulary ID',before==after);page.locator('#token-input').fill('la lampe')
    check('space is an explicit character token','espace' in page.locator('#token-cells').inner_text())
    page.locator('#memory-bits').select_option('8')
    check('memory calculator computes 835 one-byte values','835 octets' in page.locator('#memory-out').inner_text())
    page.locator('#parameter-count').fill('3')
    page.locator('#memory-bits').select_option('2')
    check('subbyte ideal storage rounds up','1 octets' in page.locator('#memory-out').inner_text())
    page.locator('#parameter-count').fill('-1')
    check('invalid parameter count is rejected','positif' in page.locator('#memory-out').inner_text())
    page.locator('#parameter-count').fill('835');page.locator('#memory-bits').select_option('32')
    page.locator('#quant-bits').select_option('2')
    check('2-bit symmetric example uses Q=1','Q = 1' in page.locator('#quant-out').inner_text())
    check('2-bit simulated rounding error matches arithmetic','0,175' in page.locator('#quant-out').inner_text())
    page.locator('#quality-min').evaluate('(e)=>{e.value=93;e.dispatchEvent(new Event("input"))}')
    check('tradeoff example rejects infeasible choices','aucune' in page.locator('#pareto-out').inner_text())
    page.locator('#quality-min').evaluate('(e)=>{e.value=90;e.dispatchEvent(new Event("input"))}')
    quizzes=page.locator('.quiz')
    for i in range(quizzes.count()):
        q=quizzes.nth(i);right=int(q.get_attribute('data-correct'))
        q.locator('button').nth(1-right).click()
        check(f'quiz {i+1} explains incorrect choice','À revoir.' in q.locator('.feedback').inner_text())
        q.locator('button').nth(right).click()
        check(f'quiz {i+1} explains correct choice','Oui.' in q.locator('.feedback').inner_text())
    check('all diagrams have textual accessible titles',page.locator('figure svg[role=img] title').count()==55)
    check('no outside scripts or fonts needed',page.locator('script[src],link[rel=stylesheet]').count()==0)
    for width in [390,768,1440]:
        page.set_viewport_size({'width':width,'height':1000})
        check(f'no page-wide horizontal overflow at {width}px',page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'))
    page.set_viewport_size({'width':1440,'height':1000})
    # Restore a pedagogically clean PDF, with answers and deeper explanations visible.
    page.reload();page.wait_for_function('window.Course&&Course.ready');page.evaluate('Course.readAll()')
    page.locator('details').evaluate_all('(items)=>items.forEach(x=>x.open=true)')
    page.evaluate('document.fonts.ready')
    page.pdf(path=str(ROOT/'cours-ia-embarquee.pdf'),format='A4',print_background=True,prefer_css_page_size=True,
             display_header_footer=False)
    page.locator('#mode').click();page.evaluate('Course.show(17)');page.wait_for_timeout(400)
    page.screenshot(path=str(V/'02-correction-poids.png'),full_page=False)
    check('no runtime JavaScript errors',not report['errors'])
    report['browser']=browser.version
    browser.close()

pdf=fitz.open(ROOT/'cours-ia-embarquee.pdf')
metadata=pdf.metadata;metadata.update(author='Roland Cédric TAYO',subject='Cours progressif grand public sur l’intelligence artificielle embarquée',keywords='IA, embarqué, pédagogie, réseaux de neurones, mémoire, déploiement');pdf.set_metadata(metadata);pdf.saveIncr()
texts=[page.get_text() for page in pdf]
full='\n'.join(texts)
check('PDF contains author, sources and glossary',all(s in full for s in ['Roland Cédric TAYO','Le petit dictionnaire','Pour vérifier et continuer']))
missing=[l['title'] for l in data['lessons'] if ' '.join(l['title'].split()) not in ' '.join(full.split())]
check('every lesson title present in PDF',not missing)
check('no blank or footer-only PDF pages',all(len(t.strip())>350 for t in texts))
report['pdf_pages']=len(pdf)
report['pdf_page_text_lengths']=[len(t) for t in texts]
report['pdf_short_pages']=[i+1 for i,t in enumerate(texts) if len(t.strip())<350]
# Reject text that spills outside the A4 printable media area.
overflow=[]
for i,p in enumerate(pdf):
    for block in p.get_text('blocks'):
        if block[0]<-1 or block[1]<-1 or block[2]>p.rect.width+1 or block[3]>p.rect.height+1:
            overflow.append({'page':i+1,'bbox':list(block[:4])})
check('no text outside PDF pages',not overflow)
report['pdf_overflow']=overflow
for page_idx in [0,12,16,len(pdf)-1]:
    pdf[page_idx].get_pixmap(matrix=fitz.Matrix(1.1,1.1)).save(V/f'pdf-page-{page_idx+1}.png')
(V/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'checks_passed':len(report['checks']),'pdf_pages':len(pdf),'errors':report['errors'],'short_pages':report['pdf_short_pages']},ensure_ascii=False))
