/* Course content, explicit teaching stages and references. */
window.REFERENCES = [
  {
    "id": "R1",
    "title": "Attention Is All You Need",
    "authors": "Ashish Vaswani et al.",
    "year": "2017",
    "url": "https://arxiv.org/abs/1706.03762",
    "type": "NeurIPS 2017",
    "use": "Transformer, attention, représentations et calculs matriciels. Le cours utilise un décodeur causal comme exemple ; le papier présente une architecture encodeur-décodeur."
  },
  {
    "id": "R2",
    "title": "Locating and Editing Factual Associations in GPT",
    "authors": "Kevin Meng, David Bau, Alex Andonian, Yonatan Belinkov",
    "year": "2022",
    "url": "https://arxiv.org/abs/2202.05262",
    "type": "NeurIPS 2022",
    "use": "Des interventions causales localisent certains calculs liés à des associations factuelles. Cela ne fournit pas une adresse universelle de chaque connaissance."
  },
  {
    "id": "R3",
    "title": "Toy Models of Superposition",
    "authors": "Nelson Elhage et al.",
    "year": "2022",
    "url": "https://transformer-circuits.pub/2022/toy_model/index.html",
    "type": "Article de recherche · modèles jouets",
    "use": "Des caractéristiques peuvent partager des dimensions, avec des interférences. Un axe n’est donc pas nécessairement un concept isolé."
  },
  {
    "id": "R4",
    "title": "Extracting Training Data from Large Language Models",
    "authors": "Nicholas Carlini et al.",
    "year": "2021",
    "url": "https://arxiv.org/abs/2012.07805",
    "type": "USENIX Security 2021 · prépublication initiale 2020",
    "use": "Des passages d’entraînement ont été extraits de GPT-2. Une représentation distribuée n’interdit ni la mémorisation ni la restitution de texte."
  },
  {
    "id": "R5",
    "title": "Roofline: An Insightful Visual Performance Model…",
    "authors": "Samuel Williams, Andrew Waterman, David Patterson",
    "year": "2008 / 2009",
    "url": "https://www2.eecs.berkeley.edu/Pubs/TechRpts/2008/EECS-2008-134.html",
    "type": "Rapport Berkeley 2008 · article CACM 2009",
    "use": "Relier le calcul et le trafic mémoire. Le maximum des deux temps est une borne optimiste, pas une prédiction exacte de latence."
  },
  {
    "id": "R6",
    "title": "GQA: Training Generalized Multi-Query Transformer Models…",
    "authors": "Joshua Ainslie et al.",
    "year": "2023",
    "url": "https://arxiv.org/abs/2305.13245",
    "type": "EMNLP 2023",
    "use": "Plusieurs têtes de requêtes partagent des têtes K/V ; cela réduit notamment le cache. Une conversion peut demander un réentraînement complémentaire."
  },
  {
    "id": "R7",
    "title": "AWQ: Activation-aware Weight Quantization…",
    "authors": "Ji Lin et al.",
    "year": "2023 / 2024",
    "url": "https://arxiv.org/abs/2306.00978",
    "type": "Prépublication 2023 · MLSys 2024",
    "use": "Quantification des poids guidée par les activations et implémentation adaptée au matériel. Ses résultats ne sont pas ceux de notre petit exemple d’arrondi."
  },
  {
    "id": "R8",
    "title": "FlashAttention: Fast and Memory-Efficient Exact Attention…",
    "authors": "Tri Dao, Daniel Y. Fu, Stefano Ermon, Atri Rudra, Christopher Ré",
    "year": "2022",
    "url": "https://arxiv.org/abs/2205.14135",
    "type": "NeurIPS 2022",
    "use": "Réorganiser le calcul par blocs pour réduire les transferts HBM/SRAM sur GPU, sans approximation de parcimonie de l’attention. Des écarts d’arrondi restent possibles."
  },
  {
    "id": "R9",
    "title": "Reformer: The Efficient Transformer",
    "authors": "Nikita Kitaev, Łukasz Kaiser, Anselm Levskaya",
    "year": "2020",
    "url": "https://arxiv.org/abs/2001.04451",
    "type": "ICLR 2020",
    "use": "LSH pour sélectionner des groupes de candidats ; c’est une attention approximative. Une signature binaire ne remplace pas à elle seule les valeurs V."
  },
  {
    "id": "R10",
    "title": "Mamba: Linear-Time Sequence Modeling with Selective State Spaces",
    "authors": "Albert Gu, Tri Dao",
    "year": "2023 / 2024",
    "url": "https://arxiv.org/abs/2312.00752",
    "type": "Prépublication 2023 · COLM 2024",
    "use": "État récurrent de taille indépendante de la longueur de séquence pour un modèle fixé. Cela n’assure pas la conservation exacte de tout le passé."
  },
  {
    "id": "R11",
    "title": "The Era of 1-bit LLMs: All Large Language Models are in 1.58 Bits",
    "authors": "Shuming Ma et al.",
    "year": "2024",
    "url": "https://arxiv.org/abs/2402.17764",
    "type": "Prépublication · résultats dans les configurations étudiées",
    "use": "BitNet b1.58, poids ternaires et entraînement adapté. Le titre n’implique pas que tous les paramètres d’un fichier réel occupent exactement 1,58 bit."
  },
  {
    "id": "R12",
    "title": "BitNet b1.58 2B4T Technical Report",
    "authors": "Shuming Ma et al.",
    "year": "2025",
    "url": "https://arxiv.org/abs/2504.12285",
    "type": "Rapport technique · prépublication",
    "use": "Un modèle natif basse précision et des implémentations ouvertes existent ; on ne peut pas présenter cette piste comme absente du monde réel."
  },
  {
    "id": "R13",
    "title": "Fast Inference from Transformers via Speculative Decoding",
    "authors": "Yaniv Leviathan, Matan Kalman, Yossi Matias",
    "year": "2023",
    "url": "https://arxiv.org/abs/2211.17192",
    "type": "ICML 2023 · prépublication initiale 2022",
    "use": "Propositions d’un petit modèle, vérification et correction d’échantillonnage par le modèle cible. La distribution est préservée sous les hypothèses de l’algorithme exact ; le gain dépend du cas."
  },
  {
    "id": "R14",
    "title": "GGUF — spécification du format",
    "authors": "Projet ggml",
    "year": "Documentation évolutive",
    "url": "https://github.com/ggml-org/ggml/blob/master/docs/gguf.md",
    "type": "Documentation officielle",
    "use": "Conteneur de tenseurs et de métadonnées. GGUF est un format ; AWQ est une méthode. Ni l’un ni l’autre n’est une promesse de vitesse universelle."
  },
  {
    "id": "R15",
    "title": "BitNet — implémentation officielle",
    "authors": "Microsoft Research",
    "year": "Code évolutif",
    "url": "https://github.com/microsoft/BitNet",
    "type": "Dépôt officiel",
    "use": "Implémentations et modèles compatibles. La disponibilité du code ne garantit ni la prise en charge de toute machine ni la qualité sur toute tâche."
  },
  {
    "id": "R16",
    "title": "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks",
    "authors": "Patrick Lewis et al.",
    "year": "2020",
    "url": "https://arxiv.org/abs/2005.11401",
    "type": "NeurIPS 2020",
    "use": "Combiner les paramètres d’un modèle et une source documentaire récupérée. Les documents sélectionnés fournissent un contexte supplémentaire ; ils ne garantissent pas une réponse vraie."
  },
  {
    "id": "R17",
    "title": "llama.cpp et llama-bench",
    "authors": "Projet ggml",
    "year": "Documentation évolutive",
    "url": "https://github.com/ggml-org/llama.cpp/tree/master/tools/llama-bench",
    "type": "Documentation et implémentation officielles",
    "use": "Mesurer séparément le traitement d’entrée et la génération. Le benchmark rapporte des temps ou débits ; il n’évalue pas la qualité et ne remplace pas la mesure du système intégré."
  },
  {
    "id": "R18",
    "title": "Raspberry Pi — matériel et fonctionnement",
    "authors": "Raspberry Pi",
    "year": "Documentation évolutive",
    "url": "https://www.raspberrypi.com/documentation/computers/raspberry-pi.html",
    "type": "Documentation officielle",
    "use": "Capacités, alimentation et fonctionnement thermique. Les valeurs théoriques du mini-cours ne sont pas des débits mesurés d’un Raspberry Pi."
  },
  {
    "id": "R19",
    "title": "MLPerf Tiny Benchmark",
    "authors": "Colby Banbury et al.",
    "year": "2021",
    "url": "https://arxiv.org/abs/2106.07597",
    "type": "NeurIPS Datasets and Benchmarks 2021",
    "use": "Évaluer ensemble qualité, latence et, avec instrumentation, énergie. Ce benchmark TinyML n’est pas un résultat mesuré sur notre Pi et ne prouve pas des garanties de temps réel."
  }
];
window.SLIDES = [
  {
    "id": "opening",
    "chapter": "1 · Cadrer le besoin",
    "eyebrow": "Une question avant de commencer",
    "title": "Où se cache<br>ce que <em>sait</em> une IA ?",
    "lead": "Un assistant doit expliquer une notice sur un appareil. Il faut une réponse utile, dans les limites de cet appareil.",
    "body": "<div class=\"points\"><div class=\"point\"><strong>Poids :</strong> réglages numériques appris.</div><div class=\"point\"><strong>Contexte :</strong> texte reçu pour cette réponse.</div><div class=\"point\"><strong>Documents :</strong> extraits qu’un outil peut ajouter au contexte.</div></div>",
    "take": "Notre objectif : repérer une brique coûteuse, imaginer une amélioration et savoir comment la mettre à l’épreuve.",
    "scene": "memory",
    "caption": "Parcours découverte : aucun prérequis en IA. Les codes R ouvrent les références ; le bouton Ingénieur donne les détails.",
    "refs": [
      "R1",
      "R2",
      "R16"
    ],
    "alt": "Le modèle utilise des réglages appris et un contexte, qui peut inclure des extraits documentaires.",
    "audience": "all",
    "steps": [
      "Recevoir la question",
      "Ajouter des informations",
      "Produire une réponse"
    ],
    "phase": 1
  },
  {
    "id": "embedded-constraints",
    "chapter": "1 · Cadrer le besoin",
    "eyebrow": "Le système impose des limites",
    "title": "Une IA utile.<br><em>Dans quelle boîte ?</em>",
    "lead": "Un système embarqué est un ordinateur intégré à un appareil pour assurer une tâche. Ses contraintes dépendent de l’usage.",
    "body": "<div class=\"points\"><div class=\"point\"><strong>Ressources :</strong> calcul, mémoire de travail et stockage.</div><div class=\"point\"><strong>Usage :</strong> délai maximal (échéance), énergie, qualité et fiabilité.</div><div class=\"point\"><strong>Terrain :</strong> capteurs, réseau, confidentialité et mises à jour.</div></div>",
    "take": "Le cahier des charges fixe ce qu’il faut respecter avant de choisir ou de modifier le modèle.",
    "scene": "constraints",
    "caption": "Un Pi Linux n’a pas les mêmes contraintes qu’un microcontrôleur. Les principes valent aussi pour l’IA de vision, de son et de capteurs.",
    "refs": [
      "R18",
      "R19"
    ],
    "alt": "Cinq limites encadrent le modèle : mémoire, temps, énergie et chaleur, fiabilité, conditions d’exploitation.",
    "audience": "all",
    "steps": [
      "Choisir une tâche",
      "Fixer les limites",
      "Écrire les critères"
    ],
    "phase": 1
  },
  {
    "id": "learn",
    "chapter": "2 · Comprendre les calculs",
    "eyebrow": "Deux moments à ne pas confondre",
    "title": "Apprendre.<br>Puis <em>utiliser</em>.",
    "lead": "Apprendre, c’est modifier les réglages à partir d’exemples. Utiliser le modèle, c’est calculer une réponse avec ces réglages.",
    "body": "<div class=\"points\"><div class=\"point\"><strong>Entraînement :</strong> on ajuste les paramètres, c’est-à-dire les réglages appris.</div><div class=\"point\"><strong>Inférence :</strong> on utilise normalement des réglages fixes.</div></div>",
    "take": "Les poids sont des paramètres. D’autres réglages appris, comme les biais, en font aussi partie.",
    "scene": "learn",
    "caption": "Un biais est une valeur ajoutée dans un calcul. Ajouter du contexte ne signifie pas réentraîner le modèle.",
    "refs": [
      "R1"
    ],
    "alt": "L’apprentissage corrige les poids ; l’inférence lit ces poids et une nouvelle entrée.",
    "engineerBody": "<div class=\"points\"><div class=\"point\"><strong>Pré-entraînement :</strong> premier apprentissage sur un grand ensemble de données.</div><div class=\"point\"><strong>Ajustement fin :</strong> entraînement supplémentaire pour adapter le modèle.</div><div class=\"point\">Les poids, biais et autres réglages appris sont des paramètres ; ils ne changent pas dans l’inférence ordinaire.</div></div>",
    "audience": "all",
    "steps": [
      "Donner des exemples",
      "Corriger les réglages",
      "Utiliser le modèle"
    ],
    "phase": 2
  },
  {
    "id": "embedding",
    "chapter": "2 · Comprendre les calculs",
    "eyebrow": "Du texte aux nombres",
    "title": "Un token.<br>Un identifiant.<br><em>Une liste de nombres.</em>",
    "lead": "Un tokenizer découpe le texte en tokens. Chaque numéro de token, appelé identifiant (ID), permet de retrouver une liste apprise de nombres.",
    "body": "<div class=\"points\"><div class=\"point\">Un <strong>vecteur</strong> est une liste ordonnée de nombres.</div><div class=\"point\">L’<strong>embedding</strong> est cette représentation apprise. Une case n’a pas forcément un sens facile à nommer.</div></div>",
    "take": "L’exemple montre trois nombres pour rester lisible. Un vrai modèle peut en utiliser beaucoup plus.",
    "scene": "embedding",
    "caption": "Découpage, identifiants et nombres fictifs pour expliquer. Choisir un token montre la ligne correspondante ; ce ne sont pas les valeurs d’un LLM réel.",
    "refs": [
      "R1",
      "R3"
    ],
    "alt": "Trois morceaux de phrase sont représentés par trois listes de nombres.",
    "audience": "all",
    "control": "embedding",
    "steps": [
      "Découper le texte",
      "Retrouver la ligne",
      "Obtenir le vecteur"
    ],
    "phase": 2
  },
  {
    "id": "attention",
    "chapter": "2 · Comprendre les calculs",
    "eyebrow": "Le contexte change l’interprétation",
    "title": "« Avril » :<br><em>qui ou quand ?</em>",
    "lead": "L’attention aide à combiner les informations déjà lues qui comptent pour la position traitée.",
    "body": "<div class=\"points\"><div class=\"point\">À la fin de « Avril chante », la phrase suggère une personne.</div><div class=\"point\">Dans « En avril, il pleut », elle suggère un mois.</div></div>",
    "take": "À une position donnée, le modèle causal étudié ne consulte pas les tokens futurs.",
    "scene": "attention",
    "caption": "Exemple d’interprétation en fin de phrase. Les liens sont dessinés, pas mesurés. La formule Q/K/V est dans le parcours Ingénieur.",
    "refs": [
      "R1"
    ],
    "alt": "Au dernier token, une requête Q est comparée aux clés K du texte déjà lu, puis l’attention combine les valeurs V.",
    "control": "context",
    "detail": "attention-math",
    "audience": "all",
    "steps": [
      "Lire le texte disponible",
      "Comparer et combiner",
      "Interpréter ici"
    ],
    "phase": 2
  },
  {
    "id": "attention-math",
    "chapter": "2 · Comprendre les calculs",
    "eyebrow": "Approfondissement ingénieur",
    "title": "Comment calculer<br><em>l’attention</em> ?",
    "lead": "Un Transformer enchaîne des blocs d’attention, qui combinent le contexte, et des transformations de vecteurs.",
    "body": "<div class=\"equation\">Attention(Q,K,V) = softmax(QKᵀ / √dₖ) V</div><div class=\"legend\">Q : requêtes, ce que l’on cherche ; K : clés à comparer.<br>V : valeurs, informations à combiner ; dₖ : taille d’une clé.<br>ᵀ échange lignes et colonnes. softmax donne des pondérations positives dont la somme vaut 1.</div>",
    "take": "Un modèle causal ne lit pas de token futur. À la fin de la phrase, toute la phrase est déjà disponible.",
    "scene": "attention",
    "caption": "Interprétation illustrée à la fin de la phrase, pas au token « Avril » isolé. Liens dessinés, pas mesurés dans un modèle.",
    "refs": [
      "R1"
    ],
    "alt": "Au dernier token, une requête Q est comparée aux clés K du texte déjà lu, puis l’attention combine les valeurs V.",
    "control": "context",
    "audience": "engineer",
    "detailOf": "attention",
    "steps": [
      "Lire le texte disponible",
      "Comparer et combiner",
      "Interpréter ici"
    ],
    "phase": 2
  },
  {
    "id": "distributed",
    "chapter": "2 · Comprendre les calculs",
    "eyebrow": "Une représentation partagée",
    "title": "Un neurone n’est pas<br>un <em>tiroir à faits</em>.",
    "lead": "Un neurone combine des entrées. Les poids se rangent en matrices, des tableaux de nombres.",
    "body": "<div class=\"points\"><div class=\"point\"><strong>MLP :</strong> perceptron multicouche, un réseau de couches de neurones.</div><div class=\"point\"><strong>Activation :</strong> fonction qui transforme le résultat d’un neurone.</div><div class=\"point\"><strong>Superposition :</strong> des propriétés partagent des dimensions de représentation.</div></div>",
    "take": "Une propriété peut mobiliser plusieurs unités. Ce partage n’empêche pas la mémorisation de passages.",
    "scene": "features",
    "caption": "Deux unités et trois propriétés illustrées : ce partage peut créer des interférences. Ce n’est pas une carte réelle de neurones.",
    "refs": [
      "R2",
      "R3",
      "R4"
    ],
    "alt": "Deux unités partagées participent à trois propriétés ; chaque propriété mobilise les deux unités.",
    "audience": "engineer",
    "steps": [
      "Observer les unités",
      "Partager les calculs",
      "Étudier les propriétés"
    ],
    "phase": 2
  },
  {
    "id": "q-memory",
    "chapter": "2 · Comprendre les calculs",
    "eyebrow": "À vous de prédire",
    "title": "J’ajoute un nom<br>dans <em>mon message</em>.",
    "lead": "Le modèle réutilise ce nom. Quelle explication suffit sans supposer de réentraînement ?",
    "question": [
      "Le contexte peut suffire à expliquer sa réponse.",
      "Les poids ont été modifiés par ce message.",
      "Le nom a été enregistré durablement pour tous."
    ],
    "answer": 0,
    "explanation": "La réponse peut utiliser le contexte. À elle seule, elle ne prouve ni mise à jour des poids ni mémoire durable.",
    "take": "Poids appris, contexte temporaire et stockage de l’application sont trois choses différentes.",
    "scene": "memory",
    "refs": [
      "R1"
    ],
    "caption": "Une réponse correcte ne suffit pas à identifier le mécanisme de mémorisation.",
    "alt": "Le message alimente le modèle sans flèche de mise à jour des poids.",
    "audience": "engineer",
    "steps": [
      "Recevoir la question",
      "Ajouter des informations",
      "Produire une réponse"
    ],
    "phase": 2
  },
  {
    "id": "decode",
    "chapter": "3 · Localiser le coût",
    "eyebrow": "Deux phases de l’inférence",
    "title": "Lire le début.<br>Puis <em>continuer</em>.",
    "lead": "D’abord, le modèle traite le texte reçu. Ensuite, il produit la suite.",
    "body": "<div class=\"points\"><div class=\"point\"><strong>Prefill :</strong> traiter le contexte d’entrée.</div><div class=\"point\"><strong>Decode :</strong> produire les tokens suivants, en réutilisant les calculs passés.</div></div>",
    "take": "Lire l’entrée offre du travail parallèle. Produire la suite dépend souvent des transferts ; cela varie selon la machine et le modèle.",
    "scene": "decode",
    "caption": "Le débit compte les tokens par seconde. Le coût réel dépend du modèle, du contexte, du nombre de requêtes et du matériel.",
    "refs": [
      "R1",
      "R13"
    ],
    "alt": "Une phrase entre en bloc, puis les tokens de sortie apparaissent successivement.",
    "engineerBody": "<div class=\"points\"><div class=\"point\"><strong>Prefill :</strong> traiter de nombreuses positions avec davantage de réutilisation des poids.</div><div class=\"point\"><strong>Decode à petit lot :</strong> moins de réutilisation ; les transferts peuvent dominer.</div><div class=\"point\">Ce diagnostic n’est pas une loi : caches, taille du lot, architecture et cible peuvent changer le facteur limitant.</div></div>",
    "audience": "all",
    "steps": [
      "Traiter le contexte",
      "Calculer la suite",
      "Ajouter des tokens"
    ],
    "phase": 3
  },
  {
    "id": "weights",
    "chapter": "3 · Localiser le coût",
    "eyebrow": "Premier budget : les poids",
    "title": "Sept milliards<br>de <em>nombres</em>.",
    "lead": "Un bit vaut 0 ou 1. Huit bits font un octet. Moins de bits par réglage réduit son volume de stockage.",
    "body": "<div class=\"points\"><div class=\"point\">Exemple idéal : 7 milliards de paramètres.</div><div class=\"point\">16 bits par paramètre : <strong>14 Go</strong>. À 4 bits : <strong>3,5 Go</strong>.</div></div>",
    "take": "Cela compte les réglages seuls. Ce n’est pas encore la mémoire totale de l’application.",
    "scene": "weights",
    "control": "bits",
    "caption": "Go = milliard d’octets. Échelles, format du fichier et autres données s’ajoutent. La formule est dans le parcours Ingénieur.",
    "refs": [
      "R7",
      "R14"
    ],
    "alt": "Une barre de poids se réduit de 14 Go à 3,5 Go lorsque la précision passe de 16 à 4 bits.",
    "detail": "weights-math",
    "audience": "all",
    "steps": [
      "Compter les réglages",
      "Choisir les bits",
      "Calculer le volume"
    ],
    "phase": 3
  },
  {
    "id": "weights-math",
    "chapter": "3 · Localiser le coût",
    "eyebrow": "Approfondissement ingénieur",
    "title": "Combien d’octets<br>pour <em>les poids</em> ?",
    "lead": "Un bit vaut 0 ou 1. Huit bits font un octet. La précision choisie change le nombre de bits par poids.",
    "body": "<div class=\"equation\">M<sub>poids</sub> = N × b / 8</div><div class=\"legend\">N : nombre de paramètres, les réglages appris.<br>b : bits par paramètre ; M : taille en octets.<br>Ici N=7×10⁹ ; 1 Go=10⁹ octets.</div>",
    "take": "Le programme, ses données de travail et le format du fichier occupent aussi de la mémoire.",
    "scene": "weights",
    "control": "bits",
    "caption": "Poids seuls : ni la RAM totale (mémoire de travail), ni un fichier complet. La barre change avec les bits.",
    "refs": [
      "R7",
      "R14"
    ],
    "alt": "Une barre de poids se réduit de 14 Go à 3,5 Go lorsque la précision passe de 16 à 4 bits.",
    "audience": "engineer",
    "detailOf": "weights",
    "steps": [
      "Compter les réglages",
      "Choisir les bits",
      "Calculer le volume"
    ],
    "phase": 3
  },
  {
    "id": "cache",
    "chapter": "3 · Localiser le coût",
    "eyebrow": "Deuxième budget : le contexte",
    "title": "Le cache grandit<br>avec <em>l’histoire</em>.",
    "lead": "Pour continuer une phrase, le modèle réutilise certains calculs sur le texte déjà lu au lieu de tout refaire.",
    "body": "<div class=\"points\"><div class=\"point\">Ce stockage de réutilisation s’appelle le <strong>cache</strong>.</div><div class=\"point\">La <strong>fenêtre de contexte</strong> est la quantité de texte que le modèle peut prendre en compte.</div></div>",
    "take": "Un contexte plus long peut demander plus de mémoire. Le cache grandit dans l’attention standard illustrée ici.",
    "scene": "cache",
    "control": "cache",
    "caption": "Exemple calculé en Go, pas un essai sur Pi. K et V sont des représentations d’attention ; la formule et le partage des têtes sont dans les détails.",
    "refs": [
      "R6"
    ],
    "alt": "Des cases de cache s’ajoutent quand le contexte s’allonge ; partager les têtes réduit leur nombre.",
    "detail": "cache-math",
    "audience": "all",
    "steps": [
      "Lire plus de texte",
      "Garder des calculs",
      "Compter la mémoire"
    ],
    "phase": 3
  },
  {
    "id": "cache-math",
    "chapter": "3 · Localiser le coût",
    "eyebrow": "Approfondissement ingénieur",
    "title": "Compter le cache<br><em>sans oublier les têtes</em>.",
    "lead": "Un cache est une mémoire de réutilisation. Celui de l’attention garde les clés K et valeurs V déjà calculées.",
    "body": "<div class=\"equation\">M<sub>KV</sub> = 2 × L × S × H<sub>KV</sub> × d × p</div><div class=\"legend\">Pour une séquence : L couches, S tokens,<br>H<sub>KV</sub> têtes K/V, d composantes par tête,<br>p octets par composante. Le 2 compte K et V.</div>",
    "take": "Une tête est une branche d’attention. En GQA, plusieurs têtes de requêtes partagent les mêmes K/V.",
    "scene": "cache",
    "control": "cache",
    "caption": "Pour une séquence : L=32, d=128, p=2. 1 Go=10⁹ octets ; 1 Gio=2³⁰ octets. Pas une mesure sur Pi.",
    "refs": [
      "R6"
    ],
    "alt": "Des cases de cache s’ajoutent quand le contexte s’allonge ; partager les têtes réduit leur nombre.",
    "audience": "engineer",
    "detailOf": "cache",
    "steps": [
      "Lire plus de texte",
      "Garder des calculs",
      "Compter la mémoire"
    ],
    "phase": 3
  },
  {
    "id": "memory-total",
    "chapter": "3 · Localiser le coût",
    "eyebrow": "Le budget complet",
    "title": "Le fichier tient.<br><em>Et le reste ?</em>",
    "lead": "La RAM est la mémoire de travail. Elle doit aussi accueillir le contexte, les calculs en cours et les logiciels.",
    "body": "<div class=\"points\"><div class=\"point\">Additionner <strong>paramètres + cache + valeurs temporaires + logiciels et système</strong>.</div><div class=\"point\">Garder une marge ; vérifier ensuite le maximum réellement occupé.</div></div>",
    "take": "Le total doit rester sous le budget disponible. Une marge calculée doit encore être confirmée par une mesure.",
    "scene": "memory-total",
    "control": "budget",
    "caption": "Calcul pédagogique : poids à 4 bits, cache selon le contexte ; 1 Go supposé pour le reste. Budgets de 4 ou 8 Go hypothétiques, pas une mesure de carte.",
    "refs": [
      "R6",
      "R17"
    ],
    "alt": "Une barre empile paramètres, cache et autres besoins ; une limite montre la marge ou le dépassement.",
    "audience": "all",
    "steps": [
      "Choisir les hypothèses",
      "Additionner les besoins",
      "Comparer au budget"
    ],
    "phase": 3
  },
  {
    "id": "roofline",
    "chapter": "3 · Localiser le coût",
    "eyebrow": "Le calcul attend parfois les données",
    "title": "Une usine rapide.<br>Une <em>route étroite</em>.",
    "lead": "Imaginons une machine : elle doit lire des données et effectuer des calculs. Le travail le plus lent peut dominer.",
    "body": "<div class=\"points\"><div class=\"point\">La <strong>latence</strong> est la durée d’une étape.</div><div class=\"point\">Réduire le temps de calcul aide peu si les données arrivent trop lentement.</div></div>",
    "take": "Réduire les octets effectivement transférés peut aider. Réduire seulement le fichier ne garantit pas ce gain.",
    "scene": "roofline",
    "control": "roofline",
    "caption": "Machine fictive, pas un Raspberry Pi : hypothèses réglables. Temps idéaux, cache et autres coûts exclus. La formule est dans les détails.",
    "refs": [
      "R5"
    ],
    "alt": "Deux durées sont comparées : transférer les poids et effectuer les opérations.",
    "detail": "roofline-math",
    "audience": "all",
    "steps": [
      "Fixer une machine",
      "Comparer les deux coûts",
      "Chercher la limite"
    ],
    "phase": 3
  },
  {
    "id": "roofline-math",
    "chapter": "3 · Localiser le coût",
    "eyebrow": "Approfondissement ingénieur",
    "title": "Une borne pour<br><em>raisonner sur le coût</em>.",
    "lead": "Le débit mémoire est la quantité de données transférable par seconde. Le calcul peut attendre ces données.",
    "body": "<div class=\"equation\">T ≥ max(D / B, F / C)</div><div class=\"legend\">T : latence, durée d’une étape ; max retient le plus grand temps.<br>D : octets transférés ; B : débit mémoire en octets/s.<br>F : opérations ; C : capacité de calcul en opérations/s.</div>",
    "take": "Cette borne n’est pas une mesure. Changer la capacité de calcul peut déplacer le facteur limitant.",
    "scene": "roofline",
    "control": "roofline",
    "caption": "Hypothèses réglables, pas de chiffres matériels de Pi. N=7×10⁹ ; D=poids effectivement lus une fois ; F≈2N. Cache et surcoûts exclus.",
    "refs": [
      "R5"
    ],
    "alt": "Deux durées sont comparées : transférer les poids et effectuer les opérations.",
    "audience": "engineer",
    "detailOf": "roofline",
    "steps": [
      "Fixer une machine",
      "Comparer les deux coûts",
      "Chercher la limite"
    ],
    "phase": 3
  },
  {
    "id": "q-bandwidth",
    "chapter": "3 · Localiser le coût",
    "eyebrow": "Un diagnostic avant une optimisation",
    "title": "Le calcul prend 7 ms.<br>La lecture, <em>70 ms</em>.",
    "lead": "Dans le modèle idéal, on double seulement la capacité de calcul. Que devient la borne de temps ?",
    "question": [
      "Elle passe à 35 ms.",
      "Elle reste à 70 ms : les transferts dominent.",
      "Elle passe à 7 ms."
    ],
    "answer": 1,
    "explanation": "La borne max(70,7) reste 70 ms quand 7 devient 3,5 ms. Une machine réelle ajoute d’autres coûts.",
    "take": "Optimiser une brique peu coûteuse peut presque ne rien changer au temps total.",
    "scene": "roofline",
    "caption": "Nombres d’un exemple analytique, pas d’une mesure de PC ou de Raspberry Pi.",
    "refs": [
      "R5"
    ],
    "alt": "Une barre mémoire de 70 ms domine une barre de calcul de 7 ms.",
    "audience": "engineer",
    "steps": [
      "Fixer une machine",
      "Comparer les deux coûts",
      "Chercher la limite"
    ],
    "phase": 3
  },
  {
    "id": "quantize",
    "chapter": "4 · Proposer une piste",
    "eyebrow": "Piste 1 · représenter autrement",
    "title": "Arrondir les poids.<br>Observer <em>la sortie</em>.",
    "lead": "Quantifier, c’est remplacer des valeurs par quelques niveaux. Les arrondis peuvent changer la sortie.",
    "body": "<div class=\"points\"><div class=\"point\"><strong>Après entraînement :</strong> convertir un modèle existant, puis vérifier les erreurs.</div><div class=\"point\"><strong>Entraînement adapté :</strong> apprendre en tenant compte de la basse précision, comme dans BitNet.</div></div>",
    "take": "Cette animation montre l’écart dû aux arrondis. Elle ne mesure pas un gain de vitesse.",
    "scene": "quantize",
    "control": "quantize",
    "caption": "Exemple calculé dans la page. Les entrées restent les mêmes ; seul l’arrondi des poids change. Ce n’est pas l’exécution d’un modèle de langage.",
    "refs": [
      "R7"
    ],
    "alt": "Quatre poids se rapprochent de niveaux de quantification ; la différence de sortie est calculée.",
    "detail": "quantize-math",
    "audience": "all",
    "steps": [
      "Prendre les mêmes poids",
      "Arrondir les valeurs",
      "Comparer la sortie"
    ],
    "phase": 4
  },
  {
    "id": "quantize-math",
    "chapter": "4 · Proposer une piste",
    "eyebrow": "Approfondissement ingénieur",
    "title": "Quantifier.<br><em>Calculer l’erreur.</em>",
    "lead": "Quantifier : remplacer des valeurs par quelques niveaux.",
    "body": "<div class=\"equation\">s = max|w| / q<sub>max</sub><br>q = borne(arrondi(w/s), −q<sub>max</sub>, q<sub>max</sub>)<br>ŵ = s × q</div><div class=\"legend\">b : bits ; q<sub>max</sub>=2ᵇ⁻¹−1 : plus grand code positif.<br>s : échelle, pas entre niveaux ; max|w| : plus grand poids sans signe.<br>w : poids ; q : code entier ; ŵ : poids reconstruit.<br>x : entrée ; y : sortie ; i : indice. Si max|w|=0 : s=1.</div>",
    "take": "Calcul en flottants (réels approchés) : le stockage réduit ne promet pas d’accélération.",
    "scene": "quantize",
    "control": "quantize",
    "caption": "w=(−0,9 ; −0,32 ; 0,18 ; 0,76), x=(1 ; 0,5 ; −1 ; 0,25). Borner ramène au code autorisé ; arrondi à mi-distance loin de zéro.",
    "refs": [
      "R7"
    ],
    "alt": "Quatre poids se rapprochent de niveaux de quantification ; la différence de sortie est calculée.",
    "audience": "engineer",
    "detailOf": "quantize",
    "steps": [
      "Prendre les mêmes poids",
      "Arrondir les valeurs",
      "Comparer la sortie"
    ],
    "phase": 4
  },
  {
    "id": "flash",
    "chapter": "4 · Proposer une piste",
    "eyebrow": "Piste 2 · changer le trajet des données",
    "title": "Même attention.<br>Moins <em>d’allers-retours</em>.",
    "lead": "Un GPU est un processeur qui effectue beaucoup de calculs en parallèle. FlashAttention réorganise ses accès mémoire.",
    "body": "<div class=\"points\"><div class=\"point\">La mémoire rapide est petite : le calcul est organisé en blocs.</div><div class=\"point\">Réutiliser un bloc évite des lectures répétées en mémoire globale.</div></div>",
    "take": "L’attention reste complète, à l’arrondi numérique près. FlashAttention ne supprime pas le cache K/V.",
    "scene": "flash",
    "caption": "Tri Dao et ses coauteurs, 2022. Schéma de principe GPU ; aucun gain automatique n’est promis sur Raspberry Pi.",
    "refs": [
      "R8"
    ],
    "alt": "Des blocs passent entre la mémoire globale et une petite zone rapide où ils sont réutilisés.",
    "audience": "engineer",
    "steps": [
      "Lire les blocs",
      "Réutiliser au bon endroit",
      "Limiter les transferts"
    ],
    "phase": 4
  },
  {
    "id": "architectures",
    "chapter": "4 · Proposer une piste",
    "eyebrow": "Piste 3 · changer la mémoire du modèle",
    "title": "Garder des éléments.<br>Ou <em>résumer le passé</em>.",
    "lead": "Une autre architecture change la manière de conserver et retrouver le passé.",
    "body": "<div class=\"points\"><div class=\"point\"><strong>Reformer · 2020 :</strong> le hachage calcule des codes pour regrouper des éléments proches. Certains éléments peuvent être manqués.</div><div class=\"point\"><strong>Mamba · 2023 :</strong> un état est un résumé numérique ; la récurrence le met à jour à chaque token.</div></div>",
    "take": "Pour un modèle fixé, l’état de Mamba ne grandit pas avec le contexte. Cela ne préserve pas forcément tous les détails.",
    "scene": "architectures",
    "caption": "Kitaev et al. pour Reformer ; Albert Gu et Tri Dao pour Mamba. Ce ne sont pas des remplacements universellement meilleurs.",
    "refs": [
      "R9",
      "R10"
    ],
    "alt": "Une branche sélectionne des cases par hachage ; une autre met à jour un petit état récurrent.",
    "audience": "engineer",
    "steps": [
      "Recevoir le même passé",
      "Sélectionner ou résumer",
      "Vérifier ce qui reste"
    ],
    "phase": 4
  },
  {
    "id": "q-hash",
    "chapter": "4 · Proposer une piste",
    "eyebrow": "La question qui évite une fausse conclusion",
    "title": "L’information utile<br>est dans <em>un autre groupe</em>.",
    "lead": "Le hachage de proximité regroupe des vecteurs d’attention. Si on ne consulte que certains groupes, quel risque reste-t-il ?",
    "question": [
      "Toutes les informations seront forcément retrouvées.",
      "Une information pertinente peut ne pas être consultée.",
      "Des vecteurs proches ne doivent jamais partager un groupe."
    ],
    "answer": 1,
    "explanation": "Le but est de regrouper des vecteurs proches. Mais un voisin pertinent peut être classé ailleurs et ne pas être consulté.",
    "take": "Ici, l’erreur à tester est une information utile non consultée, pas le simple fait de partager un code.",
    "scene": "hash-neighbor",
    "caption": "Schéma de sélection approximative de vecteurs, pas un hachage de phrases entières. Reformer utilise des groupes de proximité.",
    "refs": [
      "R9"
    ],
    "alt": "La requête consulte un groupe contenant A et C ; un vecteur utile B se trouve hors du groupe.",
    "audience": "engineer",
    "steps": [
      "Chercher une information",
      "Choisir des groupes",
      "Repérer un oubli"
    ],
    "phase": 4
  },
  {
    "id": "bitnet",
    "chapter": "4 · Proposer une piste",
    "eyebrow": "Piste 4 · entraîner pour une autre arithmétique",
    "title": "Et avec des poids<br><em>−1, 0, +1</em> ?",
    "lead": "Ternaire signifie trois valeurs possibles. BitNet b1.58 apprend avec des poids −1, 0 et +1.",
    "body": "<div class=\"equation\">(−1)×x₁ + 0×x₂ + (+1)×x₃<br>= −x₁ + x₃</div><div class=\"legend\">x₁, x₂, x₃ : trois valeurs d’entrée.<br>log₂(3)≈1,58 bits : limite idéale pour trois choix aussi fréquents.<br>Échelles et autres données s’ajoutent au stockage réel.</div>",
    "take": "Un noyau est une fonction de calcul adaptée au processeur. Entraînement et noyaux doivent être compatibles.",
    "scene": "bitnet",
    "caption": "Apprentissage adapté à la basse précision, pas une quantification post-entraînement arbitraire. Ma et al., 2024 ; modèle 2B4T, 2025.",
    "refs": [
      "R11",
      "R12",
      "R15"
    ],
    "alt": "Les produits par des poids ternaires se transforment en soustractions, zéros et additions.",
    "audience": "engineer",
    "steps": [
      "Utiliser des poids ternaires",
      "Ajouter ou soustraire",
      "Vérifier la sortie"
    ],
    "phase": 4
  },
  {
    "id": "speculative",
    "chapter": "4 · Proposer une piste",
    "eyebrow": "Piste 5 · proposer, puis vérifier",
    "title": "Un petit modèle écrit.<br>Le grand <em>contrôle</em>.",
    "lead": "Le modèle brouillon propose une suite. Le modèle cible, celui que l’on veut reproduire, la vérifie.",
    "body": "<div class=\"points\"><div class=\"point\">Vérifier plusieurs propositions ensemble peut mieux réutiliser les poids que plusieurs lectures séparées.</div><div class=\"point\">La distribution est la liste des probabilités de sortie. Une correction de tirage conserve ces probabilités dans l’algorithme exact.</div></div>",
    "take": "La vérification a un coût. Le gain dépend du brouillon, du matériel et du nombre de tokens acceptés.",
    "scene": "speculative",
    "caption": "Préserver les probabilités ne signifie pas garantir la vérité ni obtenir le même tirage aléatoire. Ce procédé peut aussi ne pas accélérer un petit appareil.",
    "refs": [
      "R13"
    ],
    "alt": "Trois tokens sont proposés ; le modèle cible en valide une partie et corrige la suite.",
    "audience": "engineer",
    "steps": [
      "Proposer des tokens",
      "Vérifier avec la cible",
      "Accepter ou corriger"
    ],
    "phase": 4
  },
  {
    "id": "optimization-levers",
    "chapter": "4 · Proposer une piste",
    "eyebrow": "Des briques où chercher",
    "title": "Quelle opération<br><em>changeriez-vous ?</em>",
    "lead": "Une brique est une opération ou un bloc du modèle. Partir du coût observé, pas d’une technique à la mode.",
    "body": "<div class=\"points\"><div class=\"point\">Choisir <strong>une brique</strong> et un coût : temps, mémoire ou énergie.</div><div class=\"point\">Proposer un changement et expliquer <strong>pourquoi</strong> il pourrait aider.</div><div class=\"point\">Nommer aussi ce qu’il pourrait dégrader.</div></div>",
    "take": "Une idée devient intéressante quand elle produit une prédiction que l’on peut vérifier ou contredire.",
    "scene": "levers",
    "control": "lever",
    "caption": "Pistes d’enquête, pas gains garantis. On peut tester un changement de code, de représentation ou d’architecture.",
    "refs": [
      "R5",
      "R7",
      "R19"
    ],
    "alt": "Une brique choisie mène à une idée de modification, puis à un risque et à un test.",
    "audience": "all",
    "steps": [
      "Choisir la brique",
      "Proposer un changement",
      "Définir le test"
    ],
    "phase": 4
  },
  {
    "id": "proof",
    "chapter": "5 · Enquêter et tester",
    "eyebrow": "Distinguer les niveaux de preuve",
    "title": "Une équation n’est pas<br>un <em>chronomètre</em>.",
    "lead": "Un calcul peut aider à choisir une piste. Il ne démontre pas la qualité d’un modèle ni sa vitesse réelle.",
    "body": "<div class=\"points\"><div class=\"point\"><strong>Hypothèse :</strong> résultat attendu, écrit avant les mesures.</div><div class=\"point\"><strong>Calculé :</strong> taille des poids ou minimum théorique de temps.</div><div class=\"point\"><strong>Mesuré :</strong> durée, RAM maximale et qualité sur des exemples de test.</div></div>",
    "take": "Une taille de fichier ne démontre ni un débit réel ni une qualité de réponse.",
    "scene": "proof",
    "caption": "Qualité : réussite sur la tâche choisie. Le jeu de test reste indépendant des données qui ont servi à choisir les réglages.",
    "refs": [
      "R5",
      "R9"
    ],
    "alt": "Trois cases séparent un compte théorique, une hypothèse et une mesure expérimentale.",
    "audience": "engineer",
    "steps": [
      "Faire un calcul",
      "Écrire une hypothèse",
      "Demander une mesure"
    ],
    "phase": 5
  },
  {
    "id": "measurement-example",
    "chapter": "5 · Enquêter et tester",
    "eyebrow": "Exercice de décision · données fictives",
    "title": "Plus rapide.<br>Mais <em>acceptable</em> ?",
    "lead": "Fixons avant l’essai : au moins 47 bonnes réponses sur 50 et une durée médiane d’au plus 150 ms.",
    "body": "<div class=\"points\"><div class=\"point\">La <strong>médiane</strong> est la valeur du milieu des durées triées. L’intervalle indique ici le minimum et le maximum.</div><div class=\"point\">Même entrée de 128 tokens, réponse de 20 tokens, modèle déjà chargé. Peut-on choisir la variante ?</div></div>",
    "take": "Non selon ce cahier des charges : 46/50 est sous le seuil de qualité. Un gain de vitesse ne suffit pas.",
    "scene": "comparison",
    "caption": "Données fictives. Durée = traitement d’une entrée de 128 tokens + génération de 20 tokens ; chargement exclu ; 5 répétitions. Même test de 50 questions.",
    "refs": [
      "R17"
    ],
    "alt": "Tableau fictif : référence 4,8 Go, médiane 120 ms, qualité 47 sur 50 ; variante 3,9 Go, médiane 80 ms, qualité 46 sur 50.",
    "audience": "all",
    "steps": [
      "Fixer les critères",
      "Comparer les résultats",
      "Accepter ou refuser"
    ],
    "phase": 5
  },
  {
    "id": "pi",
    "chapter": "5 · Enquêter et tester",
    "eyebrow": "Du PC à la machine visée",
    "title": "Sur le Pi :<br><em>choisir, puis vérifier</em>.",
    "lead": "Un logiciel d’exécution, ou runtime, charge le modèle et fait ses calculs sur la carte.",
    "body": "<div class=\"points\"><div class=\"point\">Commencer par un modèle plus petit ; limiter le contexte à ce qui est utile.</div><div class=\"point\">Essayer une quantification prise en charge par le logiciel.</div><div class=\"point\">Comparer sur la même carte : mémoire, durée et réussite sur la tâche.</div></div>",
    "take": "Référence : version de départ. Variante : une seule modification. Garder les entrées et les critères identiques.",
    "scene": "pi",
    "caption": "Contrôler température, alimentation, versions et autres programmes. Le protocole technique lié dans les ressources décrit les mesures sur Pi.",
    "refs": [
      "R17",
      "R18"
    ],
    "alt": "Une version de référence et une version modifiée sont testées sur le même Raspberry Pi puis comparées.",
    "engineerBody": "<div class=\"points\"><div class=\"point\">llama.cpp est un logiciel d’exécution ; GGUF est un format de fichier, pas une méthode de quantification.</div><div class=\"point\">Tester aussi contexte, cache pris en charge et nombre de threads, les tâches de calcul simultanées.</div><div class=\"point\">Conserver les mesures brutes en CSV, un tableau en texte. Mesurer premier token, débit, RAM et qualité ; médiane et dispersion ; température contrôlée.</div></div>",
    "audience": "engineer",
    "steps": [
      "Fixer la référence",
      "Modifier une brique",
      "Mesurer sur la cible"
    ],
    "phase": 5
  },
  {
    "id": "research",
    "chapter": "5 · Enquêter et tester",
    "eyebrow": "Votre prochaine expérience",
    "title": "Une idée.<br><em>Un test qui tranche.</em>",
    "lead": "Formuler une question, proposer une hypothèse et chercher ce qui pourrait la contredire.",
    "body": "<div class=\"points\"><div class=\"point\"><strong>Hypothèse :</strong> « Je pense que ce changement réduit ce coût, parce que… »</div><div class=\"point\"><strong>Référence :</strong> comprendre une solution existante ; comparer à entrées et qualité fixées.</div><div class=\"point\"><strong>Réfutation :</strong> quel résultat montrerait que l’idée ne marche pas ?</div></div>",
    "take": "Un gain sur PC peut disparaître sur la cible. Garder les courbes et les échecs, puis choisir l’essai suivant.",
    "scene": "research",
    "control": "research",
    "caption": "Expliquer → prédire → mesurer → confronter → recommencer. La fiche prépare un essai ; elle ne contient aucun résultat de carte.",
    "refs": [
      "R17",
      "R19"
    ],
    "alt": "Le cycle d’enquête va d’une hypothèse au test PC puis au test sur la cible et revient vers une nouvelle idée.",
    "audience": "all",
    "steps": [
      "Formuler une idée",
      "Tester sur PC",
      "Confronter à la cible"
    ],
    "phase": 5
  },
  {
    "id": "end",
    "chapter": "5 · Enquêter et tester",
    "eyebrow": "Trois réflexes d’ingénieur",
    "title": "Une contrainte.<br>Une idée.<br><em>À vous de tester.</em>",
    "lead": "Le but est de savoir où chercher, quelle idée essayer et quelles preuves demander.",
    "body": "<div class=\"points\"><div class=\"point\">Nommer les limites du système avant de chercher un modèle.</div><div class=\"point\">Expliquer l’opération qui coûte, puis proposer une amélioration testable.</div></div>",
    "take": "Écrivez : ma brique, mon idée, le gain attendu et le test qui pourrait me donner tort.",
    "scene": "end",
    "caption": "Prolongez le cours dans le laboratoire : entraînez un petit modèle, ouvrez ses calculs et testez la quantification. Les mesures y sont locales au navigateur.",
    "refs": [],
    "alt": "Un triangle relie information, coût et preuve.",
    "audience": "all",
    "steps": [
      "Nommer une contrainte",
      "Choisir une brique",
      "Préparer une enquête"
    ],
    "phase": 5,
    "control": "lab"
  },
  {
    "id": "sources-memory",
    "chapter": "Pour approfondir · 1 / 3",
    "eyebrow": "Textes originaux",
    "title": "Représenter, apprendre,<br><em>interpréter</em>.",
    "lead": "Des sources pour préciser ce que les schémas simplifient.",
    "reading": [
      "R1",
      "R2",
      "R3",
      "R4",
      "R16"
    ],
    "take": "Les mécanismes observés dans une expérience ne constituent pas une carte complète de tous les modèles.",
    "scene": "none",
    "caption": "",
    "refs": [],
    "alt": ""
  },
  {
    "id": "sources-system",
    "chapter": "Pour approfondir · 2 / 3",
    "eyebrow": "Textes originaux",
    "title": "Compter les octets.<br><em>Changer les calculs.</em>",
    "lead": "Un gain publié garde le contexte matériel et le protocole du papier.",
    "reading": [
      "R5",
      "R6",
      "R7",
      "R8",
      "R9",
      "R10"
    ],
    "take": "Les simulations de cette présentation sont des exemples pédagogiques ; aucun LLM n’a été exécuté sur Pi ici.",
    "scene": "none",
    "caption": "",
    "refs": [],
    "alt": ""
  },
  {
    "id": "sources-models",
    "chapter": "Pour approfondir · 3 / 3",
    "eyebrow": "Articles et implémentations",
    "title": "Des pistes réelles.<br>Des limites <em>à vérifier</em>.",
    "lead": "Sélection de publications et de code ; ce n’est pas un classement exhaustif de la recherche.",
    "reading": [
      "R11",
      "R12",
      "R13",
      "R14",
      "R15"
    ],
    "take": "Revenir aux données et aux conditions d’essai avant de transporter un résultat vers sa propre machine.",
    "scene": "none",
    "caption": "",
    "refs": [],
    "alt": ""
  }
];
window.DISCOVERY_IDS = ["opening", "embedded-constraints", "learn", "embedding", "attention", "decode", "weights", "cache", "memory-total", "roofline", "quantize", "optimization-levers", "measurement-example", "research", "end", "sources-memory", "sources-system", "sources-models"];
