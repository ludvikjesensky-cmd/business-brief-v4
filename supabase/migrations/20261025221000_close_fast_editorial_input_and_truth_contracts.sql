-- Fast Editorial Closure Pass: durable input and Master Editorial Truth validation.

create or replace function fast_editorial.validate_master_editorial_truth_v1(p jsonb)
returns boolean language plpgsql immutable set search_path='' as $$
declare u jsonb;
begin
  if jsonb_typeof(p)<>'object' then return false; end if;
  if p->>'contract'<>'master-editorial-truth-v1' then return false; end if;
  if jsonb_typeof(p->'edition')<>'object' then return false; end if;
  if coalesce(p->'edition'->>'date','')='' then return false; end if;
  if coalesce(p->'edition'->>'language','')='' then return false; end if;
  if jsonb_typeof(p->'units')<>'array' or jsonb_array_length(p->'units')=0 then return false; end if;
  if jsonb_typeof(p->'known_limitations')<>'array' then return false; end if;
  for u in select value from jsonb_array_elements(p->'units') loop
    if jsonb_typeof(u)<>'object' then return false; end if;
    if coalesce(u->>'unit_id','')='' then return false; end if;
    if coalesce(u->>'function','') not in ('main_story','coverage','watchlist','curated','number','other') then return false; end if;
    if coalesce(u->>'title','')='' or coalesce(u->>'body','')='' then return false; end if;
    if jsonb_typeof(u->'topic_ids')<>'array' or jsonb_typeof(u->'issue_ids')<>'array' or jsonb_typeof(u->'evidence_refs')<>'array' then return false; end if;
  end loop;
  return true;
exception when others then return false;
end $$;

create or replace function fast_editorial.validate_issue_state()
returns trigger language plpgsql set search_path='' as $$
begin
  if new.status in ('FROZEN','CORRECTED') then
    if new.frozen_snapshot_id is null then raise exception 'issue % cannot be % without frozen_snapshot_id',new.id,new.status; end if;
    if new.frozen_at is null then raise exception 'issue % cannot be % without frozen_at',new.id,new.status; end if;
    if new.freeze_revision<=0 then raise exception 'issue % cannot be % with freeze_revision <= 0',new.id,new.status; end if;
    if jsonb_typeof(new.source_ref)<>'object'
       or new.source_ref->>'contract'<>'fast-editorial-source-ref-v1'
       or new.source_ref->>'kind' not in ('SUPABASE_SOURCE','SUPABASE_STORAGE')
       or coalesce(new.source_ref->>'durable_ref','')=''
    then raise exception 'issue % freeze requires durable source_ref contract fast-editorial-source-ref-v1',new.id; end if;
    if new.source_ref->>'publication_code' is distinct from new.publication_code then raise exception 'issue % source_ref publication_code mismatch',new.id; end if;
    if new.source_ref->>'issue_date' is distinct from new.issue_date::text then raise exception 'issue % source_ref issue_date mismatch',new.id; end if;
    if new.source_ref->>'edition_variant' is distinct from new.edition_variant then raise exception 'issue % source_ref edition_variant mismatch',new.id; end if;
  end if;
  return new;
end $$;

drop trigger if exists fast_editorial_validate_issue_state on fast_editorial.issues;
create trigger fast_editorial_validate_issue_state
before insert or update of status,frozen_snapshot_id,frozen_at,freeze_revision
on fast_editorial.issues for each row execute function fast_editorial.validate_issue_state();

create or replace function fast_editorial.validate_verified_brief()
returns trigger language plpgsql set search_path='' as $$
declare pass_count integer; topic_count integer; issue_count integer; d date;
begin
  if new.status='VERIFIED' then
    if new.verified_at is null then raise exception 'VERIFIED brief % requires verified_at',new.id; end if;
    if new.content_sha256 is null or new.content_json_sha256 is null then raise exception 'VERIFIED brief % requires both content hashes',new.id; end if;
    if btrim(new.content_markdown)='' then raise exception 'VERIFIED brief % requires non-empty content_markdown',new.id; end if;
    if not fast_editorial.validate_master_editorial_truth_v1(new.content_json) then raise exception 'VERIFIED brief % fails master-editorial-truth-v1 structural validation',new.id; end if;
    if new.editorial_truth_contract<>'master-editorial-truth-v1' then raise exception 'VERIFIED brief % requires editorial_truth_contract master-editorial-truth-v1',new.id; end if;
    if coalesce(btrim(new.title),'')='' then raise exception 'VERIFIED brief % requires title',new.id; end if;
    select day_date into d from fast_editorial.days where id=new.day_id;
    if new.content_json->'edition'->>'date' is distinct from d::text then raise exception 'VERIFIED brief % content_json edition date must match day_date',new.id; end if;
    if new.content_json->'edition'->>'language' is distinct from new.language then raise exception 'VERIFIED brief % content_json language must match briefs.language',new.id; end if;
    select count(*) into pass_count from fast_editorial.brief_gates where brief_id=new.id and result='PASS';
    if pass_count<>11 then raise exception 'VERIFIED brief % requires all 11 gates PASS; found %',new.id,pass_count; end if;
    select count(*) into topic_count from fast_editorial.brief_topics where brief_id=new.id;
    if topic_count=0 then raise exception 'VERIFIED brief % requires at least one brief_topic',new.id; end if;
    select count(*) into issue_count from fast_editorial.brief_issues where brief_id=new.id;
    if issue_count=0 then raise exception 'VERIFIED brief % requires at least one brief_issue',new.id; end if;
  end if;
  return new;
end $$;

drop trigger if exists fast_editorial_validate_verified_brief on fast_editorial.briefs;
create trigger fast_editorial_validate_verified_brief
before insert or update of status,verified_at,content_sha256,content_json_sha256,content_markdown,content_json,title
on fast_editorial.briefs for each row execute function fast_editorial.validate_verified_brief();

create or replace function fast_editorial.validate_channel_output_state()
returns trigger language plpgsql set search_path='' as $$
begin
  if new.status='VERIFIED' then
    if new.adapter_contract<>'channel-adapter-v1' then raise exception 'VERIFIED channel output % requires channel-adapter-v1',new.id; end if;
    if new.semantic_check<>'PASS' then raise exception 'VERIFIED channel output % requires semantic_check PASS',new.id; end if;
    if new.verified_at is null then raise exception 'VERIFIED channel output % requires verified_at',new.id; end if;
  end if;
  return new;
end $$;

drop trigger if exists fast_editorial_validate_channel_output_state on fast_editorial.channel_outputs;
create trigger fast_editorial_validate_channel_output_state
before insert or update of status,semantic_check,verified_at on fast_editorial.channel_outputs
for each row execute function fast_editorial.validate_channel_output_state();
