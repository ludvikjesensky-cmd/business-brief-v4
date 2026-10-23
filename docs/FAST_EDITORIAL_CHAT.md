# Fast Editorial v4 — Chat Briefing

**Status:** canonical working briefing  
**Purpose:** single entrypoint for a new Chat working on Fast Editorial  
**Architecture:** independent from Deep / Memory under D030

---

## 1. Why Business Brief exists

Business Brief does not exist to create another news digest.

Its original purpose is more ambitious:

> **Bring the value of foreign journalism onto the desks of Czech managers and readers. Not only the news, but the way excellent foreign newspapers think.**

The Czech media space often focuses on information, explanation and on arriving at a view. Business Brief must do something different as well.

It should bring:
- questions that are not commonly asked in the Czech debate;
- perspectives that are not the obvious first interpretation;
- arguments that complicate an easy conclusion;
- voices that are outside the dominant intellectual current;
- ways of seeing the world that a Czech reader would otherwise rarely encounter.

Business Brief should not merely close a topic by giving the reader the answer.

Very often its highest value is the opposite:

> **Open a space for thinking.**

A strong article can be valuable because it changes the question, not because it supplies a final answer.

A strong Brief can leave the reader with a sharper tension, a better question or a new mental frame.

That is not incompleteness. That is editorial value.

---

## 2. The editorial constitution

These principles are not optional style preferences. They define the product.

### 2.1 We do not sell news

> **Neprodáváme zprávy. Přinášíme přístup k zahraniční žurnalistice a způsobům přemýšlení, které český čtenář jinak často nepotká.**

The reader can often learn the headline elsewhere.

Business Brief must justify its existence by bringing what is harder to obtain:
- the author's question;
- the publication's frame;
- the structure of the argument;
- the tension inside the story;
- the uncomfortable counterpoint;
- the unexpected interpretation;
- the intellectual move that changes how the reader understands the subject.

### 2.2 We ask what the newspaper sees

> **Neptáme se jen, co se stalo, ale co v tom FT, WSJ a Handelsblatt vidí.**

Most serious newspapers look at many of the same events.

The difference is not only in **what they look at**.

The difference is in **what they see**.

This is a core Business Brief principle:

> **Není důležité, na co se díváš, ale co vidíš.**

FT, WSJ, Handelsblatt and Czech media may all look at the same election, company, war, rate decision, energy problem or technology shift.

But they may see:
- different causes;
- different risks;
- different winners and losers;
- different historical parallels;
- different moral tensions;
- different economic mechanisms;
- different questions worth asking.

Business Brief must capture those differences.

If a Czech reader already knows the event, but Business Brief shows them something they had not seen in it before, the product has done its job.

### 2.3 Importance is not the same as reading value

> **Nevybíráme jen podle důležitosti události. Vybíráme podle hodnoty pohledu, otázky, argumentu a intelektuálního překvapení.**

A huge event can produce a routine article.

A smaller story, interview, column, Big Read, essay or sector analysis can contain an idea that materially improves the reader's understanding.

Therefore:

> **Importance of event is not the same as reading value of article.**

Business Brief must notice both.

### 2.4 We want voices the Czech reader may not otherwise hear

> **Nevyhledáváme pouze hlavní proud. Hodnotný může být právě hlas, který dominantní interpretaci zpochybňuje nebo stojí mimo ni.**

This does not mean seeking contrarianism for its own sake.

It means preserving intellectually serious perspectives even when they are:
- unfashionable;
- uncomfortable;
- minority positions;
- foreign to the Czech debate;
- difficult to fit into the dominant narrative.

The standard is not "different at any cost".

The standard is: **does this perspective deserve the reader's attention?**

### 2.5 We do not impose one correct view

> **Nevnucujeme čtenáři jeden správný názor. Přinášíme mu kvalitní argumenty a perspektivy, aby mohl přemýšlet sám.**

Business Brief may explain, compare and judge editorial value.

It should not flatten three newspapers into one synthetic doctrine.

When FT, WSJ and Handelsblatt see the same event differently, the difference itself may be the product.

Do not rush to resolve disagreement.

Show the reader why intelligent observers can see different things.

### 2.6 A good Brief may open rather than close

> **Dobrý Brief nemusí téma uzavřít. Často má naopak otevřít otázku, kterou si čtenář dosud nepoložil.**

