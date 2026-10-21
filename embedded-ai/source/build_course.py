"""Build the offline HTML deck, 16:9 PDF and compact A4 course plan."""
from pathlib import Path
from html import escape
import json
import shutil
import zipfile
import fitz
from playwright.sync_api import sync_playwright
from content import SLIDES,REFERENCES,CORE_COUNT,ADVANCED
from diagrams import draw

HERE=Path(__file__).resolve().parent
OUT=HERE.parent
REF={r['id']:r for r in REFERENCES}
CHROME=Path(r'C:\Program Files\Google\Chrome\Application\chrome.exe')


def footer(index,refs=(),detail=True):
    citations=''.join(f'<a class="ref" href="{escape(REF[k]["url"],quote=True)}" data-ref="{k}" title="{escape(REF[k]["title"],quote=True)}">{k} · {REF[k]["year"]}</a>' for k in refs)
    detail_button='<button class="detail-button" data-action="details">Approfondir ↗</button>' if detail else ''
    count=f'{index+1:02d} / {CORE_COUNT}' if index<CORE_COUNT else f'A{index-CORE_COUNT+1:02d}'
    return f'<footer class="slide-footer"><span class="author">Roland Cédric TAYO · INEM</span><span class="citations">{citations}{detail_button}</span><span class="slide-num">{count}</span></footer>'


def header(chapter,time):
    return f'<header class="topline"><span class="brand">Embedded AI <span style="font-weight:400;letter-spacing:0">/ INEM</span></span><span class="chapter">{escape(chapter)}</span><span class="plan-time">{escape(time)}</span></header>'


def build_core(item,index,start):
    title=escape(item['title']).replace('\n','<br>')
    lead=escape(item['lead']);body=''.join('<li>'+p+'</li>' for p in item['points'])
    time=f'{start:02d}–{start+item["minutes"]:02d} min · {item["minutes"]} min'
    kind=item.get('kind','');attrs=f'data-index="{index}" data-minutes="{item["minutes"]}" aria-label="{escape(item["title"].replace(chr(10)," "),quote=True)}"'
    top=header(item['chapter'],time if index<CORE_COUNT else 'Lecture libre')
    if kind=='hero':
        middle=f'<div class="hero-grid"><div><div class="eyebrow">Modèles · calcul · mémoire · preuves</div><h1>{title}</h1><p class="lead">{lead}</p><div class="hero-author">Roland Cédric TAYO</div><div class="hero-entry"><a href="workshop/" target="_blank" rel="noopener noreferrer">Construire le cours ensemble →</a></div></div><div class="hero-art">{draw("hero")}</div></div>'
    else:
        heading=f'<div class="heading"><h1>{title}</h1><p class="lead">{lead}</p></div>'
        if kind=='quiz':
            quiz=item['quiz']
            options=''.join(f'<button class="quiz-choice" data-answer="{i}" aria-pressed="false"><span class="letter">{"ABC"[i]}</span><span>{escape(option)}</span></button>' for i,option in enumerate(quiz['options']))
            task=escape(item.get('task') or 'Discutez, choisissez et justifiez.')
            context='<span class="question-mark">?</span><h2>Votre raisonnement<br>avant la réponse.</h2>'
            if item['title'].startswith('Quiz 5'):
                context='<table class="decision-table"><caption>Valeurs fictives · périmètre commun</caption><thead><tr><th>Modèle</th><th>Qualité</th><th>Kio</th><th>ms¹</th><th>mJ</th></tr></thead><tbody><tr><th>A</th><td>97 %</td><td>120</td><td>12</td><td>2,4</td></tr><tr><th>B</th><td>96 %</td><td>96</td><td>18</td><td>2,8</td></tr><tr><th>C</th><td>95 %</td><td>72</td><td>14</td><td>1,8</td></tr></tbody></table><small>¹ p95 sur 500 essais fictifs. Énergie : acquisition + calcul + action, hors veille.</small>'
            middle=heading+f'<div class="content quiz-layout"><div class="quiz-prompt">{context}<p>{task}</p></div><div class="quiz-options">{options}<p class="quiz-feedback" aria-live="polite">Écrivez votre justification, puis choisissez.</p></div></div>'
        else:
            middle=heading+f'<div class="content"><ul class="points">{body}</ul><div class="visual">{draw(item["visual"])}</div></div>'
    return f'<section class="slide {kind} {"active" if index==0 else ""} {"appendix" if index>=CORE_COUNT else ""}" {attrs}>{top}{middle}{footer(index,item["refs"])}</section>'


