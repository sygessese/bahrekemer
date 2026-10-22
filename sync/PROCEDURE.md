# Nightly Google Drive sync — procedure

You are the nightly sync for bahrekemer.com, the site of Yitbarek Gessese Merra (ይትባረክ ገሠሠ መራ), an 88-year-old Ethiopian historian, painter and author. His daughter **Selly** maintains the site. He edits the site's **Amharic** in seven Google Docs; you bring his changes into the repo, write the **English**, and prepare everything for Selly to approve. **Nothing goes live without Selly replying "push".**

Follow this file exactly. Work in the repo `sygessese/bahrekemer` (GitHub Pages serves `main`). Python 3, `beautifulsoup4` and `playwright` (Chromium is preinstalled) are used; `pip install --break-system-packages beautifulsoup4` if missing.

## The seven Docs

All in one Drive folder (its id is in your scheduled-task instructions — never write it into the repo).

| Doc | Manifest key | Each numbered section is… | He can add new ones? |
|---|---|---|---|
| ፩ · ድርሰቶች | `essays` | one essay (`writings/<slug>`) | yes → new essay |
| ፪ · ግጥሞች | `poems` | ፩ = the Poetry page (`poetry`), then one poem each (`writings/<slug>`) | yes → new poem |
| ፫ · ቅኔ | `qene` | ፩ = the Qene page (`qene`); a new qene is a new heading inside it | no |
| ፬ · መጻሕፍት | `books` | one book (`content/books.json`) | yes → new book |
| ፭ · ሥዕሎች | `paintings` | one painting (`content/paintings.json`) | yes → new painting |
| ፮ · ቁጥሮችና ቁልፍ | `numbers` | ፩ = `numbers`, ፪ = `key` (mostly tables) | no |
| ፯ · መግቢያና ሌሎች ገጾች | `pages` | ፩ `megbiya`, ፪ `index` (home page text), ፫ `books` (Books page text), ፬ `contact` | no |

Every Doc starts with a few grey instruction lines (ignored), then sections that each begin with a heading "N · title" (N in Ge'ez numerals; Arabic digits are accepted too). **The number is the link** to the site: `sync/manifest.json → docs.<doc>.sections` maps it to a page, writing, book or painting. He may change titles freely. A section whose number isn't in the manifest is **new**.

Tools in `sync/`:
- `docs.py diff DOC FILE` — compares a Doc with the site and lists, per section, what changed. FILE is the Doc as you read it (see step 3). `docs.py section DOC FILE N` prints one section; `docs.py list` shows the layout.
- `blocks.py show KEY` — the site's Amharic blocks for a page or writing, in order (`at_site_block` in a diff indexes into this).
- `overrides.json` — known, accepted differences between a Doc and the site (skipped by the diff, but mention them).
- `GLOSSARY.md` — the translation guide. **Read it before translating.**
- `idhash.py` — the repo is public, so it never holds Drive ids, only `idhash` = first 16 hex of sha256(id).

## Every night (2am Addis Ababa)

### 1. Set up
```
git clone https://github.com/sygessese/bahrekemer.git && cd bahrekemer   # or cd + git fetch if present
git fetch origin
git checkout -B drive-sync origin/drive-sync 2>/dev/null || git checkout -B drive-sync origin/main
git rebase origin/main      # bring in anything pushed since; if it conflicts: git rebase --abort, report, stop
```
If `drive-sync` already existed, it holds changes Selly hasn't approved yet — keep them; tonight's changes go on top.

### 2. Find what changed
`search_files` with `parentId = '<folder id>'` and `excludeContentSnippets: true`. For each file compute `python3 sync/idhash.py <id> …` and match it to `manifest.docs.*.idhash`.
- A Doc **changed** if its `modifiedTime` is later than its `seen_modified`. If its title changed, update `name`.
- A file that isn't in the manifest (he made a new Doc, or something else landed in the folder): don't use it — list it under **Needs you** with its title.
- A Doc in the manifest that is **missing** (trashed or moved): change nothing; **Needs you**.

If nothing changed and there is no pending `drive-sync` work: reply with one line, "No changes in the Drive folder tonight.", and stop. If nothing changed but `drive-sync` has unapproved changes: one line reminding Selly they're waiting, and stop.

### 3. Read a changed Doc and diff it
1. Read it with the Google Docs `read_doc` tool (preferred: exact headings and tables). A large result is saved to a file for you — use that path. If it comes back inline, save the JSON exactly to `/tmp/<doc>.json`. (If `read_doc` fails, `read_file_content` from Drive works too: save its result the same way; retry once if it errors or comes back empty.)
2. `python3 sync/docs.py diff <doc> <file>`. The result has `changed`, `unchanged`, `new_sections`, `missing_sections`, `warnings`.
3. **Any `warnings` → apply nothing from this Doc tonight.** Put it under **Needs you** with what you saw (e.g. a section's number or heading style was lost, so it merged into the one before; the Doc was emptied; new sections in a Doc that doesn't take them).

### 4. Apply changed sections — pages and writings (`essays`, `poems`, `qene`, `numbers`, `pages`)
Each `changed` entry has a `key` and the `changes` (from `blocks.py`). For each change:
- **Where the text lives.** `python3 sync/blocks.py show <key>` lists the site's blocks; `at_site_block` indexes into it. Block 0/1 of a section page are the page title and lede: those live in `site.json` → `pages.<key>.heading` (or `label`) and `pages.<key>.lede` (or `description`), each with `am` and `en`. A writing's title lives in `content/writings.json`. Everything else is in `content/<key>.html` (pages) or `content/writings/<slug>.html`; find it by searching for a distinctive phrase of the old Amharic.
- **How Amharic and English are paired** — keep these patterns exactly:
  - `<div lang="am"> …blocks… </div>` then `<div lang="en"> …the same blocks in the same order… </div>` (writings, long passages);
  - `<p lang="am">…</p>` immediately followed by `<p lang="en">…</p>`;
  - inline pairs `<span lang="am">…</span><span lang="en">…</span>` (headings, table cells, labels);
  - poems: `<div class="verse" lang="am">` one line per line, then `<div class="verse" lang="en">` with the same number of lines.
- **Edit**: change the Amharic to the Doc's text **exactly** (don't correct his spelling or punctuation), then rewrite only the English partner of that block, following `GLOSSARY.md` and the tone of the surrounding English. Don't touch the English of blocks he didn't change.
- **Insert**: add the new block(s) in the same place, with both languages, following the neighbouring blocks' pattern (a new qene: an `h2` with its name, then its lines, as the existing qene are).
- **Delete**: if the Doc dropped blocks, do **not** delete them from the site; list them under **Needs you** ("Dad removed this paragraph — remove it from the site?").
- **Tables** (Numbers, Key): apply cell changes precisely and list every changed row in the summary.

