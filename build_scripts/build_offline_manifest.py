#!/usr/bin/env python3
"""Walk the deployable tree and write offline-manifest.json with real byte counts; patch the
size strings in portal-settings.js. Audio comes from data/episodes.json (media origin)."""
import json, os, datetime
os.chdir(os.path.join(os.path.dirname(__file__),'..'))
SKIP={'.git','build_scripts','docs','manuals','.gitignore','README.md','BUILD_NOTES.md','offline-manifest.json','CNAME','robots.txt','manuals.json'}
core=[]
for dp,dn,fn in os.walk('.'):
    dn[:]=[d for d in dn if d not in SKIP and not d.startswith('.')]
    for f in sorted(fn):
        if f in SKIP or f.endswith(('.md','.py','.sh','.mp3')): continue
        p=os.path.join(dp,f)[1:].replace(os.sep,'/')
        core.append({'u':p,'b':os.path.getsize(p[1:])})
core.sort(key=lambda x:x['u'])
audio=[]
try:
    for e in json.load(open('data/episodes.json',encoding='utf-8')):
        if e.get('audio'): audio.append({'u':e['audio'],'b':e.get('bytes',0)})
except Exception: pass
cb=sum(x['b'] for x in core); ab=sum(x['b'] for x in audio)
json.dump({'version':1,'built':datetime.date.today().isoformat(),'coreBytes':cb,'audioBytes':ab,'core':core,'audio':audio},open('offline-manifest.json','w'),indent=0)
print('core',len(core),'files',round(cb/1048576,1),'MB; audio',len(audio),'files',round(ab/1048576,1),'MB')
import re
s=open('portal-settings.js',encoding='utf-8').read()
s=re.sub(r'About \d+ MB\.</small>', f'About {max(1,round(cb/1048576))} MB.</small>', s, count=1)
s=re.sub(r'All \d+ episodes of Flight Deck Notes(?: plus the SFTD briefing)?\. About \d+ MB\.', f'All {len(audio)} episodes of Flight Deck Notes. About {round(ab/1048576)} MB.', s)
open('portal-settings.js','w',encoding='utf-8').write(s)
