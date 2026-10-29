# bahrekemer.com — notes for Claude

- Static site built by `python3 build.py` (stdlib only) from `site.json` and `content/`. GitHub Pages serves `main`.
- **Never push to `main` unless Selly says "push"** in the conversation. Build, screenshot and show her first.
- **Yitbarek edits his Amharic himself** in the site's editor (bahrekemer.com/edit/ — `editor/README.md`). His saves land on the `dad-edits` branch; a nightly scheduled task (`sync/PROCEDURE.md`) applies them on `site-sync`, writes the English, and waits for Selly's "push". Never merge `dad-edits`.
  - Design, layout, code and English can be changed here freely. The editor works on the built pages, so new page types need nothing special — but text inside links, `nav`, buttons, `.ui`, `.kicker`, tables and similar is deliberately not editable (`SKIP` in `assets/edit/edit.js`).
  - If you change his **Amharic** here, tell Selly (he'll see it in the editor).
- Phones (≤640px) get a simplified layout for older readers; desktop is the editorial layout. Check both.
