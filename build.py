# -*- coding: utf-8 -*-
"""Acasara - static page generator.

Emits index.html. Every Romanian default string is read from assets/i18n.js (the "ro" block, which is
imported from azzupp.com), so there is one source of copy. Re-run after editing:  python build.py
"""
import html, io, json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))


def stamp(rel):
    """Append a version query so browsers pick up edited CSS/JS instead of a cached copy."""
    try:
        return "%s?v=%d" % (rel, int(os.path.getmtime(os.path.join(HERE, rel))))
    except OSError:
        return rel


# ---------------------------------------------------------------- copy

def _load():
    src = io.open(os.path.join(HERE, "assets", "i18n.js"), encoding="utf-8").read()
    return json.loads(re.search(r"window\.T = (\{.*\});", src, re.S).group(1))["ro"]

T = _load()
FORM = json.load(io.open(os.path.join(HERE, "form-data.json"), encoding="utf-8"))


def tx(key):
    return html.escape(T[key], quote=False)


def el(tag, key, cls=None, attrs=""):
    c = ' class="%s"' % cls if cls else ""
    a = " " + attrs if attrs else ""
    return '<%s%s data-i18n="%s"%s>%s</%s>' % (tag, c, key, a, tx(key), tag)


def req():
    return '<abbr class="req" title="*">*</abbr>'


# Romania outline, shared by the footer and the enquiry panel
MAP_D = "M648.6 24.0 L616.7 34.2 L603.5 58.3 L519.1 71.1 L501.6 92.6 L488.1 92.8 L460.3 61.3 L429.3 70.7 L365.2 61.8 L334.5 43.3 L292.8 85.0 L260.9 87.4 L236.2 116.4 L235.5 133.3 L201.6 179.8 L204.1 189.7 L187.0 225.0 L172.7 232.2 L170.2 260.8 L159.6 274.3 L124.0 277.7 L111.6 296.9 L99.6 288.4 L78.6 298.7 L117.7 344.2 L128.0 341.6 L124.0 378.6 L189.7 418.8 L176.1 437.1 L193.2 453.6 L175.7 457.5 L179.7 468.5 L195.3 470.4 L200.3 483.0 L232.1 486.7 L243.4 507.1 L270.0 476.8 L297.2 493.0 L300.3 498.7 L273.1 506.6 L292.2 540.0 L325.3 559.3 L311.2 568.4 L311.0 589.1 L359.1 586.3 L425.1 608.0 L454.3 597.5 L475.6 607.9 L498.0 601.9 L531.4 616.0 L568.4 603.0 L600.7 569.0 L681.9 548.5 L710.8 565.9 L732.6 561.6 L740.9 573.5 L756.4 566.4 L763.7 587.7 L816.1 600.7 L828.3 553.3 L821.6 528.1 L863.2 471.8 L903.5 466.2 L912.4 424.1 L921.4 416.4 L890.5 383.6 L848.8 404.3 L835.9 397.2 L826.8 411.5 L795.4 399.3 L780.7 379.6 L772.1 362.3 L779.6 357.7 L771.9 309.9 L773.8 281.4 L787.1 258.2 L786.5 234.6 L772.7 188.2 L744.7 167.0 L740.1 147.6 L727.0 143.4 L726.3 126.0 L701.7 100.8 L679.3 40.7 L648.6 24.0 Z"

# ---------------------------------------------------------------- icons

ARROW = ('<span class="btn-circle"><svg viewBox="0 0 17 14" fill="none" aria-hidden="true">'
         '<path d="M1 7h13M9.6 1.4 15.5 7l-5.9 5.6" stroke="currentColor" stroke-width="2" '
         'stroke-linecap="round" stroke-linejoin="round"/></svg></span>')

DOWN = ('<span class="btn-circle"><svg viewBox="0 0 14 17" fill="none" aria-hidden="true">'
        '<path d="M7 1v13M1.4 9.6 7 15.5l5.6-5.9" stroke="currentColor" stroke-width="2" '
        'stroke-linecap="round" stroke-linejoin="round"/></svg></span>')

CHECK = ('<svg viewBox="0 0 22 22" fill="none" aria-hidden="true">'
         '<path d="M4 11.5 9 16.5 18 6" stroke="currentColor" stroke-width="2.6" '
         'stroke-linecap="round" stroke-linejoin="round"/></svg>')

CHEVRON = ('<svg viewBox="0 0 11 7" fill="none" aria-hidden="true">'
           '<path d="M1 1l4.5 4.5L10 1" stroke="currentColor" stroke-width="1.8" '
           'stroke-linecap="round" stroke-linejoin="round"/></svg>')

# ---------------------------------------------------------------- partials

