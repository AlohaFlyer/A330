# Push rules

Added 2026-09-25 after the 2026-09-24 incident: four connector pushes cut `data/phase_flows.json`
from 26 phases to 11 and dropped the normal checklists, NOTES, Memory Items, Limitations and SIM Notes.
Restored in fb317e0 (v5.0).

1. Never push `data/*.json`, `flows_quiz.html` or `index.html` through the GitHub MCP connector.
   It caps a file at about 70 KB and truncates or decodes content silently (base64, private-use glyphs).
   Push those files from the Pako NUC (`/tmp/gh/A330`, deploy key `hom-nuc`) or the Mac with git.
2. Before every commit that touches `data/`, run `python3 build_scripts/check_data_integrity.py`.
   It must print `data integrity: ok`. `build.sh` runs it too, and the `data-integrity` GitHub
   Action runs it on every push to `data/`.
3. After every push, compare the blob sha from GitHub (`git rev-parse HEAD:<path>` or the API)
   with `git hash-object` on the local file. Never trust raw.githubusercontent.com for this; it lags.
4. Floors in `check_data_integrity.py` are minimums. Raise them when content grows; lowering one
   needs Ryan's OK in the commit message.
