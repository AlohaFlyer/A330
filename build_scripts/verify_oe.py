#!/usr/bin/env python3
"""Verify data/oe.json, the A330 OE Workbook bank.

Every quote must be a literal substring of the named source extract after whitespace
normalization. Prints PASS or FAIL per record and a summary. Exit 1 on any failure.

Usage: verify_oe.py [--src DIR] [--bank FILE] [--quiet]
  DIR holds A330P_FCOM_R17.md, A330P_FCOM_R17_PRO-NOR.md, A330P_QRH_R35.md,
  A330_FCTM_R5.md, A330_PRC_2026-03-09.md, FOM_125.1.md
"""
import json, re, sys, os, argparse, unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.dirname(HERE)
BOOKS = {
    'fcom': 'A330P_FCOM_R17.md',
    'pro':  'A330P_FCOM_R17_PRO-NOR.md',
    'qrh':  'A330P_QRH_R35.md',
    'fctm': 'A330_FCTM_R5.md',
    'prc':  'A330_PRC_2026-03-09.md',
    'fom':  'FOM_125.1.md',
}
DESK = "No published source located, ask the check airman"
FLEET_RX = re.compile(r'\b(EICAS|CDU|FMC|QRC|ECL|OFCR|OFAR|Dreamliner|Boeing|B787|A330F)\b', re.I)
KEYS = ['id', 'sec', 'secTitle', 'group', 'coi', 'status', 'kind', 'topic', 'q', 'a', 'qOrig',
        'detail', 'ref', 'quote', 'note', 'icao', 'book', 'src', 'fleet']


_MAP = {'\u201c': '"', '\u201d': '"', '\u2018': "'", '\u2019': "'", '\u2013': '-', '\u2014': '-', '\u2212': '-',
        '\u2010': '-', '\u2011': '-', '\u00a0': ' '}
_PUA = re.compile(r'[\ue000-\uf8ff\ufeff\u200b]')  # icon glyphs left by the PDF extract


def norm(s):
    """Whitespace normalization: quotes and dashes unified, private-use icon glyphs dropped,
    runs of whitespace collapsed to one space."""
    s = unicodedata.normalize('NFKC', s or '')
    for a, b in _MAP.items():
        s = s.replace(a, b)
    s = _PUA.sub('', s)
    return re.sub(r'\s+', ' ', s).strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--src', default=os.path.join(os.path.dirname(WORK), 'src'))
    ap.add_argument('--bank', default=os.path.join(WORK, 'data', 'oe.json'))
    ap.add_argument('--quiet', action='store_true')
    ns = ap.parse_args()

    texts = {}
    for k, fn in BOOKS.items():
        path = os.path.join(ns.src, fn)
        if os.path.exists(path):
            texts[k] = norm(open(path, encoding='utf-8', errors='replace').read())
        else:
            print('MISSING extract', path)
    bank = json.load(open(ns.bank, encoding='utf-8'))

    fails = 0
    stats = dict(total=len(bank), verified=0, desktop=0, walkthrough=0, coi=0, quoted=0)
    ids = set()
    for r in bank:
        probs = []
        for k in KEYS:
            if k not in r:
                probs.append('missing field ' + k)
        if r['id'] in ids:
            probs.append('duplicate id')
        ids.add(r['id'])
        if r['status'] not in ('verified', 'desktop'):
            probs.append('bad status')
        if r['kind'] not in ('drill', 'walkthrough'):
            probs.append('bad kind')
        if r.get('fleet') != 'pax':
            probs.append('fleet must be pax')
        if r.get('src') not in ('manual', 'sop', 'technique'):
            probs.append('bad src')
        book = r.get('book')
        if r['quote']:
            if book not in texts:
                probs.append('unknown book %r' % book)
            elif norm(r['quote']) not in texts[book]:
                probs.append('quote not in %s' % BOOKS[book])
            else:
                stats['quoted'] += 1
        if r['status'] == 'verified':
            stats['verified'] += 1
            if not r['quote']:
                probs.append('verified without quote')
            if not r['a'].strip():
                probs.append('verified without answer')
            if not r['ref'].strip():
                probs.append('verified without ref')
        else:
            stats['desktop'] += 1
            if r['a'].strip():
                probs.append('desktop with answer text')
            if DESK not in r['note']:
                probs.append('desktop note missing check airman line')
        if r['kind'] == 'walkthrough':
            stats['walkthrough'] += 1
        if r['coi']:
            stats['coi'] += 1
        for f in ('q', 'a', 'detail', 'note', 'ref'):
            if '—' in (r.get(f) or ''):
                probs.append('em dash in ' + f)
            m = FLEET_RX.search(r.get(f) or '')
            if m and f != 'ref':
                probs.append('other-fleet term %r in %s' % (m.group(0), f))
        lim = 30 if r['kind'] == 'walkthrough' else 24
        if r['status'] == 'verified' and len(r['a'].split()) > lim:
            probs.append('answer over %d words' % lim)
        line = ('PASS ' if not probs else 'FAIL ') + r['id'] + ' ' + r['sec'] + ' | ' + r['q'][:60]
        if probs:
            fails += 1
            print(line + '\n      ' + '; '.join(probs))
        elif not ns.quiet:
            print(line)
    print('\nRESULT: %d records, %d verified, %d desktop, %d walkthrough, %d COI, %d quotes checked, %d FAIL'
          % (stats['total'], stats['verified'], stats['desktop'], stats['walkthrough'], stats['coi'], stats['quoted'], fails))
    sys.exit(1 if fails else 0)


if __name__ == '__main__':
    main()