LOADER = """<div class="loader" id="loader" aria-hidden="true">
  <div class="loader-mark">
    <span class="wordmark">acasara<span class="tld">.ro</span></span>
  </div>
  <div class="loader-bar"><i></i></div>
</div>
"""


def head(title_key="meta.title", loader=True):
    return f"""<!doctype html>
<html lang="ro">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title data-i18n="{title_key}">{tx(title_key)}</title>
<meta name="description" content="{html.escape(T["meta.desc"])}">
<meta name="theme-color" content="#3F71FF">
<link rel="preload" href="assets/fonts/onest-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{stamp("assets/site.css")}">
<!--
  Acasara. All copy is imported from azzupp.com (assets/i18n.js, 11 locales) with the brand name
  swapped. Phone, e-mail, company data and the form / estimate endpoints are still open: search for
  "[", "07XX" and "TODO". Nothing is loaded from a third party: fonts (Onest, SIL OFL), images,
  video and scripts are all in assets/. See README.md.
-->
</head>
<body>
<a class="skip" href="#top">Sari la conținut</a>

{LOADER if loader else ""}"""


def navbar(cur=None):
    links = [("miert.html", "nav.why"), ("folyamat.html", "nav.process"), ("ingatlanok.html", "nav.kinds"), ("gyik.html", "nav.faq")]
    items = (chr(10) + "    ").join(
        '<a href="%s" data-i18n="%s"%s>%s</a>' % (h, k, ' aria-current="page"' if h == cur else "", tx(k)) for h, k in links)
    home = cur is None
    cls = "navbar is-away" if home else "navbar solid"
    static = "" if home else " data-static"
    return f"""
<nav class="{cls}"{static}>
  <a class="brand" href="{'#top' if home else 'index.html'}" aria-label="acasara.ro">
    <span class="wordmark">acasara<span class="tld">.ro</span></span>
  </a>
  <div class="nav-links" id="navLinks">
    {items}
  </div>
  <div class="nav-end">
    <div class="lang" data-open="false">
      <button class="lang-btn" type="button" aria-haspopup="true" aria-expanded="false" aria-label="Language">
        <span class="lang-cur">RO</span>{CHEVRON}
      </button>
      <div class="lang-menu" role="menu"></div>
    </div>
    <a class="btn" href="kezdjuk-el.html" aria-label="{html.escape(T["proc.cta"])}" data-i18n="proc.cta" data-i18n-attr="aria-label"><span data-i18n="proc.cta">{tx("proc.cta")}</span>{ARROW}</a>
    <button class="nav-burger" type="button" aria-label="Menu" aria-expanded="false" aria-controls="navLinks"><i></i><i></i></button>
  </div>
</nav>
"""


I18N_SRC = stamp("assets/i18n.js")
SITE_SRC = stamp("assets/site.js")

FOOTER = f"""
<footer class="footer">
  <div class="foot-card">
    <div class="foot-map foot-card-map" aria-hidden="true">
      <svg viewBox="0 0 1000 640" preserveAspectRatio="xMidYMid meet" role="presentation"><path class="map-outline" d="{MAP_D}"/></svg>
    </div>
    <div class="foot-card-txt">
      {el("h2", "lead.eyebrow")}
      <a class="btn btn-light" href="kezdjuk-el.html"><span data-i18n="proc.cta">{tx("proc.cta")}</span>{ARROW}</a>
    </div>
    <div class="foot-card-ct">
      {el("p", "nav.contact", "micro")}
      <a class="foot-big" href="tel:07XXXXXXXX">07XX XXX XXX</a>
      <a class="foot-big" href="mailto:[email]">[email]</a>
    </div>
  </div>

  <div class="foot-body">
    {el("p", "foot.desc", "foot-desc")}
    <nav class="foot-nav" aria-label="Footer">
      {el("a", "nav.why", None, 'href="miert.html"')}
      {el("a", "nav.process", None, 'href="folyamat.html"')}
      {el("a", "nav.kinds", None, 'href="ingatlanok.html"')}
      {el("a", "nav.faq", None, 'href="gyik.html"')}
      {el("a", "nav.contact", None, 'href="#kapcsolat"')}
    </nav>
  </div>

  <div class="foot-mark" aria-hidden="true">acasara<span class="tld">.ro</span></div>

  <div class="foot-bottom">
    <span>© <span id="year">2026</span> acasara.ro. <span data-i18n="foot.rights">{tx("foot.rights")}</span></span>
    {el("span", "foot.cond")}
  </div>
</footer>

<script src="{I18N_SRC}"></script>
<script src="{SITE_SRC}"></script>
</body>
</html>
"""

# ---------------------------------------------------------------- form helpers

