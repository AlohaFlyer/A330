#!/usr/bin/env python3
"""Verify data/phase_flows.json against the manual extracts.

Every step, checklist and note record that carries a `quote` must be a literal substring of the
extract named by its `ext` key after normalization:
  - runs of whitespace collapse to one space
  - dot leaders (three or more dots, with any surrounding spaces) collapse to " ... "
  - the U+2010 hyphen bullet and U+00A0 are treated as "-" and " "; private-use glyph markers are dropped
Also checks: every phase/step carries fleet + src, every quote has a ref, every checklist named by a
`cl` item exists in `checklists`, no em dashes anywhere, no B787/Boeing vocabulary in the data.

Usage: verify_phase_flows.py [src_dir]   (src_dir defaults to ../../src next to the work tree)
Exit code 1 on any failure."""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.abspath(os.path.join(HERE, '..'))
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(WORK), 'src')

EXTRACTS = {
    'FCOM PRO-NOR': 'A330P_FCOM_R17_PRO-NOR.md',
    'FCOM': 'A330P_FCOM_R17.md',
    'QRH': 'A330P_QRH_R35.md',
    'FCTM': 'A330_FCTM_R5.md',
    'PRC': 'A330_PRC_2026-03-09.md',
    'FOM': 'FOM_125.1.md',
}

def norm(s):
    s = s.replace('\u2010', '-').replace('\u2011', '-').replace('\u00a0', ' ')
    s = re.sub('[\ue000-\uf8ff]', ' ', s)   # private-use glyphs: option / trademark / condition markers in the extracts
    s = re.sub(r'\s*\.{3,}\s*', ' ... ', s)
    s = re.sub(r'\s+', ' ', s)
    return s.strip()

_cache = {}
def extract(key):
    if key not in _cache:
        p = os.path.join(SRC, EXTRACTS[key])
        _cache[key] = norm(open(p, encoding='utf-8').read())
    return _cache[key]

BOEING = re.compile(r'\b(B787|787|Boeing|EICAS|CDU|MCP|FLCH|TO/GA|autothrottle|A/T ARM|speedbrake lever|IAN|VREF|Dreamliner|NNC|PDSC 787)\b')

def main():
    data = json.load(open(os.path.join(WORK, 'data', 'phase_flows.json'), encoding='utf-8'))
    fails, quotes, steps = [], 0, 0
    raw = open(os.path.join(WORK, 'data', 'phase_flows.json'), encoding='utf-8').read()
    if '—' in raw:
        fails.append('em dash present in phase_flows.json')
    for m in BOEING.finditer(raw):
        fails.append(f'Boeing/B787 vocabulary in data: {m.group(0)!r} at offset {m.start()}')
    cls = data['checklists']
    for ph in data['phases']:
        if ph.get('fleet') not in ('pax', 'both') or ph.get('provenance') not in ('manual', 'sop', 'technique'):
            fails.append(f"{ph['id']}: phase missing fleet/provenance (phase.src is the engine's display string)")
        for sec in ph['sections']:
            for it in sec['items']:
                if it['k'] in ('box', 'fmc'):
                    steps += 1
                    if it.get('fleet') not in ('pax', 'both') or it.get('src') not in ('manual', 'sop', 'technique'):
                        fails.append(f"{ph['id']} | {it['t'][:40]}: step missing fleet/src")
                if it['k'] == 'cl' and it['t'] not in cls:
                    fails.append(f"{ph['id']}: checklist {it['t']!r} not in checklists map")
                q = it.get('quote')
                if q:
                    quotes += 1
                    ext, ref = it.get('ext'), it.get('ref')
                    if not ref:
                        fails.append(f"{ph['id']} | {it.get('t','')[:40]}: quote without ref")
                    if ext not in EXTRACTS:
                        fails.append(f"{ph['id']} | {it.get('t','')[:40]}: unknown ext {ext!r}")
                        continue
                    if norm(q) not in extract(ext):
                        fails.append(f"{ph['id']} | {it.get('t','')[:40]} | {ext}: quote not found: {norm(q)[:110]}")
    for name, cl in cls.items():
        q = cl.get('quote')
        if q:
            quotes += 1
            if norm(q) not in extract(cl.get('ext', 'FCTM')):
                fails.append(f"checklist {name}: trigger quote not found: {norm(q)[:110]}")
    for n in data.get('notes', []):
        q = n.get('quote')
        if q:
            quotes += 1
            if norm(q) not in extract(n.get('ext', 'FCOM PRO-NOR')):
                fails.append(f"note {n.get('h','')[:40]}: quote not found: {norm(q)[:110]}")
    print(f"phases={len(data['phases'])} steps={steps} quotes={quotes} checklists={len(cls)} notes={len(data.get('notes', []))}")
    for f in fails:
        print('FAIL', f)
    print('failures:', len(fails))
    sys.exit(1 if fails else 0)

if __name__ == '__main__':
    main()
