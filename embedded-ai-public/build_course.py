"""Build the original, offline public course. No third-party executable dependencies."""
from pathlib import Path
import json, html, hashlib

ROOT=Path(__file__).resolve().parent
chapters=['Partir du besoin','Apprendre avec des nombres','Lire les réseaux actuels','Comprendre la petite machine','Optimiser sans se raconter d’histoires','Déployer, vérifier et chercher']
refs={
 'S1':('Harvard · Vijay Janapa Reddi, Machine Learning Systems','https://mlsysbook.ai/','Manuel ouvert : conception et cycle de vie des systèmes IA.'),
 'S2':('Google · séparer entraînement, validation et test','https://developers.google.com/machine-learning/crash-course/overfitting/dividing-datasets','Pourquoi réserver des exemples indépendants.'),
 'S3':('Dive into Deep Learning · propagation et rétropropagation','https://d2l.ai/chapter_multilayer-perceptrons/backprop.html','Calcul des gradients dans un réseau.'),
 'S4':('Stanford CS231n · réseaux convolutifs','https://cs231n.github.io/convolutional-networks/','Couches, convolution et réduction spatiale.'),
 'S5':('Howard et al., 2017 · MobileNets','https://arxiv.org/abs/1704.04861','Convolutions séparables pour la vision mobile.'),
 'S6':('Vaswani et al., 2017 · Attention Is All You Need','https://arxiv.org/abs/1706.03762','Architecture Transformer ; pas une démonstration de compréhension humaine.'),
 'S7':('Jacob et al., 2018 · Quantization and Training','https://arxiv.org/abs/1712.05877','Quantification et véritable calcul entier.'),
 'S8':('Lin et al., 2020 · MCUNet','https://hanlab.mit.edu/projects/mcunet','Concevoir ensemble réseau et moteur d’exécution pour microcontrôleur.'),
 'S9':('Dao et al., 2022 · FlashAttention','https://arxiv.org/abs/2205.14135','Réduire les échanges mémoire de l’attention sur GPU.'),
 'S10':('MIT Han Lab · On-Device Training, NeurIPS 2022','https://github.com/mit-han-lab/tiny-training','Entraînement sur appareil sous fortes contraintes ; code de recherche.'),
 'S11':('Lin et al. · AWQ','https://arxiv.org/abs/2306.00978','Quantification des poids de modèles de langage avec information des activations.'),
 'S12':('Dao et Gu, 2024 · Mamba-2','https://arxiv.org/abs/2405.21060','Autres calculs de séquence et lien avec l’attention.'),
 'S13':('Google AI Edge · LiteRT for Microcontrollers','https://developers.google.com/edge/litert/microcontrollers/overview','Un moteur pour des cibles très limitées ; compatibilité à vérifier.'),
 'S14':('Arm · CMSIS-NN','https://arm-software.github.io/CMSIS-NN/latest/','Noyaux optimisés, principalement pour Cortex-M.'),
 'S15':('ONNX Runtime · quantification','https://onnxruntime.ai/docs/performance/model-optimizations/quantization.html','Conditions, formats et limites des optimisations.'),
 'S16':('Raspberry Pi · fiche du Pi 5','https://www.raspberrypi.com/products/raspberry-pi-5/','Exemple d’ordinateur embarquable sous Linux, distinct d’un microcontrôleur.'),
 'S17':('Abdin et al., 2024 · Phi-3 Technical Report','https://arxiv.org/abs/2404.14219','Exemple de recherche sur des modèles de langage utilisables localement.'),
 'S18':('Eclipse Aidge · glossaire de l’IA embarquée','https://pages.eclipse.dev/eclipse/aidge/embedded-ai-glossary/embedded-ai-glossary.fr.pdf','Complément terminologique français ; PDF conservé dans les ressources du cours INEM.')
}
lessons=[]
def L(ch,title,lead,steps,flow,analogy='',limit='',deep='',quiz=None,source=(),widget=''):
 lessons.append(dict(ch=ch,title=title,lead=lead,steps=steps,flow=flow,analogy=analogy,limit=limit,deep=deep,quiz=quiz,source=list(source),widget=widget))

L(0,'Une intelligence dans un petit objet','Mila veut une lampe qui s’allume quand elle entend « lumière ». Même si Internet est coupé.',[
 'Nous allons suivre la même idée du besoin humain jusqu’au programme qui fonctionne dans l’objet.',
 'Une intelligence artificielle, ou IA, est ici un programme qui produit une prédiction à partir de données. Ce n’est ni une personne ni une preuve de compréhension.',
 'Un système embarqué est un ordinateur intégré à un objet pour lui rendre un service : une lampe, un vélo, un appareil de mesure ou un robot.',
 'L’IA embarquée fait exécuter tout ou partie de cette prédiction près du capteur, dans l’objet ou sur une machine voisine.'],
 ['Une personne parle','Un objet calcule','La lampe répond'],limit='Cette lampe est un exemple de conception. Nous n’annonçons aucune performance mesurée sur un matériel.',deep='Mode présentation : avancer avec les flèches. Mode lecture : voir tous les chapitres. Les calculs interactifs sont de vrais calculs pédagogiques ; les dessins ne sont pas des mesures.')
L(0,'Ce que vous pourrez vraiment faire','Comprendre une technique, c’est pouvoir expliquer ses choix et vérifier ses résultats.',[
 'Décrire le trajet d’une donnée depuis le capteur jusqu’à l’action.',
 'Calculer la sortie et une correction d’un tout petit modèle.',
 'Distinguer stockage, mémoire de travail, délai de réponse et énergie.',
 'Proposer une optimisation, puis un test capable de montrer qu’elle échoue aussi bien qu’elle réussit.'],['Expliquer','Calculer','Construire','Vérifier'],limit='Ce cours construit des fondations. L’expertise exige ensuite des projets, des mesures réelles et des retours d’expérience.',deep='Prérequis : lire des phrases, additionner et multiplier. Les calculs plus avancés sont expliqués dans les encadrés « Aller plus loin ». Aucun logiciel ni matériel n’est requis pour lire ce support.')
L(0,'Pourquoi mettre le calcul dans l’objet ?','Imaginez que la lampe doive demander à un serveur l’autorisation de s’allumer.',[
 'Un serveur est un ordinateur qui rend un service à d’autres ordinateurs. Le cloud désigne des ressources informatiques accessibles par un réseau.',
 'Une coupure réseau peut interrompre le service. Un aller-retour prend du temps. Envoyer un son peut aussi révéler une conversation.',
 'Calculer localement peut éviter cet envoi et continuer hors ligne. Cela consomme toutefois de l’énergie dans l’objet.',
 'On part du besoin : quel délai est acceptable ? Quelles données peuvent sortir ? Que fait l’objet en cas d’échec ?'],['Parler','Calcul local OU serveur','Autoriser l’action'],analogy='Demander à quelqu’un dans la pièce peut être plus direct que téléphoner à un bureau lointain.',limit='Local ne veut pas dire automatiquement plus sûr, moins cher ou plus économe : cela dépend du système complet.',source=['S13'])
L(0,'L’objet doit déjà fonctionner sans IA','L’IA est une pièce du système, pas le système entier.',[
 'Un capteur transforme un phénomène physique en information : un microphone transforme les variations de pression du son en signal électrique.',
 'Un actionneur produit un effet physique : une diode émet de la lumière, un moteur tourne.',
 'Le programme lit les données, décide puis commande l’actionneur. L’alimentation fournit l’énergie nécessaire.',
 'Pour une simple minuterie, une règle suffit. Ajouter une IA n’a d’intérêt que si elle résout mieux un besoin réel.'],['Capteur : microphone','Programme : décision','Actionneur : lumière'],analogy='Dans une cuisine, le thermomètre observe, la personne décide et la plaque chauffe. Ces rôles restent distincts.',limit='La comparaison n’attribue aucune conscience au programme.',quiz=('Pour allumer la lampe à 18 h chaque jour, que choisir d’abord ?',['Une règle horaire simple','Un grand modèle de langage'],0,'Le besoin est connu et déterministe. Tester d’abord la solution la plus simple évite du calcul et des risques inutiles.'))
L(0,'Écrire une règle ou apprendre une règle ?','Le mot « lumière » change selon la voix, l’accent et le bruit.',[
 'Une règle écrite à la main décrit explicitement quoi faire. Elle est utile quand les cas sont faciles à énumérer.',
 'L’apprentissage automatique ajuste un modèle, c’est-à-dire une fonction réglable, à partir d’exemples.',
 'Un modèle associe une entrée à une sortie. Ses paramètres sont les nombres réglables qui changent pendant l’apprentissage.',
 'Après apprentissage, l’inférence utilise ces paramètres pour produire une sortie sur une entrée. Elle ne les modifie généralement pas.'],['Exemples → apprentissage','Paramètres enregistrés','Nouvelle entrée → inférence'],analogy='S’entraîner à reconnaître des panneaux et reconnaître ensuite un panneau sont deux activités différentes.',limit='Un programme n’apprend pas spontanément de chaque utilisation : une procédure de mise à jour doit être prévue.')
L(0,'Toutes les IA ne font pas la même chose','Il faut nommer le problème avant de choisir le modèle.',[
 'Classification : choisir une catégorie, par exemple « lumière », « autre parole » ou « silence ».',
 'Régression : prédire une quantité, par exemple une température future.',
 'Détection : repérer un événement ou un objet, parfois avec sa position.',
 'Génération : produire une suite, par exemple du texte. Une réponse bien écrite peut pourtant être fausse.'],['Quel besoin ?','Quelle sortie attendue ?','Quelle preuve de réussite ?'],deep='Notre lampe demande une petite classification audio, pas une conversation générale. Une anomalie est un écart inhabituel : elle peut signaler un problème sans en donner la cause.')
L(0,'Une histoire de besoins et de contraintes','L’IA embarquée n’est pas née d’un seul inventeur ni d’une seule date.',[
 'D’abord, des objets ont exécuté des règles locales. Le besoin : agir près du monde physique.',
 'Les réseaux ont permis d’apprendre des régularités plus difficiles à écrire. Le besoin : reconnaître malgré les variations.',
 'MobileNets, proposé par Andrew Howard et ses collègues en 2017, réduit le coût de certaines convolutions pour la vision mobile.',
 'MCUNet, par Ji Lin et ses collègues en 2020, associe recherche de réseau et moteur d’exécution adapté à une très petite mémoire.'],['Règles locales','Modèles appris','Réseaux adaptés au matériel','Optimisation du système entier'],limit='Ces repères ne forment pas une chronologie exhaustive. Les règles et petits modèles restent utiles aujourd’hui.',deep='L’innovation ne remplace pas toujours une méthode ancienne. Elle peut permettre le même service avec une contrainte différente. Des modèles plus grands apparaissent aussi sur téléphones, avec d’autres budgets.',source=['S5','S8'])
L(0,'La carte du voyage','Nous reviendrons toujours à cette chaîne. Chaque bloc peut réussir seul et échouer dans l’ensemble.',[
 'Acquérir : recevoir un signal. Préparer : le convertir en nombres comparables.',
 'Prédire : appliquer le modèle. Décider : interpréter sa sortie avec les règles de sécurité.',
 'Agir : commander l’objet. Observer : vérifier ce qui s’est réellement passé.',
 'La question centrale sera : quel service pouvons-nous garantir avec les ressources disponibles ?'],['Acquérir','Préparer','Prédire','Décider','Agir'],deep='Dans un robot, agir change les observations suivantes : une boucle se ferme. Un retard ou une mauvaise synchronisation peut alors dégrader le comportement, même si le modèle seul semble correct.')

L(1,'Les exemples : de quoi le modèle apprend-il ?','Pour apprendre « lumière », il faut aussi lui montrer ce qui n’est pas « lumière ». ',[
 'Une donnée est une observation enregistrée : un son, une image ou une suite de températures.',
 'Une étiquette est la réponse de référence associée à un exemple. Quelqu’un doit vérifier qu’elle est correcte.',
 'Un jeu de données est un ensemble organisé d’exemples et, selon la méthode, de leurs étiquettes.',
 'Varier voix, distances et pièces aide à représenter le besoin. Enregistrer une seule personne ne représente pas tout le monde.'],['Plusieurs personnes','Exemples vérifiés','Catégories explicites'],analogy='Réviser seulement une seule écriture du chiffre 3 prépare mal à toutes les écritures possibles.',limit='Multiplier des copies du même enregistrement ne crée pas de nouvelles personnes ni de nouvelles situations.')
L(1,'Comment un son devient-il une liste de nombres ?','Le programme ne reçoit pas le mot : il reçoit des mesures.',[
 'Échantillonner signifie mesurer un signal à intervalles réguliers. La fréquence d’échantillonnage indique le nombre de mesures par seconde.',
 'Hertz, abrégé Hz, signifie « par seconde ». À 16 000 Hz, une seconde contient 16 000 échantillons.',
 'Un bit peut valoir 0 ou 1. Un octet contient 8 bits. À 16 bits par échantillon, une seconde mono occupe 32 000 octets non compressés.',
 'Mono signifie un canal. Ce calcul exclut l’en-tête du fichier et les tampons supplémentaires.'],['Pression de l’air','Microphone','16 000 nombres par seconde'],analogy='Comme prendre des photos très rapprochées d’un mouvement, on mesure régulièrement une évolution.',limit='Le dessin du son ne montre pas toutes les mesures ; la fréquence de dessin n’est pas celle de l’acquisition.',deep='Calcul exact de cet exemple : 16 000 × 16 / 8 = 32 000 octets. Une compression peut réduire un fichier, sans changer automatiquement la taille des données une fois décodées.')
