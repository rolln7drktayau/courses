"""Original additions selected after comparing public university course descriptions."""
CHAPTERS=['Le besoin avant le modèle','Des données pour apprendre','Le neurone pas à pas','Les réseaux d’aujourd’hui','La machine et ses limites','L’art du compromis','Du PC à l’objet fiable','Apprendre à chercher']
SHORT_CHAPTERS=['Besoin','Données','Neurone','Réseaux','Machine','Compromis','Déployer','Chercher']
COURSE_REFS={
 'C1':['MIT · 6.5940, TinyML and Efficient AI Computing','https://hanlab.mit.edu/courses/2026-fall-65940','Programme public et liste des laboratoires : compression, recherche d’architecture et déploiement.'],
 'C2':['Harvard · CS249r, Tiny Machine Learning','https://sites.google.com/g.harvard.edu/cs249-tinyml-2023','Chaîne complète, données, mesures, déploiement, opérations et responsabilité.'],
 'C3':['ETH Zurich · Machine Learning on Microcontrollers','https://pbl.ee.ethz.ch/education/mlom.html','Acquisition, modèles classiques, calcul embarqué et pratique sur matériel.'],
 'C4':['Heidelberg · Embedded Machine Learning','https://hawaii.ziti.uni-heidelberg.de/teaching/eml/','Interactions entre modèle, matériel, données imparfaites et optimisations.'],
 'C5':['Harvard / TinyMLedu · ressources de formation','https://tinyml.seas.harvard.edu/courses/','Parcours fondations, applications, déploiement et maintenance ; liens vers les ressources.']}
def chapter(lesson):
 return 0 if lesson<=8 else 1 if lesson<=12 else 2 if lesson<=20 else 3 if lesson<=28 else 4 if lesson<=36 else 5 if lesson<=42 else 6 if lesson<=49 else 7

def E(after,id,title,lead,steps,flow,limit,deep='',source=(),widget=''):
 return dict(after=after,id=id,title=title,lead=lead,steps=steps,flow=flow,limit=limit,deep=deep,source=list(source),widget=widget,analogy='',quiz=None,ch=chapter(after),lesson=after,activity='')
