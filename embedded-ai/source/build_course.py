"""Build the offline HTML deck, 16:9 PDF and compact A4 course plan."""
from pathlib import Path
from html import escape
import json
import shutil
import zipfile
import base64
import fitz
from playwright.sync_api import sync_playwright
from content import SLIDES,REFERENCES,CORE_COUNT,ADVANCED
from diagrams import draw

HERE=Path(__file__).resolve().parent
OUT=HERE.parent
REF={r['id']:r for r in REFERENCES}
CHROME=Path(r'C:\Program Files\Google\Chrome\Application\chrome.exe')


def footer(index,refs=(),detail=True,badge=''):
    citations=''.join(f'<a class="ref" href="{escape(REF[k]["url"],quote=True)}" data-ref="{k}" title="{escape(REF[k]["title"],quote=True)}">{k} · {REF[k]["year"]}</a>' for k in refs)
    detail_button='<button class="detail-button" data-action="details">Approfondir ↗</button>' if detail else ''
    if index<CORE_COUNT and not SLIDES[index]['quiz'] and SLIDES[index]['kind']!='hero':
        detail_button='<button class="detail-button reveal-all" data-action="revealall">Tout montrer</button>'+detail_button
    if badge:citations='<span class="ref">'+escape(badge)+'</span>'+citations
    count=f'{index+1:02d} / {CORE_COUNT}' if index<CORE_COUNT else f'A{index-CORE_COUNT+1:02d}'
    return f'<footer class="slide-footer"><span class="author">Roland Cédric TAYO · INEM</span><span class="citations">{citations}{detail_button}</span><span class="slide-num">{count}</span></footer>'


def header(chapter,time):
    return f'<header class="topline"><span class="brand">Embedded AI <span style="font-weight:400;letter-spacing:0">/ INEM</span></span><span class="chapter">{escape(chapter)}</span><span class="plan-time">{escape(time)}</span></header>'


def quiz_support(quiz):
    """Show only the data needed to answer the current question."""
    support=quiz.get('support')
    if support=='voice':
        from story_art import picture
        return '<div class="quiz-voice">'+picture(1,'Des personnes différentes essaient une commande vocale.')+'</div>'
    if support=='forward':
        return '<div class="quiz-data"><h2>Les calculs du réseau</h2><p>h₁ = max(0, x₁ − x₂)</p><p>h₂ = max(0, 0,5x₁ + 0,5x₂)</p><p>ŷ = 2h₁ + h₂</p></div>'
    if support=='placement':
        return '<div class="quiz-data"><h2>Deux exigences</h2><p>1. Fonctionner sans Internet.</p><p>2. Garder l’audio dans la lampe.</p></div>'
    if support=='memory':
        return '<table class="quiz-data-table"><caption>Présents en RAM au même moment</caption><thead><tr><th>Usage</th><th>Kio</th></tr></thead><tbody><tr><td>Activations</td><td>60</td></tr><tr><td>Temporaires</td><td>40</td></tr><tr><td>Pile</td><td>20</td></tr><tr><td>Entrées-sorties</td><td>16</td></tr></tbody></table><p class="quiz-data-note">La carte dispose de 128 Kio de RAM.</p>'
    if support=='timing':
        return '<div class="quiz-data"><h2>Avant : 100 ms au total</h2><p>Autres étapes : 80 ms.</p><p>Brique à optimiser : 20 ms.</p><div class="quiz-time-bar"><span>80 ms</span><b>20 ms</b></div></div>'
    if quiz.get('decision'):
        return '<table class="decision-table"><caption>Valeurs fictives · même protocole</caption><thead><tr><th>Modèle</th><th>Qualité</th><th>Kio</th><th>ms¹</th><th>mJ</th></tr></thead><tbody><tr><th>A</th><td>97 %</td><td>120</td><td>12</td><td>2,4</td></tr><tr><th>B</th><td>96 %</td><td>96</td><td>18</td><td>2,8</td></tr><tr><th>C</th><td>95 %</td><td>72</td><td>14</td><td>1,8</td></tr></tbody></table><small>¹ p95 sur 500 essais fictifs. Énergie : acquisition + calcul + action, hors veille.</small>'
    return ''


