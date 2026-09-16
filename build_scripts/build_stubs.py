#!/usr/bin/env python3
"""Pages whose A330 content ships in a later build step are replaced by a stub that carries the
portal chrome (home icon, header, card, footer, settings, assist) and says which step fills it.
Remove a page from STUBS once its real build lands."""
import re, os, json
os.chdir(os.path.join(os.path.dirname(__file__),'..'))
STUBS={}
tpl=open('limitations.html',encoding='utf-8').read()
head=tpl[:tpl.index('<body>')]; homebar=re.search(r'<div class="ps-homebar">.*?</div>\n', tpl, re.S).group(0)
footer=tpl[tpl.index('<footer'):]
for f,(title,h1,sub,src,step) in STUBS.items():
    h=re.sub(r'<title>.*?</title>', f'<title>{title}</title>', head)
    body=f'''<body>
{homebar}
<div class="wrap">
  <header>
    <h1>{h1} <span class="sub">{sub}</span></h1>
    <span class="src">{src}</span>
  </header>
  <div id="app"><div class="card"><div class="summary"><div class="lbl">Building</div><div class="srcsub">This page ships in build step {step}. The portal chrome, settings and offline tiers are already live.</div></div></div></div>
</div>

'''
    ft=re.sub(r'Ver [0-9.]+', 'Ver 0.1', footer).replace('Limitations%20Drill', h1.replace(' ','%20'))
    open(f,'w',encoding='utf-8').write(h+body+ft); print('stub:',f)
