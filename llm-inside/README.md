# Dans la mémoire d’un modèle

Roland Cédric TAYO · INEM. Mini-cours en français, environ vingt minutes avec échanges : où se trouve l’information d’un modèle de langage, pourquoi l’inférence coûte cher, quelles pistes d’optimisation existent et comment les vérifier.

- [Présentation animée](https://rolln7drktayau.github.io/courses/llm-inside/)
- [PDF découverte](course.pdf) : 15 scènes essentielles et 3 pages de sources, soit 18 pages.
- [Parcours ingénieur](https://rolln7drktayau.github.io/courses/llm-inside/?audience=engineer) et [PDF complet](engineering.pdf) : 33 pages avec formules et approfondissements.
- [Protocole technique sur Pi](MESURER-SUR-PI.md).
- [Relecture selon trois publics](RELECTURE-PUBLICS.md).
- [Sources scientifiques](SOURCES.md), accessibles aussi au pied des scènes.
- [Corrections du texte initial](CORRECTIONS.md).
- [Relecture pédagogique et limites](RELECTURE.md).
- [Cours complet d’IA embarquée](../embedded-ai/).

## Utilisation

Ouvrir `index.html`. Aucun compte, aucune installation et aucun appel à un modèle ne sont nécessaires. Le support fonctionne hors ligne une fois ce dossier téléchargé.

Chaque schéma possède **trois étapes numérotées** et une étape courante visible. Les étapes sont cliquables ; flèches gauche/droite ou espace : les parcourir, puis changer de scène. Le repère supérieur distingue les cinq parties : cadrer, comprendre, localiser le coût, proposer, enquêter. `F` : plein écran ; `Home` : début ; `End` : dernière page. Le bouton **Ingénieur** ouvre les approfondissements ; **Découverte** revient au parcours accessible. Le lien PDF suit le parcours choisi. Les boutons Plan et Sources ouvrent des panneaux. La lecture automatique est facultative et s’arrête aux questions et à la conclusion. Les curseurs et boutons permettent de varier les hypothèses des calculs. Le bouton **Lire** propose une version continue, plus pratique sur un téléphone. La préférence système de réduction des animations est respectée.

Les mots soulignés sont cliquables : leur définition s’ouvre sans quitter la scène. Le bouton **Lexique** rassemble les définitions. Les mots essentiels et les symboles des équations sont aussi expliqués près de leur introduction pour que le PDF reste compréhensible seul.

Les scènes partagent un espace SVG : les objets se déplacent et les liaisons se recomposent. Les textes changent séparément ; l’animation sert la continuité du raisonnement. Les illustrations restent schématiques, et les nombres théoriques sont présentés comme tels. Le tableau référence/variante est explicitement fictif : ce n’est pas un benchmark. Son CSV distingue ce scénario des mesures réelles.

## Sources du support

- `assets/content.js` : texte, questions et bibliographie.
- `assets/keywords.js` : mots-clés et définitions.
- `assets/course.js` : dessins SVG, transitions, commandes et calculs pédagogiques.
- `assets/course.css` : présentation, lecture et impression.
- `source/build_pdf.py` : export vectoriel des scènes vers le PDF.
- `source/audit.py` : contrôles du contenu, des calculs, des interactions et du rendu.
- `verification/` : comptes rendus des contrôles réellement exécutés.

Pour fabriquer le PDF et relancer les contrôles : Python 3, `playwright`, `pymupdf`, et Chrome ou Chromium. Les scripts utilisent le chemin Chrome Windows de l’environnement de fabrication ; l’adapter si nécessaire.

```sh
python source/build_pdf.py
python source/audit.py
```

Le dossier est publié avec GitHub Pages dans le dépôt `rolln7drktayau/courses`. Aucun corrigé enseignant du TD ni donnée personnelle d’étudiant n’est inclus.

## Sortie attendue du cours

Nommer les contraintes d’une cible, choisir une brique coûteuse, proposer un changement et préparer un test capable de contredire l’hypothèse. Les scènes **Pistes** et **Enquête** donnent des exemples de questions et une fiche JSON à remplir, sans promettre de gain. Les courbes et essais PC puis cible appartiennent à l’enquête à réaliser.
