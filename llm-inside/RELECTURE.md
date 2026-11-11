# Relecture pédagogique du mini-cours

Roland Cédric TAYO · INEM. Relecture du 11 novembre 2026.

## Place et acquis visés

Ce support est un panorama complémentaire au cours d’IA embarquée. En environ vingt minutes de présentation, on vise trois acquis : distinguer les sources d’information d’un modèle, expliquer ses principaux coûts d’inférence et reconnaître ce qui demande une vérification expérimentale. Les manipulations et échanges peuvent prolonger cette durée ; celle-ci n’a pas été mesurée devant une classe.

Il ne remplace ni un apprentissage complet des Transformers ni un TP de déploiement de LLM. Pour Reformer, Mamba, BitNet et le décodage spéculatif, l’objectif est de comparer des principes et des compromis, pas de savoir les implémenter après cette seule lecture.

## Progression retenue

1. Poids, contexte et documents : distinguer avant de parler de mémoire.
2. Apprentissage et inférence : séparer les deux moments.
3. Texte, tokens, vecteurs : introduire les nombres avant les opérations.
4. Attention, puis représentations partagées : montrer l’utilisation du contexte avant l’interprétabilité.
5. Prefill, decode, poids et cache : identifier les deux phases et les budgets.
6. Temps de transfert et temps de calcul : diagnostiquer avant d’optimiser.
7. Pistes d’optimisation : quantifier, réorganiser les transferts, changer la mémoire ou l’arithmétique, proposer puis vérifier.
8. Hypothèse, mesure et comparaison sur Pi : terminer par les preuves, puis les sources.

Les trois pauses questions suivent les notions concernées. La question sur les collisions a été rapprochée du hachage. Les positions des réponses correctes sont réparties entre A, B et C ; les explications comptent davantage que la lettre choisie.

## Points corrigés

| Point relevé | Modification |
|---|---|
| Vocabulaire parfois utilisé avant sa définition. | Définitions dans les scènes et lexique accessible au premier emploi des mots soulignés. Les notions essentielles sont également expliquées dans le PDF. |
| Attention présentée après la superposition. | L’attention passe avant les représentations partagées ; le lecteur a déjà vu l’usage des vecteurs. |
| « Avril chante » pouvait suggérer une lecture du futur au token Avril. | La requête est située explicitement au dernier token. L’interprétation illustrée porte sur la phrase déjà reçue. |
| Schéma abstrait de directions peu relié aux neurones. | Deux unités sont partagées entre trois propriétés illustrées ; les interférences et la nature schématique sont signalées. |
| Le cache changeait surtout de couleur quand on modifiait les têtes. | Le nombre de lignes change avec les têtes K/V ; le nombre de colonnes change avec le contexte. La valeur en octets est calculée séparément. |
| Comparaison Reformer/Mamba trop proche de deux boîtes sans opérations. | Candidats retenus d’un côté ; ancien état + entrée → nouvel état de l’autre. |
| Le modèle spéculatif pouvait sembler corriger un fait faux. | Deux suites plausibles sont utilisées. Le texte précise qu’on vérifie des probabilités, pas une vérité. |
| Q avait deux sens rapprochés. | La limite des codes quantifiés s’appelle désormais q_max, pour la distinguer des requêtes Q. |
| Référence à une pièce jointe que les étudiants ne possèdent pas. | Suppression ; la distinction calcul/hypothèse/mesure est autonome. |
| Les documents semblaient alimenter le modèle sans passer par le contexte. | Les extraits documentaires rejoignent le contexte dans le schéma. Référence RAG ajoutée. |

## Contrôles et limites

Les scripts contrôlent les calculs jouets, la navigation, les questions, l’accès aux définitions, l’emplacement des pauses, les changements de schéma et les débordements sur cinq tailles d’écran. Le PDF reprend les 23 scènes. Les résultats des contrôles sont conservés dans `verification/`.

La cohérence scientifique et pédagogique fait aussi l’objet d’une relecture des formulations et des schémas ; elle ne se déduit pas d’un simple test automatique. Aucune évaluation de compréhension par des étudiants n’a encore été réalisée pour ce mini-cours. Aucun LLM ni Raspberry Pi n’est benchmarké par ces illustrations.
