#!/usr/bin/env python3
"""Assemble WORK/data/oe.json from the parsed workbook items, the B787 FOM-grounded records
(reused only where their quote verifies against FOM 125.1) and the A330 answer parts."""
import json, re, sys, os, unicodedata
HERE = os.path.dirname(os.path.abspath(__file__))
SCR = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from norm import norm
import ans_part1, ans_part2, ans_part3, ans_part4, ans_extra

WB = json.load(open(os.path.join(HERE, 'wb_items.json')))
B787 = {r['id']: r for r in json.load(open(os.path.join(SCR, 'src', 'ioe_questions.json')))}
FOM = norm(open(os.path.join(SCR, 'src', 'FOM_125.1.md'), encoding='utf-8').read())

COI_SECS = {'1.1.1', '1.1.2.4', '2.1.1', '3.1.1', '5.1.1.5', '5.1.2.6', '13.1.1.1.1', '8.1.1.5', '9.1.1',
            '1.2.1.2.5.3', '16.1.1.7', '12.3.5', '12.1.8', '12.1.3', '12.3.2', '12.1.7', '12.1.9'}
SKIP = ('787 Flight Deck Overhead', 'OFCR/OFAR', 'AMM database', 'correct ECL', '(787) Where can you find a list of Cabin',
        '(787) Can the Airport map', '(787) TALPA', '(787) Max Crosswind for a HUD', '(787) Which fuel remaining', '(A321)')
MISC_SEC = ('Misc', 'Miscellaneous, not associated with grade sheet tasks')
MISC_GROUPS = {'Fuel Conservation', 'Flight Deck Entry Procedures/Security', 'Holding (Procedures, speeds)', 'TCAS',
               'Megaphone (remove/use/replace)', 'MedLink', 'De/Anti-Ice Procedures', 'Freighter Operations'}
DESK = "No published source located, ask the check airman"
WALK_RX = re.compile(r'^(Demonstrate|Review|Emphasize|Perform|Discuss|Gate Arrival|ACARS Post-Flight|Debrief|EFB IOS|FD Pro|Select desired|“REFRESH”|Western)', re.I)

OVR = {}
for mod in (ans_part1, ans_part2, ans_part3, ans_part4):
    for k, v in mod.A.items():
        OVR.setdefault(k, {}).update(v)

def fix_dashes(s):
    return (s or '').replace('—', ', ').replace('–', '-')

def tighten(q):
    q = q.strip()
    q = re.sub(r'\s*\(.*?\)\s*$', '', q) if len(q) > 90 else q
    return q

out = []
n = 0
for i, it in enumerate(WB):
    txt = it['text']
    if any(s in txt for s in SKIP) or it['group'] == 'Freighter Operations':
        continue
    sec, secTitle = it['sec'], it['secTitle']
    group = it['group']
    if sec == '11.1.10.4' and group in MISC_GROUPS:
        sec, secTitle = MISC_SEC
    b = B787.get(it.get('b787'))
    o = OVR.get(i, {})
    rec = dict(sec=sec, secTitle=secTitle, group=group, coi=sec in COI_SECS,
               status='verified', kind='walkthrough' if WALK_RX.match(txt) else 'drill',
               topic=(b or {}).get('topic') or 'General Operations', q=tighten(txt), a='', qOrig=txt,
               detail='', ref='', quote='', note='', icao='', src='')
    reused = False
    if it.get('fomq') and b:
        for f in ('q', 'a', 'detail', 'ref', 'quote', 'note', 'topic', 'kind'):
            rec[f] = b[f]
        rec['src'] = 'fom'; reused = True
        if rec['topic'] == 'Oceanic and NAT': rec['topic'] = 'Oceanic'
    if o:
        for f, v in o.items():
            if f == 'reuse':
                continue
            rec[f] = v
        if not o.get('reuse') and 'kind' not in o and 'q' in o:
            rec['kind'] = 'walkthrough' if WALK_RX.match(txt) else 'drill'
    if not reused and not o:
        rec.update(status='desktop', a='', note=DESK, detail='No FOM, FCOM, QRH, FCTM or PRC text answers this item.', ref='')
    # A reused record must keep a quote that verifies against the FOM extract
    if reused and rec['status'] == 'verified' and rec['quote'] and rec.get('src') == 'fom' and norm(rec['quote']) not in FOM:
        rec['status'] = 'desktop'
    for f in ('q', 'a', 'detail', 'note'):
        rec[f] = fix_dashes(rec[f])
    rec['fleet'] = 'pax'
    rec['_idx'] = i
    out.append(rec)
    # extra records that follow this workbook item
    for x in ans_extra.X:
        if x['after'] == i:
            xr = dict(x); xr.pop('after')
            xr.setdefault('icao', ''); xr['fleet'] = 'pax'; xr['_idx'] = i + 0.5
            for f in ('q', 'a', 'detail', 'note'):
                xr[f] = fix_dashes(xr[f])
            out.append(xr)

for k, rec in enumerate(out, 1):
    rec['id'] = 'oe-%03d' % k
    rec.pop('_idx', None)
    rec.setdefault('src', 'fom')
    if rec['status'] == 'desktop':
        rec['a'] = ''
        if DESK not in rec['note']:
            rec['note'] = (DESK + '. ' + rec['note']).strip()
for rec in out:
    rec['book'] = rec.get('src') or 'fom'
    rec['src'] = 'manual' if rec['book'] in ('fcom', 'qrh', 'fctm') else 'sop'
ORDER = ['id', 'sec', 'secTitle', 'group', 'coi', 'status', 'kind', 'topic', 'q', 'a', 'qOrig', 'detail', 'ref', 'quote', 'note', 'icao', 'book', 'src', 'fleet']
out = [{k: r.get(k, '') for k in ORDER} for r in out]
dst = os.path.join(SCR, 'work', 'data', 'oe.json')
json.dump(out, open(dst, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('wrote', dst, len(out), 'records')
