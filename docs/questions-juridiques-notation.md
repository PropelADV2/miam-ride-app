# Questions juridiques : notation des boulangeries

*Créé le 4 novembre 2026. Statut : en attente d'un avis juridique. À remplir au retour du juriste.*

## Contexte

Miam Ride passe en full OpenStreetMap (tracés, boulangeries, carte). OpenStreetMap ne fournit **aucune note ni avis**. Nous voulons ne proposer que de bonnes boulangeries. Les pistes envisagées :

1. Statuts internes : « validée par nous », « notée par les cyclistes » (QR), « non vérifiée ».
2. Notes de nos propres utilisateurs, après la pause, par scan du QR de la boulangerie.
3. Éventuellement, la note Google (API officielle, payante) pour amorcer au lancement.

Ce qu'il ne faut pas faire sans avis : recopier les notes Google dans notre base ou appliquer une règle mécanique du type « validée si ≥ 4/5 sur Google ».

Estimation de coût de l'API Google (à confirmer sur la page officielle) : environ 20 $ pour 1 000 consultations de fiche avec note, soit environ 10 à 30 $ par ville pour une passe d'amorçage.

## Les 3 questions

### Question 1. Consultation manuelle de Google
Peut-on consulter à la main la note Google d'une boulangerie comme **un critère parmi d'autres** pour la marquer « validée » dans notre application, **sans enregistrer** la note ni les avis, en ne gardant que notre décision (validée ou à éviter) et une courte note interne ?

**Réponse du juriste :**

**Date et source :**

---

### Question 2. API officielle de Google
Peut-on afficher la note Google dans l'application via l'API officielle (Google Places) avec la mention de Google, et sous quelles conditions ?
- Affichage sur une carte non Google : autorisé ou non ?
- Conservation de la note dans notre base : autorisée ou non, et pour combien de temps ?
- Utilisation de la note pour filtrer ou classer les établissements (seuil 4/5, par exemple) : autorisée ?

**Réponse du juriste :**

**Date et source :**

---

### Question 3. Avis de nos propres utilisateurs
Quelles mentions légales et quelles conditions d'utilisation faut-il pour afficher les avis de nos utilisateurs (notes QR) ?
- Obligations d'information sur l'authenticité et la modération des avis (règles françaises et européennes sur les avis en ligne).
- Droit de réponse ou de contestation pour les établissements notés.
- Données personnelles (RGPD) : pseudonymat, durée de conservation, base légale.

**Réponse du juriste :**

**Date et source :**

---

## Décision finale

- [ ] Statuts internes + notes QR seulement
- [ ] Statuts internes + notes QR + Google officiel pour amorcer
- [ ] Autre : ________________

**Décidé le :** ________  **Par :** ________

## Impact sur le code (version 13)

Rien ne dépend de la réponse : la version 13 prévoit des statuts par boulangerie (validée, notée par les cyclistes, non vérifiée) et des seuils réglables. Une fois la décision prise, on branche la source de notes choisie sans refaire le reste.
