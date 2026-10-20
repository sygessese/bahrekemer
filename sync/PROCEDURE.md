# Nightly Google Drive sync — procedure

You are the nightly sync for bahrekemer.com, the site of Yitbarek Gessese Merra (ይትባረክ ገሠሠ መራ), an 88-year-old Ethiopian historian, painter and author. His daughter **Selly** maintains the site. He edits the site's **Amharic** in Google Docs; you bring his changes into the repo, write the **English**, and prepare everything for Selly to approve. **Nothing goes live without Selly replying "push".**

Follow this file exactly. Work in the repo `sygessese/bahrekemer` (GitHub Pages serves `main`). Python 3, `beautifulsoup4`, `openpyxl` and `playwright` (Chromium is preinstalled) are used; `pip install --break-system-packages beautifulsoup4` if missing.

## Who owns what

| Content | Lives in | Changed by |
|---|---|---|
| Amharic text of every page and writing | Google Docs in the Drive folder | Dad (or Selly, in the Doc) |
| English text | the repo (`content/`, `site.json`) | this sync, or Claude in chat |
| Book and painting facts | the Google Sheet "መጻሕፍትና ሥዕሎች" | anyone with the link |
| Photos | Drive `ፎቶዎች/` → repo `assets/img/` (via the GitHub Action) | Selly drops them in |
| Design, layout, code | the repo | Claude in chat |

`sync/manifest.json` maps every Drive file to its page. **The repo is public, so it never holds Drive ids** — only `idhash` = the first 16 hex characters of sha256(id) (`python3 sync/idhash.py <id>`). The ids of the Drive folders and the Sheet are in your scheduled-task instructions; never write them into the repo. `sync/blocks.py` turns a page (or a Doc's text) into an ordered list of Amharic blocks and compares them. `sync/sheet.py` compares the Sheet with `content/books.json` / `content/paintings.json`. `sync/overrides.json` lists known, accepted differences between a Doc and the site (skip them, but mention them). `sync/GLOSSARY.md` is the translation guide — **read it before translating**.

## Every night (2am Addis Ababa)

### 1. Set up
```
git clone https://github.com/sygessese/bahrekemer.git && cd bahrekemer   # or cd + git fetch if present
git fetch origin
git checkout -B drive-sync origin/drive-sync 2>/dev/null || git checkout -B drive-sync origin/main
git rebase origin/main      # bring in anything pushed since; if it conflicts: git rebase --abort, report, stop
```
If `drive-sync` already existed, it holds changes Selly hasn't approved yet — keep them; tonight's changes go on top.

### 2. Find what changed in Drive
Read `sync/manifest.json`. Using the Google Drive tools:
- `search_files` with `parentId = '<id>'` (and `excludeContentSnippets: true`) for each folder id in your instructions: root, essays, poems, photos_paintings, photos_books — and for each subfolder of photos_books (one per book). Note each file's `id`, `title`, `mimeType`, `modifiedTime`, and compute its `idhash` (`python3 sync/idhash.py id1 id2 …`).
- Match files to the manifest by `idhash` (docs, the Sheet, book photo folders).
- A **known Doc** changed if its `modifiedTime` is later than its `seen_modified`. If its title changed, update `name` too.
- A **new Doc** is one whose idhash isn't in the manifest: in `essays` → new essay; in `poems` → new poem; in `root` → don't guess, list it under **Needs you** in the summary.
- A **known Doc missing** from its folder (moved or trashed): don't delete anything from the site; list it under **Needs you**.
- The **Sheet** changed if its `modifiedTime` > `sheet.seen_modified`.
- **New photos**: image files whose idhash isn't in `processed_photos`.

If nothing changed and there is no pending `drive-sync` work: reply with one line, "No changes in the Drive folder tonight.", and stop. If nothing changed but `drive-sync` has unapproved changes: one line reminding Selly they're waiting, and stop.

### 3. A changed page or writing Doc
1. `read_file_content` the Doc. Save the result exactly (the JSON or its `fileContent`) to `/tmp/doc.json` — copy it faithfully, it is compared character by character.
2. `python3 sync/blocks.py diff <key> /tmp/doc.json` (key from the manifest, e.g. `megbiya`, `writings/zera-yacob`).
3. No `changes` → just update `seen_modified`. Otherwise apply each change:
   - **Where the text lives.** `python3 sync/blocks.py show <key>` lists the site's blocks in order; `at_site_block` indexes into it. Block 0/1 of a section page are the page title (`h1`) and lede: those live in `site.json` → `pages.<key>.heading` (or `label`) and `pages.<key>.lede` (or `description`), each with `am` and `en`. Everything else is in `content/<key>.html` (pages) or `content/writings/<slug>.html` (writings); find it by searching for a distinctive phrase of the old Amharic. A writing's title (its `h1`) lives in `content/writings.json`.
   - **How Amharic and English are paired** — keep these patterns exactly:
     - `<div lang="am"> …blocks… </div>` followed by `<div lang="en"> …the same blocks in the same order… </div>` (writings and long passages);
     - `<p lang="am">…</p>` immediately followed by `<p lang="en">…</p>`;
     - inline pairs `<span lang="am">…</span><span lang="en">…</span>` (headings, table cells, labels);
     - poems: `<div class="verse" lang="am">` one line per line, then `<div class="verse" lang="en">` with the same number of lines.
   - **Edit**: change the Amharic to the Doc's text **exactly** (don't correct his spelling or punctuation), then rewrite only the English partner of that block, following `sync/GLOSSARY.md` and the tone of the surrounding English. Don't touch the English of blocks he didn't change.
   - **Insert**: add the new block(s) in the same place, with both languages, using the pattern of the neighbouring blocks.
   - **Delete**: if the Doc dropped blocks, do **not** delete them from the site; list them under **Needs you** ("Dad removed this paragraph — remove it from the site?").
   - **Tables** (Numbers, Key): apply cell changes precisely and list every changed row in the summary.
