# Miam Ride – état au 27/10/2026 (soir)

## Fichiers (maquettes, données fictives)
- Accueil cycliste (hébergé) : https://claude.ai/artifact/7E9BYKzrKy2JC9Tv6KBhEs
- Introduction (intro toujours affichée) : https://claude.ai/artifact/1XtttXTYqTLrAt9HT2XYGQ
- Espace boulangerie : https://claude.ai/artifact/AGJ92pXFzczKo9jQu613jL
- Feuille de route (statuts enregistrés) : https://claude.ai/artifact/E2JH5ugeSJ6tunMccCELA1
- Version carte OpenStreetMap : `miam-ride-osm.html` (nécessite internet pour MapLibre)
- Documents du projet : `modele-economique.md`, `synchro-sorties-montre-gps.md`, `criteres-generation-traces.md`, `garage-50-velos.md`

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
- **Prêt pour Google** : code en deux fournisseurs interchangeables (`PlacesDemo` actuel, `PlacesGoogle` écrit mais non testé) réglés par `PLACES_CONFIG.provider`. Google fournit position, nom, adresse, photos ; les avantages viennent de notre base (`PARTNER_IDS`). Photos : emplacements vides en démo. Positions des 12 boulangeries approximatives. Conditions Google : afficher ces contenus sur une carte Google avec attribution et sans copier les photos ; au lancement, le moteur de carte actuel sera remplacé par Google Maps JS, le reste ne change pas.

- **Confirmation de l'offre par les cyclistes (29/10)** : les avis (« Tu as pris quoi ? ») servent à confirmer ce que propose une boulangerie (3 avis), à afficher une note de produit (5 avis minimum) et à classer (« Meilleur flan du secteur »). Un seul avis par produit, boulangerie et jour. Réglage de démo « avis simulés » (désactivé par défaut) pour voir les chiffres. Détails dans `notation-produits.md`.

- **Anti-abus des avis (29/10)** : règles réunies dans `AVIS_RULES` (seuils, plafond d'XP de 20 avis par mois, un avis par jour…), réponse et signalement dans l'espace boulangerie (exemples de démo). File de modération, masquage automatique et anonymisation réelle restent pour la version serveur.

- **Statistiques de la boulangerie (30/10)** : nouvel onglet « Stats » dans l'espace boulangerie (7 jours, 30 jours, 3 mois) : passages, cyclistes différents et fidèles, récompenses offertes, jours et heures les plus actifs, nouveaux et revenus, produits cités dans les avis (note à partir de 5 avis, suggestion d'ajouter un produit cité par 3 cyclistes), estimation de l'apport (passages × panier moyen saisi par la boulangerie). L'export CSV est reporté : la visionneuse bloque les téléchargements (à refaire avec la capacité « downloads » ou côté serveur). Chiffres de démonstration. C'est la « preuve de valeur » prévue dans `modele-economique.md`.

- **Horaires et temps de roulage (30/10)** : choix du départ (jour + heure) et calcul de l'heure de passage à chaque pause (22 km/h, 15 min par pause, marge ±15 min). Une boulangerie est jugée ouverte **à l'heure du passage** : ouverte, « à vérifier » (partiellement) ou fermée (non proposée). Récapitulatif avec les heures et le retour estimé ; fiche de la carte avec « ouvert / fermé » ; horaires de démonstration. Pas d'éditeur d'horaires dans l'espace boulangerie (retiré le 31/10) : les horaires viendront de Google Places. Détails dans `horaires-et-roulage.md`.

- **Photos de la vitrine (31/10)** : décision, **l'espace boulangerie reste simple et ne propose pas d'envoi de photos**, pour ne pas faire croire aux boulangeries que l'interface est compliquée. L'équipe Miam Ride collecte les photos (vitrine, carte, ardoise) et met à jour les produits elle-même. Le parcours d'envoi réalisé puis retiré de la maquette. Pas de collecte de photos Google ou Instagram (conditions d'utilisation, droits d'auteur, données personnelles, fiabilité). **À construire** : un outil interne pour l'équipe (photos reçues, reconnaissance proposée, vérification, mise à jour des produits).