L(1,'Préparer les nombres sans changer la recette','Le même traitement doit être appliqué avant l’apprentissage et dans la lampe.',[
 'Le prétraitement prépare l’entrée : durée fixe, échelle des nombres ou découpage du signal.',
 'Normaliser peut signifier soustraire une moyenne puis diviser par une échelle. Il faut préciser laquelle et éviter une division par zéro.',
 'Un spectrogramme décrit comment l’intensité de différentes fréquences évolue avec le temps. Il peut servir d’entrée à un réseau.',
 'Les réglages estimés à partir des données se calculent sur l’entraînement, puis restent fixes pour les autres partitions.'],['Son brut','Recette enregistrée','Nombres du modèle'],analogy='Une recette ne doit pas changer de balance entre la cuisine d’essai et le restaurant.',limit='Un spectrogramme n’est pas une photographie du son. Il dépend de choix de fenêtre et de représentation.',deep='L’extraction de fréquences demande elle-même du calcul et de la mémoire. La supprimer du chronométrage peut cacher une grande partie du coût réel.')
L(1,'Ne pas réviser avec les réponses de l’examen','Nous avons besoin d’une preuve sur des exemples qui n’ont pas servi à régler le modèle.',[
 'Entraînement : exemples utilisés pour ajuster les paramètres.',
 'Validation : exemples utilisés pour choisir les réglages, par exemple la taille du réseau.',
 'Test : ensemble réservé pour l’évaluation finale après ces choix.',
 'Séparer par personne ou session peut éviter qu’un enregistrement presque identique apparaisse des deux côtés. C’est prévenir une fuite de données.'],['Entraînement : ajuster','Validation : choisir','Test : évaluer à la fin'],analogy='Exercices, examen blanc, puis examen final : trois rôles différents.',limit='Un test indépendant mais très différent de l’usage visé peut aussi donner une conclusion trompeuse.',source=['S2'],quiz=('Vous avez enregistré chaque voix dix fois. Quelle séparation est la plus prudente pour tester de nouvelles voix ?',['Garder certaines personnes entièrement pour le test','Mélanger tous les fichiers au hasard sans vérifier les personnes'],0,'Séparer les personnes limite le risque de reconnaître la voix déjà vue plutôt que le mot.'))
L(1,'Un neurone : multiplier, additionner, transformer','Commençons avec seulement deux nombres. Il n’y a pas de magie cachée.',[
 'x₁ et x₂ sont les deux entrées. w₁ et w₂ sont leurs poids : ils règlent leur influence.',
 'b est le biais : un décalage ajouté au résultat. Le score est z = w₁x₁ + w₂x₂ + b.',
 'Avec x₁ = 1, x₂ = 0, w₁ = 0,2, w₂ = −0,1 et b = −0,5, le score vaut −0,3.',
 'Une fonction de sortie transforme ensuite ce score. Un seuil à zéro donnerait ici la classe 0.'],['Entrées × poids','Somme + biais','Score puis transformation'],analogy='Une balance additionne des contributions positives et négatives avant de basculer.',limit='Ce neurone mathématique simplifie fortement un neurone biologique ; il n’en est pas une reproduction.',widget='neuron',deep='L’indice ₁ signifie « première entrée », pas une puissance. Le symbole × signifie multiplier. Vous pouvez modifier les deux entrées dans le calcul interactif.')
L(1,'Pourquoi ajouter une transformation ?','Empiler uniquement des additions et multiplications fixes ne suffit pas à créer tous les types de frontières.',[
 'Une activation est une fonction appliquée à une valeur calculée dans le réseau.',
 'ReLU remplace une valeur négative par zéro et conserve une valeur positive : ReLU(z) = max(0, z).',
 'La non-linéarité signifie que la transformation ne se réduit pas à une simple droite. Elle permet d’exprimer des relations plus variées.',
 'Pour apprendre par gradient, on emploie des fonctions dont on peut calculer les variations utiles, sauf en certains points traités par convention.'],['Score −0,3','ReLU','Sortie 0'],analogy='Un clapet bloque un sens de passage et laisse passer l’autre.',limit='ReLU ne représente pas une décision consciente. Une activation positive ne signifie pas « vrai ».',deep='Une alternative, tanh, comprime les valeurs entre −1 et 1. Une sigmoïde donne une valeur entre 0 et 1. Ce sont des formes différentes, avec des propriétés d’apprentissage différentes.')
L(1,'Une couche, puis plusieurs couches','Plusieurs neurones calculent des sorties différentes à partir d’une même entrée.',[
 'Une couche regroupe des opérations d’une étape. Une couche cachée est située entre l’entrée et la sortie.',
 'Un réseau est une composition de couches : la sortie d’une étape devient l’entrée d’une autre.',
 'Une activation désigne aussi le nombre intermédiaire produit. Ces nombres occupent de la mémoire pendant le calcul.',
 'Un MLP, ou perceptron multicouche, relie des couches denses : chaque sortie utilise toutes les entrées de la couche précédente.'],['2 entrées','3 neurones cachés','2 sorties'],analogy='Une chaîne d’ateliers transforme progressivement une matière, sans que chaque atelier voie le produit final.',limit='Les couches n’apprennent pas nécessairement des concepts humains nommables. Ce dessin décrit des dépendances de calcul.',deep='Pour une couche dense de n entrées et m sorties : n × m poids et m biais. Chaque symbole représente un nombre entier positif : n compte les entrées, m les sorties.')
L(1,'Une matrice évite de redessiner tous les neurones','Une matrice est simplement un tableau de nombres organisé en lignes et colonnes.',[
 'On range les poids d’une couche dans une matrice W. Une ligne contient les poids d’une sortie.',
 'Le vecteur x est une liste de nombres, les entrées. Le vecteur b contient les biais.',
 'Le calcul y = Wx + b signifie : pour chaque sortie, multiplier ses poids par les entrées puis additionner et ajouter son biais.',
 'Un MAC est une multiplication suivie d’une accumulation, c’est-à-dire l’ajout à une somme. Une couche dense n → m utilise n × m MAC.'],['Tableau W','Liste x','Une somme par ligne → y'],deep='Une convention fréquente compte un MAC comme deux opérations arithmétiques. Il faut annoncer la convention avant de comparer des chiffres. Un nombre d’opérations ne donne pas directement une durée.')
L(1,'Comment dire au modèle qu’il se trompe ?','Il faut transformer un écart en un nombre à réduire.',[
 'La prédiction est notée ŷ, « y chapeau ». La valeur de référence est y.',
 'Une perte mesure un écart. Pour une sortie numérique : L = ½(ŷ − y)². L est la perte, le carré pénalise les grands écarts.',
 'Pour cet exemple, ŷ = 0,2 et y = 1 donnent L = 0,32. Ce choix de perte sert à comprendre le calcul.',
 'Le taux d’erreur compte les mauvaises décisions parmi les essais. Il est différent de la perte.'],['Prédiction 0,2','Référence 1','Perte 0,32'],limit='Pour une classification, on utilise souvent une autre perte, l’entropie croisée. Une perte qui baisse ne garantit pas que chaque indicateur s’améliore.',deep='Le facteur ½ simplifie la dérivée. Sur N exemples, une perte moyenne additionne les pertes puis divise par N ; N est le nombre d’exemples.',source=['S3'])
L(1,'Corriger un poids, pas au hasard','Le gradient indique comment la perte varie quand on change un paramètre.',[
 'Dans notre petit modèle linéaire, ŷ = wx + b. Prenons x = 1, y = 1, w = 0,2 et b = 0.',
 'La perte vaut 0,32. Les gradients valent ici g_w = (ŷ − y)x = −0,8 et g_b = ŷ − y = −0,8.',
 'η, lettre grecque êta, est le pas d’apprentissage. La règle est w ← w − ηg_w et b ← b − ηg_b.',
 'Avec η = 0,1, w devient 0,28 et b devient 0,08. La nouvelle sortie vaut 0,36 et la perte 0,2048.'],['Calculer la perte','Trouver la pente','Faire un petit pas','Recalculer'],analogy='Une pente aide à choisir un petit pas vers le bas, sans donner à elle seule le chemin entier.',limit='Un pas trop grand peut augmenter la perte. Ici, la baisse est calculée pour cet exemple précis, pas garantie pour tout entraînement.',widget='gradient',deep='La rétropropagation calcule ces gradients de proche en proche dans un réseau. La dérivée est la variation locale d’un résultat quand on modifie une entrée ; la règle de chaîne relie ces variations.',source=['S3'])
L(1,'L’entraînement répète ce petit cycle','Un seul exemple ne suffit généralement pas.',[
 'Initialiser : choisir les premiers paramètres, souvent avec des nombres pseudo-aléatoires.',
 'Prédire, calculer la perte, calculer les gradients, puis corriger les paramètres. Une mise à jour est une correction.',
 'Une époque est un passage sur l’ensemble d’entraînement. Un lot est un petit groupe d’exemples traité avant une correction.',
 'Une graine fixe le départ d’un générateur pseudo-aléatoire. Elle aide à reproduire un essai, sans garantir l’égalité bit à bit entre tous les matériels.'],['Initialiser','Prédire','Comparer','Corriger','Recommencer'],deep='Pendant l’entraînement, il faut aussi mémoriser des valeurs utiles au calcul des gradients. Il peut donc demander bien plus de mémoire que la seule inférence. Une perte d’entraînement basse n’est pas un certificat de réussite en usage réel.')
L(1,'Apprendre les exemples ou apprendre à généraliser ?','Généraliser, c’est réussir sur de nouveaux cas pertinents.',[
 'Le surapprentissage apparaît quand le modèle s’adapte trop aux particularités des exemples connus.',
 'On observe séparément la perte d’entraînement et la perte de validation. Si la première baisse mais que la seconde monte, il faut enquêter.',
 'Un décalage de distribution signifie que les données d’usage diffèrent : autre microphone, autre bruit, autre langue.',
 'On peut chercher de meilleures données, un modèle plus simple ou un arrêt plus tôt. On vérifie ensuite avec le protocole prévu.'],['Exemples connus','Validation indépendante','Usage réel à éprouver'],limit='Une jolie courbe ne prouve pas la causalité. La séparation des données et la représentativité restent déterminantes.',quiz=('Le modèle réussit tous ses exercices mais échoue sur de nouvelles voix. Que conclure ?',['Il faut vérifier données, séparation et généralisation','Il faut seulement faire tourner le même test plus vite'],0,'La vitesse ne corrige pas un défaut de reconnaissance. Il faut d’abord comprendre les erreurs.'))

L(2,'Les images : regarder de petites fenêtres','Une convolution réutilise le même petit ensemble de poids à plusieurs positions.',[
 'Un pixel est une petite case d’image. Un canal est une composante, par exemple rouge, vert ou bleu.',
 'Un filtre est un petit tableau de poids. Il glisse sur l’entrée et produit une nouvelle carte de nombres.',
 'Partager ces poids évite de créer un détecteur indépendant à chaque position. Un CNN est un réseau qui utilise des convolutions.',
 'Il peut reconnaître des régularités locales dans une image, mais aussi dans une représentation du son.'],['Fenêtre de pixels','Même filtre à chaque position','Carte de résultats'],analogy='Un petit gabarit passe sur une grande feuille pour comparer la même forme à plusieurs endroits.',limit='Un filtre appris n’est pas toujours un « détecteur de bord » lisible à l’œil.',source=['S4'],widget='convolution')
L(2,'Réduire une image et séparer les calculs','Faire moins de calculs peut aider, mais la qualité doit être retestée.',[
 'Le pooling regroupe une petite zone, par exemple en conservant son maximum. Il réduit la taille spatiale des données intermédiaires.',
 'Une convolution depthwise applique un filtre séparé à chaque canal. Une convolution pointwise, de taille 1 × 1, mélange ensuite les canaux.',
 'MobileNets emploie ce découpage pour diminuer certains coûts par rapport à une convolution classique.',
 'L’organisation réelle de la mémoire et les bibliothèques disponibles déterminent si le matériel accélère effectivement le calcul.'],['Filtrer chaque canal','Mélanger les canaux','Vérifier qualité et durée'],limit='Réduire l’image peut supprimer le détail qui permettait de reconnaître un petit objet.',deep='Exemple théorique sans biais : filtre 3 × 3, 16 canaux d’entrée, 32 de sortie. Convolution classique : 3×3×16×32 = 4 608 poids. Séparable : 3×3×16 + 16×32 = 656. Le rapport de poids n’est pas un rapport de vitesse mesuré.',source=['S4','S5'])
