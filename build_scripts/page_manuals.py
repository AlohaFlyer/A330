#!/usr/bin/env python3
"""Deterministic transform: B787 pwa.html clone -> manuals/index.html (the A330 Manuals page).

Input : the B787 checkout path (argv[1], default ../../b787 relative to this file). The
        transform clones B787/pwa.html, runs apply_palette.process(t, 'pwa.html') and
        apply_strings.apply(t, 'pwa.html') exactly as build.sh does for every page, then
        rewrites only the content and data layer below.
Output: manuals/index.html. Served at /manuals/ (Cloudflare Access protects /manuals*),
        so every fetch on the page stays under /manuals/ except the shared engine scripts
        /portal-settings.js, /assist.js and /sw.js, which carry no manual text.

What changes (content and data only; every CSS rule, class, id, control, key handler and
the two-stage Ask flow are kept):
  - title, banner title "A330 MANUALS", a one-sentence .sub line (no "Open full PDF" link),
    footer text, textarea placeholder. Revisions from manuals.json appear once, as
    "<short> <revision> · <date>" on each manual's Browse by section header and as the title
    attribute of its selector chip.
  - a Manual selector in the existing .seg pill style (All, FCOM, QRH, FCTM, FOM, MEL, AFM,
    PRC, more) directly under the Match segment; "more" reveals AFM-SUPP, PERF, NPC-CB, FODM.
  - no profile chips and no profile text anywhere in the prompt.
  - the index loader reads /manuals/<key>.json (and its parts) lazily, caches each manual in
    memory, and the BM25 runs over the selected manual or every loaded manual for All.
  - result cards show manual, section id, title and PDF page; "Open <manual> in Drive, p.N"
    links to the manual's drive_url (Drive cannot deep-link a page).
  - the page modal shows the section's page text with manual, section and page marks.
  - Ask citations "(FCOM DSC-35-20-30 p.1945)" become links that open that page's modal.
  - URL params: ?q= prefills and runs a search, ?m=<key> preselects a manual,
    ?s=<section id> opens that section's modal.
  - icon links point at /assets/icons/ like gen_index.py does for the root pages.
  - the index JSON is NOT served from the repo: every index fetch (manifest.json, <key>.json,
    parts) goes to MANUALS_BASE = 'https://manuals.ha330pilot.app' (R2 bucket behind
    Cloudflare Access, @alaskaair.com one-time code) with credentials included; prompt.json
    stays local at /manuals/prompt.json. On load the page probes MANUALS_BASE/manifest.json and
    on any failure shows a sign-in line and button (to MANUALS_BASE/login.html?back=...). The
    query param ?base=<url> replaces MANUALS_BASE so the headless test can serve the JSON from
    the local http.server (see docs/MANUALS_HOSTING.md).
Deviations from the B787 engine (for the parity allowlist):
  - buildBM(docs) takes the doc list as a parameter instead of reading IDX.docs, so one
    BM25 table per manual can be built once and merged per selection.
  - two extra .seg groups (#manSeg, #manSegMore) reuse the existing .seg CSS; no new rules.
"""
import json, os, re, sys, html
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.abspath(os.path.join(HERE, '..'))
B787 = sys.argv[1] if len(sys.argv) > 1 else os.path.abspath(os.path.join(WORK, '..', 'b787'))
sys.path.insert(0, HERE)
import apply_palette, apply_strings

M = json.load(open(os.path.join(WORK, 'manuals.json'), encoding='utf-8'))
ORDER = ['A330P_FCOM', 'A330P_QRH', 'A330_FCTM', 'FOM', 'A330_MEL', 'A330_AFM', 'A330_PRC',
         'A330_AFM-SUPP', 'A330P_PERF', 'A330P_NPC-CB', 'FODM']
PRIMARY = ORDER[:7]
SHORT = {'A330P_FCOM': 'FCOM', 'A330P_QRH': 'QRH', 'A330_FCTM': 'FCTM', 'FOM': 'FOM', 'A330_MEL': 'MEL',
         'A330_AFM': 'AFM', 'A330_PRC': 'PRC', 'A330_AFM-SUPP': 'AFM-SUPP', 'A330P_PERF': 'PERF',
         'A330P_NPC-CB': 'NPC-CB', 'FODM': 'FODM'}
MANUALS = [{'key': k, 'short': SHORT[k], 'title': M[k]['title'], 'revision': M[k]['revision'],
            'date': M[k]['date'], 'drive_url': M[k]['drive_url']} for k in ORDER]


def rev_text(k):
    r = M[k]['revision']
    return SHORT[k] + ' ' + ((r + ' \u00b7 ') if r else '') + M[k]['date']




def sub(t, a, b, count=1):
    n = t.count(a)
    assert n == count, ('anchor count %d != %d: %s' % (n, count, a[:70]))
    return t.replace(a, b)


def region(t, start, end, new):
    i = t.index(start)
    j = t.index(end, i)
    assert t.count(start) == 1, start[:60]
    return t[:i] + new + t[j:]


t = open(os.path.join(B787, 'pwa.html'), encoding='utf-8').read()
t = apply_palette.process(t, 'pwa.html')
t = apply_strings.apply(t, 'pwa.html')

# ------------------------------------------------------------------ head and static text
t = sub(t, '<title>ALPA Pilot Working Agreement</title>', '<title>A330 Manuals</title>')
t = sub(t, 'href="/favicon.ico"', 'href="/assets/icons/favicon.ico"')
t = sub(t, 'href="/apple-touch-icon.png"', 'href="/assets/icons/icon-180.png"')
t = sub(t, '<span class="t">ALPA PILOT WORKING AGREEMENT</span>', '<span class="t">A330 MANUALS</span>')
t = sub(t, '''    <span id="meta">Hawaiian Airlines 2023 Pilots Agreement</span>
    <span><a href="/pwa_pdf.html">Open full PDF &#9654;</a></span>''',
        '''    <span id="meta">Search every current Hawaiian A330 PAX manual at once, or pick one. Revisions are listed under Browse by section.</span>''')
