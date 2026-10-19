#!/usr/bin/env python3
"""Builds the site from site.json + content/ into static HTML.

    python3 build.py

No dependencies. What you edit:
  content/<page>.html          the body of each section page (Introduction, Numbers, Key, ...)
  content/index.html           the home page template (the <!--TOKENS--> are filled in here)
  content/writings.json        the list of writings, NEWEST FIRST — the home page fills itself from it
  content/writings/<slug>.html the text of each writing (Amharic in lang="am", English in lang="en")
  site.json                    page titles, descriptions, nav order

To publish a new poem or article: write content/writings/<new-slug>.html (copy an existing one),
add an entry at the TOP of content/writings.json, run this script, commit and push.
"""
import json, os, re, html
from datetime import date

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = json.load(open(os.path.join(ROOT, "site.json"), encoding="utf-8"))
WRITINGS = json.load(open(os.path.join(ROOT, "content", "writings.json"), encoding="utf-8"))
GEEZ = ["", "፩", "፪", "፫", "፬", "፭", "፮", "፯", "፰", "፱", "፲"]
KINDS = {"essay": ("ድርሰት", "Essay"), "poem": ("ግጥም", "Poem")}
AUTHOR_AM = "ይትባረክ ገሠሠ መራ"


def t(am, en, tag="span", cls=""):
    """Bilingual pair. Amharic always shows; English joins it in English mode."""
    c = f' class="{cls}"' if cls else ""
    return f'<{tag} lang="am"{c}>{am}</{tag}><{tag} lang="en"{c}>{en}</{tag}>'


def lx(am, en, tag="p", cls=""):
    """Language-exclusive pair: only the current site language shows (used for excerpts)."""
    c = f"lx {cls}".strip()
    return f'<{tag} lang="am" class="{c}">{am}</{tag}><{tag} lang="en" class="{c}">{en}</{tag}>'


def esc(s):
    return html.escape(s, quote=True)


def strip_tags(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s))


def href(slug):
    return "./" if slug == "index" else f"{slug}/"


def label(slug):
    return SITE["pages"][slug]["label"]


def section_no(slug):
    return GEEZ[SITE["sections"].index(slug) + 1] if slug in SITE["sections"] else ""


# ---------------------------------------------------------------- writings
def writing_body(w):
    return open(os.path.join(ROOT, "content", "writings", f'{w["slug"]}.html'), encoding="utf-8").read()


def excerpt(w, lang, limit):
    body = writing_body(w)
    if w["kind"] == "poem":
        m = re.search(rf'<div class="verse"[^>]*lang="{lang}"[^>]*>(.*?)</div>', body, re.S)
        lines = [l.strip() for l in strip_tags(m.group(1)).split("\n") if l.strip()][:2] if m else []
        return "<br>".join(esc(l) for l in lines)
    m = re.search(rf'<div lang="{lang}">(.*?)</div>', body, re.S)
    p = re.search(r"<p[^>]*>(.*?)</p>", m.group(1), re.S) if m else None
    text = re.sub(r"\s+", " ", strip_tags(p.group(1))).strip() if p else ""
    ends = ["፡፡", "።"] if lang == "am" else [". ", "? "]
    cut = min([i + len(e) for e in ends for i in [text.find(e, 40)] if i != -1] or [len(text)])
    text = text[:cut].strip()
    if len(text) > limit:
        text = text[:limit].rsplit(" ", 1)[0] + " …"
    return esc(text)


def opening(w, lang, paras=2, lines=8):
    """The first paragraphs (or verse lines) of a writing, for the front-page lead."""
    body = writing_body(w)
    if w["kind"] == "poem":
        m = re.search(rf'<div class="verse"[^>]*lang="{lang}"[^>]*>(.*?)</div>', body, re.S)
        ls = [l.strip() for l in strip_tags(m.group(1)).split("\n") if l.strip()][:lines] if m else []
        return '<p class="lead-verse">' + "<br>".join(esc(l) for l in ls) + "</p>"
    m = re.search(rf'<div lang="{lang}">(.*?)</div>', body, re.S)
    ps = re.findall(r"<p(?![^>]*class=\"continued)[^>]*>(.*?)</p>", m.group(1), re.S)[:paras] if m else []
    clean = [esc(re.sub(r"\s+", " ", strip_tags(p)).strip()) for p in ps]
    return "".join("<p>" + c + "</p>" for c in clean)