L(2,'Une série dans le temps','Un son, une vibration et une température ne sont pas des images fixes : leur ordre compte.',[
 'Une série temporelle est une suite de mesures ordonnées dans le temps.',
 'Une fenêtre de contexte est la portion du passé utilisée pour calculer la sortie courante.',
 'Une convolution 1D compare de petits motifs successifs. Un réseau récurrent conserve un état, une mémoire numérique mise à jour au fil de la suite.',
 'Le choix dépend du besoin : un choc très court et une dérive lente ne demandent pas la même fenêtre.'],['Mesures passées','Fenêtre ou état','Prédiction courante'],analogy='Pour reconnaître un rythme, un coup isolé ne suffit pas : il faut regarder la suite.',limit='Conserver un état ne signifie pas mémoriser parfaitement tout le passé. La taille et le contenu de cet état restent limités.')
L(2,'Le texte entre aussi sous forme de nombres','Avant un modèle de langage, il faut découper et numéroter.',[
 'Un token est une unité de texte choisie par un découpage appelé tokenisation : caractère, morceau de mot ou autre unité.',
 'Un vocabulaire est la liste des tokens connus. Un identifiant est le numéro d’un token dans cette liste.',
 'Un embedding, ou représentation vectorielle apprise, associe à chaque identifiant une liste de nombres réglée pendant l’apprentissage.',
 'Les nombres d’identifiants ne disent pas que le token 20 est « deux fois plus important » que le token 10.'],['« la lampe »','Tokens : l · a · espace · …','Identifiants','Vecteurs appris'],limit='Notre découpage interactif par caractères sert à voir les étapes. Les modèles réels utilisent souvent des fragments de mots.',widget='tokens',deep='Une ligne de la table d’embedding est sélectionnée par l’identifiant. La distance entre vecteurs peut avoir un intérêt appris, mais aucun axe ne doit être baptisé « intelligence » sans preuve.')
L(2,'L’attention : combiner les éléments du contexte','Pour traiter une suite, on peut calculer quelles positions contribuent à une nouvelle représentation.',[
 'Une requête Q, une clé K et une valeur V sont trois transformations numériques des représentations d’entrée.',
 'On compare requêtes et clés pour obtenir des scores. Softmax transforme ces scores en nombres positifs dont la somme vaut 1.',
 'Ces coefficients pondèrent les valeurs : le résultat est une somme de contributions.',
 'Dans la génération causale, un masque empêche une position d’utiliser des tokens futurs pendant l’apprentissage.'],['Comparer Q et K','Normaliser les scores','Pondérer V','Nouvelle représentation'],analogy='Pour faire une synthèse, on donne des poids différents à plusieurs fiches disponibles.',limit='Ces poids ne sont pas une explication complète du raisonnement ni une mesure de conscience.',deep='Avec T positions, l’attention complète compare T × T couples. T désigne la longueur de contexte. Les autres projections et couches coûtent aussi du calcul.',source=['S6'])
L(2,'Le Transformer n’est pas seulement de l’attention','Il faut relier plusieurs opérations pour obtenir un réseau utile.',[
 'Une projection est une transformation par des poids, souvent un produit matriciel.',
 'Une connexion résiduelle additionne une entrée à une transformation de cette entrée. Elle aide à faire circuler les informations dans un réseau profond.',
 'Une normalisation remet certaines valeurs à une échelle contrôlée selon une formule définie.',
 'Un bloc Transformer combine attention, projections, normalisations et réseau de transformation. Chaque intermédiaire peut prendre de la place.'],['Représentation','Attention + addition','Normalisation','Réseau dense + addition'],limit='Ce schéma explique des rôles. L’ordre exact des normalisations et les fonctions dépendent de l’architecture.',deep='Architecture désigne l’organisation du réseau. Deux modèles dits « Transformer » peuvent avoir des tailles, des caches, des opérations et des contraintes de déploiement différents.',source=['S6'])
L(2,'Comment une réponse se construit-elle ?','Un modèle de langage produit une distribution sur le prochain token, puis recommence.',[
 'Une distribution de probabilités attribue une chance à chaque choix ; la somme vaut 1.',
 'On choisit le token le plus probable, ou on effectue un tirage suivant ces probabilités.',
 'Le token choisi rejoint le texte d’entrée. Cette génération autorégressive répète le calcul jusqu’à l’arrêt prévu.',
 'Une phrase plausible peut contenir une erreur factuelle. Une probabilité de token n’est pas une garantie de vérité.'],['Texte déjà présent','Probabilités du prochain token','Choix','Texte allongé'],deep='Un cache K/V conserve certaines clés et valeurs déjà calculées pour éviter de les recalculer. Il utilise de la mémoire qui augmente avec le contexte dans les Transformers usuels. Les limites exactes dépendent du modèle.',quiz=('Un modèle donne une phrase très convaincante. Est-elle forcément vraie ?',['Non : il faut vérifier les faits utiles','Oui : une phrase fluide prouve sa vérité'],0,'La qualité de rédaction ne démontre pas la vérité. Le système doit vérifier ou limiter ses usages à risque.'))
L(2,'Le meilleur modèle dépend de la tâche','Pour la lampe, nous n’avons pas besoin d’un modèle capable de rédiger un roman.',[
 'Commencer par une référence simple, ou baseline : la solution de comparaison que l’on sait exécuter et mesurer.',
 'Un petit CNN ou un modèle temporel peut convenir à quelques commandes audio. Un grand modèle génératif résout un autre besoin.',
 'Comparer une méthode à règles, un petit modèle et une variante plus complexe si cela est justifié.',
 'Le critère est le service rendu sous contraintes, pas la nouveauté du nom du modèle.'],['Besoin précis','Référence simple','Variantes mesurées','Choix justifié'],limit='Un modèle populaire n’est pas automatiquement compatible avec votre capteur, votre carte ou vos données.')

L(3,'Qu’y a-t-il dans la petite machine ?','Le calcul doit être exécuté par des composants physiques.',[
 'Le processeur, ou CPU, exécute les instructions du programme. Sa fréquence indique un rythme de cycles, pas le nombre exact de prédictions par seconde.',
 'Un microcontrôleur regroupe généralement processeur, mémoires et interfaces sur une puce pour des tâches embarquées.',
 'Un Raspberry Pi est un petit ordinateur pouvant exécuter Linux, un système d’exploitation qui gère programmes et ressources.',
 'Un GPU effectue de nombreux calculs en parallèle. Un NPU est un accélérateur spécialisé dans certaines opérations de réseaux.'],['Instructions','Processeur et mémoire','Interfaces vers les capteurs'],analogy='Une petite cuisine et une cantine peuvent préparer des repas, mais leurs équipements et leur organisation diffèrent.',limit='Un Pi ne reproduit pas les contraintes d’un microcontrôleur. Un accélérateur ne prend pas nécessairement en charge toutes les opérations.',source=['S16'])
L(3,'Stocker n’est pas travailler','Un modèle peut tenir dans le stockage et manquer de place pendant son exécution.',[
 'Le stockage conserve fichiers et programme sans alimentation : carte microSD ou mémoire Flash, selon l’appareil.',
 'La RAM est la mémoire de travail disponible pendant l’exécution. Elle contient notamment des entrées et résultats intermédiaires.',
 'Un cache est une petite mémoire proche du processeur qui conserve des informations pour limiter des accès plus lointains.',
 'Le bus est un chemin de communication entre composants. Transférer des nombres peut prendre du temps et de l’énergie.'],['Stockage : conserver','RAM : travailler','Cache : garder à proximité'],analogy='Livre de recettes dans l’armoire, plan de travail sur la table, ingrédients à portée de main.',limit='Les poids peuvent être lus directement depuis une mémoire ou copiés en RAM selon la cible. On ne doit pas les compter deux fois sans examiner l’exécution.')
L(3,'Compter les paramètres et les octets','Le budget devient concret quand on fait les comptes.',[
 'Pour un réseau dense 48 → 16 → 3, la première couche a 48×16 + 16 = 784 paramètres.',
 'La seconde a 16×3 + 3 = 51 paramètres. Total : 835 nombres, en comptant poids et biais.',
 'Float32 utilise 32 bits, soit 4 octets par nombre : 835×4 = 3 340 octets pour ces paramètres.',
 'Int8 utilise 8 bits, soit 1 octet. Les échelles et parfois les biais ont un autre format : leur place doit être ajoutée séparément.'],['Compter les poids','Ajouter les biais','Choisir le format','Ajouter les autres mémoires'],deep='1 kB = 1 000 octets ; 1 KiB = 1 024 octets. Le calculateur donne seulement le budget des paramètres, pas la taille totale de l’application.',widget='memory')
L(3,'Le pic mémoire peut arriver au milieu','Il faut considérer ce qui doit rester vivant au même instant.',[
 'Les activations sont les résultats intermédiaires. Un tampon est une zone de mémoire réservée à des données.',
 'Pendant une couche, l’entrée, la sortie et un espace de calcul temporaire peuvent coexister.',
 'Une connexion résiduelle peut obliger à conserver une ancienne activation pour l’addition suivante.',
 'Le pic de RAM est la plus grande mémoire simultanément utilisée, pas la somme de tous les résultats produits durant toute la vie du programme.'],['Entrée encore nécessaire','Calcul temporaire','Sortie en construction'],analogy='Le problème est le nombre de plats présents en même temps sur la table, pas tous les plats servis pendant la journée.',limit='Réutiliser un tampon demande de vérifier qu’aucune opération ne lit encore les anciennes valeurs.',deep='Il faut aussi compter piles d’appels, bibliothèques, système d’exploitation et acquisition. Le budget d’un réseau seul n’est pas celui du dispositif complet.',source=['S8'])
L(3,'Calculer ou déplacer : où part le temps ?','Réduire des multiplications ne suffit pas toujours.',[
 'Un calcul dense ou convolutif répète beaucoup de produits et de sommes.',
 'Si les données ne sont pas proches du processeur, il attend parfois leurs transferts. Le débit mémoire indique une quantité transférée par seconde.',
 'La vectorisation exécute une même opération sur plusieurs nombres à la fois avec des instructions adaptées.',
 'Un profiler est un outil qui aide à repérer où le programme passe son temps. On mesure avant de choisir la brique à modifier.'],['Lire les nombres','Calculer','Écrire les résultats'],limit='Le goulet d’étranglement, c’est la ressource qui limite le débit à cet endroit. Il peut changer après une optimisation.',deep='Un DMA est un mécanisme de transfert de données qui évite au CPU de copier chaque élément lui-même. Son bénéfice dépend des échanges et de leur synchronisation ; il ne supprime pas le coût physique des transferts.')
L(3,'Répondre assez vite, pas seulement en moyenne','La latence est le délai entre une entrée définie et la sortie correspondante.',[
 'Le débit compte les réponses par unité de temps. Il est différent de la latence d’une réponse.',
 'La gigue est la variation des délais. Une échéance est la limite de temps qu’un système doit respecter.',
 'Un système temps réel doit répondre selon ses exigences temporelles. « Rapide » ne suffit pas à le définir.',
 'Le délai total comprend acquisition, préparation, attente, inférence, décision et action.'],['Acquérir','Préparer','Attendre + prédire','Décider + agir'],analogy='Un bus peut transporter beaucoup de personnes par heure tout en vous faisant attendre longtemps.',limit='Le pire délai observé durant un test n’est pas une preuve du pire délai possible. Linux généraliste ne garantit pas à lui seul toutes les échéances.',deep='Le percentile 95 est une valeur en dessous de laquelle se trouvent environ 95 % des durées observées. Il faut préciser la convention de calcul et conserver les mesures brutes.')
L(3,'La batterie paie tout le système','La puissance et l’énergie sont deux grandeurs différentes.',[
 'La puissance est un rythme de consommation d’énergie. Elle se mesure en watts, symbole W.',
 'L’énergie est une quantité consommée. Elle se mesure notamment en joules, symbole J. À puissance constante : E = P×t, où t est la durée en secondes.',
 'Exemple de calcul, non mesuré : 2 W pendant 0,1 seconde donnent 0,2 J.',
 'Il faut aussi compter micro, radio, mémoire, attente et refroidissement. Le modèle n’est pas le seul consommateur.'],['Capteurs + calcul + radio','Puissance au fil du temps','Énergie totale'],limit='Une durée plus courte ne prouve pas une énergie plus faible si la puissance augmente. Sans instrument adapté, écrire « énergie non mesurée ».')
L(3,'Choisir local, cloud ou les deux','La bonne frontière dépend du besoin et des risques.',[
 'Local : le dispositif calcule lui-même. Il peut fonctionner hors ligne dans les limites du matériel.',
 'Cloud : l’objet envoie des données à un service distant. Il faut compter réseau, délai, confidentialité et dépendance au service.',
 'Hybride : une partie est locale et une autre distante, par exemple une détection locale avant un traitement plus lourd.',
 'Définir le comportement sans réseau et les données réellement envoyées. Garder les données sur place ne dispense pas de les protéger.'],['Besoin et données','Frontière de calcul','Mode dégradé prévu'],quiz=('Une IA locale chiffre-t-elle automatiquement tous les enregistrements ?',['Non : la protection doit être conçue','Oui : local veut dire chiffré'],0,'Le lieu du calcul et le chiffrement sont deux choix différents. Il faut aussi gérer accès, stockage et mises à jour.'))

