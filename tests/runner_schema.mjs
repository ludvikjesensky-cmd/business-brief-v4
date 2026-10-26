import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {pathToFileURL} from 'node:url';
const {PGlite}=await import(pathToFileURL(process.env.PGLITE_MODULE).href);
const db=new PGlite();
await db.exec('create role anon; create role authenticated; create role service_role bypassrls; create schema bridge_private; grant usage on schema bridge_private to service_role; create table sources(id uuid primary key);');
await db.exec(await readFile(new URL('../supabase/migrations/20261026100000_add_pipeline_requests.sql',import.meta.url),'utf8'));
const sid='11111111-1111-4111-8111-111111111111', key='22222222-2222-4222-8222-222222222222';
await db.query('insert into sources values ($1)',[sid]);
await db.exec('set role service_role');
const insert="insert into bridge_private.pipeline_requests(principal_id,request_id,request_sha256,source_id,manifest_id,manifest_sha256,operation,state) values ('chat',$1,$2,$3,'r1',$2,'assembler','RUNNING')";
await db.query(insert,[key,'a'.repeat(64),sid]);
await assert.rejects(db.query(insert,[key,'a'.repeat(64),sid]));
await assert.rejects(db.query("update bridge_private.pipeline_requests set state='COMPLETE'"));
await db.exec("update bridge_private.pipeline_requests set state='COMPLETE',result='{\"status\":\"PASS\"}'");
assert.equal((await db.query('select state from bridge_private.pipeline_requests')).rows[0].state,'COMPLETE');
for (const role of ['anon','authenticated']) {
 await db.exec('reset role; set role '+role);
 await assert.rejects(db.query('select * from bridge_private.pipeline_requests'));
 await assert.rejects(db.query(insert,[key,'a'.repeat(64),sid]));
}
await db.exec('reset role');
assert.equal((await db.query("select relrowsecurity from pg_class where oid='bridge_private.pipeline_requests'::regclass")).rows[0].relrowsecurity,true);
console.log('Runner PostgreSQL: uniqueness, receipt gate, service access, denied public access and RLS passed');
await db.close();
