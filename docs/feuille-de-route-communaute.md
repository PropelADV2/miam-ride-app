# Feuille de route : espace communautaire Miam Ride

*Créée le 5 novembre 2026. Statut : mise de côté, à reprendre plus tard. Aucun code écrit.*

## 1. Vision

Le vélo est un sport qui se pratique souvent à plusieurs. Miam Ride sait déjà préparer une sortie complète (tracé calme, pauses boulangerie, horaires, GPX). L'espace communautaire permet à un cycliste de **proposer sa sortie** et à d'autres de **la rejoindre**.

Exemple type : le samedi soir, une cycliste qui roule seule publie sa sortie du dimanche (tracé, point de rendez-vous, heure, allure, places). Des cyclistes de la même ville la voient, demandent à rejoindre, sont acceptés, se retrouvent le lendemain, puis discutent sur l'application ou sur WhatsApp.

## 2. Principes

1. **Sécurité et vie privée d'abord** : jamais d'adresse du domicile, rendez-vous en lieu public, contrôle total de ce qu'on partage.
2. **Une seule ville au départ** : une communauté vide ne sert à rien, mieux vaut la densité dans un endroit.
3. **Simple d'abord** : publier, rejoindre, se retrouver. La messagerie interne vient après.
4. **Cohérent avec le reste** : la sortie communautaire est une sortie Miam Ride normale (tracé, pauses, partenaires, GPX).

## 3. Sécurité : ce que font d'autres applications

| Pratique | Qui la fait | Application chez nous |
|---|---|---|
| Masquer les 200 premiers et derniers mètres d'une activité par défaut, et pouvoir masquer toute la carte | Strava (source : TechRadar) | Le tracé public d'une sortie ne montre jamais le domicile : le départ est un **point de rendez-vous public** choisi par l'organisateur |
| Partager sa position en direct avec des proches par un lien | Strava Beacon, Garmin LiveTrack (source : TechRadar) | Option « Partager ma sortie avec un proche » avant de partir à la rencontre d'inconnus |
| Vérification de photo et d'identité | Bumble (source : support Bumble) | Profil « vérifié » (photo, puis pièce d'identité plus tard), requis pour **organiser** une sortie |
| Bloquer et signaler une personne, avec équipe de modération | Bumble (source : support Bumble) | Boutons Bloquer et Signaler sur chaque profil et chaque sortie, avec suivi par un humain |
| Échanger sans donner son numéro ou son e-mail | Bumble (appels dans l'application) | Messagerie dans l'application, ou lien d'un groupe WhatsApp créé par l'organisateur seulement une fois accepté |
| Règles de contenu claires (pas d'armes, pas de harcèlement) | Bumble | Charte de la communauté acceptée à l'inscription |
| Avis après usage (note des participants) | Type covoiturage (à vérifier pour le détail) | Avis après la sortie, visibles seulement des participants |

À ajouter propres au vélo : âge minimum à fixer (voir questions), sorties de nuit déconseillées par défaut, rappel du casque et du code de la route, numéro d'urgence accessible depuis la sortie.

## 4. Étapes

### Étape 0 : socle technique (prérequis)
- Comptes réels et connexion (Supabase), base de données partagée.
- Conditions d'utilisation, politique de confidentialité, RGPD (voir section 6).
- Application installable (PWA) ou application native pour les notifications.

### Étape 1 : proposer et rejoindre (premier produit utilisable)
- Publier une sortie : tracé Miam Ride, rendez-vous, date et heure, allure, niveau, nombre de places, description.
- Liste et carte des sorties de la ville, avec filtres (jour, distance, allure, niveau).
- Demande pour rejoindre, acceptation par l'organisateur.
- Annulation, modification, liste des participants.

### Étape 2 : se retrouver
- Notifications : nouvelle sortie à proximité, demande reçue ou acceptée, rappel la veille et une heure avant, changement ou annulation.
- Lien de groupe WhatsApp (ou autre) partagé avec les participants acceptés.
- Partage de la sortie avec un proche.

### Étape 3 : confiance
- Profil vérifié (photo, puis identité).
- Avis après la sortie, signalement, blocage, modération.
- Badges et XP de participation (cohérent avec le système existant).

### Étape 4 : vie de la communauté
- Messagerie dans l'application, fil de discussion par sortie.
- Groupes et clubs, sorties récurrentes (« tous les dimanches »).
- Partenariats boulangeries : arrêt de groupe annoncé à l'avance, avantage groupe.
- Ouverture à de nouvelles villes.

## 5. Ordre de travail proposé

1. Terminer les chantiers en cours (point d'eau, notation, mise à jour des documents).
2. Étape 0 (comptes, base, juridique) : c'est le gros morceau, commun à d'autres sujets.
3. Étape 1 sur une ville pilote avec quelques organisateurs connus.
4. Étapes 2 puis 3 avant toute ouverture publique large.
5. Étape 4 selon l'usage constaté.

## 6. Juridique et conformité (à valider avec un juriste)

- **RGPD** : localisation, liste des participants, messages. Base légale, durée de conservation, droit de suppression.
- **Responsabilité** : l'application met en relation, elle n'organise pas la sortie. Rédiger des conditions claires, avec rappel que chacun roule sous sa responsabilité. Vérifier l'assurance nécessaire pour la plateforme et le statut des sorties de club.
- **Mineurs** : âge minimum et consentement parental à définir.
- **Avis** : règles d'authenticité et de modération (voir aussi `questions-juridiques-notation.md`).
- **Modération** : obligations d'un hébergeur de contenu (retrait de contenus signalés).

## 7. Questions ouvertes

1. Sorties **publiques** ou **sur invitation** (amis, clubs) au démarrage ?
2. **Âge minimum** et vérification des profils (téléphone, pièce d'identité) ?
3. Les sorties de groupe donnent-elles des **avantages** (réductions groupées, XP en plus) ?
4. Qui **modère** (toi, une personne dédiée, un outil) et à quel rythme ?
5. Ville pilote et premiers organisateurs ?
6. Mesure du succès : nombre de sorties publiées par semaine, taux de participation, sorties répétées.

## 8. Risques principaux

| Risque | Réponse |
|---|---|
| Communauté trop petite au début | Une ville pilote, sorties amorcées par des clubs ou par toi |
| Rencontre avec une personne malveillante | Profils vérifiés, rendez-vous public, signalement et blocage, partage avec un proche |
| Données de localisation exposées | Pas de domicile, positions floutées, accord explicite |
| Charge de modération | Règles simples, signalement, outil de suivi dès l'étape 3 |
| Responsabilité en cas d'accident | Conditions d'utilisation, avis du juriste, assurance à vérifier |

## Sources

- TechRadar, « Four essential Strava safety features » : https://www.techradar.com/health-fitness/four-strava-safety-features-every-user-needs-to-know-about-including-you
- Support Bumble, « Our safety features » : https://support.bumble.com/hc/articles/28537051467293-Our-safety-features
