#!/usr/bin/env python3
"""Cross-page chrome: drop the footer mailto lines (contact now lives in Portal Settings) and give
every page the apple-touch-icon and manifest links so an iOS Add to Home Screen from any page
gets the A330 icon. Runs after page_fixups."""
import re, glob, os
os.chdir(os.path.join(os.path.dirname(__file__),'..'))
LINKS='<link rel="apple-touch-icon" href="/assets/icons/icon-180.png">\n<link rel="manifest" href="/site.webmanifest">\n<meta name="theme-color" content="#463C8F">\n'
for f in glob.glob('*.html')+glob.glob('manuals/*.html'):
    t=open(f,encoding='utf-8').read(); o=t
    t=re.sub(r'\s*<a[^>]*href="mailto:[^"]*"[^>]*>[^<]*</a>', '', t)
    if 'apple-touch-icon' not in t: t=t.replace('</head>', LINKS+'</head>',1)
    if t!=o: open(f,'w',encoding='utf-8').write(t); print('chrome:',f)
