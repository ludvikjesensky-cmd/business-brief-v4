-- Storage UI folder markers are not source documents.
create or replace function public.reconcile_technician_inbox() returns void
language sql security invoker set search_path=public as $$
 insert into public.technician_inbox_queue(object_key,object_version)
 select name,coalesce(version,id::text) from storage.objects
 where bucket_id='source-inbox' and name !~ '(^|/)\.emptyFolderPlaceholder$'
 on conflict do nothing;
$$;
do $$ declare definition text; begin
 select pg_get_functiondef(oid) into definition from pg_proc where proname='wake_technician_on_inbox_insert';
 definition:=replace(definition,'if new.bucket_id <> ''source-inbox'' then',
 'if new.bucket_id <> ''source-inbox'' or new.name ~ ''(^|/)\.emptyFolderPlaceholder$'' then');
 execute definition;
end $$;
