# Ride and train

## Temps A (fait, vers 21-22)
- Le cycliste tape une ville ou une gare ; l'appli prend la gare OSM (`railway=station|halt`) la plus proche de l'arrivée. **Une gare est toujours proposée**, même éloignée : on n'annonce jamais « pas de gare », pour qu'il puisse toujours rentrer.
- Aller avec pauses jusqu'à la gare (comme « Vers un lieu »).
- Règles vélo au retour affichées (vérifiées le 05/11/2026) : Transilien/RER, interdiction de vélo en semaine 6h30-9h30 et 16h30-19h30 ; TER en général gratuit ; TGV INOUI / Intercités 10 € non démonté (5 € sur certaines lignes) ; Ouigo 5-10 €. Jours fériés pris en compte.

## Temps B (à faire)
1. Pour chaque gare candidate, vérifier qu'elle propose un trajet retour vers le point de départ (horaires).
2. Classer ensuite par durée totale (vélo + train).
- Prérequis : compte IDFM PRIM (jeton), lecture de la licence Mobilité par l'utilisateur, serveur à nous (le jeton ne doit pas être dans la page).
- Les horaires chargés peuvent changer (perturbations, nouveaux horaires) : prévoir des mises à jour côté serveur ; scraping exclu, API officielle uniquement.
