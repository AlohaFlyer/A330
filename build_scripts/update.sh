#!/usr/bin/env bash
# Safe A330 update: regenerates banks, stamps, handouts and the offline manifest from the
# committed pages and data. Needs no B787 checkout. Never re-clones or re-transforms pages.
# Optional: A330_SRC=<manual extracts dir> also runs the source verifiers.
set -euo pipefail; cd "$(dirname "$0")/.."
python3 build_scripts/build_triggers.py
python3 build_scripts/build_weather_bank.py
python3 build_scripts/gen_index.py
python3 build_scripts/stamp_versions.py
python3 build_scripts/build_corpus.py
python3 build_scripts/lb_only.py >/dev/null
python3 build_scripts/lb_only.py --check >/dev/null || { echo 'VERIFY FAIL: kg left (lb_only)'; exit 1; }
python3 build_scripts/build_handouts.py
python3 build_scripts/build_weather_handout.py
python3 build_scripts/build_mcdu_handout.py
python3 build_scripts/build_oe_pdf.py
python3 build_scripts/check_data_integrity.py >/dev/null || { echo 'VERIFY FAIL: data integrity'; exit 1; }
SRC="${A330_SRC:-../src}"
if [ -d "$SRC" ]; then
  python3 build_scripts/build_manuals_index.py >/dev/null && python3 build_scripts/verify_manuals.py >/dev/null || { echo 'VERIFY FAIL: manuals'; exit 1; }
  for v in triggers weather mcdu oe fom phase_flows flows_trainer; do python3 build_scripts/verify_$v.py >/dev/null || { echo "VERIFY FAIL: $v"; exit 1; }; done
else echo "source verifiers skipped: no manual extracts at $SRC"; fi
python3 build_scripts/build_offline_manifest.py
echo UPDATE OK
