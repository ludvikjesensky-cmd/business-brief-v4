# History — Business Brief family

## v1 — Completeness, provenance, production foundation
První generace definovala základní produkt: český přehled hodnoty FT, WSJ a Handelsblattu, důraz na úplnost, provenance, důvěru, Brief/Detail/Memory a robustní technickou pipeline. Silná stránka byla disciplína coverage; slabina byla rostoucí technická složitost a ambice rekonstruovat vydání velmi detailně.

## v2 — Understand the issue first
v2 posunula důraz k pochopení celého vydání před publikací a k tomu, aby se inteligence používala na editorial judgment. Posílila oddělení operational state v Supabase od dlouhodobých decisions v Markdownu a princip manuálního ověření před API automatizací.

## v3 — Evidence, contracts, semantic experiments
v3 formalizovala Technician, Ingestor/Physical Map, Semantic Mapper, Comparator a silné kontrakty/provenance. Přinesla důležité lekce o hranici mezi fyzickou evidencí a semantic interpretation. Praktické experimenty ukázaly, že spolehlivě skládat články z technické mapy je obtížné, drahé a křehké. Dokumentace se zároveň rozrostla do mnoha handoffů a specializovaných souborů.

## v4 — Editorial value first
v4 vědomě převzala důvěru, provenance, completeness a Memory, ale změnila definici hodnoty. Hlavní otázka už není jen „co musí čtenář vědět“, ale „co stojí za přenos do jeho přemýšlení“. Completeness se přesouvá do Dnešních vydání; Brief je skutečný redakční výběr. Důraz je na perspektivu, argument, otázku a čtenářskou hodnotu.

Technicky v4 znovu oddělila Technician a Ingestor od editorial interpretation, odstranila nefunkční watcher a otestovala Fast Editorial na reálném WSJ. Reálný API náklad ukázal, že full-edition placený modelový průchod v této podobě není ekonomicky přijatelný.

## Documentation reset — 2026-10-10
Dosavadní v4 docs byly archivovány a nahrazeny Project Memory standardem: PROJECT.md, project-memory/ a malou sadou tematických docs. Cílem je zachovat historii bez soupeřících zdrojů pravdy.

## Semantic layout research — 2026-10-12 až 2026-10-14
Physical Map byla doplněna experimenty s vision layoutem, BODY_FLOW, geometry matching a později block-ID assembly. Některé jednotlivé stránky byly částečně úspěšné, ale obecná spolehlivost article ownership, reading order a čistého textu zůstala nedostatečná a vyžadovala opakované ruční zásahy. Tyto experimenty jsou zachovány ve FAILURES, nikoli v current architecture.

## Ingestor v2 pivot — 2026-10-14
Projekt přijal nový generační řez: Ingestor v1.1 / Physical Map production path je superseded. Ingestor v2.0 je živá Chat role nad Technician Source Bundle, pracuje jednu stránku po druhé a vytváří jeden ověřený Page JSON na stránku.

Tím se page semantics přesouvá tam, kde lze opakovaně kontrolovat source image, textovou evidence a vlastní předchozí hypotézy. Automatizace se vrací až za stabilní Page JSON contract: Assembler skládá články, Composer seskupuje témata napříč zdroji, Translator je kandidát pro API transformaci a Editorial Workflow zůstává vrstvou redakčního judgmentu.

## Ordinary Chat read and first write acceptance — consolidated 2026-10-16
Site v3 added verified PNG MCP image delivery; private Site v4 added bounded page-isolated inline OCR extraction. Ordinary Chat then returned image + OCR successfully, closing the earlier separate-connector read gate (details in docs/INGESTOR.md §20).

Acceptance source: UUID `603e8242-ffe8-4e1d-a5de-9adb3da4d188`, source SHA `2ee55f9d94af4389a6a9c20775ab2069cfe2b54f558acb19247b4c1d0672c37f`, source bundle SHA `e14e274810bbde45f738d94ca4a93f3eacefffb32bbb2221b259e2777a84e74d`, publication `the-wall-street-journal`, edition `2026-10-14`, variant `default`, 10 pages.

