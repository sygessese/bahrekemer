#!/usr/bin/env python3
"""Run by .github/workflows/drive-photos.yml: download each pending photo in sync/photo-requests.json
from Google Drive (shared "Anyone with the link") and save a large and a small JPEG for the site.

A request: {"id": "<Drive file id>", "dest": "assets/img/books/sewasewe-kemer", "large": 1100, "small": 520,
            "side": "width" | "long", "status": "pending"}
"""
import hashlib, io, json, os, urllib.request
from PIL import Image, ImageOps

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REQ = os.path.join(ROOT, "sync", "photo-requests.json")


def fit(im, size, side):
    w, h = im.size
    scale = size / (w if side == "width" else max(w, h))
    return im if scale >= 1 else im.resize((round(w * scale), round(h * scale)), Image.LANCZOS)


reqs = json.load(open(REQ))
for r in reqs:
    if r.get("status") != "pending":
        continue
    url = f'https://drive.usercontent.google.com/download?id={r["id"]}&export=download&confirm=t'
    try:
        data = urllib.request.urlopen(url, timeout=120).read()
        im = ImageOps.exif_transpose(Image.open(io.BytesIO(data))).convert("RGB")
    except Exception as e:
        r["status"] = f"error: {e.__class__.__name__} — is the Drive folder shared 'Anyone with the link'?"
        continue
    os.makedirs(os.path.dirname(os.path.join(ROOT, r["dest"])), exist_ok=True)
    side = r.get("side", "long")
    fit(im, r.get("large", 1800), side).save(os.path.join(ROOT, r["dest"] + ".jpg"), quality=84, optimize=True, progressive=True)
    fit(im, r.get("small", 900), side).save(os.path.join(ROOT, r["dest"] + "-sm.jpg"), quality=80, optimize=True, progressive=True)
    r["status"] = "done"
    r["id"] = hashlib.sha256(r["id"].encode()).hexdigest()[:16]   # the repo is public: keep only a hash once fetched
json.dump(reqs, open(REQ, "w"), indent=1)
