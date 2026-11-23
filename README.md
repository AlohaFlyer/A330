# A330 Study Portal (ha330pilot.app)

Started as a clone of the B787 study portal (as787pilot.app, being retired) in the Hawaiian
palette, with A330 data. Plan: `docs/A330_PORTAL_PLAN_v2.0.md`. B787 audit: `docs/B787_AUDIT_v2.40.md`.

## Update

The committed pages and `data/` are the source of truth. The pages started as a clone of the
B787 portal (frozen for provenance in `_engine/b787-v2.40/`, never served), but they are now
edited directly, so never re-clone over them.

```
bash build_scripts/update.sh                       # banks, stamps, handouts, offline manifest
A330_SRC=../src bash build_scripts/update.sh       # same, plus the manual-source verifiers
```

`update.sh` needs no B787 checkout. Do not run `project_data.py` on its own: it regenerates the
`*_drill.json` files from the source banks and drops hand-added drill items.
`build_scripts/legacy_clone_build.sh` is the old full clone build. It overwrites hand edits and
refuses to run without `--force-reclone`.

## Data

`data/limitations.json` and `data/memory_items.json` are the verified source banks (see
`docs/CROSSCHECK_2026-09-01.md`). `project_data.py` projects them into the engine shapes
(`*_drill.json`). Every record carries `src` (manual | sop | technique) and `fleet` (pax | frtr | both).
Manual revisions displayed anywhere come from `manuals.json` via `gen_labels.py`.
Manual PDFs and extracts never enter this repo.
