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
ft=load('data/flows_trainer.json'); docs=[]
for fl in (ft.get('FLOWS',[]) if isinstance(ft,dict) else []):
    for it in fl.get('items',[]):
        docs.append({'t':f"{fl.get('n','')}: {it.get('item','')}",'x':f"{it.get('item','')} {it.get('act','')} {it.get('role','')} {it.get('d','')}",'r':fl.get('ref','')})
out['flows']=('Flows Trainer','flows_quiz.html',docs)
M=json.load(open('manuals.json')); F=M['A330P_FCOM']; Q=M['A330P_QRH']; T=M['A330_FCTM']; FO=M['FOM']
SRC={'limitations':f"the Hawaiian Airlines A330 PAX FCOM {F['revision']} Limitations chapter and the A330 AFM",'memory':f"the Hawaiian Airlines A330 PAX FCOM {F['revision']} [MEM] procedures",'triggers':f"the Hawaiian Airlines A330 PAX FCOM {F['revision']} PRO-NOR-SOP, FCTM {T['revision']} and the A330 PRC",'weather':f"the Hawaiian Airlines FOM {FO['revision']}",'systems':f"the Hawaiian Airlines A330 systems question bank",'ioe':f"the Hawaiian Airlines Fleets OE Workbook, A330 sections, answered from FCOM {F['revision']}, QRH {Q['revision']}, FCTM {T['revision']} and FOM {FO['revision']}",'mcdu':f"the Hawaiian Airlines A330 PAX FCOM {F['revision']} PRO-NOR-SOP cockpit preparation",'fom':f"the Hawaiian Airlines FOM {FO['revision']}",'flows':f"the Hawaiian Airlines A330 PAX FCOM {F['revision']} PRO-NOR-SOP flows and FCTM {T['revision']} normal checklists"}
for k,(title,page,docs) in out.items():
    json.dump({'title':title,'page':page,'built':built,'source':SRC.get(k,''),'docs':docs},open(f'corpus/{k}.json','w',encoding='utf-8'),ensure_ascii=False)
    print(f'corpus/{k}.json {len(docs)}')
