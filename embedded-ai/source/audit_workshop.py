"""Exercise student drafts, safe file assembly, print assets and offline packaging."""
from pathlib import Path
from functools import partial
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from threading import Thread
import json
import tempfile
import zipfile
import subprocess
import fitz
from PIL import Image, ImageDraw
from playwright.sync_api import sync_playwright
from workshop_content import HALF_DAY, FULL_DAY, MISSIONS, SCHEMA
from build_workshop import ROOT, OUT, CHROME


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self,*args):pass


def main():
    checks={'half_day_minutes':HALF_DAY[-1][1],'full_day_minutes':FULL_DAY[-1][1],'teams':len(MISSIONS)}
    server=ThreadingHTTPServer(('127.0.0.1',0),partial(QuietHandler,directory=str(ROOT.parent)))
    Thread(target=server.serve_forever,daemon=True).start()
    try:
        with tempfile.TemporaryDirectory(prefix='inem-workshop-check-') as temp:
            tmp=Path(temp)
            with sync_playwright() as p:
                browser=p.chromium.launch(executable_path=str(CHROME),headless=True)
                context=browser.new_context(accept_downloads=True,reduced_motion='reduce')
                page=context.new_page()
                errors=[];page.on('pageerror',lambda err:errors.append(str(err)))
                base=f'http://127.0.0.1:{server.server_port}/embedded-ai/workshop/'
                page.goto(base)
                assert page.locator('.mission-choice').count()==7
                for width in [1440,1024,768,600,390,360]:
                    page.set_viewport_size({'width':width,'height':900})
                    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'),width
                page.set_viewport_size({'width':1440,'height':1000})
                page.screenshot(path=str(ROOT/'verification/workshop-home.png'),full_page=False)
                page.locator('[name="common_need"]').fill('Un service hors ligne ; une hypothèse à vérifier.')
                page.reload()
                assert page.locator('[name="common_need"]').input_value().startswith('Un service')
                for mission in range(1,8):
                    page.locator(f'[data-mission="{mission}"]').click()
                    assert page.locator('#mission-title').inner_text().startswith(str(mission)+' ·')
                    assert page.locator('#mission-tasks li').count()==5
                    assert page.locator('#mission-pdf').get_attribute('href')==f'group-{mission:02d}.pdf'
                page.locator('#group').select_option('2')
                assert page.locator('#mission').input_value()=='2'
                page.locator('[name="common_need"]').fill('Groupe deux : autre brouillon.')
                page.locator('#group').select_option('1')
                assert page.locator('[name="common_need"]').input_value().startswith('Un service')
                page.locator('#mission').select_option('1')
                page.locator('[name="definition"]').fill('Notre définition de travail.')
                page.locator('[name="proof"]').fill('Un calcul, pas une mesure sur carte.')
                with page.expect_download() as event:page.locator('#export-json').click()
                record=json.loads(Path(event.value.path()).read_text(encoding='utf-8'))
                assert record['schema']==SCHEMA and record['group']==1 and record['mission']==1
                assert 'exit' not in record['fields']
                with page.expect_download() as event:page.locator('#export-md').click()
                assert 'Notre définition de travail.' in Path(event.value.path()).read_text(encoding='utf-8')
                files=[]
                for group in range(1,8):
                    data=json.loads(json.dumps(record));data['group']=group;data['mission']=group
                    data['fields']['definition']=f'Définition du sujet {group}.'
                    if group==7:data['fields']['definition']='<img src=x onerror="window.workshopInjected=true">'
                    path=tmp/f'group-{group:02d}.json';path.write_text(json.dumps(data),encoding='utf-8');files.append(str(path))
                page.locator('#import-class').set_input_files(files)
                page.wait_for_function("document.getElementById('collective-status').textContent.startsWith('7 / 7')")
                assert page.locator('#collective-chapters .chapter-card').count()==7
                assert page.locator('#collective-chapters img').count()==0
                assert page.evaluate('window.workshopInjected === undefined')
                with page.expect_download() as event:page.locator('#export-course-html').click()
                html=Path(event.value.path()).read_text(encoding='utf-8')
                assert '&lt;img' in html and '<img src=x' not in html
                assert 'Définition du sujet 1.' in html
                with page.expect_download() as event:page.locator('#export-course-md').click()
                assert '## 7.' in Path(event.value.path()).read_text(encoding='utf-8')
                invalid=tmp/'invalid.json';invalid.write_text(json.dumps({'schema':'wrong'}),encoding='utf-8')
                page.locator('#import-own').set_input_files(str(invalid))
                page.wait_for_function("document.getElementById('file-status').textContent.includes('non reconnu')")
                assert page.locator('[name="definition"]').input_value()=='Notre définition de travail.'
                mismatch=json.loads(json.dumps(record));mismatch['fields']['session']='AUTRE-SEANCE'
                invalid.write_text(json.dumps(mismatch),encoding='utf-8')
                page.locator('#import-class').set_input_files(str(invalid))
                page.wait_for_function("document.getElementById('file-status').textContent.includes('Séance différente')")
                assert page.locator('#collective-status').inner_text().startswith('7 / 7')
                page.locator('#import-own').set_input_files(files[1])
                page.wait_for_function("document.getElementById('group').value === '2'")
                assert page.locator('[name="definition"]').input_value()=='Définition du sujet 2.'
                # Actual local links must resolve, including every PDF, source asset and archive.
                for path in ['protocol.pdf','worksheets.pdf','individual-check.pdf','data/toy-series.csv','repository-template.zip','workshop-materials.zip']+[f'group-{i:02d}.pdf' for i in range(1,8)]:
                    response=context.request.get(base+path);assert response.ok,(path,response.status)
                assert not errors,errors
                browser.close()
                # Verify the downloaded bundle works without a web server or network fetch for app data.
                with zipfile.ZipFile(OUT/'workshop-materials.zip') as archive:
                    assert archive.testzip() is None
                    assert not any('guide-animation' in name or 'Resolution_Enseignant' in name for name in archive.namelist())
                    archive.extractall(tmp/'offline')
                browser=p.chromium.launch(executable_path=str(CHROME),headless=True)
                offline=browser.new_page()
                requests=[];offline.on('request',lambda request:requests.append(request.url) if request.url.startswith('http') else None)
                offline.goto((tmp/'offline/embedded-ai/workshop/index.html').as_uri())
                assert offline.locator('#mission-title').inner_text().startswith('1 ·')
                offline.locator('[data-mission="6"]').click()
                assert offline.locator('#mission-title').inner_text().startswith('6 ·')
                assert not requests,requests
                browser.close()
            # Check repository support without executing any student code or model solution.
            repo=tmp/'template'
            with zipfile.ZipFile(OUT/'repository-template.zip') as archive:archive.extractall(repo)
            subprocess.run(['python',str(repo/'tools/check_evidence.py')],cwd=repo,check=True,capture_output=True)
            (repo/'submissions/group-01.json').write_text(json.dumps(record),encoding='utf-8')
            subprocess.run(['python',str(repo/'tools/check_evidence.py')],cwd=repo,check=True,capture_output=True)
    finally:server.shutdown()
    checks.update(local_save='passed',all_missions='passed',json_and_markdown='passed',seven_chapter_assembly='passed',safe_html_export='passed',invalid_import='rejected',session_mismatch='rejected',offline_bundle='passed',links='passed',repository_format_check='passed')
    pdf_pages={}
    for name,count in [('protocol.pdf',5),('worksheets.pdf',10),('individual-check.pdf',1)]+[(f'group-{i:02d}.pdf',1) for i in range(1,8)]:
        with fitz.open(OUT/name) as doc:
            assert len(doc)==count,(name,len(doc),count)
            assert doc.metadata['author']=='Roland Cédric TAYO',(name,doc.metadata)
            assert all(abs(page.rect.width/page.rect.height-210/297)<.002 for page in doc)
            assert all(len(page.get_text())>150 for page in doc)
            for page in doc:
                assert all(not link.get('uri','').startswith('file:') for link in page.get_links()),name
            pdf_pages[name]=len(doc)
    checks['pdf_pages']=pdf_pages
    with fitz.open(OUT/'worksheets.pdf') as doc:
        selected=[0,1,2,5,8,9];sheet=Image.new('RGB',(1000,3*730),'#dce6ea')
        for position,index in enumerate(selected):
            pix=doc[index].get_pixmap(matrix=fitz.Matrix(.8,.8));img=Image.frombytes('RGB',[pix.width,pix.height],pix.samples)
            x=(position%2)*500;y=(position//2)*730;sheet.paste(img,(x,y));ImageDraw.Draw(sheet).text((x+12,y+690),f'Fiche {index+1}',fill='#18394b')
        sheet.save(ROOT/'verification/workshop-sheets.png')
    (ROOT/'verification/workshop-checks.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(checks))


if __name__=='__main__':main()
