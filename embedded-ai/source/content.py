"""Original course content and primary-source reading guide, Roland Cédric TAYO."""
REFERENCES = [
    dict(id='R01',authors='Dean Pomerleau',year='1989',title='ALVINN: An Autonomous Land Vehicle In a Neural Network',status='Repère historique · publication CMU / actes NeurIPS',url='https://publications.ri.cmu.edu/alvinn-an-autonomous-land-vehicle-in-a-neural-network',takeaway='Relier perception apprise et action à bord d’un véhicule.',limit='Démonstrateur historique ; ni autonomie générale ni exécution sur microcontrôleur.'),
    dict(id='R02',authors='Andrew G. Howard et al.',year='2017',title='MobileNets: Efficient Convolutional Neural Networks for Mobile Vision Applications',status='Article fondateur · arXiv 1704.04861',url='https://arxiv.org/abs/1704.04861',takeaway='Séparer convolution spatiale et mélange des canaux pour réduire le calcul.',limit='Moins de MAC ne garantit pas la même réduction de latence sur chaque cible.'),
    dict(id='R03',authors='Benoit Jacob et al.',year='2018',title='Quantization and Training of Neural Networks for Efficient Integer-Arithmetic-Only Inference',status='CVPR 2018 · prépublication 2017',url='https://arxiv.org/abs/1712.05877',takeaway='Co-concevoir quantification, apprentissage et noyaux entiers.',limit='Le format des poids, des activations et des accumulateurs doit être distingué.'),
    dict(id='R04',authors='Ji Lin, Wei-Ming Chen et al.',year='2020',title='MCUNet: Tiny Deep Learning on IoT Devices',status='NeurIPS 2020',url='https://arxiv.org/abs/2007.10319',takeaway='Chercher ensemble l’architecture du réseau et son moteur d’exécution.',limit='Résultats sur des cibles et tâches précises, pas une capacité universelle des MCU.'),
    dict(id='R05',authors='Ji Lin, Wei-Ming Chen, Han Cai et al.',year='2021',title='MCUNetV2: Memory-Efficient Patch-based Inference for Tiny Deep Learning',status='NeurIPS 2021',url='https://arxiv.org/abs/2110.15352',takeaway='Traiter des morceaux de carte de caractéristiques pour réduire le pic mémoire.',limit='Les recouvrements peuvent ajouter du calcul ; l’ordonnancement compte.'),
    dict(id='R06',authors='Ji Lin, Ligeng Zhu et al.',year='2022',title='On-Device Training Under 256KB Memory',status='NeurIPS 2022',url='https://arxiv.org/abs/2206.15472',takeaway='Rendre possible une adaptation locale par mises à jour sélectives et co-conception.',limit='Il ne s’agit pas d’entraîner librement n’importe quel réseau dans 256 Ko.'),
    dict(id='R07',authors='Tri Dao, Daniel Y. Fu et al.',year='2022',title='FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness',status='NeurIPS 2022',url='https://arxiv.org/abs/2205.14135',takeaway='Réorganiser le calcul d’attention pour réduire les échanges mémoire sur GPU.',limit='Attention exacte à l’arrondi près ; les résultats GPU ne décrivent pas un MCU.'),
    dict(id='R08',authors='Si-An Chen et al.',year='2023',title='TSMixer: An All-MLP Architecture for Time Series Forecasting',status='Transactions on Machine Learning Research, 2023',url='https://arxiv.org/abs/2303.06053',takeaway='Mélanger les instants puis les variables avec des perceptrons multicouches.',limit='Le réseau du TD est une réduction pédagogique, pas une reproduction de l’article.'),
    dict(id='R09',authors='Ji Lin, Jiaming Tang et al.',year='2024',title='AWQ: Activation-aware Weight Quantization for LLM Compression and Acceleration',status='MLSys 2024 · prépublication 2023',url='https://arxiv.org/abs/2306.00978',takeaway='Utiliser des statistiques d’activation pour mieux préserver les canaux sensibles.',limit='Quantifier les poids ne signifie pas quantifier toute la mémoire ni tous les calculs.'),
    dict(id='R10',authors='Danfeng Qin et al.',year='2024',title='MobileNetV4 — Universal Models for the Mobile Ecosystem',status='ECCV 2024',url='https://arxiv.org/abs/2404.10518',takeaway='Concevoir des blocs et une recherche d’architecture adaptés à plusieurs matériels mobiles.',limit='L’écosystème mobile évalué ne couvre pas tous les microcontrôleurs.'),
    dict(id='R11',authors='Jianyu Wei, Shijie Cao et al.',year='2025',title='T-MAC: CPU Renaissance via Table Lookup for Low-Bit LLM Deployment on Edge',status='EuroSys 2025 · prépublication 2024',url='https://arxiv.org/abs/2407.00088',takeaway='Remplacer certaines opérations de produits mixtes par des tables de recherche adaptées.',limit='Bénéfices dépendants du bit-width, des noyaux, des formes et des matériels comparés.'),
    dict(id='R12',authors='Loubna Ben Allal et al.',year='2025',title='SmolLM2: When Smol Goes Big — Data-Centric Training of a Small Language Model',status='Prépublication arXiv 2502.02737',url='https://arxiv.org/abs/2502.02737',takeaway='La qualité et le mélange des données comptent aussi pour les petits modèles de langage.',limit='« Petit » à 1,7 milliard de paramètres reste immense pour un MCU.'),
    dict(id='R13',authors='Jianyu Wei, Qingtao Li et al.',year='2025',title='T-MAN: Enabling End-to-End Low-Bit LLM Inference on NPUs via Unified Table Lookup',status='Prépublication arXiv · 14 novembre 2025',url='https://arxiv.org/abs/2511.11248',takeaway='Adapter tables, tuilage et pipeline aux opérations réellement prises en charge par un NPU.',limit='Résultats propres aux systèmes étudiés ; le statut de publication évaluée n’est pas établi ici.'),
    dict(id='R14',authors='Emre Can Kizilates',year='2026',title='From Compression to Deployment: Real-Time and Energy-Efficient FastGRNN on Ultra-Constrained Microcontrollers',status='Prépublication arXiv · 15 juin 2026',url='https://arxiv.org/abs/2606.17249',takeaway='Étudier ensemble compression, activation par table, état récurrent et déploiement physique.',limit='Étude particulière ; variabilité entre graines et temps de mise en régime à examiner.'),
    dict(id='R15',authors='Ajay Kumar M et al.',year='2026',title='A Framework for Accelerating Transformer Inference on RISC-V for Edge AI',status='Prépublication arXiv · 6 octobre 2026',url='https://arxiv.org/abs/2610.08688',takeaway='Adapter instructions et compilation à des Transformers compacts, principalement encodeurs.',limit='Modifier un cœur RISC-V est un travail matériel ; ce gain n’est pas un simple correctif logiciel.'),
    dict(id='R16',authors='Apostol Vassilev, Alina Oprea et al.',year='2025',title='Adversarial Machine Learning: A Taxonomy and Terminology of Attacks and Mitigations',status='Rapport technique NIST AI 100-2e2025',url='https://doi.org/10.6028/NIST.AI.100-2e2025',takeaway='Distinguer attaques sur données, entrées, modèles et vie privée.',limit='Une taxonomie et des contre-mesures ne garantissent pas la sécurité d’un produit.'),
    dict(id='R17',authors='Ji Lin, Ligeng Zhu, Wei-Ming Chen, Wei-Chen Wang, Song Han',year='2023 / 2024',title='Tiny Machine Learning: Progress and Futures',status='IEEE Circuits and Systems Magazine 2023 · dépôt arXiv 2024',url='https://arxiv.org/abs/2403.19076',takeaway='Vue d’ensemble de la co-conception et du passage de l’inférence à l’adaptation locale.',limit='Date de dépôt arXiv et date de publication diffèrent ; ce panorama n’est pas un état exhaustif 2026.'),
    dict(id='R18',authors='Colby Banbury, Vijay Janapa Reddi et al.',year='2021',title='MLPerf Tiny Benchmark',status='NeurIPS 2021 · Datasets and Benchmarks',url='https://arxiv.org/abs/2106.07597',takeaway='Comparer qualité, latence et énergie avec un protocole reproductible.',limit='Respecter la tâche, le périmètre et les règles ; ne pas comparer seulement des scores isolés.'),
    dict(id='R19',authors='Arm',year='Documentation consultée en 2026',title='CMSIS-NN — Efficient neural network kernels for Arm Cortex-M',status='Dépôt officiel de noyaux optimisés',url='https://github.com/ARM-software/CMSIS-NN',takeaway='Les performances dépendent de noyaux adaptés à l’ISA et aux formats quantifiés.',limit='Une bibliothèque ne supprime pas les limites mémoire ou les vérifications de l’application.'),
    dict(id='R20',authors='Google AI Edge',year='Documentation consultée en 2026',title='LiteRT for Microcontrollers',status='Documentation officielle du moteur MCU',url='https://developers.google.com/edge/litert/microcontrollers/overview',takeaway='Déployer un sous-ensemble d’opérateurs avec une allocation adaptée au microcontrôleur.',limit='Vérifier les opérations, types et cibles pris en charge ; conversion n’est pas validation.'),
    dict(id='R21',authors='MLCommons',year='Documentation consultée en 2026',title='MLPerf Inference: Tiny',status='Méthodologie et résultats officiels',url='https://mlcommons.org/benchmarks/inference-tiny/',takeaway='Lire conjointement qualité, scénario de mesure et configuration matérielle.',limit='Aucun chiffre de classement en temps réel n’est repris dans ce support.'),
    dict(id='R22',authors='SRI International',year='1966–1972',title='Shakey the Robot',status='Histoire du projet · organisme concepteur',url='https://www.sri.com/hoi/shakey-the-robot/',takeaway='Faire percevoir un environnement et planifier des actions à un robot mobile.',limit='Repère d’IA en interaction avec le monde physique, pas un exemple de calcul entièrement à bord.'),
    dict(id='R23',authors='NIST',year='Documentation consultée en 2026',title='Edge AI',status='Programme de recherche officiel',url='https://www.nist.gov/programs-projects/edge-ai',takeaway='Rapprocher l’inférence ou l’apprentissage des données et des usages.',limit='Ressources, communications, données, confidentialité et sécurité restent des difficultés ; local ne signifie pas automatiquement sûr.'),
]

