#!/usr/bin/env python3
"""Verify the Manuals indexes against the source extracts.

For every manual index under manuals/:
  - every doc's x is a substring of its extract page (whitespace collapsed, C0 controls
    dropped, the same normalization build_manuals_index.norm_text applies), and of the
    whole extract;
  - page counts match: docs + blank pages + excluded pages == form-feed pages, and every
    doc p is unique and within 1..pdfPages;
  - section ids are unique in the toc, every doc's s is in the toc, and every toc page
    exists as a doc;
  - split manuals: the parts listed in the main file exist, hold the byte size the main
    file claims, and their docs cover the manual exactly once;
  - manifest.json lists every index file under manuals/ with its real byte size, and
    nothing outside manuals/ contains manual text (spot check: a distinctive FCOM line
    must not appear in any root html/json/js file).
Exit 1 on any failure. Prints the pass count per manual.
"""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.abspath(os.path.join(HERE, '..'))
sys.path.insert(0, HERE)
import build_manuals_index as B

OUT = os.path.join(WORK, 'manuals')
WS = re.compile(r'\s+')


def ws(s):
    return WS.sub(' ', B.CTRL.sub('', s)).strip()


fails = []


def check(cond, msg):
    if not cond:
        fails.append(msg)


total_docs = 0
manifest = json.load(open(os.path.join(OUT, 'manifest.json'), encoding='utf-8'))
mf = {f['file']: f['bytes'] for f in manifest['files']}
listed = set()
probe = None

for key, fn in B.FILES.items():
    text = open(os.path.join(B.SRC, fn), encoding='utf-8').read()
    pages = B.pages_of(text)
    flat = ws(text)
    main = json.load(open(os.path.join(OUT, key + '.json'), encoding='utf-8'))
    meta, toc = main['meta'], main['toc']
    docs = list(main.get('docs') or [])
    listed.add(key + '.json')
    if main.get('parts'):
        for p in main['parts']:
            path = os.path.join(OUT, p['file'])
            check(os.path.exists(path), '%s: missing part %s' % (key, p['file']))
            check(os.path.getsize(path) == p['bytes'], '%s: part %s bytes %d != %d' % (key, p['file'], os.path.getsize(path), p['bytes']))
            pj = json.load(open(path, encoding='utf-8'))
            check(pj['meta']['key'] == key and pj['meta']['part'] == p['part'], '%s: part meta mismatch %s' % (key, p['file']))
            check(len(pj['docs']) == p['pages'], '%s: part %s pages %d != %d' % (key, p['file'], len(pj['docs']), p['pages']))
            docs += pj['docs']
            listed.add(p['file'])
    docs.sort(key=lambda d: d['p'])
    # pages
    check(meta['pdfPages'] == len(pages), '%s: pdfPages %d != %d form feeds' % (key, meta['pdfPages'], len(pages)))
    ps = [d['p'] for d in docs]
    check(len(ps) == len(set(ps)), '%s: duplicate page numbers' % key)
    check(all(1 <= p <= len(pages) for p in ps), '%s: page out of range' % key)
    excluded = set(meta.get('excludedPages', []))
    blank = [i + 1 for i, pg in enumerate(pages) if not B.norm_text(pg)]
    covered = set(ps) | excluded | set(blank)
    check(covered == set(range(1, len(pages) + 1)), '%s: page cover mismatch, missing %s' % (key, sorted(set(range(1, len(pages) + 1)) - covered)[:10]))
    check(len(ps) + len(excluded) + len(set(blank) - excluded) == len(pages), '%s: docs+excluded+blank != pages' % key)
    # text grounding
    bad = 0
    for d in docs:
        x = ws(d['x'])
        if not x or x not in ws(pages[d['p'] - 1]) or x not in flat:
            bad += 1
            if bad <= 3:
                fails.append('%s: p%d text not a substring of its page' % (key, d['p']))
        for f in ('p', 's', 't', 'cp', 'x'):
            check(f in d, '%s: p%s missing field %s' % (key, d.get('p'), f))
        check('—' not in d['s'] and '—' not in d['t'], '%s: em dash in section label p%d' % (key, d['p']))
    check(bad == 0, '%s: %d docs fail grounding' % (key, bad))
    # sections
    ss = [str(e['s']) for e in toc]
    check(len(ss) == len(set(ss)), '%s: duplicate section ids in toc: %s' % (key, [s for s in ss if ss.count(s) > 1][:5]))
    tocset = set(ss)
    docpages = set(ps)
    check(all(str(d['s']) in tocset for d in docs), '%s: doc section not in toc' % key)
    check(all(e['p'] in docpages for e in toc), '%s: toc page without doc' % key)
    check(len(toc) == meta['sections'], '%s: meta.sections %d != %d' % (key, meta['sections'], len(toc)))
    check(len(docs) == meta['pages'], '%s: meta.pages %d != %d' % (key, meta['pages'], len(docs)))
    for f in ('key', 'title', 'revision', 'date', 'pdfPages', 'drive_url', 'built'):
        check(f in meta, '%s: meta missing %s' % (key, f))
    check(meta['key'] == key, '%s: meta key' % key)
    # manifest sizes
    check(os.path.getsize(os.path.join(OUT, key + '.json')) == mf.get(key + '.json'), '%s: manifest size wrong for main file' % key)
    if key == 'A330P_FCOM':
        probe = ws([d for d in docs if d['s'] == 'DSC-35-20-30'][0]['x'])[:120]
    total_docs += len(docs)
    print('%-14s docs %5d  sections %5d  grounding %s' % (key, len(docs), len(toc), 'FAIL' if bad else 'ok'))

# manifest completeness
for f in sorted(os.listdir(OUT)):
    if f.endswith('.json') and f not in ('manifest.json', 'prompt.json'):
        check(f in mf, 'manifest: %s not listed' % f)
        check(mf.get(f) == os.path.getsize(os.path.join(OUT, f)), 'manifest: size wrong for %s' % f)
for f in mf:
    check(os.path.exists(os.path.join(OUT, f)), 'manifest: listed file missing %s' % f)
check(manifest['totalBytes'] == sum(mf.values()), 'manifest: totalBytes wrong')

# no manual text outside manuals/
for dp, dns, fs in os.walk(WORK):
    if os.path.basename(dp) in ('manuals', '.git', 'build_scripts', 'docs'):
        dns[:] = []
        continue
    for f in fs:
        if f.endswith(('.html', '.json', '.js')):
            try:
                t = ws(open(os.path.join(dp, f), encoding='utf-8').read())
            except Exception:
                continue
            check(probe not in t, 'manual text leaked into %s' % os.path.relpath(os.path.join(dp, f), WORK))

# the page itself: no em dashes, the engine scripts absolute, sw registered
page = open(os.path.join(OUT, 'index.html'), encoding='utf-8').read()
check('—' not in page, 'index.html: em dash')
check('src="/portal-settings.js"' in page and 'src="/assist.js"' in page, 'index.html: engine script paths')
check("register('/sw.js')" in page, 'index.html: sw.js')
check("fetch('/manuals/" in page and "fetch('/pwa_" not in page, 'index.html: fetch paths')

print('docs total', total_docs, '| manifest files', len(mf), '| %.1f MB' % (manifest['totalBytes'] / 1e6))
if fails:
    print('FAIL', len(fails))
    for f in fails[:40]:
        print('  ', f)
    sys.exit(1)
print('VERIFY OK')