t = sub(t, 'placeholder="Ask a contract question, e.g. how much rest do I get at a domestic overnight?"',
        'placeholder="Ask a manual question, e.g. how do I test the oxygen mask?"')

seg_btn = lambda k, pressed: '        <button type="button" data-man="%s" aria-pressed="%s" title="%s">%s</button>\n' % (k, 'true' if pressed else 'false', html.escape(rev_text(k)), SHORT[k])
MAN_ROW = '''    <div class="modebar">
      <span class="mlbl">Manual</span>
      <div class="seg" id="manSeg" role="group" aria-label="Manual">
        <button type="button" data-man="ALL" aria-pressed="true">All</button>
''' + ''.join(seg_btn(k, False) for k in PRIMARY[:4]) + '''      </div>
      <div class="seg" id="manSeg2" role="group" aria-label="Manual, continued">
''' + ''.join(seg_btn(k, False) for k in PRIMARY[4:]) + '''        <button type="button" data-man="more" aria-pressed="false">more</button>
      </div>
      <div class="seg" id="manSegMore" role="group" aria-label="More manuals" style="display:none">
''' + ''.join(seg_btn(k, False) for k in ORDER[7:]) + '''      </div>
      <span class="mhelp" id="manHelp"></span>
    </div>
'''
t = sub(t, '''      <span class="mhelp" id="modeHelp"></span>
    </div>
''', '''      <span class="mhelp" id="modeHelp"></span>
    </div>
''' + MAN_ROW)

t = sub(t, '''    Hawaiian Airlines 2023 Pilots Agreement, effective March 2, 2023 to March 2, 2027.<br>
    Study aid only. The filed PDF governs. Verify anything you act on against the source.''',
        '''    Study aid only. The manuals in Drive govern. Verify anything you act on against the source.''')
t = sub(t, '<a class="go" id="ovlPdf" href="#">Open PDF page &#9654;</a>',
        '<a class="go" id="ovlPdf" href="#" target="_blank" rel="noopener">Open in Drive &#9654;</a>')

# ------------------------------------------------------------------ JS: state and synonyms
t = sub(t, "  var IDX = null, BM = null, LOADING = null;\n",
        "  var IDX = null, BM = null, LOADING = null;\n"
        "  var MANUALS = " + json.dumps(MANUALS, ensure_ascii=False) + ";\n"
        "  var BYKEY = {}; MANUALS.forEach(function (m) { BYKEY[m.key] = m; });\n"
        "  var BYSHORT = {}; MANUALS.forEach(function (m) { BYSHORT[m.short] = m; });\n"
        "  var STORE = {};        // key -> {meta, toc, docs, bm, parts:{name:1}}\n"
        "  var PENDING = {};      // key -> promise while a manual is loading\n"
        "  var SCOPE = 'ALL';     // manual key or ALL\n"
        "  function shortOf(k) { return BYKEY[k] ? BYKEY[k].short : k; }\n"
        "  function revText(k) { var m = BYKEY[k]; return m ? m.short + ' ' + (m.revision ? m.revision + ' \u00b7 ' : '') + m.date : k; }\n"
        "  // URL params, parsed first because ?base= steers every index fetch.\n"
        "  var QS = {};\n"
        "  try {\n"
        "    location.search.replace(/^\\?/, '').split('&').forEach(function (kv) {\n"
        "      if (!kv) return;\n"
        "      var i = kv.indexOf('='), k = decodeURIComponent(i < 0 ? kv : kv.slice(0, i));\n"
        "      QS[k] = decodeURIComponent((i < 0 ? '' : kv.slice(i + 1)).replace(/\\+/g, ' '));\n"
        "    });\n"
        "  } catch (e) {}\n"
        "  // The index JSON lives in an R2 bucket behind Cloudflare Access (company email sign-in),\n"
        "  // not in this repo. ?base=<url> overrides it so the headless test can serve it locally.\n"
        "  var MANUALS_BASE = QS.base ? String(QS.base).replace(/\\/+$/, '') : 'https://manuals.ha330pilot.app';\n"
        "  var AUTH = { ok: false, failed: false };\n")

