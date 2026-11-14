# Serveur Miam Ride (Supabase)

## Fonction `train-retour`
Reçoit une gare de départ et le point de départ du cycliste, demande à PRIM (Île-de-France Mobilités) les prochains trains, renvoie un résumé (heure du train, arrivée, durée, correspondances).

### Mise en place (une fois)
1. Supabase : créer un projet (connexion avec le compte GitHub du projet).
2. Installer la CLI : `npm i -g supabase`, puis `supabase login`.
3. Dans ce dossier : `supabase link --project-ref <réf du projet>`.
4. Secrets (le jeton PRIM ne s'écrit jamais dans un fichier) :
   `supabase secrets set PRIM_KEY=<ton jeton PRIM>`
5. Déployer : `supabase functions deploy train-retour`
6. Dans l'appli : Profil › Compte › « Horaires de trains », coller l'adresse de la fonction
   (`https://<réf>.supabase.co/functions/v1/train-retour`) et la clé « anon » du projet
   (Supabase › Project Settings › API › `anon public`).

### À vérifier dans PRIM
L'adresse exacte de l'API d'itinéraires (`PRIM_BASE`) : voir le « Playground » de la page API
« Calculateur Île-de-France Mobilités » sur prim.iledefrance-mobilites.fr.
Si elle diffère de la valeur par défaut : `supabase secrets set PRIM_BASE=<adresse>`.

### Limites
- Île-de-France seulement (Transilien, RER, bus, métro). Hors zone : réponse `hors_idf`.
- 30 requêtes par minute et par adresse IP ; quotas PRIM propres à ton compte.
- Les horaires ne sont jamais conservés.

## Base des boulangeries (`places`) : fonction `sync-places`
Charge les boulangeries d'OpenStreetMap dans Supabase pour que l'appli n'interroge plus Overpass (lent, souvent saturé).
Zone : Île-de-France + ~50 km de marge (lat 47,65–49,70 ; lng 0,85–4,20), découpée en 340 tuiles de ~14 × 13 km.

### Mise en place (une fois)
1. **Table et fonctions** : Supabase › SQL Editor › New query, coller le contenu de `sql/places.sql`, Run.
2. **Secret** : `supabase secrets set SYNC_KEY=<un mot de passe long que tu inventes>`
3. **Déployer** : `supabase functions deploy sync-places`
4. **Charger** (environ 10 à 20 minutes, à relancer au besoin) :
   `URL=https://<réf>.supabase.co ANON=<clé anon> SYNC=<SYNC_KEY> ./charger-places.sh`
   Le script traite 1 à 3 tuiles par appel, affiche chaque réponse et nettoie à la fin les lieux disparus d'OpenStreetMap.
   Si une tuile échoue (Overpass saturé), relance simplement le script : les lieux déjà chargés restent.
5. **Vérifier** : Supabase › Table Editor › `places` (≈ 12 000 à 15 000 lignes) ; dans le SQL Editor :
   `select * from places_near(48.8049, 2.1204, 3000);` doit renvoyer les boulangeries autour de Versailles.
6. **Rafraîchissement hebdomadaire** : relancer le script (ou le planifier plus tard avec pg_cron).
7. **Limite de lignes** : Supabase › Project Settings › API › « Max rows » : mettre 5000.

### Lecture par l'appli
- `rpc/places_near` (disque) et `rpc/places_near_path` (le long d'un tracé), avec la clé « anon ». Lecture publique, écriture réservée au serveur.
- Cafés : `./charger-places.sh cafe` charge les cafés nommés dans la même table (`kind = 'cafe'`).