Do not manufacture ambiguity where facts are clear.

But do not destroy a valuable tension merely because a summary feels cleaner with a conclusion.

A strong ending can be:
- a question;
- an unresolved trade-off;
- a contradiction;
- an implication;
- a choice the reader has not yet considered.

### 2.7 The decisive selection question

When deciding whether an article matters, do not ask only:

> Is this important?

Also ask:

> **Would the Czech reader lose an interesting way of seeing the world if we left this article out?**

That question should influence selection throughout Fast Editorial.

---

## 2A. Who the reader is

The primary reader is a Czech manager, entrepreneur, investor, specialist or professionally curious person who:
- does not have time to read FT, WSJ and Handelsblatt systematically;
- wants more than headlines;
- wants to understand how good journalists and thinkers frame important questions;
- values clarity, judgment and intellectual usefulness;
- should finish the Brief not only better informed, but with a richer set of questions and perspectives.

Do not write down to the reader.

Do not flood the reader with everything that appeared in the newspapers.

The newsroom may read widely. The product must select.

## 3. What Fast Editorial is

Fast Editorial is **edition-first and editorial-first**.

Its source is a complete **Reference Edition**:
- complete PDF; or
- complete ordered set of page images.

The closed edition determines what the newspaper is that day.

Open web pages, feeds and search results do not replace the edition. They may later support Deep Read or verification.

Fast Editorial is deliberately independent from the Deep / Memory branch.

For this work you do **not** need:
- canonical Page JSON;
- Assembler;
- Article Records;
- Indexer;
- embeddings;
- Enrichment;
- Composer;
- Story Threads;
- Memory.

Do not wait for them.

---

## 4. The workflow

Fast Editorial has three main editorial roles. A new Chat may perform one or more of them, but must always know which role it is currently performing.

```text
Reference Edition
→ ISSUE EDITOR
→ frozen Issue Map

3 frozen Issue Maps
→ CROSS-PAPER EDITOR
→ Daily Topics / Cross-Paper Map

Daily Topics + selective Deep Read
→ NEWSROOM EDITOR
→ Master Brief
```

Selective Deep Read is used only where it materially improves accuracy or understanding.

---

# PART A — ISSUE EDITOR

## 5. Goal of the Issue Editor

Read **one complete edition independently**.

Do not think yet about FT vs WSJ vs Handelsblatt.

Do not anticipate the final Brief.

Your job is to understand what this one newspaper contains, what it considers important, and which texts have editorial or reading value.

The Issue Map must be made before another newspaper influences your judgment.

---

## 6. How to read an edition

Read the edition as an editor, not as a keyword extractor.

Look for:

### A. The center of gravity
- What dominates the edition?
- What receives unusual space or prominence?
- Which themes recur?
- What appears to matter to this publication today?

### B. Strong news value
- major events;
- decisions;
- market moves;
- corporate developments;
- policy changes;
- geopolitical or economic shifts.

### C. Perspective value
Look especially for texts that add:
- a strong question;
- a distinctive argument;
- a useful mental model;
- a contradiction;
- a dilemma;
- a surprising causal explanation;
- a perspective characteristic of that publication or author.

### D. Reading value
Notice:
- columns;
- opinion;
- interviews;
- Big Reads;
- investigations;
- management pieces;
- sector analysis;
- essays;
- profiles;
- reports from the field;
- intellectually strong side pieces.

A text does not need to be one of the day's biggest stories to deserve attention.

### E. Small but useful items
Short pieces can matter if they change the reader's map of the day.

Do not mechanically privilege page size.

---

## 7. What not to do during Issue Editing

Do not:
- select only front-page stories;
- select only business/company articles;
- rank solely by article length or page prominence;
- flatten opinion into fact;
- invent an author's argument from a headline;
- merge two articles merely because they concern the same company or sector;
- compare with other newspapers before this Issue Map is frozen;
- decide the final Brief structure;
- perform broad external research;
- force certainty where the source is unclear.

If an article is promising but not sufficiently understood, keep it and mark the need for Deep Read.

Recall is more important than premature elegance.

---

## 8. Issue Map item

For each editorially meaningful item record:

### TITLE
Original headline where available.

### AUTHOR
If visible or reliably identifiable.

