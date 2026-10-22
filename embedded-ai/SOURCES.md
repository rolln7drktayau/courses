# Sources du cours



Roland Cédric TAYO — références scientifiques et documentation. Sources pédagogiques : TEACHING-DESIGN.md.



Les prépublications ne sont pas présentées comme un consensus ou un classement de l’état de l’art. Les schémas du cours sont originaux et les données des démonstrations sont analytiques ou illustratives.



## R01 — ALVINN: An Autonomous Land Vehicle In a Neural Network

Dean Pomerleau. 1989. Repère historique · publication CMU / actes NeurIPS.

[Source originale](https://publications.ri.cmu.edu/alvinn-an-autonomous-land-vehicle-in-a-neural-network)

Apport : Relier perception apprise et action à bord d’un véhicule.

Limite : Démonstrateur historique ; ni autonomie générale ni exécution sur microcontrôleur.



## R02 — MobileNets: Efficient Convolutional Neural Networks for Mobile Vision Applications

Andrew G. Howard et al.. 2017. Article fondateur · arXiv 1704.04861.

[Source originale](https://arxiv.org/abs/1704.04861)

Apport : Séparer convolution spatiale et mélange des canaux pour réduire le calcul.

Limite : Moins de MAC ne garantit pas la même réduction de latence sur chaque cible.



## R03 — Quantization and Training of Neural Networks for Efficient Integer-Arithmetic-Only Inference

Benoit Jacob et al.. 2018. CVPR 2018 · prépublication 2017.

[Source originale](https://arxiv.org/abs/1712.05877)

Apport : Co-concevoir quantification, apprentissage et noyaux entiers.

Limite : Le format des poids, des activations et des accumulateurs doit être distingué.



## R04 — MCUNet: Tiny Deep Learning on IoT Devices

Ji Lin, Wei-Ming Chen et al.. 2020. NeurIPS 2020.

[Source originale](https://arxiv.org/abs/2007.10319)

Apport : Chercher ensemble l’architecture du réseau et son moteur d’exécution.

Limite : Résultats sur des cibles et tâches précises, pas une capacité universelle des MCU.



## R05 — MCUNetV2: Memory-Efficient Patch-based Inference for Tiny Deep Learning

Ji Lin, Wei-Ming Chen, Han Cai et al.. 2021. NeurIPS 2021.

[Source originale](https://arxiv.org/abs/2110.15352)

Apport : Traiter des morceaux de carte de caractéristiques pour réduire le pic mémoire.

Limite : Les recouvrements peuvent ajouter du calcul ; l’ordonnancement compte.



## R06 — On-Device Training Under 256KB Memory

Ji Lin, Ligeng Zhu et al.. 2022. NeurIPS 2022.

[Source originale](https://arxiv.org/abs/2206.15472)

Apport : Rendre possible une adaptation locale par mises à jour sélectives et co-conception.

Limite : Il ne s’agit pas d’entraîner librement n’importe quel réseau dans 256 Ko.



## R07 — FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness

Tri Dao, Daniel Y. Fu et al.. 2022. NeurIPS 2022.

[Source originale](https://arxiv.org/abs/2205.14135)

Apport : Réorganiser le calcul d’attention pour réduire les échanges mémoire sur GPU.

Limite : Attention exacte à l’arrondi près ; les résultats GPU ne décrivent pas un MCU.



## R08 — TSMixer: An All-MLP Architecture for Time Series Forecasting

Si-An Chen et al.. 2023. Transactions on Machine Learning Research, 2023.

[Source originale](https://arxiv.org/abs/2303.06053)

Apport : Mélanger les instants puis les variables avec des perceptrons multicouches.

Limite : Le réseau du TD est une réduction pédagogique, pas une reproduction de l’article.



## R09 — AWQ: Activation-aware Weight Quantization for LLM Compression and Acceleration

Ji Lin, Jiaming Tang et al.. 2024. MLSys 2024 · prépublication 2023.

[Source originale](https://arxiv.org/abs/2306.00978)

Apport : Utiliser des statistiques d’activation pour mieux préserver les canaux sensibles.

Limite : Quantifier les poids ne signifie pas quantifier toute la mémoire ni tous les calculs.



## R10 — MobileNetV4 — Universal Models for the Mobile Ecosystem

Danfeng Qin et al.. 2024. ECCV 2024.

[Source originale](https://arxiv.org/abs/2404.10518)

Apport : Concevoir des blocs et une recherche d’architecture adaptés à plusieurs matériels mobiles.

Limite : L’écosystème mobile évalué ne couvre pas tous les microcontrôleurs.



## R11 — T-MAC: CPU Renaissance via Table Lookup for Low-Bit LLM Deployment on Edge

Jianyu Wei, Shijie Cao et al.. 2025. EuroSys 2025 · prépublication 2024.

[Source originale](https://arxiv.org/abs/2407.00088)

Apport : Remplacer certaines opérations de produits mixtes par des tables de recherche adaptées.

Limite : Bénéfices dépendants du bit-width, des noyaux, des formes et des matériels comparés.



## R12 — SmolLM2: When Smol Goes Big — Data-Centric Training of a Small Language Model

Loubna Ben Allal et al.. 2025. Prépublication arXiv 2502.02737.

[Source originale](https://arxiv.org/abs/2502.02737)

Apport : La qualité et le mélange des données comptent aussi pour les petits modèles de langage.

Limite : « Petit » à 1,7 milliard de paramètres reste immense pour un MCU.



## R13 — T-MAN: Enabling End-to-End Low-Bit LLM Inference on NPUs via Unified Table Lookup

Jianyu Wei, Qingtao Li et al.. 2025. Prépublication arXiv · 14 novembre 2025.

[Source originale](https://arxiv.org/abs/2511.11248)

Apport : Adapter tables, tuilage et pipeline aux opérations réellement prises en charge par un NPU.

Limite : Résultats propres aux systèmes étudiés ; le statut de publication évaluée n’est pas établi ici.



## R14 — From Compression to Deployment: Real-Time and Energy-Efficient FastGRNN on Ultra-Constrained Microcontrollers

Emre Can Kizilates. 2026. Prépublication arXiv · 15 juin 2026.

[Source originale](https://arxiv.org/abs/2606.17249)

Apport : Étudier ensemble compression, activation par table, état récurrent et déploiement physique.

Limite : Étude particulière ; variabilité entre graines et temps de mise en régime à examiner.



## R15 — A Framework for Accelerating Transformer Inference on RISC-V for Edge AI

Ajay Kumar M et al.. 2026. Prépublication arXiv · accepté à ICECS 2026 selon la notice des auteurs.

[Source originale](https://arxiv.org/abs/2610.08688)

Apport : Adapter instructions et compilation à des Transformers compacts, principalement encodeurs.

Limite : Modifier un cœur RISC-V est un travail matériel ; ce gain n’est pas un simple correctif logiciel.



## R16 — Adversarial Machine Learning: A Taxonomy and Terminology of Attacks and Mitigations

Apostol Vassilev, Alina Oprea et al.. 2025. Rapport technique NIST AI 100-2e2025.

[Source originale](https://doi.org/10.6028/NIST.AI.100-2e2025)

Apport : Distinguer attaques sur données, entrées, modèles et vie privée.

Limite : Une taxonomie et des contre-mesures ne garantissent pas la sécurité d’un produit.



## R17 — Tiny Machine Learning: Progress and Futures

Ji Lin, Ligeng Zhu, Wei-Ming Chen, Wei-Chen Wang, Song Han. 2023 / 2024. IEEE Circuits and Systems Magazine 2023 · dépôt arXiv 2024.

[Source originale](https://arxiv.org/abs/2403.19076)

Apport : Vue d’ensemble de la co-conception et du passage de l’inférence à l’adaptation locale.

Limite : Date de dépôt arXiv et date de publication diffèrent ; ce panorama n’est pas un état exhaustif 2026.



## R18 — MLPerf Tiny Benchmark

Colby Banbury, Vijay Janapa Reddi et al.. 2021. NeurIPS 2021 · Datasets and Benchmarks.

[Source originale](https://arxiv.org/abs/2106.07597)

Apport : Comparer qualité, latence et énergie avec un protocole reproductible.

Limite : Respecter la tâche, le périmètre et les règles ; ne pas comparer seulement des scores isolés.



## R19 — CMSIS-NN — Efficient neural network kernels for Arm Cortex-M

Arm. Documentation consultée en 2026. Dépôt officiel de noyaux optimisés.

[Source originale](https://github.com/ARM-software/CMSIS-NN)

Apport : Les performances dépendent de noyaux adaptés à l’ISA et aux formats quantifiés.

Limite : Une bibliothèque ne supprime pas les limites mémoire ou les vérifications de l’application.



## R20 — LiteRT for Microcontrollers

Google AI Edge. Documentation consultée en 2026. Documentation officielle du moteur MCU.

[Source originale](https://developers.google.com/edge/litert/microcontrollers/overview)

Apport : Déployer un sous-ensemble d’opérateurs avec une allocation adaptée au microcontrôleur.

Limite : Vérifier les opérations, types et cibles pris en charge ; conversion n’est pas validation.



## R21 — MLPerf Inference: Tiny

MLCommons. Documentation consultée en 2026. Méthodologie et résultats officiels.

[Source originale](https://mlcommons.org/benchmarks/inference-tiny/)

Apport : Lire conjointement qualité, scénario de mesure et configuration matérielle.

Limite : Aucun chiffre de classement en temps réel n’est repris dans ce support.



## R22 — Shakey the Robot

SRI International. 1966–1972. Histoire du projet · organisme concepteur.

[Source originale](https://www.sri.com/press/story/75-years-of-innovation-shakey-the-robot/)

Apport : Faire percevoir un environnement et planifier des actions à un robot mobile.

Limite : Repère d’IA en interaction avec le monde physique, pas un exemple de calcul entièrement à bord.



## R23 — Edge AI

NIST. Documentation consultée en 2026. Programme de recherche officiel.

[Source originale](https://www.nist.gov/programs-projects/edge-ai)

Apport : Rapprocher l’inférence ou l’apprentissage des données et des usages.

Limite : Ressources, communications, données, confidentialité et sécurité restent des difficultés ; local ne signifie pas automatiquement sûr.



## R24 — Glossaire structuré de l’IA embarquée

Embedded France avec la Fondation Eclipse. 2026. Référentiel pédagogique · v1.1, 22 juillet 2026 · CC BY 4.0.

[Source originale](https://pages.eclipse.dev/eclipse/aidge/embedded-ai-glossary/embedded-ai-glossary.fr.pdf)

Apport : Relier données, modèles, exécution, matériel, mesures et cycle de vie.

Limite : Glossaire non normatif ; ne remplace ni un cours de calcul, ni les sources techniques. Distinguer puissance en W et énergie en J ; un percentile observé ne garantit pas le temps réel.



## R25 — Electronic Neural Network, Mark I Perceptron

Smithsonian · National Museum of American History. 1958. Notice institutionnelle · date de l’objet au catalogue.

[Source originale](https://americanhistory.si.edu/collections/object/nmah_334414)

Apport : Le réseau est matérialisé par des circuits et des potentiomètres.

Limite : La datation muséale ne date pas chaque étape ; la démonstration de 1958 sur IBM 704 est distincte du Mark I matériel.



## R26 — Lecture 5 · Convolutional Neural Networks

Stanford · CS231n. 2020. Cours universitaire officiel · histoire du perceptron.

[Source originale](https://cs231n.stanford.edu/slides/2020/lecture_5.pdf)

Apport : Décrit la grille de 20 × 20 photocellules du Mark I, soit 400 entrées lumineuses.

Limite : Source pédagogique secondaire ; ne suffit pas à établir la date de mise en service ni les moteurs des potentiomètres.



## R27 — Efficient Training of Artificial Neural Networks for Autonomous Navigation

Dean A. Pomerleau. 1991. Neural Computation 3(1), 88–97 · article original.

[Source originale](https://publications.ri.cmu.edu/efficient-training-of-artificial-neural-networks-for-autonomous-navigation)

Apport : Version à 30 × 32 pixels, 5 neurones cachés et 30 sorties ; vues décalées et directions corrigées pour apprendre le retour vers la route.

Limite : Ne pas attribuer cette architecture à toutes les versions d’ALVINN ; les rotations ne sont pas établies par cette lecture.



## R28 — Gradient Based Learning Applied to Document Recognition

Yann LeCun, Léon Bottou, Yoshua Bengio, Patrick Haffner. 1998. Proceedings of the IEEE 86(11), 2278–2324 · article original.

[Source originale](https://bottou.org/papers/lecun-98h)

Apport : Réseaux convolutifs et lecture de documents, dont un système commercial de lecture de chèques.

Limite : Ce système de lecture ne prouve pas que la puce ANNA ait équipé les installations commerciales.



## R29 — A Neurocomputer Board Based on the ANNA Neural Network Chip

Eduard Säckinger, Bernhard E. Boser, Lawrence D. Jackel. 1991–1992. NeurIPS 1991 · actes publiés en 1992.

[Source originale](https://proceedings.neurips.cc/paper_files/paper/1991/hash/5e388103a391daabe3de1d76a6739ccd-Abstract.html)

Apport : Carte avec puce ANNA et DSP, évaluée notamment pour la reconnaissance de codes postaux manuscrits.

Limite : Prototype de recherche ; apprentissage hors puce puis chargement des poids.



## R30 — Optimal Brain Damage

Yann LeCun, John S. Denker, Sara A. Solla. 1989–1990. NeurIPS 1989 · actes publiés en 1990.

[Source originale](https://proceedings.neurips.cc/paper_files/paper/1989/hash/6c9882bbac1c7093bd25041881277658-Abstract.html)

Apport : Estimer la sensibilité de l’erreur pour supprimer certains poids.

Limite : L’élagage ne garantit pas un gain de temps : la structure et le moteur d’exécution comptent.



## R31 — ImageNet Classification with Deep Convolutional Neural Networks

Alex Krizhevsky, Ilya Sutskever, Geoffrey E. Hinton. 2012. NeurIPS 2012 · article original.

[Source originale](https://proceedings.neurips.cc/paper_files/paper/2012/hash/c399862d3b9d6b76c8436e924a68c45b-Abstract.html)

Apport : AlexNet illustre l’essor des réseaux profonds entraînés avec des GPU.

Limite : Résultats ImageNet ; ne décrit pas une implantation sur Raspberry Pi ou microcontrôleur.



## R32 — Deep Compression: Compressing Deep Neural Networks with Pruning, Trained Quantization and Huffman Coding

Song Han, Huizi Mao, William J. Dally. 2015–2016. Prépublication 2015 · ICLR 2016.

[Source originale](https://arxiv.org/abs/1510.00149)

Apport : Associer suppression de poids, quantification et codage pour réduire le stockage.

Limite : Taille compressée sur disque et mémoire de travail pendant l’inférence sont différentes ; aucun facteur de gain universel.



## R33 — Launching TensorFlow Lite for Microcontrollers

Pete Warden. 2019. Annonce du concepteur · 7 mars 2019.

[Source originale](https://petewarden.com/2019/03/07/launching-tensorflow-lite-for-microcontrollers/)

Apport : Lancement expérimental public après un travail commencé l’année précédente.

Limite : Jalon de structuration du TinyML ; pas la naissance de toute l’IA sur microcontrôleur.



## R34 — TinyML

Pete Warden, Daniel Situnayake. 2019. Livre · notice officielle O’Reilly, décembre 2019.

[Source originale](https://www.oreilly.com/library/view/tinyml/9781492052036/)

Apport : Organiser le passage du modèle au dispositif à faible consommation.

Limite : Ouvrage pédagogique ; les exemples ne prouvent pas que toute tâche tient sur toute carte.



## R35 — Professor’s perceptron paved the way for AI – 60 years too soon

Melanie Lefkowitz · Cornell Chronicle. 2019. Histoire institutionnelle · Cornell University.

[Source originale](https://news.cornell.edu/stories/2019/09/professors-perceptron-paved-way-ai-60-years-too-soon)

Apport : Distingue la démonstration du perceptron sur IBM 704 en juillet 1958 de la machine matérielle.

Limite : Utilisé pour cette distinction historique ; les formules journalistiques sur les réseaux modernes ne sont pas reprises.
