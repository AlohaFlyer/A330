#!/usr/bin/env python3
"""Load every page of the A330 tree (and optionally the B787 tree) headless, capture console
errors and failed requests, screenshot at phone and desktop widths, and compare structure.
Usage: smoke.py <a330 dir> [<b787 dir>]   -> writes docs/parity/*.png and prints a report."""
import sys, os, subprocess, time, json, http.server, threading, functools
from playwright.sync_api import sync_playwright
A=os.path.abspath(sys.argv[1]); B=os.path.abspath(sys.argv[2]) if len(sys.argv)>2 else None
OUT=os.path.join(A,'docs','parity'); os.makedirs(OUT,exist_ok=True)
def serve(d,port):
    h=functools.partial(http.server.SimpleHTTPRequestHandler,directory=d)
    s=http.server.ThreadingHTTPServer(('127.0.0.1',port),h); threading.Thread(target=s.serve_forever,daemon=True).start(); return s
serve(A,8331); 
if B: serve(B,8787)
PAGES=['index.html','limitations.html','memory-items.html','hot-seat.html','limit-or-bust.html','triggers.html','weather.html','wx-alternate.html','systems_quiz.html','jeopardy.html','podcast.html','ioe.html','fom_quiz.html','pwa.html','pwa_pdf.html','view.html?f=A330_Memory_Limitations.pdf','phase_flows.html','flows_quiz.html','mcdu_preflight.html']
MAP={'mcdu_preflight.html':'cdu_preflight.html','view.html?f=A330_Memory_Limitations.pdf':'view.html?f=B787_Memory_Limitations.pdf'}
report=[]
with sync_playwright() as p:
    br=p.chromium.launch()
    for W,H,tag in [(390,844,'phone'),(1280,800,'desk')]:
        ctx=br.new_context(viewport={'width':W,'height':H},device_scale_factor=1)
        for pg in PAGES:
            for side,base,port in [('a330',A,8331)]+([('b787',B,8787)] if B else []):
                url=f'http://127.0.0.1:{port}/'+(MAP.get(pg,pg) if side=='b787' else pg)
                page=ctx.new_page(); errs=[]; fails=[]
                page.on('console',lambda m: errs.append(m.text) if m.type=='error' else None)
                page.on('requestfailed',lambda r: fails.append(r.url))
                page.on('response',lambda r: fails.append(f'{r.status} {r.url}') if r.status>=400 else None)
                try:
                    page.goto(url,wait_until='networkidle',timeout=20000)
                    if pg=='index.html':
                        page.evaluate("document.cookie='ha330_access=1;path=/';localStorage.setItem('ha330_email','x@alaskaair.com');document.cookie='as787_access=1;path=/';localStorage.setItem('as787_email','x@alaskaair.com')")
                        page.reload(wait_until='networkidle')
                    page.wait_for_timeout(600)
                    name=pg.split('?')[0].replace('.html','')
                    page.screenshot(path=os.path.join(OUT,f'{name}_{tag}_{side}.png'),full_page=True)
                    skel=page.evaluate("(()=>{const w=[];document.querySelectorAll('body *').forEach(e=>{if(['SCRIPT','STYLE'].includes(e.tagName))return;w.push(e.tagName+(e.className&&typeof e.className==='string'?'.'+e.className.trim().split(/\\s+/).join('.'):''))});return w.join('|')})()")
                    report.append({'page':pg,'side':side,'view':tag,'errors':errs,'fails':[f for f in fails if 'favicon' not in f],'skel':skel})
                except Exception as e:
                    report.append({'page':pg,'side':side,'view':tag,'errors':[str(e)],'fails':fails,'skel':''})
                page.close()
        ctx.close()
    br.close()
json.dump(report,open(os.path.join(OUT,'smoke.json'),'w'),indent=1)
bad=0
for r in report:
    if r['side']!='a330': continue
    if r['errors'] or r['fails']:
        bad+=1; print(f"[{r['view']}] {r['page']}: errors={r['errors'][:3]} fails={r['fails'][:4]}")
if B:
    for pg in PAGES:
        a=[r for r in report if r['page']==pg and r['side']=='a330' and r['view']=='desk']
        b=[r for r in report if r['page']==pg and r['side']=='b787' and r['view']=='desk']
        if a and b:
            sa,sb=a[0]['skel'].split('|'),b[0]['skel'].split('|')
            import difflib; ratio=difflib.SequenceMatcher(None,sa,sb).ratio()
            print(f"skeleton {pg:48s} {ratio:.3f}  ({len(sa)} vs {len(sb)} nodes)")
print('pages with errors:',bad)
