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
