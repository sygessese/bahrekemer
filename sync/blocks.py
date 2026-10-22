#!/usr/bin/env python3
"""Amharic text of each page as an ordered list of blocks — the same shape the Google Docs have.

Used by sync/docs.py (which splits the seven Docs into sections) and directly:
  python3 sync/blocks.py doc-html KEY      HTML to create a Google Doc for KEY (Amharic only)
  python3 sync/blocks.py diff KEY FILE     compare a Doc (FILE = its text from read_file_content) with the site
  python3 sync/blocks.py show KEY          print the site's blocks for KEY

KEY is a page (megbiya, numbers, key, qene, poetry, books, paintings, contact, index)
or a writing (writings/<slug>). Block types: h1 (title), lede, h2, h3, p, li, row (table row, cells joined " | ").
"""
import json, os, re, sys, difflib, html
from bs4 import BeautifulSoup, Comment, NavigableString

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = json.load(open(os.path.join(ROOT, "site.json"), encoding="utf-8"))
WRITINGS = json.load(open(os.path.join(ROOT, "content", "writings.json"), encoding="utf-8"))
ETH = re.compile(r"[ሀ-᎟ⶀ-⷟꬀-꬯]")

BLOCK = {"h1", "h2", "h3", "h4", "p", "li", "tr", "dt", "dd", "figcaption", "blockquote"}
SKIP_CLASSES = {"ui", "sec-head", "paint-strip", "more-link", "text-link", "btn", "reader", "cover-no", "big-num", "ornament", "book-strip", "end-mark"}


def norm(s):
    s = html.unescape(s).replace(" ", " ")
    s = re.sub(r"\s+", " ", s).strip()
    return s


def page_head(slug):
    pg = SITE["pages"][slug]
    head = pg.get("heading", pg.get("label"))
    lede = pg.get("lede", pg.get("description"))
    out = []
    if head:
        out.append(("h1", norm(head["am"])))
    if lede:
        out.append(("lede", norm(lede["am"])))
    return out


def is_en(tag):
    for t in [tag] + list(tag.parents):
        if getattr(t, "get", None) and t.get("lang") == "en":
            return True
    return False


def skipped(tag):
    for t in [tag] + list(tag.parents):
        cls = set(t.get("class") or []) if getattr(t, "get", None) else set()
        if cls & SKIP_CLASSES or (getattr(t, "get", None) and t.get("aria-hidden") == "true"):
            return True
    return False


def am_text(tag):
    """Text of a tag with all English parts removed."""
    t = BeautifulSoup(str(tag), "html.parser")
    for en in t.find_all(attrs={"lang": "en"}):
        en.decompose()
    for c in t.find_all(string=lambda s: isinstance(s, Comment)):
        c.extract()
    for br in t.find_all("br"):
        br.replace_with("\n")
    return t.get_text(" ")


def html_blocks(src):
    soup = BeautifulSoup(src, "html.parser")
    out = []
    for tag in soup.find_all(True):
        if is_en(tag) or skipped(tag):
            continue
        cls = set(tag.get("class") or [])
        # a poem: one line per block
        if tag.name == "div" and "verse" in cls:
            if any(p for p in tag.parents if p.name == "div" and "verse" in (p.get("class") or [])):
                continue
            for line in am_text(tag).split("\n"):
                if norm(line):
                    out.append(("p", norm(line)))
            continue
        if tag.name not in BLOCK:
            continue
        if any(p.name in BLOCK or (p.name == "div" and "verse" in (p.get("class") or [])) for p in tag.parents):
            continue
        if tag.name == "blockquote" and tag.find(["p"]):
            continue  # its <p> children are the blocks
        if tag.name == "tr":
            cells = [norm(am_text(c)) for c in tag.find_all(["td", "th"])]
            if any(cells):
                out.append(("row", " | ".join(cells)))
            continue
        text = norm(am_text(tag))
        if not text:
            continue
        kind = {"h1": "h1", "h2": "h2", "h3": "h3", "h4": "h3", "li": "li"}.get(tag.name, "p")
        out.append((kind, text))
    return out


def writing(slug):
    for w in WRITINGS:
        if w["slug"] == slug:
            return w
    raise SystemExit(f"no writing {slug}")


def site_blocks(key):
    if key.startswith("writings/"):
        slug = key.split("/", 1)[1]
        w = writing(slug)
        src = open(os.path.join(ROOT, "content", "writings", f"{slug}.html"), encoding="utf-8").read()
        return [("h1", norm(w["title"]["am"]))] + html_blocks(src)
    src_path = os.path.join(ROOT, "content", f"{key}.html")
    src = open(src_path, encoding="utf-8").read() if os.path.exists(src_path) else ""
    head = page_head(key) if key in SITE["pages"] and key != "index" else []
    return head + html_blocks(src)