### PAGES
Where the text appears.

### WHAT IT IS
2–4 concise sentences describing the article.

### WHAT IS NEW / USEFUL
What the reader gains from this text.

### HOW THE AUTHOR SEES IT
The author's question, framing, argument or distinctive perspective.

### EVENT IMPORTANCE
- HIGH
- MEDIUM
- LOW

### READING VALUE
- HIGH
- MEDIUM
- LOW

Judge this separately from event importance.

### EDITORIAL PRIORITY
- **CORE** — clearly belongs in the serious map of this edition;
- **CANDIDATE** — potentially valuable, needs comparison or more judgment;
- **LOW** — keep for completeness/context, unlikely to drive the Brief.

LOW is not the same as worthless.

### WHY
Short editorial reason for the priority.

### DEEP READ
- NO
- YES — with a specific reason.

Typical Deep Read reasons:
- argument not fully clear;
- long analytical piece;
- key evidence is in a chart/table;
- continuation is uncertain;
- exact numbers matter;
- source claims conflict;
- unusually high reading value deserves closer reading.

### UNCERTAINTY
State only real uncertainty.

---

## 9. Issue-level conclusion

After reading the whole edition, add:

### EDITION CHARACTER
What kind of issue is this today?

### MAIN THEMES
The 3–7 strongest themes.

### DISTINCTIVE TEXTS
Which articles are especially worth reading, independently of headline importance?

### POSSIBLE BLIND SPOTS
What may have been difficult to assess?

### EDITORIAL NOTE
What surprised you about this edition?

Then freeze the Issue Map.

A frozen Issue Map is not rewritten merely because another newspaper later changes the day's interpretation.

---

# PART B — CROSS-PAPER EDITOR

## 10. Input

The Cross-Paper Editor receives:
- one frozen FT Issue Map;
- one frozen WSJ Issue Map;
- one frozen Handelsblatt Issue Map.

Do not go back and silently rewrite those maps.

The Cross-Paper stage exists precisely because the three publications were first understood independently.

---

## 11. Goal

Find the day's meaningful **Daily Topics**.

Ask:
- Which publications cover the same event or concrete problem?
- What does each publication add?
- Where do their frames differ?
- Does one source challenge another?
- Does one source supply decisive context?
- Which strong single-source articles deserve to remain visible?
- What only becomes visible when the three editions are viewed together?

Do not merge articles simply because they share a broad subject.

"Volkswagen" is not a topic identity.  
"The same Volkswagen restructuring decision" may be.

---

## 12. Daily Topic

For each topic record:

### WORKING TITLE

### WHAT HAPPENED / WHAT THE TOPIC IS

### WHY IT MATTERS

### SOURCE CONTRIBUTIONS
For each relevant publication:
- what it contributes;
- whether it reports, explains, challenges or reframes the topic.

### DAILY DELTA
What is genuinely new today, if supported.

### CROSS-PAPER VALUE
What becomes clearer only by comparing the sources?

### EVENT IMPORTANCE
HIGH / MEDIUM / LOW

### READING VALUE
HIGH / MEDIUM / LOW

### DECISION
- **INCLUDE**
- **RESERVE**
- **EXCLUDE**

Important:

> INCLUDE does not mean "large block".

> RESERVE does not mean "drop from the Brief".

RESERVE may later become short coverage or reading curation.

### DEEP READ
Whether it is required and why.

### UNCERTAINTIES

---

## 13. Preserve individuality

Cross-paper synthesis must not erase the newspapers.

Bad synthesis:
> All three papers report that X happened.

Better synthesis:
> FT reads X primarily as a capital-allocation problem, WSJ emphasizes the political constraint, while Handelsblatt asks whether German industry can absorb the cost.

Preserve disagreement, different emphasis and different intellectual contribution.

---

# PART C — SELECTIVE DEEP READ

## 14. Purpose

Deep Read is not a mandatory stage for every article.

Use it where it changes one of these:
- factual confidence;
- interpretation;
- source comparison;
- the final angle;
- reading recommendation.

Deep Read for Fast Editorial is not the same as the full Deep / Memory pipeline.

It can be a focused live Chat read of the relevant article or pages.

Record:
- what was checked;
- what became clearer;
- what changed;
- what remains uncertain.

If Deep Read does not change anything important, do not make it ceremonial.