SYN_NEW = '''  var SYN = {
    oxygen: ['oxy', 'mask', 'crew oxygen'], mask: ['oxygen', 'oxy', 'quick donning'],
    takeoff: ['tkof', 't.o', 'toga', 'flex'], landing: ['ldg', 'approach', 'touchdown'],
    gear: ['landing gear', 'l/g', 'lg'], autopilot: ['ap', 'a/p', 'fmgec'],
    autothrust: ['a/thr', 'athr', 'thrust lever'], director: ['fd', 'flight director'],
    engine: ['eng', 'trent', 'n1', 'epr'], hydraulic: ['hyd', 'green', 'blue', 'yellow'],
    electrical: ['elec', 'gen', 'bus'], pressurization: ['cab pr', 'cabin pressure', 'outflow valve'],
    flaps: ['flap', 'slat', 'conf'], radar: ['wxr', 'weather radar'], tcas: ['traffic', 'ra', 'ta'],
    terrain: ['gpws', 'egpws', 'pull up'], apu: ['auxiliary power unit', 'apu bleed'],
    fuel: ['fob', 'trim tank', 'jettison', 'imbalance'], brakes: ['brk', 'autobrake', 'antiskid'],
    ecam: ['warning', 'caution', 'master'], mcdu: ['fmgs', 'fms', 'fmgec', 'init', 'perf'],
    goaround: ['go around', 'ga', 'toga'], approach: ['appr', 'app', 'final', 'minimum'],
    autoland: ['cat ii', 'cat iii', 'cat 2', 'cat 3', 'land', 'flare'], minimums: ['minima', 'da', 'mda', 'dh', 'rvr'],
    alternate: ['altn', 'divert', 'diversion'], etops: ['orcn', 'oceanic', 'etp'],
    deice: ['de-ice', 'anti-ice', 'holdover', 'hot'], icing: ['ice', 'anti ice', 'wing anti ice', 'engine anti ice'],
    crosswind: ['xwind', 'wind', 'gust'], tailwind: ['tail wind', 'wind component'],
    mel: ['inoperative', 'inop', 'dispatch', 'deferred'], rest: ['fatigue', 'duty', 'crew rest'],
    memory: ['memory item', 'immediate action', 'from memory'], limitation: ['limit', 'maximum', 'minimum', 'max'],
    speed: ['vmo', 'mmo', 'vfe', 'vle', 'vlo', 'kt'], weight: ['mtow', 'mlw', 'mzfw', 'kg', 'lb'],
    pushback: ['push back', 'towing', 'tow'], taxi: ['taxiing', 'single engine taxi'],
    smoke: ['fumes', 'fire', 'avncs'], evacuation: ['evac', 'emer evac'], ditching: ['forced landing'],
    unreliable: ['adr', 'airspeed', 'pitot'], runway: ['rwy', 'contaminated', 'wet', 'rcam']
  };
'''
t = region(t, '  var SYN = {', '  function norm(w) {', SYN_NEW + '\n')

EXPAND_NEW = '''  function expand(terms, query) {
    var out = terms.slice(), joined = terms.join(' ');
    for (var key in SYN) {
      if (joined.indexOf(norm(key)) >= 0) SYN[key].forEach(function (s) { tok(s).forEach(function (t) { if (out.indexOf(t) < 0) out.push(t); }); });
    }
    return out;
  }
'''
t = region(t, '  var PAYQ = ', '  /* ---------- literal modes ----------', EXPAND_NEW + '\n')
t = sub(t, 'adds related contract terms.', 'adds related manual terms.')

# buildBM takes its docs so one table per manual is built once and merged per selection.
t = sub(t, '''  function buildBM() {
    var docs = IDX.docs, N = docs.length''', '''  function buildBM(docs) {
    var N = docs.length''')
t = sub(t, '''      var t = tok(docs[i].x), c = {}, ht = tok(docs[i].h || '');''',
        '''      var t = tok(docs[i].x), c = {}, ht = tok((docs[i].s || '') + ' ' + (docs[i].t || ''));''')

# search(): drop the pay and Compensation boosts, keep the explicit section reference boost.
t = region(t, '''    // a pay question belongs in Compensation''', '''    var order = [];''',
           '''    // explicit section reference, e.g. "DSC-35-20-30", "PRO-NOR-SOP-06", "5.4.2" or "21-51-1A"
    var secRef = query.match(/\\b([A-Z]{2,4}(?:-[A-Z0-9_]+)+|\\d{1,2}(?:\\.\\d{1,3})+|\\d{2}-\\d{2}-\\d{1,2}[A-Z]?)\\b/i);
    if (secRef) {
      var want = secRef[1].toUpperCase();
      for (var d3 = 0; d3 < BM.N; d3++) if (String(IDX.docs[d3].s).toUpperCase() === want) scores[d3] += 6;
    }
''')
t = sub(t, "' [rate table] '", "' [table] '")
t = sub(t, "  // Rate tables are walls of digits. Collapse them so the sentence survives.",
        "  // Performance tables are walls of digits. Collapse them so the sentence survives.")

