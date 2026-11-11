# Corrections du texte de départ

Roland Cédric TAYO · INEM. Ce document explique les choix scientifiques du mini-cours. La conversation originale n’est pas publiée. Les sources sont détaillées dans [SOURCES.md](SOURCES.md) et dans la présentation.

| Formulation initiale | Correction retenue et source |
|---|---|
| Les systèmes experts stockent nécessairement leurs faits en tables relationnelles ou en arbres. | Il existe plusieurs architectures symboliques. Cette opposition générale est retirée ; le cours se concentre sur les modèles de langage neuronaux. |
| Rien n’est stocké en clair ; le modèle ne mémorise pas. | Des passages peuvent être mémorisés et restitués. La mémorisation n’est ni une consultation systématique du corpus ni une garantie de confidentialité. Carlini et al. (R4). |
| Chaque dimension d’embedding représente une caractéristique nommable. | Une dimension n’a pas nécessairement une interprétation isolée. Les représentations peuvent être distribuées et superposées, avec interférences. R1–R3. |
| Roi − homme + femme ≈ reine est une règle logique générale. | Certaines analogies vectorielles ont été observées ; ce n’est pas une garantie pour chaque modèle, espace ou relation. L’exemple est retiré pour ne pas confondre illustration et mécanisme universel. |
| Toute connaissance est introuvable dans les poids ou, inversement, rangée dans un neurone. | Certaines associations sont partiellement localisables par intervention. Ce résultat n’est pas une carte universelle de la connaissance. R2. |
| L’attention consulte une mémoire interne véridique. | L’attention pondère et combine des valeurs représentées ; les autres transformations et le contexte comptent. Elle ne vérifie pas automatiquement les faits. R1. |
| « Compression holographique du Web », « moindre résistance électrique ». | Métaphores supprimées : elles ne décrivent pas un mécanisme établi. Le contenu appris dépend des données, de l’entraînement et de l’architecture. |
| Toute inférence est limitée par la bande passante. | Distinguer prefill, decode, taille du lot, longueur du contexte, architecture et cible. Le decode dense à petit lot est souvent limité par les transferts ; pas tous les cas. R5. |
| Tous les poids sont obligatoirement transférés de la RAM à chaque token. | Le trafic dépend des caches, de la réutilisation, du lot, de la parcimonie et de l’architecture. Le calcul du mini-cours suppose explicitement des poids denses lus une fois par étape depuis le niveau mémoire considéré. |
| T = max(temps mémoire, temps calcul) est une mesure de latence. | C’est ici une borne optimiste ; le chevauchement, les débits effectifs et les surcoûts doivent être évalués. La formule par étape est utilisée pour une séquence. R5. |
| KV = 2 L d_model S p dans tous les Transformers. | Pour une séquence à têtes K/V usuelles : KV = 2 L S H_KV d p. Ajouter le lot, les surcoûts et les particularités de l’architecture si nécessaire. GQA change H_KV. R6. |
| La génération est impossible à paralléliser. | Les dépendances existent en decode ordinaire ; des calculs internes et la vérification spéculative peuvent être parallélisés. R13. |
| O(1) signifie zéro mémoire pour Mamba. | La taille de l’état est indépendante de la longueur du contexte, pour une architecture et un lot fixés. Poids et état restent nécessaires. R10. |
| Mamba ou BitNet ont échoué de façon générale. | Les performances dépendent des tâches et des conditions d’entraînement. Aucun jugement universel ni besoin inévitable d’augmenter massivement la taille n’est établi ici. Des résultats et implémentations existent. R10–R12, R15. |
| Ternaire implique uniquement XOR/POPCNT. | Avec des activations non binaires, des poids −1,0,+1 permettent notamment des additions/soustractions. Un noyau spécialisé, des échelles et d’autres opérations restent nécessaires. R11, R15. |
| 2 bits divisent le payload FP16 par 8 à 16. | Le ratio idéal FP16/2 bits est 16/2 = 8. À 1 bit, il serait 16. Le stockage réel a des surcoûts et des tenseurs mixtes. |
| GGUF et AWQ sont deux formats équivalents. | GGUF est un format de fichier ; AWQ est une méthode de quantification. Leur présence ne démontre pas un gain sur toute cible. R7, R14. |
| Une empreinte de 128 bits remplace exactement K et V. | Une empreinte peut sélectionner des candidats et subir des collisions ; elle ne contient pas automatiquement les valeurs V nécessaires au calcul. R9. |
| LSH assure une recherche exacte et conserve 99,2 % de fidélité. | Aucune expérience traçable n’accompagne ce chiffre dans le texte fourni. Retiré. Reformer propose une attention approximative. R9. |
| 32 000 × couches × 16 octets ≈ 260 Mo. | Avec l’hypothèse explicite de 32 couches : 32 000 × 32 × 16 = 16 384 000 octets, soit 16,384 Mo. Ce compte de signatures ne constitue toujours pas un cache K/V complet. |
| INT4, SIMD et alignement suppriment tout dépaquetage. | Une disposition et des noyaux compatibles restent nécessaires. Des instructions de produits scalaires sur octets ne consomment pas arbitrairement des codes INT4 ou des codebooks sans traitement. Le cours ne promet pas cette propriété. |
| Alignement parfait = un XOR/POPCNT par cycle et aucun coût. | Aucun code ni matériel précis ne justifie ces affirmations. Elles sont retirées. |
| 120–150 tokens/s, 5 ms CPU et une RAM totale de 3,8 Go sont démontrés. | Chiffres non mesurés et hypothèses insuffisantes. Le cours affiche uniquement des comptes analytiques ou des bornes explicitement étiquetées. Aucun LLM n’est exécuté sur carte dans ce mini-cours. |
| Une optimisation est sans compromis, ou toute l’industrie refuse les alternatives. | Position non étayée et démentie par la disponibilité de plusieurs pistes. Le cours présente les gains et les risques, sans attribuer d’intentions aux acteurs. |

## Ce qui a réellement été exécuté pour ce support

Les calculs JavaScript de taille de poids, de cache K/V, de borne Roofline et de quantification d’un produit scalaire jouet sont vérifiés par le script d’audit. La navigation, les questions, les transitions, les liens et la mise en page sont contrôlés dans un navigateur. Ce sont des vérifications du support pédagogique, **pas des expériences validant un nouveau modèle ou une architecture de LLM**.

## Inspiration visuelle

Vidéo indiquée par l’enseignant : [Nerdy Kings — La fin des tokens ? Une nouvelle architecture pourrait changer l’IA](https://www.youtube.com/watch?v=gYG4J6Do0UU). Des planches d’images publiques de cette vidéo ont été examinées pour le rythme visuel : fond clair, schémas qui se construisent, peu de texte par scène. La présentation utilise ses propres textes, schémas SVG et code de transition. Aucun extrait, logo, personnage ou dessin de la chaîne n’est distribué.
