#!/usr/bin/env python3
"""Apply palette_map.py to every html/js file in a tree, in place.
Usage: apply_palette.py <dir>   (skips base64 blobs and HTML entities)."""
import re, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from palette_map import MAP, LIME, LIME_TEXT_ON_DARK, LIME_FILL_ON_LIGHT, LIME_BORDER_ON_LIGHT, OVERRIDES, DARK_FAMILY

HEX = re.compile(r'(?<![&\w])#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b')
DECL = re.compile(r'([a-zA-Z-]+)\s*:\s*([^;{}"\']*)')

def lime_for(prop, dark):
    p = prop.lower()
    if dark: return LIME_TEXT_ON_DARK
    if p.startswith('background') or p == 'fill' or p.startswith('accent'): return LIME_FILL_ON_LIGHT
    if p.startswith('border') or p.startswith('outline'): return LIME_BORDER_ON_LIGHT
    return LIME_TEXT_ON_DARK   # color on a dark surface (banners, modal headers, footers)

def hover_bg(prop, val, value):
    # atlas as a hover/button background -> deep fuchsia, not link fuchsia
    return value in ('#00679c','#007cba','#0074c8') and prop.lower().startswith('background')

def process(text, name):
    stem = name.rsplit('.',1)[0]
    dark = stem in DARK_FAMILY
    for a,b in OVERRIDES.get(name, []):
        if a not in text: print(f'  override miss in {name}: {a[:60]}')
        text = text.replace(a,b)
    # protect base64 blobs
    blobs=[]
    def keep(m): blobs.append(m.group(0)); return f'\x00BLOB{len(blobs)-1}\x00'
    text = re.sub(r'data:[a-z/+.-]+;base64,[A-Za-z0-9+/=]+', keep, text)
    out=[]; pos=0
    for d in DECL.finditer(text):
        prop, val = d.group(1), d.group(2)
        if '#' not in val: continue
        def rep(m):
            h='#'+m.group(1).lower()
            if h==LIME: return lime_for(prop, dark)
            if hover_bg(prop,val,h): return '#831A57'
            return MAP.get(h, m.group(0))
        nv = HEX.sub(rep, val)
        if nv!=val:
            s=d.start(2); out.append(text[pos:s]); out.append(nv); pos=d.end(2)
    out.append(text[pos:]); text=''.join(out)
    # anything left outside a declaration (JS string colors like fill:'#01416e' handled above; bare literals here)
    def rep2(m):
        h='#'+m.group(1).lower()
        if h==LIME: return LIME_TEXT_ON_DARK if dark else LIME_FILL_ON_LIGHT
        return MAP.get(h, m.group(0))
    text = HEX.sub(rep2, text)
    text = re.sub(r'\x00BLOB(\d+)\x00', lambda m: blobs[int(m.group(1))], text)
    return text

if __name__=='__main__':
    root=sys.argv[1]
    for dp,_,fs in os.walk(root):
        if '.git' in dp or 'build_scripts' in dp: continue
        for f in fs:
            if f.endswith(('.html','.js','.webmanifest','.json')) and f!='manuals.json':
                p=os.path.join(dp,f); t=open(p,encoding='utf-8').read(); n=process(t,f)
                if n!=t: open(p,'w',encoding='utf-8').write(n); print('palette:',f)
