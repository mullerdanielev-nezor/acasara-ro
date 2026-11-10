# -*- coding: utf-8 -*-
"""Acasara — static page generator.

Emits the six HTML pages from shared partials so the navbar, footer and head
stay identical everywhere. Re-run after editing a partial:  python build.py
"""
import io, os

HERE = os.path.dirname(os.path.abspath(__file__))

def stamp(rel):
    """Append a version query so browsers pick up edited CSS/JS instead of a cached copy."""
    try:
        return "%s?v=%d" % (rel, int(os.path.getmtime(os.path.join(HERE, rel))))
    except OSError:
        return rel

# ---------------------------------------------------------------- icons

ARROW = ('<span class="btn-circle"><svg viewBox="0 0 17 14" fill="none" aria-hidden="true">'
         '<path d="M1 7h13M9.6 1.4 15.5 7l-5.9 5.6" stroke="currentColor" stroke-width="2" '
         'stroke-linecap="round" stroke-linejoin="round"/></svg></span>')

PLAY = ('<span class="btn-circle"><svg viewBox="0 0 12 14" fill="none" aria-hidden="true">'
        '<path d="M2 1.6 11 7l-9 5.4V1.6Z" fill="currentColor"/></svg></span>')

CHECK = ('<svg viewBox="0 0 22 22" fill="none" aria-hidden="true">'
         '<path d="M4 11.5 9 16.5 18 6" stroke="currentColor" stroke-width="2.6" '
         'stroke-linecap="round" stroke-linejoin="round"/></svg>')

CROSS = ('<svg viewBox="0 0 22 22" fill="none" aria-hidden="true">'
         '<path d="M6 6l10 10M16 6 6 16" stroke="currentColor" stroke-width="2.6" '
         'stroke-linecap="round"/></svg>')

STORY_ARROW = ('<span class="story-arrow"><svg viewBox="0 0 16 16" fill="none" aria-hidden="true">'
               '<path d="M4 12 12 4M5.5 4H12v6.5" stroke="currentColor" stroke-width="2" '
               'stroke-linecap="round" stroke-linejoin="round"/></svg></span>')

SQUIGGLE = ('<svg viewBox="0 0 60 26" fill="none" aria-hidden="true">'
            '<path d="M2 20c10 4 18-6 10-10-5-2-7 4-2 6 9 4 24 1 46-9" stroke="currentColor" '
            'stroke-width="2.4" stroke-linecap="round"/>'
            '<path d="M50 3l6 4-6 5" stroke="currentColor" stroke-width="2.4" '
            'stroke-linecap="round" stroke-linejoin="round"/></svg>')

CHEVRON = ('<svg viewBox="0 0 11 7" fill="none" aria-hidden="true">'
           '<path d="M1 1l4.5 4.5L10 1" stroke="currentColor" stroke-width="1.8" '
           'stroke-linecap="round" stroke-linejoin="round"/></svg>')

# ---------------------------------------------------------------- partials

def head(title_key, title_ro, desc_ro):
    return f"""<!doctype html>
<html lang="ro">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title data-i18n="{title_key}">{title_ro}</title>
<meta name="description" content="{desc_ro}">
<meta name="theme-color" content="#3F71FF">
<link rel="preconnect" href="https://cdn.prod.website-files.com" crossorigin>
<link rel="stylesheet" href="{stamp("assets/site.css")}">
<!--
  Acasara. Brand copy, phone, e-mail, address and company data are placeholders:
  search for "[" and "07XX". Translations live in assets/i18n.js (10 locales).
  Fonts are loaded from a third-party CDN for this mockup and are NOT licensed to us -
  see README.md before going live.
-->
</head>
<body>
<a class="skip" href="#top">Sari la conținut</a>

<div class="loader" id="loader" aria-hidden="true">
  <div class="loader-mark">
    <span class="wordmark">acasara<span class="tld">.ro</span></span>
  </div>
  <div class="loader-bar"><i></i></div>
</div>
"""


