import fs from 'node:fs';
import {execFileSync} from 'node:child_process';
import assert from 'node:assert/strict';
const {chromium} = await import(process.env.PLAYWRIGHT_MODULE);
const html=execFileSync('python',['-c','from business_brief.dashboard import HTML; print(HTML)'],{env:{...process.env,PYTHONPATH:'src'},encoding:'utf8'});
const fixture={observed_at:'2026-10-26T12:00:00Z',editions:[{source_id:'wsj-test',canonical_name:'The Wall Street Journal',edition_date:'2026-10-14',edition_variant:'default',prepared:true,technician_status:'READY_FOR_INGESTOR',source_status:'READY_FOR_INGESTOR',page_receipts:9,page_count:10,selections:[{manifest_id:'wsj-test-selection',manifest_sha256:'a'.repeat(64),label:'Indexováno',next_step:'Provést a vyhodnotit kontrolní vyhledávání.',articles:21,indexed:21,chunks:39,requests:[{request_id:'test-request',operation:'indexer',state:'COMPLETE',result_status:'PASS',persist_requested:'false',updated_at:'2026-10-26T12:00:00Z',counts:{eligible:21,persisted:0}}]}]}]};
const browser=await chromium.launch({executablePath:process.env.CHROME_BIN||'/usr/bin/google-chrome',headless:true});
try{
 const page=await browser.newPage({viewport:{width:1440,height:1000}}),errors=[];
 page.on('pageerror',e=>errors.push(e.message));
 let fail=false;
 await page.route('http://dashboard.test/**',r=>r.fulfill({status:fail&&r.request().url().endsWith('/api/dashboard')?503:200,contentType:r.request().url().endsWith('/api/dashboard')?'application/json':'text/html',body:r.request().url().endsWith('/api/dashboard')?JSON.stringify(fixture):html}));
 await page.goto('http://dashboard.test/');await page.waitForSelector('section.card');
 assert.match(await page.locator('#app').innerText(),/21 \/ 21/);
 await page.locator('summary').click();
 assert.match(await page.locator('#app').innerText(),/Plán bez zápisu/);
 fs.mkdirSync('dashboard-qa',{recursive:true});
 await page.screenshot({path:'dashboard-qa/desktop.png',fullPage:true});
 await page.selectOption('#filter','wsj-test');assert.equal(await page.locator('section.card').count(),1);
 await page.setViewportSize({width:390,height:844});
 assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false);
 await page.screenshot({path:'dashboard-qa/mobile.png',fullPage:true});
 fail=true;await page.locator('#refresh').click();await page.waitForFunction(()=>document.getElementById('error').textContent.includes('zastaralé'));
 assert.equal(await page.locator('section.card').count(),1);assert.deepEqual(errors,[]);
 console.log('Browser PASS: actual HTML, desktop/mobile, history, filter, refresh failure, no JS errors/overflow. Synthetic fixture, no production calls.');
}finally{await browser.close();}
