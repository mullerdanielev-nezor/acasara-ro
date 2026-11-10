/* Acasara — shared behaviour: i18n, preloader, navbar, reveal, parallax, offer form.
   Depends on i18n.js (window.T, window.LOCALES). No other dependencies. */
(function () {
  "use strict";

  var LOCALES = window.LOCALES || [];
  var T = window.T || {};
  var CODES = LOCALES.map(function (l) { return l.code; });
  var FALLBACK = "ro";
  var STORE = "acasara.lang";

  /* ---------- locale resolution ---------- */

  function pickLocale() {
    var q = new URLSearchParams(location.search).get("lang");
    if (q && CODES.indexOf(q) > -1) return q;

    var saved;
    try { saved = localStorage.getItem(STORE); } catch (e) { /* private mode */ }
    if (saved && CODES.indexOf(saved) > -1) return saved;

    var nav = (navigator.languages || [navigator.language || ""]);
    for (var i = 0; i < nav.length; i++) {
      var base = String(nav[i]).toLowerCase().split("-")[0];
      if (CODES.indexOf(base) > -1) return base;
    }
    return FALLBACK;
  }

  function translate(code) {
    var dict = T[code] || T[FALLBACK];
    var base = T[FALLBACK];

    document.documentElement.lang = code;

    document.querySelectorAll("[data-i18n]").forEach(function (el) {
      var key = el.getAttribute("data-i18n");
      var val = dict[key] !== undefined ? dict[key] : base[key];
      if (val === undefined) return;             // unknown key: leave the markup alone
      var attr = el.getAttribute("data-i18n-attr");
      if (attr) el.setAttribute(attr, val);
      else el.textContent = val;
    });

    // <title> carries its own key so each page gets a translated tab label
    var t = document.querySelector("title[data-i18n]");
    if (t) document.title = t.textContent;

    try { localStorage.setItem(STORE, code); } catch (e) { /* ignore */ }

    // keep ?lang= in the URL so a copied link keeps the language
    var url = new URL(location.href);
    url.searchParams.set("lang", code);
    history.replaceState(null, "", url);

    // internal links carry the language across pages
    document.querySelectorAll('a[href]').forEach(function (a) {
      var href = a.getAttribute("href");
      if (!href || /^(https?:|mailto:|tel:|#)/.test(href)) return;
      var u = new URL(href, location.href);
      u.searchParams.set("lang", code);
      a.setAttribute("href", u.pathname.split("/").pop() + u.search + u.hash);
    });

    document.querySelectorAll(".lang-menu button").forEach(function (b) {
      b.setAttribute("aria-current", String(b.dataset.code === code));
    });
    var cur = document.querySelector(".lang-cur");
    if (cur) cur.textContent = code.toUpperCase();

    document.dispatchEvent(new CustomEvent("acasara:lang"));
  }

  /* ---------- language switcher ---------- */

  function buildSwitcher(code) {
    var wrap = document.querySelector(".lang");
    if (!wrap) return;

    var menu = wrap.querySelector(".lang-menu");
    menu.innerHTML = "";
    LOCALES.forEach(function (l) {
      var b = document.createElement("button");
      b.type = "button";
      b.dataset.code = l.code;
      b.innerHTML = "<b>" + l.code + "</b><span></span>";
      b.querySelector("span").textContent = l.label;
      b.addEventListener("click", function () {
        translate(l.code);
        wrap.dataset.open = "false";
      });
      menu.appendChild(b);
    });

    var btn = wrap.querySelector(".lang-btn");
    btn.addEventListener("click", function (e) {
      e.stopPropagation();
      wrap.dataset.open = wrap.dataset.open === "true" ? "false" : "true";
      btn.setAttribute("aria-expanded", wrap.dataset.open);
    });
    document.addEventListener("click", function () { wrap.dataset.open = "false"; });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") wrap.dataset.open = "false";
    });
    menu.addEventListener("click", function (e) { e.stopPropagation(); });
  }

  /* ---------- preloader ---------- */

  function preloader() {
    var el = document.getElementById("loader");
    if (!el) return;
    var start = Date.now();
    function hide() {
      setTimeout(function () { el.classList.add("done"); }, Math.max(0, 1400 - (Date.now() - start)));
    }
    if (document.readyState === "complete") hide();
    else window.addEventListener("load", hide);
    // never trap the page behind a stalled asset
    setTimeout(function () { el.classList.add("done"); }, 6000);
  }

  /* ---------- navbar over a video hero ---------- */

  function navbar() {
    var bar = document.querySelector(".navbar");
    var hero = document.querySelector(".hero");
    if (!bar || !hero || !window.IntersectionObserver) return;
    new IntersectionObserver(function (entries) {
      bar.classList.toggle("is-fixed", !entries[0].isIntersecting);
    }, { rootMargin: "-120px 0px 0px 0px", threshold: 0 }).observe(hero);
  }

  /* ---------- reveal on scroll ---------- */

  function reveal() {
    // the footer map traces itself once it scrolls into view
    var map = document.querySelector(".foot-map");
    if (map && window.IntersectionObserver) {
      var mio = new IntersectionObserver(function (es) {
        if (es[0].isIntersecting) { map.classList.add("in"); mio.disconnect(); }
      }, { threshold: .25 });
      mio.observe(map);
    } else if (map) {
      map.classList.add("in");
    }

    var items = document.querySelectorAll(".rv");
    if (!window.IntersectionObserver) {
      items.forEach(function (el) { el.classList.add("in"); });
      return;
    }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        var sibs = Array.prototype.filter.call(e.target.parentNode.children, function (n) {
          return n.classList.contains("rv");
        });
        e.target.style.transitionDelay = (Math.max(0, sibs.indexOf(e.target)) * 70) + "ms";
        e.target.classList.add("in");
        io.unobserve(e.target);
      });
    }, { rootMargin: "0px 0px -12% 0px", threshold: .12 });
    items.forEach(function (el) { io.observe(el); });
  }

  /* ---------- scatter parallax ---------- */

  function parallax() {
    var stage = document.querySelector(".scatter-stage");
    if (!stage) return;
    var layers = [].slice.call(stage.querySelectorAll(".sct"));
    var depths = [.16, -.1, .22, -.16, .1, -.22];
    var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    var ticking = false;

    function frame() {
      ticking = false;
      if (reduce || window.innerWidth <= 860) return;
      var r = stage.getBoundingClientRect();
      if (r.bottom < 0 || r.top > window.innerHeight) return;
      var mid = (r.top + r.height / 2 - window.innerHeight / 2) / window.innerHeight;
      layers.forEach(function (el, i) {
        el.style.translate = "0 " + (mid * (depths[i % depths.length] * 170)).toFixed(1) + "px";
      });
    }
    window.addEventListener("scroll", function () {
      if (!ticking) { ticking = true; requestAnimationFrame(frame); }
    }, { passive: true });
    window.addEventListener("resize", function () {
      if (window.innerWidth <= 860) layers.forEach(function (el) { el.style.translate = ""; });
      frame();
    });
    frame();
  }

  /* ---------- offer form ---------- */

  function offerForm() {
    var form = document.getElementById("offerForm");
    if (!form) return;
    var msg = document.getElementById("formMsg");

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var code = document.documentElement.lang || FALLBACK;
      var dict = T[code] || T[FALLBACK];
      var ok = true;

      ["address", "name", "phone"].forEach(function (id) {
        var input = form.elements[id];
        var field = input.closest(".field");
        var bad = !input.value.trim();
        field.classList.toggle("invalid", bad);
        input.setAttribute("aria-invalid", String(bad));
        if (bad) ok = false;
      });
      if (!form.elements.consent.checked) ok = false;

      msg.className = "form-msg show " + (ok ? "ok" : "bad");
      msg.textContent = ok ? dict["offer.thanks"] : dict["offer.err"];

      if (ok) {
        // TODO: POST to your endpoint / CRM here. Shape of the payload:
        // { address, type, name, phone, lang: code, page: location.pathname }
        form.reset();
        ["address", "name", "phone"].forEach(function (id) {
          form.elements[id].closest(".field").classList.remove("invalid");
        });
      }
    });
  }

  /* ---------- hero playlist ---------- */

  function heroPlaylist() {
    var wrap = document.getElementById("heroMedia");
    if (!wrap) return;

    var clips = (wrap.dataset.clips || "").split(",").filter(Boolean);
    if (clips.length < 2) return;

    var vids = [].slice.call(wrap.querySelectorAll(".hero-vid"));
    if (vids.length < 2) return;

    var SEGMENT = 6000;   // how long each clip stays on screen
    var FADE    = 1100;   // must match the CSS transition

    var at = 0;           // index of the clip on screen
    var live = 0;         // which <video> element is showing it
    var passes = [];      // how many times each clip has been shown
    clips.forEach(function () { passes.push(0); });
    var timer = null;

    function other() { return live === 0 ? 1 : 0; }

    // each time a clip comes round again, start it further in, so the
    // sequence keeps showing new footage instead of replaying the same seconds
    function offsetFor(index, video) {
      var d = video.duration;
      if (!d || !isFinite(d) || d <= SEGMENT / 1000) return 0;
      var usable = d - SEGMENT / 1000;
      return (passes[index] * (SEGMENT / 1000)) % usable;
    }

    function queueNext() {
      var nextClip = clips[(at + 1) % clips.length];
      var idle = vids[other()];
      if (idle.getAttribute("src") !== nextClip) {
        idle.setAttribute("src", nextClip);
        idle.load();
      }
    }

    function arm() {
      clearTimeout(timer);
      timer = setTimeout(advance, SEGMENT);
    }

    function advance() {
      clearTimeout(timer);
      var idle = vids[other()];
      var showing = vids[live];
      var nextIndex = (at + 1) % clips.length;

      // not buffered yet: keep the current clip running rather than cutting to black
      if (idle.readyState < 2) { arm(); return; }

      passes[nextIndex]++;
      try { idle.currentTime = offsetFor(nextIndex, idle); } catch (e) { /* seek refused */ }

      var p = idle.play();
      if (p && p.catch) p.catch(function () { /* autoplay refused */ });

      idle.classList.add("is-on");
      showing.classList.remove("is-on");

      at = nextIndex;
      live = other();

      setTimeout(function () { showing.pause(); queueNext(); }, FADE);
      arm();
    }

    vids.forEach(function (v) {
      // a clip shorter than the segment still hands over cleanly
      v.addEventListener("ended", function () { if (v.classList.contains("is-on")) advance(); });
      v.addEventListener("error", function () { if (v.classList.contains("is-on")) advance(); });
    });

    vids[0].play().catch(function () { /* ignore */ });
    queueNext();
    arm();

    // no point burning frames on a hidden tab
    document.addEventListener("visibilitychange", function () {
      if (document.hidden) clearTimeout(timer);
      else arm();
    });
  }

  /* ---------- offer calculator ---------- */

  function calculator() {
    var form = document.getElementById("calcForm");
    if (!form) return;
    var out = document.getElementById("calcVal");

    // indicative EUR/m2 by build type, then adjusted for condition and age.
    // deliberately simple and visible: it is a guide, not a valuation.
    var BASE  = { brick: 1500, panel: 1250, house: 1100, studio: 1600 };
    var COND  = { new: 1.15, renovated: 1.05, liveable: 0.95, torenovate: 0.80 };
    var BUY   = [0.78, 0.86];   // what a cash buyer pays against market value

    function ageFactor(year) {
      if (!year) return 1;
      if (year >= 2010) return 1.08;
      if (year >= 1990) return 1.00;
      if (year >= 1970) return 0.94;
      return 0.88;
    }

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var type = (form.querySelector('input[name="ctype"]:checked') || {}).value || "brick";
      var size = parseFloat(form.elements.csize.value) || 0;
      var year = parseInt(form.elements.cyear.value, 10) || 0;
      var cond = form.elements.ccond.value || "liveable";

      if (size <= 0) { out.textContent = "—"; return; }

      var market = BASE[type] * (COND[cond] || 1) * ageFactor(year) * size;
      var lo = Math.round(market * BUY[0] / 1000) * 1000;
      var hi = Math.round(market * BUY[1] / 1000) * 1000;

      var code = document.documentElement.lang || FALLBACK;
      var fmt = new Intl.NumberFormat(code, { style: "currency", currency: "EUR",
                                              maximumFractionDigits: 0 });
      out.textContent = fmt.format(lo) + " – " + fmt.format(hi);
    });
  }

  /* ---------- enquiry form: four steps ---------- */

  function enquiryForm() {
    var form = document.getElementById("enquiry");
    if (!form) return;

    var panes  = [].slice.call(form.querySelectorAll(".wiz-pane"));
    var rail   = [].slice.call(form.querySelectorAll("#wizRail li"));
    var bar    = document.getElementById("wizBar");
    var count  = document.getElementById("wizCount");
    var back   = document.getElementById("wizBack");
    var next   = document.getElementById("wizNext");
    var send   = document.getElementById("wizSend");
    var msg    = document.getElementById("wizMsg");

    // which fields each step insists on before it lets you move on
    var NEEDED = { 2: ["paddress"], 4: ["plast", "pfirst", "pemail", "pphone"] };
    var at = 0;

    function dict() {
      var code = document.documentElement.lang || FALLBACK;
      return T[code] || T[FALLBACK];
    }

    function flag(el, bad) {
      var field = el.closest(".field");
      if (field) field.classList.toggle("invalid", bad);
      el.setAttribute("aria-invalid", String(bad));
    }

    function render() {
      panes.forEach(function (p, i) { p.classList.toggle("is-hidden", i !== at); });
      rail.forEach(function (li, i) {
        li.classList.toggle("done", i < at);
        if (i === at) li.setAttribute("aria-current", "step");
        else li.removeAttribute("aria-current");
      });
      bar.style.width = (((at + 1) / panes.length) * 100) + "%";
      count.textContent = (dict()["f.stepOf"] || "").replace("{n}", String(at + 1));
      back.classList.toggle("is-hidden", at === 0);
      next.classList.toggle("is-hidden", at === panes.length - 1);
      send.classList.toggle("is-hidden", at !== panes.length - 1);
      msg.className = "form-msg";
    }

    // validate one step; returns true when it may be left
    function stepOk(index) {
      var ids = NEEDED[index + 1] || [];
      var ok = true, firstBad = null;

      ids.forEach(function (id) {
        var el = form.elements[id];
        var bad = !el.value.trim();
        if (!bad && id === "pemail") bad = !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(el.value.trim());
        flag(el, bad);
        if (bad) { ok = false; firstBad = firstBad || el; }
      });

      // the consent box lives on the last step
      if (index === panes.length - 1) {
        var c = form.elements.pconsent;
        if (!c.checked) { ok = false; firstBad = firstBad || c; c.setAttribute("aria-invalid", "true"); }
        else c.setAttribute("aria-invalid", "false");
      }

      if (!ok) {
        msg.className = "form-msg show bad";
        msg.textContent = dict()["offer.err"];
        if (firstBad) firstBad.focus();
      }
      return ok;
    }

    next.addEventListener("click", function () {
      if (!stepOk(at)) return;
      at = Math.min(at + 1, panes.length - 1);
      render();
      form.scrollIntoView({ block: "start", behavior: "smooth" });
    });

    back.addEventListener("click", function () {
      at = Math.max(at - 1, 0);
      render();
      form.scrollIntoView({ block: "start", behavior: "smooth" });
    });

    // clicking a rail step jumps back to it (never forward past an unfilled step)
    rail.forEach(function (li, i) {
      li.addEventListener("click", function () {
        if (i < at) { at = i; render(); }
      });
    });

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      // re-check every step, not just the last one
      for (var i = 0; i < panes.length; i++) {
        if (!stepOk(i)) { at = i; render(); msg.className = "form-msg show bad";
                          msg.textContent = dict()["offer.err"]; return; }
      }
      msg.className = "form-msg show ok";
      msg.textContent = dict()["offer.thanks"];

      // TODO: POST to your endpoint / CRM. Payload:
      // { role, ptype, paddress, psize, pplot, pcond, padv, plisting, pprice,
      //   plast, pfirst, pemail, pphone, pmsg, lang }
      form.reset();
      Object.keys(NEEDED).forEach(function (k) {
        NEEDED[k].forEach(function (id) { flag(form.elements[id], false); });
      });
      at = 0;
      render();
      msg.className = "form-msg show ok";
      msg.textContent = dict()["offer.thanks"];
    });

    // clear a field's error as soon as it is filled
    Object.keys(NEEDED).forEach(function (k) {
      NEEDED[k].forEach(function (id) {
        var el = form.elements[id];
        el.addEventListener("input", function () { if (el.value.trim()) flag(el, false); });
      });
    });

    // the step counter has to follow a language change
    document.addEventListener("acasara:lang", render);

    render();
  }

  /* ---------- boot ---------- */

  function start() {
    var code = pickLocale();
    buildSwitcher(code);
    translate(code);
    preloader();
    navbar();
    reveal();
    parallax();
    heroPlaylist();
    offerForm();
    enquiryForm();
    calculator();
    var y = document.getElementById("year");
    if (y) y.textContent = new Date().getFullYear();
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start);
  else start();
})();
