#!/usr/bin/env bash
# Rebuild the whole ha330pilot.app tree from the B787 source checkout + A330 data.
# Usage: build.sh <path-to-B787-checkout>   (run from the A330 repo root)
set -euo pipefail
B787="${1:?path to B787 checkout}"; cd "$(dirname "$0")/.."
rm -f ./*.html portal-settings.js assist.js sw.js site.webmanifest robots.txt
cp "$B787"/*.html . && mv cdu_preflight.html mcdu_preflight.html
cp "$B787"/portal-settings.js "$B787"/assist.js "$B787"/sw.js "$B787"/site.webmanifest "$B787"/robots.txt .
python3 build_scripts/apply_palette.py . >/dev/null
python3 build_scripts/apply_strings.py . >/dev/null
python3 build_scripts/page_mcdu_preflight.py
python3 build_scripts/page_phase_flows.py
python3 build_scripts/page_flows_quiz.py
python3 build_scripts/project_data.py
python3 build_scripts/build_triggers.py
python3 build_scripts/build_weather_bank.py
python3 build_scripts/build_fom_bank.py
python3 build_scripts/externalize.py limitations.html DATA data/limitations_drill.json
python3 build_scripts/externalize.py memory-items.html DATA data/memory_items_drill.json
python3 build_scripts/externalize.py hot-seat.html DATA data/memory_items_drill.json SCN data/hot_seat_scenarios.json
python3 build_scripts/externalize.py limit-or-bust.html NUM data/limit_or_bust_num.json BOOL data/limit_or_bust_bool.json
python3 build_scripts/externalize.py triggers.html DATA data/triggers.json
python3 build_scripts/externalize.py weather.html DATA data/weather.json
python3 build_scripts/externalize.py systems_quiz.html QUESTIONS data/systems.json FCOM_DETAIL data/systems_fcom_detail.json SOURCE_DETAIL data/systems_source_detail.json
python3 build_scripts/externalize.py jeopardy.html POOL data/jeopardy_pool.json
python3 build_scripts/externalize.py podcast.html EPISODES data/episodes.json
sed -i 's|fetch("ioe_questions.json").catch(()=>caches.match("ioe_questions.json"))|fetch("data/oe.json").catch(()=>caches.match("data/oe.json"))|' ioe.html
sed -i "s|fetch('fom_questions.json',{cache:'no-store'})|fetch('data/fom_questions.json',{cache:'no-store'})|" fom_quiz.html
python3 build_scripts/page_fixups.py
python3 build_scripts/gen_labels.py
python3 build_scripts/gen_index.py
python3 build_scripts/build_stubs.py
python3 build_scripts/stamp_versions.py
python3 build_scripts/build_corpus.py
python3 build_scripts/build_handouts.py
python3 build_scripts/build_weather_handout.py
python3 build_scripts/build_mcdu_handout.py
python3 build_scripts/build_oe_pdf.py
for v in triggers weather mcdu oe fom phase_flows flows_trainer; do python3 build_scripts/verify_$v.py >/dev/null || { echo "VERIFY FAIL: $v"; exit 1; }; done
python3 build_scripts/build_offline_manifest.py
echo BUILD OK