4. Re-run the diff. It must report no changes except deletions you held back. If it doesn't, fix it before moving on.
5. Set the Doc's `seen_modified` in the manifest to its `modifiedTime`.

`diff` also prints `warnings` (empty Doc, a large share of the page removed). If there is a warning, don't apply that Doc at all — put it under **Needs you** with what you saw.

### 4. A new essay or poem
1. Read the Doc. Its first heading (or first line) is the title; if neither, use the Doc's name. Ignore an empty Doc (he may still be writing) — mention it.
2. Translate the title; make a slug from the English title (lowercase ASCII, hyphens, ≤ 5 words, unique among `content/writings/`).
3. Write `content/writings/<slug>.html`:
   - essay: `<!-- <English title> — edit the Amharic in lang="am", the English in lang="en". -->` then `<div lang="am">` with one `<p>` per paragraph (`<h3>` for his headings), then `<div lang="en">` with the same blocks translated;
   - poem: copy the structure of `content/writings/fruit-of-peace.html` (a `verse-pair` with an Amharic and an English `verse`, one line per line);
   - if the last line names a source (a book and year), make it `<p class="cite"><span lang="am">…</span><span lang="en">…</span></p>` as in the existing writings.
4. Add `{"slug": …, "kind": "essay"|"poem", "title": {"am": …, "en": …}}` at the **top** of `content/writings.json` — that makes it the "Latest" piece on the home page.
5. Add it to the manifest under `docs` as `writings/<slug>` (`idhash`, `name`, `folder`, `seen_modified`).
6. `python3 sync/blocks.py diff writings/<slug> /tmp/doc.json` must report no changes.

### 5. The Sheet
1. `read_file_content` the Sheet; save to `/tmp/sheet.json`; run `python3 sync/sheet.py /tmp/sheet.json`.
2. **changed** cells → update `content/books.json` / `content/paintings.json`. For each Amharic field that changed (`title.am`, `sub.am`, `publisher.am`, `about.am`, `motto.am`), update its `en` too (translate; for printers use the English names already in the file when the Amharic matches). "Title (English)" in the Sheet is compared as plain text — if it changed, use it, keeping `<i>…</i>` around a transliterated book name as the existing titles do. Only one book may have `"newest": true` (the ✓ row).
3. **new_rows** → a new book or painting. Make a slug from the English title (translate the Amharic title if the English is empty), add the entry, and for a book create a photo folder for it in Drive (`create_file`, folder, parent = the photos_books folder id, named its Amharic title) and record its idhash in `book_photo_folders`. You can't edit the Sheet, so under **Needs you** give Selly the slug to paste into that row's "መለያ (አይቀየር)" cell (until she does, match the row by its Amharic title).
4. **missing_from_sheet** → don't delete; ask under **Needs you**.
5. Keep the order of `books.json` / `paintings.json` the same as the Sheet's rows (the newest book first).
6. Set `sheet.seen_modified`.

