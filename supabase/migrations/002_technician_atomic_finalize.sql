-- Atomic Technician finalization.
create or replace function public.finalize_technician_source(
  p_source_id uuid,
  p_edition_id uuid,
  p_arrival_id uuid,
  p_job_id uuid
) returns text
language plpgsql
security invoker
set search_path = public
as $$
declare
  v_active uuid;
  v_status text;
begin
  select active_source_id into v_active from public.editions where id=p_edition_id for update;
  if v_active is null or v_active=p_source_id then
    v_status := 'READY_FOR_INGESTOR';
    update public.sources set status=v_status where id=p_source_id;
    update public.editions set active_source_id=p_source_id,status='READY',updated_at=now() where id=p_edition_id;
    update public.technician_jobs set status=v_status,completed_at=now(),heartbeat_at=now(),updated_at=now(),last_error=null where id=p_job_id;
  else
    v_status := 'EDITION_COLLISION';
    update public.sources set status=v_status where id=p_source_id;
    update public.editions set status='COLLISION',updated_at=now() where id=p_edition_id;
    update public.technician_jobs set status=v_status,completed_at=now(),heartbeat_at=now(),updated_at=now(),last_error=null where id=p_job_id;
  end if;
  update public.source_arrivals set source_id=p_source_id,disposition=case when v_status='READY_FOR_INGESTOR' then 'ARCHIVED' else v_status end where id=p_arrival_id;
  return v_status;
end;
$$;
