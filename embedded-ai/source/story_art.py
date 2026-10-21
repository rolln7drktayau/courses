"""Fictional scenes, paired with independently labelled engineering diagrams.

The illustrations never represent measured results or portraits of researchers.
All labels and quantitative explanations remain editable text and SVG.
"""
from html import escape


def fragment(step,body):
    return f'<g class="fragment" data-step="{step}">{body}</g>'


def picture(panel,label):
    x=(panel%3)*50;y=(panel//3)*100
    return f'<div class="scene-picture" role="img" aria-label="{escape(label,quote=True)}" style="background-position:{x}% {y}%"></div>'


def stage(panel,label,caption='',extra=''):
    return '<figure class="story-stage">'+picture(panel,label)+extra+(f'<figcaption>{caption}</figcaption>' if caption else '')+'</figure>'


def draw_story(name):
    from diagrams import text,rect,arrow,circle,path,cells,svg,TEAL,INK,MUTED,GOLD
    def year(label,subtitle):
        return text(35,46,label,31,INK,'start',650)+text(35,83,subtitle,21,MUTED,'start')

    if name=='story_cover':
        return stage(0,'Alice près de sa lampe, chez elle.')
    if name=='story_request':
        return stage(0,'Alice porte un carton près de sa lampe.',
                     'Un bouton fonctionne. La voix pourrait rendre un autre service.',
                     '<div class="spoken fragment" data-step="1">« Lumière, s’il te plaît ! »</div>')
    if name=='story_voices':
        return stage(1,'Alice et deux amis essaient une commande vocale.',
                     'Trois personnes. Un même mot. Des sons différents.',
                     '<div class="scene-label fragment" data-step="2">Le modèle reçoit des nombres, pas des mots écrits.</div>')
    if name in {'story_remote','story_outage'}:
        offline=name=='story_outage'
        flow=svg(text(65,65,'Micro',23)+arrow(110,60,195,60)+text(275,65,'Serveur',23)+arrow(352,60,435,60)+text(505,65,'Lampe',23),'Trajet logique de la commande')
        flow=flow.replace('viewBox="0 0 760 500"','viewBox="0 0 600 110"')
        return ('<div class="visual-stack network-stack"><div class="network-scene '+('offline' if offline else 'online')+'">'
                +'<div class="when-online">'+picture(1,'La commande est essayée lorsque la liaison est disponible.')+'</div>'
                +'<div class="when-offline">'+picture(3,'Alice attend une réponse alors que la liaison manque.')+'</div>'
                +'<div class="network-route">'+flow+'</div><div class="remote-reply">La réponse peut revenir.</div>'
                +'<div class="link-failure">Pas de liaison → pas de réponse distante.</div></div>'
                +'<button class="demo-button" data-action="network-toggle">'+('Rétablir la liaison' if offline else 'Couper la liaison')+'</button>'
                +'<span class="scene-caption">Le bouton change le schéma. Il ne contacte aucun serveur.</span></div>')
    if name=='story_pause':
        return stage(4,'Alice prépare la carte sur son établi.','Après la pause : comment le faire tenir et fonctionner ?')
    if name=='story_epilogue':
        return stage(5,'Alice explique son travail à deux camarades.','Reprenez les quatre questions du départ : vos réponses ont-elles changé ?')
    if name=='story_robustness':
        return stage(1,'Des personnes différentes utilisent la commande.',
                     'Essayer d’autres personnes, d’autres bruits, d’autres conditions.',
                     '<div class="scene-label fragment" data-step="2">Et si le modèle hésite ?</div>')
    if name=='story_memory_wait':
        z=year('Le calcul n’est pas seul.','Il faut déplacer les nombres.')
        z+=rect(65,150,180,120,'#fff1e8','#ffc6b1',5)+text(155,218,'Processeur',24)
        z+=rect(505,150,180,120,'#e5f5f3','#9cd6cf',5)+text(595,218,'Mémoire',24)
        z+=fragment(1,arrow(492,182,258,182)+text(375,155,'Lire les données',22,TEAL))
        z+=fragment(2,arrow(258,244,492,244)+text(375,300,'Écrire les résultats',22,TEAL))
        z+=fragment(3,text(375,382,'Lire une fois, réutiliser plusieurs fois ?',27,INK)+text(375,430,'Une piste à tester, selon les données et le matériel.',21,MUTED))
        return svg(z,'Échanges entre processeur et mémoire')
    if name=='story_energy':
        z=year('La batterie paie toute la chaîne.','Écoute + calcul + échanges + veille')
        z+=rect(245,130,270,125,'white',INK,10)+rect(515,167,19,48,INK,INK,3)
        for i,c in enumerate(['#ff926b','#f4c751','#7ecdc0']):z+=rect(262+82*i,146,66,93,c,c,4)
        for i,(label,sub) in enumerate([('Écouter','Micro et acquisition'),('Calculer','Modèle et mémoire'),('Échanger','Radio et réseau')]):
            body=circle(130+i*250,349,27,str(i+1),fill='#fff6de',color=GOLD)+text(130+i*250,405,label,25,INK)+text(130+i*250,443,sub,19,MUTED)
            z+=fragment(i+1,body)
        return svg(z,'Les postes de consommation')
    if name=='story_shakey':
        return ('<figure class="history-stage"><div class="history-picture history-shakey" role="img" '
                'aria-label="Reconstitution illustrée : Shakey, ses roues, sa caméra et un ordinateur de laboratoire."></div>'
                '<figcaption><span class="fragment" data-step="1">Le robot observe et agit.</span> '
                '<span class="fragment" data-step="2">L’ordinateur extérieur participe au calcul.</span>'
                '<small>Reconstitution pédagogique de Shakey · SRI, 1966–1972. Ce n’est pas une photographie d’archive.</small></figcaption></figure>')
    if name=='story_alvinn':
        return ('<figure class="history-stage"><div class="history-picture history-alvinn" role="img" '
                'aria-label="Reconstitution illustrée : véhicule de recherche des années 1980 observant une route."></div>'
                '<figcaption><span class="fragment" data-step="1">Observer la route</span> '
                '<span class="fragment" data-step="2">→ calculer avec le réseau</span> '
                '<span class="fragment" data-step="3">→ proposer une direction.</span>'
                '<small>Illustration du principe d’ALVINN · Dean Pomerleau, 1989. Véhicule reconstitué, pas une archive.</small></figcaption></figure>')
    if name=='story_mobilenet':
        z=year('2017 · MobileNets','Andrew Howard et ses collègues')
        for i,c in enumerate(['#ff926b','#f4c751','#7ecdc0']):
            x=45+i*108
            z+=rect(x,149,79,100,c,c,2)+text(x+40,287,f'Canal {i+1}',19)
        z+=fragment(1,arrow(166,307,166,343)+text(166,391,'Filtrer chaque canal',24,TEAL))
        z+=fragment(2,arrow(347,222,413,222)+rect(440,153,229,100,'#e5edf3',INK,3)+text(555,195,'Combiner',24)+text(555,228,'les canaux · 1 × 1',21)+text(555,290,'Projection',20,MUTED))
        z+=fragment(3,text(470,414,'Moins d’opérations.',27,INK)+text(470,457,'Le gain de temps reste à mesurer.',21,TEAL))
        return svg(z,'Séparer filtrage spatial et combinaison des canaux')
    if name=='story_jacob':
        z=year('2018 · Calcul entier','Benoit Jacob et ses collègues')
        z+=cells(60,158,4,8,23)+text(170,335,'32 bits par poids',23)
        z+=fragment(1,arrow(340,225,417,225)+cells(450,199,1,8,23)+text(560,335,'8 bits par poids',23,TEAL))
        z+=fragment(2,text(390,396,'4 fois moins de place pour ces poids.',25,INK))
        z+=fragment(3,text(390,446,'Il faut aussi les échelles et des accumulateurs adaptés.',21,MUTED))
        return svg(z,'Du format FP32 au format INT8 ; place des poids seulement')
    if name=='story_mcunet':
        z=year('2020 · MCUNet','Ji Lin, Wei-Ming Chen et leur équipe')
        z+=circle(178,225,82,'Réseau',fill='#fff0e7',color=GOLD)
        z+=fragment(1,circle(581,225,82,'Moteur',fill='#e5f5f3',color=TEAL))
        z+=fragment(2,arrow(277,205,483,205)+arrow(483,252,277,252)+text(380,326,'Concevoir ensemble',27,INK))
        z+=fragment(3,text(380,399,'Sur une carte donnée,',23)+text(380,437,'avec une mémoire et un délai donnés.',23,TEAL))
        return svg(z,'Co-conception du réseau et du moteur d’inférence')
    if name=='story_frontiers':
        z=year('Trois pistes parmi d’autres','Chaque résultat dépend de sa tâche et de sa cible.')
        for i,(label,sub,c) in enumerate([('Mieux calculer','MobileNetV4','#ff926b'),('Mieux représenter','AWQ','#f4c751'),('Apprendre sur place','Mises à jour partielles','#7ecdc0')]):
            x=130+i*250
            body=circle(x,213,50,str(i+1),fill=c,color=c)+text(x,314,label,21,INK)+text(x,354,sub,18,MUTED)
            z+=fragment(i+1,body)
        z+=text(380,447,'Quel compromis pour votre appareil ?',26,TEAL)
        return svg(z,'Architecture, représentation et adaptation locale')
    raise ValueError('Unknown story illustration: '+name)
