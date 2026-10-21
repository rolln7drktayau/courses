"""Original guided-inquiry workshop, student-facing data only."""

HALF_DAY = [
    (0, 10, 'Se poser la question', 'Chacun écrit sa première réponse ; former les équipes et distribuer les rôles.'),
    (10, 40, 'Construire le socle commun', 'Tous calculent une sortie, comptent les paramètres et identifient les budgets.'),
    (40, 85, 'Enquêter en équipe', 'Une mission : hypothèse, test, source, résultat et limite.'),
    (85, 95, 'Faire une pause', 'Dix minutes incluses.'),
    (95, 120, 'Faire relire sa preuve', 'G1 relit G2, G2 relit G3… G7 relit G1. Répondre à une objection.'),
    (120, 155, 'Enseigner aux autres', 'Sept restitutions de 4 min, puis 1 min de prise de notes chacune.'),
    (155, 180, 'Assembler notre cours', 'Chaque équipe complète les sept lignes de synthèse ; réunir les sept fiches.'),
    (180, 195, 'Vérifier sa compréhension', 'Billet individuel sans support : cinq questions, pas un travail de groupe.'),
    (195, 210, 'Valider et ouvrir la suite', 'Confronter les réponses, corriger les conclusions et formuler une piste pour le TD.'),
]

FULL_DAY = [
    (210, 240, 'Définir l’expérience', 'Choisir une seule hypothèse sur le réseau jouet ; figer entrées, référence et tolérance.'),
    (240, 285, 'Écrire et tester', 'Écrire soi-même l’inférence 2 → 2 → 1 dans son langage ; tester au moins trois entrées calculées à la main.'),
    (285, 295, 'Faire une pause', 'Dix minutes incluses ; la pause déjeuner est en dehors des sept heures.'),
    (295, 340, 'Comparer une variante', 'Modifier un seul facteur ; vérifier les sorties avant les temps. Garder les mêmes poids.'),
    (340, 375, 'Mesurer et, si prêt, transférer', 'Mesurer sur PC. Sur Pi disponible, transférer les sources et reconstruire sur la cible ; sinon annoncer la limite PC.'),
    (375, 400, 'Faire reproduire', 'Une autre équipe relance l’expérience depuis le commit et les consignes. Ne pas classer des PC différents.'),
    (400, 420, 'Conclure en une page', 'Une question, une figure, le résultat, une limite et le prochain test. Aucun gain n’est imposé.'),
]