### 5. Apply changed sections — books and paintings (`books`, `paintings`)
Each `changed` entry has a `slug` and `changes` keyed by the Doc's label, each with `site`, `doc` and `field`:
- `title` → `title.am`; translate `title.en` (keep `<i>…</i>` around a transliterated book name, as the existing titles do). A painting titled `[ርእስ]` is a placeholder he is now filling in.
- Plain fields (`year`, `pages`, `price`) copy as they are. `sold_out` / `newest` are "አዎ" (yes) or empty → `true` or remove the key. Only one book may be `newest`.
- Amharic text fields (`sub`, `publisher`, `motto`, `medium`) → set `am`, translate `en` (printers: reuse the English names already in the file; medium: "oil on canvas", "acrylic", etc.).
- `about` → `{"am": paragraphs joined with "\n", "en": the same paragraphs translated, joined with "\n"}`.

### 6. New sections
`python3 sync/docs.py section <doc> <file> <N> > /tmp/new.md` prints it (first line is its title). Ignore an empty one (he may still be writing) — mention it.
- **New essay / poem** (`essays`, `poems`):
  1. Translate the title; slug from the English title (lowercase ASCII, hyphens, ≤ 5 words, unique among `content/writings/`).
  2. Write `content/writings/<slug>.html` — essay: `<!-- <English title> — edit the Amharic in lang="am", the English in lang="en". -->`, then `<div lang="am">` one `<p>` per paragraph (`<h3>` for his headings), then `<div lang="en">` with the same blocks translated. Poem: copy the structure of `content/writings/fruit-of-peace.html`. If the last line names a source (a book and year), make it `<p class="cite"><span lang="am">…</span><span lang="en">…</span></p>` as in the existing writings.
  3. Add `{"slug": …, "kind": "essay"|"poem", "title": {"am": …, "en": …}}` at the **top** of `content/writings.json` — that makes it "Latest" on the home page.
  4. Add `"<N>": "writings/<slug>"` to `manifest.docs.<doc>.sections`.
- **New book / painting**: slug from the English title; add it to the JSON (a new book goes **first** in `books.json`; a painting goes last), with the fields from the section; add `"<N>": "<slug>"` to the manifest sections. Photos come later from Selly in chat: until then a book gets a drawn cover; a painting without a photo can't be shown — say so under **Needs you**.
- **New section in `qene`, `numbers` or `pages`**: don't guess — **Needs you**.

### 7. Check, build, push the branch
- Re-run `docs.py diff` for every Doc you applied: it must report nothing except deletions you held back. Fix anything else before moving on. Then set the Doc's `seen_modified` to its `modifiedTime`.
- `python3 build.py` — must succeed.
- Screenshot each changed page at desktop (1280 wide) and phone (390 wide), Amharic, and for writings/pages also English: `python3 -m http.server 8765 &`, Playwright `chromium.launch()`, full page. Look at them yourself: nothing broken, no missing English, no empty blocks.
- Update `last_run` in the manifest, then:
```
git add -A && git commit -m "Drive sync <date>: <short list>"
git push --force-with-lease origin drive-sync
```
Never push to `main` in the nightly run.

### 8. The message to Selly
Write it for her to read on her phone. Plain, short, in this order:
1. **One line:** what changed tonight (e.g. "Dad edited the Introduction and added a new poem.").
2. **Each change:** the Doc and section; for edits, the words removed/added in Amharic (the `words` from the diff) and the new English sentence(s); for something new, its title in both languages and the full English. Send the screenshots of the changed pages.
3. **Needs you:** deletions held back, warnings, unknown files, photos needed — each with exactly what to do.
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
- **"skip" / "don't publish" something Dad changed**: revert that change on the branch and add an entry to `sync/overrides.json` — `{"key": "<page or writings/slug>", "doc": "<the Doc block's text>", "site": "<the site block's text>", "note": "<why>"}` (one entry per block, texts exactly as `blocks.py` prints them) — so it isn't proposed again until the Doc changes. Mention it in "Still different" each night.
- **"remove it"** for a held deletion: remove the block (both languages), push the branch, wait for "push".

## Rules

- Never change his Amharic except to match his Doc exactly. Never "fix" his spelling.
- Never delete content, pages, writings or photos without Selly saying so.
- Never push to `main` without Selly's "push" in this conversation.
- Never edit his Docs, except to repair something only when Selly asks.
- If anything is unclear or a step fails, stop that part, keep the rest, and explain under **Needs you**.
- Claude sessions that change Amharic directly in the repo (outside this sync) must add an override and tell Selly to copy the change into the Doc — the Doc is the master copy of the Amharic.
