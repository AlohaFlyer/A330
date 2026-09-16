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
  # Exterior flows (noflow) hide the cockpit map: the steps happen outside the airplane.
  ('  @media (max-width:740px){\n    .layout{grid-template-columns:1fr;}\n  }',
   '  @media (max-width:740px){\n    .layout{grid-template-columns:1fr;}\n  }\n  .layout.noflow{grid-template-columns:1fr;}\n  .layout.noflow .mapbox{display:none;}'),
  ('function render(){\n  syncPhaseUI();\n  const f = FLOWS[flowIdx];',
   'function render(){\n  syncPhaseUI();\n  const f = FLOWS[flowIdx];\n  document.getElementById("drillLayout").classList.toggle("noflow", !!f.noflow);'),
  # Per-seat dot position: an item may carry pos:{CA:[x,y],FO:[x,y]} (e.g. each pilot\'s own EFB or MCDU);
  # the map uses the current seat\'s pair and falls back to x,y. mir:true means x,y are drawn for the
  # CM1 seat and the map mirrors x across the centerline (300-x) in the CM2 seat (own MCDU, EFIS, PFD/ND, window).
  ('function mapPt(x,y){ return [x,y]; }',
   'function mapPt(x,y){ return [x,y]; }\nfunction seatPt(it){ const p = it.pos && (it.pos[seat] || (seat==="BOTH" && it.pos.FO)); if(p) return [p[0],p[1]]; if(it.mir && seat==="FO") return [Math.round((300-it.x)*10)/10, it.y]; return [it.x,it.y]; }'),
  ('  const xs = all.map(i=>i.x), ys = all.map(i=>i.y);','  const xs = all.map(i=>seatPt(i)[0]), ys = all.map(i=>seatPt(i)[1]);'),
  ('  const P = seq.map(it=>[it.x,it.y]);','  const P = seq.map(it=>seatPt(it));'),
  ('  off.forEach(it=>{ s += `<circle class="dot inactive" cx="${it.x}" cy="${it.y}" r="6"/>`; });',
   '  off.forEach(it=>{ const q=seatPt(it); s += `<circle class="dot inactive" cx="${q[0]}" cy="${q[1]}" r="6"/>`; });'),
  ('    s += `<circle class="${cls}" data-i="${i}" cx="${it.x}" cy="${it.y}" r="8"/>`;\n    s += `<text class="${lightNum?\'numlight\':\'num\'}" data-i="${i}" x="${it.x-3}" y="${it.y+3.5}">${i+1}</text>`;',
   '    const q=seatPt(it);\n    s += `<circle class="${cls}" data-i="${i}" cx="${q[0]}" cy="${q[1]}" r="8"/>`;\n    s += `<text class="${lightNum?\'numlight\':\'num\'}" data-i="${i}" x="${q[0]-3}" y="${q[1]+3.5}">${i+1}</text>`;'),
 ],
 'assist.js':[
  ("var hits = search(q, 8);","var broad = /\\b(whole|entire|all|every|section|complete|confirm|summari[sz]e|list)\\b/i.test(q);\n      var hits = search(q, broad ? 30 : 8);"),
  ("'You are scoped to ONE section of a study portal: ' + CORPUS.title + '. ' +","'You are scoped to ONE section of a study portal: ' + CORPUS.title + '. ' + (CORPUS.source ? 'Every excerpt is from ' + CORPUS.source + '. ' : '') +"),
 ],
 'portal-settings.js':[
  # ha330 unlock log collector: separate Apps Script deployment, never the as787 one.
  # LOG_URL stays empty until Ryan deploys build_scripts/apps_script/unlock_log.gs; an empty
  # LOG_URL makes portal-settings.js keep the queue local and show device-only counts.
  ("var LOG_URL = 'https://script.google.com/macros/s/AKfycbyrHlq0FrUwA2CtCHBo3dGB_CjZaR-igFntcR9nVBGWF84MrLK0VKW6UdCFpyUHVNdN2w/exec';","var LOG_URL = '';"),
  ("'<div class=\"ps-h3\">Offline</div>' +","'<div class=\"ps-h3\">Contact</div>' +\n    '<p class=\"ps-note\">Questions, corrections, requests: <a href=\"mailto:ryan.pettit@alaskaair.com?subject=A330%20Study%20Portal\" style=\"color:#CE0C88;font-weight:700;text-decoration:none\">ryan.pettit@alaskaair.com</a></p>' +\n    '<div class=\"ps-h3\">Offline</div>' +"),
 ],
 'phase_flows.html':[
  ('<button data-s="C" class="on">CA</button>\n      <button data-s="F">FO</button>','<button data-s="C">CM1 (CA)</button>\n      <button data-s="F" class="on">CM2 (FO)</button>'),
  ("let state={phase:'preflight',seat:'C',duty:'PF'","let state={phase:'preflight',seat:'F',duty:'PM'"),   # FO seat, PM duty default
  # QUICK REF: Ryan's own A330 OEM Quick Reference card (2 pages, assets/quickref/p1.png p2.png,
  # PDF at /A330_OEM_Quick_Reference.pdf) as a full-screen overlay with Back, its own Day/Night
  # and a PDF link. Back button, Esc and the browser/phone back gesture all close it.
  ('.notesbtn.on{background:#37d9a8;color:#053b2c;}',
   '.notesbtn.on{background:#37d9a8;color:#053b2c;}\n'
   '.qref{position:fixed;inset:0;z-index:80;background:#E4E0EE;display:flex;flex-direction:column;}\n'
   '.qref[hidden]{display:none;}\n'
   '.qref .qbar{flex:none;display:flex;align-items:center;gap:10px;background:#463C8F;color:#fff;padding:calc(6px + env(safe-area-inset-top)) 12px 6px;}\n'
   '.qref .qbar button,.qref .qbar a{height:36px;line-height:36px;padding:0 12px;border:0;border-radius:8px;background:rgba(255,255,255,.14);color:#fff;font-weight:800;font-size:12px;letter-spacing:.3px;cursor:pointer;text-decoration:none;font-family:inherit;}\n'
   '.qref .qbar .qttl{flex:1;text-align:center;font-weight:800;font-size:12px;letter-spacing:.6px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}\n'
   '.qref .qpages{flex:1;overflow:auto;-webkit-overflow-scrolling:touch;padding:8px 8px calc(8px + env(safe-area-inset-bottom));}\n'
   '.qref .qpages img{display:block;width:100%;max-width:1100px;margin:0 auto 10px;background:#fff;box-shadow:0 2px 10px rgba(30,26,46,.25);}\n'
   '.qref.dark{background:#111015;}\n'
   '.qref.dark .qpages img{filter:invert(1) hue-rotate(180deg);box-shadow:none;}'),
  ('<button class="notesbtn" id="notesBtn" title="Quick Reference Notes">NOTES</button>',
   '<button class="notesbtn" id="notesBtn" title="Quick Reference Notes">NOTES</button>\n    <button class="notesbtn" id="qrefBtn" title="A330 OEM Quick Reference card">QUICK REF</button>'),
  ('<div class="gate" id="gate"></div>',
   '<div class="qref" id="qref" hidden>\n'
   '  <div class="qbar"><button id="qrefBack" type="button">&#9664; Back</button><span class="qttl">A330 OEM QUICK REFERENCE</span>'
   '<button id="qrefTheme" type="button" title="Day / Night">&#9790;</button><a href="/A330_OEM_Quick_Reference.pdf" target="_blank" rel="noopener">PDF</a></div>\n'
   '  <div class="qpages"><img src="assets/quickref/p1.png" alt="A330 OEM Quick Reference page 1"><img src="assets/quickref/p2.png" alt="A330 OEM Quick Reference page 2"></div>\n'
   '</div>\n<div class="gate" id="gate"></div>'),
  ("themeBtn.addEventListener('click',()=>setTheme(!document.body.classList.contains('dark')));",
   "themeBtn.addEventListener('click',()=>setTheme(!document.body.classList.contains('dark')));\n"
   "const qref=document.getElementById('qref'), qrefTheme=document.getElementById('qrefTheme');\n"
   "function setQrefTheme(dark){ qref.classList.toggle('dark',dark); qrefTheme.innerHTML=dark?'&#9728;':'&#9790;'; try{localStorage.setItem('a330qrefdark',dark?'1':'0');}catch(e){} }\n"
   "function openQref(){ let d=document.body.classList.contains('dark'); try{const v=localStorage.getItem('a330qrefdark'); if(v!==null) d=(v==='1');}catch(e){} setQrefTheme(d); qref.hidden=false; document.getElementById('qrefBtn').classList.add('on'); try{history.pushState({qref:1},'');}catch(e){} }\n"
   "function closeQref(fromPop){ if(qref.hidden) return; qref.hidden=true; document.getElementById('qrefBtn').classList.remove('on'); if(!fromPop && history.state && history.state.qref){ try{history.back();}catch(e){} } }\n"
   "document.getElementById('qrefBtn').addEventListener('click',()=>{ if(qref.hidden) openQref(); else closeQref(); });\n"
   "document.getElementById('qrefBack').addEventListener('click',()=>closeQref());\n"
   "qrefTheme.addEventListener('click',()=>setQrefTheme(!qref.classList.contains('dark')));\n"
   "window.addEventListener('popstate',()=>closeQref(true));\n"
   "document.addEventListener('keydown',e=>{ if(e.key==='Escape' && !qref.hidden) closeQref(); });"),
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
