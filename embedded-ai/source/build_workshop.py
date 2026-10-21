"""Build the public collaborative workshop, worksheets and student-only download bundle."""
from pathlib import Path
from html import escape
from urllib.parse import urljoin
import re
import csv
import io
import json
import math
import zipfile
import fitz
from playwright.sync_api import sync_playwright
from workshop_content import HALF_DAY, FULL_DAY, MISSIONS, EXIT, SCHEMA

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'workshop'
CHROME=Path(r'C:\Program Files\Google\Chrome\Application\chrome.exe')


def field(name,title,hint='',rows=3):
    return f'<label class="field"><span class="label">{escape(title)}</span><span class="hint">{escape(hint)}</span><textarea name="{name}" rows="{rows}" maxlength="1600"></textarea></label>'


def schedule(rows):
    return '<div class="table-wrap"><table class="schedule"><thead><tr><th>Minutes</th><th>Étape</th><th>Ce que vous faites</th></tr></thead><tbody>'+''.join(f'<tr><td>{start}–{end}</td><td>{escape(title)}</td><td>{escape(task)}</td></tr>' for start,end,title,task in rows)+'</tbody></table></div>'


def build_site():
    OUT.mkdir(exist_ok=True)
    data=json.dumps(dict(schema=SCHEMA,missions=MISSIONS),ensure_ascii=False).replace('<','\\u003c')
    options=''.join(f'<option value="{i}">{i}</option>' for i in range(1,8))
    mission_buttons=''.join(f'<button type="button" class="mission-choice" data-mission="{m["id"]}" aria-pressed="false"><strong>{m["id"]:02d}</strong><span>{escape(m["title"])}</span></button>' for m in MISSIONS)
    evidence=''.join('<tr><td><select name="e'+str(i)+'_kind" aria-label="Nature de la trace '+str(i+1)+'"><option value="">Choisir</option><option>Prévision</option><option>Calcul</option><option>Mesure navigateur</option><option>Mesure PC</option><option>Mesure carte</option><option>Source publiée</option><option>Test de scénario</option></select></td>'+''.join(f'<td><input name="e{i}_{key}" maxlength="500" aria-label="{title} de la trace {i+1}"></td>' for key,title in [('claim','Affirmation'),('value','Valeur ou fichier'),('unit','Unité'),('conditions','Conditions')])+'</tr>' for i in range(3))
    common=field('common_need','Quel service et pourquoi à bord ?','Deux phrases, puis un schéma sur papier. Écrire d’abord sa réponse personnelle.')+field('common_y','Que produit le réseau jouet pour (1,2) ?','Écrire h₁, h₂, ŷ et les étapes. Comparer au support après le calcul.')+field('common_params','Combien de paramètres et de MAC ?','Compter poids et biais séparément ; ne pas confondre ces nombres avec la RAM.')+field('common_ram','Quel pic RAM annonce la carte fictive ?','Tous les objets indiqués sont simultanés. Donner le total, l’unité et l’écart au budget.')
    inquiry=field('prediction','Notre hypothèse avant le test','Ce que l’on prévoit et pourquoi. Une autre réponse doit rester possible.')+field('protocol','Notre protocole','Entrées, référence, variante, conditions maintenues et vérification de correction.')+field('finding','Notre résultat','Préciser la nature : calcul, observation, mesure réelle ou résultat publié.')+field('source','Notre source identifiable','Titre, auteur/organisme, URL et passage utile. Un assistant n’est pas une source de mesure.')+field('limits','Ce que ce résultat ne démontre pas','Une limite et un test qui pourrait remettre notre conclusion en cause.')
    poster=''.join(field(key,title,hint,2) for key,title,hint in [
        ('definition','1. Notre définition','Une phrase simple que toute la classe doit comprendre.'),
        ('mechanism','2. Comment cela fonctionne','Deux phrases ou un schéma à dessiner sur la fiche.'),
        ('proof','3. Notre preuve','Un nombre avec unité, un tableau, un fichier ou un scénario vérifié ; préciser le statut.'),
        ('caution','4. La limite à retenir','La condition qui empêche de généraliser.'),
        ('research','5. La question à poursuivre','Une expérience faisable, pas une promesse de battre un record.')])
    peer=field('review_group','Qui a relu notre fiche ?','G1 relit G2… G7 relit G1 ; noter le groupe et la question posée.',2)+field('objection','L’objection du pair','Ce qui manque pour croire ou reproduire le résultat.',2)+field('revision','Notre réponse et notre révision','Dire précisément ce que l’on a corrigé, ou justifier le désaccord.',2)+field('ai_usage','Usage éventuel d’un assistant','Outil, aide reçue, vérifications effectuées. Chacun doit pouvoir expliquer la fiche.',2)
    synthesis=''.join(f'<tr><th>{m["id"]} · {escape(m["title"])}</th><td><textarea name="takeaway_{m["id"]}" rows="2" maxlength="1600" aria-label="Ce que je retiens du sujet {m["id"]}"></textarea></td></tr>' for m in MISSIONS)
    html=f'''<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="author" content="Roland Cédric TAYO"><meta name="description" content="Atelier guidé : construire ensemble un cours d’IA embarquée par calculs, expériences et recherche en petits groupes."><title>Construire notre cours d’IA embarquée — Roland Cédric TAYO</title><link rel="stylesheet" href="workshop.css"></head><body>
<header class="mast"><div class="wrap"><nav class="topbar"><strong>ROLAND CÉDRIC TAYO / INEM</strong><a href="../">Le support de référence ↗</a></nav><div class="hero"><div><div class="eyebrow">Atelier de conception et d’enquête</div><h1>Le cours, c’est vous<br>qui le construisez.</h1><p>Une question réelle. Des petits groupes. Des preuves que l’on peut discuter. À la fin, vos fiches deviennent notre cours d’IA embarquée.</p><div class="actions"><a class="button" href="#depart">Commencer l’enquête →</a><a class="button secondary" href="protocol.pdf">Lire le protocole PDF</a><a class="button secondary" href="workshop-materials.zip" download>Tout télécharger</a></div></div><div class="hero-card"><div><strong>3 h 30</strong><span>Format recommandé · pause comprise</span></div><hr><div><strong>7 × 5</strong><span>Environ 35 étudiants · 7 enquêtes</span></div><hr><span>Un PC par équipe suffit.<br>Aucun capteur à acheter.<br>Extension possible à 7 heures.</span></div></div></div></header>
<nav class="subnav" aria-label="Étapes de l’atelier"><div class="wrap"><a href="#depart">01 · Le cas</a><a href="#rythme">02 · Le rythme</a><a href="#fiches">03 · Notre fiche</a><a href="#collectif">04 · Notre cours</a><a href="#sortie">05 · Individuellement</a><a href="#ressources">Ressources</a></div></nav>
<main class="wrap"><section class="section" id="depart"><div class="kicker">01 · Une seule situation, des questions complémentaires</div><h2>Faire entrer un calcul utile dans une boîte.</h2><p class="section-lead">Un technicien veut qu’un boîtier estime la prochaine mesure d’un équipement et reste utile sans Internet. Il ne commande aucune action critique. Nous étudions les choix et les limites, sans prétendre valider un produit industriel.</p>
<div class="flow" aria-label="Chaîne du service"><span>Une personne</span><b>→</b><span>Des mesures</span><b>→</b><span>Un modèle</span><b>→</b><span>Un boîtier</span><b>→</b><span>Une décision à vérifier</span></div>
<div class="grid"><article class="card"><h3>Un réseau jouet commun</h3><p>Deux valeurs d’entrée, deux neurones cachés, une sortie. Les biais sont nuls dans les calculs ; ils restent des paramètres.</p><div class="inline-math">h₁ = max(0, x₁ − x₂)<br>h₂ = max(0, 0,5x₁ + 0,5x₂)<br>ŷ = 2h₁ + h₂</div><p class="small">x : entrée · h : activation après ReLU · ŷ : valeur prédite. Ce réseau sert à comprendre ; ce n’est pas le Mixer du TD.</p></article><article class="card"><h3>Une carte mémoire fictive</h3><p>Capacité : <b>128 Kio de RAM</b>. Tous les objets ci-dessous sont présents au même instant.</p><table><tbody><tr><th>État de l’application</th><td>60 Kio</td></tr><tr><th>Acquisition</th><td>32 Kio</td></tr><tr><th>Traitement, réseau inclus</th><td>24 Kio</td></tr><tr><th>Pile</th><td>8 Kio</td></tr><tr><th>Entrées-sorties</th><td>8 Kio</td></tr></tbody></table><p class="small">Les 9 paramètres du jouet sont en Flash FP32, 4 octets chacun. La carte décrit toute l’application, pas uniquement le réseau. 1 Kio = 1 024 octets.</p></article></div>
<div class="notice"><p><b>Pas de faux résultats.</b> Un calcul sur cette carte fictive n’est pas une mesure sur MCU. La somme chronométrée dans le navigateur n’est pas une mesure Raspberry Pi. Le TD prolongera l’enquête avec votre propre code sur une vraie cible.</p></div><p><b>À produire :</b> une fiche de groupe, une trace vérifiable, une relecture et cinq phrases à enseigner. Chacun repart avec une synthèse des sept sujets et répond seul au billet final.</p></section>
<section class="section" id="rythme"><div class="kicker">02 · Le rythme de la demi-journée</div><h2>On cherche, on teste, on se contredit.</h2>{schedule(HALF_DAY)}<div class="grid" style="margin-top:22px"><div class="card"><h3>Des rôles qui tournent</h3><div class="roles"><span>Faciliter</span><span>Chercher</span><span>Calculer / tester</span><span>Contredire</span><span>Rédiger / expliquer</span></div><p class="small" style="margin-top:15px">Changer les rôles entre socle, enquête et restitution. Aucun étudiant ne reste seulement secrétaire. À quatre, regrouper facilitation et rédaction.</p></div><div class="card"><h3>Même contrat pour les sept équipes</h3><p>45 minutes d’enquête ; une hypothèse ; un test ; une source ; un résultat ; une limite ; une objection. Un résumé ou une figure utile suffit pour entrer dans un article.</p><p class="small">Ne pas répartir seulement les tâches : tous doivent comprendre le socle et pouvoir expliquer le résultat de leur groupe.</p></div></div><details><summary>Extension à une journée de 7 heures</summary><p>La matinée reste identique. L’après-midi sert à écrire un petit calcul, le tester et étudier une variante. Elle ne prétend pas faire réaliser tout le projet de décembre en une journée.</p>{schedule(FULL_DAY)}<p class="small">Si la carte n’est pas prête, conclure honnêtement sur PC et écrire le protocole de transfert restant à faire. Une cible partagée peut être réservée par créneaux ; aucune comparaison entre PC différents n’est un classement d’optimisations.</p></details></section>
<section class="section" id="fiches"><div class="kicker">03 · Un carnet de groupe</div><h2>Écrire ce que l’on pense, puis ce que l’on constate.</h2><p class="section-lead">D’abord, chaque personne tente le socle pendant trois minutes. Ensuite, le groupe confronte ses réponses et consulte les diapositives utiles. La fiche reste modifiable après relecture.</p>
<div class="controls"><label><span class="label">Notre groupe</span><select id="group">{options}</select></label><label><span class="label">Notre mission</span><select id="mission">{options}</select></label></div>
<form id="notebook" autocomplete="off"><div class="controls"><label class="wide"><span class="label">Séance commune à la classe</span><input name="session" maxlength="80" value="INEM-2026-2027"></label><label class="wide"><span class="label">Équipe ou pseudonymes</span><input name="team" maxlength="200"></label></div>{field('roles','Répartition puis rotation des rôles','Noter les initiales ou pseudonymes, sans donnée personnelle inutile.',2)}
<details open><summary>Socle commun à tous les groupes · 30 minutes</summary>{common}<p><a href="../index.html#slide=7" target="_blank" rel="noopener noreferrer">Vérifier le calcul dans le support, après votre essai ↗</a></p></details>
<div class="mission-choices" aria-label="Choisir une enquête">{mission_buttons}</div><article class="card mission-detail" id="mission-detail"><div class="mission-tag" id="mission-concept"></div><h3 id="mission-title"></h3><p id="mission-question"></p><p class="small" id="assigned-note"></p><ol class="steps" id="mission-tasks"></ol><div class="teaching-output"><b>Production attendue</b><p id="mission-expected"></p><p class="small" id="mission-table"></p></div><details><summary>Lectures et diapositives utiles</summary><ul class="link-list" id="mission-links"></ul></details><a class="button secondary" id="mission-pdf" href="group-01.pdf">Fiche de cette mission · PDF</a></article>
<div class="grid"><div>{inquiry}</div><div><h3 style="margin-top:25px">Notre morceau de cours</h3><p class="small">Une phrase ou deux par champ. Ces cinq éléments deviennent votre chapitre dans la synthèse collective.</p>{poster}</div></div>
<h3>Nos traces et leurs conditions</h3><div class="evidence-types"><b>Prévu</b><b>Calculé</b><b>Mesuré</b><b>Lu dans une source</b></div><div class="table-wrap" style="margin-top:15px"><table class="evidence"><thead><tr><th>Nature</th><th>Affirmation</th><th>Valeur / fichier</th><th>Unité</th><th>Conditions</th></tr></thead><tbody>{evidence}</tbody></table></div>
<details><summary>Relecture obligatoire · 25 minutes</summary><p>Le groupe précédent relit votre fiche ; vous relisez le suivant (G7 relit G1). Vérifier une affirmation précise et la trace qui la soutient, puis répondre à une objection.</p>{peer}</details>
<details><summary>Notre synthèse des sept sujets · à remplir pendant les restitutions</summary><p>Une idée, une preuve et une limite par sujet. Cette étape évite de n’apprendre que sa propre mission.</p><table><thead><tr><th>Sujet</th><th>Ce que nous retenons</th></tr></thead><tbody>{synthesis}</tbody></table></details></form>
<div class="progress-track"><i id="progress-fill"></i></div><p class="small" id="progress-label"></p><p class="save-state" id="save-state" role="status"></p><div class="toolbar"><button class="button" id="export-json">Exporter notre fiche JSON</button><button class="button secondary" id="export-md">Exporter en Markdown</button><label class="file-button button secondary">Reprendre une fiche <input id="import-own" type="file" accept=".json,application/json"></label></div><p class="small">Le navigateur conserve un brouillon par groupe. Il n’y a pas de synchronisation entre machines. Exportez, puis échangez vos fichiers par le dépôt de classe ou le canal annoncé.</p></section>
<section class="section" id="collectif"><div class="kicker">04 · Assembler les preuves, pas seulement les textes</div><h2>Notre cours construit ensemble.</h2><p class="section-lead">Réunir les sept JSON, vérifier les objections, puis relire ensemble la synthèse. Importer ne valide ni une affirmation ni une mesure. Un nouveau fichier du même groupe remplace sa fiche dans cette synthèse.</p><p class="small">Les imports collectifs restent en mémoire sur cette page : exporter la synthèse avant de fermer ou recharger. Les JSON originaux restent vos traces.</p><div class="toolbar"><label class="file-button button">Importer les fiches des groupes <input id="import-class" type="file" multiple accept=".json,application/json"></label><button class="button secondary" id="export-course-html">Exporter notre cours HTML</button><button class="button secondary" id="export-course-md">Exporter notre cours Markdown</button><button class="button secondary" id="print-course">Imprimer / PDF de la synthèse</button></div><p class="save-state" id="file-status" role="status"></p><p id="collective-status" class="notice"></p><div class="collective-list" id="collective-chapters"></div></section>
<section class="section" id="sortie"><div class="kicker">05 · Chacun sait-il expliquer ?</div><h2>Quinze minutes, individuellement.</h2><p class="section-lead">Sans fiche, sans échange, sans assistant. Le billet vérifie la compréhension ; il ne cherche pas une formulation apprise par cœur.</p><ol class="exit-questions">{''.join('<li>'+escape(question)+'</li>' for _,question in EXIT)}</ol><a class="button secondary" href="individual-check.pdf">Billet individuel à imprimer</a><details><summary>Si la séance est notée : proposition de barème sur 20</summary><p><b>Collectif : 12 points.</b> Socle expliqué 4 ; preuves et sources 4 ; chapitre clair 2 ; objection et révision 2.</p><p><b>Individuel : 8 points.</b> Les cinq questions valent respectivement 2, 2, 2, 1 et 1 points. La note n’augmente pas parce que le résultat est positif.</p><p class="small">Barème à annoncer avant la séance. Cet atelier ne modifie pas le barème du projet : son éventuel poids dans le module est fixé séparément.</p></details></section>
<section class="section" id="ressources"><div class="kicker">Des outils au service de la question</div><h2>Tout pour commencer, rien à installer pour la demi-journée.</h2><div class="download-grid"><a href="workshop-materials.zip" download>Dossier complet<small>Page, PDF, données illustratives, gabarits et support de référence pour lecture hors ligne.</small></a><a href="protocol.pdf">Protocole académique<small>Objectifs, déroulement, attentes, journée longue et évaluation.</small></a><a href="worksheets.pdf">Les dix fiches papier<small>Socle, sept missions, synthèse et billet individuel.</small></a><a href="data/toy-series.csv" download>Les signaux illustratifs<small>Trois séquences A/B/C pour étudier le fenêtrage. Ce ne sont pas les données du TD.</small></a><a href="repository-template.zip" download>Structure du dépôt étudiant<small>Dossiers, consignes de tests et CI de format ; aucun réseau résolu.</small></a><a href="../lab/">Le projet et son énoncé<small>Écrire, entraîner et optimiser son Mixer ; prolonger l’enquête sur une vraie cible.</small></a></div>
<details><summary>Versionner la recherche, sans transformer la séance en installation</summary><p>Pour la demi-journée, le navigateur et un éditeur ou tableur suffisent. Si Git est prêt, créer le dépôt de groupe et inviter <b>rolln7drktayau</b>. Sinon, conserver les exports et les déposer au jalon convenu ; les commandes Git ne doivent pas prendre la place de l’enquête.</p><pre>docs: record initial hypothesis\nexperiment: add raw observations and conditions\nreview: record peer objection\ndocs: revise conclusion and next test</pre><p>Chaque jalon doit correspondre à une vraie modification. Préférer anglais pour noms, code, commentaires et messages de commit. Le dépôt de classe reçoit les fiches par pull request ; aucun accès à un dépôt extérieur n’est accordé automatiquement.</p></details>
<details><summary>Pourquoi cette méthode ? Sources pédagogiques et limites</summary><p>Une enquête guidée, une relecture et une responsabilité individuelle sont retenues ici. Ce n’est pas une recherche libre sans critères, ni une garantie d’efficacité pour chaque classe.</p><ul class="source-list"><li><a href="https://doi.org/10.1073/pnas.1319030111" target="_blank" rel="noopener noreferrer">Freeman et al., 2014 — synthèse de recherches sur l’apprentissage actif en sciences et ingénierie.</a></li><li><a href="https://teaching.cornell.edu/resource/getting-started-designing-group-work-assignments" target="_blank" rel="noopener noreferrer">Cornell — aligner objectifs, étapes, durée et retour collectif.</a></li><li><a href="https://www.cmu.edu/teaching/designteach/inclusiveexcellence/groupwork/index.html" target="_blank" rel="noopener noreferrer">Carnegie Mellon — petits groupes, rôles tournants et participation.</a></li></ul><p>Le support de référence et ses sources scientifiques restent disponibles. Aucun corrigé du projet, poids entraîné ou résultat de carte n’est fourni dans cet atelier.</p></details></section></main><footer><div class="wrap">Roland Cédric TAYO · INEM · Atelier d’IA pour les systèmes embarqués · <a href="../">Support de référence</a> · <a href="https://github.com/rolln7drktayau/courses/tree/main/embedded-ai/workshop">Sources de l’atelier</a></div></footer><script id="workshop-data" type="application/json">{data}</script><script src="workshop.js"></script></body></html>'''
    (OUT/'index.html').write_text(html,encoding='utf-8')


