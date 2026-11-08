// Miam Ride : horaires de retour en train (Île-de-France) via PRIM / Île-de-France Mobilités.
// Le jeton PRIM reste ici, dans les secrets Supabase : jamais dans l'appli.
// Secrets attendus : PRIM_KEY (obligatoire), PRIM_BASE (facultatif).
// PRIM_BASE par défaut : https://prim.iledefrance-mobilites.fr/marketplace/v2/navitia
// (à confirmer dans le « Playground » de PRIM : l'adresse exacte de l'API d'itinéraires).

const BASE = Deno.env.get("PRIM_BASE") ?? "https://prim.iledefrance-mobilites.fr/marketplace/v2/navitia";
const KEY = Deno.env.get("PRIM_KEY") ?? "";
const CORS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, apikey, content-type, x-client-info",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
};
// Île-de-France (rectangle large) : hors de cette zone on ne répond pas.
const IDF = { latMin: 48.1, latMax: 49.25, lngMin: 1.45, lngMax: 3.6 };
const inIdf = (p: { lat: number; lng: number }) =>
  p.lat >= IDF.latMin && p.lat <= IDF.latMax && p.lng >= IDF.lngMin && p.lng <= IDF.lngMax;

const json = (o: unknown, status = 200) =>
  new Response(JSON.stringify(o), { status, headers: { ...CORS, "Content-Type": "application/json" } });

// Limite simple par adresse IP : 30 requêtes par minute.
const hits = new Map<string, number[]>();
function limited(ip: string) {
  const now = Date.now();
  const l = (hits.get(ip) ?? []).filter((t) => now - t < 60000);
  l.push(now);
  hits.set(ip, l);
  return l.length > 30;
}
const num = (v: unknown) => (typeof v === "number" && isFinite(v) ? v : NaN);
const parseDt = (s: string) => { // "20261108T175500" -> minutes depuis minuit + date "2026-11-08"
  const m = /^(\d{4})(\d{2})(\d{2})T(\d{2})(\d{2})/.exec(s);
  if (!m) return null;
  return { date: `${m[1]}-${m[2]}-${m[3]}`, min: +m[4] * 60 + +m[5] };
};

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response(null, { headers: CORS });
  if (req.method !== "POST") return json({ ok: false, reason: "methode" }, 405);
  if (!KEY) return json({ ok: false, reason: "serveur_non_configure" }, 500);
  const ip = req.headers.get("x-forwarded-for")?.split(",")[0] ?? "?";
  if (limited(ip)) return json({ ok: false, reason: "trop_de_requetes" }, 429);

  let b: any;
  try { b = await req.json(); } catch { return json({ ok: false, reason: "json" }, 400); }
  const from = { lat: num(b?.from?.lat), lng: num(b?.from?.lng) };
  const to = { lat: num(b?.to?.lat), lng: num(b?.to?.lng) };
  const dt = String(b?.datetime ?? ""); // "2026-11-08T17:55" (heure de Paris)
  if (isNaN(from.lat) || isNaN(from.lng) || isNaN(to.lat) || isNaN(to.lng) || !/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}$/.test(dt))
    return json({ ok: false, reason: "parametres" }, 400);
  if (!inIdf(from) || !inIdf(to)) return json({ ok: false, reason: "hors_idf" });

  const nav = dt.replace(/[-:]/g, "") + "00"; // 20261108T175500
  const url = `${BASE}/journeys?from=${from.lng};${from.lat}&to=${to.lng};${to.lat}` +
    `&datetime=${nav}&datetime_represents=departure&min_nb_journeys=5&count=6&data_freshness=realtime`;
  let r: Response;
  try { r = await fetch(url, { headers: { apiKey: KEY, Accept: "application/json" } }); }
  catch { return json({ ok: false, reason: "prim_injoignable" }, 502); }
  if (r.status === 401 || r.status === 403) return json({ ok: false, reason: "cle_refusee" }, 502);
  if (r.status === 429) return json({ ok: false, reason: "quota_prim" }, 429);
  if (!r.ok && r.status !== 404) return json({ ok: false, reason: "prim_" + r.status }, 502);
  const d = await r.json().catch(() => null);
  const J = Array.isArray(d?.journeys) ? d.journeys : [];
  if (!J.length) return json({ ok: true, trajets: [] });

  const trajets = J.map((j: any) => {
    const S: any[] = j.sections ?? [];
    const pt = S.filter((s) => s.type === "public_transport");
    const dep = parseDt(pt[0]?.departure_date_time ?? j.departure_date_time);
    const arr = parseDt(j.arrival_date_time);
    return {
      depart_gare: dep, // heure du premier train (date + minutes)
      arrivee: arr,
      duree_min: Math.round((j.duration ?? 0) / 60),
      correspondances: j.nb_transfers ?? Math.max(0, pt.length - 1),
      depart_trajet: parseDt(j.departure_date_time),
      etapes: S.filter((x) => x.type !== "crow_fly" && (x.duration ?? 0) > 0).map((x) => ({
        type: x.type, // public_transport, street_network, transfer, waiting
        mode: x.mode ?? x.transfer_type ?? "",
        de: x.from?.name ?? "",
        a: x.to?.name ?? "",
        min: Math.round((x.duration ?? 0) / 60),
        mode_tc: x.display_informations?.commercial_mode ?? "",
        ligne: x.display_informations?.code ?? "",
        reseau: x.display_informations?.network ?? "",
      })),
      lignes: pt.map((s) => ({
        mode: s.display_informations?.commercial_mode ?? "",
        ligne: s.display_informations?.code ?? s.display_informations?.label ?? "",
        reseau: s.display_informations?.network ?? "",
      })),
    };
  }).filter((t: any) => t.depart_gare && t.arrivee);
  // un seul trajet par heure de départ, du plus tôt au plus tard
  const vus = new Set<string>();
  const uniques = trajets
    .sort((x: any, y: any) => (x.depart_gare.date + x.depart_gare.min.toString().padStart(4, "0")).localeCompare(y.depart_gare.date + y.depart_gare.min.toString().padStart(4, "0")))
    .filter((t: any) => { const k = t.depart_gare.date + t.depart_gare.min; if (vus.has(k)) return false; vus.add(k); return true; });
  return json({ ok: true, trajets: uniques });
});
