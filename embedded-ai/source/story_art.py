"""Original SVG stage artwork. Alice is fictional; named researchers use name cards."""


def fragment(step,body):
    return f'<g class="fragment" data-step="{step}">{body}</g>'


def alice(x,y,scale=1,pose='ask'):
    arms={
        'ask':'M42,99 L15,127 L6,111 M80,100 L106,78 L111,55',
        'carry':'M42,100 L25,126 L91,126 M79,100 L96,126 L39,126',
        'point':'M42,99 L25,144 M80,99 L111,104 L139,87',
        'wait':'M42,99 L26,139 L53,142 M80,99 L97,139 L72,142',
    }[pose]
    return f'''<g transform="translate({x} {y}) scale({scale})" class="alice-character" aria-label="Alice, personnage fictif">
    <path d="M33 47 Q31 12 61 11 Q96 14 90 60 L80 84 L39 78Z" fill="#313f4a"/>
    <ellipse cx="61" cy="49" rx="24" ry="30" fill="#efbc93"/>
    <path d="M37 37 Q48 14 75 23 L86 37 Q69 37 63 24 Q56 39 37 42" fill="#313f4a"/>
    <circle cx="52" cy="48" r="2.2" fill="#20394a"/><circle cx="70" cy="48" r="2.2" fill="#20394a"/>
    <path d="M54 62 Q61 68 68 62" fill="none" stroke="#9b5b48" stroke-width="2.2" stroke-linecap="round"/>
    <path d="M52 75 V86 H71 V75" fill="#efbc93"/><path d="M42 88 Q60 80 81 88 L89 155 H34Z" fill="#cb9158"/>
    <path d="M51 88 L61 112 L72 88" fill="#f4f3e9"/>
    <path d="M39 155 L36 213 H54 L61 166 L68 213 H87 L82 155Z" fill="#087e7b"/>
    <path d="M34 212 H54 V225 H28 Q26 216 34 212 M68 212 H87 L95 225 H68Z" fill="#263f50"/>
    <path d="{arms}" fill="none" stroke="#cb9158" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/>
    <circle cx="{111 if pose=='ask' else 25}" cy="{54 if pose=='ask' else 144}" r="6" fill="#efbc93"/>
    </g>'''