def label(key, for_id=None, required=False, cls=None):
    f = ' for="%s"' % for_id if for_id else ""
    c = ' class="%s"' % cls if cls else ""
    return '<label%s%s><span data-i18n="%s">%s</span>%s</label>' % (f, c, key, tx(key), req() if required else "")


# property types as selectable tiles (same values and i18n keys as the old dropdown)
TYPE_ICON = [
    '<rect x="5" y="3" width="14" height="18" rx="1.5"/><path d="M9 7h.01M12 7h.01M15 7h.01M9 11h.01M12 11h.01M15 11h.01M10 21v-4h4v4"/>',
    '<path d="M3.5 11 12 4l8.5 7M6 9.5V20h12V9.5"/><path d="M10 20v-5h4v5"/>',
    '<path d="M2.5 12 7 8l4.5 4V20h-9z"/><path d="M12.5 12 17 8l4.5 4V20h-9z"/>',
    '<path d="M2 20v-8l3.3-3 3.3 3v8M8.6 20v-8l3.3-3 3.3 3v8M15.2 20v-8l3.3-3 3.3 3v8M2 20h19.8"/>',
    '<path d="M4 17l4-9h8l4 9z"/><path d="M12 8v9M6.5 12.5h11"/>',
    '<path d="M4 9l1.5-5h13L20 9"/><path d="M4 9a2.7 2.7 0 0 0 5.3 0 2.7 2.7 0 0 0 5.4 0 2.7 2.7 0 0 0 5.3 0"/><path d="M5 11.5V20h14v-8.5M10 20v-5h4v5"/>',
    '<rect x="3" y="7" width="18" height="13" rx="2"/><path d="M9 7V5a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v2M3 13h18"/>',
    '<path d="M3 20V9l9-5 9 5v11"/><path d="M7 20v-6h10v6M7 17h10M12 14v6"/>',
    '<circle cx="6" cy="12" r="1.5"/><circle cx="12" cy="12" r="1.5"/><circle cx="18" cy="12" r="1.5"/>',
]


def type_tiles(values):
    out = []
    for i, v in enumerate(values):
        icon = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" '
                'stroke-linejoin="round" aria-hidden="true">%s</svg>' % TYPE_ICON[i])
        out.append('            <label class="type"><input type="radio" name="ingatlan_tipusa" value="%s">'
                   '<span class="tb"><i>%s</i><b data-i18n="lead.o.ingatlan_tipusa.%d">%s</b></span></label>'
                   % (html.escape(v), icon, i, tx("lead.o.ingatlan_tipusa.%d" % i)))
    return chr(10).join(out)


def pill_field(label_key, name, values, prefix, small=False):
    cls = "pills pills-s" if small else "pills"
    return f"""        <div class="field">
          {el("span", label_key, "field-label")}
          <div class="{cls}" role="radiogroup" data-clearable>
{pills("radio", name, values, prefix)}
          </div>
        </div>"""


def pills(kind, name, values, prefix):
    return chr(10).join(
        '            <label class="pill"><input type="%s" name="%s" value="%s"><span data-i18n="%s.%d">%s</span></label>'
        % (kind, name, html.escape(v), prefix, i, tx("%s.%d" % (prefix, i))) for i, v in enumerate(values))


# ---------------------------------------------------------------- hero, proof

def sec_hero():
    return f"""
  <section class="hero">
    <div class="hero-media" id="heroMedia"
         data-clips="assets/video/hero-sanpetru.mp4,assets/video/r-14864002.mp4,assets/video/village.mp4,assets/video/r-14665250.mp4,assets/video/r-18070174.mp4,assets/video/city.mp4">
      <video class="hero-vid is-on" autoplay muted playsinline preload="auto"
             poster="assets/img/hero-poster.jpg" src="assets/video/hero-sanpetru.mp4"></video>
      <video class="hero-vid" muted playsinline preload="auto"></video>
    </div>
    <div class="hero-in">
      <div class="hero-copy">
        <h1>{el("span", "hero.h1a")} {el("em", "hero.h1b")}</h1>
        <div class="hero-actions">
          <a class="btn" href="#kalkulator-section"><span data-i18n="hero.btnCalc">{tx("hero.btnCalc")}</span>{ARROW}</a>
          <a class="btn btn-ghost" href="#kapcsolat"><span data-i18n="hero.btnOffer">{tx("hero.btnOffer")}</span>{DOWN}</a>
        </div>
        <ul class="hero-assure">
          <li>{CHECK}{el("span", "hero.a1")}</li>
          <li>{CHECK}{el("span", "hero.a2")}</li>
          <li>{CHECK}{el("span", "hero.a3")}</li>
        </ul>
      </div>
    </div>
  </section>
"""


