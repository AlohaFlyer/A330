#!/usr/bin/env python3
"""Stamp manual revision labels from manuals.json into the cloned pages, and render the
index footer revision table. Run after apply_strings.py. Idempotent on a fresh clone."""
import json, re, os, sys
ROOT=os.path.join(os.path.dirname(__file__),'..'); os.chdir(ROOT)
M=json.load(open('manuals.json'))
F=M['A330P_FCOM']; Q=M['A330P_QRH']; T=M['A330_FCTM']; MEL=M['A330_MEL']; FOM=M['FOM']; AFM=M['A330_AFM']
fr=F['revision']; qr=Q['revision']
RULES={
 'limitations.html':[
  ('<span class="src">FCOM R10 L.10</span>', f'<span class="src">FCOM {fr} LIM</span>'),
  ('Amber "Memorize" = memory item (#) per FCOM L.10', f'Amber "Memorize" = know-cold set, FCOM {fr} LIM'),
 ],
 'memory-items.html':[
  ('<span class="src">QRH R7</span>', f'<span class="src">FCOM {fr} [MEM]</span>'),
  ('QRH Source &mdash;', 'FCOM Source &mdash;'),
  ('QRH R7 (19 Jan 2026). Verbatim recall items above the dashed line, recited cold.', f'FCOM {fr} ({F["date"]}). [MEM] procedures, boxed lines recited cold, verbatim.'),
 ],
 'hot-seat.html':[
  ('<span class="src">QRH R7</span>', f'<span class="src">FCOM {fr} [MEM]</span>'),
  ('10 emergency injects, QRH R7 verbatim', f'10 emergency injects, FCOM {fr} verbatim'),
 ],
 'systems_quiz.html':[
  ('FCOM R10 &nbsp;|&nbsp; QRH R7', f'FCOM {fr} &nbsp;|&nbsp; QRH {qr}'),
  ('no supporting passage located in FCOM R10, FCTM R9, FOM, or QRH R7 during the source audit', f'no supporting passage located in FCOM {fr}, FCTM {T["revision"]}, FOM, or QRH {qr} during the source audit'),
  ('SFTD 1 & 2 study podcast','systems study podcast'),
 ],
 'podcast.html':[
  ('FCOM R10, FCTM R9, QRH R7, FOM 125.1, MEL R5', f'FCOM {fr}, FCTM {T["revision"]}, QRH {qr}, FOM {FOM["revision"]}, MEL {MEL["revision"]}'),
 ],
 'weather.html':[
  ('<span class="src">FOM Rev 125.1</span>', f'<span class="src">FOM Rev {FOM["revision"]}</span>'),
 ],
 'limit-or-bust.html':[
  ('<span class="src">FCOM L.10 &middot; FOM 9.2</span>', f'<span class="src">FCOM {fr} LIM</span>'),
  ('Snap judgment, FCOM L.10 limits', f'Snap judgment, FCOM {fr} LIM limits'),
 ],
}
def row(key,label):
    m=M[key]; rev=m['revision'] or ''; d=m['date']; link=m.get('drive_url') or '#'
    return f'      <tr><td><a href="{link}" target="_blank" rel="noopener">{label}</a></td><td>{rev}</td><td>{d}</td></tr>'
rows='\n'.join([row('A330P_FCOM','FCOM'),row('A330P_QRH','QRH'),row('A330_FCTM','FCTM'),row('FOM','FOM'),row('A330_MEL','MEL'),row('A330_AFM','AFM')])
RULES['index.html']=[(re.compile(r'    <tbody>\n.*?    </tbody>',re.S), '    <tbody>\n'+rows+'\n    </tbody>')]
for f,rules in RULES.items():
    t=open(f,encoding='utf-8').read(); o=t
    for a,b in rules:
        if isinstance(a,str):
            if a not in t: print(f'  MISS {f}: {a[:50]}')
            t=t.replace(a,b)
        else: t=a.sub(b,t)
    if t!=o: open(f,'w',encoding='utf-8').write(t); print('labels:',f)
