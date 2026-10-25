-- Fast Editorial Closure Pass: final persistence invariants and relationship integrity.
-- Applied to production Supabase on 2026-10-25.

create or replace function fast_editorial.validate_artifact_binding()
returns trigger language plpgsql set search_path='' as $$
begin
  if new.artifact_type='ISSUE_MAP_SNAPSHOT' and new.issue_id is null then
    raise exception 'ISSUE_MAP_SNAPSHOT requires issue_id';
  end if;
  if new.artifact_type in ('BRIEF_SNAPSHOT','VERIFIED_MASTER_BRIEF') and new.brief_id is null then
    raise exception '% requires brief_id',new.artifact_type;
  end if;
  return new;
end $$;

drop trigger if exists fast_editorial_validate_artifact_binding on fast_editorial.artifacts;
create trigger fast_editorial_validate_artifact_binding
before insert or update on fast_editorial.artifacts
for each row execute function fast_editorial.validate_artifact_binding();

create or replace function fast_editorial.prevent_immutable_artifact_mutation()
returns trigger language plpgsql set search_path='' as $$
begin
  if old.immutable then
    raise exception 'immutable artifact % cannot be updated or deleted',old.id;
  end if;
  if tg_op='DELETE' then return old; end if;
  return new;
end $$;

drop trigger if exists fast_editorial_prevent_immutable_artifact_update on fast_editorial.artifacts;
create trigger fast_editorial_prevent_immutable_artifact_update
before update or delete on fast_editorial.artifacts
for each row execute function fast_editorial.prevent_immutable_artifact_mutation();

create or replace function fast_editorial.prevent_editorial_note_mutation()
returns trigger language plpgsql set search_path='' as $$
begin
  raise exception 'editorial_notes are append-only; create a correction/change note instead';
end $$;

drop trigger if exists fast_editorial_editorial_notes_append_only on fast_editorial.editorial_notes;
create trigger fast_editorial_editorial_notes_append_only
before update or delete on fast_editorial.editorial_notes
for each row execute function fast_editorial.prevent_editorial_note_mutation();

revoke update,delete on fast_editorial.editorial_notes from service_role;
grant select,insert on fast_editorial.editorial_notes to service_role;

create or replace function fast_editorial.validate_same_day_links()
returns trigger language plpgsql set search_path='' as $$
declare d1 uuid; d2 uuid; d3 uuid; v1 integer;
begin
  if tg_table_name='topic_sources' then
    select day_id into d1 from fast_editorial.topics where id=new.topic_id;
    select i.day_id into d2 from fast_editorial.issue_items ii join fast_editorial.issues i on i.id=ii.issue_id where ii.id=new.issue_item_id;
    if d1 is distinct from d2 then raise exception 'topic_sources must link topic and issue_item from same day'; end if;
  elsif tg_table_name='deep_read_notes' then
    select day_id into d1 from fast_editorial.topics where id=new.topic_id;
    if new.day_id is distinct from d1 then raise exception 'deep_read_notes.day_id must match topic day'; end if;
  elsif tg_table_name='brief_topics' then
    select day_id into d1 from fast_editorial.briefs where id=new.brief_id;
    select day_id into d2 from fast_editorial.topics where id=new.topic_id;
    if d1 is distinct from d2 then raise exception 'brief_topics must link brief and topic from same day'; end if;
  elsif tg_table_name='brief_issues' then
    select day_id into d1 from fast_editorial.briefs where id=new.brief_id;
    select day_id into d2 from fast_editorial.issues where id=new.issue_id;
    if d1 is distinct from d2 then raise exception 'brief_issues must link brief and issue from same day'; end if;
  elsif tg_table_name='editorial_notes' then
    if new.issue_id is not null then
      select day_id into d1 from fast_editorial.issues where id=new.issue_id;
      if new.day_id is distinct from d1 then raise exception 'editorial_notes issue must belong to note day'; end if;
    end if;
    if new.topic_id is not null then
      select day_id into d2 from fast_editorial.topics where id=new.topic_id;
      if new.day_id is distinct from d2 then raise exception 'editorial_notes topic must belong to note day'; end if;
    end if;
    if new.brief_id is not null then
      select day_id,version into d3,v1 from fast_editorial.briefs where id=new.brief_id;
      if new.day_id is distinct from d3 then raise exception 'editorial_notes brief must belong to note day'; end if;
      if new.brief_version is not null and new.brief_version<>v1 then raise exception 'editorial_notes.brief_version must match linked brief version'; end if;
    end if;
  elsif tg_table_name='artifacts' then
    if new.issue_id is not null then
      select day_id into d1 from fast_editorial.issues where id=new.issue_id;
      if new.day_id is distinct from d1 then raise exception 'artifact issue must belong to artifact day'; end if;
    end if;
    if new.topic_id is not null then
      select day_id into d2 from fast_editorial.topics where id=new.topic_id;
      if new.day_id is distinct from d2 then raise exception 'artifact topic must belong to artifact day'; end if;
    end if;
    if new.brief_id is not null then
      select day_id into d3 from fast_editorial.briefs where id=new.brief_id;
      if new.day_id is distinct from d3 then raise exception 'artifact brief must belong to artifact day'; end if;
    end if;
  elsif tg_table_name='handover_state' and new.last_verified_brief_id is not null then
    select day_id into d1 from fast_editorial.briefs where id=new.last_verified_brief_id;
    if new.day_id is distinct from d1 then raise exception 'handover last_verified_brief_id must belong to handover day'; end if;
  end if;
  return new;
