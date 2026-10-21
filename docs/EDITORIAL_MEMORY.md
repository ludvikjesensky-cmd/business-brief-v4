# Editorial Memory — Business Brief v4

Tento dokument popisuje **produktovou Editorial Memory**, nikoli Project Memory v `project-memory/`.

Editorial Memory je dlouhodobá hybridní znalostní vrstva nad immutable Article Records, derived enrichmentem, denními tématy, Story Threads, Signals, Trends, publikovanými výstupy a jejich provenance.

Její role:
- rozpoznat, co je dnes nové a co opakované;
- přidat kontinuitu přes Story Threads;
- zachytit dnešní Signals bez předčasného vyhlašování Trendů;
- sledovat vývoj Trendů v čase včetně oslabení, proti-signálů a obratu;
- podporovat porovnání zdrojů;
- umožnit Trendy, Analýzy a Business Intelligence;
- zabránit tomu, aby Brief opakoval stejné sdělení bez nové hodnoty.

## Knowledge model

```text
Article / current-day event
→ Story Thread
→ Signal
→ Trend
→ Analysis / Business Intelligence
```

Story Thread je konkrétní pokračující příběh. Signal je nový důkaz. Trend je širší dlouhodobý fenomén, který nevzniká z jednoho článku ani jednoho daily topicu.

Kanonický enrichment/knowledge kontrakt je v [ENRICHMENT.md](ENRICHMENT.md). Article-level enrichment zůstává derived sidecar vázaný na přesný `article_id + article_record_sha256`; canonical Article Record bytes se nemění.

## Hybrid retrieval

Memory není pouze vector RAG. Kombinuje:
1. SQL metadata a přesné relationships;
2. PostgreSQL full-text;
3. multilingual vector retrieval přes BB-EMBEDDING-V1;
4. čas a provenance;
5. entities, topics, industries, geographies, Story Threads, Signals a Trends;
6. editorial history a publikované výstupy.

Cohere vytváří multilingual embeddings. Supabase/Postgres pgvector ukládá a porovnává numerické vektory a sám o sobě není jazykový model.

## Product boundary

Pro ranní Brief platí:

> **Daily = delta. Memory = context.**

Dnešní vydání je primární. Memory jej podporuje, ne přebíjí. Composer nejdřív seskupí dnešní corpus a teprve potom doplňuje continuity. Starý článek nikdy nenahrazuje chybějící dnešní coverage.

Pro Trendy a Analýzy platí:

> **Memory = primary knowledge material.**

Přijetí Story Threadu nebo Trendu je explicitní reviewed knowledge decision. Candidate vytvořený enrichmentem nebo Composerem není automaticky accepted knowledge.

Only explicitly content-accepted source generations may feed Article Records and downstream retrieval. Technical persistence flags do not approve source content.
