-- Durable arrival queue; Storage events enqueue before attempting a wake-up.
create table if not exists public.technician_inbox_queue (
 id uuid primary key default gen_random_uuid(),
 object_key text not null,
 object_version text not null,
 status text not null default 'PENDING',
 attempt integer not null default 0,
 lease_token uuid,
 lease_until timestamptz,
 available_at timestamptz not null default now(),
 last_error text,
 created_at timestamptz not null default now(),
 updated_at timestamptz not null default now(),
 unique(object_key,object_version)
);
alter table public.technician_inbox_queue enable row level security;
revoke all on public.technician_inbox_queue from anon,authenticated;
grant all on public.technician_inbox_queue to service_role;
create or replace function public.reconcile_technician_inbox() returns void
language sql security invoker set search_path=public as $$
 insert into public.technician_inbox_queue(object_key,object_version)
 select name,coalesce(version,id::text) from storage.objects where bucket_id='source-inbox'
 on conflict do nothing;
$$;
create or replace function public.claim_technician_inbox() returns setof public.technician_inbox_queue
language sql security invoker set search_path=public as $$
 update public.technician_inbox_queue q set status='PROCESSING',attempt=attempt+1,
 lease_token=gen_random_uuid(),lease_until=now()+interval '10 minutes',updated_at=now()
 where id=(select id from public.technician_inbox_queue
 where (status in ('PENDING','RETRY') and available_at<=now())
 or (status='PROCESSING' and lease_until<now())
 order by created_at for update skip locked limit 1) returning q.*;
$$;
revoke all on function public.reconcile_technician_inbox() from public,anon,authenticated;
revoke all on function public.claim_technician_inbox() from public,anon,authenticated;
grant execute on function public.reconcile_technician_inbox() to service_role;
grant execute on function public.claim_technician_inbox() to service_role;
-- Preserve the existing authenticated wake destination, but enqueue durably first.
do $migration$
declare definition text;
begin
 select pg_get_functiondef(oid) into definition from pg_proc where proname='wake_technician_on_inbox_insert';
 if definition is null then raise exception 'Existing wake function is required'; end if;
 definition := replace(definition, E'begin\n', E'begin\n if new.bucket_id <> ''source-inbox'' then return new; end if;\n insert into public.technician_inbox_queue(object_key,object_version) values(new.name,coalesce(new.version,new.id::text)) on conflict do nothing;\n');
 execute definition;
end $migration$;
revoke all on function public.wake_technician_on_inbox_insert() from public,anon,authenticated;
select public.reconcile_technician_inbox();
