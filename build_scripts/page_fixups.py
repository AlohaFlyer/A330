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
  # group-colored markers (2026-09-21), after the seatPt edit above so both anchors hold
  ("    if(it.trg){ cls += \" trigpt\"; }\n    const q=seatPt(it);\n    s += `<circle class=\"${cls}\" data-i=\"${i}\" cx=\"${q[0]}\" cy=\"${q[1]}\" r=\"8\"/>`;",
   "    if(it.trg){ cls += \" trigpt\"; }\n    const q=seatPt(it);\n    let gstyle = \"\";\n    if(it.gc){ cls += \" grp\"; lightNum = true; gstyle = ` style=\"fill:${it.gc}${(!showAll && i===upto) ? \";stroke:#1A1630;stroke-width:2.5\" : (i===0||i===last||it.trg) ? \"\" : \";stroke:#fff;stroke-width:1.5\"}\"`; }\n    s += `<circle class=\"${cls}\" data-i=\"${i}\" cx=\"${q[0]}\" cy=\"${q[1]}\" r=\"8\"${gstyle}/>`;"),
  # v3.8 (Ryan, 2026-09-22): Step button between back and FF; Reveal / Next step fixed bottom-right on wide screens;
  # tap a group chip to show only that group (map + done list); flows without a map are centred
  ('<button id="prevBtn" title="Previous step">&#9664;</button><button id="endBtn"',
   '<button id="prevBtn" title="Previous step">&#9664;</button><button id="stepBtn" title="Reveal, then next step">Step</button><button id="endBtn"'),
  ('  .layout.noflow .mapbox{display:none;}',
   '  .layout.noflow .mapbox{display:none;}\n  .layout.noflow{justify-items:center;}\n  .layout.noflow .card{width:100%;max-width:560px;}\n  @media (min-width:741px){ .actions{position:fixed;right:20px;bottom:84px;width:230px;margin:0;z-index:50;box-shadow:0 6px 18px rgba(0,0,0,.25);} .card{padding-bottom:70px;} }\n  .grplegend span{cursor:pointer;} .grplegend.filt span:not(.sel){opacity:.35;} .grplegend span.all{background:#334e68;}'),
  ('function grpLegend(f){\n  if(!f.groups) return "";\n  const items = activeItems(f);\n  return "<div class=\\"grplegend\\">" + f.groups.map(g=>{ const n = items.filter(it=>it.g===g.g).length; return n ? "<span style=\\"background:"+g.gc+"\\">"+(g.gb?g.gb+" · ":"")+g.g+" "+n+"</span>" : ""; }).join("") + "</div>";\n}',
   'let grpFilter = null;\nwindow.setGrpFilter=function(g){ grpFilter = (grpFilter===g) ? null : g; render(); }; // on window: the engine runs inside the data-fetch callback\n'
   'function grpLegend(f){\n  if(!f.groups) return "";\n  const items = activeItems(f);\n  const esc = s=>s.replace(/\'/g,"\\\\\'");\n  return "<div class=\\"grplegend" + (grpFilter?" filt":"") + "\\" title=\\"Tap a group to show only that group\\">" + f.groups.map(g=>{ const n = items.filter(it=>it.g===g.g).length; return n ? "<span class=\\""+(grpFilter===g.g?"sel":"")+"\\" style=\\"background:"+g.gc+"\\" onclick=\\"setGrpFilter(\'"+esc(g.g)+"\')\\">"+(g.gb?g.gb+" · ":"")+g.g+" "+n+"</span>" : ""; }).join("") + (grpFilter ? "<span class=\\"all\\" onclick=\\"setGrpFilter(null)\\">All</span>" : "") + "</div>";\n}'),
  ('  svgEl.innerHTML = s;\n}',
   '  svgEl.innerHTML = s;\n  if(grpFilter && flow.groups){ const gc = (flow.groups.find(g=>g.g===grpFilter)||{}).gc; seq.forEach((it,i)=>{ if(it.g!==grpFilter) svgEl.querySelectorAll(\'[data-i="\'+i+\'"]\').forEach(el=>el.style.display="none"); }); const cn=c=>{ const d=document.createElement(\'i\'); d.style.color=c||\'\'; return d.style.color; }; const want=cn(gc); svgEl.querySelectorAll(\'.trace\').forEach(pth=>{ if(cn(pth.style.stroke)!==want) pth.style.display="none"; }); svgEl.querySelectorAll(\'.ghost, .dot.inactive\').forEach(el=>el.style.display="none"); }\n}'),
  ('  for(let i=0;i<stepIdx;i++){\n    const gh = grpHeader(items, i);',
   '  for(let i=0;i<stepIdx;i++){\n    if(grpFilter && items[i].g!==grpFilter) continue;\n    const gh = grpHeader(items, i);'),
  ('document.getElementById("reveal").onclick = ()=>{',
   'document.getElementById("stepBtn").onclick = ()=>document.getElementById("reveal").onclick();\ndocument.getElementById("reveal").onclick = ()=>{'),
  # v4.2 (Ryan, 2026-09-22): poster zoom + / 100% / - ; the image scales by width inside a scrolling frame, pinch still works on the phone
  ('<div id="posterView" class="hidden" style="width:100%;max-width:980px;margin:0 auto;text-align:center;"><img id="posterImg" alt="A330 cockpit poster" style="width:100%;max-width:680px;height:auto;display:inline-block;margin:0 auto;border-radius:6px;"></div>',
   '<div id="posterView" class="hidden" style="width:100%;max-width:980px;margin:0 auto;text-align:center;">'
   '<div class="pzbar" style="display:flex;gap:8px;justify-content:center;margin:0 0 8px;"><button id="pzOut" title="Zoom out">&minus;</button><button id="pzReset" title="Reset zoom">100%</button><button id="pzIn" title="Zoom in">+</button></div>'
   '<div id="pzWrap" style="overflow:auto;max-height:82vh;-webkit-overflow-scrolling:touch;border-radius:6px;"><img id="posterImg" alt="A330 cockpit poster" style="width:100%;max-width:680px;height:auto;display:inline-block;margin:0 auto;border-radius:6px;"></div></div>'),
  ('  .miniBtns button:hover{background:var(--midnight);color:#fff;}',
   '  .miniBtns button:hover{background:var(--midnight);color:#fff;}\n  .pzbar button{min-width:52px;min-height:40px;font-size:18px;font-weight:800;background:#fff;color:var(--midnight);border:1.5px solid var(--midnight);border-radius:6px;cursor:pointer;} .pzbar #pzReset{font-size:13px;min-width:70px;}'),
  ('const posterBtn = document.getElementById("posterBtn");',
   'let pz = 1;\nfunction setPz(z){ pz = Math.min(4, Math.max(1, z)); const img = document.getElementById("posterImg"); img.style.width = (100*pz)+"%"; img.style.maxWidth = (680*pz)+"px"; document.getElementById("pzReset").textContent = Math.round(pz*100)+"%"; }\n'
   'document.getElementById("pzIn").onclick = ()=>setPz(pz*1.25);\ndocument.getElementById("pzOut").onclick = ()=>setPz(pz/1.25);\ndocument.getElementById("pzReset").onclick = ()=>{ setPz(1); document.getElementById("pzWrap").scrollTo(0,0); };\n'
   'const posterBtn = document.getElementById("posterBtn");'),
  # v4.2: an item whose title already carries the action has act '' (spine synced to the phase flows); render without the dash
  ('"<b>" + items[i].item + "</b> - " + items[i].act + " <small>("', '"<b>" + items[i].item + "</b>" + (items[i].act ? " - " + items[i].act : "") + " <small>("'),
  ('(items[stepIdx].item + " - " + items[stepIdx].act + "  (" + items[stepIdx].role + ")")', '(items[stepIdx].item + (items[stepIdx].act ? " - " + items[stepIdx].act : "") + "  (" + items[stepIdx].role + ")")'),
  ('"<b>"+it.item+"</b> — "+it.act+" <small>("+it.role+")</small>"', '"<b>"+it.item+"</b>"+(it.act ? " — "+it.act : "")+" <small>("+it.role+")</small>"'),
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
   "function setQrefTheme(dark){ qref.classList.toggle('dark',dark); qrefTheme.innerHTML=dark?'&#9790;':'&#9728;'; try{localStorage.setItem('a330qrefdark',dark?'1':'0');}catch(e){} }\n"
   "function openQref(){ let d=document.body.classList.contains('dark'); try{const v=localStorage.getItem('a330qrefdark'); if(v!==null) d=(v==='1');}catch(e){} setQrefTheme(d); qref.hidden=false; document.getElementById('qrefBtn').classList.add('on'); try{history.pushState({qref:1},'');}catch(e){} }\n"
   "function closeQref(fromPop){ if(qref.hidden) return; qref.hidden=true; document.getElementById('qrefBtn').classList.remove('on'); if(!fromPop && history.state && history.state.qref){ try{history.back();}catch(e){} } }\n"
   "document.getElementById('qrefBtn').addEventListener('click',()=>{ if(qref.hidden) openQref(); else closeQref(); });\n"
   "document.getElementById('qrefBack').addEventListener('click',()=>closeQref());\n"
   "qrefTheme.addEventListener('click',()=>setQrefTheme(!qref.classList.contains('dark')));\n"
   "window.addEventListener('popstate',()=>closeQref(true));\n"
   "document.addEventListener('keydown',e=>{ if(e.key==='Escape' && !qref.hidden) closeQref(); });"),
  # Dark mode contrast (Ryan, 2026-09-22): a phase colour used as TEXT or OUTLINE on the dark ground is lightened
  # 45 % toward white (computed from CL_COLORS, --pcl); headers keep the full colour with white text; checklist
  # rows and FMC titles use the Jeppesen label yellow.
  ("function phaseColor(id){ const c=PHASE_CL[id]; return c ? CL_COLORS[c] : ''; }",
   "function phaseColor(id){ const c=PHASE_CL[id]; return c ? CL_COLORS[c] : ''; }\nfunction lighten(h,f){ f=f===undefined?0.45:f; const n=parseInt(h.slice(1),16); const r=n>>16, g=(n>>8)&255, b=n&255; const m=x=>Math.round(x+(255-x)*f).toString(16).padStart(2,'0'); return '#'+m(r)+m(g)+m(b); }\nfunction pcStyle(pc){ return `--pc:${pc};--pcl:${lighten(pc)}`; }"),
  ('<button data-p="${p.id}"${pc?` data-pc="1" style="--pc:${pc}"`:``}>', '<button data-p="${p.id}"${pc?` data-pc="1" style="${pcStyle(pc)}"`:``}>'),
  ('<button class="ab" data-p="${p.id}"${pc?` data-pc="1" style="--pc:${pc}"`:``}>', '<button class="ab" data-p="${p.id}"${pc?` data-pc="1" style="${pcStyle(pc)}"`:``}>'),
  ('style="--pc:${pc}"`:``}>${ph.title}', 'style="${pcStyle(pc)}"`:``}>${ph.title}'),
  ("if(pc) g.style.setProperty('--pc',pc); else g.style.removeProperty('--pc');", "if(pc){ g.style.setProperty('--pc',pc); g.style.setProperty('--pcl',lighten(pc)); } else { g.style.removeProperty('--pc'); g.style.removeProperty('--pcl'); }"),
  ('body.dark .tech{color:#f2d24c;}', 'body.dark .tech{color:#f2d24c;}\nbody.dark nav button[data-pc]:not(.on),body.dark .rail button[data-pc]:not(.on){color:var(--pcl);border-color:var(--pcl);}\nbody.dark .phasehead.tinted{color:var(--pcl);border-left-color:var(--pcl);}\nbody.dark .cl{color:#f2d24c;border-left-color:#f2d24c;background:rgba(242,210,76,.10);border-color:rgba(242,210,76,.4);}\nbody.dark .cl.cc{color:#8fe3b0;border-left-color:#8fe3b0;}\nbody.dark .clcc{color:#8fe3b0;}\nbody.dark .it.fmc .t{color:#f2d24c;}\nbody.dark .exp{color:#f2d24c;border-color:#f2d24c;}'),
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
  # v4.3 (Ryan, 2026-09-22): drill his own memory-item wording (data/memory_items_myset.json, generated with the phase flows) or the FCOM verbatim set
  ("Promise.all([fetch('data/memory_items_drill.json',{cache:'no-store'}).then(r=>r.json())]).then(function(__b){\nconst [DATA]=__b;",
   "Promise.all([fetch('data/memory_items_drill.json',{cache:'no-store'}).then(r=>r.json()),fetch('data/memory_items_myset.json',{cache:'no-store'}).then(r=>r.json())]).then(function(__b){\nconst [FCOMSET,MYSET]=__b;\nlet SETMODE=(localStorage.getItem('a330_mi_set')==='fcom')?'fcom':'mine';\nlet DATA=SETMODE==='fcom'?FCOMSET:MYSET;\n"
   "function paintSet(){ var sl=document.querySelector('header .src'); if(sl) sl.textContent=SETMODE==='fcom'?'FCOM R17 [MEM]':'My notes · FCOM R17 [MEM]'; var m=document.getElementById('sb-mine'),f=document.getElementById('sb-fcom'); if(m&&f){m.className=SETMODE==='mine'?'on':'';f.className=SETMODE==='fcom'?'on':'';} }\n"
   "window.setSet=function(m){ if(m===SETMODE)return; SETMODE=m; localStorage.setItem('a330_mi_set',m); DATA=(m==='fcom')?FCOMSET:MYSET; paintSet(); start(false); };"),
  ('  <div id="app"></div>', '  <div class="fleetbar" id="setbar"><button id="sb-mine" onclick="setSet(\'mine\')">My notes</button><button id="sb-fcom" onclick="setSet(\'fcom\')">FCOM verbatim</button></div>\n  <div id="app"></div>'),
  ('.hint{', '.fleetbar{display:flex;align-items:center;gap:0;margin:0 0 14px;border:1px solid var(--line);border-radius:6px;overflow:hidden;width:fit-content}\n.fleetbar button{border:0;border-radius:0;padding:7px 16px;font-size:12.5px;font-family:var(--mono);letter-spacing:.06em;text-transform:uppercase;background:transparent;color:var(--muted)}\n.fleetbar button.on{background:var(--atlas);color:#fff}\n.fleetbar button:not(.on):hover{background:var(--panel2);color:var(--ink)}\n.hint{'),
  ('start(false);\nObject.assign(window,{grade, render, reveal, shuffle, start, stepsHTML, summary, toggleSrc});', 'paintSet();start(false);\nObject.assign(window,{grade, render, reveal, shuffle, start, stepsHTML, summary, toggleSrc, paintSet});'),
  ('<div class="cond">Condition: ${d.cond}</div>','${d.cond?`<div class="cond">Condition: ${d.cond}</div>`:``}'),
  ('Condition: ${d.cond}<br>','${d.cond?`Condition: ${d.cond}<br>`:``}'),
 ],
 'limitations.html':[
  # Freighter fleet toggle (hand-edited 2026-09-17, carried here 2026-09-22 so a rebuild keeps it) + Rev 13 set toggle (v4.3):
  # "Rev 13 set" drills only the cards in Ryan's Limitations Summary Rev 13 (data/limitations_myset.json, generated with the phase flows)
  ("Promise.all([fetch('data/limitations_drill.json',{cache:'no-store'}).then(r=>r.json())]).then(function(__b){\nconst [DATA]=__b;",
   "Promise.all([fetch('data/limitations_drill.json',{cache:'no-store'}).then(r=>r.json()),fetch('data/limitations_myset.json',{cache:'no-store'}).then(r=>r.json())]).then(function(__b){\nconst [DATA,MYSET]=__b;"),
  ('  <div id="app"></div>', '  <div class="fleetbar" id="fleetbar">\n    <button id="fb-pax"  onclick="setFleet(\'pax\')">Passenger</button>\n    <button id="fb-frtr" onclick="setFleet(\'frtr\')">Freighter</button>\n  </div>\n  <div class="fleetbar" id="setbar"><button id="sb-rev13" onclick="setSet(\'rev13\')">Rev 13 set</button><button id="sb-all" onclick="setSet(\'all\')">All FCOM</button></div>\n  <div id="app"></div>'),
  ('.hint{', '.fleetbar{display:flex;align-items:center;gap:0;margin:0 0 14px;border:1px solid var(--line);border-radius:6px;overflow:hidden;width:fit-content}\n.fleetbar button{border:0;border-radius:0;padding:7px 16px;font-size:12.5px;font-family:var(--mono);letter-spacing:.06em;text-transform:uppercase;background:transparent;color:var(--muted)}\n.fleetbar button.on{background:var(--atlas);color:#fff}\n.fleetbar button:not(.on):hover{background:var(--panel2);color:var(--ink)}\n#setbar{margin-top:-6px}\n.unver{display:inline-block;font-family:var(--mono);font-size:9.5px;letter-spacing:.1em;text-transform:uppercase;color:#1A1630;background:var(--amber);border-radius:3px;padding:2px 6px;margin-left:8px;font-weight:700;vertical-align:middle}\n.unvernote{border-left:3px solid var(--amber);background:#2A2033;border-radius:4px;padding:10px 12px;font-size:12.5px;color:#EBD9C6;line-height:1.45;margin-top:2px}\n.hint{'),
  ("const MEM=DATA.map((d,i)=>i).filter(i=>DATA[i].mem);",
   "let FLEET=(localStorage.getItem('a330_lim_fleet')==='frtr')?'frtr':'pax';\nlet SETMODE=(localStorage.getItem('a330_lim_set')==='all')?'all':'rev13';\nconst MYIDS=new Set(MYSET.ids||[]);\nfunction inFleet(d){return d.fleet===FLEET||d.fleet==='both'||!d.fleet}\nfunction inSet(d){return SETMODE==='all'||MYIDS.has(d.id)}\nlet MEM=[];\nfunction buildMem(){MEM=DATA.map((d,i)=>i).filter(i=>DATA[i].mem&&inFleet(DATA[i])&&inSet(DATA[i]));}\n"
   "function paintFleet(){\n  var sl=document.querySelector('header .src');\n  if(sl)sl.textContent=((FLEET==='frtr')?'A330F FCOM R10 LIM':'FCOM R17 LIM')+(SETMODE==='rev13'?' · Rev 13 set':'');\n  var p=document.getElementById('fb-pax'),f=document.getElementById('fb-frtr');\n  if(p&&f){p.className=FLEET==='pax'?'on':'';f.className=FLEET==='frtr'?'on':'';}\n  var a=document.getElementById('sb-rev13'),b=document.getElementById('sb-all');\n  if(a&&b){a.className=SETMODE==='rev13'?'on':'';b.className=SETMODE==='all'?'on':'';}\n}\n"
   "function setFleet(f){\n  if(f===FLEET)return;\n  FLEET=f;localStorage.setItem('a330_lim_fleet',f);\n  buildMem();paintFleet();start(false);\n}\n"
   "function setSet(m){\n  if(m===SETMODE)return;\n  SETMODE=m;localStorage.setItem('a330_lim_set',m);\n  buildMem();paintFleet();start(false);\n}"),
  ("<div class=\"cat\">${d.s}${d.mem?'<span class=\"mem\">Memorize</span>':''}</div>", "<div class=\"cat\">${d.s}${d.mem?'<span class=\"mem\">Memorize</span>':''}${d.confidence==='UNVERIFIED'?'<span class=\"unver\">Unverified</span>':''}</div>"),
  ("<div class=\"readout${revealed?' show':''}\"><div class=\"answer\">${d.a}</div></div>", "<div class=\"readout${revealed?' show':''}\"><div class=\"answer\">${d.a}</div>${d.confidence==='UNVERIFIED'?'<div class=\"unvernote\">Not located in the A330F book. The figure shown is the passenger value and is <b>unconfirmed for the freighter</b> - verify before relying on it.</div>':''}</div>"),
  ("start(false);\nObject.assign(window,{grade, render, reveal, shuffle, start, summary, toggleSrc});", "buildMem();paintFleet();start(false);\nObject.assign(window,{grade, render, reveal, shuffle, start, summary, toggleSrc, setFleet, setSet, buildMem, paintFleet});"),
 ],
}
for f,eds in EDITS.items():
    t=open(f,encoding='utf-8').read()
    for a,b in eds:
        assert a in t, (f,a[:40]); t=t.replace(a,b)
    open(f,'w',encoding='utf-8').write(t); print('fixups:',f)