First production page 1 persisted as VERIFIED / CREATED at `page-ingest/the-wall-street-journal/2026-10-14/2ee55f9d94af4389a6a9c20775ab2069cfe2b54f558acb19247b4c1d0672c37f/ingestor-v2.0/page-0001.json`, artifact SHA `f135489008902816526cd4d2b73710e18e4833931f8adcae47af5ab793741e97`, 42424 B, readback identity verified, usable_for_assembly=true.

The object remains immutable technical acceptance evidence, product-superseded because it inventories irrelevant items, represents What's News digests separately and expands perspective metadata unnecessarily (F009). D019/D020 introduce relevant source-faithful extraction and a separate v3 generation; no v2 rewrite or new production pass occurred during consolidation. Acceptance facts were supplied by the user; raw runtime events stay in operational storage.

## Minimal v3 rollout and page-1 acceptance — 2026-10-16
Bridge commit 1442da050a0b3dcb4a5de9a11611a2b5ec9084c9 was pinned and deployed on Railway (7d1fa8aa-401d-4a2c-8fe0-5a4804eeb029, SUCCESS). The existing owner-private Site v4 needed no transport change. The PR chain remained open to avoid unrelated main-linked service deploys.

Post-deploy resolve → page-1 image + OCR → visual comparison → local v3 validation → one production persist ran through the connected plugin in Codex, using the ordinary-Chat-compatible transport. Six relevant article starts, no PerspectiveEvidence or rejected-item inventory, were stored at `page-ingest/the-wall-street-journal/2026-10-14/2ee55f9d94af4389a6a9c20775ab2069cfe2b54f558acb19247b4c1d0672c37f/ingestor-v2.1/page-0001.json`, SHA `bc287714ea5a290833976b7dfec6caf56f09a668e2c0d401c9e317ac246055e6`, 14,568 B. Receipt: STORED/CREATED, VERIFIED_WITH_NOTES, identity_matches=true, usable_for_assembly=true; downloaded SHA matched locally computed RFC8785 bytes. Notes preserve page-boundary fragments. Existing v2 bytes were never targeted; no next page or assembly ran. This establishes one-page acceptance, not corpus quality or a new separate ordinary-Chat session.

## Article assets / immutable v4 contract — 2026-10-18
D022 separates faithful continuous article prose from preserved visual evidence. The new v4 generation adds article-owned PNG crops with physical page and logical text anchors, reusing the private page-ingest bucket and source/generation namespace. Assembler joins text before re-anchoring; ambiguity remains unplaced. v2/v3 are compatibility artifacts, never schema-rewritten. The user reports v3 page-2 production persistence in addition to the page-1 receipt recorded above; this task did not independently inspect page 2 or invent its SHA/key receipt.

Documentation and contracts consolidate the decision in existing canonical files, with strict schema/bounds/anchor checks and immutable path tests. Binary crop writer/adapter transport remains gated and nonempty-assets writes fail closed. Work starts from current #6 head, preserving the open #4 → #5 → #6 chain. No deployment, production ingest/persist, overwrite, deletion or assembly occurred in this consolidation.

Local verification: 191 tests passed, including v2/v3 compatibility and 53 new article-assets tests; git diff --check clean. No new Markdown files were created.

## Article asset persistence rollout and page-2 acceptance — 2026-10-18
Bridge runtime is pinned to `b6d465c49dbf546f0ea31876d218121428d495c8`, Railway deployment `4489131f-d578-4062-b88f-40adc3716932` (SUCCESS, 1 replica, iad). PR #8 is stacked after #7; no merge or unrelated service deployment. Site v4 remains unchanged and owner-only. The existing generic tool transported artifact:null v4 JSON and the enriched receipt successfully; no raw image bytes or signed URLs were passed in the write request.

