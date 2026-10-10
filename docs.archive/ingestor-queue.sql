-- Apply once before running bb-ingestor-worker. Server-only durable queue.
create table public.ingestor_jobs (
 id uuid primary key default gen_random_uuid(),
 source_id uuid not null references public.sources(id),
 ingestor_version text not null,
 status text not null default 'PENDING' check(status in ('PENDING','PROCESSING','RETRY','BLOCKED','DONE')),
 attempt integer not null default 0,
 lease_token uuid,
 lease_until timestamptz,
 available_at timestamptz not null default now(),
 physical_map_path text,
 physical_map_sha256 text,
 metrics jsonb,
 last_error text,
 created_at timestamptz not null default now(),
 updated_at timestamptz not null default now(),
 unique(source_id,ingestor_version)
);
alter table public.ingestor_jobs enable row level security;
revoke all on public.ingestor_jobs from anon,authenticated;
grant all on public.ingestor_jobs to service_role;
create index ingestor_jobs_claim_idx on public.ingestor_jobs(ingestor_version,status,available_at);

create function public.reconcile_ingestor_queue(p_version text) returns void
language sql security invoker set search_path=public as $$
 insert into public.ingestor_jobs(source_id,ingestor_version)
 select s.id,p_version from public.sources s join public.editions e on e.active_source_id=s.id
 where s.status='READY_FOR_INGESTOR' and s.source_bundle_contract='source-bundle-v4'
 on conflict do nothing;
$$;
create function public.claim_ingestor_job(p_version text,p_source_id uuid default null) returns setof public.ingestor_jobs
language sql security invoker set search_path=public as $$
 update public.ingestor_jobs q set status='PROCESSING',attempt=attempt+1,
 lease_token=gen_random_uuid(),lease_until=now()+interval '10 minutes',updated_at=now()
 where id=(select j.id from public.ingestor_jobs j
 join public.sources s on s.id=j.source_id join public.editions e on e.active_source_id=s.id
 where j.ingestor_version=p_version and (p_source_id is null or j.source_id=p_source_id) and s.status='READY_FOR_INGESTOR' and
 ((j.status in ('PENDING','RETRY') and j.available_at<=now()) or (j.status='PROCESSING' and j.lease_until<now()))
 order by j.created_at for update of j skip locked limit 1) returning q.*;
$$;
create function public.heartbeat_ingestor_job(p_job_id uuid,p_lease_token uuid) returns void
language sql security invoker set search_path=public as $$
 update public.ingestor_jobs set lease_until=now()+interval '10 minutes',updated_at=now()
 where id=p_job_id and lease_token=p_lease_token and status='PROCESSING' and lease_until>now();
$$;
create function public.finalize_ingestor_job(p_job_id uuid,p_lease_token uuid,p_path text,p_sha256 text,p_metrics jsonb) returns void
language plpgsql security invoker set search_path=public as $$
begin
 if p_path is null or p_sha256 is null or p_sha256 !~ '^[0-9a-f]{64}$' then raise exception 'Invalid artifact'; end if;
 update public.ingestor_jobs j set status='DONE',physical_map_path=p_path,physical_map_sha256=p_sha256,
 metrics=p_metrics,last_error=null,lease_until=null,updated_at=now()
 where j.id=p_job_id and j.lease_token=p_lease_token and j.status='PROCESSING' and j.lease_until>now()
 and exists(select 1 from public.sources s join public.editions e on e.active_source_id=s.id
 where s.id=j.source_id and s.status='READY_FOR_INGESTOR' and s.page_count=(p_metrics->>'page_count')::integer);
 if not found then raise exception 'Lost lease or source no longer eligible'; end if;
end;
$$;
create function public.fail_ingestor_job(p_job_id uuid,p_lease_token uuid,p_error text,p_blocked boolean) returns void
language sql security invoker set search_path=public as $$
 update public.ingestor_jobs set status=case when p_blocked then 'BLOCKED' else 'RETRY' end,
 last_error=p_error,lease_until=null,available_at=now()+interval '5 minutes',updated_at=now()
 where id=p_job_id and lease_token=p_lease_token and status='PROCESSING';
$$;
revoke all on function public.reconcile_ingestor_queue(text),public.claim_ingestor_job(text,uuid),public.heartbeat_ingestor_job(uuid,uuid),public.finalize_ingestor_job(uuid,uuid,text,text,jsonb),public.fail_ingestor_job(uuid,uuid,text,boolean) from public,anon,authenticated;
grant execute on function public.reconcile_ingestor_queue(text),public.claim_ingestor_job(text,uuid),public.heartbeat_ingestor_job(uuid,uuid),public.finalize_ingestor_job(uuid,uuid,text,text,jsonb),public.fail_ingestor_job(uuid,uuid,text,boolean) to service_role;
