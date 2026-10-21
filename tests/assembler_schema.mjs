// Local PostgreSQL semantics test for Assembler persistence. No network/database credentials.
// Install @electric-sql/pglite and set PGLITE_MODULE to its dist/index.js before running.
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { pathToFileURL } from 'node:url';

const { PGlite } = await import(pathToFileURL(process.env.PGLITE_MODULE).href);
const db = new PGlite();
let checks = 0;
const query = (sql, params = []) => db.query(sql, params);
async function rejects(sql, params = []) { await assert.rejects(query(sql, params)); checks++; }

await db.exec("create role anon; create role authenticated; create role service_role bypassrls; create schema storage; create table storage.buckets(id text primary key, name text not null, public boolean not null default false); create table public.publications(id uuid primary key, publication_id text not null unique, canonical_name text not null); create table public.editions(id uuid primary key, publication_id uuid not null references public.publications(id), edition_date date not null, edition_variant text not null); create table public.sources(id uuid primary key, edition_id uuid references public.editions(id));");

await db.exec(await readFile(new URL('../supabase/migrations/20261021130000_add_assembler_articles.sql', import.meta.url), 'utf8'));

const pub = '11111111-1111-4111-8111-111111111111';
const edition = '22222222-2222-4222-8222-222222222222';
const source = '33333333-3333-4333-8333-333333333333';
const h = '1'.repeat(64);
const pageh = '2'.repeat(64);
const texth = '3'.repeat(64);
const article = 'art-' + 'a'.repeat(64);

await query("insert into publications values ($1,'wsj','WSJ')", [pub]);
await query("insert into editions values ($1,$2,'2026-10-14','default')", [edition,pub]);
await query("insert into sources values ($1,$2)", [source,edition]);

const bucket = await query("select public from storage.buckets where id='article-records'");
assert.equal(bucket.rows.length, 1); checks++;
assert.equal(bucket.rows[0].public, false); checks++;

const articleInsert = "insert into articles(article_id,publication_id,edition_id,source_id,source_sha256,manifest_id,manifest_sha256,title,byline,item_type,assembly_status,post_check_status,storage_key,artifact_sha256,artifact_byte_size,assembler_version) values ($1,$2,$3,$4,$5,'m1',$5,'Title','Byline','article','VERIFIED','PASS','article-key',$5,100,'assembler-v1')";
await query(articleInsert,[article,pub,edition,source,h]);

await query("insert into article_source_parts values ($1,0,1,'p1','page-key',$2,$3)",[article,pageh,texth]);
await rejects("insert into article_source_parts values ($1,0,2,'p2','page-key-2',$2,$3)",[article,pageh,texth]);
await rejects("insert into article_source_parts values ($1,1,1,'p1','page-key',$2,$3)",[article,pageh,texth]);

const badArticle = 'art-' + 'b'.repeat(64);
await rejects("insert into articles(article_id,publication_id,edition_id,source_id,source_sha256,manifest_id,manifest_sha256,item_type,assembly_status,post_check_status,storage_key,artifact_sha256,artifact_byte_size,assembler_version) values ($1,$2,$3,$4,$5,'m2',$5,'article','NEEDS_REVIEW','PASS','k2',$5,10,'assembler-v1')",[badArticle,pub,edition,source,h]);

await db.exec('set role anon');
await rejects('select * from articles');
await db.exec('reset role; set role service_role');
const visible = await query('select count(*)::int n from articles');
assert.equal(visible.rows[0].n,1); checks++;
await rejects("update articles set title='changed'");
await db.exec('reset role');

const rls = await query("select count(*)::int n from pg_tables where schemaname='public' and tablename in ('articles','article_source_parts') and rowsecurity");
assert.equal(rls.rows[0].n,2); checks++;

await db.close();
console.log(`${checks} Assembler PostgreSQL schema checks passed (in-memory PGlite).`);
