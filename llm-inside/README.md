# Dans la mémoire d’un modèle

Roland Cédric TAYO · INEM. Mini-cours en français, environ vingt minutes avec échanges : où se trouve l’information d’un modèle de langage, pourquoi l’inférence coûte cher, quelles pistes d’optimisation existent et comment les vérifier.

- [Présentation animée](https://rolln7drktayau.github.io/courses/llm-inside/)
- [PDF](course.pdf) : les mêmes 23 scènes, construites et avec les réponses aux pauses questions.
- [Sources scientifiques](SOURCES.md), accessibles aussi au pied des scènes.
- [Corrections du texte initial](CORRECTIONS.md).
- [Cours complet d’IA embarquée](../embedded-ai/).

## Utilisation

Ouvrir `index.html`. Aucun compte, aucune installation et aucun appel à un modèle ne sont nécessaires. Le support fonctionne hors ligne une fois ce dossier téléchargé.

Flèches gauche/droite ou espace : revenir, construire un schéma, puis avancer. `F` : plein écran ; `Home` : début ; `End` : dernière page. Les boutons Plan et Sources ouvrent des panneaux. La lecture automatique est facultative et s’arrête aux questions et à la conclusion. Les curseurs et boutons permettent de varier les hypothèses des calculs. Le bouton **Lire** propose une version continue, plus pratique sur un téléphone. La préférence système de réduction des animations est respectée.

Les scènes partagent un espace SVG : les objets se déplacent et les liaisons se recomposent. Les textes changent séparément ; l’animation sert la continuité du raisonnement. Les illustrations restent schématiques, et les nombres théoriques sont présentés comme tels.

## Sources du support

- `assets/content.js` : texte, questions et bibliographie.
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
