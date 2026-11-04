# Horaires d'ouverture et temps de roulage – Miam Ride

*Maquette réalisée le 30/10/2026. Horaires de démonstration (inventés, sur des noms de boulangeries réels) : en vrai ils viendront de Google Places.*

## Principe
Une boulangerie est jugée **à l'heure où le cycliste y passera**, pas à l'heure du départ. Exemple : départ à 8 h, la boulangerie ouvre à 8 h 30, le cycliste y arrive vers 9 h 20 → elle est proposée, avec la mention « Ouverte à ton passage (vers 9 h 20) · ouvre à 8 h 30 ».

## Ce que fait la maquette
- **Départ** : jour (aujourd'hui, demain… 7 jours) et heure, dans l'écran « Où t'arrêter ». Par défaut : maintenant arrondi au quart d'heure ; après 17 h, demain 8 h.
- **Heure de passage** = heure de départ + (km jusqu'à la pause ÷ vitesse) + durée des pauses précédentes.
- **Trois états** pour chaque boulangerie, avec une marge d'incertitude sur l'heure de passage :
  - **Ouverte** (vert) : ouverte pendant toute la fenêtre [passage − marge ; passage + marge].
  - **À vérifier** (orange) : ouverte seulement sur une partie de la fenêtre (ex. « ouvre à 8 h 30, tu passes vers 8 h 20 »). Elle reste proposée, avec l'avertissement.
  - **Fermée** (rouge) : fermée sur toute la fenêtre. Elle n'est pas proposée. Si toutes les boulangeries de la zone sont fermées, on les affiche quand même avec un message.
- **Récapitulatif** : heure de passage et état à chaque pause, puis « Départ 8 h · retour vers 10 h 55 (≈ 2 h 53 avec 1 pause) ».
- **Changer le départ** après avoir choisi : une pause devenue fermée est retirée, avec un message.
- **Mode Mamie, Carte** : mêmes règles. Sur la carte, la fiche affiche « Ouvert · ferme à 19 h » ou « Fermé · ouvre demain à 8 h 30 » et les horaires de la semaine ; les pastilles des boulangeries fermées **maintenant** sont grisées.
- **Espace boulangerie** : aucun éditeur d'horaires (retiré le 31/10, pour ne pas surcharger l'interface). Les horaires et fermetures viennent de Google ; la boulangerie les corrige sur sa fiche Google.

## Réglages (`HOURS_RULES`, en haut du bloc dans le code)
| Réglage | Valeur | Rôle |
|---|---|---|
| `speed` | 22 km/h | vitesse moyenne, pauses non comprises |
| `pauseMin` | 15 min | temps passé à chaque pause précédente |
| `margin` | ± 15 min | incertitude sur l'heure de passage |
| `closeBuffer` | 15 min | il faut être encore ouvert 15 min après le passage |

Les horaires de démonstration sont dans `HRS` (format « Mar-Sam 7:00-13:30,15:30-19:30; Dim 7:30-13:00 »), les fermetures exceptionnelles dans `HRS_EXC`.

## Pour la vraie version
- **Google Places** : champ `regularOpeningHours` (déjà demandé et converti par `gHours` dans le fournisseur Google, non testé) ; `currentOpeningHours` pour les jours fériés et fermetures exceptionnelles.
- **Source unique** : Google Places. Si un horaire est faux, la boulangerie le corrige sur sa fiche Google (ou notre équipe le signale), pas dans notre espace.
- **Vitesse** : à terme, calculer la vitesse moyenne du cycliste à partir de son historique (le réglage de 22 km/h est une moyenne de départ), et tenir compte du dénivelé du tracé.
- **Risque** : des horaires faux ou périmés (surtout en vacances) donnent un mauvais conseil. Prévoir un signalement « fermé quand je suis passé » et le retour dans la fiche.
- **Fuseau et jours fériés** : à gérer côté serveur.
