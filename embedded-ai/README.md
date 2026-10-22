# Une lampe qui comprend, même sans Internet

**Roland Cédric TAYO · INEM.** Cours en français, trois heures avec pause et échanges.

[Présentation narrative](https://rolln7drktayau.github.io/courses/embedded-ai/) · [PDF](https://rolln7drktayau.github.io/courses/embedded-ai/course.pdf) · [Plan](https://rolln7drktayau.github.io/courses/embedded-ai/course-plan.pdf)

Ce storyboard est le cours principal. L’[énoncé du TD et les ressources étudiantes](https://rolln7drktayau.github.io/courses/embedded-ai/lab/) prolonge le cours. Aucun corrigé enseignant n’est inclus.

## Parcours

Alice voudrait commander une lampe à la voix. Cette situation permet d’expliquer, dans l’ordre, le besoin d’un modèle, ses calculs, le choix de les exécuter dans un objet et les contraintes qui apparaissent. Quatre questions orales ouvrent le parcours après la couverture, sans score ni outil externe. Six chapitres et 40 scènes conduisent du service attendu à une petite question de recherche. Six pauses questions demandent de calculer, d’expliquer ou de choisir sous contraintes. Vingt-six pages complémentaires rassemblent extensions, vocabulaire, lectures et réponses.

L’idée de chaque scène est résumée en une phrase. Les termes sont expliqués lors de leur introduction ; les formules et leurs limites restent accessibles. Ce choix facilite une première lecture, sans prétendre qu’une lecture seule qualifie un ingénieur ou qu’un enfant maîtrise les mathématiques de l’apprentissage.

## Présenter

- **→ / Espace** : dévoiler une étape, puis avancer.
- **←** : revenir. **A** : tout montrer sur la page.
- **T** : sommaire, recherche et accès direct aux six pauses questions.
- **D** : explications complémentaires. **F** : plein écran.
- Le PDF affiche les scènes entières ; les réponses raisonnées et deux pages de liaison vers le TD sont en annexe.

L’HTML contient ses scripts, styles et illustrations : il peut se lire sans connexion. Les liens vers articles et TD nécessitent une connexion. Le bouton de liaison modifie un schéma et l’illustration ; il ne réalise pas un test réseau. Le chronométrage de sommes mesure réellement le navigateur, sans en déduire des performances sur Pi ou MCU. Les budgets et résultats du tableau de décision sont fictifs et signalés comme tels.

Alice est fictive. Les chercheurs et leurs contributions sont documentés dans [SOURCES.md](SOURCES.md). Les schémas historiques sont des reconstructions pédagogiques et non des portraits ou photographies d’archives. Le petit réseau numérique ne reconnaît pas la voix : il sert à suivre chaque calcul. Le TD poursuit le raisonnement sur une autre tâche, la prédiction d’un signal.

Le cours relie explicitement quatre repères au TD : chaîne complète (scène 16), éléments à déployer (19), coûts du calcul et de la mémoire (23 et 28), preuves de mesure (30–34). La scène 36 présente le cycle Python PC → inférence C PC → Pi → CSV → courbes → nouvelle variante. Le Pi chronomètre son propre calcul ; le PC récupère et analyse les résultats. Le TD conserve quatre séances de 3 h 30, puis le travail personnel.

Le [glossaire Embedded France–Eclipse](https://pages.eclipse.dev/eclipse/aidge/embedded-ai-glossary/embedded-ai-glossary.fr.pdf), v1.1 du 22 juillet 2026, CC BY 4.0, est une référence de vocabulaire non normative. Lire selon le besoin : données (§2), modèles et optimisation (§3), outils et matériel (§5–6), mesures (§9), confiance et cycle de vie (§10–11). Le programme n’exige pas d’en apprendre les 83 pages. Les diapositives distinguent puissance/énergie et percentile observé/borne garantie.

## Sources et reproduction

`source/content.py` contient les scènes ; `story_art.py` et `diagrams.py`, les illustrations et schémas ; `course.js` et `course.css`, les interactions et la présentation. `assets/alice-scenes.png` est la planche originale d’illustrations, intégrée à l’HTML pendant la génération. Sa provenance et son prompt figurent dans [assets/ILLUSTRATIONS.md](assets/ILLUSTRATIONS.md).

```sh
python -m pip install -r source/requirements.txt
python -m playwright install chromium
python source/build_course.py
python source/audit_course.py
python source/build_lab.py
python source/audit_lab.py
```

Le générateur utilise Chrome local s’il existe, sinon Chromium de Playwright. L’audit vérifie cinq tailles d’écran, les six réponses, les calculs interactifs, les étapes de dévoilement, le chronométrage/CSV, les illustrations imprimées et la pagination. Les résultats sont dans `verification/checks.json`. L’exactitude pédagogique nécessite aussi la lecture critique et le retour des étudiants.

Préparé avec assistance IA ; illustrations générées avec l’outil intégré, textes et schémas retravaillés et vérifiés. Le PDF ADARE de l’auteur a servi de référence de narration, sans être redistribué.

## Introduction et plan détaillé

[Perceptron · énoncé PDF](https://rolln7drktayau.github.io/courses/embedded-ai/perceptron.pdf) · [Plan minuté et rééquilibrage](course-plan.pdf) · [Historique, sources et points à vérifier](HISTORY-AND-ROS.md).

Le pont vers la séance ROS se trouve avant la conclusion, à 175–177 minutes.