def navbar(active, solid=False):
    links = [("#miert",    "nav.why",     "De ce noi"),
             ("#cum",      "nav.how",     "Cum funcționează"),
             ("#cumparam", "nav.what",    "Ce cumpărăm"),
             ("#gyik",     "nav.faq",     "Întrebări")]
    out = []
    for href, key, ro in links:
        cur = ' aria-current="page"' if href == active else ""
        out.append(f'<a href="{href}" data-i18n="{key}"{cur}>{ro}</a>')
    cls = "navbar solid" if solid else "navbar"
    return f"""
<nav class="{cls}">
  <a class="brand" href="#top" aria-label="acasara.ro">
    <span class="wordmark">acasara<span class="tld">.ro</span></span>
  </a>
  <div class="nav-links">
    {chr(10) + "    ".join(out)}
  </div>
  <div class="nav-end">
    <div class="lang" data-open="false">
      <button class="lang-btn" type="button" aria-haspopup="true" aria-expanded="false" aria-label="Language">
        <span class="lang-cur">RO</span>{CHEVRON}
      </button>
      <div class="lang-menu" role="menu"></div>
    </div>
    <a class="btn" href="#cerere" aria-label="Cere oferta" data-i18n="nav.offer" data-i18n-attr="aria-label"><span data-i18n="nav.offer">Cere oferta</span>{ARROW}</a>
  </div>
</nav>
"""


CTA = f"""
<section class="cta rv">
  <h2 data-i18n="cta.h2">Vrei să vezi cât valorează?</h2>
  <a class="btn" href="#cerere"><span data-i18n="cta.btn">Cere oferta</span>{ARROW}</a>
</section>
"""

I18N_SRC = stamp("assets/i18n.js")
SITE_SRC = stamp("assets/site.js")

