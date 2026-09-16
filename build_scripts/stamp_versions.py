#!/usr/bin/env python3
"""Stamp page footers and the portal BUILD string from versions.json. Convention (same as the
B787): bump a page by 0.1 when its file changes, bump build every deploy."""
import json, re, os, glob
os.chdir(os.path.join(os.path.dirname(__file__),'..'))
V=json.load(open('versions.json'))
for f in glob.glob('*.html'):
    v=V['pages'].get(f, V['default']); t=open(f,encoding='utf-8').read()
    n=re.sub(r'Ver \d+\.\d+', f'Ver {v}', t)
    if n!=t: open(f,'w',encoding='utf-8').write(n)
s=open('portal-settings.js',encoding='utf-8').read()
s=re.sub(r"var BUILD = 'v[\d.]+';", f"var BUILD = '{V['build']}';", s); open('portal-settings.js','w',encoding='utf-8').write(s)
print('versions stamped, build', V['build'])
