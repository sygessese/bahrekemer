# bahrekemer.com — notes for Claude

- Static site built by `python3 build.py` (stdlib only) from `site.json` and `content/`. GitHub Pages serves `main`.
- **Never push to `main` unless Selly says "push"** in the conversation. Build, screenshot and show her first.
- **The Amharic is owned by Google Docs.** Yitbarek edits his text in seven Docs in a shared Drive folder (essays, poems, Qene, books, paintings, Numbers & Key, other pages — see `sync/docs.py`); a nightly scheduled task (`sync/PROCEDURE.md`) brings changes in on the `drive-sync` branch, writes the English, and waits for Selly's "push".
  - Design, layout, code and English can be changed here freely.
  - If you change any **Amharic** here, the Doc will disagree with the site. Add an entry to `sync/overrides.json` and give Selly the exact text to paste into the Doc.
  - Each Doc is numbered sections ("፩ · title"); `sync/manifest.json → docs.*.sections` maps each number to a page, writing, book or painting. If you add or remove a page, writing, book or painting, add or remove its section in the right Doc (Google Docs connector) and update the manifest in the same change.
  - Book and painting facts and descriptions come from the Docs ፬ · መጻሕፍት and ፭ · ሥዕሎች; keep `content/books.json` / `content/paintings.json` in step with them.
  - Home-page labels that are design, not his text, carry class `ui` so the sync skips them.
- Phones (≤640px) get a simplified layout for older readers; desktop is the editorial layout. Check both.
