#!/usr/bin/env python3
"""Deterministic A330 transform for flows_quiz.html (Flows Trainer).

Input: the freshly cloned page, already palette- and string-mapped (apply_palette, apply_strings),
at <repo>/flows_quiz.html. With --from <B787/flows_quiz.html> the clone is produced here first
(copy + apply_palette + apply_strings) so the script also runs standalone.

What changes (data, text content and A330 labels only; CSS, class names, DOM skeleton, controls
and keyboard handling stay byte-identical to the B787 engine):
  1. the inline FLOWS / XREFS / NORMAL_CHECKLISTS literals are removed and the whole engine script
     is wrapped in a fetch of data/flows_trainer.json (same wrapper pattern as externalize.py);
  2. const BG (1.26 MB base64 B787 cockpit JPEG) becomes the URL assets/a330_cockpit.jpg;
  3. the .src line reads the FCOM revision from manuals.json (no lights legend: no A330 light photos);
  4. the checklist overlay footer and the not-found text name the FCTM (A330 normal checklists live
     in FCTM PR-NP-CL; the QRH R35 has none), revision from manuals.json;
  5. the cross-reference linkifier SP.n becomes the A330 manual token set (DSC / PRO / LIM / PER /
     FCTM PR / QRH, longest first) and runs before the all-caps highlighter; the xref box adds the
     section id, PDF page and an Open in Manuals link (/manuals/?s=<section id>) via the .xref class;
  6. the legend label FMC becomes FMS;
  7. the banner logo PNG becomes the placeholder wordmark SVG that gen_index.py uses on index.html.
Each edit asserts its anchor so a changed B787 engine fails loudly.
"""
import os, re, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, '..'))
sys.path.insert(0, HERE)
PAGE = os.path.join(ROOT, 'flows_quiz.html')
if len(sys.argv) > 2 and sys.argv[1] == '--from':
    import apply_palette, apply_strings
    t = open(sys.argv[2], encoding='utf-8').read()
    t = apply_strings.apply(apply_palette.process(t, 'flows_quiz.html'), 'flows_quiz.html')
else:
    t = open(PAGE, encoding='utf-8').read()
if 'const FLOWS = [' not in t:
    sys.exit('flows_quiz.html is not the cloned B787 page (const FLOWS missing); run after apply_strings, not on the stub')
M = json.load(open(os.path.join(ROOT, 'manuals.json'), encoding='utf-8'))
FCOM_REV, FCTM_REV = M['A330P_FCOM']['revision'], M['A330_FCTM']['revision']

def sub1(old, new, flags=0):
    global t
    n = len(re.findall(old, t, flags)) if flags else t.count(old)
    assert n == 1, (old[:60], n)
    t = re.sub(old, lambda m: new, t, flags=flags) if flags else t.replace(old, new)

def literal_end(s, i):
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

# 1. externalize the three banks and wrap the engine in the fetch
s0 = t.index('<script>\n// role: CA | FO | BOTH | PF | PM.') + len('<script>\n')
e0 = t.index('</script>', s0)
body = t[s0:e0]
for name in ('FLOWS', 'XREFS', 'NORMAL_CHECKLISTS'):
    m = re.search(r'^const ' + name + r'\s*=\s*(?=[\[{])', body, re.M); assert m, name
    end = literal_end(body, m.end())
    while end < len(body) and body[end] in ' ;': end += 1
    if end < len(body) and body[end] == '\n': end += 1
    body = body[:m.start()] + body[end:]
funcs = sorted(set(re.findall(r'^function (\w+)\(', body, re.M)))
wrapped = ("/* FLOWS, XREFS and NORMAL_CHECKLISTS live in data/flows_trainer.json, loaded here; engine below is unchanged */\n"
           "fetch('data/flows_trainer.json',{cache:'no-store'}).then(r=>r.json()).then(function(__d){\n"
           "const FLOWS=__d.FLOWS, XREFS=__d.XREFS, NORMAL_CHECKLISTS=__d.NORMAL_CHECKLISTS;\n"
           "if(!FLOWS.length){document.getElementById('drillLayout').innerHTML='<div class=\"card\"><div class=\"tag\">Bank not loaded yet</div><div class=\"who\">This bank is built in a later step. The engine is live.</div></div>';return;}\n"
           + body.rstrip() + "\n"
           "Object.assign(window,{" + ', '.join(funcs) + "});\n"
           "}).catch(function(e){document.getElementById('drillLayout').innerHTML='<div class=\"card\"><div class=\"tag\">Bank failed to load</div><div class=\"who\">'+e.message+'</div></div>';});\n")
t = t[:s0] + wrapped + t[e0:]

# 2. cockpit image: URL instead of the base64 blob
sub1(r'const BG = "data:image/jpeg;base64,[A-Za-z0-9+/=]+";', 'const BG = "assets/a330_cockpit.jpg";', re.S)