FOOTER = f"""
<footer class="footer">
  <div class="foot-cta">
    <h2 data-i18n="foot.ctaH">Gata să vinzi?</h2>
    <a class="btn btn-light" href="#cerere"><span data-i18n="cta.btn">Cere oferta</span>{ARROW}</a>
  </div>

  <div class="foot-grid">
    <nav class="foot-nav" aria-label="Subsol">
      <a href="#cum" data-i18n="nav.how">Cum funcționează</a>
      <a href="#cumparam" data-i18n="nav.what">Ce cumpărăm</a>
      <a href="#cash" data-i18n="cash.badge">Plată cash</a>
      <a href="#gyik" data-i18n="nav.faq">Întrebări</a>
    </nav>
    <div class="foot-col">
      <p class="micro" data-i18n="foot.contact">Contact</p>
      <a class="foot-big" href="tel:07XXXXXXXX">07XX XXX XXX</a>
      <a class="foot-big" href="mailto:[email]">[email]</a>
    </div>
    <div class="foot-col">
      <p class="micro" data-i18n="foot.follow">Urmărește-ne</p>
      <a href="#" rel="noopener">Instagram</a>
      <a href="#" rel="noopener">Facebook</a>
      <a href="#" rel="noopener">LinkedIn</a>
      <p class="micro" style="margin-top:1.6rem" data-i18n="foot.address">Adresă</p>
      <address>[Stradă și număr],<br>[Oraș], România</address>
    </div>
  </div>


  <div class="foot-map" aria-hidden="true">
    <svg viewBox="0 0 1000 640" preserveAspectRatio="xMidYMid meet" role="presentation">
      <defs>
        <linearGradient id="veinFade" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0%" stop-color="#A85362"/>
          <stop offset="100%" stop-color="#7B2D3B"/>
        </linearGradient>
      </defs>

      <path class="map-outline" d="M648.6 24.0 L616.7 34.2 L603.5 58.3 L519.1 71.1 L501.6 92.6 L488.1 92.8 L460.3 61.3 L429.3 70.7 L365.2 61.8 L334.5 43.3 L292.8 85.0 L260.9 87.4 L236.2 116.4 L235.5 133.3 L201.6 179.8 L204.1 189.7 L187.0 225.0 L172.7 232.2 L170.2 260.8 L159.6 274.3 L124.0 277.7 L111.6 296.9 L99.6 288.4 L78.6 298.7 L117.7 344.2 L128.0 341.6 L124.0 378.6 L189.7 418.8 L176.1 437.1 L193.2 453.6 L175.7 457.5 L179.7 468.5 L195.3 470.4 L200.3 483.0 L232.1 486.7 L243.4 507.1 L270.0 476.8 L297.2 493.0 L300.3 498.7 L273.1 506.6 L292.2 540.0 L325.3 559.3 L311.2 568.4 L311.0 589.1 L359.1 586.3 L425.1 608.0 L454.3 597.5 L475.6 607.9 L498.0 601.9 L531.4 616.0 L568.4 603.0 L600.7 569.0 L681.9 548.5 L710.8 565.9 L732.6 561.6 L740.9 573.5 L756.4 566.4 L763.7 587.7 L816.1 600.7 L828.3 553.3 L821.6 528.1 L863.2 471.8 L903.5 466.2 L912.4 424.1 L921.4 416.4 L890.5 383.6 L848.8 404.3 L835.9 397.2 L826.8 411.5 L795.4 399.3 L780.7 379.6 L772.1 362.3 L779.6 357.7 L771.9 309.9 L773.8 281.4 L787.1 258.2 L786.5 234.6 L772.7 188.2 L744.7 167.0 L740.1 147.6 L727.0 143.4 L726.3 126.0 L701.7 100.8 L679.3 40.7 L648.6 24.0 Z"/>

      <g class="veins">
        <path class="v1" d="M595.8 512.7 Q596 480 588.7 447.7"/>
        <path class="v1" d="M588.7 447.7 Q577 399 551.4 357.2"/>
        <path class="v1" d="M551.4 357.2 Q488 339 422.9 338.1"/>
        <path class="v1" d="M422.9 338.1 Q408 272 374.2 214.5"/>
        <path class="v1" d="M374.2 214.5 Q302 186 225.3 178.8"/>
        <path class="v1" d="M595.8 512.7 Q495 533 391.9 525.4"/>
        <path class="v1" d="M391.9 525.4 Q262 455 164.2 344.4"/>
        <path class="v1" d="M595.8 512.7 Q706 543 820.0 545.8"/>
        <path class="v1" d="M588.7 447.7 Q673 403 766.8 384.0"/>
        <path class="v1" d="M766.8 384.0 Q730 277 728.7 164.8"/>
        <path class="v1" d="M728.7 164.8 Q673 125 609.1 102.3"/>
        <path class="v3" d="M551.4 357.2 Q443 311 374.2 214.5"/>
        <path class="v3" d="M766.8 384.0 Q777 470 820.0 545.8"/>
        <path class="v3" d="M422.9 338.1 Q294 372 164.2 344.4"/>
        <path class="v3" d="M609.1 102.3 Q477 128 374.2 214.5"/>
        <path class="v3" d="M391.9 525.4 Q495 544 595.8 512.7"/>
        <path class="v3" d="M728.7 164.8 Q717 280 766.8 384.0"/>
        <path class="v3" d="M225.3 178.8 Q175 254 164.2 344.4"/>
        <path class="v3" d="M551.4 357.2 Q594 429 595.8 512.7"/>
      </g>

      <g class="nodes">
        <circle cx="595.8" cy="512.7" r="9"/>
        <circle cx="374.2" cy="214.5" r="6"/>
        <circle cx="164.2" cy="344.4" r="6"/>
        <circle cx="728.7" cy="164.8" r="6"/>
        <circle cx="820.0" cy="545.8" r="6"/>
        <circle cx="551.4" cy="357.2" r="6"/>
        <circle cx="391.9" cy="525.4" r="5"/>
        <circle cx="225.3" cy="178.8" r="5"/>
        <circle cx="766.8" cy="384.0" r="5"/>
        <circle cx="422.9" cy="338.1" r="5"/>
        <circle cx="609.1" cy="102.3" r="5"/>
        <circle cx="588.7" cy="447.7" r="5"/>
      </g>
    </svg>
  </div>

  <div class="foot-mark" aria-hidden="true">acasara<span class="tld">.ro</span></div>

  <div class="foot-bottom">
    <span>© <span id="year">2026</span> [Denumire SRL] — CUI [—]</span>
    <span><a href="#" data-i18n="foot.terms">Termeni și condiții</a> ·
          <a href="#" data-i18n="foot.privacy">Politica de confidențialitate</a></span>
  </div>
</footer>

<script src="{I18N_SRC}"></script>
<script src="{SITE_SRC}"></script>
</body>
</html>
"""

# ---------------------------------------------------------------- blocks

SCATTER_ITEMS = [
    ("balconies.jpg", "Bloc de apartamente cu balcoane",      "buy.l1", "Apartamente",        "lbl-r"),
    ("keys.jpg",      "Predarea cheilor unei locuințe",       "buy.l2", "Cheile",             "lbl-b"),
    ("block.jpg",     "Bloc rezidențial pe cer senin",        "buy.l3", "Garsoniere",         "lbl-l"),
    ("signing.jpg",   "Semnarea documentelor cu un consultant","buy.l4", "La notar",           "lbl-l"),
    ("boxes.jpg",     "Cuplu care cară cutii la mutare",      "buy.l5", "Mutare fără grabă",  "lbl-r"),
    ("for-sale.jpg",  "Semn de vânzare ținut în mână",        "buy.l6", "Vânzare rapidă",     "lbl-b"),
]