DOC_CSS='''@page{size:A4;margin:17mm 20mm}*{box-sizing:border-box}body{margin:0;color:#18394b;font:10.2pt/1.4 Georgia,'Times New Roman',serif}.page{height:263mm;display:flex;flex-direction:column;break-after:page}.page:last-child{break-after:auto}.kicker{font:8pt Arial,sans-serif;color:#0b7d76;text-transform:uppercase;letter-spacing:1px;border-bottom:1px solid #cddde2;padding-bottom:9px}h1{font-size:23pt;line-height:1.13;font-weight:normal;margin:18px 0 12px}h2{font-size:12pt;margin:16px 0 7px}h3{font-size:10.7pt;margin:11px 0 6px}p{margin:5px 0 10px}li{margin:5px 0}ol,ul{padding-left:20px}table{border-collapse:collapse;width:100%;font-size:9pt;margin:9px 0}th,td{text-align:left;vertical-align:top;padding:7px 6px;border-bottom:1px solid #d1dee3}th{background:#edf4f3}.small{font-size:8.7pt;color:#5e7682;line-height:1.35}.footer{margin-top:auto;border-top:1px solid #ccdbe0;padding-top:8px;color:#607783;font-size:8pt}.box{border:1px solid #bacfd5;padding:11px 13px;margin:9px 0;min-height:23mm;border-radius:3px}.blank{min-height:26mm}.line{height:7mm;border-bottom:1px solid #c8d7de}.math{font-size:12pt;line-height:1.6;background:#edf5f2;padding:11px}a{color:#087b76;text-decoration:none;overflow-wrap:anywhere}.compact td,.compact th{padding:5px 6px}.mission-tasks{font-size:9.8pt}.note{border-left:3px solid #0c867d;padding:6px 11px;background:#f0f6f4}.identity{font:9pt Arial,sans-serif;margin:10px 0}pre{font:8.4pt/1.4 Consolas,monospace;background:#eff4f6;padding:10px;white-space:pre-wrap}.worksheet h1{font-size:20pt}.worksheet .footer{font-size:8pt}caption{text-align:left;font-weight:bold;margin-bottom:5px}'''