def source(w):
    m = re.search(r'<p class="cite"><span lang="am">(.*?)</span><span lang="en">(.*?)</span></p>', writing_body(w), re.S)
    return m.groups() if m else None


def kicker(w):
    am, en = KINDS.get(w["kind"], KINDS["essay"])
    if w.get("continuing"):
        am, en = am + " ፡ ይቀጥላል", en + " · Continuing"
    return t(am, en)


def w_href(w, p=""):
    return f'{p}writings/{w["slug"]}/'


# ---------------------------------------------------------------- chrome
def nav_links(current, p):
    return "".join(
        f'<a href="{p}{href(s)}"{" aria-current=page" if s == current else ""}>'
        f'<span class="n-am">{label(s)["am"]}</span><span class="n-en">{label(s)["en"]}</span></a>'
        for s in SITE["nav"])


GROUPS = [  # phone home page: five groups instead of eight items
    ("writings/", "ጽሑፎች", "Writings"),
    ("megbiya/", "ባሕረ ቀመር", "Bahre Kemer"),
    ("qene/", "ቅኔና ግጥም", "Qene & Poetry"),
    ("books/", "መጻሕፍትና ሥዕሎች", "Books & Paintings"),
    ("contact/", "ያግኙን", "Contact"),
]


def group_links(p):
    return "".join(f'<a href="{p}{h}"><span class="n-am">{am}</span><span class="n-en">{en}</span></a>' for h, am, en in GROUPS)


MENU_BTN = ('<button class="menu-btn" type="button" aria-expanded="false" aria-controls="nav">'
            '<span class="menu-icon" aria-hidden="true"></span>'
            '<span class="menu-label">ክፍሎች <span class="menu-en">Sections</span></span></button>')


def header(current, p):
    util = f'''<a class="skip" href="#main">ወደ ዋናው ይዘት ይዝለሉ · Skip to content</a>
<div class="util">
  <div class="wrap util-bar">
    <p class="today" data-today></p>
    <div class="util-ctl">
      <button type="button" class="size-btn" data-size-toggle aria-pressed="false" aria-label="ፊደል አሳድግ · Larger text"><span class="s1" aria-hidden="true">ሀ</span><span class="s2" aria-hidden="true">ሀ</span><span class="s-mob" aria-hidden="true">ሀ+ ፊደል</span></button>
      <div class="lang-switch" role="group" aria-label="ቋንቋ · Language">
        <button type="button" class="ls ls-am" data-set-lang="am">አማርኛ</button>
        <button type="button" class="ls ls-en" data-set-lang="en">English</button>
      </div>
    </div>
  </div>
</div>'''
    if current == "index":
        return util + f'''
<header class="masthead">
  <div class="wrap">
    <a class="mast-title" href="{p}./">
      <span class="mast-am">ባሕረ ቀመር</span>
      <span class="mast-sub">Bahrekemer · The works of Memhir Yitbarek Gessese Merra</span>
    </a>
    <div class="mast-id m-only">
      <p class="mast-who blk">{t("የታሪክ ምሁርና ሠዓሊ ይትባረክ ገሠሠ መራ ሥራዎች", "The works of historian and painter Yitbarek Gessese Merra")}</p>
      <p class="mast-what">{t("ታሪክ ፡ ቅኔ ፡ ሥዕል ፡ የባሕረ ቀመር ቁጥር", "History · Qene · Painting · The Bahre Kemer numbers")}</p>
    </div>
    <nav class="m-nav m-only" aria-label="ዋና ክፍሎች · Main sections">{group_links(p)}</nav>
    <div class="navrow">
      <nav id="nav" class="nav" aria-label="Main">{nav_links(current, p)}</nav>
      {MENU_BTN}
    </div>
  </div>
</header>'''
    return util + f'''
<header class="topbar">
  <div class="wrap bar">
    <a class="brand" href="{p}./">ባሕረ ቀመር</a>
    <nav id="nav" class="nav" aria-label="Main">{nav_links(current, p)}</nav>
    {MENU_BTN}
  </div>
</header>'''


