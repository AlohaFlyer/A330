# One-time generators (need the manual extracts)

These build the committed data banks from the verified sources. They are NOT part of build.sh
because they read the manual text extracts, which never enter the repo. Set `A330_SRC` to a folder
holding the extracts (A330P_FCOM_R17.md, A330P_FCOM_R17_PRO-NOR.md, A330P_QRH_R35.md, A330_FCTM_R6.md,
A330_PRC_2026-08-31.md, FOM_125.3.md, OE_Workbook.txt, the panel PDF) and run from the repo root:

- `gen_phase_flows.py` -> data/phase_flows.json (from data/flows.json, memory items, limitations)
- `gen_flows_trainer.py` -> data/flows_trainer.json (dot coordinates from img/layout.json)
- `build_cockpit_image.py` -> assets/a330_cockpit.jpg (from the A330 All Panels poster PDF)
- `build_oe.py` + `parse_wb.py` + `ans_part*.py` -> data/oe.json (from the Fleets OE Workbook)

Re-verify after any regeneration: `python3 build_scripts/verify_<bank>.py`.
