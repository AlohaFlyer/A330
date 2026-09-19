#!/usr/bin/env python3
"""parse_a330_ep.py <script.md> <epN>

Parses a 330 Flight Deck Notes script into A330_podcast_build/ep<N>_manifest.json.
Pronunciation is .pls-derived (the B787 flight-deck-notes.pls is the shared
single source of truth) plus an A330/Airbus addition table below.
Matching is CASE-SENSITIVE and longest-first, so lowercase words are never hit.
Hosts never voice a pronunciation aloud - correct sound comes only from spelling
it phonetically in the hidden API text. Clean script files keep proper spelling.
"""
import json, os, re, sys

ROOT = os.path.expanduser("~/mnt/Claude - Alaska Airlines")
PLS  = os.path.join(ROOT, "AS - Boeing 787", "flight-deck-notes.pls")
BUILD= os.path.join(ROOT, "HA - Airbus A330", "A330_podcast_build")

VOICES = {
    "Pualani": ("cgSgspJ2msm6clMCkdW9", "Jessica - Playful, Bright, Warm"),
    "Chester": ("nPczCjzI2devNBz1zQrb", "Brian - Deep, Resonant and Comforting"),
    "Otto":    ("jOEnNSVLOHUgmrNwfqQE", "John - New Zealand, Cheerful, and Bright"),
}

# Applied BEFORE the .pls, for forms the .pls omits or where A330 differs.
LOCKED = [
    ("A330", "ay three thirty"), ("330", "three thirty"), ("787", "seven-eight-seven"),
    ("FCOM", "eff com"), ("FCTM", "eff see tee em"), ("FOM", "eff oh em"),
    ("ADIRS", "ay dirs"), ("ECAM", "ee cam"), ("EFIS", "ee fiss"), ("ISIS", "eye siss"),
    ("MCDU", "em see dee you"), ("FCU", "eff see you"), ("RMP", "are em pee"),
    ("PWS", "pee dubya ess"), ("DMC", "dee em see"), ("OEB", "oh ee bee"),
    ("STS", "ess tee ess"), ("EFOB", "ee eff oh bee"), ("FOB", "eff oh bee"),
    ("CFP", "see eff pee"), ("PDC", "pee dee see"), ("DCL", "dee see el"),
    ("X-BLEED", "cross bleed"), ("CSTR", "constraints"),
    ("SEC F-PLN", "seck eff plan"), ("F-PLN", "eff plan"),
    ("INIT A", "init ay"), ("INIT B", "init bee"),
    ("RAD NAV", "rad nav"), ("TRANS ALT", "trans alt"),
    ("CM1", "see em one"), ("CM2", "see em two"),
    ("ADS", "ay dee ess"), ("ADF", "ay dee eff"),
    ("A-DIFSRIPP", "ay DIF-srip"), ("DIFSRIPP", "DIF-srip"), ("DIFRIP", "DIF-rip"),
    ("LEAP", "leap"),
    ("APU", "ay pee you"), ("ATIS", "ay tiss"), ("ACARS", "ay cars"),
    ("L/G", "landing gear"), ("W/W", "double-u double-u"),
]

def load_pls(path):
    if not os.path.exists(path): return []
    t = open(path).read()
    return re.findall(r"<grapheme>(.*?)</grapheme>\s*<alias>(.*?)</alias>", t, re.S)

def build_subs():
    subs = [(g.strip(), a.strip()) for g, a in load_pls(PLS)]
    seen = {g for g, _ in LOCKED}
    merged = list(LOCKED) + [(g, a) for g, a in subs if g not in seen]
    merged.sort(key=lambda p: -len(p[0]))          # longest-first
    return merged

SUBS = build_subs()

def phon(text):
    out = text
    for g, a in SUBS:
        if g in out:
            out = out.replace(g, a)
    return out

def parse(md_path):
    segs = []
    for line in open(md_path):
        m = re.match(r"^\*\*(Pualani|Chester|Otto):\*\*\s*(.+)$", line.strip())
        if not m: continue
        who, text = m.group(1), m.group(2).strip()
        vid, vname = VOICES[who]
        segs.append({"i": len(segs) + 1, "speaker": who, "voice_id": vid,
                     "voice_name": vname, "clean": text, "text": phon(text)})
    return segs

def main():
    md, ep = sys.argv[1], sys.argv[2]
    segs = parse(md)
    os.makedirs(BUILD, exist_ok=True)
    out = os.path.join(BUILD, "%s_manifest.json" % ep)
    json.dump({"episode": ep, "source_script": os.path.basename(md),
               "model": "eleven_v3", "output_format": "mp3_44100_192",
               "settings": {"stability": 0.5, "similarity_boost": 0.75, "style": 0.18},
               "segments": segs}, open(out, "w"), indent=1)
    chars = sum(len(s["text"]) for s in segs)
    print("%s: %d segments, %d TTS chars -> %s" % (ep, len(segs), chars, out))
    for s in segs[:3]:
        print("  %02d %-8s %s" % (s["i"], s["speaker"], s["text"][:90]))

if __name__ == "__main__":
    main()
