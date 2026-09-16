#!/usr/bin/env python3
"""Project the verified A330 source banks (data/limitations.json, data/memory_items.json)
into the exact record shapes the cloned B787 engines consume. Source files stay the
truth; the *_drill.json files are generated, never hand-edited."""
import json, re, os, html
ROOT=os.path.join(os.path.dirname(__file__),'..'); D=os.path.join(ROOT,'data')
def load(n): return json.load(open(os.path.join(D,n),encoding='utf-8'))
def dump(n,o):
    json.dump(o,open(os.path.join(D,n),'w',encoding='utf-8'),ensure_ascii=False,indent=1); print(n,len(o) if isinstance(o,list) else '')
ws=lambda s: re.sub(r'\s+',' ',(s or '')).strip()
def short_ref(ident, id_):
    book='AFM' if 'afm' in id_ else 'FCOM'
    m=re.match(r'([A-Z][A-Z_\-0-9]*?)(?:-\d{8}|\.\d)',ident)
    return f"{book} {m.group(1) if m else ident}"

# ---- limitations -> {s,q,a,ref,mem,src} ----
L=load('limitations.json'); out=[]; skipped=[]
for x in L:
    if x.get('fleet')=='frtr': continue
    p=ws(x['parameter']); c=ws(x.get('condition','')); lim=ws(x['limit'])
    q=p
    if c and c.lower() not in p.lower() and c.lower() not in ('all phases','') and len(c)<70: q=f"{p}, {c}"
    q=q.rstrip('?')+'?'
    mem = x.get('confidence')=='VERIFIED' and bool(re.search(r'\d',lim)) and 'graphic' not in lim.lower()
    if not mem: skipped.append(x['id'])
    out.append({'id':x['id'],'s':x['system'],'q':q,'a':lim,'ref':short_ref(x['ref'],x['id']),'mem':mem,
                'src':ws(x['verbatim'])+f" [{x['ref']}]",'fleet':x.get('fleet','pax'),'provenance':x.get('src','manual'),'confidence':x.get('confidence')})
dump('limitations_drill.json',out); print(' memorize set:',sum(1 for o in out if o['mem']),' excluded:',len(skipped))

# ---- limit-or-bust NUM / BOOL ----
NUM=[];BOOL=[]
unit_re=re.compile(r'^([+-]?\d[\d ]*(?:\.\d+)?)\s*(kt|ft|%|°C|PSI|psi|min|NM|nm|lb|kg|g|°)\b')
for o in out:
    if not o['mem']: continue
    m=unit_re.match(o['a'].replace('M ','M'))
    pl=o['q'].lower()
    if m:
        v=float(m.group(1).replace(' ','')); u=m.group(2)
        k='max' if 'max' in pl else 'min' if 'min' in pl else None
        if k:
            step=1 if v>=20 else 0.5 if v>=5 else 0.1
            NUM.append({'p':o['q'].rstrip('?'),'v':v,'u':u,'k':k,'ref':o['ref'],'step':step,'spread':max(step*6, round(v*0.25,1)) ,'dec':1 if step<1 else 0})
    elif re.search(r'\b(prohibited|not permitted|not allowed|must not|do not)\b',o['a'].lower()):
        BOOL.append({'p':o['q'].rstrip('?'),'legal':False,'ref':o['ref'],'lim':o['a']})
    elif re.search(r'\b(permitted|allowed|approved)\b',o['a'].lower()):
        BOOL.append({'p':o['q'].rstrip('?'),'legal':True,'ref':o['ref'],'lim':o['a']})
dump('limit_or_bust_num.json',NUM); dump('limit_or_bust_bool.json',BOOL)

# ---- memory items -> {name,ref,cond,fctm?,steps:[{t,n,h}]} ----
M=load('memory_items.json'); seen=set(); mi=[]
def fmt(line):
    line=html.escape(ws(line))
    if ' ... ' in line:
        a,b=line.rsplit(' ... ',1); return f"{a} ... <b>{b}</b>"
    return line
for x in M:
    name=re.sub(r'^\[MEM\]\s*','',x['procedure']).strip()
    if name in seen: continue   # EMER DESCENT is in FCOM and QRH with identical boxes; drill it once
    seen.add(name)
    steps=[]; n=0
    for ln in x['actions']:
        s=ws(ln)
        if not s: continue                       # box break
        if ' ... ' in s: n+=1; steps.append({'t':'n','n':str(n),'h':fmt(s)})
        elif s.endswith(':') or s.startswith(('"','\u201c')): steps.append({'t':'s','h':f"<i>{html.escape(s)}</i>"})
        else: steps.append({'t':'b','h':html.escape(s)})
    twin=[y for y in M if re.sub(r'^\[MEM\]\s*','',y['procedure']).strip()==name and y is not x]
    ref=f"{x['book']} {x['page_label']}" + (f" and {twin[0]['book']} {twin[0]['page_label']}" if twin else '')
    mi.append({'id':x['id'],'name':name,'ref':ref,'ident':x['ref'],'cond':'','steps':steps,
               'fctm':f"Memory items per {x['book']} {x['page_label']}, ident {x['ref']}. {x['classification']}. Boxed lines recited cold, verbatim.",
               'fleet':x.get('fleet','pax'),'provenance':x.get('src','manual')})
dump('memory_items_drill.json',mi)