def footer(p):
    links = "".join(f'<a href="{p}{href(s)}"><span class="n-am">{label(s)["am"]}</span> <span class="n-en">{label(s)["en"]}</span></a>'
                    for s in SITE["nav"])
    return f'''<footer class="site-footer">
  <div class="wrap foot-grid">
    <div class="foot-id">
      <p class="foot-name">ባሕረ ቀመር</p>
      <p class="foot-tag blk">{t("በነፃ ባህሉን ያውቅ ዘንድ ዌብሳይቱን በኢትዮጵያዊነቱ ለሚያምን ያስተላልፉ።",
                             "Share this site freely with all who cherish their Ethiopian heritage.")}</p>
    </div>
    <nav class="foot-nav" aria-label="Footer">{links}</nav>
    <div class="foot-contact">
      <p class="label">{t("ያግኙን", "Contact")}</p>
      <a href="mailto:yigeme.yg7@gmail.com">yigeme.yg7@gmail.com</a>
      <span>+251 913 547 463</span>
      <span>{t("ፖ.ሣ.ቁ. 25458/1000 ፡ አዲስ አበባ", "P.O. Box 25458/1000, Addis Ababa")}</span>
    </div>
  </div>
  <div class="wrap copy">© {SITE["since"]}–{date.today().year} {SITE["author"]}</div>
</footer>'''


READER = ('<div class="reader" role="group" aria-label="የንባብ ቋንቋ · Reading language">'
          '<button type="button" data-read-set="am">አማርኛ</button>'
          '<button type="button" data-read-set="both">ጎን ለጎን<span class="rb-en"> · Side by side</span></button>'
          '<button type="button" data-read-set="en">English</button></div>')


def page_hero(slug):
    pg = SITE["pages"][slug]
    l = pg.get("heading", label(slug))
    d = pg.get("lede", pg["description"])
    n = section_no(slug)
    num = SITE["sections"].index(slug) + 1 if n else 0
    kick = f'<p class="kicker">{t(f"ክፍል {n}", f"Part {num}")}</p>' if n else ""
    return f'''<header class="page-hero">
  <div class="wrap">
    {kick}
    <h1>{t(l["am"], l["en"])}</h1>
    <p class="lede blk">{t(d["am"], d["en"])}</p>
  </div>
</header>'''


# ---------------------------------------------------------------- home
def home_front(p=""):
    lead, side, more = WRITINGS[0], WRITINGS[1:4], WRITINGS[4:8]
    lead_html = f'''<article class="lead">
      <p class="kicker d-only">{kicker(lead)}</p>
      <p class="kicker m-only">{t("አዲሱ ጽሑፍ", "Latest")}</p>
      <h1 class="lead-title"><a href="{w_href(lead, p)}">{t(lead["title"]["am"], lead["title"]["en"])}</a></h1>
      {lx(opening(lead, "am"), opening(lead, "en"), tag="div", cls="dek")}
      <div class="byline-row">
        <p class="byline">{t(AUTHOR_AM, "By " + SITE["author"])}</p>
        <a class="more-link" href="{w_href(lead, p)}">{t("ሙሉውን ያንብቡ →", "Read in full →")}</a>
      </div>
    </article>'''
    side_html = "".join(f'''<article class="side-item">
        <p class="kicker">{kicker(w)}</p>
        <h3><a href="{w_href(w, p)}">{t(w["title"]["am"], w["title"]["en"])}</a></h3>
        {lx(excerpt(w, "am", 120), excerpt(w, "en", 120), cls="side-ex")}
      </article>''' for w in side)
    more_html = "".join(f'''<article class="more-item">
        <p class="kicker">{kicker(w)}</p>
        <h3><a href="{w_href(w, p)}">{t(w["title"]["am"], w["title"]["en"])}</a></h3>
      </article>''' for w in more)
    return lead_html, side_html, more_html