# ------------------------------------------------------------------ JS: loader
LOAD_NEW = '''  /* ---------- index loading ----------
     One JSON per manual under /manuals/. Big manuals are split into parts listed in
     their main file; every part fetched is remembered so All never re-downloads. */
  function fetchJSON(path) {
    var url = MANUALS_BASE + path;
    return fetch(url, { credentials: 'include', mode: 'cors' }).then(function (r) {
      if (!r.ok || r.redirected) throw new Error(path.split('/').pop() + ' ' + (r.redirected ? 'redirected' : r.status));
      return r.json();
    });
  }
  // Access answers an unauthenticated request with a redirect to its login page, which the
  // browser reports as a CORS TypeError or a redirect. Either way: ask for the sign-in.
  function showSignIn() {
    AUTH.failed = true;
    $('status').innerHTML = 'Company email sign-in required for the manuals. ' +
      '<div class="seg" style="margin-top:8px"><button type="button" id="signIn">Sign in with @alaskaair.com</button></div>';
    $('signIn').addEventListener('click', function () {
      location.href = MANUALS_BASE + '/login.html?back=' + encodeURIComponent(location.href);
    });
  }
  function probeAuth() {
    return fetchJSON('/manifest.json').then(function (j) {
      AUTH.ok = true; AUTH.failed = false;
      return j;
    }).catch(function () { showSignIn(); throw new Error('sign-in'); });
  }
  function adopt(key, docs) {
    docs.forEach(function (d) { d.m = key; });
    return docs;
  }
  function loadManual(key) {
    if (STORE[key] && STORE[key].done) return Promise.resolve(STORE[key]);
    if (PENDING[key]) return PENDING[key];
    var m = BYKEY[key];
    setStatus('Loading the ' + m.short + ' index...');
    PENDING[key] = fetchJSON('/' + key + '.json').then(function (j) {
      var st = STORE[key] || (STORE[key] = { meta: j.meta, toc: j.toc, docs: [], parts: {}, done: false });
      st.meta = j.meta; st.toc = j.toc;
      if (!j.parts || !j.parts.length) {
        st.docs = adopt(key, j.docs || []);
        return st;
      }
      var todo = j.parts.filter(function (p) { return !st.parts[p.part]; }), got = 0;
      return todo.reduce(function (chain, p) {
        return chain.then(function () {
          return fetchJSON('/' + p.file).then(function (pj) {
            st.parts[p.part] = 1;
            st.docs = st.docs.concat(adopt(key, pj.docs || []));
            got++;
            setStatus('Loading the ' + m.short + ' index, ' + got + ' of ' + todo.length + ' parts...');
          });
        });
      }, Promise.resolve()).then(function () {
        st.docs.sort(function (a, b) { return a.p - b.p; });
        return st;
      });
    }).then(function (st) {
      st.bm = buildBM(st.docs);
      st.done = true;
      delete PENDING[key];
      return st;
    }).catch(function (e) {
      delete PENDING[key];
      if (!navigator.onLine) setStatus('No connection. The manuals index is served from the company sign-in bucket, so this search needs signal.');
      else showSignIn();
      throw e;
    });
    return PENDING[key];
  }
  // Merge the per-manual BM25 tables for the current scope into the engine's IDX and BM.
  function activate() {
    var keys = SCOPE === 'ALL' ? MANUALS.map(function (m) { return m.key; }) : [SCOPE];
    var docs = [], tf = [], len = [], df = {}, sum = 0;
    keys.forEach(function (k) {
      var st = STORE[k];
      if (!st || !st.done) return;
      docs = docs.concat(st.docs);
      tf = tf.concat(st.bm.tf); len = len.concat(st.bm.len); sum += st.bm.avg * st.bm.N;
      for (var w in st.bm.df) df[w] = (df[w] || 0) + st.bm.df[w];
    });
    IDX = { docs: docs };
    BM = { N: docs.length, df: df, tf: tf, len: len, avg: docs.length ? sum / docs.length : 1 };
    paintToc();
    paintProfile();
  }
  function load() {
    if (LOADING) return LOADING;
    var keys = SCOPE === 'ALL' ? MANUALS.map(function (m) { return m.key; }) : [SCOPE];
    var need = keys.filter(function (k) { return !(STORE[k] && STORE[k].done); });
    if (!need.length) { activate(); return Promise.resolve(IDX); }
    LOADING = need.reduce(function (chain, k) { return chain.then(function () { return loadManual(k); }); }, Promise.resolve())
      .then(function () { LOADING = null; activate(); setStatus(''); return IDX; })
      .catch(function (e) { LOADING = null; activate(); throw e; });
    return LOADING;
  }
  function paintToc() {
    var ol = $('tocList'); ol.innerHTML = '';
    var keys = SCOPE === 'ALL' ? MANUALS.map(function (m) { return m.key; }) : [SCOPE];
    keys.forEach(function (k) {
      var st = STORE[k];
      if (!st || !st.done) return;
      var li = document.createElement('li');
      var inner = st.toc.map(function (s) {
        return '<li><a class="cite" data-m="' + k + '" data-p="' + s.p + '" data-s="' + esc(String(s.s)) + '">' +
          esc(String(s.s)) + ' &mdash; ' + esc(s.t || '') + '</a></li>';
      }).join('');
      li.innerHTML = '<details><summary>' + esc(revText(k)) + ' &middot; ' + esc(st.meta.title) +
        ' &middot; ' + st.toc.length + ' sections</summary><ol>' + inner + '</ol></details>';
      ol.appendChild(li);
    });
  }
'''
t = region(t, '  function load() {', '  function setStatus(t) {', LOAD_NEW + '\n')

RENDER_NEW = '''  function render(hits) {
    var box = $('results'); box.innerHTML = '';
    if (!hits.length) { setStatus(emptyMsg()); return; }
    setStatus(hits.length + ' matching page' + (hits.length === 1 ? '' : 's') +
      ' · ' + MODES[MODE].label + (MODE === 'keywords' ? ', best first' : ' match') +
      ' · ' + scopeText() + '.');
    hits.forEach(function (h) {
      var d = h.doc, div = document.createElement('div'), mm = BYKEY[d.m];
      div.className = 'res';
      div.innerHTML =
        '<div class="h"><span>' + esc(shortOf(d.m)) + ' &middot; ' + esc(String(d.s)) + (d.t && d.t !== d.s ? ' &middot; ' + esc(d.t) : '') +
        (d.cp ? ' &middot; ' + esc(d.cp) : '') + '</span>' +
        '<span class="pg"><a href="' + esc(mm.drive_url) + '" target="_blank" rel="noopener">Open ' + esc(mm.short) + ' in Drive, p.' + d.p + ' &#9654;</a></span></div>' +
        '<div class="sn">' + (h.lit
          ? highlightLit(snippetLit(d.x, h.lit), h.lit)
          : highlight(snippet(d.x, h.terms), h.base)) + '</div>';
      div.setAttribute('role', 'button');
      div.setAttribute('tabindex', '0');
      div.addEventListener('click', function (ev) {
        if (ev.target.closest('a')) return;
        openRef(d.m, d.p, String(d.s), h.base.concat(h.terms));
      });
      div.addEventListener('keydown', function (ev) {
        if (ev.key === 'Enter' || ev.key === ' ') { ev.preventDefault(); div.click(); }
      });
      box.appendChild(div);
    });
  }

  function emptyMsg() {
    if (MODE === 'phrase') return 'That exact phrase is not in ' + scopeText() + '. Try Exact, or drop a word.';
    if (MODE === 'exact') return 'No page contains every one of those words. Try Keywords, or drop a word.';
    return 'No match in ' + scopeText() + '. Try different words, or a section id like DSC-35-20-30 or 5.4.2.';
  }
'''
t = region(t, '  function render(hits) {', '  function setMode(m, rerun) {', RENDER_NEW + '\n')
t = sub(t, "LS.set('pwa_search_mode', m);", "LS.set('manuals_search_mode', m);")
t = sub(t, "setMode(LS.get('pwa_search_mode', 'keywords'), false);", "setMode(LS.get('manuals_search_mode', 'keywords'), false);")

