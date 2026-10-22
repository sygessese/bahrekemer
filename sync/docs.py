#!/usr/bin/env python3
"""The seven Google Docs Yitbarek edits, and how each one maps onto the site.

  python3 sync/docs.py list                      the Docs, their sections and the site page each section feeds
  python3 sync/docs.py doc-html DOC              HTML to create DOC from the site (Amharic only)
  python3 sync/docs.py diff DOC FILE             compare DOC with the site. FILE = the saved result of the Google Docs
                                                 read_doc tool (preferred) or of Drive read_file_content
  python3 sync/docs.py section DOC FILE N        print section N of DOC as Markdown (for a new essay or poem)

DOC is one of: essays poems qene books paintings numbers pages.

Every Doc is a short instruction paragraph, then numbered sections: a heading "፩ · title" and what belongs
under it. The number ties a section to its page on the site (sync/manifest.json -> docs.DOC.sections), so he
can change a title freely. A section whose number isn't in the manifest is new. Text before the first numbered
heading (the instructions) is ignored.
"""
import json, os, re, sys, html

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import blocks  # noqa: E402
from blocks import doc_blocks, norm, site_blocks  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST = os.path.join(ROOT, "sync", "manifest.json")
BASE = "https://bahrekemer.com"
YES = "አዎ"

# ---------------------------------------------------------------- Ge'ez numbers
ONES = "፩፪፫፬፭፮፯፰፱"
TENS = "፲፳፴፵፶፷፸፹፺"


def geez(n):
    if n >= 100:
        h, n = divmod(n, 100)
        return ("" if h == 1 else geez(h)) + "፻" + (geez(n) if n else "")
    t, o = divmod(n, 10)
    return (TENS[t - 1] if t else "") + (ONES[o - 1] if o else "")


def from_geez(s):
    s = s.strip()
    if s.isascii() and s.isdigit():
        return int(s)
    total, cur = 0, 0
    for ch in s:
        if ch in ONES:
            cur += ONES.index(ch) + 1
        elif ch in TENS:
            cur += 10 * (TENS.index(ch) + 1)
        elif ch == "፻":
            total += (cur or 1) * 100
            cur = 0
        else:
            return None
    return total + cur or None


NUM = r"([፩-፼]+|[0-9]+)"
HEAD_RE = re.compile(rf"^{NUM}\s*[·.\-—–:፡።]\s*(.+)$")


# ---------------------------------------------------------------- the seven Docs
def _w(kind):
    w = json.load(open(os.path.join(ROOT, "content", "writings.json"), encoding="utf-8"))
    return ["writings/" + x["slug"] for x in reversed(w) if x["kind"] == kind]  # oldest first


def _items(name):
    return [x["slug"] for x in json.load(open(os.path.join(ROOT, "content", f"{name}.json"), encoding="utf-8"))]


LABELS = {"index": "መነሻ ገጽ"}  # sections whose page has no title of its own

