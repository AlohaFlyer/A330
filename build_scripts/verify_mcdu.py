#!/usr/bin/env python3
"""Grounding check for data/mcdu.json: every doc's x must be a verbatim substring of the FCOM
PRO-NOR extract after whitespace normalization (runs of whitespace -> one space).
Usage: verify_mcdu.py [path-to-A330P_FCOM_R17_PRO-NOR.md]   (default: ../src next to the repo)"""
import json, os, re, sys
os.chdir(os.path.join(os.path.dirname(__file__), '..'))
src = sys.argv[1] if len(sys.argv) > 1 else os.path.join('..', 'src', 'A330P_FCOM_R17_PRO-NOR.md')
norm = lambda s: re.sub(r'\s+', ' ', s).strip()
corpus = norm(open(src, encoding='utf-8').read())
docs = json.load(open('data/mcdu.json', encoding='utf-8'))
bad = []
for d in docs:
    assert set(d) == {'t', 'x', 'r'} and all(isinstance(d[k], str) and d[k] for k in d), d
    if norm(d['x']) not in corpus: bad.append(d['t'])
    if '—' in d['x'] or '—' in d['t']: bad.append(d['t'] + ' (em dash)')
    if not d['r'].startswith('FCOM PRO-NOR-SOP-0'): bad.append(d['t'] + ' (ref)')
page = open('mcdu_preflight.html', encoding='utf-8').read()
if '—' in page: bad.append('mcdu_preflight.html (em dash)')
print(f'mcdu.json: {len(docs)} docs, {len(docs)-len([b for b in bad if "(" not in b])} verbatim, {len(bad)} failures')
for b in bad: print('  FAIL', b)
sys.exit(1 if bad else 0)
