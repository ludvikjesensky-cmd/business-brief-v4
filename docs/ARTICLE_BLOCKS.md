# Controller-directed article blocks

Experimentální lokální alternativa k odhadu bbox hranic modelem. Controller (zatím asistent s vizuální kontrolou) rozhoduje o článcích, relevanci, pořadí řádků, odstavcích a typografických spojích. Python pouze připravuje neutrální evidenci a vykonává explicitní plan. Bez API calls, uložené Visual Page Map, produkční queue nebo změny role Ingestoru/Assembleru.

## Opakovatelný postup

```bash
bb-article-blocks prepare --pdf work/prepared.pdf --page 2 --output work/page2
# Controller prohlédne page.png a blocks.txt a vytvoří plan.json z plan-template.json.
bb-article-blocks assemble --blocks work/page2/blocks.json --plan work/page2/plan.json --output work/page2/result
```

Bez instalovaného entrypointu lze použít `PYTHONPATH=src python -m business_brief.article_blocks`. Vyžaduje stávající PyMuPDF, žádnou novou závislost. Pro nové vstupy doporučen nový adresář. Rotované PDF je odmítnuto; normalizaci musí dodat upstream. Prepare neprovádí OCR.

`blocks.json` obsahuje zdrojový PDF hash, fyzické číslo stránky, rozměry, přesné textové řádky s lokálními ID a bbox. `native_groups` jsou technické PDF bloky, nejsou to automaticky články ani spolehlivé odstavce. `page_digest` váže celou evidenci k planu. ID jsou stabilní pro stejný soubor/extrakci; přenos mezi soubory/stránkami bez správného digestu není povolen.

## Plan

```json
{
  "version": "article-blocks-v1",
  "page_digest": "digest z blocks.json",
  "articles": [{
    "id": "article-1",
    "title_ids": ["L0001"],
    "intro_ids": [],
    "byline_ids": [],
    "paragraphs": [["L0002", "L0003"], ["L0004"]],
    "relevance": "controller decision",
    "continuation": null
  }],
  "excluded": [{"ids": ["L0005"], "reason": "photo caption"}],
  "hyphenation": {"L0002": "remove"},
  "no_space_after": []
}
```

Pořadí v `paragraphs` a uvnitř každého odstavce je závazné; Python neřadí podle x/y a nehádá sloupce. Nadpis/intro/byline/body/exclusions mají výhradní vlastnictví ID; neznámé ID či duplicitní přiřazení jsou chybou. Byline je evidovaná v auditu, čtenářský výstup zůstává pouze `title` a `text`.

`hyphenation` je explicitní rozhodnutí pro spoj s dalším řádkem téhož odstavce: `remove` odstraní tiskový spojovník, `keep` zachová lexikální spojovník. Bez rozhodnutí se původní spoj zachová se zalomením a warningem. Nepoužité rozhodnutí je chyba. `no_space_after` je výhradně kontrolovaný spoj samostatné iniciály s následujícím slovem, ne obecné přepisování textu. Volitelné `title_text` může měnit pouze whitespace původního titulku (např. slepená slova z PDF), nikoli jeho znaky.

## Výstupy a kontrola

`articles.json`: pole `title`/`text`, čitelné odstavce z přesné zdrojové evidence. `audit.json`: zdrojový/plan hash, IDs a vlastníci, rozhodnutí o relevanci/continuation, počty zahrnutých/vyloučených řádků a warnings. Vynechané IDs jsou viditelné; source duplicity či vadné znaky se hlásí, automaticky se nemažou. Zápis JSON je přes dočasný soubor a replace.

`needs_review=false` znamená pouze absenci mechanických warnings. `semantic_validation=controller_authored_not_independently_verified` výslovně připomíná, že úplnost článku, role, pořadí a správnost exclusion stále posuzuje controller. Zachování znaků neprokazuje správné seskupení ani pravdivost novinového obsahu. Pokračování přes stránky se neslučují automaticky.

## WSJ strana 2 — první kontrolovaný průchod

565 řádků, 107 technických PDF groups. Controller sestavil dva hlavní ekonomické články a čtyři krátké zprávy; grafy včetně legend/poznámek, fotografie/popisky, credits, opravy, hlavička a publication utility byly explicitně vyřazeny. Drop caps S/H/Y spojeny explicitně, slepený titulek opraven jen vložením mezer; tiskové a lexikální spojovníky reviewed.

Naměřeno při původním průchodu: prepare přibližně 0,22 s; assemble přibližně 0,003 s. Nejde o čas celého workflow: příprava kódu, controllerovo přiřazení a čtení/kontrola v těchto časech nejsou. Vzorek dokládá technickou funkci, nikoli univerzální automatickou rekonstrukci či produkční acceptance. Placené API a produkce se neměnily. Licencované články/PDF/obrazy a konkrétní source plan zůstávají lokálními artefakty, ne součástí veřejného repository.
