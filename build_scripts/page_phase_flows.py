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
    t = t.replace(a, "  { let f=GFONT, h=applyCols(grid,CARDS,ncol,f); while(h>avail && f>FLOOR){ f-=0.5; h=applyCols(grid,CARDS,ncol,f); } } // a page with unsplittable cards may need its own shrink (2026-09-21)\n  requestAnimationFrame(positionCues);")
    # ---- (h) Jeppesen dark palette (Ryan, 2026-09-22)
    a = "body.dark{\n  --bg:#15131C;--card:#211D2E;--ink:#EDE9F3;--muted:#A29DB0;--line:#453F58;\n  --head:#2A2440;--nav:#1A1630;--navbtn:#2A2440;--navink:#EAE5F4;--accent:#E26DB8;\n  --limbg:#46380e;--limink:#ffd86b;--qbg:#1A1630;\n}"
    assert t.count(a) == 1, 'phase_flows (h): anchor missing'
    t = t.replace(a, "body.dark{\n  /* Jeppesen FD Pro dark palette, sampled from the airport moving map (Ryan, 2026-09-22):\n     chrome #21232a, buttons #41434d, active blue #3579c1, map ground #0a1117, slate #35434d, labels yellow */\n  --bg:#0a1117;--card:#1b232b;--ink:#f2f4f6;--muted:#9aa8b3;--line:#35434d;\n  --head:#21232a;--nav:#0a1117;--navbtn:#21232a;--navink:#e6e9ec;--accent:#3579c1;\n  --limbg:#3a3418;--limink:#f2d24c;--qbg:#14234c;--blue:#f2d24c;\n}\nbody.dark .rtag.C{background:#41434d;}body.dark .it.fmc .stepn{background:#41434d;color:#f2d24c;}")
    a = "body.dark .tech{color:#E26DB8;}"
    assert t.count(a) == 1, 'phase_flows (h): anchor missing'
    t = t.replace(a, "body.dark .tech{color:#f2d24c;}")
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
