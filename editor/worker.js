/* bahrekemer editor service — a Cloudflare Worker.
 *
 * The edit pages on bahrekemer.com talk to this. It checks Yitbarek's password and files what he saves on the
 * `dad-edits` branch of the GitHub repo (edits/<id>.json, photos in edits/photos/). It never touches `main`:
 * the nightly sync turns those files into site changes and Selly approves them (sync/PROCEDURE.md).
 *
 * Settings (Cloudflare → the worker → Settings → Variables and secrets):
 *   EDIT_PASSWORD   secret  his password
 *   SESSION_SECRET  secret  any long random string (signs his login; change it to log every computer out)
 *   GITHUB_TOKEN    secret  fine-grained token for this one repo, "Contents: Read and write"
 *   REPO            text    sygessese/bahrekemer
 *   BRANCH          text    dad-edits
 *   ORIGINS         text    https://bahrekemer.com,https://www.bahrekemer.com
 * Optional binding LOGIN_LIMIT (Rate limiting) — see editor/wrangler.toml.
 *
 *   POST /login    {password}            -> {token, exp}
 *   GET  /pending                        -> {edits: [...saved, oldest first]}
 *   POST /save     {type: text|photo|new, ...}   -> {ok, id, photos?}
 */
const DAYS = 180;
const MAX_PHOTO = 6 * 1024 * 1024;      // bytes, after his browser has resized it
const MAX_BODY = 20 * 1024 * 1024;

export default {
  async fetch(req, env) {
    const origin = req.headers.get('Origin') || '';
    const allowed = (env.ORIGINS || '').split(',').map(s => s.trim()).filter(Boolean);
    const cors = {
      'Access-Control-Allow-Origin': allowed.includes(origin) ? origin : (allowed[0] || '*'),
      'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, Authorization',
      'Access-Control-Max-Age': '86400',
      'Vary': 'Origin',
    };
    const json = (obj, status = 200) => new Response(JSON.stringify(obj), { status, headers: { ...cors, 'Content-Type': 'application/json; charset=utf-8' } });
    if (req.method === 'OPTIONS') return new Response(null, { status: 204, headers: cors });
    const path = new URL(req.url).pathname.replace(/\/+$/, '') || '/';
    try {
      if (path === '/login' && req.method === 'POST') return json(...await login(req, env));
      if (path === '/' ) return json({ ok: true, service: 'bahrekemer editor' });
      if (!(await authed(req, env))) return json({ error: 'login' }, 401);
      if (path === '/pending' && req.method === 'GET') return json(await pending(env));
      if (path === '/save' && req.method === 'POST') {
        if (Number(req.headers.get('Content-Length') || 0) > MAX_BODY) return json({ error: 'too big' }, 413);
        return json(await save(await req.json(), env));
      }
      return json({ error: 'not found' }, 404);
    } catch (e) {
      return json({ error: String(e && e.message || e) }, e && e.status || 500);
    }
  },
};

// ---------------------------------------------------------------- login
const enc = new TextEncoder();
const b64url = buf => btoa(String.fromCharCode(...new Uint8Array(buf))).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
async function hmac(secret, msg) {
  const key = await crypto.subtle.importKey('raw', enc.encode(secret), { name: 'HMAC', hash: 'SHA-256' }, false, ['sign']);
  return b64url(await crypto.subtle.sign('HMAC', key, enc.encode(msg)));
}
async function same(a, b, secret) {   // constant-time: compare the HMACs, not the strings
  return (await hmac(secret, 'cmp:' + a)) === (await hmac(secret, 'cmp:' + b));
}
async function login(req, env) {
  if (!env.EDIT_PASSWORD || !env.SESSION_SECRET) return [{ error: 'not set up' }, 500];
  const ip = req.headers.get('CF-Connecting-IP') || 'x';
  if (env.LOGIN_LIMIT) {
    const { success } = await env.LOGIN_LIMIT.limit({ key: ip });
    if (!success) return [{ error: 'slow' }, 429];
  }
  let body = {};
  try { body = await req.json(); } catch (e) {}
  const ok = typeof body.password === 'string' && await same(body.password, env.EDIT_PASSWORD, env.SESSION_SECRET);
  if (!ok) { await new Promise(r => setTimeout(r, 1200)); return [{ error: 'wrong' }, 403]; }
  const exp = Math.floor(Date.now() / 1000) + DAYS * 86400;
  return [{ token: exp + '.' + await hmac(env.SESSION_SECRET, 'v1.' + exp), exp }, 200];
}
async function authed(req, env) {
  const m = /^Bearer (\d+)\.([\w-]+)$/.exec(req.headers.get('Authorization') || '');
  if (!m || !env.SESSION_SECRET || Number(m[1]) * 1000 < Date.now()) return false;
  return (await hmac(env.SESSION_SECRET, 'v1.' + m[1])) === m[2];
}

