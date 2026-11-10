# Miam Ride – état au 10/11/2026

> **Changement majeur (04/11/2026) : on passe en full OpenStreetMap (tracés, boulangeries, carte). Google n'est plus utilisé pour les tracés.** Voir la section « Mise à jour du 08/11 » en bas, `osm-versions-12-22.md` et `integration-google.md`. Les paragraphes plus anciens qui parlent de « tout Google » sont conservés pour mémoire et signalés *(remplacé)*.

## Fichiers (maquettes, données fictives)
- **Version de travail actuelle : `Miam ride osm - vers 29.html`** (aussi dans le dépôt GitHub `PropelADV2/miam-ride-app`, dossier `maquettes/osm-vers-29.html`). À ouvrir en fichier local (double-clic) : la clé OpenRouteService est à coller dans le bandeau jaune de l'accueil à chaque nouveau fichier.
- Accueil cycliste (hébergé, démo) : https://claude.ai/artifact/7E9BYKzrKy2JC9Tv6KBhEs
- Introduction (intro toujours affichée) : https://claude.ai/artifact/1XtttXTYqTLrAt9HT2XYGQ
- Espace boulangerie : https://claude.ai/artifact/AGJ92pXFzczKo9jQu613jL
- Feuille de route (statuts enregistrés) : https://claude.ai/artifact/E2JH5ugeSJ6tunMccCELA1
- Version carte OpenStreetMap : `miam-ride-osm.html` (nécessite internet pour MapLibre)
- Documents du projet : `modele-economique.md`, `synchro-sorties-montre-gps.md`, `criteres-generation-traces.md`, `garage-50-velos.md`, `osm-versions-12-22.md`, `ride-and-train.md`, `questions-juridiques-notation.md`, `feuille-de-route-communaute.md`

## Fonctionnalités de la maquette
- Génération de tracé, choix des boulangeries, deux boutons : « Partage sur ta montre ou GPS » et « Lancer le trajet ».
- Création de compte / connexion en démo, avec mode invité.
- Résumé de fin de sortie avec barre d'XP animée.
- Synchro montre/GPS simulée, validation automatique à l'ouverture de l'appli, écran de victoire plein écran.
- XP, défis du mois, badges et garage de vélos liés à l'historique.
- Mode « sortie en cours » : prochaine pause, validation du passage par QR.
- Défis : pause (3 boulangeries), 100 km, Lève-tôt (départ avant 8 h), Matinal (arrivée avant midi), régularité (5 sorties/mois), train.

## Règle « tracé terminé » (ajoutée le 27/10)
- Une sortie ne valide défis et badges que si elle est terminée : au moins 90 % du tracé prévu, ou au moins 10 km en sortie libre.
- Une sortie non terminée garde ses kilomètres en XP, apparaît « non terminée » dans l'historique, et n'est pas comptée dans les défis ni les badges.
- Au départ avant 8 h, une bannière « Défi Lève-tôt en cours » s'affiche, mais rien n'est validé avant la fin du tracé.
- Les sorties validées par la synchro comptent comme terminées.
- Le seuil de 90 % est modifiable (100 % ou 80 % possibles).

