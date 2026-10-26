-- One read-only snapshot. No privileged views or new Data API exposure.
with recent as (
 select s.id source_id,s.status source_status,s.page_count,s.source_bundle_path,
        e.edition_date,e.edition_variant,p.canonical_name,s.received_at,
        (select j.status from public.technician_jobs j where j.source_id=s.id order by j.created_at desc limit 1) technician_status
 from public.sources s
 join public.editions e on e.id=s.edition_id and e.active_source_id=s.id
 join public.publications p on p.id=e.publication_id
 where e.status <> 'SUPERSEDED'
 order by s.received_at desc,s.id limit 100
), selections as (
 select a.source_id,a.manifest_id,a.manifest_sha256 from public.articles a join recent r on r.source_id=a.source_id
 union
 select b.source_id,regexp_replace(b.target_key,'^.*/edition-selection/|\.json$','','g'),b.artifact_sha256
 from bridge_private.bindings b join recent r on r.source_id=b.source_id
 where b.state='VERIFIED' and b.target_key ~ '/edition-selection/[^/]+\.json$' and b.artifact_sha256 is not null
 union
 select q.source_id,q.manifest_id,q.manifest_sha256 from bridge_private.pipeline_requests q join recent r on r.source_id=q.source_id
)
select r.*,
 (select count(distinct substring(b.target_key from '/ingestor-v2\.2/(?:revisions/)?page-([0-9]{4})'))
  from bridge_private.bindings b where b.source_id=r.source_id and b.state='VERIFIED'
  and b.target_key ~ '/ingestor-v2\.2/(page-[0-9]{4}\.json|revisions/page-[0-9]{4}/[^/]+/page\.json)$') page_receipts,
 coalesce((select jsonb_agg(t order by t.manifest_id,t.manifest_sha256) from (
  select x.manifest_id,x.manifest_sha256,
   (select count(*) from public.articles a where a.source_id=x.source_id and a.manifest_id=x.manifest_id and a.manifest_sha256=x.manifest_sha256) articles,
   (select count(*) from public.articles a where a.source_id=x.source_id and a.manifest_id=x.manifest_id and a.manifest_sha256=x.manifest_sha256
     and (a.assembly_status not in ('VERIFIED','VERIFIED_WITH_NOTES') or a.post_check_status <> 'PASS')) review_articles,
   (select count(distinct a.article_id) from public.articles a join public.article_index_runs i on i.article_id=a.article_id and i.article_record_sha256=a.artifact_sha256
     where a.source_id=x.source_id and a.manifest_id=x.manifest_id and a.manifest_sha256=x.manifest_sha256 and i.status='INDEXED') indexed,
   (select count(*) from public.article_chunks c join public.articles a on a.article_id=c.article_id and a.artifact_sha256=c.article_record_sha256
     where a.source_id=x.source_id and a.manifest_id=x.manifest_id and a.manifest_sha256=x.manifest_sha256) chunks,
   coalesce((select jsonb_agg(z order by z.updated_at desc) from (
     select q.request_id,q.operation,q.state,q.updated_at,q.result->>'status' result_status,
            q.result->'persistence'->>'requested' persist_requested,q.result->'counts' counts
     from bridge_private.pipeline_requests q where q.source_id=x.source_id and q.manifest_id=x.manifest_id and q.manifest_sha256=x.manifest_sha256
     order by q.updated_at desc limit 50
   ) z),'[]'::jsonb) requests
  from selections x where x.source_id=r.source_id
 ) t),'[]'::jsonb) selections
from recent r order by r.received_at desc,r.source_id