Connected-plugin acceptance in Codex (ordinary-Chat-compatible transport, not a newly observed separate ordinary Chat session) completed exactly WSJ 2026-10-14 page 2: STORED/CREATED, VERIFIED_WITH_NOTES, identity_matches=true, usable_for_assembly=true. Three relevant articles and three chart PNGs (both requested banking charts plus the home-price chart) were visually checked before persistence. Bank continuation retains its visible opening fragment. All three text anchors are unique; no placement guess. Final Page JSON SHA `f271f52b378852b186ee919f39d48983db57d469891bd4fad437107efefed60f`, 17,165 RFC8785 bytes. Exact downloaded PNG SHA/size/dimensions match independent local source-derived expected bytes. Both original-request and deterministic set bindings are VERIFIED. Full canonical keys/crop identities are in HISTORY.

The first attempt encountered the existing bucket's JSON-only MIME restriction, leaving PENDING claims and zero v4 objects. The tested deployment hook additively allowed image/png and raised the bucket limit from 5 to 32 MiB while retaining private access. Retrying the original wrapper and idempotency key completed the same intended write; no claim cleanup or object overwrite/delete. Supabase inspection verified four v4 objects and unchanged v2/v3 object IDs/ETags/sizes/updated_at, including v3 page 2. STOP after page 2: no page 3 or assembly.

Source UUID/bundle remain the exact WSJ identity recorded above. New page key: `page-ingest/the-wall-street-journal/2026-10-14/2ee55f9d94af4389a6a9c20775ab2069cfe2b54f558acb19247b4c1d0672c37f/ingestor-v2.2/page-0002.json` in private bucket page-ingest. Its sibling crop directory is `.../ingestor-v2.2/assets/page-0002/`:

| Asset ID / title | Pixel bbox | Dimensions | Bytes | SHA-256 |
| --- | --- | --- | --- | --- |
| p0002-a01-chart-01 / U.S. median existing-home price, change from a year earlier | [433,177,557,378] | 124×201 | 99970 | 82d6b4ba466e3867b4d5189927d6dbd3a80e8355ebfb582b96eb0c2d6f829a77 |
| p0002-a02-chart-01 / Fixed-income, currencies and commodities revenue, by bank | [183,1130,367,1331] | 184×201 | 148215 | 558dc841db2aaef3ff67ba3e2515506afc6e3ffdf38556c12f228cf0fc285e5d |
| p0002-a02-chart-02 / Third-quarter net profit | [374,1130,557,1331] | 183×201 | 147411 | fcc0a3729305845bfdecaf9a4cfaf0720046ae8095a68643ba16537ab2f74533 |

Crop IDs map to owning p0002-a01/p0002-a02 items and `.png` filenames. No canonical chart/table OCR was stored. 226 tests pass; diff check clean. The first bridge runtime deployment was superseded by the tested additive bucket-capability fix; final runtime pin above includes both. Existing object bytes/paths were not modified.

## Ordinary-Chat edition pass — consolidated 2026-10-18
The original conversation `6acf97b3-4370-83eb-9ec9-a9da736f0e81` reports repeated one-page read → visual/OCR validation → v4 JSON/asset metadata → plugin/bridge persist → STOP on pages 3–10, with page 8 completed last. This is a meaningful reported workflow milestone across continuations, an empty ad-only page, prose sidebar and photo/map/chart/infographic assets. It is qualified by F011 and evidence limits below; it is not full visual corpus acceptance.

**Evidence inspected:** current PR #4–#8 metadata and canonical memory at #8 head `823f5cb614bf6eb44caab492a9ef3689dd1d0715`; archived `page-0002-v4-acceptance.json` from the earlier 2026-10-18 Codex acceptance output, and `page-0001-v3-receipt.json` from the 2026-10-16 output. The v4 receipt request_id is `8cf4f999-9922-4005-9d81-185614ff3fa3`, verified_at `2026-10-18T13:10:20.912431Z`; v3 request_id is `1f7649d8-6c41-460f-a024-161a88a19d0d`, verified_at `2026-10-16T17:32:20.516234Z`. Receipt source UUID/SHA/bundle/date/page-count and artifact identities agree with the records above. These are historical bridge readback receipts inspected now, not newly executed storage reads or deployment health checks.

