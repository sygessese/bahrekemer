#!/usr/bin/env python3
"""Compare the "መጻሕፍትና ሥዕሎች" Google Sheet with content/books.json and content/paintings.json.

  python3 sync/sheet.py FILE      FILE = the sheet's text from read_file_content (raw JSON or just the text)

Prints JSON: per tab, rows whose cells differ from the site, new rows, and rows missing from the sheet.
Only the Amharic-side facts are compared; English titles are compared as plain text (the site may add <i>).
"""
import json, os, re, sys, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOKS = json.load(open(os.path.join(ROOT, "content", "books.json"), encoding="utf-8"))
PAINTINGS = json.load(open(os.path.join(ROOT, "content", "paintings.json"), encoding="utf-8"))

BOOK_COLS = {  # sheet header -> getter on a books.json entry
    "መለያ (አይቀየር)": lambda b: b["slug"],
    "ርእስ": lambda b: b["title"]["am"],
    "Title (English)": lambda b: plain(b["title"]["en"]),
    "ንዑስ ርእስ": lambda b: b.get("sub", {}).get("am", ""),
    "ዓመት (ዓ.ም.)": lambda b: b.get("year", ""),
    "ገጽ": lambda b: b.get("pages", ""),
    "ማተሚያ ቤት": lambda b: b.get("publisher", {}).get("am", ""),
    "ዋጋ (ብር)": lambda b: b.get("price", ""),
    "አዲሱ መጽሐፍ (✓)": lambda b: "✓" if b.get("newest") else "",
    "ስለ መጽሐፉ": lambda b: b.get("about", {}).get("am", ""),
    "መሪ ቃል": lambda b: b.get("motto", {}).get("am", ""),
}
PAINTING_COLS = {
    "መለያ (አይቀየር)": lambda p: p["slug"],
    "ርእስ": lambda p: p["title"]["am"],
    "Title (English)": lambda p: p["title"]["en"],
    "ዓመት": lambda p: p.get("year", ""),
    "ቅብ": lambda p: (p.get("medium") or {"am": "የዘይት ቀለም"})["am"],
    "የፎቶው ስም": lambda p: p.get("photo", "(በድረ ገጹ ላይ ያለ)"),
}


def plain(s):
    return re.sub(r"<[^>]+>", "", s)


def norm(s):
    s = html.unescape(str(s or "")).replace(" ", " ")
    s = re.sub(r"\\(.)", r"\1", s)
    s = re.sub(r"\s+", " ", s).strip()
    return re.sub(r"\.0$", "", s)  # 2016.0 -> 2016


def tables(text):
    """{sheet name: [ {header: value} ]} from the Markdown-ish text Drive returns."""
    out, name, rows = {}, None, None
    for line in text.split("\n"):
        m = re.match(r"#+\s*Sheet Name:\s*(.+)", line)
        if m:
            name = m.group(1).strip(); out[name] = []; rows = None
            continue
        if name is None or not line.strip().startswith("|"):
            if rows is not None and line.strip() and not line.strip().startswith("|"):
                rows = None if line.startswith("#") else rows
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if all(re.fullmatch(r":?-+:?", c) or c == "" for c in cells):
            continue
        cells = [norm(c) for c in cells]
        if rows is None:
            rows = {"header": cells}
            out[name].append(rows)
        else:
            out[name].append(dict(zip(rows["header"], cells)))
    return {k: [r for r in v if "header" not in r] for k, v in out.items()}


def compare(rows, items, cols):
    by_id = {it["slug"]: it for it in items}
    seen, changed, new = set(), [], []
    for r in rows:
        rid = r.get("መለያ (አይቀየር)", "")
        if not any(r.values()):
            continue
        if not rid or rid not in by_id:
            new.append(r)
            continue
        seen.add(rid)
        diffs = {}
        for col, get in cols.items():
            if col in r and norm(get(by_id[rid])) != r[col]:
                diffs[col] = {"site": norm(get(by_id[rid])), "sheet": r[col]}
        if diffs:
            changed.append({"id": rid, "changes": diffs})
    missing = [s for s in by_id if s not in seen]
    return {"changed": changed, "new_rows": new, "missing_from_sheet": missing}


if __name__ == "__main__":
    txt = open(sys.argv[1], encoding="utf-8").read()
    try:
        txt = json.loads(txt)["fileContent"]
    except Exception:
        pass
    t = tables(txt)
    print(json.dumps({"books": compare(t.get("መጻሕፍት", []), BOOKS, BOOK_COLS),
                      "paintings": compare(t.get("ሥዕሎች", []), PAINTINGS, PAINTING_COLS)},
                     ensure_ascii=False, indent=1))