L(4,'Optimiser : améliorer quoi, sans perdre quoi ?','Une amélioration n’a de sens qu’avec une comparaison équitable.',[
 'Fixer la tâche, les données et la cible. Définir une qualité minimale acceptable.',
 'Choisir une métrique principale : pic mémoire, délai ou énergie. Une métrique est un nombre qui décrit un aspect mesurable.',
 'Garder une référence exécutable et tester une modification identifiable.',
 'Comparer aussi ce qui peut se dégrader : qualité, robustesse, maintenabilité ou coût de conversion.'],['Référence','Une modification','Même protocole','Conclusion limitée'],deep='Un compromis qualité–latence–mémoire n’est pas un seul score universel. Les contraintes de votre application décident quelles solutions sont admissibles.')
L(4,'Quantifier : une règle avec moins de graduations','On représente les poids avec un nombre plus petit de valeurs possibles.',[
 'Dans un exemple symétrique signé, q est un entier entre −Q et Q. s est l’échelle qui relie l’entier au nombre réel.',
 'La recette est q = borner(arrondir(w/s), −Q, Q), puis poids reconstruit ŵ = s×q. w désigne le poids initial.',
 'Pour b bits, nous choisissons Q = 2^(b−1) − 1. À 2 bits, cette convention utilise −1, 0, +1 : trois niveaux.',
 'Une échelle globale sert à tout le groupe ; des échelles par couche ou canal s’adaptent à plusieurs groupes, avec un coût supplémentaire.'],['Poids réel','Arrondi sur une grille','Entier + échelle','Valeur reconstruite'],analogy='Mesurer au centimètre prend moins de graduations qu’au millimètre, mais perd de petits détails.',limit='Le calculateur simule l’arrondi puis calcule en flottant. Il ne mesure ni un calcul entier réel ni un gain matériel.',widget='quantization',deep='Borner signifie ramener une valeur trop grande à la limite. Si tous les poids d’un groupe sont nuls, on choisit par convention s = 1 pour éviter une division par zéro.',source=['S7'])
L(4,'Un fichier plus petit n’est pas forcément plus rapide','Il faut que le programme et le matériel sachent utiliser le format choisi.',[
 'La calibration est l’observation d’exemples représentatifs pour choisir certaines échelles de quantification.',
 'Quantifier après l’entraînement, ou PTQ, transforme un modèle déjà appris. L’entraînement conscient de la quantification, ou QAT, simule ses effets pendant l’apprentissage.',
 'Une véritable inférence entière doit gérer aussi les activations, accumulations, biais et changements d’échelle.',
 'Certaines opérations restent en flottant ou entraînent des conversions coûteuses. On vérifie la compatibilité puis on mesure sur la cible.'],['Poids compactés','Noyaux compatibles ?','Conversions éventuelles','Temps réel mesuré'],limit='Int8 ne garantit pas quatre fois moins de RAM totale ni quatre fois plus de vitesse que Float32.',deep='Un noyau, ou kernel, est ici une routine de calcul spécialisée. Le mot ne désigne pas le noyau du système d’exploitation dans cet encadré.',source=['S7','S15'])
L(4,'Retirer, simplifier ou transmettre un savoir','Plusieurs méthodes changent le réseau lui-même.',[
 'L’élagage, ou pruning, retire des poids ou des groupes de calcul. Une valeur zéro n’accélère pas nécessairement une multiplication dense.',
 'L’élagage structuré retire par exemple des canaux entiers, plus faciles à exploiter avec certaines routines.',
 'La distillation entraîne un petit modèle, l’élève, à reproduire certaines sorties d’un modèle enseignant plus grand.',
 'Réduire la taille d’entrée ou choisir une architecture plus simple est parfois plus efficace qu’une compression compliquée.'],['Réduire la structure','Réentraîner si nécessaire','Retester les erreurs'],analogy='Un résumé peut suffire pour une tâche, mais il faut vérifier qu’il conserve l’information utile.',limit='L’enseignant peut transmettre ses erreurs. Le mot « savoir » est ici une image pour ses sorties, pas une propriété humaine.')
L(4,'Réorganiser le travail sans changer la réponse','On peut aussi mieux exécuter les mêmes opérations.',[
 'Le calcul par tuiles traite de petits blocs pour mieux réutiliser les données proches du processeur.',
 'La fusion regroupe des opérations pour éviter d’écrire puis relire certains intermédiaires.',
 'Une allocation planifiée réutilise des zones mémoire dont les contenus ne sont plus nécessaires.',
 'Après modification, comparer les sorties avec une tolérance numérique annoncée, puis mesurer le temps et le pic mémoire.'],['Petit bloc chargé','Plusieurs usages proches','Moins de transferts'],analogy='Préparer plusieurs gestes avec les ingrédients déjà sur le plan de travail évite des allers-retours.',limit='L’ordre des additions peut changer les derniers chiffres en calcul flottant. L’équivalence doit être définie et testée.',deep='FlashAttention, proposé par Tri Dao et ses collègues en 2022, illustre le rôle des échanges mémoire dans l’attention sur GPU. Son bénéfice ne se transpose pas automatiquement à un Raspberry Pi.',source=['S9'])
L(4,'Choisir un compromis plutôt qu’un champion unique','Un modèle peut être meilleur en mémoire et moins bon en qualité.',[
 'Une solution domine une autre si elle est au moins aussi bonne sur chaque critère choisi, et strictement meilleure sur au moins un.',
 'Les solutions non dominées forment un front de Pareto. Il peut rester plusieurs bons choix.',
 'Appliquer d’abord les contraintes obligatoires : par exemple mémoire disponible et taux de détection minimal.',
 'Expliquer ensuite le choix selon l’usage. Ne pas sélectionner uniquement le point le plus spectaculaire du graphique.'],['Contraintes','Solutions admissibles','Compromis non dominés','Choix argumenté'],limit='Le graphique interactif suivant utilise des données fictives explicitement étiquetées. Il apprend à choisir ; il ne classe aucun modèle réel.',widget='pareto')

L(5,'Passer du PC à la carte','Le fichier de poids ne suffit pas à faire une application.',[
 'Enregistrer poids, architecture, catégories et recette de prétraitement dans des versions identifiables.',
 'Exporter signifie enregistrer le modèle dans un format exploitable. Convertir signifie le transformer pour un autre outil ou format.',
 'Le runtime est le logiciel qui exécute les opérations du modèle. Son backend est le chemin d’exécution choisi pour le matériel.',
 'Sur la carte, charger l’entrée, préparer, prédire, interpréter et commander. Prévoir aussi les erreurs de lecture et les sorties invalides.'],['PC : référence','Export et vérification','Carte : même entrée','Comparaison des sorties'],deep='En production, utiliser une bibliothèque vérifiée est souvent préférable. Pour comprendre, on peut écrire une petite couche à la main ; on compare alors son résultat à une référence.',source=['S13'])
L(5,'Choisir un outil qui sait exécuter les opérations','La compatibilité se vérifie avant de promettre un déploiement.',[
 'Sur un ordinateur embarqué sous Linux, plusieurs runtimes sont possibles selon le modèle et les formats pris en charge.',
 'LiteRT for Microcontrollers vise les petites cibles. CMSIS-NN fournit des routines optimisées principalement pour les processeurs Arm Cortex-M.',
 'ONNX est un format d’échange de modèles ; ONNX Runtime est un logiciel d’exécution. Ce ne sont pas deux noms du même objet.',
 'Vérifier les versions, dimensions, types numériques, opérations et licences. Une opération manquante peut bloquer tout le chemin.'],['Format accepté ?','Opérations prises en charge ?','Mémoire suffisante ?','Essai sur la cible'],limit='CMSIS-NN n’est pas le choix automatique pour le CPU d’un Raspberry Pi. Le processeur et les routines doivent correspondre.',source=['S13','S14','S15'])
L(5,'Mesurer proprement sur un Raspberry Pi','La carte est le juge de ses performances ; le PC aide à préparer et analyser.',[
 'Fixer modèle de Pi, alimentation, refroidissement, système, versions, nombre de fils d’exécution et fichier d’entrée.',
 'Échauffer : exécuter quelques appels avant la mesure. Chronométrer un groupe de K inférences avec une horloge monotone, qui ne recule pas si l’heure civile change.',
 'Répéter et alterner référence puis variante, puis l’ordre inverse. Garder les durées brutes et une somme de contrôle des sorties.',
 'Renvoyer les CSV au PC pour tracer médiane, dispersion, qualité et mémoire. Un CSV est un tableau texte de valeurs séparées.'],['PC prépare','Pi exécute','CSV brut','PC compare'],deep='K est le nombre d’appels. On peut le doubler jusqu’à une durée de groupe suffisante, puis garder K fixe pour la comparaison. Rapporter aussi température, charge et durée de l’acquisition. L’énergie reste « non mesurée » sans instrument.')
L(5,'Une prédiction correcte peut conduire à une mauvaise action','Il faut tester la chaîne complète dans son contexte.',[
 'La robustesse est la capacité à rester acceptable quand les conditions changent dans un domaine défini.',
 'Tester silence, bruit, microphone débranché, entrée trop forte, fichier invalide et mots proches de la commande.',
 'Un faux positif est une activation alors qu’il ne fallait pas agir. Un faux négatif est une commande manquée.',
 'Un comportement de repli est une action prévue en cas de doute ou de panne : ne pas agir, demander confirmation ou passer en mode sûr.'],['Données inattendues','Modèle et règles','Action ou repli'],limit='Un score élevé du modèle n’est pas à lui seul une confiance fiable. Les conséquences d’une erreur déterminent les précautions nécessaires.')
L(5,'Quand l’action change les données suivantes','La lampe et le robot ne posent pas exactement le même problème.',[
 'Un robot qui avance modifie ce que ses capteurs verront ensuite. L’action rentre indirectement dans la prochaine entrée.',
 'Une boucle relie observation, décision, action et nouvel état du monde.',
 'Un retard peut rendre une correction inadaptée et favoriser une oscillation. Des calculs parallèles peuvent aussi produire des résultats de dates différentes.',
 'Tester synchronisation, dates des mesures et comportement complet. Un résultat sur des fichiers enregistrés ne prouve pas la stabilité de la boucle.'],['Observer','Décider','Agir','Monde modifié → observer'],limit='Cette introduction ne remplace pas un cours d’automatique. Une oscillation est une possibilité à étudier, pas une conséquence systématique de l’IA.')
L(5,'Sécurité et vie privée : prévoir les mauvais jours','Un objet connecté reste un logiciel qu’il faut protéger et maintenir.',[
 'La confidentialité limite qui peut accéder aux informations. Le chiffrement rend des données illisibles sans la clé appropriée.',
 'La sécurité informatique vise notamment à empêcher des accès ou modifications non autorisés. La sûreté de fonctionnement concerne aussi les conséquences des défaillances.',
 'Limiter les données collectées et conservées. Définir autorisations, mises à jour et comportement hors ligne.',
 'Prévoir qu’un bruit volontaire ou un fichier modifié puisse tromper le système. Tester les risques liés à son usage réel.'],['Collecter le nécessaire','Protéger les accès','Prévoir les défaillances','Maintenir'],limit='Une IA locale peut toujours être trompée ou compromise. Aucune architecture n’élimine tous les risques.')
L(5,'Garder une trace de ce que l’on a réellement testé','Une expérience scientifique doit pouvoir être comprise et reprise.',[
 'Git conserve des versions du code. Un commit est un état enregistré avec un message expliquant le changement.',
 'Un manifeste décrit code, données, modèle, configuration, machine et mesures d’une campagne. Une empreinte SHA-256 aide à identifier le contenu exact d’un fichier.',
 'Un test unitaire contrôle une petite fonction. Un test d’intégration vérifie plusieurs composants ensemble. La CI lance automatiquement des contrôles sur des changements.',
 'Documenter le lancement, les unités, les limites et le retour à une version connue. DevOps relie développement et exploitation pour livrer et maintenir.'],['Version identifiable','Tests automatiques','Mesures conservées','Livraison reproductible'],limit='Une empreinte vérifie un contenu, pas la vérité d’une conclusion ni l’identité de son auteur.',deep='Exemple de dépôt : src/ pour le code, tests/ pour les contrôles, configs/ pour les réglages, experiments/ pour les CSV, figures/ pour les graphiques et deployment/ pour le lancement sur carte. Ne pas publier d’enregistrements personnels sans base appropriée.')
L(5,'Votre première enquête : combien de bits suffisent ?','Un petit projet peut déjà apprendre à raisonner comme un chercheur.',[
 'Choisir un petit réseau de référence et un jeu d’essai distinct. Ne pas commencer par entraîner un grand modèle génératif.',
 'Écrire avant mesure : « Je pense que 8 bits conserveront la qualité dans ces conditions ; je cherche où apparaît une dégradation. » C’est une hypothèse à tester.',
 'Comparer 32, 8, 4 et 2 bits sur les mêmes exemples propres puis bruités. Conserver les graines 42, 43 et 44 pour les variations aléatoires définies.',
 'Mesurer sur PC puis sur Pi. Distinguer arrondi simulé et calcul entier. Rapporter aussi les résultats nuls ou défavorables.'],['Hypothèse écrite','Protocole fixe','Mesures brutes','Conclusion limitée'],deep='Ne pas ajouter des données au test pour choisir le meilleur réglage. La comparaison propre doit garder les mêmes entrées pour toutes les variantes. Les graines contrôlent les tirages prévus ; préciser si elles concernent entraînement, bruit ou les deux.')