SLIDES=[]
def slide(ch,title,lead,points,visual,minutes,refs=(),detail='',kind='',quiz=None):
    SLIDES.append(dict(chapter=ch,title=title,lead=lead,points=points,visual=visual,minutes=minutes,
                       refs=list(refs),detail=detail,kind=kind,quiz=quiz))

# Chapter 1: 27 minutes. Begin with a person's need, then architecture and history.
slide('01 · Comprendre le besoin','Faire tenir l’IA\ndans le monde réel.',
      'IA pour les systèmes embarqués · Du besoin humain à la preuve · 3 heures',
      ['Roland Cédric TAYO'],
      'hero',2,kind='hero',detail='Le point de départ est une personne qui attend un service : comprendre une commande, reconnaître un objet ou être avertie à temps. Nous allons décider si une IA aide, où placer son calcul, puis comment la rendre compatible avec le matériel. Les sources et le TD sont accessibles par Ressources ; Plan & questions donne accès aux cinq questions directrices et aux cinq quiz.')
slide('01 · Comprendre le besoin','Les cinq questions du cours.',
      'Un besoin humain → un choix technique → une preuve sur le matériel.',
      ['<b>1. Pour qui et pour quoi ?</b> Définir le service attendu.',
       '<b>2. Pourquoi une IA ?</b> Comprendre ce qu’elle apprend et calcule.',
       '<b>3. Pourquoi à bord ?</b> Choisir le lieu et le budget du calcul.',
       '<b>4. Comment la faire tenir ?</b> Réduire ses coûts sans perdre le service.',
       '<b>5. Comment lui faire confiance ?</b> Tester, mesurer et prévoir ses erreurs.'],
      'route',3,kind='guide',detail='Ces cinq questions structurent les cinq chapitres. Elles ne sont pas les cinq quiz : les quiz sont cinq courtes mises en situation, numérotées et accessibles depuis Plan & questions. Cliquer sur une réponse affiche son explication. Prérequis : tableaux, fonctions, boucles, vecteurs et bases CPU/mémoire. Les 180 minutes incluent les échanges et dix minutes de pause.')
