# Ride and train

## Temps A (fait, vers 21-22)
- Le cycliste tape une ville ou une gare ; l'appli prend la gare OSM (`railway=station|halt`) la plus proche de l'arrivée. **Une gare est toujours proposée**, même éloignée : on n'annonce jamais « pas de gare », pour qu'il puisse toujours rentrer.
- Aller avec pauses jusqu'à la gare (comme « Vers un lieu »).
- Règles vélo au retour affichées (vérifiées le 05/11/2026) : Transilien/RER, interdiction de vélo en semaine 6h30-9h30 et 16h30-19h30 ; TER en général gratuit ; TGV INOUI / Intercités 10 € non démonté (5 € sur certaines lignes) ; Ouigo 5-10 €. Jours fériés pris en compte.

## Temps B (fait côté code, vers 24 : à tester avec le vrai PRIM)
- Pour chaque gare candidate (4 au plus), l'appli demande à une **fonction Supabase** (`serveur/supabase/functions/train-retour`) les prochains trains vers le point de départ. La fonction garde le jeton PRIM dans les secrets Supabase.
- **Vers 26** : le tracé va **au lieu saisi** (l'adresse reste affichée en entier). La gare la plus proche n'est cherchée qu'après le choix des pauses ; le tronçon lieu → gare est calculé et ajouté au tracé et au GPX (repère « Gare de retour »).
- **Vers 25** : la carte « Retour en train » s'affiche quand toutes les pauses sont choisies. Elle montre la ligne (badge), le train conseillé, la liste des prochains trains (en cas de retard) avec la règle vélo à l'heure de chaque train, puis les autres gares.
- Affichage par gare : heure du train, arrivée chez soi, durée, correspondances, lignes, règle vélo **à l'heure réelle du train**, durée totale de la sortie. La gare la plus rapide est signalée ; un clic change de gare.
- Île-de-France seulement (Transilien, RER, bus, métro). Hors zone : message clair. TER et grandes lignes hors IDF : source à ajouter plus tard.
- Mise en place : voir `serveur/README.md`. À confirmer avec le « Playground » PRIM : l'adresse exacte de l'API d'itinéraires (variable `PRIM_BASE`).
- Pas de scraping : API officielle uniquement. Les horaires ne sont pas conservés.
- Reste à faire : tester avec le vrai jeton ; durée exacte du trajet vélo par gare alternative (aujourd'hui estimée) ; licence « Mobilité » à relire.
