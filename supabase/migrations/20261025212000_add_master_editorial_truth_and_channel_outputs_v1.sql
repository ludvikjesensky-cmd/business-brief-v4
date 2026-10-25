-- Business Brief v4: Master Editorial Truth + channel outputs v1.

alter table fast_editorial.briefs
  add column if not exists content_json jsonb not null default '{}'::jsonb,
  add column if not exists content_json_sha256 text
    check (content_json_sha256 is null or content_json_sha256 ~ '^[0-9a-f]{64}$'),
  add column if not exists editorial_truth_contract text not null default 'master-editorial-truth-v1';

comment on column fast_editorial.briefs.content_json is
'Canonical machine-readable Master Editorial Truth for this exact Brief version. Must represent the same editorial meaning as content_markdown.';
comment on column fast_editorial.briefs.content_markdown is
'Canonical human-readable rendering of the same Master Editorial Truth version stored in content_json.';
comment on column fast_editorial.briefs.content_sha256 is
'SHA-256 of canonical human-readable content_markdown bytes.';
comment on column fast_editorial.briefs.content_json_sha256 is
'SHA-256 of canonical serialized content_json bytes.';
comment on column fast_editorial.briefs.editorial_truth_contract is
'Versioned contract identifying the structure of content_json.';

create table if not exists fast_editorial.channel_outputs (
  id uuid primary key default gen_random_uuid(),
  brief_id uuid not null references fast_editorial.briefs(id) on delete restrict,
  channel text not null check (channel in ('EMAIL','WEB','VOICE')),
  version integer not null check (version > 0),
  status text not null default 'GENERATED'
    check (status in ('GENERATED','VERIFIED','SUPERSEDED','BLOCKED')),
  format text not null check (format in ('MARKDOWN','HTML','JSON','TEXT','SSML')),
  content_text text,
  content_json jsonb,
  content_sha256 text not null check (content_sha256 ~ '^[0-9a-f]{64}$'),
  adapter_contract text not null default 'channel-adapter-v1',
  adaptation_notes jsonb not null default '[]'::jsonb,
  semantic_check text not null default 'PENDING'
    check (semantic_check in ('PENDING','PASS','FAIL')),
  generated_at timestamptz not null default now(),
  verified_at timestamptz,
  unique(brief_id, channel, version),
  check (content_text is not null or content_json is not null)
);

comment on table fast_editorial.channel_outputs is
'Channel-specific adaptations derived only from one exact VERIFIED Master Brief version. They may change form, never editorial truth.';
comment on column fast_editorial.channel_outputs.semantic_check is
'Confirms the adaptation did not add, strengthen, weaken or materially alter source editorial meaning.';

create index if not exists fast_editorial_channel_outputs_brief_idx
  on fast_editorial.channel_outputs(brief_id, channel, version);
create index if not exists fast_editorial_channel_outputs_status_idx
  on fast_editorial.channel_outputs(channel, status, generated_at);

create or replace function fast_editorial.enforce_verified_brief_for_channel_output()
returns trigger
language plpgsql
set search_path = ''
as $$
declare
  brief_status text;
begin
  select b.status into brief_status
  from fast_editorial.briefs b
  where b.id = new.brief_id;

  if brief_status is distinct from 'VERIFIED' then
    raise exception 'channel output requires VERIFIED Master Brief; brief % has status %',
      new.brief_id, coalesce(brief_status, '<missing>');
  end if;

  return new;
end;
$$;

drop trigger if exists fast_editorial_channel_output_requires_verified_brief
  on fast_editorial.channel_outputs;
create trigger fast_editorial_channel_output_requires_verified_brief
before insert or update of brief_id
on fast_editorial.channel_outputs
for each row
execute function fast_editorial.enforce_verified_brief_for_channel_output();

alter table fast_editorial.channel_outputs enable row level security;
revoke all on fast_editorial.channel_outputs from public, anon, authenticated;
grant select, insert, update, delete on fast_editorial.channel_outputs to service_role;
revoke all on function fast_editorial.enforce_verified_brief_for_channel_output() from public, anon, authenticated;
grant execute on function fast_editorial.enforce_verified_brief_for_channel_output() to service_role;