REF_NEW = '''  /* ---------- reference popout ---------- */
  function docByPage(key, pg) {
    var st = STORE[key];
    if (!st || !st.done) return null;
    for (var i = 0; i < st.docs.length; i++) if (st.docs[i].p === pg) return st.docs[i];
    return null;
  }

  function docsForSection(key, s) {
    var st = STORE[key];
    if (!st || !st.done) return [];
    return st.docs.filter(function (d) { return String(d.s) === String(s); }).sort(function (a, b) { return a.p - b.p; });
  }

  // A section is its labelled pages plus the page its toc entry starts on (FOM headings
  // start mid-page, so the start page carries the previous heading's label).
  function tocEntry(key, s) {
    var st = STORE[key];
    if (!st) return null;
    for (var i = 0; i < st.toc.length; i++) if (String(st.toc[i].s) === String(s)) return st.toc[i];
    return null;
  }
  function pagesForSection(key, s) {
    var out = docsForSection(key, s), e = tocEntry(key, s);
    if (e && !out.some(function (d) { return d.p === e.p; })) {
      var d0 = docByPage(key, e.p);
      if (d0) out.push(d0);
    }
    return out.sort(function (a, b) { return a.p - b.p; });
  }

  function drivePdf(key, pg) {
    var mm = BYKEY[key], a = $('ovlPdf');
    a.setAttribute('href', mm ? mm.drive_url : '#');
    a.innerHTML = 'Open ' + esc(mm ? mm.short : key) + ' in Drive, p.' + pg + ' &#9654;';
  }

  // Show the whole section, continuous, and jump to the page you came from.
  function openRef(key, pg, label, terms) {
    if (!BYKEY[key]) { key = BYSHORT[key] ? BYSHORT[key].key : key; }
    if (!BYKEY[key]) return;
    if (!STORE[key] || !STORE[key].done) {
      setStatus('Loading the ' + shortOf(key) + ' index...');
      loadManual(key).then(function () { activate(); setStatus(''); openRef(key, pg, label, terms); }).catch(function () {});
      return;
    }
    var d = docByPage(key, pg), e = label ? tocEntry(key, label) : null;
    if (!d && label) {
      var secPages = pagesForSection(key, label);
      if (secPages.length) { d = secPages[0]; pg = d.p; }
    }
    if (!d) {
      $('ovlTitle').textContent = shortOf(key) + ' PDF p.' + pg;
      $('ovlBody').innerHTML = 'That page is not in the offline index. Open the manual in Drive instead.';
      drivePdf(key, pg);
      $('ovl').classList.add('on');
      return;
    }
    var sec = e ? String(e.s) : String(d.s), secT = e ? (e.t || '') : (d.t || '');
    var all = pagesForSection(key, sec), list = all, note = '';
    if (all.length > 20) {                       // long sections: a window, not a novel
      var at = all.findIndex(function (x) { return x.p === d.p; });
      var from = Math.max(0, at - 8), to = Math.min(all.length, from + 20);
      list = all.slice(from, to);
      note = '<div class="pgnote">Showing pages ' + list[0].p + ' to ' + list[list.length - 1].p +
        ' of a ' + all.length + ' page section. Open the manual in Drive for the rest.</div>';
    }
    $('ovlTitle').textContent = shortOf(key) + ' · ' + sec + (secT && secT !== sec ? ' · ' + secT : '') +
      '  ·  ' + all.length + (all.length === 1 ? ' page' : ' pages');
    $('ovlBody').innerHTML = note + list.map(function (x) {
      return '<div class="pgmark" id="pgm' + x.p + '">' + esc(shortOf(key)) + ' · ' + esc(String(x.s)) + ' · PDF p.' + x.p + (x.cp ? '  ·  ' + esc(x.cp) : '') + '</div>' +
        '<div class="pgtext">' + highlight(x.x, terms || []) + '</div>';
    }).join('');
    drivePdf(key, pg);
    $('ovl').classList.add('on');
    var anchor = document.getElementById('pgm' + pg);
    if (anchor) $('ovlBody').scrollTop = anchor.offsetTop - 8; else $('ovlBody').scrollTop = 0;
  }

  function closeRef() { $('ovl').classList.remove('on'); }

  // Turn "(FCOM DSC-35-20-30 p.1945)", "(FOM 5.4.2, p.250)" and "(QRH p.121)" into popout links.
  var MANRE = MANUALS.map(function (m) { return m.short.replace(/[-]/g, '\\\\-'); }).sort(function (a, b) { return b.length - a.length; }).join('|');
  function linkCites(text) {
    var html = esc(text);
    html = html.replace(new RegExp('\\\\(\\\\s*(' + MANRE + ')\\\\s+([^()]{1,90}?)\\\\s*,?\\\\s*p\\\\.?\\\\s*(\\\\d{1,4})\\\\s*\\\\)', 'g'),
      function (m, man, sec, pg) {
        var key = BYSHORT[man] ? BYSHORT[man].key : man;
        return '<a class="cite" data-m="' + key + '" data-p="' + pg + '" data-s="' + sec.replace(/"/g, '') + '">' + m + '</a>';
      });
    html = html.replace(new RegExp('(^|[^"=;])\\\\(\\\\s*(' + MANRE + ')\\\\s*,?\\\\s*p\\\\.?\\\\s*(\\\\d{1,4})\\\\s*\\\\)', 'g'),
      function (m, pre, man, pg) {
        var key = BYSHORT[man] ? BYSHORT[man].key : man;
        return pre + '<a class="cite" data-m="' + key + '" data-p="' + pg + '">(' + man + ' p.' + pg + ')</a>';
      });
    return html;
  }
'''
t = region(t, '  /* ---------- reference popout ---------- */', '  // Lead sentence, then real bullets.', REF_NEW + '\n')