## Choix par produit (ajouté le 29/10)
- Appli cycliste : ligne facultative « Je cherche… » (Flan, Croissant, Pain au chocolat, Éclair, Tarte, Baguette tradition, Sandwich, plus « Autre… »). Un seul produit à la fois.
- Avec un produit choisi, seules les boulangeries qui le proposent restent dans la liste (mention « Propose : flan »). Aucune note de produit ni badge « meilleur » n'est affichée : retiré le 29/10 pour ne pas rattacher de faux chiffres à de vrais commerces. L'ordre reste partenaires d'abord, puis note générale (fictive).
- Espace boulangerie : « Tes spécialités » (le commerce coche ce qu'il fait) et « Où tu apparaîtras » (recherches concernées).
- Données de démonstration : 12 boulangeries réelles de Versailles (noms et adresses) ; produits proposés, notes, avis et avantages partenaires fictifs.
- **Validation du passage = toujours par QR sur le téléphone**, même avec montre ou GPS (bouton « Je suis chez … » dans Historique > Tracés à rouler). La notation est proposée à la fin du tracé.
- **Notification à 500 m** d'une boulangerie du tracé : « Prépare ton QR code » (réglage dans le profil). En vrai, détection par la position du téléphone (géorepérage), pas par la montre. Détails dans `notation-produits.md`.
- **Notation des produits (29/10)** : fenêtre « Tu as pris quoi ? » (produit + note de 1 à 5, +5 XP). L'avis est gardé sur l'appareil, affiché « ton avis : 5/5 » dans la recherche par produit, compté dans le profil. Pas de notes d'autres utilisateurs en démo. Détails et règles anti-abus dans `notation-produits.md`.

- **Mode Mamie (29/10)** : après le tirage, mêmes deux boutons que les autres modes (« Partage sur ta montre ou GPS » / « Lancer le trajet ») et un bouton « Une autre surprise » pour relancer.

- **Petits écrans (29/10)** : une fois toutes les pauses choisies, le panneau du bas se réduit tout seul (nom de la boulangerie et distance sur une ligne, boutons visibles). On le rouvre en touchant la barre grise. Sur un écran de 360 × 640, la carte passe de 122 à 235 px de haut.

- **Carte des boulangeries (29/10)** : nouvel onglet « Carte » (style explorer). On déplace, zoome, dézoome ; chaque partenaire est une pastille jaune avec son avantage (« -10 % », « Café offert »), les non-partenaires sont de petits points gris sans chiffre, et les pastilles proches se regroupent en un rond avec le nombre. Filtres : « Partenaires » et « Je cherche… ». Toucher une pastille ouvre une fiche (avantage, fidélité, spécialités, photos clients Google et « Passer par ici »). « Passer par ici » ajoute la boulangerie aux pauses du tracé sur l'accueil (une pause de plus si besoin).
- **Prêt pour Google** *(remplacé le 04/11 par OSM)* : code en deux fournisseurs interchangeables (`PlacesDemo` actuel, `PlacesGoogle` écrit mais non testé) réglés par `PLACES_CONFIG.provider`. Google fournit position, nom, adresse, photos ; les avantages viennent de notre base (`PARTNER_IDS`). Conditions Google : afficher ces contenus sur une carte Google avec attribution et sans copier les photos.

- **Confirmation de l'offre par les cyclistes (29/10)** : les avis (« Tu as pris quoi ? ») servent à confirmer ce que propose une boulangerie (3 avis), à afficher une note de produit (5 avis minimum) et à classer (« Meilleur flan du secteur »). Un seul avis par produit, boulangerie et jour. Réglage de démo « avis simulés » (désactivé par défaut) pour voir les chiffres. Détails dans `notation-produits.md`.

- **Anti-abus des avis (29/10)** : règles réunies dans `AVIS_RULES` (seuils, plafond d'XP de 20 avis par mois, un avis par jour…), réponse et signalement dans l'espace boulangerie (exemples de démo). File de modération, masquage automatique et anonymisation réelle restent pour la version serveur.

- **Statistiques de la boulangerie (30/10)** : nouvel onglet « Stats » dans l'espace boulangerie (7 jours, 30 jours, 3 mois) : passages, cyclistes différents et fidèles, récompenses offertes, jours et heures les plus actifs, nouveaux et revenus, produits cités dans les avis (note à partir de 5 avis, suggestion d'ajouter un produit cité par 3 cyclistes), estimation de l'apport (passages × panier moyen saisi par la boulangerie). L'export CSV est reporté : la visionneuse bloque les téléchargements. Chiffres de démonstration. C'est la « preuve de valeur » prévue dans `modele-economique.md`.

- **Horaires et temps de roulage (30/10)** : choix du départ (jour + heure) et calcul de l'heure de passage à chaque pause (22 km/h, 15 min par pause, marge ±15 min). Une boulangerie est jugée ouverte **à l'heure du passage** : ouverte, « à vérifier » (partiellement) ou fermée (non proposée). Pas d'éditeur d'horaires dans l'espace boulangerie (retiré le 31/10). Détails dans `horaires-et-roulage.md`. *(Depuis le 04/11, les horaires viennent d'OpenStreetMap, plus de Google.)*