- **Couche Google codée (31/10)** : tout repose sur Google, comme décidé. Un réglage `PLACES_CONFIG.provider` (démo / google). Tracé : Routes API en mode vélo, boucle fabriquée par l'appli (points de passage, rayon ajusté sur la distance), puis tracé final avec les pauses dans l'ordre. Boulangeries : Places API (note, avis, horaires) autour de la boucle ; les horaires nourrissent le calcul « ouvert à mon passage ». Partenaires : table `PARTNERS` indexée par l'identifiant Google du lieu. Cartes : Google Maps JavaScript. **Testé uniquement avec des réponses Google simulées** ; de vrais essais (simulations Versailles / Chevreuse) après obtention de la clé et de la facturation. Détails et checklist dans `integration-google.md`.

- **Direction artistique (01/11)** : six styles proposés (page « Miam Ride – Styles »). Décision : on reste sur **Pop** ; les autres sont mis de côté et gelés. Détails dans `styles-alternatifs.md`.

## Décisions
- **Modèle économique** : abonnement payé par les boulangeries, appli gratuite pour les cyclistes (détails dans `modele-economique.md`). Abonnement utilisateur reporté. Prix à fixer par une étude de marché.
- **Authentification** : la vraie connexion (Supabase, e-mail + mot de passe puis Google et Apple) est reportée à la fin du projet, quand la structure des données sera stable.
- Connexion par Strava abandonnée pour l'instant.
- Demandes de partenariat (Garmin, Wahoo, Strava, Coros, Suunto, Polar) à faire plus tard.

## Feuille de route (20 points + étude de prix)
- Fait : carte des boulangeries (maquette), mode Mamie, petits écrans, création de compte (maquette), historique ↔ XP/défis, sortie en cours, modèle économique.
- En cours : synchro automatique montre/GPS (maquette faite, vraie synchro dépend des partenariats).
- À faire, priorité haute : étude de marché du prix de l'abonnement, vrai moteur de routage, demandes de partenariat, vraie authentification.
- À faire, priorité moyenne : inscription du commerce, données personnelles et conditions d'utilisation.
- À faire, priorité basse : partage de sorties, notifications, envoi réel vers Garmin/Wahoo, connexion Strava, images des 50 vélos (à fournir).

## Zone de test (31/10)
- **Zone de test : Versailles et 50 km autour.** **Cœur de lancement : Versailles et la vallée de Chevreuse** (décision du 31/10), pour recruter de vrais partenaires et valider le routage sur une petite zone. Débloque le vrai moteur de routage et le dimensionnement de l'étude de prix.
- **Vérification faite le 31/10** : depuis l'environnement de développement, les données OpenStreetMap (Geofabrik, Overpass) et les services de routage (OpenRouteService, OSRM, BRouter) ne sont pas accessibles, donc le routage ne peut pas être testé ici. **Décision du 31/10 : rester sur Google pour tout** (carte, lieux, photos, horaires, routage). La documentation de Google Routes API liste le mode vélo, mais ses options d'évitement se limitent aux péages, autoroutes, ferries et intérieurs, et ne mentionne ni boucles ni routes calmes : nous générerons les boucles (points de passage) et noterons le calme des routes nous-mêmes, puis nous testerons le résultat réel avec une clé API.

## Limites connues
- Pas de vrai moteur de routage : les tracés sont fictifs.
- Les API des marques de montres/GPS demandent des partenariats.
- La bibliothèque de carte (MapLibre) est bloquée dans mon environnement de test : la version OSM n'a été testée qu'avec une simulation.

## Mise à jour — look « produit » (nov. 2026)
- La maquette se présente comme une vraie appli : plus aucune mention démo/fictif/exemple côté utilisateur.
- Outils de présentation (heure simulée, démo accélérée, saisie de position…) masqués : activer avec `#demo` dans l'URL, désactiver avec `#nodemo`.
- Les vrais noms de boulangeries ont été remplacés par des noms inventés (notes et statut partenaire fictifs = risque vis-à-vis de tiers). Sauvegardes bak4_* conservées pour revenir en arrière.
- Le formulaire de connexion reste factice (aucun vrai mot de passe) : vraie auth Supabase + CGU/RGPD = prochain gros chantier.
- Le minuteur d'enregistrement reste accéléré ×60 tant que la vraie géoloc n'est pas branchée.
