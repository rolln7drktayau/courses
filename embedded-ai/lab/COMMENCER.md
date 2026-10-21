# Commencer le TD

Roland Cédric TAYO · INEM.

## Ce que vous allez réaliser

Générer trois signaux, apprendre sur PC un petit réseau de **388 paramètres**, puis faire exécuter ses prédictions par un **Raspberry Pi sous Linux**. Ensuite, modifier une seule brique de calcul et vérifier si le système gagne réellement en temps ou en mémoire. Le projet ne demande ni reconnaissance vocale, ni capteur, ni grand modèle de langage.

Le cours storyboard de trois heures donne une vue d’ensemble. Il ne remplace pas les 14 heures de cours du module, les 14 heures de TD et le travail personnel jusqu’au rendu. Les équations et les règles complètes restent dans `assignment.pdf`.

## Ce qu’il faut

- Par groupe : un PC, un Raspberry Pi identifié, son alimentation adaptée et une microSD avec Raspberry Pi OS. Avec environ 14 Pi pour 35 étudiants, sept groupes de cinq ont chacun au moins une carte. Un accès réseau permet SSH ; écran et clavier sont une autre possibilité.
- Sur PC : Git, un langage maîtrisé et ses tests. **Python standard pour apprendre sur PC, puis C/C++ pour la carte** est un choix simple ; un autre langage reste possible s’il est réellement pris en charge par la cible.
- Pour le Pi : Git et le langage choisi ; compiler directement sur le Pi simplifie le déploiement C/C++. Vérifier démarrage, transfert et lancement avant les séances de mesures. Noter modèle, architecture 32/64 bits, RAM et version de l’OS.
- Pour rendre le travail : GitHub et accès de l’enseignant `rolln7drktayau`. Matplotlib peut servir aux figures ; Overleaf et l’anglais sont des options bonifiées selon le barème.

Aucun GPU, capteur, jeu de données téléchargé ou service payant n’est requis. Une mesure d’énergie exige un instrument adapté : sans instrument, vous ne prétendez pas avoir mesuré l’énergie. Le Raspberry Pi est la seule cible matérielle demandée ; aucune Nucleo n’est nécessaire.

## Prérequis à vérifier avant de commencer

Vous savez écrire et tester une fonction, parcourir un tableau, compiler ou lancer un programme et utiliser un terminal. Vous savez calculer une somme de produits et une dérivée simple. La règle de chaîne et l’addition des gradients d’un paramètre partagé sont à travailler avec les rappels du sujet et les annexes du cours.

Si ces prérequis manquent, le projet complet ne se termine pas raisonnablement dans les seules séances. Le signaler au premier point de passage, avant de lancer un entraînement incompris.

## Les quatre passages

1. **Données et fonctions.** Générer les 24 séquences ; séparer apprentissage, validation et test avant les fenêtres. La première fenêtre conservée va de t=32 à 47 et prédit x1(48). Vérifier les 2 304 / 576 / 576 fenêtres et la normalisation calculée sur l’apprentissage seul.
2. **Apprentissage.** Vérifier les gradients, puis entraîner. Comparer au dernier point observé et au modèle linéaire. La meilleure méthode peut être la plus simple. Chronométrer deux époques avant un lancement complet.
3. **Déploiement.** Transférer sources, poids et données par Git, SCP ou clé USB ; compiler si nécessaire et exécuter localement sur le Pi. Faire tourner les mêmes données et poids sur PC et sur Pi. Comparer les sorties avant tout chronométrage. La carte calcule elle-même ; le PC peut recueillir les résultats.
4. **Expérience.** Écrire une hypothèse, figer une référence, tester une variante et répéter les mesures sur carte. Générer les figures depuis les CSV, conserver les versions Git et expliquer les limites.

## Mesurer sur le Pi

Échauffer le calcul, puis chronométrer des lots sans fichiers ni affichage avec une horloge monotone. Alterner référence et variante sur le même Pi, dans le même langage, avec les mêmes options ; répéter au moins trois campagnes. Noter charge, fréquence CPU, température et refroidissement : Linux et la chauffe peuvent changer le résultat. Les gains se comparent sur une même carte, pas entre modèles de Pi différents.

Compter séparément poids, buffers, fichiers et mémoire du processus. Le petit réseau ne saturera pas la RAM du Pi : on étudie ses coûts, sans prétendre démontrer un manque de mémoire ni un temps réel garanti.

## La petite recherche attendue

Exemple de question : **sur notre carte, calculer deux sorties ensemble est-il préférable à la référence scalaire, et à partir de quelles dimensions ?** Vous pouvez aussi étudier un ordre de boucles ou la réutilisation de buffers, avec les mêmes poids et un calcul numériquement vérifié.

Un assistant peut aider à comprendre, coder et proposer des hypothèses. Aucune partie ne rend l’IA « inutile ». En revanche, une suggestion ou un texte généré ne démontre ni la correction ni le gain sur votre carte. La preuve attendue est une expérience traçable : version du code → configuration → binaire → mesures brutes → figure → conclusion.

À l’oral, chaque membre explique une fonction, prédit l’effet d’une condition nouvelle puis la teste. Cette vérification individuelle et la reproduction par une autre équipe rendent le travail observable ; elles ne garantissent pas une absence totale de triche.

Un gain nul, une variante plus lente ou un modèle linéaire meilleur restent des résultats recevables, s’ils sont établis et interprétés. Le sujet vise une initiation à la recherche expérimentale ; il ne promet ni record ni publication acceptée.

## Premier geste

Lire `assignment.pdf`, identifier la carte, créer le dépôt et inviter l’enseignant. Écrire ensuite le générateur et tracer une séquence. Ne télécharger ni réseau prêt à l’emploi ni corrigé. Le ZIP d’article contient uniquement un gabarit et des figures illustratives.
