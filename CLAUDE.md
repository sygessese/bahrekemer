# bahrekemer.com — notes for Claude

- Static site built by `python3 build.py` (stdlib only) from `site.json` and `content/`. GitHub Pages serves `main`.
- **Never push to `main` unless Selly says "push"** in the conversation. Build, screenshot and show her first.
- **The Amharic is owned by Google Docs.** Yitbarek edits his text in a shared Drive folder; a nightly scheduled task (`sync/PROCEDURE.md`) brings changes in on the `drive-sync` branch, writes the English, and waits for Selly's "push".
  - Design, layout, code and English can be changed here freely.
  - If you change any **Amharic** here, the Doc will disagree with the site. Add an entry to `sync/overrides.json` and give Selly the exact text to paste into the Doc.
  - If you add, rename or remove a page or writing, mirror it in Drive (create/rename/trash the Doc) and update `sync/manifest.json` in the same change.
  - Book and painting facts come from the Google Sheet "መጻሕፍትና ሥዕሎች"; keep `content/books.json` / `content/paintings.json` in step with it.
- Phones (≤640px) get a simplified layout for older readers; desktop is the editorial layout. Check both.