slide('01 · Comprendre le besoin','Un besoin simple : se faire\ncomprendre par un objet.',
      'Exemple : une personne veut allumer une lampe en disant « lumière ».',
      ['<b>La personne :</b> elle veut agir sans utiliser ses mains.',
       '<b>La difficulté :</b> les voix et le bruit changent ; le son n’est jamais identique.',
       '<b>Le service attendu :</b> reconnaître la commande, ou la refuser en cas de doute.'],
      'human_need',4,detail='Cet exemple illustre le raisonnement, sans imposer un nouveau projet ni du matériel audio pour le TD. Un interrupteur peut suffire si le besoin ne justifie pas la voix. Si la voix apporte une aide, il faut traiter les accents, les bruits, les fausses activations et une commande manuelle de secours. Reconnaître un mot court ne demande pas nécessairement un grand modèle de langage.')
slide('01 · Comprendre le besoin','Pourquoi ne pas tout\nenvoyer à un serveur ?',
      'Embarquer une IA, c’est exécuter son calcul dans l’objet ou à proximité de ses données.',
      ['<b>Répondre à temps :</b> éviter un aller-retour réseau quand le délai compte.',
       '<b>Rester utile hors connexion :</b> la commande peut fonctionner sans Internet.',
       '<b>Limiter les échanges :</b> conserver l’audio localement si le système le permet.'],
      'placement',4,refs=['R23'],detail='Un serveur distant peut offrir davantage de calcul et simplifier certaines mises à jour. Le local peut réduire les échanges, mais il faut mesurer énergie et délai de la chaîne entière. Il ne garantit pas à lui seul la confidentialité : stockage, mises à jour et accès doivent aussi être protégés. Une architecture hybride partage les fonctions et précise ce qui reste possible hors connexion. L’inférence peut être locale même si l’entraînement a eu lieu sur PC ou serveur.')
slide('01 · Comprendre le besoin','D’où vient ce besoin\nd’agir dans le monde réel ?',
      'Trois repères, pas un inventeur unique : percevoir, apprendre, puis réduire le coût.',
      ['<b>1966–1972 · SRI, Shakey :</b> percevoir une pièce et planifier un déplacement.',
       '<b>1989 · Dean Pomerleau, ALVINN :</b> apprendre à suivre une route à partir d’images.',
       '<b>2017 · Howard et al., MobileNets :</b> rendre la vision moins coûteuse sur mobile.'],
      'history1',4,refs=['R22','R01','R02'],detail='Le besoin naît de tâches physiques utiles, pas du désir de miniaturiser tous les modèles. Shakey, développé à SRI de 1966 à 1972, planifie des actions ; son calcul n’est pas entièrement embarqué. C’est un ancêtre de la question, pas du TinyML. ALVINN utilise un réseau sur un véhicule équipé d’ordinateurs et réussit sous certaines conditions, sans autonomie générale. MobileNets réduit le calcul de la vision mobile. Ces étapes ne représentent pas toute l’histoire de l’automatique, de la robotique ou de l’IA embarquée.')
slide('01 · Comprendre le besoin','Des IA locales existent.\nPourquoi pas dans chaque objet ?',
      'Une démonstration qui fonctionne ne suffit pas à livrer un service fiable.',
      ['<b>Ce qui a progressé :</b> petits réseaux, calcul entier et moteurs adaptés aux puces.',
       '<b>Ce qui bloque :</b> mémoire, batterie, délai et erreurs en conditions réelles.',
       '<b>Ce que l’on cherche :</b> adapter ensemble le modèle, le logiciel et le matériel.'],
      'barriers',4,refs=['R04','R17','R23'],detail='MCUNet, en 2020, associe recherche d’architecture et moteur pour faire tenir certaines tâches de vision sur MCU. Aujourd’hui, reconnaissance de mots, vision et prédiction peuvent être locales, selon la tâche et la cible ; un LLM reste une autre échelle de ressources. Données insuffisantes, changement d’environnement, coût de maintenance et conséquences d’une erreur peuvent rendre l’IA inadaptée. Les pistes de recherche étudiées ensuite sont la réduction des formats, les échanges mémoire, les noyaux spécialisés, l’adaptation locale et des protocoles de validation reproductibles. Il faut aussi pouvoir conclure qu’une règle ou un traitement distant convient mieux.')
slide('01 · Comprendre le besoin','Une IA est-elle\nvraiment nécessaire ?',
      'On choisit une méthode à partir du problème, puis on vérifie son utilité.',
      ['<b>Règle simple :</b> un seuil ou un bouton suffit-il ?',
       '<b>Modèle appris :</b> reconnaître des variations que l’on décrit mal par des règles.',
       '<b>Décision finale :</b> gérer l’incertitude et garder une solution de repli.'],
      'tasks',3,detail='Classer signifie choisir une catégorie, par exemple un mot. La régression estime une valeur, comme dans le TD de prédiction de signaux. Une décision est l’action choisie à partir du résultat et des contraintes. Un score n’est pas nécessairement une probabilité fiable. Comparer au départ une règle, un filtre ou un modèle linéaire ; le réseau doit apporter un service utile au regard de son coût et de ses erreurs.')
slide('01 · Comprendre le besoin','Quiz 1 / 5 · Sans Internet,\nque doit-il rester possible ?',
      'La commande vocale de la lampe doit fonctionner pendant une coupure Internet.',
      [],'quiz',3,kind='quiz',quiz=dict(options=['Utiliser seulement un modèle distant, même pendant la coupure.','Reconnaître la commande localement et garder une commande manuelle.','Réduire les poids du modèle distant sans changer son emplacement.'],correct=1,answer='La fonction exigée pendant la coupure doit avoir un chemin local. La commande manuelle permet de garder la main en cas d’erreur.'),detail='Une fonction distante facultative peut rester indisponible pendant la coupure. On ne demande pas de tout embarquer : on définit précisément le service qui doit continuer et le comportement en cas d’entrée inconnue. Revenir au besoin de la personne avant de choisir un modèle.')

