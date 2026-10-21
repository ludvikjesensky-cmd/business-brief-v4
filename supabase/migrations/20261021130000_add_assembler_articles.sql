-- Business Brief v4: deterministic Assembler persistence.
-- Canonical Article Record JSON remains authoritative in private Storage.

insert into storage.buckets(id, name, public)
values ('article-records', 'article-records', false)
on conflict (id) do nothing;

do $
begin
  if not exists (select 1 from storage.buckets where id='article-records' and name='article-records' and public=false) then
    raise exception 'article-records bucket must exist and be private';
  end if;
end $;

create table if not exists public.articles (
  article_id text primary key check (article_id ~ '^art-[0-9a-f]{64}$'),
  publication_id uuid not null references public.publications(id),
  edition_id uuid not null references public.editions(id),
  source_id uuid not null references public.sources(id),
  source_sha256 text not null check (source_sha256 ~ '^[0-9a-f]{64}$'),
  manifest_id text not null check (btrim(manifest_id) <> ''),
  manifest_sha256 text not null check (manifest_sha256 ~ '^[0-9a-f]{64}$'),
  title text,
  byline text,
  item_type text not null check (btrim(item_type) <> ''),
  assembly_status text not null check (assembly_status in ('VERIFIED','VERIFIED_WITH_NOTES')),
  post_check_status text not null check (post_check_status = 'PASS'),
  storage_bucket text not null default 'article-records' check (storage_bucket = 'article-records'),
  storage_key text not null unique check (btrim(storage_key) <> ''),
  artifact_sha256 text not null check (artifact_sha256 ~ '^[0-9a-f]{64}$'),
  artifact_byte_size bigint not null check (artifact_byte_size > 0),
  assembler_version text not null check (btrim(assembler_version) <> ''),
  created_at timestamptz not null default now(),
  unique(article_id, artifact_sha256)
);

create table if not exists public.article_source_parts (
  article_id text not null references public.articles(article_id) on delete restrict,
  ordinal integer not null check (ordinal >= 0),
  page_no integer not null check (page_no > 0),
  page_item_id text not null check (btrim(page_item_id) <> ''),
  page_artifact_key text not null check (btrim(page_artifact_key) <> ''),
  page_artifact_sha256 text not null check (page_artifact_sha256 ~ '^[0-9a-f]{64}$'),
  text_sha256 text not null check (text_sha256 ~ '^[0-9a-f]{64}$'),
  primary key(article_id, ordinal),
  unique(article_id, page_no, page_item_id)
);

create index if not exists articles_edition_idx on public.articles(edition_id);
create index if not exists articles_source_idx on public.articles(source_id);
create index if not exists articles_manifest_idx on public.articles(manifest_id, manifest_sha256);
create index if not exists article_source_parts_page_idx on public.article_source_parts(page_no, page_item_id);

alter table public.articles enable row level security;
alter table public.article_source_parts enable row level security;

revoke all on public.articles, public.article_source_parts from public, anon, authenticated;
grant select, insert on public.articles, public.article_source_parts to service_role;

comment on table public.articles is
  'Operational/query index for immutable article-record-v1 artifacts in private article-records Storage. Canonical prose is not stored here.';
comment on table public.article_source_parts is
  'Ordered provenance index for exact Page JSON source parts used by deterministic Assembler.';
