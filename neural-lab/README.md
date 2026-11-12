# À l’intérieur du calcul

Roland Cédric TAYO · INEM

Laboratoire interactif accompagnant [Dans la mémoire d’un modèle](../llm-inside/). Ouvrir [le laboratoire](https://rolln7drktayau.github.io/courses/neural-lab/). Aucun compte, aucune installation ni clé d’API requis pour la page publiée. Le calcul reste local ; aucun corpus n’est téléversé. L’hébergeur reçoit les requêtes habituelles de chargement des fichiers.

## Conversation, données et probabilités

Ouvrir [la conversation](https://rolln7drktayau.github.io/courses/neural-lab/#conversation). Le jeu `conversation-data.json` contient quatre questions : `salut`, `merci`, `etat?`, `stop?`. Pour `salut`, sept exemples répondent `bonjour` et trois `salut`. Les autres réponses sont `de rien`, `pret`, `arret`. Les repères `Q:` et `R:` font partie du texte réellement encodé.

Le mini-Transformer de conversation (dimension 8, contexte 12, une tête) apprend à prévoir les caractères de la réponse seulement, y compris le saut de ligne final. Le préfixe connu est fourni à chaque étape (teacher forcing). « Charger les poids entraînés » ouvre le checkpoint réellement produit en 22 000 corrections ; « Entraîner depuis zéro » exécute 6 000 corrections dans un travailleur du navigateur. L’entraînement peut être arrêté et ses mesures exportées. Les conversations peuvent aussi être transférées au parcours d’ingestion, en sélectionnant le premier caractère d’une réponse comme cible.

La réponse n’est pas choisie dans une table de textes préécrits : chaque caractère est calculé par le réseau puis sélectionné, jusqu’au saut de ligne ou à la limite de longueur. Cliquer un caractère montre sa distribution et ses scores softmax. La vue statistique revient ensuite au premier caractère, pour le comparer aux exemples. Le bouton 100 tirages tire réellement dans cette distribution : il ne génère pas 100 réponses complètes. La graine rend les tirages reproductibles.

**Fréquence observée et probabilité apprise sont distinctes.** Les exemples `salut` donnent 70 % de premières lettres `b` et 30 % `s`. Le checkpoint calcule une distribution différente, conservée dans les résultats. Cette surconfiance est affichée, pas remplacée artificiellement par 70/30. On peut discuter calibration, taille du jeu et optimisation. Le bon résultat sur ces quatre questions d’entraînement ne démontre aucune capacité de conversation générale.

Reproduire le checkpoint : `node neural-lab/tests/build_conversation.mjs`, puis `node neural-lab/tests/refine_conversation.mjs`. La première campagne utilise la graine 42, η=0,04, 16 000 corrections. La seconde repart de ces poids : graine 43, η=0,004, 6 000 corrections. Le journal garde les résultats initiaux défavorables et signale une limite de sa première métrique : un sous-échantillon d’un cas sur cinq pouvait manquer des cibles contradictoires. La campagne de finition et le travailleur navigateur évaluent tous les cas. Les mesures sont sur les données d’entraînement, sans test indépendant.

## Plein écran et manipulation

La simulation est la zone principale dès l’ouverture ; les conversations sont placées plus bas et accessibles par le bouton « Conversation ». Les blocs sont debout sur un plan vertical, avec une caméra de face et un cadrage automatique. « Agrandir la simulation » l’isole dans la page, sur un fond assombri, sans mettre toute la page en plein écran. « Simulation en plein écran » place uniquement la scène et ses commandes en plein écran natif. L’option « Tout l’espace » reste disponible dans l’atelier avancé. Lecture, étapes, zoom, recentrage et sortie restent accessibles dans la scène. Glisser pour tourner ; molette ou boutons pour approcher. Après une manipulation, « Garder ma vue » conserve l’angle entre étapes. Échap quitte le plein écran. Un repli CSS est prévu si l’API native ne peut pas être utilisée.

Les briques du parcours sont arrondies, debout face au lecteur, avec une face colorée et une épaisseur visible lorsque la caméra tourne. Elles étaient auparavant disposées sur un plan horizontal : cette vue de table a été remplacée. Le bouton de recentrage restaure la vue frontale. Un clic de sélection ne verrouille pas la caméra ; une rotation ou un zoom manuel conserve ensuite la vue choisie entre les étapes. Leurs mots et valeurs restent le contenu réel de la trace. Les effets de présentation n’annoncent aucune performance matérielle.

## Parcours guidé pour découvrir

« Suivre ma phrase » démarre une animation continue : la phrase se déplace vers l’entrée, le tampon se remplit, les caractères deviennent des tokens, puis des identifiants. Les cartes se déplacent réellement dans la scène 3D ; la pause et la tête de lecture arrêtent ou repositionnent ces transformations. La vitesse choisie est celle de l’animation, pas une mesure du temps d’ingestion ou du processeur.

Pour apprendre, coller des données ou ouvrir un fichier `.txt` UTF-8 (100 à 12 000 caractères), puis cliquer « Ingérer mes données ». Un nouveau modèle est initialisé avec le vocabulaire de ce texte. Toute la séquence est reçue et tokenisée avant d’en extraire l’exemple à suivre. À la position i, le contexte contient jusqu’à six caractères précédents et la cible est le caractère i ; il y a N−1 exemples possibles pour N caractères. Le numéro de l’exemple peut être changé. Aucun exemple ni caractère n’est inventé pour compléter les données. Modifier le texte demande de l’ingérer à nouveau.

L’animation montre un groupe de huit tokens à la fois et un extrait mobile du tampon pour les textes longs. Elle parcourt ainsi tout le flux, sans prétendre tout afficher simultanément. Après conversion, la fenêtre du mini-modèle (six tokens dans le parcours de base, douze pour la conversation) est rendue explicite : les tokens hors fenêtre sont barrés. La cible d’apprentissage reste séparée de l’entrée. Le fichier est effectivement lu dans le navigateur ; le trajet visuel est la relecture ralentie des données et des calculs réels, pas un chronométrage d’I/O.

La page s’ouvre sur une seule transformation à la fois : lire le texte, le découper en caractères, attribuer les identifiants, sélectionner les lignes d’embedding, mélanger le contexte, calculer les probabilités, choisir un caractère et continuer.

« Apprendre à prédire » ajoute la réponse connue, la perte, le gradient, la correction et un nouvel essai sur la même entrée. Revenir sur une étape rejoue la trace ; une correction n’est jamais appliquée deux fois. Le texte « relecture avant correction » distingue le calcul précédent des poids déjà mis à jour.

Les couleurs ont un sens stable : bleu pour texte et identifiants, violet pour nombres appris, vert pour résultats, orange pour apprentissage. Les libellés donnent la même information ; la couleur n’est pas le seul repère. Le contour marque l’élément examiné. Il n’y a plus de flux de nombres décoratif dans ce parcours.

Un clic sur un token montre la ligne réellement sélectionnée. Les probabilités sont visibles avant le choix. La tokenisation du laboratoire est explicitement une tokenisation par caractères, différente d’une tokenisation par fragments de mots. Voir [Sennrich, Haddow et Birch (2016)](https://aclanthology.org/P16-1162/).

Le mode 2D présente les mêmes cartes sans WebGL. « Atelier avancé » donne accès aux fonctions ci-dessous. Le parcours guidé porte sur le mini-Transformer ; le basculement vers l’atelier y charge ses poids.

## Atelier avancé

Les trois modèles peuvent aussi être chargés déjà entraînés sur le corpus public d’Alice (2 000 corrections, graine 42 ; empreinte vérifiée). Il s’agit de démonstrations propres au laboratoire, pas des corrigés des TD.

1. Garder le mini-Transformer et le corpus d’Alice. Initialiser les poids.
2. Cliquer les quatre étapes : prédiction, perte, gradients, correction. Observer les valeurs avant/après.
3. Le bouton « 10 corrections au ralenti » exécute les mêmes quatre étapes, avec une pause entre chacune ; il est possible de le suspendre. Ouvrir une brique, une matrice ou une activation. Remonter les opérations jusqu’aux paramètres. Rejouer les opérations d’un résultat.
4. Entraîner 300 corrections, puis prédire quelques caractères. Une correction utilise une fenêtre ; ce n’est pas une époque.
5. Écrire une hypothèse, comparer les précisions, exporter les CSV. Refaire l’essai avec les graines 42, 43 et 44. Conserver un résultat nul ou défavorable.

La vue 3D tourne avec la souris, se rapproche à la molette et se sélectionne au clic. La vue 2D et les boutons donnent accès aux mêmes briques. Les parents d’une opération peuvent être ouverts successivement. Ce zoom s’arrête aux feuilles d’un graphe fini : aucune opération fictive n’est ajoutée.

## Ce qui est calculé

- **Bigramme** : lecture d’une ligne de poids selon le dernier caractère, biais, softmax.
- **MLP** : embeddings concaténés pour une fenêtre fixe (PAD à gauche), couche cachée tanh, projection et softmax.
- **Mini-Transformer** : embeddings de caractères et de positions appris, un bloc pré-normalisé, une tête d’attention causale Q/K/V, projection O, connexion résiduelle, normalisation, réseau tanh à deux projections, seconde connexion résiduelle, projection vers le vocabulaire.
- Perte d’entropie croisée sur la dernière position : `L = −ln(p[bonne lettre])` ; calcul stable par log-sum-exp. La perte est en nats. La précision mesure la fraction des bonnes lettres arrivant en tête et peut évoluer autrement que la perte.
- Rétropropagation scalaire écrite dans `engine.js`, par règle de chaîne. SGD, pas η, norme du gradient limitée à 1. Chaque correction est réelle. L’erreur de signe proposée inverse réellement la correction.
- Cache K/V réellement réutilisé pendant l’extension d’un préfixe. Si la fenêtre glisse, les positions apprises changent et le cache est reconstruit. Pas de cache d’entraînement.

La vue entière représente les dépendances entre briques ; le graphe scalaire expose le détail numérique. Les particules rejouent des valeurs à vitesse humaine. Leur mouvement ne représente ni un cycle CPU ni un bus matériel. Q, K et V sont trois projections de la même entrée.

## Données et protocole

Trois corpus synthétiques répétés, livrés dans le code, ou texte local de 100 à 12 000 caractères. Vocabulaire construit sur l’ensemble du corpus (information de prétraitement partagée, pas un protocole de vocabulaire tenu à l’écart) ; PAD et inconnu sont explicites. Découpage chronologique du texte : 70 % entraînement, 15 % validation, 15 % test réservé. Aucune fenêtre ne franchit une frontière. Les motifs répétés réapparaissent dans les partitions : **ce jeu ne prouve pas la généralisation à une langue**. Le test réservé n’est pas utilisé par les comparaisons du laboratoire.

Les courbes portent sur 20 fenêtres fixes par partition, les comparaisons de précision sur 48 fenêtres de validation identiques pour toutes les précisions. Une graine fixe les poids et les tirages. Une campagne lancée en une fois est reproductible ; relancer une campagne après une pause réinitialise le flux d’échantillonnage avec le compteur de corrections, ce qui diffère d’un lancement continu.

## Quantification et mémoire

Le moteur et ses opérations utilisent les nombres JavaScript Float64. Les poids maîtres sont Float64. La référence « 32 bits » arrondit ses poids avec `Math.fround`, puis calcule en Float64.

Pour 8, 4 et 2 bits : quantification symétrique des matrices, `Q = 2^(bits−1)−1`, `s = max(|w|)/Q`, `q = clamp(round(w/s), −Q, Q)`, `w_reconstruit = s*q`. Les niveaux sont symétriques : à 2 bits, cela donne **−1, 0, +1**, soit trois valeurs utilisées sur quatre codes possibles. Une échelle globale ou une par matrice. Biais et gains sont arrondis en float32, sans quantification entière. Les échelles sont stockées en nombres JavaScript ; leur budget float32 est théorique.

**C’est une simulation de quantification des poids.** Aucune matrice n’est compactée en mémoire dans l’application et aucun noyau entier n’est exécuté. Les budgets affichés comptent le stockage idéal des matrices compactées, les vecteurs float32 et les échelles float32 séparément. Cache maximal : `2 × contexte × dimension × 4` octets, hypothèse float32. Activations temporaires, trace autodiff, objets JS, runtime et OS sont exclus. **La RAM réelle et l’énergie ne sont pas mesurées.**

## Chronométrage

Après échauffement, K double jusqu’à ce que K inférences de référence prennent au moins 100 ms (limite de sécurité 65 536 appels). Cinq répétitions alternent l’ordre référence/version quantifiée ; médiane et min–max sont affichés, checksum et temps bruts conservés. Horloge : `performance.now()` dans un Web Worker du navigateur.

Ce temps inclut la construction du graphe scalaire pédagogique. Il ne mesure ni une implémentation optimisée, ni une vitesse GPU, ni un Raspberry Pi. Une baisse du budget de stockage ne garantit pas une accélération de ce moteur. La charge du système n’est pas maîtrisée ; le navigateur et le nombre de processeurs logiques sont consignés dans le protocole exporté. Une validation sur cible reste nécessaire.

## Exporter et reprendre

Exporter les poids produit un JSON contenant modèle, dimensions, corpus, vocabulaire, poids, historique et SHA-256 du contenu. Importer vérifie l’empreinte, les dimensions et les valeurs finies. L’empreinte prouve l’intégrité du contenu, pas son auteur. Le corpus est inclus : vérifier sa confidentialité avant de partager le fichier.

Exporter une expérience fournit `protocol.json`, `training.csv`, `quantization.csv`, `timings.csv` et une courbe SVG. Le navigateur peut demander d’autoriser plusieurs téléchargements. La configuration et les graines restent indispensables pour interpréter les courbes. Les poids s’exportent séparément.

## Exécuter et vérifier localement

Depuis la racine du dépôt :

```sh
python -m http.server 8766
```

Puis `http://localhost:8766/neural-lab/`. Servir les fichiers par HTTP est nécessaire pour les modules et le travailleur ; ne pas ouvrir directement `index.html` en `file://`.

```sh
node neural-lab/tests/engine.test.mjs
python neural-lab/tests/browser.py
python neural-lab/tests/journey.py
python neural-lab/tests/ingestion.py
node neural-lab/tests/conversation.test.mjs
python neural-lab/tests/conversation-browser.py
python neural-lab/tests/presentation.py
```

Les fichiers de `examples/` se régénèrent avec `node neural-lab/tests/build_examples.mjs`.

Node n’a besoin d’aucun paquet. Les tests navigateur utilisent Python, Playwright et Chrome installés sur la machine de validation ; son chemin Chrome peut être adapté. `validation/results.json`, les CSV et `validation/browser.json` donnent les exécutions enregistrées, leur environnement et leurs limites. Une démonstration qui apprend une suite répétée reste une démonstration, pas un résultat publiable sur un modèle généraliste.

## Sources primaires

- Bengio, Ducharme, Vincent et Jauvin (2003), [A Neural Probabilistic Language Model](https://www.jmlr.org/papers/v3/bengio03a.html). Représentations apprises et modélisation probabiliste ; simplification pédagogique aux caractères ici.
- Vaswani et al. (2017), [Attention Is All You Need](https://arxiv.org/abs/1706.03762). Attention, masque, connexions résiduelles ; architecture réduite et tanh ici, sans prétendre reproduire le modèle de l’article.
- Stanford CS231n, [Backpropagation, Intuitions](https://cs231n.github.io/optimization-2/). Règle de chaîne et graphes de calcul.
- Jacob et al. (2018), [Quantization and Training of Neural Networks for Efficient Integer-Arithmetic-Only Inference](https://arxiv.org/abs/1712.05877). Référence de distinction avec une véritable inférence entière, qui n’est pas implémentée ici.
- [Three.js, documentation officielle](https://threejs.org/docs/). Affichage 3D uniquement. Version, empreintes et licence MIT dans `vendor/`.

Code pédagogique commenté en anglais ; explications en français. Aucun corrigé privé des TD n’est incorporé au laboratoire.
