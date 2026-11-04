# Styles alternatifs (mis de côté)

**Décision (01/11/2026)** : on reste sur le style **Pop** (jaune, noir, pêche, Poppins). Toutes les prochaines modifications ne s'appliquent qu'à Pop. Les autres styles sont **gelés** : ils ne suivront pas les évolutions de l'appli.

## Ce qui existe
Une page « Miam Ride – Styles » (artefact publié) regroupe six styles, mêmes fonctions : 1 Pop (identique à l'appli), 2 Sentier (vert, esprit Komoot), 3 Nuit (noir et orange, esprit Strava), 4 Chunky (vert vif, esprit Duolingo), 5 Affiche (papier, bleu nuit, rouge, slab), 6 Violette (aubergine et jaune, Syne, coins « feuille »).
Liens directs : `#pop`, `#sentier`, `#nuit`, `#chunky`, `#retro`, `#violet`.

## Comment c'est construit
Le script `styles-alternatifs-build.py` part du fichier de l'appli et remplace les couleurs, bordures, ombres, rayons et polices par des variables CSS, puis ajoute une couche par style. Pour reprendre un style plus tard, relancer le script sur la version à jour de l'appli.
