# Audit pédagogique et technique — persona Sam

Date : 16 novembre 2026.

## Périmètre et profil

Relecture du cours-source.json (55 étapes, glossaire et références), du HTML généré et du code de ses calculateurs. Contrôle des corrections dans les schémas HTML des étapes 15, 16, 25, 32 et 42. Inspection des captures 02-correction-poids.png et pdf-page-1.png.

Sam est un persona fictif : 10 ans, curieux, capable de lire, additionner et multiplier, sans vocabulaire préalable en informatique. Il demande le sens des mots, la cause des résultats et un exemple concret avant une formule générale. Ce contrôle éditorial ne rapporte aucun témoignage et aucun essai auprès d'un enfant réel.

Une seconde grille, technique, vérifie les distinctions conceptuelles, les calculs, les unités, les conditions de mesure et les limites des affirmations. Le support est évalué comme un cours grand public progressif, pas comme une certification ou une formation pratique complète d'ingénieur.

## Grille de vérification

| Critère | Question de contrôle | Avis final |
|---|---|---|
| Vocabulaire | Les notions essentielles sont-elles définies au moment utile ? | Acceptable ; rappels mathématiques renforcés. |
| Causalité | Le lecteur peut-il suivre pourquoi une modification produit un résultat ? | Renforcée par l'exemple du poids 0,20 puis 0,21. |
| Analogies | Éclairent-elles le mécanisme sans lui attribuer des propriétés humaines ? | Acceptable ; limites explicites. |
| Schémas | Montrent-ils les bonnes dépendances et la simultanéité lorsque nécessaire ? | Corrections importantes vérifiées. |
| Apprentissage / inférence | Ajustement des paramètres et utilisation sont-ils distingués ? | Oui. |
| Contraintes embarquées | Mémoire, calcul, énergie et délai sont-ils distingués ? | Oui, avec unités et réserves adaptées. |
| Recherche | Hypothèse, protocole, comparaison et limites sont-ils explicités ? | Oui ; démarche progressive et prudente. |
| Mesures et promesses | Les simulations sont-elles distinguées des résultats matériels ? | Oui ; aucune performance originale annoncée. |
| Progression | La lecture est-elle présentée comme une base pour pratiquer ensuite ? | Oui ; aucune expertise délivrée par simple lecture. |

## Défauts initiaux et corrections vérifiées

| Étapes | Défaut initial | Correction constatée | Statut |
|---|---|---|---|
| 7 | Jargon technique avant introduction : réseaux, convolutions, moteur. | Réseaux de neurones brièvement définis ; MobileNets et MCUNet décrits par leur but. | Résolu. |
| 11 | « Partitions » prématuré et risque de confusion entre fréquences du son et fréquence d'échantillonnage. | Groupes d'exemples annoncés ; distinction grave/aigu et nombre de mesures visible. | Résolu. |
| 13, 14, 17, 18, 38 | Signes et notations utilisés trop vite. | Indices, négatifs, max, carré, demi, affectation et puissance accompagnés d'explications ou d'exemples. | Amélioré suffisamment pour le parcours. |
| 18 | Gradient donné sans lien causal accessible. | Variation 0,20 → 0,21, baisse de perte 0,32 → 0,31205 et explication détaillée des gradients. La mise à jour vers w=0,28 et b=0,08 donne bien une perte de 0,2048. | Résolu pour une introduction ; approfondissement toujours optionnel. |
| 15, 16 | Réseau et matrice représentés uniquement par des boîtes abstraites. | Liaisons complètes entre couches ; vrai tableau matriciel 2×2 à deux lignes colorées, exemple numérique et calcul de chaque sortie en légende. | Résolu. |
| 24 | Identifiants de tokens recalculés selon l'ordre des caractères de chaque texte. | Table fixe dans le JavaScript, identifiant inconnu explicite, portée pédagogique annoncée. | Résolu par inspection du code ; le test navigateur complémentaire relève de la validation principale. |
| 25 | Attention introduite sans somme pondérée concrète ; dépendances peu visibles. | Exemple 0,6×2 + 0,3×10 + 0,1×0 = 4,2 ; Q et K produisent les coefficients, V fournit les valeurs. | Résolu. |
| 32 | Schéma séquentiel alors que le sujet est la coexistence des zones RAM. | Entrée, travail temporaire et sortie dans une boîte « Même instant ». Tailles symboliques signalées. | Résolu. |
| 36 | Chiffrement utilisé dans le quiz avant sa définition. | Courte définition ajoutée à la question. | Résolu. |
| 42 | Graphique annoncé mais absent ; admissibilité sans illustration de la domination. | Nuage de points, seuils et cartes ; B domine C, A et B ne se dominent pas. Couleur verte explicitement limitée à l'admissibilité. | Résolu. |
| 45 | Chronométrage par groupes risquant d'être interprété comme une distribution des latences individuelles. | Moyenne durée/K et dispersion entre groupes distinguées des mesures par appel et percentiles. Coût de chronométrage mentionné. | Résolu. |
| 46 | Titre sur la mauvaise action malgré une prédiction correcte sans exemple précis. | Télévision prononçant « lumière », mot reconnu mais commande non souhaitée. | Résolu. |
| 49 | Trop de notions de traçabilité et livraison concentrées dans le parcours principal. | But pratique recentré sur fiche d'expérience, versions et tests ; CI, SHA-256 et DevOps déplacés en approfondissement. | Amélioré. |
| Glossaire | « Volatile » et « flottant » sans définition directement disponible. | Deux entrées expliquent la perte du contenu sans alimentation et la représentation numérique à précision limitée avec arrondis. Présence vérifiée dans le HTML final. | Résolu. |

## Réserves non bloquantes

- La densité reste élevée pour une lecture autonome à 10 ans, surtout aux étapes 18, 22, 25–26 et 38–39. Des pauses, manipulations et reformulations sont souhaitables. La compréhension dès cet âge reste une intention pédagogique, pas un résultat observé.
- Certains détails avancés demeurent brefs, ce qui est acceptable ici. Par exemple, le cours expose le rôle du gradient sans démonstration complète du calcul différentiel et décrit le Transformer sans en donner une implémentation exhaustive.
- L'encadré de l'étape 49 mentionne une empreinte avant son explication en approfondissement. C'est une petite imperfection d'ordre de présentation, sans conséquence sur le mécanisme enseigné.

## Limites de cet audit

Cet audit ne certifie ni accessibilité universelle, ni apprentissage effectif, ni exactitude exhaustive des publications citées. Les références sont lues comme éléments du support ; elles n'ont pas toutes été revérifiées en ligne dans cette passe. L'inspection de deux captures ne constitue pas un contrôle visuel de toutes les pages PDF. Les 45 contrôles de validation et la vérification des 59 pages PDF sont rapportés par l'agent principal ; ce rapport ne prétend pas les avoir réexécutés indépendamment. Aucune performance sur Raspberry Pi n'a été mesurée par ce relecteur.

## Verdict final

Aucun défaut pédagogique ou technique bloquant identifié dans la version relue. Les principales erreurs susceptibles d'installer une représentation fausse ont été corrigées. Avis favorable à la livraison comme cours grand public progressif, avec accompagnement et pratique pour les notions avancées. Une validation avec de vrais lecteurs novices serait nécessaire pour établir le niveau d'autonomie effectif à 10 ans.