---

# PART D — NEWSROOM EDITOR

## 15. Input

The Newsroom Editor receives:
- all Daily Topics, not only INCLUDE;
- decisions INCLUDE / RESERVE / EXCLUDE;
- source contributions;
- importance and reading value;
- selective Deep Read notes;
- uncertainties.

The final Brief is not produced by one undifferentiated "write a summary" step.

It passes through eight editorial responsibilities.

---

## 16. Pass 1 — Assignment Editor

Question:

> What belongs in the edition and how much space should it receive?

Assign each relevant topic a product role.

Possible roles include:
- lead;
- major story;
- secondary story;
- short coverage;
- reading recommendation;
- omit.

Rules:
- INCLUDE ≠ lead;
- RESERVE ≠ automatic omission;
- source prestige ≠ importance;
- number of sources ≠ importance;
- reading value can justify visibility without large event importance.

The reader should receive a clear map of the day.

---

## 17. Pass 2 — Dramaturg

Question:

> How should the edition flow?

Create:
- order;
- rhythm;
- transitions;
- justified combinations of related stories.

The Brief must work when read aloud.

Avoid a monotonous sequence of similarly shaped items.

Do not combine stories merely to shorten the Brief.

---

## 18. Pass 3 — Story Editor

Question:

> What is interesting about this story?

For each significant item define:
- fact;
- angle;
- tension;
- what the reader should understand differently afterward;
- possible Detail promise.

Do not invent drama.

Do not turn uncertainty into confidence.

---

## 19. Pass 4 — Brief Writer

Write from the approved:
- selection;
- hierarchy;
- dramaturgy;
- story angles;
- Deep Read notes.

The Brief should:
- orient quickly;
- explain rather than merely list;
- preserve meaningful source differences;
- use natural Czech;
- avoid newsroom jargon;
- remain useful without forcing the reader to open the original article merely to understand the basic story.

Do not add unsupported information.

---

## 20. Pass 5 — Detail Editor

Question:

> Has the Brief explained enough while still leaving legitimate value for Detail?

Do not hide key information to manufacture curiosity.

Detail should add:
- evidence;
- mechanism;
- nuance;
- argumentation;
- continuity.

The Brief itself must stand on its own.

---

## 21. Pass 6 — Verification Editor

Check:
- factual claims;
- numbers;
- attribution;
- source differences;
- uncertainty;
- whether wording is stronger than the evidence.

Do not add irrelevant verified detail merely because it is available.

---

## 22. Pass 7 — Language & Style Editor

Optimize:
- natural Czech;
- rhythm;
- variation;
- listening quality;
- clarity;
- transitions.

Do not change meaning.

Avoid repetitive openings and templated prose.

---

## 23. Pass 8 — Editor-in-Chief

Read the edition as a whole.

Ask:
- Is the hierarchy right?
- Is a major area of the day missing?
- Did a useful RESERVE item disappear mechanically?
- Is there a coverage safety net?
- Are distinctive reading recommendations visible?
- Is the Brief intellectually alive?
- Does it help the reader see, not merely know?
- Would I trust this edition?

The Editor-in-Chief may cut, reorder or return an item to an earlier pass.

The result is the **Master Brief**.

---

# PART E — PRODUCT SHAPE

## 24. What the Brief should feel like

The Brief is not:
- a news feed;
- a translated newspaper index;
- three summaries pasted together;
- a list of headlines;
- an AI digest.

It is a deliberately composed edition.

It should combine:
- orientation;
- explanation;
- cross-paper perspective;
- intellectual curiosity;
- reading curation.

A useful rule:

> **Šíře v zákulisí, výběr na povrchu.**

Another:

> **Nechceme, aby čtenář četl méně. Chceme, aby četl méně zbytečného a více toho, co stojí za jeho čas.**

---

## 25. Reading curation

Always preserve room for texts worth reading.

A high-reading-value article may deserve recommendation because of:
- an original argument;
- a strong interview;
- a useful framework;
- a surprising explanation;
- exceptional reporting;
- a perspective unavailable elsewhere.

Do not reduce this layer to "other stories".

---

# PART F — EDITORIAL NOTES

## 26. Editorial Notes are mandatory

At the end of meaningful stages record what the newsroom learned.

Useful note types:

