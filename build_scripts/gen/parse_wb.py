import re, json
lines = open('src/OE_Workbook.txt', encoding='utf-8').read().split('\n')
SEC = re.compile(r'^(\d+(?:\.\d+)+)\s+(.*\S)\s*$')
items=[]; sec=None; secTitle=None; group=''
cur=None; prev_hdr=None; prev_raw=''
def flush():
    global cur
    if cur: items.append(cur); cur=None
start = next(i for i,l in enumerate(lines) if l.startswith('1.2.3 '))
for raw in lines[start:]:
    l = raw.rstrip(); s = l.strip()
    if not s: continue
    if re.fullmatch(r'\d+', s): continue
    if 'Fleets OE Workbook' in s: continue
    m = SEC.match(s)
    if m and not s.startswith(('•','o ')):
        flush(); sec, secTitle = m.group(1), m.group(2); group=''; prev_hdr='sec'; prev_raw=raw; continue
    if s.startswith('•'):
        flush(); cur={'sec':sec,'secTitle':secTitle,'group':group,'text':s[1:].strip(),'sub':False}; prev_hdr=None; prev_raw=raw; continue
    if s.startswith('o '):
        flush(); cur={'sec':sec,'secTitle':secTitle,'group':group,'text':s[2:].strip(),'sub':True}; prev_hdr=None; prev_raw=raw; continue
    if cur is not None and len(raw)-len(raw.lstrip())>=8:
        cur['text'] += ' ' + s; prev_raw=raw; continue
    if prev_hdr=='sec' and cur is None and not raw.startswith(' ') and len(prev_raw.rstrip())>95:
        secTitle += ' ' + s; prev_raw=raw; continue
    if s.startswith('Miscellaneous'):
        flush(); sec, secTitle = 'Misc', 'Miscellaneous, not associated with grade sheet tasks'; group=''; prev_hdr='sec'; prev_raw=raw; continue
    flush(); group = s; prev_hdr='grp'; prev_raw=raw
flush()
old = json.load(open('scratch/wb_items_old.json'))
assert len(old)==len(items), (len(old), len(items))
for o,n in zip(old,items):
    assert o['text']==n['text'], (o['text'], n['text'])
    for k in ('b787','b787sim','fomq'):
        if k in o: n[k]=o[k]
json.dump(items, open('scratch/wb_items.json','w'), indent=1, ensure_ascii=False)
import collections
print(len(items)); print(collections.Counter((i['sec'],i['group']) for i in items).most_common()[:80])
