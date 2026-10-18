#!/usr/bin/env python3
"""Builds the site: content/<page>.html + site.json  ->  <page>/index.html, 404.html, sitemap.xml.

Usage:  python3 build.py
No dependencies. Edit text in content/, page titles/descriptions in site.json, then re-run.
"""
import json, os, html
from datetime import date

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = json.load(open(os.path.join(ROOT, "site.json"), encoding="utf-8"))
GEEZ = ["", "፩", "፪", "፫", "፬", "፭", "፮", "፯", "፰", "፱", "፲"]


def t(am, en, tag="span", cls=""):
    """Bilingual pair: both are in the HTML; CSS shows the active language."""
    c = f' class="{cls}"' if cls else ""
    return f'<{tag} lang="am"{c}>{am}</{tag}><{tag} lang="en"{c}>{en}</{tag}>'


def esc(s):
    return html.escape(s, quote=True)


def href(slug):
    return "./" if slug == "index" else f"{slug}/"


def label(slug):
    return SITE["pages"][slug]["label"]


def section_no(slug):
    return GEEZ[SITE["sections"].index(slug) + 1] if slug in SITE["sections"] else ""


CROSS = ('<svg class="cross" viewBox="0 0 64 64" aria-hidden="true"><g fill="currentColor">'
         '<rect x="28" y="8" width="8" height="48" rx="1"/><rect x="8" y="28" width="48" height="8" rx="1"/>'
         '<circle cx="32" cy="6" r="5"/><circle cx="32" cy="58" r="5"/><circle cx="6" cy="32" r="5"/><circle cx="58" cy="32" r="5"/>'
         '<circle cx="18" cy="18" r="3.2"/><circle cx="46" cy="18" r="3.2"/><circle cx="18" cy="46" r="3.2"/><circle cx="46" cy="46" r="3.2"/>'
         '<rect x="26" y="26" width="12" height="12" transform="rotate(45 32 32)"/></g>'
         '<rect x="29.5" y="29.5" width="5" height="5" transform="rotate(45 32 32)" fill="var(--navy)"/></svg>')


def header(current, p):
    links = "".join(
        f'<a href="{p}{href(s)}"{" aria-current=page" if s == current else ""}>{t(label(s)["am"], label(s)["en"])}</a>'
        for s in SITE["nav"])
    return f'''<a class="skip" href="#main">{t("ወደ ዋናው ይዘት ይዝለሉ", "Skip to content")}</a>
<header class="site-header">
  <div class="wrap bar">
    <a class="brand" href="{p}./"><span class="brand-am">ባሕረ ቀመር</span><span class="brand-en">BAHREKEMER</span></a>
    <nav id="nav" class="nav" aria-label="Main">{links}</nav>
    <button class="lang-btn" type="button" data-lang-toggle>
      <span class="show-am" aria-label="Switch to English">EN</span><span class="show-en" aria-label="ወደ አማርኛ ይቀይሩ">አማ</span>
    </button>
    <button class="menu-btn" type="button" aria-expanded="false" aria-controls="nav">
      <span class="menu-icon" aria-hidden="true"></span>{t("ማውጫ", "Menu", cls="sr-only")}
    </button>
  </div>
</header>'''


def footer(p):
    links = "".join(f'<a href="{p}{href(s)}">{t(label(s)["am"], label(s)["en"])}</a>' for s in SITE["nav"])
    return f'''<footer class="site-footer">
  <div class="wrap">
    {CROSS}
    <p class="foot-name">ባሕረ ቀመር</p>
    <p class="foot-tag">{t("በነፃ ባህሉን ያውቅ ዘንድ ዌብሳይቱን በኢትዮጵያዊነቱ ለሚያምን ያስተላልፉ።",
                         "Share this site freely with all who cherish their Ethiopian heritage.")}</p>
    <div class="ornament" aria-hidden="true"><span></span></div>
    <nav class="foot-nav" aria-label="Footer">{links}</nav>
    <p class="copy">© {SITE["since"]}–{date.today().year} {SITE["author"]}. {t("መብቱ በሕግ የተጠበቀ ነው።", "All rights reserved.")}</p>
  </div>
</footer>'''