DOCS = {
    "essays": {"title": "፩ · ድርሰቶች", "kind": "pages", "new": "essay", "start": lambda: _w("essay"),
               "help": ["ይህ ሰነድ ሁሉንም ድርሰቶች ይዟል። እያንዳንዱ ድርሰት በቁጥርና በርእስ ይጀምራል።",
                        "ለማስተካከል፡ እንደ ማንኛውም ጽሑፍ ይጻፉ፣ ይሰርዙ ወይም ይቀይሩ። ማስቀመጥ አያስፈልግም፤ በራሱ ይቀመጣል።",
                        "አዲስ ድርሰት ለመጨመር፡ ወደ ሰነዱ መጨረሻ ይሂዱ፤ በአዲስ መስመር ቀጣዩን ቁጥርና ርእሱን ይጻፉ (ለምሳሌ «{next} · ርእስ»)፤ ከዚያ በታች ድርሰቱን ይጻፉ። አዲሱ ድርሰት በድረ ገጹ መነሻ ገጽ ላይ «አዲሱ» ሆኖ ይታያል።"]},
    "poems": {"title": "፪ · ግጥሞች", "kind": "pages", "new": "poem", "start": lambda: ["poetry"] + _w("poem"),
              "help": ["ይህ ሰነድ ግጥሞቹን ይዟል። ፩ኛው የ«ወቅታዊ ግጥም» ገጽ ነው።",
                       "ለማስተካከል፡ እንደ ማንኛውም ጽሑፍ ይጻፉ፣ ይሰርዙ ወይም ይቀይሩ። እያንዳንዱን የግጥም መስመር በ Enter ይለዩ።",
                       "አዲስ ግጥም ለመጨመር፡ ወደ ሰነዱ መጨረሻ ይሂዱ፤ በአዲስ መስመር ቀጣዩን ቁጥርና ርእሱን ይጻፉ (ለምሳሌ «{next} · ርእስ»)፤ ከዚያ በታች ግጥሙን ይጻፉ።"]},
    "qene": {"title": "፫ · ቅኔ", "kind": "pages", "new": None, "start": lambda: ["qene"],
             "help": ["ይህ ሰነድ የቅኔ ገጹን ይዟል። እንደ ማንኛውም ጽሑፍ ይጻፉ፣ ይሰርዙ ወይም ይቀይሩ።",
                      "አዲስ ቅኔ ለመጨመር፡ በሰነዱ መጨረሻ በአዲስ መስመር የቅኔውን ስም ይጻፉ (ለምሳሌ «… — 3ኛ ቅኔ»)፤ ከዚያ በታች ቅኔውን፣ ፍቺውንና ሒሣቡን ይጻፉ።"]},
    "books": {"title": "፬ · መጻሕፍት", "kind": "catalog", "new": "book", "start": lambda: _items("books"),
              "help": ["ይህ ሰነድ የእያንዳንዱን መጽሐፍ መረጃ ይዟል። ከ«፡» በኋላ ያለውን ብቻ ይቀይሩ።",
                       "መጽሐፍ ተሸጦ ካለቀ «ተሸጦ አልቋል፡» ከሚለው በኋላ «አዎ» ይጻፉ። ስለ መጽሐፉ የፈለጉትን ያህል «ስለ መጽሐፉ፡» ከሚለው በታች ይጻፉ።",
                       "አዲስ መጽሐፍ ለመጨመር፡ በሰነዱ መጨረሻ በአዲስ መስመር ቀጣዩን ቁጥርና ርእሱን ይጻፉ (ለምሳሌ «{next} · ርእስ»)፤ ከዚያ በታች የሚያውቁትን ይጻፉ። የሽፋኑን ፎቶ ለሰላም ይላኩ።"]},
    "paintings": {"title": "፭ · ሥዕሎች", "kind": "catalog", "new": "painting", "start": lambda: _items("paintings"),
                  "help": ["ይህ ሰነድ የእያንዳንዱን ሥዕል መረጃ ይዟል። ርእሱን፣ ዓመቱንና ቅቡን (ዘይት፣ አክሬሊክ…) ከ«፡» በኋላ ይጻፉ።",
                           "ስለ ሥዕሉ የፈለጉትን ያህል «ስለ ሥዕሉ፡» ከሚለው በታች ይጻፉ።",
                           "አዲስ ሥዕል ለመጨመር፡ በሰነዱ መጨረሻ በአዲስ መስመር ቀጣዩን ቁጥርና ርእሱን ይጻፉ (ለምሳሌ «{next} · ርእስ»)። የሥዕሉን ፎቶ ለሰላም ይላኩ።"]},
    "numbers": {"title": "፮ · ቁጥሮችና ቁልፍ", "kind": "pages", "new": None, "start": lambda: ["numbers", "key"],
                "help": ["ይህ ሰነድ የ«ቁጥሮች» እና የ«ቁልፍ» ገጾችን ይዟል። በሰንጠረዦቹ ውስጥ ያለውን ጽሑፍ መቀየር ይቻላል።",
                         "እባክዎ የሰንጠረዥ መስመርም ሆነ ዓምድ አይሰርዙ፤ መጨመር ካስፈለገ ለሰላም ይንገሩ።"]},
    "pages": {"title": "፯ · መግቢያና ሌሎች ገጾች", "kind": "pages", "new": None, "start": lambda: ["megbiya", "index", "books", "contact"],
              "help": ["ይህ ሰነድ መግቢያውን፣ የመነሻ ገጹን ጽሑፍ፣ የመጻሕፍት ገጹን ጽሑፍና የአድራሻ ገጹን ይዟል።",
                       "እንደ ማንኛውም ጽሑፍ ይጻፉ፣ ይሰርዙ ወይም ይቀይሩ። ማስቀመጥ አያስፈልግም።"]},
}
FOOT = ("ቁጥሮቹን (፩፣ ፪፣ ፫…) እባክዎ አይቀይሩ ወይም አይሰርዙ። ለውጦቹ በየሌሊቱ ተሰብስበው ወደ እንግሊዝኛ ይተረጎማሉ፤ "
        "ሰላም ካየቻቸው በኋላ ድረ ገጹ ላይ ይወጣሉ። ምንም ነገር ወዲያው አይለወጥም፤ የቀድሞው ሁሉ ተቀምጦ ይገኛል።")


