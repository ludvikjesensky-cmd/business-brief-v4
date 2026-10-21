# Editorial Memory — Business Brief v4

Tento dokument popisuje **produktovou Editorial Memory**, nikoli Project Memory v `project-memory/`.

Editorial Memory je dlouhodobá evidence nad zdroji, vydáními, texty, tématy, tvrzeními, argumenty, publikovanými výstupy a jejich provenance.

Její role:
- rozpoznat, co je dnes nové a co opakované;
- přidat kontinuitu;
- ukázat vývoj tématu;
- podporovat porovnání zdrojů;
- umožnit Trendy a Analýzy;
- zabránit tomu, aby Brief opakoval stejné sdělení bez nové hodnoty.

Pro denní Brief je dnešní vydání primární; Memory jej podporuje, ne přebíjí. Pro Trendy a Analýzy / Business Intelligence je Memory hlavní znalostní surovinou. Retrieval má být selektivní a provenance-preserving.

Memory je hybridní redakční znalostní systém: SQL metadata, full-text, vectors, provenance, čas, entity, Story Threads, Signals, Trends a editorial history jsou rovnocenné stavební části. RAG je technika nad Memory. **Daily = delta. Memory = context.**


Only explicitly content-accepted generations should feed future article retrieval. Technical persistence flags do not approve source content; the first v2 page-1 object is superseded acceptance evidence (HISTORY/D020).

## Enrichment and knowledge contract — D028
[ENRICHMENT.md](ENRICHMENT.md) defines the derived, versioned article/topic knowledge model and normalized persistence design. Article / Event → Story Thread → Signal → Trend → Analysis / BI retains v3 intent. Trends span repeated evidence over time; Story Threads track concrete continuing stories; signals can support, weaken, contradict or neutrally relate. Candidate labels never become accepted knowledge without explicit evidence review/promotion. A single article never establishes a Trend.

Indexer hybrid retrieval and Composer knowledge_links consume exact reviewed metadata/history without rewriting Article Records. Composer works with today's concrete story and signal/delta; knowledge links do not choose inclusion/hierarchy, erase article perspective or define the final angle. Offline integrity helpers are implemented; Q019 records physical schema/adapters/review and real-source acceptance gates.
