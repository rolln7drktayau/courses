# À l’intérieur du calcul

Roland Cédric TAYO · INEM

Laboratoire interactif accompagnant [Dans la mémoire d’un modèle](../llm-inside/). Ouvrir [le laboratoire](https://rolln7drktayau.github.io/courses/neural-lab/). Aucun compte, aucune installation ni clé d’API requis pour la page publiée. Le calcul reste local ; aucun corpus n’est téléversé. L’hébergeur reçoit les requêtes habituelles de chargement des fichiers.

## Apprentissage, puis inférence automatique sur des dialogues quotidiens

L’ouverture présente **1 · Apprendre**. **2 · Faire une prédiction** reste désactivé sans poids appris. Les textes sont des dialogues français originaux sur une pause café, un trajet en train et une promenade. [DailyDialog (Li et al., 2017)](https://aclanthology.org/I17-1099/) sert de référence de format : les textes livrés ici ne sont pas des extraits de son corpus.

Le fichier `conversation-data.json` contient trois dialogues de quatre tours et sept variantes d’exemples question/réponse. Le texte d’entraînement conserve les tours `Q:` / `R:` et les paragraphes. Les occurrences pondérées donnent soixante paires : pour « Bonjour ! Comment vas-tu ? », sept réponses « Je vais bien, merci. » et trois « Très bien, merci. ». Les autres échanges portent notamment sur un café, un rendez-vous à la gare et la météo.

Le parcours manuel montre une réception des données, une tokenisation par caractères, la préparation du contexte et de sa cible, puis une correction réelle des poids. « Entraîner les dialogues de démonstration » ouvre l’apprentissage complet du jeu. Le MLP de démonstration a une dimension de vecteurs de 12, un contexte de 12 caractères, 24 neurones cachés et 5 182 paramètres. La couche cachée utilise tanh. Le modèle est entraîné sur les caractères des réponses et sur leur saut de ligne final, en fournissant le préfixe déjà connu (teacher forcing).

Le bouton « Démarrer l’apprentissage » exécute **24 000 corrections** depuis zéro dans un travailleur du navigateur : graine 42, η=0,04, norme du gradient limitée à 1. À son terme, **la simulation bascule automatiquement vers l’inférence avec les poids obtenus**, suit la première prédiction et poursuit une réponse en phrase complète. L’utilisateur peut accélérer la relecture ou avancer par étapes. La réponse est également visible près de la scène. Un arrêt prématuré laisse l’apprentissage interrompu et ne lance pas cette inférence automatique.

« Utiliser un entraînement déjà effectué » charge le checkpoint réellement produit par le même protocole et lance également la démonstration d’inférence ; il ne prétend pas avoir entraîné un modèle instantanément. Le modèle restitue les réponses du petit jeu, par exemple « Je vais bien, merci. » ou « Oui, avec plaisir. ». Cela ne démontre aucune capacité de conversation générale, de mémoire longue ni de généralisation hors de ces exemples. La fenêtre de douze caractères est une limite explicitement affichée.

Une expérience de mini-Transformer (dimension 12, contexte 12, une tête, même objectif et mêmes réglages) a aussi été exécutée. Elle produit ici des réponses dégradées. Les essais et erreurs restent dans `validation/daily-transformer-attempt.json`. Le MLP a été retenu pour ce parcours, sur la base de ces essais limités ; ce n’est pas un classement général des architectures. Le Transformer reste disponible dans l’atelier avancé.

La fréquence observée et la probabilité apprise sont affichées séparément. Cliquer un caractère retrouve sa distribution et ses scores softmax. Le bouton 100 tirages effectue réellement cent choix dans cette distribution ; il ne génère pas cent réponses complètes. Les probabilités du modèle peuvent être trop confiantes. Elles ne sont pas remplacées artificiellement par les fréquences des exemples. Les mesures portent sur tous les cas d’entraînement, sans test indépendant.

Reproduire le checkpoint : `node neural-lab/tests/build_conversation.mjs`. Pour reproduire l’essai Transformer séparé : `node neural-lab/tests/build_conversation.mjs --transformer`. Les résultats initiaux défavorables et les réponses intermédiaires sont conservés. Le parcours `tests/daily-flow.py` exécute aussi une campagne complète dans le navigateur et vérifie le passage automatique, l’identité des poids, la conservation des retours à la ligne et l’absence d’inférence automatique après interruption.

## Plein écran et manipulation

La simulation est la zone principale dès l’ouverture ; les conversations sont placées plus bas et accessibles par le bouton « Conversation ». Les blocs sont debout sur un plan vertical, avec une caméra de face et un cadrage automatique. « Agrandir la simulation » l’isole dans la page, sur un fond assombri, sans mettre toute la page en plein écran. « Simulation en plein écran » place uniquement la scène et ses commandes en plein écran natif. L’option « Tout l’espace » reste disponible dans l’atelier avancé. Lecture, étapes, zoom, recentrage et sortie restent accessibles dans la scène. Glisser pour tourner ; molette ou boutons pour approcher. Après une manipulation, « Garder ma vue » conserve l’angle entre étapes. Échap quitte le plein écran. Un repli CSS est prévu si l’API native ne peut pas être utilisée.

Les briques du parcours sont arrondies, debout face au lecteur, avec une face colorée et une épaisseur visible lorsque la caméra tourne. Elles étaient auparavant disposées sur un plan horizontal : cette vue de table a été remplacée. Le bouton de recentrage restaure la vue frontale. Un clic de sélection ne verrouille pas la caméra ; une rotation ou un zoom manuel conserve ensuite la vue choisie entre les étapes. Leurs mots et valeurs restent le contenu réel de la trace. Les effets de présentation n’annoncent aucune performance matérielle.

## Parcours guidé pour découvrir

« Suivre ma phrase » démarre une animation continue : la phrase se déplace vers l’entrée, le tampon se remplit, les caractères deviennent des tokens, puis des identifiants. Les cartes se déplacent réellement dans la scène 3D ; la pause et la tête de lecture arrêtent ou repositionnent ces transformations. La vitesse choisie est celle de l’animation, pas une mesure du temps d’ingestion ou du processeur.

Pour apprendre, coller des données ou ouvrir un fichier `.txt` UTF-8 (100 à 12 000 caractères), puis cliquer « Ingérer mes données ». Un nouveau modèle est initialisé avec le vocabulaire de ce texte. Toute la séquence est reçue et tokenisée avant d’en extraire l’exemple à suivre. À la position i, le contexte contient jusqu’à douze caractères précédents et la cible est le caractère i ; il y a N−1 exemples possibles pour N caractères. Le numéro de l’exemple peut être changé. Aucun exemple ni caractère n’est inventé pour compléter les données. Modifier le texte demande de l’ingérer à nouveau.

L’animation montre un groupe de huit tokens à la fois et un extrait mobile du tampon pour les textes longs. Elle parcourt ainsi tout le flux, sans prétendre tout afficher simultanément. Après conversion, la fenêtre du mini-modèle (douze caractères pour les dialogues) est rendue explicite : les tokens hors fenêtre sont barrés. La cible d’apprentissage reste séparée de l’entrée. Le fichier est effectivement lu dans le navigateur ; le trajet visuel est la relecture ralentie des données et des calculs réels, pas un chronométrage d’I/O.

La page s’ouvre sur une seule transformation à la fois : lire le texte, le découper en caractères, attribuer les identifiants, sélectionner les lignes d’embedding, mélanger le contexte, calculer les probabilités, choisir un caractère et continuer.

« Apprendre à prédire » ajoute la réponse connue, la perte, le gradient, la correction et un nouvel essai sur la même entrée. Revenir sur une étape rejoue la trace ; une correction n’est jamais appliquée deux fois. Le texte « relecture avant correction » distingue le calcul précédent des poids déjà mis à jour.

Les couleurs ont un sens stable : bleu pour texte et identifiants, violet pour nombres appris, vert pour résultats, orange pour apprentissage. Les libellés donnent la même information ; la couleur n’est pas le seul repère. Le contour marque l’élément examiné. Il n’y a plus de flux de nombres décoratif dans ce parcours.

Un clic sur un token montre la ligne réellement sélectionnée. Les probabilités sont visibles avant le choix. La tokenisation du laboratoire est explicitement une tokenisation par caractères, différente d’une tokenisation par fragments de mots. Voir [Sennrich, Haddow et Birch (2016)](https://aclanthology.org/P16-1162/).

Le mode 2D présente les mêmes cartes sans WebGL. « Atelier avancé » donne accès aux fonctions ci-dessous. Le parcours guidé porte sur le MLP de démonstration ; le basculement vers l’atelier y charge ses poids.

## Atelier avancé

Les trois modèles peuvent aussi être chargés déjà entraînés sur le corpus public d’Alice (2 000 corrections, graine 42 ; empreinte vérifiée). Il s’agit de démonstrations propres au laboratoire, pas des corrigés des TD.

1. Garder les dialogues quotidiens fournis. Initialiser les poids.
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
python neural-lab/tests/daily-flow.py
python neural-lab/tests/presentation.py
```

Les fichiers de `examples/` se régénèrent avec `node neural-lab/tests/build_examples.mjs`.

Node n’a besoin d’aucun paquet. Pour lancer un test avec son propre serveur temporaire : `python neural-lab/tests/run_browser.py daily-flow.py`. Le serveur est arrêté à la fin du contrôle.

Les tests navigateur utilisent Python, Playwright et Chrome installés sur la machine de validation ; son chemin Chrome peut être adapté. `validation/results.json`, les CSV et `validation/browser.json` donnent les exécutions enregistrées, leur environnement et leurs limites. Une démonstration qui apprend une suite répétée reste une démonstration, pas un résultat publiable sur un modèle généraliste.

## Sources primaires

- Bengio, Ducharme, Vincent et Jauvin (2003), [A Neural Probabilistic Language Model](https://www.jmlr.org/papers/v3/bengio03a.html). Représentations apprises et modélisation probabiliste ; simplification pédagogique aux caractères ici.
- Vaswani et al. (2017), [Attention Is All You Need](https://arxiv.org/abs/1706.03762). Attention, masque, connexions résiduelles ; architecture réduite et tanh ici, sans prétendre reproduire le modèle de l’article.
- Stanford CS231n, [Backpropagation, Intuitions](https://cs231n.github.io/optimization-2/). Règle de chaîne et graphes de calcul.
- Jacob et al. (2018), [Quantization and Training of Neural Networks for Efficient Integer-Arithmetic-Only Inference](https://arxiv.org/abs/1712.05877). Référence de distinction avec une véritable inférence entière, qui n’est pas implémentée ici.
- [Three.js, documentation officielle](https://threejs.org/docs/). Affichage 3D uniquement. Version, empreintes et licence MIT dans `vendor/`.

Code pédagogique commenté en anglais ; explications en français. Aucun corrigé privé des TD n’est incorporé au laboratoire.
