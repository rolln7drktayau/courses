# Commencer le TD

Roland Cédric TAYO · INEM.

## Ce que vous allez réaliser

Générer trois signaux, apprendre sur PC un petit réseau de **388 paramètres**, puis faire exécuter ses prédictions par un **Raspberry Pi sous Linux**. Ensuite, modifier une seule brique de calcul et vérifier si le système gagne réellement en temps ou en mémoire. Le projet ne demande ni reconnaissance vocale, ni capteur, ni grand modèle de langage.

Le cours storyboard donne une vue d’ensemble. Les ateliers du TD et le travail personnel permettent de passer des calculs à un programme vérifié. Les équations et les règles complètes restent dans `assignment.pdf`.

## Ce qu’il faut

- Par groupe : un PC, un Raspberry Pi identifié, son alimentation adaptée et une microSD avec Raspberry Pi OS. Avec environ 14 Pi pour 35 étudiants, sept groupes de cinq ont chacun au moins une carte. Un accès réseau permet SSH ; écran et clavier sont une autre possibilité.
- Langages du TD : **Python 3 sur PC pour les données et l’apprentissage ; C pour l’inférence et l’optimisation sur Pi**. Seule la prédiction est portée en C, pas l’entraînement. Git et les outils de tests accompagnent le travail.
- Pour le Pi : Git, GCC et Make ; compiler directement sur le Pi. Vérifier démarrage, transfert et lancement avant les séances de mesures. Noter modèle, architecture 32/64 bits, RAM et version de l’OS.
- Pour rendre le travail : GitHub et accès de l’enseignant `rolln7drktayau`. Matplotlib peut servir aux figures ; Overleaf est facultatif ; une rédaction claire en anglais est recommandée.

Aucun GPU, capteur, jeu de données téléchargé ou service payant n’est requis. Une mesure d’énergie exige un instrument adapté : sans instrument, vous ne prétendez pas avoir mesuré l’énergie. Le Raspberry Pi est la seule cible matérielle demandée ; aucune Nucleo n’est nécessaire.

## Prérequis à vérifier avant de commencer

Vous savez écrire et tester une fonction, parcourir un tableau, compiler ou lancer un programme et utiliser un terminal. Vous savez calculer une somme de produits et une dérivée simple. La règle de chaîne et l’addition des gradients d’un paramètre partagé sont à travailler avec les rappels du sujet et les annexes du cours.

Si ces prérequis manquent, le projet complet ne se termine pas raisonnablement dans les seules séances. Le signaler au premier point de passage, avant de lancer un entraînement incompris.

## Les quatre passages

1. **Données et fonctions.** Suivre l’atelier A (§8 du sujet) : faire un petit calcul sur papier, écrire sa fonction Python et le transformer en test. Générer ensuite les séquences, vérifier les fenêtres et tracer les signaux. Montrer une fiche de calcul avant d’assembler le réseau.
2. **Apprentissage.** Suivre l’atelier B (§9) : calculer un petit gradient à la main, programmer le retour et vérifier les dérivées. Assembler le réseau ; entraîner et comparer les deux références. Tracer perte train et erreur de validation. Comparer aussi au témoin analytique du simulateur. Chronométrer deux époques avant le lancement complet.
3. **Déploiement.** Porter uniquement les fonctions de prédiction en C. Tester le petit calcul, puis comparer Python PC, C PC et C Pi sur les mêmes fenêtres et poids. Sur Pi, récupérer le tag Git et les fichiers exportés ; écrire les cibles `make test-c`, `make inference` et `make benchmark`, puis les utiliser. Le README indique les arguments et chemins exacts. Le Pi exécute lui-même les calculs ; récupérer ses CSV.
4. **Expérience.** Écrire une hypothèse et conserver la référence. Modifier une seule brique, vérifier ses sorties, puis répéter les mesures sur Pi. Tracer le temps selon les dimensions pour les deux versions, avec dispersion, et montrer l’effet sur le réseau entier. Un gain n’est pas obligatoire.

## Écrire à la main, avec quels outils ?

Vous écrivez projection, ReLU, résidu, perte, gradients, mise à jour et inférence avec des boucles. Les bibliothèques standard sont autorisées pour mathématiques, fichiers, temps, mémoire et aléatoire. Matplotlib sert aux figures, les outils de tests aux vérifications. Pas de framework, autodifférentiation, NumPy ou BLAS pour réaliser le modèle à votre place. Aucun entraînement C n’est demandé.

Chaque groupe conserve une fiche : fonction → entrée → résultat manuscrit → résultat du test → rôle. Les petits exemples sont calculés sur papier ; les 388 paramètres du réseau ne le sont pas. À chaque point de passage, un membre différent explique ce qui a été vérifié.

Les tests décident du passage à l’étape suivante ; un pair les relit. Le sujet fixe les données, le réseau, les réglages initiaux, les tolérances et le protocole. Aucune valeur technique n’est à demander à l’enseignant. La première expérience est réalisée en TD ; son approfondissement et le rapport continuent ensuite.

