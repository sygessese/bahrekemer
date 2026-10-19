// ባሕረ ቀመር — language, reading mode, text size, Ethiopian date, menu, gentle reveal
(function () {
  var d = document.documentElement;
  function store(k, v) { try { localStorage.setItem(k, v); } catch (e) {} }
  function all(sel, root) { return Array.prototype.slice.call((root || document).querySelectorAll(sel)); }

  function sync() {
    all("[data-set-lang]").forEach(function (b) { b.setAttribute("aria-pressed", String(b.getAttribute("data-set-lang") === d.getAttribute("data-lang"))); });
    all("[data-read-set]").forEach(function (b) { b.setAttribute("aria-pressed", String(b.getAttribute("data-read-set") === d.getAttribute("data-read"))); });
    all("[data-size-toggle]").forEach(function (b) { b.setAttribute("aria-pressed", String(d.classList.contains("big"))); });
  }

  function setRead(r) { d.setAttribute("data-read", r); store("read", r); sync(); }

  function setLang(l) {
    d.setAttribute("data-lang", l);
    d.lang = l;
    document.title = d.getAttribute("data-title-" + l) || document.title;
    store("lang", l);
    var phone = matchMedia("(max-width: 640px)").matches;
    setRead(phone ? l : (l === "en" ? "both" : "am"));   // Amharic: Amharic only. English: both languages.
    try {
      var url = new URL(location.href);
      if (l === "en") url.searchParams.set("lang", "en"); else url.searchParams.delete("lang");
      history.replaceState(null, "", url);
    } catch (e) {}
  }

  all("[data-set-lang]").forEach(function (b) { b.addEventListener("click", function () { setLang(b.getAttribute("data-set-lang")); }); });
  all("[data-read-set]").forEach(function (b) { b.addEventListener("click", function () { setRead(b.getAttribute("data-read-set")); }); });
  all("[data-size-toggle]").forEach(function (b) {
    b.addEventListener("click", function () { var on = d.classList.toggle("big"); store("big", on ? "1" : "0"); sync(); });
  });

  // ---- Ethiopian calendar date line --------------------------------------------------------
  function geez(n) {
    var ones = ["", "፩", "፪", "፫", "፬", "፭", "፮", "፯", "፰", "፱"], tens = ["", "፲", "፳", "፴", "፵", "፶", "፷", "፸", "፹", "፺"];
    function two(x) { return tens[Math.floor(x / 10)] + ones[x % 10]; }
    if (n < 100) return two(n);
    var hi = Math.floor(n / 100), lo = n % 100;
    return (hi === 1 ? "" : two(hi)) + "፻" + (lo ? two(lo) : "");
  }
  function ethiopic(dt) {
    var y = dt.getFullYear(), m = dt.getMonth() + 1, day = dt.getDate();
    var a = Math.floor((14 - m) / 12), yy = y + 4800 - a, mm = m + 12 * a - 3;
    var jdn = day + Math.floor((153 * mm + 2) / 5) + 365 * yy + Math.floor(yy / 4) - Math.floor(yy / 100) + Math.floor(yy / 400) - 32045;
    var e = jdn - 1723856, r = ((e % 1461) + 1461) % 1461, n = (r % 365) + 365 * Math.floor(r / 1460);
    return { year: 4 * Math.floor(e / 1461) + Math.floor(r / 365) - Math.floor(r / 1460), month: Math.floor(n / 30) + 1, day: (n % 30) + 1 };
  }
  var today = document.querySelector("[data-today]");
  if (today) {
    var now = new Date(), et = ethiopic(now);
    var wd = ["እሑድ", "ሰኞ", "ማክሰኞ", "ረቡዕ", "ሐሙስ", "ዓርብ", "ቅዳሜ"][now.getDay()];
    var mo = ["መስከረም", "ጥቅምት", "ኅዳር", "ታኅሣሥ", "ጥር", "የካቲት", "መጋቢት", "ሚያዝያ", "ግንቦት", "ሰኔ", "ሐምሌ", "ነሐሴ", "ጳጉሜን"][et.month - 1];
    var en = now.toLocaleDateString("en-GB", { weekday: "long", day: "numeric", month: "long", year: "numeric" });
    today.innerHTML = '<span lang="am">' + wd + "፡ " + mo + " " + geez(et.day) + " ቀን " + geez(et.year) + ' ዓ.ም.</span><span lang="en">' + en + "</span>";
  }

  // ---- Reading pages: pair each Amharic block with its English so they can sit side by side ----
  function pair(root) {
    all('[lang="am"]:not(span):not(.lx):not(.always)', root).forEach(function (am) {
      if (!am.isConnected || (am.parentElement && am.parentElement.classList.contains("bi"))) return;
      var en = am.nextElementSibling;
      if (!en || en.getAttribute("lang") !== "en" || en.tagName === "SPAN") return;
      var ka = Array.prototype.slice.call(am.children), ke = Array.prototype.slice.call(en.children);
      var same = am.tagName === "DIV" && en.tagName === "DIV" && !am.className && !en.className && ka.length > 1 &&
                 ka.length === ke.length && ka.every(function (c, i) { return c.tagName === ke[i].tagName; });
      if (same) {   // two parallel blocks → one row per paragraph/heading
        var group = document.createElement("div");
        group.className = "bi-group";
        ka.forEach(function (c, i) {
          var row = document.createElement("div");
          row.className = "bi" + (/^H\d$/.test(c.tagName) ? " bi-head" : "");
          c.setAttribute("lang", "am"); ke[i].setAttribute("lang", "en");
          row.appendChild(c); row.appendChild(ke[i]);
          group.appendChild(row);
        });
        am.parentNode.insertBefore(group, am);
        am.remove(); en.remove();
      } else {
        var wrap = document.createElement("div");
        wrap.className = "bi";
        am.parentNode.insertBefore(wrap, am);
        wrap.appendChild(am); wrap.appendChild(en);
      }
    });
  }
  if (document.body.classList.contains("is-reader")) {
    var pb = document.querySelector(".page-body");
    if (pb) pair(pb);
  }
  sync();

  // ---- Book covers: front / back ------------------------------------------------------------
  all("[data-flip]").forEach(function (f) {
    var faces = all(".flip-face", f), i = 0;
    function show(n) {
      i = Math.max(0, Math.min(faces.length - 1, n));
      faces.forEach(function (x, k) { x.classList.toggle("is-on", k === i); });
      all("[data-flip-to]", f).forEach(function (b) { b.setAttribute("aria-pressed", String(+b.getAttribute("data-flip-to") === i)); });
      var prev = f.querySelector(".flip-prev"), next = f.querySelector(".flip-next");
      if (prev) prev.hidden = i === 0;
      if (next) next.hidden = i === faces.length - 1;
    }
    all("[data-flip-go]", f).forEach(function (b) { b.addEventListener("click", function () { show(i + +b.getAttribute("data-flip-go")); }); });
    all("[data-flip-to]", f).forEach(function (b) { b.addEventListener("click", function () { show(+b.getAttribute("data-flip-to")); }); });
    faces.forEach(function (x) { x.addEventListener("click", function () { show(i === faces.length - 1 ? 0 : i + 1); }); x.style.cursor = "pointer"; });
    document.addEventListener("keydown", function (e) {
      if (e.key === "ArrowRight") show(i + 1);
      if (e.key === "ArrowLeft") show(i - 1);
    });
    var x0 = null;
    f.addEventListener("touchstart", function (e) { x0 = e.touches[0].clientX; }, { passive: true });
    f.addEventListener("touchend", function (e) {
      if (x0 === null) return;
      var dx = e.changedTouches[0].clientX - x0; x0 = null;
      if (Math.abs(dx) > 50) show(i + (dx < 0 ? 1 : -1));
    });
    show(0);
  });

  // ---- Menu ---------------------------------------------------------------------------------
  var menuBtn = document.querySelector(".menu-btn"), nav = document.getElementById("nav");
  if (menuBtn && nav) {
    menuBtn.addEventListener("click", function () {
      var open = nav.classList.toggle("open");
      menuBtn.setAttribute("aria-expanded", open ? "true" : "false");
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && nav.classList.contains("open")) {
        nav.classList.remove("open"); menuBtn.setAttribute("aria-expanded", "false"); menuBtn.focus();
      }
    });
  }

  // ---- Gentle fade as content scrolls into view -------------------------------------------
  if ("IntersectionObserver" in window && !matchMedia("(prefers-reduced-motion: reduce)").matches && !matchMedia("(max-width: 640px)").matches) {
    var sel = ".front > *, .band-inner, .contents li, .more-item, .profile-inner > *, .book-strip li, " +
              ".page-body .bi, .page-body .prose > p, .key-sec, .num-entry, .notice, .qene, .worksheet, .poem, " +
              ".shelf-item, .gallery figure, .contact-card, .guest, .buy, .writings-list li";
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        var el = e.target;
        el.classList.add("in");
        io.unobserve(el);
        el.addEventListener("transitionend", function done() {
          el.classList.remove("reveal", "in"); el.style.removeProperty("--d");
          el.removeEventListener("transitionend", done);
        });
      });
    }, { rootMargin: "0px 0px -6% 0px", threshold: 0.06 });
    all(sel).forEach(function (el) {
      var i = el.parentElement ? Array.prototype.indexOf.call(el.parentElement.children, el) : 0;
      if (el.matches(".contents li, .more-item, .book-strip li, .shelf-item, .gallery figure, .front > *")) el.style.setProperty("--d", (i % 4) * 0.08 + "s");
      el.classList.add("reveal");
      io.observe(el);
    });
  }
})();
