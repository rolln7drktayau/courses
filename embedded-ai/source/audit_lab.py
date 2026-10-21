"""Verify the explicit student-material whitelist and nested archive consistency."""
from pathlib import Path
import hashlib
import io
import json
import zipfile
import fitz

ROOT=Path(__file__).resolve().parents[1]
LAB=ROOT/'lab'
TEMPLATE={'README.md','main.tex','example.tex','references.bib','plot_example.py','draw_architecture.py',
          'requirements-example.txt','figures/architecture.pdf','figures/illustrative_signal.pdf','data/illustrative_trace.csv'}
KIT={'README.md','COMMENCER.md','getting-started.html','assignment.pdf','report-guidelines.pdf','article-example.pdf','article-template.zip'}
EXPECTED={'index.html',*KIT,'student-materials.zip',*('article-template/'+name for name in TEMPLATE)}


def digest(data):return hashlib.sha256(data).hexdigest()


def main():
    actual={p.relative_to(LAB).as_posix() for p in LAB.rglob('*') if p.is_file()}
    assert actual==EXPECTED,{'extra':sorted(actual-EXPECTED),'missing':sorted(EXPECTED-actual)}
    with zipfile.ZipFile(LAB/'article-template.zip') as z:
        assert z.testzip() is None
        assert set(z.namelist())==TEMPLATE
        for name in TEMPLATE:assert z.read(name)==(LAB/'article-template'/name).read_bytes()
    with zipfile.ZipFile(LAB/'student-materials.zip') as z:
        assert z.testzip() is None
        assert set(z.namelist())==KIT
        for name in KIT:assert z.read(name)==(LAB/name).read_bytes()
        with zipfile.ZipFile(io.BytesIO(z.read('article-template.zip'))) as nested:
            assert nested.testzip() is None and set(nested.namelist())==TEMPLATE
    documents={}
    for name,pages in [('assignment.pdf',13),('report-guidelines.pdf',3),('article-example.pdf',5)]:
        with fitz.open(LAB/name) as doc:
            assert len(doc)==pages and doc.metadata['author']=='Roland Cédric TAYO'
            text=' '.join(' '.join(p.get_text().split()) for p in doc)
            assert 'V0' not in text
            if name=='article-example.pdf':assert 'no network training results' in text
            documents[name]={'pages':pages,'author':doc.metadata['author']}
    python_files={p.name for p in LAB.rglob('*.py')}
    assert python_files=={'plot_example.py','draw_architecture.py'}
    report={'student_only':True,'public_file_count':len(actual),'documents':documents,
            'template_files':sorted(TEMPLATE),'student_archive_files':sorted(KIT),
            'checks':'Explicit file whitelist; nested ZIP integrity; PDF identity; figure-only Python sources.',
            'files':{name:{'bytes':(LAB/name).stat().st_size,'sha256':digest((LAB/name).read_bytes())} for name in sorted(actual)}}
    output=ROOT/'verification'/'student-materials.json'
    output.write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps({'student_only':True,'files':len(actual),'pdf_pages':{k:v['pages'] for k,v in documents.items()},'nested_archives':'passed'}))


if __name__=='__main__':main()