def page(title,body,number,total,kicker='INEM · Atelier d’IA embarquée',cls=''):
    return f'<article class="page {cls}"><div class="kicker">{kicker}</div><h1>{title}</h1>{body}<div class="footer">Roland Cédric TAYO · {number} / {total}</div></article>'


def document(body,title):
    body=re.sub(r'href="([^"]+)"',lambda m:'href="'+escape(urljoin('https://rolln7drktayau.github.io/courses/embedded-ai/workshop/',m.group(1)),quote=True)+'"',body)
    return f'<!doctype html><html lang="fr"><meta charset="utf-8"><meta name="author" content="Roland Cédric TAYO"><title>{escape(title)}</title><style>{DOC_CSS}</style><body>{body}</body></html>'


def build_documents(browser):
    base='<p class="identity">Groupe : ________ &nbsp; Séance : __________ &nbsp; Équipe : _______________________</p>'
    protocol=[]
    body='''<p><b>Conception, recherche guidée et enseignement entre pairs.</b><br>Demi-journée recommandée : 3 h 30 ; extension : 7 h hors déjeuner. Environ 35 étudiants : sept groupes de cinq.</p><h2>Résumé</h2><p>Chaque équipe contribue à un cours commun à partir d’une enquête courte. Tous traitent un socle, puis une mission complémentaire, font relire leur preuve et enseignent ce qu’ils ont compris. Le cours final rassemble définitions, résultats, sources, limites et questions ouvertes.</p><h2>Le besoin</h2><p>Un technicien veut qu’un boîtier estime la prochaine mesure d’un équipement sans dépendre d’Internet. Les données sont illustratives ; aucune action critique ni application industrielle validée n’est annoncée.</p><div class="math">h₁ = max(0, x₁ − x₂)<br>h₂ = max(0, 0,5x₁ + 0,5x₂)<br>ŷ = 2h₁ + h₂</div><p class="small">x : entrée ; h : activation ; ŷ : prédiction. Les biais valent zéro dans les calculs. Ce réseau 2 → 2 → 1 sert de modèle jouet ; ce n’est pas le Mixer du projet.</p><h2>Acquis observables</h2><ul><li>Justifier un service et le lieu du calcul.</li><li>Expliquer une sortie, des paramètres et une correction d’apprentissage.</li><li>Compter une mémoire et distinguer calcul, mesure et résultat publié.</li><li>Formuler une hypothèse, la confronter à une preuve et expliquer sa limite.</li><li>Faire une relecture et construire une synthèse que d’autres peuvent comprendre.</li></ul><h2>Matériel</h2><p>Au moins un ordinateur avec navigateur par équipe ; papier et crayon ; connexion pour consulter les sources, ou dossier téléchargé à l’avance. Aucun capteur, GPU, compte payant ni environnement d’apprentissage n’est requis pour la demi-journée.</p><p class="note">Cette séance remplace une partie du module ; elle ne s’ajoute pas automatiquement aux 28 heures. Le projet et les tests sur cible prolongent le travail.</p>'''
    protocol.append(page('Construire ensemble<br>notre cours d’IA embarquée',body,1,5))
    rows=''.join(f'<tr><td>{a}–{b}</td><td>{escape(t)}</td><td>{escape(d)}</td></tr>' for a,b,t,d in HALF_DAY)
    body=f'''<table class="compact"><thead><tr><th>Min.</th><th>Étape</th><th>Action</th></tr></thead><tbody>{rows}</tbody></table><h2>Organisation</h2><p>Former des équipes aux compétences complémentaires. Faire tourner facilitation, recherche, calcul/test, critique et rédaction/explication. À quatre, fusionner facilitation et rédaction. Les rôles ne dispensent personne de comprendre.</p><h2>Relecture</h2><p>G1 relit G2, G2 relit G3… G7 relit G1. Vérifier une affirmation précise, demander sa trace et formuler une objection. La fiche doit montrer la réponse et la révision, pas seulement « relu ».</p><h2>Restitutions</h2><p>Chaque groupe dispose de 4 min : définition, mécanisme, preuve, limite, prochaine question. La classe prend ensuite 1 min pour compléter sa ligne de synthèse. Total : 7 × 5 = 35 min.</p><p class="note">Une difficulté peut être signalée sans attendre la fin. L’enseignant circule, questionne et valide les points essentiels ; aucun exposé de trois heures n’est nécessaire.</p>'''
    protocol.append(page('Le déroulement<br>de la demi-journée',body,2,5))
    rows=''.join(f'<tr><th>{m["id"]} · {escape(m["title"])}</th><td>{escape(m["expected"])}</td></tr>' for m in MISSIONS)
    body=f'''<p>Tous commencent par le socle ; chaque groupe mène ensuite sa mission pendant 45 min. Lire d’abord le résumé, une figure ou le passage utile de la source ; une revue complète de littérature n’est pas attendue.</p><table><thead><tr><th>Mission</th><th>Production équivalente</th></tr></thead><tbody>{rows}</tbody></table><h2>Le même contrat d’enquête</h2><p>Une hypothèse écrite avant le test ; un protocole ; une trace ; une source ; une limite ; une objection ; cinq phrases à enseigner. L’absence de gain est un résultat recevable.</p><h2>Nature des résultats</h2><p>Étiqueter « calcul », « mesure navigateur », « mesure PC », « mesure carte », « test de scénario » ou « source publiée ». Une taille théorique n’est pas un pic RAM mesuré. Un chronométrage du navigateur ne prouve rien sur une carte non testée.</p><p>Fiches détaillées : une page par mission dans <a href="worksheets.pdf">worksheets.pdf</a>, ou group-01.pdf à group-07.pdf. Les équations ne constituent pas un corrigé du TD.</p>'''
    protocol.append(page('Sept contributions<br>à un même cours',body,3,5))
    body='''<h2>Livrables de la demi-journée</h2><ol><li>Une fiche de groupe JSON et sa version Markdown, ou les fiches papier complétées.</li><li>Les traces associées : calculs, schéma, CSV réel si la mission en comporte, source et conditions.</li><li>Une objection et une révision ; la synthèse des sept restitutions.</li><li>Un billet individuel de cinq questions, réalisé sans support.</li></ol><h2>Assembler le cours</h2><p>La page permet d’importer les sept JSON et d’exporter une synthèse HTML ou Markdown, imprimable en PDF. Les imports sont des déclarations, pas des résultats certifiés. Relire la synthèse en séance avant de la diffuser comme cours.</p><p>La sauvegarde est locale au navigateur. Exporter avant de changer de machine. Pour échanger, utiliser le dépôt ou le canal annoncé ; aucune collaboration en temps réel n’est simulée.</p><h2>Versionnement</h2><p>Si Git est prêt, créer le dépôt étudiant, inviter rolln7drktayau et conserver quatre jalons : hypothèse, observations, objection, révision. Sinon, garder les exports puis les déposer au jalon convenu. Préférer des noms, commentaires et messages de commit en anglais.</p><pre>docs: record initial hypothesis\nexperiment: add raw observations and conditions\nreview: record peer objection\ndocs: revise conclusion and next test</pre><h2>Compréhension et assistance</h2><p>Une source ou un assistant peut aider pendant l’enquête si l’usage est déclaré et vérifié. Le billet individuel se fait sans aide. Chacun doit pouvoir recalculer un exemple et expliquer une trace ; aucun dispositif ne garantit à lui seul l’absence de fraude.</p><h2>Barème proposé, si la séance est notée</h2><p>Collectif 12 points : socle 4, preuves/sources 4, chapitre clair 2, relecture/révision 2. Individuel 8 points : 2 + 2 + 2 + 1 + 1. Annoncer le coefficient avant la séance ; le barème du projet reste distinct.</p>'''
    protocol.append(page('Rendre la pensée<br>et les preuves visibles',body,4,5))
    rows=''.join(f'<tr><td>{a}–{b}</td><td>{escape(t)}</td><td>{escape(d)}</td></tr>' for a,b,t,d in FULL_DAY)
    body=f'''<p>La matinée est inchangée. L’après-midi ajoute une expérience programmée sur le réseau jouet, pas la réalisation complète du Mixer.</p><table class="compact"><thead><tr><th>Min.</th><th>Étape</th><th>Action</th></tr></thead><tbody>{rows}</tbody></table><h2>Transfert sur cible, si la cible est prête</h2><p>Sur un Pi Linux, transférer les sources puis compiler ou installer sur le Pi avec son outil. Ne pas exécuter un binaire PC x86 comme s’il était ARM. Sur microcontrôleur, utiliser la chaîne et la procédure de flash de la carte identifiée. Si la cible manque ou n’est pas prête, rapporter uniquement les mesures PC.</p><h2>Où lire</h2><p><a href="https://rolln7drktayau.github.io/courses/embedded-ai/workshop/">Page de l’atelier</a> · <a href="../index.html">support de référence</a> · <a href="../lab/">énoncé du projet</a>. Les sources de chaque mission sont liées dans la page et dans sa fiche. Documentation : <a href="https://git-scm.com/downloads/">Git</a>, <a href="https://www.python.org/downloads/">Python si choisi</a>, <a href="https://www.raspberrypi.com/documentation/computers/remote-access.html">transfert et accès Pi</a>.</p><p class="small">Conception inspirée des recommandations Cornell et Carnegie Mellon sur le travail de groupe et de Freeman et al. (2014), DOI 10.1073/pnas.1319030111. Ces travaux ne garantissent pas l’efficacité de chaque séance ; le billet individuel et les difficultés observées servent à l’améliorer.</p>'''
    protocol.append(page('Prolonger en une journée<br>sans promettre l’impossible',body,5,5))
    (OUT/'protocol.html').write_text(document(''.join(protocol),'Protocole — Atelier IA embarquée'),encoding='utf-8')

    sheets=[]
    body=base+'''<p>Avant les ressources : trois minutes de réponse personnelle. Puis confronter, calculer et vérifier ensemble.</p><h2>1. Le service et son lieu</h2><div class="box blank">Pour qui ? Pour quoi ? Quelle fonction doit rester disponible sans Internet ?<br>Schéma : personne → données → calcul → service.</div><h2>2. Le réseau jouet</h2><div class="math">h₁ = max(0, x₁ − x₂) ; h₂ = max(0, 0,5x₁ + 0,5x₂) ; ŷ = 2h₁ + h₂.</div><div class="box blank">Pour (1,2) : étapes, h₁, h₂, ŷ.<br>Poids : ____ &nbsp; Biais : ____ &nbsp; Paramètres : ____ &nbsp; MAC, biais exclus : ____</div><h2>3. Le pic RAM fictif</h2><p>Capacité 128 Kio ; objets simultanés : application 60, acquisition 32, traitement réseau inclus 24, pile 8, entrées-sorties 8 Kio. Les 9 paramètres FP32 sont en Flash.</p><div class="box blank">Total RAM : __________ &nbsp; Écart : __________<br>Ce qui est calculé ; ce qui reste à mesurer sur une vraie carte :</div><h2>4. Une limite que nous avons identifiée</h2><div class="line"></div><div class="line"></div>'''
    sheets.append(page('Le socle de toute la classe',body,1,10,cls='worksheet'))
    for m in MISSIONS:
        body=base+f'<p><b>Question :</b> {escape(m["question"])}</p><ol class="mission-tasks">'+''.join('<li>'+escape(t)+'</li>' for t in m['tasks'])+'</ol>'
        body+=f'<p class="small"><b>Source :</b> <a href="{m["source"][1]}">{escape(m["source"][0])}</a> · <a href="{m["extra"][1]}">{escape(m["extra"][0])}</a>.</p>'
        body+='<div class="box"><b>Notre hypothèse avant test</b><div class="line"></div></div><p class="small">Tableau conseillé : '+escape(m['table'])+'</p>'
        body+='<table><thead><tr><th>Trace / résultat / unité</th><th>Nature et conditions</th><th>Ce que cela permet de dire</th></tr></thead><tbody>'+''.join('<tr><td style="height:12mm"></td><td></td><td></td></tr>' for _ in range(3))+'</tbody></table>'
        body+='<div class="box"><b>Notre phrase à enseigner, sa limite et la prochaine question</b><div class="line"></div><div class="line"></div></div><p>Groupe relecteur : ____ &nbsp; Objection / révision : __________________________</p>'
        sheets.append(page(f'{m["id"]}. {escape(m["title"])}',body,m['id']+1,10,cls='worksheet'))
    body=base+'<p>Pendant chaque restitution : une idée, une preuve et une limite. Tout le monde doit comprendre les sept sujets.</p><table><thead><tr><th>Sujet</th><th>Définition / idée</th><th>Preuve / source</th><th>Limite / question</th></tr></thead><tbody>'+''.join(f'<tr style="height:23mm"><th>{m["id"]}. {escape(m["title"])}</th><td></td><td></td><td></td></tr>' for m in MISSIONS)+'</tbody></table><p class="note">Avant partage : vérifier les unités, les conditions, les objections et la nature des résultats. La synthèse reste provisoire tant qu’elle n’a pas été relue en séance.</p>'
    sheets.append(page('Notre synthèse collective',body,9,10,cls='worksheet'))
    body='<p class="identity">Identifiant : __________________ &nbsp; Groupe : ____ &nbsp; Séance : __________</p><p><b>15 minutes. Sans support ni assistant.</b> Expliquer les étapes compte davantage qu’une réponse isolée.</p>'
    for points,question in EXIT:
        body+=f'<h3>{escape(points)} · {escape(question)}</h3><div class="line"></div><div class="line"></div>'
    body+='<p class="small">Une incompréhension repérée ici indique ce qu’il faut reprendre pendant le module ; elle ne doit pas être masquée par le résultat collectif.</p>'
    sheets.append(page('Ce que je peux expliquer seul',body,10,10,cls='worksheet'))
    (OUT/'worksheets.html').write_text(document(''.join(sheets),'Fiches — Atelier IA embarquée'),encoding='utf-8')
    page_browser=browser.new_page()
    for name,count in [('protocol',5),('worksheets',10)]:
        page_browser.goto((OUT/(name+'.html')).as_uri())
        page_browser.pdf(path=str(OUT/(name+'.pdf')),prefer_css_page_size=True,print_background=True)
        with fitz.open(OUT/(name+'.pdf')) as doc:
            if len(doc)!=count:raise AssertionError((name,'page overflow',len(doc),count))
            doc.set_metadata({'title':name+' — Atelier IA embarquée','author':'Roland Cédric TAYO'})
            target=OUT/(name+'.pdf');temporary=OUT/(name+'.metadata.pdf')
            doc.save(temporary,garbage=4,deflate=True)
        temporary.replace(target)
    with fitz.open(OUT/'worksheets.pdf') as full:
        for i in range(7):
            one=fitz.open();one.insert_pdf(full,from_page=i+1,to_page=i+1);one.set_metadata({'author':'Roland Cédric TAYO','title':MISSIONS[i]['title']});one.save(OUT/f'group-{i+1:02d}.pdf');one.close()
        one=fitz.open();one.insert_pdf(full,from_page=9,to_page=9);one.set_metadata({'author':'Roland Cédric TAYO','title':'Billet individuel'});one.save(OUT/'individual-check.pdf');one.close()
    page_browser.close()


