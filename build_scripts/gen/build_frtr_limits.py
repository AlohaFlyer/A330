#!/usr/bin/env python3
"""
Build the fleet:"frtr" half of data/limitations_drill.json from the A330F FCOM.

Every freighter item's `ref` and `src` come ONLY from the A330F book. An item
that cannot be located there is emitted with confidence "UNVERIFIED" and a note
naming what still has to be checked - it never inherits a PAX quote, because
PAX facts come from A330P books and freighter facts from A330F books, never
cross-cited (docs/REVISION_PROCESS.md).
"""
import json, re, unicodedata
from pathlib import Path

HOME = Path.home(); REPO = HOME / "A330"
FRTR = HOME / ("My Drive (ryanpettit@gmail.com)/Claude - Alaska Airlines/"
               "HA - Airbus A330/extracts/A330F_FCOM_R10.md")

def norm(s):
    s = unicodedata.normalize("NFKC", s)
    for a, b in [("\u2010","-"),("\u2011","-"),("\u2013","-"),("\u2019","'"),("\u00a0"," ")]:
        s = s.replace(a, b)
    return re.sub(r"\s+", " ", s).strip()

raw = norm(FRTR.read_text(encoding="utf-8", errors="replace"))
bank = json.loads((REPO / "data" / "limitations_drill.json").read_text())
pax = [b for b in bank if b.get("fleet") == "pax"]

DOTS = re.compile(r"\.{4,}")
# Items whose source is the AFM / PRC, not the FCOM. The A330F AFM is not
# extracted, so these cannot be sourced from the freighter book at all.
AFM_SOURCED = {"lim-afm-01","lim-afm-02","lim-afm-03","lim-afm-04","lim-afm-05","lim-afm-06"}
# Hand probes for items the generic matcher cannot key on.
PROBE = {
 "lim-spd-03":"1 240 HOLDING","lim-spd-04":"1+F 215 TAKEOFF","lim-spd-06":"2 196 TAKEOFF/APPROACH",
 "lim-spd-07":"3 3 186 TAKEOFF/APPR/LDG","lim-spd-08":"FULL FULL 180 LANDING",
 "lim-spd-02":"VMO / MMO CRUISE","lim-afs-13":"RNP accuracy with GPS PRIMARY",
 "lim-afs-27":"Headwind:","lim-afs-28":"Tailwind :","lim-eng-03":"On ground 700",
 "lim-eng-04":"In flight 850","lim-eng-21":"Selection of TOGA thrust is not permitted",
 "lim-oxy-01":"REF Temperature","lim-oxy-04":"Protection against smoke with 100",
 "lim-afs-08":"LPV approach",
}

def label_of(src):
    m = DOTS.search(src)
    if not m: return None
    head = re.sub(r".*?\]\s*", "", src[:m.start()])
    w = head.split()
    return " ".join(w[-8:]) if w else None

def ident_near(pos):
    seg = raw[max(0, pos-4000):pos]
    ids = re.findall(r"Ident\.:\s*([A-Z0-9\-\._]+)", seg)
    return ids[-1] if ids else None

def sentence_at(pos, span=340):
    s = raw[pos:pos+span]
    cut = s.rfind(". ")
    return (s[:cut+1] if cut > 80 else s).strip()

def value_after(pos, probe):
    tail = raw[pos+len(probe):pos+len(probe)+160]
    tail = DOTS.sub(" ", tail)
    m = re.match(r"[\s.]*([^A-Z\[]{1,60})", tail)
    return norm(m.group(1)) if m else None


# --- hand-verified overrides -------------------------------------------------
# Each was re-read directly in the A330F FCOM extract. Where the freighter value
# is identical to PAX the parser had grabbed an adjacent line, not a difference.
SAME_AS_PAX = {
    "lim-afs-20": "freighter text reads 'disengaged no later than at 80 ft AGL', same as PAX; parser had grabbed the decision-height line",
    "lim-afs-22": "freighter text reads 'disengaged no later than at 80 ft AGL', same as PAX; parser had grabbed the decision-height line",
    "lim-lg-02":  "freighter reads 'Maximum brake temperature for takeoff (brake fans off) 300 °C', same as PAX",
    "lim-spd-01": "freighter COCKPIT WINDOW OPEN MAXIMUM SPEED is 230 kt, same as PAX; parser had matched a table-of-contents line",
}

out, report = [], []
for it in pax:
    src = re.sub(r"\s*\[[^\]]*\]\s*$", "", norm(it["src"]))
    fid = it["id"] + "-f"
    base = {k: it[k] for k in ("s","q","mem")}
    base["id"] = fid; base["fleet"] = "frtr"; base["provenance"] = "manual"

    if it["id"] in AFM_SOURCED:
        base.update(a=it["a"], ref="A330F AFM (not extracted)",
            src="NOT LOCATED in A330F FCOM R10. This limitation is AFM-sourced; "
                "the A330 Freighter AFM has not been extracted, so the freighter "
                "value is unconfirmed. The value shown is the PAX figure and must "
                "be verified against the freighter AFM before it is relied on.",
            confidence="UNVERIFIED")
        out.append(base); report.append((fid,"AFM-NOT-EXTRACTED",it["a"],"-")); continue

    probe = PROBE.get(it["id"]) or label_of(src)
    pos = raw.find(probe) if probe else -1
    if pos < 0:
        for n in (14,11,8,6):
            w = src.split()
            if len(w) < n: continue
            probe = " ".join(w[:n]); pos = raw.find(probe)
            if pos >= 0: break
    if pos < 0:
        base.update(a=it["a"], ref="A330F FCOM R10 (not located)",
            src="NOT LOCATED in the A330F FCOM R10 extract. Value shown is the PAX "
                "figure and is unconfirmed for the freighter. Verify in the "
                "freighter book before relying on it.",
            confidence="UNVERIFIED")
        out.append(base); report.append((fid,"NOT-FOUND",it["a"],"-")); continue

    ident = ident_near(pos); quote = sentence_at(pos)
    fval = value_after(pos, probe) if DOTS.search(src) else None
    pval = it["a"]
    differs = bool(fval) and norm(fval).rstrip(".") not in norm(pval) and norm(pval) not in norm(fval)
    if it["id"] in SAME_AS_PAX:
        differs = False
    base.update(
        a=(fval if differs and fval else pval),
        ref=("A330F FCOM " + ident.split("-0")[0]) if ident else "A330F FCOM R10",
        src=f"{quote} [{ident or 'A330F FCOM R10'}]",
        confidence=it.get("confidence","VERIFIED"))
    out.append(base)
    report.append((fid, "DIFF" if differs else "same", pval, fval or ""))

json.dump(out, open(REPO/"build_scripts/gen/frtr_items.json","w"), indent=1, ensure_ascii=False)
from collections import Counter
print(Counter(r[1] for r in report))
print("\n--- value DIFFERENCES (freighter vs pax) ---")
for fid,st,p,f in report:
    if st=="DIFF": print(f"{fid:18s} pax={p[:44]:46s} frtr={f[:44]}")
print("\n--- unverified ---")
for fid,st,p,f in report:
    if st in ("AFM-NOT-EXTRACTED","NOT-FOUND"): print(f"{fid:18s} {st}")