def manifest():
    return json.load(open(MANIFEST, encoding="utf-8"))


def sections(name):
    """{number: key} from the manifest, or the starting layout if the Doc isn't there yet."""
    d = manifest().get("docs", {}).get(name)
    if d and d.get("sections"):
        return {int(k): v for k, v in d["sections"].items()}
    return {i: k for i, k in enumerate(DOCS[name]["start"](), 1)}


# ---------------------------------------------------------------- books and paintings
BOOK_FIELDS = [
    ("ንዑስ ርእስ", "sub", lambda b: (b.get("sub") or {}).get("am", "")),
    ("ዓመት (ዓ.ም.)", "year", lambda b: b.get("year", "")),
    ("ገጽ", "pages", lambda b: b.get("pages", "")),
    ("ማተሚያ ቤት", "publisher", lambda b: (b.get("publisher") or {}).get("am", "")),
    ("ዋጋ (ብር)", "price", lambda b: b.get("price", "")),
    ("ተሸጦ አልቋል", "sold_out", lambda b: YES if b.get("sold_out") else ""),
    ("አዲሱ መጽሐፍ", "newest", lambda b: YES if b.get("newest") else ""),
    ("መሪ ቃል", "motto", lambda b: (b.get("motto") or {}).get("am", "")),
]
PAINT_FIELDS = [
    ("ዓመት", "year", lambda p: p.get("year", "")),
    ("ቅብ", "medium", lambda p: (p.get("medium") or {}).get("am", "")),
]
CAT = {"books": (BOOK_FIELDS, "ስለ መጽሐፉ"), "paintings": (PAINT_FIELDS, "ስለ ሥዕሉ")}
LABEL_RE = re.compile(r"^(.+?)\s*[፡:]\s*(.*)$")


def catalog_items(name):
    return {x["slug"]: x for x in json.load(open(os.path.join(ROOT, "content", f"{name}.json"), encoding="utf-8"))}


def about_paras(item):
    return [x for x in (item.get("about") or {}).get("am", "").split("\n") if x.strip()]


def item_img(name, item):
    if name == "books":
        return item["faces"][0]["img"] if item.get("faces") else None
    return item["slug"]


def parse_item(name, blks):
    fields, about, in_about = {}, [], False
    labels = [l for l, _, _ in CAT[name][0]]
    for _, t in blks:
        m = LABEL_RE.match(t)
        if m and m.group(1).strip() == CAT[name][1]:
            in_about = True
            if m.group(2).strip():
                about.append(m.group(2).strip())
            continue
        if m and m.group(1).strip() in labels and not in_about:
            fields[m.group(1).strip()] = m.group(2).strip()
            continue
        if in_about:
            about.append(t)
    return fields, about


def item_diff(name, item, title, blks):
    fields, about = parse_item(name, blks)
    ch = {}
    if norm(title) != norm(item["title"]["am"]):
        ch["ርእስ"] = {"site": item["title"]["am"], "doc": title, "field": "title"}
    for label, field, get in CAT[name][0]:
        if label in fields and norm(fields[label]) != norm(get(item)):
            ch[label] = {"site": get(item), "doc": fields[label], "field": field}
    if [norm(x) for x in about] != [norm(x) for x in about_paras(item)]:
        ch[CAT[name][1]] = {"site": about_paras(item), "doc": about, "field": "about"}
    return ch


