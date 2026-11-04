# Intégration Google (décision : tout repose sur Google)

**Décision (31/10/2026)** : le cœur de l'appli, ce sont les choix de boulangeries. Les notes, avis, photos et horaires viennent donc de Google, et le tracé aussi (Routes API, mode vélo). Zone de test : Versailles + 50 km ; cœur de lancement : Versailles + vallée de Chevreuse.

## État du code (maquette)
Un seul réglage : `PLACES_CONFIG.provider = 'demo' | 'google'` (+ `googleKey`, `mapsKey`, `mapId`).
- **Tracé** : `RoutingGoogle` (Routes API `computeRoutes`, `travelMode: BICYCLE`, évite autoroutes/péages/bacs). La boucle est fabriquée par nous : points de passage sur un cercle autour du départ, rayon ajusté jusqu'à la distance demandée (±5 km). Une fois les pauses choisies, nouveau calcul avec les pauses insérées dans l'ordre.
- **Boulangeries** : Places API (New), `searchNearby` autour de 4 points de la boucle, avec note, nombre d'avis, horaires. Les horaires alimentent le calcul « ouvert à mon passage ».
- **Partenaires** : table `PARTNERS` (identifiant Google du lieu → avantage, catégories). Seule donnée à nous.
- **Cartes** : Google Maps JavaScript pour l'accueil (tracé + repères) et l'onglet Carte.
- **Test** : uniquement avec des réponses Google simulées. **Jamais testé contre le vrai Google.**

## À faire pour activer
1. Projet Google Cloud + facturation ; activer Places API (New), Routes API, Maps JavaScript API.
2. Clé Maps JS restreinte au domaine ; clé Places/Routes **côté serveur** (ne pas laisser dans la page).
3. Budget et alertes de quota. Le coût dépend des champs demandés (`FieldMask`) : note et horaires coûtent plus cher que le nom seul.
4. Relire les conditions Google : affichage des données Places sur une carte Google, durée de mise en cache, attributions.

## Inconnues à vérifier sur Versailles / Chevreuse
- Qualité du mode vélo de Google en France (pistes, chemins, côtes).
- Google ne propose ni boucle, ni « routes calmes » : notre critère « calme » reste à construire (point d'entrée `calmHook`).
- Nombre d'appels par tracé (≈ 3 itinéraires + 4 recherches) à mesurer pour chiffrer le coût.