L(5,'Chercher : une question étroite, une preuve solide','La recherche commence quand la réponse est réellement à vérifier.',[
 'Lire un article et identifier exactement sa question, sa cible, ses données et ses limites.',
 'Reproduire une référence, puis modifier une seule idée à la fois. Une ablation retire ou change un élément pour comprendre sa contribution.',
 'Exemple : une échelle par couche réduit-elle les erreurs à 4 bits sur notre réseau audio, sans dépasser le budget mémoire ?',
 'Montrer les points individuels, les moyennes utiles, la dispersion et les limites. Avec trois graines, l’incertitude reste importante.'],['Question','Référence','Modification','Preuve ou réfutation'],limit='Battre un chiffre publié sur un autre matériel n’est pas une comparaison valable. Une IA générative peut aider au code et à l’analyse ; elle ne remplace pas une mesure vérifiée sur votre matériel.',deep='Un résultat original modeste peut ouvrir une piste. Une petite étude de classe n’est pas automatiquement publiable : nouveauté, comparaison, rigueur et portée doivent être évaluées.')
L(5,'Où les travaux récents cherchent-ils encore ?','Il n’existe pas un seul verrou : modèle, mémoire, calcul et usage doivent progresser ensemble.',[
 'Quantifier des modèles de langage sans perdre trop de qualité : AWQ utilise des informations d’activation pour guider le traitement des poids.',
 'Traiter des contextes longs avec moins d’échanges ou d’état : FlashAttention et les modèles de type Mamba explorent des calculs différents.',
 'Adapter un modèle directement sur une petite cible sans dépasser sa RAM : l’entraînement local limité reste un domaine d’étude.',
 'Garantir un comportement utile malgré bruit, changements et échéances : la validation du système reste indispensable.'],['Moins de mémoire','Moins de transferts','Adaptation locale','Fiabilité dans l’usage'],limit='Ce sont des pistes documentées, pas une liste exhaustive ni un classement des « meilleurs modèles ». Les gains d’un article valent dans ses conditions expérimentales.',deep='Question concrète de lecture : quel matériel, quel noyau, quelle taille de lot, quelle longueur de contexte et quelle mesure ? Sans ces conditions, une promesse de gain est incomplète.',source=['S9','S10','S11','S12'])
L(5,'Trois lectures pour passer du nom à la méthode','Pour chaque article, cherchez le problème avant les performances.',[
 'MCUNet : que gagne-t-on en concevant réseau et moteur ensemble ? Regarder mémoire des activations et planification, pas seulement les poids.',
 'FlashAttention : comment réduire les allers-retours mémoire tout en calculant l’attention ? Regarder la hiérarchie mémoire du GPU étudié.',
 'Phi-3 : que signifie « modèle de langage local » ? Examiner taille, protocole, appareil, qualité et limites plutôt que l’idée d’un modèle universel pour toute carte.',
 'Pour votre projet, reprendre une idée compatible avec votre besoin, puis écrire ce qui reste à vérifier sur votre cible.'],['Problème précis','Idée de l’article','Conditions','Votre question'],limit='Aucun chiffre de ces articles n’est présenté comme une mesure de notre cours ou de notre Pi.',source=['S8','S9','S17'])
L(5,'Pouvez-vous conseiller Mila maintenant ?','La lampe doit fonctionner sans réseau et ne pas envoyer les voix.',[
 'Choisir une petite classification locale plutôt qu’un assistant généraliste si quelques commandes suffisent.',
 'Garder des voix indépendantes pour tester et vérifier les mots proches, bruits et silences.',
 'Préparer un budget paramètres + activations + programme, puis mesurer le délai de bout en bout sur la cible.',
 'Si la qualité devient insuffisante après compression, garder le résultat et revoir le compromis plutôt que cacher l’échec.'],['Besoin','Données','Modèle','Matériel','Mesures et limites'],quiz=('Les poids tiennent en mémoire. Peut-on annoncer que la lampe est prête ?',['Non : il reste exécution, qualité, délais et sécurité à valider','Oui : la taille du fichier suffit'],0,'L’application doit aussi conserver ses activations, lire le son, produire les bonnes décisions et respecter ses exigences.'))
L(5,'De la compréhension à l’autonomie','Une étape est acquise quand vous pouvez la montrer, pas seulement la reconnaître.',[
 'Débutant : expliquer avec vos mots données, modèle, apprentissage et inférence ; refaire le calcul d’un neurone.',
 'Pratiquant : construire une chaîne simple, contrôler les données et comparer ses sorties entre PC et carte.',
 'Ingénieur : justifier les contraintes, les tests, le compromis et la maintenance avec des preuves reproductibles.',
 'Chercheur en apprentissage : formuler une question nouvelle et étroite, lire l’existant, tester puis expliquer ce que le résultat permet et ne permet pas de conclure.'],['Expliquer','Reproduire','Justifier','Explorer'],limit='Ce support ne délivre pas une expertise par simple lecture. Il vous donne la carte, les premiers outils et les critères pour progresser.',deep='Défi final : dessiner votre propre objet IA en cinq blocs. Pour chaque bloc, préciser une entrée, une sortie, un coût et un risque. Entourer la première chose à mesurer. Puis expliquer votre dessin à une personne qui ne connaît pas l’IA.')

# Apply the independent persona review before generating the deliverables.
lessons[1]['deep']='Prérequis : lire des phrases, additionner et multiplier. On rappelle les signes et les petites opérations au moment de les utiliser. Les encadrés « Aller plus loin » donnent des détails supplémentaires. Aucun logiciel ni matériel n’est requis pour lire ce support.'
lessons[6]['steps'][1]='Les réseaux de neurones sont des modèles organisés en plusieurs étapes de calcul. Ils permettent d’apprendre des régularités difficiles à écrire sous forme de règles.'
lessons[6]['steps'][2]='MobileNets, proposé par Andrew Howard et ses collègues en 2017, réduit certains calculs d’analyse d’images pour les appareils mobiles. Nous verrons comment au chapitre 3.'
lessons[6]['steps'][3]='MCUNet, par Ji Lin et ses collègues en 2020, adapte ensemble le modèle et le logiciel qui l’exécute pour une très petite mémoire.'
lessons[10]['steps'][2]='Un spectrogramme décrit l’intensité des fréquences du son au fil du temps : sons plus graves ou plus aigus. Ces fréquences ne sont pas le nombre de mesures prises par seconde.'
lessons[10]['steps'][3]='Les réglages estimés à partir des données se calculent sur l’entraînement. Ils restent ensuite fixes pour les autres groupes d’exemples, expliqués à l’étape suivante.'
lessons[12]['steps'][0]='x₁ et x₂ sont les deux entrées : les indices ₁ et ₂ disent « première » et « deuxième ». w₁ et w₂ sont les poids, qui règlent leur influence.'
lessons[12]['steps'][1]='b est le biais, un décalage ajouté à la somme. Le score est z = w₁×x₁ + w₂×x₂ + b. Le signe × demande une multiplication.'
lessons[12]['steps'][2]='Avec x₁ = 1, x₂ = 0, w₁ = 0,2, w₂ = −0,1 et b = −0,5, le score vaut −0,3. Un nombre négatif se trouve sous zéro, comme une température de −3 degrés.'
lessons[13]['lead']='Sans transformation supplémentaire, empiler des calculs linéaires ne permet pas de séparer tous les groupes d’exemples.'
lessons[13]['steps'][1]='ReLU garde le plus grand entre 0 et le score z : c’est le sens de max(0, z). Exemples : −1 devient 0 ; 0 reste 0 ; +1 reste +1.'
lessons[13]['steps'][3]='Les transformations sont choisies pour ce qu’elles permettent au modèle d’exprimer et pour leur facilité à être calculées et apprises.'
lessons[16]['steps'][1]='Une perte mesure un écart. Exemple : L = ½(ŷ − y)². Le carré signifie multiplier l’écart par lui-même ; ½ signifie diviser par deux. L est la perte.'
lessons[17]['steps'][1]='Si w passe de 0,20 à 0,21 en gardant b = 0, la sortie passe à 0,21 et la perte de 0,32 à 0,31205. Ici, augmenter ce poids un peu diminue la perte.'
lessons[17]['steps'][2]='Le gradient chiffre ce sens et cette sensibilité locale. Ici il vaut −0,8 pour w et b. Avec un pas η = 0,1 : w ← w − η×(−0,8). Le signe ← signifie « remplacer par le nouveau résultat ».'
lessons[17]['deep']='Pourquoi le gradient vaut-il −0,8 ? Pour L = ½(ŷ−y)², la pente par rapport à ŷ est ŷ−y = −0,8. Le symbole Δ signifie « petit changement ». Changer w de Δw change ŷ de x×Δw ; on multiplie donc la pente par x. Ici x = 1. Changer b de Δb change ŷ de Δb. Les deux gradients valent donc −0,8. On calcule tous les gradients avant de modifier les paramètres. Dans un grand réseau, cette transmission des pentes est la rétropropagation.'
lessons[23]['deep']='Une ligne de la table d’embedding est sélectionnée par l’identifiant. Le calculateur utilise une table fixe de caractères : un même caractère garde son identifiant quand la phrase change. Un caractère absent reçoit l’identifiant 0, nommé [INCONNU]. Les modèles emploient leur propre vocabulaire fixé à l’avance ; les numéros de notre exemple ne sont pas universels. Un axe d’embedding ne doit pas être baptisé « intelligence » sans preuve.'
lessons[24]['steps'].insert(0,'Exemple : trois positions donnent les valeurs 2, 10 et 0. Avec les coefficients 0,6, 0,3 et 0,1, la somme pondérée est 0,6×2 + 0,3×10 + 0,1×0 = 4,2. Les coefficients totalisent 1.')
lessons[35]['quiz']=('Une IA locale chiffre-t-elle, c’est-à-dire rend-elle illisibles sans une clé, tous les enregistrements automatiquement ?',['Non : la protection doit être conçue','Oui : local veut dire chiffré'],0,'Le lieu du calcul et le chiffrement sont deux choix différents. Il faut aussi gérer accès, stockage et mises à jour.')
lessons[37]['steps'][2]='b est le nombre de bits. Pour notre convention : à 4 bits, Q = 2×2×2 − 1 = 7. Plus généralement, Q = 2^(b−1) − 1 ; la puissance compte les multiplications par 2. À 2 bits, on garde −1, 0, +1.'
lessons[38]['quiz']=('Les poids Int8 prennent moins de place. Le programme sera-t-il forcément plus rapide ?',['Oui, toujours quatre fois plus rapide','Non : il faut un calcul compatible et une mesure sur la cible'],1,'Un fichier compact peut entraîner des conversions ou ne pas profiter des instructions disponibles. Seule la mesure vérifie le gain.')
lessons[44]['deep']='K est le nombre d’appels. Diviser la durée du groupe par K donne un temps moyen par appel dans ces conditions, pas une latence individuelle. Pour calculer des percentiles de latence, mesurer les appels séparément avec leurs conditions et le coût du chronométrage. Rapporter température, charge, acquisition et nombre de répétitions. L’énergie reste « non mesurée » sans instrument.'
lessons[44]['steps'][3]='Renvoyer les CSV au PC. Pour chaque groupe, calculer la durée divisée par K, puis la médiane et la dispersion entre groupes. Mesurer les appels séparément si l’on veut étudier leurs latences individuelles.'
lessons[45]['steps'][3]='La télévision peut prononcer réellement « lumière » : le mot est bien reconnu, mais personne n’a demandé à la lampe de s’allumer. Un repli prévu peut être de ne pas agir ou de demander confirmation.'
lessons[45]['deep']='Un faux positif est une activation non souhaitée ; un faux négatif est une commande manquée. Prévoir un comportement de repli en cas de doute ou de panne. Un score élevé n’est pas à lui seul une confiance fiable.'
lessons[48]['steps'][1]='Une fiche d’expérience, ou manifeste, décrit la version du code, les données, le modèle, les réglages, la machine et les mesures de la campagne.'
lessons[48]['steps'][2]='Un test unitaire contrôle une petite fonction. Un test d’intégration vérifie plusieurs composants ensemble. Ils donnent des preuves ciblées, pas une garantie universelle.'
lessons[48]['steps'][3]='Documenter le lancement, les unités, les limites et le retour à une version connue. Le but est simple : savoir ce que l’on a testé, retrouver les fichiers et refaire la mesure.'
lessons[48]['deep']='Une empreinte SHA-256 aide à identifier le contenu exact d’un fichier. La CI lance automatiquement des contrôles après des changements. DevOps relie développement et exploitation pour livrer et maintenir. Exemple de dépôt : src/, tests/, configs/, experiments/, figures/, deployment/. Ne pas publier d’enregistrements personnels sans base appropriée.'
lessons[54]['steps'][3]='Apprenti chercheur : formuler une question nouvelle et étroite, lire l’existant, tester puis expliquer ce que le résultat permet et ne permet pas de conclure.'
# Alternate option positions instead of teaching a trivial quiz-position pattern.
for idx,l in enumerate(lessons):
 if l['quiz'] and idx%2:
  q,options,c,reason=l['quiz'];l['quiz']=(q,list(reversed(options)),1-c,reason)