# outline icons for the proof strip: direct contact, no commission, discreet, flexible move-out
PROOF_ICON = [
    '<path d="M4 5.5h16v10H10l-4 3.5v-3.5H4z"/><path d="M8.5 10.5h.01M12 10.5h.01M15.5 10.5h.01"/>',
    '<circle cx="12" cy="12" r="9"/><path d="M15.5 8.5l-7 7"/><path d="M9 9h.01M15 15h.01"/>',
    '<path d="M12 3l7 3v5.5c0 4.4-2.9 7.9-7 9.5-4.1-1.6-7-5.1-7-9.5V6z"/><rect x="9" y="11" width="6" height="5" rx="1"/><path d="M10.2 11V9.8a1.8 1.8 0 0 1 3.6 0V11"/>',
    '<circle cx="8" cy="15" r="3.5"/><path d="M10.5 12.5L20 3M16.5 6.5l3 3M13.5 9.5l2 2"/>',
]


def proof_icon(i):
    return ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" '
            'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">%s</svg>' % PROOF_ICON[i - 1])


def sec_proof():
    lis = chr(10).join('      <li><i class="proof-ico">%s</i><b>%02d</b>%s</li>' % (proof_icon(i), i, el("span", "proof.%d" % i)) for i in range(1, 5))
    return f"""
  <section class="proof">
    <ul class="proof-list">
{lis}
    </ul>
  </section>
"""


# ---------------------------------------------------------------- calculator (fields of azzupp.com's calculator)

# outline icons for the calculator (24x24, currentColor)
def svg_ico(paths, sw="1.7"):
    return ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="%s" '
            'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">%s</svg>' % (sw, paths))


KNOW_ICON = [
    '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    '<path d="M13 3L5 13.5h6L10 21l8-10.5h-6z"/>',
    '<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2z"/>',
    '<rect x="4" y="9" width="16" height="11" rx="1.5"/><path d="M12 9v11M3 9h18M12 9C9 9 8 4.5 10.5 4.5S12 9 12 9zM12 9c3 0 4-4.5 1.5-4.5S12 9 12 9z"/>',
    '<rect x="5" y="11" width="14" height="9" rx="2"/><path d="M8 11V8a4 4 0 0 1 8 0v3"/>',
]

# one icon per calculator step: location, property, size, condition, extras, contact, cash offer
STEP7_ICON = [
    '<path d="M12 21s7-6.2 7-11.5A7 7 0 0 0 5 9.5C5 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/>',
    '<path d="M3.5 11 12 4l8.5 7M6 9.5V20h12V9.5"/><path d="M10 20v-5h4v5"/>',
    '<path d="M4 9V4h5M20 15v5h-5M4 4l6 6M20 20l-6-6"/>',
    '<path d="M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8z"/><path d="M18.5 16.5l.7 1.8 1.8.7-1.8.7-.7 1.8-.7-1.8-1.8-.7 1.8-.7z"/>',
    '<rect x="4" y="4" width="16" height="16" rx="4"/><path d="M12 8v8M8 12h8"/>',
    '<circle cx="12" cy="8" r="3.5"/><path d="M5 20c0-3.9 3.1-6.5 7-6.5s7 2.6 7 6.5"/>',
    '<rect x="3" y="7" width="18" height="10" rx="2"/><circle cx="12" cy="12" r="2.5"/><path d="M6.5 12h.01M17.5 12h.01"/>',
]

# icons that sit inside the form inputs
INPUT_ICON = {
    "city": '<path d="M4 20V8l6-3v15M10 20V10l6 2v8M3 20h18"/><path d="M7 11h.01M7 14h.01M13 14h.01M13 17h.01"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3.5 7l8.5 6 8.5-6"/>',
    "street": '<path d="M6 21V4M6 5h12l-2.5 3.5L18 12H6"/>',
    "person": STEP7_ICON[5],
    "phone": KNOW_ICON[2],
}


def ii(name):
    """opens an input wrapper with its icon; close it with </div>"""
    return '<div class="ico-in">%s' % svg_ico(INPUT_ICON[name], "1.8")


def cb_head(n, with_note=True):
    note = el("span", "calc.b%dn" % n, "cb-note") if with_note else ""
    return ('<div class="cb-h"><i class="cb-ico">%s</i><div class="cb-txt"><span class="cb-num">%02d</span>%s%s</div></div>'
            % (svg_ico(STEP7_ICON[n - 1]), n, el("span", "calc.b%dt" % n, "cb-title"), note))