def scatter():
    figs = []
    for i, (img, alt, key, ro, side) in enumerate(SCATTER_ITEMS, start=1):
        figs.append(f"""      <figure class="sct sct-{i} rv">
        <img src="assets/img/{img}" alt="{alt}" loading="lazy">
        <figcaption class="sct-label {side}">{SQUIGGLE}<i data-i18n="{key}">{ro}</i></figcaption>
      </figure>""")
    return f"""
  <section class="scatter" id="cumparam">
    <div class="scatter-head rv">
      <h2 data-i18n="buy.h2">Cumpărăm exact ce ai tu de vândut</h2>
      <p data-i18n="buy.sub">Apartament, casă, garsonieră, moștenire sau un imobil pe care nu ai apucat să-l renovezi. Îl luăm în starea în care este.</p>
    </div>
    <div class="scatter-stage">
{chr(10).join(figs)}
    </div>
    <div class="scatter-cta rv">
      <a class="btn" href="#proces"><span data-i18n="buy.cta">Vezi ce cumpărăm</span>{ARROW}</a>
    </div>
  </section>
"""

STORIES = [
    ("signing.jpg", "Semnarea documentelor la notar",  "st.g1", "Drumul nostru", "st.t1", "Cum am ajuns să cumpărăm case fără comision"),
    ("packing.jpg", "Cuplu care împachetează la mutare","st.g2", "Oameni",        "st.t2", "Teoria celor 14 zile: discuție cu fondatorul"),
    ("for-sale.jpg","Anunț de vânzare în fața unei case","st.g3","Oameni",        "st.t3", "Ce m-a învățat o vânzare pe care am ratat-o"),
    ("agent-keys.jpg","Chei de locuință în mână",       "st.g4", "Piața",         "st.t4", "Prețul corect e greu. Uite cum îl calculăm"),
]

def story_cards():
    out = []
    for img, alt, gk, gro, tk, tro in STORIES:
        out.append(f"""      <article class="story rv">
        <div class="story-media">
          <img src="assets/img/{img}" alt="{alt}" loading="lazy">
          {STORY_ARROW}
        </div>
        <div class="story-meta">
          <span class="tag" data-i18n="{gk}">{gro}</span>
          <span class="read" data-i18n="st.read">6 min citire</span>
        </div>
        <h3 data-i18n="{tk}">{tro}</h3>
      </article>""")
    return chr(10).join(out)


# ---------------------------------------------------------------- enquiry wizard

def req(): return '<abbr class="req" title="obligatoriu">*</abbr>'

