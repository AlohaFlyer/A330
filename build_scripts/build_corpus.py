#!/usr/bin/env python3
"""Derive corpus/<key>.json ({title,page,built,docs:[{t,x,r}]}) for assist.js from the data banks.
Empty banks produce an empty corpus so Search this section reports 'nothing here' cleanly."""
import json, os, re, datetime
os.chdir(os.path.join(os.path.dirname(__file__),'..')); os.makedirs('corpus',exist_ok=True)
built=datetime.date.today().isoformat()
strip=lambda h: re.sub(r'<[^>]+>','',h).replace('&quot;','"').replace('&amp;','&').replace('&lt;','<').replace('&gt;','>')
def load(p):
    try: return json.load(open(p,encoding='utf-8'))
    except Exception: return []
out={}
lim=load('data/limitations_drill.json')
out['limitations']=('Limitations','limitations.html',[{'t':d['q'],'x':f"{d['q']} {d['a']} {d['src']} {d['s']}",'r':d['ref']} for d in lim])
mi=load('data/memory_items_drill.json')
out['memory']=('Memory Items','memory-items.html',[{'t':d['name'],'x':d['name']+' '+' '.join(strip(s['h']) for s in d['steps'])+' '+strip(d.get('fctm','')),'r':d['ref']} for d in mi])
def simple(key,title,page,path,tf,xf,rf):
    rows=load(path); out[key]=(title,page,[{'t':tf(d),'x':xf(d),'r':rf(d)} for d in rows] if isinstance(rows,list) else [])
simple('triggers','Triggers','triggers.html','data/triggers.json',lambda d:d['q'],lambda d:f"{d['q']} {d['a']} {d.get('src','')}",lambda d:d.get('ref',''))
simple('weather','Weather','weather.html','data/weather.json',lambda d:d['q'],lambda d:f"{d['q']} {' '.join(strip(a) for a in d['a'])} {d.get('src','')}",lambda d:d.get('ref',''))
simple('systems','Systems Quiz','systems_quiz.html','data/systems.json',lambda d:d['q'],lambda d:f"{d['q']} {d['a']} {d.get('src','')} {d.get('system','')}",lambda d:f"{d.get('system','')} · {d.get('src','')}")
simple('ioe','OE Workbook Trainer','ioe.html','data/oe.json',lambda d:d['q'],lambda d:f"{d['q']} {d['a']} {d.get('detail','')} {d.get('quote','')}",lambda d:f"{d.get('sec','')} {d.get('secTitle','')}")
simple('mcdu','MCDU Preflight (PF)','mcdu_preflight.html','data/mcdu.json',lambda d:d['t'],lambda d:d['x'],lambda d:d.get('r',''))
simple('fom','FOM Quizzer','fom_quiz.html','data/fom_all.json',lambda d:d['q'],lambda d:f"{d['q']} {d['a']} {d.get('src',{}).get('quote','') if isinstance(d.get('src'),dict) else ''}",lambda d:f"{d.get('chapterName','')} {d.get('ref','')}")
fl=load('data/flows.json'); docs=[]
for ph in (fl.get('phases',[]) if isinstance(fl,dict) else []):
    for st in ph.get('steps',[]):
        if isinstance(st,dict): docs.append({'t':f"{ph.get('label','')}: {st.get('item',st.get('t',''))}",'x':json.dumps(st,ensure_ascii=False),'r':ph.get('src','')})
out['flows']=('Flows Trainer','flows_quiz.html',docs)
for k,(title,page,docs) in out.items():
    json.dump({'title':title,'page':page,'built':built,'docs':docs},open(f'corpus/{k}.json','w',encoding='utf-8'),ensure_ascii=False)
    print(f'corpus/{k}.json {len(docs)}')