# ---------------------------------------------------------------- create
def body_html(blks):
    """Blocks (without the title) as Doc HTML: headings, paragraphs, lists, tables."""
    parts, rows, in_list = [], [], False

    def flush():
        if rows:
            parts.append("<table>" + "".join("<tr>" + "".join(f"<td>{html.escape(c)}</td>" for c in r.split(" | ")) + "</tr>"
                                             for r in rows) + "</table>")
            rows.clear()
    for kind, text in blks:
        if kind != "row":
            flush()
        if kind != "li" and in_list:
            parts.append("</ul>"); in_list = False
        e = html.escape(text)
        if kind == "row":
            rows.append(text)
        elif kind == "li":
            if not in_list:
                parts.append("<ul>"); in_list = True
            parts.append(f"<li>{e}</li>")
        elif kind in ("h2", "h3"):
            parts.append(f"<{kind}>{e}</{kind}>")
        else:  # p, lede (and an h1 inside a body would be odd; keep it as text)
            parts.append(f"<p>{e}</p>")
    flush()
    if in_list:
        parts.append("</ul>")
    return "".join(parts)


def section_title(key):
    b = site_blocks(key)
    return b[0][1] if b and b[0][0] == "h1" else LABELS.get(key, key)


def doc_html(name):
    spec = DOCS[name]
    secs = sections(name)
    nxt = geez(max(secs) + 1 if secs else 1)
    out = ["<html><body>"]
    for line in spec["help"] + [FOOT]:
        out.append(f'<p><span style="color:#6b6b6b;font-size:11pt">{html.escape(line.format(next=nxt))}</span></p>')
    if spec["kind"] == "catalog":
        items = catalog_items(name)
        fields, about_label = CAT[name]
        folder = "books" if name == "books" else "paintings"
        for n, slug in sorted(secs.items()):
            it = items[slug]
            out.append(f"<h1>{geez(n)} · {html.escape(it['title']['am'])}</h1>")
            img = item_img(name, it)
            if img:
                out.append(f'<p><img src="{BASE}/assets/img/{folder}/{img}-sm.jpg" width="160"></p>')
            for label, _, get in fields:
                out.append(f"<p>{label}፡ {html.escape(str(get(it)))}</p>")
            out.append(f"<p>{about_label}፡</p>")
            out += [f"<p>{html.escape(p)}</p>" for p in about_paras(it)]
    else:
        for n, key in sorted(secs.items()):
            b = site_blocks(key)
            out.append(f"<h1>{geez(n)} · {html.escape(section_title(key))}</h1>")
            out.append(body_html(b[1:] if b and b[0][0] == "h1" else b))
    out.append("</body></html>")
    return "".join(out)


# ---------------------------------------------------------------- read back
def split(md, known, takes_new=False):
    """[(number, title, [lines])]. A section starts at a Heading 1 that reads "N · title" (N going up).
    In a Doc that takes new pieces, a short line "N · title" with the next number also starts one,
    whatever its style, since he may not use the heading style."""
    out, last = [], 0
    for raw in md.split("\n"):
        s = raw.strip()
        if re.match(r"^!\[|^\[image\d+\]:", s):
            continue
        txt = blocks.clean(re.sub(r"^#{1,6}\s+", "", s)) if s and not s.startswith("|") else ""
        txt = re.sub(r"^[\s\-—–_*·.]+(?=[፩-፼0-9])", "", txt)  # a stray rule or bullet before the number
        m = HEAD_RE.match(txt) if txt else None
        if m:
            n = from_geez(m.group(1))
            h1 = s.startswith("# ")
            nxt = max(set(known) | {last}) + 1
            if n and n > last and (h1 or (takes_new and n == nxt and len(txt) < 80 and not re.match(r"^\d+\.\s", s))):
                out.append((n, m.group(2).strip(), []))
                last = n
                continue
        if out:
            out[-1][2].append(raw)
    return out