def build_appendices():
    sections=[];data=[]
    for item in ADVANCED:
        index=CORE_COUNT+len(sections)
        sections.append(build_core(item,index,0))
        data.append(item)
    for group in range(0,len(REFERENCES),4):
        refs=REFERENCES[group:group+4];index=CORE_COUNT+len(sections)
        title=f'Sources et limites de lecture · {group//4+1}/6'
        cards=''
        for r in refs:
            cards+=f'<article class="reference-item"><span class="reference-code">{r["id"]}</span><div><h2><a href="{escape(r["url"],quote=True)}" target="_blank" rel="noopener noreferrer">{escape(r["title"])} ↗</a></h2><p class="ref-meta">{escape(r["authors"])} · {escape(r["year"])} · {escape(r["status"])}</p><p class="ref-takeaway">{escape(r["takeaway"])}</p></div></article>'
        if len(refs)==1:
            for key in ['R10','R09','R11']:
                r=REF[key]
                cards+=f'<article class="reference-item"><span class="reference-code">À lire</span><div><h2><a href="{r["url"]}">{escape(r["title"])} ↗</a></h2><p class="ref-takeaway">{escape(r["limit"])}</p></div></article>'
        sections.append(f'<section class="slide appendix" data-index="{index}" aria-label="{title}">{header("Annexes · Bibliographie","Lecture libre")}<div class="heading"><h1>{title}</h1><p class="lead">Articles originaux, prépublications et documentation officielle · lire les limites de chaque source.</p></div><div class="reference-list">{cards}</div>{footer(index,detail=False)}</section>')
        data.append(dict(title=title,chapter='Annexes · Sources',lead='Bibliographie scientifique',minutes=0,refs=[],detail='Les intitulés distinguent les actes ou revues identifiés, les prépublications et la documentation. La date de dépôt peut différer de la date de publication. Lire les résultats avec leurs configurations et limites.'))
    glossaries=[[
        ('MCU','Microcontrôleur : processeur, mémoire et périphériques réunis pour une application embarquée.'),
        ('CPU / GPU / NPU','Calcul général / calcul parallèle / accélération spécialisée de réseaux.'),
        ('Flash','Mémoire non volatile : programme et constantes, selon le placement choisi.'),
        ('SRAM / RAM','Mémoire de travail volatile. Compter les données simultanément vivantes.'),
        ('SIMD','Une instruction traite plusieurs valeurs ; les formats et alignements comptent.'),
        ('DMA','Transfert de données piloté par un contrôleur ; bande passante et synchronisation restent limitées.'),
        ('ISA','Jeu d’instructions du processeur. Un noyau doit exploiter ce qui est réellement disponible.'),
        ('Ko / Kio','Ko = 1000 octets ; Kio = 1024 octets. Mio = 1024² octets dans ce cours.'),
    ],[
        ('Paramètre / activation','Un paramètre est appris ; une activation dépend de l’entrée en cours de calcul.'),
        ('MAC','Multiplier puis accumuler. Préciser la convention avant de comparer des opérations.'),
        ('Perte / gradient','La perte mesure une erreur ; le gradient indique comment elle varie avec les paramètres.'),
        ('PTQ / QAT','Quantification après entraînement / apprentissage tenant compte de la quantification.'),
        ('Cache KV','Clés et valeurs conservées pour éviter certains recalculs pendant la génération.'),
        ('Runtime / backend','Moteur qui exécute le graphe / implémentation qui choisit les noyaux de la cible.'),
        ('Latence / débit','Temps d’une réponse / quantité de réponses par unité de temps. Ils ne se confondent pas.'),
        ('CI / manifeste','Tests et construction automatisés / fiche qui relie version, conditions et fichiers de l’expérience.'),
    ]]
    for i,glossary in enumerate(glossaries):
        index=CORE_COUNT+len(sections);title='Lexique · '+('Matériel et mémoire' if i==0 else 'Modèles et expérimentation')
        cards=''.join(f'<article class="glossary-item"><h2>{escape(a)}</h2><p>{escape(b)}</p></article>' for a,b in glossary)
        sections.append(f'<section class="slide appendix" data-index="{index}" aria-label="{title}">{header("Annexes · Définitions","Lecture libre")}<div class="heading"><h1>{title}</h1><p class="lead">Des termes à expliquer avec un exemple, pas seulement à mémoriser.</p></div><div class="glossary-grid">{cards}</div>{footer(index,detail=False)}</section>')
        data.append(dict(title=title,chapter='Annexes · Lexique',lead='Définitions',minutes=0,refs=[],detail='Revenir à la brique et au budget concernés pour vérifier la compréhension du terme.'))
    quizzes=[(i+1,s) for i,s in enumerate(SLIDES) if s['quiz']]
    for group in range(0,5,3):
        index=CORE_COUNT+len(sections);title=f'Réponses raisonnées · {group//3+1}/2';cards=''
        for q_index,(slide_index,s) in enumerate(quizzes[group:group+3],start=group+1):
            quiz=s['quiz'];letter='ABC'[quiz['correct']]
            cards+=f'<article class="answer-item"><h2>Question {q_index} · réponse {letter} · diapositive {slide_index}</h2><p>{escape(quiz["answer"])}</p></article>'
        sections.append(f'<section class="slide appendix" data-index="{index}" aria-label="{title}">{header("Annexes · Raisonnement","Après discussion")}<div class="heading"><h1>{title}</h1><p class="lead">L’argument compte davantage que la lettre choisie.</p></div><div class="answer-list">{cards}</div>{footer(index,detail=False)}</section>')
        data.append(dict(title=title,chapter='Annexes · Questions',lead='Réponses et explications',minutes=0,refs=[],detail='Ces réponses dépendent des conditions énoncées. Faire varier une condition et demander ce qui change.'))
    return sections,data


