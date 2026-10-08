-- Business Brief v4: canonical source archive and Technician queue.
-- Apply to the future v4 Supabase project after that project is created.
create extension if not exists pgcrypto;

create table public.publications (
  id uuid primary key default gen_random_uuid(),
  publication_id text not null unique,
  canonical_name text not null,
  aliases text[] not null default '{}',
  languages text[] not null default '{}',
  country_code text,
  frequency text,
  identity_patterns jsonb not null default '{}'::jsonb,
  first_seen_at timestamptz not null default now(),
  last_seen_at timestamptz not null default now(),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table public.editions (
  id uuid primary key default gen_random_uuid(),
  publication_id uuid not null references public.publications(id),
  edition_date date not null,
  edition_variant text not null default 'default',
  status text not null default 'DISCOVERED',
  active_source_id uuid,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique(publication_id, edition_date, edition_variant)
);

create table public.source_blobs (
  id uuid primary key default gen_random_uuid(),
  sha256 text not null unique check (sha256 ~ '^[0-9a-f]{64}$'),
  byte_size bigint not null check (byte_size >= 0),
  mime_type text not null,
  immutable_original_path text not null unique,
  created_at timestamptz not null default now()
);

create table public.sources (
  id uuid primary key default gen_random_uuid(),
  edition_id uuid references public.editions(id),
  blob_id uuid not null references public.source_blobs(id),
  identity_confidence numeric(5,4),
  identity_evidence jsonb not null default '[]'::jsonb,
  language text,
  status text not null default 'REGISTERED',
  technician_version text,
  source_bundle_contract text,
  source_bundle_path text,
  page_count integer check (page_count is null or page_count > 0),
  received_at timestamptz not null default now(),
  created_at timestamptz not null default now(),
  unique(blob_id, technician_version, source_bundle_contract)
);

alter table public.editions
  add constraint editions_active_source_fk
  foreign key (active_source_id) references public.sources(id);

create table public.source_arrivals (
  id uuid primary key default gen_random_uuid(),
  bucket_id text not null,
  object_key text not null,
  object_version text,
  original_filename text not null,
  byte_size bigint,
  received_at timestamptz not null default now(),
  blob_id uuid references public.source_blobs(id),
  source_id uuid references public.sources(id),
  disposition text not null default 'RECEIVED',
  duplicate_of_arrival_id uuid references public.source_arrivals(id),
  created_at timestamptz not null default now()
);

create unique index source_arrivals_object_version_uq
  on public.source_arrivals(bucket_id, object_key, coalesce(object_version, ''));

create table public.technician_jobs (
  id uuid primary key default gen_random_uuid(),
  source_id uuid not null references public.sources(id),
  technician_version text not null,
  contract_version text not null,
  status text not null default 'PENDING',
  attempt integer not null default 0,
  worker_id text,
  claimed_at timestamptz,
  heartbeat_at timestamptz,
  completed_at timestamptz,
  last_error text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique(source_id, technician_version, contract_version)
);

create index editions_lookup_idx on public.editions(publication_id, edition_date, edition_variant);
create index sources_edition_idx on public.sources(edition_id);
create index technician_jobs_claim_idx on public.technician_jobs(status, created_at);
create index technician_jobs_heartbeat_idx on public.technician_jobs(status, heartbeat_at);

alter table public.publications enable row level security;
alter table public.editions enable row level security;
alter table public.source_blobs enable row level security;
alter table public.sources enable row level security;
alter table public.source_arrivals enable row level security;
alter table public.technician_jobs enable row level security;

-- No anon/authenticated policies by design. Technician uses server-side credentials only.
