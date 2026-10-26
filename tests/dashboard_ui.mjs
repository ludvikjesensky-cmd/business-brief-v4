// Execute the shipped inline script with a minimal DOM; no external packages.
import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
const html = fs.readFileSync('src/business_brief/dashboard.py', 'utf8');
const script = html.match(/<script>([\s\S]*?)<\/script>/)[1];
const elements = Object.fromEntries(['app','error','filter','refresh','stamp'].map(id=>[id,{value:id==='filter'?'all':'',innerHTML:'',textContent:''}]));
const sample = {observed_at:'2026-10-26T12:00:00Z',editions:[{
 source_id:'source-1',canonical_name:'WSJ <img onerror=alert(1)>',edition_date:'2026-10-14',prepared:true,page_receipts:9,page_count:10,
 selections:[{manifest_id:'selection',manifest_sha256:'abc',label:'Indexováno',next_step:'Vyhodnotit výsledky',articles:21,indexed:21,chunks:39,
 requests:[{operation:'indexer',state:'COMPLETE',result_status:'PASS',persist_requested:'false',counts:{test:'<script>bad</script>'}}]}]
}]};
let fail = false;
const context = vm.createContext({document:{getElementById:id=>elements[id]},fetch:async()=>({ok:!fail,json:async()=>sample}),setInterval:()=>{},Date,JSON,String});
vm.runInContext(script,context);
await vm.runInContext('refresh()',context);
assert.match(elements.app.innerHTML,/21 \/ 21/);
assert.match(elements.app.innerHTML,/39 textových/);
assert.match(elements.app.innerHTML,/Plán bez zápisu/);
assert.match(elements.app.innerHTML,/&lt;img/);
assert(!elements.app.innerHTML.includes('<script>bad'));
elements.filter.value='different-source';elements.filter.onchange();
assert.match(elements.app.innerHTML,/Žádná vydání/);
elements.filter.value='all';elements.filter.onchange();
const previous = elements.app.innerHTML;fail=true;
await vm.runInContext('refresh()',context);
assert.equal(elements.app.innerHTML,previous);
assert.match(elements.error.textContent,/zastaralé/);
console.log('Dashboard JS PASS: counts, plan label, escaping, filter, stale-data warning');