WIZARD = f"""
  <section class="wizard" id="cerere">
    <div class="wizard-head rv">
      <h2 data-i18n="f.heading">Spune-ne despre locuință</h2>
      <p data-i18n="f.lead">Patru pași scurți. Te sunăm înapoi în 24 de ore.</p>
    </div>

    <div class="wiz-split rv">
      <aside class="wiz-side">
        <h3 data-i18n="cash.h2">Cumpărăm cu banii noștri, nu cu creditul băncii</h3>
        <p data-i18n="hero.sub">Fără comision, fără renovări, fără zeci de vizionări. O ofertă scrisă în 48 de ore și cheile predate atunci când ești tu pregătit.</p>
        <figure class="wiz-key">
          <img src="assets/img/key.png" alt="" width="620" height="230" loading="lazy">
        </figure>
        <ul class="wiz-trust">
          <li>{CHECK}<span data-i18n="offer.p1">0 lei comision</span></li>
          <li>{CHECK}<span data-i18n="proc.b3">Banii intră prin transfer bancar în aceeași zi.</span></li>
          <li>{CHECK}<span data-i18n="offer.p3">Fără obligații</span></li>
        </ul>
      </aside>

    <form class="wiz-card" id="enquiry" novalidate>
      <ol class="wiz-steps" id="wizRail">
        <li><b>1</b><span data-i18n="f.s1">Cine ești</span></li>
        <li><b>2</b><span data-i18n="f.s2">Locuința</span></li>
        <li><b>3</b><span data-i18n="f.s3">Preț și anunț</span></li>
        <li><b>4</b><span data-i18n="f.s4">Date de contact</span></li>
      </ol>
      <div class="wiz-bar"><i id="wizBar"></i></div>
      <p class="wiz-count" id="wizCount">Pasul 1 din 4</p>


      <fieldset class="wiz-pane" data-pane="1">
        <legend data-i18n="f.s1">Cine ești</legend>
        <div class="field">
          <span class="field-label" data-i18n="f.role">Ești…</span>
          <div class="pills" role="radiogroup">
            <label class="pill"><input type="radio" name="role" value="private" checked>
              <span data-i18n="f.rolePrivate">Persoană fizică</span></label>
            <label class="pill"><input type="radio" name="role" value="agent">
              <span data-i18n="f.roleAgent">Agent imobiliar</span></label>
          </div>
        </div>
        <div class="field">
          <label for="ptype" data-i18n="offer.type">Tipul locuinței</label>
          <select class="select" id="ptype" name="ptype">
            <option value="apartament" data-i18n="offer.t1">Apartament</option>
            <option value="casa" data-i18n="offer.t2">Casă</option>
            <option value="garsoniera" data-i18n="offer.t3">Garsonieră</option>
            <option value="teren" data-i18n="offer.t4">Teren</option>
            <option value="altceva" data-i18n="offer.t5">Altceva</option>
          </select>
        </div>
      </fieldset>

      <fieldset class="wiz-pane is-hidden" data-pane="2">
        <legend data-i18n="f.s2">Locuința</legend>
        <div class="field">
          <label for="paddress"><span data-i18n="f.address">Adresa exactă a locuinței</span>{req()}</label>
          <input class="input" id="paddress" name="paddress" type="text" autocomplete="street-address">
        </div>
        <div class="row-2">
          <div class="field">
            <label for="psize" data-i18n="f.size">Suprafața (m²)</label>
            <input class="input" id="psize" name="psize" type="number" min="1" inputmode="numeric">
          </div>
          <div class="field">
            <label for="pplot" data-i18n="f.plot">Suprafața terenului (m², dacă există)</label>
            <input class="input" id="pplot" name="pplot" type="number" min="1" inputmode="numeric">
          </div>
        </div>
        <div class="field">
          <label for="pcond" data-i18n="f.condition">Starea locuinței</label>
          <select class="select" id="pcond" name="pcond">
            <option value="" data-i18n="f.selectPlease">Alege…</option>
            <option value="new" data-i18n="f.cond1">Nouă</option>
            <option value="renovated" data-i18n="f.cond2">Renovată</option>
            <option value="liveable" data-i18n="f.cond3">Locuibilă</option>
            <option value="torenovate" data-i18n="f.cond4">De renovat</option>
          </select>
        </div>
      </fieldset>

      <fieldset class="wiz-pane is-hidden" data-pane="3">
        <legend data-i18n="f.s3">Preț și anunț</legend>
        <div class="field">
          <label for="padv" data-i18n="f.advertised">Locuința este deja listată?</label>
          <select class="select" id="padv" name="padv">
            <option value="" data-i18n="f.selectPlease">Alege…</option>
            <option value="yes" data-i18n="f.advYes">Da</option>
            <option value="no" data-i18n="f.advNo">Nu</option>
          </select>
        </div>
        <div class="field">
          <label for="plisting" data-i18n="f.listing">Link către anunț (opțional)</label>
          <input class="input" id="plisting" name="plisting" type="url" placeholder="https://">
        </div>
        <div class="field">
          <label for="pprice" data-i18n="f.price">Ai o idee despre preț?</label>
          <input class="input" id="pprice" name="pprice" type="text"
                 data-i18n="f.pricePh" data-i18n-attr="placeholder" placeholder="ex. 95.000 EUR">
        </div>
      </fieldset>

      <fieldset class="wiz-pane is-hidden" data-pane="4">
        <legend data-i18n="f.s4">Date de contact</legend>
        <div class="row-2">
          <div class="field">
            <label for="plast"><span data-i18n="f.lastName">Nume</span>{req()}</label>
            <input class="input" id="plast" name="plast" type="text" autocomplete="family-name">
          </div>
          <div class="field">
            <label for="pfirst"><span data-i18n="f.firstName">Prenume</span>{req()}</label>
            <input class="input" id="pfirst" name="pfirst" type="text" autocomplete="given-name">
          </div>
        </div>
        <div class="row-2">
          <div class="field">
            <label for="pemail"><span data-i18n="f.email">Adresă de e-mail</span>{req()}</label>
            <input class="input" id="pemail" name="pemail" type="email" autocomplete="email">
          </div>
          <div class="field">
            <label for="pphone"><span data-i18n="f.phone">Telefon</span>{req()}</label>
            <input class="input" id="pphone" name="pphone" type="tel" autocomplete="tel">
          </div>
        </div>
        <div class="field">
          <label for="pmsg" data-i18n="f.message">Altceva important</label>
          <textarea class="input textarea" id="pmsg" name="pmsg" rows="4"
                    data-i18n="f.messagePh" data-i18n-attr="placeholder"
                    placeholder="Scrie-ne orice crezi că ne ajută să înțelegem situația ta."></textarea>
        </div>
        <label class="consent">
          <input type="checkbox" id="pconsent" name="pconsent">
          <span><span data-i18n="f.consent">Am citit și accept nota de confidențialitate.</span>{req()}</span>
        </label>
      </fieldset>

      <div class="wiz-nav">
        <button class="btn btn-quiet is-hidden" type="button" id="wizBack" data-i18n="f.back">Înapoi</button>
        <button class="btn" type="button" id="wizNext">
          <span data-i18n="f.next">Mai departe</span>{ARROW}</button>
        <button class="btn is-hidden" type="submit" id="wizSend">
          <span data-i18n="f.submit">Cere să fii sunat</span>{ARROW}</button>
      </div>

      <p class="wiz-note" data-i18n="f.required">Câmpurile marcate cu asterisc sunt obligatorii. Folosim datele doar pentru a răspunde solicitării tale.</p>
      <p class="form-msg" id="wizMsg" role="status" aria-live="polite"></p>
    </form>
    </div>
  </section>
"""

