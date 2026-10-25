-- Fast Editorial Closure Pass: seal exact Brief/channel versions after final review.

create or replace function fast_editorial.validate_gate_insert()
returns trigger language plpgsql set search_path='' as $$
declare s text; h1 text; h2 text;
begin
  select status,content_sha256,content_json_sha256 into s,h1,h2 from fast_editorial.briefs where id=new.brief_id;
  if s='VERIFIED' then raise exception 'cannot add gate to VERIFIED brief %; create a new Brief version',new.brief_id; end if;
  if h1 is null or h2 is null then raise exception 'brief % must have both content hashes before final gates are recorded',new.brief_id; end if;
  return new;
end $$;

drop trigger if exists fast_editorial_validate_gate_insert on fast_editorial.brief_gates;
create trigger fast_editorial_validate_gate_insert before insert on fast_editorial.brief_gates
for each row execute function fast_editorial.validate_gate_insert();

create or replace function fast_editorial.prevent_gated_brief_mutation()
returns trigger language plpgsql set search_path='' as $$
declare gate_count integer;
begin
  if old.status<>'VERIFIED' then
    select count(*) into gate_count from fast_editorial.brief_gates where brief_id=old.id;
    if gate_count>0 and (
      new.content_markdown is distinct from old.content_markdown or new.content_json is distinct from old.content_json
      or new.content_sha256 is distinct from old.content_sha256 or new.content_json_sha256 is distinct from old.content_json_sha256
      or new.title is distinct from old.title or new.deck is distinct from old.deck or new.language is distinct from old.language
      or new.editorial_summary is distinct from old.editorial_summary or new.known_limitations is distinct from old.known_limitations
      or new.editorial_truth_contract is distinct from old.editorial_truth_contract
    ) then raise exception 'brief % already has final gates; content mutation requires a new Brief version',old.id; end if;
  end if;
  return new;
end $$;

drop trigger if exists fast_editorial_prevent_gated_brief_mutation on fast_editorial.briefs;
create trigger fast_editorial_prevent_gated_brief_mutation before update on fast_editorial.briefs
for each row execute function fast_editorial.prevent_gated_brief_mutation();

create or replace function fast_editorial.prevent_verified_brief_content_mutation()
returns trigger language plpgsql set search_path='' as $$
begin
  if old.status='VERIFIED' then
    if new.status='SUPERSEDED' then
      if new.content_markdown is distinct from old.content_markdown or new.content_json is distinct from old.content_json
        or new.content_sha256 is distinct from old.content_sha256 or new.content_json_sha256 is distinct from old.content_json_sha256
        or new.title is distinct from old.title or new.deck is distinct from old.deck or new.language is distinct from old.language
        or new.editorial_summary is distinct from old.editorial_summary or new.known_limitations is distinct from old.known_limitations
      then raise exception 'VERIFIED brief % may only transition to SUPERSEDED without content mutation',old.id; end if;
      return new;
    end if;
    if new is distinct from old then raise exception 'VERIFIED brief % is immutable; create a new version',old.id; end if;
  end if;
  return new;
end $$;

drop trigger if exists fast_editorial_prevent_verified_brief_content_mutation on fast_editorial.briefs;
create trigger fast_editorial_prevent_verified_brief_content_mutation before update on fast_editorial.briefs
for each row execute function fast_editorial.prevent_verified_brief_content_mutation();

create or replace function fast_editorial.protect_verified_brief_dependencies()
returns trigger language plpgsql set search_path='' as $$
declare target_brief uuid; s text;
begin
  target_brief:=case when tg_op='INSERT' then new.brief_id else old.brief_id end;
  select status into s from fast_editorial.briefs where id=target_brief;
  if s='VERIFIED' then raise exception 'cannot modify provenance/gates for VERIFIED brief %; create a new Brief version',target_brief; end if;
  if tg_op='DELETE' then return old; end if;
  return new;
end $$;

drop trigger if exists fast_editorial_protect_verified_gate on fast_editorial.brief_gates;
create trigger fast_editorial_protect_verified_gate before update or delete on fast_editorial.brief_gates for each row execute function fast_editorial.protect_verified_brief_dependencies();
drop trigger if exists fast_editorial_protect_verified_brief_topic on fast_editorial.brief_topics;
create trigger fast_editorial_protect_verified_brief_topic before insert or update or delete on fast_editorial.brief_topics for each row execute function fast_editorial.protect_verified_brief_dependencies();
drop trigger if exists fast_editorial_protect_verified_brief_issue on fast_editorial.brief_issues;
create trigger fast_editorial_protect_verified_brief_issue before insert or update or delete on fast_editorial.brief_issues for each row execute function fast_editorial.protect_verified_brief_dependencies();

create or replace function fast_editorial.prevent_verified_brief_delete()
returns trigger language plpgsql set search_path='' as $$
begin
  if old.status='VERIFIED' then raise exception 'VERIFIED brief % cannot be deleted; supersede it with a newer version',old.id; end if;
  return old;
end $$;

drop trigger if exists fast_editorial_prevent_verified_brief_delete on fast_editorial.briefs;
create trigger fast_editorial_prevent_verified_brief_delete before delete on fast_editorial.briefs for each row execute function fast_editorial.prevent_verified_brief_delete();

create or replace function fast_editorial.prevent_verified_channel_output_mutation()
returns trigger language plpgsql set search_path='' as $$
begin
  if old.status='VERIFIED' then
    if new.status='SUPERSEDED' then
      if new.brief_id is distinct from old.brief_id or new.channel is distinct from old.channel or new.version is distinct from old.version
        or new.format is distinct from old.format or new.content_text is distinct from old.content_text or new.content_json is distinct from old.content_json
        or new.content_sha256 is distinct from old.content_sha256 or new.adapter_contract is distinct from old.adapter_contract
        or new.adaptation_notes is distinct from old.adaptation_notes or new.semantic_check is distinct from old.semantic_check
      then raise exception 'VERIFIED channel output % may only transition to SUPERSEDED without content mutation',old.id; end if;
      return new;
    end if;
    if new is distinct from old then raise exception 'VERIFIED channel output % is immutable; create a new output version',old.id; end if;
  end if;
  return new;
end $$;

drop trigger if exists fast_editorial_prevent_verified_channel_output_mutation on fast_editorial.channel_outputs;
create trigger fast_editorial_prevent_verified_channel_output_mutation before update on fast_editorial.channel_outputs
for each row execute function fast_editorial.prevent_verified_channel_output_mutation();
