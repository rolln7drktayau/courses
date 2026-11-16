# L’IA dans les objets

Roland Cédric TAYO · INEM

[Cours animé](https://rolln7drktayau.github.io/courses/embedded-ai-public/) · [PDF complet](cours-ia-embarquee.pdf) · [Lire](reading.html) · [Comparaison des cursus](curriculum-comparison.html)

Huit chapitres nommés, 63 notions et quatre scènes pratiques : 67 diapositives, sans défilement en présentation. Les explications et les schémas avancent ensemble. Le fil conducteur est une lampe qui reconnaît une commande vocale sans Internet.

1. Le besoin avant le modèle.
2. Des données pour apprendre.
3. Le neurone pas à pas.
4. Les réseaux d’aujourd’hui.
5. La machine et ses limites.
6. L’art du compromis.
7. Du PC à l’objet fiable.
8. Apprendre à chercher.

## Présenter et manipuler

Les flèches avancent d’abord dans l’explication, puis vers la diapositive suivante. Les boutons numérotés et le curseur permettent de revenir à une phase. « Construire le schéma » compose les éléments et trace les connexions. Le rythme est réglable ; la durée de lecture dépend du texte. Pause, reprise et reconstruction restent sous contrôle de l’utilisateur. Le mode de réduction des animations est respecté.

Sept calculateurs permettent de manipuler neurone, gradient, filtre, caractères, mémoire des paramètres, quantification et compromis. Quatre scènes pratiques ajoutent assemblage par glisser-déposer ou clic, rotation et isolation d’une maquette 3D, budget RAM et trajet PC–carte–PC.

Les petits calculs sont réellement exécutés dans le navigateur. Les budgets fictifs, quantifications simulées et transferts virtuels sont étiquetés. Aucun Raspberry Pi n’est connecté à ce support et aucune performance originale sur matériel n’est annoncée.

Le format de présentation utilise HTML, SVG, JavaScript et une maquette CSS 3D. Garder index.html avec assets/ pour un usage hors ligne. reading.html reste autonome ; le PDF restitue la théorie et les approfondissements, sans les manipulations exécutables. Plan, lexique et sources sont paginés ; la version « Lire » est le document continu pour réviser.

## Origine du contenu et vérification

[CURRICULUM-COMPARISON.md](CURRICULUM-COMPARISON.md) documente les sources officielles MIT, Harvard, ETH Zurich et Heidelberg, les lacunes relevées et les huit ajouts retenus. Il distingue programmes publics, exercices consultables et ressources fermées. Ce cours grand public ne prétend pas équivaloir à un cursus universitaire ni produire une expertise par simple lecture.

Le [persona Sam](persona-verification.pdf) et [l’audit initial](verification/persona-audit.md) concernent les fondations éditoriales. La relecture de la nouvelle présentation et des ajouts est résumée dans [SLIDES-REVIEW.md](verification/SLIDES-REVIEW.md). Ces relectures sont simulées ; aucun enfant réel n’a testé le support.

Les contrôles réellement exécutés sont dans verification/slides-validation.json et verification/validation.json. Ils vérifient calculs, interactions, présentation sur plusieurs écrans et PDF. Ils ne sont ni une étude d’utilisateurs ni des mesures embarquées.

## Régénérer et tester

Installer Python et les dépendances de requirements-course.txt. Les scripts de validation utilisent Chrome ; adapter son chemin selon le poste.

```sh
python build_course.py
python validate_reader.py
python validate_slides.py
```

build_reader.py conserve les fondations du cours. curriculum.py contient les ajouts retenus après comparaison. build_course.py rassemble le document de lecture, le texte structuré, les références et les scènes. index.html et assets/slides.* définissent la présentation ; assets/composition.js gère la construction contrôlable des schémas.

Les textes et schémas sont originaux. Les publications sont citées pour vérifier et prolonger les notions. Aucun corrigé privé de TD ni donnée d’étudiant n’est inclus. manifest-sha256.json identifie les fichiers livrés.
