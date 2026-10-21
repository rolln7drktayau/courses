"""Original, vector-native engineering illustrations; no external image dependencies."""
from html import escape
import math

INK='#18394b';MUTED='#617582';TEAL='#008b83';GOLD='#bd783b';PALE='#e9f1f1';LINE='#c5d4da'

def text(x,y,label,size=24,color=INK,anchor='middle',weight=500):
    lines=str(label).split('\n')
    return ''.join(f'<text x="{x}" y="{y+i*(size+7)}" text-anchor="{anchor}" fill="{color}" font-size="{size}" font-weight="{weight}">{escape(line)}</text>' for i,line in enumerate(lines))

def rect(x,y,w,h,fill='white',stroke=LINE,r=15):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>'

def node(x,y,w,h,label,sub='',fill='white',color=INK):
    z=rect(x,y,w,h,fill)
    lines=label.count('\n')+1
    z+=text(x+w/2,y+h/2-(lines-1)*15+(0 if sub else 8),label,24,color)
    if sub:z+=text(x+w/2,y+h-18,sub,18,MUTED)
    return z

def arrow(x1,y1,x2,y2,color=TEAL,dashed=False):
    return f'<path d="M{x1},{y1} L{x2},{y2}" fill="none" stroke="{color}" stroke-width="3" marker-end="url(#arr)" '+('stroke-dasharray="8 7"' if dashed else '')+'/>'

def path(d,color=TEAL,dash=False):
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="3" '+('stroke-dasharray="8 7"' if dash else '')+'/>'

def circle(x,y,r,label='',fill=PALE,color=TEAL):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{color}" stroke-width="2"/>'+text(x,y+8,label,25,color)

def svg(body,title):
    return f'''<svg class="diagram" viewBox="0 0 760 500" role="img" aria-label="{escape(title,quote=True)}" xmlns="http://www.w3.org/2000/svg"><defs><marker id="arr" markerWidth="10" markerHeight="10" refX="7" refY="3" orient="auto" markerUnits="strokeWidth"><path d="M0,0 L7,3 L0,6" fill="{TEAL}"/></marker></defs>{body}</svg>'''

def cells(x,y,rows,cols,size=28,active=(),zeros=False):
    z=''
    for i in range(rows):
        for j in range(cols):
            selected=(i,j) in active
            z+=rect(x+j*(size+5),y+i*(size+5),size,size,TEAL if selected else PALE,LINE,4)
            if zeros and (i+j)%3:z+=text(x+j*(size+5)+size/2,y+i*(size+5)+size*.72,'0',size*.65,MUTED)
    return z