# ---------------------------------------------------------------- sections

def sec_how():
    ro = [("Ne spui adresa", "Online, la telefon sau pe WhatsApp, în câteva minute."),
          ("Te sunăm", "Clarificăm situația și verificăm extrasul de carte funciară."),
          ("O singură vizionare", "Durează 30–45 de minute, fără obligații."),
          ("Oferta scrisă", "Cu prețul, calculul și termenele, valabilă 30 de zile."),
          ("Semnare la notar", "Onorariul notarului și intabularea le plătim noi."),
          ("Predai cheile", "Rămâi în locuință până la 90 de zile, dacă ai nevoie.")]
    items = []
    for i, (sro, bro) in enumerate(ro, start=1):
        items.append(f"""        <li class="walk-step rv">
          <span class="walk-num">{i:02d}</span>
          <div class="walk-body">
            <h3 data-i18n="how.s{i}">{sro}</h3>
            <p data-i18n="how.b{i}">{bro}</p>
          </div>
        </li>""")
    return f"""
  <section class="walk" id="cum">
    <div class="walk-head rv">
      <p class="kicker" data-i18n="proc.kicker">Drumul vânzării</p>
      <h2 data-i18n="how.h1">De la primul mesaj la notar, în cel mult 14 zile</h2>
      <p class="walk-lead" data-i18n="how.lead">Știi dinainte fiecare pas. Decizi abia după ce ai oferta scrisă în mână.</p>
    </div>
    <ol class="walk-list">
{chr(10).join(items)}
    </ol>
  </section>
"""


def sec_what():
    ys = ["Apartamente și garsoniere în bloc", "Case și vile cu teren",
          "Imobile nerenovate sau cu chiriaș", "Moșteniri cu acte în regulă",
          "Imobile cu ipotecă de stins"]
    ns = ["Imobile fără carte funciară", "Construcții fără autorizație", "Imobile în litigiu"]
    yl = chr(10).join(f'        <li>{CHECK}<span data-i18n="what.y{i}">{t}</span></li>'
                      for i, t in enumerate(ys, start=1))
    nl = chr(10).join(f'        <li>{CROSS}<span data-i18n="what.n{i}">{t}</span></li>'
                      for i, t in enumerate(ns, start=1))
    return f"""
  <section class="section-what">
    <header class="pagehead rv">
      <h2 data-i18n="what.h1">Ce cumpărăm și ce nu</h2>
      <p data-i18n="what.lead">Suntem direcți: dacă nu se potrivește, îți spunem din prima, nu după trei săptămâni.</p>
    </header>
    <div class="twocol">
      <div class="panel panel-yes rv">
        <h3 data-i18n="what.yes">Cumpărăm</h3>
        <ul>
{yl}
        </ul>
      </div>
      <div class="panel panel-no rv">
        <h3 data-i18n="what.no">Nu cumpărăm</h3>
        <ul>
{nl}
        </ul>
      </div>
    </div>
  </section>
"""


def sec_cash():
    pts = chr(10).join(
        f'        <li>{CHECK}<span data-i18n="cash.p{i}">{ro}</span></li>'
        for i, ro in enumerate(["Fonduri proprii, verificabile",
                                "Fără credit, fără condiție suspensivă",
                                "Banii intră prin transfer în ziua semnării",
                                "Preluăm și imobilele cu ipotecă de stins"], start=1))
    return f"""
  <section class="cash" id="cash">
    <div class="cash-in">
      <p class="cash-badge rv" data-i18n="cash.badge">Plată cash</p>
      <h2 class="rv" data-i18n="cash.h2">Cumpărăm cu banii noștri, nu cu creditul băncii</h2>
      <p class="cash-lead rv" data-i18n="cash.lead">Nu depindem de aprobarea unei bănci, așa că nu există clauză suspensivă și nu există vânzare care pică în ultima zi.</p>
      <ul class="cash-points rv">
{pts}
      </ul>
      <div class="cash-foot rv">
        <a class="btn btn-light" href="#cerere"><span data-i18n="cta.btn">Cere oferta</span>{ARROW}</a>
        <p class="cash-note" data-i18n="cash.note">Plata se face prin transfer bancar, la notar. Nu lucrăm cu numerar fizic.</p>
      </div>
    </div>
  </section>
"""


