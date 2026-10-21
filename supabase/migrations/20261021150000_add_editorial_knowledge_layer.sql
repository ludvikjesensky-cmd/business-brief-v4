-- Derived candidate staging only. Not yet applied to any production database.
-- Q019 gates accepted knowledge on real Article/Index FKs, immutable readback,
-- revision selection and authorized review/promotion transactions.
-- Never add a second canonical article/prose catalog to satisfy these missing FKs.

create table public.article_enrichment_runs (
  id uuid primary key default gen_random_uuid(),
  contract_version text not null check (contract_version = 'editorial-enrichment-v1'),
  profile text not null check (btrim(profile) <> ''),
  profile_version text not null check (btrim(profile_version) <> ''),
  producer text not null check (btrim(producer) <> ''),
  producer_version text not null check (btrim(producer_version) <> ''),
  method_version text not null check (btrim(method_version) <> ''),
  taxonomy_version text not null check (btrim(taxonomy_version) <> ''),
  input_manifest_sha256 text not null check (input_manifest_sha256 ~ '^[0-9a-f]{64}$'),
  input_manifest jsonb not null check (jsonb_typeof(input_manifest) = 'array'),
  status text not null default 'PENDING' check (status in ('PENDING','RUNNING','FAILED','NEEDS_REVIEW')),
  started_at timestamptz not null default now(),
  completed_at timestamptz,
  error text
);

-- Multiple immutable attempt outputs are retained; selected success is gated.
create table public.article_enrichments (
  run_id uuid not null references public.article_enrichment_runs(id),
  article_id text not null check (btrim(article_id) <> ''),
  article_record_sha256 text not null check (article_record_sha256 ~ '^[0-9a-f]{64}$'),
  storage_bucket text not null check (storage_bucket = 'article-records'),
  storage_key text not null check (btrim(storage_key) <> ''),
  output_sha256 text not null check (output_sha256 ~ '^[0-9a-f]{64}$'),
  created_at timestamptz not null default now(),
  primary key (run_id, article_id, article_record_sha256),
  unique (run_id, article_id)
);
create index article_enrichments_article_idx on public.article_enrichments(article_id, article_record_sha256);

-- One normalized facet relation table, rather than five duplicate article tables.
-- term_id is a proposed resolution, not proof of catalog membership/acceptance.
create table public.enrichment_annotations (
  run_id uuid not null,
  article_id text not null,
  article_record_sha256 text not null,
  field text not null check (field in ('category','topics','tags','entities','geographies','industries')),
  normalized_label text not null check (btrim(normalized_label) <> ''),
  label text not null check (btrim(label) <> ''),
  term_id text,
  confidence numeric not null check (confidence >= 0 and confidence <= 1 and confidence <> 'NaN'::numeric),
  evidence_refs jsonb not null check (jsonb_typeof(evidence_refs) = 'array' and jsonb_array_length(evidence_refs) > 0),
  status text not null default 'candidate' check (status in ('candidate','needs_review','rejected','superseded')),
  foreign key (run_id, article_id, article_record_sha256)
    references public.article_enrichments(run_id, article_id, article_record_sha256),
  primary key (run_id, article_id, article_record_sha256, field, normalized_label)
);
create unique index enrichment_annotation_term_uq
  on public.enrichment_annotations(run_id, article_id, article_record_sha256, field, term_id) where term_id is not null;
create index enrichment_annotation_filter_idx on public.enrichment_annotations(field, term_id, status);

-- Revisions are append-only identities, with candidates never served as accepted.
create table public.story_threads (
  story_thread_id text not null check (btrim(story_thread_id) <> ''),
  revision_sha256 text not null check (revision_sha256 ~ '^[0-9a-f]{64}$'),
  run_id uuid not null references public.article_enrichment_runs(id),
  origin_article_id text not null,
  origin_article_record_sha256 text not null,
  canonical_label text not null check (btrim(canonical_label) <> ''),
  definition text not null check (btrim(definition) <> ''),
  status text not null default 'candidate' check (status in ('candidate','needs_review','rejected','superseded')),
  lifecycle text not null check (lifecycle in ('active','dormant','resolved','superseded')),
  foreign key (run_id, origin_article_id, origin_article_record_sha256)
    references public.article_enrichments(run_id, article_id, article_record_sha256),
  primary key (story_thread_id, revision_sha256),
  unique (story_thread_id, revision_sha256, run_id)
);
create index story_threads_run_idx on public.story_threads(run_id, origin_article_id, origin_article_record_sha256);
create table public.trends (
  trend_id text not null check (btrim(trend_id) <> ''),
  revision_sha256 text not null check (revision_sha256 ~ '^[0-9a-f]{64}$'),
  run_id uuid not null references public.article_enrichment_runs(id),
  origin_article_id text not null,
  origin_article_record_sha256 text not null,
  canonical_label text not null check (btrim(canonical_label) <> ''),
  definition text not null check (btrim(definition) <> ''),
  status text not null default 'candidate' check (status in ('candidate','needs_review','rejected','superseded')),
  lifecycle text not null check (lifecycle in ('emerging','established','weakening','reversed','dormant','superseded')),
  foreign key (run_id, origin_article_id, origin_article_record_sha256)
    references public.article_enrichments(run_id, article_id, article_record_sha256),
  primary key (trend_id, revision_sha256),
  unique (trend_id, revision_sha256, run_id)
);
create index trends_run_idx on public.trends(run_id, origin_article_id, origin_article_record_sha256);

