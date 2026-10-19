# ባሕረ ቀመር · Bahrekemer

Bilingual (Amharic / English) static site for **bahrekemer.com**, hosted on GitHub Pages.

## Publishing a new poem or article

1. Copy any file in `content/writings/` to a new name, e.g. `content/writings/meskel-2019.html`,
   and replace the text — Amharic inside `lang="am"`, English inside `lang="en"`
   (a poem uses the `verse-pair` block; an essay uses the two `<div>` blocks, one `<p>` per paragraph,
   **the same number of paragraphs in each** so they line up side by side).
2. Add an entry at the **top** of `content/writings.json`:
   ```json
   { "slug": "meskel-2019", "kind": "poem", "title": { "am": "…", "en": "…" } },
   ```
   `kind` is `"essay"` or `"poem"`; add `"continuing": true` for a piece that will be continued.
3. Run `python3 build.py`, then commit and push. The new piece becomes the lead story on the home page,
   and the others move down automatically.

## Editing everything else

| What | Where |
|---|---|
| Section pages (Introduction, Numbers, Key, Qene, Poetry, Books, Paintings, Contact) | `content/<page>.html` |
| Home page (fixed parts: Numbers box, Introduction quote, profile, book strip) | `content/index.html` |
| Page titles, SEO descriptions, nav order, which pages get the reading slider | `site.json` |
| Header, footer, `<head>`/SEO template | `build.py` |
| Styles / scripts | `assets/css/style.css`, `assets/js/main.js` |
| Images | `assets/img/` — `author.jpg` (4:5) appears in the profile automatically; `og.png` 1200×630 for link previews |

Text is written twice, side by side:

```html
<span lang="am">አማርኛ</span><span lang="en">English</span>      ← titles and labels
<p lang="am">…</p><p lang="en">…</p>                         ← paragraphs
```

- **Amharic mode** (default) shows only Amharic; the header and menu stay bilingual.
- **English mode** shows the Amharic with the English beside it.
- Reading pages have a slider — **አማርኛ / ጎን ለጎን (side by side) / English** — that pairs each Amharic
  paragraph with its English one.
- The **ሀ ሀ** button enlarges all text. Choices are remembered in the browser; `?lang=en` makes English links shareable.

Then rebuild (Python 3, no dependencies) and commit **both** `content/` and the generated pages:

```sh
python3 build.py
python3 -m http.server 8000   # preview at http://localhost:8000
```

## Deploy (one-time, done)

GitHub → *Settings → Pages*: `main` / `(root)`, custom domain `bahrekemer.com`, **Enforce HTTPS**.
GoDaddy DNS: four **A** records `@` → `185.199.108.153`, `.109.153`, `.110.153`, `.111.153`; **CNAME** `www` → `sygessese.github.io`.