def sec_calc():
    c = FORM["calc"]
    rail = (chr(10) + "        ").join('<li><b>%s</b>%s</li>' % (svg_ico(STEP7_ICON[i - 1]), el("span", "calc.b%dt" % i)) for i in range(1, 8))
    know = chr(10).join('        <li><i class="know-ico">%s</i>%s</li>' % (svg_ico(KNOW_ICON[i - 1]), el("span", "calc.know%d" % i)) for i in range(1, 6))
    return f"""
  <section class="calc" id="kalkulator-section">
    <div class="calc-head rv">
      {el("p", "calc.eyebrow", "kicker")}
      <h2><em data-i18n="calc.h1a">{tx("calc.h1a")}</em> <span data-i18n="calc.h1b">{tx("calc.h1b")}</span></h2>
      {el("p", "calc.lead", "calc-lead")}
    </div>

    <div class="calc-know rv">
      {el("h3", "calc.knowH")}
      <ul>
{know}
      </ul>
    </div>

    <form class="calc-card rv" id="calcForm" novalidate>
      <ol class="calc-rail" id="calcRail">
        {rail}
      </ol>
      <div class="wiz-bar"><i id="calcBar"></i></div>
      <p class="wiz-count" id="calcCount">1 / 7</p>

      <div class="cb calc-pane">
        {cb_head(1)}
        <input type="hidden" name="orszag" value="Románia">
        <div class="field">{label("calc.l.varos", "c_varos", True)}
            {ii("city")}<input class="input" id="c_varos" name="varos" type="text" required autocomplete="address-level2"></div></div>
        <div class="row-2">
          <div class="field">{label("calc.l.iranyitoszam", "c_iranyitoszam")}
            {ii("mail")}<input class="input" id="c_iranyitoszam" name="iranyitoszam" type="text" autocomplete="postal-code"></div></div>
          <div class="field">{label("calc.l.utca", "c_utca")}
            {ii("street")}<input class="input" id="c_utca" name="utca" type="text" autocomplete="address-line1"></div></div>
        </div>
      </div>

      <div class="cb calc-pane is-hidden">
        {cb_head(2, False)}
        <div class="pills" role="radiogroup">
{pills("radio", "tipus", c["tipus"], "calc.o.tipus")}
        </div>
      </div>

      <div class="cb calc-pane is-hidden">
        {cb_head(3, False)}
        <div class="field">
          <div class="range-head"><span class="field-label" data-i18n="calc.l.alapterulet">{tx("calc.l.alapterulet")}</span><b class="range-val" id="areaVal">65 m²</b></div>
          <input class="range" id="areaRange" name="alapterulet" type="range" min="15" max="400" value="65">
          <div class="range-ticks"><span>15</span><span>100</span><span>200</span><span>300</span><span>400 m²</span></div>
        </div>
{pill_field("calc.l.szobak", "szobak", c["szobak"], "calc.o.szobak", True)}
{pill_field("calc.l.emelet", "emelet", c["emelet"], "calc.o.emelet", True)}
        <div class="field field-narrow">{label("calc.l.epites_eve", "c_epites")}
            <input class="input" id="c_epites" name="epites_eve" type="number" min="1850" max="2026" inputmode="numeric"></div>
      </div>

      <div class="cb calc-pane is-hidden">
        {cb_head(4, False)}
        <div class="field">
          <span class="field-label" data-i18n="calc.l.allapot">{tx("calc.l.allapot")}</span>
          <div class="pills" role="radiogroup">
{pills("radio", "allapot", c["allapot"], "calc.o.allapot")}
          </div>
        </div>
{pill_field("calc.l.kilatas", "kilatas", c["kilatas"], "calc.o.kilatas")}
{pill_field("calc.l.komfort", "komfort", c["komfort"], "calc.o.komfort")}
      </div>

      <div class="cb calc-pane is-hidden">
        {cb_head(5)}
        <div class="pills">
{pills("checkbox", "extra[]", c["extra"], "calc.o.extra")}
        </div>
      </div>

      <div class="cb calc-pane is-hidden">
        {cb_head(6)}
        <div class="row-3">
          <div class="field">{label("calc.l.nev", "c_nev", True)}
            {ii("person")}<input class="input" id="c_nev" name="nev" type="text" required autocomplete="name"></div></div>
          <div class="field">{label("calc.l.phone", "c_phone", True)}
            {ii("phone")}<input class="input" id="c_phone" name="phone" type="tel" required autocomplete="tel"></div></div>
          <div class="field">{label("calc.l.email", "c_email", True)}
            {ii("mail")}<input class="input" id="c_email" name="email" type="email" required autocomplete="email"></div></div>
        </div>
        <label class="consent"><input type="checkbox" name="gdpr" required>
          <span><span data-i18n="calc.gdpr">{tx("calc.gdpr")}</span>{req()}</span></label>
      </div>

      <div class="cb calc-pane is-hidden" id="cashBlock">
        {cb_head(7)}
        <div class="cash-box">
          {el("span", "calc.cash.badge", "cash-tag")}
          {el("p", "calc.cash.question", "cash-q")}
          <div class="cash-btns">
            <button class="btn btn-quiet" type="button" id="cashYes" aria-pressed="false" data-i18n="calc.cash.yes">{tx("calc.cash.yes")}</button>
            <button class="btn btn-quiet" type="button" id="cashNo" aria-pressed="false" data-i18n="calc.cash.no">{tx("calc.cash.no")}</button>
          </div>
          <div class="cash-body is-hidden" id="cashBody">
            {el("p", "calc.cash.phone_help", "cash-help")}
            <div class="field">{label("calc.cash.phone_label", "c_cashphone")}
              <input class="input" id="c_cashphone" name="telefon" type="tel" autocomplete="tel" disabled></div>
          </div>
        </div>
        <input type="hidden" name="cash_offer" id="cashChoice" value="">
      </div>

      <div class="wiz-nav">
        <button class="btn btn-quiet is-hidden" type="button" id="calcBack" aria-label="Back">&larr;</button>
        <button class="btn" type="button" id="calcNext" aria-label="Next">&rarr;</button>
        <button class="btn is-hidden" type="submit" id="calcSend"><span id="calcSubmitLabel" data-i18n="calc.submit">{tx("calc.submit")}</span>{ARROW}</button>
      </div>
      <p class="form-msg" id="calcMsg" role="status" aria-live="polite"></p>
    </form>
  </section>
"""


