# acasara

Többnyelvű, **egyoldalas** statikus weboldal egy közvetlen ingatlanfelvásárló cégnek (acasara.ro).
Kinézet: preloader, ráúsztatott navbar, videó hero, kalkulátor, idővonal, bordó sáv, GYIK, osztott
megkeresés-panel, díszítő Románia-térkép a láblécben.

**A szöveges tartalom minden eleme az azzupp.com-ról való** (11 nyelvi oldal), a márkanév „AZZUPP"
helyett „acasara.ro". Nincs kitalált állítás, szám vagy esettanulmány az oldalon.

## Futtatás

```
cd C:\Users\miklo\acasara-ro
uv run --no-project python -m http.server 8731 --bind 127.0.0.1
```

Aztán: http://127.0.0.1:8731/index.html (a `file://` alatt a videók és a nyelvváltó akadozhat).

## Felépítés

```
index.html          generált, ne kézzel szerkeszd (a főoldal)
kezdjuk-el.html     a jelentkezős oldal (generált); a menü a főoldal szekcióira (#horgonyokra) mutat
build.py            oldalgenerátor; a román alapszövegeket az assets/i18n.js "ro" blokkjából olvassa
form-data.json      a két űrlap select/rádió/jelölőnégyzet értékei (a forrás magyar értékei)
assets/
  i18n.js           MINDEN szöveg, 11 nyelven (érvényes JSON a "window.T =" után)
  site.css          közös stíluslap
  site.js           nyelvváltó, preloader, navbar, reveal, hero-lejátszó, idővonal, kalkulátor, űrlap
  fonts/            Onest, helyi woff2 (SIL OFL)
  img/  video/      Pexels anyagok
```

Módosítás után: `uv run --no-project python build.py` (ezen a gépen nincs telepített Python). A build a
CSS/JS hivatkozásokra `?v=` bélyeget tesz, ezért CSS/JS-módosítás után is futtatni kell.

## Szekciók (a forrás sorrendjében)

hero → négy előny-sáv → **kalkulátor** (`#kalkulator-section`) → **5 ok** (`#miert`) → **3 lépés** idővonal
(`#folyamat`) → **mit vásárolunk** (`#ingatlanok`) → **„Decizia vă aparține"** sáv → **GYIK** (`#gyik`) →
**megkeresés** (`#kapcsolat`) → lábléc.

## Nyelvek

`hu, en, ro, de, sk, fr, it, es, pl, ru, zh` (a forrás nyelvei, a forrás nyelvválasztójának sorrendjében).
Ukrán nincs, mert a forráson sincs. A kínai a forrás `/cn/` oldaláról jön (a forrás saját `/zh/` linkje hibás).
Sorrend: `?lang=xx` az URL-ben → `localStorage` → böngésző nyelve → `ro`.

A fordítás `data-i18n="kulcs"` attribútummal működik, a `data-i18n-attr="aria-label"` a megadott
attribútumot írja át. Új szöveg: ugyanazt a kulcsot kell felvenni **minden** nyelvi blokkba. Paritás-ellenőrzés:

```
node -e 'global.window={};require("vm").runInThisContext(require("fs").readFileSync("assets/i18n.js","utf8"));const T=window.T,b=Object.keys(T.ro);for(const c of window.LOCALES.map(l=>l.code)){const m=b.filter(k=>!(k in T[c]));if(m.length)console.log(c,m)}console.log("kész",b.length)'
```

A kínai nyelvhez nincs betűfájl, a rendszer CJK betűjére esik vissza (PingFang SC / Microsoft YaHei / Noto Sans SC).

## Űrlapok

- **Kalkulátor** (`#calcForm`): a forrás kalkulátorának mezői (ország, város, irányítószám, utca, típus, alapterület-csúszka,
  szobák, építés éve, emelet, állapot, kilátás, komfort, extrák, név, telefon, e-mail, GDPR), majd az opcionális
  készpénzajánlat-lépés. A menet a forrásé: első küldésre előbb a készpénzajánlat kérdése jön, aztán fut.
- **Megkeresés** (`#enquiry`): a forrás kapcsolatűrlapjának mezői négy lépésben (megkereső típusa és ingatlantípus →
  cím, méret, állapot → hirdetés, ár → név, e-mail, telefon, megjegyzés, hozzájárulás). Lépésenként ellenőriz.

**Egyik sem küld sehova.** A `site.js` elején az `ENDPOINT = { lead: "", estimate: "" }` üres (`// TODO`).
Üresen az űrlapok validálnak, és a forrás visszaigazoló szövegét mutatják. A GDPR/szerveroldali validáció hiányzik.

**Becslés:** az azzupp.com kalkulátora az értéket egy privát szerveroldali modellből (`becsles.php`, forintban)
számolja. Ezt nem másoltam és nem is találtam ki: a kalkulátor most csak az adatokat gyűjti. A forrás szövegei
(„Estimare preliminară imediată") a végleges működésre utalnak, ezért ezek addig nem teljesen igazak, amíg
az `estimate` endpoint nincs bekötve (vagy a modell nincs átvéve). A forrás eredményablaka (max, min −6%) és a
pénznemváltó emiatt nincs az oldalon.

## Betűtípusok

Helyből szolgált, nyílt licencű (SIL OFL) betűk: **Onest** (szöveg + display, latin, latin-ext, cirill). Csere: `--font-display` és `--font-body` a `site.css` elején. Nincs külső (CDN) betöltés.

## Képek és videók

Minden Pexels-ről, **Pexels License** alatt (ingyenes, kereskedelmi használatra is, névmegjelölés nem kötelező):

- videó: 14864541 (Sânpetru), 14864002 (Brassó óváros), 14665012 (kisváros), 14665250 (Fekete templom),
  18070174 (óváros), 19806381 (Kolozsvár)
- kép: 7641904, 18153132, 9308434, 8962228, 8962684, 7599735, 7203883, 8469937, 4246267, 261621

`assets/img/key.png` stock fotóból körbevágott kulcs (Pexels #3868576). A hat videó összesen ~41 MB: élesben
tömörítés vagy CDN kell hozzá.

## Márkanév és domain

Az `acasara` a román *acasă* („otthon") szóból jön. A domain-ellenőrzés állapota: **acasara.com** szabad volt
(RDAP), **acasara.ro** nincs NS rekordja (nem bizonyíték, erősítsd meg a rotld.ro-n), **acasara.eu** nem ellenőrzött.
Ez **nem védjegykutatás**: OSIM (RO) és EUIPO keresés hátravan.

## Még nyitott

- Telefonszám, e-mail és cégadatok (a forráson nincs): keresd a `[`, `07XX` mintát a `build.py`-ban.
- Űrlap- és becslés-endpoint, spam-védelem, GDPR-tájékoztató oldal (a forrásnak van `/adatvedelem.html` oldala),
  cookie-banner (ha analitika jön).
- A forrás blogja (`/blog`) és adatvédelmi oldala nincs átvéve.
- `sitemap.xml`, `robots.txt`, `hreflang` a 11 nyelvhez.
- Képek: a forrás oldalán nincsenek fotók (csak logó és zászlók), ezért az itteni képek és videók továbbra is Pexels stock anyagok.