def sec_contact():
    return f"""
  <section class="section-contact" id="contact">
    <header class="pagehead rv">
      <h2 data-i18n="contact.h1">Hai să vorbim</h2>
      <p data-i18n="contact.lead">Răspundem la telefon între 9 și 19, în fiecare zi lucrătoare.</p>
    </header>
    <div class="contact-grid">
      <div class="ccard rv">
        <p class="micro" data-i18n="contact.phoneL">Telefon</p>
        <a href="tel:07XXXXXXXX">07XX XXX XXX</a>
      </div>
      <div class="ccard rv">
        <p class="micro" data-i18n="contact.emailL">E-mail</p>
        <a href="mailto:[email]">[email]</a>
      </div>
      <div class="ccard rv">
        <p class="micro" data-i18n="contact.hoursL">Program</p>
        <address data-i18n="contact.hours">Luni–Vineri, 9:00–19:00</address>
      </div>
    </div>
  </section>
"""


# ---------------------------------------------------------------- azzupp-shaped sections

def sec_proof():
    items = ["Contact direct","Vanzare fara comision","Discretie totala","Data de mutare flexibila"]
    lis = chr(10).join(
        f'      <li><b>{i:02d}</b><span data-i18n="proof.p{i}">{t}</span></li>'
        for i,t in enumerate(items, start=1))
    return f"""
  <section class="proof">
    <ul class="proof-list">
{lis}
    </ul>
  </section>
"""


def sec_calc():
    types = [("brick","calc.t1","Apartament caramida"),("panel","calc.t2","Apartament panouri"),
             ("house","calc.t3","Casa"),("studio","calc.t4","Garsoniera")]
    pills = chr(10).join(
        f'            <label class="pill"><input type="radio" name="ctype" value="{v}"{" checked" if i==0 else ""}><span data-i18n="{k}">{ro}</span></label>'
        for i,(v,k,ro) in enumerate(types))
    conds = [("renovated","f.cond2","Renovata"),("liveable","f.cond3","Locuibila"),("torenovate","f.cond4","De renovat")]
    copts = chr(10).join(f'            <option value="{v}" data-i18n="{k}">{ro}</option>' for v,k,ro in conds)
    return f"""
  <section class="calc" id="calculator">
    <div class="calc-head rv">
      <p class="kicker" data-i18n="cash.badge">Plata cash</p>
      <h2 data-i18n="calc.h2">Calculator de oferta</h2>
      <p class="calc-lead" data-i18n="calc.lead">Patru date si vezi pe loc un interval orientativ.</p>
    </div>

    <form class="calc-card rv" id="calcForm" novalidate>
      <div class="calc-grid">
        <div class="field">
          <label for="ccity" data-i18n="calc.city">Oras</label>
          <input class="input" id="ccity" name="ccity" type="text" autocomplete="address-level2">
        </div>
        <div class="field">
          <label for="csize" data-i18n="calc.size">Suprafata (m2)</label>
          <input class="input" id="csize" name="csize" type="number" min="12" max="600" value="58" inputmode="numeric">
        </div>
        <div class="field">
          <label for="crooms" data-i18n="calc.rooms">Camere</label>
          <select class="select" id="crooms" name="crooms">
            <option value="1">1</option><option value="2" selected>2</option>
            <option value="3">3</option><option value="4">4</option><option value="5">5+</option>
          </select>
        </div>
        <div class="field">
          <label for="cyear" data-i18n="calc.year">Anul constructiei</label>
          <input class="input" id="cyear" name="cyear" type="number" min="1900" max="2026" value="1985" inputmode="numeric">
        </div>
        <div class="field">
          <label for="ccond" data-i18n="calc.cond">Starea</label>
          <select class="select" id="ccond" name="ccond">
            <option value="new" data-i18n="f.cond1">Noua</option>
{copts}
          </select>
        </div>
      </div>

      <div class="field">
        <span class="field-label" data-i18n="calc.type">Tipul imobilului</span>
        <div class="pills" role="radiogroup">
{pills}
        </div>
      </div>

      <div class="calc-foot">
        <button class="btn" type="submit"><span data-i18n="calc.go">Calculeaza</span>{ARROW}</button>
        <div class="calc-out" id="calcOut" aria-live="polite">
          <p class="calc-out-label" data-i18n="calc.res">Interval orientativ</p>
          <strong id="calcVal">-</strong>
        </div>
      </div>
      <p class="calc-note" data-i18n="calc.note">Estimare automata, nu o evaluare.</p>
    </form>
  </section>
"""


