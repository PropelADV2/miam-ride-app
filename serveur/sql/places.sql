-- Miam Ride : base des lieux (boulangeries, plus tard cafés...), chargée depuis OpenStreetMap.
-- À coller une fois dans Supabase › SQL Editor › New query › Run.

create table if not exists public.places (
  id        text primary key,                 -- identifiant OpenStreetMap, ex. 'node/123456'
  kind      text not null default 'bakery',   -- 'bakery' ou 'cafe'
  name      text not null,
  addr      text,
  lat       double precision not null,
  lng       double precision not null,
  hours     text,                              -- opening_hours d'OpenStreetMap, tel quel
  status    text not null default 'non_verifiee', -- 'non_verifiee' | 'validee' | 'notee' (voir questions-juridiques-notation.md)
  seen_at   timestamptz not null default now() -- dernière fois vue dans OpenStreetMap
);
create index if not exists places_geo  on public.places (kind, lat, lng);
create index if not exists places_seen on public.places (kind, seen_at);

-- Lecture publique (la clé « anon » de l'appli peut lire), écriture réservée au serveur.
alter table public.places enable row level security;
drop policy if exists "lecture publique" on public.places;
create policy "lecture publique" on public.places for select using (true);

-- Lieux autour d'un point (disque).
create or replace function public.places_near(p_lat double precision, p_lng double precision, p_radius_m int, p_kind text default 'bakery')
returns table (id text, kind text, name text, addr text, lat double precision, lng double precision, hours text, status text)
language sql stable as $$
  select p.id, p.kind, p.name, p.addr, p.lat, p.lng, p.hours, p.status
  from public.places p
  where p.kind = p_kind
    and p.lat between p_lat - p_radius_m / 110570.0 and p_lat + p_radius_m / 110570.0
    and p.lng between p_lng - p_radius_m / (111320.0 * cos(radians(p_lat))) and p_lng + p_radius_m / (111320.0 * cos(radians(p_lat)))
    and power((p.lat - p_lat) * 110570.0, 2) + power((p.lng - p_lng) * 111320.0 * cos(radians(p_lat)), 2) <= power(p_radius_m, 2)
$$;

-- Lieux le long d'un tracé : p_pts = [{"lat":48.8,"lng":2.1}, ...] (quelques dizaines de points).
create or replace function public.places_near_path(p_pts jsonb, p_radius_m int, p_kind text default 'bakery')
returns table (id text, kind text, name text, addr text, lat double precision, lng double precision, hours text, status text)
language sql stable as $$
  with q as (select (e->>'lat')::double precision as lat, (e->>'lng')::double precision as lng from jsonb_array_elements(p_pts) e),
       b as (select min(lat) as s, max(lat) as n, min(lng) as w, max(lng) as e, avg(lat) as m from q)
  select p.id, p.kind, p.name, p.addr, p.lat, p.lng, p.hours, p.status
  from public.places p, b
  where p.kind = p_kind
    and p.lat between b.s - p_radius_m / 110570.0 and b.n + p_radius_m / 110570.0
    and p.lng between b.w - p_radius_m / (111320.0 * cos(radians(b.m))) and b.e + p_radius_m / (111320.0 * cos(radians(b.m)))
    and exists (
      select 1 from q
      where power((p.lat - q.lat) * 110570.0, 2) + power((p.lng - q.lng) * 111320.0 * cos(radians(q.lat)), 2) <= power(p_radius_m, 2)
    )
$$;