def draw_story(name):
    from diagrams import text,rect,node,arrow,circle,path,cells,svg,TEAL,INK,MUTED,GOLD,LINE,PALE
    z=''
    def lamp(x,y,on=False):
        return circle(x,y,42,fill='#f7db8f' if on else '#e4edf0',color=GOLD if on else MUTED)+path(f'M{x-21},{y+40} V{y+61} H{x+21} V{y+40}',GOLD)+path(f'M{x-15},{y+73} H{x+15}',GOLD)
    def box(x,y,label='MODÈLE'):
        return node(x,y,190,122,label,'Calcul sur des nombres',PALE)
    def scientist(initials,names,year):
        return rect(25,20,710,95,'white')+circle(74,68,27,initials)+text(125,57,names,24,INK,'start',650)+text(125,88,year,20,TEAL,'start')

    if name in {'story_cover','story_epilogue'}:
        z+=rect(20,30,720,435,'#f2f7f6','#9ccdc3',24)
        z+=alice(65,140,1.12,'point')
        z+=box(310,185,'IA À BORD')+lamp(640,240,True)
        z+=arrow(245,250,298,250)+arrow(505,250,585,250)
        z+=text(450,100,'Un service utile, ici.',30,TEAL,weight=650)
        z+=text(455,411,'Comprendre · Adapter · Vérifier',22)
    elif name=='story_request':
        z+=alice(70,170,1.05,'carry')
        z+=rect(88,280,114,65,'#e5ca9c','#b39b78',5)+path('M145,280 V345',GOLD)
        z+=text(143,448,'Alice',24)
        z+=lamp(615,237,False)+text(615,375,'La lampe',24)
        z+=fragment(1,node(268,68,375,100,'« Lumière ! »','Demande d’Alice'))
        z+=fragment(2,box(300,257,'COMPRENDRE ?')+arrow(215,220,291,280)+arrow(495,310,564,275))
        z+=fragment(3,text(480,451,'Un besoin, avant une technique.',23,TEAL))
    elif name=='story_voices':
        z+=alice(15,190,.9,'ask')
        for i,label in enumerate(['Alice','Une autre voix','Avec du bruit']):
            y=65+i*132;body=text(222,y+16,label,21,INK,'start')
            import math
            coords=' '.join(f'{"M" if j==0 else "L"}{380+j*7},{y+48+18*math.sin(j*(.45+i*.13))*math.sin(j*.19)}' for j in range(42))
            body+=path(coords,TEAL if i<2 else GOLD)
            z+=body if i==0 else fragment(i,body)
        z+=fragment(3,text(423,465,'Son → caractéristiques → modèle → mot ou refus',20,TEAL))
    elif name=='story_shakey':
        z+=scientist('SRI','Équipe Shakey','1966–1972 · Percevoir et planifier')
        z+=rect(80,240,150,137,PALE)+circle(113,393,20)+circle(195,393,20)
        z+=path('M155,240 V180',INK)+rect(120,154,76,45,INK,INK,5)+circle(176,175,10,fill='#8ed9cb')
        z+=text(155,447,'Le robot',23)
        z+=fragment(1,node(425,195,280,150,'ORDINATEUR','Calcul déporté'))
        z+=fragment(2,arrow(242,275,412,275,dashed=True)+text(331,245,'Liaison',21,TEAL))
        z+=fragment(3,text(465,435,'Agir ≠ tout calculer à bord',23,TEAL))
    elif name=='story_alvinn':
        z+=scientist('DP','Dean Pomerleau','1989 · ALVINN')
        z+=path('M70,450 L185,160 H265 L380,450',MUTED)+path('M225,185 V435',GOLD,True)
        z+=rect(164,274,125,75,TEAL,TEAL,16)+rect(185,284,82,27,'#d7efe8')
        z+=circle(180,355,15)+circle(274,355,15)
        z+=fragment(1,node(430,156,280,88,'Observations','Images et télémétrie'))
        z+=fragment(2,arrow(570,250,570,282)+node(430,293,280,98,'Réseau appris','Une direction de sortie',PALE))
        z+=fragment(3,text(565,450,'Des essais sous conditions.',21,TEAL))
    elif name in {'story_remote','story_outage'}:
        offline=name=='story_outage'
        z+=alice(16,210,.78,'ask' if offline else 'point')
        z+=box(163,170,'OBJET')+node(470,170,250,122,'SERVEUR','Inférence distante')
        z+=fragment(1,arrow(360,205,457,205,dashed=True)+text(413,160,'Son',23,TEAL))
        reply=arrow(462,265,363,265)+text(412,315,'Réponse',22,TEAL)
        z+=fragment(2,'<g class="remote-reply">'+reply+'</g>')
        z+='<g class="link-failure">'+path('M383,220 L443,280','#b15948')+path('M443,220 L383,280','#b15948')+text(425,357,'Liaison indisponible',23,'#a14f40')+'</g>'
        z+=fragment(3,text(440,423,'Dépendre du réseau change le service.',22,TEAL))
        diagram=svg(z,name).replace('class="diagram"',f'class="diagram network-scene {"offline" if offline else "online"}"')
        return '<div class="visual-stack network-stack">'+diagram+'<button class="demo-button" data-action="network-toggle">'+('Rétablir la liaison' if offline else 'Couper la liaison')+'</button><span class="scene-caption">Schéma logique : aucun serveur contacté, aucun délai mesuré.</span></div>'
    elif name=='story_pause':
        z+=alice(77,157,1.05,'wait')+node(320,150,340,150,'10 MINUTES','La boîte attend…',PALE)
        z+=text(415,405,'Comprendre la suite, puis la mesurer.',24,TEAL)
    elif name=='story_mobilenet':
        z+=scientist('AH','Andrew Howard et ses collègues','2017 · MobileNets')
        z+=node(35,167,270,170,'Convolution','Espace et canaux ensemble')
        z+=fragment(1,arrow(314,252,362,252)+node(375,150,340,110,'Filtrage par canal','Depthwise',PALE))
        z+=fragment(2,arrow(545,267,545,305)+node(375,317,340,110,'Mélange des canaux','Projection 1 × 1',PALE))
        z+=fragment(3,text(380,475,'Moins d’opérations ; temps à mesurer.',23,TEAL))
    elif name=='story_jacob':
        z+=scientist('BJ','Benoit Jacob et ses collègues','2018 · Quantification et calcul entier')
        z+=cells(72,177,4,8,24)+text(188,340,'Poids FP32',25)
        z+=fragment(1,arrow(345,250,411,250)+cells(445,211,1,8,24)+text(560,340,'Poids INT8',25,TEAL))
        z+=fragment(2,node(390,375,330,78,'+ échelles','+ accumulateurs adaptés'))
        z+=fragment(3,text(220,430,'Qualité à vérifier',23,TEAL))
    elif name=='story_memory_wait':
        z+=alice(15,195,.88,'wait')+node(190,170,200,135,'CPU','Attend les données')
        z+=fragment(1,node(500,170,220,135,'MÉMOIRE','Lit et écrit'))
        z+=fragment(2,arrow(400,195,487,195)+arrow(488,271,401,271)+text(447,355,'Échanges',23,GOLD))
        z+=fragment(3,node(255,392,440,75,'Réutiliser / fusionner','Puis vérifier sur la cible',PALE))
    elif name=='story_mcunet':
        z+=scientist('JL','Ji Lin, Wei-Ming Chen et leur équipe','2020 · MCUNet · 2021 · MCUNetV2')
        z+=node(25,162,300,125,'RÉSEAU','Architecture')
        z+=fragment(1,node(435,162,300,125,'MOTEUR','Noyaux et mémoire'))
        z+=fragment(2,arrow(332,200,425,200)+arrow(425,246,332,246))
        z+=fragment(3,arrow(175,295,290,349)+arrow(585,295,470,349)+node(180,365,400,95,'BUDGET DE LA CIBLE','Qualité · mémoire · délai',PALE))
    elif name=='story_energy':
        z+=alice(35,190,.95,'ask')
        z+=rect(270,100,380,138,'white',INK,18)+rect(650,141,20,55,INK,INK,4)
        for i in range(3):z+=rect(290+i*112,120,95,98,'#91cbbc',TEAL,5)
        z+=fragment(1,node(240,286,150,90,'Écouter'))
        z+=fragment(2,node(405,286,150,90,'Calculer'))
        z+=fragment(3,node(570,286,150,90,'Échanger')+text(475,448,'Batterie : toute la chaîne compte.',24,TEAL))
    elif name=='story_robustness':
        z+=alice(25,180,1,'ask')
        for i,(label,sub) in enumerate([('Voix connue','Cas nominal'),('Bruit seul','Entrée non prévue'),('Redémarrage','État à reconstruire')]):
            body=node(260,25+i*140,460,110,label,sub,PALE if i==0 else 'white')
            z+=body if i==0 else fragment(i,body)
        z+=fragment(3,text(475,474,'Tester le refus et le repli.',24,TEAL))
    elif name=='story_frontiers':
        for i,(label,sub) in enumerate([('Architecture','MobileNetV4 · 2024'),('Représentation','AWQ · 2024'),('Adaptation locale','Mises à jour ciblées')]):
            body=node(180,27+i*139,530,110,label,sub,PALE if i==0 else 'white')
            z+=fragment(i+1,body)
        z+=alice(18,205,.9,'point')+text(455,478,'Le besoin choisit l’échelle du modèle.',22,TEAL)
    else:
        raise ValueError('Unknown story illustration: '+name)
    return svg(z,name)
