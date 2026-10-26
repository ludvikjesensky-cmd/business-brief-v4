-- Business Brief v4: Indexer v1 derived search layer.
-- Canonical Article Record JSON in private Storage remains authoritative.

create extension if not exists vector with schema extensions;

create table if not exists public.article_index_runs (
  index_run_id text primary key check (index_run_id ~ '^idx-[0-9a-f]{64}$'),
  article_id text not null,
  article_record_sha256 text not null check (article_record_sha256 ~ '^[0-9a-f]{64}$'),
  indexer_version text not null check (btrim(indexer_version) <> ''),
  tokenizer_profile text not null check (btrim(tokenizer_profile) <> ''),
  chunking_profile text not null check (btrim(chunking_profile) <> ''),
  embedding_profile text not null check (btrim(embedding_profile) <> ''),
  embedding_model text not null check (btrim(embedding_model) <> ''),
  embedding_dimensions integer not null check (embedding_dimensions = 1024),
  status text not null check (status in ('PENDING','INDEXING','INDEXED','FAILED')),
  expected_chunk_count integer not null check (expected_chunk_count > 0),
  actual_chunk_count integer,
  article_embedding_input_sha256 text not null check (article_embedding_input_sha256 ~ '^[0-9a-f]{64}$'),
  error text,
  started_at timestamptz not null default now(),
  completed_at timestamptz,
  foreign key(article_id, article_record_sha256)
    references public.articles(article_id, artifact_sha256) on delete restrict
);

create table if not exists public.article_embeddings (
  article_id text not null,
  article_record_sha256 text not null check (article_record_sha256 ~ '^[0-9a-f]{64}$'),
  embedding_profile text not null,
  embedding_model text not null,
  input_type text not null check (input_type = 'search_document'),
  input_sha256 text not null check (input_sha256 ~ '^[0-9a-f]{64}$'),
  embedding extensions.vector(1024) not null,
  created_at timestamptz not null default now(),
  primary key(article_id, article_record_sha256, embedding_profile),
  foreign key(article_id, article_record_sha256)
    references public.articles(article_id, artifact_sha256) on delete restrict
);

create table if not exists public.article_chunks (
  chunk_id text not null check (chunk_id ~ '^chk-[0-9a-f]{64}$'),
  article_id text not null,
  article_record_sha256 text not null check (article_record_sha256 ~ '^[0-9a-f]{64}$'),
  tokenizer_profile text not null,
  chunking_profile text not null,
  embedding_profile text not null,
  embedding_model text not null,
  input_type text not null check (input_type = 'search_document'),
  chunk_index integer not null check (chunk_index >= 0),
  paragraph_from integer not null check (paragraph_from >= 0),
  paragraph_to integer not null check (paragraph_to >= paragraph_from),
  fragment_offsets jsonb,
  token_count integer not null check (token_count > 0 and token_count <= 700),
  text text not null check (text <> ''),
  text_sha256 text not null check (text_sha256 ~ '^[0-9a-f]{64}$'),
  embedding extensions.vector(1024) not null,
  fts tsvector generated always as (to_tsvector('simple', text)) stored,
  created_at timestamptz not null default now(),
  primary key(chunk_id, embedding_profile),
  unique(article_id, article_record_sha256, chunking_profile, embedding_profile, chunk_index),
  foreign key(article_id, article_record_sha256)
    references public.articles(article_id, artifact_sha256) on delete restrict
);

create index if not exists article_index_runs_article_idx
  on public.article_index_runs(article_id, article_record_sha256, embedding_profile, status);

create index if not exists article_chunks_article_idx
  on public.article_chunks(article_id, article_record_sha256, embedding_profile, chunk_index);

create index if not exists article_chunks_fts_idx
  on public.article_chunks using gin(fts);

create index if not exists article_chunks_embedding_hnsw_idx
  on public.article_chunks using hnsw (embedding vector_cosine_ops);

create index if not exists article_embeddings_embedding_hnsw_idx
  on public.article_embeddings using hnsw (embedding vector_cosine_ops);

alter table public.article_index_runs enable row level security;
alter table public.article_embeddings enable row level security;
alter table public.article_chunks enable row level security;

revoke all on public.article_index_runs, public.article_embeddings, public.article_chunks
  from public, anon, authenticated;
grant select, insert, update, delete on
  public.article_index_runs, public.article_embeddings, public.article_chunks
  to service_role;

create or replace function public.search_article_chunks_vector_v1(
  query_embedding extensions.vector(1024),
  match_count integer default 20,
  embedding_profile_filter text default 'BB-EMBEDDING-V1'
)
returns table (
  chunk_id text,
  article_id text,
  article_record_sha256 text,
  chunk_index integer,
  text text,
  score double precision
)
language sql
stable
security invoker
set search_path = public, extensions
as $$
  select
    c.chunk_id,
    c.article_id,
    c.article_record_sha256,
    c.chunk_index,
    c.text,
    1 - (c.embedding <=> query_embedding) as score
  from public.article_chunks c
  join public.article_index_runs r
    on r.article_id = c.article_id
   and r.article_record_sha256 = c.article_record_sha256
   and r.embedding_profile = c.embedding_profile
   and r.status = 'INDEXED'
  where c.embedding_profile = embedding_profile_filter
  order by c.embedding <=> query_embedding
  limit greatest(1, least(match_count, 100));
$$;

create or replace function public.search_article_chunks_lexical_v1(
  query_text text,
  match_count integer default 20,
  embedding_profile_filter text default 'BB-EMBEDDING-V1'
)
returns table (
  chunk_id text,
  article_id text,
  article_record_sha256 text,
  chunk_index integer,
  text text,
  score double precision
)
language sql
stable
security invoker
set search_path = public, extensions
as $$
  select
    c.chunk_id,
    c.article_id,
    c.article_record_sha256,
    c.chunk_index,
    c.text,
    ts_rank(c.fts, plainto_tsquery('simple', query_text))::double precision as score
  from public.article_chunks c
  join public.article_index_runs r
    on r.article_id = c.article_id
   and r.article_record_sha256 = c.article_record_sha256
   and r.embedding_profile = c.embedding_profile
   and r.status = 'INDEXED'
  where c.embedding_profile = embedding_profile_filter
    and c.fts @@ plainto_tsquery('simple', query_text)
  order by score desc, c.chunk_id
  limit greatest(1, least(match_count, 100));
$$;

revoke all on function public.search_article_chunks_vector_v1(extensions.vector, integer, text)
  from public, anon, authenticated;
revoke all on function public.search_article_chunks_lexical_v1(text, integer, text)
  from public, anon, authenticated;
grant execute on function public.search_article_chunks_vector_v1(extensions.vector, integer, text)
  to service_role;
grant execute on function public.search_article_chunks_lexical_v1(text, integer, text)
  to service_role;

comment on table public.article_index_runs is
  'Indexer publication gate. Retrieval serves only rows whose exact article version/profile has status INDEXED.';
comment on table public.article_embeddings is
  'Rebuildable article-level BB-EMBEDDING-V1 projection bound to an immutable Article Record SHA.';
comment on table public.article_chunks is
  'Rebuildable paragraph-derived chunks, lexical projection and embeddings. Canonical prose remains in Article Record Storage.';