def page_hero(slug):
    pg = SITE["pages"][slug]
    l = pg.get("heading", label(slug))
    d = pg.get("lede", pg["description"])
    n = section_no(slug)
    sec = label(slug)
    eyebrow = t(f"ክፍል {n}" if n else "ባሕረ ቀመር", f"Section {n} · {sec['am']}" if n else "Bahrekemer")
    return f'''<header class="page-hero">
  <div class="wrap">
    <p class="eyebrow">{eyebrow}</p>
    <h1>{t(l["am"], l["en"])}</h1>
    <p class="lede">{t(d["am"], d["en"])}</p>
    <div class="ornament" aria-hidden="true"><span></span></div>
  </div>
</header>'''


def section_cards():
    out = []
    for i, s in enumerate(SITE["sections"], 1):
        l, d = label(s), SITE["pages"][s]["description"]
        feature = " card-feature" if i == 1 else ""
        start = t("ከዚህ ይጀምሩ", "Start here", cls="card-start") if i == 1 else ""
        out.append(f'''<a class="card{feature}" href="{href(s)}">
      <span class="card-no" aria-hidden="true">{GEEZ[i]}</span>
      <span class="card-body">
        {start}<span class="card-am always" lang="am">{l["am"]}</span>
        <span class="card-title" lang="en">{l["en"]}</span>
        <span class="card-desc">{t(d["am"], d["en"])}</span>
      </span>
      <span class="card-arrow" aria-hidden="true">→</span>
    </a>''')
    return '<div class="cards">\n    ' + "\n    ".join(out) + "\n  </div>"


def jsonld(slug, url):
    if slug != "index":
        return ""
    data = {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "WebSite", "name": "ባሕረ ቀመር", "alternateName": "Bahrekemer", "url": url,
             "inLanguage": ["am", "en"]},
            {"@type": "Person", "name": SITE["author"], "alternateName": "Bahrekemer", "url": url,
             "jobTitle": "Historian, author and artist",
             "email": "mailto:yigeme.yg7@gmail.com", "telephone": "+251913547463",
             "address": {"@type": "PostalAddress", "postOfficeBoxNumber": "25458/1000",
                         "addressLocality": "Addis Ababa", "addressCountry": "ET"},
             "knowsAbout": ["Ethiopian Orthodox Tewahedo tradition", "Qene", "Geez", "Ethiopian painting",
                            "Bahire Hasab", "Ethiopian history"]},
        ],
    }
    return f'<script type="application/ld+json">{json.dumps(data, ensure_ascii=False)}</script>\n'


