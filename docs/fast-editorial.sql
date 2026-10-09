-- Provisional edition maps. These are not canonical Article/Memory records.
create table public.fast_editorial_jobs (
 id uuid primary key default gen_random_uuid(),
 source_id uuid not null references public.sources(id),
 worker_version text not null,
 model text not null,
 status text not null default 'PENDING' check(status in ('PENDING','RUNNING','FAILED','FROZEN')),
 attempt integer not null default 0,
 lease_token uuid,
 lease_until timestamptz,
 artifact_path text,
 artifact_sha256 text,
 issue_map jsonb,
 last_error text,
 created_at timestamptz not null default now(),
 updated_at timestamptz not null default now(),
 unique(source_id,worker_version,model)
);
create table public.fast_editorial_pages (
 job_id uuid not null references public.fast_editorial_jobs(id),
 page_no integer not null check(page_no>0),
 input_sha256 text not null,
 response jsonb not null,
 created_at timestamptz not null default now(),
 primary key(job_id,page_no)
);
create table public.editorial_map_items (
 job_id uuid not null references public.fast_editorial_jobs(id),
 provisional_id text not null,
 item_order integer not null,
 payload jsonb not null,
 primary key(job_id,provisional_id),
 unique(job_id,item_order)
);
alter table public.fast_editorial_jobs enable row level security;
alter table public.fast_editorial_pages enable row level security;
alter table public.editorial_map_items enable row level security;
revoke all on public.fast_editorial_jobs,public.fast_editorial_pages,public.editorial_map_items from public,anon,authenticated;
grant select,insert,update on public.fast_editorial_jobs,public.fast_editorial_pages,public.editorial_map_items to service_role;

create function public.claim_fast_editorial(p_source_id uuid,p_version text,p_model text)
returns setof public.fast_editorial_jobs language plpgsql security invoker set search_path=public as $$
begin
 if not exists(select 1 from sources s join editions e on e.active_source_id=s.id
 where s.id=p_source_id and s.status='READY_FOR_INGESTOR'
 and exists(select 1 from ingestor_jobs i where i.source_id=s.id and i.status='DONE')) then
 raise exception 'Source is not eligible for Fast Editorial'; end if;
 insert into fast_editorial_jobs(source_id,worker_version,model) values(p_source_id,p_version,p_model) on conflict do nothing;
 return query update fast_editorial_jobs set status='RUNNING',attempt=attempt+1,
 lease_token=gen_random_uuid(),lease_until=now()+interval '10 minutes',updated_at=now(),last_error=null
 where source_id=p_source_id and worker_version=p_version and model=p_model
 and (status in ('PENDING','FAILED') or (status='RUNNING' and lease_until<now())) returning *;
end $$;
create function public.heartbeat_fast_editorial(p_job_id uuid,p_lease_token uuid) returns void
language sql security invoker set search_path=public as $$
 update fast_editorial_jobs set lease_until=now()+interval '10 minutes',updated_at=now()
 where id=p_job_id and lease_token=p_lease_token and status='RUNNING' and lease_until>now();
$$;
create function public.save_fast_editorial_page(p_job_id uuid,p_lease_token uuid,p_page_no integer,p_input_sha256 text,p_response jsonb) returns void
language plpgsql security invoker set search_path=public as $$
begin
 perform 1 from fast_editorial_jobs where id=p_job_id and lease_token=p_lease_token and status='RUNNING' and lease_until>now() for update;
 if not found then raise exception 'Lost editorial lease'; end if;
 if (p_response->'result'->>'page_no')::integer is distinct from p_page_no then raise exception 'Page reference mismatch'; end if;
 insert into fast_editorial_pages(job_id,page_no,input_sha256,response) values(p_job_id,p_page_no,p_input_sha256,p_response) on conflict do nothing;
 if not exists(select 1 from fast_editorial_pages where job_id=p_job_id and page_no=p_page_no and input_sha256=p_input_sha256) then
 raise exception 'Checkpoint input changed'; end if;
end $$;
create function public.finalize_fast_editorial(p_job_id uuid,p_lease_token uuid,p_path text,p_sha256 text,p_map jsonb) returns void
language plpgsql security invoker set search_path=public as $$
declare job fast_editorial_jobs; pages integer;
begin
 select * into strict job from fast_editorial_jobs where id=p_job_id and lease_token=p_lease_token and status='RUNNING' and lease_until>now() for update;
 select s.page_count into strict pages from sources s join editions e on e.active_source_id=s.id where s.id=job.source_id and s.status='READY_FOR_INGESTOR' for share of s,e;
 if p_path is null or p_sha256 is null or p_sha256 !~ '^[0-9a-f]{64}$'
 or p_map->>'schema_version' is distinct from 'editorial-issue-map-v1'
 or p_map->>'source_id' is distinct from job.source_id::text
 or (p_map->>'page_count')::integer is distinct from pages
 or p_map->>'provisional' is distinct from 'true'
 or exists(select 1 from generate_series(1,pages) n where not exists(select 1 from fast_editorial_pages p where p.job_id=job.id and p.page_no=n))
 then raise exception 'Incomplete/invalid provisional Issue Map'; end if;
 insert into editorial_map_items(job_id,provisional_id,item_order,payload)
 select job.id,item->>'provisional_id',ordinality::integer,item from jsonb_array_elements(p_map->'items') with ordinality as x(item,ordinality);
 update fast_editorial_jobs set status='FROZEN',artifact_path=p_path,artifact_sha256=p_sha256,
 issue_map=p_map,lease_until=null,updated_at=now(),last_error=null where id=job.id;
end $$;
create function public.fail_fast_editorial(p_job_id uuid,p_lease_token uuid,p_error text) returns void
language sql security invoker set search_path=public as $$
 update fast_editorial_jobs set status='FAILED',last_error=p_error,lease_until=null,updated_at=now()
 where id=p_job_id and lease_token=p_lease_token and status='RUNNING';
$$;
revoke all on function public.claim_fast_editorial(uuid,text,text),public.heartbeat_fast_editorial(uuid,uuid),public.save_fast_editorial_page(uuid,uuid,integer,text,jsonb),public.finalize_fast_editorial(uuid,uuid,text,text,jsonb),public.fail_fast_editorial(uuid,uuid,text) from public,anon,authenticated;
grant execute on function public.claim_fast_editorial(uuid,text,text),public.heartbeat_fast_editorial(uuid,uuid),public.save_fast_editorial_page(uuid,uuid,integer,text,jsonb),public.finalize_fast_editorial(uuid,uuid,text,text,jsonb),public.fail_fast_editorial(uuid,uuid,text) to service_role;
notify pgrst,'reload schema';