def build_data_and_repository():
    (OUT/'data').mkdir(exist_ok=True)
    with (OUT/'data'/'toy-series.csv').open('w',encoding='utf-8',newline='') as stream:
        writer=csv.writer(stream);writer.writerow(['sequence','t','value'])
        for k,name in enumerate('ABC'):
            for t in range(24):writer.writerow([name,t,f'{math.sin(2*math.pi*t/12+k*.3)+.1*math.cos(t*.7):.6f}'])
    (OUT/'data'/'experiment-template.csv').write_text('experiment,group,claim,kind,variant,value,unit,conditions,raw_file,commit\n',encoding='utf-8')
    template={
        'README.md':'''# Student inquiry repository

Invite the teacher account **rolln7drktayau**. This is a blank evidence structure, not a solved network.
Place exported group JSON files in `submissions/`, raw CSV in `raw/`, plots in `figures/` and source code in `src/` if doing the full-day extension. Keep an experiment manifest in `experiments/`.

Milestones: `docs: record initial hypothesis`, `experiment: add raw observations and conditions`, `review: record peer objection`, `docs: revise conclusion and next test`.

Write numerical tests and inference yourself. Prefer English names, comments and commit messages. Required tests for a coded experiment: hand-calculated nominal input, zero input, varied input, reference/variant equivalence with a justified tolerance. Add `python -m unittest discover -s tests -v` or your language's test command to CI once real tests exist. The supplied CI validates JSON structure only; it does not validate scientific conclusions, timings or device safety.

Run the provided format check with `python tools/check_evidence.py`. It permits an empty initial repository and does not grade answers. A useful final submission must also contain evidence, sources, peer criticism and limitations. Do not commit private identifiers or invent data. The class repository can assemble the Markdown/HTML after human review.
''',
        '.gitignore':'__pycache__/\n*.pyc\n.venv/\n',
        '.github/workflows/evidence.yml':'''name: Check evidence format
on: [push, pull_request]
permissions:
  contents: read
jobs:
  format:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v7
      - uses: actions/setup-python@v7
        with:
          python-version: '3.13'
      - run: python tools/check_evidence.py
''',
        '.github/pull_request_template.md':'## Question and claim\n\n## Evidence and conditions\n\n## Checks performed\n\n## Peer objection and revision\n\n## Limits and next test\n',
        'tools/check_evidence.py':'''"""Check exported inquiry-file structure; never grade the scientific answer."""
from pathlib import Path
import json

files=list(Path('submissions').glob('*.json'))
for path in files:
    data=json.loads(path.read_text(encoding='utf-8'))
    assert data.get('schema')=='inem-embedded-ai-workshop/1', path
    assert type(data.get('group')) is int and 1<=data['group']<=7, path
    assert type(data.get('mission')) is int and 1<=data['mission']<=7, path
    assert isinstance(data.get('fields'),dict), path
    assert all(isinstance(k,str) and isinstance(v,str) and len(v)<=2000 for k,v in data['fields'].items()), path
print(f'Format checked: {len(files)} file(s). Scientific content and device performance require human review.')
''',
        'experiments/manifest-template.json':json.dumps(dict(question='',hypothesis='',commit='',platform='',toolchain='',options='',input_file='',weights='',correctness_check='',timer='',repetitions='',raw_files=[],limitations=''),indent=2)+'\n',
        'tests/README.md':'Write meaningful numerical and equivalence tests for your implementation. No model implementation or expected TD solution is supplied here.\n',
        'src/README.md':'Your code goes here for the full-day experiment or the later project.\n',
        'raw/README.md':'Unedited observations, with units and conditions. Browser observations are not MCU measurements.\n',
        'figures/README.md':'Figures generated from identified raw files; label illustrative data explicitly.\n',
        'submissions/README.md':'Place your exported group-01.json ... group-07.json here.\n'
    }
    with zipfile.ZipFile(OUT/'repository-template.zip','w',zipfile.ZIP_DEFLATED) as archive:
        for name,text in template.items():archive.writestr(name,text)