def draw(name):
    z=''
    if name=='tiny_network':
        for x,ys,labels in [(95,[150,335],['x₁','x₂']),(365,[150,335],['h₁','h₂']),(645,[242],['ŷ'])]:
            for y,label in zip(ys,labels):z+=circle(x,y,41,label)
        for y in [150,335]:
            for h in [150,335]:z+=arrow(140,y,317,h)
        for h in [150,335]:z+=arrow(410,h,597,242)
        z+=text(95,65,'ENTRÉES',22)+text(365,65,'ReLU',22,TEAL)+text(645,65,'SORTIE',22)
        z+=text(380,415,'6 poids + 3 biais = 9 paramètres',25,TEAL)
        z+=text(380,459,'2 × 2 + 2 × 1 = 6 MAC, biais exclus',24)
    elif name=='forward_lab':
        return '''<div class="interactive-panel forward-lab"><div class="micro-label">INFÉRENCE · POIDS FIXES</div><label>x₁ <output data-forward-value="x1">1</output><input aria-label="Entrée x1" data-forward="x1" type="range" min="-1" max="3" step="0.25" value="1"></label><label>x₂ <output data-forward-value="x2">2</output><input aria-label="Entrée x2" data-forward="x2" type="range" min="-1" max="3" step="0.25" value="2"></label><div class="forward-values"><span>h₁ <b data-forward-value="h1">0</b></span><span>h₂ <b data-forward-value="h2">1,5</b></span></div><div class="big-result small-result"><span>ŷ =</span><output data-forward-value="y">1,5</output></div><p class="caption">h₁, h₂ : activations après ReLU. Les biais sont nuls ici ; aucun poids ne change.</p></div>'''
    elif name=='learning_step':
        return '''<div class="interactive-panel learning-lab"><div class="micro-label">UNE CORRECTION · UN SEUL POIDS</div><label>Pas η <output data-learning-value="eta">0,1</output><input aria-label="Pas d’apprentissage" data-learning="eta" type="range" min="0.01" max="1" step="0.01" value="0.1"></label><div class="learning-grid"><div><span>Poids après correction</span><strong data-learning-value="w">1,15</strong></div><div><span>Nouvelle sortie ŷ</span><strong data-learning-value="y">1,725</strong></div><div><span>Perte avant</span><strong>0,25</strong></div><div><span>Perte après</span><strong data-learning-value="loss">0,075625</strong></div></div><p class="caption" data-learning-value="verdict">La perte diminue sur cet exemple.</p><p class="caption">h₂ = 1,5 et cible c = 2 sont fixes. Une correction n’est pas un entraînement complet.</p></div>'''
    elif name=='td_bridge':
        z+=cells(130,70,3,16,24)
        z+=text(380,40,'3 variables × 16 instants = 48 valeurs',24)
        z+=arrow(380,180,380,228)
        z+=node(160,240,440,100,'Mélanger instants et variables','Réseau à écrire dans le TD',PALE)
        z+=arrow(380,348,380,385)
        z+=text(380,427,'Prédire la prochaine valeur',28,TEAL)
        z+=text(380,472,'PC : apprendre · carte : inférer et mesurer',22,MUTED)
    elif name=='families':
        for i,(label,sub) in enumerate([('CONVOLUTION','Un motif local réutilisé'),('RÉCURRENCE','Un état transmis dans le temps'),('ATTENTION','Des relations calculées selon l’entrée')]):
            z+=node(35,25+i*145,690,115,label,sub,PALE if i==0 else 'white')
    elif name=='placement_precise':
        for i,(label,sub) in enumerate([('DANS L’OBJET','Capteur → modèle local → action'),('PASSERELLE DE PROXIMITÉ','Objet → liaison locale → calcul'),('SERVEUR DISTANT','Objet → réseau → calcul distant')]):
            z+=node(25,28+i*140,705,113,label,sub,PALE if i==0 else 'white')
    elif name=='hardware_precise':
        for x,label,sub in [(20,'MICROCONTRÔLEUR','Application dédiée'),(395,'SYSTÈME LINUX','Exemple : Raspberry Pi')]:
            z+=rect(x,45,345,330,'white')+text(x+172,90,label,23,TEAL,weight=650)
            z+=node(x+30,122,285,80,'CPU')
            z+=text(x+172,248,'Flash + SRAM' if x==20 else 'RAM + stockage',24)
            z+=text(x+172,297,'Périphériques' if x==20 else 'OS + périphériques',23)
            z+=text(x+172,347,sub,19,MUTED)
        z+=text(380,440,'NPU / GPU : accélérateurs éventuels du système',23,TEAL)
        z+=text(380,479,'Vérifier le matériel réellement présent sur votre carte.',20,MUTED)
    elif name=='benchmark_lab':
        return '''<div class="interactive-panel benchmark-lab"><div class="micro-label">NAVIGATEUR ACTUEL · SOMME DE 4 096 VALEURS</div><div class="benchmark-actions"><button class="demo-button" data-action="benchmark">Mesurer ici</button><button class="demo-button" data-action="benchmark-csv" disabled>Exporter CSV</button></div><p class="benchmark-status" role="status">Pas encore mesuré. Aucune durée préremplie.</p><table class="benchmark-table"><thead><tr><th>Par somme</th><th>Médiane</th><th>Min–max</th></tr></thead><tbody><tr><th>Boucle</th><td data-bench="loop">—</td><td data-bench="loop-range">—</td></tr><tr><th>reduce</th><td data-bench="reduce">—</td><td data-bench="reduce-range">—</td></tr></tbody></table><p class="caption">Résultat vérifié avant et après. Données : Float64Array, 32 Kio ; ceci n’est pas un pic RAM système.</p><p class="caption">Les mesures varient avec le navigateur et sa charge. Aucune énergie ni durée sur carte n’est déduite.</p></div>'''
    elif name in {'hero','closing'}:
        dark=name=='hero';color='#9ae5d9' if dark else TEAL;ink='#e5f0f3' if dark else INK
        for k in range(7):
            y=100+k*45
            z+=path(f'M15,{y} H{130+(k%3)*30} L240,{125+k*35}',color)
            z+=path(f'M520,{125+k*35} L{620-(k%3)*25},{y} H745',color)
            z+=f'<circle class="signal-dot" style="animation-delay:{k*.18}s" cx="{100+k*8}" cy="{y}" r="5" fill="{color}"/>'
        z+=rect(240,95,280,290,'#113246' if dark else 'white',color,26)
        z+=rect(265,120,230,240,'#0b2538' if dark else PALE,color,18)
        for k in range(5):
            z+=path(f'M{285+k*46},75 V95',color)+path(f'M{285+k*46},385 V405',color)
        z+=text(380,202,'EMBEDDED',27,ink,weight=650)+text(380,253,'AI',64,ink,weight=650)
        z+=text(380,318,'Données · Modèle · Système',17,color)
        z+=text(380,454,'Le service réel fixe le budget.',24,ink)
    elif name=='route':
        labels=[('01','Pour qui ?','Besoin et histoire · 20 min'),('02','Comment apprend-elle ?','Un réseau complet · 35 min'),('03','Comment l’embarquer ?','Déploiement et coûts · 30 min'),('04','Comment l’alléger ?','Deux leviers · 35 min'),('05','Quelle preuve ?','Enquête + décision · 50 min')]
        for i,(n,label,t) in enumerate(labels):
            y=18+i*80;z+=circle(58,y+29,26,n)+text(108,y+23,label,26,anchor='start',weight=650)+text(108,y+53,t,20,MUTED,anchor='start')
            if i<4:z+=path(f'M58,{y+57} V{y+77}',LINE)
        z+=text(380,465,'Quiz : 6 · 13 · 19 · 26 · 31 · pause : 10 min',21,TEAL)
    elif name=='human_need':
        z+=circle(110,115,36,'',fill=PALE)
        z+=path('M50,235 V205 Q110,155 170,205 V235',TEAL)
        z+=text(110,280,'Une personne',23)+text(110,315,'« lumière »',24,TEAL)
        z+=arrow(180,200,263,200)
        z+=node(275,130,215,155,'Reconnaître\nle mot','Calcul local',PALE)
        z+=arrow(495,200,555,200)
        z+=circle(645,177,49,'',fill='#f4e5b4',color=GOLD)
        z+=path('M622,220 V245 H668 V220',GOLD)+path('M627,260 H663',GOLD)
        z+=text(645,315,'La lampe',24)
        z+=rect(55,375,650,85,'white')
        z+=text(380,410,'Voix inconnue ou doute ?',24,weight=650)
        z+=text(380,441,'Ne pas agir · garder la commande manuelle',21,MUTED)
    elif name=='placement':
        for i,(a,b) in enumerate([('LOCAL','Capteur → modèle'),('DISTANT','Capteur → réseau → serveur'),('HYBRIDE','Traitement local + recours distant')]):
            y=28+i*140;z+=node(25,y,705,113,a,b,PALE if i==0 else 'white')
            z+=circle(665,y+34,12,fill=TEAL if i==0 else '#d8e3e6')
    elif name=='history1':
        z+=path('M100,230 H660',LINE)
        for x,year,who,label in [(130,'1966–72','SRI','Shakey\nPercevoir et planifier'),(380,'1989','Dean Pomerleau','ALVINN\nApprendre à guider'),(630,'2017','Howard et al.','MobileNets\nRéduire le calcul')]:
            z+=circle(x,230,12,fill=TEAL)+text(x,103,year,32,TEAL,weight=650)+text(x,146,who,20)
            z+=rect(x-112,278,224,119)
            z+=text(x,320,label,21)
        z+=text(380,457,'Le besoin précède la miniaturisation.',24,TEAL)
    elif name=='barriers':
        for i,(label,sub) in enumerate([('MÉMOIRE','Tout ne tient pas en RAM.'),('ÉNERGIE','La batterie n’est pas infinie.'),('DÉLAI','La réponse doit arriver à temps.'),('CONFIANCE','Une erreur peut avoir un coût.')]):
            x=20+(i%2)*375;y=30+(i//2)*180
            z+=rect(x,y,345,145,'white')
            z+=text(x+172,y+57,label,25,TEAL,weight=650)
            z+=text(x+172,y+104,sub,19,MUTED)
        z+=text(380,452,'Piste : réduire → adapter → vérifier',25,TEAL)
    elif name=='history2':
        labels=[('2020','MCUNet','Réseau + moteur'),('2022','Apprentissage local','Mises à jour ciblées'),('2024–25','Mobile / LLM','Formats + noyaux'),('2026','Co-conception','Logiciel + matériel')]
        for i,(year,label,sub) in enumerate(labels):
            x=25+(i%2)*375;y=35+(i//2)*215
            z+=node(x,y,335,177,label,sub)+text(x+30,y+44,year,24,TEAL,'start',650)
    elif name=='tasks':
        for i,(a,b) in enumerate([('CLASSIFICATION','normal / inhabituel'),('RÉGRESSION','prochaine valeur : 0,42'),('DÉCISION','alerter / attendre / replier')]):
            z+=node(45,25+i*145,660,115,a,b,PALE if i==1 else 'white')
    elif name in {'pipeline','deployment','measurement','research'}:
        if name=='pipeline':labels=['Acquérir','Préparer','Inférer','Interpréter','Surveiller','Agir']
        elif name=='deployment':labels=['PC : apprendre','Exporter','Compiler','Flasher','Comparer','Intégrer']
        elif name=='measurement':labels=['Version Git','Configuration','Binaire','CSV brut','Analyse','Figure']
        else:labels=['Question','Hypothèse','Implémentation','Correction','Mesures','Limites / suite']
        for i,label in enumerate(labels):
            col=i%3 if i<3 else 2-i%3;row=0 if i<3 else 1
            x=20+col*250;y=80+row*240
            z+=node(x,y,220,100,label,fill=PALE if i in {0,5} else 'white')
            z+=text(x+25,y-13,f'0{i+1}',19,TEAL,'start',650)
            if i<2:z+=arrow(x+220,y+50,x+248,y+50)
            elif i==2:z+=arrow(x+110,y+110,x+110,y+230)
            elif i<5:z+=arrow(x-4,y+50,x-28,y+50)
        if name=='research':z+=text(380,462,'La conclusion peut être négative.',22,TEAL)
    elif name=='split':
        for s in range(24):
            x=25+(s%12)*59;y=67+(s//12)*62
            fill=TEAL if s<16 else GOLD if s<20 else INK
            z+=rect(x,y,46,43,fill,fill,5)+text(x+23,y+29,str(s),20,'white')
        z+=text(145,245,'16 train',25,TEAL)+text(389,245,'4 validation',25,GOLD)+text(635,245,'4 test',25,INK)
        z+=arrow(380,270,380,320)
        for i in range(16):z+=rect(40+i*35,352,30,66,PALE,LINE,4)
        z+=arrow(615,385,665,385)+node(671,352,60,66,'y')
        z+=text(380,462,'Une fenêtre reste dans une seule séquence.',21,MUTED)
    elif name=='dense':
        W=[[1,0,-1],[2,1,0]];X=[2,1,3]
        z+=text(194,65,'W',28)+text(464,65,'x',28)+text(666,65,'y',28)
        for i,row in enumerate(W):
            for j,v in enumerate(row):
                x=67+j*86;y=105+i*88
                z+=f'<g data-mac-cell="{i*3+j}">'+rect(x,y,73,72,'white')+text(x+36,y+45,str(v),30)+'</g>'
        for i,v in enumerate(X):z+=node(425,88+i*72,75,61,str(v))
        z+=text(367,185,'×',45,TEAL)+text(556,185,'=',45,TEAL)
        z+=node(607,116,118,72,'−1')+node(607,210,118,72,'6')
        z+=text(650,329,'b = [0, 1]',22,MUTED)
        z+=text(380,400,'y₁ = 1×2 + 0×1 − 1×3 + 0 = −1',24)
        z+=text(380,444,'6 MAC + 2 additions de biais',22,TEAL)
        return '<div class="visual-stack">'+svg(z,'Projection dense de trois entrées vers deux sorties')+'<button class="demo-button" data-action="mac">Suivre les 6 MAC</button></div>'
    elif name=='residual':
        z+=node(20,200,106,80,'x')+arrow(126,240,200,240)
        z+=node(205,195,260,90,'f(x)','Calcul appris')+arrow(467,240,555,240)
        z+=circle(595,240,39,'+')+arrow(636,240,700,240)
        z+=path('M155,240 V90 H595 V199',GOLD)
        z+=text(370,64,'Entrée à conserver jusqu’ici',23,GOLD)
        z+=text(389,391,'x + f(x)',37,TEAL)+text(389,440,'Le raccourci prolonge la vie de x.',21,MUTED)
    elif name=='convolution':
        z+=cells(35,95,5,5,31,active=[(i,j) for i in range(3) for j in range(3)])
        z+=text(125,65,'Image / carte',23)
        z+=arrow(225,178,285,178)+node(295,110,175,132,'Depthwise','3×3 par canal')
        z+=arrow(475,178,520,178)+node(531,110,195,132,'Pointwise','Mélange 1×1')
        z+=node(45,325,305,108,'18 432 MAC','Convolution classique')
        z+=node(405,325,305,108,'2 336 MAC','Séparée : exemple 32 → 64')
        z+=text(380,473,'Calcul par position · exemple arithmétique, pas un benchmark',17,MUTED)
    elif name=='recurrent':
        for i in range(3):
            x=40+i*250;z+=node(x,170,185,110,'Cellule','Poids partagés')
            z+=text(x+93,92,f'x(t{["−1","","+1"][i]})',25)+arrow(x+93,113,x+93,163)
            z+=arrow(x+93,285,x+93,345)+text(x+93,382,'Sortie',24)
            if i<2:z+=arrow(x+190,223,x+244,223)+text(x+218,196,'h',21,TEAL)
        z+=text(380,450,'État transmis ≠ historique complet stocké',24,TEAL)
    elif name=='attention':
        z+=text(156,50,'Scores entre positions',23)
        for i in range(7):
            for j in range(7):
                opacity=.15+.75*((i*3+j*5)%8)/7
                z+=f'<rect x="{35+j*39}" y="{85+i*39}" width="34" height="34" rx="3" fill="{TEAL}" opacity="{opacity}"/>'
        z+=arrow(337,220,393,220)+node(410,140,310,155,'Normaliser\npuis mélanger','softmax(QKᵀ / √d) V')
        z+=text(544,345,'ᵀ : transpose · d : dimension d’une tête',18,MUTED)
        z+=text(380,425,'Doubler la longueur → 4× plus de scores naïfs',25,TEAL)
        z+=text(380,465,'Carte d’attention illustrative ; aucune sortie de modèle mesurée',17,MUTED)
    elif name=='kv':
        return '''<div class="interactive-panel"><div class="micro-label">CACHE KV · EXEMPLE ANALYTIQUE · LOT 1</div><div class="big-result"><output data-output="kv">16</output><span>Mio</span></div><div class="cache-grid">'''+''.join('<i></i>' for _ in range(32))+'''</div><label>Tokens conservés <output data-output="tokens">1024</output><input aria-label="Nombre de tokens du cache" data-control="kv" type="range" min="128" max="4096" step="128" value="1024"></label><p class="math">2 × 16 couches × T × 4 têtes KV × 64 × 2 octets</p><p class="caption">T est le nombre de tokens. Ici FP16 ; aucune mémoire de poids incluse.</p></div>'''
    elif name=='training':
        for x,label in [(35,'Entrée'),(285,'Réseau'),(535,'Perte L')]:z+=node(x,110,185,100,label)
        z+=arrow(225,160,278,160)+arrow(477,160,528,160)
        z+=path('M625,220 V330 H377 V220',GOLD)+path('M377,330 H127 V220',GOLD)
        z+=text(382,375,'Gradients ∇L : parcours arrière',25,GOLD)
        z+=text(380,448,'θ ← θ − η∇L',40,TEAL)
        z+=text(380,490,'θ : paramètres · η : pas · ∇L : gradient de la perte',20,MUTED)
    elif name=='hardware':
        items=[('MCU','Flash + SRAM','Noyaux compacts'),('CPU / Linux','Caches + RAM','Services et système'),('GPU','Calcul parallèle','Transferts et lots'),('NPU','Opérateurs ciblés','Formats compatibles')]
        for i,(a,b,c) in enumerate(items):
            x=25+(i%2)*375;y=30+(i//2)*225
            z+=node(x,y,335,184,a,c,PALE if i==0 else 'white')+text(x+167,y+111,b,21,MUTED)
    elif name=='memory':
        return '''<div class="interactive-panel"><div class="micro-label">EXEMPLE MCU · POIDS CONSERVÉS EN FLASH</div><div class="memory-columns"><div><h3>Poids bruts</h3><strong data-output="weights">400 Ko</strong><span>100 000 paramètres</span><div class="memory-bar"><i data-output="weightbar"></i></div></div><div><h3>Travail SRAM</h3><strong>120 Ko</strong><span>activations + buffers + pile</span><div class="memory-bar"><i style="width:30%;background:var(--gold)"></i></div></div></div><div class="segmented"><button class="selected" data-weight-bits="32">Poids FP32</button><button data-weight-bits="8">Poids INT8 seuls</button></div><p class="caption">Budgets fictifs distincts. Échelles et métadonnées exclues du payload ; SRAM inchangée dans cet exemple.</p></div>'''
    elif name=='roofline':
        z+=path('M83,45 V390 H720',INK)
        z+=path('M85,375 L358,115 H716',TEAL)
        z+=path('M358,115 V390',LINE,True)
        z+=text(225,245,'Transferts limitants',22,TEAL)+text(545,88,'Calcul limitant',22,TEAL)
        z+=text(385,451,'Intensité : MAC par octet transféré →',23)
        z+=text(120,48,'Débit utile',22,INK,'start')
        z+=circle(235,270,9,fill=GOLD,color=GOLD)+circle(510,179,9,fill=GOLD,color=GOLD)
        z+=text(520,302,'Mieux réutiliser\npeut déplacer le goulot.',23,MUTED)
        z+=text(380,479,'Schéma conceptuel · axes non calibrés',16,MUTED)
    elif name=='deadline':
        x0=95;scale=22
        for i,d in enumerate([12,17,24]):
            y=100+i*107;z+=text(65,y+34,f'#{i+1}',22,MUTED)
            z+=rect(x0,y,d*scale,52,TEAL if d<20 else '#ad5f49','none',8)+text(x0+d*scale/2,y+35,f'{d} ms',25,'white')
        z+=path(f'M{x0+20*scale},60 V420',GOLD,True)+text(x0+20*scale,40,'Échéance : 20 ms',24,GOLD)
        z+=text(380,469,'Durées pédagogiques · le troisième appel est trop tardif.',22)
    elif name=='energy':
        z+=path('M100,60 V390 H705',INK)
        z+=rect(180,140,240,248,'#d4e9e4','none',0)+path('M100,360 H180 V140 H420 V360 H695',TEAL)
        z+=text(300,108,'P = 0,1 W',27,TEAL)+text(300,430,'Durée Δt = 0,02 s',25)
        z+=text(579,201,'E = P × Δt',29)+text(579,250,'= 2 mJ',36,TEAL)
        z+=text(380,480,'Exemple à puissance constante · pas une mesure de carte',18,MUTED)
    elif name=='codesign':
        z+=node(15,50,330,150,'MODÈLE','Blocs · précision · dimensions')
        z+=node(415,50,330,150,'EXÉCUTION','Noyaux · buffers · ordre')
        z+=arrow(352,123,407,123)+arrow(408,156,352,156)
        z+=arrow(190,212,300,320)+arrow(590,212,476,320)
        z+=node(200,325,360,120,'Budget de la cible','Qualité · latence · mémoire')
    elif name=='pause':
        for r in [80,125,170]:z+=f'<circle cx="380" cy="240" r="{r}" fill="none" stroke="{LINE}" stroke-width="2"/>'
        z+=circle(380,240,80,'10 min')
        z+=text(380,465,'Le modèle et son matériel forment un système.',22,MUTED)
    elif name=='levers':
        for i,(a,b) in enumerate([('REPRÉSENTATION','Bits et échelles'),('STRUCTURE','Blocs et canaux'),('EXÉCUTION','Ordre et buffers'),('MATÉRIEL','ISA et accélérateur')]):
            x=20+(i%2)*385;y=30+(i//2)*235
            z+=node(x,y,330,175,a,b,PALE if i in {0,3} else 'white')
    elif name=='quant':
        return '''<div class="interactive-panel"><div class="micro-label">ARRONDI SYMÉTRIQUE · EXEMPLE SUR [−1, 1]</div><svg class="quant-chart" viewBox="0 0 700 235" aria-label="Valeurs originales et valeurs quantifiées" role="img"></svg><label>Précision des codes <output data-output="bits">4 bits</output><input aria-label="Nombre de bits de quantification" data-control="quant" type="range" min="4" max="8" step="1" value="4"></label><div class="demo-stats"><span>Pas s : <b data-output="step">0,1429</b></span><span>Erreur max illustrée : <b data-output="qerror">0,069</b></span></div><p class="caption">Cercles : valeurs initiales ; carrés : valeurs reconstruites. Pas un test de qualité de réseau.</p></div>'''
    elif name=='awq':
        for i,label in enumerate(['Activations\nde calibration','Échelles\npar canal','Quantification\ndes poids']):
            x=25+i*250;z+=node(x,108,210,155,label)
            if i<2:z+=arrow(x+215,185,x+244,185)
        z+=text(380,345,'Préserver ce qui change le plus la sortie',25,TEAL)
        z+=text(380,405,'Puis vérifier qualité et noyau réellement exécuté.',23,MUTED)
    elif name=='compression':
        z+=cells(45,100,6,7,30,zeros=True)+text(165,65,'Zéros dispersés',24)
        for i in range(6):
            for j in range(4):z+=rect(460+j*42,100+i*35,30,30,TEAL if j==1 else PALE,LINE,4)
        z+=text(545,65,'Canaux retirés',24)+arrow(310,205,408,205)
        z+=text(380,390,'Le noyau doit exploiter la structure restante.',25,TEAL)
        z+=text(380,450,'Distillation : enseignant → petit élève à entraîner',22,MUTED)
    elif name=='fusion':
        z+=text(380,52,'DEUX OPÉRATIONS SÉPARÉES',22,MUTED)
        z+=node(30,95,180,94,'Dense')+node(286,95,190,94,'Écriture RAM')+node(548,95,175,94,'ReLU')
        z+=arrow(215,142,279,142)+arrow(481,142,541,142)
        z+=text(380,275,'UNE FUSION POSSIBLE',22,TEAL)
        z+=node(88,320,300,104,'Dense + ReLU',fill=PALE)+arrow(392,372,455,372)+node(467,320,235,104,'Sortie écrite')
        z+=text(380,475,'Moins d’écritures si le graphe et le noyau le permettent.',20,MUTED)
    elif name=='lut':
        z+=text(185,70,'Entrée : [2, −1]',27)+text(185,121,'Poids : −1 ou +1',23,MUTED)
        for i,(bits,val) in enumerate([('00','−1'),('01','−3'),('10','3'),('11','1')]):
            z+=node(55,170+i*61,250,51,f'{bits}  →  {val}',fill=PALE if i==2 else 'white')
        z+=arrow(319,302,430,302)+node(448,230,260,120,'Code 10 → 3','Au lieu de refaire les produits')
        z+=text(380,466,'Exemple à 2 termes · préparer la table puis amortir son coût',18,MUTED)
    elif name=='amdahl':
        return '''<div class="interactive-panel"><div class="micro-label">TRAVAIL FIXE · SURCOÛTS NOUVEAUX EXCLUS</div><div class="amdahl-bars"><span>Avant</span><div class="time-bar"><i data-output="before-part"></i><b>100</b></div><span>Après</span><div class="time-bar after" data-output="after-bar"><i data-output="after-part"></i><b data-output="after-time">90</b></div></div><div class="big-result small-result"><output data-output="speedup">1,11</output><span>× global</span></div><label>Part initiale de la brique <output data-output="p">20 %</output><input aria-label="Part initiale du temps dans la brique" data-control="fraction" type="range" min="0" max="100" step="5" value="20"></label><label>Accélération de la brique <output data-output="s">2 ×</output><input aria-label="Accélération locale" data-control="speed" type="range" min="1" max="10" step="0.5" value="2"></label></div>'''
    elif name=='reliability':
        z+=path('M55,350 H710',INK)
        for shift,color,label in [(0,TEAL,'Apprentissage'),(190,GOLD,'Déploiement modifié')]:
            points=[(70+j*7,350-200*math.exp(-((70+j*7-280-shift)/100)**2)) for j in range(90)]
            z+=path('M'+' L'.join(f'{x},{y:.1f}' for x,y in points),color)
            z+=text(250+shift,100 if shift==0 else 150,label,22,color)
        z+=text(380,407,'Un changement de distribution peut déplacer les erreurs.',23)
        z+=text(380,460,'Schéma qualitatif : aucune fréquence mesurée.',18,MUTED)
    elif name=='security':
        for i,label in enumerate(['Données','Modèle','Entrées','Action']):
            x=20+i*188;z+=node(x,180,163,95,label)
            if i<3:z+=arrow(x+166,227,x+184,227)
        for x,label in [(100,'Empoisonner'),(286,'Altérer / extraire'),(474,'Tromper'),(662,'Détourner')]:
            z+=text(x,85,label,19,GOLD)+arrow(x,105,x,170,GOLD)
        z+=node(145,345,470,100,'Droits · Vérification · Mise à jour','Réduire le risque, sans garantie absolue',PALE)
    elif name=='llm':
        z+=node(40,70,680,130,'1,7 milliard × 4 bits ÷ 8','Payload : 850 000 000 octets ≈ 850 Mo')
        z+=arrow(380,210,380,265)
        z+=node(40,280,680,150,'+ cache + activations + moteur','Une taille de poids n’est pas un budget système.',PALE)
    elif name=='npu':
        z+=node(40,60,260,110,'CPU','Opération non prise en charge')+node(450,60,260,110,'NPU','Noyau compatible')
        z+=arrow(310,100,438,100)+arrow(438,145,310,145)
        z+=text(380,225,'Copies · conversions · synchronisation',23,GOLD)
        z+=node(98,310,565,120,'Mesurer le graphe entier','Schéma possible, dépendant du backend',PALE)
    elif name=='frontier':
        z+=rect(20,60,345,340)+text(50,111,'JUIN 2026',20,TEAL,'start',650)
        z+=text(193,181,'FastGRNN sur MCU',25,weight=650)+text(193,263,'Mise en régime\nà examiner',25,TEAL)
        z+=text(193,370,'Emre Can Kizilates',21,MUTED)
        z+=rect(397,60,345,340)+text(427,111,'OCTOBRE 2026',20,TEAL,'start',650)
        z+=text(570,181,'Transformer sur RISC-V',23,weight=650)
        z+=text(570,263,'Instructions + compilation\nAire et énergie à compter',23,TEAL)
        z+=text(570,370,'Ajay Kumar M et al.',21,MUTED)
        z+=text(380,459,'Deux prépublications : hypothèses et périmètres à vérifier.',20,MUTED)
    else:
        z+=circle(380,220,120,'?')+text(380,420,'Argumenter avant de choisir.',25,TEAL)
    return svg(z,name)