**Evidence limits:** connected bridge tools expose source resolve, source-page evidence and persist, with no stored-ingest read/list or receipt lookup. The retrieved Chat history supplies user/assistant messages, not raw persist tool outputs. No raw receipts for pages 3–10 were available in the inspected history/repo/local acceptance files. Treat their keys/SHA/status/content and preview claims below as REPORTED, not independently verified storage facts. Do not infer asset hashes, sizes, exact asset keys or verified_at timestamps absent from that evidence. No POST, production mutation or source processing was used to fill these gaps.

Page 1: historical v2 acceptance plus receipt-backed v3 `ingestor-v2.1/page-0001.json`, SHA `bc287714ea5a290833976b7dfec6caf56f09a668e2c0d401c9e317ac246055e6`, STORED/CREATED, VERIFIED_WITH_NOTES, usable_for_assembly=true, identity_matches=true. No actual v4 page-0001 object is evidenced. Page 2: receipt-backed v4 key and three exact chart identities recorded above, STORED/CREATED, VERIFIED_WITH_NOTES, usable_for_assembly=true, identity_matches=true. Thus reported ten-page processing spans generations; homogeneous all-v4 coverage is not established.

The following are exact reported JSON object keys (private bucket `page-ingest`) and SHA values. Every row reports STORED/CREATED, usable_for_assembly=true and identity_matches=true; page_status is the historical reported assertion, not a fresh acceptance decision. **Page 6 has a known visual failure despite its reported status.**

| Page | Exact reported canonical key | Reported SHA-256 | Reported page_status |
| --- | --- | --- | --- |
| 3 | `page-ingest/the-wall-street-journal/2026-10-14/2ee55f9d94af4389a6a9c20775ab2069cfe2b54f558acb19247b4c1d0672c37f/ingestor-v2.2/page-0003.json` | `dec8c31c9f81b3dcf0220b19e70f82bd5a32d56034d3c7a142f3c331c146f8a3` | VERIFIED |
| 4 | `page-ingest/the-wall-street-journal/2026-10-14/2ee55f9d94af4389a6a9c20775ab2069cfe2b54f558acb19247b4c1d0672c37f/ingestor-v2.2/page-0004.json` | `ead3ba94f29294f5cc0f7b14e7560acdb7e471a49ecb8b235dbfe4edc99e700b` | VERIFIED_WITH_NOTES |
| 5 | `page-ingest/the-wall-street-journal/2026-10-14/2ee55f9d94af4389a6a9c20775ab2069cfe2b54f558acb19247b4c1d0672c37f/ingestor-v2.2/page-0005.json` | `1cc7f3caf305f1610fee90aacd07671363636b778a1021cea03bb905e335f7a8` | VERIFIED |
| 6 | `page-ingest/the-wall-street-journal/2026-10-14/2ee55f9d94af4389a6a9c20775ab2069cfe2b54f558acb19247b4c1d0672c37f/ingestor-v2.2/page-0006.json` | `d8672242e2cf88e51518c824c4ffceefbcfd524eb07a50d33a6611e2af4531ef` | VERIFIED_WITH_NOTES |
| 7 | `page-ingest/the-wall-street-journal/2026-10-14/2ee55f9d94af4389a6a9c20775ab2069cfe2b54f558acb19247b4c1d0672c37f/ingestor-v2.2/page-0007.json` | `5ad1a64f69000c6ef013205ea27f3addb415b7010ba748267e3d57cee4a7401c` | VERIFIED |
| 8 | `page-ingest/the-wall-street-journal/2026-10-14/2ee55f9d94af4389a6a9c20775ab2069cfe2b54f558acb19247b4c1d0672c37f/ingestor-v2.2/page-0008.json` | `9861a5ef3c9f36ce3e4080c391beb558ab9415f965953d847095c8160b2df569` | VERIFIED |
| 9 | `page-ingest/the-wall-street-journal/2026-10-14/2ee55f9d94af4389a6a9c20775ab2069cfe2b54f558acb19247b4c1d0672c37f/ingestor-v2.2/page-0009.json` | `51a0d162692602712bcb6158ab81b69420e49ba36af8310cbd843ea9a5707802` | VERIFIED |
| 10 | `page-ingest/the-wall-street-journal/2026-10-14/2ee55f9d94af4389a6a9c20775ab2069cfe2b54f558acb19247b4c1d0672c37f/ingestor-v2.2/page-0010.json` | `91c26ea5ca98cf10b058b91f3957fda772b612654df8f5f8f5e4e0b9fceb894b` | VERIFIED_WITH_NOTES |