def build_core(item,index,start):
    title=escape(item['title']).replace('\n','<br>')
    lead=escape(item['lead']);is_main=index<CORE_COUNT
    body=''.join(f'<li class="fragment" data-step="{i+1}">'+point+'</li>' if is_main else '<li>'+point+'</li>' for i,point in enumerate(item['points']))
    time=f'{start:02d}–{start+item["minutes"]:02d} min · {item["minutes"]} min'
    kind=item.get('kind','');attrs=f'data-index="{index}" data-minutes="{item["minutes"]}" aria-label="{escape(item["title"].replace(chr(10)," "),quote=True)}"'
    top=header(item['chapter'],time if is_main else 'Lecture libre')
    quote=item.get('quote','')
    dialogue=f'<blockquote class="dialogue"><p>{escape(quote)}</p><cite>Alice</cite></blockquote>' if quote else ''
    takeaway=f'<p class="takeaway fragment" data-step="3"><span>L’idée à retenir</span>{escape(item.get("takeaway",""))}</p>' if item.get('takeaway') else ''
    if kind=='hero':
        middle=f'<div class="hero-grid"><div><div class="eyebrow">IA pour les systèmes embarqués</div><h1>{title}</h1><p class="lead">{lead}</p><div class="hero-author">Roland Cédric TAYO</div><p class="fiction-note">3 heures · Six chapitres · Questions et expériences<br>Alice est fictive. Les découvertes sont documentées.</p><p class="entry-help">→ Dévoiler puis avancer · A Tout montrer · T Sommaire</p></div><div class="hero-art">{draw(item["visual"])}</div></div>'
    else:
        heading=f'<div class="heading"><h1>{title}</h1><p class="lead">{lead}</p></div>'
        if kind=='opening':
            cards=''.join(f'<article class="opening-card fragment" data-step="{i+1}"><span>{i+1:02d}</span><h2>{escape(question)}</h2></article>' for i,question in enumerate(item['prompts']))
            middle=heading+f'<div class="content opening-content"><div class="opening-grid">{cards}</div><p class="opening-instruction">Proposez une réponse avec vos mots. Gardez-la en tête pour la fin du cours.</p></div>'
        elif item['visual']=='history_timeline':
            middle=heading+f'<div class="content history-wide"><div class="visual fragment" data-step="1">{draw(item["visual"])}</div>{takeaway}</div>'
        elif kind=='quiz':
            quiz=item['quiz']
            options=''.join(f'<button class="quiz-choice" data-answer="{i}" aria-pressed="false"><span class="letter">{"ABC"[i]}</span><span>{escape(option)}</span></button>' for i,option in enumerate(quiz['options']))
            task=escape(item.get('task') or 'Expliquez votre raisonnement avant de choisir.')
            context=quiz_support(quiz)
            discussion='<div class="quiz-followup" hidden><small>Pour poursuivre après la réponse</small><ul class="discussion">'+''.join('<li>'+escape(question)+'</li>' for question in item.get('questions',[]))+'</ul></div>'
            middle=heading+f'<div class="content quiz-layout"><div class="quiz-prompt">{context}<p>{task}</p>{discussion}</div><div class="quiz-options">{options}<p class="quiz-feedback" aria-live="polite">Discutez, calculez, puis choisissez. L’explication apparaîtra ici.</p></div></div>'
        else:
            copy=dialogue+f'<ul class="points">{body}</ul>'+takeaway
            middle=heading+f'<div class="content"><div class="story-copy">{copy}</div><div class="visual">{draw(item["visual"])}</div></div>'
    classes=f'slide {kind} {"story" if is_main else "appendix"} {item.get("layout", "technical")} {"active" if index==0 else ""}'
    return f'<section class="{classes}" {attrs}>{top}{middle}{footer(index,item["refs"],badge=item.get("badge",""))}</section>'


