-- Provision technician_wake_token in Supabase Vault and the matching Railway
-- TECHNICIAN_WAKE_TOKEN outside source control before applying this SQL.
create or replace function public.wake_technician_queue() returns bigint
language plpgsql security definer set search_path=public as $$
declare token text; request_id bigint;
begin
 select decrypted_secret into strict token from vault.decrypted_secrets where name='technician_wake_token';
 select net.http_post(url:='https://technician-production-c39c.up.railway.app/wake',
 headers:=jsonb_build_object('Content-Type','application/json','X-Technician-Token',token),
 body:='{"reason":"durable_queue"}'::jsonb,timeout_milliseconds:=10000) into request_id;
 return request_id;
end; $$;
revoke all on function public.wake_technician_queue() from public,anon,authenticated;
grant execute on function public.wake_technician_queue() to service_role;
create or replace function public.wake_technician_on_inbox_insert() returns trigger
language plpgsql security definer set search_path=public as $$
begin
 if new.bucket_id <> 'source-inbox' then return new; end if;
 insert into public.technician_inbox_queue(object_key,object_version)
 values(new.name,coalesce(new.version,new.id::text)) on conflict do nothing;
 begin
  perform public.wake_technician_queue();
 exception when others then
  raise warning 'Technician wake failed; durable queue retained: %',sqlerrm;
 end;
 return new;
end; $$;
revoke all on function public.wake_technician_on_inbox_insert() from public,anon,authenticated;
select cron.alter_job(1,command:='select public.reconcile_technician_inbox(); select public.wake_technician_queue();');
alter view public.dashboard_today set (security_invoker=true);
alter view public.dashboard_technician_jobs set (security_invoker=true);
alter view public.dashboard_metrics_30d set (security_invoker=true);
