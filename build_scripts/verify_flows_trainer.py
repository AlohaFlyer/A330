#!/usr/bin/env python3
"""Grounding check for data/flows_trainer.json (A330 Flows Trainer).

Every quoted line in an item's `d` (the lines under a "[FCOM <ident> ...:]" or "[FCTM <ident> ...:]"
header, bullets and prose alike), every XREF body line and every NORMAL_CHECKLISTS row must be a
literal substring of the named source extract after normalization:
  - runs of whitespace collapse to one space (the brief's rule);
  - dot leaders (3 or more periods) collapse to "......", because the PDF text prints each
    challenge/response line with a leader of arbitrary length;
  - a trailing " …" or " ..." on a quoted line marks a deliberate truncation and is stripped before the check;
  - the Airbus conditional-branch glyphs U+E113/U+E114 become "▸" on both sides.
Lines under "[Card vs FCOM:]", "[Exterior lights ...:]" and lines starting with a checklist mark are
labels or technique, not quotes, and are skipped. XREF bodies are checked against the manual their
`manual` field names (FCOM: the full A330P_FCOM_R17 extract, since cross-references leave PRO-NOR;
FCTM: A330_FCTM_R6); every XREF must also carry `ref` and a positive `page`. Checklist rows are checked as
"<challenge> <leader> <response>" against the FCTM (the A330 QRH R35 carries no normal checklists;
FCOM PRO-NOR-SOP refers to FCTM PR-NP-CL).
Usage: verify_flows_trainer.py [src_dir]   (default: the scratchpad src next to the work tree)
"""
import json, re, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); WORK = os.path.join(HERE, '..')
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(WORK, '..', 'src')
def norm(s):
    s = re.sub(r'[\ue113\ue114]', '▸', s)   # Airbus conditional-branch glyphs (private-use codepoints) -> arrow
    s = re.sub(r'\.{3,}', '......', s)
    return re.sub(r'\s+', ' ', s).strip()
TXT = {'FCOM': norm(open(os.path.join(SRC, 'A330P_FCOM_R17_PRO-NOR.md'), encoding='utf-8').read()),
       'FCOM_FULL': norm(open(os.path.join(SRC, 'A330P_FCOM_R17.md'), encoding='utf-8').read()),
       'FCTM': norm(open(os.path.join(SRC, 'A330_FCTM_R6.md'), encoding='utf-8').read())}
D = json.load(open(os.path.join(WORK, 'data', 'flows_trainer.json'), encoding='utf-8'))
HEAD = re.compile(r'^\[(FCOM|FCTM) ([^\]:]+):\]$')
SKIP = ('[', '✅', '🔶', '💡', '#')
ok = fail = 0; fails = []
def check(src, quote, where):
    global ok, fail
    q = quote.strip()
    if q.startswith('• '): q = q[2:]
    if q.endswith(' …'): q = q[:-2]
    if q.endswith(' ...'): q = q[:-4]
    q = norm(q)
    if not q: return
    if q in TXT[src]: ok += 1
    else: fail += 1; fails.append((where, src, q[:120]))
for f in D['FLOWS']:
    for it in f['items']:
        src = None
        for line in it['d'].split('\n'):
            m = HEAD.match(line)
            if m: src = m.group(1); continue
            if line.startswith(SKIP): src = None if line.startswith('[') else src; continue
            if src: check(src, line, f"{f['n']} / {it['item']}")
for k, x in D['XREFS'].items():
    src = 'FCTM' if x.get('manual') == 'FCTM' else 'FCOM_FULL'
    for line in x['body'].split('\n'):
        check(src, line, f'XREF {k}')
    if not x.get('ref') or not isinstance(x.get('page'), int) or x['page'] < 1:
        fail += 1; fails.append((f'XREF {k}', src, 'missing ref/page'))
    elif x['ref'] not in TXT[src]:
        fail += 1; fails.append((f'XREF {k}', src, f"ref {x['ref']} not printed in the extract"))
    else: ok += 1
for name, rows in D['NORMAL_CHECKLISTS'].items():
    for ch, resp, who in rows:
        q = norm(ch); r = norm(resp)
        pat = re.escape(q) + r'\s*(?:\.{6}\s*)?' + re.escape(r) if r else re.escape(q)
        if re.search(pat, TXT['FCTM']): ok += 1
        else: fail += 1; fails.append((f'CHECKLIST {name}', 'FCTM', f'{ch} / {resp}'))
for w, s, q in fails: print('FAIL', s, w, '::', q)
n_items = sum(len(f['items']) for f in D['FLOWS'])
print(f"flows {len(D['FLOWS'])} items {n_items} xrefs {len(D['XREFS'])} checklists {len(D['NORMAL_CHECKLISTS'])} "
      f"rows {sum(len(v) for v in D['NORMAL_CHECKLISTS'].values())} :: quotes ok {ok} fail {fail}")
sys.exit(1 if fail else 0)
