#!/usr/bin/env python3
"""Guard against truncated or partial data pushes (the 2026-09-24 phase_flows.json loss).

Every data/*.json must parse, and the two flow banks must keep their full shape. Run before any
commit that touches data/, and in CI on every push. Exit 1 on any failure.
Floors are minimums, not exact counts: raise them when content grows, never lower them silently.
"""
import json, os, sys, glob
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
FLOORS = {
    'data/phase_flows.json': lambda d: [
        ('phases', len(d.get('phases', [])), 26),
        ('checklists', len(d.get('checklists', {})), 11),
        ('notes', len(d.get('notes', [])), 4),
        ('memory-items/limits/sim-notes phases',
         sum(p.get('id') in ('memory-items', 'limits', 'sim-notes') for p in d.get('phases', [])), 3)],
    'data/flows_trainer.json': lambda d: [
        ('flows', len(d.get('FLOWS', [])), 13),
        ('items', sum(len(f.get('items', [])) for f in d.get('FLOWS', [])), 209),
        ('normal checklists', len(d.get('NORMAL_CHECKLISTS', {})), 11),
        ('xrefs', len(d.get('XREFS', {})), 17)],
}
MIN_BYTES = {'data/phase_flows.json': 200_000, 'data/flows_trainer.json': 120_000}
fails = []
for p in sorted(glob.glob(os.path.join(ROOT, 'data', '*.json'))):
    rel = os.path.relpath(p, ROOT)
    try:
        d = json.load(open(p, encoding='utf-8'))
    except Exception as e:
        fails.append(f'{rel}: does not parse ({e})'); continue
    if rel in MIN_BYTES and os.path.getsize(p) < MIN_BYTES[rel]:
        fails.append(f'{rel}: {os.path.getsize(p)} bytes, below the {MIN_BYTES[rel]} floor (truncated push?)')
    for name, got, floor in FLOORS.get(rel, lambda d: [])(d):
        if got < floor: fails.append(f'{rel}: {name} {got} < {floor}')
for f in fails: print('INTEGRITY FAIL', f)
print('data integrity:', 'FAIL' if fails else 'ok')
sys.exit(1 if fails else 0)