glossary={
 'Activation':'Fonction appliquée dans un réseau, ou résultat intermédiaire de son calcul selon le contexte.',
 'Apprentissage':'Procédure qui ajuste les paramètres d’un modèle à partir d’un objectif et de données.',
 'Architecture':'Organisation des opérations et couches d’un modèle.',
 'Biais':'Paramètre ajouté à une somme pondérée ; à distinguer d’un biais des données.',
 'Biais des données':'Déséquilibre ou particularité systématique qui peut fausser la représentation du besoin.',
 'Bit / octet':'Un bit prend deux valeurs ; un octet contient huit bits.',
 'Calibration':'Choix de réglages à partir d’exemples représentatifs ; préciser le contexte, notamment la quantification.',
 'Capteur / actionneur':'Le capteur observe un phénomène ; l’actionneur produit un effet physique.',
 'Classification':'Attribution d’une catégorie à une entrée.',
 'Convolution':'Application répétée d’un filtre partagé sur des voisinages de données.',
 'CPU / GPU / NPU':'Processeur généraliste / processeur parallèle / accélérateur spécialisé pour certaines opérations IA.',
 'Énergie / puissance':'Quantité consommée en joules / rythme de consommation en watts.',
 'Époque / mise à jour':'Passage sur l’entraînement / correction des paramètres.',
 'Float32 / Int8':'Formats numériques utilisant respectivement 32 bits flottants et 8 bits entiers.',
 'Flottant':'Représentation de nombres avec une précision limitée, permettant des valeurs petites ou grandes ; certains calculs sont arrondis.',
 'Volatile':'Se dit ici d’une mémoire qui perd son contenu quand son alimentation est coupée.',
 'Généralisation':'Réussite sur des données nouvelles pertinentes pour le besoin.',
 'Gradient':'Ensemble de variations locales de la perte par rapport aux paramètres.',
 'Inférence':'Utilisation d’un modèle pour calculer une sortie ; les poids restent généralement fixes.',
 'Latence / débit':'Délai d’une réponse / quantité de réponses par unité de temps.',
 'Mémoire Flash / RAM':'Mémoire non volatile / mémoire de travail généralement volatile.',
 'Modèle / paramètres':'Fonction réglable / nombres qui règlent cette fonction.',
 'Normalisation':'Transformation selon une règle d’échelle explicite ; plusieurs méthodes existent.',
 'Perte / taux d’erreur':'Écart numérique optimisé / proportion de mauvaises décisions.',
 'Quantification':'Représentation d’un ensemble de valeurs par un ensemble plus limité de niveaux.',
 'Runtime / backend':'Logiciel d’exécution / chemin choisi pour réaliser ses calculs sur un matériel.',
 'Temps réel':'Respect d’exigences temporelles définies ; pas seulement un calcul rapide.',
 'Token / embedding':'Unité discrète d’une suite / liste de nombres apprise associée à cette unité.',
 'Validation / test':'Données pour choisir les réglages / données réservées à l’évaluation finale.'}

def esc(s):return html.escape(str(s),quote=True)
def special_diagram(i):
 """Draw actual structures where a linear storyboard would hide the mechanism."""
 content='';caption=''
 def box(x,y,w,h,label,color='n0'):
  return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" class="node {color}"/><text x="{x+w/2}" y="{y+h/2+6}" text-anchor="middle">{esc(label)}</text>'
 def line(x,y,xx,yy):return f'<path d="M{x} {y} L{xx} {yy}" class="arrow" marker-end="url(#sarr{i})"/>'
 if i==0:
  content='<circle cx="95" cy="65" r="24" fill="#f4d5b2" stroke="#648c98"/><path d="M95 90v65m0-42l-35 24m35-24l35 24m-35 18l-28 38m28-38l28 38" class="arrow"/>'
  content+=box(160,25,225,58,'« lumière »','n2')+line(390,65,475,65)+box(480,25,250,80,'Calcul dans l’objet','n1')
  content+=line(735,65,820,65)+'<path d="M835 105 L875 25 L915 105 Z" fill="#f5d99b" stroke="#648c98"/><path d="M875 105v55m-35 0h70" class="arrow"/><text x="600" y="153" text-anchor="middle">Le réseau n’est pas nécessaire</text><text x="875" y="195" text-anchor="middle">Lampe</text>'
  caption='Une personne parle à la lampe ; le calcul local produit une décision sans aller-retour réseau.'
 elif i==9:
  content='<path d="M35 110 C65 20 95 200 125 110 S185 20 215 110 S275 200 305 110" fill="none" stroke="#3b889a" stroke-width="3"/>'
  for x,y in [(35,110),(80,90),(125,110),(170,130),(215,110),(260,90),(305,110)]:content+=f'<path d="M{x} 180 V{y}" stroke="#8cb6b2" stroke-width="2"/><circle cx="{x}" cy="{y}" r="5" fill="#28748b"/>'
  content+=line(340,110,430,110)+box(440,65,500,85,'Une liste de mesures ordonnées','n1')+'<text x="170" y="215" text-anchor="middle">Mesures à intervalles réguliers</text>'
  caption='Courbe et points schématiques : les points montrent des instants de mesure, pas les 16 000 valeurs de l’exemple.'
 elif i==12:
  content=box(20,20,140,65,'x₁ = 1')+box(20,135,140,65,'x₂ = 0')
  content+=line(165,52,280,100)+line(165,167,280,115)
  content+='<text x="210" y="45" text-anchor="middle">× 0,2</text><text x="210" y="193" text-anchor="middle">× −0,1</text>'
  content+=box(290,70,270,85,'Somme + b = −0,3','n1')+line(565,110,665,110)+box(675,70,290,85,'Seuil : classe 0','n2')
  content+='<text x="430" y="195" text-anchor="middle">b = −0,5</text>'
  caption='Les deux contributions arrivent à la même somme. Le biais est ajouté avant le seuil de décision.'
 elif i==14:
  for xx,ys,xxx,ys2 in [(170,[70,170],500,[40,120,200]),(500,[40,120,200],830,[70,170])]:
   for y in ys:
    for yy in ys2:content+=line(xx+24,y,xxx-30,yy)
  for x,ys,c in [(170,[70,170],'#d8eaf2'),(500,[40,120,200],'#dcefe6'),(830,[70,170],'#fae7c7')]:
   for k,y in enumerate(ys):content+=f'<circle cx="{x}" cy="{y}" r="25" fill="{c}" stroke="#648c98" stroke-width="2"/><text x="{x}" y="{y+6}" text-anchor="middle">{k+1}</text>'
  content+='<text x="170" y="252" text-anchor="middle">2 entrées</text><text x="500" y="252" text-anchor="middle">3 neurones cachés</text><text x="830" y="252" text-anchor="middle">2 sorties</text>'
  caption='Chaque cercle est une valeur ou un neurone. Chaque flèche entre couches porte un poids. Biais et activations ne sont pas dessinés.'
 elif i==15:
  content='<text x="150" y="25" text-anchor="middle">Matrice W</text>'
  for x,y,t,c in [(35,45,'0,2','n0'),(155,45,'−0,1','n0'),(35,115,'0,4','n1'),(155,115,'0,3','n1')]:content+=box(x,y,110,60,t,c)
  content+=box(340,40,180,135,'x = [1 ; 0]','n1')+box(575,40,390,135,'Wx = [0,2 ; 0,4]','n2')
  content+='<text x="150" y="210" text-anchor="middle">Une ligne par sortie</text><text x="310" y="115" text-anchor="middle">×</text><text x="550" y="115" text-anchor="middle">=</text>'
  caption='Exemple sans biais : chaque ligne est multipliée par les deux entrées. Sorties : 0,2×1−0,1×0 ; 0,4×1+0,3×0.'
 elif i==24:
  content=box(15,65,170,80,'Entrée')+box(245,10,130,55,'Q')+box(245,95,130,55,'K','n1')+box(245,180,130,55,'V','n2')
  content+=line(190,105,240,38)+line(190,105,240,122)+line(190,105,240,207)
  content+=line(380,38,455,80)+line(380,122,455,100)+box(460,45,225,80,'Scores → softmax','n1')
  content+=line(690,85,755,135)+line(380,207,755,160)+box(760,110,225,85,'Somme pondérée','n2')
  caption='Q et K produisent les coefficients. V fournit les valeurs pondérées : Q, K et V ne sont pas trois étapes successives.'
 elif i==31:
  content='<rect x="35" y="15" width="930" height="225" rx="15" fill="#f1f6f4" stroke="#648c98"/><text x="500" y="51" text-anchor="middle">Même instant : tout doit tenir dans la RAM disponible</text>'
  content+=box(65,85,270,100,'Entrée à garder')+box(365,85,270,100,'Travail temporaire','n2')+box(665,85,270,100,'Sortie à écrire','n1')
  content+='<text x="500" y="218" text-anchor="middle">Ajouter les autres mémoires réellement présentes</text>'
  caption='Les trois zones coexistent. Leur taille est symbolique ; aucune proportion de RAM n’est annoncée.'
 elif i==46:
  content=box(25,30,200,70,'Observer')+box(275,30,200,70,'Décider','n1')+box(525,30,200,70,'Agir','n2')+box(775,30,200,70,'Environnement')
  content+=line(230,65,270,65)+line(480,65,520,65)+line(730,65,770,65)+'<path d="M875 105 V190 H125 V105" class="arrow" marker-end="url(#sarr46)"/><text x="500" y="177" text-anchor="middle">L’action modifie l’observation suivante ; il existe un retard</text>'
  caption='La flèche de retour ferme la boucle d’action. Il faut étudier le système complet, pas seulement la prédiction.'
 if not content:return None
 height=280 if i==14 else 255
 svg=f'<svg viewBox="0 0 1000 {height}" role="img" aria-labelledby="diag{i}"><title id="diag{i}">{esc(caption)}</title><defs><marker id="sarr{i}" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto"><path d="M0 0 L6 3 L0 6" fill="#56747c"/></marker></defs>{content}</svg>'
 return svg,caption

def diagram(flow,i):
 n=len(flow);width=1000;box=(width-40-(n-1)*28)/n;out=[]
 for j,label in enumerate(flow):
  x=20+j*(box+28);words=label.split();lines=['']
  for w in words:
   if len(lines[-1])+len(w)>max(13,int(box/9)):lines.append(w)
   else:lines[-1]+=(' ' if lines[-1] else '')+w
  out.append(f'<rect x="{x:.1f}" y="22" width="{box:.1f}" height="104" rx="16" class="node n{j%3}"/>')
  for k,line in enumerate(lines):out.append(f'<text x="{x+box/2:.1f}" y="{76-(len(lines)-1)*11+k*22}" text-anchor="middle">{esc(line)}</text>')
  if j<n-1:out.append(f'<path d="M{x+box+4:.1f} 74 h20" class="arrow" marker-end="url(#arr{i})"/>')
 return f'<svg viewBox="0 0 1000 150" role="img" aria-labelledby="diag{i}"><title id="diag{i}">{esc(" → ".join(flow))}</title><defs><marker id="arr{i}" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto"><path d="M0 0 L6 3 L0 6" fill="#56747c"/></marker></defs>'+''.join(out)+'</svg>'

def quiz_html(q,i):
 title,options,correct,feedback=q
 return f'<div class="quiz" data-correct="{correct}"><h3>À vous de décider</h3><p>{esc(title)}</p><div class="options">'+''.join(f'<button type="button" data-answer="{j}">{esc(o)}</button>' for j,o in enumerate(options))+f'</div><p class="feedback" aria-live="polite" hidden>{esc(feedback)}</p><details class="print-answer"><summary>Voir la réponse et sa raison</summary><p>{esc(options[correct])} — {esc(feedback)}</p></details></div>'

