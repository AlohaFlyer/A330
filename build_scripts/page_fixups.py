#!/usr/bin/env python3
"""Tiny, enumerated edits to cloned pages that the record-shape projection needs. Each one is
listed in docs/PARITY_ALLOWLIST.md. Anything not listed here is a defect."""
import os; os.chdir(os.path.join(os.path.dirname(__file__),'..'))
EDITS={
 'ioe.html':[
  ('"ioe.html","ioe_questions.json","A330_OE_Workbook_Answered.pdf"','"ioe.html","data/oe.json","A330_OE_Workbook_Answered.pdf"'),
  ('ioe_questions.json is missing from the repo root.','data/oe.json is missing from the repo.'),
  # Original (unanswered) workbook beside the answered PDF (Ryan, 2026-09-21); opens the Drive copy, the PDF stays out of the public repo
  ('<a class="btn" id="pdfLink" href="view.html?f=A330_OE_Workbook_Answered.pdf">Full Workbook PDF</a>',
   '<span style="display:flex;gap:8px;flex-wrap:wrap;"><a class="btn" id="pdfLink" href="view.html?f=A330_OE_Workbook_Answered.pdf">Full Workbook PDF</a><a class="btn" id="origLink" href="https://drive.google.com/file/d/1BLAJs8MJVA_zCMZk-utQj4FKVf1985Et/view" target="_blank" rel="noopener" title="787/A321/A330 Fleets OE Workbook, Version 2, January 2026 (unanswered original, Drive)">Original OE Workbook</a></span>'),
  ('from the company manuals (FOM, FCOM, QRH, FCTM, MEL) or, where those are silent, FAA and Jeppesen material.','from the company manuals (FOM, FCOM, QRH, FCTM, PRC).'),
 ],
 'triggers.html':[
  ('Trigger Map &middot; FCOM NP.21','FCOM PRO-NOR-SOP &middot; FCTM PR-NP-CL &middot; PRC'),
  ('href="podcast.html?ep=44"','href="podcast.html"'),
    ('  .navbtn.pod{border-color:var(--green);color:#9ad9b9}','  .navbtn[hidden]{display:none;}\n  .navbtn.pod{border-color:var(--green);color:#9ad9b9}'),
 ],
 'flows_quiz.html':[
  ('let seat = "CA"','let seat = "FO"'),   # Ryan flies the FO seat; the first flow is CM2-only
  # "How to memorize" button in the header bar, linking the memorization plan page (Ryan, 2026-09-18)
  ('A330 FLOWS TRAINER</span></div>','A330 FLOWS TRAINER</span><a href="flow_memorization.html" style="margin-left:auto;background:#463C8F;color:#fff;text-decoration:none;font-size:12px;font-weight:700;letter-spacing:.03em;padding:6px 12px;border-radius:6px;border:1px solid #CE0C88;white-space:nowrap;">How to memorize</a></div>'),
  # Audit 2026-09-16: the checklist-named flow title is longer than the B787 one and ran under the
  # prev / end / restart buttons on a phone. Reserve their width beside the title.
  ('  .tag{font-size:12px;font-weight:700;color:var(--blue);text-transform:uppercase;letter-spacing:1px;}',
   '  .tag{font-size:12px;font-weight:700;color:var(--blue);text-transform:uppercase;letter-spacing:1px;padding-right:150px;min-height:40px;}'),
  # Airbus crew-member labels and a CM3 (IRO) seat; engine ids stay CA/FO/IRO
  ('<button id="seatCA" class="active">CA</button>\n    <button id="seatFO">FO</button>',
   '<button id="seatCA">CM1 (CA)</button>\n    <button id="seatFO" class="active">CM2 (FO)</button>\n    <button id="seatIRO">CM3 (IRO)</button>'),
  ('document.getElementById("seatFO").onclick = e=>setSeat("FO", e.target);',
   'document.getElementById("seatFO").onclick = e=>setSeat("FO", e.target);\ndocument.getElementById("seatIRO").onclick = e=>setSeat("IRO", e.target);'),
  ('if(it.role==="IRO") return true; // observer items always greyed','if(it.role==="IRO") return seat!=="IRO"; // CM3 items show in the CM3 seat'),
  ('if(it.role==="CA" || it.role==="FO") return it.role!==seat;','if(it.role==="CA" || it.role==="FO") return seat==="IRO" ? true : it.role!==seat;'),
  ('(seat==="BOTH"?"both seats":seat)','(seat==="BOTH"?"both seats":({CA:"CM1 (CA)",FO:"CM2 (FO)",IRO:"CM3 (IRO)"}[seat]||seat))'),
  ('"No " + seat + " items in this flow. Switch seat or flow."','"No " + ({CA:"CM1 (CA)",FO:"CM2 (FO)",IRO:"CM3 (IRO)"}[seat]||seat) + " items in this flow. Switch seat or flow."'),
  # A newly selected flow (page load, phase, flow, seat or duty change) opens fully revealed; Restart steps through it.
  ('let stepIdx = 0;','let stepIdx = -1; // -1: a newly selected flow opens fully revealed (Ryan); Restart steps through it'),
  ('if(first>=0){ flowIdx = first; stepIdx = 0; }','if(first>=0){ flowIdx = first; stepIdx = -1; }'),
  ('b.onclick = ()=>{ flowIdx = i; stepIdx = 0; buildFlowBtns(); render(); };','b.onclick = ()=>{ flowIdx = i; stepIdx = -1; buildFlowBtns(); render(); };'),
  ('  seat = s; stepIdx = 0;','  seat = s; stepIdx = -1;'),
  ('  duty = d; stepIdx = 0;','  duty = d; stepIdx = -1;'),
  ('  if(stepIdx > items.length) stepIdx = 0;\n','  if(stepIdx < 0) stepIdx = items.length;\n  if(stepIdx > items.length) stepIdx = 0;\n'),
  # Phase bar named after the A330 normal checklists (Ryan): Cockpit Prep, Before Start, After Start, Taxi, Line-Up, Climb, Approach, After Landing, Parking.
  ('  "Preflight":"#463C8F","Before Start & Pushback":"#00568F","Engine Start":"#CE0C88","Taxi Out":"#2E90D0",\n  "Takeoff":"#E0A100","Climb":"#EAA52A","Cruise":"#D98A00","Descent":"#E2761A","Approach":"#D8650C","Go-Around":"#B85000",\n  "Landing Roll":"#00805E","Taxi In":"#2E9B7C","Shutdown & Secure":"#5CB89A"',
   '  "Cockpit Prep":"#463C8F","Before Start":"#00568F","After Start":"#CE0C88","Taxi":"#2E90D0",\n  "Line-Up":"#E0A100","Climb":"#EAA52A","Cruise":"#D98A00","Descent":"#E2761A","Approach":"#D8650C","Go-Around":"#B85000",\n  "Landing Roll":"#00805E","After Landing":"#2E9B7C","Parking":"#5CB89A"'),
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
  # Home icon moves into the page's top bar, right end (Ryan, 2026-09-16).
  ('      if (document.querySelector(\'.ps-home\')) return;\n      var css = document.createElement(\'style\');\n      css.textContent =\n        \'.ps-homebar{align-self:stretch;width:100%;box-sizing:border-box;padding:8px 0 0 10px;flex:0 0 auto;text-align:left;}\' +\n        \'.ps-home{display:inline-flex;align-items:center;justify-content:center;width:34px;height:34px;border-radius:9px;\' +\n        \'background:#fff;border:2px solid #463C8F;color:#463C8F;text-decoration:none;box-shadow:0 1px 4px rgba(1,23,43,.2);\' +\n        \'transition:background .12s,color .12s;-webkit-tap-highlight-color:transparent;}\' +\n        \'.ps-home:hover,.ps-home:focus-visible{background:#463C8F;color:#fff;}\' +\n        \'.ps-home:focus{outline:none;}\' +\n        \'.ps-home svg{display:block;}\' +\n        \'@media (max-width:480px){.ps-homebar{padding:6px 0 0 8px;}.ps-home{width:40px;height:40px;}}\';\n      document.head.appendChild(css);\n\n      var bar = document.createElement(\'div\');\n      bar.className = \'ps-homebar\';\n      bar.innerHTML = \'<a class="ps-home" href="/index.html" title="A330 Study Portal" aria-label="A330 Study Portal">\' +\n        \'<svg viewBox="0 0 24 24" width="19" height="19" aria-hidden="true" focusable="false">\' +\n        \'<path d="M3 11.3 12 4l9 7.3" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>\' +\n        \'<path d="M5.7 10.1v9.4h12.6v-9.4" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>\' +\n        \'<path d="M10 19.5v-5.1h4v5.1" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>\' +\n        \'</svg></a>\';\n      document.body.insertBefore(bar, document.body.firstChild);\n',
   '      // The home icon lives at the right end of the page\'s top bar (Ryan, 2026-09-16): the\n      // page\'s static .ps-homebar is emptied and its link moved into the banner; pages without\n      // one get a fresh link. Falls back to the old top-left bar when no banner is found.\n      var css = document.createElement(\'style\');\n      css.textContent =\n        \'.ps-homebar{align-self:stretch;width:100%;box-sizing:border-box;padding:8px 0 0 10px;flex:0 0 auto;text-align:left;}\' +\n        \'.ps-homebar:empty{display:none;}\' +\n        \'.ps-home{display:inline-flex;align-items:center;justify-content:center;width:34px;height:34px;border-radius:9px;\' +\n        \'background:#fff;border:2px solid #463C8F;color:#463C8F;text-decoration:none;box-shadow:0 1px 4px rgba(1,23,43,.2);\' +\n        \'transition:background .12s,color .12s;-webkit-tap-highlight-color:transparent;}\' +\n        \'.ps-home:hover,.ps-home:focus-visible{background:#463C8F;color:#fff;}\' +\n        \'.ps-home:focus{outline:none;}\' +\n        \'.ps-home svg{display:block;}\' +\n        \'.ps-home.in-bar{margin-left:12px;flex:0 0 auto;background:rgba(255,255,255,.16);border:0;color:#fff;box-shadow:none;width:36px;height:36px;}\' +\n        \'.ps-home.in-bar:hover,.ps-home.in-bar:focus-visible{background:#fff;color:#463C8F;}\' +\n        \'@media (max-width:480px){.ps-homebar{padding:6px 0 0 8px;}.ps-home{width:40px;height:40px;}.ps-home.in-bar{width:36px;height:36px;margin-left:8px;}}\';\n      document.head.appendChild(css);\n\n      var a = document.querySelector(\'.ps-home\');\n      if (!a) {\n        a = document.createElement(\'a\');\n        a.className = \'ps-home\'; a.href = \'/index.html\'; a.title = \'A330 Study Portal\'; a.setAttribute(\'aria-label\', \'A330 Study Portal\');\n        a.innerHTML = \'<svg viewBox="0 0 24 24" width="19" height="19" aria-hidden="true" focusable="false">\' +\n          \'<path d="M3 11.3 12 4l9 7.3" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>\' +\n          \'<path d="M5.7 10.1v9.4h12.6v-9.4" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>\' +\n          \'<path d="M10 19.5v-5.1h4v5.1" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>\';\n      }\n      if (a.classList.contains(\'in-bar\')) return;\n      var host = document.querySelector(\'header .ctrls\') || document.querySelector(\'header\') ||\n        document.querySelector(\'div[style*="background:var(--midnight)"]\') || document.querySelector(\'.banner\');\n      if (host) {\n        var last = host.lastElementChild;\n        if (last && host.children.length > 1 && !document.querySelector(\'header .ctrls\') && host.tagName !== \'HEADER\' && last.tagName === \'SPAN\') last.style.marginLeft = \'auto\';\n        a.classList.add(\'in-bar\');\n        host.appendChild(a);\n        var bar0 = document.querySelector(\'.ps-homebar\');\n        if (bar0 && !bar0.children.length) bar0.parentNode.removeChild(bar0);\n      } else if (!a.parentNode) {\n        var bar = document.createElement(\'div\');\n        bar.className = \'ps-homebar\';\n        bar.appendChild(a);\n        document.body.insertBefore(bar, document.body.firstChild);\n      }\n'),
  # ha330 unlock log collector: separate Apps Script deployment (deployed 2026-09-16, sheet
  # "ha330pilot unlock log" in HA - Airbus A330), never the as787 one.
  ("var LOG_URL = 'https://script.google.com/macros/s/AKfycbyrHlq0FrUwA2CtCHBo3dGB_CjZaR-igFntcR9nVBGWF84MrLK0VKW6UdCFpyUHVNdN2w/exec';","var LOG_URL = 'https://script.google.com/macros/s/AKfycbzbpHnlzrRXeiTd1UfAXNGfIxHpDxqlg-E1t5Ip_JwFoZFXwjV5eLW0uNpUCg2SzwODnQ/exec';"),
  ("'<div class=\"ps-h3\">Offline</div>' +","'<div class=\"ps-h3\">Contact</div>' +\n    '<p class=\"ps-note\">Questions, corrections, requests: <a href=\"mailto:ryan.pettit@alaskaair.com?subject=A330%20Study%20Portal\" style=\"color:#CE0C88;font-weight:700;text-decoration:none\">ryan.pettit@alaskaair.com</a></p>' +\n    '<div class=\"ps-h3\">Offline</div>' +"),
 ],
 'phase_flows.html':[
  ('<button data-s="C" class="on">CA</button>\n      <button data-s="F">FO</button>','<button data-s="C">CM1 (CA)</button>\n      <button data-s="F" class="on">CM2 (FO)</button>'),
  ("let state={phase:'preflight',seat:'C',duty:'PF'","let state={phase:'preflight',seat:'F',duty:'PM'"),   # FO seat, PM duty default
  # Checklist colour coding (Ryan): nav buttons, phase header and gate bar carry the checklist colour, same hexes as the Flows Trainer phase bar.
  ('.phasehead .src{font-size:.7em;font-weight:600;color:var(--muted);}',
   '.phasehead .src{font-size:.7em;font-weight:600;color:var(--muted);}\n.phasehead.tinted{color:var(--pc);border-left:6px solid var(--pc);padding-left:10px;}\n.gate.tinted{background:var(--pc);}\nnav button[data-pc],.rail button[data-pc]{color:var(--pc);border-color:var(--pc);}\nnav button[data-pc].on,.rail button[data-pc].on{background:var(--pc);color:#fff;border-color:var(--pc);}'),
  ("const NORMAL=PHASES.filter(p=>p.kind==='n'), ABN=PHASES.filter(p=>p.kind==='a');",
   "const NORMAL=PHASES.filter(p=>p.kind==='n'), ABN=PHASES.filter(p=>p.kind==='a');\n// Checklist colours, identical to the Flows Trainer phase bar, keyed by the checklist each phase sits under.\nconst CL_COLORS={'Cockpit Prep':'#463C8F','Before Start':'#00568F','After Start':'#CE0C88','Taxi':'#2E90D0','Line-Up':'#E0A100','Climb':'#EAA52A','Cruise':'#D98A00','Descent':'#E2761A','Approach':'#D8650C','Landing':'#00805E','Go-Around':'#B85000','After Landing':'#2E9B7C','Parking':'#5CB89A'};\nconst PHASE_CL={'preflight':'Cockpit Prep','cockpit-prep':'Cockpit Prep','before-push':'Before Start','before-start':'Before Start','after-start':'After Start','taxi':'Taxi','before-takeoff':'Line-Up','after-takeoff':'Climb','cruise':'Cruise','descent':'Descent','approach':'Approach','landing':'Landing','go-around':'Go-Around','after-landing':'After Landing','parking':'Parking'};\nfunction phaseColor(id){ const c=PHASE_CL[id]; return c ? CL_COLORS[c] : ''; }"),
  ('  NORMAL.forEach(p=>{ html+=`<button data-p="${p.id}">${p.label}</button>`; });',
   '  NORMAL.forEach(p=>{ const pc=phaseColor(p.id); html+=`<button data-p="${p.id}"${pc?` data-pc="1" style="--pc:${pc}"`:``}>${p.label}</button>`; });'),
  ('  ABN.forEach(p=>{ html+=`<button class="ab" data-p="${p.id}">${p.label}</button>`; });',
   '  ABN.forEach(p=>{ const pc=phaseColor(p.id); html+=`<button class="ab" data-p="${p.id}"${pc?` data-pc="1" style="--pc:${pc}"`:``}>${p.label}</button>`; });'),
  ('  main.innerHTML=`<div class="phasehead">${ph.title}<span class="src">${ph.src}</span></div><div class="grid" id="grid"></div>`;\n  const g=document.getElementById(\'gate\'); const gn=gateFor(ph);\n  if(gn.length){ g.className=\'gate\';',
   '  const pc=phaseColor(ph.id);\n  main.innerHTML=`<div class="phasehead${pc?` tinted`:``}"${pc?` style="--pc:${pc}"`:``}>${ph.title}<span class="src">${ph.src}</span></div><div class="grid" id="grid"></div>`;\n  const g=document.getElementById(\'gate\'); const gn=gateFor(ph);\n  if(pc) g.style.setProperty(\'--pc\',pc); else g.style.removeProperty(\'--pc\');\n  if(gn.length){ g.className=\'gate\'+(pc?\' tinted\':\'\');'),
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
 'index.html':[
    # Systems Quiz was hidden until its bank was approved (Ryan, 2026-09-16); unhidden 2026-09-21 with the REV1 bank.
  ('  .menu a.podcast{background:#FDF1F8;}','  .menu a.podcast{background:#FDF1F8;}\n  .menu a[hidden]{display:none;}'),
  # One login only (Ryan, 2026-09-16): Cloudflare Access already checked the company email at the site
  # gate, so the home page reads the identity Access holds (same-origin /cdn-cgi/access/get-identity),
  # records it for the unlock log and skips its own email box. The box stays as the fallback.
  ("  if(hasAccess()&&known()){open_();}\n  else if(inp){inp.focus();}\n",
   "  function askBox(){if(gate)gate.style.visibility='';if(inp)inp.focus();}\n"
   "  function fromAccess(){\n"
   "    if(gate)gate.style.visibility='hidden';\n"
   "    try{\n"
   "      fetch('/cdn-cgi/access/get-identity',{credentials:'same-origin',cache:'no-store'})\n"
   "        .then(function(r){return r.ok?r.json():null;})\n"
   "        .then(function(j){\n"
   "          var e=j&&j.email?String(j.email).trim():'';\n"
   "          if(/^[^\\s@]+@alaskaair\\.com$/i.test(e)){grant();note(e);open_();}\n"
   "          else askBox();\n"
   "        }).catch(askBox);\n"
   "    }catch(e){askBox();}\n"
   "  }\n"
   "  if(hasAccess()&&known()){open_();}\n"
   "  else fromAccess();\n"),
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
