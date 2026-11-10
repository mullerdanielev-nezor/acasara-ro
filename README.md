# acasara

Többnyelvű, **egyoldalas** statikus weboldal egy közvetlen ingatlanfelvásárló cégnek.
Szerkezetileg a wildbran.pt felépítését követi: preloader, ráúsztatott navbar, teljes
szélességű videó hero, kézírásos címkés scatter szekció, elmosott hátterű folyamat-sáv,
történetkártyák, CTA, footer.

## Futtatás

Statikus fájlok, de a `file://` protokoll alatt a videók és a nyelvváltó URL-kezelése
akadozhat, ezért érdemes kiszolgálni:

```
cd D:\Letolt\acasara
python -m http.server 8731 --bind 127.0.0.1
```

Aztán: http://127.0.0.1:8731/index.html

## Felépítés

```
acasara/
  index.html              a teljes oldal, horgonyokkal:
                            #top #cerere #cumparam #proces #cum #povesti #contact
  logo.html               a három logóirány összehasonlítása (nem publikus oldal)
  build.py                oldalgenerátor — a navbar/footer/head innen jön
  assets/
    site.css              közös stíluslap
    i18n.js               10 nyelv szótára
    site.js               nyelvváltó, preloader, navbar, reveal, parallax, űrlap
    img/  video/          Pexels anyagok
```

**Az oldalakat ne kézzel szerkeszd.** A navbar, a footer és a `<head>` a `build.py`
partialjaiból áll elő. Módosítás után:

```
python build.py
```

## Nyelvek

Tíz nyelv: `ro` (alap), `en`, `hu`, `de`, `it`, `es`, `fr`, `pl`, `uk`, `ru`.

A nyelv sorrendben ebből dől el: `?lang=xx` az URL-ben → `localStorage` →
a böngésző nyelve → `ro`. A választás bekerül az URL-be, így a másolt link
megtartja a nyelvet, és az oldalon belüli linkek is viszik tovább.

A fordítás `data-i18n="kulcs"` attribútummal működik; a `data-i18n-attr="aria-label"`
nem a szöveget, hanem a megadott attribútumot írja át.

### Új nyelv hozzáadása

1. `assets/i18n.js` → `window.LOCALES` tömbbe egy `{ code, label }` sor.
2. Ugyanitt a `window.T` objektumba egy új blokk **ugyanazokkal a kulcsokkal**.
3. Paritás-ellenőrzés:

```
node -e 'global.window={};require("vm").runInThisContext(require("fs").readFileSync("assets/i18n.js","utf8"));const T=window.T,b=Object.keys(T.ro);for(const c of window.LOCALES.map(l=>l.code)){const m=b.filter(k=>!(k in T[c]));if(m.length)console.log(c,m)}console.log("kész")'
```

## Űrlapok

**Négylépcsős megkeresés-űrlap** közvetlenül a hero alatt (`#cerere`).
Lépések: ki vagy → az ingatlan → ár és hirdetés → elérhetőség. Az azzupp.com
mezőkészletét követi. Lépéssáv, folyamatjelző és „Tovább / Vissza" gombok.

A léptetés csak akkor enged tovább, ha az adott lépés kötelező mezői ki vannak
töltve: 2. lépés → pontos cím; 4. lépés → vezeték- és keresztnév, e-mail (formátum-
ellenőrzéssel), telefon, hozzájárulás. A sávon visszafelé lehet kattintani, előre nem.
Küldéskor mind a négy lépés újra ellenőrződik, és hibánál a hibás lépésre ugrik vissza.
Nem küld sehova. A `site.js` `enquiryForm()` függvényében a `// TODO: POST`
megjegyzésnél kell bekötni az endpointot vagy a CRM-et. A payload:

```
{ role, ptype, paddress, psize, pplot, pcond, padv, plisting, pprice,
  plast, pfirst, pemail, pphone, pmsg, lang }
```

(Az `offerForm()` a korábbi, rövid űrlaphoz tartozott; az aloldalakkal együtt
kikerült, a függvény ártalmatlanul bent maradt a `site.js`-ben.)

A kliensoldali validáció él (cím, név, telefon és a hozzájárulás kötelező), de ez
csak kényelmi réteg — **a szerveroldali validáció és a GDPR-kezelés még hiányzik.**

## Logó

Nincs jel, csak a domain: **acasara.ro** szóvédjegyként, Vinila 900-as vastagságban.
A `.ro` a `.tld` osztályt kapja — a fejlécben halványabb, a preloaderben bordó.
A korábbi három logóirány (`logo.html`) elvetve és törölve.

## Hero videó

Hat romániai klip megy egymás után, átúsztatással (`heroPlaylist()` a `site.js`-ben),
összesen **110 másodperc**, mielőtt bármi ismétlődne — nincs látható újraindulás.
A sorrend a `#heroMedia` elem `data-clips` attribútumában van, vesszővel elválasztva;
oda írj be vagy vegyél ki klipet. Két egymásra fektetett `<video>` váltakozik, a
következő klip mindig előtöltődik. Ha egy klip hibázik vagy nem töltött be időben,
az aktuális megy tovább ahelyett, hogy elsötétülne.

## Gyorsítótár