def widget(w):
 if w=='neuron':return '<div class="lab" data-widget="neuron"><h3>Manipuler le neurone</h3><label>x₁ <input id="x1" type="range" min="-2" max="2" step="0.1" value="1"></label><label>x₂ <input id="x2" type="range" min="-2" max="2" step="0.1" value="0"></label><output id="neuron-out"></output><p>Poids fixes : 0,2 et −0,1 ; biais : −0,5. Les curseurs changent les entrées, pas les poids.</p></div>'
 if w=='gradient':return '<div class="lab" data-widget="gradient"><h3>Une vraie correction, calculée ici</h3><p>Modèle ŷ = wx + b ; x = 1 et référence y = 1.</p><button id="gradient-step">Faire une correction avec η = 0,1</button> <button id="gradient-reset">Repartir de w = 0,2 et b = 0</button><output id="gradient-out"></output><p id="gradient-log" aria-live="polite"></p></div>'
 if w=='convolution':return '<div class="lab" data-widget="convolution"><h3>Suivre une fenêtre 1D, version simplifiée</h3><p>Entrée [1, 2, 0, 3, 1] ; filtre partagé [1, −1]. Sans biais, pas de 1, sans ajout aux bords.</p><button id="conv-next">Déplacer le filtre</button><output id="conv-out"></output><div id="conv-cells" class="cells"></div></div>'
 if w=='tokens':return '<div class="lab" data-widget="tokens"><h3>Voir le découpage par caractères</h3><label>Votre texte <input id="token-input" maxlength="60" value="la lampe"></label><div id="token-cells" class="cells"></div><p id="token-vocab"></p><p>Vocabulaire fixe de démonstration : un caractère garde le même identifiant quand la phrase change. Les caractères absents utilisent ID 0 = [INCONNU]. Ici, aucun modèle n’est entraîné.</p></div>'
 if w=='memory':return '<div class="lab" data-widget="memory"><h3>Calculer le budget des paramètres</h3><label>Nombre de paramètres <input id="parameter-count" type="number" min="1" max="100000000000" value="835"></label><label>Bits par paramètre <select id="memory-bits"><option>32</option><option>16</option><option>8</option><option>4</option><option>2</option></select></label><output id="memory-out"></output><p>Stockage idéal compacté, arrondi à l’octet supérieur. Échelles, activations, programme et système exclus.</p></div>'
 if w=='quantization':return '<div class="lab" data-widget="quantization"><h3>Voir ce que l’arrondi change</h3><label>Bits <select id="quant-bits"><option>8</option><option>4</option><option>2</option></select></label><output id="quant-out"></output><div id="quant-cells" class="cells"></div><p>Poids fixés pour l’exemple : [−1, −0,3, 0,1, 0,7]. Erreur : moyenne des écarts absolus. Quantification simulée, aucun benchmark matériel.</p></div>'
 if w=='pareto':return '<div class="lab" data-widget="pareto"><h3>Choisir avec deux contraintes</h3><p>Données fictives : A = 92 %, 20 ms, 100 kB ; B = 90 %, 10 ms, 70 kB ; C = 89 %, 18 ms, 100 kB.</p><label>Qualité minimale (%) <input id="quality-min" type="range" min="85" max="95" value="90"></label><label>Latence maximale (ms) <input id="latency-max" type="range" min="5" max="25" value="20"></label><output id="pareto-out"></output><svg id="pareto-chart" viewBox="0 0 600 230" role="img" aria-label="Comparaison fictive qualité et latence : la meilleure direction va vers le haut et la gauche"><path d="M60 20V190H570" fill="none" stroke="#648c98"/><text x="300" y="225" text-anchor="middle">Latence (ms) : à gauche, plus rapide</text><text x="15" y="15">Qualité (%)</text><text x="35" y="195">85</text><text x="35" y="30">95</text><text x="60" y="212">5</text><text x="550" y="212">25</text><path id="quality-line" stroke="#c37c24" stroke-dasharray="5 5" d=""/><path id="latency-line" stroke="#c37c24" stroke-dasharray="5 5" d=""/><g id="pareto-dots"></g></svg><div id="pareto-points" class="cells"></div><p>B domine C. A et B ne se dominent pas : A a une meilleure qualité, B est plus rapide et plus petit. La couleur verte indique le respect des deux contraintes ; elle ne prouve pas la domination.</p></div>'
 return ''

articles=[]
for i,l in enumerate(lessons):
 extra=''
 if l['analogy']:extra+=f'<aside class="analogy"><b>Une image pour comprendre</b><p>{esc(l["analogy"])}</p></aside>'
 if l['limit']:extra+=f'<aside class="limit"><b>La limite à garder en tête</b><p>{esc(l["limit"])}</p></aside>'
 if l['deep']:extra+=f'<details class="deeper"><summary>Aller plus loin, sans sauter d’étape</summary><p>{esc(l["deep"])}</p></details>'
 if l['quiz']:extra+=quiz_html(l['quiz'],i)
 sources=' · '.join(f'<a href="{esc(refs[r][1])}" target="_blank" rel="noopener">{r} · {esc(refs[r][0])}</a>' for r in l['source'])
 special=special_diagram(i)
 drawing,caption=special if special else (diagram(l['flow'],i),'Lire les blocs de gauche à droite. Les flèches indiquent le chemin de l’explication, pas une durée mesurée.')
 articles.append(f'<article class="lesson" id="etape-{i+1}" data-chapter="{l["ch"]}" aria-labelledby="title-{i}"><div class="eyebrow">CHAPITRE {l["ch"]+1} · {esc(chapters[l["ch"]])} · ÉTAPE {i+1}</div><h1 id="title-{i}">{esc(l["title"])}</h1><p class="lead">{esc(l["lead"])}</p><figure>{drawing}<figcaption>{esc(caption)}</figcaption></figure><ol class="steps">'+''.join(f'<li><span>{j+1:02}</span><p>{esc(s)}</p></li>' for j,s in enumerate(l['steps']))+'</ol>'+widget(l['widget'])+extra+(f'<p class="sources">Pour vérifier : {sources}</p>' if sources else '')+f'<footer>Roland Cédric TAYO · INEM <span>{i+1} / {len(lessons)}</span></footer></article>')

