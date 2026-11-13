#!/usr/bin/env bash
# Charge toutes les boulangeries de la zone (Île-de-France + marge) dans Supabase.
# Usage : URL=https://<réf>.supabase.co ANON=<clé anon> SYNC=<SYNC_KEY> ./charger-places.sh [bakery|cafe]
set -u
KIND="${1:-bakery}"
: "${URL:?URL manquante}" "${ANON:?ANON manquante}" "${SYNC:?SYNC manquante}"
F="$URL/functions/v1/sync-places"
START=$(date -u +%Y-%m-%dT%H:%M:%SZ)
i=0; FAILS=""
while true; do
  R=$(curl -sS -m 170 -X POST "$F" -H "Authorization: Bearer $ANON" -H "apikey: $ANON" -H "x-sync-key: $SYNC" \
      -H "Content-Type: application/json" -d "{\"kind\":\"$KIND\",\"from\":$i,\"count\":3}")
  echo "$R"
  case "$R" in *'"ok":true'*) ;; *) echo "Erreur : arrêt (relance depuis la tuile $i avec FROM=$i)"; exit 1;; esac
  case "$R" in *'"echecs":[]'*) ;; *) FAILS="$FAILS $i";; esac
  case "$R" in *'"done":true'*) break;; esac
  i=$(echo "$R" | sed -n 's/.*"next":\([0-9]*\).*/\1/p')
  [ -z "$i" ] && { echo "Réponse inattendue"; exit 1; }
done
if [ -n "$FAILS" ]; then
  echo "Des tuiles ont échoué (appels commençant à :$FAILS). Relance le script : les lieux déjà chargés ne sont pas perdus. Pas de nettoyage."; exit 2
fi
curl -sS -X POST "$F" -H "Authorization: Bearer $ANON" -H "apikey: $ANON" -H "x-sync-key: $SYNC" \
  -H "Content-Type: application/json" -d "{\"kind\":\"$KIND\",\"action\":\"purge\",\"before\":\"$START\"}"; echo
echo "Terminé."