## Mesurer sur le Pi

Pour garder le même chronométrage C, travailler sous Linux sur PC et Pi ; sur un PC Windows, WSL permet ce parcours (installation officielle : https://learn.microsoft.com/en-us/windows/wsl/install). Sous Raspberry Pi OS, installer Git, GCC et Make avec `sudo apt install git build-essential time` après mise à jour de la liste des paquets. Les commandes du projet restent écrites par l’équipe.

En C sous Linux, utiliser `clock_gettime(CLOCK_MONOTONIC, ...)` et convertir secondes/nanosecondes dans une seule unité. Mesurer le pic mémoire du processus avec `/usr/bin/time -v` autour de son exécution ; noter le champ Maximum resident set size et son unité, séparément des tailles de tableaux calculées. La mémoire d’un processus Python ne se compare pas directement à celle des seuls buffers C.

Utiliser le même code C et les options `-O2` pour référence et variante, sur PC puis sur Pi. Échauffer 100 appels. Pour chaque forme et campagne, doubler K à partir de 1 jusqu’à un lot de référence d’au moins 100 ms (plafond : 2^24 appels). Garder K pour les deux versions ; si le plafond ne suffit pas, signaler la limite.

Faire trois campagnes de dix paires, en inversant l’ordre à chaque paire. Garder durées et K, puis calculer durée/K. Exclure fichiers et affichage du chronométrage ; varier les entrées de manière déterministe et utiliser le checksum après le lot. Tracer médiane et min–max sur PC et Pi. Aucun gain minimum n’est exigé ; les recouvrements et résultats négatifs doivent être expliqués.

Noter charge, fréquence CPU, température et refroidissement. Comparer sur une même carte, pas les temps bruts de modèles de Pi différents. Une horloge monotone sous Linux mesure le temps écoulé ; elle n’établit pas une garantie temps réel.

Compter séparément poids, buffers, fichiers et mémoire du processus. Le petit réseau ne saturera pas la RAM du Pi : on étudie ses coûts, sans prétendre démontrer un manque de mémoire ni un temps réel garanti.

## La petite recherche attendue

Exemple de question : **sur notre carte, calculer deux sorties ensemble est-il préférable à la référence scalaire, et à partir de quelles dimensions ?** Vous pouvez aussi étudier un ordre de boucles ou la réutilisation de buffers, avec les mêmes poids et un calcul numériquement vérifié.

Un assistant peut aider à comprendre, coder et proposer des hypothèses. Aucune partie ne rend l’IA « inutile ». En revanche, une suggestion ou un texte généré ne démontre ni la correction ni le gain sur votre carte. La preuve attendue est une expérience traçable : version du code → configuration → binaire → mesures brutes → figure → conclusion.

À l’oral, chaque membre explique une fonction, prédit l’effet d’une condition nouvelle puis la teste. Cette vérification individuelle et la reproduction par une autre équipe rendent le travail observable ; elles ne garantissent pas une absence totale de triche.

Un gain nul, une variante plus lente ou un modèle linéaire meilleur restent des résultats recevables, s’ils sont établis et interprétés. Le sujet vise une initiation à la recherche expérimentale ; il ne promet ni record ni publication acceptée.

## Premier geste

Lire `assignment.pdf`, identifier la carte, créer le dépôt et inviter l’enseignant. Écrire ensuite le générateur et tracer une séquence. Ne télécharger ni réseau prêt à l’emploi ni corrigé. Le ZIP d’article contient uniquement un gabarit et des figures illustratives.

## Vocabulaire à consulter

Le glossaire Embedded France–Eclipse est lié dans les ressources du cours et à la fin du sujet. Repères : données au chapitre 2, optimisation au 3, outils et matériel aux 5–6, mesures au 9, versions et déploiement au 11. Il complète le cours ; il ne constitue pas une lecture intégrale obligatoire.

## Si un contrôle échoue

- Mauvais nombre de fenêtres : vérifier le retrait des 32 instants, la fenêtre de 16 et la cible suivante ; ne pas traverser les séquences.
- Gradient incorrect : revenir au calcul réduit, garder les valeurs intermédiaires, cumuler les usages partagés et moyenner le lot une seule fois.
- Perte non finie : arrêter ; contrôler normalisation, gradients et mise à jour. Ne pas augmenter le nombre d’époques au hasard.
- Sorties Python/C différentes : vérifier ordre des poids, normalisation, aplatissement et type numérique. Garder la tolérance du sujet.
- Résultats de temps instables : noter charge et chauffe, fermer les tâches non nécessaires et répéter la campagne entière sans supprimer les passages lents.
- Variante plus lente : conserver les mesures. Expliquer le résultat et proposer une prochaine expérience ; un résultat négatif n’est pas une faute.
