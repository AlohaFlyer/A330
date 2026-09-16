#!/usr/bin/env python3
"""Verify data/weather.json against src/FOM_125.3.md.

Every record's src must be verbatim FOM text: after whitespace normalization (runs of
whitespace -> one space) each " ... "-separated fragment must be a literal substring of the
FOM extract, and the fragments must appear in FOM order within one 4000-character window
(so a src cannot be stitched from unrelated passages). Also checks required fields, fleet
values, ref format, tbl row shape, and no em dashes anywhere in the bank. Exit 1 on failure.

Usage: verify_weather.py [--fom PATH] [--work PATH]
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.abspath(os.path.join(HERE, '..'))
DEFAULT_FOM = os.path.abspath(os.path.join(WORK, '..', 'src', 'FOM_125.3.md'))
WINDOW = 4000

def norm(s):
    return re.sub(r'\s+', ' ', s).strip()

def main():
    fom_path, work = DEFAULT_FOM, WORK
    args = sys.argv[1:]
    while args:
        a = args.pop(0)
        if a == '--fom': fom_path = args.pop(0)
        elif a == '--work': work = args.pop(0)
    fom = norm(open(fom_path, encoding='utf-8').read())
    path = os.path.join(work, 'data', 'weather.json')
    recs = json.load(open(path, encoding='utf-8'))
    fails, frags = [], 0
    ref_re = re.compile(r'^FOM \d+(\.\d+)*$')
    for i, r in enumerate(recs):
        tag = '#%d %s' % (i + 1, r.get('q', '')[:50])
        for k in ('cat', 'ref', 'q', 'a', 'src', 'fleet', 'srcType'):
            if k not in r: fails.append('%s: missing %s' % (tag, k))
        if not isinstance(r.get('a'), list) or not r['a']: fails.append('%s: a must be a non-empty list' % tag)
        if r.get('fleet') not in ('pax', 'both'): fails.append('%s: fleet %r' % (tag, r.get('fleet')))
        if r.get('srcType') not in ('manual', 'sop', 'technique'): fails.append('%s: srcType %r' % (tag, r.get('srcType')))
        if not ref_re.match(r.get('ref', '')): fails.append('%s: ref %r not "FOM x.y.z"' % (tag, r.get('ref')))
        if 'tbl' in r:
            if not (isinstance(r['tbl'], list) and all(isinstance(x, list) and len(x) == 3 for x in r['tbl'])):
                fails.append('%s: tbl must be a list of [label, value, hi] rows' % tag)
        blob = json.dumps(r, ensure_ascii=False)
        if '—' in blob: fails.append('%s: em dash in record' % tag)
        src = norm(r.get('src', ''))
        if not src: fails.append('%s: empty src' % tag); continue
        parts = [p.strip() for p in src.split(' ... ') if p.strip()]
        pos, start = 0, None
        for p in parts:
            frags += 1
            j = fom.find(p, pos)
            if j < 0:
                if p in fom: fails.append('%s: fragment out of order: %s' % (tag, p[:80]))
                else: fails.append('%s: fragment not in FOM: %s' % (tag, p[:80]))
                break
            if start is None: start = j
            if j - start > WINDOW: fails.append('%s: fragments span > %d chars (not one passage): %s' % (tag, WINDOW, p[:60])); break
            pos = j + len(p)
    print('weather.json: %d records, %d fragments checked' % (len(recs), frags))
    for f in fails: print('FAIL', f)
    print('PASS' if not fails else '%d failure(s)' % len(fails))
    sys.exit(1 if fails else 0)

if __name__ == '__main__':
    main()