def earlier_list(p=""):
    rows = ""
    for w in WRITINGS[1:6]:
        kam, ken = KINDS.get(w["kind"], KINDS["essay"])
        rows += (f'<li><a href="{w_href(w, p)}"><span class="e-title blk">{t(w["title"]["am"], w["title"]["en"])}</span>'
                 f'<span class="e-kind">{t(kam, ken)}</span></a></li>')
    return f'<ul class="earlier">{rows}</ul>'


def contents_list():
    rows = []
    for i, s in enumerate(SITE["nav"], 1):
        d = SITE["pages"][s]["description"]
        rows.append(f'''<li><a href="{href(s)}">
        <span class="c-no" aria-hidden="true">{GEEZ[i]}</span>
        <span class="c-body"><span class="c-title blk">{t(label(s)["am"], label(s)["en"])}</span>
        {lx(d["am"], d["en"], tag="span", cls="c-desc")}</span>
        <span class="c-arrow" aria-hidden="true">→</span></a></li>''')
    return '<ol class="contents">' + "".join(rows) + "</ol>"


def build_home():
    tpl = open(os.path.join(ROOT, "content", "index.html"), encoding="utf-8").read()
    lead, side, more = home_front()
    portrait = os.path.join(ROOT, "assets", "img", "author.jpg")
    pic = ('<figure class="profile-pic"><img src="assets/img/author.jpg" alt="Yitbarek Gessese Merra" '
           'width="600" height="750" loading="lazy"></figure>') if os.path.exists(portrait) else ""
    return (tpl.replace("<!--LEAD-->", lead).replace("<!--SIDE-->", side).replace("<!--MORE-->", more)
               .replace("<!--CONTENTS-->", contents_list()).replace("<!--EARLIER-->", earlier_list()).replace("<!--PORTRAIT-->", pic))


# ---------------------------------------------------------------- writing pages
def writing_page(i, w):
    p = "../../"
    src = source(w)
    by = f'<p class="byline">{t(AUTHOR_AM, "By " + SITE["author"])}</p>'
    if src:
        by += f'<p class="source blk">{t(src[0], src[1])}</p>'
    newer = WRITINGS[i - 1] if i > 0 else None
    older = WRITINGS[i + 1] if i + 1 < len(WRITINGS) else None

    def nav_item(w2, cls, am, en):
        if not w2:
            return "<span></span>"
        return (f'<a class="{cls}" href="{w_href(w2, p)}"><span class="label">{t(am, en)}</span>'
                f'<span class="pn-title blk">{t(w2["title"]["am"], w2["title"]["en"])}</span></a>')
    body = writing_body(w)
    body = re.sub(r'<p class="cite">.*?</p>\s*', "", body, flags=re.S)  # shown in the byline instead
    return f'''<header class="page-hero article-hero">
  <div class="wrap">
    <p class="kicker">{kicker(w)}</p>
    <h1>{t(w["title"]["am"], w["title"]["en"])}</h1>
    <div class="byline-box">{by}</div>
  </div>
</header>
<div class="page-body wrap">
{READER}
<article class="prose article{" poem-article" if w["kind"] == "poem" else ""}">
{body}
</article>
<p class="end-mark" aria-hidden="true">፨</p>
<nav class="prevnext" aria-label="ተጨማሪ ጽሑፎች · More writings">
  {nav_item(older, "pn-prev", "← የቀደመው", "← Earlier")}
  {nav_item(newer, "pn-next", "አዲሱ →", "Newer →")}
</nav>
<p class="all-link"><a class="more-link" href="{p}writings/">{t("ሁሉም ጽሑፎች", "All writings")}</a></p>
</div>'''


