# Jour 1 — du perceptron à MNIST

Roland Cédric TAYO · INEM. Supports étudiants, sans correction du réseau.

1. Lire `perceptron.pdf` et remplir les prévisions dans `fiches.pdf`.
2. Créer le dépôt GitHub du groupe ; inviter `rolln7drktayau`.
3. Installer Python 3 ; pour C, GCC et Make sous Linux/WSL ou sur Raspberry Pi.
4. Télécharger/vérifier MNIST avec `python3 fetch_mnist.py data/mnist` (source CVDF), puis lancer `python3 -m unittest discover -s tests -v` (Windows : `py -3`).
5. Écrire les fonctions du modèle et les tests manquants dans `src/` et `tests/`.

## Ce qui est fourni

- `patterns/` : dix motifs distincts, 8 lignes × 6 pixels, puis le label.
- `noise.csv` : les mêmes copies pour toutes les méthodes ; graine du bruit 2026.
- `tools.py` : validation des motifs et IDX, bruit déterministe, lecture des poids.
- `gradient_check.py` : différences finies ; fournir VOTRE perte et VOS gradients.
- `debug_update.py` : exercice volontairement incorrect ; expliquer le défaut par un test.
- `toy_case.json` : cas 2→2→2 ; ordre exact des 12 paramètres.
- `weights/seed42.bin`, `seed43.bin`, `seed44.bin` : poids de secours appris sur 5 000 images.
- `golden.json` : trois entrées de validation par graine et sorties C de référence.
- `SHA256SUMS.json` : empreintes des ressources.
- `ci-template.yml` et `.github/workflows/ci.yml` : squelette à compléter avec les tests de votre modèle.

## MNIST

Télécharger les quatre fichiers depuis le [miroir CVDF](https://github.com/cvdfoundation/mnist), puis les décompresser. Les données MNIST complètes ne sont pas incluses dans ce ZIP. `fetch_mnist.py` télécharge, décompresse et vérifie les empreintes du fichier `MNIST-SHA256.json`.

Dans Python, `tools.check_mnist("data/mnist")` doit valider les quatre en-têtes, dimensions, tailles et labels. Garder les SHA-256 renvoyés.

Apprentissage : images train 0–4 999. Validation : 5 000–5 999. Test officiel : les 10 000 images `t10k`, après gel des choix. Ne pas régler un modèle sur le test.

## Poids de secours

Format binaire : 8 octets ASCII `INEMMLP1`, puis trois entiers uint32 little-endian (784,100,10), puis 79 510 float32 IEEE-754 little-endian. Taille totale : 318 060 octets. Ordre : W1 par lignes (78 400), b1 (100), W2 par lignes (1 000), b2 (10).

`tools.read_weights(path)` valide et lit ce format, sans fournir l’inférence. Écrire votre prédiction. Sur les cas de `golden.json`, vérifier chaque sortie : `abs(votre_sortie-reference) <= 1e-5 + 1e-4*abs(reference)`. Sauvegarder puis relire doit conserver les valeurs ; ne pas changer la tolérance pour faire passer un test.

Ces secours sont destinés au bloc mémoire/quantification si l’apprentissage n’est pas terminé. Signaler leur utilisation ; ce n’est pas votre entraînement. Les trois graines désignent l’initialisation et l’ordre des exemples, pas trois jeux de test différents.

## Bruit MNIST commun

`tools.mnist_noisy_pixels("data/mnist/t10k-images-idx3-ubyte", seed=2026)` renvoie les pixels bruités sans en-tête : exactement 78 indices distincts par image sont inversés (`pixel <- 255-pixel`). La même image reçoit le même masque pour chaque précision et chaque modèle. Ne pas mélanger ce bruit avec l’inversion binaire des motifs 8×6.

## Versionnement et remise

Jalons conseillés : `day1-data`, `day1-core`, `day1-trained`, `day1-quantization`, `day1-submission`. Un changement cohérent par commit, par exemple `feat(data): validate IDX headers`, `test(gradient): check output biases`, `exp(quant): compare global and layer scales`. Pousser les branches et tags ; relire à plusieurs.

Rendre code commenté, tests, configuration, graines, hypothèse datée avant les mesures, poids ou leur provenance, CSV bruts, figures, manifeste et bilan individuel. Anglais conseillé pour code et commentaires. Déclarer les aides d’IA et montrer une sortie corrigée avec une preuve. Une CI qui ne teste que les données ne valide pas encore le réseau.

Ce bloc mesure un PC. Aucune énergie ou performance de Raspberry Pi/microcontrôleur n’est fournie. Le projet suivant exige les mesures sur le vrai Pi.

Si vous choisissez C pour une étape, adapter la cible correspondante du Makefile pour compiler et exécuter vos sources. Le Makefile fourni ne prétend pas contenir des scripts de modèle déjà écrits.

Outils : [Python](https://www.python.org/downloads/), [Git](https://git-scm.com/downloads/), [GCC](https://gcc.gnu.org/), [Make](https://www.gnu.org/software/make/). Un éditeur et un terminal suffisent ; aucun environnement de modèle préinstallé n’est fourni.
