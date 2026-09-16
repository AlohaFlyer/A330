#!/usr/bin/env python3
"""Tiny, enumerated edits to cloned pages that the record-shape projection needs. Each one is
listed in docs/PARITY_ALLOWLIST.md. Anything not listed here is a defect."""
import os; os.chdir(os.path.join(os.path.dirname(__file__),'..'))
EDITS={
 # TEMPORARY: the 14.6 MB PWA PDF exceeds the 10 MB browser-upload cap; until Ryan drags it into the
 # A330 repo (GitHub web, 25 MB limit) the viewer reads the sister portal's copy. Remove both lines then.
 'pwa_pdf.html':[
  ('<a id="direct" href="/2023-pwa.pdf">','<a id="direct" href="https://as787pilot.app/2023-pwa.pdf">'),
  ("var PDF = '/2023-pwa.pdf'","var PDF = 'https://as787pilot.app/2023-pwa.pdf'"),
 ],
 'ioe.html':[
  ('"ioe.html","ioe_questions.json","A330_OE_Workbook_Answered.pdf"','"ioe.html","data/oe.json","A330_OE_Workbook_Answered.pdf"'),
  ('ioe_questions.json is missing from the repo root.','data/oe.json is missing from the repo.'),
  ('from the company manuals (FOM, FCOM, QRH, FCTM, MEL) or, where those are silent, FAA and Jeppesen material.','from the company manuals (FOM, FCOM, QRH, FCTM, PRC).'),
 ],
 'triggers.html':[
  ('Trigger Map &middot; FCOM NP.21','FCOM PRO-NOR-SOP &middot; FCTM PR-NP-CL &middot; PRC'),
  ('href="podcast.html?ep=44"','href="podcast.html"'),
 ],
 'flows_quiz.html':[
  ('let seat = "CA"','let seat = "FO"'),   # Ryan flies the FO seat; the first flow is CM2-only
  # Airbus crew-member labels and a CM3 (IRO) seat; engine ids stay CA/FO/IRO
  ('<button id="seatCA" class="active">CA</button>\n    <button id="seatFO">FO</button>',
   '<button id="seatCA">CM1 (CA)</button>\n    <button id="seatFO" class="active">CM2 (FO)</button>\n    <button id="seatIRO">CM3 (IRO)</button>'),
  ('document.getElementById("seatFO").onclick = e=>setSeat("FO", e.target);',
   'document.getElementById("seatFO").onclick = e=>setSeat("FO", e.target);\ndocument.getElementById("seatIRO").onclick = e=>setSeat("IRO", e.target);'),
  ('if(it.role==="IRO") return true; // observer items always greyed','if(it.role==="IRO") return seat!=="IRO"; // CM3 items show in the CM3 seat'),
  ('if(it.role==="CA" || it.role==="FO") return it.role!==seat;','if(it.role==="CA" || it.role==="FO") return seat==="IRO" ? true : it.role!==seat;'),
  ('(seat==="BOTH"?"both seats":seat)','(seat==="BOTH"?"both seats":({CA:"CM1 (CA)",FO:"CM2 (FO)",IRO:"CM3 (IRO)"}[seat]||seat))'),
  ('"No " + seat + " items in this flow. Switch seat or flow."','"No " + ({CA:"CM1 (CA)",FO:"CM2 (FO)",IRO:"CM3 (IRO)"}[seat]||seat) + " items in this flow. Switch seat or flow."'),
 ],
 'assist.js':[
  ("var hits = search(q, 8);","var broad = /\\b(whole|entire|all|every|section|complete|confirm|summari[sz]e|list)\\b/i.test(q);\n      var hits = search(q, broad ? 30 : 8);"),
  ("'You are scoped to ONE section of a study portal: ' + CORPUS.title + '. ' +","'You are scoped to ONE section of a study portal: ' + CORPUS.title + '. ' + (CORPUS.source ? 'Every excerpt is from ' + CORPUS.source + '. ' : '') +"),
 ],
 'portal-settings.js':[
  ("'<div class=\"ps-h3\">Offline</div>' +","'<div class=\"ps-h3\">Contact</div>' +\n    '<p class=\"ps-note\">Questions, corrections, requests: <a href=\"mailto:ryan.pettit@alaskaair.com?subject=A330%20Study%20Portal\" style=\"color:#CE0C88;font-weight:700;text-decoration:none\">ryan.pettit@alaskaair.com</a></p>' +\n    '<div class=\"ps-h3\">Offline</div>' +"),
 ],
 'phase_flows.html':[
  ('<button data-s="C" class="on">CA</button>\n      <button data-s="F">FO</button>','<button data-s="C">CM1 (CA)</button>\n      <button data-s="F" class="on">CM2 (FO)</button>'),
  ("let state={phase:'preflight',seat:'C',duty:'PF'","let state={phase:'preflight',seat:'F',duty:'PM'"),   # FO seat, PM duty default
 ],
 'weather.html':[
  ('Open 1-page handout (PDF)','Open 2-page handout (PDF)'),
 ],
 'memory-items.html':[
  ('<div class="cond">Condition: ${d.cond}</div>','${d.cond?`<div class="cond">Condition: ${d.cond}</div>`:``}'),
  ('Condition: ${d.cond}<br>','${d.cond?`Condition: ${d.cond}<br>`:``}'),
 ],
}
for f,eds in EDITS.items():
    t=open(f,encoding='utf-8').read()
    for a,b in eds:
        assert a in t, (f,a[:40]); t=t.replace(a,b)
    open(f,'w',encoding='utf-8').write(t); print('fixups:',f)