PROFILE_NEW = '''  /* ---------- scope, no pilot profile on this page ---------- */
  function PS() { return window.PortalSettings || null; }
  function scopeText() {
    if (SCOPE === 'ALL') return 'all manuals';
    var mm = BYKEY[SCOPE];
    return mm ? mm.short + (mm.revision ? ' ' + mm.revision : '') : SCOPE;
  }
  function paintProfile() {
    var keys = SCOPE === 'ALL' ? MANUALS.map(function (m) { return m.key; }) : [SCOPE];
    $('chips').innerHTML = keys.filter(function (k) { return STORE[k] && STORE[k].done; }).map(function (k) {
      return '<span class="chip">' + esc(shortOf(k)) + ' ' + STORE[k].docs.length + ' pp</span>';
    }).join('');
  }
'''
t = region(t, '  /* ---------- profile, from portal settings ---------- */', '  function updateAskState() {', PROFILE_NEW)

SYS_NEW = '''  /* ---------- ask ---------- */
  var SYS = 'You answer questions about the Hawaiian Airlines A330 passenger fleet from its manuals (FCOM, QRH, FCTM, FOM, MEL, AFM, PRC, PERF, NPC-CB, FODM). '
    + 'Use ONLY the excerpts provided. Answer in TLDR format: line 1 is the bottom line in one sentence under 20 words, '
    + 'then 2 to 5 one-line bullets under 18 words each, every bullet ending with its citation like (FCOM DSC-35-20-30 p.1945). '
    + 'A citation names the manual, the section id and the PDF page exactly as the excerpt marker prints them. '
    + 'No preamble, no closing summary, no em dashes, no run-on sentences. Numbers carry units and conditions. '
    + 'Never invent a section id, a page, or a figure.';
  var ROUTER_SYS = 'You route questions about the Hawaiian Airlines A330 manuals to the sections that answer them. '
    + 'Reply with the menu numbers only, comma separated, at most 4, most likely first. No words, no punctuation beyond commas. '
    + 'Choose generously: include any section that could plausibly govern any part of the question.';

  // Answer style lives in manuals/prompt.json so it can be tuned without touching this page.
  fetch('/manuals/prompt.json').then(function (r) { return r.ok ? r.json() : null; }).then(function (j) {
    if (!j) return;
    if (j.system) SYS = j.system;
    if (j.router) ROUTER_SYS = j.router;
  }).catch(function () {});

  // Section menu for the router pass: the distinct sections behind the top ranked pages,
  // numbered, so the router answers with numbers whatever shape the section ids have.
  function sectionMenu(hits) {
    var seen = {}, out = [];
    hits.forEach(function (h) {
      var d = h.doc, k = d.m + '|' + d.s;
      if (seen[k]) return;
      seen[k] = 1;
      out.push({ m: d.m, s: String(d.s), t: d.t || '' });
    });
    return out.slice(0, 120);
  }
  function sectionPages(key, s) {
    return pagesForSection(key, s);
  }
  var CTX_CAP = 140000;
  function buildWholeSections(entries, hits) {
    var out = [], used = 0, seenPage = {}, readList = [];
    entries.forEach(function (e) {
      var pages = sectionPages(e.m, e.s);
      if (!pages.length) return;
      var lab = shortOf(e.m) + ' ' + e.s;
      readList.push(lab + ' (' + pages.length + (pages.length === 1 ? ' page)' : ' pages)'));
      var head = '===== ' + lab + ' ' + (pages[0].t && pages[0].t !== e.s ? pages[0].t : '') + ', COMPLETE TEXT =====';
      var body = pages.map(function (d) {
        seenPage[d.m + '|' + d.p] = 1;
        return '[' + shortOf(d.m) + ' ' + d.s + ' p.' + d.p + (d.cp ? ', ' + d.cp : '') + '] ' + String(d.x || '').replace(/\\s+/g, ' ');
      }).join('\\n');
      var block = head + '\\n' + body;
      if (used + block.length > CTX_CAP) block = block.slice(0, Math.max(0, CTX_CAP - used));
      if (!block) return;
      out.push(block); used += block.length;
    });
    // Always append the ranked hits, so a page outside the routed sections still lands.
    var extra = [];
    hits.forEach(function (h) {
      var d = h.doc;
      if (seenPage[d.m + '|' + d.p]) return;
      seenPage[d.m + '|' + d.p] = 1;
      extra.push('[' + shortOf(d.m) + ' ' + d.s + ' p.' + d.p + (d.cp ? ', ' + d.cp : '') + '] ' + (d.t || '') +
        '\\n' + String(d.x || '').replace(/\\s+/g, ' '));
    });
    if (extra.length && used < CTX_CAP) {
      out.push('===== ADDITIONAL PAGES MATCHED BY SEARCH =====\\n' + extra.join('\\n\\n').slice(0, CTX_CAP - used));
    }
    return { text: out.join('\\n\\n'), read: readList };
  }
'''
t = region(t, '  /* ---------- ask ---------- */', '  /* ---------- attachments ----------', SYS_NEW + '\n')

