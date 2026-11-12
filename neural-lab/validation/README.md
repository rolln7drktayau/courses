# Validation du laboratoire

Roland Cédric TAYO · INEM

Ce document résume des exécutions conservées, pas des performances promises sur une carte.

Moteur : 68 contrôles réussis. Atelier avancé : 43 contrôles réussis. Parcours guidé : 30 contrôles réussis. Ingestion animée : 24 contrôles réussis.

Exécution du moteur : 2026-11-12T00:54:49.438Z ; v24.14.0 ; AMD Ryzen 5 7535HS with Radeon Graphics         ; win32 x64.
Exécution du navigateur : 2026-11-12T08:48:57.296953+00:00 ; Chrome 157.0.8103.39. Rendu de test WebGL logiciel (SwiftShader). Charge système non maîtrisée.

## Calculs et contrôles

Dérivées par différences finies, probabilités normalisées, perte différée jusqu’au bouton 2, correction dans le bon ou le mauvais sens, masque causal, cache K/V égal au calcul complet, initialisation et apprentissage reproductibles, arrondi float32 et import/export intègre.

Le parcours navigateur vérifie aussi le chargement des trois modèles, la correction manuelle, les courbes, la génération avec cache, le zoom sur matrices et opérations, les survols 3D, les exports CSV, les réglages de campagne figés, la pause du mode lent, trois largeurs d’écran et le repli 2D sans WebGL. Aucune erreur JavaScript observée dans ce parcours. Ce n’est pas une étude auprès d’utilisateurs réels.

## Parcours guidé grand public

Tokenisation avec espace, identifiants issus du vocabulaire, sélection réelle de la ligne d’embedding, masquage du futur, probabilités avant sélection, argmax, poids fixes en inférence, gradient et mise à jour en apprentissage, absence de double correction lors d’une relecture, comparaison avant/après, repli 2D, caractères inconnus et entrée vide. Les captures guided-*.png et journey.json en donnent les traces. Les couleurs portent des rôles explicites ; le parcours ne fait pas circuler des nombres décoratifs.

## Ingestion animée et données fournies

Le test ingestion.py saisit une phrase entière, contrôle l’avancement et la pause, vérifie le déplacement géométrique de la phrase, parcourt les premiers et derniers tokens, contrôle les identifiants et l’exclusion des tokens hors contexte. Un fichier UTF-8 généré par le test initialise un nouveau modèle ; le texte du modèle est comparé exactement au fichier, le vocabulaire et l’exemple sont vérifiés, puis une vraie correction est exécutée. Les caractères UTF-8 invalides sont rejetés. Ces vérifications sont dans ingestion.json et les captures phrase-in-motion.png et dataset-to-example.png. Il s’agit d’une animation de traces réelles, pas d’une mesure du débit d’ingestion.

## Entraînement mesuré dans Node.js

Corpus répété d’Alice, η = 0,04, norme de gradient limitée à 1. Validation sur 48 fenêtres fixes, sans consultation du test réservé. Les durées ci-dessous couvrent les corrections ; les bilans avant/après sont mesurés séparément. Les courbes de la page portent sur 20 fenêtres ; les exemples livrés sur 48.

| Modèle | D / contexte | Graine | Corrections | Perte avant → après (nats) | Bonnes réponses avant → après | Durée (ms) |
|---|---|---|---|---|---|---|
| bigram | 4 / 3 | 42 | 600 | 2.6512 → 1.8338 | 10.42 % → 45.83 % | 34.20 |
| mlp | 4 / 3 | 42 | 600 | 2.7176 → 1.6761 | 12.50 % → 43.75 % | 54.08 |
| transformer | 4 / 3 | 42 | 600 | 3.0300 → 2.1331 | 4.17 % → 2.08 % | 114.51 |
| transformer-default | 8 / 6 | 42 | 300 | 2.7903 → 1.5280 | 22.92 % → 45.83 % | 238.43 |
| transformer-default | 8 / 6 | 43 | 300 | 3.2778 → 2.1038 | 4.17 % → 45.83 % | 218.39 |
| transformer-default | 8 / 6 | 44 | 300 | 3.0118 → 1.9159 | 25.00 % → 39.58 % | 214.92 |

La petite configuration Transformer D=4 améliore ici sa perte mais réduit son nombre de bonnes réponses. Ce résultat défavorable est conservé. Une perte et un taux de réussite n’évaluent pas la même chose.

## Exemples entraînés livrés

Ils sont réellement générés par `tests/build_examples.mjs` sur le corpus public, avec 2 000 corrections et la graine 42. Leur intégrité est vérifiée au chargement. Les chiffres sur ce corpus répétitif ne sont pas une évaluation de compréhension linguistique.

| Modèle | Paramètres | Perte validation | Bonnes réponses (48 fenêtres) |
|---|---|---|---|
| bigram | 240 | 1.3231 | 50.00 % |
| mlp | 1159 | 0.4254 | 85.42 % |
| transformer | 871 | 0.4454 | 83.33 % |

## Quantification et temps

Les fichiers `quantization.csv` et `results.json` conservent toutes les valeurs, dont les trois graines 42, 43 et 44 du Transformer par défaut. Les matrices sont arrondies puis réutilisées dans un calcul flottant. Les octets représentent un stockage idéal ; la RAM réelle du navigateur n’est pas mesurée.

Les observations de chronométrage du navigateur sont dans `browser.json`, champ `timing` : échauffement, calibration K, cinq paires alternées, temps individuels et checksum. Elles concernent le moteur scalaire avec construction de la trace. La présence du moteur 3D et d’autres tâches peut perturber les temps. Aucun gain de vitesse industrielle n’est revendiqué.

## Points restant à vérifier sur une cible réelle

- Portage vers un runtime adapté et, si nécessaire, des noyaux entiers réels.
- Stockage effectif, pic de RAM, latence et variabilité sur le Raspberry Pi concerné.
- Énergie avec un instrument approprié ; aucune valeur d’énergie n’est donnée ici.
- Qualité sur des données indépendantes représentatives du besoin, et non sur ces phrases répétées.
- Accessibilité avec des utilisateurs réels, autres navigateurs et appareils mobiles physiques.

## Traçabilité

Les CSV, JSON et captures viennent des scripts de `tests/`. `manifest.json` fixe les empreintes SHA-256 des fichiers du laboratoire. Le commit qui contient le manifeste identifie la livraison. Les versions de Three.js et sa licence sont dans `vendor/`. Les exemples sont des démonstrations du laboratoire ; aucun corrigé privé des TD n’est repris.
