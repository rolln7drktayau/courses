"""Package only the course, keeping every instructor-solution file outside the archive."""
from pathlib import Path
import json
import zipfile
import fitz

ROOT=Path(__file__).resolve().parents[1]
checks=json.loads((ROOT/'verification'/'checks.json').read_text(encoding='utf-8'))
assert checks['minutes']==180 and checks['oral_slides']==44
assert not any(checks['viewports'].values()),checks['viewports']
assert not checks['console_errors'] and not checks['external_requests']
assert not checks['quiz_feedback_overflow']
assert checks['pdf_pages']==54
for name,count in [('course.pdf',54),('course-plan.pdf',2)]:
    with fitz.open(ROOT/name) as doc:
        assert len(doc)==count
        assert doc.metadata['author']=='Roland Cédric TAYO'
archive=ROOT.parent/'embedded-ai.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
    for p in sorted(ROOT.rglob('*')):
        if not p.is_file() or '__pycache__' in p.parts:continue
        if p.suffix in {'.pyc','.png','.tmp'}:continue
        z.write(p,p.relative_to(ROOT).as_posix())
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None
    assert 'index.html' in z.namelist()
    assert not any('Resolution_Enseignant' in p for p in z.namelist())
print('Course archive:',archive)
print('Bytes:',archive.stat().st_size)