def package():
    files=[p for p in OUT.rglob('*') if p.is_file() and p.name!='workshop-materials.zip' and p.suffix not in {'.png','.pyc'}]
    with zipfile.ZipFile(OUT/'workshop-materials.zip','w',zipfile.ZIP_DEFLATED) as archive:
        for path in files:archive.write(path,'embedded-ai/workshop/'+path.relative_to(OUT).as_posix())
        for name in ['index.html','course.pdf','course-plan.pdf']:
            archive.write(ROOT/name,'embedded-ai/'+name)
        archive.writestr('README.txt','Open embedded-ai/workshop/index.html. No installation is required. Local drafts are not synchronised; export JSON. Online source links need Internet.\n')
    with zipfile.ZipFile(OUT/'workshop-materials.zip') as archive:
        assert archive.testzip() is None
        assert not any('guide-animation' in name or 'Resolution_Enseignant' in name for name in archive.namelist())


def main():
    build_site();build_data_and_repository()
    with sync_playwright() as p:
        browser=p.chromium.launch(executable_path=str(CHROME) if CHROME.exists() else None,headless=True)
        build_documents(browser);browser.close()
    package()
    print(json.dumps({'workshop':'3h30 / optional 7h','teams':7,'protocol_pages':5,'worksheet_pages':10,'package_bytes':(OUT/'workshop-materials.zip').stat().st_size}))


if __name__=='__main__':main()
