-- Business Brief v4: Fast Editorial persistence schema v1.
-- Separate from historical public.fast_editorial_* experiment tables.
-- Fast Editorial remains independent from the Deep/Memory canonical article pipeline.

create schema if not exists fast_editorial;

comment on schema fast_editorial is
'Fast Editorial v1 operational persistence. Separate from historical public.fast_editorial_* experiment tables and from Deep/Memory canonical article pipeline.';

create table if not exists fast_editorial.days (
  id uuid primary key default gen_random_uuid(),
  day_date date not null unique,
  status text not null default 'OPEN'
    check (status in ('OPEN','READING','CROSS_PAPER','DEEP_READ','EDITORIAL','VERIFIED','CLOSED','BLOCKED')),
  current_step text,
  next_step text,
  last_error text,
  metadata jsonb not null default '{}'::jsonb,
  opened_at timestamptz not null default now(),
  verified_at timestamptz,
  closed_at timestamptz,
  updated_at timestamptz not null default now()
);

create table if not exists fast_editorial.issues (
  id uuid primary key default gen_random_uuid(),
  day_id uuid not null references fast_editorial.days(id) on delete cascade,
  publication_code text not null check (btrim(publication_code) <> ''),
  issue_date date not null,
  edition_variant text not null default 'default',
  intake_order integer not null check (intake_order > 0),
  edition_id uuid references public.editions(id) on delete set null,
  source_id uuid references public.sources(id) on delete set null,
  source_ref jsonb not null default '{}'::jsonb,
  page_count integer check (page_count is null or page_count > 0),
  reading_mode text,
  ocr_performed boolean,
  status text not null default 'WORKING'
    check (status in ('WORKING','FROZEN','CORRECTED','BLOCKED')),
  coverage jsonb not null default '{}'::jsonb,
  editorial_currents jsonb not null default '[]'::jsonb,
  unique_contributions jsonb not null default '[]'::jsonb,
  important_distinctions jsonb not null default '[]'::jsonb,
  counts jsonb not null default '{}'::jsonb,
  process_caveats jsonb not null default '[]'::jsonb,
  frozen_at timestamptz,
  freeze_revision integer not null default 0 check (freeze_revision >= 0),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique(day_id, publication_code, issue_date, edition_variant),
  unique(day_id, intake_order)
);

create table if not exists fast_editorial.issue_items (
  id uuid primary key default gen_random_uuid(),
  issue_id uuid not null references fast_editorial.issues(id) on delete cascade,
  provisional_id text not null check (btrim(provisional_id) <> ''),
  item_order integer not null check (item_order >= 0),
  source_locator jsonb not null default '{}'::jsonb,
  headline_original text,
  working_label_cs text,
  author text,
  genre text,
  article_point text not null,
  editorial_value text,
  priority text not null check (priority in ('CORE','CANDIDATE','LOW')),
  priority_reason text,
  deep_read_candidate boolean not null default false,
  deep_read_questions jsonb not null default '[]'::jsonb,
  memory_candidate boolean not null default false,
  structural_notes jsonb not null default '[]'::jsonb,
  author_view jsonb not null default '{}'::jsonb,
  what_is_new_or_useful text,
  event_importance text check (event_importance is null or event_importance in ('HIGH','MEDIUM','LOW')),
  reading_value text check (reading_value is null or reading_value in ('HIGH','MEDIUM','LOW')),
  uncertainties jsonb not null default '[]'::jsonb,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique(issue_id, provisional_id),
  unique(issue_id, item_order)
);