# ---------------------------------------------------------------- five reasons, three steps, what we buy, band, FAQ

def sec_why():
    imgs = ["keys-home.jpg", "signing-desk.jpg", "house-old.jpg", "boxes-room.jpg", "fog-village.jpg"]
    cards = chr(10).join(f"""        <article class="why-p">
          <img src="assets/img/{imgs[i - 1]}" alt="" loading="lazy">
          <span class="why-n">{i:02d}</span>
          <div class="why-in">{el("h3", "why.%dt" % i)}{el("p", "why.%dp" % i)}</div>
        </article>""" for i in range(1, 6))
    return f"""
  <section class="why" id="miert">
    <div class="why-pin">
      <div class="why-head">
        <div>
          {el("p", "why.eyebrow", "kicker")}
          {el("h2", "why.h2")}
        </div>
        {el("p", "why.lead", "why-lead")}
      </div>
      <div class="why-track">
{cards}
        <article class="why-p why-end">{el("p", "why.note")}</article>
      </div>
      <div class="why-bar"><i></i></div>
    </div>
  </section>
"""


def sec_process():
    imgs = ["phone-morning.jpg", "city-street.jpg", "signing.jpg"]
    cols = chr(10).join(f"""        <li class="how-col" style="--d:{(i - 1) * 0.18:.2f}s">
          <div class="how-num"><span>{i:02d}</span></div>
          <div class="how-photo"><img src="assets/img/{imgs[i - 1]}" alt="" loading="lazy"></div>
          {el("span", "proc.%dn" % i, "how-n")}
          {el("h3", "proc.%dt" % i)}
          {el("p", "proc.%dp" % i)}
        </li>""" for i in range(1, 4))
    return f"""
  <section class="walk" id="folyamat">
    <div class="walk-head">
      {el("p", "proc.eyebrow", "kicker")}
      {el("h2", "proc.h2")}
      {el("p", "proc.lead", "walk-lead")}
    </div>
    <ol class="how-cols">
{cols}
    </ol>
    <div class="how-foot">
      <a class="btn btn-ink" href="kezdjuk-el.html"><span data-i18n="proc.cta">{tx("proc.cta")}</span>{ARROW}</a>
    </div>
  </section>
"""


def sec_kinds():
    pts = chr(10).join(f"""        <li style="--i:{i - 1}">{CHECK}<span>{el("strong", "kinds.%dt" % i)} {el("span", "kinds.%dp" % i)}</span></li>"""
                       for i in range(1, 7))
    return f"""
  <section class="cash" id="ingatlanok">
    <div class="cash-in">
      <div class="cash-top">
        <div>
          {el("p", "kinds.eyebrow", "cash-badge rv")}
          {el("h2", "kinds.h2", "rv")}
          {el("p", "kinds.lead", "cash-lead rv")}
        </div>
        <figure class="band-photo rv"><img src="assets/img/house-rain.jpg" alt="" width="1500" height="844" loading="lazy"></figure>
      </div>
      <ul class="cash-points band-points rv">
{pts}
      </ul>
    </div>
  </section>
"""


