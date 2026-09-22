#!/usr/bin/env python3
"""phase_flows.html: deterministic A330 transform of the palette- and string-mapped B787 clone.

Input : phase_flows.html in the repo root, already run through apply_palette + apply_strings
        (pass --from <B787 checkout> to clone and map it here first).
Output: the same file, with
  (a) every CSS rule, class, id, control, keyboard/gesture handler and builder function untouched;
  (b) the inline B787 PHASES / QUOTES / CHECKLISTS literals removed and rebuilt from
      data/phase_flows.json through the SAME builders (box/fmc/sub/trig/cl/book/note/S), the whole
      engine wrapped in the fetch callback exactly like build_scripts/externalize.py does;
  (c) the header subtitle versions read from manuals.json (never hardcoded);
  (d) the approach-type toggle relabelled to the A330 FCOM set (ILS / RNP APCH / NPA) with the
      existing markup and CSS;
  (e) the NOTES quick-reference cards rebuilt from data/phase_flows.json `notes` through the same
      c/bl/tg helpers (the B787 gouge cards were inline content).
Usage: page_phase_flows.py [--from <b787_dir>]     run from anywhere; edits <repo>/phase_flows.html
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..'))
PAGE = os.path.join(ROOT, 'phase_flows.html')
sys.path.insert(0, HERE)

def clone_from(b787):
    import apply_palette, apply_strings
    t = open(os.path.join(b787, 'phase_flows.html'), encoding='utf-8').read()
    t = apply_palette.process(t, 'phase_flows.html')
    t = apply_strings.apply(t, 'phase_flows.html')
    open(PAGE, 'w', encoding='utf-8').write(t)

def versions_string():
    m = json.load(open(os.path.join(ROOT, 'manuals.json'), encoding='utf-8'))
    def rev(k):
        e = m[k]; return e['revision'] if e.get('revision') else e['date']
    return ' · '.join(['FCOM ' + rev('A330P_FCOM'), 'QRH ' + rev('A330P_QRH'), 'FCTM ' + rev('A330_FCTM'),
                       'FOM ' + rev('FOM'), 'PRC ' + rev('A330_PRC')])

def literal_end(s, i):
    """i points at the opening [ or {. Return index just past the matching close, string-aware."""
    depth = 0; q = None; j = i
    while j < len(s):
        c = s[j]
        if q:
            if c == '\\': j += 2; continue
            if c == q: q = None
        elif c in '"\'`': q = c
        elif c in '[{': depth += 1
        elif c in ']}':
            depth -= 1
            if depth == 0: return j + 1
        j += 1
    raise SystemExit('unbalanced literal')

def cut_decl(body, name):
    """Remove `const NAME=<literal>;` (plus trailing newline) from body; return (body, removed_text)."""
    m = re.search(r'^const ' + name + r'\s*=\s*(?=[\[{])', body, re.M)
    if not m: raise SystemExit('const ' + name + ' not found')
    end = literal_end(body, m.end())
    while end < len(body) and body[end] in ' ;': end += 1
    if end < len(body) and body[end] == '\n': end += 1
    return body[:m.start()] + body[end:], body[m.start():end]

RECON = """/* phase records, checklists, quotes and NOTES live in data/phase_flows.json and are rebuilt
   here through the builders above; nothing else in this script changes (see build_scripts/page_phase_flows.py) */
const __mk=it=>{ const q=it.quote?it.quote+(it.ref?' ['+it.ref+']':''):'';
  switch(it.k){
    case 'box': return box(it.t,it.s,it.r,it.call,q);
    case 'fmc': return fmc(it.t,it.s,it.r,q);
    case 'sub': return sub(it.t,it.c);
    case 'trig': return trig(it.t,it.r);
    case 'cl': return cl(it.t,it.w,it.bold,it.cc);
    case 'book': return book(it.t,it.s);
    default: return note(it.t||'');
  } };
const PHASES=PHASE_FLOWS.phases.map(p=>({id:p.id,label:p.label,kind:p.kind,title:p.title,src:p.src,
  sections:p.sections.map(s=>S(s.h,s.c,s.items.map(__mk),s.cite,s.appr))}));
const VERSIONS=%s;
document.getElementById('srcsub').textContent=VERSIONS;
const QUOTES=PHASE_FLOWS.quotes||{};
const NOTES=PHASE_FLOWS.notes||[];
"""

def transform(t):
    # ---- script body boundaries
    s0 = t.index('<script>\n') + len('<script>\n')
    e0 = t.index('</script>', s0)
    body = t[s0:e0]

    # ---- (b) drop the inline PHASES literal + MAINTENANCE comment + VERSIONS + QUOTES literal
    body, _ = cut_decl(body, 'PHASES')
    mm = re.search(r'\n?/\* =+\n   MAINTENANCE:.*?=+ \*/\n', body, re.S)
    if not mm: raise SystemExit('MAINTENANCE comment not found')
    body = body[:mm.start()] + '\n' + body[mm.end():]
    vm = re.search(r"^const VERSIONS='[^\n]*';\n", body, re.M)
    if not vm: raise SystemExit('VERSIONS not found')
    body = body[:vm.start()] + body[vm.end():]
    body = body.replace("document.getElementById('srcsub').textContent=VERSIONS;\n", '', 1)
    body, _ = cut_decl(body, 'QUOTES')
    # CHECKLISTS literal (and its one-line comment) -> from data
    body = body.replace('// QRH normal checklists (item, response, role) for click-to-show with role greying\n', '', 1)
    body, _ = cut_decl(body, 'CHECKLISTS')
    body = body.replace("let state={phase:'preflight'",
        "const CHECKLISTS=Object.fromEntries(Object.entries(PHASE_FLOWS.checklists).map(([k,v])=>[k,v.items]));\nlet state={phase:'preflight'", 1)
    # reconstruct through the same builders, right after the builder definitions
    anchor = "const S=(h,c,items,cite,appr)=>({h,c,items,cite:cite||'',appr:appr||'all'});\n"
    if anchor not in body: raise SystemExit('builder anchor not found')
    body = body.replace(anchor, anchor + '\n' + RECON % json.dumps(versions_string(), ensure_ascii=False), 1)

    # ---- (e) NOTES cards from data through the same c / bl / tg helpers
    n0 = body.index('function notesCards(){')
    n1 = body.index('\nfunction fitNotesToScreen', n0)
    seg = body[n0:n1]
    r0 = seg.index('  return [')
    r1 = seg.rindex('  ];')
    seg = seg[:r0] + ("  return NOTES.map(n=> n.k==='tg' ? tg(n.t) : n.k==='ol' ? c(n.h,n.ec,'<ol class=\"cl-order\">'+n.items.map(x=>`<li>${x}</li>`).join('')+'</ol>') : c(n.h,n.ec,bl(n.items)));") + seg[r1 + len('  ];'):]
    body = body[:n0] + seg + body[n1:]

    # checklist footer wording: A330 SCO has the PM announce "__ CHECKLIST COMPLETE"
    body = body.replace('<div class="clcc">both pilots: CHECKLIST COMPLETE</div>', '<div class="clcc">PM: __ CHECKLIST COMPLETE</div>', 1)

    # ---- fetch wrapper (same shape as externalize.py: engine byte-identical inside the callback)
    funcs = sorted(set(re.findall(r'^function (\w+)\(', body, re.M)))
    fail = ("(document.getElementById('main')||document.body).innerHTML='<div class=\"empty\">Phase data failed to load: '+e.message+'</div>';")
    wrapped = ("/* bank PHASE_FLOWS lives in data/phase_flows.json, loaded here; engine below is unchanged */\n"
               "Promise.all([fetch('data/phase_flows.json',{cache:'no-store'}).then(r=>r.json())]).then(function(__b){\n"
               "const [PHASE_FLOWS]=__b;\n" + body.rstrip() + "\n"
               "Object.assign(window,{" + ', '.join(funcs) + "});\n"
               "}).catch(function(e){" + fail + "});\n")
    t = t[:s0] + wrapped + t[e0:]

    # ---- (d) approach-type toggle: A330 FCOM set, same markup and CSS
    t = t.replace('<button data-a="IAN">IAN</button>', '<button data-a="RNP">RNP&nbsp;APCH</button>', 1)
    t = t.replace('<button data-a="RNPAR">RNP&nbsp;AR</button>', '<button data-a="NPA">NPA</button>', 1)

    # ---- (e) memorization sections (2026-09-21): a section with mem:true (resection_cockpit_prep.py)
    #      paints its card header in the section color instead of only the left stripe
    a = 'sections:p.sections.map(s=>S(s.h,s.c,s.items.map(__mk),s.cite,s.appr))}));'
    assert t.count(a) == 1, 'phase_flows: sections map anchor missing'
    t = t.replace(a, 'sections:p.sections.map(s=>Object.assign(S(s.h,s.c,s.items.map(__mk),s.cite,s.appr),s.mem?{mem:true}:{}))}));')
    a = '<div class="ch" style="--ec:${sec.c}">'
    assert t.count(a) == 2, 'phase_flows: card header anchor count'
    t = t.replace(a, '<div class="ch" style="--ec:${sec.c}${sec.mem?`;background:${sec.c}`:``}">')

    # ---- (f) MINE hides a section whose role-carrying items are all the other pilot's, and a memorization
    #      header's count follows the current seat/duty (2026-09-21)
    a = "function sectionInner(sec,cite,ctx,pid){"
    assert t.count(a) == 1, 'phase_flows (f): anchor missing: ' + a[:50]
    t = t.replace(a, "function secVisible(sec){\n  // role-carrying items of a section that match the current seat/duty (2026-09-21, MINE fix)\n  const roled = sec.items.filter(it=>['box','fmc','trig','cl','book'].includes(it.k) && it.r);\n  const steps = sec.items.filter(it=>['box','fmc','book'].includes(it.k) ? roleMatch(it.r) : it.k==='cl');\n  return {roled: roled.length, vis: roled.filter(it=>roleMatch(it.r)).length, n: steps.length};\n}\nfunction secHead(sec){\n  const v = secVisible(sec);\n  if(!sec.mem || !v.vis) return sec.h;\n  let h = sec.h.replace(/(·\\s*)(\\d+)\\s*$/, (m,a)=>a+v.n);\n  if(state.seat==='C') h = h.replace(/^CM2 · /, 'CM1 · '); // the seat-indexed groups read as the seat being viewed\n  return h;\n}\nfunction sectionInner(sec,cite,ctx,pid){")
    a = "CARDS.push(`<div class=\"card\"><div class=\"ch\" style=\"--ec:${sec.c}${sec.mem?`;background:${sec.c}`:``}\"><span class=\"hn\">${sec.h}</span><span class=\"cardcite\">${cite}</span></div><div class=\"cb\">${inner}</div></div>`);"
    assert t.count(a) == 1, 'phase_flows (f): anchor missing: ' + a[:50]
    t = t.replace(a, "CARDS.push(`<div class=\"card\"><div class=\"ch\" style=\"--ec:${sec.c}${sec.mem?`;background:${sec.c}`:``}\"><span class=\"hn\">${secHead(sec)}</span><span class=\"cardcite\">${cite}</span></div><div class=\"cb\">${inner}</div></div>`);")
    a = "out.push(`<div class=\"card\"><div class=\"ch\" style=\"--ec:${sec.c}${sec.mem?`;background:${sec.c}`:``}\"><span class=\"hn\">${sec.h}</span><span class=\"cardcite\">${cite}</span></div><div class=\"cb\">${inner}</div></div>`);"
    assert t.count(a) == 1, 'phase_flows (f): anchor missing: ' + a[:50]
    t = t.replace(a, "out.push(`<div class=\"card\"><div class=\"ch\" style=\"--ec:${sec.c}${sec.mem?`;background:${sec.c}`:``}\"><span class=\"hn\">${secHead(sec)}</span><span class=\"cardcite\">${cite}</span></div><div class=\"cb\">${inner}</div></div>`);")
    a = "  ph.sections.forEach(sec=>{\n    if(!apprVisible(sec.appr))return;\n    const cite=sec.cite||ph.src;\n    const inner=sectionInner(sec,cite,ctx,ph.id);\n    CARDS.push("
    assert t.count(a) == 1, 'phase_flows (f): anchor missing: ' + a[:50]
    t = t.replace(a, "  ph.sections.forEach(sec=>{\n    if(!apprVisible(sec.appr))return;\n    { const v=secVisible(sec); if(state.hideOther && v.roled && !v.vis) return; }\n    const cite=sec.cite||ph.src;\n    const inner=sectionInner(sec,cite,ctx,ph.id);\n    CARDS.push(")
    a = "  ph.sections.forEach(sec=>{ if(!apprVisible(sec.appr))return; const cite=sec.cite||ph.src;\n    const inner=sectionInner(sec,cite,ctx,ph.id);\n    out.push("
    assert t.count(a) == 1, 'phase_flows (f): anchor missing: ' + a[:50]
    t = t.replace(a, "  ph.sections.forEach(sec=>{ if(!apprVisible(sec.appr))return; { const v=secVisible(sec); if(state.hideOther && v.roled && !v.vis) return; } const cite=sec.cite||ph.src;\n    const inner=sectionInner(sec,cite,ctx,ph.id);\n    out.push(")
    # ---- (g) a memorization card never splits across columns, so its colored header stays with its items
    a = ".it,.trig,.cl,.clwrap,.book,.sub,.note{break-inside:avoid;-webkit-column-break-inside:avoid;}"
    assert t.count(a) == 1, 'phase_flows (g): anchor missing: ' + a[:50]
    t = t.replace(a, ".it,.trig,.cl,.clwrap,.book,.sub,.note{break-inside:avoid;-webkit-column-break-inside:avoid;}\n.card.mem{break-inside:avoid;-webkit-column-break-inside:avoid;}")
    a = "CARDS.push(`<div class=\"card\"><div class=\"ch\""
    assert t.count(a) == 1, 'phase_flows (g): anchor missing: ' + a[:50]
    t = t.replace(a, "CARDS.push(`<div class=\"card${sec.mem&&sec.items.length<=5?' mem':''}\"><div class=\"ch\"")
    a = "out.push(`<div class=\"card\"><div class=\"ch\""
    assert t.count(a) == 1, 'phase_flows (g): anchor missing: ' + a[:50]
    t = t.replace(a, "out.push(`<div class=\"card${sec.mem&&sec.items.length<=5?' mem':''}\"><div class=\"ch\"")
    a = "  applyCols(grid,CARDS,ncol,GFONT);\n  requestAnimationFrame(positionCues);"
    assert t.count(a) == 1, 'phase_flows (g): fit anchor missing'
    t = t.replace(a, "  const sparse = CARDS.length < colsForWidth(W); grid.style.maxWidth = sparse ? (ncol*640)+'px' : ''; grid.style.margin = sparse ? '0' : ''; // sparse pages: column-width cards, left-justified (Ryan, 2026-09-22)\n  { let f = sparse ? bestFontFor(CARDS,ncol,avail,grid) : GFONT; let h=applyCols(grid,CARDS,ncol,f); while(h>avail && f>FLOOR){ f-=0.5; h=applyCols(grid,CARDS,ncol,f); } } // sparse pages (fewer cards than columns) narrow the grid and use their own best font; a page with unsplittable cards may need its own shrink\n  requestAnimationFrame(positionCues);")
    # ---- (h) Jeppesen dark palette (Ryan, 2026-09-22)
    a = "body.dark{\n  --bg:#15131C;--card:#211D2E;--ink:#EDE9F3;--muted:#A29DB0;--line:#453F58;\n  --head:#2A2440;--nav:#1A1630;--navbtn:#2A2440;--navink:#EAE5F4;--accent:#E26DB8;\n  --limbg:#46380e;--limink:#ffd86b;--qbg:#1A1630;\n}"
    assert t.count(a) == 1, 'phase_flows (h): anchor missing'
    t = t.replace(a, "body.dark{\n  /* Jeppesen FD Pro dark palette, sampled from the airport moving map (Ryan, 2026-09-22):\n     chrome #21232a, buttons #41434d, active blue #3579c1, map ground #0a1117, slate #35434d, labels yellow */\n  --bg:#0a1117;--card:#1b232b;--ink:#f2f4f6;--muted:#9aa8b3;--line:#35434d;\n  --head:#21232a;--nav:#0a1117;--navbtn:#21232a;--navink:#e6e9ec;--accent:#3579c1;\n  --limbg:#3a3418;--limink:#f2d24c;--qbg:#14234c;--blue:#f2d24c;\n}\nbody.dark .rtag.C{background:#41434d;}body.dark .it.fmc .stepn{background:#41434d;color:#f2d24c;}")
    a = "body.dark .tech{color:#E26DB8;}"
    assert t.count(a) == 1, 'phase_flows (h): anchor missing'
    t = t.replace(a, "body.dark .tech{color:#f2d24c;}")
    # ---- (i) never more columns than cards
    a = "  const W=grid.clientWidth||main.clientWidth;\n  const ncol=colsForWidth(W);\n  if(!GFONT"
    assert t.count(a) == 1, 'phase_flows (i): anchor missing'
    t = t.replace(a, "  const W=grid.clientWidth||main.clientWidth;\n  const ncol=Math.min(colsForWidth(W), Math.max(1, CARDS.length)); // never more columns than cards (Ryan, 2026-09-22)\n  if(!GFONT")
    # ---- (j) theme icons show the current state; phase arrows only where a phase exists that way
    a = "function setTheme(dark){ document.body.classList.toggle('dark',dark); themeBtn.innerHTML=dark?'&#9728;':'&#9790;';"
    assert t.count(a) == 1, 'phase_flows (j): anchor missing'
    t = t.replace(a, "function setTheme(dark){ document.body.classList.toggle('dark',dark); themeBtn.innerHTML=dark?'&#9790;':'&#9728;'; // moon while dark, sun while light (Ryan, 2026-09-22)")
    a = "  document.querySelectorAll('#nav button, #rail button').forEach(b=>b.classList.toggle('on',b.dataset.p===state.phase));\n  saveState();"
    assert t.count(a) == 1, 'phase_flows (j): anchor missing'
    t = t.replace(a, "  document.querySelectorAll('#nav button, #rail button').forEach(b=>b.classList.toggle('on',b.dataset.p===state.phase));\n  { const pi=PHASES.findIndex(p=>p.id===state.phase); document.getElementById('prev').style.visibility=pi>0?'':'hidden'; document.getElementById('next').style.visibility=pi<PHASES.length-1?'':'hidden'; } // arrows only where a phase exists that way\n  saveState();")
    # ---- (k) phone reads vertically; wider screens get a FIT toggle (Ryan, 2026-09-22)
    # Fit mode (the old behaviour) constrains the grid height so multicol overflows into extra columns to
    # the RIGHT (horizontal scroll, shrinking font). Read mode lets the grid grow, 16 px, one column on a
    # phone / two on wider screens, so the page scrolls vertically only. Phones are always in read mode
    # and never see the FIT button; wider screens default to FIT on, choice persisted like the theme.
    a = '    <button class="themebtn filt" id="filt" title="Show or hide the other crew member\'s steps">BOTH</button>\n'
    assert t.count(a) == 1, 'phase_flows (k): filt button anchor missing'
    t = t.replace(a, a + '    <button class="themebtn filt" id="fit" title="Fit the page to the screen, or scroll it at reading size"><svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 4l16 16M20 4L4 20"/><path d="M4 4h6M4 4v6M20 4h-6M20 4v6M4 20h6M4 20v-6M20 20h-6M20 20v-6"/></svg></button>\n')  # X with arrows on the corners (Ryan, 2026-09-22)
    a = "@media (max-width:600px){.arrow{display:none;}}"
    assert t.count(a) == 1, 'phase_flows (k): media anchor missing'
    t = t.replace(a, a + "\n#fit{min-width:40px;padding:0;display:inline-flex;align-items:center;justify-content:center;}\n@media (max-width:600px){#fit{display:none;}}  /* a phone always reads vertically; FIT is a Mac/iPad control (the media rule must come after the base rule) */")
    a = "function colsForWidth(W){ return W>=1100?4 : W>=820?3 : W>=600?2 : 1; }\n"
    assert t.count(a) == 1, 'phase_flows (k): colsForWidth anchor missing'
    t = t.replace(a, a + "function readMode(W){ return !state.fit || colsForWidth(W)===1; }\n"
        "function applyRead(grid,cards,W,avail){ const phone=colsForWidth(W)===1; const ncol=phone?1:Math.min(colsForWidth(W),Math.max(1,cards.length)); grid.style.flex=phone?'0 0 auto':''; const sparse=!phone && cards.length<colsForWidth(W); const lock=!phone && !sparse; grid.style.height=lock?avail+'px':''; grid.style.columnFill=lock?'auto':''; grid.style.flex=lock?'':'0 0 auto'; grid.style.minHeight=''; grid.style.maxWidth=sparse?(ncol*640)+'px':''; grid.style.margin=sparse?'0':''; applyCols(grid,cards,ncol,16); } // sparse pages (fewer cards than columns) are column-width, left-justified and scroll down instead of sideways // FIT off: phone scrolls down; Mac/iPad keep 16 px, the height lock and the columns continuing to the right (Ryan, 2026-09-22)\n"
        "function unRead(grid){ grid.style.flex='0 0 auto'; grid.style.height=''; grid.style.columnFill=''; } // fit mode too lets the grid grow: multicol balances its columns and only the font shrinks to fit, never extra columns off to the right (Ryan, 2026-09-22)\n")
    a = "  const W=grid.clientWidth||main.clientWidth;\n  const ncol=Math.min(colsForWidth(W), Math.max(1, CARDS.length));"
    assert t.count(a) == 1, 'phase_flows (k): fit anchor missing'
    t = t.replace(a, "  const W=grid.clientWidth||main.clientWidth;\n  if(readMode(W)){ applyRead(grid,CARDS,W,avail); requestAnimationFrame(positionCues); return; } unRead(grid);\n  const ncol=Math.min(colsForWidth(W), Math.max(1, CARDS.length));")
    a = "  const W=grid.clientWidth||main.clientWidth;\n  const ncol=colsForWidth(W);\n  const f=bestFontFor(CARDS,ncol,avail,grid);"
    assert t.count(a) == 1, 'phase_flows (k): notes fit anchor missing'
    t = t.replace(a, "  const W=grid.clientWidth||main.clientWidth;\n  if(readMode(W)){ applyRead(grid,CARDS,W,avail); requestAnimationFrame(positionCues); return; } unRead(grid);\n  const ncol=colsForWidth(W);\n  const f=bestFontFor(CARDS,ncol,avail,grid);")
    a = "appr:'ILS',cat:1,hideOther:false,notesOpen:false};"
    assert t.count(a) == 1, 'phase_flows (k): state anchor missing'
    t = t.replace(a, "appr:'ILS',cat:1,hideOther:false,notesOpen:false,fit:true};")
    a = "themeBtn.addEventListener('click',()=>setTheme(!document.body.classList.contains('dark')));\n"
    assert t.count(a) == 1, 'phase_flows (k): theme anchor missing'
    t = t.replace(a, a + "const fitBtn=document.getElementById('fit');\n"
        "function setFit(on){ state.fit=on; fitBtn.classList.toggle('on',on); fitBtn.title=on?'Fit to screen is on. Tap to scroll at reading size':'Reading size. Tap to fit the page to the screen'; try{localStorage.setItem('a330fit',on?'1':'0');}catch(e){} }\n"
        "fitBtn.addEventListener('click',()=>{ setFit(!state.fit); GFONT=0; fitCurrent(); });\n"
        "{ let f=true; try{f=localStorage.getItem('a330fit')!=='0';}catch(e){} setFit(f); }\n")
    # ---- (l) a checklist is read complete (Ryan, 2026-09-22): every card row shows under BOTH and MINE;
    #      rows where this pilot does not respond are dimmed, never dropped; BOTH rows carry PF and PM chips side by side
    a = "const body=items.filter(ci=>!(state.hideOther&&!roleMatch(ci[2]))).map(ci=>`<div class=\"cli${roleMatch(ci[2])?'':' dim'}\"><span class=\"cii\">${ci[0]}</span><span class=\"civ\">${deco(ci[1])}</span>${rtagHtml(ci[2])}</div>`).join('')||'<div class=\"cli\">(reference)</div>';"
    assert t.count(a) == 1, 'phase_flows (l): checklist row anchor missing'
    t = t.replace(a, "const clTag=r=>r==='B'?rtagHtml('PF')+rtagHtml('PM'):rtagHtml(r); // BOTH rows: both responders shown\n    const body=items.map(ci=>`<div class=\"cli${roleMatch(ci[2])?'':' dim'}\"><span class=\"cii\">${ci[0]}</span><span class=\"civ\">${deco(ci[1])}</span>${clTag(ci[2])}</div>`).join('')||'<div class=\"cli\">(reference)</div>';")
    # ---- (n) phase bar (Ryan, 2026-09-22): 44 px buttons, 15 px text, snap on touch, wheel scrolls sideways on a Mac,
    #      pagers 52 px wide jumping a full bar width; the active phase is already centred by scrollActive()
    a = "nav button{flex:none;border:1.5px solid transparent;background:var(--navbtn);color:var(--navink);font-weight:800;\nfont-size:13px;padding:9px 14px;border-radius:18px;cursor:pointer;letter-spacing:.2px;}"
    assert t.count(a) == 1, 'phase_flows (n): nav button css anchor missing'
    t = t.replace(a, "nav button{flex:none;border:1.5px solid transparent;background:var(--navbtn);color:var(--navink);font-weight:800;\nfont-size:15px;padding:0 16px;min-height:44px;border-radius:22px;cursor:pointer;letter-spacing:.2px;scroll-snap-align:center;}")
    a = "scroll-behavior:smooth;touch-action:pan-x;scrollbar-width:none;}"
    assert t.count(a) == 1, 'phase_flows (n): nav css anchor missing'
    t = t.replace(a, "scroll-behavior:smooth;touch-action:pan-x;scrollbar-width:none;scroll-snap-type:x proximity;gap:12px;}")
    a = ".npag{position:sticky;flex:none;align-self:stretch;width:38px;min-width:38px;"
    assert t.count(a) == 1, 'phase_flows (n): pager css anchor missing'
    t = t.replace(a, ".npag{position:sticky;flex:none;align-self:stretch;width:52px;min-width:52px;")
    a = "function navPage(dir){ navEl.scrollBy({left:dir*Math.max(170,navEl.clientWidth*0.72),behavior:'smooth'}); }\n"
    assert t.count(a) == 1, 'phase_flows (n): navPage anchor missing'
    t = t.replace(a, "function navPage(dir){ navEl.scrollBy({left:dir*Math.max(170,navEl.clientWidth-120),behavior:'smooth'}); } // a full bar width less the pagers\n"
        "navEl.addEventListener('wheel',e=>{ if(Math.abs(e.deltaY)>Math.abs(e.deltaX)){ navEl.scrollLeft+=e.deltaY; e.preventDefault(); } },{passive:false}); // Mac: vertical wheel or trackpad over the bar scrolls it sideways\n")
    # ---- (o) exterior light switch actions in green (Ryan, 2026-09-22): NOSE / RWY TURN OFF / STROBE / LAND / WING / BEACON / NAV & LOGO
    a = "function deco(s){ return s? hl(boldST(boldCO(s))) : ''; }"
    assert t.count(a) == 1, 'phase_flows (o): deco anchor missing'
    t = t.replace(a, "const LIGHTS=/((?:NOSE|STROBE|BEACON|WING|LAND(?: LIGHT)?|RWY TURN OFF|NAV & LOGO|Rwy Turnoff|Strobes|Nose|Land|Nav|Beacon|Wing)(?: sw)?(?: \\.\\.\\. | )(?:ON|OFF|TAXI|T\\.O\\.?|AUTO|1|AS RQRD))(?![\\w])/g;\n"
        "function lights(s){ return s.replace(LIGHTS,\"<span class='lt'>$1</span>\"); } // single quotes: boldCO turns double quotes into callouts\n"
        "function deco(s){ return s? hl(boldST(boldCO(lights(s)))) : ''; }")
    a = "body.dark .tech{color:#f2d24c;}"
    assert t.count(a) == 1, 'phase_flows (o): css anchor missing'
    t = t.replace(a, a + "\n.lt{background:#E0F2FE;color:#075985;font-weight:800;border-radius:3px;padding:0 3px;}.lt b{color:#075985;}body.dark .lt{background:#0c3a55;color:#7dd3fc;}body.dark .lt b{color:#7dd3fc;}  /* sky-blue chip: light switches (Ryan, 2026-09-22) */")
    # ---- (p) altitude gates written the FCOM way with a space (18 000 ft, 10 000 ft) get the same highlight as 18,000 (Ryan, 2026-09-22)
    a = "|10,000 ft|18,000|FL180|FL100|"
    assert t.count(a) == 1, 'phase_flows (p): LIM anchor missing'
    t = t.replace(a, "|10,000 ft|10 000 ft(?: MSL| AAL)?|18,000|18 000 ft(?: MSL)?|FL180|FL100|")
    # a height token inside a bigger number (12 500 ft, 9 200 ft, 17 500 ft) is not a gate: no digit or digit-space before it
    a = "|300 ft|500 ft|400 ft|200 ft|75 ft|"
    assert t.count(a) == 1, 'phase_flows (p): height tokens anchor missing'
    t = t.replace(a, "|(?<!\\d)(?<!\\d )300 ft|(?<!\\d)(?<!\\d )500 ft|(?<!\\d)(?<!\\d )400 ft|(?<!\\d)(?<!\\d )200 ft|(?<!\\d)(?<!\\d )75 ft|")
    # ---- (q) whole row light blue when the item changes an exterior light (Ryan, 2026-09-22)
    a = "    const cls='it'+(it.call?' say':'')+(it.fmc?' fmc':'')+(q?' has-q':'')+dim;"
    assert t.count(a) == 1, 'phase_flows (q): cls anchor missing'
    t = t.replace(a, "    const cls='it'+(it.call?' say':'')+(it.fmc?' fmc':'')+(q?' has-q':'')+dim+(LIGHTS.test(it.t+' '+(it.s||''))?' lights':''); LIGHTS.lastIndex=0;")
    a = "body.dark .tech{color:#f2d24c;}"
    assert t.count(a) == 1, 'phase_flows (q): css anchor missing'
    t = t.replace(a, a + "\n.it.lights{background:#EAF6FF;border-radius:6px;margin-left:-4px;padding-left:4px;margin-right:-4px;padding-right:4px;}body.dark .it.lights{background:#0f2a3f;}")
    # ---- (r) long bullet lists fold to a cue (first 5) until tapped (Ryan, 2026-09-22): the card stays a memorization cue,
    #      the full FCOM list is one tap away, and the phone page stops being a wall of text
    a = "(LIGHTS.test(it.t+' '+(it.s||''))?' lights':''); LIGHTS.lastIndex=0;"
    assert t.count(a) == 1, 'phase_flows (r): cls anchor missing'
    t = t.replace(a, "(LIGHTS.test(it.t+' '+(it.s||''))?' lights':'')+(((it.s||'').split(' · ').length>6)?' long':''); LIGHTS.lastIndex=0;")
    a = "  const q=e.target.closest('.it.has-q'); if(q){ q.classList.toggle('open'); return; }"
    assert t.count(a) == 1, 'phase_flows (r): click anchor missing'
    t = t.replace(a, "  const lg=e.target.closest('.it.long'); if(lg){ lg.classList.toggle('open'); return; }\n" + a)
    a = "body.dark .tech{color:#f2d24c;}"
    assert t.count(a) == 1, 'phase_flows (r): css anchor missing'
    t = t.replace(a, a + "\n.it.long{cursor:pointer;}.it.long:not(.open) ul.bl li:nth-child(n+6){display:none;}.it.long:not(.open) ul.bl::after{content:'… tap for the full list';display:block;font-size:.7em;font-weight:700;color:var(--accent);padding-left:13px;margin-top:2px;}")
    return t

if __name__ == '__main__':
    if len(sys.argv) > 2 and sys.argv[1] == '--from':
        clone_from(sys.argv[2])
    t = open(PAGE, encoding='utf-8').read()
    if 'const PHASES=[' not in t:
        raise SystemExit('phase_flows.html is not the B787 engine clone (already transformed, or a stub); pass --from <b787_dir>')
    t = transform(t)
    open(PAGE, 'w', encoding='utf-8').write(t)
    print('phase_flows.html transformed; versions:', versions_string())
