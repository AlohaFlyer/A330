#!/usr/bin/env python3
"""Tiny, enumerated edits to cloned pages that the record-shape projection needs. Each one is
listed in docs/PARITY_ALLOWLIST.md. Anything not listed here is a defect."""
import os; os.chdir(os.path.join(os.path.dirname(__file__),'..'))
EDITS={
 # TEMPORARY: the 14.6 MB PWA PDF exceeds the 10 MB browser-upload cap; until Ryan drags it into the
 # A330 repo (GitHub web, 25 MB limit) the viewer reads the sister portal's copy. Remove both lines then.
 'pwa_pdf.html':[
  ('<a id="direct" href="/2023-pwa.pdf">','<a id="direct" href="https://as787pilot.app/2023-pwa.pdf">'),
  ("var PDF = '/2023-pwa.pdf'","var PDF = 'https://as787pilot.app/2023-pwa.pdf'"),
 ],
 'memory-items.html':[
  ('<div class="cond">Condition: ${d.cond}</div>','${d.cond?`<div class="cond">Condition: ${d.cond}</div>`:``}'),
  ('Condition: ${d.cond}<br>','${d.cond?`Condition: ${d.cond}<br>`:``}'),
 ],
}
for f,eds in EDITS.items():
    t=open(f,encoding='utf-8').read()
    for a,b in eds:
        assert a in t, (f,a[:40]); t=t.replace(a,b)
    open(f,'w',encoding='utf-8').write(t); print('fixups:',f)