def sec_faq():
    items = chr(10).join(
        f'      <details class="faq-item rv"><summary>{el("span", "faq.q%d" % i)}</summary>{el("p", "faq.a%d" % i)}</details>'
        for i in range(1, 7))
    return f"""
  <section class="faq" id="gyik">
    <div class="faq-in">
      <div class="faq-head rv">
        {el("p", "faq.eyebrow", "kicker")}
        {el("h2", "faq.h2")}
        {el("p", "faq.lead", "faq-lead")}
        <a class="btn btn-ink" href="#kapcsolat"><span data-i18n="faq.cta">{tx("faq.cta")}</span>{ARROW}</a>
      </div>
      <div class="faq-list">
{items}
      </div>
    </div>
  </section>
"""


# ---------------------------------------------------------------- lead form (fields of azzupp.com's contact form)

def sec_lead():
    l = FORM["lead"]
    return f"""
  <section class="wizard" id="kapcsolat">
    <div class="wiz-split rv">
      <aside class="wiz-side">
        {el("p", "lead.eyebrow", "kicker kicker-light")}
        {el("h3", "lead.h2")}
        {el("p", "lead.lead", "wiz-lead")}
        <figure class="wiz-map" aria-hidden="true">
          <svg viewBox="0 0 1000 640" preserveAspectRatio="xMidYMid meet" role="presentation">
            <defs>
              <pattern id="roDots" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="11" cy="11" r="3.1" fill="#F6CDD3"/></pattern>
              <clipPath id="roClip"><path d="{MAP_D}"/></clipPath>
              <mask id="roMask" maskUnits="userSpaceOnUse" x="0" y="0" width="1000" height="640"><circle class="wm-reveal" cx="500" cy="320" r="0" fill="#fff"/></mask>
            </defs>
            <g clip-path="url(#roClip)">
              <rect width="1000" height="640" fill="url(#roDots)" mask="url(#roMask)" opacity=".6"/>
              <circle class="wm-ring" cx="500" cy="320" r="14"/>
              <circle class="wm-ring wm-ring2" cx="500" cy="320" r="14"/>
            </g>
            <path class="map-outline" d="{MAP_D}"/>
            <circle class="wm-pen" r="6" cx="0" cy="0"/>
          </svg>
        </figure>
        <ul class="wiz-trust">
          <li>{CHECK}{el("span", "hero.a1")}</li>
          <li>{CHECK}{el("span", "hero.a2")}</li>
          <li>{CHECK}{el("span", "hero.a3")}</li>
        </ul>
        {el("p", "lead.note", "wiz-side-note")}
      </aside>

    <form class="wiz-card" id="enquiry" novalidate>
      <ol class="wiz-steps" id="wizRail">
        <li><b>1</b></li><li><b>2</b></li><li><b>3</b></li><li><b>4</b></li>
      </ol>
      <div class="wiz-bar"><i id="wizBar"></i></div>
      <p class="wiz-count" id="wizCount">1 / 4</p>

      <fieldset class="wiz-pane" data-pane="1">
        <div class="field">
          <div class="pills" role="radiogroup">
            <label class="pill"><input type="radio" name="kapcsolat_tipusa" value="{l["kapcsolat_tipusa"][1]}" checked>
              <span data-i18n="lead.role2">{tx("lead.role2")}</span></label>
            <label class="pill"><input type="radio" name="kapcsolat_tipusa" value="{l["kapcsolat_tipusa"][0]}">
              <span data-i18n="lead.role1">{tx("lead.role1")}</span></label>
          </div>
        </div>
        <div class="field">
          {el("span", "lead.l.ingatlan_tipusa", "field-label")}
          <div class="types" role="radiogroup">
{type_tiles(l["ingatlan_tipusa"])}
          </div>
        </div>
      </fieldset>

      <fieldset class="wiz-pane is-hidden" data-pane="2">
        <div class="field">
          {label("lead.l.ingatlan_pontos_cime", "l_cim", True)}
          <input class="input" id="l_cim" name="ingatlan_pontos_cime" type="text" autocomplete="street-address">
        </div>
        <div class="row-2">
          <div class="field">
            {label("lead.l.ingatlan_merete", "l_meret")}
            <input class="input" id="l_meret" name="ingatlan_merete" type="number" min="0" inputmode="numeric">
          </div>
          <div class="field">
            {label("lead.l.telekmeret", "l_telek")}
            <input class="input" id="l_telek" name="telekmeret" type="number" min="0" inputmode="numeric">
          </div>
        </div>
{pill_field("lead.l.ingatlan_allapota", "ingatlan_allapota", l["ingatlan_allapota"], "lead.o.ingatlan_allapota")}
      </fieldset>

      <fieldset class="wiz-pane is-hidden" data-pane="3">
{pill_field("lead.l.hirdetve_van", "hirdetve_van", l["hirdetve_van"], "lead.o.hirdetve_van")}
        <div class="field">
          {label("lead.l.hirdetes_linkje", "l_link")}
          <input class="input" id="l_link" name="hirdetes_linkje" type="url" placeholder="https://">
        </div>
        <div class="field">
          {label("lead.l.piaci_ar_elkepzeles", "l_ar")}
          <input class="input" id="l_ar" name="piaci_ar_elkepzeles" type="text">
        </div>
      </fieldset>

      <fieldset class="wiz-pane is-hidden" data-pane="4">
        <div class="row-2">
          <div class="field">
            {label("lead.l.vezeteknev", "l_vnev", True)}
            <input class="input" id="l_vnev" name="vezeteknev" type="text" autocomplete="family-name">
          </div>
          <div class="field">
            {label("lead.l.keresztnev", "l_knev", True)}
            <input class="input" id="l_knev" name="keresztnev" type="text" autocomplete="given-name">
          </div>
        </div>
        <div class="row-2">
          <div class="field">
            {label("lead.l.email", "l_email", True)}
            <input class="input" id="l_email" name="email" type="email" autocomplete="email">
          </div>
          <div class="field">
            {label("lead.l.telefon", "l_tel", True)}
            <input class="input" id="l_tel" name="telefon" type="tel" autocomplete="tel">
          </div>
        </div>
        <div class="field">
          {label("lead.l.megjegyzes", "l_msg")}
          <textarea class="input textarea" id="l_msg" name="megjegyzes" rows="4"></textarea>
        </div>
        <label class="consent">
          <input type="checkbox" id="pconsent" name="adatkezeles_elfogadva" value="1">
          <span><span data-i18n="lead.privacy">{tx("lead.privacy")}</span>{req()}</span>
        </label>
      </fieldset>

      <div class="wiz-nav">
        <button class="btn btn-quiet is-hidden" type="button" id="wizBack" aria-label="Back">&larr;</button>
        <button class="btn btn-next" type="button" id="wizNext" aria-label="Next">&rarr;</button>
        <button class="btn is-hidden" type="submit" id="wizSend">
          <span data-i18n="lead.submit">{tx("lead.submit")}</span>{ARROW}</button>
      </div>

      {el("p", "lead.required", "wiz-note")}
      <p class="form-msg" id="wizMsg" role="status" aria-live="polite"></p>
    </form>
    </div>
  </section>
"""