def diff(name, text):
    spec = DOCS[name]
    secs = sections(name)
    found = split(text, set(secs), bool(spec["new"]))
    res = {"doc": name, "changed": [], "unchanged": [], "new_sections": [], "missing_sections": [], "warnings": []}
    seen = set()
    items = catalog_items(name) if spec["kind"] == "catalog" else {}
    for n, title, lines in found:
        body = "\n".join(lines)
        if n not in secs:
            res["new_sections"].append({"n": n, "title": title, "markdown": body.strip()})
            continue
        seen.add(n)
        key = secs[n]
        if spec["kind"] == "catalog":
            ch = item_diff(name, items[key], title, doc_blocks(body))
            (res["changed"].append({"n": n, "slug": key, "changes": ch}) if ch else res["unchanged"].append(n))
            continue
        has_title = bool(site_blocks(key)) and site_blocks(key)[0][0] == "h1"
        md = (f"# {title}\n\n" if has_title else "") + body
        d = blocks.diff(key, md)
        if d["changes"] or d["warnings"]:
            res["changed"].append({"n": n, "key": key, **{k: d[k] for k in ("changes", "warnings", "held_by_overrides")}})
        else:
            res["unchanged"].append(n)
    res["missing_sections"] = [{"n": n, "key": k} for n, k in sorted(secs.items()) if n not in seen]
    if not found:
        res["warnings"].append("NO NUMBERED SECTIONS FOUND — the Doc may have been emptied or its numbers removed. Apply nothing from it.")
    elif res["missing_sections"]:
        res["warnings"].append(f"{len(res['missing_sections'])} of {len(secs)} numbered sections are missing (deleted, or the heading lost its "
                               "number or style, which would merge it into the section before) — apply nothing from this Doc.")
    if res["new_sections"] and not spec["new"]:
        res["warnings"].append("New numbered sections in a Doc that doesn't take new pieces — ask Selly what they are.")
    return res


def section_md(name, text, n):
    for k, title, lines in split(text, set(sections(name)), bool(DOCS[name]["new"])):
        if k == n:
            return f"# {title}\n\n" + "\n".join(lines).strip()
    raise SystemExit(f"no section {n}")


def _doc_json_md(d):
    """A Google Docs API document (read_doc) as the same Markdown shape read_file_content gives."""
    d = d.get("content", d)
    tab = d["tabs"][0]["documentTab"] if "tabs" in d else d
    out = []

    def text(p):
        return "".join(e.get("textRun", {}).get("content", "") for e in p["elements"]).rstrip("\n")
    for el in tab["body"]["content"]:
        if "paragraph" in el:
            p = el["paragraph"]
            t = text(p)
            if not t.strip():
                continue
            st = p.get("paragraphStyle", {}).get("namedStyleType", "")
            if st.startswith("HEADING_"):
                out.append("#" * int(st[-1]) + " " + t)
            elif "bullet" in p:
                out.append("  - " + t)
            else:
                out.append(t)
        elif "table" in el:
            for r in el["table"]["tableRows"]:
                cells = [" ".join(text(c2["paragraph"]) for c2 in c["content"] if "paragraph" in c2) for c in r["tableCells"]]
                out.append("| " + " | ".join(cells) + " |")
    return "\n\n".join(out)


def read_file(path):
    """The Doc's text from a saved read_file_content result ({"fileContent": …}), a saved read_doc result
    (the Docs API JSON), or plain Markdown."""
    txt = open(path, encoding="utf-8").read()
    try:
        d = json.loads(txt)
    except Exception:
        return txt
    if isinstance(d, dict) and "fileContent" in d:
        return d["fileContent"]
    if isinstance(d, dict) and ("content" in d or "tabs" in d or "body" in d):
        return _doc_json_md(d)
    return txt


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "list":
        for name, spec in DOCS.items():
            print(spec["title"], f"({name})")
            for n, k in sorted(sections(name).items()):
                print(f"   {geez(n)} {n:>2}  {k}")
    elif cmd == "doc-html":
        print(doc_html(sys.argv[2]))
    elif cmd == "diff":
        print(json.dumps(diff(sys.argv[2], read_file(sys.argv[3])), ensure_ascii=False, indent=1))
    elif cmd == "section":
        print(section_md(sys.argv[2], read_file(sys.argv[3]), int(sys.argv[4])))
    else:
        raise SystemExit(__doc__)