# Chapter 2: 40 minutes.
slide('02 · Lire les briques','Une prédiction traverse\nune chaîne entière.',
      'Le modèle n’est qu’une partie du temps et de la mémoire consommés.',
      ['<b>Entrée :</b> échantillonner, synchroniser et vérifier.',
       '<b>Calcul :</b> préparer les données puis exécuter le graphe.',
       '<b>Sortie :</b> interpréter, surveiller et agir.'],
      'pipeline',3,detail='Un capteur mal horodaté ou une normalisation incohérente peut dégrader une bonne architecture. Définir les interfaces : forme des tableaux, ordre des canaux, unités, fréquence et traitement des valeurs absentes. Le budget doit couvrir toute cette chaîne.')
slide('02 · Lire les briques','Brique 1 · Les données\ndéfinissent ce que l’on apprend.',
      'Séparer les séquences avant de fabriquer les fenêtres.',
      ['<b>Apprentissage :</b> ajuster poids et normalisation.',
       '<b>Validation :</b> choisir les réglages.',
       '<b>Test réservé :</b> évaluer après avoir figé les choix.'],
      'split',4,refs=['R08','R12'],detail='Deux fenêtres proches partagent presque les mêmes mesures. Les répartir au hasard entre apprentissage et test peut donner une impression trompeuse de généralisation. Selon le cas réel, séparer aussi machines, personnes ou périodes. La normalisation du test ne doit pas réajuster les statistiques d’apprentissage.')
slide('02 · Lire les briques','Brique 2 · Le produit dense :\nmultiplier, puis additionner.',
      'Un même calcul revient dans les petits réseaux, les convolutions et les Transformers.',
      ['<b>Poids W :</b> coefficients appris ; <b>entrée x :</b> observations.',
       '<b>Biais b :</b> décalage ajouté à chaque sortie.',
       '<b>Coût :</b> m × n MAC pour n entrées et m sorties.'],
      'dense',5,refs=['R11'],detail='Un MAC est une multiplication suivie d’une accumulation. Selon la convention, il peut être compté comme deux opérations flottantes ; toujours préciser l’unité. Une projection y=Wx+b de 3 entrées vers 2 sorties utilise 6 MAC, puis les biais. Les poids sont appris sur PC et relus lors de chaque inférence.')
slide('02 · Lire les briques','Brique 3 · Transformer\net conserver l’information.',
      'Activation, connexion résiduelle et normalisation ont des rôles différents.',
      ['<b>ReLU :</b> max(0, x), pour introduire une non-linéarité.',
       '<b>Résidu :</b> x + f(x), pour ajouter une correction apprise.',
       '<b>Normalisation :</b> stabiliser une échelle ; son coût dépend de sa forme.'],
      'residual',4,detail='Une connexion résiduelle conserve l’entrée jusqu’à l’addition : elle peut prolonger la vie d’un buffer. En inférence, une BatchNorm à statistiques figées peut souvent être absorbée dans la couche précédente. Une LayerNorm dépend de l’entrée courante et ne se fusionne pas de la même manière. Une exponentielle ou une racine peut rester coûteuse selon les instructions disponibles.')
slide('02 · Lire les briques','Brique 4 · La convolution\nréutilise un petit motif.',
      'Une convolution séparée découpe le filtrage spatial et le mélange des canaux.',
      ['<b>Classique :</b> chaque sortie combine espace et canaux.',
       '<b>Depthwise + 1×1 :</b> filtrer chaque canal, puis les mélanger.',
       '<b>À vérifier :</b> moins de MAC peut encore produire plus de transferts.'],
      'convolution',5,refs=['R02','R10'],detail='Exemple à mêmes dimensions spatiales, filtre 3×3, 32 canaux d’entrée et 64 de sortie : 18 432 MAC par position en convolution classique ; 2 336 en depthwise suivie de 1×1, soit environ 7,9 fois moins. Cela ignore ici effets de bord et biais. Ce ratio arithmétique n’est pas un facteur de vitesse matériel. Pooling et réduction globale peuvent aussi diminuer la taille des cartes à transmettre à une tête dense.')
slide('02 · Lire les briques','Brique 5 · Un état mémorise\nune partie du passé.',
      'Un réseau récurrent met à jour un petit état à chaque échantillon.',
      ['<b>État h :</b> résumé réutilisé au pas suivant.',
       '<b>Intérêt :</b> traiter un flux sans garder tout son historique.',
       '<b>Limite :</b> dépendance séquentielle, dérive et temps de mise en régime.'],
      'recurrent',5,refs=['R14'],detail='Schéma simplifié : h_t=f(Wx_t+Uh_(t−1)). t est le pas courant, W et U sont des poids et f une activation. Dans un système à état, le coût d’un appel ne donne pas le délai nécessaire avant une prédiction fiable après démarrage. Le Mixer du TD utilise au contraire une fenêtre explicite de 16 instants ; il n’est pas un réseau récurrent.')
slide('02 · Lire les briques','Brique 6 · L’attention choisit\nquelles relations regarder.',
      'Au lieu d’un mélange fixe, les relations dépendent du contenu de l’entrée.',
      ['<b>Q, K, V :</b> requêtes, clés et valeurs calculées par projections.',
       '<b>Comparer :</b> associer chaque position à d’autres positions.',
       '<b>Coût :</b> une matrice naïve de scores grandit comme le carré de la longueur.'],
      'attention',4,refs=['R07'],detail='L’attention standard s’écrit softmax(QKᵀ/√d)V : d est la dimension d’une tête et softmax normalise chaque ligne de scores. FlashAttention réorganise cette attention exacte en réduisant les échanges mémoire sur GPU. Il ne rend pas toutes les couches gratuites et n’établit pas le même gain sur MCU. Le TD ne contient aucune attention.')
slide('02 · Lire les briques','Brique 7 · Le contexte\nconsomme aussi de la mémoire.',
      'Un cache KV évite de recalculer d’anciennes clés et valeurs lors de la génération.',
      ['<b>Préremplissage :</b> traiter la consigne initiale.',
       '<b>Décodage :</b> produire ensuite un token à la fois.',
       '<b>Conséquence :</b> réduire les poids ne réduit pas automatiquement le cache.'],
      'kv',3,detail='Exemple pédagogique, lot de taille 1 : mémoire KV = 2 × nombre de couches × tokens conservés × têtes KV × dimension d’une tête × octets par valeur. Avec 16 couches, 4 têtes KV, 64 valeurs par tête et FP16 (2 octets), 1024 tokens occupent 16 Mio. Les architectures à états, fenêtres glissantes ou cache compressé changent ce budget. Le cache d’un modèle ne se déduit pas seulement de son nombre de paramètres.')