def build_appendices():
    sections=[];data=[]
    for item in ADVANCED:
        index=CORE_COUNT+len(sections)
        sections.append(build_core(item,index,0))
        data.append(item)
    for group in range(0,len(REFERENCES),4):
        refs=REFERENCES[group:group+4];index=CORE_COUNT+len(sections)
        title=f'Sources et limites de lecture · {group//4+1}/{(len(REFERENCES)+3)//4}'
        cards=''
        for r in refs:
            cards+=f'<article class="reference-item"><span class="reference-code">{r["id"]}</span><div><h2><a href="{escape(r["url"],quote=True)}" target="_blank" rel="noopener noreferrer">{escape(r["title"])} ↗</a></h2><p class="ref-meta">{escape(r["authors"])} · {escape(r["year"])} · {escape(r["status"])}</p><p class="ref-takeaway">{escape(r["takeaway"])}</p></div></article>'
            if group>=24:
                cards=cards[:-len('</div></article>')]+f'<p class="ref-limit">Limite : {escape(r["limit"])}</p></div></article>'
        if len(refs)==1:
            for key in ['R10','R09','R11']:
                r=REF[key]
                cards+=f'<article class="reference-item"><span class="reference-code">À lire</span><div><h2><a href="{r["url"]}">{escape(r["title"])} ↗</a></h2><p class="ref-takeaway">{escape(r["limit"])}</p></div></article>'
        bib_class=' history-bib' if group>=24 else ''
        sections.append(f'<section class="slide appendix{bib_class}" data-index="{index}" aria-label="{title}">{header("Annexes · Bibliographie","Lecture libre")}<div class="heading"><h1>{title}</h1><p class="lead">Articles originaux, prépublications et documentation officielle · lire les limites de chaque source.</p></div><div class="reference-list">{cards}</div>{footer(index,detail=False)}</section>')
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
    for group in range(0,len(quizzes),3):
        index=CORE_COUNT+len(sections);title=f'Réponses raisonnées · {group//3+1}/2';cards=''
        for q_index,(slide_index,s) in enumerate(quizzes[group:group+3],start=group+1):
            quiz=s['quiz'];letter='ABC'[quiz['correct']]
            cards+=f'<article class="answer-item"><h2>Questions {q_index} · réponse {letter} · diapositive {slide_index}</h2><p>{escape(quiz["answer"])}</p></article>'
        sections.append(f'<section class="slide appendix" data-index="{index}" aria-label="{title}">{header("Annexes · Raisonnement","Après discussion")}<div class="heading"><h1>{title}</h1><p class="lead">L’argument compte davantage que la lettre choisie.</p></div><div class="answer-list">{cards}</div>{footer(index,detail=False)}</section>')
        data.append(dict(title=title,chapter='Annexes · Questions',lead='Réponses et explications',minutes=0,refs=[],detail='Ces réponses dépendent des conditions énoncées. Faire varier une condition et demander ce qui change.'))
    return sections,data