A `build.py` a CSS és JS hivatkozásokra a fájl módosítási idejéből képzett `?v=`
bélyeget tesz. Stíluslap- vagy JS-módosítás után **futtasd a buildet**, különben a
böngésző a régi fájlt használja. (Pontosan ebbe futottam bele fejlesztés közben.)


## Kapcsolatfelvevő — osztott panel

A `#cerere` szekció két hasábos: bal oldalt bordó panel az ígérettel, a saját rajzolású
kulcs-PNG-vel és három bizalmi ponttal, jobbra a négylépcsős űrlap. 900 px alatt egymás
alá kerül.

### A kulcs

`assets/img/key.png` — **stock fotóból körbevágva**: Pexels #3868576 (sárgaréz kulcsok
világos márványon, Pexels License). A bal felső, felirat nélküli ajtókulcsot vágtam ki.

A kivágás menete: a márvány „világos és majdnem szürke", a sárgaréz viszont telített és
meleg, így színküszöbbel különválik — ettől a kulcs fejében lévő lyukak is átlátszóvá
válnak, nem csak a külső háttér. Utána medián-szűrő a pixelzajra, a legnagyobb összefüggő
folt megtartása (így a képbe lógó betűkockák törmeléke eltűnik), végül egy pixel erózió és
enyhe elmosás, hogy ne ollóval kivágottnak tűnjön a széle.

Két zsákutca volt: a sötét hátterű kulcsfotóból a fényerő-alapú kivágás szétesett (a kulcsok
saját árnyéka is kiesett), a kép alsó kulcsa pedig **Mitsubishi-feliratú autókulcs** —
idegen védjegy, ezért nem használható.

## Fejléc

Lebegő kapszula: fix pozíció, teljes lekerekítés, üveges háttér a videó fölött, és
betöltéskor rugós mozgással ereszkedik le. A heróból kiérve behúz `1180px`-re, tömör
sötét háttérre vált és erősebb árnyékot kap. A menüpontok 1040 px alatt eltűnnek, hogy
ne törjenek két sorba; a nyelvváltó és az ajánlatkérő gomb marad.

## Lábléc térkép

Románia körvonala **valódi határadatból**: a `georgique/world-geojson` közkincs határfájljából
vettem a legnagyobb gyűrűt, Ramer–Douglas–Peucker algoritmussal 1209 pontról 85-re egyszerűsítettem,
és szélességkorrigált equirectangular vetítéssel tettem SVG-koordinátákba. A 12 város a tényleges
hosszúsági/szélességi fokain ül, Bukarest a „szív". A vonalak görgetésre rajzolódnak ki.

Ellenőrizve: mind a 19 ér 209 mintapontja és mind a 12 városcsomópont a határon belül esik.

## Fontos tudnivalók élesítés előtt

### Betűtípusok — licencelni kell

A `site.css` a **PP Pangaia**, **Vinila** és **Marrydale** fontokat a wildbran.pt
Webflow CDN-jéről tölti be. Ezek kereskedelmi, licencelt betűk, **nem a mieink**.
Jelenleg csak a Vinila (szöveg + display) és a Marrydale (kézírásos címkék) van
használatban; a PP Pangaia már nincs, a `@font-face` sora törölhető.

Élesítés előtt: licenc vásárlása és self-hosting, vagy csere a `--font-display`,
`--font-body`, `--font-hand` változókban. A fallback stackek tiszták, az oldal
összeesés nélkül visszaesik rájuk.

### Képek és videók

Minden Pexels-ről, **Pexels License** alatt: ingyenes, kereskedelmi használatra is,
névmegjelölés nem kötelező. A forrás-ID-k:

- videó: 14864541 (Sânpetru), 14864002 (Brassó óváros), 14665012 (kisváros),
  14665250 (Fekete templom), 18070174 (óváros), 19806381 (Kolozsvár)
- kép: 7641904, 18153132, 9308434, 8962228, 8962684, 7599735, 7203883, 8469937, 4246267, 261621

### Márkanév és domain

Az `acasara` nevet a román *acasă* („otthon") adja. Az ellenőrzés állapota:

- **acasara.com** — szabad volt, RDAP-pal ellenőrizve (Verisign, HTTP 404)
- **acasara.ro** — nincs NS rekordja, tehát valószínűleg szabad. **Ez nem bizonyíték:**
  regisztrált domainnek is lehet, hogy nincs NS-e. Erősítsd meg a rotld.ro-n.
- **acasara.eu** — **nem ellenőrzött**. A `.eu` RDAP-lekérdezés nálunk nem működött
  (a kontroll is megbukott), szóval erről semmit nem állítunk.

A domain-ellenőrzés **nem védjegykutatás**. OSIM (RO) és EUIPO keresés még hátravan.

### Placeholderek

Telefonszám, e-mail, cím, cégadatok, közösségi linkek és a „Termeni / Politica"
oldalak mind kitöltetlenek. Keresd a `[` és a `07XX` mintát.

## Ami még nincs kész

- az űrlap szerveroldali fogadása, spam-védelem, GDPR-tájékoztató
- cookie-banner (jelenleg nincs sütihasználat, de analitika bekötésekor kelleni fog)
- a történetkártyák mögött nincsenek valódi cikkek (a `href` mindenhol `#`)
- `sitemap.xml`, `robots.txt`, `hreflang` tagek a 10 nyelvhez
- a hat videó összesen ~41 MB — élesben tömörítés vagy CDN kell hozzá
