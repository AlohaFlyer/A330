#!/usr/bin/env python3
"""
Build data/memory_items_v3.json from memory_items_v2.json + PASS1_fixes.json.

  python3 build_scripts/apply_pass1_memory_fixes.py

1. Apply every PASS1 correction (each fix names id, field, index and the
   exact `current` string, which must match before it is replaced).
2. A corrected string containing "\\n" becomes two consecutive elements.
3. Insert the box-break sentinel "" where the rendered page shows SEPARATE
   boxes (grouping read from the pages by the coordinator, 2026-09-01).
   "" is never graded and never counted; the renderer starts a new box.
4. Write /home/claude/a330/data/memory_items_v3.json and copy it to
   repo/data/memory_items.json (the canonical copy the page embeds).
"""
import json, shutil, sys

DATA = "/home/claude/a330/data"
REPO_DATA = "/home/claude/a330/repo/data"

src = json.load(open(f"{DATA}/memory_items_v2.json", encoding="utf-8"))
fixes = json.load(open(f"{DATA}/PASS1_fixes.json", encoding="utf-8"))
by_id = {e["id"]: e for e in src}

# 1 + 2: apply fixes, highest index first so earlier indices stay valid
from collections import defaultdict
per_id = defaultdict(list)
for f in fixes:
    per_id[f["id"]].append(f)
applied = 0
for pid, fl in per_id.items():
    e = by_id[pid]
    for f in sorted(fl, key=lambda x: -x["index"]):
        assert f["field"] == "actions"
        cur = e["actions"][f["index"]]
        assert cur == f["current"], (pid, f["index"], cur)
        e["actions"][f["index"]:f["index"] + 1] = f["corrected"].split("\n")
        applied += 1
print(f"applied {applied} PASS1 fixes")

# 3: box breaks. Each entry: id -> list of lines AFTER which a break "" goes.
BREAK_AFTER = {
    "mi-vis-06": ["REV ... MAX", "BRAKE PEDALS ... RELEASE", "A/SKID OFF ... ORDER"],
    "mi-vis-07": ["PITCH ... PULL UP", "BANK ... WINGS LEVEL or ADJUST"],
    "mi-vis-08": ["PITCH ... PULL UP", "BANK ... WINGS LEVEL or ADJUST"],
    "mi-vis-10": ["BOTH FDs ... OFF", "GO-AROUND ... PERFORM", "VERTICAL SPEED ... MONITOR",
                  "LATERAL AND VERTICAL GUIDANCE ... ADJUST"],
    "mi-vis-11": ["SRS ORDERS ... FOLLOW@2",   # the second occurrence (airborne block)
                  "DO NOT CHANGE CONFIGURATION (SLATS/FLAPS, GEAR) UNTIL OUT OF WINDSHEAR."],
}
for pid, marks in BREAK_AFTER.items():
    e = by_id[pid]
    for m in marks:
        text, _, occ = m.partition("@")
        occ = int(occ or 1)
        hits = [i for i, t in enumerate(e["actions"]) if t == text]
        assert len(hits) >= occ, (pid, m, hits)
        i = hits[occ - 1]
        assert e["actions"][i + 1] != "", (pid, m)
        e["actions"].insert(i + 1, "")
    # a break must sit between two boxed lines, never next to a header or at the ends
    a = e["actions"]
    for i, t in enumerate(a):
        if t == "":
            assert 0 < i < len(a) - 1 and a[i - 1] != "" and a[i + 1] != "", (pid, i)
            assert not a[i - 1].endswith(":") and not a[i + 1].endswith(":"), (pid, i)

for e in src:
    e.setdefault("audit", []).append({
        "pass": "PASS1 2026-09-01",
        "note": "actions re-read against the rendered page; quoted alert-name lines are unboxed headers; \"\" marks a box break",
    }) if e["id"] in per_id or e["id"] in BREAK_AFTER else None

out = f"{DATA}/memory_items_v3.json"
json.dump(src, open(out, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
open(out, "a", encoding="utf-8").write("\n")
shutil.copyfile(out, f"{REPO_DATA}/memory_items.json")
print("wrote", out, "and copied to", f"{REPO_DATA}/memory_items.json")
for e in src:
    n_hdr = sum(1 for t in e["actions"] if t and (t.endswith(":") or (t[0] in "\"“'‘" and " ... " not in t)))
    n_brk = sum(1 for t in e["actions"] if t == "")
    print(f"  {e['id']:<10} {len(e['actions']):>2} elements, {n_hdr} headers, {n_brk} breaks, {len(e['actions']) - n_hdr - n_brk} boxed lines")
