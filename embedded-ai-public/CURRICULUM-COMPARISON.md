# Pourquoi ce parcours ? Comparaison avec des cursus de référence

Roland Cédric TAYO · INEM

L’objectif est un cours progressif accessible au grand public, avec une ouverture vers l’ingénierie. Les cursus ci-dessous ont été choisis pour leurs programmes publics, leur lien avec les ressources limitées et leur place accordée à la pratique. Il ne s’agit pas d’un classement mondial des « meilleurs cours », ni d’une équivalence avec un semestre universitaire.

## Les quatre points de comparaison

| Cursus et source officielle | Accent du programme public | Activités accessibles ou annoncées | Ce qui est retenu ici |
|---|---|---|---|
| [MIT 6.5940 — TinyML and Efficient AI Computing, 2026](https://hanlab.mit.edu/courses/2026-fall-65940) | Compression, recherche d’architecture, calcul efficace et modèles génératifs. | La liste publiée annonce des laboratoires GPU, élagage, recherche d’architecture, quantification et déploiement de modèles de langage. Certains liens Colab consultés demandent une connexion : leur contenu intégral n’a pas été audité. | Raisonner sur le matériel et vérifier les gains ; ajouter le goulet mémoire/calcul, la calibration et le choix d’architecture. |
| [Harvard CS249r — Tiny Machine Learning, 2023](https://sites.google.com/g.harvard.edu/cs249-tinyml-2023) | Données, chaîne de déploiement, mesures, sécurité, maintenance et responsabilité. | Projet pratique et revue de publications ; [dépôt public historique des assignments 2020](https://github.com/Harvard-CS249R-Fall2020/assignments) avec familles hello_world, wake_words, gesture_recognition, person_detection et responsible_ai. Ce dépôt historique n’est pas présenté comme le sujet courant. | Suivre une application entière ; ajouter les exigences, les événements rares, la veille et le suivi après livraison. |
| [ETH Zurich — Machine Learning on Microcontrollers, 2026](https://pbl.ee.ethz.ch/education/mlom.html) | Acquisition, caractéristiques utiles, modèles classiques et profonds, optimisation et co-conception. | Le descriptif annonce classification son/image sur matériel, compression et profilage énergétique. Il ne fournit pas sur cette page tous les énoncés détaillés. | Garder capteur et prétraitement dans le raisonnement ; présenter l’arbre de décision et le compromis propre à la cible. |
| [Heidelberg — Embedded Machine Learning, 2026–2027](https://hawaii.ziti.uni-heidelberg.de/teaching/eml/) | Interaction modèle–matériel, données imparfaites, réseaux, architectures et optimisations. | Programme comprenant réseaux construits à partir des bases, différentiation et séances d’exercices annoncées ; détail des exercices non audité ici. | Relier les opérations aux coûts et séparer équivalence de calcul et modification approximative du modèle. |

Les [ressources TinyMLedu](https://tinyml.seas.harvard.edu/courses/) relient également fondations, applications, déploiement et MLOps. Elles permettent de poursuivre avec des supports et du matériel adaptés.

## Ce qui était déjà présent

Le cours initial couvrait données et partitions, neurone et gradient, CNN et attention, mémoire et latence, quantification, déploiement, tests et méthode de recherche. La comparaison ne justifiait pas de recommencer ces bases ni de copier des cours entiers.

## Les ajouts ciblés

| Lacune ou point trop bref | Ajout dans le cours | Question que le lecteur doit pouvoir traiter |
|---|---|---|
| Besoin encore peu testable | **Avant de construire : promettre quoi ?** | Quelles conditions et quels critères vérifier ? |
| Indicateur global trop facile à surinterpréter | **99 % de réussite peut cacher un échec** | Le système détecte-t-il les événements importants ? |
| Vision centrée sur les réseaux | **Un arbre de décision peut suffire** | Faut-il réellement un réseau pour cette tâche ? |
| Profilage encore abstrait | **Qui attend qui : le calcul ou la mémoire ?** | Quelle ressource limite le système ? |
| Attente et réveil insuffisamment visibles | **Écouter sans tout calculer en permanence** | Que coûte le système quand rien ne se passe ? |
| Quantification présentée trop vite comme un arrondi | **Avant d’arrondir : regarder les vraies valeurs** | Les échelles couvrent-elles les données utiles ? |
| Architecture et cible peu reliées | **Le meilleur réseau dépend aussi de la carte** | Quel compromis reste valable sur le matériel visé ? |
| Fin du projet assimilée à la livraison | **Après livraison, la maison peut changer** | Comment détecter un problème et revenir à une version fiable ? |

Ces explications, schémas et exemples sont originaux. Les exemples chiffrés ajoutés sont explicitement fictifs ou calculés ; aucune mesure sur carte n’est inventée.

## Ce qui n’est pas ajouté au parcours principal

Le calcul distribué de grands entraînements, l’écriture complète de noyaux GPU, les modèles de diffusion et la conception détaillée d’accélérateurs demandent des prérequis et un autre volume de cours. Ils restent des pistes d’approfondissement, sans être nécessaires pour comprendre puis déployer un premier petit modèle embarqué. Le cours conserve la distinction entre PC, ordinateur embarqué sous Linux et microcontrôleur ; il n’impose pas l’achat d’une nouvelle carte.

## Architecture pédagogique et format

Huit chapitres nommés suivent le besoin, les données, le neurone, les réseaux, la machine, les compromis, le déploiement et la recherche. Dans une diapo, les explications et le dessin progressent ensemble. Les éléments futurs ne sont pas tous affichés dès l’arrivée : l’utilisateur construit, interrompt, remonte ou rejoue la scène. Les manipulations numériques restent de vrais petits calculs exécutés dans le navigateur.

Le format retenu est **HTML, SVG et JavaScript**, avec une maquette 3D CSS. Il permet la publication sur GitHub Pages, le contrôle de la progression et les manipulations au clavier ou à la souris. Une vidéo permet de revoir une explication ; ce format ajoute la manipulation des éléments et le calcul interactif. La version de lecture et le PDF conservent les explications complètes pour réviser.

### Référence visuelle fournie

La [vidéo de Nerdy Kings indiquée par l’utilisateur](https://www.youtube.com/watch?v=ZLYJXe7V3NU) est une référence de style, pas une source scientifique du cours. Son titre a été récupéré via les métadonnées publiques YouTube ; le visionnage direct n’a pas été disponible dans l’outil de recherche. Aucune analyse image par image de son montage n’est revendiquée. L’adaptation répond au besoin décrit : composition progressive, liens visibles, pauses et manipulations.

## Limite de cette comparaison

Les pages officielles et les ressources publiques consultables permettent une comparaison de couverture et de démarche. Elles ne permettent pas de certifier la qualité d’un enseignement en classe ni d’inspecter des exercices fermés. Ce cours grand public ne devient pas équivalent à un cursus de master par l’ajout de ses thèmes ; la compétence se vérifie ensuite par des réalisations et des mesures.
