#!/usr/bin/env python3
"""Prove the inlined data blocks equal their canonical JSON, item for item.
   python3 build_scripts/verify/check_embedded_data.py   (run from the repo root)"""
import json, re, sys
DATA = "/home/claude/a330/data"

def block(html, name):
    m = re.search(r"/\* BEGIN data/%s\.json \*/\nconst \w+ =\n(.*?);\n/\* END data/%s\.json \*/" % (name, name), html, re.S)
    assert m, "markers for %s not found" % name
    return json.loads(m.group(1))

# memory items
html = open("memory-items.html", encoding="utf-8").read()
emb = block(html, "memory_items")
src = json.load(open(f"{DATA}/memory_items_v3.json", encoding="utf-8"))
canon = json.load(open("data/memory_items.json", encoding="utf-8"))
assert len(emb) == 11 and [e["id"] for e in emb] == [e["id"] for e in src]
for e, s in zip(emb, src):
    assert e["actions"] == s["actions"], "actions differ for " + e["id"]
    assert e == s, "entry differs for " + e["id"]
assert canon == src
print(f"memory-items.html: {len(emb)} entries embedded; every entry == memory_items_v3.json; repo data/memory_items.json == v3: True")
v2 = json.load(open(f"{DATA}/memory_items_v2.json", encoding="utf-8"))
changed = [e["id"] for e, o in zip(src, v2) if e["actions"] != o["actions"]]
breaks = sum(e["actions"].count("") for e in src)
print(f"  v2 -> v3: actions changed on {changed}; {breaks} box-break sentinels")
for e in src:
    for t in e["actions"]:
        assert "\n" not in t, "unsplit newline in " + e["id"]
print("  no embedded newlines remain in any action line")

# limitations
html = open("limitations.html", encoding="utf-8").read()
emb = block(html, "limitations")
src = json.load(open(f"{DATA}/limitations_v3.json", encoding="utf-8"))
assert len(emb) == 160 and [e["id"] for e in emb] == [e["id"] for e in src]
for e, s in zip(emb, src):
    assert e == s, "item differs for " + e["id"]
from collections import Counter
c = Counter(i["confidence"] for i in emb)
print(f"limitations.html: {len(emb)} items embedded; every item == limitations_v3.json; {c['VERIFIED']} VERIFIED / {c['UNCLEAR']} UNCLEAR")
print(f"  refs with backslash-underscore: {sum(chr(92)+'_' in i['ref'] for i in emb)}; items with corroboration: {sum('corroboration' in i for i in emb)}; with audit: {sum('audit' in i for i in emb)}")
