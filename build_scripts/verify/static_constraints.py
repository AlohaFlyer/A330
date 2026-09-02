#!/usr/bin/env python3
"""Static constraints on the engine pages and the dist builds. Run from the repo root."""
import re, sys, os
files = ["limitations.html", "memory-items.html", "fom-delta.html", "oral-prep.html", "dist/limitations.html", "dist/memory-items.html", "dist/fom-delta.html", "dist/oral-prep.html"]
bad = 0
for f in files:
    s = open(f, encoding="utf-8").read(); b = s.encode("utf-8")
    scripts = "\n".join(re.findall(r"<script>(.*?)</script>", s, re.S))
    checks = {
        "em dash": s.count("—"),
        "&mdash;": s.count("&mdash;"),
        "localStorage/sessionStorage": len(re.findall(r"localStorage|sessionStorage", s)),
        "private-use chars": sum(1 for c in s if 0xE000 <= ord(c) <= 0xF8FF or 0xF0000 <= ord(c) <= 0x10FFFD),
        "backslash-u / backslash-x in JS": len(re.findall(r"\\[ux][0-9A-Fa-f]", scripts)),
        "external src/href (http, https, protocol-relative)": len(re.findall(r"""(?:src|href)=["'](?:https?:)?//""", s)),
        "fetch calls other than the relative data fetch": len([m for m in re.findall(r"fetch\(([^)]*)\)", scripts) if not m.startswith('"data/')]),
        "raw hex outside the palette block (comments ignored)": len([l for l in s.split("</style>")[0].splitlines()[120:] if re.search(r"#[0-9A-Fa-f]{6}\b", re.sub(r"/\*.*?\*/", "", l))]),
    }
    size_ok = True if f.startswith("dist/") else len(b) < 100000
    line = ", ".join(f"{k}={v}" for k, v in checks.items())
    ok = all(v == 0 for v in checks.values()) and size_ok
    bad += not ok
    print(f"{f}: {len(b)} bytes{'' if f.startswith('dist/') else ' (engine, must be < 100000: ' + str(size_ok) + ')'}; {line} -> {'PASS' if ok else 'FAIL'}")
print("STATIC CONSTRAINTS:", "ALL PASSED" if not bad else f"{bad} FAILED"); sys.exit(1 if bad else 0)