def build_html():
    total=0;sections=[]
    for i,item in enumerate(SLIDES):
        sections.append(build_core(item,i,total));total+=item['minutes']
    appendices,extra=build_appendices();sections.extend(appendices)
    css=(HERE/'course.css').read_text(encoding='utf-8');js=(HERE/'course.js').read_text(encoding='utf-8')
    json_refs=json.dumps(REFERENCES,ensure_ascii=False).replace('</','<\\/')
    json_slides=json.dumps(SLIDES+extra,ensure_ascii=False).replace('</','<\\/')
    html=f'''<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="author" content="Roland Cédric TAYO"><meta name="description" content="Cours de trois heures sur l’IA embarquée : briques, contraintes, optimisation, recherche et validation."><title>IA pour les systèmes embarqués — Roland Cédric TAYO</title><style>{css}</style></head><body><main id="viewport" aria-label="Présentation IA embarquée"><div id="scaled"><div id="deck">{''.join(sections)}</div></div></main><nav class="controls" aria-label="Navigation"><button data-action="prev" aria-label="Diapositive précédente">←</button><button data-action="next" aria-label="Diapositive suivante">→</button><span class="position" id="position">1 / {CORE_COUNT} · parcours</span><span class="key-hint">← → · T plan · D approfondir · F plein écran</span><button data-action="toc" aria-label="Ouvrir le plan, les cinq questions et les cinq quiz">Plan &amp; questions</button><button data-action="sources" aria-label="Accéder au TD, aux sources et aux documents du cours">Ressources</button><a class="pdf-link" href="lab/" target="_blank" rel="noopener noreferrer" aria-label="Ouvrir l’énoncé et les ressources du TD">TD ↗</a><a class="pdf-link" href="course.pdf" target="_blank" rel="noopener noreferrer" aria-label="Ouvrir le cours en PDF">PDF ↗</a><button data-action="motion" aria-pressed="false">Animation : oui</button><button data-action="fullscreen" aria-label="Basculer le plein écran">⛶</button></nav><div id="progress" class="progress-line" aria-hidden="true"></div><div id="announcement" class="sr-only" aria-live="polite"></div><dialog id="reader" aria-labelledby="reader-title"><div class="dialog-header"><h2 id="reader-title">Approfondir</h2><button data-action="close" aria-label="Fermer la fenêtre">×</button></div><div id="reader-body" class="dialog-body"></div></dialog><script type="application/json" id="reference-data">{json_refs}</script><script type="application/json" id="slide-data">{json_slides}</script><script>{js}</script></body></html>'''
    path=OUT/'index.html';path.write_text(html,encoding='utf-8')
    (OUT/'references.json').write_text(json.dumps(REFERENCES,indent=2,ensure_ascii=False),encoding='utf-8')
    lines=['# Sources du cours','', 'Roland Cédric TAYO — références scientifiques et documentation. Sources pédagogiques : TEACHING-DESIGN.md.','',
           'Les prépublications ne sont pas présentées comme un consensus ou un classement de l’état de l’art. Les schémas du cours sont originaux et les données des démonstrations sont analytiques ou illustratives.','']
    for r in REFERENCES:
        lines.extend([f'## {r["id"]} — {r["title"]}',f'{r["authors"]}. {r["year"]}. {r["status"]}.',f'[Source originale]({r["url"]})',f'Apport : {r["takeaway"]}',f'Limite : {r["limit"]}',''])
    (OUT/'SOURCES.md').write_text('\n\n'.join(lines).rstrip()+'\n',encoding='utf-8')
    (OUT/'references.bib').write_text('\n\n'.join('@misc{'+r['id']+',\n  title={'+r['title']+'},\n  author={{'+r['authors']+'}},\n  year={'+(r['year'][:4] if r['year'][:4].isdigit() else 'n.d.')+'},\n  howpublished={'+r['status']+'},\n  url={'+r['url']+'},\n  urldate={2026-10-20},\n  note={Consulted 20 October 2026; date label: '+r['year']+'}\n}' for r in REFERENCES),encoding='utf-8')
    return path,len(sections)