def build_html():
    total=0;sections=[]
    for i,item in enumerate(SLIDES):
        sections.append(build_core(item,i,total));total+=item['minutes']
    appendices,extra=build_appendices();sections.extend(appendices)
    css=(HERE/'course.css').read_text(encoding='utf-8');js=(HERE/'course.js').read_text(encoding='utf-8')
    sheet=base64.b64encode((OUT/'assets'/'alice-scenes.png').read_bytes()).decode('ascii')
    # Direct URL avoids Chromium's size limit on CSS custom-property values.
    css+='\n.scene-picture{background-image:url("data:image/png;base64,'+sheet+'")!important}'
    history=base64.b64encode((OUT/'assets'/'history-scenes.png').read_bytes()).decode('ascii')
    history_image=fitz.Pixmap(str(OUT/'assets'/'history-scenes.png'))
    ratio=f'{history_image.width/2}/{history_image.height}'
    css+='\n.history-picture{aspect-ratio:'+ratio+';background-image:url("data:image/png;base64,'+history+'")!important}'
    json_refs=json.dumps(REFERENCES,ensure_ascii=False).replace('</','<\\/')
    json_slides=json.dumps(SLIDES+extra,ensure_ascii=False).replace('</','<\\/')
    html=f'''<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="author" content="Roland Cédric TAYO"><meta name="description" content="Cours de trois heures sur l’IA embarquée : briques, contraintes, optimisation, recherche et validation."><title>IA pour les systèmes embarqués — Roland Cédric TAYO</title><style>{css}</style></head><body><main id="viewport" aria-label="Présentation IA embarquée"><div id="scaled"><div id="deck">{''.join(sections)}</div></div></main><nav class="controls" aria-label="Navigation"><button data-action="prev" aria-label="Diapositive précédente">←</button><button data-action="next" aria-label="Étape ou diapositive suivante">→</button><span class="position" id="position">1 / {CORE_COUNT} · histoire</span><span class="key-hint">→ dévoiler · A tout · T plan · F plein écran</span><button data-action="toc" aria-label="Ouvrir le plan, les six actes et leurs questions">Histoire &amp; questions</button><button data-action="sources" aria-label="Accéder au TD, aux sources et aux documents du cours">Ressources</button><a class="pdf-link" href="https://rolln7drktayau.github.io/courses/embedded-ai/lab/" target="_blank" rel="noopener noreferrer" aria-label="Ouvrir l’énoncé et les ressources du TD">TD ↗</a><a class="pdf-link" href="course.pdf" target="_blank" rel="noopener noreferrer" aria-label="Ouvrir le cours en PDF">PDF ↗</a><button data-action="motion" aria-pressed="false">Animation : oui</button><button data-action="fullscreen" aria-label="Basculer le plein écran">⛶</button></nav><div id="progress" class="progress-line" aria-hidden="true"></div><div id="announcement" class="sr-only" aria-live="polite"></div><dialog id="reader" aria-labelledby="reader-title"><div class="dialog-header"><h2 id="reader-title">Approfondir</h2><button data-action="close" aria-label="Fermer la fenêtre">×</button></div><div id="reader-body" class="dialog-body"></div></dialog><script type="application/json" id="reference-data">{json_refs}</script><script type="application/json" id="slide-data">{json_slides}</script><script>{js}</script></body></html>'''
    path=OUT/'index.html';path.write_text(html,encoding='utf-8')
    (OUT/'references.json').write_text(json.dumps(REFERENCES,indent=2,ensure_ascii=False),encoding='utf-8')
    lines=['# Sources du cours','', 'Roland Cédric TAYO — références scientifiques et documentation. Sources pédagogiques : TEACHING-DESIGN.md.','',
           'Les prépublications ne sont pas présentées comme un consensus ou un classement de l’état de l’art. Les schémas du cours sont originaux et les données des démonstrations sont analytiques ou illustratives.','']
    for r in REFERENCES:
        lines.extend([f'## {r["id"]} — {r["title"]}',f'{r["authors"]}. {r["year"]}. {r["status"]}.',f'[Source originale]({r["url"]})',f'Apport : {r["takeaway"]}',f'Limite : {r["limit"]}',''])
    (OUT/'SOURCES.md').write_text('\n\n'.join(lines).rstrip()+'\n',encoding='utf-8')
    (OUT/'references.bib').write_text('\n\n'.join('@misc{'+r['id']+',\n  title={'+r['title']+'},\n  author={{'+r['authors']+'}},\n  year={'+(r['year'][:4] if r['year'][:4].isdigit() else 'n.d.')+'},\n  howpublished={'+r['status']+'},\n  url={'+r['url']+'},\n  urldate={2026-10-20},\n  note={Consulted 20 October 2026; date label: '+r['year']+'}\n}' for r in REFERENCES),encoding='utf-8')
    return path,len(sections)




from plan_build import build_plan


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
        else:assert len(doc)==5,len(doc)
        temporary=target.with_suffix('.tmp.pdf');doc.save(temporary,garbage=4,deflate=True);doc.close();temporary.replace(target)
    print(json.dumps({'oral_slides':CORE_COUNT,'appendices':count-CORE_COUNT,'minutes_including_break':180,'references':len(REFERENCES),'html_bytes':path.stat().st_size}))


if __name__=='__main__':main()
