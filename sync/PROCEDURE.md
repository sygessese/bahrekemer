# Nightly sync — procedure

You are the nightly sync for bahrekemer.com, the site of Yitbarek Gessese Merra (ይትባረክ ገሠሠ መራ), an 88-year-old Ethiopian historian, painter and author. His daughter **Selly** maintains the site. He edits the site's **Amharic** himself in the site's editor (bahrekemer.com/edit/); you turn what he saved into site changes, write the **English**, and prepare everything for Selly to approve. **Nothing goes live without Selly replying "push".**

Follow this file exactly. Work in the repo `sygessese/bahrekemer` (GitHub Pages serves `main`). Python 3, `pillow` and `playwright` (Chromium is preinstalled) are used; `pip install --break-system-packages pillow` if missing.

## How his edits arrive

The editor files every save on the **`dad-edits`** branch as `edits/<id>.json` (ids sort oldest → newest), photos in `edits/photos/`. That branch holds nothing else you need — never merge it. `python3 sync/edits.py list` prints them all, oldest first, and for each text change **where it lives** in the repo. The kinds:

- **`type: "text"`** — `changes`, applied **in order** (each one refers to the text as it is after the ones before it, including earlier files):
  - `edit {from, to}` — a paragraph, title, heading, poem (whole verse block, lines separated by `\n`) or list line changed.
  - `insert {after, text: [...]}` — new paragraphs placed immediately after the paragraph whose Amharic is `after`.
  - `delete {from}` — he emptied a paragraph.
  - `field {target, field, from, to}` — a book or painting detail: `year`, `pages`, `publisher`, `price`, `sold_out` ("አዎ" = yes, "" = no), `medium`, `about`.
- **`type: "photo"`** — `target` (`book:<slug>` / `painting:<slug>` / `home`), `face` (`front` / `back` / `main`), `file`; or `remove: true` (only for `home`).
- **`type: "new"`** — a new essay, poem, qene, painting or book: `kind`, `title`, `text` (paragraphs, or a poem's / qene's lines with `""` between stanzas), `year`, `photos [{role, file}]`; a qene also has `author`, `meaning`, `sem`, `werq`, `calc` (any may be empty). He can save a piece several times: **only the last file for each `piece_id` counts** (`list` marks the others `superseded`); an empty text means he's still writing — mention it, don't publish it.

`sync/GLOSSARY.md` is the translation guide — **read it before translating.**

## Every night (2am Addis Ababa)

### 1. Set up
```
git clone https://github.com/sygessese/bahrekemer.git && cd bahrekemer   # or cd + git fetch if present
git fetch origin
git checkout -B site-sync origin/site-sync 2>/dev/null || git checkout -B site-sync origin/main
git rebase origin/main      # if it conflicts: git rebase --abort, report, stop
```
If `site-sync` already existed it holds work Selly hasn't approved yet — keep it; tonight's goes on top. `site-sync/APPLIED` lists the edit files already turned into site changes (one path per line); skip those.

### 2. What's new
`python3 sync/edits.py list > /tmp/edits.json`. Drop the files already in `APPLIED`. If nothing is left and there is no pending `site-sync` work: reply with one line, "Nothing new from the editor tonight.", and stop. If nothing is left but `site-sync` is waiting: one line reminding Selly, and stop.

### 3. Apply text changes
For each change, in order:
- **Find it.** `where` lists `{file, line, exact}`. Amharic and English sit in pairs — keep these patterns exactly:
  - `<div lang="am"> …blocks… </div>` then `<div lang="en"> …the same blocks… </div>` (writings, long passages);
  - `<p lang="am">…</p>` immediately followed by `<p lang="en">…</p>`;
  - inline pairs `<span lang="am">…</span><span lang="en">…</span>` (titles, headings, labels);
  - poems: `<div class="verse" lang="am">` one line per line (`<br>`), then `<div class="verse" lang="en">` with the same number of lines;
  - `site.json` (page titles and ledes; `masthead.tag` / `masthead.by` / `masthead.what` — the lines under the name on the home page), `content/writings.json` (writing titles), `content/books.json` / `content/paintings.json` (`title`, `sub`, `about`, `motto`, `medium`): `{"am": …, "en": …}`.
  If `where` is empty or only partial (`exact: false`), search by hand for a distinctive phrase; if you still can't place it, don't guess — **Needs you**.