- **Photos de la vitrine (31/10)** : décision, **l'espace boulangerie reste simple et ne propose pas d'envoi de photos**. L'équipe Miam Ride collecte les photos et met à jour les produits elle-même. Pas de collecte de photos Google ou Instagram (conditions d'utilisation, droits d'auteur, données personnelles, fiabilité). **À construire** : un outil interne pour l'équipe.

- **Couche Google codée (31/10)** *(remplacée le 04/11)* : Routes API vélo, Places API, Google Maps JS, testés uniquement avec des réponses simulées. Mise de côté pour des raisons de coût (voir `integration-google.md`). Le code est conservé dans les maquettes d'origine.

- **Direction artistique (01/11)** : six styles proposés (page « Miam Ride – Styles »). Décision : on reste sur **Pop** ; les autres sont mis de côté et gelés. Détails dans `styles-alternatifs.md`.

## Décisions
- **Full OpenStreetMap (04/11/2026)** : tracés (OpenRouteService), boulangeries (Overpass/OpenStreetMap), carte (MapLibre + OpenFreeMap), adresses (Base Adresse Nationale + Photon). Raison : le coût de Google augmente avec chaque requête (≈ 0,20 à 0,25 $ par tracé en version naïve) et menaçait la rentabilité. **Abroge** la décision du 31/10 « rester sur Google pour tout ».
- **Notation des boulangeries** : OSM ne fournit aucune note. Statuts internes (validée par nous, notée par les cyclistes via QR, non vérifiée) ; Google ne servirait éventuellement qu'à amorcer les notes, **sous réserve d'un avis juridique** (`questions-juridiques-notation.md`). Pas de recopie des notes Google dans notre base.
- **Modèle économique** : abonnement payé par les boulangeries, appli gratuite pour les cyclistes (détails dans `modele-economique.md`). Abonnement utilisateur reporté. Prix à fixer par une étude de marché.
- **Authentification** : la vraie connexion (Supabase) est reportée, mais devient nécessaire pour la suite (serveur, notes, clé API, horaires de trains, communauté).
- Connexion par Strava abandonnée pour l'instant.
- Demandes de partenariat (Garmin, Wahoo, Strava, Coros, Suunto, Polar) à faire plus tard.
- **Points d'eau** : mis en attente (05/11).

## Feuille de route (20 points + étude de prix)
- Fait : carte des boulangeries (maquette), mode Mamie, petits écrans, création de compte (maquette), historique ↔ XP/défis, sortie en cours, modèle économique, **vrai moteur de routage (OSM/ORS), GPX réel, « Vers un lieu », Ride and train temps A (08/11)**.
- En cours : synchro automatique montre/GPS (maquette faite, vraie synchro dépend des partenariats) ; GPX téléchargeable pour une Coros (à confirmer par un test réel).
- À faire, priorité haute : serveur + vraie authentification (Supabase), étude de marché du prix de l'abonnement, demandes de partenariat, avis juridique sur les notes, hébergement fixe de l'appli (clé et GPS).
- À faire, priorité moyenne : cafés comme type de pause, Ride and train temps B (horaires), points d'eau, inscription du commerce, données personnelles et conditions d'utilisation.
- À faire, priorité basse : espace communautaire (`feuille-de-route-communaute.md`), partage de sorties, notifications, envoi réel vers Garmin/Wahoo, connexion Strava, images des 50 vélos (à fournir).

## Zone de test
- **Zone de test : Versailles et 50 km autour.** **Cœur de lancement : Versailles et la vallée de Chevreuse** (décision du 31/10).
- *(Abrogé le 04/11)* Décision du 31/10 de rester sur Google pour tout, prise parce que les services OSM n'étaient pas joignables depuis l'environnement de développement. Le test réel se fait désormais sur l'ordinateur de l'utilisateur, avec une clé OpenRouteService.

## Limites connues
- Les tests automatiques utilisent des réponses simulées : l'environnement de développement n'accède pas aux vrais services (OpenRouteService, Overpass, adresses). Les vrais essais se font sur l'appareil de l'utilisateur.
- Les API des marques de montres/GPS demandent des partenariats.
- La clé OpenRouteService est stockée dans le navigateur, **fichier par fichier** : à recoller à chaque nouvelle version, d'où le besoin d'un hébergement fixe.
- Quotas gratuits OpenRouteService (≈ 40 requêtes/minute, ≈ 2 000/jour, à vérifier) : une génération consomme 5 à 8 appels.
- Overpass public : usage de test, à remplacer par notre base de boulangeries pour la production.

