#!/usr/bin/env python3
"""The "መጻሕፍትና ሥዕሎች" Doc — one section per book and per painting — and content/books.json, content/paintings.json.

  python3 sync/catalog.py doc-html              HTML to create the Doc from the site's data
  python3 sync/catalog.py diff FILE             compare the Doc (FILE = its text from read_file_content) with the site

Each item in the Doc is a Heading 2 (the Amharic title), its photo, then "label፡ value" lines, then any
free paragraphs about it, and a last line "(መለያ፡ <slug> — አይቀየር)" that ties it to the site.
"""
import json, os, re, sys, html

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from blocks import doc_blocks, norm  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://bahrekemer.com"
BOOKS_F = os.path.join(ROOT, "content", "books.json")
PAINT_F = os.path.join(ROOT, "content", "paintings.json")
YES = "አዎ"

# label in the Doc -> (field, getter)
BOOK_FIELDS = [
    ("ንዑስ ርእስ", "sub", lambda b: b.get("sub", {}).get("am", "")),
    ("ዓመት (ዓ.ም.)", "year", lambda b: b.get("year", "")),
    ("ገጽ", "pages", lambda b: b.get("pages", "")),
    ("ማተሚያ ቤት", "publisher", lambda b: b.get("publisher", {}).get("am", "")),
    ("ዋጋ (ብር)", "price", lambda b: b.get("price", "")),
    ("ተሸጦ አልቋል", "sold_out", lambda b: YES if b.get("sold_out") else ""),
    ("አዲሱ መጽሐፍ", "newest", lambda b: YES if b.get("newest") else ""),
    ("መሪ ቃል", "motto", lambda b: b.get("motto", {}).get("am", "")),
]
PAINT_FIELDS = [
    ("ዓመት", "year", lambda p: p.get("year", "")),
    ("ቅብ", "medium", lambda p: (p.get("medium") or {}).get("am", "")),
]
ABOUT = {"books": "ስለ መጽሐፉ", "paintings": "ስለ ሥዕሉ"}
SECTION = {"books": "መጻሕፍት", "paintings": "ሥዕሎች"}


def load():
    return (json.load(open(BOOKS_F, encoding="utf-8")), json.load(open(PAINT_F, encoding="utf-8")))


def about_paras(item):
    a = item.get("about", {}).get("am", "")
    return [x for x in a.split("\n") if x.strip()]


# ---------------------------------------------------------------- create
def doc_html():
    books, paintings = load()
    e = html.escape
    out = ["<html><body>",
           "<p>እያንዳንዱ መጽሐፍና ሥዕል ከታች ራሱን የቻለ ክፍል አለው። ከ«፡» በኋላ ያለውን ብቻ ይቀይሩ። "
           "«ስለ መጽሐፉ» ወይም «ስለ ሥዕሉ» ከሚለው በታች የፈለጉትን ያህል መጻፍ ይቻላል። "
           "የመጨረሻውን «መለያ» መስመር አይቀይሩ።</p>"]
    for kind, items, fields, folder in (("books", books, BOOK_FIELDS, "books"), ("paintings", paintings, PAINT_FIELDS, "paintings")):
        out.append(f"<h1>{SECTION[kind]}</h1>")
        for it in items:
            out.append(f"<h2>{e(it['title']['am'])}</h2>")
            img = (it["faces"][0]["img"] if kind == "books" and it.get("faces") else (it["slug"] if kind == "paintings" else None))
            if img:
                out.append(f'<p><img src="{BASE}/assets/img/{folder}/{img}-sm.jpg" width="160"></p>')
            for label, _, get in fields:
                out.append(f"<p>{label}፡ {e(get(it))}</p>")
            out.append(f"<p>{ABOUT[kind]}፡</p>")
            for para in about_paras(it):
                out.append(f"<p>{e(para)}</p>")
            out.append(f'<p><span style="color:#999999;font-size:9pt">(መለያ፡ {it["slug"]} — አይቀየር)</span></p>')
    out.append("</body></html>")
    return "".join(out)


# ---------------------------------------------------------------- read back
LABEL_RE = re.compile(r"^(.+?)\s*[፡:]\s*(.*)$")
ID_RE = re.compile(r"\(?\s*መለያ\s*[፡:]\s*([a-z0-9-]+)")


def parse(text):
    """{"books": [item], "paintings": [item]} — item = {"title", "fields": {label: value}, "about": [paras], "id"}"""
    lines = [l for l in text.split("\n") if not re.match(r"^\s*!\[", l) and not re.match(r"^\s*\[image\d+\]:", l)]
    out = {"books": [], "paintings": []}
    kind, item, in_about = None, None, False
    for k, t in doc_blocks("\n".join(lines)):
        if k == "h1":
            kind = next((x for x, name in SECTION.items() if name in t), None)
            item = None
            continue
        if kind is None:
            continue
        if k in ("h2", "h3"):
            item = {"title": t, "fields": {}, "about": [], "id": None}
            out[kind].append(item)
            in_about = False
            continue
        if item is None or not t:
            continue
        m = ID_RE.search(t)
        if m:
            item["id"] = m.group(1)
            in_about = False
            continue
        labels = [l for l, _, _ in (BOOK_FIELDS if kind == "books" else PAINT_FIELDS)]
        m = LABEL_RE.match(t)
        if m and m.group(1).strip() == ABOUT[kind]:
            in_about = True
            if m.group(2).strip():
                item["about"].append(m.group(2).strip())
            continue
        if m and m.group(1).strip() in labels and not in_about:
            item["fields"][m.group(1).strip()] = m.group(2).strip()
            continue
        if in_about:
            item["about"].append(t)
    return out


def diff(text):
    books, paintings = load()
    doc = parse(text)
    res = {}
    for kind, items, fields in (("books", books, BOOK_FIELDS), ("paintings", paintings, PAINT_FIELDS)):
        by = {i["slug"]: i for i in items}
        seen, changed, new = [], [], []
        for d in doc[kind]:
            if not d["id"] or d["id"] not in by:
                new.append(d)
                continue
            seen.append(d["id"])
            site = by[d["id"]]
            ch = {}
            if norm(d["title"]) != norm(site["title"]["am"]):
                ch["ርእስ"] = {"site": site["title"]["am"], "doc": d["title"]}
            for label, field, get in fields:
                if label in d["fields"] and norm(d["fields"][label]) != norm(get(site)):
                    ch[label] = {"site": get(site), "doc": d["fields"][label], "field": field}
            if [norm(x) for x in d["about"]] != [norm(x) for x in about_paras(site)]:
                ch[ABOUT[kind]] = {"site": about_paras(site), "doc": d["about"], "field": "about"}
            if ch:
                changed.append({"id": d["id"], "changes": ch})
        order_doc = [i for i in seen]
        order_site = [i["slug"] for i in items if i["slug"] in seen]
        res[kind] = {"changed": changed, "new_items": new,
                     "missing_from_doc": [s for s in by if s not in seen],
                     "order_changed": order_doc != order_site, "doc_order": order_doc}
    return res


if __name__ == "__main__":
    if sys.argv[1] == "doc-html":
        print(doc_html())
    elif sys.argv[1] == "diff":
        txt = open(sys.argv[2], encoding="utf-8").read()
        try:
            txt = json.loads(txt)["fileContent"]
        except Exception:
            pass
        print(json.dumps(diff(txt), ensure_ascii=False, indent=1))
