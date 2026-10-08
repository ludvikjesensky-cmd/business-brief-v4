# WSJ Edition Watcher — Railway PoC

Stav: implementovaný PoC, dosud bez živého automatického stažení a bez nasazení.
Samostatná služba; nenahrazuje existující pipeline. Žádná hesla ani cookies ze Safari
nejsou součástí balíčku.

## Ověřený mechanismus

Reader volá `openUrlHotspot(1)` → `downloadFullEdi()`. Funkce sestavuje POST formulář
na `SERVER_NAME + /action/php-script/down_full.php`, cílený do `formPhodir`.
Pole: `pSetup`, `MACHINEID`, `language`, `TAUID`, `file`, `archiveName`, `edition`
a opakované `checkedpdf[]` podle seznamu stránek aktuálního vydání.
Metadata ručně staženého PDF potvrzují cestu:

```
https://wsj-bcdn.newsmemory.com/eebrowser/ipad/html5.check.26022621//action/php-script/down_full.php
```

Datum ani soubory stránek nehádáme. PoC používá existující tlačítko a autentizaci
readeru. Přesná životnost session, serverové kontroly přístupu, stabilita cesty
a kompatibilita s Railway jsou neověřené.

## Railway

1. Samostatná služba z adresáře tohoto balíčku, Dockerfile build, jedna replika.
2. Persistent volume připojený na `/data` (profile, reference, SQLite outbox).
3. Region Amsterdam, sleep vypnutý. Neukládat session do image/repozitáře/logů.
4. Proměnné: `MODE=login`, `ADMIN_PASSWORD` náhodné alespoň 24 znaků, `DATA_DIR=/data`.
   `PORT` dodá Railway. Healthcheck `/health`; ten potvrzuje život procesu,
   nikoli připravenost WSJ nebo pipeline. Autentizovaný `/status` ukazuje stav.
5. Dočasná HTTPS doména pro přihlášení: `/vnc.html?autoconnect=true&resize=scale`.
   HTTP Basic username `admin`, password z `ADMIN_PASSWORD`. Heslo nikdy v URL.
   Veřejné rozhraní umožňuje ovládat browser: zapnout pouze pro vlastní přihlášení.
6. Uživatel se běžně přihlásí k WSJ v tomto vzdáleném browseru a otevře dnešní číslo.
   MFA/CAPTCHA dokončí ručně. Přihlášení ze Safari se nekopíruje.
7. Změnit `MODE=once` a redeploy: browser znovu použije stejný profil, jednou stáhne
   dnešní vydání a zůstane se stavem pro kontrolu. VNC je v tomto režimu vypnuté.
8. Až projde živý test, nastavit `MODE=watch`. Kontroluje 07:50–09:00 Europe/Prague,
   každé 2 minuty, při chybách backoff. Mimo okno nespouští WSJ requesty.
9. Po třech chybách/požadavku na autentizaci pozastaví daný den. Náprava:
   přepnout do `login`, obnovit session, pak znovu `once`/`watch`.

Chromium běží jako `pwuser`, sandbox je vyžadovaný. Pokud hostitel nepovolí potřebné
user namespaces, nesnižovat ochranu přes `--no-sandbox`; ověřit kompatibilní runtime.
VNC porty nejsou publikované: reverse proxy ověřuje uživatele i pro websocket.
Před zapnutím služby zkontrolovat dostupné kredity a účet Railway.

## Validace a výstup

Počet stránek musí odpovídat `#pullDownPage`; kontroluje se datum na titulce,
PDF signatura, strict parser, čitelnost textu každé stránky a výskyt očekávaného
označení na příslušné stránce. Výskyt označení není důkaz redakční kompletnosti
obsahu. PoC neřeší obrazové PDF: při chybějícím textu se zastaví.
Současná edice je pevně The Wall Street Journal; při změně UI se zastaví.
Číslo načtené v readeru musí zůstat stejné před i po downloadu.

```
/data/reference/YYYY-MM-DD/wsj/edition.pdf
/data/reference/YYYY-MM-DD/wsj/manifest.json
/data/outbox.sqlite3
```

Reference se zveřejní atomickým přejmenováním adresáře. SQLite událost
`WSJ_REFERENCE_READY` má stabilní jedinečné ID, hash a lokální cesty.
Pád po zveřejnění před zápisem události opraví recovery při restartu.
Duplicita nevytvoří další událost. Revidovaná vydání vyžadují ruční rozhodnutí.

## Pipeline a upozornění — zbývající integrace

PoC vytváří trvalý outbox, **dosud nespouští skutečnou navazující pipeline a neposílá
upozornění**. Záměrně nepředpokládá rozhraní v4, které nebylo potvrzeno.
Consumer musí přijmout PDF (lokální cesta není dostupná jiné Railway službě bez
transportu), deduplikovat `event_id` a označit `acked=1` až po trvalém přijetí.
Další práce: napojit potvrzený storage/ingest kontrakt a notifikace na AUTH_REQUIRED,
VALIDATION failure a deadline. Pouhé zapsání události není end-to-end spuštění.
Nevycházející/kombinovaná čísla zatím nemají kalendář; po 09:00 automat nevybere
včerejší vydání jako náhradu.

## Kontroly

```
python -m unittest discover -s tests -v
```

Jednotkové kontroly: login HTML, špatné datum, neúplný soubor, změněné pořadí stránek,
idempotence, zotavení outboxu a letní/zimní čas.
Docker build, sandbox, VNC, skutečné WSJ click/download a obnovení session je nutné
ověřit na serveru. Žádný testovací úspěch nenahrazuje tyto živé kontroly.