def writings_index():
    items = "".join(f'''<li><a href="{w["slug"]}/">
      <span class="kicker">{kicker(w)}</span>
      <span class="wi-title blk">{t(w["title"]["am"], w["title"]["en"])}</span>
      {lx(excerpt(w, "am", 200), excerpt(w, "en", 200), tag="span", cls="wi-ex")}
    </a></li>''' for w in WRITINGS)
    return page_hero("writings") + f'\n<div class="page-body wrap">\n<ol class="writings-list">{items}</ol>\n</div>'


# ---------------------------------------------------------------- page shell
def jsonld(slug, url):
    if slug != "index":
        return ""
    data = {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "WebSite", "name": "ባሕረ ቀመር", "alternateName": "Bahrekemer", "url": url,
             "inLanguage": ["am", "en"]},
            {"@type": "Person", "name": SITE["author"], "alternateName": AUTHOR_AM, "url": url,
             "jobTitle": "Historian, author and artist",
             "email": "mailto:yigeme.yg7@gmail.com", "telephone": "+251913547463",
             "address": {"@type": "PostalAddress", "postOfficeBoxNumber": "25458/1000",
                         "addressLocality": "Addis Ababa", "addressCountry": "ET"},
             "knowsAbout": ["Ethiopian Orthodox Tewahedo tradition", "Qene", "Geez", "Ethiopian painting",
                            "Bahire Hasab", "Ethiopian history"]},
        ],
    }
    return f'<script type="application/ld+json">{json.dumps(data, ensure_ascii=False)}</script>\n'


BOOT = ('(function(){var d=document.documentElement,l="am",r,b;try{var q=new URLSearchParams(location.search);'
        'l=q.get("lang")||localStorage.getItem("lang")||"am";r=localStorage.getItem("read");b=localStorage.getItem("big")}catch(e){}'
        'if(l!=="en")l="am";if(["am","both","en"].indexOf(r)<0)r=l==="en"?"both":"am";'
        'd.className+=" js"+(b==="1"?" big":"");d.setAttribute("data-lang",l);d.setAttribute("data-read",r);d.lang=l;'
        'if(l==="en")document.title=d.getAttribute("data-title-en")})();')


def render(slug, body, p="", title=None, desc=None, url_path=None, reader=False):
    pg = SITE["pages"].get(slug, SITE["pages"]["index"])
    base = SITE["url"].rstrip("/")
    if url_path is None:
        url_path = "/" if slug in ("index", "404") else f"/{slug}/"
    url = base + url_path
    if title:
        ta, te = title
    elif "title" in pg:
        ta, te = pg["title"]["am"], pg["title"]["en"]
    else:
        ta, te = f'{pg["label"]["am"]} · ባሕረ ቀመር', f'{pg["label"]["en"]} · Bahrekemer'
    if slug == "404":
        ta, te = "ገጹ አልተገኘም · ባሕረ ቀመር", "Page not found · Bahrekemer"
    desc = desc or f'{pg["description"]["am"]} {pg["description"]["en"]}'
    og = f'{base}/{SITE["og_image"]}'
    has_og = os.path.exists(os.path.join(ROOT, SITE["og_image"]))
    is_article = url_path.startswith("/writings/") and url_path != "/writings/"
    fonts = "".join(f'<link rel="preload" href="{p}assets/fonts/{f}" as="font" type="font/woff2" crossorigin>\n'
                    for f in ["noto-serif-ethiopic-ethiopic-700-normal.woff2", "noto-serif-ethiopic-ethiopic-400-normal.woff2"])
    seo = "" if slug == "404" else f'''<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="am" href="{url}">
<link rel="alternate" hreflang="en" href="{url}?lang=en">
<link rel="alternate" hreflang="x-default" href="{url}">
'''
    ogimg = (f'<meta property="og:image" content="{og}">\n<meta name="twitter:card" content="summary_large_image">\n'
             if has_og else "")
    return f'''<!doctype html>
<html lang="am" data-lang="am" data-read="am" data-title-am="{esc(ta)}" data-title-en="{esc(te)}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<script>{BOOT}</script>
<title>{esc(ta)}</title>
<meta name="description" content="{esc(desc)}">
{seo}<meta property="og:type" content="{"article" if is_article else "website"}">
<meta property="og:site_name" content="ባሕረ ቀመር · Bahrekemer">
<meta property="og:title" content="{esc(ta)} | {esc(te)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:locale" content="am_ET">
<meta property="og:locale:alternate" content="en_US">
{ogimg}<meta name="theme-color" content="#ffffff">
<link rel="icon" href="{p}assets/img/favicon.svg" type="image/svg+xml">
{fonts}<link rel="stylesheet" href="{p}assets/css/style.css">
{jsonld(slug, url)}</head>
<body class="page-{slug}{" is-reader" if reader else ""}{" is-article" if is_article else ""}">
{header(slug, p)}
<main id="main">
{body}
</main>
{footer(p)}
<script src="{p}assets/js/main.js" defer></script>
</body>
</html>
'''