### 6. Photos
For each new image file:
- In a **book's folder** (`book_photo_folders`): a name containing ፊት/front is the front cover, ጀርባ/back the back; otherwise the older file is the front. Add a request to `sync/photo-requests.json`:
  `{"id": "<file id>", "dest": "assets/img/books/<slug>" (front) or "assets/img/books/<slug>-back" (back), "large": 1100, "small": 520, "side": "width", "status": "pending"}`
  and set the book's `faces` in `books.json` to `[{"img": "<slug>", "label": {"am": "ፊት", "en": "Front"}}, {"img": "<slug>-back", "label": {"am": "ጀርባ", "en": "Back"}}]` (only the faces that exist).
- In **`photos_paintings`**: match it to the Sheet row whose "የፎቶው ስም" equals the file's name. Request `{"id": …, "dest": "assets/img/paintings/<slug>", "large": 1800, "small": 900, "side": "long", "status": "pending"}`. No matching row → **Needs you**.
- Add every handled file's idhash to `processed_photos`. (The request itself must carry the real id so the Action can download it; `fetch_photos.py` replaces it with the hash once fetched.)
- The GitHub Action `drive-photos` downloads them after you push the branch; it needs the Drive folder shared "Anyone with the link". Photos therefore appear on the branch a few minutes after your push, not in tonight's screenshots — say so.

### 7. Build, check, push the branch
```
python3 build.py                                   # must succeed
```
Screenshot each changed page at desktop (1280 wide) and phone (390 wide), Amharic, and for writings/pages also English — serve the folder with `python3 -m http.server 8765 &` and use Playwright (`chromium.launch()`), full page. Look at them yourself: nothing broken, no missing English, no empty blocks.

Update `last_run` in the manifest, then:
```
git add -A && git commit -m "Drive sync <date>: <short list>" 
git push --force-with-lease origin drive-sync
```
Never push to `main` in the nightly run.

### 8. The message to Selly
This is the whole point — write it for her to read on her phone. Plain, short, in this order:

1. **One line:** what changed tonight (e.g. "Dad edited the Introduction and added a new poem.").
2. **Each change:** the page name; for edits, the words removed/added in Amharic (the `words` from the diff) and the new English sentence(s); for a new writing, its title in both languages and the full English. Send the screenshots of the changed pages.
3. **Needs you:** deletions held back, new files in the wrong place, rows to fill in, warnings — each with exactly what to do.
4. **Ask Dad:** words you weren't sure of (Amharic word, the sentence it's in, your guess).
5. **Still different** (from `sync/overrides.json`): one line per item, so they don't get forgotten.
6. Last line: **Reply "push" to publish, or tell me what to change.**

## When Selly replies

- **"push"**:
  ```
  git fetch origin && git checkout drive-sync && git rebase origin/main
  python3 build.py && git add -A && git commit -m "Rebuild" || true
  git checkout main && git reset --hard origin/main && git merge --ff-only drive-sync
  git push origin main && git push origin --delete drive-sync
  ```
  Confirm it's live (GitHub Pages takes a minute or two).
- **A correction to the English**: make it on `drive-sync`, push the branch, show it, wait for "push".
- **"skip" / "don't publish" something Dad changed**: revert that change on the branch and add an entry to `sync/overrides.json` — `{"key": "<page>", "doc": "<the Doc block's text>", "site": "<the site block's text>", "note": "<why>"}` (one entry per block, texts exactly as `blocks.py` prints them) — so it isn't proposed again until the Doc changes. Mention it in "Still different" each night.
- **"remove it"** for a held deletion: remove the block (both languages), push the branch, wait for "push".

## Rules

- Never change his Amharic except to match his Doc exactly. Never "fix" his spelling.
- Never delete content, pages, writings or photos without Selly saying so.
- Never push to `main` without Selly's "push" in this conversation.
- If anything is unclear or a step fails, stop that part, keep the rest, and explain under **Needs you**.
- Claude sessions that change Amharic directly in the repo (outside this sync) must add an override and tell Selly to copy the change into the Doc — the Doc is the master copy of the Amharic.
