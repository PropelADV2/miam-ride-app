# Intégration Google (mise de côté le 04/11/2026 : on passe en full OSM)

> **Statut : abandonnée pour les tracés et les boulangeries.** Décision du 04/11/2026 : full OpenStreetMap. La décision du 31/10 « tout repose sur Google » est abrogée. Ce document est conservé pour mémoire et pour un éventuel usage ciblé (notes des boulangeries, sous réserve d'un avis juridique).

## Pourquoi on y renonce
- Le coût monte avec chaque requête. Estimation d'une génération « naïve » (3 itinéraires + 4 recherches de lieux + détails) : environ 0,20 à 0,25 $ par tracé. Trop risqué pour le modèle économique (appli gratuite pour les cyclistes, abonnement payé par les boulangeries).
- Les conditions de Google limitent la conservation des données et obligent à les afficher sur une carte Google avec attribution : incompatible avec notre carte OSM.
- Google ne fournit ni boucles ni « routes calmes » : on devait de toute façon fabriquer ces critères nous-mêmes.

## Ce qui remplace Google
Voir `osm-versions-12-22.md` : OpenRouteService (tracé), Overpass (boulangeries), MapLibre + OpenFreeMap (carte), Base Adresse Nationale + Photon (adresses).

## Ce que Google pourrait encore apporter (hypothèse, non décidée)
- **Notes et nombre d'avis** pour amorcer, via l'API officielle uniquement, sur les 4 à 6 boulangeries réellement proposées (pas pour les tracés). Ordre de grandeur indicatif : environ 20 $ pour 1 000 consultations de fiche avec note, soit 10 à 30 $ par ville pour une passe d'amorçage (tarifs à confirmer sur la page officielle de Google).
- **À ne pas faire** : recopier les notes Google dans notre base, ni appliquer une règle mécanique « validée si ≥ 4/5 sur Google ».
- Dépend de l'avis juridique : `questions-juridiques-notation.md`.

## Historique : état du code d'origine (31/10, maquettes d'origine)
Un seul réglage : `PLACES_CONFIG.provider = 'demo' | 'google'` (+ `googleKey`, `mapsKey`, `mapId`).
- **Tracé** : `RoutingGoogle` (Routes API `computeRoutes`, `travelMode: BICYCLE`). Boucle fabriquée par nous : points de passage sur un cercle autour du départ, rayon ajusté jusqu'à la distance demandée (±5 km).
- **Boulangeries** : Places API (New), `searchNearby` autour de 4 points de la boucle.
- **Partenaires** : table `PARTNERS` (identifiant du lieu → avantage, catégories). Seule donnée à nous.
- **Cartes** : Google Maps JavaScript. **Jamais testé contre le vrai Google.**
- La version OSM reprend le même mécanisme (mêmes points d'entrée `gOn`, `PLACES`, `RoutingGoogle`, `PlacesGoogle`) en redirigeant vers OSM quand `osmOn()` est vrai.