def write(out, text):
    path = os.path.join(ROOT, out)
    os.makedirs(os.path.dirname(path) or ROOT, exist_ok=True)
    open(path, "w", encoding="utf-8").write(text)


def build():
    written = []
    readers = set(SITE.get("reader_pages", []))
    for slug in SITE["pages"]:
        if slug == "writings":
            continue
        if slug == "index":
            body = build_home()
        else:
            src = os.path.join(ROOT, "content", f"{slug}.html")
            body = open(src, encoding="utf-8").read() if os.path.exists(src) else ""
            reader = READER + "\n" if slug in readers else ""
            body = page_hero(slug) + f'\n<div class="page-body wrap">\n{reader}{body}\n</div>'
        out = "index.html" if slug == "index" else f"{slug}/index.html"
        write(out, render(slug, body, p="" if slug == "index" else "../", reader=slug in readers))
        written.append(out)

    write("writings/index.html", render("writings", writings_index(), p="../"))
    written.append("writings/index.html")
    for i, w in enumerate(WRITINGS):
        out = f'writings/{w["slug"]}/index.html'
        write(out, render("writings", writing_page(i, w), p="../../", reader=True,
                          title=(f'{w["title"]["am"]} · ባሕረ ቀመር', f'{w["title"]["en"]} · Bahrekemer'),
                          desc=f'{strip_tags(excerpt(w, "am", 150))} {strip_tags(excerpt(w, "en", 150))}',
                          url_path=f'/writings/{w["slug"]}/'))
        written.append(out)

    nf = f'''<section class="page-hero"><div class="wrap">
  <p class="kicker">404</p>
  <h1>{t("ገጹ አልተገኘም", "Page not found")}</h1>
  <p class="lede blk">{t("የፈለጉት ገጽ የለም ወይም ተዛውሯል።", "The page you were looking for doesn’t exist or has moved.")}</p>
  <p><a class="more-link" href="/">{t("ወደ መነሻ ገጽ ይመለሱ →", "Return to the home page →")}</a></p>
</div></section>'''
    write("404.html", render("404", nf, p="/"))
    written.append("404.html")

    base = SITE["url"].rstrip("/")
    today = date.today().isoformat()
    locs = [base + "/" if s == "index" else f"{base}/{s}/" for s in SITE["pages"]]
    locs += [f'{base}/writings/{w["slug"]}/' for w in WRITINGS]
    urls = [f'''  <url><loc>{loc}</loc><lastmod>{today}</lastmod>
    <xhtml:link rel="alternate" hreflang="am" href="{loc}"/>
    <xhtml:link rel="alternate" hreflang="en" href="{loc}?lang=en"/>
  </url>''' for loc in locs]
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n'
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
          + "\n".join(urls) + "\n</urlset>\n")
    write("robots.txt", f"User-agent: *\nAllow: /\nDisallow: /content/\nSitemap: {base}/sitemap.xml\n")
    print(f"Built {len(written)} pages + sitemap.xml, robots.txt")


if __name__ == "__main__":
    build()
