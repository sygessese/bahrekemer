/* Edit mode for bahrekemer.com — for Yitbarek, on a computer that has logged in at /edit/.
 *
 * The real pages, with his Amharic made click-to-type. "አስቀምጥ" (Save) sends what changed on the page to the
 * editor service (editor/worker.js), which files it on the `dad-edits` branch. Nothing reaches the live site
 * until the nightly sync has written the English and Selly has said "push" (sync/PROCEDURE.md).
 *
 * What a save sends ({type: "text"}): changes, applied in order —
 *   {op: "edit",   from, to}        a paragraph/title/line changed (from = its text before)
 *   {op: "insert", after, text: []} new paragraphs right after the paragraph whose text is `after`
 *   {op: "delete", from}            a paragraph emptied
 *   {op: "field",  target, field, from, to}   a book/painting detail (year, pages, …)
 * Other saves: {type: "photo", target, face, photo} and {type: "new", id, kind, title, text, year, photos}.
 */
(function () {
  'use strict';
  var LOCAL = /^(localhost|127\.0\.0\.1|\[::1\])$/.test(location.hostname);
  // On a local preview with no editor service set up, a practice mode keeps saves in this browser only.
  var API = window.BK_EDITOR_API || (LOCAL ? 'demo' : ''), RAW = window.BK_RAW || '';
  var DEMO = API === 'demo';
  function src(file) { return /^data:/.test(file) ? file : RAW + file; }
  var me = document.currentScript;
  var ROOT = me ? me.src.replace(/assets\/edit\/edit\.js.*$/, '') : '/';
  var d = document.documentElement, main = document.getElementById('main');
  if (!main) return;
  var KEY = main.getAttribute('data-ed') || '';
  var FIELDS = {};
  try { FIELDS = JSON.parse(main.getAttribute('data-fields') || '{}'); } catch (e) {}

  // ---------------------------------------------------------------- session
  function session() {
    try { var s = JSON.parse(localStorage.getItem('bk-ed')); return s && s.exp * 1000 > Date.now() && (s.token === 'demo') === (API === 'demo') ? s : null; } catch (e) { return null; }
  }
  var S = session();
  if (!S) {
    try { localStorage.removeItem('bk-ed'); } catch (e) {}
    var b0 = document.createElement('div'); b0.className = 'edbar';
    b0.innerHTML = '<div class="edbar-in"><span class="edbar-tag">✎ ማስተካከያ</span><span class="edbar-hint">ለማስተካከል እንደገና መግባት ያስፈልጋል።</span>' +
      '<a class="ed-btn" href="' + ROOT + 'edit/">ግባ</a></div>';
    document.body.prepend(b0);
    return;
  }
  d.classList.add('editing'); d.setAttribute('data-lang', 'am'); d.setAttribute('data-read', 'am'); d.lang = 'am';
  try { localStorage.setItem('lang', 'am'); } catch (e) {}

  // ---------------------------------------------------------------- helpers
  function norm(s) {
    return (s || '').replace(/ /g, ' ').replace(/\r/g, '').replace(/[ \t]+/g, ' ')
      .replace(/ *\n */g, '\n').replace(/\n{3,}/g, '\n\n').trim();
  }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function el(tag, cls, html) { var e = document.createElement(tag); if (cls) e.className = cls; if (html != null) e.innerHTML = html; return e; }
  function isVerse(b) { return b.matches('div.verse'); }
  function textOf(b) { return isVerse(b) ? norm(b.innerText).replace(/\n\n+/g, '\n') : norm(b.innerText).replace(/\n+/g, ' '); }
  function setText(b, t) { if (isVerse(b)) b.innerHTML = t.split('\n').map(esc).join('<br>'); else b.textContent = t; }

  function demoCall(path, body) {
    var all = [];
    try { all = JSON.parse(localStorage.getItem('bk-ed-demo') || '[]'); } catch (e) {}
    if (path === '/pending') return Promise.resolve({ edits: all });
    var rec = JSON.parse(JSON.stringify(body)), out = { ok: true };
    rec.id = new Date().toISOString().replace(/[-:.]/g, '') + Math.random().toString(36).slice(2, 6); out.id = rec.id;
    if (rec.type === 'photo') { rec.file = rec.photo.data; delete rec.photo; }
    if (rec.type === 'new') { rec.piece_id = body.id; rec.photos = (rec.photos || []).map(function (p) { return { role: p.role, file: p.data || p.file }; }); out.photos = rec.photos; }
    all.push(rec);
    try { localStorage.setItem('bk-ed-demo', JSON.stringify(all)); }
    catch (e) { return Promise.reject(new Error('full')); }
    return new Promise(function (res) { setTimeout(function () { res(out); }, 300); });
  }
  function call(path, body) {
    if (DEMO) return demoCall(path, body);
    var opt = { headers: { 'Authorization': 'Bearer ' + S.token } };
    if (body) { opt.method = 'POST'; opt.headers['Content-Type'] = 'application/json'; opt.body = JSON.stringify(body); }
    return fetch(API + path, opt).then(function (r) {
      return r.json().catch(function () { return {}; }).then(function (j) {
        if (r.status === 401) { var e = new Error('login'); e.login = true; throw e; }
        if (!r.ok) throw new Error(j.error || ('HTTP ' + r.status));
        return j;
      });
    });
  }
  function toast(html, bad, ms) {
    var t = el('div', 'ed-toast' + (bad ? ' bad' : ''), html);
    document.body.appendChild(t);
    setTimeout(function () { t.remove(); }, ms || 5000);
  }
  function modal(title, text, buttons) {
    var bg = el('div', 'ed-modal-bg'), m = el('div', 'ed-modal');
    m.appendChild(el('h2', '', esc(title)));
    if (text) m.appendChild(el('p', '', esc(text)));
    var bs = el('div', 'ed-modal-btns');
    buttons.forEach(function (b) {
      var x = el('button', b.cancel ? 'ed-cancel' : 'ed-btn' + (b.line ? ' ed-btn-line' : ''), esc(b.label));
      x.type = 'button';
      x.onclick = function () { bg.remove(); if (b.go) b.go(); };
      bs.appendChild(x);
    });
    m.appendChild(bs); bg.appendChild(m);
    bg.addEventListener('click', function (e) { if (e.target === bg) bg.remove(); });
    document.body.appendChild(bg);
    return bg;
  }
  function failed(err) {
    if (err && err.login) {
      modal('እንደገና መግባት ያስፈልጋል', 'ለውጡ አልተቀመጠም። እባክዎ እንደገና ይግቡ።', [{ label: 'ግባ', go: function () { location.href = ROOT + 'edit/'; } }, { label: 'ተመለስ', cancel: true }]);
    } else {
      toast('አልተቀመጠም ✗<small>ኢንተርኔቱን አረጋግጠው «አስቀምጥ»ን እንደገና ይጫኑ።</small>', true, 8000);
    }
  }
  function readImage(file) {
    return new Promise(function (res, rej) {
      var url = URL.createObjectURL(file), img = new Image();
      img.onload = function () {
        var w = img.naturalWidth, h = img.naturalHeight, s = Math.min(1, 2000 / Math.max(w, h));
        var c = document.createElement('canvas'); c.width = Math.round(w * s); c.height = Math.round(h * s);
        c.getContext('2d').drawImage(img, 0, 0, c.width, c.height);
        URL.revokeObjectURL(url); res(c.toDataURL('image/jpeg', 0.88));
      };
      img.onerror = function () { URL.revokeObjectURL(url); rej(new Error('image')); };
      img.src = url;
    });
  }
  function pickImage() {
    return new Promise(function (res) {
      var i = el('input'); i.type = 'file'; i.accept = 'image/*';
      i.onchange = function () {
        if (!i.files[0]) return;
        readImage(i.files[0]).then(res, function () { toast('ይህን ፎቶ መክፈት አልተቻለም። ሌላ ፎቶ ይሞክሩ።', true); });
      };
      i.click();
    });
  }

  // ---------------------------------------------------------------- the bar
  var bar = el('div', 'edbar');
  bar.innerHTML = '<div class="edbar-in"><span class="edbar-tag">✎ ማስተካከያ</span>' +
    '<span class="edbar-hint">መቀየር የሚፈልጉትን ጽሑፍ ይጫኑና ይጻፉ። ሲጨርሱ «አስቀምጥ»ን ይጫኑ።</span>' +
    '<span class="edbar-status">ምንም ለውጥ የለም</span><button class="ed-btn ed-btn-save off" type="button">አስቀምጥ</button>' +
    '<button class="ed-btn-out" type="button">ውጣ</button></div>';
  document.body.prepend(bar);
  var statusEl = bar.querySelector('.edbar-status'), saveBtn = bar.querySelector('.ed-btn-save');
  var busy = false, extraDirty = null;   // extraDirty: a function the new-piece page sets

  // ---------------------------------------------------------------- editable blocks
  var SKIP = 'nav, footer, .ui, .kicker, .label, .byline, .source, .reader, .phone-end, .pb-bottom, .phone-home, ' +
    '.flip-tabs, .more-link, .prevnext, .enquire, .wlist, .writings-list, .book-strip, .paint-strip, .sec-head, .pt-back, ' +
    '.pt-meta, .shelf, .gallery, .newest-links, .rule-head, .contents, table, .edbar, .ed-adds, .ed-pending-list, .ed-fields, ' +
    'a, button, .cover, .shelf-meta, .end-mark, .all-link, .key-toc, .cite, .newp, .worksheet, .grand';
  var blocks = [], nextId = 1, fieldInputs = [];

  function mark(b, orig) {
    b.classList.add('ed'); b.contentEditable = 'true'; b.spellcheck = false;
    b.setAttribute('data-ph', 'ጽሑፍ ይጻፉ…');
    b.dataset.bid = String(nextId++);
    b.dataset.orig = orig != null ? orig : textOf(b);
    b.addEventListener('input', function () { refresh(b); });
    b.addEventListener('keydown', keys);
    b.addEventListener('paste', paste);
    blocks.push(b);
    return b;
  }
  if (KEY !== 'edit-new') {
    main.querySelectorAll('h1, h2, h3, h4, p, li, dt, dd, blockquote, div.verse').forEach(function (x) {
      if (x.closest(SKIP)) return;
      if (x.matches('div.verse') && x.getAttribute('lang') !== 'am' && !x.classList.contains('geez')) return;
      if (!x.matches('div.verse') && x.closest('div.verse')) return;
      if (x.matches('blockquote') && x.querySelector('p')) return;
      var t = x.querySelector(':scope > span[lang="am"]') || x;
      if (t.closest('[lang="en"]')) return;
      if (t === x && x.querySelector('p, div, ul, ol, h1, h2, h3, table, figure')) return;
      if (!textOf(t)) return;
      var a = t.querySelector('a');
      if (a && norm(a.innerText) === textOf(t)) return;   // a paragraph that is only a link
      mark(t);
    });
  }

  if (KEY === 'index') document.querySelectorAll('.masthead .mast-tag, .masthead .mast-by').forEach(function (x) { mark(x); });

  function changedCount() {
    var n = blocks.filter(function (b) { return b.isConnected && (b.dataset.isNew ? !!textOf(b) : textOf(b) !== b.dataset.orig); }).length;
    n += fieldInputs.filter(function (f) { return f.value() !== f.orig; }).length;
    if (extraDirty) n += extraDirty();
    return n;
  }
  function refresh(b) {
    if (b) b.classList.toggle('changed', b.dataset.isNew ? !!textOf(b) : textOf(b) !== b.dataset.orig);
    var n = changedCount();
    statusEl.className = 'edbar-status' + (n ? ' dirty' : '');
    if (n) delete statusEl.dataset.auto;
    statusEl.textContent = n ? (n === 1 ? '1 ለውጥ — ገና አልተቀመጠም' : n + ' ለውጦች — ገና አልተቀመጡም') : (statusEl.dataset.auto ? 'በራሱ ተቀምጧል ✓' : 'ምንም ለውጥ የለም');
    saveBtn.classList.toggle('off', !n || busy);
  }

  function keys(e) {
    var b = e.currentTarget;
    if (e.key !== 'Enter') return;
    if (isVerse(b)) { e.preventDefault(); document.execCommand('insertLineBreak'); return; }
    e.preventDefault();
    if (b.tagName !== 'P') return;            // titles and list lines stay one line
    var sel = getSelection(); if (!sel.rangeCount) return;
    var r = sel.getRangeAt(0); r.deleteContents();
    var rest = document.createRange(); rest.setStart(r.endContainer, r.endOffset); rest.setEnd(b, b.childNodes.length);
    var frag = rest.extractContents();
    var np = el(b.tagName, b.className.replace(/\b(ed|changed|pending)\b/g, '').trim());
    np.appendChild(frag);
    b.after(np);
    mark(np, '');
    np.dataset.isNew = '1';
    np.dataset.anchor = b.dataset.isNew ? b.dataset.anchor : b.dataset.bid;
    var c = document.createRange(); c.setStart(np, 0); c.collapse(true); sel.removeAllRanges(); sel.addRange(c);
    np.focus(); refresh(b); refresh(np);
  }
  function paste(e) {
    e.preventDefault();
    var t = (e.clipboardData || window.clipboardData).getData('text/plain') || '';
    if (!isVerse(e.currentTarget)) t = t.replace(/\s*\n\s*/g, ' ');
    document.execCommand('insertText', false, t);
  }

  // ---------------------------------------------------------------- book and painting details
  function addFields() {
    var isBook = KEY.indexOf('book:') === 0, isPainting = KEY.indexOf('painting:') === 0;
    if (!isBook && !isPainting) return;
    var host = main.querySelector('.pt-caption') || main.querySelector('.pt-figure figcaption') || main.querySelector('.painting-page');
    if (!host) return;
    var box = el('div', 'ed-fields');
    var defs = isBook
      ? [['year', 'ዓመት (ዓ.ም.)', 'num'], ['pages', 'ገጽ', 'num'], ['publisher', 'ማተሚያ ቤት', 'text'], ['price', 'ዋጋ (ብር)', 'num'], ['sold_out', 'ተሸጦ አልቋል', 'check']]
      : [['year', 'ዓመት', 'num'], ['medium', 'ቅብ (ዘይት፣ አክሬሊክ…)', 'text']];
    if (!FIELDS.has_about) defs.push(['about', isBook ? 'ስለ መጽሐፉ' : 'ስለ ሥዕሉ', 'area']);
    box.innerHTML = '<p class="ed-fields-h">ዝርዝር</p>';
    defs.forEach(function (f) {
      var row = el('label', 'ed-field'), inp;
      row.appendChild(el('span', '', esc(f[1])));
      if (f[2] === 'check') { inp = el('input'); inp.type = 'checkbox'; inp.checked = !!FIELDS[f[0]]; }
      else if (f[2] === 'area') { inp = el('textarea'); inp.rows = 4; inp.value = ''; }
      else { inp = el('input'); inp.type = 'text'; inp.value = FIELDS[f[0]] || ''; if (f[2] === 'num') inp.inputMode = 'numeric'; }
      row.appendChild(inp); box.appendChild(row);
      var rec = { field: f[0], inp: inp, value: function () { return f[2] === 'check' ? (inp.checked ? 'አዎ' : '') : norm(inp.value); } };
      rec.orig = rec.value();
      inp.addEventListener('input', function () { refresh(); }); inp.addEventListener('change', function () { refresh(); });
      fieldInputs.push(rec);
    });
    host.appendChild(box);
  }
  addFields();

  // ---------------------------------------------------------------- save (text and details)
  function collect() {
    var ch = [];
    blocks.forEach(function (b) {
      if (!b.isConnected || b.dataset.isNew) return;
      var cur = textOf(b), orig = b.dataset.orig, anchor = orig;
      var news = blocks.filter(function (n) { return n.isConnected && n.dataset.isNew && n.dataset.anchor === b.dataset.bid; })
        .map(textOf).filter(Boolean);
      if (cur !== orig) {
        if (!cur && news.length) { ch.push({ op: 'edit', from: orig, to: news[0] }); anchor = news.shift(); }
        else if (!cur) { ch.push({ op: 'delete', from: orig }); anchor = null; }
        else { ch.push({ op: 'edit', from: orig, to: cur }); anchor = cur; }
      }
      if (news.length && anchor) ch.push({ op: 'insert', after: anchor, text: news });
    });
    fieldInputs.forEach(function (f) {
      if (f.value() !== f.orig) ch.push({ op: 'field', target: KEY, field: f.field, from: f.orig, to: f.value() });
    });
    return ch;
  }
  function settle() {   // after a save: what he sees becomes the new "before", marked as waiting
    blocks.slice().forEach(function (b) {
      if (!b.isConnected) return;
      var cur = textOf(b);
      if (b.dataset.isNew && !cur) { b.remove(); return; }
      if (!b.dataset.isNew && !cur) { b.style.display = 'none'; return; }
      if (cur !== b.dataset.orig || b.dataset.isNew) b.classList.add('pending');
      b.dataset.orig = cur; delete b.dataset.isNew; delete b.dataset.anchor;
      b.classList.remove('changed');
    });
    fieldInputs.forEach(function (f) { f.orig = f.value(); });
  }
  function save() {
    if (busy || !changedCount()) return Promise.resolve();
    if (KEY === 'edit-new') return newSave();
    var ch = collect();
    if (!ch.length) { settle(); refresh(); return Promise.resolve(); }
    busy = true; saveBtn.textContent = 'በማስቀመጥ ላይ…'; refresh();
    return call('/save', { type: 'text', page: location.pathname, key: KEY, changes: ch })
      .then(function () {
        settle(); toast('ተቀምጧል ✓<small>ሰላም ካየችው በኋላ ድረ ገጹ ላይ ይወጣል።</small>');
      }, failed)
      .then(function () { busy = false; saveBtn.textContent = 'አስቀምጥ'; refresh(); });
  }
  saveBtn.addEventListener('click', save);

  // leaving with unsaved changes
  var leaving = false;
  window.addEventListener('beforeunload', function (e) { if (!leaving && changedCount()) { e.preventDefault(); e.returnValue = ''; } });
  document.addEventListener('click', function (e) {
    if (e.target.closest && e.target.closest('.ed') && e.target.closest('a[href]')) { e.preventDefault(); return; }   // typing, not following the link
    var a = e.target.closest && e.target.closest('a[href]');
    if (!a || !changedCount() || a.target === '_blank' || a.getAttribute('href').charAt(0) === '#') return;
    e.preventDefault();
    var go = function () { leaving = true; location.href = a.href; };
    modal('ያልተቀመጠ ለውጥ አለ', 'ከዚህ ገጽ ከመውጣትዎ በፊት ላስቀምጠው?', [
      { label: 'አስቀምጥና ቀጥል', go: function () { save().then(function () { if (!changedCount()) go(); }); } },
      { label: 'ሳላስቀምጥ ቀጥል', line: true, go: go },
      { label: 'ተመለስ', cancel: true }
    ]);
  }, true);
  bar.querySelector('.ed-btn-out').addEventListener('click', function () {
    var out = function () { try { localStorage.removeItem('bk-ed'); } catch (e) {} leaving = true; location.href = ROOT; };
    if (!changedCount()) return out();
    modal('ያልተቀመጠ ለውጥ አለ', 'ለውጡ ሳይቀመጥ ልውጣ?', [{ label: 'አስቀምጥ', go: save }, { label: 'ሳላስቀምጥ ውጣ', line: true, go: out }, { label: 'ተመለስ', cancel: true }]);
  });

  // ---------------------------------------------------------------- photos on book and painting pages
  // A photo saves the moment it's chosen (no «አስቀምጥ» needed), so say so plainly, next to the photo and in the bar.
  var PH_TEXT = { saving: 'ፎቶው እየተቀመጠ ነው…', saved: '✓ ፎቶው ተቀምጧል — ሰላም ካየችው በኋላ ድረ ገጹ ላይ ይወጣል።', bad: '✗ ፎቶው አልተቀመጠም — እባክዎ እንደገና ይሞክሩ።' };
  function photoFlag(anchor, state) {
    if (!anchor) return;
    var f = anchor._edFlag;
    if (!f) { f = anchor._edFlag = el('p', 'ed-flag ed-ph-flag'); anchor.before(f); }
    f.className = 'ed-flag ed-ph-flag' + (state === 'bad' ? ' bad' : state === 'saving' ? ' wait' : '');
    f.textContent = PH_TEXT[state];
    if (state !== 'saving' && !changedCount()) { statusEl.className = 'edbar-status ' + (state === 'bad' ? 'bad' : 'saved'); statusEl.textContent = state === 'bad' ? 'ፎቶው አልተቀመጠም' : 'ፎቶው ተቀምጧል ✓'; }
  }
  function photoButton() {
    var isBook = KEY.indexOf('book:') === 0, isPainting = KEY.indexOf('painting:') === 0;
    if (!isBook && !isPainting) return;
    var stage = main.querySelector('.flip-stage, .book-drawn, .pt-figure');
    if (!stage) return;
    stage.style.position = 'relative';
    var b = el('button', 'ed-btn ed-photo' + (isPainting ? ' ed-photo-top' : ''), '📷 ' + (isBook ? 'ፎቶ ጨምር ወይም ቀይር' : 'ፎቶውን ቀይር')); b.type = 'button';
    stage.appendChild(b);
    b.onclick = function () {
      var send = function (face) {
        pickImage().then(function (data) {
          showPhoto(face, data); photoFlag(stage, 'saving');
          call('/save', { type: 'photo', page: location.pathname, target: KEY, face: face, photo: { data: data } })
            .then(function () { photoFlag(stage, 'saved'); toast('ፎቶው ተቀምጧል ✓<small>ሰላም ካየችው በኋላ ድረ ገጹ ላይ ይወጣል።</small>', false, 8000); },
                  function (err) { photoFlag(stage, 'bad'); failed(err); });
        });
      };
      if (isPainting) return send('main');
      modal('የትኛውን ሽፋን?', '', [{ label: 'የፊት ሽፋን', go: function () { send('front'); } }, { label: 'የጀርባ ሽፋን', line: true, go: function () { send('back'); } }, { label: 'ተመለስ', cancel: true }]);
    };
  }
  function showPhoto(face, src) {
    var img;
    if (KEY.indexOf('painting:') === 0) img = main.querySelector('.pt-figure img');
    else {
      var f = main.querySelector('.flip-face[data-face="' + (face === 'back' ? 1 : 0) + '"] img');
      img = f || (face === 'front' ? main.querySelector('.flip-face img') : null);
      var drawn = main.querySelector('.book-drawn .cover');
      if (!img && drawn && face === 'front') {   // a drawn cover: the photo takes its place
        drawn.querySelectorAll('.cover-title, .cover-no').forEach(function (x) { x.remove(); });
        drawn.classList.add('has-img'); img = el('img'); drawn.prepend(img);
      }
      if (!img) {   // no photo of this side yet: show it beside the stage
        var stage = main.querySelector('.flip, .book-drawn');
        var fig = el('figure', 'ed-new-face'); img = el('img'); img.style.maxWidth = '16rem';
        fig.appendChild(el('p', 'ed-flag', face === 'back' ? 'የጀርባ ሽፋን' : 'የፊት ሽፋን')); fig.appendChild(img);
        (stage || main).after(fig);
      }
    }
    if (img) { img.src = src; img.removeAttribute('srcset'); img.closest('figure') && img.closest('figure').classList.add('is-on'); }
  }
  photoButton();

  // the optional photo above the name on the home page
  function homeSlot() {
    if (KEY !== 'index') return null;
    var mh = document.querySelector('.masthead .wrap'); if (!mh) return null;
    var slot = el('div', 'ed-mast-slot');
    var add = el('button', 'ed-btn ed-btn-line', ''); add.type = 'button';
    var rm = el('button', 'ed-btn-out', 'ፎቶውን አስወግድ'); rm.type = 'button';
    slot.appendChild(add); slot.appendChild(rm);
    (mh.querySelector('.mast-photo') || mh.querySelector('.mast-lines')).before(slot);
    function draw() { var has = !!mh.querySelector('.mast-photo:not([hidden])'); add.textContent = has ? '📷 ፎቶውን ቀይር' : '📷 እዚህ ፎቶ ጨምር (ካስፈለገ)'; rm.hidden = !has; }
    slot.fig = function () { return mh.querySelector('.mast-photo'); };
    slot.show = function (src) {
      var fig = mh.querySelector('.mast-photo');
      if (!fig) { fig = el('figure', 'mast-photo', '<img alt="">'); slot.after(fig); }
      if (src) { fig.hidden = false; fig.querySelector('img').src = src; fig.querySelector('img').removeAttribute('width'); }
      else { fig.hidden = true; if (fig._edFlag) { fig._edFlag.remove(); fig._edFlag = null; } }
      draw();
    };
    add.onclick = function () {
      pickImage().then(function (data) {
        slot.show(data); photoFlag(slot.fig(), 'saving');
        call('/save', { type: 'photo', page: location.pathname, target: 'home', face: 'main', photo: { data: data } })
          .then(function () { photoFlag(slot.fig(), 'saved'); toast('ፎቶው ተቀምጧል ✓<small>ሰላም ካየችው በኋላ ድረ ገጹ ላይ ይወጣል።</small>', false, 8000); },
                function (err) { photoFlag(slot.fig(), 'bad'); failed(err); });
      });
    };
    rm.onclick = function () {
      modal('ፎቶውን ላስወግደው?', '', [{ label: 'አዎ፣ አስወግድ', go: function () {
        slot.show(null);
        call('/save', { type: 'photo', page: location.pathname, target: 'home', remove: true })
          .then(function () { toast('ተቀምጧል ✓<small>ፎቶው ሰላም ካየችው በኋላ ይወገዳል።</small>', false, 8000); }, failed);
      } }, { label: 'ተመለስ', cancel: true }]);
    };
    draw();
    return slot;
  }
  var home = homeSlot();

  // ---------------------------------------------------------------- "add new" buttons and waiting pieces
  var KIND_LABEL = { essay: 'ድርሰት', poem: 'ግጥም', qene: 'ቅኔ', painting: 'ሥዕል', book: 'መጽሐፍ' };
  function addButtons() {
    var spots = [
      ['index', '.front-list .wlist', [['essay', '＋ አዲስ ጽሑፍ ጨምር']]],
      ['writings', '.writings-list', [['essay', '＋ አዲስ ድርሰት ጨምር'], ['poem', '＋ አዲስ ግጥም ጨምር']]],
      ['poetry', '.page-body', [['poem', '＋ አዲስ ግጥም ጨምር']]],
      ['qene', '.page-body', [['qene', '＋ አዲስ ቅኔ ጨምር']]],
      ['books', '.shelf', [['book', '＋ አዲስ መጽሐፍ ጨምር']]],
      ['paintings', '.gallery', [['painting', '＋ አዲስ ሥዕል ጨምር']]]
    ];
    spots.forEach(function (s) {
      if (s[0] !== KEY) return;
      var at = main.querySelector(s[1]); if (!at) return;
      var box = el('div', 'ed-adds');
      s[2].forEach(function (k) { var a = el('a', 'ed-btn', esc(k[1])); a.href = ROOT + 'edit/new/?kind=' + k[0]; box.appendChild(a); });
      if (s[1] === '.page-body') at.prepend(box); else at.before(box);
      box.after(el('ul', 'ed-pending-list'));
    });
  }
  addButtons();

  // ---------------------------------------------------------------- what he saved before (not yet on the site)
  function findBlock(text) {
    for (var i = 0; i < blocks.length; i++) if (blocks[i].isConnected && blocks[i].style.display !== 'none' && blocks[i].dataset.orig === text) return blocks[i];
    return null;
  }
  function overlay(edits) {
    var latestNew = {};
    edits.forEach(function (e) {
      if (e.type === 'text') (e.changes || []).forEach(function (c) {
        var b;
        if (c.op === 'edit' && (b = findBlock(c.from))) { setText(b, c.to); b.dataset.orig = c.to; b.classList.add('pending'); }
        else if (c.op === 'delete' && (b = findBlock(c.from))) { b.style.display = 'none'; }
        else if (c.op === 'insert' && (b = findBlock(c.after))) {
          var at = b;
          c.text.forEach(function (t) {
            var np = el(b.tagName, b.className.replace(/\b(ed|changed|pending)\b/g, '').trim()); setText(np, t);
            at.after(np); mark(np, t); np.classList.add('pending'); at = np;
          });
        } else if (c.op === 'field' && c.target === KEY) {
          fieldInputs.forEach(function (f) {
            if (f.field !== c.field) return;
            if (f.inp.type === 'checkbox') f.inp.checked = c.to === 'አዎ'; else f.inp.value = c.to;
            f.orig = f.value(); f.inp.classList.add('pending');
          });
        }
      });
      else if (e.type === 'photo' && e.target === 'home' && home) { home.show(e.remove ? null : src(e.file)); if (!e.remove) photoFlag(home.fig(), 'saved'); }
      else if (e.type === 'photo' && e.target === KEY && e.file) { showPhoto(e.face, src(e.file)); photoFlag(main.querySelector('.flip-stage, .book-drawn, .pt-figure'), 'saved'); }
      else if (e.type === 'new') latestNew[e.piece_id] = e;
    });
    var lists = main.querySelectorAll('.ed-pending-list');
    var kinds = { index: ['essay', 'poem'], writings: ['essay', 'poem'], poetry: ['poem'], qene: ['qene'], books: ['book'], paintings: ['painting'] }[KEY] || [];
    Object.keys(latestNew).forEach(function (id) {
      var n = latestNew[id];
      if (kinds.indexOf(n.kind) < 0) return;
      lists.forEach(function (l) {
        var li = el('li', '', '<a href="' + ROOT + 'edit/new/?id=' + encodeURIComponent(id) + '">' + esc(n.title || '(ርእስ የለውም)') +
          '<small>' + esc(KIND_LABEL[n.kind] || '') + ' — ተቀምጧል፤ ሰላም እስክታየው ይጠብቃል። ለመቀጠል ይጫኑ።</small></a>');
        l.appendChild(li);
      });
    });
    window.BK_PENDING_NEW = latestNew;
  }
  var pending = API ? call('/pending').then(function (j) { var e = j.edits || []; overlay(e); return e; })
    .catch(function (err) { if (err && err.login) failed(err); return []; }) : Promise.resolve([]);

  // ---------------------------------------------------------------- the new-piece page (/edit/new/)
  var newSave = function () { return Promise.resolve(); };
  if (KEY === 'edit-new') {
    var box = document.getElementById('newp');
    var q = new URLSearchParams(location.search);
    var piece = { id: q.get('id') || ('n' + Date.now().toString(36)), kind: q.get('kind') || 'essay', photos: {} };
    var title = box.querySelector('.np-title'), text = box.querySelector('.np-text'), year = box.querySelector('.np-year');
    var photosBox = box.querySelector('.np-photos'), textLbl = box.querySelector('.np-text-lbl');
    title.setAttribute('data-ph', 'ርእሱን እዚህ ይጻፉ…');
    var qbox = box.querySelector('.np-qene'), titleLbl = box.querySelector('.np-title-lbl');
    var QF = ['author', 'meaning', 'sem', 'werq', 'calc'];
    function qval(f) { var x = qbox.querySelector('[data-q="' + f + '"]'); return x ? norm(x.value) : ''; }
    var saved = {};
    function cur() {
      var c = { title: norm(title.innerText).replace(/\n+/g, ' '), text: norm(text.innerText), year: norm(year.value), photos: JSON.stringify(piece.photos) };
      QF.forEach(function (f) { c[f] = piece.kind === 'qene' ? qval(f) : ''; });
      return c;
    }
    extraDirty = function () { var c = cur(); return Object.keys(c).some(function (k) { return c[k] !== (saved[k] || ''); }) ? 1 : 0; };
    qbox.querySelectorAll('input, textarea').forEach(function (x) { x.addEventListener('input', function () { refresh(); }); });
    var SLOTS = { essay: [['main', 'ፎቶ (ካለ)']], poem: [['main', 'ፎቶ (ካለ)']], qene: [], painting: [['main', 'የሥዕሉ ፎቶ']], book: [['front', 'የፊት ሽፋን'], ['back', 'የጀርባ ሽፋን']] };
    var TEXT_LBL = { essay: ['ጽሑፉ', 'ጽሑፉን እዚህ ይጻፉ…'], poem: ['ግጥሙ — እያንዳንዱን መስመር በ Enter ይለዩ', 'ግጥሙን እዚህ ይጻፉ…'],
                     qene: ['ቅኔው — እያንዳንዱን መስመር በ Enter ይለዩ', 'ቅኔውን እዚህ ይጻፉ…'],
                     painting: ['ስለ ሥዕሉ (ካለ)', 'ስለ ሥዕሉ የሚፈልጉትን ይጻፉ…'], book: ['ስለ መጽሐፉ (ካለ)', 'ስለ መጽሐፉ የሚፈልጉትን ይጻፉ…'] };
    function drawKind() {
      box.querySelectorAll('.kind button').forEach(function (b) { b.setAttribute('aria-pressed', String(b.dataset.kind === piece.kind)); });
      box.querySelector('.np-year-row').hidden = !(piece.kind === 'painting' || piece.kind === 'book');
      textLbl.textContent = TEXT_LBL[piece.kind][0]; text.setAttribute('data-ph', TEXT_LBL[piece.kind][1]);
      qbox.hidden = piece.kind !== 'qene';
      titleLbl.textContent = piece.kind === 'qene' ? 'የቅኔው ስም (ለምሳሌ «ጉባዔ ቃና — 3ኛ ቅኔ»)' : 'ርእስ';
      photosBox.innerHTML = '';
      SLOTS[piece.kind].forEach(function (s) {
        var p = piece.photos[s[0]], src = p ? (p.data || src(p.file)) : '';
        var slot = el('div', 'np-photo', '<div class="ph-box">' + (src ? '<img alt="" src="' + esc(src) + '">' : '<span>📷</span>') + '</div>');
        var b = el('button', 'ed-btn ed-btn-line', src ? 'ፎቶ ቀይር' : esc(s[1])); b.type = 'button';
        b.onclick = function () { pickImage().then(function (data) { piece.photos[s[0]] = { data: data }; drawKind(); refresh(); }); };
        slot.appendChild(b); photosBox.appendChild(slot);
      });
      refresh();
    }
    box.querySelectorAll('.kind button').forEach(function (b) { b.onclick = function () { piece.kind = b.dataset.kind; drawKind(); if (typeof changed === 'function') changed(); }; });
    [title, text].forEach(function (x) { x.addEventListener('input', function () { refresh(); }); });
    year.addEventListener('input', function () { refresh(); });
    title.addEventListener('keydown', function (e) { if (e.key === 'Enter') e.preventDefault(); });
    title.addEventListener('paste', paste);
    text.addEventListener('paste', function (e) { e.preventDefault(); document.execCommand('insertText', false, (e.clipboardData || window.clipboardData).getData('text/plain') || ''); });
    function lines() {
      var t = norm(text.innerText);
      if (!t) return [];
      return piece.kind === 'poem' || piece.kind === 'qene' ? t.split('\n') : t.split(/\n+/).filter(Boolean);
    }
    // ---- keeping his work safe: a copy in this browser on every keystroke, and an automatic save a few seconds after he stops
    var DRAFT_KEY = 'bk-ed-draft-' + piece.id, touched = false, loaded = false, autoTimer = null;
    function fill(v) {
      piece.kind = v.kind || piece.kind;
      title.textContent = v.title || '';
      text.innerHTML = (v.text || []).map(function (l) { return '<div>' + (l ? esc(l) : '<br>') + '</div>'; }).join('');
      year.value = v.year || '';
      QF.forEach(function (f) { var x = qbox.querySelector('[data-q="' + f + '"]'); if (x) x.value = v[f] || ''; });
      (v.photos || []).forEach(function (p) { piece.photos[p.role] = { file: p.file }; });
    }
    function asSaved(v) {   // what cur() would read once v is on the page
      var c = { title: norm(v.title || ''), text: norm((v.text || []).join('\n')), year: norm(v.year || ''), photos: '' };
      QF.forEach(function (f) { c[f] = v.kind === 'qene' ? norm(v[f] || '') : ''; });
      return c;
    }
    function keepDraft() {
      if (!q.get('id')) { q.set('id', piece.id); q.delete('kind'); history.replaceState(null, '', '?' + q.toString()); }
      var d = { at: new Date().toISOString(), kind: piece.kind, title: cur().title, text: lines(), year: cur().year };
      QF.forEach(function (f) { d[f] = qval(f); });
      try { localStorage.setItem(DRAFT_KEY, JSON.stringify(d)); } catch (e) {}
    }
    function dropDraft() { try { localStorage.removeItem(DRAFT_KEY); } catch (e) {} }
    function changed() {
      touched = true; keepDraft();
      clearTimeout(autoTimer);
      autoTimer = setTimeout(autoSave, 8000);
    }
    function autoSave() { if (loaded && !busy && extraDirty() && cur().title) newSave(true); }
    [title, text, year].forEach(function (x) { x.addEventListener('input', changed); });
    qbox.querySelectorAll('input, textarea').forEach(function (x) { x.addEventListener('input', changed); });
    document.addEventListener('visibilitychange', function () {   // he switches away or closes the tab: save now
      if (document.visibilityState === 'hidden') { clearTimeout(autoTimer); autoSave(); }
    });
    var fieldsAll = [year].concat([].slice.call(qbox.querySelectorAll('input, textarea')));
    function lock(on) {   // continuing a saved piece: nothing can be typed until it has loaded, so nothing he types is overwritten
      [title, text].forEach(function (x) { x.contentEditable = on ? 'false' : 'true'; x.classList.toggle('np-loading', on); });
      fieldsAll.forEach(function (x) { x.disabled = on; });
      if (on) { title.setAttribute('data-ph', 'በመጫን ላይ…'); text.setAttribute('data-ph', 'በመጫን ላይ…'); }
      else { title.setAttribute('data-ph', 'ርእሱን እዚህ ይጻፉ…'); }
    }
    if (q.get('id')) lock(true);
    pending.then(function () {   // continuing a piece he saved before
      lock(false);
      var prev = (window.BK_PENDING_NEW || {})[piece.id], draft = null;
      try { draft = JSON.parse(localStorage.getItem(DRAFT_KEY)); } catch (e) {}
      if (draft && prev && prev.at && draft.at <= prev.at) { dropDraft(); draft = null; }
      if (!touched && prev) fill(prev);
      drawKind();
      // only the server's copy counts as saved; anything typed before the page finished loading stays, unsaved
      saved = touched || !prev ? (prev ? asSaved(prev) : { photos: '{}' }) : cur();
      if (prev) saved.photos = JSON.stringify((prev.photos || []).reduce(function (o, p) { o[p.role] = { file: p.file }; return o; }, {}));
      if (!touched && draft) { fill(draft); drawKind(); }   // newer than what reached the server: put it back, and it will be saved
      loaded = true; refresh();
      if (extraDirty() && cur().title) changed();
    });
    drawKind(); saved = { photos: '{}' }; refresh();
    newSave = function (quiet) {
      var c = cur();
      if (!c.title) { toast('እባክዎ ርእስ ይጻፉ።', true); title.focus(); return Promise.resolve(); }
      if (!loaded) return pending.then(function () { return newSave(quiet); });
      clearTimeout(autoTimer);
      busy = true; saveBtn.textContent = 'በማስቀመጥ ላይ…'; refresh();
      var photos = Object.keys(piece.photos).filter(function (r) { return SLOTS[piece.kind].some(function (s) { return s[0] === r; }); })
        .map(function (r) { var p = piece.photos[r]; return p.data ? { role: r, data: p.data } : { role: r, file: p.file }; });
      var body = { type: 'new', page: location.pathname, id: piece.id, kind: piece.kind, title: c.title, text: lines(), year: c.year, photos: photos };
      if (piece.kind === 'qene') QF.forEach(function (f) { body[f] = c[f]; });
      return call('/save', body)
        .then(function (j) {
          (j.photos || []).forEach(function (p) { piece.photos[p.role] = { file: p.file }; });
          c.photos = JSON.stringify(piece.photos); saved = c;   // what was sent — typing during the save stays unsaved
          if (!q.get('id')) { q.set('id', piece.id); q.delete('kind'); history.replaceState(null, '', '?' + q.toString()); }
          if (extraDirty()) changed(); else dropDraft();
          if (!quiet) toast('ተቀምጧል ✓<small>ሰላም ካየችው በኋላ ድረ ገጹ ላይ ይወጣል። መጻፍ መቀጠል ይችላሉ።</small>');
          else { statusEl.dataset.auto = '1'; }
        }, failed)
        .then(function () { busy = false; saveBtn.textContent = 'አስቀምጥ'; refresh(); });
    };
    bar.querySelector('.edbar-hint').textContent = 'ዓይነቱን ይምረጡ፤ ርእሱንና ጽሑፉን ይጻፉ። በሚጽፉበት ጊዜ በራሱ ይቀመጣል፤ ሲጨርሱ «አስቀምጥ»ን ይጫኑ።';
  }

  // ---------------------------------------------------------------- typing Amharic the Power Ge'ez way
  // The same keys as Power Ge'ez (Phonetic), which he types from memory: a letter alone is the 1st form (l ለ), then
  // u i a y e o for the others (lu ሉ, li ሊ, la ላ, ly ሌ, le ል, lo ሎ), W for ሏ (qW ቋ, qWo ቈ, qWi ቊ). Capitals and
  // x X Y are other letters (H ሐ, S ሸ, T ጠ, x አ, X ዐ, Y የ); Caps Lock gives h ኀ, H ኸ, s ሠ, t ጸ, T ፀ (also J L K F V).
  // Like Power Ge'ez, a vowel changes the letter just before the cursor. Keys follow SIL's "Ethiopic Power-G" (Keyman),
  // except punctuation, which follows his own texts: ":" is ፡ every time (his full stop is ፡፡), "." stays a dot, "," ፣.
  // The «ፊ» button in the bar turns it on and off (remembered on this computer).
  var PG = (function () {
    var ch = String.fromCharCode, cp = function (s) { return s ? s.charCodeAt(0) : 0; };
    var BASE = { h: 0x1200, l: 0x1208, H: 0x1210, m: 0x1218, J: 0x1220, r: 0x1228, s: 0x1230, S: 0x1238, q: 0x1240, Q: 0x1250,
      b: 0x1260, v: 0x1268, t: 0x1270, c: 0x1278, L: 0x1280, n: 0x1290, N: 0x1298, x: 0x12A0, k: 0x12A8, K: 0x12B8, w: 0x12C8,
      X: 0x12D0, z: 0x12D8, Z: 0x12E0, Y: 0x12E8, d: 0x12F0, D: 0x12F8, j: 0x1300, g: 0x1308, G: 0x1318, T: 0x1320, C: 0x1328,
      P: 0x1330, F: 0x1338, V: 0x1340, f: 0x1348, p: 0x1350 };
    var FIRST = {}; for (var b in BASE) FIRST[BASE[b]] = 1;
    var CAPS = { h: 0x1280, H: 0x12B8, s: 0x1220, t: 0x1338, T: 0x1340 };                       // with Caps Lock on
    var BRACKET = { 0x1200: 0x1280, 0x1210: 0x12B8, 0x1230: 0x1220, 0x1270: 0x1338, 0x1320: 0x1340 };   // h[ ኀ, s[ ሠ …
    var ORDER = { u: 1, i: 2, a: 3, y: 4, e: 5, o: 6 };
    var ALONE = { u: 0x12A1, i: 0x12A2, a: 0x12A3, e: 0x12A5, o: 0x12A6, W: 0x12A7,
      U: 0x12D1, I: 0x12D2, A: 0x12D3, E: 0x12D5, O: 0x12D6 };
    var DIPH = { 0x1200: 0, 0x1240: 0x124B, 0x1250: 0x125B, 0x1280: 0x128B, 0x12A8: 0x12B3, 0x12B8: 0x12C3,
      0x12C8: 0, 0x12D0: 0, 0x12E8: 0, 0x1308: 0x1313, 0x1340: 0 };                          // otherwise base + 7 (ሏ)
    // after ሟ ሯ ቋ ቛ ቧ ኋ ኳ ዃ ጓ ጟ ፏ ፗ: u i y o I (qWo ቈ)
    var DG = [0x121F, 0x122F, 0x124B, 0x125B, 0x1267, 0x128B, 0x12B3, 0x12C3, 0x1313, 0x131F, 0x134F, 0x1357];
    var DGV = {
      u: [0x1383, 0x122F, 0x124D, 0x125D, 0x1387, 0x128D, 0x12B5, 0x12C5, 0x1315, 0x2D96, 0x138B, 0x138F],
      i: [0x1381, 0x122F, 0x124A, 0x125A, 0x1385, 0x128A, 0x12B2, 0x12C2, 0x1312, 0x2D94, 0x1389, 0x138D],
      y: [0x1382, 0x122F, 0x124C, 0x125C, 0x1386, 0x128C, 0x12B4, 0x12C4, 0x1314, 0x2D95, 0x138A, 0x138E],
      o: [0x1380, 0x122F, 0x1248, 0x1258, 0x1384, 0x1288, 0x12B0, 0x12C0, 0x1310, 0x2D93, 0x1388, 0x138C],
      I: [0x1359, 0x1358, 0x124B, 0x125B, 0x1267, 0x128B, 0x12B3, 0x12C3, 0x1313, 0x131F, 0x135A, 0x1357] };
    function diph(c) { return c in DIPH ? DIPH[c] : c + 7; }
    var GEEZNUM = '፩፪፫፬፭፮፯፰፱', TENS = '፲፳፴፵፶፷፸፹፺';
    // one key → { remove: how many characters before the cursor it replaces, text } ; null = type the key as it is
    function key(k, caps, prev) {
      var p = cp(prev), r = function (n, c) { return { remove: n, text: typeof c === 'number' ? ch(c) : c }; };
      if (caps && CAPS[k]) return r(0, CAPS[k]);
      if (k === '[' && BRACKET[p]) return r(1, BRACKET[p]);
      if (BASE[k]) return r(0, BASE[k]);
      var dg = DG.indexOf(p);
      if (dg >= 0 && DGV[k]) return r(1, DGV[k][dg]);                    // qWo ቈ, qWi ቊ
      if (dg >= 0 && k === 'a') return r(1, p);                           // qWa: still ቋ
      if (FIRST[p] && ORDER[k] != null) return r(1, p + ORDER[k]);        // le ል, lu ሉ
      if (FIRST[p] && k === 'W') return r(1, diph(p) || p);              // lW ሏ
      if (k === 'a' && prev && p === diph(p - 7) && FIRST[p - 7]) return r(1, p);   // lWa: still ሏ
      if (ALONE[k]) return r(0, ALONE[k]);                                // a ኣ, e እ, A ዓ, E ዕ
      if (k === 'y' || k === 'B' || k === 'M' || k === 'R') return r(0, '');   // no letter of their own
      if (k === ':') return r(0, '፡');
      if (k === ',') return r(prev === '፣' ? 1 : 0, '፣');
      if (k === ';') return r(0, '፤');
      if (k === '<' && prev === '<') return r(1, '«');
      if (k === '>' && prev === '>') return r(1, '»');
      if (k === '*' && /[1-9]/.test(prev || '')) return r(1, GEEZNUM[+prev - 1]);   // 1* ፩
      if (k === '0' && GEEZNUM.indexOf(prev) >= 0) return r(1, TENS[GEEZNUM.indexOf(prev)]);   // 1*0 ፲
      if (k === '0' && prev === '፲') return r(1, '፻');                    // 1*00 ፻
      return null;
    }
    return { key: key };
  })();
  var amOn = true;
  try { amOn = localStorage.getItem('bk-ed-am') !== 'off'; } catch (e) {}
  var amBtn = el('button', 'ed-am', 'ፊ'); amBtn.type = 'button';
  var amHelp = el('button', 'ed-am-help', '?'); amHelp.type = 'button';
  function drawAm() {
    amBtn.classList.toggle('on', amOn);
    amBtn.textContent = amOn ? 'ፊ' : 'A';
    amBtn.title = amOn ? 'አማርኛ እየጻፉ ነው (እንደ ፓወር ግዕዝ) — ለእንግሊዝኛ ይጫኑ' : 'እንግሊዝኛ እየጻፉ ነው — ለአማርኛ ይጫኑ';
  }
  amBtn.onclick = function () { amOn = !amOn; drawAm(); try { localStorage.setItem('bk-ed-am', amOn ? 'on' : 'off'); } catch (e) {} };
  amHelp.onclick = function () {
    var rows = [['ሀ', 'h'], ['ለ', 'l'], ['ሐ', 'H'], ['መ', 'm'], ['ሠ', 'J'], ['ረ', 'r'], ['ሰ', 's'], ['ሸ', 'S'], ['ቀ', 'q'],
      ['በ', 'b'], ['ቨ', 'v'], ['ተ', 't'], ['ቸ', 'c'], ['ኀ', 'L'], ['ነ', 'n'], ['ኘ', 'N'], ['አ', 'x'], ['ከ', 'k'], ['ኸ', 'K'],
      ['ወ', 'w'], ['ዐ', 'X'], ['ዘ', 'z'], ['ዠ', 'Z'], ['የ', 'Y'], ['ደ', 'd'], ['ጀ', 'j'], ['ገ', 'g'], ['ጠ', 'T'], ['ጨ', 'C'],
      ['ጰ', 'P'], ['ጸ', 'F'], ['ፀ', 'V'], ['ፈ', 'f'], ['ፐ', 'p']];
    var bg = modal('አማርኛ እንደ ፓወር ግዕዝ', '', [{ label: 'ገባኝ' }]);
    var m = bg.querySelector('.ed-modal'), btns = m.querySelector('.ed-modal-btns');
    var ex = el('div', 'ed-am-table',
      '<p>እንደ ፓወር ግዕዝ ይጻፉ። <b>ፊ</b> (ሰማያዊ) ሲሆን አማርኛ፣ <b>A</b> ሲሆን እንግሊዝኛ።</p>' +
      '<p class="ed-am-ex"><b>l</b> ለ · <b>lu</b> ሉ · <b>li</b> ሊ · <b>la</b> ላ · <b>ly</b> ሌ · <b>le</b> ል · <b>lo</b> ሎ · <b>lW</b> ሏ</p>' +
      '<p class="ed-am-ex"><b>slame</b> ሰላም · <b>xmareNa</b> አማርኛ · <b>geXeze</b> ግዕዝ · <b>qWiTere</b> ቊጥር · <b>a</b> ኣ · <b>e</b> እ · <b>A</b> ዓ · <b>E</b> ዕ</p>' +
      '<p class="ed-am-ex">Caps Lock፦ <b>h</b> ኀ · <b>H</b> ኸ · <b>s</b> ሠ · <b>t</b> ጸ · <b>T</b> ፀ &nbsp; · &nbsp; <b>:</b> ፡ · <b>,</b> ፣ · <b>;</b> ፤ · <b>&lt;&lt;</b> « · <b>1*</b> ፩ · <b>1*0</b> ፲</p>' +
      '<div class="ed-am-grid">' + rows.map(function (r) { return '<span><b>' + r[0] + '</b> ' + esc(r[1]) + '</span>'; }).join('') + '</div>');
    m.insertBefore(ex, btns);
  };
  var hint = bar.querySelector('.edbar-hint');
  hint.parentNode.insertBefore(amBtn, hint.nextSibling); amBtn.after(amHelp);
  drawAm();

  function typable(t) {
    if (!t || !t.closest || t.closest('.edbar, .ed-modal')) return false;
    if (t.isContentEditable) return true;
    if (t.matches('textarea')) return true;
    return t.matches('input[type="text"], input:not([type])') && t.inputMode !== 'numeric';
  }
  function before(t) {   // the character just before the cursor ('' when text is selected or at the start)
    if (t.isContentEditable) {
      var s = window.getSelection(); if (!s.rangeCount || !s.isCollapsed) return '';
      var r = s.getRangeAt(0), pre = document.createRange();
      pre.selectNodeContents(t); pre.setEnd(r.endContainer, r.endOffset);
      var all = pre.toString(); return all.slice(-1);
    }
    if (t.selectionStart !== t.selectionEnd) return '';
    return t.value.slice(Math.max(0, t.selectionStart - 1), t.selectionStart);
  }
  function put(t, remove, text) {   // replace the selection, or the `remove` characters before the cursor, with `text`
    if (t.isContentEditable) {
      var s = window.getSelection();
      for (var i = 0; i < remove; i++) s.modify('extend', 'backward', 'character');
      if (text) document.execCommand('insertText', false, text);
      else if (remove || !s.isCollapsed) document.execCommand('delete');
    } else {
      var a = t.selectionStart - remove, z = t.selectionEnd;
      t.setRangeText(text, a, z, 'end');
      t.dispatchEvent(new Event('input', { bubbles: true }));
    }
  }
  document.addEventListener('keydown', function (e) {
    var t = e.target;
    if (!amOn || e.ctrlKey || e.metaKey || e.altKey || e.isComposing || !typable(t)) return;
    var k = e.key, caps = /^[a-zA-Z]$/.test(k) && !!(e.getModifierState && e.getModifierState('CapsLock'));
    if (caps) k = k === k.toUpperCase() ? k.toLowerCase() : k.toUpperCase();   // undo Caps Lock: it only picks ኀ ኸ ሠ ጸ ፀ
    if (k.length !== 1) return;
    var r = PG.key(k, caps, before(t));
    if (!r) return;
    e.preventDefault();
    put(t, r.remove, r.text);
  }, true);

  // ---------------------------------------------------------------- how many people read each page (GoatCounter)
  var STATS = window.BK_STATS || '';
  function reads(path) {
    return fetch(STATS + '/counter/' + encodeURIComponent(path) + '.json')
      .then(function (r) { return r.status === 404 ? { count: '0' } : r.ok ? r.json() : null; })
      .then(function (j) { return j && j.count != null ? String(j.count) : null; }, function () { return null; });
  }
  function readsText(n) { return n === '0' ? 'ገና ያነበበው የለም' : n + ' ሰዎች አንብበውታል'; }
  if (STATS && KEY !== 'edit-new') {
    reads(location.pathname).then(function (n) {
      if (n == null) return;
      var chip = el('span', 'ed-reads', '👁 ' + esc(readsText(n)));
      chip.title = 'ይህን ገጽ ያነበቡ ሰዎች ብዛት';
      statusEl.parentNode.insertBefore(chip, statusEl);
    });
    main.querySelectorAll('.writings-list a[href], .wlist a[href]').forEach(function (a) {
      var path = new URL(a.href, location.href).pathname;
      reads(path).then(function (n) { if (n != null) a.appendChild(el('small', 'ed-reads-sm', '👁 ' + esc(readsText(n)))); });
    });
  }

  refresh();
  if (DEMO) bar.querySelector('.edbar-hint').textContent = 'ልምምድ ብቻ — የሚቀመጠው በዚህ ኮምፒውተር ብቻ ነው፤ ወደ ድረ ገጹ አይላክም።';
  if (!API) { statusEl.className = 'edbar-status bad'; statusEl.textContent = 'ማስተካከያው ገና አልተገናኘም'; }
})();
