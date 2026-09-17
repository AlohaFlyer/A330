#!/bin/bash
# master_a330_ep.sh <N> <out.mp3>
#
# Masters one A330 Flight Deck Notes episode from the per-segment TTS folders.
# Same audio recipe as the B787 build (master_ep_fast.sh): 0.2s pad per segment,
# concat, atempo 1.2 + dynaudnorm on the body, intro/outro bumpers, loudnorm master.
#
# LAYOUT DIFFERENCE vs B787: the A330 segments live in a FLAT set of folders named
# ep<N>_seg<NN> under A330_podcast_build/, not nested under an ep<N>/ parent.
#   A330_podcast_build/ep1_seg01/tts_*.mp3
#   A330_podcast_build/ep1_seg02/tts_*.mp3
# Sorting is by -V on the folder name so seg02 < seg10 orders correctly.
#
# Usage:
#   ./master_a330_ep.sh 1 /tmp/flight-deck-notes-ep1.mp3
#   for n in 1 2 3 4; do ./master_a330_ep.sh $n /tmp/flight-deck-notes-ep$n.mp3; done
#
# Set SRC to the local Drive-synced "HA - Airbus A330" folder, and BUMPERS to
# wherever the shared music_test bumpers live (they were built for the B787 series
# and are reused unchanged here).

set -e

SRC="${SRC:-$HOME/My Drive (ryanpettit@gmail.com)/Claude - Alaska Airlines/HA - Airbus A330/A330_podcast_build}"
BUMPERS="${BUMPERS:-$HOME/My Drive (ryanpettit@gmail.com)/Claude - Alaska Airlines/AS - Boeing 787/music_test}"

EP="$1"; OUT="$2"
if [ -z "$EP" ] || [ -z "$OUT" ]; then
  echo "usage: $0 <episode-number> <output.mp3>" >&2
  exit 2
fi

INTRO="$BUMPERS/intro_v1.mp3"
OUTRO1="$BUMPERS/outro_v1_hook.mp3"
OUTRO2="$BUMPERS/outro_v2_ending.mp3"

for f in "$INTRO" "$OUTRO1" "$OUTRO2"; do
  [ -f "$f" ] || { echo "missing bumper: $f" >&2; exit 1; }
done

B="/tmp/a330_m_$EP"; rm -rf "$B"; mkdir -p "$B"

# bash 3.2 (stock macOS) has no mapfile, and BSD sort has no -V.
# Read into an array the portable way, and sort numerically on the seg number.
dirs=()
while IFS= read -r line; do
  [ -n "$line" ] && dirs+=("$line")
done < <(ls -d "$SRC/ep${EP}_seg"* 2>/dev/null \
         | sed 's/.*_seg\([0-9]*\)$/\1 &/' | sort -n -k1,1 | cut -d' ' -f2-)
if [ "${#dirs[@]}" -eq 0 ]; then
  echo "no segment folders matched $SRC/ep${EP}_seg*" >&2
  exit 1
fi
echo "ep$EP: ${#dirs[@]} segment folders"

: > "$B/list.txt"; idx=0; n=0; missing=0
for d in "${dirs[@]}"; do
  # newest tts_*.mp3 in the folder wins (re-generated segments supersede older takes)
  f=$(ls -t "$d"/tts_*.mp3 2>/dev/null | head -1)
  if [ -z "$f" ]; then
    echo "  WARN: no tts_*.mp3 in $(basename "$d")" >&2
    missing=$((missing+1)); continue
  fi
  idx=$((idx+1)); o=$(printf "%s/s%03d.wav" "$B" "$idx")
  echo "file '$o'" >> "$B/list.txt"
  ffmpeg -nostdin -v error -y -i "$f" \
    -af "aformat=sample_fmts=s16:sample_rates=44100:channel_layouts=mono,apad=pad_dur=0.2" "$o" &
  n=$((n+1)); (( n % 4 == 0 )) && wait
done
wait

echo "ep$EP: encoded $idx segments ($missing folders empty)"

ffmpeg -nostdin -v error -y -f concat -safe 0 -i "$B/list.txt" \
  -af "atempo=1.2,dynaudnorm" "$B/body.wav"

for pair in "INTRO:$INTRO" "OUTRO1:$OUTRO1" "OUTRO2:$OUTRO2"; do
  nm=${pair%%:*}; src=${pair#*:}
  ffmpeg -nostdin -v error -y -i "$src" \
    -af "aformat=sample_fmts=s16:sample_rates=44100:channel_layouts=mono" "$B/$nm.wav"
done

printf "file '%s'\n" "$B/INTRO.wav" "$B/body.wav" "$B/OUTRO1.wav" "$B/OUTRO2.wav" > "$B/final.txt"

ffmpeg -nostdin -v error -y -f concat -safe 0 -i "$B/final.txt" \
  -af "loudnorm=I=-16:TP=-1.5:LRA=11" -ar 44100 -ac 1 -b:a 96k "$OUT"

dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$OUT" | cut -d. -f1)
sz=$(du -h "$OUT" | cut -f1)
echo "ep$EP -> $OUT  (${dur}s, $sz)"
