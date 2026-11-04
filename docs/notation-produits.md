# Notation des produits après passage – Miam Ride

*Maquette réalisée le 29/10/2026. Les règles « en vrai » ci-dessous sont à valider avant le lancement.*

## Ce que fait la maquette
- **Validation du passage : toujours avec le téléphone, par QR code**, même si le cycliste roule avec une montre ou un GPS (leurs API ne permettent pas de valider un passage). Pendant une sortie lancée dans l'appli, bouton « Valider mon passage ». Pour un tracé envoyé sur la montre, onglet Historique > « Tracés à rouler » : bouton « Je suis chez … » pour chaque pause.
- **La notation est proposée à la fin du tracé** : après l'écran « Sortie validée » (sortie venant de la montre) ou sur la carte « Noter mes pauses » de l'écran de fin (sortie lancée dans l'appli). Seules les boulangeries dont le passage a été validé par QR peuvent être notées. Un lien « Noter » reste disponible pendant la sortie.
- La fenêtre « Ton avis » demande : « Tu as pris quoi chez … ? »
- Le cycliste choisit un produit (pastilles : flan, croissant, pain au chocolat, éclair, tarte, baguette tradition, sandwich, plus « Autre… » pour mille-feuille, chausson aux pommes, macaron, religieuse, Paris-Brest), puis une note de 1 à 5.
- Bouton « Plus tard » : l'arrêt garde un lien « Noter » dans la liste des arrêts de la sortie en cours.
- Récompense : +5 XP par avis envoyé.
- L'avis est enregistré sur l'appareil. Quand on cherche ce produit dans la liste des boulangeries, la fiche affiche « ton avis : 5/5 ». Le profil compte les avis donnés.
- Espace boulangerie, onglet Passages : bloc « Avis des cyclistes » (vide en démo, avec l'explication du fonctionnement).
- Aucune note d'autres utilisateurs n'est affichée : pas de faux chiffres attachés à de vrais commerces.

## Règles proposées pour la vraie version
1. **Un avis par passage validé.** Seul un passage validé par QR (position vérifiée) donne le droit de noter. C'est ce qui évite les faux avis.
2. **Un seul avis par produit et par boulangerie et par jour** pour un même cycliste, avec modification possible pendant 24 h.
3. **Seuil d'affichage.** Un produit n'est classé dans une boulangerie qu'à partir d'un nombre minimal d'avis (par exemple 5). Avant, on affiche « pas assez d'avis » et la boulangerie reste listée comme proposant le produit.
4. **Score pondéré.** Moyenne ramenée vers une note de référence quand il y a peu d'avis, pour qu'une note de 5 donnée par 2 personnes ne passe pas devant 4,7 donné par 40 personnes. Formule de la maquette : (note × avis + 4 × 5) / (avis + 5).
5. **Le commerce ne peut ni supprimer ni modifier un avis.** Il peut en signaler un (propos injurieux, produit qui n'existe pas) pour modération.
6. **Bouton « Signaler »** sur chaque avis, et modération minimale avant affichage de textes libres. En version 1, pas de texte libre : produit + note seulement.
7. **Anti-abus XP.** Les +5 XP sont limités (un avis récompensé par passage, plafond par mois) pour éviter de noter pour gagner de l'XP.
8. **Données personnelles.** Les avis affichés à la boulangerie sont anonymisés (pas de nom). À valider avec les règles RGPD du projet.

## Confirmation par les cyclistes et classement par produit (ajouté le 29/10)
- **Les avis servent trois choses** : la note du produit, la confirmation de l'offre de la boulangerie, et le classement « Meilleur flan du secteur ».
- **Offre confirmée** : un produit déclaré par la boulangerie est « confirmé par les cyclistes » à partir de 3 avis. Un produit absent de sa liste mais cité par 3 avis est « ajouté par les cyclistes » (et apparaît dans la recherche par produit).
- **Note affichée** à partir de 5 avis : « 4,6/5 (12 avis) ». Avant : « pas encore assez d'avis ». Seuils réglables (`CONF_MIN`, `REV_MIN` dans le code).
- **Classement** : avec un produit choisi, les partenaires restent d'abord, puis tri par score pondéré (seulement ceux qui ont au moins 5 avis), puis note générale. Badge « Meilleur/Meilleure … du secteur » pour le premier au-dessus du seuil.
- **Un avis par produit, par boulangerie et par jour** : un second avis le même jour met à jour le premier, sans nouvelle XP.
- **Fiche de la carte** : liste « Produits et avis des cyclistes » de la boulangerie.
- **Avis simulés (démo)** : par défaut, la maquette ne compte que tes propres avis. Réglage Profil > « Démo : avis simulés d'autres cyclistes » pour afficher des chiffres d'exemple (clairement indiqués), car sans autres utilisateurs aucun seuil n'est atteint. Ces chiffres sont fictifs, même sur des noms de boulangeries réels.
- **Règles réglables (ajouté le 29/10)** : tout est dans un seul objet `AVIS_RULES` en haut du code de l'appli (à affiner avec le temps) :

| Réglage | Valeur actuelle | Rôle |
|---|---|---|
| `confMin` | 3 | avis pour confirmer ou ajouter un produit |
| `revMin` | 5 | avis avant d'afficher une note et de classer |
| `priorNote` / `priorWeight` | 4 / 5 | score pondéré (note de référence et poids) |
| `onePerDay` | oui | un avis par produit, boulangerie et jour |
| `xpPerReview` | 5 | XP par avis |
| `xpMonthlyCap` | 20 | avis récompensés par mois au maximum |
| `reportHideAt` | 3 | signalements avant masquage automatique (version serveur, pas actif en démo) |
| `replyMax` | 280 | longueur de la réponse d'une boulangerie |
| `anonymous` | oui | avis anonymes côté boulangerie |

- **Espace boulangerie (démo)** : onglet Passages, 5 avis d'exemple (produit + note, sans nom). La boulangerie peut **répondre** (280 caractères, modifiable) et **signaler** un avis avec un motif ; l'avis reste visible jusqu'à la décision. Elle ne peut ni le supprimer ni le modifier. Un encadré « Règles des avis » résume les réglages (les valeurs y sont écrites à la main, à tenir à jour avec `AVIS_RULES`).
- **Plafond d'XP** : au-delà de 20 avis dans le mois, un avis est enregistré mais ne rapporte plus d'XP (message à l'envoi).
- **Pas encore fait (version serveur)** : file de modération et décisions, masquage automatique après `reportHideAt` signalements, anonymisation réelle des données, contrôle de cohérence avancé, bouton « Signaler » côté cyclistes (les avis des autres ne sont pas affichés individuellement). Reste dans « Anti-abus et modération ».

## À faire ensuite
- Brancher les vrais classements par produit : « Meilleur flan du secteur » quand le seuil d'avis est atteint.
- Côté boulangerie : statistiques par produit (avis reçus, note moyenne, évolution).

## Notification d'approche à 500 m (ajoutée le 29/10)
- Quand le cycliste arrive à moins de 500 m d'une boulangerie de son tracé, l'appli envoie une notification : « Maison Renaissance dans 500 m. Prépare ton QR code Poulidor, c'est l'heure de se régaler » Le bouton ouvre directement le QR code.
- Une seule notification par boulangerie et par sortie. Seules les boulangeries partenaires sont concernées (les autres n'ont pas de QR).
- Réglage dans le profil : « Alerte à 500 m d'une boulangerie » (activée par défaut).
- **Dans la maquette :** pendant une sortie lancée dans l'appli, la notification se déclenche toute seule avec la simulation de position ; pour un tracé envoyé sur la montre, le lien « Démo : j'approche de la prochaine boulangerie (500 m) » la simule.
- **En vrai :** la détection ne peut pas venir de la montre ni du GPS vélo (pas d'accès en direct à leur position sans API partenaire). Elle vient de la position du téléphone : à l'envoi du tracé, l'appli enregistre un périmètre de 500 m autour de chaque boulangerie (géorepérage), et le système du téléphone la réveille à l'entrée du périmètre, même appli fermée. Prérequis : le cycliste emporte son téléphone et autorise la localisation « toujours » et les notifications. À prévoir dans les conditions d'utilisation et la politique de confidentialité.