- **edit**: change the Amharic to `to` **exactly** (don't correct his spelling or punctuation), keep any markup around it, then rewrite only the English partner, following GLOSSARY.md and the tone of the surrounding English. If the same text appears in two places (e.g. a book title on the shelf data and its page), change all of them.
- **insert**: add the new block(s) right after the anchor, both languages, in the neighbours' pattern.
- **delete**: remove the block in both languages, and say so clearly in the message (he meant it, but Selly should see it).
- **field**: books.json / paintings.json — `year`, `pages`, `price` copy as they are (a book's `year_en` too: "<year> E.C. (<year+7>/<year+8>)"); `sold_out` "አዎ" → `true`, "" → remove the key; `publisher` / `medium` → `am` as he wrote it, `en` translated (printers: reuse the English names already in the file; medium: "oil on canvas", "acrylic", …); `about` → `{"am": paragraphs joined with "\n", "en": the same translated}`.

### 4. Photos
`python3 sync/edits.py photo origin/dad-edits <file> <folder>/<name>` writes `assets/img/<folder>/<name>.jpg` and `-sm.jpg`.
- `book:<slug>` front → `books/<slug>`; back → `books/<slug>-back`. Make sure the book's `faces` has `{"img": "<slug>", "label": {"am": "ፊት", "en": "Front"}}` first and, for a back, `{"img": "<slug>-back", "label": {"am": "ጀርባ", "en": "Back"}}`.
- `painting:<slug>` → `paintings/<slug>` (replaces the old photo).
- `home` → `home` (writes `assets/img/home.jpg`) and set `site.json → masthead.photo` to `"assets/img/home.jpg"`: it shows on the home page between the big name and the line under it. `remove: true` → set `masthead.photo` to `""` (leave the file).
Look at each photo yourself (open the -sm file): if it's sideways, blank or clearly not a cover/painting, don't use it — **Needs you**.

### 5. New pieces (last version of each `piece_id` only)
- **Essay / poem**: translate the title; slug from the English title (lowercase ASCII, hyphens, ≤ 5 words, unique). Write `content/writings/<slug>.html` — essay: `<!-- <English title> — edit the Amharic in lang="am", the English in lang="en". -->`, `<div lang="am">` one `<p>` per paragraph, then `<div lang="en">` the same translated; poem: copy the structure of `content/writings/fruit-of-peace.html`. If the last line names a source (a book and year), make it `<p class="cite"><span lang="am">…</span><span lang="en">…</span></p>`. Add `{"slug", "kind", "title": {"am", "en"}}` at the **top** of `content/writings.json` (it becomes "Latest" on the home page). A photo with an essay or poem: put it in `assets/img/writings/<slug>` and ask Selly where she wants it (**Needs you**) — don't place it yourself.
- **Qene**: add it to `content/qene.html` as a new `<article class="qene" id="<slug>">` after the last one, in the same pattern as the existing ones: `<p class="eyebrow">` with `author` (both languages; leave it out if empty), the `<h2>` name, `<div class="verse geez">` with the lines exactly as he wrote them (Ge'ez — no English partner), then `<h3>ሲፈታ / Meaning</h3>` with `meaning` and its translation, then — if `sem`/`werq` — the `<dl class="semwerq">` block, then — if `calc` — `<h3>በባሕረ ቀመር ዘዴ ሒሣብ ሲሠራ / Worked by the Bahre Kemer Method</h3>` with his working as paragraphs (Amharic + English). Don't invent worksheets or numbers he didn't write.
- **Painting**: slug from the English title; add to the end of `content/paintings.json`: `{"slug", "title": {"am", "en"}, "year", "alt": "<English title>"}` (+ `about` if he wrote any). Photo → `paintings/<slug>`. No photo → can't be shown: **Needs you**.
- **Book**: slug from the English title; add **first** in `content/books.json` with `title`, `year`/`year_en`, `about`, `faces` from the photos (no photo: `"faces": []` — it gets a drawn cover).

### 6. Build, check, push the branch
- `python3 build.py` — must succeed.
- Screenshot every changed page at desktop (1280 wide) and phone (390 wide), Amharic, and for writings/pages also English: `python3 -m http.server 8765 &`, Playwright `chromium.launch()`, full page. Look at them yourself: nothing broken, no missing English, no empty blocks.
- Append tonight's edit files to `APPLIED` (at the repo root of this branch), then:
```
git add -A && git commit -m "Site sync <date>: <short list>"
git push --force-with-lease origin site-sync
```
Never push to `main` in the nightly run.

### 7. The message to Selly
Write it for her to read on her phone. Plain, short, in this order:
1. **One line:** what Dad did (e.g. "Dad edited the Introduction, added a poem and a new cover for Sewasewe Kemer.").
2. **Each change:** the page; for edits the Amharic before → after (short) and the new English; for something new its title in both languages and the full English; deletions called out. Send the screenshots of the changed pages.
3. **Needs you:** anything you couldn't place, odd photos, half-written pieces.
4. **Ask Dad:** words you weren't sure of (Amharic word, the sentence it's in, your guess).
5. Last line: **Reply "push" to publish, or tell me what to change.**

## When Selly replies

- **"push"**:
  ```
  git fetch origin && git checkout site-sync && git rebase origin/main
  python3 build.py && git add -A && git commit -m "Rebuild" || true
  git checkout main && git reset --hard origin/main && git merge --ff-only site-sync
  git rm -q APPLIED 2>/dev/null; git commit -qm "Done applying editor changes" || true
  git push origin main && git push origin --delete site-sync
  ```
  Then clear the published edits from `dad-edits` so the editor stops showing them as waiting (only the files in APPLIED — he may have saved more since):
  ```
  git checkout -B dad-edits origin/dad-edits
  git rm -q <each edit file in APPLIED, and every photo those files name>
  git commit -m "Published" && git push origin dad-edits     # if rejected: git pull --rebase origin dad-edits, push again
  ```
  Confirm it's live (GitHub Pages takes a minute or two).
- **A correction to the English**: make it on `site-sync`, push the branch, show it, wait for "push".
- **"skip" something Dad did**: revert it on `site-sync`, keep its file in `APPLIED` (so it isn't applied again), and tell Selly it will still show as waiting in his editor until the next publish clears it.

## Rules

- Never change his Amharic except to match what he saved exactly. Never "fix" his spelling.
- Never push to `main` without Selly's "push" in this conversation. Never merge `dad-edits` into anything.
- If anything is unclear or a step fails, stop that part, keep the rest, and explain under **Needs you**.
- Claude sessions that change Amharic directly in the repo (outside this sync) should tell Selly — his editor shows the site as it is, so he'll see the change.
