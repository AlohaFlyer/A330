# One-time generators (need the manual extracts)

These build the committed data banks from the verified sources. They are NOT part of build.sh
because they read the manual text extracts, which never enter the repo. Set `A330_SRC` to a folder
holding the extracts (A330P_FCOM_R17.md, A330P_FCOM_R17_PRO-NOR.md, A330P_QRH_R35.md, A330_FCTM_R6.md,
A330_PRC_2026-08-31.md, FOM_125.3.md, OE_Workbook.txt, the panel PDF) and run from the repo root:

- `gen_phase_flows.py`, `gen_flows_trainer.py`, `spine_cockpit_prep.py`, `resection_cockpit_prep.py`:
  RETIRED 2026-09-25 (v5.0). data/phase_flows.json and data/flows_trainer.json are now the source of
  truth and are edited directly; the scripts refuse to run without `--force-regenerate` because a
  rerun reverts every hand edit since v4.x. Manual revision workflow for the two flow banks: point
  `A330_SRC` at the new extracts, run `verify_flows_trainer.py`, `verify_phase_flows.py` and
  `verify_spine_sync.py`, and fix each flagged quote in the data file by hand (the verifiers name the
  item and the missing line). Then `check_data_integrity.py` and push per docs/PUSH_RULES.md.
- `build_cockpit_image.py` -> assets/a330_cockpit.jpg (from the A330 All Panels poster PDF)
- `build_oe.py` + `parse_wb.py` + `ans_part*.py` -> data/oe.json (from the Fleets OE Workbook)

Re-verify after any regeneration: `python3 build_scripts/verify_<bank>.py`.
