#!/usr/bin/env python3
"""Verify data/triggers.json against the source extracts.

Checks, per record:
  * `src` is a literal substring of the extract named by `ext`, after
    whitespace normalization (runs of whitespace -> one space) on both sides.
    The only markup allowed inside `src` is <wbr> (zero-width break opportunity
    inside long dotted leaders); it is stripped before the comparison. Any other
    '<' in src fails.
  * required keys present, category valid, fleet == pax, kind in the enum
  * no em dash (U+2014) anywhere in the record
  * flow items (if any) are non-empty strings
Exit code 1 on any failure. Prints pass/fail counts.
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.dirname(HERE)
SRC = os.path.normpath(os.path.join(WORK, '..', 'src'))
BANK = os.path.join(WORK, 'data', 'triggers.json')

EXTRACTS = {
    'FCOM': 'A330P_FCOM_R17_PRO-NOR.md',
    'FCTM': 'A330_FCTM_R5.md',
    'PRC': 'A330_PRC_2026-03-09.md',
    'QuickRef': 'QuickRef.md',
}
CATS = {'Phase Triggers', 'Approach Setup', 'Go-Around Brief', 'Checklist Order'}
KINDS = {'manual', 'sop', 'technique'}


def norm(s):
    return re.sub(r'\s+', ' ', s).strip()


def main():
    data = json.load(open(BANK, encoding='utf-8'))
    texts = {k: norm(open(os.path.join(SRC, v), encoding='utf-8').read()) for k, v in EXTRACTS.items()}
    ok = 0
    fails = []
    for i, d in enumerate(data):
        problems = []
        for k in ('s', 'q', 'a', 'ref', 'src', 'fleet', 'kind', 'ext'):
            if not d.get(k):
                problems.append(f'missing {k}')
        if d.get('s') not in CATS:
            problems.append(f'bad category {d.get("s")!r}')
        if d.get('fleet') != 'pax':
            problems.append(f'fleet {d.get("fleet")!r}')
        if d.get('kind') not in KINDS:
            problems.append(f'kind {d.get("kind")!r}')
        ext = d.get('ext')
        if ext not in texts:
            problems.append(f'unknown ext {ext!r}')
        else:
            raw = d.get('src', '')
            plain = raw.replace('<wbr>', '')
            if re.search(r'</?[a-zA-Z]', plain) or re.search(r'&[a-zA-Z#][a-zA-Z0-9]*;', plain):
                problems.append('markup in src other than <wbr>')
            if norm(plain) not in texts[ext]:
                problems.append(f'src not found in {ext}: {raw[:80]!r}')
        blob = json.dumps(d, ensure_ascii=False)
        if '—' in blob:
            problems.append('em dash present')
        fl = d.get('flow')
        if fl is not None:
            if not (isinstance(fl, dict) and fl.get('n') and isinstance(fl.get('i'), list) and fl['i']
                    and all(isinstance(x, str) and x.strip() for x in fl['i'])):
                problems.append('bad flow object')
        if problems:
            fails.append((i, d.get('q'), problems))
        else:
            ok += 1
    print(f'triggers.json: {len(data)} records, {ok} pass, {len(fails)} fail')
    for i, q, p in fails:
        print(f'  [{i}] {q}')
        for x in p:
            print(f'      - {x}')
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main())
