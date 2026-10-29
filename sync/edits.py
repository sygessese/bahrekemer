#!/usr/bin/env python3
"""What Yitbarek saved in the editor (bahrekemer.com/edit/), waiting on the `dad-edits` branch.

  python3 sync/edits.py list [REF]          every saved edit, oldest first, with where each text lives in the repo
                                            (REF defaults to origin/dad-edits; run `git fetch origin` first)
  python3 sync/edits.py where "TEXT"        the files and lines where an Amharic text appears
  python3 sync/edits.py photo REF FILE OUT  copy a saved photo to assets/img/OUT.jpg (≤1600px) and OUT-sm.jpg (≤520px)
                                            e.g. photo origin/dad-edits edits/photos/…-front.jpg books/sewasewe-kemer

Each saved edit is a JSON file edits/<id>.json (see assets/edit/edit.js and editor/worker.js):
  {type: "text",  key, page, changes: [{op: edit|insert|delete|field, …}]}   — apply the changes in order
  {type: "photo", target: "book:<slug>"|"painting:<slug>"|"home", face: front|back|main, file}  (or remove: true)
  {type: "new",   piece_id, kind: essay|poem|qene|painting|book, title, text: [...], year, photos: [{role, file}]}
                  (a qene also: author, meaning, sem, werq, calc)
                  — a piece can be saved several times: only the LAST file per piece_id counts.
"""
import glob, html, io, json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCES = ["site.json", "content/*.json", "content/*.html", "content/writings/*.html"]


def git(*args, binary=False):
    out = subprocess.run(["git", "-C", ROOT, *args], capture_output=True, check=True).stdout
    return out if binary else out.decode("utf-8")


def norm(s):
    s = html.unescape(s).replace(" ", " ")
    return re.sub(r"\s+", " ", s).strip()


def plain(s):
    return norm(re.sub(r"<[^>]+>", " ", s.replace("<br>", "\n")))


def where(text):
    """[(file, line)] — matched on the first few words, ignoring markup and spacing."""
    first = norm(text.split("\n")[0])
    probe = " ".join(first.split()[:6]) or first
    hits = []
    for pat in SOURCES:
        for f in sorted(glob.glob(os.path.join(ROOT, pat))):
            rel = os.path.relpath(f, ROOT)
            for n, line in enumerate(open(f, encoding="utf-8"), 1):
                txt = plain(line.replace('\\"', '"'))
                if probe and probe in txt:
                    hits.append({"file": rel, "line": n, "exact": first in txt})
    return hits


def load(ref="origin/dad-edits"):
    try:
        names = git("ls-tree", "--name-only", f"{ref}:edits").split()
    except subprocess.CalledProcessError:
        return []
    out = []
    for name in sorted(n for n in names if n.endswith(".json")):
        rec = json.loads(git("show", f"{ref}:edits/{name}"))
        rec["_file"] = f"edits/{name}"
        out.append(rec)
    return out


def listing(ref):
    edits = load(ref)
    last_new = {}
    for e in edits:
        if e.get("type") == "new":
            last_new[e.get("piece_id")] = e["id"]
    for e in edits:
        if e.get("type") == "text":
            for c in e.get("changes", []):
                probe = c.get("from") or c.get("after")
                if probe and c["op"] != "field":
                    c["where"] = where(probe)
        if e.get("type") == "new":
            e["superseded"] = last_new.get(e.get("piece_id")) != e["id"]
    return edits


def photo(ref, file, out):
    from PIL import Image, ImageOps  # pip install --break-system-packages pillow
    img = ImageOps.exif_transpose(Image.open(io.BytesIO(git("show", f"{ref}:{file}", binary=True)))).convert("RGB")
    dest = os.path.join(ROOT, "assets", "img", out)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    for suffix, size in (("", 1600), ("-sm", 520)):
        im = img.copy()
        im.thumbnail((size, size * 2))
        im.save(f"{dest}{suffix}.jpg", "JPEG", quality=86, optimize=True, progressive=True)
        print(f"assets/img/{out}{suffix}.jpg", im.size)


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "list"
    if cmd == "list":
        print(json.dumps(listing(sys.argv[2] if len(sys.argv) > 2 else "origin/dad-edits"), ensure_ascii=False, indent=1))
    elif cmd == "where":
        print(json.dumps(where(sys.argv[2]), ensure_ascii=False, indent=1))
    elif cmd == "photo":
        photo(sys.argv[2], sys.argv[3], sys.argv[4])
    else:
        raise SystemExit(__doc__)
