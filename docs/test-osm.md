# Test avec de vraies données OpenStreetMap (version « osm-reel »)

Fichier : `miam-ride-osm-reel.html` (copie de la version OSM ; les maquettes d'origine sont intactes).
Principe : même mécanisme que la couche Google, avec OpenRouteService (tracé vélo) + Overpass (boulangeries) + Nominatim (adresse de départ).

## Étapes
1. Créer un compte gratuit sur openrouteservice.org (e-mail perso), puis Dashboard › Request a token › type « Free », nommer la clé, copier la clé.
2. Télécharger `miam-ride-osm-reel.html` et l'ouvrir dans Chrome ou Safari (double-clic). Il doit être ouvert en fichier local, pas en artifact (appels externes bloqués).
3. Profil › Compte › « Test OSM (vraies routes) » : coller la clé, passer sur « Activés », toucher « Tester la clé » → « OK : 1,9 km ».
4. Accueil : départ = « Me localiser » (autoriser la position) ou taper une adresse puis valider. Par défaut : Versailles.
5. Choisir la distance, puis « Je choisis où je me régale » : le tracé de boucle s'affiche sur la vraie carte, avec les vraies boulangeries autour.
6. Choisir une boulangerie : l'itinéraire final est recalculé avec la pause. La distance, le dénivelé et le % de routes calmes affichés viennent du tracé réel.

## Ce qui est réel / simulé
- Réel : tracé vélo (profil cycling-road, évite bacs et escaliers), distance, dénivelé, % de routes calmes (estimé d'après le type de voie ORS : rue, chemin, piste, voie cyclable = calme ; route nationale/départementale = non calme), boulangeries OSM (nom, adresse, horaires quand renseignés).
- Simulé / absent : notes, avis, photos, partenaires, récompenses. Le résumé du tracé et le profil altimétrique du résumé restent ceux de la maquette.

## Limites connues
- Écrit sans pouvoir appeler les vrais services depuis notre environnement (réseau bloqué) : testé avec des réponses simulées. Premier vrai test à faire.
- Quotas gratuits ORS à vérifier sur leur site (environ 40 requêtes/minute) ; ≈ 4 appels par tracé.
- Overpass : service public partagé, usage de test uniquement. Horaires OSM souvent incomplets.
- Nominatim : 1 requête/seconde maximum, usage de test uniquement.
- Pour la production : serveur à nous (clé ORS hors de la page), instance dédiée ou service payant, cache des boulangeries dans notre base.

## Questions à trancher après le test
- Les boucles sont-elles roulables et calmes autour de Versailles / vallée de Chevreuse ? Forme des boucles (cercle de points de passage) correcte ?
- Le % de routes calmes est-il cohérent avec ton ressenti ?
- Qualité des boulangeries et horaires OSM vs Google.

## Versions récentes (nov. 2026)
- Vers 10 : 5 serveurs Overpass en course, 3 tours, mémoire locale 24 h des boulangeries, nouvel essai automatique, message d'erreur visible.
- Vers 11 : préchauffage des boulangeries (chargées dès le départ connu), tracé affiché dès qu'il est calculé, tracé coloré (noir = voie calme, rouge = route principale), détail « voies cyclables / routes principales / chemins non revêtus », horaires OSM mieux lus (listes de jours, plages, Sa-Mo), doublons et commerces sans nom écartés.
- Le suivi de version se fait désormais dans GitHub (`alanbtl/Miam-ride`).
