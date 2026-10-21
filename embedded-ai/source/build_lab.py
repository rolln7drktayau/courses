"""Rebuild student statement PDFs and package their current, explicit file list."""
from pathlib import Path
from html import escape
import json,zipfile,re
import fitz
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
CHROME=Path(r'C:\Program Files\Google\Chrome\Application\chrome.exe')


def main():
    results={}
    # The start sheet uses only headings, paragraphs and flat lists; no runtime dependency.
    parts=[];paragraph=[];list_kind=None
    def inline(text):
        text=escape(text)
        text=re.sub(r'\*\*(.+?)\*\*',r'<strong>\1</strong>',text)
        return re.sub(r'`(.+?)`',r'<code>\1</code>',text)
    def flush():
        nonlocal list_kind
        if paragraph:parts.append('<p>'+inline(' '.join(paragraph))+'</p>');paragraph.clear()
        if list_kind:parts.append('</'+list_kind+'>');list_kind=None
    for line in (ROOT/'lab/COMMENCER.md').read_text(encoding='utf-8').splitlines():
        if not line.strip():flush();continue
        if line.startswith('#'):
            flush();level=len(line)-len(line.lstrip('#'));parts.append(f'<h{level}>'+inline(line[level:].strip())+f'</h{level}>');continue
        match=re.match(r'^(?:- |\d+\. )(.*)',line)
        if match:
            kind='ul' if line.startswith('- ') else 'ol'
            if list_kind!=kind:flush();parts.append('<'+kind+'>');list_kind=kind
            parts.append('<li>'+inline(match.group(1))+'</li>');continue
        flush();paragraph.append(line)
    flush()
    page_html='''<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Commencer le TD · IA embarquée</title><style>body{font:18px/1.65 'Segoe UI',Arial,sans-serif;color:#25384a;background:#f7f9f9;margin:0}main{max-width:950px;margin:auto;background:white;padding:40px 48px}h1{font-size:40px;line-height:1.15}h2{margin-top:38px;color:#177d79;font-size:27px}li{margin:12px 0}a{color:#177d79}code{font-size:.9em;background:#edf4f3;padding:2px 4px}nav{padding-bottom:25px;border-bottom:1px solid #dce4e4}strong{font-weight:650}@media(max-width:650px){main{padding:25px}h1{font-size:32px}}</style></head><body><main><nav><a href="https://rolln7drktayau.github.io/courses/embedded-ai/">Cours</a> · <a href="index.html">Documents du TD</a> · <a href="assignment.pdf">Énoncé PDF</a></nav>'''+''.join(parts)+'</main></body></html>'
    (ROOT/'lab/getting-started.html').write_text(page_html,encoding='utf-8')
    with sync_playwright() as p:
        browser=p.chromium.launch(executable_path=str(CHROME) if CHROME.exists() else None,headless=True)
        page=browser.new_page()
        for name,pages in [('assignment',13),('report-guidelines',3)]:
            page.goto((ROOT/'source/lab'/f'{name}.html').as_uri())
            page.emulate_media(media='print')
            overflow=page.locator('.page').evaluate_all('''ss=>ss.flatMap((s,i)=>{
                const footer=s.querySelector('footer').getBoundingClientRect();
                const bottom=Math.max(...[...s.querySelector('main').children].map(e=>e.getBoundingClientRect().bottom));
                return bottom>footer.top-3?[{page:i+1,pixels:bottom-footer.top}]:[];
            })''')
            assert not overflow,(name,overflow)
            target=ROOT/'lab'/f'{name}.pdf'
            page.pdf(path=str(target),prefer_css_page_size=True,print_background=True)
            doc=fitz.open(target);assert len(doc)==pages,(name,len(doc))
            doc.set_metadata({'title':'TD IA embarquée' if name=='assignment' else 'Consignes du rapport scientifique',
                              'author':'Roland Cédric TAYO','subject':'INEM · 2026–2027'})
            if name=='assignment':
                doc.set_toc([[1,title,index] for title,index in [
                    ('1. Problème et objectifs',1),('Rappels A — Données',2),('2. Données et références',3),
                    ('3. Réseau et apprentissage',4),('Rappels B — Réseau',5),('4. Déploiement',6),
                    ('5. Recherche et mesures',7),('6. Règles et évaluation',8),('7. GitHub',9),
                    ('Jalons',10),('8. Atelier A — Fonctions',11),('9. Atelier B — Apprentissage et tests',12),('10. Outils et sources',13)]])
            temporary=target.with_suffix('.tmp.pdf');doc.save(temporary,garbage=4,deflate=True);doc.close();temporary.replace(target)
            results[name]={'pages':pages,'overflows':overflow}
        browser.close()
    from audit_lab import TEMPLATE
    with zipfile.ZipFile(ROOT/'lab/article-template.zip','w',zipfile.ZIP_DEFLATED) as z:
        for name in sorted(TEMPLATE):z.write(ROOT/'lab/article-template'/name,name)
    files=['README.md','COMMENCER.md','getting-started.html','assignment.pdf','report-guidelines.pdf','article-example.pdf','article-template.zip']
    with zipfile.ZipFile(ROOT/'lab/student-materials.zip','w',zipfile.ZIP_DEFLATED) as z:
        for name in files:z.write(ROOT/'lab'/name,name)
    print(json.dumps(results))


if __name__=='__main__':main()