slide('02 · Lire les briques','Brique 8 · Apprendre demande\nplus que prédire.',
      'L’inférence lit les poids ; l’apprentissage calcule aussi comment les changer.',
      ['<b>Perte :</b> mesurer l’erreur entre prédiction et cible.',
       '<b>Gradient :</b> calculer la sensibilité de cette erreur aux poids.',
       '<b>Mise à jour :</b> corriger les poids avec un petit pas.'],
      'training',3,refs=['R06'],detail='Mise à jour : θ ← θ − η∇L. θ désigne les paramètres ; η le pas ; L la perte ; ∇L ses dérivées. Le calcul arrière a besoin de valeurs intermédiaires et de gradients, parfois d’un état d’optimiseur. Lin, Zhu et al. étudient en 2022 des mises à jour sélectives et un moteur adapté pour un budget de 256 Ko de SRAM. Ce n’est pas un entraînement général sans contraintes.')
slide('02 · Lire les briques','Quiz 2 / 5 · « 4 bits »\nveut-il dire « tout petit » ?',
      'Les poids passent de 16 à 4 bits. Le cache KV, les activations et le runtime sont inchangés.',
      [],'quiz',4,kind='quiz',quiz=dict(options=['Toute la RAM est forcément divisée par quatre.','Le stockage brut des poids est divisé par quatre ; le reste doit être recompté.','Le modèle produit forcément quatre fois plus de sorties.'],correct=1,answer='Le ratio concerne seulement le payload des poids, avant métadonnées. Cache, activations, buffers et noyaux peuvent imposer un autre plafond mémoire ou temps.'),detail='Un format de stockage ne définit pas à lui seul le format de calcul. Des poids INT4 peuvent être utilisés avec des activations FP16, puis décompressés par un noyau. La vitesse dépend aussi du décodage, des accès mémoire et du matériel.')

# Chapter 3: 30 minutes, followed by a 10-minute break.
slide('03 · Lire la cible','Un MCU, un Pi et un NPU\nne posent pas le même problème.',
      'Choisir une famille de cible avant de recopier un résultat de papier.',
      ['<b>MCU :</b> petite SRAM, Flash, souvent sans système Linux.',
       '<b>Processeur Linux :</b> RAM plus grande, caches, services et ordonnancement.',
       '<b>GPU / NPU :</b> parallélisme spécialisé, formats et opérations imposés.'],
      'hardware',4,refs=['R19','R20'],detail='CPU = processeur général ; MCU = microcontrôleur ; GPU = processeur graphique ; NPU = accélérateur de réseaux ; DSP = processeur de signal. Un SoC peut en réunir plusieurs. SIMD traite plusieurs valeurs avec une instruction. DMA déplace des données sans piloter chaque copie par le CPU ; la bande passante et la synchronisation restent à gérer. Les TOPS annoncés ne représentent pas automatiquement votre précision, sparsité et graphe.')
slide('03 · Lire la cible','La mémoire a plusieurs adresses\net plusieurs durées de vie.',
      'Poids stockés, valeurs intermédiaires et pic de travail sont trois questions.',
      ['<b>Flash :</b> programme et constantes conservés hors alimentation.',
       '<b>SRAM / RAM :</b> buffers, pile, données en cours de calcul.',
       '<b>Pic :</b> somme des objets vivants au même instant, pas de tous les objets du graphe.'],
      'memory',5,refs=['R05'],detail='Un tableau de poids constant peut rester en Flash sur un MCU ; un autre système peut charger le modèle en RAM. Vérifier le linker et le runtime. Réutiliser un buffer seulement après sa dernière lecture. Le résidu peut empêcher une réutilisation trop précoce. Une estimation des buffers n’est pas une mesure de pile ni un pic SRAM complet.')
slide('03 · Lire la cible','Le calcul peut attendre\nla mémoire.',
      'Compter les opérations ne suffit pas : il faut les alimenter en données.',
      ['<b>Réemploi :</b> utiliser plusieurs fois une donnée déjà proche du cœur.',
       '<b>Localité :</b> parcourir les adresses dans un ordre favorable.',
       '<b>Borne utile :</b> comparer temps de calcul et temps de transfert.'],
      'roofline',5,refs=['R07'],detail='Borne simplifiée : T ≥ max(N_MAC / débit_MAC, octets transférés / bande passante). T est le temps ; N_MAC le nombre de MAC ; les débits sont soutenus dans le périmètre étudié. Ce modèle ignore synchronisations et autres surcoûts. Le tuilage découpe un calcul en morceaux réutilisables ; sa meilleure taille dépend des registres, caches et mémoires. FlashAttention illustre l’idée sur GPU, sans constituer un noyau MCU universel.')
slide('03 · Lire la cible','Un temps moyen ne garantit\npas une échéance.',
      'La sortie doit être disponible à temps, même quand le système est occupé.',
      ['<b>Latence :</b> délai pour une entrée ; <b>débit :</b> sorties par seconde.',
       '<b>Gigue :</b> variation de ce délai entre les appels.',
       '<b>Temps réel :</b> définir l’échéance, la surcharge et le repli.'],
      'deadline',4,detail='Mesurer médiane, dispersion et percentiles élevés selon le nombre d’observations. Le pire cas observé n’est pas une borne WCET démontrée. Ajouter acquisition, interruptions, pré/post-traitement et échanges au budget. Un GPU rapide en lot peut ne pas convenir à une requête isolée avec échéance stricte. Définir ce que fait le système si la sortie arrive trop tard.')
slide('03 · Lire la cible','Énergie, puissance et autonomie :\ntrois grandeurs différentes.',
      'Un calcul plus rapide peut aider ; la mesure doit porter sur le bon périmètre.',
      ['<b>Puissance P :</b> consommation instantanée, en watts.',
       '<b>Énergie E :</b> consommation sur une durée, en joules.',
       '<b>Système :</b> intégrer capteur, veille, calcul, radio et alimentation.'],
      'energy',4,refs=['R18'],detail='E = ∫ P(t) dt ; pour une puissance constante, E=P×Δt. Δt est une durée. Exemple pédagogique : 0,1 W pendant 0,02 s donne 0,002 J, soit 2 mJ. Une énergie par inférence doit préciser si la veille et les périphériques sont inclus. Temps et nombre de MAC ne suffisent pas à annoncer des joules. Une mesure fiable exige instrument, échantillonnage et synchronisation adaptés.')
