# Vérification de la présentation et des ajouts

Roland Cédric TAYO · INEM

## Ce qui a été revu

La comparaison des programmes MIT, Harvard, ETH Zurich et Heidelberg a conduit à huit ajouts originaux. Le document CURRICULUM-COMPARISON.md précise les sources consultées et les limites d’accès aux exercices. Les 55 notions initiales sont conservées ; le parcours comporte 63 notions, quatre activités et huit chapitres nommés.

Une relecture indépendante simulée a examiné les ajouts, la comparaison et le mécanisme de composition des schémas. Elle n’est pas un test auprès d’enfants réels.

## Trois corrections issues de cette relecture

1. L’étiquette du masque causal précise qu’il est déjà appliqué aux scores avant softmax. Sa révélation tardive est une étape d’explication, pas une opération effectuée après le résultat.
2. La lecture automatique ne remplace plus le texte toutes les 1,5 seconde. Le délai dépend du nombre de mots, avec un rythme réglable. Pause, retour à une phase et reconstruction restent possibles.
3. Le choix du HTML est justifié par les manipulations et calculs interactifs. Le document ne prétend pas qu’une vidéo ne peut pas être interrompue ou parcourue.

## Vérifications exécutées

- 229 contrôles du diaporama : présentation sans défilement sur sept formats d’écran, ajustement de toutes les explications, calculateurs, assemblage par clic et glisser-déposer, mémoire, retour de calcul virtuel, questions, outils et plein écran.
- Les contrôles de composition vérifient que des éléments apparaissent, que le dessin complet est atteint, que le retour retire les éléments futurs et que la pause arrête l’avancement.
- Le navigateur a réellement exécuté les animations : présence des animations natives et changement de matrice de transformation pendant la rotation 3D.
- 45 contrôles du document de lecture : calculs, entrées, questions et export PDF. Le PDF contient 68 pages sans page vide ni pied de page isolé ; les titres sont tous retrouvés et aucun texte ne déborde du format.

Les traces sont dans slides-validation.json et validation.json. Les captures viennent de ces exécutions, pas de maquettes d’interface inventées. Les tests concernent Chrome sur la machine indiquée dans les rapports ; ils ne garantissent pas tous les navigateurs ni tous les appareils physiques.

## Précautions pédagogiques

La construction d’un schéma est un ordre d’explication. Elle ne représente pas une durée CPU ni une mesure énergétique. La RAM est représentée au même instant, et l’arbre de décision montre des branches alternatives. La carte 3D est une maquette, et le trajet PC–carte–PC est virtuel. Aucun Raspberry Pi n’est connecté ni mesuré par ce support.

La lecture dès 10 ans reste un objectif de conception. Les notions avancées peuvent demander un accompagnement et de la pratique. Le cours ne délivre pas une expertise par simple lecture. La référence YouTube a fourni un cadrage de style ; aucune analyse image par image de son montage n’est revendiquée.


## Correction de l’orchestration et des quiz

Le placement des formes ne détermine plus l’ordre de révélation. orchestration.py définit des groupes explicites et vérifie que les primitives des scènes particulières sont toutes affectées. La personne, ses membres, les textes et les briques sont révélés en ensembles cohérents. Les connexions sont animées après le début d’apparition des objets reliés. La formule du neurone précède son résultat numérique ; en RAM, les zones de travail apparaissent simultanément.

La première diapositive a été exécutée en lecture automatique dans un navigateur avec animations actives, et ses quatre états ont été capturés. Les 253 phases des 63 schémas ont été contrôlées : aucune phase non définie et aucune connexion vers un objet absent. Les quatre autres diapositives sont des activités manipulables déjà couvertes par les tests.

Les sept quiz ont chacun été testés avec les deux réponses, dans trois formats d’écran. Le bouton Continuer est désactivé avant réponse, activé après correction et avance exactement d’une diapositive. La correction et le bouton restent visibles sans défilement. Ces contrôles fonctionnels ne sont pas une preuve de compréhension auprès d’un public réel.
