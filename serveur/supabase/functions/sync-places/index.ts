// Miam Ride : charge les boulangeries (ou cafés) d'OpenStreetMap dans la table `places`.
// Zone : Île-de-France + environ 50 km de marge. Découpée en tuiles ; chaque appel traite quelques tuiles
// (une fonction Supabase s'arrête après ~2 minutes). Le script serveur/charger-places.sh enchaîne les appels.
// Secrets attendus : SYNC_KEY (mot de passe du chargement). SUPABASE_URL et SUPABASE_SERVICE_ROLE_KEY existent déjà.
import { createClient } from "npm:@supabase/supabase-js@2";

const OVP = [
  "https://overpass-api.de/api/interpreter",
  "https://overpass.kumi.systems/api/interpreter",
  "https://overpass.private.coffee/api/interpreter",
  "https://overpass.openstreetmap.fr/api/interpreter",
];
const ZONE = { latMin: 47.65, latMax: 49.7, lngMin: 0.85, lngMax: 4.2 };
const STEP_LAT = 0.25, STEP_LNG = 0.35;
const CORS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, apikey, content-type, x-client-info, x-sync-key",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
};
const json = (o: unknown, status = 200) =>
  new Response(JSON.stringify(o), { status, headers: { ...CORS, "Content-Type": "application/json" } });

const tiles: { s: number; w: number; n: number; e: number }[] = [];
for (let la = ZONE.latMin; la < ZONE.latMax - 1e-9; la += STEP_LAT)
  for (let ln = ZONE.lngMin; ln < ZONE.lngMax - 1e-9; ln += STEP_LNG)
    tiles.push({ s: la, w: ln, n: Math.min(la + STEP_LAT, ZONE.latMax), e: Math.min(ln + STEP_LNG, ZONE.lngMax) });

const filtre = (kind: string) => kind === "cafe" ? `["amenity"="cafe"]["name"]` : `["shop"="bakery"]`;

async function overpass(q: string): Promise<any[]> {
  let last = "";
  for (let tour = 0; tour < 2; tour++) {
    for (const u of OVP) {
      try {
        const r = await fetch(u, {
          method: "POST",
          headers: { "Content-Type": "application/x-www-form-urlencoded" },
          body: "data=" + encodeURIComponent(q),
          signal: AbortSignal.timeout(45000),
        });
        if (!r.ok) { last = `Overpass ${r.status}`; continue; }
        const j = await r.json();
        if (j.remark && /error|timed out|memory/i.test(j.remark) && !(j.elements ?? []).length) { last = "Overpass surchargé"; continue; }
        return j.elements ?? [];
      } catch (e) { last = String((e as Error).message ?? e); }
    }
    await new Promise((res) => setTimeout(res, 2000));
  }
  throw new Error(last || "Overpass injoignable");
}

function toRow(e: any, kind: string) {
  const t = e.tags ?? {};
  const lat = e.lat ?? e.center?.lat, lng = e.lon ?? e.center?.lon;
  if (lat == null || lng == null) return null;
  const addr = [[t["addr:housenumber"], t["addr:street"]].filter(Boolean).join(" "), t["addr:city"]].filter(Boolean).join(", ");
  return {
    id: `${e.type}/${e.id}`, kind, name: t.name ?? (kind === "cafe" ? "Café" : "Boulangerie"),
    addr: addr || null, lat, lng, hours: t.opening_hours ?? null, seen_at: new Date().toISOString(),
  };
}

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response(null, { headers: CORS });
  if (req.method !== "POST") return json({ ok: false, reason: "methode" }, 405);
  const KEY = Deno.env.get("SYNC_KEY") ?? "";
  if (!KEY) return json({ ok: false, reason: "serveur_non_configure" }, 500);
  if (req.headers.get("x-sync-key") !== KEY) return json({ ok: false, reason: "cle_refusee" }, 403);

  let b: any;
  try { b = await req.json(); } catch { return json({ ok: false, reason: "json" }, 400); }
  const kind = b?.kind === "cafe" ? "cafe" : "bakery";
  const db = createClient(Deno.env.get("SUPABASE_URL")!, Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!);

  // Fin de chargement : on supprime les lieux qui n'existent plus dans OpenStreetMap.
  if (b?.action === "purge") {
    const before = String(b?.before ?? "");
    if (!/^\d{4}-\d{2}-\d{2}T/.test(before)) return json({ ok: false, reason: "parametres" }, 400);
    const { error, count } = await db.from("places").delete({ count: "exact" }).eq("kind", kind).lt("seen_at", before);
    if (error) return json({ ok: false, reason: "base", detail: error.message }, 500);
    return json({ ok: true, supprimes: count ?? 0 });
  }

  const from = Math.max(0, Math.floor(Number(b?.from ?? 0)));
  const count = Math.min(6, Math.max(1, Math.floor(Number(b?.count ?? 3))));
  const fait: { tuile: number; lieux: number }[] = [], echecs: { tuile: number; erreur: string }[] = [];
  for (let i = from; i < Math.min(from + count, tiles.length); i++) {
    const t = tiles[i], bb = `${t.s.toFixed(4)},${t.w.toFixed(4)},${t.n.toFixed(4)},${t.e.toFixed(4)}`;
    const f = filtre(kind);
    const q = `[out:json][timeout:40];(node${f}(${bb});way${f}(${bb}););out center tags;`;
    try {
      const rows = (await overpass(q)).map((e) => toRow(e, kind)).filter(Boolean) as any[];
      for (let k = 0; k < rows.length; k += 500) {
        const { error } = await db.from("places").upsert(rows.slice(k, k + 500), { onConflict: "id" });
        if (error) throw new Error("base : " + error.message);
      }
      fait.push({ tuile: i, lieux: rows.length });
    } catch (e) { echecs.push({ tuile: i, erreur: String((e as Error).message ?? e) }); }
  }
  const next = Math.min(from + count, tiles.length);
  return json({ ok: true, done: next >= tiles.length, next, total: tiles.length, fait, echecs });
});
