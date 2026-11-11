/* Acasara - behaviour: i18n, preloader, navbar, reveal, hero playlist, process timeline, calculator, enquiry form.
   Depends on i18n.js (window.T, window.LOCALES). No other dependencies. */
(function () {
  "use strict";

  var LOCALES = window.LOCALES || [];
  var T = window.T || {};
  var CODES = LOCALES.map(function (l) { return l.code; });
  var FALLBACK = "ro";
  var STORE = "acasara.lang";

  // TODO: back-end addresses. Empty = nothing is sent yet; the forms still validate and show the confirmation.
  //   lead     - receives the enquiry form (fields as in the markup)
  //   estimate - receives the calculator form (azzupp.com computes the estimate on a private server model)
  var ENDPOINT = { lead: "", estimate: "" };

  function dict() { return T[document.documentElement.lang] || T[FALLBACK]; }

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
    var d = T[code] || T[FALLBACK];
    var base = T[FALLBACK];

    document.documentElement.lang = code;

    document.querySelectorAll("[data-i18n]").forEach(function (el) {
      var key = el.getAttribute("data-i18n");
      var val = d[key] !== undefined ? d[key] : base[key];
      if (val === undefined) return;             // unknown key: leave the markup alone
      var attr = el.getAttribute("data-i18n-attr");
      if (attr) el.setAttribute(attr, val);
      else el.textContent = val;
    });

    // <title> carries its own key so the tab label is translated too
    var t = document.querySelector("title[data-i18n]");
    if (t) document.title = t.textContent;
    var md = document.querySelector('meta[name="description"]');
    if (md && d["meta.desc"]) md.setAttribute("content", d["meta.desc"]);

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

  function buildSwitcher() {
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
    if (!bar) return;
    // mobile menu: the burger opens the full-screen overlay (clip-path circle grows out of the button)
    var burger = bar.querySelector(".nav-burger");
    var overlay = document.getElementById("menuFull");
    if (burger && overlay) {
      var setOpen = function (open) {
        document.body.classList.toggle("menu-open", open);
        bar.classList.toggle("open", open);
        burger.setAttribute("aria-expanded", open ? "true" : "false");
        overlay.setAttribute("aria-hidden", open ? "false" : "true");
      };
      burger.addEventListener("click", function () { setOpen(!document.body.classList.contains("menu-open")); });
      overlay.querySelectorAll("a").forEach(function (a) { a.addEventListener("click", function () { setOpen(false); }); });
      document.addEventListener("keydown", function (e) { if (e.key === "Escape") setOpen(false); });
      window.addEventListener("resize", function () { if (window.innerWidth > 1040) setOpen(false); });
    }
    // sub-pages keep the bar visible from the top
    if (bar.hasAttribute("data-static")) return;
    // hidden on the very first screen position; appears once you scroll down and stays (hysteresis avoids flicker)
    var away = true;
    function sync() {
      var y = window.pageYOffset || document.documentElement.scrollTop || 0;
      if (away && y > 56) { away = false; bar.classList.remove("is-away"); }
      else if (!away && y < 8) { away = true; bar.classList.add("is-away"); }
    }
    window.addEventListener("scroll", sync, { passive: true });
    sync();
    var hero = document.querySelector(".hero");
    if (!hero || !window.IntersectionObserver) return;
    new IntersectionObserver(function (entries) {
      bar.classList.toggle("is-fixed", !entries[0].isIntersecting);
    }, { rootMargin: "-120px 0px 0px 0px", threshold: 0 }).observe(hero);
  }

  /* ---------- reveal on scroll ---------- */

  /* ---------- enquiry-panel map: a light draws the outline, dots flood in from the centre, then soft rings ---------- */

  function romaniaIntro(map, instant) {
    var path = map.querySelector(".map-outline"), pen = map.querySelector(".wm-pen"), rev = map.querySelector(".wm-reveal");
    var rings = [].slice.call(map.querySelectorAll(".wm-ring"));
    var L = path.getTotalLength(), bb = path.getBBox();
    var cx = bb.x + bb.width / 2, cy = bb.y + bb.height / 2;
    var R = Math.sqrt(bb.width * bb.width + bb.height * bb.height) / 2 + 20;
    rev.setAttribute("cx", cx); rev.setAttribute("cy", cy);
    rings.forEach(function (r) { r.setAttribute("cx", cx); r.setAttribute("cy", cy); });
    path.style.strokeDasharray = L;
    var calm = instant || (window.matchMedia && matchMedia("(prefers-reduced-motion:reduce)").matches);
    function finish() { pen.style.opacity = 0; path.style.strokeDashoffset = 0; rev.setAttribute("r", R); map.classList.add("done"); }
    if (calm) { finish(); return; }
    path.style.strokeDashoffset = L;
    var DRAW = 3000, FLOOD = 2800, FLOOD_AT = 1300, t0 = null;
    function ease(x) { return x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2; }
    function out(x) { return 1 - Math.pow(1 - x, 3); }
    function frame(now) {
      if (t0 === null) t0 = now;
      var t = now - t0;
      var d = Math.min(1, t / DRAW), e = ease(d);
      path.style.strokeDashoffset = L * (1 - e);
      var pt = path.getPointAtLength(L * e);
      pen.setAttribute("cx", pt.x); pen.setAttribute("cy", pt.y);
      pen.style.opacity = d < 1 ? 1 : Math.max(0, 1 - (t - DRAW) / 400);
      var f = Math.max(0, Math.min(1, (t - FLOOD_AT) / FLOOD));
      rev.setAttribute("r", R * out(f));
      if (t < FLOOD_AT + FLOOD) requestAnimationFrame(frame); else finish();
    }
    requestAnimationFrame(frame);
  }

  function reveal() {
    // the Romania outlines (footer + enquiry panel) trace themselves once they scroll into view
    var maps = [].slice.call(document.querySelectorAll(".foot-map, .wiz-map"));
    maps.forEach(function (map) {
      if (!window.IntersectionObserver) { map.classList.add("in"); if (map.classList.contains("wiz-map")) romaniaIntro(map, true); return; }
      var mio = new IntersectionObserver(function (es) {
        if (es[0].isIntersecting) { map.classList.add("in"); if (map.classList.contains("wiz-map")) romaniaIntro(map); mio.disconnect(); }
      }, { threshold: .25 });
      mio.observe(map);
    });

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

  /* ---------- shared: send a form (or accept it while no endpoint is set) ---------- */

  function postForm(url, form, msg, done) {
    msg.className = "form-msg show";
    msg.textContent = dict()["msg.sending"];

    function finish(ok) {
      msg.className = "form-msg show " + (ok ? "ok" : "bad");
      msg.textContent = dict()[ok ? "msg.success" : "msg.error"];
      if (ok && done) done();
    }
    if (!url) { finish(true); return; }                       // TODO: endpoint not configured yet
    fetch(url, { method: "POST", body: new FormData(form) })
      .then(function (r) { if (!r.ok) throw new Error("http " + r.status); finish(true); })
      .catch(function () { finish(false); });
  }

  /* ---------- "Trei pași clari" timeline: the rail fills, steps light up as you pass them ---------- */

  /* ---------- "5 reasons": vertical scroll drives a horizontal track ---------- */

  /* ---------- below-the-fold photos: fetched quietly once the page has settled, so they are ready when you arrive ---------- */

  /* ---------- optional single-choice pills: click the chosen one again to clear it ---------- */

  function clearablePills() {
    [].forEach.call(document.querySelectorAll("[data-clearable] input[type=radio]"), function (r) {
      r.addEventListener("pointerdown", function () { r._was = r.checked; });
      r.addEventListener("click", function () {
        if (r._was) { r.checked = false; r._was = false; r.dispatchEvent(new Event("change", { bubbles: true })); }
      });
    });
  }

  function warmImages() {
    var go = function () {
      [].forEach.call(document.querySelectorAll("img[loading=lazy]"), function (img) {
        img.loading = "eager";
        if (img.decode) img.decode().catch(function () {});
      });
    };
    if (document.readyState === "complete") setTimeout(go, 600);
    else window.addEventListener("load", function () { setTimeout(go, 600); });
  }

  function whyScroll() {
    var sec = document.getElementById("miert");
    if (!sec) return;
    var track = sec.querySelector(".why-track");
    var bar = sec.querySelector(".why-bar i");
    function frame() {
      if (innerWidth <= 820) { track.style.transform = ""; return; }
      var r = sec.getBoundingClientRect();
      var max = sec.offsetHeight - innerHeight;
      var p = Math.min(1, Math.max(0, -r.top / max));
      var pad = parseFloat(getComputedStyle(track).paddingLeft) || 0;     // scrollWidth leaves out the end padding
      var dist = Math.max(0, track.scrollWidth + pad - track.parentElement.clientWidth);
      track.style.transform = "translateX(" + (-p * dist) + "px)";
      bar.style.width = (p * 100) + "%";
    }
    addEventListener("scroll", frame, { passive: true });
    addEventListener("resize", frame);
    frame();
  }

  function howTrack() {
    var cols = [].slice.call(document.querySelectorAll(".how-col"));
    if (!cols.length) return;
    if (!window.IntersectionObserver) { cols.forEach(function (c) { c.classList.add("on"); }); return; }
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("on"); io.unobserve(e.target); } });
    }, { threshold: 0.25 });
    cols.forEach(function (c) { io.observe(c); });
  }

  /* ---------- calculator form: seven steps (blocks of azzupp.com's calculator) ---------- */

  function calcForm() {
    var form = document.getElementById("calcForm");
    if (!form) return;

    var panes = [].slice.call(form.querySelectorAll(".calc-pane"));      // 6 data blocks + the cash-offer question
    var rail = [].slice.call(form.querySelectorAll("#calcRail li"));
    var bar = document.getElementById("calcBar");
    var count = document.getElementById("calcCount");
    var back = document.getElementById("calcBack");
    var next = document.getElementById("calcNext");
    var send = document.getElementById("calcSend");
    var label = document.getElementById("calcSubmitLabel");
    var msg = document.getElementById("calcMsg");
    var body = document.getElementById("cashBody");
    var yes = document.getElementById("cashYes");
    var no = document.getElementById("cashNo");
    var choice = document.getElementById("cashChoice");
    var phone = document.getElementById("c_cashphone");
    var range = document.getElementById("areaRange");
    var rangeVal = document.getElementById("areaVal");
    var CASH = panes.length - 1;
    var at = 0;

    function setLabel(key) {
      label.setAttribute("data-i18n", key);
      label.textContent = dict()[key];
    }

    function paintRange() {
      rangeVal.textContent = range.value + " m²";
      range.style.setProperty("--p", ((range.value - range.min) / (range.max - range.min) * 100) + "%");
    }
    range.addEventListener("input", paintRange);

    function render() {
      panes.forEach(function (p, i) { p.classList.toggle("is-hidden", i !== at); });
      rail.forEach(function (li, i) {
        li.classList.toggle("done", i < at);
        if (i === at) li.setAttribute("aria-current", "step"); else li.removeAttribute("aria-current");
      });
      bar.style.width = (((at + 1) / panes.length) * 100) + "%";
      count.textContent = (at + 1) + " / " + panes.length;
      back.classList.toggle("is-hidden", at === 0);
      next.classList.toggle("is-hidden", at >= CASH - 1);
      send.classList.toggle("is-hidden", at < CASH - 1);
      setLabel(at === CASH ? "calc.cash.continue" : "calc.submit");
      msg.className = "form-msg";
    }

    // the required fields of one pane; shows the browser's own hint on the first bad one
    function paneOk(i) {
      var fields = [].slice.call(panes[i].querySelectorAll("input,select,textarea"));
      for (var k = 0; k < fields.length; k++) {
        if (!fields[k].disabled && !fields[k].checkValidity()) {
          msg.className = "form-msg show bad";
          msg.textContent = dict()["msg.invalid"];
          fields[k].reportValidity();
          return false;
        }
      }
      return true;
    }

    function go(i) { at = Math.max(0, Math.min(i, CASH)); render(); form.scrollIntoView({ block: "start", behavior: "smooth" }); }

    next.addEventListener("click", function () { if (paneOk(at)) go(at + 1); });
    back.addEventListener("click", function () { go(at - 1); });
    rail.forEach(function (li, i) {
      li.addEventListener("click", function () { if (i < at) go(i); });     // back only, never past an unchecked step
    });

    function chooseCash(wants) {
      choice.value = wants ? "igen" : "nem";
      phone.disabled = !wants;
      phone.required = wants;
      phone.setCustomValidity("");
      body.classList.toggle("is-hidden", !wants);
      yes.setAttribute("aria-pressed", String(wants));
      no.setAttribute("aria-pressed", String(!wants));
      yes.classList.toggle("is-on", wants);
      no.classList.toggle("is-on", !wants);
      if (wants) phone.focus();
      else { phone.value = ""; form.requestSubmit(); }
    }
    yes.addEventListener("click", function () { chooseCash(true); });
    no.addEventListener("click", function () { chooseCash(false); });
    phone.addEventListener("input", function () { phone.setCustomValidity(""); });

    function reset() {
      form.reset();
      choice.value = "";
      phone.disabled = true;
      body.classList.add("is-hidden");
      yes.classList.remove("is-on");
      no.classList.remove("is-on");
      at = 0;
      paintRange();
      render();
    }

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      // every data step must be valid, whichever one the person is on
      for (var i = 0; i < CASH; i++) {
        if (!paneOk(i)) { at = i; render(); paneOk(i); return; }
      }
      // all data in: next comes the optional cash-offer question, then the run
      if (!choice.value) {
        if (at !== CASH) { go(CASH); yes.focus({ preventScroll: true }); }
        else { msg.className = "form-msg show bad"; msg.textContent = dict()["msg.invalid"]; yes.focus(); }
        return;
      }
      if (choice.value === "igen") {
        var digits = phone.value.replace(/\D/g, "");
        if (!/^[+\d\s().-]+$/.test(phone.value) || digits.length < 7 || digits.length > 15) {
          phone.setCustomValidity(dict()["calc.cash.phone_error"]);
          phone.reportValidity();
          return;
        }
      }
      postForm(ENDPOINT.estimate, form, msg, function () {
        var text = msg.textContent;
        reset();
        msg.className = "form-msg show ok";
        msg.textContent = text;
      });
    });

    document.addEventListener("acasara:lang", function () { setLabel(label.getAttribute("data-i18n")); });
    paintRange();
    render();
  }

  /* ---------- enquiry form: four steps (fields of azzupp.com's contact form) ---------- */

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
    var NEEDED = { 2: ["ingatlan_pontos_cime"], 4: ["vezeteknev", "keresztnev", "email", "telefon"] };
    var at = 0;

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
      count.textContent = (at + 1) + " / " + panes.length;
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
        if (!bad && id === "email") bad = !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(el.value.trim());
        flag(el, bad);
        if (bad) { ok = false; firstBad = firstBad || el; }
      });

      // the consent box lives on the last step
      if (index === panes.length - 1) {
        var c = form.elements.adatkezeles_elfogadva;
        if (!c.checked) { ok = false; firstBad = firstBad || c; c.setAttribute("aria-invalid", "true"); }
        else c.setAttribute("aria-invalid", "false");
      }

      if (!ok) {
        msg.className = "form-msg show bad";
        msg.textContent = dict()["msg.invalid"];
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
        if (!stepOk(i)) {
          at = i; render();
          msg.className = "form-msg show bad";
          msg.textContent = dict()["msg.invalid"];
          return;
        }
      }
      postForm(ENDPOINT.lead, form, msg, function () {
        var text = msg.textContent;
        form.reset();
        Object.keys(NEEDED).forEach(function (k) {
          NEEDED[k].forEach(function (id) { flag(form.elements[id], false); });
        });
        at = 0;
        render();
        msg.className = "form-msg show ok";
        msg.textContent = text;
      });
    });

    // clear a field's error as soon as it is filled
    Object.keys(NEEDED).forEach(function (k) {
      NEEDED[k].forEach(function (id) {
        var el = form.elements[id];
        el.addEventListener("input", function () { if (el.value.trim()) flag(el, false); });
      });
    });

    render();
  }

  /* ---------- boot ---------- */

  function start() {
    var code = pickLocale();
    buildSwitcher();
    translate(code);
    preloader();
    navbar();
    reveal();
    heroPlaylist();
    howTrack();
    whyScroll();
    warmImages();
    clearablePills();
    calcForm();
    enquiryForm();
    var y = document.getElementById("year");
    if (y) y.textContent = new Date().getFullYear();
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start);
  else start();
})();
