"""Build the no-scroll deck from the existing reviewed course and its illustrations."""
from pathlib import Path
import json,runpy
import markdown
from bs4 import BeautifulSoup
from curriculum import CHAPTERS,SHORT_CHAPTERS,COURSE_REFS,ADDITIONS,chapter

ROOT=Path(__file__).resolve().parent
helpers=runpy.run_path(str(ROOT/'build_reader.py'))
data=json.loads((ROOT/'cours-source.json').read_text(encoding='utf-8'))
reader=BeautifulSoup((ROOT/'reading.html').read_text(encoding='utf-8'),'html.parser')
slides=[]
data['references'].update(COURSE_REFS)
data['chapters']=CHAPTERS
all_lessons=[]
activities={
 8:dict(id='assembler',title='Construisez la chaîne de la lampe',lead='Une prédiction ne produit une action utile que si les bonnes briques sont reliées.',activity='assembly',ch=0,
        steps=['Choisissez une brique dans la réserve. Placez-la dans une case en cliquant, ou faites-la glisser.',
               'L’ordre recherché commence avec le son réel et finit avec la lumière. Les données changent de forme entre les deux.',
               'Vérifiez votre chaîne. Expliquez ce que reçoit et produit chaque brique, puis suivez le trajet animé.'],
        limit='Les flèches montrent un ordre logique, pas une durée. Une vraie acquisition peut fonctionner en parallèle du calcul.'),
 29:dict(id='objet-3d',title='Ouvrez la petite machine',lead='Tournez l’objet pour explorer trois rôles : conserver, calculer et travailler.',activity='board',ch=3,
        steps=['Faites glisser le dessin pour le tourner. Le curseur permet aussi de régler la rotation sans souris.',
               'Cliquez sur Stockage, CPU ou RAM. Chaque pièce décrit ce qu’elle garde ou ce qu’elle fait.',
               'Isolez une pièce, puis réassemblez. Le CPU ne remplace ni le stockage ni la RAM.'],
        limit='Maquette 3D schématique en CSS. Ce n’est ni une carte électronique réelle ni une simulation de ses performances.'),
 32:dict(id='table-memoire',title='Faites tenir le travail dans la RAM',lead='Tout ce qui sert au même instant doit tenir sur la même table de travail.',activity='packing',ch=3,
        steps=['Le budget fictif est de 100 octets de RAM. Les entrées, activations et calculs temporaires occupent ici 32 + 16 + 64 = 112 octets.',
               'Réduisez la mémoire temporaire avec le curseur. Observez le total et la place qui reste.',
               'Dans un vrai programme, réduire le temporaire demande une méthode : réutiliser un tampon, traiter par blocs ou changer le calcul, puis vérifier les sorties.'],
        limit='Exemple de budget fictif : ces tailles ne viennent pas d’un benchmark. Les autres mémoires d’une vraie application ne sont pas comptées.'),
 45:dict(id='aller-retour',title='Suivez un essai du PC à la carte',lead='On prépare la même entrée, on exécute le modèle sur la cible, puis on récupère les résultats.',activity='deployment',ch=5,
        steps=['Préparer sur PC : entrée [1, 0], poids [0,2 ; −0,1], biais −0,5 et version du programme.',
               'Exécuter sur la carte, puis récupérer sortie et mesures brutes. Ici, le trajet est simulé dans le navigateur : aucun Raspberry Pi n’est connecté.',
               'Comparer au PC. Dans cet exemple, le score vaut −0,3 et la classe vaut 0 au seuil zéro. Le temps sur Pi est indiqué « non mesuré ».'],
        limit='L’animation ne représente pas un transfert réseau réel. Le petit calcul est réellement exécuté dans le navigateur, sans mesure matérielle.'),
}
for index,item in enumerate(data['lessons'],1):
 article=reader.find('article',id=f'etape-{index}')
 item=dict(item,id=f'etape-{index}',ch=chapter(index))
 article['data-chapter']=str(item['ch'])
 article.find('div',class_='eyebrow').string=f"CHAPITRE {item['ch']+1} · {CHAPTERS[item['ch']]} · REPÈRE {index}"
 figure=article.find('figure')
 item=dict(item,id=f'etape-{index}',lesson=index,activity='',diagram=str(figure.find('svg')),caption=figure.find('figcaption').get_text())
 slides.append(item)
 all_lessons.append({k:v for k,v in item.items() if k not in ['diagram','caption','activity']})
 if index in activities:
  a=dict(activities[index],ch=chapter(index))
  slides.append(dict(analogy='',deep='',quiz=None,widget='',source=[],flow=[],diagram='',caption='',lesson=index,**a))
 previous=article
 for extra in [e for e in ADDITIONS if e['after']==index]:
  e=dict(extra)
  e['diagram']=helpers['diagram'](e['flow'],e['id'])
  e['caption']='Construction progressive d’un schéma logique. Aucun résultat matériel original n’est annoncé.'
  if e['id']=='arbre-simple':
   e['diagram']='''<svg viewBox="0 0 1000 470" role="img" aria-labelledby="tree-title"><title id="tree-title">Présence ? Non : éteindre. Oui : vérifier si la pièce est sombre, puis allumer ou éteindre.</title><defs><marker id="tree-arrow" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto"><path d="M0 0 L6 3 L0 6" fill="#688480"/></marker></defs><rect class="node n0" x="350" y="20" width="300" height="75" rx="14" data-phase="0"/><text x="500" y="64" text-anchor="middle" data-phase="0">Présence détectée ?</text><path class="arrow" d="M430 95 L220 210" marker-end="url(#tree-arrow)" data-phase="1"/><text x="285" y="150" data-phase="1">Non</text><rect class="node n1" x="70" y="210" width="300" height="75" rx="14" data-phase="1"/><text x="220" y="255" text-anchor="middle" data-phase="1">Garder éteint</text><path class="arrow" d="M570 95 L760 210" marker-end="url(#tree-arrow)" data-phase="2"/><text x="700" y="150" data-phase="2">Oui</text><rect class="node n2" x="610" y="210" width="300" height="75" rx="14" data-phase="2"/><text x="760" y="255" text-anchor="middle" data-phase="2">Pièce sombre ?</text><path class="arrow" d="M690 285 L560 370" marker-end="url(#tree-arrow)" data-phase="3"/><path class="arrow" d="M830 285 L870 370" marker-end="url(#tree-arrow)" data-phase="3"/><text x="580" y="335" data-phase="3">Non</text><text x="860" y="335" data-phase="3">Oui</text><rect class="node n1" x="425" y="370" width="270" height="65" rx="14" data-phase="3"/><text x="560" y="410" text-anchor="middle" data-phase="3">Garder éteint</text><rect class="node n2" x="735" y="370" width="250" height="65" rx="14" data-phase="3"/><text x="860" y="410" text-anchor="middle" data-phase="3">Allumer</text></svg>'''
   e['caption']='Chaque branche correspond à une réponse, pas à une succession d’actions. Arbre écrit pour l’exemple, sans entraînement.'
  slides.append(e)
  all_lessons.append({k:v for k,v in e.items() if k not in ['diagram','caption','activity','after']})
  H=helpers['esc']
  ref_links=' · '.join(f'<a href="{H(data["references"][r][1])}">{H(r)} · {H(data["references"][r][0])}</a>' for r in e['source'])
  markup=f'<article class="lesson" id="{e["id"]}" data-chapter="{e["ch"]}"><div class="eyebrow">CHAPITRE {e["ch"]+1} · {H(CHAPTERS[e["ch"]])}</div><h1>{H(e["title"])}</h1><p class="lead">{H(e["lead"])}</p><figure>{e["diagram"]}<figcaption>{H(e["caption"])}</figcaption></figure><ol class="steps">'+''.join(f'<li><span>{n+1:02}</span><p>{H(t)}</p></li>' for n,t in enumerate(e['steps']))+f'</ol><aside class="limit"><b>La limite à garder en tête</b><p>{H(e["limit"])}</p></aside><details class="deeper"><summary>Aller plus loin, sans sauter d’étape</summary><p>{H(e["deep"])}</p></details><p class="sources">Pour continuer : {ref_links}</p><footer>Roland Cédric TAYO · INEM <span></span></footer></article>'
  tag=BeautifulSoup(markup,'html.parser').article
  previous.insert_after(tag);previous=tag
