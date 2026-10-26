-- Bridge-only execution ledger; canonical persistence remains in existing runtimes.
create table bridge_private.pipeline_requests (
 principal_id text not null,
 request_id uuid not null,
 request_sha256 text not null check (request_sha256 ~ '^[0-9a-f]{64}$'),
 source_id uuid not null references public.sources(id),
 manifest_id text not null,
 manifest_sha256 text not null check (manifest_sha256 ~ '^[0-9a-f]{64}$'),
 operation text not null check (operation in ('assembler','indexer','search')),
 state text not null check (state in ('RUNNING','UNKNOWN','COMPLETE')),
 result jsonb,
 updated_at timestamptz not null default now(),
 primary key (principal_id, request_id),
 check ((state='COMPLETE') = (result is not null))
);
alter table bridge_private.pipeline_requests enable row level security;
revoke all on bridge_private.pipeline_requests from public, anon, authenticated;
grant select, insert, update on bridge_private.pipeline_requests to service_role;