slide('03 · Lire la cible','Deux recherches : déplacer\nla contrainte au bon endroit.',
      'Architecture et exécution se répondent ; une seule métrique masque le compromis.',
      ['<b>MCUNetV2 · 2021 :</b> calculer par morceaux pour réduire le pic mémoire.',
       '<b>MobileNetV4 · 2024 :</b> concevoir des blocs efficaces pour plusieurs cibles mobiles.',
       '<b>Question ouverte :</b> le gain reste-t-il vrai sur notre cible et notre tâche ?'],
      'codesign',4,refs=['R05','R10'],detail='Lin et al. montrent le rôle de l’ordonnancement par patches et de la répartition du calcul dans le réseau. Qin et al. associent blocs, recherche d’architecture et distillation pour l’écosystème mobile. Lire les matériels effectivement évalués et les contraintes, puis formuler une expérience locale ; ne pas transformer un résultat mobile en promesse sur tous les MCU.')
slide('03 · Lire la cible','Quiz 3 / 5 · Le modèle tient-il ?',
      'Une carte a 128 Kio de SRAM. Le modèle utilise 80 Kio de constantes placées en Flash.',
      [],'quiz',4,kind='quiz',quiz=dict(options=['Oui : 80 est inférieur à 128.','Impossible de conclure sans activations, buffers, pile et placement réel.','Non : tous les poids doivent toujours être copiés en SRAM.'],correct=1,answer='Les deux budgets ne se confondent pas. Il faut vérifier la Flash disponible, le placement effectif des constantes, puis le pic SRAM de l’application complète.'),detail='1 Kio = 1024 octets ; 1 Ko = 1000 octets dans ce support. Le TD distingue 1552 octets de paramètres float32 et le reste de l’inférence. Vérifier les sections du binaire et la pile, plutôt que déduire toute la mémoire du nombre de poids.')
slide('03 · Lire la cible','Pause · 10 minutes.',
      'Au retour : choisir une optimisation, puis chercher la preuve de son intérêt.',
      ['Avant la pause, retenez : <b>qualité + mémoire + temps + énergie.</b>',
       'Une opération rapide seule peut laisser le système lent.'],
      'pause',10,kind='break')

# Chapter 4: 32 minutes.
slide('04 · Optimiser avec méthode','Quatre leviers,\nquatre façons de se tromper.',
      'Commencer par le goulot observé, pas par la technique à la mode.',
      ['<b>Représentation :</b> réduire la précision utile.',
       '<b>Modèle :</b> réduire largeur, blocs ou structure.',
       '<b>Exécution et matériel :</b> réutiliser, fusionner et choisir les bons noyaux.'],
      'levers',3,detail='Quantification : risque d’erreur numérique. Compression structurelle : risque de perdre la qualité. Fusion et tuilage : risque de code ou buffers supplémentaires. Accélérateur : risque de transfert ou d’opérateur non pris en charge. Le choix dépend d’une mesure initiale et d’une hypothèse falsifiable.')
slide('04 · Optimiser avec méthode','Quantifier : garder\nmoins de chiffres utiles.',
      'Le format réduit un coût, au prix d’une approximation à vérifier.',
      ['<b>Échelle s :</b> taille d’un pas entre deux valeurs représentables.',
       '<b>Code q :</b> entier arrondi et limité à une plage.',
       '<b>Attention :</b> poids, activations et accumulateurs peuvent avoir des formats différents.'],
      'quant',5,refs=['R03'],detail='Démonstration symétrique : q=clip(arrondi(x/s),−q_max,q_max), puis x̂=sq ; q_max=2^(b−1)−1 pour b bits. Ici s=1/q_max et x appartient à [−1,1] : le code négatif extrême n’est pas utilisé. clip borne la valeur. Les schémas réels peuvent ajouter un point zéro et des échelles par canal. Une accumulation INT32 peut être nécessaire même avec des entrées INT8.')
slide('04 · Optimiser avec méthode','Calibrer, entraîner,\npuis comparer le vrai calcul.',
      'La meilleure précision n’est pas forcément uniforme dans tout le réseau.',
      ['<b>PTQ :</b> quantifier après entraînement, avec calibration si nécessaire.',
       '<b>QAT :</b> simuler les effets de quantification pendant l’apprentissage.',
       '<b>AWQ · 2024 :</b> protéger les canaux sensibles à partir des activations.'],
      'awq',4,refs=['R09'],detail='PTQ signifie Post-Training Quantization ; QAT, Quantization-Aware Training. La calibration doit représenter les entrées réelles et rester distincte du test réservé. AWQ propose une mise à l’échelle guidée par des statistiques d’activation pour la quantification des poids de LLM. Elle ne supprime ni les accès mémoire ni le besoin d’un noyau matériel adapté.')
slide('04 · Optimiser avec méthode','Supprimer, simplifier,\nou apprendre à imiter.',
      'Compresser un fichier ne suffit pas à accélérer son exécution.',
      ['<b>Élagage :</b> retirer poids ou canaux ; exploiter réellement la structure obtenue.',
       '<b>Distillation :</b> entraîner un petit élève à reproduire un enseignant.',
       '<b>Choix d’architecture :</b> chercher un compromis compatible avec la cible.'],
      'compression',4,refs=['R10'],detail='Des zéros dans une matrice dense ne retirent pas automatiquement les multiplications du noyau. La sparsité non structurée peut ajouter indices et irrégularité ; retirer des canaux change les dimensions de façon plus régulière. La distillation coûte un entraînement et peut transmettre des erreurs de l’enseignant. Une recherche d’architecture a elle-même un budget à annoncer.')
