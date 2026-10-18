// Language toggle + mobile menu
(function () {
  var root = document.documentElement;

  function setLang(lang, push) {
    root.setAttribute("data-lang", lang);
    root.lang = lang;
    document.title = root.getAttribute("data-title-" + lang) || document.title;
    try { localStorage.setItem("lang", lang); } catch (e) {}
    if (push) {
      try {
        var url = new URL(location.href);
        if (lang === "en") url.searchParams.set("lang", "en"); else url.searchParams.delete("lang");
        history.replaceState(null, "", url);
      } catch (e) {}
    }
  }

  document.querySelectorAll("[data-lang-toggle]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      setLang(root.getAttribute("data-lang") === "en" ? "am" : "en", true);
    });
  });

  var menuBtn = document.querySelector(".menu-btn");
  var nav = document.getElementById("nav");
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

  // Fade/rise content in as it scrolls into view
  if ("IntersectionObserver" in window && !matchMedia("(prefers-reduced-motion: reduce)").matches) {
    var sel = ".section-head, .card, .about > *, .page-body .prose > *, .megbiya h3, .megbiya p, .entry p, .entry blockquote, .entry .verse, " +
              ".book, .shelf-item, .qene-essay p, .qene, .worksheet, .key-sec h2, .key-sec p, .key-sec .table-wrap, .key-sec ol, .key-toc, .num-entry, .notice, .buy, .guest, .gallery figure, .poem, .glossary dt, .glossary dd, .contact-card";
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
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    document.querySelectorAll(sel).forEach(function (el) {
      var sibs = el.parentElement ? Array.prototype.indexOf.call(el.parentElement.children, el) : 0;
      if (el.matches(".card, .gallery figure, .shelf-item")) el.style.setProperty("--d", (sibs % 4) * 0.1 + "s");
      el.classList.add("reveal");
      io.observe(el);
    });
  }
})();