create table public.signals (
  signal_id text not null check (btrim(signal_id) <> ''),
  run_id uuid not null,
  article_id text not null,
  article_record_sha256 text not null,
  observed_on date not null,
  description text not null check (btrim(description) <> ''),
  confidence numeric not null check (confidence >= 0 and confidence <= 1 and confidence <> 'NaN'::numeric),
  evidence_refs jsonb not null check (jsonb_typeof(evidence_refs) = 'array' and jsonb_array_length(evidence_refs) > 0),
  status text not null default 'candidate' check (status in ('candidate','needs_review','rejected','superseded')),
  foreign key (run_id, article_id, article_record_sha256)
    references public.article_enrichments(run_id, article_id, article_record_sha256),
  primary key (signal_id, run_id)
);
create index signals_article_fk_idx on public.signals(run_id, article_id, article_record_sha256);
create index signals_day_idx on public.signals(observed_on);

create table public.story_thread_articles (
  story_thread_id text not null,
  revision_sha256 text not null,
  run_id uuid not null,
  article_id text not null,
  article_record_sha256 text not null,
  relation text not null check (relation in ('supports','weakens','contradicts','neutral')),
  evidence_refs jsonb not null check (jsonb_typeof(evidence_refs) = 'array' and jsonb_array_length(evidence_refs) > 0),
  foreign key (story_thread_id, revision_sha256, run_id) references public.story_threads(story_thread_id, revision_sha256, run_id),
  foreign key (run_id, article_id, article_record_sha256) references public.article_enrichments(run_id, article_id, article_record_sha256),
  primary key (story_thread_id, revision_sha256, run_id, article_id, article_record_sha256)
);
create index story_thread_articles_article_fk_idx on public.story_thread_articles(run_id, article_id, article_record_sha256);

create table public.story_thread_signals (
  story_thread_id text not null,
  revision_sha256 text not null,
  run_id uuid not null,
  signal_id text not null,
  relation text not null check (relation in ('supports','weakens','contradicts','neutral')),
  foreign key (story_thread_id, revision_sha256, run_id) references public.story_threads(story_thread_id, revision_sha256, run_id),
  foreign key (signal_id, run_id) references public.signals(signal_id, run_id),
  primary key (story_thread_id, revision_sha256, run_id, signal_id)
);
create index story_thread_signals_signal_fk_idx on public.story_thread_signals(signal_id, run_id);
create table public.trend_signals (
  trend_id text not null,
  revision_sha256 text not null,
  run_id uuid not null,
  signal_id text not null,
  relation text not null check (relation in ('supports','weakens','contradicts','neutral')),
  foreign key (trend_id, revision_sha256, run_id) references public.trends(trend_id, revision_sha256, run_id),
  foreign key (signal_id, run_id) references public.signals(signal_id, run_id),
  primary key (trend_id, revision_sha256, run_id, signal_id)
);
create index trend_signals_signal_fk_idx on public.trend_signals(signal_id, run_id);

-- Staging has no selected/accepted state, promotion RPC or public API access.
-- No UPDATE/DELETE grants to the worker; corrections append new runs/revisions.
-- Production owner roles could alter constraints: rollout remains explicitly Q019.
do $$
declare t text;
begin
  foreach t in array array['article_enrichment_runs','article_enrichments','enrichment_annotations',
    'story_threads','trends','signals','story_thread_articles','story_thread_signals','trend_signals']
  loop
    execute format('alter table public.%I enable row level security', t);
    execute format('revoke all on public.%I from public, anon, authenticated, service_role', t);
    execute format('grant select, insert on public.%I to service_role', t);
  end loop;
end $$;
comment on table public.article_enrichments is
  'Derived candidate staging only; Q019 gates canonical Article/Index FKs, exact readback and atomic selected output publication.';
comment on table public.trends is
  'Accepted state deliberately unavailable until Q019 reviewed multi-article, multi-date promotion and immutable revision selection are implemented.';
