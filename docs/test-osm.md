# Version OSM de test (fichiers « Miam ride osm - vers N.html »)

**Version actuelle : vers 29** (`Miam ride osm - vers 29.html`, copie dans le dépôt GitHub `alanbtl/Miam-ride`, dossier `maquettes/`). Les maquettes d'origine sont intactes. Le détail de chaque version est dans `osm-versions-12-22.md`. Depuis la version 12, **OSM est actif par défaut** dès qu'une clé est présente.

## Étapes
1. Créer un compte gratuit sur openrouteservice.org (e-mail personnel), puis Dashboard › « Request a token » › type « Free », nommer la clé et la copier. Ne jamais la coller dans une conversation ou dans le code.
2. Ouvrir le fichier `Miam ride osm - vers N.html` dans Chrome ou Safari (double-clic). Il doit être ouvert en fichier local, pas en artifact (appels externes bloqués).
3bis. (Ride and train) Profil › Compte › « Horaires de trains » : adresse de la fonction Supabase + clé anon (voir `serveur/README.md`). Bouton « Tester ».
3. **Coller la clé dans le bandeau jaune de l'accueil** (« Mode démo… »), puis « Activer ». Elle est enregistrée dans le navigateur, **fichier par fichier** : à refaire à chaque nouvelle version tant que l'appli n'est pas hébergée à une adresse fixe. Autre endroit : Profil › Compte.
4. Départ : taper une adresse (suggestions) ou « Me localiser » (peut échouer sur un fichier local : taper l'adresse). Par défaut : rue de la Paroisse, Versailles.
5. Choisir le mode (Boucle, Vers un lieu, Ride and train, Laisse Mamie choisir), l'ambiance et la distance, puis générer.
6. Choisir les boulangeries, puis le résumé : télécharger le GPX.

## Ce qui est réel / simulé
- **Réel** : tracé vélo (OpenRouteService, profil cycling-road), distance, dénivelé, % de routes calmes (type de voie), boulangeries OpenStreetMap (nom, adresse, horaires quand renseignés), gares OpenStreetMap, adresses (Base Adresse Nationale + Photon), GPX.
- **Simulé / absent** : notes, avis, photos, partenaires, récompenses (données de démonstration). Les horaires de trains (Île-de-France) viennent de PRIM via Supabase, à partir de la vers 24.

## Limites connues
- Les tests automatiques utilisent des réponses simulées ; le premier vrai test des fonctions récentes est à faire sur l'appareil de l'utilisateur.
- Quotas gratuits ORS à vérifier (≈ 40 requêtes/minute, ≈ 2 000/jour). Une génération consomme 5 à 8 appels (3 boucles candidates + recalcul) : le quota du jour peut être atteint rapidement en test.
- Overpass : service public partagé, usage de test uniquement ; cinq miroirs en course, cache de 24 h dans le navigateur. Horaires et étiquetage OSM incomplets (pâtisseries, boulangeries absentes).
- Pour la production : serveur à nous (clé ORS hors de la page), base de boulangeries à nous, hébergement fixe.

## Questions à trancher après les tests
- Les boucles sont-elles roulables et calmes autour de Versailles / vallée de Chevreuse ? L'ambiance est-elle bien respectée ?
- Les boulangeries proposées sont-elles pertinentes (ligne de contrôle sous le tracé : nombre à chaque étape) ?
- Le GPX s'ouvre-t-il bien sur une Coros / un GPS (trace, pauses, altitude) ?
- Les gares proposées pour Ride and train sont-elles justes ?

## Historique des versions
- **Vers 10-11 (nov.)** : 5 serveurs Overpass en course, cache 24 h, préchauffage des boulangeries, tracé coloré (noir = voie calme, rouge = route principale), détail des voies cyclables, routes principales et chemins non revêtus, horaires OSM mieux lus.
- **Vers 12 à 29 (nov.)** : voir `osm-versions-12-22.md`.
- Le suivi de version se fait dans GitHub (`alanbtl/Miam-ride`).
