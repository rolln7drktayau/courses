# L’IA dans les objets

Roland Cédric TAYO · INEM

[Cours interactif](https://rolln7drktayau.github.io/courses/embedded-ai-public/) · [PDF](cours-ia-embarquee.pdf) · [Persona de vérification](persona-verification.pdf) · [Audit](verification/persona-audit.md)

Cours grand public progressif : 55 étapes, six chapitres, sept manipulations interactives, questions corrigées, glossaire et références primaires. Le fil conducteur est une lampe qui reconnaît une commande vocale sans réseau.

1. Partir du besoin : IA, système embarqué, apprentissage et inférence.
2. Apprendre avec des nombres : données, neurone, perte et correction.
3. Lire les réseaux actuels : convolution, séries, tokens et attention.
4. Comprendre la petite machine : stockage, RAM, calcul, délai et énergie.
5. Optimiser : quantification et compromis mesurables.
6. Déployer, vérifier et chercher : cible, protocole et démarche scientifique.

Le fichier index.html est autonome, sans dépendance réseau pour les exercices. Le PDF de 59 pages contient les approfondissements et les réponses expliquées. « Tout lire » affiche toutes les étapes ; les flèches permettent de les parcourir une par une. Le mode plein écran dépend des possibilités du navigateur.

Les calculateurs effectuent les petits calculs pédagogiques dans le navigateur. La quantification est simulée, et les points A/B/C sont fictifs. Aucune performance originale sur carte n’est annoncée. L’expertise demande ensuite de la pratique sur des données et un matériel réels.

Sam, 10 ans, est un persona fictif de vérification accompagné d’une lecture technique indépendante. Aucun test auprès d’un enfant réel n’est revendiqué. Les notions avancées peuvent demander un accompagnement.

## Sources et reproduction

cours-source.json contient texte structuré, glossaire et références. build_course.py produit index.html et le JSON. validate_course.py exécute les contrôles navigateur et exporte le PDF (Python, Playwright, PyMuPDF et Chrome ; adapter le chemin de Chrome selon le poste).

```sh
python build_course.py
python validate_course.py
```

verification/validation.json conserve les contrôles exécutés. verification/persona-audit.md décrit les défauts relevés et les corrections. Les captures sont des preuves de contrôle, pas une étude utilisateurs. manifest-sha256.json identifie les fichiers livrés.

Textes et schémas originaux pour ce cours. Publications citées pour vérifier et prolonger les notions. Aucun corrigé privé des TD ni donnée d’étudiant n’est inclus.