Reported editorial coverage (not a new source validation):
- Page 3: Regulators Say Shkreli Violated Drug Stock Trading Ban; Trump Spokeswoman Has Rough Debut; Six Flags Closes Several Rides Following Roller-Coaster Death. Three photos (Shkreli, Katie Zacharia, Goliath coaster); Tupac sentencing story and ad omitted.
- Page 4: Paxton, on Dubai Trip, Partied With Fugitives; Guilfoyle Resigns as Ambassador continuation; Condo Borrows From Buyers continuation. Two photos (Paxton/Guilfoyle). Pull quote beginning “The fugitives at the Dubai event...” was not duplicated into canonical prose, item or asset: pull quotes are presentation/layout, not new semantic content. Guilfoyle's source-visible opening fragment was retained.
- Page 5: full-page PAID ADVERTISEMENT; valid v4 items:[], explanatory notes, no article assets. Empty editorial result reported canonical/usable_for_assembly.
- Page 6: Desert Test Shows Army’s Struggle to Revamp; Trump’s Mystery Sailor continuation. Soldier/drone-controller photo and About Face infographic; continuation opening fragment retained. Later standalone display led the user to identify clipping of the infographic's left side. Asset `p0006-a02-infographic-01` was reported 451×590; no raw asset receipt was inspected. F011 is OPEN: immutable page-6 v4 has a known visually-invalid crop. Approximate wider bbox [0.335, 0.445, 0.790, 0.810] is a manual unpersisted candidate, not production-writer-verified/canonical. Q014 requires revision/correction and explicit supersession, never overwrite.
- Page 7: Drone Attacks on Ships Test NATO; U.K. Spy Agency Confronts Hybrid War With Russia, Iran; Houthis Are Using Chinese Parts In Bid to Build Advanced Missile. Four assets: Chelsea 3 rescue photo, Strikes on commercial vessels map, MI5/Ken McCallum photo, Kheibar Shekan photo. Pope health story omitted. All four crops reported independently previewed before persistence.
- Page 8: U.S. Defense Startups Flock to Taiwan; distinct prose sidebar Shipbuilder Signs Pact In Rhode Island; North Korea Flaunts Missiles That Can Reach U.S. Mainland. Two photos: Taiwan sea drone and Kim Jong Un at National Defense Revolution Museum, both reported independently previewed. World Watch briefs and WSJ Future of Health sponsor ad omitted. The boxed prose sidebar remains an editorial item, not a visual asset.
- Page 9: In China, a Battle Rages for the Soul of Tibet; Beijing Doesn’t Want to Join Ranks of Developed Countries. M.S. Rau ad omitted. Tibet photo and combined comparative GNI charts block reported independently previewed. Internal subheads Fading culture and Tough destination were retained as source-visible article structure.
- Page 10: Car-Free Park Drives Backlash and China’s Gen Z Is Losing Hope continuations. Six assets reported independently previewed: one Upper Great Highway/Sunset Dunes photo, three Gen Z photos and two chart assets. Visible opening continuation fragments retained; no off-page reconstruction or assembly.

D023 makes independent server-equivalent standalone crop preview a normative pre-persistence requirement. Q015 tracks receipt reconciliation and explicit generation selection; Q010/Q011 remain open. This consolidation creates no new Markdown authority, performs no deployment/merge/assembly/new ingest and leaves every immutable production artifact untouched. The open dependency chain #4 → #5 → #6 → #7 → #8 is preserved; documentation work branches from exact #8 head.