def render(slug, body, p=""):
    pg = SITE["pages"].get(slug, SITE["pages"]["index"])
    base = SITE["url"].rstrip("/")
    url = base + "/" if slug in ("index", "404") else f"{base}/{slug}/"
    if "title" in pg:
        ta, te = pg["title"]["am"], pg["title"]["en"]
    else:
        ta, te = f'{pg["label"]["am"]} · ባሕረ ቀመር', f'{pg["label"]["en"]} · Bahrekemer'
    if slug == "404":
        ta, te = "ገጹ አልተገኘም · ባሕረ ቀመር", "Page not found · Bahrekemer"
    desc = f'{pg["description"]["am"]} {pg["description"]["en"]}'
    og = f'{base}/{SITE["og_image"]}'
    has_og = os.path.exists(os.path.join(ROOT, SITE["og_image"]))
    fonts = "".join(f'<link rel="preload" href="{p}assets/fonts/{f}" as="font" type="font/woff2" crossorigin>\n'
                    for f in ["noto-serif-ethiopic-ethiopic-400-normal.woff2", "eb-garamond-latin-400-normal.woff2"])
    seo = "" if slug == "404" else f'''<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="am" href="{url}">
<link rel="alternate" hreflang="en" href="{url}?lang=en">
<link rel="alternate" hreflang="x-default" href="{url}">
'''
    return f'''<!doctype html>
<html lang="am" data-lang="am" data-title-am="{esc(ta)}" data-title-en="{esc(te)}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<script>(function(){{var l="am";try{{l=new URLSearchParams(location.search).get("lang")||localStorage.getItem("lang")||"am"}}catch(e){{}}if(l!=="en")l="am";var d=document.documentElement;d.className+=" js";d.setAttribute("data-lang",l);d.lang=l;if(l==="en")document.title=d.getAttribute("data-title-en")}})();</script>
<title>{esc(ta)}</title>
<meta name="description" content="{esc(desc)}">
{seo}<meta property="og:type" content="website">
<meta property="og:site_name" content="ባሕረ ቀመር · Bahrekemer">
<meta property="og:title" content="{esc(ta)} | {esc(te)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:locale" content="am_ET">
<meta property="og:locale:alternate" content="en_US">
{f'<meta property="og:image" content="{og}">' + chr(10) + '<meta name="twitter:card" content="summary_large_image">' + chr(10) if has_og else ""}<meta name="theme-color" content="#1c2f5a">
<link rel="icon" href="{p}assets/img/favicon.svg" type="image/svg+xml">
{fonts}<link rel="stylesheet" href="{p}assets/css/style.css">
{jsonld(slug, url)}</head>
<body class="page-{slug}">
{header(slug, p)}
<main id="main">
{body}
</main>
{footer(p)}
<script src="{p}assets/js/main.js" defer></script>
</body>
</html>
'''


def build():
    written = []
    for slug in SITE["pages"]:
        src = os.path.join(ROOT, "content", f"{slug}.html")
        body = open(src, encoding="utf-8").read() if os.path.exists(src) else ""
        body = body.replace("<!--SECTIONS-->", section_cards())
        if slug != "index":
            body = page_hero(slug) + '\n<div class="page-body wrap">\n' + body + "\n</div>"
        out = "index.html" if slug == "index" else f"{slug}/index.html"
        os.makedirs(os.path.dirname(os.path.join(ROOT, out)), exist_ok=True)
        open(os.path.join(ROOT, out), "w", encoding="utf-8").write(render(slug, body, p="" if slug == "index" else "../"))
        written.append(out)

    nf = f'''<section class="page-hero"><div class="wrap">
  <p class="eyebrow">404</p>
  <h1>{t("ገጹ አልተገኘም", "Page not found")}</h1>
  <p class="lede">{t("የፈለጉት ገጽ የለም ወይም ተዛውሯል።", "The page you were looking for doesn’t exist or has moved.")}</p>
  <p><a class="text-link" href="/">{t("ወደ መነሻ ገጽ ይመለሱ →", "Return to the home page →")}</a></p>
</div></section>'''
    open(os.path.join(ROOT, "404.html"), "w", encoding="utf-8").write(render("404", nf, p="/"))
    written.append("404.html")

    base = SITE["url"].rstrip("/")
    today = date.today().isoformat()
    urls = []
    for slug in SITE["pages"]:
        loc = base + "/" if slug == "index" else f"{base}/{slug}/"
        urls.append(f'''  <url><loc>{loc}</loc><lastmod>{today}</lastmod>
    <xhtml:link rel="alternate" hreflang="am" href="{loc}"/>
    <xhtml:link rel="alternate" hreflang="en" href="{loc}?lang=en"/>
  </url>''')
    open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8").write(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
        + "\n".join(urls) + "\n</urlset>\n")
    open(os.path.join(ROOT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nDisallow: /content/\nSitemap: {base}/sitemap.xml\n")
    print("Built:", ", ".join(written), "+ sitemap.xml, robots.txt")


if __name__ == "__main__":
    build()
