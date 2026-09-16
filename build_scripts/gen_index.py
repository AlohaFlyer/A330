#!/usr/bin/env python3
"""Rewrite the index tile subtitles from the data banks so counts never drift, swap the
banner logo and hero placeholders, and point icon links at assets/icons/. Run after gen_labels."""
import json, re, os
os.chdir(os.path.join(os.path.dirname(__file__),'..'))
def n(p):
    try:
        j=json.load(open(p,encoding='utf-8')); return len(j) if isinstance(j,list) else len(j.get('docs') or j.get('phases') or j)
    except Exception: return 0
M=json.load(open('manuals.json')); fr=M['A330P_FCOM']['revision']
lim=json.load(open('data/limitations_drill.json')); mem=[x for x in lim if x['mem']]
mi=n('data/memory_items_drill.json'); fl=n('data/flows.json')
sysq=n('data/systems.json') if os.path.exists('data/systems.json') else 0
eps=n('data/episodes.json') if os.path.exists('data/episodes.json') else 0
SUB={
 'phase_flows.html':'Interactive flows, callouts, checklists, memory items &amp; limitations',
 'ioe.html':'Fleets OE Workbook, A330 sections - short cards, answer on tap, citation and verbatim quote behind Source',
 'flows_quiz.html':f'Gate to gate, {fl} flows, sequence drill and poster',
 'mcdu_preflight.html':f'FCOM {fr} PRO-NOR-SOP page-flow spine + 1-page PDF handout',
 'triggers.html':'Event &rarr; flow &rarr; checklist: gate-to-gate trigger drill, approach setup, go-around brief, checklist order',
 'limitations.html':f'FCOM {fr} LIM - {len(mem)} know-cold limitations drill, {len(lim)} in the bank',
 'memory-items.html':f'FCOM {fr} [MEM] procedures - all {mi}, verbatim recall',
 'systems_quiz.html':(f'{sysq:,} questions, vetted against current manuals' if sysq else 'Engine live - question bank lands when the training bank is supplied'),
 'fom_quiz.html':'Flight Operations Manual, chapter by chapter, each question with its FOM source citation',
 'weather.html':'FOM weather and alternate planning, vetted, with 1-page PDF handout',
 'podcast.html':(f'Learn-by-banter A330 podcast with Pualani, Chester &amp; Otto - all {eps} episodes' if eps else 'Learn-by-banter A330 podcast with Pualani, Chester &amp; Otto - first episodes coming'),
 'pwa.html':'Hawaiian 2023 Pilots Agreement - ask a question, ranked offline search, full PDF',
}
t=open('index.html',encoding='utf-8').read()
for href,sub in SUB.items():
    t,k=re.subn(r'(href="'+re.escape(href)+r'"><span>(?:<span class="nw">)?[^<]*(?:</span>)?<small>)[^<]*(</small>)', lambda m: m.group(1)+sub+m.group(2), t)
    if k!=1: print('  tile miss',href)
# banner logo: Hawaiian Airlines wordmark, white text on the midnight banner (assets/hawaiian_logo.png, Ryan 2026-09-16)
import base64
_logo='data:image/png;base64,'+base64.b64encode(open('assets/hawaiian_logo.png','rb').read()).decode()
t=re.sub(r'<img src="data:image/png;base64,[A-Za-z0-9+/=]+" alt="Hawaiian Airlines">', lambda m: '<img src="'+_logo+'" alt="Hawaiian Airlines">', t)
t=t.replace('href="/favicon.ico"','href="/assets/icons/favicon.ico"').replace('href="/favicon-32x32.png"','href="/assets/icons/icon-32.png"').replace('href="/favicon-16x16.png"','href="/assets/icons/icon-16.png"').replace('href="/apple-touch-icon.png"','href="/assets/icons/icon-180.png"')
# Manuals tile, directly above the ALPA tile, same tint class (no new CSS)
if 'href="manuals/"' not in t:
    t=t.replace('  <a class="alpa" href="pwa.html">', '  <a class="alpa" href="manuals/"><span>Manuals<small>FCOM, QRH, FCTM, FOM, MEL, AFM, PRC - search every manual at once, ask Pualani, company email login</small></span><span class="arrow">&#9654;</span></a>\n  <a class="alpa" href="pwa.html">',1)
open('index.html','w',encoding='utf-8').write(t); print('index rewritten')
for f in ['pwa.html','pwa_pdf.html','fom_quiz.html','jeopardy.html']:
    s=open(f,encoding='utf-8').read(); o=s
    s=s.replace('href="/favicon.ico"','href="/assets/icons/favicon.ico"').replace('href="favicon.ico"','href="/assets/icons/favicon.ico"').replace('href="/apple-touch-icon.png"','href="/assets/icons/icon-180.png"')
    if s!=o: open(f,'w',encoding='utf-8').write(s)
w=open('site.webmanifest').read().replace('"/icon-192.png"','"/assets/icons/icon-192.png"').replace('"/icon-512.png"','"/assets/icons/icon-512.png"'); open('site.webmanifest','w').write(w)