for n,article in enumerate(reader.select('article.lesson'),1):
 footer=article.find('footer')
 if footer and footer.find('span'):footer.find('span').string=f'{n} / {len(all_lessons)}'
for r,v in COURSE_REFS.items():
 li=BeautifulSoup(f'<li id="{r}"><b>{helpers["esc"](r+" · "+v[0])}</b><p>{helpers["esc"](v[2])}</p><a href="{v[1]}">{v[1]}</a></li>','html.parser').li
 reader.select_one('.references').append(li)
extra_style=reader.new_tag('style');extra_style.string='@media print{#arbre-simple figure svg{max-height:230px}}';reader.head.append(extra_style)
(ROOT/'reading.html').write_text(str(reader),encoding='utf-8')
data['lessons']=all_lessons
(ROOT/'cours-source.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
payload={'slides':slides,'chapters':CHAPTERS,'shortChapters':SHORT_CHAPTERS,'references':data['references'],'glossary':data['glossary']}
(ROOT/'assets/course-data.js').write_text('window.COURSE_DATA='+json.dumps(payload,ensure_ascii=False,separators=(',',':'))+';\n',encoding='utf-8')
print(f'{len(slides)} slides; {len(all_lessons)} concepts; {len(activities)} practical scenes; eight named chapters.')
comparison=markdown.markdown((ROOT/'CURRICULUM-COMPARISON.md').read_text(encoding='utf-8'),extensions=['tables'])
style='body{max-width:1080px;margin:40px auto;padding:0 24px;font:18px/1.6 "Segoe UI",Arial,sans-serif;color:#18342f;background:#f7f6f1}h1{font-size:40px;line-height:1.2}h2{margin-top:40px}a{color:#087e79}table{width:100%;border-collapse:collapse;font-size:15px;background:#fff}th,td{border:1px solid #cad8ce;padding:13px;text-align:left;vertical-align:top}th{background:#d7eee5}@media(max-width:700px){table{display:block;overflow-x:auto}body{font-size:16px}h1{font-size:30px}}'
(ROOT/'curriculum-comparison.html').write_text('<!doctype html><html lang="fr"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Comparer les cursus · IA embarquée</title><style>'+style+'</style><body><a href="./">← Revenir au cours</a>'+comparison+'</body></html>',encoding='utf-8')