slide('04 · Optimiser avec méthode','Réorganiser sans changer\nla fonction mathématique.',
      'Une optimisation de brique doit rester correcte une fois réintégrée.',
      ['<b>Réemploi :</b> traiter plusieurs sorties avec les mêmes entrées.',
       '<b>Fusion :</b> éviter une écriture intermédiaire lorsque c’est possible.',
       '<b>Coût caché :</b> registres, conversions, code et buffers temporaires.'],
      'fusion',5,detail='Le TD étudie y=Wx+b, poids fixés. Une permutation des boucles ou un petit bloc peut améliorer la localité, mais empêcher une vectorisation favorable. Les additions flottantes ne sont pas parfaitement associatives : vérifier les sorties avec une tolérance expliquée. La bibliothèque optimisée sert de comparateur séparé ; une référence scalaire correcte reste utile pour comprendre.')
slide('04 · Optimiser avec méthode','T-MAC · Remplacer un calcul\npar une consultation de table.',
      'Jianyu Wei et al. · EuroSys 2025 · Une idée système pour produits bas bits sur CPU.',
      ['<b>Problème :</b> les poids bas bits peuvent coûter cher à déquantifier.',
       '<b>Idée :</b> préparer des combinaisons, puis les retrouver par indices.',
       '<b>Limite :</b> la table et ses accès doivent être moins coûteux que le calcul évité.'],
      'lut',4,refs=['R11'],detail='T-MAC organise des produits mixtes bas bits autour de tables de recherche. Le papier évalue plusieurs matériels edge et modèles ; il ne prouve pas qu’une table remplace avantageusement n’importe quelle multiplication. Pour une petite projection float32 du TD, coût de préparation, taille et réutilisation doivent être mesurés avant de choisir cette piste.')
slide('04 · Optimiser avec méthode','Accélérer une brique ne suffit\npas à accélérer le système.',
      'La partie inchangée impose une limite au gain global.',
      ['<b>p :</b> fraction du temps initial passée dans la brique.',
       '<b>s :</b> accélération de cette seule brique.',
       '<b>Gain global :</b> 1 / [(1 − p) + p/s], si le reste est inchangé.'],
      'amdahl',4,detail='Exemple : si la projection occupe 20 % du temps, la rendre deux fois plus rapide ne rend pas le système deux fois plus rapide : gain global ≈1,11, soit 10 % du temps économisé. Cette relation suppose un travail fixe et aucun surcoût nouveau. Si des copies ou conversions sont ajoutées, les compter explicitement.')
slide('04 · Optimiser avec méthode','Quiz 4 / 5 · Quel résultat\npeut-on défendre ?',
      'Sur PC, la projection gagne 10 %. Le réseau entier ralentit de 5 %. La carte n’a pas été testée.',
      [],'quiz',3,kind='quiz',quiz=dict(options=['L’IA embarquée est accélérée de 10 %.','La brique gagne dans ce protocole PC, sans gain global ni preuve sur carte.','Il faut conserver seulement le meilleur chronométrage.'],correct=1,answer='Un résultat local n’établit ni l’effet système ni la portabilité. Le ralentissement est un résultat scientifique à expliquer, pas à cacher.'),detail='Déterminer quelles formes ou quels appels provoquent le ralentissement. Comparer référence et variante avec les mêmes options et données. Rechercher un surcoût de préparation ou un effet de compilateur ; ne pas attribuer une cause sans preuve.')

# Chapter 5: 41 minutes.
slide('05 · Livrer et questionner','Déployer : exporter,\ncompiler, vérifier, intégrer.',
      'Un modèle qui s’ouvre dans un outil n’est pas encore une application validée.',
      ['<b>Exporter :</b> graphe, poids, formes et normalisation.',
       '<b>Vérifier :</b> opérateurs, types, ordre des canaux et équivalence numérique.',
       '<b>Intégrer :</b> entrées réelles, états, tâches, erreurs et mises à jour.'],
      'deployment',5,refs=['R19','R20'],detail='Un runtime exécute le graphe ; un backend choisit des noyaux adaptés. Un opérateur absent peut provoquer un échec ou un retour CPU avec transferts supplémentaires. LiteRT for Microcontrollers et CMSIS-NN illustrent respectivement moteur et noyaux sur certaines cibles. Le TD utilise d’abord sa propre inférence ; une solution de production peut préférer des composants éprouvés après validation.')
slide('05 · Livrer et questionner','Mesurer pour qu’un autre\ningénieur puisse vous contredire.',
      'Un chiffre devient une preuve quand son origine est retrouvable.',
      ['<b>Figer :</b> données, poids, carte, compilateur, options et périmètre.',
       '<b>Mesurer :</b> timer vérifié, répétitions, alternance et données brutes.',
       '<b>Relier :</b> commit → binaire → CSV → figure → conclusion.'],
      'measurement',4,refs=['R18','R21'],detail='Séparer préparation, calcul et transmission série. Éviter la suppression du calcul par le compilateur avec un résultat effectivement utilisé. Dépasser la résolution du timer et rester sous son débordement. Le TD demande au moins trois campagnes, médiane et dispersion. Une CI vérifie tests et compilation ; ses temps ne certifient pas les performances du MCU.')
slide('05 · Livrer et questionner','Une bonne moyenne\npeut masquer une panne.',
      'La fiabilité concerne les entrées inattendues et les conséquences des erreurs.',
      ['<b>Dérive :</b> capteur vieilli, autre machine ou environnement différent.',
       '<b>Erreur :</b> faux positif, faux négatif et coût associé.',
       '<b>Repli :</b> signaler l’incertitude, limiter l’action ou revenir à une règle.'],
      'reliability',4,detail='Tester données manquantes, hors plage, bruit, saturation et redémarrage. Séparer qualité statistique, respect d’échéance et comportement sûr. Un score softmax élevé ne démontre pas qu’une entrée est connue ou qu’une action est acceptable. Le choix d’une stratégie de repli relève du contexte et d’une analyse de risque, pas d’une règle universelle donnée par le réseau.')
slide('05 · Livrer et questionner','Local ne signifie pas\nconfidentiel, robuste ou sûr.',
      'L’IA ajoute des surfaces d’attaque à celles du logiciel embarqué.',
      ['<b>Données / entrées :</b> empoisonnement et perturbations adverses.',
       '<b>Modèle / logiciel :</b> extraction, dépendances ou mises à jour altérées.',
       '<b>Action :</b> contrôler les droits et valider les commandes proposées.'],
      'security',5,refs=['R16'],detail='Le NIST distingue objectifs, capacités et étapes d’attaque. Les exemples du cours sont des catégories, pas un audit de produit. Réduire les transferts peut limiter certaines expositions, mais un appareil ou un modèle peut rester compromis. Une mise à jour doit être authentifiée et pouvoir être diagnostiquée ou retirée. Un LLM recevant des documents peut subir une injection d’instructions même sans accès au cloud.')