IMG_NEW = '''  // The system prompt says to use ONLY the manual excerpts. That is right for
  // procedures and limits and wrong for an ECAM, MCDU or logbook screenshot the pilot
  // attached on purpose, so widen it only when images are actually present, and keep
  // the two sources separately citable so a fact's origin is never ambiguous.
  function imageRule(n) {
    return '\\n\\nThe user attached ' + n + ' image' + (n === 1 ? '' : 's') +
      ', such as an ECAM, MCDU page, weather, NOTAM, release or logbook screenshot. Treat those images as the ' +
      'situation being asked about: read the values, messages and entries they show. ' +
      'Keep using ONLY the manual excerpts for procedures, limits and policy. ' +
      'When a fact comes from an image, cite it as (from your image) rather than a section. ' +
      'If two images disagree, say which you used and why. Never invent a value that is in ' +
      'neither the excerpts nor the images. If an image is unreadable, say so rather than guessing.';
  }
'''
t = region(t, '  // The system prompt says to use ONLY the agreement excerpts.', '  function threadHTML() {', IMG_NEW + '\n')

t = sub(t, "      $('answerWho').textContent = s.modelLabel() + ' · asked as ' + profileText() +",
        "      $('answerWho').textContent = s.modelLabel() + ' · ' + scopeText() +")

ASK_BODY_OLD_START = '''    load().then(function () {
      paintProfile();
      var hits = search(q, 8);'''
ASK_NEW = '''    load().then(function () {
      paintProfile();
      var hits = search(q, 8);
      render(hits);
      var menuHits = search(q, 60);
      var menu = sectionMenu(menuHits);

      THREAD = { sys: SYS, messages: [], turns: [], readList: [], pendingQ: q, imgs: ATT.main.length };
      if (ATT.main.length) THREAD.sys = SYS + imageRule(ATT.main.length);
      $('answer').style.display = 'block';
      $('fuWrap').style.display = 'none';
      $('answerBody').innerHTML = workingHTML('Working out which sections govern this...');
      $('answerWho').textContent = s.modelLabel() + ' · ' + scopeText() +
        (s.threadsAreCheap && s.threadsAreCheap() ? '' : ' · follow-ups re-send the full text on this provider');

      var routerUser = 'Question: ' + q + '\\n\\nSection menu:\\n' + menu.map(function (e, i) {
        return (i + 1) + '. ' + shortOf(e.m) + ' ' + e.s + (e.t && e.t !== e.s ? ': ' + e.t : '');
      }).join('\\n');

      function fallbackEntries() {
        return menu.slice(0, 2);
      }
      function answerWith(entries) {
        var built = buildWholeSections(entries, hits);
        if (!built.text) { $('answerBody').textContent = 'Nothing in ' + scopeText() + ' matched.'; THREAD = null; return; }
        $('answerBody').innerHTML = workingHTML('Reading ' + (built.read.join(', ') || 'the matched pages') + '...');
        // Everything the thread will ever need from the manuals rides in this one
        // message, which is also the cache anchor. Follow-ups add a bare question.
        var user = 'Question: ' + q +
          '\\n\\nYou have been given the COMPLETE text of these sections of the Hawaiian Airlines A330 manuals: ' +
          (built.read.join('; ') || 'the pages matched by search') +
          '. Read all of it before answering. Cite the manual, section id and PDF page from the [MANUAL SECTION p.N] markers. ' +
          'Later questions in this conversation refer back to this same text.\\n\\n' + built.text;
        THREAD.readList = built.read;
        var first = { role: 'user', content: user };
        if (ATT.main.length) {
          first.images = ATT.main.map(function (im) { return { mime: im.mime, b64: im.b64 }; });
          ATT.main = []; paintAtts('main');
        }
        THREAD.messages.push(first);
        send(s);
      }

      s.ask(ROUTER_SYS, routerUser).then(function (txt) {
        var nums = String(txt || '').match(/\\d+/g) || [];
        var entries = [];
        nums.forEach(function (n) {
          var e = menu[parseInt(n, 10) - 1];
          if (e && entries.indexOf(e) < 0) entries.push(e);
        });
        entries = entries.slice(0, 4);
        if (!entries.length) entries = fallbackEntries();
        answerWith(entries);
      }).catch(function () {
        answerWith(fallbackEntries());
      });
    }).catch(function (e) {
      $('answer').style.display = 'block';
      $('answerBody').textContent = 'Could not load the manual index. ' + (e && e.message ? e.message : '');
    });
  }
'''
t = region(t, ASK_BODY_OLD_START, '  /* ---------- wire up ---------- */', ASK_NEW + '\n')

# ------------------------------------------------------------------ JS: wire-up
t = sub(t, '''    openRef(parseInt(a.getAttribute('data-p'), 10), a.getAttribute('data-l') || '', tok($('q').value || ''));''',
        '''    openRef(a.getAttribute('data-m') || SCOPE, parseInt(a.getAttribute('data-p'), 10), a.getAttribute('data-s') || '', tok($('q').value || ''));''')

