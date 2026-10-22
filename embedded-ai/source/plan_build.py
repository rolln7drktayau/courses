"""Build a five-page A4 course plan from the same timed slide data."""
from pathlib import Path
from html import escape
import json


def build_plan(page):
    root=Path(__file__).resolve().parent.parent
    data=json.loads((root/'source/planning.json').read_text(encoding='utf-8'))
    from content import SLIDES
    clock=0
    for expected,actual in zip(data['slides'],SLIDES,strict=True):
        assert (expected['title'],expected['start'],expected['end'],expected['minutes'])==(actual['title'].replace('\n',' '),clock,clock+actual['minutes'],actual['minutes'])
        clock+=actual['minutes']
    assert clock==180
    pages=[]
    chapters=[]
    for s in data['slides']:
        if not chapters or chapters[-1]['name']!=s['chapter']:
            chapters.append(dict(name=s['chapter'],start=s['start'],end=s['end']))
        else:chapters[-1]['end']=s['end']
    rows=''.join(f'<tr><td>{escape(c["name"])}</td><td>{c["start"]}–{c["end"]} min</td></tr>' for c in chapters)
    pages.append('''<div class="kicker">IA pour les systèmes embarqués · INEM</div><h1>Une lampe qui comprend.<br>Même sans Internet.</h1><p class="lead">Du besoin humain aux calculs, puis du modèle à la preuve sur une carte.</p>
    <p>Roland Cédric TAYO · 3 heures · 40 diapositives · pause comprise.</p><h2>Le parcours</h2><table><tbody>'''+rows+'''</tbody></table>
    <h2>Ce que l’on apprend à expliquer</h2><ol><li>Pourquoi calculer dans un objet plutôt que sur un serveur.</li><li>Comment un petit réseau transforme ses entrées et apprend de ses erreurs.</li><li>Pourquoi stockage, RAM, temps et énergie imposent des compromis.</li><li>Comment vérifier une variante sur PC, puis sur Raspberry Pi.</li><li>Pourquoi une hypothèse testée et documentée vaut plus qu’un gain annoncé sans preuve.</li></ol>
    <h2>Usage du support</h2><p>→ dévoile puis avance ; A montre la scène ; T ouvre le plan ; F passe en plein écran. Le bouton Ressources donne accès aux TD, aux sources et au PDF. Les annexes sont des lectures complémentaires hors des trois heures.</p>
    <p>Le perceptron est une introduction distincte. Le TD de recherche utilise un petit réseau de prédiction sur signaux simulés, à programmer et à mesurer sur Raspberry Pi. Les corrigés enseignants ne sont pas publiés.</p>''')
    for start in [0,20]:
        rows=''.join(f'<tr><td>{s["number"]:02d}</td><td>{escape(s["title"])}</td><td>{s["start"]}–{s["end"]}</td><td>{s["minutes"]}</td></tr>' for s in data['slides'][start:start+20])
        pages.append(f'<div class="kicker">Déroulement complet · {start+1}–{start+20}</div><h1>Plan minuté</h1><table class="schedule"><thead><tr><th>N°</th><th>Sujet</th><th>Min</th><th>Durée</th></tr></thead><tbody>{rows}</tbody></table><p>Les six quiz sont aux diapositives 10, 15, 20, 27, 33 et 38. Leurs données, questions et corrections sont conservées. Les renvois des réponses en annexes suivent automatiquement la numérotation.</p>')
    rows=''.join(f'<tr><td>{b["old"]} → {b["new"]}</td><td>{b["before"]} → {b["after"]}</td><td>{escape(b["reason"])}</td></tr>' for b in data['balance'])
    rows+=''.join(f'<tr><td>Ajout {s["number"]}</td><td>0 → {s["minutes"]}</td><td>{escape(s["title"])}</td></tr>' for s in data['added'])
    pages.append('''<div class="kicker">Rééquilibrage avant / après</div><h1>Toujours 180 minutes</h1><p>Les scènes historiques ajoutent 11 minutes ; le pont vers ROS, 2 minutes. Ces 13 minutes sont reprises sur les transitions et échanges.</p><table class="balance"><thead><tr><th>Ancien → nouveau n°</th><th>Minutes</th><th>Justification</th></tr></thead><tbody>'''+rows+'''</tbody></table><p><b>Invariants :</b> pause de 80 à 90 minutes ; calculs et durées conservés (anciennes diapositives 8–12, 24, 29–30). Quiz et corrections inchangés. Énoncé du TD inchangé. Le choix du modèle termine à 175 minutes ; pont ROS 175–177 ; conclusion 177–180.</p>''')
    pages.append('''<div class="kicker">Sources, portée et rigueur</div><h1>Une histoire documentée</h1><h2>Les repères ajoutés</h2><p>R25–26 et R35 : perceptron, Mark I et distinction entre démonstration sur IBM 704 et machine matérielle. R27 : ALVINN, version 1991 et vues décalées. R28–29 : lecture de documents et prototype ANNA. R30 : Optimal Brain Damage. R31 : AlexNet. R32 : Deep Compression. R33–34 : diffusion des outils et du livre TinyML en 2019.</p>
    <p>Les repères déjà présents restent utilisés : R22 pour Shakey ; R02–03 pour MobileNets et le calcul entier ; R04–05 pour MCUNet ; R18 et R21 pour MLPerf Tiny.</p>
    <h2>Ce qui n’est pas affirmé</h2><ul><li>La date exacte de mise en service et la motorisation des potentiomètres du Mark I restent à confirmer dans une archive primaire. La grille de 400 photocellules est décrite par le cours officiel Stanford.</li><li>Les dimensions 960 → 5 → 30 sont celles d’ALVINN en 1991. Les vues décalées sont documentées ; les rotations ne sont pas affirmées.</li><li>ANNA est un prototype ; les lecteurs commerciaux de chèques sont une application distincte.</li><li>2019 est un jalon de diffusion du TinyML, pas l’invention de toute IA sur microcontrôleur.</li><li>Le pont ROS cadre la suite avec Philippe. Aucun gain chiffré, équation de stabilité ou citation non publiée ne lui est attribué.</li></ul>
    <h2>Les questions d’ouverture</h2><p>Leur texte et leur sens restent identiques. L’histoire aide à répondre à la question sur le passage du PC à une petite carte. Trois minutes sont prévues pour des réponses brèves ; les explications reviennent dans le cours.</p>
    <h2>Pour retrouver les détails</h2><p><a href="https://rolln7drktayau.github.io/courses/embedded-ai/">Présentation et ressources</a> · <a href="https://github.com/rolln7drktayau/courses/blob/main/embedded-ai/HISTORY-AND-ROS.md">Contenu des changements, rééquilibrage et points à vérifier</a> · <a href="https://github.com/rolln7drktayau/courses/blob/main/embedded-ai/SOURCES.md">Bibliographie complète</a>.</p>
    <p>Le rythme doit encore être observé en situation de cours. Les vérifications du support ne remplacent pas l’évaluation de sa compréhension par les étudiants.</p>''')
    css='''@page{size:A4;margin:0}*{box-sizing:border-box}body{margin:0;font:11pt/1.42 "Segoe UI",Arial;color:#18394b}article{width:210mm;height:297mm;padding:18mm 19mm;position:relative;break-after:page;overflow:hidden}article:last-child{break-after:auto}h1{font-size:25pt;line-height:1.12;margin:10px 0 18px}h2{font-size:13pt;margin:17px 0 7px;color:#008b83}p{margin:9px 0}.lead{font-size:14pt;color:#526d7d}.kicker{font-size:9pt;letter-spacing:.08em;text-transform:uppercase;color:#008b83}table{border-collapse:collapse;width:100%;font-size:10pt;margin:14px 0}th,td{text-align:left;padding:7px 6px;border-bottom:1px solid #d4dfe2;vertical-align:top}th{background:#e8f1ef;color:#007d78}.schedule{font-size:9.5pt}.schedule td{padding:8px 5px}.schedule td:nth-last-child(-n+2){white-space:nowrap}.balance{font-size:9pt}.balance td{padding:6px 5px}li{margin:6px 0}footer{position:absolute;bottom:12mm;left:19mm;right:19mm;border-top:1px solid #cbdadd;padding-top:7px;font-size:9pt;color:#5d7581;display:flex;justify-content:space-between}a{color:#00877c}'''
    html='<!doctype html><html lang="fr"><meta charset="utf-8"><title>Plan du cours · Roland Cédric TAYO</title><style>'+css+'</style><body>'+''.join(f'<article>{p}<footer><span>Roland Cédric TAYO · INEM</span><span>{i} / 5</span></footer></article>' for i,p in enumerate(pages,1))+'</body></html>'
    target=root/'source/plan.html';target.write_text(html,encoding='utf-8')
    page.goto(target.as_uri());page.emulate_media(media='print')
    overflow=page.locator('article').evaluate_all('(pages)=>pages.map((p,i)=>({page:i+1,bottom:Math.max(...[...p.children].filter(c=>c.tagName!=="FOOTER").map(c=>c.getBoundingClientRect().bottom)),limit:p.querySelector("footer").getBoundingClientRect().top})).filter(x=>x.bottom>x.limit-6)')
    assert not overflow,overflow
    page.pdf(path=str(root/'course-plan.pdf'),prefer_css_page_size=True,print_background=True)