ADDITIONS=[
 E(8,'exigences','Avant de construire : promettre quoi ?','Un besoin humain doit devenir des exigences que l’on peut vérifier.',[
  'Le cahier des charges décrit le service attendu et les contraintes obligatoires. Pour Mila : reconnaître certaines commandes, hors ligne, sans envoyer le son.',
  'Écrire aussi les situations à prendre en charge : voix, distances, bruits et durée d’écoute. Une promesse sans conditions ne se teste pas correctement.',
  'Définir les critères avant de choisir le modèle : commandes manquées, activations non souhaitées, délai total, mémoire et énergie disponible.',
  'Si une exigence n’est pas tenue, revoir le besoin, le matériel ou la méthode. Ne pas changer le critère après mesure pour sauver le résultat.'],
 ['Besoin humain','Exigences','Protocole','Choix de conception'],
 'Les valeurs limites doivent venir de l’usage et du matériel. Le cours ne leur attribue pas des seuils arbitraires mesurés.',
 'Exemple de question vérifiable : une commande lancée depuis la pièce voisine doit-elle fonctionner ? Si oui, il faut représenter cette situation dans les données et les essais. Un résultat moyen ne suffit pas à vérifier tous les cas importants.',source=['C2']),
 E(20,'evenements-rares','99 % de réussite peut cacher un échec','Une lampe entend beaucoup plus de silence que de commandes.',[
  'Exemple fictif : 1 000 fenêtres audio contiennent 990 silences et 10 commandes. Une fenêtre est une courte portion du signal.',
  'Le programme qui répond toujours « silence » réussit 990 décisions sur 1 000, soit 99 %. Pourtant, il manque les 10 commandes.',
  'Le rappel d’une classe est la part de ses exemples réellement détectés. Ici, le rappel des commandes vaut 0 sur 10, donc 0 %.',
  'Séparer les erreurs par catégorie et par situation. Pour un objet qui écoute longtemps, compter aussi les activations non souhaitées par durée d’écoute.'],
 ['990 silences + 10 commandes','Toujours « silence »','99 % global','0 % des commandes trouvées'],
 'Ces nombres illustrent un piège de lecture ; ils ne décrivent pas un système testé.',
 'Une matrice de confusion croise les catégories attendues et prédites. Elle permet de distinguer les commandes manquées des activations non souhaitées. Le terme « précision » est ambigu : annoncer exactement la métrique et sa formule.',source=['C2','C4']),
 E(28,'arbre-simple','Un arbre de décision peut suffire','L’IA embarquée ne se limite pas aux réseaux de neurones.',[
  'Un arbre de décision enchaîne des questions simples sur les données. Chaque branche mène à une autre question ou à une réponse.',
  'Exemple écrit pour comprendre : « Une présence est-elle détectée ? » Si non, garder la lumière éteinte ; si oui, vérifier si la pièce est sombre.',
  'Les questions et leurs seuils peuvent être appris à partir de données. L’arbre de cet exemple est écrit à la main : nous ne prétendons pas l’avoir entraîné.',
  'Pour des mesures numériques simples, comparer aussi une règle, une régression ou un petit arbre. Un réseau plus gros n’est pas automatiquement meilleur.'],
 ['Présence ?','Non : éteindre','Oui : pièce sombre ?','Allumer si nécessaire'],
 'Ce petit arbre ne reconnaît pas le langage. Son intérêt est de montrer une autre organisation de décision.',
 'D’autres méthodes classiques existent : voisins proches, forêts d’arbres et machines à vecteurs de support. Elles n’ont pas toutes le même coût d’exécution ni le même besoin de stockage. Les choisir exige une comparaison sur la tâche et la cible.',source=['C3']),
 E(33,'goulet','Qui attend qui : le calcul ou la mémoire ?','Une machine peut manquer de vitesse de calcul, ou attendre ses données.',[
  'Un goulet d’étranglement est la ressource qui limite l’exécution. Ajouter des unités de calcul aide peu si les nombres n’arrivent pas assez vite.',
  'Exemple théorique : transférer 1 000 000 octets avec un débit de 100 000 000 octets par seconde demande au moins 0,01 seconde dans ce modèle idéal.',
  'Si le calcul idéal demande 0,002 seconde, les échanges peuvent dominer. Réutiliser des données déjà proches peut alors être plus utile que retirer quelques multiplications.',
  'Un profiler et des expériences ciblées servent à vérifier cette hypothèse. Changer une taille de bloc, mesurer, puis contrôler les sorties.'],
 ['Données à transférer','Débit mémoire','Calcul disponible','Ressource limitante'],
 'C’est une borne simplifiée, pas un chronométrage. Les surcoûts, caches et possibilités de recouvrement changent le résultat réel.',
 'Le modèle roofline relie le débit de calcul, le débit mémoire et la quantité d’opérations réalisées par octet transféré. Il aide à raisonner, mais ne remplace pas un profilage sur la cible.',source=['C1','C4']),
 E(35,'veille','Écouter sans tout calculer en permanence','La lampe doit surtout attendre. L’attente fait partie du budget.',[
  'Un fonctionnement toujours actif traite les entrées en continu. Même quand personne ne parle, capteur et programme peuvent consommer.',
  'Une cascade utilise un premier traitement léger pour décider si un calcul plus coûteux est nécessaire. Par exemple : détecter un signal avant de reconnaître une commande.',
  'Le rapport cyclique est la part du temps où un composant est actif. Le réduire peut économiser de l’énergie, mais un réveil trop tardif peut manquer le début d’un mot.',
  'Comparer le système complet : attente, réveil, tampon audio, modèle principal et erreurs supplémentaires. Une optimisation du modèle seul peut manquer le coût dominant.'],
 ['Écoute légère','Événement possible','Calcul complet','Retour à l’attente'],
 'Aucun gain d’énergie n’est annoncé ici. Un système en veille continue à consommer et sa mesure doit être définie.',
 'Dans le schéma, le calcul complet n’est appelé que si le premier bloc le demande. Il faut choisir ce déclencheur avec soin : bruit et faux réveils peuvent annuler le bénéfice attendu.',source=['C2','C3']),
 E(39,'calibration','Avant d’arrondir : regarder les vraies valeurs','Un format réduit doit couvrir les valeurs utiles sans gaspiller ses niveaux.',[
  'La calibration observe des exemples représentatifs pour choisir des échelles, notamment celles des activations d’un modèle quantifié.',
  'Si une échelle couvre une plage énorme, les petits écarts ont peu de graduations. Une plage trop étroite peut au contraire écrêter, c’est-à-dire bloquer des valeurs aux limites.',
  'Choisir les réglages avec les données prévues pour cela, sans utiliser le test final pour optimiser ces échelles.',
  'Comparer la qualité après conversion. Si elle baisse trop, enquêter sur les couches sensibles ou utiliser un entraînement qui tient compte de la quantification.'],
 ['Exemples représentatifs','Plages observées','Échelles choisies','Qualité à retester'],
 'Une bonne calibration sur des données peu représentatives ne garantit pas le comportement sur de nouvelles situations.',
 'Poids seuls et poids plus activations sont deux expériences différentes. Annoncer ce qui est quantifié, les formats, les échelles, les données de calibration et les routines d’exécution.',source=['S15','C1']),
 E(40,'architecture-cible','Le meilleur réseau dépend aussi de la carte','Choisir l’organisation du réseau fait partie de l’optimisation.',[
  'Une recherche d’architecture compare plusieurs organisations de modèle : largeur des couches, filtres ou blocs utilisés.',
  'Une recherche guidée par le matériel prend en compte les limites ou les performances de la cible, au lieu de regarder seulement le nombre d’opérations.',
  'Deux réseaux de taille proche peuvent avoir des délais différents si les opérations, accès mémoire ou bibliothèques diffèrent.',
  'Commencer modestement : deux ou trois variantes, même protocole, mêmes données de validation et mesure sur la carte. Garder le test final à l’écart du choix.'],
 ['Variantes de réseau','Qualité de validation','Mesures sur cible','Compromis admissible'],
 'Chercher beaucoup de variantes coûte du temps et peut suradapter le choix à la validation. Trois essais ne prouvent pas un optimum global.',
 'On parle de co-conception matériel–logiciel lorsque l’on adapte ensemble l’organisation du calcul et son exécution. MCUNet est un exemple de cette démarche pour des contraintes très serrées.',source=['S8','C1','C3']),
 E(49,'suivi','Après livraison, la maison peut changer','Un autre micro, une autre pièce ou de nouveaux usages peuvent dégrader les résultats.',[
  'Une dérive des données est un changement des entrées reçues au fil du temps. Le système peut alors sortir du domaine évalué.',
  'Prévoir des observations utiles et limitées : défauts du capteur, demandes de confirmation ou erreurs vérifiées. Collecter une conversation entière n’est pas toujours nécessaire ni acceptable.',
  'Une mise à jour doit repasser les tests de qualité, de ressources et d’intégration. Garder une version connue pour pouvoir revenir en arrière.',
  'Les MLOps, opérations des systèmes d’apprentissage, organisent ce cycle : données, versions, déploiement, surveillance et maintenance.'],
 ['Observer sans surcollecter','Détecter un problème','Valider une nouvelle version','Mettre à jour ou revenir'],
 'Le modèle ne se corrige pas tout seul en usage. Une adaptation automatique demanderait un protocole et des protections supplémentaires.',
 'Un changement de distribution n’est pas automatiquement une défaillance. Il faut relier les observations à des critères de service et vérifier les conséquences. Le suivi est une partie du produit, pas seulement un tableau de statistiques.',source=['C5'])
]
