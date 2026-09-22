#!/usr/bin/env python3
"""Every Flows Trainer spine item (data/flows_trainer.json) must open with its paired phase-flows Cockpit Prep item:
title on the first detail line and every bullet of that item's `s` present. Source of truth: data/phase_flows.json."""
import json, os, sys
WORK = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
T = json.load(open(os.path.join(WORK, 'data', 'flows_trainer.json'), encoding='utf-8'))
PF = json.load(open(os.path.join(WORK, 'data', 'phase_flows.json'), encoding='utf-8'))
cp = next(p for p in PF['phases'] if p['id'] == 'cockpit-prep')
pitems = [it for sec in cp['sections'] for it in sec['items'] if it['k'] in ('box', 'fmc', 'cl')]
sp = next(f for f in T['FLOWS'] if f.get('spine'))
bad = []; pi = 0; prev = None; n = 0
for it in sp['items']:
    if not (prev is not None and it['item'] == prev['item']): pi += 1
    prev = it
    pit = pitems[pi - 1]
    d = it.get('d', '')
    lines = d.split('\n')
    if not d.startswith('[Phase flows') or len(lines) < 2 or lines[1] != pit['t']:
        bad.append((it['item'], 'title', pit['t'])); continue
    sub = pit.get('s') or ''
    for b in [x.strip() for x in (sub if isinstance(sub, list) else sub.split(' · ')) if x.strip()]:
        if ('• ' + b) not in d: bad.append((it['item'], 'bullet', b)); break
    n += 1
if pi != len(pitems): bad.append(('pairing', pi, len(pitems)))
print(f'spine items {len(sp["items"])} paired with {len(pitems)} phase items; in sync {n}; mismatches {len(bad)}')
for b in bad: print('  MISMATCH', b)
sys.exit(1 if bad else 0)
