#!/bin/bash
# publish_a330_podcast.sh [ep ...]
#
# One-command publish for the A330 Flight Deck Notes podcast.
#   1. Masters each episode from its per-segment TTS folders (master_a330_ep.sh)
#   2. Measures real duration + byte size from the finished mp3
#   3. Regenerates data/episodes.json with those measured values
#   4. Leaves the mp3s and episodes.json in the repo working tree, staged-ready
#
# It does NOT commit or push - review, then commit. Audio files are large, so
# push them in batches if using the GitHub web uploader (~25MB/commit cap).
#
# Usage (from the root of a local clone of AlohaFlyer/A330):
#   ./build_scripts/publish_a330_podcast.sh            # all four episodes
#   ./build_scripts/publish_a330_podcast.sh 4          # just ep4
#
# NOTE ON EP1-3: the mp3s currently live on main were built from the OLD scripts
# (with [pause] markers, kilogram weights, and "ay-tiss" for ATIS). This script
# OVERWRITES them with the corrected v2 audio. That replacement is intended.

set -e

HERE="$(cd "$(dirname "$0")" && pwd)"
REPO="$(cd "$HERE/.." && pwd)"
MASTER="$HERE/master_a330_ep.sh"

[ -x "$MASTER" ] || chmod +x "$MASTER"

EPS=("$@")
if [ "${#EPS[@]}" -eq 0 ]; then EPS=(1 2 3 4 5 6 7); fi

for n in "${EPS[@]}"; do
  out="$REPO/flight-deck-notes-ep${n}.mp3"
  echo "=== mastering ep$n ==="
  "$MASTER" "$n" "$out"
done

echo
echo "=== regenerating data/episodes.json ==="

python3 - "$REPO" "${EPS[@]}" << 'PY'
import json, os, subprocess, sys

repo = sys.argv[1]
eps  = [int(x) for x in sys.argv[2:]]

META = {
  1: ("Review", "Limitations - The Numbers That Bite",
      "Speeds, weights, wind, engines, APU, autoflight, fuel and icing limits - FCOM R17 LIM chapter, AFM",
      "limitations.html"),
  2: ("Review", "Memory Items - Boxed and Cold",
      "Emergency descent, stall recovery, stall warning at liftoff, unreliable speed, loss of braking, TAWS, TCAS RA, reactive windshear - FCOM R17 PRO-ABN, QRH R35",
      "memory-items.html"),
  3: ("Chair-Fly", "Chair-Fly 1 - Preflight to Before Start",
      "Triggers, flows and checklists from the safety exterior inspection through the Before Start checklist - FCOM R17 PRO-NOR-SOP-03 to SOP-07, NPC card book, FCTM PR-NP-CL",
      "phase_flows.html"),
  4: ("Review", "Limitations - Freighter Numbers",
      "Speeds, weights, wind, engines, APU, autoflight, fuel and icing limits for the freighter - A330 Freighter FCOM R10 LIM chapter",
      "limitations.html"),
  5: ("Flows", "Preliminary Cockpit Prep - CM2 as PF",
      "Four gates, the eight-station spiral and A-DIFSRIPP, from sitting down through the Cockpit Preparation checklist, flown from the right seat as PF. Gate grouping here predates Ep7; Ep7 has the current card-order version - FCOM R17 PRO-NOR-SOP-04/05/06, NPC-CB Cockpit Preparation card, FCTM PR-NP-CL",
      "phase_flows.html"),
  6: ("Flows", "Preliminary Cockpit Prep - CM2 as PM",
      "Same flow from the monitoring seat: the two questions of Before Walkaround, the exterior split, and the eight-item FMS crosscheck through the Cockpit Preparation checklist. Gate grouping here predates Ep7; Ep7 has the current card-order version - FCOM R17 PRO-NOR-SOP-04/05/06, NPC-CB Cockpit Preparation card, FCTM PR-NP-CL",
      "phase_flows.html"),
  7: ("Flows", "Preliminary Cockpit Prep - One Spine, Two Roles",
      "Why CM2 runs one fifteen-item flow, not two: the four gates re-cut into card order, the two-item PF tail, Before Walkaround as an all-PM block, the wording traps and the branch-point drill - FCOM R17 PRO-NOR-SOP-04, NPC-CB Cockpit Preparation card",
      "phase_flows.html"),
}

path = os.path.join(repo, "data", "episodes.json")
existing = []
if os.path.exists(path):
    with open(path) as f:
        existing = json.load(f)
by_n = {e["n"]: e for e in existing}

for n in eps:
    audio = "flight-deck-notes-ep%d.mp3" % n
    full  = os.path.join(repo, audio)
    if not os.path.exists(full):
        print("  skip ep%d (no mp3)" % n)
        continue
    dur = float(subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "csv=p=0", full]).decode().strip())
    mins, secs = divmod(int(round(dur)), 60)
    group, title, topic, quiz = META[n]
    by_n[n] = {
        "n": n, "group": group, "title": title, "topic": topic,
        "len": "%d:%02d" % (mins, secs),
        "audio": audio, "quiz": quiz,
        "bytes": os.path.getsize(full),
    }
    print("  ep%d  %d:%02d  %s bytes" % (n, mins, secs, f"{os.path.getsize(full):,}"))

out = [by_n[k] for k in sorted(by_n)]
os.makedirs(os.path.dirname(path), exist_ok=True)
with open(path, "w") as f:
    json.dump(out, f, separators=(",", ":"))
    f.write("\n")
print("wrote %s (%d episodes)" % (path, len(out)))
PY

echo
echo "=== done ==="
echo "Review, then commit:"
echo "  git -C '$REPO' add data/episodes.json flight-deck-notes-ep*.mp3"
echo "  git -C '$REPO' commit -m 'Rebuild podcast ep1-3 from corrected scripts, add ep4 freighter limitations'"
echo
echo "Also bump podcast.html in versions.json (it is currently 1.6)."