## Immutable revisions and first explicit edition selection — 2026-10-18
D024 resolves Q014/Q015 for WSJ 2026-10-14. New source-scoped readback/list independently downloaded and verified all canonical Page JSONs and selected PNGs. Pages 3–10 exact canonical keys/SHA/status match the earlier REPORTED rows above without discrepancies; those identity assertions are now authoritatively read back. No v4 page 1 exists in the inventory; v3 page 2 also exists (SHA 34af2878ac058da7ddbffb19d2b674f8959a602010f65fffa88e5eddc0a0b336), while the explicit selection uses v4 page 2. Product-superseded v2 page 1 and defective canonical v4 page 6 remain readable but blocked for accepted selection.

Runtime pin 388f2c879ae5d30b9544a08d95b7283a2f4c6fe6, Railway fdaf8dfa-5ec9-4706-a5ef-7e15a209610a SUCCESS (iad), exactly tested tree 0361481f77a79fb07af9a5d32e17e25a77f02cd5. 249 Python tests pass (23 new); git diff --check clean. Private Site v6 source 58652309a5720bfa2e25eb29b216e106ff24ac47, deployment appgdep_6ad5259db29c8191aee9f97bc8c8896f succeeded; 6 Site tests/build passed. Intermediate v5 (3eb1765252f37cf8115a72653754570cfa999fa2, appgdep_6ad524772c6c8191bfc19977aadfbd24) introduced named tools; v6 also supports cached original plugin tool lists. Connected-plugin resolve/source-page readback and explicit revision/manifest envelopes passed in Codex; no new separate ordinary Chat session or independent invocation of the refreshed standalone tool names is claimed. Owner-only audience preserved.

F011 remediation: source PNG SHA 05b849e71ecbc45c252f48b1e657e11b6a4e3cae0b004fe8f1f64f4f909f5916 (1190×1684). Standalone deterministic crop inspection rejected the earlier approximate candidate in favor of infographic bbox [0.360,0.453,0.671,0.779], pixels [428,762,799,1312], 371×550, 816878 bytes, SHA db6cd769e5c1a23f285e611b04faafc6bf89cfec07b285fb969a22084bbaf3c6. Independent preview exposed a second existing defect: photo bbox [0.225,0.101,0.579,0.276] clipped the left photo and included prose. The user's evidence-based exception authorizes correction to [0.150,0.101,0.459,0.248], pixels [178,170,547,418], 369×248, 366389 bytes, SHA 7a975a9d6d88859683f8db2d99bf7663046eeb234a60161233cf166a561653c9. Both exact revised crops were independently inspected. All page text, anchors and other non-crop metadata compare unchanged.

Full snapshot r1: `ingestor-v2.2/revisions/page-0006/r1/page.json`, SHA 28fb43b41dec104745307204356bb758fa1c2f3044edc1e2688570865638d066, 18942 JCS bytes, reason `incomplete infographic crop`, canonical supersedes SHA d8672242e2cf88e51518c824c4ffceefbcfd524eb07a50d33a6611e2af4531ef. Production receipt request ebca773f-8d63-470e-966f-796b4c7ab091, verified_at 2026-10-18T20:03:00.150835Z, CREATED/VERIFIED, then separate GET readback independently verified r1 and unchanged original. Original PNG SHAs remain 005863cb008e51d0a2d78698ff8b06c04019e02847fef70e56fd0acf877682c9 (photo, 499538 bytes) and dcc488264d5dfccf925e756dee330d9719421da07abd44f95c0ec78b4699bdd6 (infographic, 1065098 bytes). No original overwrite/delete.

First manifest `wsj-2026-10-14-selection-r1`, ACCEPTED_FOR_ASSEMBLY, key `page-ingest/the-wall-street-journal/2026-10-14/2ee55f9d94af4389a6a9c20775ab2069cfe2b54f558acb19247b4c1d0672c37f/edition-selection/wsj-2026-10-14-selection-r1.json`, SHA f78c5339c3f4e406f78645a3c6e3fe3b8f53d89a3919ab6adad4c7e8f29a1d77, 6534 RFC8785 bytes, STORED/VERIFIED. All ten selected JSONs and 24 PNG assets independently read back before manifest write; server repeated selection verification while source-fenced. Local manifest/revision JCS SHA match production receipts exactly.

