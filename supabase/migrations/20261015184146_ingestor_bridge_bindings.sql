-- Operational idempotency and crash fence only; Page JSON authority remains Storage.
create schema bridge_private;
revoke all on schema bridge_private from public,anon,authenticated;
grant usage on schema bridge_private to service_role;
create table bridge_private.bindings (
 principal text not null,
 idempotency_key uuid not null,
 request_sha256 text not null check(request_sha256 ~ '^[0-9a-f]{64}$'),
 target_key text not null,
 source_id uuid not null references public.sources(id),
 edition_id uuid not null references public.editions(id),
 blob_id uuid not null references public.source_blobs(id),
 publication_id uuid not null references public.publications(id),
 state text not null default 'PENDING' check(state in ('PENDING','VERIFIED','CONFLICT')),
 artifact_sha256 text check(artifact_sha256 ~ '^[0-9a-f]{64}$'),
 created_at timestamptz not null default now(),
 primary key(principal,idempotency_key)
);
alter table bridge_private.bindings enable row level security;
revoke all on bridge_private.bindings from public,anon,authenticated;
-- Technician's invoker triggers need only read access to the private crash fence.
grant select on bridge_private.bindings to service_role;
create index bridge_pending_source on bridge_private.bindings(source_id) where state='PENDING';
create index bridge_pending_edition on bridge_private.bindings(edition_id) where state='PENDING';
create index bridge_pending_blob on bridge_private.bindings(blob_id) where state='PENDING';
create index bridge_pending_publication on bridge_private.bindings(publication_id) where state='PENDING';

create function bridge_private.guard_pending_write() returns trigger
language plpgsql security invoker set search_path=pg_catalog,bridge_private as $$
declare changed boolean := TG_OP='DELETE'; col text;
begin
 if TG_OP='UPDATE' then
  foreach col in array string_to_array(TG_ARGV[1],',') loop
   if (to_jsonb(NEW)->col) is distinct from (to_jsonb(OLD)->col) then changed:=true; end if;
  end loop;
 end if;
 if changed and exists(select 1 from bridge_private.bindings b
   where b.state='PENDING' and (to_jsonb(b)->>TG_ARGV[0])::uuid=OLD.id) then
  raise exception using errcode='55000',message='Pending bridge write requires verified readback reconciliation';
 end if;
 if TG_OP='DELETE' then return OLD; else return NEW; end if;
end $$;
revoke all on function bridge_private.guard_pending_write() from public,anon,authenticated;
grant execute on function bridge_private.guard_pending_write() to service_role;
create trigger bridge_source_fence before update or delete on public.sources for each row execute function bridge_private.guard_pending_write('source_id','id,edition_id,blob_id,status,technician_version,source_bundle_contract,source_bundle_path,page_count');
create trigger bridge_edition_fence before update or delete on public.editions for each row execute function bridge_private.guard_pending_write('edition_id','id,publication_id,edition_date,edition_variant,active_source_id');
create trigger bridge_blob_fence before update or delete on public.source_blobs for each row execute function bridge_private.guard_pending_write('blob_id','id,sha256,byte_size,immutable_original_path');
create trigger bridge_publication_fence before update or delete on public.publications for each row execute function bridge_private.guard_pending_write('publication_id','id,publication_id,canonical_name');