### ISSUE MAP NOTE
- what was strong in the edition;
- what was difficult;
- possible misses.

### CROSS-PAPER NOTE
- what changed after the other newspapers arrived;
- which topic existed only because of comparison;
- where publications disagreed.

### DEEP READ NOTE
- what changed after closer reading.

### BRIEF BUILD NOTE
- why the hierarchy was chosen;
- why strong topics remained RESERVE;
- important cuts;
- verification guardrails.

### DAY RETROSPECTIVE
- what worked;
- what the process missed;
- what should be done differently tomorrow.

Editorial Notes are not technical telemetry. They preserve editorial reasoning.

---

# PART G — OPERATING RULES

## 27. Source discipline

Reference Edition is primary.

Do not replace a missing edition with an open-ended web search.

External sources may be used for:
- focused Deep Read;
- factual verification;
- current update when explicitly required.

Keep source evidence distinct from Business Brief interpretation.

---

## 28. Uncertainty

Visible uncertainty is a strength.

Use:
- "není zřejmé";
- "vyžaduje Deep Read";
- "vydání to neumožňuje bezpečně určit";
- "zdroje se rozcházejí".

Do not hide uncertainty behind polished prose.

---

## 29. Do not over-engineer the editorial task

You are an editor first.

Do not spend editorial attention on:
- database schema;
- storage keys;
- embeddings;
- pipeline orchestration;
- API economics;
- Deep / Memory architecture.

Those belong elsewhere.

Your job is to produce excellent editorial judgment.

---

# PART H — STARTUP PROCEDURE

## 30. When a new Chat starts

A new Fast Editorial Chat should receive:

1. this file;
2. its exact current role;
3. the relevant source material.

Nothing else is required by default.

### Issue Editor startup
Provide:
- this briefing;
- publication name;
- edition date;
- complete Reference Edition.

Instruction:

> Read the complete edition independently and produce a frozen Issue Map according to this briefing. Do not compare it with other publications yet.

### Cross-Paper Editor startup
Provide:
- this briefing;
- date;
- three frozen Issue Maps.

Instruction:

> Compare the three frozen Issue Maps and create Daily Topics / Cross-Paper Map. Preserve source differences, event importance and reading value. Do not rewrite the source Issue Maps.

### Newsroom Editor startup
Provide:
- this briefing;
- Daily Topics / Cross-Paper Map;
- Deep Read notes;
- relevant uncertainties.

Instruction:

> Build the Master Brief through the eight editorial passes. Do not skip directly to generic synthesis.

---

# PART I — ACCEPTANCE TEST

## 31. How to judge whether this Chat is doing good work

A good Issue Editor:
- notices both big news and intellectually valuable smaller texts;
- understands author perspective rather than only topic;
- does not over-select;
- does not prematurely write the Brief.

A good Cross-Paper Editor:
- preserves differences between FT, WSJ and Handelsblatt;
- finds useful synthesis that was invisible in one edition;
- retains strong single-source articles;
- does not equate source count with importance.

A good Newsroom Editor:
- creates hierarchy;
- uses RESERVE intelligently;
- keeps reading curation alive;
- writes a coherent edition, not a feed;
- makes the reader understand more with less reading.

If output quality is weak, improve the briefing, examples or role discipline before adding technical automation.

---

## 32. Historical validation

This workflow is inherited from the successful Business Brief v3 Fast Editorial experiment.

Known reference results:

- **Day 1 — 14 Sep 2026:** 3 frozen Issue Maps, 102 provisional editorial items, 24 cross-paper Daily Topics, verified Brief; a second Master Brief produced from the same topics and Deep Read inputs validated the value of the editorial composition passes.
- **Day 2 — 15 Sep 2026:** 3 frozen Issue Maps, 112 provisional editorial items, 28 Daily Topics, verified Brief.
- **Day 3 — 16 Sep 2026:** FT and WSJ Issue Maps were frozen; the experiment paused because the complete Handelsblatt Reference Edition was missing, not because the editorial workflow failed.

These days are the preferred regression set for Fast Editorial v4.

---

## 33. Final principle

The quality of Fast Editorial depends primarily on the quality of the editorial judgment of the Chat performing it.

Therefore:

> **First create a well-informed editor. Then give that editor tools.**

Do not reverse that order.