def build_plan(page):
    css="""@page{size:A4;margin:19mm 21mm}*{box-sizing:border-box}body{font:10.5pt/1.4 Georgia,'Times New Roman',serif;color:#18394b;margin:0}.page{height:258mm;display:flex;flex-direction:column;break-after:page}.page:last-child{break-after:auto}h1{font-size:23pt;line-height:1.15;font-weight:normal;margin:20px 0 12px}h2{font-size:12pt;margin:16px 0 6px}p{margin:6px 0 9px}table{width:100%;border-collapse:collapse;font-size:10pt}td,th{text-align:left;padding:7px 6px;border-bottom:1px solid #d1dce0;vertical-align:top}th{border-top:2px solid #008b83}a{color:#006f70;text-decoration:none}li{margin-bottom:7px}.small{font-size:9pt;color:#607684}.footer{margin-top:auto;border-top:1px solid #cdd9df;padding-top:9px;font-size:9pt;color:#607684}.kicker{font:9pt Arial;letter-spacing:1px;text-transform:uppercase;color:#008b83}"""
    html=f"""<!doctype html><html lang="fr"><meta charset="utf-8"><title>Parcours — IA embarquée</title><style>{css}</style><body>
<article class="page"><div class="kicker">INEM · IA pour les systèmes embarqués</div><h1>Du besoin à la preuve</h1><p><b>Roland Cédric TAYO</b> · 180 minutes, pause et échanges compris.</p><p>Ce cours de synthèse ouvre le module de <b>14 h de cours et 14 h de TD</b>. Le TD et le projet prolongent la programmation, le déploiement et les expériences ; les trois heures ne constituent pas à elles seules tout le module.</p>
<h2>Parcours principal · {CORE_COUNT} diapositives</h2><table><thead><tr><th>Minutes</th><th>Question et activité</th><th>Preuve attendue</th></tr></thead><tbody>
<tr><td>0–20</td><td>Besoin, histoire et lieu du calcul</td><td>Justifier où reconnaître une commande.</td></tr>
<tr><td>20–55</td><td>Un réseau complet ; lien avec le TD</td><td>Calculer une sortie, une perte et un nombre de paramètres.</td></tr>
<tr><td>55–85</td><td>Déployer, mémoire, délai et énergie</td><td>Reconstituer un pic RAM et un budget.</td></tr>
<tr><td>85–95</td><td>Pause</td><td>10 minutes incluses.</td></tr>
<tr><td>95–130</td><td>Quantifier, réutiliser et expérimenter</td><td>Vérifier les sorties, lire les mesures et le gain global.</td></tr>
<tr><td>130–160</td><td>Enquête, risques et reproductibilité</td><td>Décrire une expérience falsifiable et ses traces.</td></tr>
<tr><td>160–180</td><td>Décision finale et acquis</td><td>Défendre un choix face à quatre contraintes.</td></tr></tbody></table>
<h2>Cinq quiz</h2><p>Diapositives 6, 13, 19, 26 et 31 : architecture, paramètres et MAC, pic RAM, gain global, puis choix multicritère. Calculer ou dessiner avant de choisir ; expliquer ce qui pourrait changer la réponse.</p>
<h2>Prérequis</h2><p>Fonctions, tableaux, boucles, vecteurs/matrices, moyenne et dérivées simples ; bases processeur/mémoire. Les symboles indispensables sont expliqués dans les diapositives.</p>
<div class="footer">Roland Cédric TAYO · 1 / 2</div></article>
<article class="page"><div class="kicker">Comprendre, manipuler et prolonger</div><h1>Acquis et ressources</h1>
<ol><li>Relier un service humain au choix d’une méthode et au lieu du calcul.</li><li>Suivre un petit réseau 2 → 2 → 1 : poids, biais, activation, prédiction, perte et correction.</li><li>Distinguer apprentissage sur PC, export, inférence sur carte et vérification des sorties.</li><li>Compter poids et pic RAM ; distinguer temps, puissance et énergie.</li><li>Étudier une approximation et une réorganisation, puis comparer référence et variante.</li><li>Relier une conclusion à un commit, une configuration, des mesures brutes et des limites.</li></ol>
<h2>Manipulations dans la présentation HTML</h2><p>Modifier les entrées du petit réseau ; ajuster un pas d’apprentissage ; observer une quantification ; comparer deux sommes avec échauffement, sept paires alternées et export CSV. Les mesures de cette dernière expérience sont celles du <b>navigateur utilisé</b>, jamais celles d’un MCU ou d’un Pi.</p>
<h2>Du cours au TD</h2><p>Le TD utilise trois signaux simulés et un petit Mixer de prédiction. Les exemples du cours expliquent des mécanismes indépendants ; ils ne fournissent pas le corrigé du réseau, ses poids entraînés ou ses résultats sur carte. Les mesures de qualité du TD sont des erreurs de régression, pas un taux de bonnes classes.</p>
<h2>Annexes et lectures</h2><p>Convolution, récurrence, attention, cache KV, compression et veille récente restent disponibles hors parcours oral. Lire MCUNet et MCUNetV2 pour la co-conception ; TSMixer pour la famille du TD. AWQ, T-MAC et les prépublications récentes sont des prolongements.</p>
<p><a href="https://rolln7drktayau.github.io/courses/embedded-ai/">Présentation et accès aux ressources</a> · <a href="https://rolln7drktayau.github.io/courses/embedded-ai/lab/">Énoncé et documents étudiants</a>.</p><p class="small">Sources scientifiques : SOURCES.md. Choix pédagogiques et cours d’inspiration : TEACHING-DESIGN.md. Le PDF affiche les exemples initiaux et les réponses aux quiz en annexes ; les interactions et l’export des mesures nécessitent le HTML.</p><div class="footer">Roland Cédric TAYO · 2 / 2</div></article></body></html>"""
    path=OUT/'source'/'plan.html';path.write_text(html,encoding='utf-8')
    page.goto(path.as_uri());page.emulate_media(media='print');page.pdf(path=str(OUT/'course-plan.pdf'),prefer_css_page_size=True,print_background=True)