# 3. source line from manuals.json
sub1('<div class="src">FCOM R10 NP.21 &middot; exact items, exact order &middot; gate to gate by phase<br>✅ checklist · 🔶 flow trigger · 🗣️ briefing · 💡 lights</div>',
     f'<div class="src">FCOM {FCOM_REV} PRO-NOR-SOP &middot; exact items, exact order &middot; gate to gate by phase<br>✅ checklist · 🔶 flow trigger · 🗣️ briefing</div>')

# 4. checklist overlay source and not-found text
sub1("QRH R7 Normal Checklists (NC.1-2)", f"FCTM {FCTM_REV} Normal Checklists (PR-NP-CL)")
sub1("Checklist not found - see QRH Normal Checklists.", "Checklist not found - see FCTM Normal Checklists.")

# 5. manual cross-reference tokens. The B787 engine links SP.n tokens after its all-caps highlighter. The
#    A330 tokens (DSC-35-20-30, PRO-NOR-SUP-SEC, LIM-APU, PER-..., FCTM PR-NP-CL-..., QRH ...) are one
#    alternation, longest first, and the block moves in front of the all-caps highlighter, because that
#    highlighter wraps "APU APU" in "Refer to LIM-APU APU Start" (and "FCTM PR") in a span, which would
#    split the token. A key containing a space is written with \x20 inside the onclick so the highlighter
#    cannot match inside the attribute either.
XREF_TOKENS = r"FCTM PR-[A-Z0-9-]+|QRH [A-Z0-9.-]+|PRO-(?:NOR|ABN|SPO|SUP)-[A-Z0-9-]+|DSC-\d\d-\d\d(?:-\d\d)?|LIM-[A-Z0-9-]+|PER-[A-Z0-9-]+"
SP_BLOCK = ("  t = t.replace(/\\b(SP\\.\\d+(?:\\.\\d+)?)\\b/g, function(m){\n"
            "    if(XREFS[m]) return '<span class=\"xref\" onclick=\"showXref(\\''+m+'\\');\">'+m+'</span>';\n"
            "    return m;\n"
            "  });\n")
assert t.count(SP_BLOCK) == 1, 'SP.n linkifier block'
t = t.replace(SP_BLOCK, '')
XREF_BLOCK = ("  t = t.replace(/\\b(" + XREF_TOKENS + ")\\b/g, function(m){\n"
              "    if(XREFS[m]) return '<span class=\"xref\" onclick=\"showXref(\\''+m.replace(/ /g,'\\\\x20')+'\\');\">'+m+'</span>';\n"
              "    return m;\n"
              "  });\n")
CAPS_LINE = "  t = t.replace(/([A-Z]{2,}(?:\\s[A-Z0-9\\/]{2,}){1,4})/g, function(m){\n"
sub1(CAPS_LINE, XREF_BLOCK + CAPS_LINE)

# 5b. the cross-reference box also prints the section id and PDF page and links the Manuals page
#     (it accepts ?s=<section id>); the link is styled by the existing .xref class only, no new CSS.
BOX_LINE = '''  box.innerHTML = "<b style='font-size:11px;color:#888;'>" + x.title + "</b>\\n" + x.body;'''
sub1(BOX_LINE, BOX_LINE[:-1] + ''' + (x.ref ? "\\n<b style='font-size:11px;color:#888;'>" + x.ref + (x.page ? " &middot; PDF p. " + x.page : "") + "</b> <a class=\\"xref\\" href=\\"/manuals/?s=" + encodeURIComponent(x.ref) + "\\" target=\\"_blank\\" rel=\\"noopener\\">Open in Manuals</a>" : "");''')

# 6. legend label
sub1('</i>FMC</span>', '</i>FMS</span>')

# 7. banner logo: the same placeholder wordmark gen_index.py uses (until the Hawaiian logo file lands)
logo = "<svg xmlns='http://www.w3.org/2000/svg' width='149' height='44' viewBox='0 0 149 44'><text x='0' y='29' font-family='Segoe UI,Arial,sans-serif' font-size='17' font-weight='700' fill='%23FFFFFF' letter-spacing='1'>HAWAIIAN</text></svg>"
sub1(r'<img src="data:image/png;base64,[A-Za-z0-9+/=]+" alt="Hawaiian Airlines" style="height:30px;">',
     '<img src="data:image/svg+xml,' + logo + '" alt="Hawaiian Airlines" style="height:30px;">', re.S)

assert 'B787' not in t and '787' not in t.replace('assets/A330_hero.svg', ''), 'Boeing string survived'
open(PAGE, 'w', encoding='utf-8').write(t)
print('page_flows_quiz: wrote', PAGE, len(t), 'bytes; window exports:', ', '.join(funcs))