Every selected key below is relative to `page-ingest/the-wall-street-journal/2026-10-14/2ee55f9d94af4389a6a9c20775ab2069cfe2b54f558acb19247b4c1d0672c37f/` in private bucket page-ingest.

| Page | Selected artifact | SHA-256 | Status | PNGs | Readback UTC |
| --- | --- | --- | --- | --- | --- |
| 1 | `ingestor-v2.1/page-0001.json` | `bc287714ea5a290833976b7dfec6caf56f09a668e2c0d401c9e317ac246055e6` | VERIFIED_WITH_NOTES | 0 | 2026-10-18T20:03:30.723838Z |
| 2 | `ingestor-v2.2/page-0002.json` | `f271f52b378852b186ee919f39d48983db57d469891bd4fad437107efefed60f` | VERIFIED_WITH_NOTES | 3 | 2026-10-18T20:03:29.577196Z |
| 3 | `ingestor-v2.2/page-0003.json` | `dec8c31c9f81b3dcf0220b19e70f82bd5a32d56034d3c7a142f3c331c146f8a3` | VERIFIED | 3 | 2026-10-18T20:03:27.099399Z |
| 4 | `ingestor-v2.2/page-0004.json` | `ead3ba94f29294f5cc0f7b14e7560acdb7e471a49ecb8b235dbfe4edc99e700b` | VERIFIED_WITH_NOTES | 2 | 2026-10-18T20:03:49.036994Z |
| 5 | `ingestor-v2.2/page-0005.json` | `1cc7f3caf305f1610fee90aacd07671363636b778a1021cea03bb905e335f7a8` | VERIFIED | 0 | 2026-10-18T20:03:51.839407Z |
| 6 | `ingestor-v2.2/revisions/page-0006/r1/page.json` | `28fb43b41dec104745307204356bb758fa1c2f3044edc1e2688570865638d066` | VERIFIED_WITH_NOTES | 2 | 2026-10-18T20:03:53.836085Z |
| 7 | `ingestor-v2.2/page-0007.json` | `5ad1a64f69000c6ef013205ea27f3addb415b7010ba748267e3d57cee4a7401c` | VERIFIED | 4 | 2026-10-18T20:04:10.480979Z |
| 8 | `ingestor-v2.2/page-0008.json` | `9861a5ef3c9f36ce3e4080c391beb558ab9415f965953d847095c8160b2df569` | VERIFIED | 2 | 2026-10-18T20:04:14.239884Z |
| 9 | `ingestor-v2.2/page-0009.json` | `51a0d162692602712bcb6158ab81b69420e49ba36af8310cbd843ea9a5707802` | VERIFIED | 2 | 2026-10-18T20:04:15.993926Z |
| 10 | `ingestor-v2.2/page-0010.json` | `91c26ea5ca98cf10b058b91f3957fda772b612654df8f5f8f5e4e0b9fceb894b` | VERIFIED_WITH_NOTES | 6 | 2026-10-18T20:04:31.207837Z |

The edition selection is intentionally heterogeneous; technical acceptance does not close broader Q010 or Assembler policy Q011. Work stopped after manifest persistence. No assembly/composer/editorial, unrelated service deployment, schema migration or main merge. Stacked PR #10 preserves #4 → #5 → #6 → #7 → #8 → #9.

## 2026-10-18 — Ingest handoff merged; runtime pins preserved
GitHub verification confirms PRs #4–#10 merged/closed, ending at main `d35e963847721b49e5ef3aea71716ea0fb7b2825` (PR #10). This supersedes the pre-merge stack status in the acceptance entry above; PR #3 remains a separate open Draft. Q014/Q015 remain resolved and `wsj-2026-10-14-selection-r1` remains ACCEPTED_FOR_ASSEMBLY.

Railway verification confirms bridge pin `388f2c879ae5d30b9544a08d95b7283a2f4c6fe6`, deployment `fdaf8dfa-5ec9-4706-a5ef-7e15a209610a` SUCCESS. The legacy `ingestor` cron was isolated before merge on `a8d6c26e8002c8a4dcad42fce7fa6c5763e65580`, redeploy `2e44c090-63b8-4b95-b5c6-8e263b14850e` SUCCESS; both pins remain configured. The next planned step is Assembler over the explicit Edition Selection Manifest, subject to Q011; no downstream run occurred in this cleanup.