## Mise à jour — look « produit » (nov. 2026)
- La maquette se présente comme une vraie appli : plus aucune mention démo/fictif/exemple côté utilisateur.
- Outils de présentation (heure simulée, démo accélérée, saisie de position…) masqués : activer avec `#demo` dans l'URL, désactiver avec `#nodemo`.
- Les vrais noms de boulangeries ont été remplacés par des noms inventés (notes et statut partenaire fictifs = risque vis-à-vis de tiers).
- Le formulaire de connexion reste factice : vraie auth Supabase + CGU/RGPD = prochain gros chantier.
- Le minuteur d'enregistrement reste accéléré ×60 tant que la vraie géoloc n'est pas branchée.

## Mise à jour du 08/11/2026 — passage full OSM (versions 12 à 22)
Détail complet dans `osm-versions-12-22.md`. En résumé :
- **v12** : OSM par défaut ; 3 boucles candidates comparées, la mieux notée selon l'**ambiance** est gardée (objectifs de routes calmes 85 / 65 / 45 %) ; correction par évitement des routes principales ; ligne « objectif atteint ou non ».
- **v12 (suite)** : départ par défaut explicite, bouton de localisation avec messages clairs (échec fréquent sur un fichier local).
- **v13** : boulangeries cherchées d'abord ; notation des boucles avec les boulangeries ouvertes dans les fenêtres de pause ; mode ville / campagne ; statuts de boulangerie et écran de validation (Profil › Compte) ; filtre des chaînes.
- **v14, v16, v17, v18** : « Vers un lieu » fonctionnel (recherche d'adresse avec suggestions, boucle qui passe par le lieu, trajet le plus rapide, ligne de contrôle « Passage par »), suggestions aussi pour le départ, recherche d'arrivée sans biais de proximité, bandeau « mode démo » quand la clé manque.
- **v15** : export **GPX** réel (tracé + altitude, départ, pauses, arrivée), partage ou téléchargement.
- **v19, v20** : boulangeries proposées selon leur **position réelle sur le tracé** (fenêtres de pause respectées), et ligne de contrôle du nombre de boulangeries à chaque étape.
- **v21, v22** : **Ride and train, temps A** (`ride-and-train.md`) : gares OSM, aller avec pauses jusqu'à la gare, règles vélo au retour, toujours une gare proposée.

## Mise à jour du 10/11/2026 — vers 23 à 29, serveur et GitHub
- **Ride and train, temps B fait (vers 24-29)** : horaires de retour réels via PRIM (Île-de-France Mobilités) par une fonction Supabase qui garde le jeton. Carte de retour : gare, prochains trains avec pastille de ligne, autres gares, « Détail du trajet ». Le tracé va au lieu saisi, puis jusqu'à la gare (tronçon ajouté au GPX). Test réel OK (« 4 trajets »). Cas Versailles → Boulogne (3 h 09) à éclaircir.
- **Règles vélo des trains** : retirées de l'affichage (décision du 09/11), le code reste.
- **Compte du projet** : nouveau compte GitHub unique (`PropelADV2`), dépôt `miam-ride-app` (à passer en privé), compte Supabase relié. Ancien dépôt `alanbtl/Miam-ride` abandonné.
- **Serveur** : dossier `serveur/` (fonction `train-retour`, README de mise en place). Prochain usage de Supabase : comptes, statuts de boulangeries partagés, notes QR.
- **Limites** : horaires seulement en Île-de-France ; Overpass public parfois saturé (429) ; logos officiels SNCF non utilisés (marque protégée).

## Prochaines étapes
1. Cafés comme autre type de pause (filtre Boulangerie / Café / Les deux) : prochaine tâche.
2. L'utilisateur teste en réel (vers 29), GPX sur Coros, localisation sur un site en https.
3. Avis juridique sur les notes ; décision sur Google pour amorcer.
4. Serveur + authentification (Supabase) ; hébergement fixe.
5. Horaires hors Île-de-France (TER, grandes lignes) et espace communautaire.
6. Points d'eau (en attente).
