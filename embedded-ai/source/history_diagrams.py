"""Original teaching schematics, not historical images or measured results."""
from diagrams import text, rect, arrow, path, node, svg, TEAL, INK, MUTED, PALE, GOLD


def history_diagram(name):
    z=''
    if name=='history_timeline':
        rows=[
            ('1958 →','Rosenblatt · perceptron → Mark I','400 photocellules ; poids physiques','R25–26,35'),
            ('1966–72','Shakey · SRI','Percevoir et agir','R22'),
            ('1989–91','ALVINN · Pomerleau','Voir les cas difficiles','R01,27'),
            ('1989–98','Bell Labs · LeCun / ANNA','Lire ; choisir le matériel','R28–29'),
            ('1989–90','Optimal Brain Damage','Retirer certains poids','R30'),
            ('2012','AlexNet','Le calcul prend de l’ampleur','R31'),
            ('2015–16','Deep Compression','Compresser les réseaux','R32'),
            ('2019–21','TinyML / MLPerf Tiny','Déployer ; comparer','R18,21,33–34'),
            ('2020–21','MCUNet / MCUNetV2','Réseau + mémoire','R04–05'),
        ]
        z+=text(24,28,'DATE',22,MUTED,'start')+text(260,28,'PERSONNES ET PROJETS',22,MUTED,'start')+text(840,28,'CONTRAINTE À RETENIR',22,MUTED,'start')
        for i,(year,label,lesson,ref) in enumerate(rows):
            y=66+i*44
            if i%2==0:z+=rect(10,y-27,1420,40,'#e4eeec','none',5)
            z+=text(24,y,year,25,TEAL,'start',650)
            z+=text(260,y,label,25,INK,'start',600)
            z+=text(840,y,lesson,25,INK,'start')
            z+=text(1415,y,ref,14,MUTED,'end')
        z+=text(720,474,'Sélection de jalons ; les démarches coexistent. Schéma pédagogique, pas une archive.',22,MUTED)
        return svg(z,'Frise chronologique de l’IA embarquée').replace('0 0 760 500','0 0 1440 500')
    elif name=='alvinn_recovery':
        z+=text(380,34,'LA VUE CHANGE. LA CORRECTION AUSSI.',22,TEAL,weight=650)
        for i,(label,shift,command) in enumerate([
            ('Au centre',0,'Continuer'),('Vue décalée',-34,'Revenir à gauche'),('Vue décalée',34,'Revenir à droite')]):
            x=20+i*248
            z+=rect(x,67,228,243,'white')+text(x+114,100,label,22)
            z+=f'<path d="M{x+29+shift},264 L{x+83+shift},127 L{x+145+shift},127 L{x+199+shift},264 Z" fill="#dce5e8"/>'
            z+=path(f'M{x+114+shift},135 L{x+114+shift},255',MUTED,True)
            z+=rect(x+98,229,32,43,TEAL,TEAL,6)
            z+=text(x+114,297,command,18,TEAL)
        z+=arrow(380,320,380,356)
        z+=node(105,366,550,73,'Vue transformée + direction corrigée',fill=PALE)
        z+=text(380,470,'Principe de l’augmentation des données d’ALVINN.',19,MUTED)
        z+=text(380,495,'Reconstitution pédagogique ; pas une vue de sa caméra.',16,MUTED)
    elif name=='why_embedded':
        for i,(label,sub) in enumerate([
            ('LA LIAISON','Le service doit-il fonctionner hors ligne ?'),
            ('LES RESSOURCES','Que peut contenir et alimenter la boîte ?'),
            ('LES PREUVES','Que donne le même essai sur la vraie carte ?')]):
            y=20+i*143
            z+=rect(20,y,720,118,'white')
            z+=text(48,y+37,label,23,TEAL,'start',650)
            z+=text(48,y+81,sub,23,INK,'start')
        z+=text(380,475,'Un choix à justifier, puis à mesurer.',23,TEAL)
        z+=text(380,498,'Schéma pédagogique ; aucune performance annoncée.',16,MUTED)
    elif name=='feedback_bridge':
        z+=node(45,60,270,95,'Capter','Lire les capteurs',PALE)
        z+=node(445,60,270,95,'Décider','Exécuter le modèle',PALE)
        z+=node(445,260,270,95,'Agir','Commander le mouvement',PALE)
        z+=node(45,260,270,95,'Environnement','Il a changé',PALE)
        z+=arrow(323,107,435,107)+arrow(580,165,580,250)+arrow(435,307,325,307)
        z+=arrow(180,250,180,165)
        z+=text(113,209,'retard',21,GOLD)
        z+=text(380,401,'ROS : plusieurs nœuds, plusieurs cadences',21,TEAL)
        z+=text(380,447,'Capter, décider, agir, puis percevoir',20,INK)
        z+=text(380,472,'le résultat de son action.',20,INK)
        z+=text(380,497,'Schéma pédagogique. Aucune mesure ni performance annoncée.',15,MUTED)
    else:raise ValueError(name)
    return svg(z,name.replace('_',' '))