## 2026-10-22 — Railway to Hetzner migration and Q020 acceptance
Following an operator-reported Railway Variables security warning, stored credentials were treated as potentially exposed. The Supabase secret was rotated for the Hetzner environment. This is a precautionary security response, not evidence of confirmed application-data compromise; no secret values are recorded here.

Current production moved to `tannenberg-prod-01`, `46.225.32.16`, Ubuntu 26.04.1 LTS. Caddy terminates HTTPS; `bridge.businessbrief.cz` proxies to Docker Bridge on `127.0.0.1:8080`. `businessbrief.cz` serves static files from the separate `business-brief-web-v2` repository. Supabase remains operational PostgreSQL/Storage. Railway pins/deployment IDs in earlier dated entries are historical provenance only. Public authenticated Bridge `/ready` returned 200 READY and the website returned 200 after cutover.

Q020 accepted WSJ source `603e8242-ffe8-4e1d-a5de-9adb3da4d188`, manifest `wsj-2026-10-14-selection-r1`, SHA `f78c5339c3f4e406f78645a3c6e3fe3b8f53d89a3919ab6adad4c7e8f29a1d77`. Read-only produced 27 page_items and 21 article_records: 16 VERIFIED, 5 VERIFIED_WITH_NOTES, 0 NEEDS_REVIEW, 0 BLOCKED (21 eligible, 0 persisted). First `--persist` returned CREATED receipts; identical rerun returned REPLAYED. This supersedes earlier statements that assembly had not run for this selection. No Indexer/Composer/enrichment acceptance is implied.

Infrastructure documentation was introduced in `5e0337239e186cc7da61e7348915b9681998b0e0`; PROJECT/README references followed. This consolidation preserves immutable artifact identities and unrelated editorial sections. Evidence is the operator's migration/acceptance report and prior conversation, not newly executed production checks. Operational detail: [INFRASTRUCTURE.md](../docs/INFRASTRUCTURE.md).


## 2026-10-26 — Indexer v1 live acceptance on WSJ corpus
PR #16 merged as `47227d97cfdb3ec7f4b9d54d9839a9482b67a4b3` after green CI. Production Supabase migration `add_indexer_v1` was applied and verified with pgvector 0.8.2, RLS-protected `article_index_runs`, `article_embeddings`, `article_chunks` and service-role-only SECURITY INVOKER retrieval RPCs.

Hetzner pulled current `main` and rebuilt the Docker image. The exact accepted WSJ source/manifest from Q020 was indexed:
- plan mode: 21 article rows, 21 eligible, 0 skipped, 39 planned chunks;
- first persist: 21 CREATED receipts;
- exact replay: 21 REPLAYED;
- direct DB readback: 21 runs, 21 INDEXED, 21 article embeddings, 39 chunks covering all 21 articles.

Initial Czech→English semantic retrieval spot checks passed for bank rates/profits, U.S. defense startups in Taiwan and Chinese economic stagnation/Gen Z; expected articles occupied the top vector positions. Lexical results were empty for the Czech-vs-English cases, consistent with the deliberately separate lexical/vector calibration surface.

This establishes Indexer implementation, live persistence, post-check/replay and preliminary Czech→English retrieval evidence. It does not close Q017: Czech→German Handelsblatt acceptance, a predeclared multilingual benchmark, latency/cost measurement and final hybrid fusion remain open.

## Deep/Memory runner — 2026-10-26 repository implementation

Bridge now has an opt-in authenticated Deep runner using existing principals/publication allowlists, explicit source/manifest/SHA, asynchronous receipts/status, durable request binding and source session locks. It calls existing Assembler/Indexer plan/persist/post-check functions; writes are disabled by default. Search filters to exact authorized selection. Technician fails closed because the existing inbox drain is global. See docs/DEEP_RUNNER.md. No production migration, deployment, live paid call or clean ordinary Chat acceptance is claimed; Fast Editorial and Q017/Q018/Q019 gates are unchanged.
