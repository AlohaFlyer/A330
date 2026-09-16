#!/usr/bin/env python3
"""Move an inline `const NAME=[...];` (or {...};) bank out of a cloned page into data/<file>.json.
The rest of that <script> block is wrapped in the fetch callback so every engine line stays
byte-identical; functions called from inline onclick= handlers are re-exported to window.
Usage: externalize.py page.html NAME data/file.json [NAME2 data/file2.json ...]
Adds an empty-bank guard: if the first bank is empty the page shows a 'not loaded yet' card."""
import re, sys
page=sys.argv[1]; pairs=list(zip(sys.argv[2::2], sys.argv[3::2]))
t=open(page,encoding='utf-8').read()
# find the <script> that holds the first bank
first=pairs[0][0]
m=re.search(r'<script>\n(?=(?:[^<]|<(?!/script>))*?(?:const|var|let) '+first+r'\s*=)', t)
if not m: sys.exit('bank script not found')
s0=m.end(); e0=t.index('</script>', s0)
body=t[s0:e0]
fetches=[]
def literal_end(s, i):
    """i points at the opening [ or {. Return index just past the matching close, string-aware."""
    depth=0; q=None; j=i
    while j<len(s):
        c=s[j]
        if q:
            if c=='\\': j+=2; continue
            if c==q: q=None
        elif c in '"\'`': q=c
        elif c in '[{': depth+=1
        elif c in ']}':
            depth-=1
            if depth==0: return j+1
        j+=1
    raise SystemExit('unbalanced literal')
for name,path in pairs:
    bm=re.search(r'^(?:const|var|let) '+name+r'\s*=\s*(?=[\[{])', body, re.M)
    if not bm: sys.exit('bank '+name+' not found')
    end=literal_end(body, bm.end())
    # swallow the trailing ; and newline
    while end<len(body) and body[end] in ' ;': end+=1
    if end<len(body) and body[end]=='\n': end+=1
    body=body[:bm.start()]+body[end:]
    fetches.append((name,path))
funcs=sorted(set(re.findall(r'^function (\w+)\(', body, re.M)))
names=', '.join(n for n,_ in fetches)
load='Promise.all(['+', '.join(f"fetch('{p}',{{cache:'no-store'}}).then(r=>r.json())" for _,p in fetches)+'])'
guard=(f"if(!(Array.isArray({first})?{first}.length:Object.keys({first}).length)){{(document.getElementById('main')||document.getElementById('app')||document.getElementById('list')||document.getElementById('board')||document.body).innerHTML="
       "'<div class=\"card\"><div class=\"summary\"><div class=\"lbl\">Bank not loaded yet</div>"
       "<div class=\"srcsub\">This bank is built in a later step. The engine is live.</div></div></div>';return;}\n")
wrapped=(f"/* bank(s) {names} live in data/, loaded here; engine below is unchanged */\n"
         f"{load}.then(function(__b){{\nconst [{names}]=__b;\n{guard}{body.rstrip()}\n"
         f"Object.assign(window,{{{', '.join(funcs)}}});\n}}).catch(function(e){{(document.getElementById('main')||document.getElementById('app')||document.getElementById('list')||document.getElementById('board')||document.body).innerHTML='<div class=\"card\"><div class=\"summary\"><div class=\"lbl\">Bank failed to load</div><div class=\"srcsub\">'+e.message+'</div></div></div>';}});\n")
t=t[:s0]+wrapped+t[e0:]
open(page,'w',encoding='utf-8').write(t); print(page,'externalized',names,'funcs:',len(funcs))
