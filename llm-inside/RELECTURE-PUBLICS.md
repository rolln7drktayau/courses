# Relecture selon trois publics

Roland Cédric TAYO · INEM · 12 novembre 2026.

Une simulation critique par un agent distinct a examiné le support comme ingénieur embarqué, novice et lecteur RH. Cette simulation ne constitue pas une évaluation menée avec de vrais lecteurs.

## Diagnostic initial retenu

Les trois profils repéraient une surcharge du parcours principal : définir les mots ne suffisait pas à justifier l’introduction simultanée de nombreuses formules. Les ingénieurs demandaient un budget mémoire complet et des décisions concrètes ; les deux autres profils perdaient le fil à l’attention formelle et aux familles de recherche.

Le PDF public de départ était bien à jour : ses octets correspondaient au fichier local de 23 pages. Les critiques de contenu ne provenaient donc pas simplement d’un ancien PDF. Certains espacements de mots lors de l’extraction de texte ne correspondaient pas à des mots visuellement collés ; les images et la mise en page ont été contrôlées séparément.

## Décisions

- **Découverte :** 15 scènes essentielles, puis trois pages de sources. Les formules avancées et les noms de familles de recherche ne sont pas requis pour comprendre le fil.
- **Ingénieur :** parcours complet de 30 pages, avec formules, architectures, limites et sources. Le bouton change aussi le lien vers le PDF correspondant.
- **Mémoire totale :** paramètres + cache + autres valeurs et logiciels. L’hypothèse pédagogique de 1 Go pour les autres besoins est visible ; elle n’est pas une mesure.
- **Coûts :** les chiffres de la machine théorique sont explicitement fictifs. Prefill et decode présentent des tendances conditionnelles, pas des lois universelles.
- **Quantification :** distinguer réduction du fichier, données effectivement transférées, calcul après reconstruction et apprentissage adapté à la basse précision.
- **Hachage de proximité :** la question porte désormais sur un voisin pertinent non consulté. Regrouper des vecteurs proches dans un groupe est recherché.
- **Comparaison :** tableau et CSV explicitement fictifs. La durée couvre une entrée de 128 tokens puis une sortie de 20 tokens, modèle déjà chargé. La variante échoue au seuil de qualité malgré sa vitesse.
- **Pi :** leviers concrets et protocole lié ; aucune mesure de LLM sur carte revendiquée.

## Corrections finales après la seconde lecture

L’agent a demandé de retirer les notations et termes techniques restant dans la scène de quantification Découverte, de définir le périmètre des durées du tableau et de corriger un titre dont le point d’interrogation passait seul à la ligne. Ces points ont été corrigés et les deux PDF régénérés. Une dernière relecture ciblée les a confirmés.

Les tests du support contrôlent les calculs, les deux parcours, les questions, les définitions, les changements de schéma, les liens, les tailles d’écran et les deux PDF. Ils ne prouvent pas que le public a appris ; une séance avec de vrais lecteurs reste la façon de vérifier cela.

## Renforcement : étapes et recherche sous contraintes

Après le retour sur l’illustration des embeddings, le bloc abstrait a été remplacé par des tokens, des identifiants fictifs, une table de vecteurs et une sortie sélectionnée. Les schémas ont trois états numérotés distincts ; un parcours en cinq parties les situe dans la démarche.

Le parcours Découverte reste à 15 scènes et 3 pages de sources. Les contraintes, les pistes par brique et la préparation d’une enquête remplacent des éléments moins prioritaires ; ces derniers restent dans le parcours Ingénieur, désormais de 33 pages. Une fiche d’hypothèse JSON est téléchargeable sans transmettre de données. Le critère pédagogique final est de savoir choisir un coût, expliquer une idée, annoncer un risque et préparer un test, pas seulement réciter des termes.

Une relecture ciblée par l’agent a confirmé la distinction des trois étapes, le fonctionnement du choix de token et la présence des contraintes mémoire, temps, énergie/chaleur, fiabilité et exploitation. Cela reste une simulation de lecture, pas un test auprès de vrais apprenants.