MISSIONS = [
    dict(id=1, title='Le besoin et son histoire', question='Pourquoi calculer dans un objet plutôt que tout envoyer ailleurs ?',
         concept='Besoin humain · local / passerelle / distant', slides=[3, 4, 5, 6],
         tasks=[
             'Écrire qui utilise le boîtier et ce qui doit continuer pendant une coupure Internet.',
             'Dessiner trois trajets : calcul dans l’objet, sur une passerelle, sur un serveur distant.',
             'Tester ces trajets sur deux conditions : réseau disponible, puis absent. Dire quelle fonction cesse de marcher.',
             'Lire les notices Shakey et ALVINN : personne ou équipe, date, besoin, réponse et limite ; distinguer calcul déporté et calcul à bord.',
             'Proposer un cas où une règle simple ou un calcul distant serait préférable ; rédiger une conclusion conditionnelle.'
         ],
         table='Architecture | Réseau requis | Fonction conservée hors connexion | Donnée transmise | Limite',
         source=('SRI — Shakey ; CMU — ALVINN', 'https://www.sri.com/hoi/shakey-the-robot/'),
         extra=('CMU — ALVINN', 'https://publications.ri.cmu.edu/alvinn-an-autonomous-land-vehicle-in-a-neural-network'),
         expected='Un schéma d’architecture, deux tests de scénario et deux repères historiques reliés à une difficulté.'),
    dict(id=2, title='Le réseau qui apprend', question='Que calcule le réseau et qu’est-ce qui change pendant l’apprentissage ?',
         concept='Poids · biais · activation · perte · gradient', slides=[7, 8, 9, 13],
         tasks=[
             'Tracer les deux couches du réseau jouet et distinguer poids, biais, activations et sortie.',
             'Calculer à la main pour (x₁,x₂) = (1,2), (2,1) et (0,0), puis comparer avec la manipulation HTML.',
             'Pour la cible c = 2 et l’entrée (1,2), calculer L = (ŷ − c)² et la pente 2(ŷ − c)h₂ du seul poids de sortie w.',
             'Tester trois pas η = 0,05 ; 0,1 ; 1 dans la démonstration. Noter poids, sortie et perte après correction.',
             'Expliquer pourquoi une perte qui diminue sur un exemple ne démontre pas une bonne généralisation.'
         ],
         table='Entrée ou pas η | Sortie avant | Sortie après | Perte | Calcul / observation | Limite',
         source=('CS231n — réseaux et apprentissage', 'https://cs231n.github.io/neural-networks-1/'),
         extra=('Cours : une correction de poids', '../index.html#slide=9'),
         expected='Trois sorties vérifiées et trois pas comparés ; une phrase qui distingue apprentissage et inférence.'),
    dict(id=3, title='Les données et les erreurs', question='Comment éviter de se convaincre avec un test trop facile ?',
         concept='Fenêtre · normalisation · séparation · généralisation', slides=[10, 11, 28],
         tasks=[
             'Ouvrir data/toy-series.csv dans un tableur ou un éditeur. Il contient trois séquences illustratives, pas le jeu du TD.',
             'Dans la séquence A, construire les fenêtres t=0..2 et t=1..3 ; leur cible est la valeur juste après la fenêtre.',
             'Marquer les observations partagées. Expliquer le risque si ces fenêtres sont séparées au hasard entre apprentissage et test.',
             'Proposer une séparation par séquence A/B/C. Décrire quelles observations servent à calculer moyenne et écart-type.',
             'Proposer un test avec bruit, changement d’échelle ou valeur manquante ; préciser ce qu’on peut conclure sans avoir entraîné de modèle.'
         ],
         table='Fenêtre | Instants lus | Cible | Partie choisie | Chevauchement | Risque',
         source=('Google — séparation des données', 'https://developers.google.com/machine-learning/crash-course/overfitting/dividing-datasets'),
         extra=('Cours : séparer avant fenêtrage', '../index.html#slide=10'),
         expected='Deux fenêtres annotées, une séparation justifiée et un test de robustesse ; aucune précision de modèle inventée.'),
    dict(id=4, title='La mémoire de la boîte', question='Qu’est-ce qui doit réellement tenir en mémoire en même temps ?',
         concept='Flash · RAM · objets vivants · pic mémoire', slides=[15, 16, 19],
         tasks=[
             'Lire la carte mémoire fictive commune. Dessiner tous les objets déclarés simultanément présents en RAM.',
             'Calculer leur somme et comparer au budget de 128 Kio. Distinguer ce calcul d’une mesure de firmware.',
             'Compter le stockage brut des neuf paramètres FP32 du réseau jouet, en Flash dans ce scénario.',
             'Proposer une réutilisation qui ferait passer le tampon de traitement de 24 à 16 Kio ; préciser quelles durées de vie il faudrait vérifier.',
             'Lire le résumé ou le schéma MCUNetV2. Expliquer le lien entre découpage du calcul, mémoire économisée et calcul éventuellement ajouté.'
         ],
         table='Objet | Flash ou RAM | Taille | Présent au pic ? | Justification | Variante proposée',
         source=('Lin et al. — MCUNetV2', 'https://arxiv.org/abs/2110.15352'),
         extra=('Cours : poids et travail SRAM', '../index.html#slide=16'),
         expected='Une carte mémoire et deux totaux ; une optimisation proposée avec sa condition de validité, pas un gain présenté comme mesuré.'),
    dict(id=5, title='Le temps et l’énergie', question='Une opération plus rapide rend-elle le service plus rapide et plus sobre ?',
         concept='Protocole · dispersion · gain global · énergie', slides=[17, 18, 24, 25, 26],
         tasks=[
             'Avant de lancer la micro-expérience, prédire laquelle des deux sommes sera plus rapide et pourquoi.',
             'Lancer la mesure du navigateur, exporter les 14 lignes CSV et relever médiane et min–max des deux variantes.',
             'Noter navigateur, date, protocole et nom du CSV. Ne transformer ces durées ni en cycles MCU ni en joules.',
             'Profil fictif : 100 ms au total, dont 20 ms dans une brique. Recalculer le total si cette brique est deux fois plus rapide.',
             'Calcul fictif distinct : 0,1 W pendant 0,02 s. Calculer l’énergie ; indiquer ce qu’il faudrait instrumenter pour la mesurer sur carte.'
         ],
         table='Variante | Prévision | Médiane et unité | Min–max | Conditions | Conclusion permise',
         source=('MLCommons — méthodologie Tiny', 'https://mlcommons.org/benchmarks/inference-tiny/'),
         extra=('Lancer la micro-expérience', '../index.html#slide=24'),
         expected='Le CSV réel du navigateur, un tableau de temps et deux calculs clairement étiquetés comme fictifs.'),
    dict(id=6, title='Les nombres et la précision', question='Que gagne-t-on, et que perd-on, quand on stocke moins de bits ?',
         concept='Quantification · échelle · erreur · noyau matériel', slides=[21, 22, 23],
         tasks=[
             'Utiliser les six poids du réseau jouet : 1, −1, 0,5, 0,5, 2, 1. Garder les trois biais à zéro en FP32.',
             'Prendre s = 2/127 ; calculer q = arrondi(w/s), borné entre −127 et 127, puis ŵ = s×q pour les poids 0,5 ; 1 ; 2.',
             'Noter l’écart |ŵ−w| et distinguer erreur d’arrondi, erreur de sortie et erreur de prédiction sur des données.',
             'Comparer le stockage des six poids FP32 à six entiers INT8 et une échelle FP32 commune ; garder les trois biais FP32 dans les deux cas.',
             'Chercher dans Jacob et al. ce qui rend une inférence entière exécutable. Expliquer pourquoi cette économie de stockage ne prouve pas un gain de temps ou de RAM.'
         ],
         table='Poids w | Échelle s | Code q | Reconstruit ŵ | Écart | Statut : calcul',
         source=('Jacob et al. — quantification entière', 'https://arxiv.org/abs/1712.05877'),
         extra=('Cours : quantifier sur une grille', '../index.html#slide=22'),
         expected='Trois arrondis, deux budgets de stockage incluant échelle et biais, et une limite matérielle expliquée.'),
    dict(id=7, title='La preuve et la confiance', question='Qu’est-ce qui rend une conclusion vérifiable par quelqu’un d’autre ?',
         concept='Reproductibilité · tests · provenance · risques', slides=[27, 28, 29, 30],
         tasks=[
             'Écrire l’hypothèse « le plus petit code est le plus rapide ». Choisir une observation qui pourrait la contredire.',
             'Relancer deux fois la micro-expérience dans le même navigateur et conserver les deux CSV ; comparer les médianes et dispersions sans inventer la cause des écarts.',
             'Écrire un manifeste minimal : code/commit, entrée, version, cible réelle, timer, répétitions et fichiers bruts.',
             'Définir trois tests : entrée normale, valeur manquante et redémarrage. Pour chacun, écrire la sortie ou le repli attendu.',
             'Proposer un test automatique de correction et expliquer pourquoi un succès de CI ne certifie ni performance sur carte ni sûreté du produit.'
         ],
         table='Affirmation | Test qui peut la contredire | Trace conservée | Résultat | Limite',
         source=('MLPerf Tiny — protocole reproductible', 'https://arxiv.org/abs/2106.07597'),
         extra=('Cours : tracer une expérience', '../index.html#slide=29'),
         expected='Deux CSV réels, un manifeste et trois tests ; séparer résultat vérifié, hypothèse et explication encore à tester.'),
]

EXIT = [
    ('2 points', 'Donnez une raison d’embarquer le calcul et un cas où une règle ou un serveur serait préférable.'),
    ('2 points', 'Pour (x₁,x₂)=(2,1), calculez h₁, h₂ et ŷ. Distinguez un poids d’une activation.'),
    ('2 points', 'RAM fictive : 60 + 32 + 16 + 8 + 8 Kio simultanés ; capacité 128 Kio. Le budget est-il respecté ? Que change le placement des poids en Flash ?'),
    ('1 point', 'Un programme prend 100 ms, dont 40 ms dans une brique. Cette brique devient deux fois plus rapide : quel est le nouveau total ?'),
    ('1 point', 'Pourquoi le CSV du navigateur ne prouve-t-il pas un gain sur Pi ? Proposez la prochaine vérification.'),
]

SCHEMA = 'inem-embedded-ai-workshop/1'

assert HALF_DAY[-1][1] == 210
assert FULL_DAY[-1][1] == 420
assert all(a[1] == b[0] for a, b in zip(HALF_DAY, HALF_DAY[1:]))
assert len(MISSIONS) == 7
