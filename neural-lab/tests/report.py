"""Summarize measured artifacts and pin the delivered files. No new measurements."""
from pathlib import Path
import hashlib,json,subprocess
ROOT=Path(__file__).resolve().parents[1]
data=json.loads((ROOT/'validation/results.json').read_text(encoding='utf-8'))
browser=json.loads((ROOT/'validation/browser.json').read_text(encoding='utf-8'))
examples=json.loads((ROOT/'validation/examples.json').read_text(encoding='utf-8'))
lines=['# Validation du laboratoire','',
       'Roland Cédric TAYO · INEM','',
       'Ce document résume des exécutions conservées, pas des performances promises sur une carte.', '',
       f"Moteur : {len(data['tests'])} contrôles réussis. Parcours navigateur : {len(browser['checks'])} contrôles réussis.",'',
       f"Exécution du moteur : {data['executed_utc']} ; {data['runtime']} ; {data['machine']['cpu']} ; {data['machine']['platform']} {data['machine']['arch']}.",
       f"Exécution du navigateur : {browser['executed_utc']} ; Chrome {browser['browser']}. Rendu de test WebGL logiciel (SwiftShader). Charge système non maîtrisée.",'',
       '## Calculs et contrôles','',
       'Dérivées par différences finies, probabilités normalisées, perte différée jusqu’au bouton 2, correction dans le bon ou le mauvais sens, masque causal, cache K/V égal au calcul complet, initialisation et apprentissage reproductibles, arrondi float32 et import/export intègre.', '',
       'Le parcours navigateur vérifie aussi le chargement des trois modèles, la correction manuelle, les courbes, la génération avec cache, le zoom sur matrices et opérations, les survols 3D, les exports CSV, les réglages de campagne figés, la pause du mode lent, trois largeurs d’écran et le repli 2D sans WebGL. Aucune erreur JavaScript observée dans ce parcours. Ce n’est pas une étude auprès d’utilisateurs réels.','',
       '## Entraînement mesuré dans Node.js','',
       'Corpus répété d’Alice, η = 0,04, norme de gradient limitée à 1. Validation sur 48 fenêtres fixes, sans consultation du test réservé. Les durées ci-dessous couvrent les corrections ; les bilans avant/après sont mesurés séparément. Les courbes de la page portent sur 20 fenêtres ; les exemples livrés sur 48.','',
       '| Modèle | D / contexte | Graine | Corrections | Perte avant → après (nats) | Bonnes réponses avant → après | Durée (ms) |',
       '|---|---|---|---|---|---|---|']
for r in data['training']:
    a,b=r['before'],r['after']
    lines.append(f"| {r['type']} | {r['dim']} / {r['context']} | {r['seed']} | {r['updates']} | {a['loss']:.4f} → {b['loss']:.4f} | {a['accuracy']*100:.2f} % → {b['accuracy']*100:.2f} % | {r['elapsed_ms']:.2f} |")
lines += ['', 'La petite configuration Transformer D=4 améliore ici sa perte mais réduit son nombre de bonnes réponses. Ce résultat défavorable est conservé. Une perte et un taux de réussite n’évaluent pas la même chose.', '',
          '## Exemples entraînés livrés','',
          'Ils sont réellement générés par `tests/build_examples.mjs` sur le corpus public, avec 2 000 corrections et la graine 42. Leur intégrité est vérifiée au chargement. Les chiffres sur ce corpus répétitif ne sont pas une évaluation de compréhension linguistique.','',
          '| Modèle | Paramètres | Perte validation | Bonnes réponses (48 fenêtres) |',
          '|---|---|---|---|']
for r in examples['examples']:
    v=r['validation'];lines.append(f"| {r['type']} | {r['parameters']} | {v['validation_loss']:.4f} | {v['validation_accuracy']*100:.2f} % |")
lines += ['', '## Quantification et temps','',
          'Les fichiers `quantization.csv` et `results.json` conservent toutes les valeurs, dont les trois graines 42, 43 et 44 du Transformer par défaut. Les matrices sont arrondies puis réutilisées dans un calcul flottant. Les octets représentent un stockage idéal ; la RAM réelle du navigateur n’est pas mesurée.', '',
          'Les observations de chronométrage du navigateur sont dans `browser.json`, champ `timing` : échauffement, calibration K, cinq paires alternées, temps individuels et checksum. Elles concernent le moteur scalaire avec construction de la trace. La présence du moteur 3D et d’autres tâches peut perturber les temps. Aucun gain de vitesse industrielle n’est revendiqué.', '',
          '## Points restant à vérifier sur une cible réelle','',
          '- Portage vers un runtime adapté et, si nécessaire, des noyaux entiers réels.',
          '- Stockage effectif, pic de RAM, latence et variabilité sur le Raspberry Pi concerné.',
          '- Énergie avec un instrument approprié ; aucune valeur d’énergie n’est donnée ici.',
          '- Qualité sur des données indépendantes représentatives du besoin, et non sur ces phrases répétées.',
          '- Accessibilité avec des utilisateurs réels, autres navigateurs et appareils mobiles physiques.', '',
          '## Traçabilité','',
          'Les CSV, JSON et captures viennent des scripts de `tests/`. `manifest.json` fixe les empreintes SHA-256 des fichiers du laboratoire. Le commit qui contient le manifeste identifie la livraison. Les versions de Three.js et sa licence sont dans `vendor/`. Les exemples sont des démonstrations du laboratoire ; aucun corrigé privé des TD n’est repris.', '']
(ROOT/'validation/README.md').write_text('\n'.join(lines),encoding='utf-8')
# Keep delivered text bytes identical to GitHub's LF-normalized files.
for p in ROOT.rglob('*'):
    if p.is_file() and p.suffix in {'.js','.mjs','.css','.html','.json','.csv','.md','.py','.txt'}:
        raw=p.read_bytes()
        if b'\r\n' in raw:p.write_bytes(raw.replace(b'\r\n',b'\n'))
files={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(ROOT.rglob('*')) if p.is_file() and p.name!='manifest.json' and '__pycache__' not in p.parts}
base=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
(ROOT/'validation/manifest.json').write_text(json.dumps({'format':'inem-neural-lab-manifest/1','source_base_commit':base,'delivery_revision':'Git commit containing this manifest; file hashes pin this delivery','sha256':files},indent=2)+'\n',encoding='utf-8',newline='\n')
print(f'Report and {len(files)} file hashes written')
