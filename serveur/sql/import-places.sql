-- Miam Ride : permet à la page « charger-boulangeries.html » d'enregistrer les lieux dans la table `places`.
-- À coller dans Supabase › SQL Editor › New snippet › Run (après places.sql).
-- ⚠ Remplace MOT_DE_PASSE_A_CHOISIR (ligne « insert into ») par un mot de passe long, sans espace.

create table if not exists public.app_secrets (name text primary key, value text not null);
alter table public.app_secrets enable row level security;   -- aucune règle : illisible depuis l'extérieur

insert into public.app_secrets (name, value) values ('IMPORT_KEY', 'MOT_DE_PASSE_A_CHOISIR')
on conflict (name) do update set value = excluded.value;

create or replace function public.import_places(p_key text, p_kind text, p_rows jsonb)
returns int language plpgsql security definer set search_path = public as $$
declare n int;
begin
  if p_key is distinct from (select value from app_secrets where name = 'IMPORT_KEY') then raise exception 'cle_refusee'; end if;
  if p_kind not in ('bakery', 'cafe') then raise exception 'type_inconnu'; end if;
  insert into places (id, kind, name, addr, lat, lng, hours, seen_at)
  select r->>'id', p_kind, coalesce(nullif(r->>'name', ''), 'Boulangerie'), r->>'addr',
         (r->>'lat')::double precision, (r->>'lng')::double precision, r->>'hours', now()
  from jsonb_array_elements(p_rows) r
  where r->>'id' is not null and r->>'lat' is not null and r->>'lng' is not null
  on conflict (id) do update set name = excluded.name, addr = excluded.addr, lat = excluded.lat,
                                 lng = excluded.lng, hours = excluded.hours, seen_at = now();
  get diagnostics n = row_count;
  return n;
end $$;

create or replace function public.purge_places(p_key text, p_kind text, p_before timestamptz)
returns int language plpgsql security definer set search_path = public as $$
declare n int;
begin
  if p_key is distinct from (select value from app_secrets where name = 'IMPORT_KEY') then raise exception 'cle_refusee'; end if;
  delete from places where kind = p_kind and seen_at < p_before;
  get diagnostics n = row_count;
  return n;
end $$;
