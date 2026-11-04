# Synchro automatique des sorties (montre / GPS) – spécification

Décision du 27/10/2026 : intégrer le même mécanisme que Strava pour que chaque sortie soit enregistrée automatiquement à la fin. Les demandes de partenariat seront faites plus tard.

## Objectif
Quand un cycliste roule un tracé Miam Ride avec sa montre ou son GPS, la sortie arrive seule dans l'appli à la synchro de l'appareil : le tracé est validé, l'XP est attribuée, les défis et badges avancent, et l'historique est mis à jour.

## Déroulé
1. Le cycliste génère un tracé et l'envoie sur son appareil (ou l'exporte en GPX). Statut : **Prévu** puis **Envoyé**.
2. Il roule. L'appareil enregistre.
3. À la fin, l'appareil se synchronise avec sa plateforme (Garmin Connect, Wahoo, Coros, Suunto, Polar, Strava…).
4. La plateforme prévient Miam Ride (webhook : « nouvelle activité »). Statut : **Sortie détectée**.
5. Miam Ride récupère la trace GPS et la compare au tracé prévu :
   - le fichier GPX n'a pas d'identifiant fiable, donc comparaison **géométrique** ;
   - sortie du même jour, dans la fenêtre horaire attendue ;
   - part de la trace restée à moins de 50 m du tracé prévu ;
   - passage à proximité de la ou des boulangeries choisies.
6. Correspondance ≥ 80 % (seuil à ajuster) : statut **Validée** → XP (1 km = 1 XP), défis, badges, compteur de boulangeries, écran de fin de sortie avec barre d'XP animée.
7. Sinon : statut **À vérifier**, le cycliste peut contester ou importer un fichier.

## Sources de données
| Source | Mode | Statut |
|---|---|---|
| Garmin, Wahoo, Coros, Suunto, Polar, Hammerhead | API partenaire + webhook | Demande de partenariat à faire |
| Strava | API + webhook | Nouveau compte développeur : 1 athlète, puis 10 sans revue, au-delà revue Strava (non garantie) ; règles : cache 7 jours, pas d'usage IA |
| Agrégateurs (Terra, Junction…) | Une connexion pour plusieurs marques | Payant, conditions non vérifiées |
| Import manuel GPX/FIT | Upload | Aucun partenariat, solution de secours |
| Téléphone (« Lancer le trajet ») | Enregistrement dans l'appli | Déjà dans la maquette |

## Règles et garde-fous
- Anti-triche : validation par correspondance de trace, un passage en boulangerie validé par QR compte comme point de contrôle.
- Consentement explicite pour lire les sorties ; possibilité de se déconnecter et de supprimer ses données.
- Respecter les conditions de chaque API (durée de conservation, usages interdits).

## Maquette à construire
- Statuts de tracé dans l'historique : Prévu → Envoyé → Sortie détectée → Validée.
- Bouton de démonstration « Simuler la synchro de ma montre » : arrivée de la sortie, comparaison (« 94 % du tracé suivi »), validation, écran d'XP animé.
- Bouton « Importer un fichier » en secours.

## À faire plus tard
- Demandes de partenariat (délais non garantis, à anticiper avant le lancement).
- Choix : intégrations directes ou agrégateur.
- Serveur pour recevoir les webhooks et stocker les traces.