def main():
    path,count=build_html()
    with sync_playwright() as p:
        browser=p.chromium.launch(executable_path=str(CHROME) if CHROME.exists() else None,headless=True)
        page=browser.new_page(viewport={'width':1600,'height':1000})
        page.goto(path.as_uri());page.wait_for_function('document.documentElement.dataset.ready === "true"')
        page.emulate_media(media='print');page.pdf(path=str(OUT/'course.pdf'),prefer_css_page_size=True,print_background=True)
        build_plan(page);browser.close()
    for file,title in [('course.pdf','IA pour les systèmes embarqués — Du besoin à la preuve'),('course-plan.pdf','Plan du cours — 180 minutes')]:
        target=OUT/file;doc=fitz.open(target);doc.set_metadata({'title':title,'author':'Roland Cédric TAYO','subject':'INEM'})
        if file=='course.pdf':
            assert len(doc)==count,(len(doc),count)
            toc=[];seen=set()
            for i,s in enumerate(SLIDES):
                if s['chapter'] not in seen:toc.append([1,s['chapter'],i+1]);seen.add(s['chapter'])
                toc.append([2,s['title'].replace('\n',' '),i+1])
            toc.append([1,'Annexes — Architectures, recherche et références',CORE_COUNT+1])
            _,extra=build_appendices()
            toc.extend([2,s['title'],CORE_COUNT+1+i] for i,s in enumerate(extra));doc.set_toc(toc)
        else:assert len(doc)==2,len(doc)
        temporary=target.with_suffix('.tmp.pdf');doc.save(temporary,garbage=4,deflate=True);doc.close();temporary.replace(target)
    print(json.dumps({'oral_slides':CORE_COUNT,'appendices':count-CORE_COUNT,'minutes_including_break':180,'references':len(REFERENCES),'html_bytes':path.stat().st_size}))


if __name__=='__main__':main()