appendix='<section class="appendix" id="glossaire"><div class="eyebrow">RESSOURCE · LES MOTS UTILES</div><h1>Le petit dictionnaire</h1><p>Revenez ici dès qu’un mot vous arrête.</p><dl>'+''.join(f'<dt>{esc(k)}</dt><dd>{esc(v)}</dd>' for k,v in glossary.items())+'</dl></section>'
appendix+='<section class="appendix" id="sources"><div class="eyebrow">RESSOURCE · SOURCES ET PROVENANCE</div><h1>Pour vérifier et continuer</h1><p>Texte et schémas originaux. Références primaires et supports institutionnels consultés pour cette édition du 16 novembre 2026. Les exemples numériques sont des calculs pédagogiques, sauf indication contraire. Aucun résultat matériel original n’est annoncé.</p><ol class="references">'+''.join(f'<li id="{r}"><b>{r} · {esc(v[0])}</b><p>{esc(v[2])}</p><a href="{esc(v[1])}">{esc(v[1])}</a></li>' for r,v in refs.items())+'</ol><p>Les ressources ne sont pas copiées intégralement. Les liens officiels peuvent évoluer. Le glossaire Aidge est cité comme complément ; le téléchargement via le navigateur de recherche n’a pas été disponible lors de cette préparation.</p></section>'
css='''
:root{--ink:#17323e;--muted:#536976;--paper:#f6f4ed;--blue:#246b82;--mint:#d8eee6;--amber:#f5e4ba;--line:#ccd8d8}*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font-family:Segoe UI,Arial,sans-serif;font-size:18px;line-height:1.55}button,input,select{font:inherit}button,select{cursor:pointer}button{border:1px solid #b0c8ca;background:white;color:var(--ink);border-radius:9px;padding:.58rem .95rem}button:hover{background:var(--mint)}button:focus-visible,a:focus-visible,input:focus-visible,select:focus-visible{outline:3px solid #cf701f;outline-offset:3px}button:disabled{opacity:.4;cursor:default}a{color:#175b77;text-underline-offset:3px}header{position:sticky;top:0;background:#153240;color:white;z-index:10;padding:12px 24px;display:flex;gap:15px;align-items:center;flex-wrap:wrap;border-bottom:4px solid #7dc7b4}header strong{font-size:16px;letter-spacing:.04em;margin-right:auto}header a{color:white;font-size:14px}header button,header select{font-size:14px;background:#234856;color:white;border-color:#567781}#progress{height:4px;background:#d6e3e2}#bar{height:100%;background:#d79442;transition:width .3s}main{max-width:1150px;margin:35px auto;padding:0 20px 80px}.lesson,.appendix{background:#fffefd;padding:46px 60px;border:1px solid #dbe0db;border-radius:18px;box-shadow:0 10px 40px #15324009;margin-bottom:32px;animation:appear .35s ease-out}.lesson[hidden],.appendix[hidden]{display:none}.eyebrow{font-size:12px;font-weight:750;letter-spacing:.14em;color:#266875;text-transform:uppercase}h1{font-size:clamp(29px,3.6vw,46px);line-height:1.14;letter-spacing:-.025em;max-width:920px;margin:16px 0}h3{font-size:20px;margin:0 0 12px}.lead{font-size:22px;color:#47636b;max-width:860px;margin:18px 0 22px}figure{margin:22px 0 28px;padding:15px 10px 8px;border-radius:14px;background:#f5f8f7;border:1px solid #e0e9e5}svg{width:100%;height:auto;display:block}svg .node{stroke:#648c98;stroke-width:1.3}.n0{fill:#d8eaf2}.n1{fill:#dcefe6}.n2{fill:#fae7c7}svg text{font-family:Segoe UI,Arial,sans-serif;font-size:19px;fill:#163544;font-weight:600}.arrow{fill:none;stroke:#56747c;stroke-width:2}figcaption{font-size:11px;color:#596d76;padding:0 10px 5px}.steps{padding:0;list-style:none;margin:22px 0}.steps li{display:flex;gap:18px;align-items:flex-start;padding:12px 0;border-bottom:1px solid #e7ecea}.steps li>span{flex:none;font-size:12px;font-weight:750;color:#277c80;background:#e8f2ef;padding:7px;border-radius:8px}.steps li p{margin:0}.analogy,.limit{padding:17px 20px;border-radius:10px;margin-top:17px}.analogy{background:#e7f2ee;border-left:4px solid #4e9e8c}.limit{background:#fcf1dc;border-left:4px solid #d69843}aside b{font-size:14px}aside p{margin:6px 0 0;font-size:16px}.deeper{margin-top:19px;border:1px solid #cadbdc;border-radius:10px;padding:14px 18px;font-size:16px}summary{cursor:pointer;font-weight:650}.deeper p{margin-bottom:0}.sources{font-size:12px;line-height:1.7;margin-top:25px}footer{display:flex;justify-content:space-between;border-top:1px solid #d6e1df;margin-top:25px;padding-top:12px;font-size:12px;color:#5a7479}.quiz{padding:22px;background:#eef3fa;margin-top:22px;border-radius:12px}.quiz p{margin:8px 0 16px}.options{display:flex;gap:10px;flex-wrap:wrap}.options button{font-size:16px;text-align:left}.options .correct{background:#cce8d5;border-color:#34724a}.options .wrong{background:#fbe2ce;border-color:#aa653a}.feedback{border-left:3px solid #337d6d;padding:8px 16px;font-size:16px}.print-answer{font-size:14px;margin-top:15px}.lab{padding:22px;border:1px solid #bdd7dc;background:#f0f8f8;border-radius:12px;margin:24px 0}.lab label{display:inline-flex;align-items:center;gap:10px;margin:8px 20px 8px 0;font-size:16px}.lab input[type=number]{width:135px}.lab input[type=text],#token-input{max-width:100%}.lab p{font-size:14px}.lab output{display:block;font-family:Consolas,monospace;background:#163a48;color:#e6fff4;padding:15px;border-radius:8px;margin:15px 0;font-size:16px;white-space:pre-line}.cells{display:flex;gap:8px;flex-wrap:wrap;margin:15px 0}.cell{padding:9px 12px;border:1px solid #c2d8d8;background:white;border-radius:7px;font-size:16px}.cell b{display:block}.cell.active{background:#f6dca8;border-color:#bb8027}.cell small{display:block;color:#526b75}.references li{padding:12px 0;font-size:15px;break-inside:avoid}.references a{overflow-wrap:anywhere;font-size:12px}.references p{margin:5px 0}.appendix dl{font-size:16px}.appendix dt{font-weight:750;margin-top:16px}.appendix dd{margin:5px 0}.bottom{position:fixed;bottom:0;left:0;right:0;padding:10px 25px;background:#f4f7f5f5;border-top:1px solid #c4d4d2;display:flex;justify-content:center;gap:18px;align-items:center;z-index:9}.bottom span{font-size:14px;min-width:85px;text-align:center}.hint{font-size:13px;color:#567177;margin:0 auto 22px;max-width:1050px}.reading .lesson{animation:none}.reading .bottom{position:static}#outline{max-width:265px}.noscript{padding:20px;background:#ffe7b1}.print-only{display:none}@keyframes appear{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:none}}@media(prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important;scroll-behavior:auto!important}}@media(max-width:700px){header{padding:10px 12px;gap:8px}header strong{width:100%}header a{display:none}#outline{max-width:210px;font-size:12px}main{padding:0 10px 80px;margin-top:16px}.lesson,.appendix{padding:25px 21px;border-radius:12px}.lead{font-size:19px}body{font-size:17px}figure{overflow:auto}figure svg{min-width:560px}.steps li{gap:10px}.bottom{gap:8px;padding:8px}.bottom button{font-size:14px}.lab label{display:flex;flex-wrap:wrap}.lab button{font-size:14px}}@media print{@page{size:A4;margin:17mm 16mm 17mm}body{background:white;font-size:10.5pt;color:#172f3b;line-height:1.43}header,#progress,.bottom,.hint,.options,.lab button{display:none!important}main{margin:0;padding:0;max-width:none}.lesson,.appendix,.lesson[hidden],.appendix[hidden]{display:block!important;box-shadow:none;border:0;border-radius:0;margin:0;padding:0;break-before:page;animation:none}.lesson:first-child{break-before:auto}h1{font-size:25pt;margin:9pt 0 11pt}.lead{font-size:13pt;margin:10pt 0}.eyebrow{font-size:8pt}figure{margin:12pt 0;padding:8pt;break-inside:avoid}figure svg{width:100%;min-width:0}figcaption{font-size:7pt}.steps{margin:10pt 0}.steps li{padding:7pt 0;gap:10pt;break-inside:avoid}.steps li>span{font-size:8pt;padding:4pt}aside,.deeper,.lab,.quiz{break-inside:avoid}.analogy,.limit{padding:8pt 10pt;margin-top:9pt}aside b{font-size:9pt}aside p,.deeper,.lab p,.quiz p{font-size:9.5pt}.deeper{padding:8pt 10pt;margin-top:9pt}.sources{font-size:7.5pt;margin-top:12pt}footer{font-size:8pt;padding-top:7pt;margin-top:12pt}.lab{padding:9pt;margin:12pt 0}.lab h3,.quiz h3{font-size:11pt}.lab label{font-size:9pt}.lab output{font-size:9pt;padding:8pt;background:#e8f1f1;color:#17323e}.lab input[type=range]{display:none}.quiz{padding:10pt;margin-top:10pt}.print-answer{font-size:9pt}details>*{display:block!important}summary{display:block}.print-only{display:block}.cell{font-size:9pt;padding:5pt}.references li{font-size:10pt}.references a{font-size:8pt}.appendix dl{font-size:10pt}a{color:#17556b}figure,aside,li,details{page-break-inside:avoid}}
'''
js='''
(()=>{'use strict';
const $=s=>document.querySelector(s),$$=s=>[...document.querySelectorAll(s)],lessons=$$('.lesson'),appendices=$$('.appendix');let pos=0,reading=false;
const select=$('#outline');lessons.forEach((s,i)=>{let o=document.createElement('option');o.value=i;o.textContent=(i+1)+'. '+s.querySelector('h1').textContent;select.append(o)});
function show(n,scroll=true){pos=Math.max(0,Math.min(lessons.length-1,n));lessons.forEach((s,i)=>s.hidden=!reading&&i!==pos);appendices.forEach(s=>s.hidden=!reading);$('#counter').textContent=(pos+1)+' / '+lessons.length;$('#prev').disabled=pos===0;$('#next').disabled=pos===lessons.length-1;$('#bar').style.width=((pos+1)/lessons.length*100)+'%';select.value=pos;$('#mode').textContent=reading?'Mode présentation':'Tout lire';document.body.classList.toggle('reading',reading);history.replaceState(null,'','#etape-'+(pos+1));if(scroll)window.scrollTo({top:0,behavior:'instant'})}
$('#prev').onclick=()=>show(pos-1);$('#next').onclick=()=>show(pos+1);select.onchange=()=>show(Number(select.value));$('#mode').onclick=()=>{reading=!reading;show(pos)};
document.addEventListener('keydown',e=>{if(e.target.closest('input,select,textarea,button,summary'))return;if(e.key==='ArrowRight'){e.preventDefault();show(pos+1)}if(e.key==='ArrowLeft'){e.preventDefault();show(pos-1)}});
$('#fullscreen').onclick=async()=>{try{if(document.fullscreenElement)await document.exitFullscreen();else await document.documentElement.requestFullscreen()}catch(e){$('#notice').textContent='Plein écran indisponible dans ce navigateur. La lecture reste accessible.'}};
$('#glossary-link').onclick=e=>{e.preventDefault();reading=true;show(pos,false);$('#glossaire').scrollIntoView()};$('#source-link').onclick=e=>{e.preventDefault();reading=true;show(pos,false);$('#sources').scrollIntoView()};
$$('.quiz').forEach(q=>{q.querySelectorAll('[data-answer]').forEach(b=>b.onclick=()=>{q.querySelectorAll('button').forEach(x=>x.classList.remove('correct','wrong'));const ok=Number(b.dataset.answer)===Number(q.dataset.correct);b.classList.add(ok?'correct':'wrong');const f=q.querySelector('.feedback');f.hidden=false;f.textContent=(ok?'Oui. ':'À revoir. ')+f.dataset.original});q.querySelector('.feedback').dataset.original=q.querySelector('.feedback').textContent});
const fmt=n=>Number(n).toLocaleString('fr-FR',{maximumFractionDigits:5});
function neuron(){let a=Number($('#x1').value),b=Number($('#x2').value),z=.2*a-.1*b-.5;$('#neuron-out').textContent=`x₁ = ${fmt(a)} ; x₂ = ${fmt(b)}\nz = 0,2 × ${fmt(a)} − 0,1 × ${fmt(b)} − 0,5 = ${fmt(z)}\nClasse au seuil zéro : ${z>=0?1:0} ; ReLU(z) = ${fmt(Math.max(0,z))}`}
$('#x1').oninput=$('#x2').oninput=neuron;neuron();
let w=.2,bias=0,updates=0;function grad(){const yhat=w+bias,loss=.5*(yhat-1)**2;$('#gradient-out').textContent=`Corrections : ${updates}\nw = ${fmt(w)} ; b = ${fmt(bias)}\nŷ = ${fmt(yhat)} ; L = ${fmt(loss)}`;return{yhat,loss}}
$('#gradient-step').onclick=()=>{const before=grad(),g=before.yhat-1;w-=.1*g;bias-=.1*g;updates++;const after=grad();$('#gradient-log').textContent=`Avant : L = ${fmt(before.loss)} ; gradient de chaque paramètre = ${fmt(g)}. Après : L = ${fmt(after.loss)}.`};$('#gradient-reset').onclick=()=>{w=.2;bias=0;updates=0;$('#gradient-log').textContent='';grad()};grad();
let cp=0;function conv(){const v=[1,2,0,3,1];$('#conv-out').textContent=`Position ${cp+1} : ${v[cp]} × 1 + ${v[cp+1]} × (−1) = ${v[cp]-v[cp+1]}\nToutes les sorties : [−1, 2, −3, 2]`;$('#conv-cells').replaceChildren(...v.map((v,i)=>cell(String(v),i===cp||i===cp+1?'Fenêtre active':'',i===cp||i===cp+1)))}function cell(value,sub='',active=false){const d=document.createElement('div');d.className='cell'+(active?' active':'');let v=document.createElement('b');v.textContent=value;d.append(v);if(sub){let s=document.createElement('small');s.textContent=sub;d.append(s)}return d}$('#conv-next').onclick=()=>{cp=(cp+1)%4;conv()};conv();
const tokenTable=['[INCONNU]',...Array.from(new Set(Array.from(' abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789éèêëàâäîïôöùûüçÉÈÊÀÇ.,!?;:’\"-')))]
function tokens(){const chars=Array.from($('#token-input').value),id=c=>Math.max(0,tokenTable.indexOf(c));$('#token-cells').replaceChildren(...chars.map(c=>cell(c===' '?'espace':c,'ID '+id(c)+(id(c)===0?' · inconnu':''))));$('#token-vocab').textContent=`${chars.length} tokens ; table fixe de ${tokenTable.length} entrées. Identifiants utilisés : `+[...new Set(chars)].map(c=>id(c)+' = '+(c===' '?'espace':c)).join(' ; ')}$('#token-input').oninput=tokens;tokens();
function memory(){const n=Number($('#parameter-count').value),b=Number($('#memory-bits').value);if(!Number.isFinite(n)||n<1||!Number.isInteger(n)){$('#memory-out').textContent='Choisir un nombre entier positif de paramètres.';return}const bytes=Math.ceil(n*b/8);$('#memory-out').textContent=`${fmt(n)} × ${b} / 8 → ${fmt(bytes)} octets\n${fmt(bytes/1000)} kB ; ${fmt(bytes/1024)} KiB\nBudget des paramètres uniquement.`}$('#parameter-count').oninput=$('#memory-bits').onchange=memory;memory();
function quant(){const bits=Number($('#quant-bits').value),Q=2**(bits-1)-1,s=1/Q,v=[-1,-.3,.1,.7],vals=v.map(w=>{let q=Math.min(Q,Math.max(-Q,Math.round(w/s)));return{w,q,hat:q*s}});$('#quant-cells').replaceChildren(...vals.map(o=>cell(fmt(o.w)+' → '+fmt(o.hat),'q = '+o.q)));$('#quant-out').textContent=`${bits} bits ; Q = ${Q} ; s = ${fmt(s)}\nErreur absolue moyenne = ${fmt(vals.reduce((a,o)=>a+Math.abs(o.hat-o.w),0)/v.length)}`};$('#quant-bits').onchange=quant;quant();
function pareto(){let quality=Number($('#quality-min').value),latency=Number($('#latency-max').value),p=[['A',92,20,100],['B',90,10,70],['C',89,18,100]],ok=p.filter(x=>x[1]>=quality&&x[2]<=latency);$('#pareto-out').textContent=`Contraintes : qualité ≥ ${quality} % et latence ≤ ${latency} ms\nAdmissibles : ${ok.map(x=>x[0]).join(', ')||'aucune'}\nJeu fictif : aucune mesure de modèle réel.`;$('#pareto-points').replaceChildren(...p.map(x=>cell(x[0],`${x[1]} % · ${x[2]} ms · ${x[3]} kB`,ok.includes(x))));const ns='http://www.w3.org/2000/svg';$('#pareto-dots').replaceChildren(...p.map(x=>{let g=document.createElementNS(ns,'g'),c=document.createElementNS(ns,'circle'),t=document.createElementNS(ns,'text');c.setAttribute('cx',60+(x[2]-5)*25);c.setAttribute('cy',190-(x[1]-85)*16);c.setAttribute('r','8');c.setAttribute('fill',ok.includes(x)?'#287e6b':'#bb6c48');t.setAttribute('x',73+(x[2]-5)*25);t.setAttribute('y',195-(x[1]-85)*16);t.textContent=x[0];g.append(c,t);return g}));const yy=190-(quality-85)*16,xx=60+(latency-5)*25;$('#quality-line').setAttribute('d',`M60 ${yy}H560`);$('#latency-line').setAttribute('d',`M${xx} 25V190`)}$('#quality-min').oninput=$('#latency-max').oninput=pareto;pareto();
window.Course={show,get position(){return pos},get total(){return lessons.length},readAll(){reading=true;show(pos)},ready:true};
const initial=Number(location.hash.replace('#etape-',''))-1;show(Number.isFinite(initial)&&initial>=0?initial:0,false);
})();
'''
css+='''header button:hover{background:#d8eee6;color:var(--ink)}@media print{@page{margin:14mm 15mm}body{font-size:9.6pt;line-height:1.36}h1{font-size:23pt;margin:7pt 0 9pt}.lead{font-size:12pt;margin:8pt 0}figure{margin:9pt 0;padding:6pt}figure svg{max-height:118px}#etape-38 figure svg{max-height:70px}#etape-42 figure{display:none}#pareto-chart{max-height:130px}.steps li{padding:6pt 0}.steps{margin:8pt 0}.analogy,.limit{padding:7pt 9pt;margin-top:7pt}.deeper{padding:7pt 9pt;margin-top:7pt}aside p,.deeper,.lab p,.quiz p{font-size:9pt}.sources{margin-top:9pt;font-size:7pt}footer{margin-top:9pt;break-before:avoid}.lab{margin:9pt 0;padding:8pt}.lab output{margin:8pt 0;padding:7pt}.quiz{margin-top:8pt;padding:8pt}.references li{padding:8pt 0}}'''
page='<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="Comprendre l’intelligence artificielle embarquée, du premier neurone aux mesures sur une petite machine. Cours progressif illustré."><title>L’IA dans les objets · Roland Cédric TAYO</title><style>'+css+'</style></head><body><header><strong>RCT / L’IA DANS LES OBJETS</strong><select id="outline" aria-label="Choisir une étape"></select><button id="mode">Tout lire</button><button id="fullscreen">Plein écran</button><a href="cours-ia-embarquee.pdf">Le PDF</a><a href="#glossaire" id="glossary-link">Les mots</a><a href="#sources" id="source-link">Les sources</a></header><div id="progress" aria-hidden="true"><div id="bar"></div></div><noscript><p class="noscript">JavaScript est désactivé. Toutes les étapes restent lisibles. Les calculateurs nécessitent JavaScript.</p></noscript><main><p class="hint" id="notice">Un besoin, une explication, un schéma, puis un essai. Flèches ← → pour avancer. « Tout lire » pour le parcours continu.</p>'+''.join(articles)+appendix+'</main><nav class="bottom" aria-label="Navigation du cours"><button id="prev">← Étape précédente</button><span id="counter" aria-live="polite"></span><button id="next">Étape suivante →</button></nav><script>'+js+'</script></body></html>'
(ROOT/'index.html').write_text(page,encoding='utf-8')
(ROOT/'cours-source.json').write_text(json.dumps({'author':'Roland Cédric TAYO','date':'2026-11-16','chapters':chapters,'lessons':lessons,'references':refs,'glossary':glossary},ensure_ascii=False,indent=2),encoding='utf-8')
print(f'{len(lessons)} étapes écrites ; HTML autonome : {len(page.encode("utf-8")):,} octets')
