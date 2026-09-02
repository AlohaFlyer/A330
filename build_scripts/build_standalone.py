#!/usr/bin/env python3
"""
Build the offline standalone pages.

  python3 build_scripts/build_standalone.py

Reads each engine page, inlines the corresponding JSON between the
/* @@DATA_START <tag> */ and /* @@DATA_END */ markers as
`const <NAME> = <json>;` (compact JSON, ensure_ascii=False), and writes
dist/limitations.html, dist/memory-items.html and dist/fom-delta.html. The dist files are the
offline deliverables (they open from file://); the engine pages keep their
data external and load it with fetch(). The touch icon and the manifest the
pages link relatively are copied alongside. dist/ is generated, not committed.
"""
import hashlib, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES = [
    ("limitations.html", "limitations", "LIMITATIONS", "data/limitations.json"),
    ("memory-items.html", "memory-items", "MEMORY_ITEMS", "data/memory_items.json"),
    ("fom-delta.html", "fom-delta", "FOM_DELTA", "data/fom_delta.json"),
    ("oral-prep.html", "oral-prep", "ORAL_SCOPE", "data/oral_scope.json"),
]

def entry_count(data):
    # A bank is either a flat list of items or an object whose "areas"
    # (oral_scope.json) carry the items.
    if isinstance(data, dict) and isinstance(data.get("areas"), list):
        return len(data["areas"])
    return len(data)

def build(page, tag, const, json_rel):
    src = open(os.path.join(ROOT, page), encoding="utf-8").read()
    data = json.load(open(os.path.join(ROOT, json_rel), encoding="utf-8"))
    blob = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    for bad in ("</script", "<!--"):
        assert bad.lower() not in blob.lower(), "JSON would close the script block"
    start = "/* @@DATA_START %s */" % tag
    end = "/* @@DATA_END */"
    a = src.index(start) + len(start)
    b = src.index(end, a)
    n = entry_count(data)
    out = (src[:a] + "\n/* inlined by build_scripts/build_standalone.py from %s, %d entries; canonical copy is that file */\n"
           % (json_rel, n) + "const %s = %s;\n" % (const, blob) + src[b:])
    os.makedirs(os.path.join(ROOT, "dist"), exist_ok=True)
    dst = os.path.join(ROOT, "dist", page)
    open(dst, "w", encoding="utf-8").write(out)
    print("%s: %d entries from %s -> dist/%s (%d bytes)" % (page, n, json_rel, page, len(out.encode("utf-8"))))

# The pages link assets/icons/icon-180.png and site.webmanifest relatively; copy
# those two small files so a dist/ folder is self-consistent when moved.
SIDE_FILES = ["assets/icons/icon-180.png", "site.webmanifest"]

if __name__ == "__main__":
    for p in PAGES:
        build(*p)
    import shutil
    for rel in SIDE_FILES:
        dst = os.path.join(ROOT, "dist", rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copyfile(os.path.join(ROOT, rel), dst)
        print("copied", rel, "-> dist/" + rel)
