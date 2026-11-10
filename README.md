# Miam Ride

Application de vélo de route : boucles calmes, pauses en boulangerie, avantages chez les commerçants partenaires, carte de fidélité par QR code, progression (XP, garage de vélos) et abonnement boulangerie.

> État : **maquettes** (HTML autonomes, données fictives). Aucune vraie connexion, aucun vrai compte, aucun appel à un service externe sauf pour la version « test OSM ».

## Ouvrir les maquettes
Chaque fichier de `maquettes/` est une page HTML autonome : double-clic dans Chrome ou Safari.

| Fichier | Contenu |
|---|---|
| `accueil.html` | L'appli côté cycliste (accueil, carte, historique, enregistrement, fidélité, profil). Style « Pop ». |
| `introduction.html` | Idem avec l'écran d'introduction. |
| `accueil-osm.html` | Même appli avec une vraie carte (MapLibre). |
| `test-osm-reel.html` | Test avec de vraies données OpenStreetMap : tracé vélo (OpenRouteService), boulangeries (Overpass), adresse (Base Adresse Nationale). Demande une clé OpenRouteService gratuite, à saisir dans Profil › Compte › Test OSM. À ouvrir **en local** (pas en page hébergée). |
| `osm-vers-12.html` à `osm-vers-29.html` | **Versions de travail OSM** (la dernière, `osm-vers-29.html`, est la version courante) : tracé réel, boulangeries, « Vers un lieu », GPX, Ride and train. Voir `docs/osm-versions-12-22.md` et `docs/test-osm.md`. Clé OpenRouteService à coller dans le bandeau de l'accueil, à chaque fichier. |
| `espace-boulangerie.html` | L'espace commerçant. |
| `inscription-boulangerie-v1.html`, `inscription-boulangerie-v2-menus.html` | Deux versions du parcours d'inscription d'une boulangerie. |
| `styles-alternatifs.html` | Comparaison des 6 styles graphiques (gelés : on reste sur « Pop »). |

Mode présentation : ajouter `#demo` à l'adresse pour afficher les outils de simulation (heure, avance rapide…) ; `#nodemo` pour les masquer.

## Documentation (`docs/`)
`etat-du-projet.md` (point d'étape), `osm-versions-12-22.md` (versions OSM 12 à 29), `ride-and-train.md`, `questions-juridiques-notation.md`, `feuille-de-route-communaute.md`, `integration-google.md`, `test-osm.md` (mode d'emploi du test OSM), `modele-economique.md`, `criteres-generation-traces.md`, `horaires-et-roulage.md`, `notation-produits.md`, `synchro-sorties-montre-gps.md`, `garage-50-velos.md`, `styles-alternatifs.md`, `feuille-de-route.html`.

## Outils (`outils/`)
- `build_styles.py` : génère la page des styles alternatifs.
- `build_osm_reel.py` : génère `test-osm-reel.html` à partir de `accueil-osm.html`.
- `tests/` : scripts Playwright (parcours complet `e2e.py`, test OSM `t_osm.py`, etc.).
- `patchs/` : scripts de modification successifs (historique de construction).

Les scripts ont été écrits dans un environnement où les fichiers sont dans `/mnt/user-data/outputs` et `/home/claude/p` : adapter les chemins en haut de chaque script pour les relancer.

## Archives
`archives/test-osm-versions/` : versions 2 à 10 du fichier de test OSM (la 10 est la dernière).

## Décisions en vigueur
- Style graphique : **Pop** uniquement.
- Cible : tout sur Google (Places, Routes, Maps) une fois la clé et la facturation en place ; clés côté serveur.
- Prochain gros chantier : vraie connexion (Supabase), CGU, données personnelles / RGPD.
- Toutes les données (boulangeries, avis, partenaires) sont inventées dans les maquettes.
