# A330 Study Portal (ha330pilot.app)

Exact clone of the B787 study portal (as787pilot.app, AlohaFlyer/B787) in the Hawaiian palette,
with A330 data. Plan: `docs/A330_PORTAL_PLAN_v2.0.md`. B787 audit: `docs/B787_AUDIT_v2.40.md`.

## Rebuild

```
git clone https://github.com/AlohaFlyer/B787 ../B787
bash build_scripts/build.sh ../B787
python3 build_scripts/build_handouts.py
python3 build_scripts/verify/parity_diff.py ../B787 .      # must print "parity failures: 0"
python3 build_scripts/verify/smoke.py . ../B787            # screenshots to docs/parity (gitignored)
```

Pages are generated from the B787 source plus `build_scripts/palette_map.py`, `apply_strings.py`
and the enumerated edits in `page_fixups.py` (allowlisted in `docs/PARITY_ALLOWLIST.md`).
Never hand-edit a page; change the map or the data and rebuild.

## Data

`data/limitations.json` and `data/memory_items.json` are the verified source banks (see
`docs/CROSSCHECK_2026-09-01.md`). `project_data.py` projects them into the engine shapes
(`*_drill.json`). Every record carries `src` (manual | sop | technique) and `fleet` (pax | frtr | both).
Manual revisions displayed anywhere come from `manuals.json` via `gen_labels.py`.
Manual PDFs and extracts never enter this repo.