def sec_reasons():
    ro = ["Nu platesti comision de agentie","Nu renovezi si nu faci zeci de vizionari",
          "Stii pretul in 48 de ore, in scris","Banii intra in ziua semnarii la notar",
          "Te muti cand esti pregatit, pana la 90 de zile"]
    lis = chr(10).join(
        f'      <li class="reason rv"><span class="reason-n">{i:02d}</span><p data-i18n="reasons.r{i}">{t}</p></li>'
        for i,t in enumerate(ro, start=1))
    return f"""
  <section class="reasons" id="miert">
    <div class="reasons-head rv">
      <h2 data-i18n="reasons.h2">5 motive pentru care proprietarii aleg o oferta cash</h2>
    </div>
    <ul class="reasons-list">
{lis}
    </ul>
  </section>
"""


def sec_faq():
    qa = [("Cum functioneaza vanzarea directa?","Ne spui adresa, venim la o singura vizionare si primesti oferta scrisa in 48 de ore."),
          ("Trebuie sa platesc comision de agentie?","Nu. Cumparam direct de la tine."),
          ("Pot vinde un imobil care are nevoie de renovare?","Da. Cumparam in starea actuala."),
          ("Cat de repede primesc banii?","Semnam la notar in 7-14 zile, iar suma intra in aceeasi zi."),
          ("Trebuie sa ma mut imediat dupa vanzare?","Nu. Poti ramane pana la 90 de zile."),
          ("Sunt obligat sa accept oferta?","Nu. Oferta este valabila 30 de zile.")]
    items = chr(10).join(
        f'      <details class="faq-item rv"><summary><span data-i18n="faq.q{i}">{q}</span></summary><p data-i18n="faq.a{i}">{a}</p></details>'
        for i,(q,a) in enumerate(qa, start=1))
    return f"""
  <section class="faq" id="gyik">
    <div class="faq-head rv">
      <h2 data-i18n="faq.h2">Bine de stiut dinainte</h2>
    </div>
    <div class="faq-list">
{items}
    </div>
  </section>
"""


# ---------------------------------------------------------------- the page

def page_index():
    return head("meta.indexT", "Acasara — îți cumpărăm locuința direct",
                "Cumpărăm apartamente și case direct de la proprietari. Ofertă scrisă în 48 de ore, 0 lei comision.")     + navbar("#top") + f"""
<main id="top">

  <section class="hero">
    <div class="hero-media" id="heroMedia"
         data-clips="assets/video/hero-sanpetru.mp4,assets/video/r-14864002.mp4,assets/video/village.mp4,assets/video/r-14665250.mp4,assets/video/r-18070174.mp4,assets/video/city.mp4">
      <video class="hero-vid is-on" autoplay muted playsinline preload="auto"
             poster="assets/img/balconies.jpg" src="assets/video/hero-sanpetru.mp4"></video>
      <video class="hero-vid" muted playsinline preload="auto"></video>
    </div>
    <div class="hero-in">
      <div>
        <h1><span data-i18n="hero.t1">Vinde casa.</span><br><span data-i18n="hero.t2">Păstrează ritmul.</span></h1>
        <p data-i18n="hero.sub">Fără comision, fără renovări, fără zeci de vizionări. O ofertă scrisă în 48 de ore și cheile predate atunci când ești tu pregătit.</p>
      </div>
      <div class="hero-cta">
        <a class="btn" href="#cerere"><span data-i18n="hero.cta">Cere oferta</span>{PLAY}</a>
      </div>
    </div>
  </section>
{sec_proof()}
{sec_calc()}
{sec_reasons()}
{sec_how()}
{scatter()}
{sec_what()}
{sec_cash()}
{sec_faq()}
{WIZARD}
{CTA}
</main>
{FOOTER}"""


PAGES = {"index.html": page_index}

if __name__ == "__main__":
    import os
    for name, fn in PAGES.items():
        path = os.path.join(HERE, name)
        io.open(path, "w", encoding="utf-8", newline=chr(10)).write(fn())
        print("%-24s %6d bytes" % (name, os.path.getsize(path)))