# ---------------------------------------------------------------- the page

def page_index():
    return head() + navbar() + f"""
<main id="top">
{sec_hero()}
{sec_proof()}
{sec_calc()}
{sec_why()}
{sec_process()}
{sec_kinds()}
{sec_lead()}
{sec_faq()}
</main>
{FOOTER}"""


SUBS = [("miert.html", "nav.why", sec_why), ("folyamat.html", "nav.process", sec_process),
        ("ingatlanok.html", "nav.kinds", sec_kinds), ("gyik.html", "nav.faq", sec_faq)]


def make_sub(i):
    def page():
        name, key, sec = SUBS[i]
        nname, nkey, _ = SUBS[(i + 1) % len(SUBS)]
        out = head(key, False) + navbar(name) + f"""
<main id="top">
  <header class="page-head{" wide" if name == "miert.html" else ""}">
    <p class="crumbs"><a href="index.html">acasara.ro</a><i>/</i><span data-i18n="{key}">{tx(key)}</span></p>
    {el("h1", key)}
  </header>
{sec()}
  <a class="next-page" href="{nname}"><span class="np-t" data-i18n="{nkey}">{tx(nkey)}</span><span class="np-ar" aria-hidden="true">&rarr;</span></a>
</main>
{FOOTER}"""
        return out.replace('href="#kapcsolat"', 'href="kezdjuk-el.html"')
    return page


def page_apply():
    key = "proc.cta"
    return head(key, False) + navbar("kezdjuk-el.html") + f"""
<main id="top">
  <header class="page-head">
    <p class="crumbs"><a href="index.html">acasara.ro</a><i>/</i><span data-i18n="{key}">{tx(key)}</span></p>
    {el("h1", key)}
  </header>
{sec_lead()}
</main>
{FOOTER}"""


PAGES = {"index.html": page_index, "kezdjuk-el.html": page_apply}
for _i, (_name, _k, _s) in enumerate(SUBS):
    PAGES[_name] = make_sub(_i)

if __name__ == "__main__":
    for name, fn in PAGES.items():
        path = os.path.join(HERE, name)
        io.open(path, "w", encoding="utf-8", newline=chr(10)).write(fn())
        print("%-24s %6d bytes" % (name, os.path.getsize(path)))
