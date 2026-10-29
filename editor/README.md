# The editor (bahrekemer.com/edit/)

Yitbarek edits the site's Amharic himself, on the real pages:

- **/edit/** — the login page (one password). After that his computer stays signed in for six months.
- **Every page** then opens in edit mode: a green bar on top, his text outlined, click and type, «አስቀምጥ» (Save).
  Book and painting pages also get a photo button and a "details" box (year, pages, printer, price, sold out, medium).
  The home page, Writings, Poetry, Books and Paintings get «＋ አዲስ …» buttons for a new essay, poem, book or painting.
- What he saved but isn't live yet shows in **blue**, so he can see it's kept.

Nothing he does reaches the live site by itself. The pieces:

| Piece | Where | What it does |
|---|---|---|
| `assets/edit/edit.js`, `edit.css` | the site | edit mode; only loaded where someone has logged in (`build.py → editor_loader`) |
| `editor/login.html` → `/edit/`, `/edit/new/` | the site | login page; the new-piece page |
| `editor/worker.js` | Cloudflare (free) | checks the password; files each save on the `dad-edits` branch (`edits/<id>.json`, photos in `edits/photos/`) |
| `sync/edits.py`, `sync/PROCEDURE.md` | the nightly task | turns those files into site changes on `site-sync`, writes the English, messages Selly, waits for "push" |

## One-time setup

### 1. A GitHub token for the worker
GitHub → Settings → Developer settings → **Fine-grained tokens** → Generate new token
- Name: `bahrekemer editor` · Expiration: 1 year (put a reminder in your calendar to renew it)
- Repository access: **Only select repositories** → `sygessese/bahrekemer`
- Permissions → Repository → **Contents: Read and write** (nothing else)
- Generate, and copy the token (`github_pat_…`). It's shown once.

### 2. The worker on Cloudflare
**Either** in the browser:
1. Sign up at dash.cloudflare.com (free). **Workers & Pages → Create → Create Worker**, name it `bahrekemer-editor`, **Deploy**.
2. **Edit code**, replace everything with the contents of `editor/worker.js`, **Deploy**.
3. **Settings → Variables and secrets → Add**:
   - Text: `REPO` = `sygessese/bahrekemer` · `BRANCH` = `dad-edits` · `ORIGINS` = `https://bahrekemer.com,https://www.bahrekemer.com`
   - Secret: `EDIT_PASSWORD` = his password · `SESSION_SECRET` = any long random string (e.g. `openssl rand -base64 32`) · `GITHUB_TOKEN` = the token from step 1
4. Copy the worker's address (`https://bahrekemer-editor.<you>.workers.dev`).

**Or** from a terminal (this also turns on the 5-tries-a-minute password limit in `wrangler.toml`):
```
cd editor
npx wrangler login
npx wrangler deploy
npx wrangler secret put EDIT_PASSWORD
npx wrangler secret put SESSION_SECRET
npx wrangler secret put GITHUB_TOKEN
```

### 3. Point the site at it
Put the worker address in `site.json → editor.api`, run `python3 build.py`, publish.

### 4. His computer
Open bahrekemer.com/edit/, type the password, let the browser save it, bookmark the page. Done.

## Changing things later
- **New password**: change the `EDIT_PASSWORD` secret. Computers already signed in stay signed in.
- **Sign every computer out**: change `SESSION_SECRET`.
- **Token expired** (saves fail with a GitHub error): make a new token (step 1) and replace `GITHUB_TOKEN`.
