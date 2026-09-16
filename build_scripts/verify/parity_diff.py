#!/usr/bin/env python3
"""CSS and DOM parity between the B787 original and the A330 clone.
For each page pair: transform the B787 file with apply_palette + apply_strings in memory, then
compare (a) every <style> block, (b) every inline style="", (c) CSS string literals in the JS,
(d) the tag/class skeleton with text stripped. Must be empty except docs/PARITY_ALLOWLIST.md.
Usage: parity_diff.py <b787 dir> <a330 dir>"""
import sys, os, re, difflib, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__),'..'))
import apply_palette, apply_strings
B, A = sys.argv[1], sys.argv[2]
PAIRS={'mcdu_preflight.html':'cdu_preflight.html'}
STUBS=set(json.load(open(os.path.join(A,'versions.json'))).get('stubs',[]))
ALLOW=[l[2:].strip() for l in open(os.path.join(A,'docs','PARITY_ALLOWLIST.md')) if l.startswith('- ')]
def transform(text,name):
    return apply_strings.apply(apply_palette.process(text,name),name)
def css_of(t):
    out=re.findall(r'<style[^>]*>(.*?)</style>', t, re.S)
    out+=re.findall(r'style="([^"]*)"', t)
    out+=re.findall(r"'((?:[.#@][\w\-#.:>,\s\[\]=\"()]+\{[^']*\})+)'", t)  # CSS in JS strings
    return [re.sub(r'\s+',' ',x).strip() for x in out]
def skel(t):
    body=t.split('<body',1)[-1]
    body=re.sub(r'<script.*?</script>','',body,flags=re.S)
    return re.findall(r'<([a-z0-9]+)(?:[^>]*?class="([^"]*)")?', body)
fails=0
for f in sorted(os.listdir(A)):
    if not f.endswith(('.html','.js')) or f in STUBS: continue
    src=os.path.join(B, PAIRS.get(f,f))
    if not os.path.exists(src): print('no twin for',f); continue
    b=transform(open(src,encoding='utf-8').read(), f); a=open(os.path.join(A,f),encoding='utf-8').read()
    d=[l for l in difflib.unified_diff(css_of(b), css_of(a), lineterm='', n=0) if l.startswith(('+','-')) and not l.startswith(('+++','---'))]
    d=[l for l in d if not any(k in l for k in ALLOW)]
    if f.endswith('.html'):
        sd=[l for l in difflib.unified_diff([' '.join(x) for x in skel(b)], [' '.join(x) for x in skel(a)], lineterm='', n=0) if l.startswith(('+','-')) and not l.startswith(('+++','---'))]
        sd=[l for l in sd if not any(k in l for k in ALLOW)]
    else: sd=[]
    if d or sd:
        fails+=1; print(f'== {f}: css {len(d)} dom {len(sd)}')
        for l in (d+sd)[:8]: print('   ',l[:160])
print('parity failures:',fails)
sys.exit(1 if fails else 0)
