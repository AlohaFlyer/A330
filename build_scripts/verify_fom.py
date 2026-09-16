#!/usr/bin/env python3
"""Verify the FOM Quizzer bank.

Every record's src.quote must be a literal substring of the FOM extract after
whitespace normalization (runs of whitespace -> one space). Also checks the
manifest counts, id uniqueness, id format, required fields, and no em dashes
in q/a/note text. Exit 1 on any failure.

Usage: verify_fom.py [--fom PATH] [--work PATH]
"""
import json, os, re, sys, glob

HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.abspath(os.path.join(HERE, '..'))
DEFAULT_FOM = os.path.abspath(os.path.join(WORK, '..', 'src', 'FOM_125.1.md'))

def norm(s):
    return re.sub(r'\s+', ' ', s).strip()

def main():
    fom_path = DEFAULT_FOM
    work = WORK
    args = sys.argv[1:]
    while args:
        a = args.pop(0)
        if a == '--fom': fom_path = args.pop(0)
        elif a == '--work': work = args.pop(0)
    fom = norm(open(fom_path, encoding='utf-8').read())
    manifest = json.load(open(os.path.join(work, 'data', 'fom_questions.json')))
    fails = []
    total = 0
    ids = set()
    id_re = re.compile(r'^fom\d{2}-\d{3}$')
    all_flat = []
    for ch in manifest['chapters']:
        path = os.path.join(work, ch['file'])
        recs = json.load(open(path, encoding='utf-8'))
        if len(recs) != ch['count']:
            fails.append('%s: manifest count %d != %d records' % (ch['file'], ch['count'], len(recs)))
        for r in recs:
            total += 1
            all_flat.append(r)
            rid = r.get('id', '?')
            if rid in ids: fails.append('%s: duplicate id' % rid)
            ids.add(rid)
            if not id_re.match(rid): fails.append('%s: bad id format' % rid)
            for k in ('id', 'chapter', 'chapterName', 'q', 'a', 'ref', 'src', 'fleet'):
                if k not in r: fails.append('%s: missing %s' % (rid, k))
            if r.get('chapter') != ch['chapter']: fails.append('%s: chapter %r != manifest %r' % (rid, r.get('chapter'), ch['chapter']))
            if r.get('chapterName') != ch['name']: fails.append('%s: chapterName mismatch' % rid)
            if r.get('fleet') not in ('pax', 'both'): fails.append('%s: fleet %r' % (rid, r.get('fleet')))
            s = r.get('src') or {}
            q = norm(s.get('quote', ''))
            if not q: fails.append('%s: empty quote' % rid)
            elif q not in fom: fails.append('%s: quote not in FOM: %s' % (rid, q[:90]))
            for k in ('q', 'a'):
                if '—' in r.get(k, ''): fails.append('%s: em dash in %s' % (rid, k))
            if '—' in (s.get('note') or ''): fails.append('%s: em dash in note' % rid)
    flat_path = os.path.join(work, 'data', 'fom_all.json')
    if os.path.exists(flat_path):
        flat = json.load(open(flat_path))
        if [x['id'] for x in flat] != [x['id'] for x in all_flat]:
            fails.append('fom_all.json does not match chapter files')
    else:
        fails.append('data/fom_all.json missing')
    print('records: %d  chapters: %d  failures: %d' % (total, len(manifest['chapters']), len(fails)))
    for f in fails: print('FAIL', f)
    sys.exit(1 if fails else 0)

if __name__ == '__main__':
    main()
