# Versions OSM 12 à 29 (nov. 2026)

Moteur : OpenRouteService (profil cycling-road), Overpass (boulangeries, gares), MapLibre + OpenFreeMap (carte), Base Adresse Nationale + Photon (adresses). Chaque version = `Miam ride osm - vers N.html` ; scripts de build et tests dans le dépôt `alanbtl/Miam-ride` (`outils/`, `outils/tests/`).

| Version | Apport |
|---|---|
| 12 | OSM par défaut. 3 boucles candidates, la mieux notée selon l'ambiance est gardée (calme visé : 85 / 65 / 45 %). Évitement des routes principales. Ligne de contrôle « objectif atteint ». Départ par défaut + localisation avec messages clairs. |
| 13 | Boulangeries cherchées d'abord, boucles notées selon les boulangeries ouvertes dans les fenêtres de pause. Mode ville / campagne. Statuts (validée, notée, non vérifiée, à éviter) et écran de validation (Profil › Compte). Filtre des chaînes. |
| 14 | « Vers un lieu » fonctionnel : recherche d'adresse, boucle qui passe par le lieu. |
| 15 | Export GPX réel (tracé, altitude, départ, pauses, arrivée), partage ou téléchargement. |
| 16-17 | Suggestions d'adresse personnalisées (départ et arrivée), attente de la résolution avant génération, ligne « Passage par ». |
| 18 | Recherche d'arrivée sans biais de proximité (villes lointaines). Bandeau « mode démo » quand la clé manque (clé stockée par fichier). |
| 19 | Boulangeries proposées selon leur position réelle sur le tracé (pas trop tôt). |
| 20 | Ligne de contrôle du nombre de boulangeries à chaque étape. |
| 21-22 | Ride and train, temps A (voir `ride-and-train.md`). |
| 23 | Ride and train : plus de choix de distance, seulement le lieu d'arrivée (adresse, ville ou gare). |
| 24 | Ride and train temps B : horaires de retour via une fonction Supabase + PRIM (Île-de-France Mobilités). |
| 25 | Carte « Retour en train » après le choix des pauses : ligne, prochains trains (en cas de retard), autres gares. |
| 26 | Le tracé va au lieu saisi (adresse affichée en entier) ; la gare la plus proche est cherchée après les pauses, avec le tronçon lieu → gare ajouté au tracé et au GPX. |
| 27 | Carte condensée, pastilles de ligne colorées (pas les logos officiels), règles vélo retirées de l'affichage. |
| 28 | « Détail du trajet » (étapes marche / train / correspondance) pour diagnostiquer les durées. |
| 29 | Gares : nouvel essai si Overpass limite le débit (429), cache de 30 jours, moins de requêtes. |

## Décisions associées
- Full OSM, Google abandonné (`integration-google.md`).
- Notes de boulangeries : avis juridique d'abord (`questions-juridiques-notation.md`).
- Points d'eau en attente ; espace communautaire en feuille de route (`feuille-de-route-communaute.md`).
- Serveur : projet Supabase (compte GitHub du projet), fonction `train-retour` qui garde le jeton PRIM (voir `serveur/README.md`).
- Cafés (`amenity=cafe`) : prochaine étape, filtre Boulangerie / Café / Les deux.

## Limites
Tout a été vérifié avec des services simulés ; les vrais services (ORS, Overpass, Photon, BAN) ne sont pas joignables depuis l'environnement de développement. Le test réel est à faire sur l'appareil de l'utilisateur.
