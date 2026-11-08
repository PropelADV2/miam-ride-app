# Critères de génération des tracés Miam Ride

Document de référence (version vivante : https://claude.ai/artifact/HBYAT2Wu9fUC1Tc4qZ37G1). Dernière mise à jour : 2026-10-23. Les valeurs chiffrées sont des propositions à calibrer sur de vrais tracés.

## Les trois ambiances
Le moteur minimise un « coût » et non la distance : chaque ambiance change le coût de chaque type de route et le détour accepté pour rester au calme. La distance totale reste celle du curseur (± 5 km) : le détour ne s'y ajoute jamais, il fixe seulement jusqu'où on peut allonger un passage entre deux points. Pour « Le plus rapide », le rallongement maximal de 8 km pour une boulangerie reste la règle.

| | Routes très calmes | Calmes, avec quelques axes | Le plus direct |
| --- | --- | --- | --- |
| Principe | Petites routes d'abord | Compromis, par défaut | Itinéraire efficace |
| Détour max par tronçon vs son trajet le plus court | +20 % | +10 % | 0 % |
| Routes principales | Évitées sauf traversée < 500 m | Autorisées si < 2 km consécutifs | Autorisées |
| Routes très chargées (> 10 000 véh./jour) | Exclues | Exclues | Évitées sauf impasse |
| Autoroutes et voies express | Exclues | Exclues | Exclues |
| Part visée de routes calmes | ≥ 85 % | ≥ 65 % | ≥ 45 % |
| Virages et carrefours | Plus nombreux, acceptés | Moyens | Minimisés |

Une « route calme » = route à faible trafic estimé. OpenStreetMap ne donne pas le trafic réel : le pourcentage affiché est une estimation.

## Coût par type de route (balise OSM `highway`)
1,0 = neutre, plus c'est haut, plus on évite.

| Type de route | Exemple | Très calmes | Quelques axes | Direct |
| --- | --- | --- | --- | --- |
| cycleway, voie verte | Voie verte, piste | 0,9 | 0,95 | 1,1 |
| residential, unclassified, service | Route de village | 1,0 | 1,0 | 1,1 |
| tertiary | D secondaire | 1,0 | 1,1 | 1,1 |
| secondary | D principale | 1,8 | 1,3 | 1,1 |
| primary | Nationale, grosse D | 4,0 | 2,2 | 1,4 |
| trunk | Voie rapide 2x2 | Exclu | Exclu | 3,0 |
| motorway | Autoroute | Exclu | Exclu | Exclu |
| track, chemin non revêtu | Piste | Exclu | Exclu | Exclu |

Bonus : aménagement cyclable (bande, accotement large) = ×0,85 sur secondary et primary.

## Trafic réel des routes
Une nationale d'Île-de-France n'a pas la fréquentation d'une nationale bretonne : le moteur utilise les comptages quand ils existent, le type de route en secours.

| Trafic moyen par jour (TMJA) | Classe | Coefficient |
| --- | --- | --- |
| < 1 500 | Calme | 1,0 |
| 1 500 à 5 000 | Moyen | ×1,3 |
| 5 000 à 10 000 | Chargé | ×2,0 |
| > 10 000 | Très chargé | Exclu (Très calmes, Quelques axes), évité sauf impasse (Direct) |

Le comptage remplace le coefficient du type de route et se combine avec la vitesse autorisée. Sans comptage : estimation selon le type de route et la proximité d'une grande ville. Sources à vérifier : jeux TMJA sur data.gouv.fr (https://www.data.gouv.fr/datasets/d30-tmja) et comptages départementaux/régionaux ; couverture, fraîcheur et licence à confirmer par région ; moyenne annuelle, pas l'heure de pointe.

## Autres critères
| Critère | Donnée OSM | Règle |
| --- | --- | --- |
| Vitesse autorisée | maxspeed | ≤ 50 : neutre. 70-80 : ×1,2. 90 : ×1,6. > 90 : ×2,5 (Direct : ×1,3) |
| Revêtement | surface, smoothness | Asphalte/béton : neutre. Pavés : ×1,8 (exclus en Très calmes si > 300 m). Gravier, terre : exclus |
| Aménagement cyclable | cycleway, bicycle | Bande/piste : ×0,85. Interdit aux vélos : exclu |
| Carrefours et feux | traffic_signals, ronds-points | Feu : +20 m. Rond-point : +10 m. Traversée route principale sans feu : +60 m |
| Dénivelé | Altitude (MNT) | Pente > 10 % sur > 300 m : ×1,5 |
| Sens interdit, travaux | oneway | Toujours respectés |
| Pause | Zone de 35 à 65 % du trajet | Boulangerie dans cette fenêtre |

## À valider et à calibrer
- [ ] Valider les trois ambiances et leurs détours (+20 %, +10 %, 0 %)
- [ ] Confirmer que les routes très chargées restent exclues même en « Le plus direct » (hors impasse)
- [ ] Choisir la région de test (moteur et coefficients réglés dessus)
- [ ] Préciser si le pavé est acceptable
- [ ] Décider d'un niveau de relief séparé (plat, vallonné, montagne)

Méthode : générer 10 boucles par ambiance dans la région, les faire juger par des cyclistes locaux, corriger les coefficients jusqu'à un classement cohérent des ambiances.
