# Passer du cours à une mesure sur Raspberry Pi

Roland Cédric TAYO · INEM. Protocole proposé ; les commandes ci-dessous n’ont pas été exécutées sur un Pi pour fabriquer ce mini-cours. Aucun résultat de carte n’est fourni.

## Choisir une référence réaliste

Commencer par un modèle assez petit pour la RAM disponible, avec une licence et un format compatibles avec le logiciel. `llama.cpp` est un logiciel d’exécution ; GGUF est un format de fichier ; une quantification est une méthode de représentation. Conserver le modèle exact, son SHA-256, le tokenizer et la version du logiciel.

Avant un benchmark, vérifier le chargement, une sortie connue et le comportement lorsque le contexte augmente. Estimer poids + cache + valeurs temporaires + logiciel/système, puis mesurer. La présence d’un fichier dans le stockage ne prouve pas que l’application tient en RAM. L’échange de mémoire avec le stockage, appelé swap, peut rendre les temps très différents.

## Une modification à la fois

Définir la tâche, les données de test, le seuil de qualité et la contrainte de temps avant les mesures. Exemples de variantes : taille du modèle, précision des poids, longueur du contexte, nombre de threads. Un thread est une tâche d’exécution ; en ajouter ne garantit pas un gain. Le cache peut également être quantifié si le modèle et le runtime le prennent en charge, avec une nouvelle vérification de qualité.

La distillation apprend à un modèle plus petit à reproduire certains comportements d’un modèle plus grand. L’élagage retire des éléments du réseau. Ces pistes demandent leur propre apprentissage ou une prise en charge adaptée ; elles ne sont pas des options magiques à activer.

## Exemple de commande de performance

Suivre les [instructions de compilation officielles de llama.cpp](https://github.com/ggml-org/llama.cpp/blob/master/docs/build.md), puis consulter `llama-bench --help` pour la version utilisée. Exemple CPU, pour une carte où 1, 2 et 4 threads sont pertinents :

```sh
./build/bin/llama-bench -m model.gguf -p 128 -n 64 -r 5 -t 1,2,4 -ngl 0 -o json > bench.json
```

`model.gguf` est à remplacer par le fichier choisi. La commande demande des tests de traitement de 128 tokens et de génération de 64 tokens, répétés cinq fois, pour plusieurs nombres de threads. `-ngl 0` conserve ce test sur CPU. Ne pas désactiver l’échauffement sans justification.

Le JSON documenté contient les échantillons `samples_ns` et `samples_ts`. Conserver ces valeurs brutes ; calculer médiane, minimum et maximum par configuration. Le logiciel rapporte également moyenne et écart-type : ne pas les renommer « médiane ». Les unités et le nombre de tokens doivent accompagner les nombres.

**Ce que ce benchmark ne démontre pas :** la qualité des réponses, le temps de chargement ou le délai complet de votre application jusqu’au premier token. Mesurer séparément ces étapes avec des points de chronométrage explicités. Pour la RAM, conserver le pic résident du processus et une observation de la mémoire du système ; ce sont des périmètres distincts.

## Comparer sans confondre les causes

- Faire des essais de chauffe, puis alterner référence et variante ; conserver toutes les répétitions.
- Fixer modèle, entrée, tokens générés, contexte, threads, options et version, sauf le facteur étudié.
- Noter modèle de carte, OS, température, refroidissement, alimentation, fréquence et éventuel bridage thermique. Les outils `vcgencmd` sont décrits dans la [documentation Raspberry Pi](https://www.raspberrypi.com/documentation/computers/os.html).
- Tester la qualité sur des exemples indépendants : mêmes questions, même règle de correction, résultats individuels conservés. Un nombre de réponses correctes n’est pas interchangeable avec la perplexité, une mesure de prédiction des tokens.
- Si un instrument adapté mesure l’alimentation, préciser si l’énergie inclut toute la carte et le repos. Sans instrument, écrire « énergie non mesurée ».

Un fichier de résultats indique au minimum configuration, répétition, durée, unité, qualité et température si disponible. Le manifeste relie code, données, modèle et options. Conclure seulement sur la tâche, le contexte et la carte réellement testés.

[Documentation originale de llama-bench](https://github.com/ggml-org/llama.cpp/tree/master/tools/llama-bench) · [Spécification GGUF](https://github.com/ggml-org/ggml/blob/master/docs/gguf.md)

## Distinguer vitesse moyenne et temps réel

Une exigence de temps réel porte sur une échéance à respecter, pas seulement sur une moyenne ou une médiane agréable. Mesurer gigue, dépassements et comportement en surcharge selon l’usage. Le plus grand temps observé n’est pas, à lui seul, une preuve de borne garantie. Définir également le comportement prévu lorsque l’entrée sort du domaine connu ou qu’un résultat n’est pas assez fiable.

Avant de modifier une brique, examiner sa version de référence : article, code, données et conditions matérielles. Reproduire d’abord ce que l’on peut vérifier, puis documenter une seule modification et l’essai qui pourrait l’invalider.