create table if not exists fast_editorial.topics (
  id uuid primary key default gen_random_uuid(),
  day_id uuid not null references fast_editorial.days(id) on delete cascade,
  working_title text not null,
  central_question text,
  synthesis text,
  why_now text,
  decision text not null default 'RESERVE'
    check (decision in ('INCLUDE','RESERVE','EXCLUDE')),
  decision_reason text,
  reading_value_notes text,
  differences_and_tensions jsonb not null default '[]'::jsonb,
  open_questions jsonb not null default '[]'::jsonb,
  deep_read_status text not null default 'PENDING'
    check (deep_read_status in ('PENDING','IN_PROGRESS','DONE','NEEDS_REVIEW','NOT_REQUIRED')),
  temporal_context jsonb not null default '{}'::jsonb,
  interpretation_changes jsonb not null default '[]'::jsonb,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists fast_editorial.topic_sources (
  topic_id uuid not null references fast_editorial.topics(id) on delete cascade,
  issue_item_id uuid not null references fast_editorial.issue_items(id) on delete restrict,
  role text not null check (role in ('PRIMARY','SUPPORTING','CONTRASTING','BACKGROUND')),
  contribution text not null,
  distinctive_perspective text,
  evidence_refs jsonb not null default '[]'::jsonb,
  created_at timestamptz not null default now(),
  primary key(topic_id, issue_item_id)
);

create table if not exists fast_editorial.deep_read_notes (
  id uuid primary key default gen_random_uuid(),
  day_id uuid not null references fast_editorial.days(id) on delete cascade,
  topic_id uuid not null references fast_editorial.topics(id) on delete cascade,
  source_passages jsonb not null default '[]'::jsonb,
  initial_interpretation text,
  known_questions jsonb not null default '[]'::jsonb,
  verified_findings jsonb not null default '[]'::jsonb,
  newly_discovered_problems jsonb not null default '[]'::jsonb,
  apparent_conflicts jsonb not null default '[]'::jsonb,
  interpretation_before text,
  interpretation_after text,
  change_reason text,
  perspective_recovered_or_corrected text,
  wording_guardrails jsonb not null default '{}'::jsonb,
  selection_before text,
  selection_after text,
  remaining_uncertainties jsonb not null default '[]'::jsonb,
  review_result text not null
    check (review_result in ('DONE','NEEDS_MORE_EVIDENCE','CLAIM_REJECTED','TOPIC_TO_RESERVE')),
  created_at timestamptz not null default now()
);

create table if not exists fast_editorial.briefs (
  id uuid primary key default gen_random_uuid(),
  day_id uuid not null references fast_editorial.days(id) on delete cascade,
  version integer not null check (version > 0),
  status text not null default 'DRAFT' check (status in ('DRAFT','VERIFIED','SUPERSEDED')),
  content_markdown text not null,
  content_sha256 text check (content_sha256 is null or content_sha256 ~ '^[0-9a-f]{64}$'),
  known_limitations jsonb not null default '[]'::jsonb,
  created_at timestamptz not null default now(),
  verified_at timestamptz,
  unique(day_id, version)
);

create table if not exists fast_editorial.brief_topics (
  brief_id uuid not null references fast_editorial.briefs(id) on delete cascade,
  topic_id uuid not null references fast_editorial.topics(id) on delete restrict,
  editorial_function text check (editorial_function is null or editorial_function in ('MAIN_STORY','COVERAGE','WATCHLIST','CURATED','NUMBER','OTHER')),
  unit_key text,
  created_at timestamptz not null default now(),
  primary key(brief_id, topic_id)
);

create table if not exists fast_editorial.brief_issues (
  brief_id uuid not null references fast_editorial.briefs(id) on delete cascade,
  issue_id uuid not null references fast_editorial.issues(id) on delete restrict,
  created_at timestamptz not null default now(),
  primary key(brief_id, issue_id)
);

create table if not exists fast_editorial.brief_gates (
  brief_id uuid not null references fast_editorial.briefs(id) on delete cascade,
  gate_name text not null check (gate_name in (
    'COVERAGE','HIERARCHY','CURIOSITY','TRUST','PRODUCT_FIT','NINETY_SECOND',
    'PERSPECTIVE','DIFFERENCE','READER_AUTONOMY','TIME_RESPECT','LIFE'
  )),
  result text not null check (result in ('PASS','FAIL','NEEDS_REVISION')),
  reason text not null,
  checked_at timestamptz not null default now(),
  primary key(brief_id, gate_name)
);

create table if not exists fast_editorial.editorial_notes (
  id uuid primary key default gen_random_uuid(),
  day_id uuid not null references fast_editorial.days(id) on delete cascade,
  note_type text not null check (btrim(note_type) <> ''),
  issue_id uuid references fast_editorial.issues(id) on delete set null,
  topic_id uuid references fast_editorial.topics(id) on delete set null,
  brief_id uuid references fast_editorial.briefs(id) on delete set null,
  brief_version integer,
  review_question text,
  findings jsonb not null default '[]'::jsonb,
  decisions jsonb not null default '[]'::jsonb,
  changes jsonb not null default '[]'::jsonb,
  unresolved jsonb not null default '[]'::jsonb,
  result text not null default 'INFORMATIONAL'
    check (result in ('PASS','NEEDS_REVISION','INFORMATIONAL')),
  evidence_refs jsonb not null default '[]'::jsonb,
  artifact_refs jsonb not null default '[]'::jsonb,
  created_at timestamptz not null default now()
);

create table if not exists fast_editorial.artifacts (
  id uuid primary key default gen_random_uuid(),
  day_id uuid not null references fast_editorial.days(id) on delete cascade,
  artifact_type text not null check (artifact_type in (
    'ISSUE_MAP_SNAPSHOT','CROSS_PAPER_SNAPSHOT','BRIEF_SNAPSHOT','VERIFIED_MASTER_BRIEF',
    'DAY_RETROSPECTIVE','HANDOVER_SNAPSHOT','OTHER'
  )),
  issue_id uuid references fast_editorial.issues(id) on delete set null,
  topic_id uuid references fast_editorial.topics(id) on delete set null,
  brief_id uuid references fast_editorial.briefs(id) on delete set null,
  format text not null check (format in ('JSON','MARKDOWN','TEXT')),
  payload_jsonb jsonb,
  text_content text,
  storage_bucket text,
  storage_key text,
  sha256 text not null check (sha256 ~ '^[0-9a-f]{64}$'),
  byte_size bigint not null check (byte_size >= 0),
  immutable boolean not null default true,
  created_at timestamptz not null default now(),
  check (
    payload_jsonb is not null
    or text_content is not null
    or (storage_bucket is not null and storage_key is not null)
  )
);

alter table fast_editorial.issues
  add column if not exists frozen_snapshot_id uuid references fast_editorial.artifacts(id) on delete set null;

create table if not exists fast_editorial.story_threads (
  id uuid primary key default gen_random_uuid(),
  label text not null check (btrim(label) <> ''),
  status text not null default 'ACTIVE' check (status in ('ACTIVE','CLOSED','PAUSED')),
  last_known_date date,
  last_known_state text,
  what_reader_already_knows jsonb not null default '[]'::jsonb,
  important_qualifications jsonb not null default '[]'::jsonb,
  interpretation_to_avoid text,
  next_material_change jsonb not null default '[]'::jsonb,
  source_refs jsonb not null default '[]'::jsonb,
  note_refs jsonb not null default '[]'::jsonb,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists fast_editorial.handover_state (
  day_id uuid primary key references fast_editorial.days(id) on delete cascade,
  last_completed_day date,
  last_verified_brief_id uuid references fast_editorial.briefs(id) on delete set null,
  active_status text,
  completed_steps jsonb not null default '[]'::jsonb,
  frozen_issue_ids jsonb not null default '[]'::jsonb,
  cross_paper_status text,
  deep_read_status text,
  editorial_review_status text,
  next_step text,
  blocking_inputs jsonb not null default '[]'::jsonb,
  open_story_thread_ids jsonb not null default '[]'::jsonb,
  inherited_guardrails jsonb not null default '[]'::jsonb,
  source_refs jsonb not null default '[]'::jsonb,
  artifact_refs jsonb not null default '[]'::jsonb,
  updated_at timestamptz not null default now()
);

create index if not exists fast_editorial_issues_day_status_idx on fast_editorial.issues(day_id, status);
create index if not exists fast_editorial_issue_items_issue_priority_idx on fast_editorial.issue_items(issue_id, priority, item_order);
create index if not exists fast_editorial_topics_day_decision_idx on fast_editorial.topics(day_id, decision);
create index if not exists fast_editorial_topics_day_deep_read_idx on fast_editorial.topics(day_id, deep_read_status);
create index if not exists fast_editorial_deep_read_topic_idx on fast_editorial.deep_read_notes(topic_id, created_at);
create index if not exists fast_editorial_editorial_notes_day_type_idx on fast_editorial.editorial_notes(day_id, note_type, created_at);
create index if not exists fast_editorial_artifacts_day_type_idx on fast_editorial.artifacts(day_id, artifact_type, created_at);
create index if not exists fast_editorial_briefs_day_status_idx on fast_editorial.briefs(day_id, status, version);
create index if not exists fast_editorial_story_threads_status_idx on fast_editorial.story_threads(status, last_known_date);

create or replace function fast_editorial.touch_updated_at()
returns trigger
language plpgsql
set search_path = ''
as $$
begin
  new.updated_at = now();
  return new;
end;
$$;

create trigger fast_editorial_days_touch_updated_at before update on fast_editorial.days for each row execute function fast_editorial.touch_updated_at();
create trigger fast_editorial_issues_touch_updated_at before update on fast_editorial.issues for each row execute function fast_editorial.touch_updated_at();
create trigger fast_editorial_issue_items_touch_updated_at before update on fast_editorial.issue_items for each row execute function fast_editorial.touch_updated_at();
create trigger fast_editorial_topics_touch_updated_at before update on fast_editorial.topics for each row execute function fast_editorial.touch_updated_at();
create trigger fast_editorial_story_threads_touch_updated_at before update on fast_editorial.story_threads for each row execute function fast_editorial.touch_updated_at();
create trigger fast_editorial_handover_touch_updated_at before update on fast_editorial.handover_state for each row execute function fast_editorial.touch_updated_at();

alter table fast_editorial.days enable row level security;
alter table fast_editorial.issues enable row level security;
alter table fast_editorial.issue_items enable row level security;
alter table fast_editorial.topics enable row level security;
alter table fast_editorial.topic_sources enable row level security;
alter table fast_editorial.deep_read_notes enable row level security;
alter table fast_editorial.briefs enable row level security;
alter table fast_editorial.brief_topics enable row level security;
alter table fast_editorial.brief_issues enable row level security;
alter table fast_editorial.brief_gates enable row level security;
alter table fast_editorial.editorial_notes enable row level security;
alter table fast_editorial.artifacts enable row level security;
alter table fast_editorial.story_threads enable row level security;
alter table fast_editorial.handover_state enable row level security;

revoke all on schema fast_editorial from public, anon, authenticated;
revoke all on all tables in schema fast_editorial from public, anon, authenticated;
revoke all on all functions in schema fast_editorial from public, anon, authenticated;

grant usage on schema fast_editorial to service_role;
grant select, insert, update, delete on all tables in schema fast_editorial to service_role;
grant execute on all functions in schema fast_editorial to service_role;

alter default privileges in schema fast_editorial revoke all on tables from public, anon, authenticated;
alter default privileges in schema fast_editorial grant select, insert, update, delete on tables to service_role;
alter default privileges in schema fast_editorial revoke all on functions from public, anon, authenticated;
alter default privileges in schema fast_editorial grant execute on functions to service_role;

comment on table fast_editorial.days is 'One Fast Editorial newsroom day. Operational state only; method lives in GitHub documentation.';
comment on table fast_editorial.issues is 'Independent issue-reading state. Freeze preserves the edition-first judgment before Cross-Paper.';
comment on table fast_editorial.issue_items is 'Editorial objects discovered during independent reading. Includes V4 perspective fields without making them a numeric score.';
comment on table fast_editorial.topics is 'Cross-Paper daily stories. A topic is a concrete daily story/question, not a broad subject label.';
comment on table fast_editorial.topic_sources is 'Provenance-preserving topic-to-source links with explicit editorial contribution and perspective.';
comment on table fast_editorial.deep_read_notes is 'Append-style Deep Read evidence and interpretation records. New corrections should normally be new rows, not silent rewrites.';
comment on table fast_editorial.briefs is 'Concrete Master Brief versions. A VERIFIED row is a canonical editorial version, not proof of publication.';
comment on table fast_editorial.brief_gates is 'Final V3 and V4 product gates, bound to one exact Master Brief version.';
comment on table fast_editorial.editorial_notes is 'Operational editorial memory/audit. Concrete daily notes live in Supabase, while their contract lives in GitHub.';
comment on table fast_editorial.artifacts is 'Canonical or checkpoint artifacts. v1 may keep bodies inline in Postgres; optional Storage pointers allow later large-artifact persistence without changing editorial identities.';
comment on table fast_editorial.handover_state is 'Current operational handover state. GitHub may hold a template, but concrete handover data belongs here.';
