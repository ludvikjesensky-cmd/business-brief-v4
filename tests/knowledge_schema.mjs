// Local PostgreSQL semantics test. No network/database credentials are used.
// Install @electric-sql/pglite@0.3.14 in a scratch directory with --ignore-scripts,
// then set PGLITE_MODULE to its dist/index.js and run node tests/knowledge_schema.mjs.
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { pathToFileURL } from 'node:url';
const { PGlite } = await import(pathToFileURL(process.env.PGLITE_MODULE).href);
const db = new PGlite();
let checks = 0;
const query = (sql, params = []) => db.query(sql, params);
async function rejects(sql, params = []) {
  await assert.rejects(query(sql, params)); checks++;
}
await db.exec('create role anon; create role authenticated; create role service_role bypassrls;');
await db.exec(await readFile(new URL('../supabase/migrations/20261021150000_add_editorial_knowledge_layer.sql', import.meta.url), 'utf8'));
const run = '11111111-1111-4111-8111-111111111111';
const h = '1'.repeat(64), h2 = '2'.repeat(64);
const insertRun = `insert into article_enrichment_runs(id, contract_version,profile,profile_version,producer,producer_version,method_version,taxonomy_version,input_manifest_sha256,input_manifest) values ($1,'editorial-enrichment-v1','BB-ENRICHMENT-V1','1','test','1','manual-v1','test-v1',$2,'[]')`;
await query(insertRun, [run, h]);
await query(`insert into article_enrichments values ($1,'a1',$2,'article-records','edition/a1.json',$2,now())`, [run,h]);
await rejects(`insert into article_enrichments values ($1,'a1',$2,'article-records','edition/a1-r2.json',$2,now())`, [run,h2]);
await rejects(`insert into article_enrichments values ($1,'a2','bad','article-records','edition/a2.json',$2,now())`, [run,h]);
await rejects(`update article_enrichment_runs set producer_version=null where id=$1`, [run]);
const addSignal = `insert into signals(signal_id,run_id,article_id,article_record_sha256,observed_on,description,confidence,evidence_refs) values ('sig1',$1,'a1',$2,'2026-10-20','new evidence',.8,$3)`;
await rejects(addSignal, [run,h,'[]']);
await rejects(addSignal, [run,h2,'["e1"]']);
await query(addSignal, [run,h,'["e1"]']);
await query(`insert into trends values ('trend1',$1,$2,'a1',$1,'Auto restructuring','European sector','candidate','emerging')`,[h,run]);
await rejects(`insert into trends values ('trend2',$1,$2,'missing',$1,'Auto restructuring','European sector','candidate','emerging')`,[h,run]);
await rejects(`update trends set status='accepted' where trend_id='trend1'`);
await rejects(`insert into trend_signals values ('unknown',$1,$2,'sig1','supports')`, [h,run]);
await query(`insert into trend_signals values ('trend1',$1,$2,'sig1','contradicts')`,[h,run]);
const polarity = await query('select relation from trend_signals');
assert.equal(polarity.rows[0].relation,'contradicts'); checks++;
await query(`insert into enrichment_annotations values ($1,'a1',$2,'entities','mercedes-benz','Mercedes-Benz','mercedes',.8,'["e1"]','candidate')`,[run,h]);
await rejects(`insert into enrichment_annotations values ($1,'a1',$2,'entities','mercedes alias','Mercedes','mercedes',.8,'["e1"]','candidate')`,[run,h]);
await db.exec('set role anon');
await rejects('select * from trends');
await db.exec('reset role; set role service_role');
await rejects(`update trends set canonical_label='changed'`);
await rejects('delete from article_enrichment_runs');
await db.exec('reset role');
const rls = await query(`select count(*)::int n from pg_tables where schemaname='public' and rowsecurity`);
assert.equal(rls.rows[0].n,9); checks++;
await db.close();
console.log(`${checks} PostgreSQL schema checks passed (in-memory PGlite; candidate staging only).`);
