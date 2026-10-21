-- Business Brief v4: derived editorial enrichment and long-term knowledge layer.
-- Canonical Article Record prose remains in immutable Storage; these tables are rebuildable/auditable sidecars.

create table if not exists public.article_enrichment_runs (
  id uuid primary key default gen_random_uuid(),
  profile text not null,
  producer text not null,
  producer_version text,
  status text not null default 'PENDING'
    check (status in ('PENDING','VERIFIED','VERIFIED_WITH_NOTES','NEEDS_REVIEW','BLOCKED')),
  intended_count integer not null default 0 check (intended_count >= 0),
  completed_count integer not null default 0 check (completed_count >= 0),
  started_at timestamptz not null default now(),
  completed_at timestamptz,
  error text,
  metadata jsonb not null default '{}'::jsonb
);

create table if not exists public.article_enrichments (
  id uuid primary key default gen_random_uuid(),
  run_id uuid not null references public.article_enrichment_runs(id) on delete cascade,
  article_id text not null,
  article_record_sha256 text not null,
  profile text not null,
  producer text not null,
  status text not null default 'PENDING'
    check (status in ('PENDING','VERIFIED','VERIFIED_WITH_NOTES','NEEDS_REVIEW','BLOCKED')),
  category text not null,
  topics text[] not null default '{}',
  tags text[] not null default '{}',
  entities jsonb not null default '[]'::jsonb,
  geographies text[] not null default '{}',
  industries text[] not null default '{}',
  story_thread_candidates jsonb not null default '[]'::jsonb,
  trend_candidates jsonb not null default '[]'::jsonb,
  signals jsonb not null default '[]'::jsonb,
  evidence jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now(),
  unique(article_id, article_record_sha256, profile, producer)
);

create table if not exists public.story_threads (
  story_thread_id text primary key,
  canonical_label text not null,
  description text,
  status text not null default 'candidate'
    check (status in ('candidate','accepted','rejected','retired')),
  version integer not null default 1 check (version > 0),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  provenance jsonb not null default '{}'::jsonb
);

create table if not exists public.story_thread_articles (
  story_thread_id text not null references public.story_threads(story_thread_id) on delete cascade,
  article_id text not null,
  article_record_sha256 text not null,
  relation text not null,
  status text not null default 'candidate'
    check (status in ('candidate','accepted','rejected','retired')),
  evidence_refs jsonb not null default '[]'::jsonb,
  created_at timestamptz not null default now(),
  primary key(story_thread_id, article_id, article_record_sha256)
);

create table if not exists public.signals (
  signal_id text primary key,
  editorial_day date,
  article_id text not null,
  article_record_sha256 text not null,
  description text not null,
  polarity text not null check (polarity in ('supports','weakens','contradicts','neutral')),
  target_kind text check (target_kind is null or target_kind in ('story_thread','trend')),
  target_ref text,
  status text not null default 'candidate'
    check (status in ('candidate','accepted','rejected','retired')),
  profile text not null,
  producer text not null,
  evidence_refs jsonb not null,
  created_at timestamptz not null default now()
);

create table if not exists public.trends (
  trend_id text primary key,
  canonical_label text not null,
  description text,
  status text not null default 'candidate'
    check (status in ('candidate','accepted','rejected','retired')),
  version integer not null default 1 check (version > 0),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  provenance jsonb not null default '{}'::jsonb
);

create table if not exists public.trend_signals (
  trend_id text not null references public.trends(trend_id) on delete cascade,
  signal_id text not null references public.signals(signal_id) on delete cascade,
  relation text not null default 'evidence',
  status text not null default 'candidate'
    check (status in ('candidate','accepted','rejected','retired')),
  evidence_refs jsonb not null default '[]'::jsonb,
  created_at timestamptz not null default now(),
  primary key(trend_id, signal_id)
);

create unique index if not exists article_enrichments_one_accepted_profile_idx
  on public.article_enrichments(article_id, article_record_sha256, profile)
  where status in ('VERIFIED','VERIFIED_WITH_NOTES');

create index if not exists article_enrichments_topics_gin_idx on public.article_enrichments using gin(topics);
create index if not exists article_enrichments_tags_gin_idx on public.article_enrichments using gin(tags);
create index if not exists article_enrichments_entities_gin_idx on public.article_enrichments using gin(entities);
create index if not exists article_enrichments_geographies_gin_idx on public.article_enrichments using gin(geographies);
create index if not exists article_enrichments_industries_gin_idx on public.article_enrichments using gin(industries);
create index if not exists article_enrichments_article_idx on public.article_enrichments(article_id, article_record_sha256);
create index if not exists signals_article_idx on public.signals(article_id, article_record_sha256);
create index if not exists signals_day_idx on public.signals(editorial_day);
create index if not exists story_threads_status_idx on public.story_threads(status);
create index if not exists trends_status_idx on public.trends(status);

alter table public.article_enrichment_runs enable row level security;
alter table public.article_enrichments enable row level security;
alter table public.story_threads enable row level security;
alter table public.story_thread_articles enable row level security;
alter table public.signals enable row level security;
alter table public.trends enable row level security;
alter table public.trend_signals enable row level security;

revoke all on public.article_enrichment_runs, public.article_enrichments, public.story_threads,
  public.story_thread_articles, public.signals, public.trends, public.trend_signals
  from anon, authenticated;
grant select, insert, update, delete on public.article_enrichment_runs, public.article_enrichments,
  public.story_threads, public.story_thread_articles, public.signals, public.trends, public.trend_signals
  to service_role;

comment on table public.article_enrichments is
  'Derived BB-ENRICHMENT-V1 sidecars bound to immutable article_id + article_record_sha256; never canonical prose.';
comment on table public.trends is
  'Long-term broad phenomena. Accepted promotion requires multi-signal reviewed evidence in application logic.';
