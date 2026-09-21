import re,json,sys
txt=open('rev1.txt').read()
pages=txt.split('\f')
HEAD=re.compile(r'^\s*([A-Z][A-Za-z0-9 /&().,\'’-]{1,40}?)\s{3,}((?:DSC|PRO|LIM|QRH|FCTM|FOM|OEB)[^\n]*)$')
secs=[]; cur=None
for pi,pg in enumerate(pages):
    pno=pi+1
    for line in pg.split('\n'):
        if re.match(r'^Rev\. 1\s+\d+\s*$',line) or not line.strip(): continue
        m=HEAD.match(line)
        if m:
            cur={'h':m.group(1).strip(),'ref':m.group(2).strip(),'page':pno,'bul':[]}
            secs.append(cur); continue
        if cur is None: continue
        s=line.rstrip()
        ind=len(s)-len(s.lstrip())
        t=s.strip()
        if t.startswith('•'):
            cur['bul'].append({'t':t[1:].strip(),'sub':[],'page':pno,'ind':ind})
        elif re.match(r'^o\s',t) and cur['bul']:
            cur['bul'][-1]['sub'].append({'t':t[2:].strip(),'sub':[],'ind':ind})
        elif re.match(r'^[▪◦■]\s?',t) and cur['bul'] and cur['bul'][-1]['sub']:
            cur['bul'][-1]['sub'][-1]['sub'].append(re.sub(r'^[▪◦■]\s?','',t))
        else:
            # continuation: append to deepest open node
            if not cur['bul']: cur.setdefault('pre',[]).append(t); continue
            b=cur['bul'][-1]
            if b['sub']:
                ss=b['sub'][-1]
                if ss['sub']: ss['sub'][-1]+=' '+t
                elif ind>ss['ind']+1: ss['t']+=' '+t
                else: ss['t']+=' '+t
            else: b['t']+=' '+t
json.dump(secs,open('rev1_parsed.json','w'),indent=1)
tot=sum(len(s['bul']) for s in secs)
print(len(secs),'sections',tot,'bullets')
for s in secs: print(f"p{s['page']:2d} {s['h']:<28} {len(s['bul']):3d}  {s['ref']}")