end $$;

drop trigger if exists fast_editorial_same_day_topic_sources on fast_editorial.topic_sources;
create trigger fast_editorial_same_day_topic_sources before insert or update on fast_editorial.topic_sources for each row execute function fast_editorial.validate_same_day_links();
drop trigger if exists fast_editorial_same_day_deep_read on fast_editorial.deep_read_notes;
create trigger fast_editorial_same_day_deep_read before insert or update on fast_editorial.deep_read_notes for each row execute function fast_editorial.validate_same_day_links();
drop trigger if exists fast_editorial_same_day_brief_topics on fast_editorial.brief_topics;
create trigger fast_editorial_same_day_brief_topics before insert or update on fast_editorial.brief_topics for each row execute function fast_editorial.validate_same_day_links();
drop trigger if exists fast_editorial_same_day_brief_issues on fast_editorial.brief_issues;
create trigger fast_editorial_same_day_brief_issues before insert or update on fast_editorial.brief_issues for each row execute function fast_editorial.validate_same_day_links();
drop trigger if exists fast_editorial_same_day_editorial_notes on fast_editorial.editorial_notes;
create trigger fast_editorial_same_day_editorial_notes before insert or update on fast_editorial.editorial_notes for each row execute function fast_editorial.validate_same_day_links();
drop trigger if exists fast_editorial_same_day_artifacts on fast_editorial.artifacts;
create trigger fast_editorial_same_day_artifacts before insert or update on fast_editorial.artifacts for each row execute function fast_editorial.validate_same_day_links();
drop trigger if exists fast_editorial_same_day_handover on fast_editorial.handover_state;
create trigger fast_editorial_same_day_handover before insert or update on fast_editorial.handover_state for each row execute function fast_editorial.validate_same_day_links();

create or replace function fast_editorial.validate_day_state()
returns trigger language plpgsql set search_path='' as $$
declare verified_briefs integer; handovers integer;
begin
  if new.status in ('VERIFIED','CLOSED') then
    select count(*) into verified_briefs from fast_editorial.briefs where day_id=new.id and status='VERIFIED';
    if verified_briefs=0 then raise exception 'day % cannot be % without a VERIFIED brief',new.id,new.status; end if;
    if new.verified_at is null then raise exception 'day % cannot be % without verified_at',new.id,new.status; end if;
  end if;
  if new.status='CLOSED' then
    if new.closed_at is null then raise exception 'CLOSED day % requires closed_at',new.id; end if;
    select count(*) into handovers from fast_editorial.handover_state where day_id=new.id;
    if handovers=0 then raise exception 'CLOSED day % requires handover_state',new.id; end if;
  end if;
  return new;
end $$;

drop trigger if exists fast_editorial_validate_day_state on fast_editorial.days;
create trigger fast_editorial_validate_day_state
before insert or update of status,verified_at,closed_at on fast_editorial.days
for each row execute function fast_editorial.validate_day_state();
