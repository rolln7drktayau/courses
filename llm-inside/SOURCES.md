# Sources du mini-cours

Roland Cédric TAYO · INEM. Sources originales. Comptes analytiques ; tableau de comparaison fictif. Aucun débit de LLM sur carte revendiqué.

## R1 — Attention Is All You Need

Ashish Vaswani et al.. 2017. **NeurIPS 2017.**

[Source originale](https://arxiv.org/abs/1706.03762)

Transformer, attention, représentations et calculs matriciels. Le cours utilise un décodeur causal comme exemple ; le papier présente une architecture encodeur-décodeur.

## R2 — Locating and Editing Factual Associations in GPT

Kevin Meng, David Bau, Alex Andonian, Yonatan Belinkov. 2022. **NeurIPS 2022.**

[Source originale](https://arxiv.org/abs/2202.05262)

Des interventions causales localisent certains calculs liés à des associations factuelles. Cela ne fournit pas une adresse universelle de chaque connaissance.

## R3 — Toy Models of Superposition

Nelson Elhage et al.. 2022. **Article de recherche · modèles jouets.**

[Source originale](https://transformer-circuits.pub/2022/toy_model/index.html)

Des caractéristiques peuvent partager des dimensions, avec des interférences. Un axe n’est donc pas nécessairement un concept isolé.

## R4 — Extracting Training Data from Large Language Models

Nicholas Carlini et al.. 2021. **USENIX Security 2021 · prépublication initiale 2020.**

[Source originale](https://arxiv.org/abs/2012.07805)

Des passages d’entraînement ont été extraits de GPT-2. Une représentation distribuée n’interdit ni la mémorisation ni la restitution de texte.

## R5 — Roofline: An Insightful Visual Performance Model…

Samuel Williams, Andrew Waterman, David Patterson. 2008 / 2009. **Rapport Berkeley 2008 · article CACM 2009.**

[Source originale](https://www2.eecs.berkeley.edu/Pubs/TechRpts/2008/EECS-2008-134.html)

Relier le calcul et le trafic mémoire. Le maximum des deux temps est une borne optimiste, pas une prédiction exacte de latence.

## R6 — GQA: Training Generalized Multi-Query Transformer Models…

Joshua Ainslie et al.. 2023. **EMNLP 2023.**

[Source originale](https://arxiv.org/abs/2305.13245)

Plusieurs têtes de requêtes partagent des têtes K/V ; cela réduit notamment le cache. Une conversion peut demander un réentraînement complémentaire.

## R7 — AWQ: Activation-aware Weight Quantization…

Ji Lin et al.. 2023 / 2024. **Prépublication 2023 · MLSys 2024.**

[Source originale](https://arxiv.org/abs/2306.00978)

Quantification des poids guidée par les activations et implémentation adaptée au matériel. Ses résultats ne sont pas ceux de notre petit exemple d’arrondi.

## R8 — FlashAttention: Fast and Memory-Efficient Exact Attention…

Tri Dao, Daniel Y. Fu, Stefano Ermon, Atri Rudra, Christopher Ré. 2022. **NeurIPS 2022.**

[Source originale](https://arxiv.org/abs/2205.14135)

Réorganiser le calcul par blocs pour réduire les transferts HBM/SRAM sur GPU, sans approximation de parcimonie de l’attention. Des écarts d’arrondi restent possibles.

## R9 — Reformer: The Efficient Transformer

Nikita Kitaev, Łukasz Kaiser, Anselm Levskaya. 2020. **ICLR 2020.**

[Source originale](https://arxiv.org/abs/2001.04451)

LSH pour sélectionner des groupes de candidats ; c’est une attention approximative. Une signature binaire ne remplace pas à elle seule les valeurs V.

## R10 — Mamba: Linear-Time Sequence Modeling with Selective State Spaces

Albert Gu, Tri Dao. 2023 / 2024. **Prépublication 2023 · COLM 2024.**

[Source originale](https://arxiv.org/abs/2312.00752)

État récurrent de taille indépendante de la longueur de séquence pour un modèle fixé. Cela n’assure pas la conservation exacte de tout le passé.

## R11 — The Era of 1-bit LLMs: All Large Language Models are in 1.58 Bits

Shuming Ma et al.. 2024. **Prépublication · résultats dans les configurations étudiées.**

[Source originale](https://arxiv.org/abs/2402.17764)

BitNet b1.58, poids ternaires et entraînement adapté. Le titre n’implique pas que tous les paramètres d’un fichier réel occupent exactement 1,58 bit.

## R12 — BitNet b1.58 2B4T Technical Report

Shuming Ma et al.. 2025. **Rapport technique · prépublication.**

[Source originale](https://arxiv.org/abs/2504.12285)

Un modèle natif basse précision et des implémentations ouvertes existent ; on ne peut pas présenter cette piste comme absente du monde réel.

## R13 — Fast Inference from Transformers via Speculative Decoding

Yaniv Leviathan, Matan Kalman, Yossi Matias. 2023. **ICML 2023 · prépublication initiale 2022.**

[Source originale](https://arxiv.org/abs/2211.17192)

Propositions d’un petit modèle, vérification et correction d’échantillonnage par le modèle cible. La distribution est préservée sous les hypothèses de l’algorithme exact ; le gain dépend du cas.

## R14 — GGUF — spécification du format

Projet ggml. Documentation évolutive. **Documentation officielle.**

[Source originale](https://github.com/ggml-org/ggml/blob/master/docs/gguf.md)

Conteneur de tenseurs et de métadonnées. GGUF est un format ; AWQ est une méthode. Ni l’un ni l’autre n’est une promesse de vitesse universelle.

## R15 — BitNet — implémentation officielle

Microsoft Research. Code évolutif. **Dépôt officiel.**

[Source originale](https://github.com/microsoft/BitNet)

Implémentations et modèles compatibles. La disponibilité du code ne garantit ni la prise en charge de toute machine ni la qualité sur toute tâche.

## R16 — Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks

Patrick Lewis et al.. 2020. **NeurIPS 2020.**

[Source originale](https://arxiv.org/abs/2005.11401)

Combiner les paramètres d’un modèle et une source documentaire récupérée. Les documents sélectionnés fournissent un contexte supplémentaire ; ils ne garantissent pas une réponse vraie.

## R17 — llama.cpp et llama-bench

Projet ggml. Documentation évolutive. **Documentation et implémentation officielles.**

[Source originale](https://github.com/ggml-org/llama.cpp/tree/master/tools/llama-bench)

Mesurer séparément le traitement d’entrée et la génération. Le benchmark rapporte des temps ou débits ; il n’évalue pas la qualité et ne remplace pas la mesure du système intégré.

## R18 — Raspberry Pi — matériel et fonctionnement

Raspberry Pi. Documentation évolutive. **Documentation officielle.**

[Source originale](https://www.raspberrypi.com/documentation/computers/raspberry-pi.html)

Capacités, alimentation et fonctionnement thermique. Les valeurs théoriques du mini-cours ne sont pas des débits mesurés d’un Raspberry Pi.

## Inspiration visuelle

Nerdy Kings, [vidéo indiquée par l’enseignant](https://www.youtube.com/watch?v=gYG4J6Do0UU). Référence de rythme ; schémas et code originaux.