slide('05 · Livrer et questionner','« Petit modèle de langage »\nne signifie pas « modèle pour MCU ».',
      'Le mot petit dépend du point de comparaison.',
      ['<b>1,7 milliard de paramètres à 4 bits :</b> environ 850 Mo de poids bruts.',
       '<b>À ajouter :</b> métadonnées, activations, cache KV et moteur.',
       '<b>À décider :</b> besoin réel de génération, ou classification spécialisée ?'],
      'llm',4,refs=['R12'],detail='L’exemple prend la taille de SmolLM2 documentée en 2025. Le calcul 1,7×10⁹×4/8 donne 850×10⁶ octets, hors tout surcoût ; il n’est pas une mesure du modèle téléchargé ni une promesse de compatibilité Pi. Embeddings et tête vocabulaire sont aussi des matrices coûteuses. Une commande vocale peut utiliser un petit classifieur spécialisé plutôt qu’un générateur de texte.')
slide('05 · Livrer et questionner','Veille 2025 · Le NPU ne gagne\nque si le graphe lui convient.',
      'T-MAN · Wei, Li et al. · Prépublication : lire ce qui est accéléré, et ce qui ne l’est pas.',
      ['<b>Problème :</b> des opérations périphériques limitent un accélérateur spécialisé.',
       '<b>Piste :</b> adapter tables, tuilage et pipeline.',
       '<b>À contrôler :</b> préremplissage, décodage, transferts et comparaison de départ.'],
      'npu',3,refs=['R13'],detail='Le résultat étudié concerne des NPUs et systèmes précis. Il ne permet pas de conclure qu’un NPU sera toujours plus rapide ou plus sobre qu’un CPU. Le statut d’article évalué n’est pas établi dans cette préparation : la source est présentée comme prépublication arXiv datée, avec ses résultats à examiner et à reproduire.')
slide('05 · Livrer et questionner','Veille 2026 · Deux voies,\ndeux niveaux d’intervention.',
      'Des pistes actuelles à examiner ; aucune promesse universelle de performance.',
      ['<b>FastGRNN · Kizilates :</b> très petite récurrence, tables et validation sur MCU.',
       '<b>RISC-V · Kumar et al. :</b> instructions et compilation pour Transformers compacts.',
       '<b>Regard critique :</b> mise en régime, graines, mémoire, aire et protocole.'],
      'frontier',4,refs=['R14','R15'],detail='La prépublication FastGRNN rapporte un temps de mise en régime médian de 1,48 s : un appel rapide ne suffit donc pas à décrire la disponibilité du service. La prépublication RISC-V vise surtout des encodeurs et modifie le matériel ; il faut examiner le coût en aire et l’implémentation évaluée. Les deux références sont datées de 2026 ; leur statut de publication évaluée n’est pas établi ici.')
slide('05 · Livrer et questionner','Notre TD : une petite question,\nune expérience défendable.',
      'Le travail de recherche commence quand on accepte que l’hypothèse puisse échouer.',
      ['<b>Construire :</b> petit Mixer manuel, apprentissage et références.',
       '<b>Enquêter :</b> une projection dense, une hypothèse, des variantes limitées.',
       '<b>Conclure :</b> qualité, coûts PC puis carte, limites et expérience suivante.'],
      'research',5,refs=['R08'],detail='Le sujet fournit les équations, pas le code du réseau. Les étudiants écrivent calculs, gradients et tests, puis portent l’inférence. Une proposition de code, humaine ou issue d’un assistant, ne démontre ni sa correction ni sa performance sur la carte. La note porte sur preuves, compréhension et analyse, sans garantie de découverte nouvelle ou d’article accepté. Le corrigé enseignant ne fait pas partie du support du cours.')
slide('05 · Livrer et questionner','Quiz 5 / 5 · Le réseau\nperd face au modèle linéaire.',
      'Les données et le protocole sont corrects. La variante optimisée ralentit aussi le réseau sur carte.',
      [],'quiz',4,kind='quiz',quiz=dict(options=['Changer le test jusqu’à obtenir une victoire.','Rapporter les résultats, expliquer les limites et proposer un nouveau test séparé.','Masquer les références simples dans l’article.'],correct=1,answer='Une conclusion négative rigoureuse est utile. Elle peut montrer qu’un modèle plus simple convient mieux, ou que l’optimisation cible le mauvais coût.'),detail='La recherche cherche une réponse fiable à une question, pas une amélioration imposée. Un nouveau simulateur, une autre tâche ou une nouvelle cible doit être présenté comme une expérience distincte, avec des choix figés avant son évaluation finale.')
slide('05 · Livrer et questionner','La suite : une IA utile,\nsobre et vérifiable.',
      'Partir d’une personne, faire un choix mesuré, puis garder la maîtrise du système.',
      ['<b>Besoin clair.</b> Référence simple et données crédibles.',
       '<b>Budget explicite.</b> Matériel, mémoire, temps et énergie.',
       '<b>Preuve reproductible.</b> Tests, mesures, limites et maintien en service.'],
      'closing',3,kind='closing',detail='Pour prolonger : lire MobileNetV4 pour l’architecture, AWQ pour les représentations, et T-MAC pour les noyaux. La suite du travail consiste à développer, déployer et mesurer sur une cible identifiée. Trois heures donnent une carte de lecture ; la maîtrise vient de ces expériences et de leur analyse.')

assert len(SLIDES)==44
assert sum(s['minutes'] for s in SLIDES)==180

# Vary answer positions: the quiz tests reasoning, not a repeated answer pattern.
permutations=[[0,1,2],[1,0,2],[0,2,1],[1,2,0],[0,2,1]]
for item,order in zip((s for s in SLIDES if s['quiz']),permutations):
    quiz=item['quiz'];original=quiz['options'][:];correct=quiz['correct']
    quiz['options']=[original[k] for k in order];quiz['correct']=order.index(correct)