WIRE_NEW = '''  /* ---------- manual selector ---------- */
  function setScope(k, rerun) {
    if (k !== 'ALL' && !BYKEY[k]) k = 'ALL';
    SCOPE = k;
    LS.set('manuals_scope', k);
    var more = k !== 'ALL' && MANUALS.slice(7).some(function (m) { return m.key === k; });
    ['manSeg', 'manSeg2', 'manSegMore'].forEach(function (id) {
      var btns = $(id).querySelectorAll('button');
      for (var i = 0; i < btns.length; i++) {
        var v = btns[i].getAttribute('data-man');
        btns[i].setAttribute('aria-pressed', (v === k || (v === 'more' && more)) ? 'true' : 'false');
      }
    });
    if (more) $('manSegMore').style.display = '';
    var mm = BYKEY[k];
    $('manHelp').textContent = k === 'ALL'
      ? 'Every manual. The first All search downloads every index (' + MANUALS.length + ' manuals, about 13 MB); they stay cached in this tab.'
      : mm.title + (mm.revision ? ' ' + mm.revision : '') + ', ' + mm.date + '.';
    activate();
    if (rerun && SEARCHED && $('q').value.trim()) doSearch();
  }
  ['manSeg', 'manSeg2', 'manSegMore'].forEach(function (id) {
    $(id).addEventListener('click', function (e) {
      var b = e.target.closest('button[data-man]');
      if (!b) return;
      var v = b.getAttribute('data-man');
      if (v === 'more') {
        var box = $('manSegMore'), open = box.style.display !== 'none';
        box.style.display = open ? 'none' : '';
        b.setAttribute('aria-pressed', open ? 'false' : 'true');
        return;
      }
      setScope(v, true);
    });
  });

  /* ---------- wire up ---------- */
'''
t = sub(t, '  /* ---------- wire up ---------- */\n', WIRE_NEW)

t = sub(t, '''  load().catch(function () {});
  if ('serviceWorker' in navigator) navigator.serviceWorker.register('/sw.js').catch(function () {});''',
        '''  // URL params: ?q=<text> prefills and runs a search, ?m=<key or short> preselects a manual,
  // ?s=<section id> opens that section's page modal (cross-reference links from other pages),
  // ?base=<url> points the index fetches at another host (local testing).
  var startScope = QS.m ? (BYKEY[QS.m] ? QS.m : (BYSHORT[QS.m.toUpperCase()] ? BYSHORT[QS.m.toUpperCase()].key : 'ALL'))
    : LS.get('manuals_scope', 'ALL');
  if (QS.s && !QS.m) {
    // guess the manual from the id shape, then confirm against the loaded toc
    var sid = QS.s.trim(), guess = [];
    var mq = sid.match(/^(FCOM|QRH|FCTM|FOM|MEL|AFM|AFM-SUPP|PRC|PERF|NPC-CB|FODM)\\s+(.+)$/i);
    if (mq) { guess = [BYSHORT[mq[1].toUpperCase()].key]; sid = mq[2]; }
    else if (/^(DSC|PRO|LIM|PER|GEN|PLP|TAB|BUL|TRL)\\b/i.test(sid)) guess = ['A330P_FCOM', 'A330_AFM'];
    else if (/^(PR|AS|AOP|GI|FI)\\b/i.test(sid)) guess = ['A330_FCTM'];
    else if (/^(ABN|EMER|NORM|MCDL|APP|SPERF|PERF|APPRO)\\b/i.test(sid)) guess = ['A330_AFM', 'A330P_FCOM'];
    else if (/^\\d{2}-\\d{2}/.test(sid)) guess = ['A330_MEL'];
    else if (/^\\d{1,2}(\\.\\d{1,3})*$/.test(sid)) guess = ['FOM', 'FODM'];
    else guess = ['A330P_QRH', 'A330_PRC', 'A330P_PERF'];
    QS.s = sid;
    var tries = guess.slice();
    var tryNext = function () {
      var k = tries.shift();
      if (!k) { setStatus('Section ' + sid + ' is not in the offline index.'); return; }
      loadManual(k).then(function (st) {
        var hit = st.toc.filter(function (e) { return String(e.s).toUpperCase() === sid.toUpperCase(); })[0];
        if (hit) { setScope(k, false); openRef(k, hit.p, String(hit.s), tok($('q').value || '')); }
        else tryNext();
      }).catch(tryNext);
    };
    setScope(startScope, false);
    probeAuth().then(tryNext).catch(function () {});
  } else {
    setScope(startScope, false);
    if (QS.q) $('q').value = QS.q;
    probeAuth().then(function () {
    if (QS.q) doSearch();
    if (QS.s) {
      loadManual(SCOPE === 'ALL' ? 'A330P_FCOM' : SCOPE).then(function (st) {
        var hit = st.toc.filter(function (e) { return String(e.s).toUpperCase() === QS.s.toUpperCase(); })[0];
        if (hit) openRef(st.meta.key, hit.p, String(hit.s), tok($('q').value || ''));
        else setStatus('Section ' + QS.s + ' is not in the ' + shortOf(st.meta.key) + ' index.');
      }).catch(function () {});
    }
    if (!QS.q && !QS.s && SCOPE !== 'ALL') load().catch(function () {});
    }).catch(function () {});
  }
  if ('serviceWorker' in navigator) navigator.serviceWorker.register('/sw.js').catch(function () {});''')

# The .sub meta line is static now; the loader no longer rewrites it.
assert "$('meta').textContent" not in t
assert 'pwa_' not in t.replace('pwa.html', ''), [l for l in t.split('\n') if 'pwa_' in l][:3]
assert 'profileText' not in t and 'PROFILE_INSTRUCTION' not in t and 'PAYQ' not in t
assert '—' not in re.sub(r'&mdash;', '', t.replace('—', '', 0)) or True
# no em dashes in page text (the &mdash; entity in the toc line mirrors the B787 page and renders as a dash)
assert '—' not in t, 'em dash in page'

os.makedirs(os.path.join(WORK, 'manuals'), exist_ok=True)
out = os.path.join(WORK, 'manuals', 'index.html')
open(out, 'w', encoding='utf-8').write(t)
print('wrote', os.path.relpath(out, WORK), len(t), 'bytes')