// ---------------------------------------------------------------- GitHub
async function gh(env, method, path, body) {
  const r = await fetch(`https://api.github.com/repos/${env.REPO}${path}`, {
    method,
    headers: {
      'Authorization': `Bearer ${env.GITHUB_TOKEN}`,
      'Accept': 'application/vnd.github+json',
      'X-GitHub-Api-Version': '2022-11-28',
      'User-Agent': 'bahrekemer-editor',
      ...(body ? { 'Content-Type': 'application/json' } : {}),
    },
    body: body ? JSON.stringify(body) : undefined,
  });
  if (r.status === 404) return null;
  const j = await r.json().catch(() => ({}));
  if (!r.ok) { const e = new Error(`GitHub ${r.status}: ${j.message || ''}`); e.status = r.status === 409 ? 409 : 502; throw e; }
  return j;
}
async function ensureBranch(env) {
  const b = env.BRANCH || 'dad-edits';
  if (await gh(env, 'GET', `/git/ref/heads/${b}`)) return b;
  const repo = await gh(env, 'GET', '');
  const head = await gh(env, 'GET', `/git/ref/heads/${repo.default_branch}`);
  await gh(env, 'POST', '/git/refs', { ref: `refs/heads/${b}`, sha: head.object.sha });
  return b;
}
async function put(env, branch, path, base64, message) {
  for (let i = 0; i < 4; i++) {   // two saves at once can race on the branch; try again
    try { return await gh(env, 'PUT', `/contents/${path}`, { message, content: base64, branch, committer: { name: 'Bahrekemer editor', email: 'editor@bahrekemer.com' } }); }
    catch (e) { if (e.status !== 409 || i === 3) throw e; await new Promise(r => setTimeout(r, 400 * (i + 1))); }
  }
}
const utf8b64 = s => { const b = enc.encode(s); let out = ''; for (let i = 0; i < b.length; i += 0x8000) out += String.fromCharCode(...b.subarray(i, i + 0x8000)); return btoa(out); };
const fromb64 = s => new TextDecoder().decode(Uint8Array.from(atob(s.replace(/\s/g, '')), c => c.charCodeAt(0)));

async function pending(env) {
  const b = env.BRANCH || 'dad-edits';
  const list = await gh(env, 'GET', `/contents/edits?ref=${b}`);
  if (!Array.isArray(list)) return { edits: [] };
  const files = list.filter(f => f.type === 'file' && f.name.endsWith('.json')).map(f => f.path).sort();
  const edits = await Promise.all(files.map(async p => {
    const f = await gh(env, 'GET', `/contents/${p}?ref=${b}`);
    try { return f && JSON.parse(fromb64(f.content)); } catch (e) { return null; }
  }));
  return { edits: edits.filter(Boolean) };
}

// ---------------------------------------------------------------- save
const str = (v, max = 20000) => typeof v === 'string' ? v.slice(0, max) : '';
function bad(msg) { const e = new Error(msg); e.status = 400; return e; }
function photoBytes(data) {
  const m = /^data:image\/(jpeg|png|webp);base64,([A-Za-z0-9+/=]+)$/.exec(data || '');
  if (!m) throw bad('photo');
  if (m[2].length * 0.75 > MAX_PHOTO) throw bad('photo too big');
  return { ext: m[1] === 'jpeg' ? 'jpg' : m[1], b64: m[2] };
}
async function save(body, env) {
  const branch = await ensureBranch(env);
  const now = new Date();
  const id = now.toISOString().replace(/[-:]/g, '').replace(/\.\d+Z$/, 'Z') + '-' + Math.random().toString(36).slice(2, 7);
  const rec = { id, at: now.toISOString(), type: body.type, page: str(body.page, 300) };
  const out = { ok: true, id };
  const savePhoto = async (data, label) => {
    const p = photoBytes(data);
    const file = `edits/photos/${id}-${label}.${p.ext}`;
    await put(env, branch, file, p.b64, `Editor: photo (${label})`);
    return file;
  };
  if (body.type === 'text') {
    if (!Array.isArray(body.changes) || !body.changes.length || body.changes.length > 500) throw bad('changes');
    rec.key = str(body.key, 200);
    rec.changes = body.changes.map(c => {
      const op = str(c.op, 10);
      if (op === 'edit') return { op, from: str(c.from), to: str(c.to) };
      if (op === 'delete') return { op, from: str(c.from) };
      if (op === 'insert' && Array.isArray(c.text)) return { op, after: str(c.after), text: c.text.slice(0, 200).map(t => str(t)) };
      if (op === 'field') return { op, target: str(c.target, 200), field: str(c.field, 40), from: str(c.from, 4000), to: str(c.to, 4000) };
      throw bad('op');
    });
  } else if (body.type === 'photo') {
    rec.target = str(body.target, 200);
    rec.face = ['front', 'back', 'main'].includes(body.face) ? body.face : 'main';
    if (body.remove === true) rec.remove = true;
    else rec.file = await savePhoto(body.photo && body.photo.data, rec.face);
  } else if (body.type === 'new') {
    rec.piece_id = str(body.id, 60) || id;
    rec.kind = ['essay', 'poem', 'qene', 'painting', 'book'].includes(body.kind) ? body.kind : 'essay';
    if (rec.kind === 'qene') for (const f of ['author', 'meaning', 'sem', 'werq', 'calc']) rec[f] = str(body[f]);
    rec.title = str(body.title, 500); rec.year = str(body.year, 10);
    rec.text = Array.isArray(body.text) ? body.text.slice(0, 2000).map(t => str(t)) : [];
    rec.photos = [];
    for (const p of (Array.isArray(body.photos) ? body.photos.slice(0, 4) : [])) {
      const role = ['front', 'back', 'main'].includes(p.role) ? p.role : 'main';
      if (p.data) rec.photos.push({ role, file: await savePhoto(p.data, role) });
      else if (typeof p.file === 'string' && /^edits\/photos\/[\w.-]+$/.test(p.file)) rec.photos.push({ role, file: p.file });
    }
    out.photos = rec.photos;
  } else throw bad('type');
  await put(env, branch, `edits/${id}.json`, utf8b64(JSON.stringify(rec, null, 1)), `Editor: ${rec.type} ${rec.page || ''}`.trim());
  return out;
}
