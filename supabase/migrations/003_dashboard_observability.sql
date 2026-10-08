-- Structured observability for the Business Brief v4 control tower.
create table public.pipeline_runs (
  id uuid primary key default gen_random_uuid(),
  run_date date not null,
  status text not null default 'RUNNING',
  publication_gate text not null default 'WAITING',
  started_at timestamptz not null default now(),
  completed_at timestamptz,
  metadata jsonb not null default '{}'::jsonb,
  unique(run_date)
);

create table public.pipeline_events (
  id bigint generated always as identity primary key,
  occurred_at timestamptz not null default now(),
  run_id uuid references public.pipeline_runs(id) on delete set null,
  edition_id uuid references public.editions(id) on delete set null,
  source_id uuid references public.sources(id) on delete set null,
  job_id uuid references public.technician_jobs(id) on delete set null,
  component text not null,
  stage text,
  event text not null,
  severity text not null default 'INFO',
  status text,
  duration_ms bigint,
  message text,
  metadata jsonb not null default '{}'::jsonb
);
create index pipeline_events_time_idx on public.pipeline_events(occurred_at desc);
create index pipeline_events_source_idx on public.pipeline_events(source_id,occurred_at);
create index pipeline_events_run_idx on public.pipeline_events(run_id,occurred_at);
create index pipeline_events_component_idx on public.pipeline_events(component,occurred_at desc);

alter table public.pipeline_runs enable row level security;
alter table public.pipeline_events enable row level security;

create or replace view public.dashboard_technician_jobs as
select j.id job_id,j.status,j.attempt,j.created_at,j.claimed_at,j.heartbeat_at,j.completed_at,j.last_error,
       s.id source_id,s.status source_status,s.page_count,s.identity_confidence,s.source_bundle_path,s.received_at,
       e.id edition_id,e.edition_date,e.edition_variant,e.status edition_status,
       p.publication_id,p.canonical_name,
       b.sha256,b.byte_size,b.immutable_original_path
from public.technician_jobs j
join public.sources s on s.id=j.source_id
left join public.editions e on e.id=s.edition_id
left join public.publications p on p.id=e.publication_id
join public.source_blobs b on b.id=s.blob_id;

create or replace view public.dashboard_today as
select p.canonical_name,p.publication_id,e.edition_date,e.edition_variant,e.status edition_status,
       s.id source_id,s.status source_status,s.page_count,s.identity_confidence,s.received_at,
       j.id job_id,j.status job_status,j.attempt,j.claimed_at,j.completed_at,j.last_error
from public.editions e
join public.publications p on p.id=e.publication_id
left join public.sources s on s.id=e.active_source_id
left join public.technician_jobs j on j.source_id=s.id
where e.edition_date=current_date;

create or replace view public.dashboard_metrics_30d as
select
 count(*) filter(where j.status='READY_FOR_INGESTOR') successful,
 count(*) filter(where j.status='FAILED') failed,
 count(*) filter(where j.status='EDITION_COLLISION') collisions,
 count(*) total_jobs,
 percentile_cont(.5) within group(order by extract(epoch from (j.completed_at-j.claimed_at))) filter(where j.completed_at is not null and j.claimed_at is not null) median_seconds,
 avg(s.page_count) filter(where s.page_count is not null) average_pages,
 sum(greatest(j.attempt-1,0)) retries
from public.technician_jobs j join public.sources s on s.id=j.source_id
where j.created_at>=now()-interval '30 days';