# ---------------------------------------------------------------- Doc side
def doc_blocks(md):
    """Blocks from the Markdown-like text Google Drive returns for a Doc."""
    out = []
    first_p_after_h1 = False
    for raw in md.split("\n"):
        line = raw.rstrip()
        if not line.strip():
            continue
        s = line.strip()
        if s.startswith("|"):
            cells = [c.strip() for c in s.strip("|").split("|")]
            if all(re.fullmatch(r":?-+:?", c) or c == "" for c in cells):
                continue  # separator / empty header row
            cells = [clean(c) for c in cells]
            out.append(("row", " | ".join(cells)))
            continue
        m = re.match(r"(#{1,6})\s+(.*)", s)
        if m:
            level = len(m.group(1))
            kind = "h1" if level == 1 else ("h2" if level == 2 else "h3")
            out.append((kind, clean(m.group(2))))
            first_p_after_h1 = kind == "h1" and len(out) == 1
            continue
        m = re.match(r"(?:[-*+]|\d+\.)\s+(.*)", s)
        if m and re.match(r"\s*(?:[-*+]|\d+\.)\s", line):
            out.append(("li", clean(m.group(1))))
            continue
        out.append(("p", clean(s)))
    return out


def clean(s):
    s = re.sub(r"\\(.)", r"\1", s)            # markdown escapes
    s = re.sub(r"\\", "", s)
    s = re.sub(r"(\*\*|__)(.*?)\1", r"\2", s)  # bold
    s = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?!\w)", r"\1", s)  # italic
    return norm(s)


def as_page_doc(key, blocks):
    """The Doc's first paragraph after the title is the lede on section pages."""
    if key in SITE["pages"] and key != "index" and len(blocks) > 1 and blocks[0][0] == "h1" and blocks[1][0] == "p":
        blocks = [blocks[0], ("lede", blocks[1][1])] + blocks[2:]
    return blocks


def doc_html(key):
    b = site_blocks(key)
    parts, rows = [], []

    def flush():
        if rows:
            parts.append("<table>" + "".join(
                "<tr>" + "".join(f"<td>{html.escape(c)}</td>" for c in r.split(" | ")) + "</tr>" for r in rows) + "</table>")
            rows.clear()
    in_list = False
    for kind, text in b:
        if kind != "row":
            flush()
        if kind != "li" and in_list:
            parts.append("</ul>"); in_list = False
        t = html.escape(text)
        if kind == "row":
            rows.append(text)
        elif kind == "li":
            if not in_list:
                parts.append("<ul>"); in_list = True
            parts.append(f"<li>{t}</li>")
        elif kind in ("h1", "h2", "h3"):
            parts.append(f"<{kind}>{t}</{kind}>")
        else:
            parts.append(f"<p>{t}</p>")
    flush()
    if in_list:
        parts.append("</ul>")
    return "<html><body>" + "".join(parts) + "</body></html>"


# ---------------------------------------------------------------- compare
def word_diff(old, new):
    """Short word-level summary: '−removed +added' pieces, for the nightly message."""
    a, b = old.split(), new.split()
    out = []
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(a=a, b=b, autojunk=False).get_opcodes():
        if op in ("replace", "delete"):
            out.append("− " + " ".join(a[i1:i2]))
        if op in ("replace", "insert"):
            out.append("+ " + " ".join(b[j1:j2]))
    return out


def overrides(key):
    p = os.path.join(ROOT, "sync", "overrides.json")
    data = json.load(open(p, encoding="utf-8")) if os.path.exists(p) else []
    return [(o["doc"], o["site"]) for o in data if o["key"] == key]


def diff(key, doc_text):
    site = site_blocks(key)
    doc = as_page_doc(key, doc_blocks(doc_text))
    ign = overrides(key)
    sm = difflib.SequenceMatcher(a=[f"{k}\t{t}" for k, t in site], b=[f"{k}\t{t}" for k, t in doc], autojunk=False)
    changes, held = [], []
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == "equal":
            continue
        before, after = site[i1:i2], doc[j1:j2]
        if len(before) == len(after) and all((a[1], b[1]) in ign for a, b in zip(after, before)):
            held.append({"site": before, "doc": after})
            continue
        ch = {"op": op, "at_site_block": i1, "site": before, "doc": after,
              "context_before": site[i1 - 1][1][:80] if i1 > 0 else None}
        if op == "replace" and len(before) == len(after):
            ch["words"] = [word_diff(a[1], b[1]) for a, b in zip(before, after)]
        changes.append(ch)
    site_chars = sum(len(t) for _, t in site)
    removed = sum(len(t) for c in changes for _, t in c["site"]) - sum(len(t) for c in changes if c["op"] == "replace" for _, t in c["doc"])
    warn = []
    if not doc:
        warn.append("THE DOC IS EMPTY")
    elif site_chars and removed > 0.2 * site_chars:
        warn.append(f"About {round(100 * removed / site_chars)}% of the page's text would be removed")
    return {"key": key, "changes": changes, "held_by_overrides": held, "warnings": warn,
            "site_blocks": len(site), "doc_blocks": len(doc)}


if __name__ == "__main__":
    cmd, key = sys.argv[1], sys.argv[2]
    if cmd == "doc-html":
        print(doc_html(key))
    elif cmd == "show":
        for k, t in site_blocks(key):
            print(f"{k}\t{t}")
    elif cmd == "diff":
        txt = open(sys.argv[3], encoding="utf-8").read()
        try:
            txt = json.loads(txt)["fileContent"]
        except Exception:
            pass
        print(json.dumps(diff(key, txt), ensure_ascii=False, indent=1))
