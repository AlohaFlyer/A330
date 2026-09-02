# Build Notes

Record of the scaffolding build and the tooling test run. Written 2026-09-01.

Everything below was actually executed with `python3` 3.11.15 from the repo
root. This is a transcript, not a plan.

## Test fixture

A throwaway bank, `data/_sample.json`, with three items, plus a throwaway page,
`_sample_page.html`, to exercise the HTML side of the index. Both were deleted
after the run. Fixture design:

| Item | `src` | `fleet` | `ref` | Purpose |
| --- | --- | --- | --- | --- |
| `LIM-HYD-001` | manual | pax | `["A330P FCOM 5.4.1", "A330P FCOM 5.4.2"]` | Valid. Two sibling sections, to test prefix matching. Answer fully supported by its `verbatim`. |
| `SOP-TAXI-002` | sop | both | `FOM 12.3` | Valid. Non-manual `src`, so grounding must skip it while the index still picks up its ref. |
| `LIM-ELEC-003` | manual | pax | *(absent)* | Deliberately bad. `src: "manual"` with no `ref`, the R3 violation. |

The page cited `A330P QRH R35 ABN-17`, `A330P FCOM 5.41` (the negative case for
prefix matching), `A330 FCTM PR-NP-SOP-160`, and one line of prose reading "the
MEL requires a placard for this item" to confirm prose is not mistaken for a
citation.

---

## Test 1: provenance_lint.py catches the bad item

```
$ python3 build_scripts/provenance_lint.py
FAIL data/_sample.json  (1 of 3 items)
  item: LIM-ELEC-003
    at: items[2]
    - R3 src is 'manual' but 'ref' is missing or empty; a manual fact must cite the manual section it came from


provenance lint: 3 items across 1 file; 1 error in 1 file.
EXIT=1
```

Correct. Exit 1, exactly one item named, the two valid items silent. The
`_meta` block was correctly not counted as an item (3 items found, not 4).

## Test 2: citation_index.py covers JSON banks as well as HTML

```
$ python3 build_scripts/citation_index.py
scanned 1 JSON data banks and 1 HTML pages
indexed 6 citations across 4 manuals
wrote docs/CITATION_INDEX.md
wrote docs/citation_index.json
EXIT=0
```

Index contents:

| Manual | Section | Source file | Item id | Kind |
| --- | --- | --- | --- | --- |
| A330P_FCOM | 5.4.1 | `data/_sample.json` | LIM-HYD-001 | json |
| A330P_FCOM | 5.4.2 | `data/_sample.json` | LIM-HYD-001 | json |
| A330P_FCOM | 5.41 | `_sample_page.html` | fcom-hyd-detail | html |
| A330P_QRH | ABN-17 | `_sample_page.html` | qrh-abnormals | html |
| A330_FCTM | PR-NP-SOP-160 | `_sample_page.html` | fcom-hyd-detail | html |
| FOM | 12.3 | `data/_sample.json` | SOP-TAXI-002 | json |

Four things confirmed here:

1. **JSON banks are covered.** Three of the six citations came from
   `data/_sample.json`. This is the predecessor's known gap and it is closed.
2. Refs given as a **list** were expanded to one entry each.
3. Loose spellings resolved to canonical codes: `A330P FCOM` to `A330P_FCOM`,
   `A330 FCTM` to `A330_FCTM`. Revision tokens (`R35`) were consumed and not
   mistaken for the section.
4. The prose line "the MEL requires a placard" was **not** indexed. See the
   patch note below.

## Test 3: manual_diff.py prefix matching

```
$ python3 build_scripts/manual_diff.py A330P_FCOM 5.4
RE-VERIFY CHECKLIST
manual         : A330P_FCOM
changed sections: 5.4
index generated : 2026-09-01 05:28:20

data/_sample.json  (2 items)
  [ ] LIM-HYD-001                  5.4.1          A330P FCOM 5.4.1
  [ ] LIM-HYD-001                  5.4.2          A330P FCOM 5.4.2

TOTAL: 2 citations, 1 item, 1 file.
Re-verify each against the new revision, then update manuals.json last_vetted.
EXIT=0
```

The critical result: `5.4` matched `5.4.1` and `5.4.2` and did **not** match
`5.41`, which sits in the same index under the same manual. Segment-boundary
matching works.

```
$ python3 build_scripts/manual_diff.py A330P_QRH ABN --json
{
  "manual": "A330P_QRH",
  "changed_sections": ["ABN"],
  "index_generated": "2026-09-01 05:28:20",
  "match_count": 1,
  "file_count": 1,
  "item_count": 1,
  "results": [
    {
      "manual": "A330P_QRH",
      "changed_section": "ABN",
      "cited_section": "ABN-17",
      "file": "_sample_page.html",
      "page": "_sample_page.html",
      "kind": "html",
      "item_id": "qrh-abnormals",
      "locator": null,
      "raw_ref": "A330P QRH R35 ABN-17"
    }
  ]
}
EXIT=0
```

`--json` is valid JSON and prefix matching works on ident-style sections too
(`ABN` catches `ABN-17`).

```
$ python3 build_scripts/manual_diff.py A330_MEL 25
error: 'A330_MEL' has no citations in the index.
       Manuals present: A330P_FCOM, A330P_QRH, A330_FCTM, FOM
EXIT=3
```

A manual with no citations exits 3 and lists what is actually indexed, rather
than printing an empty checklist that reads like good news.

## Test 4: verify_grounding.py

Clean pass on the fixture:

```
$ python3 build_scripts/verify_grounding.py data/_sample.json
grounding check: 3 items scanned, 2 with src='manual', 0 ungrounded (threshold 0.60).
Every manual-sourced answer is supported by its own cited text.
EXIT=0
```

Then the real test. A copy of the bank with one number changed in the answer and
**not** in the `verbatim`, which is exactly how a revision sweep goes wrong:

```
$ # limit changed from "3000 PSI" to "5000 PSI", verbatim left saying 3000
$ python3 build_scripts/verify_grounding.py /tmp/.../_drift.json
UNGROUNDED ITEMS

_drift.json :: LIM-HYD-001
  at      : items[0]
  reason  : answer contains 1 numeric term(s) absent from its own cited text
  numbers not in cited text: 5000
  coverage: 83% of 6 keyword(s)

grounding check: 3 items scanned, 2 with src='manual', 1 ungrounded (threshold 0.60).
EXIT=1
```

Caught. Note the coverage was 83%, well above the 0.60 threshold: the item was
flagged because a **number** was unsupported. That is the intended behaviour and
the reason numbers are disqualifying on their own rather than just counted.

## Test 5: lint exits zero once the bad item is gone

```
$ # LIM-ELEC-003 removed from data/_sample.json, 2 items remain
$ python3 build_scripts/provenance_lint.py
ok   data/_sample.json  (2 items)

provenance lint: 2 items across 1 file; 0 errors in 0 files.
EXIT=0
```

Confirmed both directions: exit 1 with the unprovenanced item present, exit 0
with it removed. Nothing else changed between the two runs.

## Test 6: clean state after fixture removal

```
$ rm -f data/_sample.json _sample_page.html
$ python3 build_scripts/citation_index.py
scanned 0 JSON data banks and 0 HTML pages
indexed 0 citations across 0 manuals
wrote docs/CITATION_INDEX.md
wrote docs/citation_index.json
EXIT=0

$ python3 build_scripts/provenance_lint.py
error: no data files found under <repo>/data
EXIT=2
```

Empty repo does not crash the index. The lint exits 2 (bad input, distinct from
1 which means a real violation) because there is genuinely nothing to lint yet.
That is expected on an empty scaffold and will go away with the first data bank.

---

## Fix made during testing

The first citation regex matched any word after a manual name, so the prose line
"the **MEL requires** a placard for this item" indexed as a citation to
`A330_MEL` section `REQUIRES`. False citations are worse than missing ones here:
they pad the re-verify checklist with work that does not exist and erode trust
in the output.

Two changes to `citation_index.py`:

1. Added `\b` before the manual name and a `(?![A-Za-z0-9])` after the section,
   so partial words cannot match.
2. A section token must now contain **at least one digit**. Real manual sections
   do (`5.4.1`, `ABN-17`, `PR-NP-SOP-160`, `27-10-00`); a following English word
   does not.

Re-ran test 2 after the patch and confirmed 6 citations, with the MEL prose line
absent.

---

## Design decisions taken without asking

- **`data/*.json` walked shape-agnostically.** Items are found by recursive walk
  and identified by marker keys, not by a fixed schema. Quiz banks, flow banks
  and card banks nest differently and a bank added next year should not require
  a code change in four tools. Cost: a dict carrying a marker key that is not
  really an item would get linted. `_meta` and `_comment` blocks are excluded.
- **Ambiguous bare manual tails are rejected, not guessed.** `FCTM`, `MEL`,
  `PRC` and `AFM` resolve on their own because only one manual owns each tail.
  `FCOM`, `QRH` and `PERF` do not, because both the A330P and A330F books own
  them. A bare `FCOM 5.4` therefore fails to resolve and is warned about rather
  than being silently assigned to the PAX book. Cross-citing PAX and freighter is
  the failure this guards against, so guessing was not acceptable.
- **A missing number fails grounding on its own,** regardless of overall keyword
  coverage. An unsupported figure is the specific thing this tool exists to catch.
- **`verify_grounding.py` exits non-zero by default** so it works as a build gate,
  with `--report-only` for triaging a large bank without failing the run.
- **Exit code 2 is reserved for bad input** across all tools, separate from 1
  which always means a real content violation. A missing index and a failing item
  should not look alike to CI.
- **`manuals.json` carries a `_comment` key** stating its own rules. Any consumer
  must skip keys starting with `_`. Both tools that read it already do.
- **`docs/MANUAL_VERSIONS.md` was generated from `manuals.json`,** not typed by
  hand, so the seed cannot disagree with the source of truth on day one.

## Not done, deliberately

- No HTML pages. The task was scaffolding and tooling. The only page written was
  the throwaway test fixture, now deleted. The footer-renders-from-`manuals.json`
  contract is specified in `README.md` and awaits the first real page.
- `assets/palette.css` is entirely placeholder hex. Real Hawaiian brand values
  are being sourced separately and must be dropped in before styling is called
  done.
- `last_vetted` is `null` for all fifteen manuals. Nothing has been swept yet
  because there is no content yet.


---

# Memory-items drill, palette and app-icon build (2026-09-01)

Second build on the same day. Three deliverables, all under the repo root, all
executed with `python3` 3.11 and `node` 22 from the repo root. Transcript, not
a plan.

## What was built

1. **`assets/palette.css`, rewritten.** Every PLACEHOLDER replaced with the
   VERIFIED Hawaiian tokens from `palette/HAWAIIAN_PALETTE.md` section 4.
   Existing semantic token names kept (pages reference them); a few tokens
   added for surfaces and hover states the Hawaiian set defines. Header keeps
   the no-hex-outside-this-file rule and now cites the three source URLs.
   Coral `#EE453D` is an accent only, never text; coral text uses `#97322A`.
   Lagoon `#00A5BA` is out. Dark block provided.
2. **`memory-items.html`, new, page version 0.1.** Standalone offline drill,
   same engine, keyboard model, banner and footer pattern as
   `limitations.html` 0.4. Ten procedures from the eleven verified entries
   (`mi-vis-01` FCOM and `mi-vis-04` QRH are the same EMER DESCENT block and
   are merged at load into one item carrying both citations). Whole-procedure
   and line-by-line modes; procedure-to-actions and actions-to-procedure
   directions; verbatim self-grade per line with the grading copy stating
   that paraphrase is a miss; running score, missed-procedure queue re-served
   at round end, per-procedure served / clean / never-missed board.
3. **`limitations.html`, patched in place to 0.5.** Three icon links added in
   `<head>` (inline data-URI favicon, apple-touch-icon, manifest), META
   version bumped to 0.5 with the note `(0.5: app icon wired)`. Nothing else
   changed; the Hawaiian values it already inlines are the same values now in
   `assets/palette.css`.

Verification scripts were kept under `build_scripts/verify/` so the run below
can be repeated.

## Verification transcript

```
$ python3 build_scripts/verify/check_memory_items_data.py
embedded entries: 11
actions arrays identical to source for all 11 entries: True
entire embedded block == memory_items_v2.json: True
repo data/memory_items.json == memory_items_v2.json: True
boxes arrays (5 entries) consistent with actions: True
distinct procedures by identical actions: 10
EXIT=0

$ bash build_scripts/verify/node_check_scripts.sh
memory-items.html: 2 script blocks extracted
node --check memory-items.html.script1.js: OK
node --check memory-items.html.script2.js: OK
limitations.html: 2 script blocks extracted
node --check limitations.html.script1.js: OK
node --check limitations.html.script2.js: OK
EXIT=0

$ for f in memory-items.html limitations.html; do echo "$f em-dash=$(grep -c $'\xe2\x80\x94' $f) mdash=$(grep -c "&mdash;" $f) localStorage=$(grep -c localStorage $f) sessionStorage=$(grep -c sessionStorage $f) fetch-calls=$(grep -E "fetch\(" $f | grep -vc "no fetch()") external-src=$(grep -cE "src=[\"']?(https?:)?//" $f) any-src-attr=$(grep -oE "<(script|img|iframe|link)[^>]*src=" $f | wc -l); done
memory-items.html em-dash=0 mdash=0 localStorage=0 sessionStorage=0 fetch-calls=0 external-src=0 any-src-attr=0
limitations.html em-dash=0 mdash=0 localStorage=0 sessionStorage=0 fetch-calls=0 external-src=0 any-src-attr=0
$ grep -c PLACEHOLDER assets/palette.css
0
$ grep -nE "fetch\(" memory-items.html limitations.html   # the only matches are the comment saying there is no fetch()
memory-items.html:542:   with no fetch() and no network.
limitations.html:552:   offline when opened straight from disk (file://) with no fetch() and no

$ python3 build_scripts/verify/playwright_smoke.py
[limitations] scrollY after load: 0
[limitations] focused element on load: answerBox
[limitations] console errors: 0 []
[limitations] banner present: True
[limitations] icon href starts with data:image/png;base64: True
[limitations] apple-touch-icon: assets/icons/icon-180.png   manifest: site.webmanifest
[limitations] horizontal overflow: False (scrollWidth 1100, innerWidth 1100)
[limitations] footer: Generated 2026-09-01 · page version 0.5 · 160 items from limitations_v2.json, verified FCOM set merged with the AFM addendum; 257 numeric tokens re-checked, 0 wrong or fabricated numbers, no limit value changed
[memory-items] scrollY after load: 0
[memory-items] focused element on load: answerBox
[memory-items] console errors: 0 []
[memory-items] banner present: True
[memory-items] icon href starts with data:image/png;base64: True
[memory-items] apple-touch-icon: assets/icons/icon-180.png   manifest: site.webmanifest
[memory-items] horizontal overflow: False (scrollWidth 1100, innerWidth 1100)
[memory-items] banner carries the TCAS CAUTION unboxed fact and the Smoke/Fumes p3164 At-ANY-TIME fact: True
[memory-items] footer: A330P FCOM R17, issue 15 MAY 26, A330 passenger fleet, Memory items only, the FCOM's own [MEM] convention | A330P QRH R35, issue 26 JUN 26, cited where the QRH carries the block (EMER DESCENT, UNRELIABLE SPEED INDICATION). | Generated 2026-09-01 · page version 0.1 · 10 procedures from memory_items.json, ten procedures, all visually verified against rendered pages
[memory-items] procedures built at load: 10
    mi-vis-01 [MEM] EMER DESCENT lines= 5 books= ['FCOM R17', 'QRH R35'] headers= 1
    mi-vis-02 [MEM] STALL RECOVERY lines= 6 books= ['FCOM R17'] headers= 2
    mi-vis-03 [MEM] STALL WARNING AT LIFTOFF lines= 3 books= ['FCOM R17'] headers= 1
    mi-vis-05 UNRELIABLE SPEED INDICATION lines= 13 books= ['QRH R35'] headers= 0
    mi-vis-06 [MEM] LOSS OF BRAKING lines= 7 books= ['FCOM R17'] headers= 2
    mi-vis-07 [MEM] TAWS CAUTION lines= 14 books= ['FCOM R17'] headers= 10
    mi-vis-08 [MEM] TAWS WARNING lines= 6 books= ['FCOM R17'] headers= 1
    mi-vis-09 [MEM] TCAS CAUTION - TRAFFIC ADVISORY lines= 1 books= ['FCOM R17'] headers= 0
    mi-vis-10 [MEM] TCAS WARNING - RESOLUTION ADVISORY lines= 9 books= ['FCOM R17'] headers= 3
    mi-vis-11 [MEM] WINDSHEAR WARNING - REACTIVE WINDSHEAR lines= 10 books= ['FCOM R17'] headers= 3
[memory-items] DATA_WARNINGS: []
[memory-items] whole mode, procedure 1: [MEM] TAWS WARNING (6 lines), focused box:  answerBox
[memory-items] V shows source: FCOM R17, page PRO-ABN-SURV P 3/8 (pdf 3211), ident PRO-ABN-SURV-00026799.0001001 · MEMORY ITEMS · HIGH · manu
[memory-items] after grading 6 lines: counts={'got': 5, 'missed': 1} owed=1
[memory-items] advanced to procedure 2: [MEM] TAWS CAUTION
[memory-items] end of round 1: phase=roundbreak counts={'got': 73, 'missed': 1}
[memory-items] round 2 re-serves: [MEM] TAWS WARNING
[memory-items] phase after round 2: done
[memory-items] scoreboard: 9 never missed, 1 missed at least once
[memory-items] line-by-line, procedure: [MEM] LOSS OF BRAKING (7 lines)
[memory-items] line-by-line completed clean: counts={'got': 7, 'missed': 0}
[memory-items] actions -> procedure: revealed [MEM] EMER DESCENT, graded got; counts={'got': 1, 'missed': 0}
[memory-items] reference tab: 11 citations listed, TCAS CAUTION marked printed unboxed
[memory-items] console errors after full drive: 0
[memory-items phone/dark] scrollY=0 overflow=False (scrollWidth 375, innerWidth 375) body bg=rgb(21, 19, 28) errors=[]
ALL PLAYWRIGHT CHECKS PASSED
EXIT=0
```

## Judgment calls made without asking

- **Dark-mode values.** The palette doc states the Auro inverse tokens were
  not extracted or contrast-checked (section 6, item 6). Rather than invent a
  second set, `palette.css` and `memory-items.html` carry the dark block
  `limitations.html` 0.4 already ships, built from the same three Hawaiian
  ramps (orchid `#ACA1CC`, fuchsia-subtle `#E26DB8`, coral-subtle `#FF9080`);
  the surfaces in that block are derived, not Auro tokens, and the header
  comment says so. Re-verify against the Auro inverse block when extracted.
- **Repeated condition header in STALL RECOVERY.** The visual pass recorded
  "When out of stall (no longer stall indications) :" on two consecutive
  boxes. The page prints a consecutive duplicate header once, above the first
  of the two boxes. The data is untouched; only the rendering dedupes.
- **Gradable lines.** Every line inside a box is graded, including plain
  boxed statements ("DO NOT CHANGE CONFIGURATION ... UNTIL CLEAR OF
  OBSTACLE.") and the QRH unreliable-speed box's own leading lines ("If the
  safe conduct of the flight is impacted", "PITCH/THRUST"), because they are
  printed inside the box. Lines ending in ":" are condition headers, shown
  unboxed and never graded. TCAS CAUTION's single line renders unboxed via a
  `RENDER_HINTS` entry keyed by id, since the schema has no field for it.
- **Enter in the whole-procedure answer box.** The box is multi-line, so a
  bare Enter inserts a new line; Enter on an empty line, or Ctrl/Cmd+Enter,
  reveals. Line-by-line and actions-to-procedure boxes are single-line and
  Enter reveals as in `limitations.html`. The legend states this.
- **Typed-text check** compares each printed line to what was typed after
  ignoring case, spacing and the dot leader only; words and order are not
  normalised. It is shown as an aid next to each line; the self-grade is the
  grade.
- **`limitations.html` version note.** The file had no version-note field, so
  the required text was added as a comment beside `version: "0.5"` rather
  than inventing a new META field.
- **Reference tab** added to `memory-items.html` (all ten procedures rendered
  as printed with citations), mirroring the Drill / Reference split in
  `limitations.html`. Not asked for, cheap, and it is where "book, page label
  and Airbus ident on demand" lives outside the drill.

## Not done

- No cross-check against the training-department worksheets; the banner says
  so and that remains the gating item before this page is used to decide
  readiness.
- The Project copies of `palette.css`, `BUILD_NOTES.md` and `limitations.html`
  were not re-uploaded; the repo on disk is the current state.


---

# Fix round from verification passes 1 to 4 (2026-09-01)

Inputs: `data/PASS1_fixes.json`, `PASS3_failures.json`, `PASS4_failures.json`,
`PASS4_visual.md`, `data/limitations_v3.json`. Both pages patched in place;
limitations.html is now 0.6, memory-items.html 0.2.

## What changed

Data
- `data/memory_items_v3.json` built by `build_scripts/apply_pass1_memory_fixes.py`
  from v2 + the 12 PASS1 corrections (split at "\n" into consecutive
  elements, typographic quotes adopted as given), plus 13 box-break sentinels
  `""` placed exactly per the coordinator's grouping (LOSS OF BRAKING 3, TAWS
  CAUTION 2, TAWS WARNING 2, TCAS WARNING 4, WINDSHEAR 2). Copied to
  `repo/data/memory_items.json` and re-embedded. Entries 01 to 05 untouched.
- Renderer: `isHeader()` now also treats a line starting with a quote
  character (straight or curly) and carrying no " ... " as an unboxed header;
  `""` ends the current box and renders a 4px unboxed gap. Neither is graded
  or counted; the UI line counts are boxed lines only (TAWS CAUTION 14,
  TCAS WARNING 9, WINDSHEAR 10, LOSS OF BRAKING 7, TAWS WARNING 6).
- limitations re-embedded from `limitations_v3.json` (160 items, 144
  VERIFIED / 16 UNCLEAR, 9 with `corroboration`, 15 with `audit`, 0 refs with
  the backslash-underscore artifact). `corroboration` was already rendered.
  Gaps panel: "16 unclear", flaps/slats unit bullet dropped, UNCLEAR reason
  for LIM-AG-SPD-00019939.0001001 narrowed to CONF 1*; the UNCLEAR_REASONS
  key for the crosswind table updated to the clean ref. `repo/data/limitations.json`
  updated to v3.

Runtime (pass 3, items 3 to 8)
- Both: `startNextRound()` clears `S.typed`; re-served cards start empty.
  Arrow keys work from an empty answer box; Skip's button was already wired.
- limitations: reference table is `table-layout: fixed` (19/39/22/20 %),
  source text opens in a full-width `tr.srcrow` under the item, `.tablewrap`
  scrolls at phone width, `.verbatim` breaks long dot-leader runs. Grade pill
  driven by a per-round `S.gradedRound` (cleared on re-serve) while `S.graded`
  keeps the latest-grade counter semantics the harness models. UNCLEAR reason
  moved after reveal (badge only before). Expand-all label recomputed from
  state; clicking it with anything open collapses everything.

Visual (pass 4, items 9 to 20)
- Non-flipping `--ink-on-brand` / `--pale-on-brand` tokens in both inline
  palettes, used for all header and footer text; the four raw `#FFFFFF` in
  limitations.html are gone (pressed segment and table header use
  `--ink-inverse`, 7.64:1 on the lifted purple in dark mode).
- memory-items phone: `.mline` wraps with baseline alignment, value falls to a
  right-aligned line under its item inside the box; `.board` scrolls; no
  gutter box on ungraded lines; `.tmark` 11px.
- Both: `.seg` no longer clips the focus ring (end buttons rounded instead),
  `.btn .k` at full opacity, `color-scheme: light dark` and `accent-color`
  on `:root`, info panels are `<details>` with a summary and count, open on
  desktop and collapsed at or under 640px. limitations: `.recovered .tag`
  styled, status-bar fragments wrapped in spans.

## Verification transcript

```
$ python3 build_scripts/apply_pass1_memory_fixes.py
applied 12 PASS1 fixes
wrote /home/claude/a330/data/memory_items_v3.json and copied to /home/claude/a330/repo/data/memory_items.json
  mi-vis-01   5 elements, 0 headers, 0 breaks, 5 boxed lines
  mi-vis-02   6 elements, 0 headers, 0 breaks, 6 boxed lines
  mi-vis-03   3 elements, 0 headers, 0 breaks, 3 boxed lines
  mi-vis-04   5 elements, 0 headers, 0 breaks, 5 boxed lines
  mi-vis-05  13 elements, 0 headers, 0 breaks, 13 boxed lines
  mi-vis-06  12 elements, 2 headers, 3 breaks, 7 boxed lines
  mi-vis-07  29 elements, 13 headers, 2 breaks, 14 boxed lines
  mi-vis-08  10 elements, 2 headers, 2 breaks, 6 boxed lines
  mi-vis-09   1 elements, 0 headers, 0 breaks, 1 boxed lines
  mi-vis-10  16 elements, 3 headers, 4 breaks, 9 boxed lines
  mi-vis-11  16 elements, 4 headers, 2 breaks, 10 boxed lines
EXIT=0

$ python3 build_scripts/verify/check_embedded_data.py
memory-items.html: 11 entries embedded; every entry == memory_items_v3.json; repo data/memory_items.json == v3: True
  v2 -> v3: actions changed on ['mi-vis-06', 'mi-vis-07', 'mi-vis-08', 'mi-vis-10', 'mi-vis-11']; 13 box-break sentinels
  no embedded newlines remain in any action line
limitations.html: 160 items embedded; every item == limitations_v3.json; 144 VERIFIED / 16 UNCLEAR
  refs with backslash-underscore: 0; items with corroboration: 9; with audit: 15
EXIT=0

$ bash build_scripts/verify/node_check_scripts.sh
memory-items.html: 2 script blocks extracted
node --check memory-items.html.script1.js: OK
node --check memory-items.html.script2.js: OK
limitations.html: 2 script blocks extracted
node --check limitations.html.script1.js: OK
node --check limitations.html.script2.js: OK
EXIT=0

$ for f in memory-items.html limitations.html; do ... grep counts ...; done
memory-items.html em-dash=0 mdash=0 localStorage=0 sessionStorage=0 fetch-calls=0 external-src=0 any-src-attr=0 raw-hex-outside-palette-block=0 backslash-underscore=0
limitations.html em-dash=0 mdash=0 localStorage=0 sessionStorage=0 fetch-calls=0 external-src=0 any-src-attr=0 raw-hex-outside-palette-block=0 backslash-underscore=0
em dashes in data files: limitations_v3.json=0 memory_items_v3.json=0

$ python3 build_scripts/verify/pass3_runtime.py   (output trimmed to the summary; full report in data/PASS3_runtime.md)
EXIT=0
Generated 2026-09-01 14:53:09 by `build_scripts/verify/pass3_runtime.py` (Playwright, headless Chromium, file://).

## Matrix

| Test | Scope | memory-items | limitations |
|---|---|---|---|
| A | Load (scroll, errors, banner, overflow) at 1280x900 / 390x844 / 360x780 + narrow state sweeps | PASS (14/14) | PASS (14/14) |
| B | Dark scheme load checks + computed colours | PASS (18/18) | PASS (18/18) |
| C | memory-items whole-procedure full session incl. re-serve | PASS (253/253) | n/a |
| D | memory-items line-by-line full session | PASS (1222/1222) | n/a |
| E | memory-items actions -> procedure direction | PASS (166/166) | n/a |
| F | limitations full sessions (both directions), UNCLEAR toggle, system filters | n/a | PASS (101/101) |
| G | Reference tabs | PASS (9/9) | PASS (31/31) |
| I | Text integrity across visited states | PASS (1/1) | PASS (1/1) |
| H | Keyboard edge cases | PASS (72/72) | PASS (24/24) |
| J | Icon links | PASS (5/5) | PASS (5/5) |
**Checks recorded: 1954. Pass: 1954. Fail: 0. States scanned for text integrity and overflow: 2055.**

$ python3 build_scripts/verify/pass4_visual_checks.py
[limitations.html light] .site-head h1                        rgb(255, 255, 255) on rgb(70, 60, 143) = 9.12:1 PASS
[limitations.html light] .site-head .sub                      rgb(234, 229, 244) on rgb(70, 60, 143) = 7.39:1 PASS
[limitations.html light] footer .id                           rgb(255, 255, 255) on rgb(70, 60, 143) = 9.12:1 PASS
[limitations.html light] footer .muted                        rgb(234, 229, 244) on rgb(70, 60, 143) = 7.39:1 PASS
[limitations.html light] .seg button[aria-pressed=true]       rgb(255, 255, 255) on rgb(70, 60, 143) = 9.12:1 PASS
[limitations.html light] thead th                             rgb(255, 255, 255) on rgb(70, 60, 143) = 9.12:1 PASS
[limitations.html light] .seg overflow-x = visible PASS
[limitations.html light] .btn .k opacity = 1 PASS
[limitations.html light] color-scheme = 'light dark' PASS
[limitations.html light] desktop: info panels open = [True, True] PASS
[limitations.html dark] .site-head h1                        rgb(255, 255, 255) on rgb(49, 41, 92) = 13.11:1 PASS
[limitations.html dark] .site-head .sub                      rgb(234, 229, 244) on rgb(49, 41, 92) = 10.62:1 PASS
[limitations.html dark] footer .id                           rgb(255, 255, 255) on rgb(49, 41, 92) = 13.11:1 PASS
[limitations.html dark] footer .muted                        rgb(234, 229, 244) on rgb(49, 41, 92) = 10.62:1 PASS
[limitations.html dark] .seg button[aria-pressed=true]       rgb(21, 19, 28) on rgb(172, 161, 204) = 7.64:1 PASS
[limitations.html dark] thead th                             rgb(21, 19, 28) on rgb(172, 161, 204) = 7.64:1 PASS
[limitations.html dark] .seg overflow-x = visible PASS
[limitations.html dark] .btn .k opacity = 1 PASS
[limitations.html dark] color-scheme = 'light dark' PASS
[limitations.html dark] desktop: info panels open = [True, True] PASS
[limitations.html phone] info panels collapsed = [True, True] PASS
[limitations.html phone] no horizontal overflow on load: True (390/390)
[limitations.html phone] reference, all sources expanded, no page-level horizontal overflow: True (390/390)
[limitations.html 360px] reference, all sources expanded, no page-level horizontal overflow: True (360/360)
[limitations.html] .recovered .tag styled (border solid): PASS
[limitations.html] status bar fragments wrapped in spans: 6 PASS
[memory-items.html light] .site-head h1                        rgb(255, 255, 255) on rgb(70, 60, 143) = 9.12:1 PASS
[memory-items.html light] .site-head .sub                      rgb(234, 229, 244) on rgb(70, 60, 143) = 7.39:1 PASS
[memory-items.html light] footer .id                           rgb(255, 255, 255) on rgb(70, 60, 143) = 9.12:1 PASS
[memory-items.html light] footer .muted                        rgb(234, 229, 244) on rgb(70, 60, 143) = 7.39:1 PASS
[memory-items.html light] .seg button[aria-pressed=true]       rgb(255, 255, 255) on rgb(70, 60, 143) = 9.12:1 PASS
[memory-items.html light] .modes button[aria-selected=true]    rgb(206, 12, 136) on rgb(255, 255, 255) = 5.21:1 PASS
[memory-items.html light] .seg overflow-x = visible PASS
[memory-items.html light] .btn .k opacity = 1 PASS
[memory-items.html light] color-scheme = 'light dark' PASS
[memory-items.html light] desktop: info panels open = [True] PASS
[memory-items.html dark] .site-head h1                        rgb(255, 255, 255) on rgb(49, 41, 92) = 13.11:1 PASS
[memory-items.html dark] .site-head .sub                      rgb(234, 229, 244) on rgb(49, 41, 92) = 10.62:1 PASS
[memory-items.html dark] footer .id                           rgb(255, 255, 255) on rgb(49, 41, 92) = 13.11:1 PASS
[memory-items.html dark] footer .muted                        rgb(234, 229, 244) on rgb(49, 41, 92) = 10.62:1 PASS
[memory-items.html dark] .seg button[aria-pressed=true]       rgb(21, 19, 28) on rgb(172, 161, 204) = 7.64:1 PASS
[memory-items.html dark] .modes button[aria-selected=true]    rgb(226, 109, 184) on rgb(21, 19, 28) = 6.23:1 PASS
[memory-items.html dark] .seg overflow-x = visible PASS
[memory-items.html dark] .btn .k opacity = 1 PASS
[memory-items.html dark] color-scheme = 'light dark' PASS
[memory-items.html dark] desktop: info panels open = [True] PASS
[memory-items.html phone] info panels collapsed = [True] PASS
[memory-items.html phone] no horizontal overflow on load: True (390/390)
[memory-items.html phone] .mline values inside their box and not above their item: 64 checked, 0 bad [] PASS
[memory-items.html phone] reference tab no horizontal overflow: True
[memory-items.html phone] .board overflow-x = auto PASS
[memory-items.html phone] gutter marks after reveal (only the cursor line carries one): ['grade'] PASS
VISUAL CHECKS: ALL PASSED
EXIT=0

$ python3 build_scripts/verify/playwright_smoke.py   (tail)
[memory-items] line-by-line completed clean: counts={'got': 14, 'missed': 0}
[memory-items] actions -> procedure: revealed [MEM] EMER DESCENT, graded got; counts={'got': 1, 'missed': 0}
[memory-items] reference tab: 11 citations listed, TCAS CAUTION marked printed unboxed
[memory-items] console errors after full drive: 0
[memory-items phone/dark] scrollY=0 overflow=False (scrollWidth 375, innerWidth 375) body bg=rgb(21, 19, 28) errors=[]
ALL PLAYWRIGHT CHECKS PASSED
EXIT=0
```

## Judgment calls

- `limitations_v3.json` carried one em dash inside a hand-authored
  `corroboration` note on lim-acgen-01 ("two books, FCOM and AFM agree"); it
  was replaced with a comma in the source file so the embedded block still
  equals the file item for item and the no-em-dash rule holds. No manual text
  was touched.
- Item 5 asked to reset `S.graded` on re-serve. Doing that literally breaks
  the "latest grade wins" counter semantics the pass-3 harness models (round-2
  status checks failed 300+ times). The pill now reads from a per-round
  record and the counters keep their semantics; the harness passes both ways.
- The pass-3 harness hardcoded 139 for the VERIFIED count (v2). It now derives
  the number from the embedded data (144 on v3); nothing else in it changed.
- The dot leader is not hidden when a value wraps on a phone; it stays on the
  item's line and the value drops to the next line, right-aligned, inside
  the box. Hiding it would need a wrap-detection script; judged not worth it.
- The apply script appends a short `audit` entry to the five memory-item
  entries it changed, mirroring the limitations audit trail.

## Not done

- The " :" spacing in condition headers (PASS4 F13b) was left as extracted;
  the finding itself says confirm against the printed page first.
- No sort control on the phone reference view (F13f); phone view is unsorted.


---

# Pass 5 polish (2026-09-01)

limitations.html 0.7, memory-items.html 0.3.

1. limitations re-embedded from `limitations_v3.json` (7 verbatim escape artifacts gone upstream); embed == file, 160 items, no string carries a backslash.
2. `.verbatim` uses `overflow-wrap: anywhere` only (no `word-break: break-all`); 0 mid-word breaks at 1280 and 390 by the pass-5 detector.
3. `label.check` is `inline-block` (was `inline-flex` with a gap that split "(", the count and ")"); reads "Include UNCLEAR items (16)".
4. Verbatim trimmed at render time in the drill citation and the reference rows; data untouched.
5. Ref column fixed at 260px (fits the longest ident, `nowrap` on the code), parameter column takes the rest; 0 of 160 idents wrap on desktop.
6. Phone scoreboard restacked: one grid row per procedure (name, then served / clean with labels, then status); nothing clipped, no scroll needed.
7. "1 line" / "n lines" pluralised on the board.
8. Mode segment aria-pressed follows the mode in force: both false in actions -> procedure, restored on return. Disabled segment buttons use `--ink-muted` on `--surface-sunken` instead of opacity so they stay AA.

## Verification transcript

```
$ python3 build_scripts/verify/check_embedded_data.py
memory-items.html: 11 entries embedded; every entry == memory_items_v3.json; repo data/memory_items.json == v3: True
  v2 -> v3: actions changed on ['mi-vis-06', 'mi-vis-07', 'mi-vis-08', 'mi-vis-10', 'mi-vis-11']; 13 box-break sentinels
  no embedded newlines remain in any action line
limitations.html: 160 items embedded; every item == limitations_v3.json; 144 VERIFIED / 16 UNCLEAR
  refs with backslash-underscore: 0; items with corroboration: 9; with audit: 15
EXIT=0
$ bash build_scripts/verify/node_check_scripts.sh
memory-items.html: 2 script blocks extracted
node --check memory-items.html.script1.js: OK
node --check memory-items.html.script2.js: OK
limitations.html: 2 script blocks extracted
node --check limitations.html.script1.js: OK
node --check limitations.html.script2.js: OK
EXIT=0
memory-items.html em-dash=0 mdash=0 localStorage=0 sessionStorage=0 fetch-calls=0 external-src=0 any-src-attr=0 raw-hex-outside-palette-block=0
limitations.html em-dash=0 mdash=0 localStorage=0 sessionStorage=0 fetch-calls=0 external-src=0 any-src-attr=0 raw-hex-outside-palette-block=0
$ python3 build_scripts/verify/pass5_polish_checks.py
limitations embed == limitations_v3.json: True | items: 160 | strings with a backslash: 0
UNCLEAR label: ' Include UNCLEAR items (16)' PASS
source blocks rendered with a leading space: 0 PASS
idents wrapping mid-string on desktop: 0 of 160 PASS
plain words split across lines in source text (desktop): 0 PASS
desktop overflow: False
360px all sources expanded overflow: False (360/360)
scoreboard '1 lines': False | '1 line' present: True PASS
phone scoreboard cells beyond the board edge: 0 PASS
mode segment after switching to actions -> procedure: ['false', 'false', 'line', 'a2p'] PASS
mode segment after Whole procedure: ['true', 'false', 'whole'] PASS
versions: 0.7 0.3 PASS
POLISH CHECKS: ALL PASSED
EXIT=0
$ python3 build_scripts/verify/pass4_visual_checks.py  (tail)
[memory-items.html phone] gutter marks after reveal (only the cursor line carries one): ['grade'] PASS
VISUAL CHECKS: ALL PASSED
EXIT=0
$ python3 build_scripts/verify/playwright_smoke.py  (tail)
ALL PLAYWRIGHT CHECKS PASSED
EXIT=0
$ python3 build_scripts/verify/pass3_runtime.py  (summary line from data/PASS3_runtime.md)
EXIT=0
**Checks recorded: 2011. Pass: 2011. Fail: 0. States scanned for text integrity and overflow: 2062.**
$ python3 build_scripts/verify/pass5/run_pass5.py  (independent harness, unmodified; tail)

1319/1320 assertions passed, 1 failures, 103s
FAIL memory-items.html C7-counters board TCAS CAUTION - TRAFFIC ADVISORY: shows 1 lines: [{'name': 'TCAS CAUTION - TRAFFIC ADVISORY', 'lines': '1 line'}]
```

## Notes on the pass-5 harness (not modified)

- The one remaining failure, `C7-counters board TCAS CAUTION ... shows 1 lines`, is the harness asserting the text equals "1 lines" verbatim, which item 7 of this round asked me to change. The page now says "1 line". Left as a known harness conflict.
- `contrast_checks` clicks Got then Missed on whatever procedure the shuffle serves first; when that is TCAS CAUTION (one line) there is no second button and the run aborts on a 30 s timeout. Two of four runs hit it; the reported run is a clean pass of the rest. A deterministic first procedure or a length check in the harness would remove the flake.


---

# Engine / dist split (2026-09-01)

Data/engine separation applied. `limitations.html` and `memory-items.html`
are now engine pages: the data slot between `/* @@DATA_START <tag> */` and
`/* @@DATA_END */` holds `var LIMITATIONS = null;` (resp. `MEMORY_ITEMS`),
and a loader at the end of the second script fetches `data/limitations.json`
(resp. `data/memory_items.json`) on DOMContentLoaded, assigns it and calls
`boot()`. `boot()` is the previous top-level data-dependent initialisation
(PARAM_COUNT, BY_ID, SYSTEMS, UNCLEAR_TOTAL, S / PROCS, BY_PID, S) plus
`renderHead(); startSession();`; every function and the state object stay
global so the harnesses' page.evaluate hooks still work. If the fetch cannot
run (file:// in most browsers) the drill card shows "Open the standalone build
(dist/) for offline use, or serve this folder over http." Nothing else changed
(one-off transform kept as `build_scripts/make_engine_pages.py`).

`build_scripts/build_standalone.py` inlines compact JSON (ensure_ascii=False)
between the markers as `const <NAME> = <json>;` and writes `dist/`, copying
the touch icon and manifest the pages link relatively so the folder is
self-consistent. `dist/` is in `.gitignore` (generated, not committed).

Verification scripts now default to `dist/` (pass3 harness honours
`A330_PAGES_DIR`); `static_constraints.py` and `verify_engine_and_dist.py`
are new.

## Verification transcript

```
$ python3 build_scripts/build_standalone.py
limitations.html: 160 entries from data/limitations.json -> dist/limitations.html (147826 bytes)
memory-items.html: 11 entries from data/memory_items.json -> dist/memory-items.html (82469 bytes)
copied assets/icons/icon-180.png -> dist/assets/icons/icon-180.png
copied site.webmanifest -> dist/site.webmanifest
EXIT=0
$ python3 -m http.server 8765 --bind 127.0.0.1 &  (repo root)
$ python3 build_scripts/verify/verify_engine_and_dist.py http://localhost:8765/
[file:// dist limitations.html] data=160 (want 160) booted=True console errors=0 [] reveal+grade={'revealed': False, 'counts': {'got': 1, 'missed': 0}, 'idx': 1, 'phase': 'drill'} PASS
[file:// dist memory-items.html] data=11 (want 11) booted=True console errors=0 [] reveal+grade={'revealed': True, 'counts': {'got': 7, 'missed': 0}, 'idx': 0, 'phase': 'drill'} PASS
[http engine limitations.html] data=160 (want 160) booted=True console errors=0 [] reveal+grade={'revealed': False, 'counts': {'got': 1, 'missed': 0}, 'idx': 1, 'phase': 'drill'} PASS
[http engine memory-items.html] data=11 (want 11) booted=True console errors=0 [] reveal+grade={'revealed': True, 'counts': {'got': 7, 'missed': 0}, 'idx': 0, 'phase': 'drill'} PASS
[file:// engine limitations.html] card says: 'Data not loadedOpen the standalone build (dist/) for offline use, or serve this folder over http.'
[file:// engine memory-items.html] card says: 'Data not loadedOpen the standalone build (dist/) for offline use, or serve this folder over http.'
ENGINE/DIST CHECKS: ALL PASSED
EXIT=0
$ kill %http.server
server killed: no response on :8765
$ bash build_scripts/verify/node_check_scripts.sh
memory-items.html: 2 script blocks extracted
node --check memory-items.html.script1.js: OK
node --check memory-items.html.script2.js: OK
limitations.html: 2 script blocks extracted
node --check limitations.html.script1.js: OK
node --check limitations.html.script2.js: OK
dist/memory-items.html: 2 script blocks extracted
node --check dist_memory-items.html.script1.js: OK
node --check dist_memory-items.html.script2.js: OK
dist/limitations.html: 2 script blocks extracted
node --check dist_limitations.html.script1.js: OK
node --check dist_limitations.html.script2.js: OK
EXIT=0
$ python3 build_scripts/verify/static_constraints.py
limitations.html: 63030 bytes (engine, must be < 100000: True); em dash=0, &mdash;=0, localStorage/sessionStorage=0, private-use chars=0, backslash-u / backslash-x in JS=0, external src/href (http, https, protocol-relative)=0, fetch calls other than the relative data fetch=0, raw hex outside the palette block (comments ignored)=0 -> PASS
memory-items.html: 71932 bytes (engine, must be < 100000: True); em dash=0, &mdash;=0, localStorage/sessionStorage=0, private-use chars=0, backslash-u / backslash-x in JS=0, external src/href (http, https, protocol-relative)=0, fetch calls other than the relative data fetch=0, raw hex outside the palette block (comments ignored)=0 -> PASS
dist/limitations.html: 147826 bytes; em dash=0, &mdash;=0, localStorage/sessionStorage=0, private-use chars=0, backslash-u / backslash-x in JS=0, external src/href (http, https, protocol-relative)=0, fetch calls other than the relative data fetch=0, raw hex outside the palette block (comments ignored)=0 -> PASS
dist/memory-items.html: 82469 bytes; em dash=0, &mdash;=0, localStorage/sessionStorage=0, private-use chars=0, backslash-u / backslash-x in JS=0, external src/href (http, https, protocol-relative)=0, fetch calls other than the relative data fetch=0, raw hex outside the palette block (comments ignored)=0 -> PASS
STATIC CONSTRAINTS: ALL PASSED
EXIT=0
$ python3 build_scripts/verify/check_embedded_data.py
dist/memory-items.html: 11 entries embedded; every entry == memory_items_v3.json; repo data/memory_items.json == v3: True
  v2 -> v3: actions changed on ['mi-vis-06', 'mi-vis-07', 'mi-vis-08', 'mi-vis-10', 'mi-vis-11']; 13 box-break sentinels
  no embedded newlines remain in any action line
dist/limitations.html: 160 items embedded; every item == limitations_v3.json; 144 VERIFIED / 16 UNCLEAR
  refs with backslash-underscore: 0; items with corroboration: 9; with audit: 15
EXIT=0
$ pass3_runtime.py against dist/ (A330_PAGES_DIR default)
**Checks recorded: 2038. Pass: 2038. Fail: 0. States scanned for text integrity and overflow: 2068.**
$ wc -c limitations.html memory-items.html dist/limitations.html dist/memory-items.html
 63030 limitations.html
 71932 memory-items.html
147826 dist/limitations.html
 82469 dist/memory-items.html
365257 total
$ git hash-object limitations.html memory-items.html data/limitations.json data/memory_items.json
f8e82f840c30e4246aaff1060741d02c2ce32bf9  limitations.html
e925cd0ceeb16e7dde8f61554676cb6a9f22bb03  memory-items.html
88e39d0d2ce0ea73135bf18233ae23495a8eeeec  data/limitations.json
7cdc78f8e0a4e4d47c98d9cb7b89954cd89c7855  data/memory_items.json
```


---

# Training-document cross-check integration (2026-09-02)

Inputs: `data/memory_items_CROSSCHECK.md`, `data/limitations_CROSSCHECK.md`.
limitations.html is 0.8, memory-items.html 0.4.

## What changed

- `build_scripts/apply_crosscheck_upgrades.py` (new, kept for the record):
  upgraded lim-eng-01 (#73 EGT), lim-fuel-06/07 (#107/108 imbalance) and
  lim-oxy-01 (#131 oxygen) from UNCLEAR to VERIFIED in limitations_v3.json,
  each with the screenshot-corroboration text and an audit entry. The
  cross-check calls them "three items" but the imbalance table is two dataset
  rows, so four rows moved: now 148 VERIFIED / 12 UNCLEAR. Copied to
  repo/data/limitations.json. Gaps panel updated to 12 unclear with the
  upgrade note; the three now-moot UNCLEAR_REASONS keys pruned; head sub,
  chips and filter counts derive from data and follow automatically
  (verified: "Include UNCLEAR items (12)", Engines chip no longer flagged).
- memory_items_v4.json: `relearn: true` + one-sentence `relearn_note` on
  mi-vis-06/07/08/10/11 (LOSS OF BRAKING, TAWS CAUTION, TAWS WARNING,
  TCAS WARNING, WINDSHEAR). EMER DESCENT not flagged: the cross-check's
  finding there (SPD BRK unconditional) is a confirmation, not a relearn.
  TCAS CAUTION - TA is absent from the legacy doc entirely, so it is carried
  by the banner and the relearn list rather than a "CHANGED" pill, which
  would misstate it. Copied to repo/data/memory_items.json.
- memory-items renderer: "CHANGED since your old notes" pill on flagged
  procedures (drill card and reference), relearn note shown on reveal only.
- Banner rewritten: cross-checked 2026-09-01 against LO Rev 7 (04/06/23)
  and the personal doc; ten [MEM] procedures stand as drill scope; the one
  conflict (LOSS OF BRAKING park brake / anti-skid wording) resolved in the
  FCOM's favor; "13 lines in the legacy study doc are now wrong; see
  memory_items_CROSSCHECK.md in the project for the relearn list"; TCAS
  CAUTION and Smoke/Fumes facts kept. The "Not cross-checked" gaps bullet
  replaced with the reconciliation record, including the PF-callouts caveat.
- dist/ rebuilt; verify scripts repointed at v4 / 12-unclear / 0.8 / 0.4.

## Verification transcript

```
$ python3 build_scripts/apply_crosscheck_upgrades.py   (already applied; shown for the record)
$ python3 build_scripts/build_standalone.py
limitations.html: 160 entries from data/limitations.json -> dist/limitations.html (149729 bytes)
memory-items.html: 11 entries from data/memory_items.json -> dist/memory-items.html (85807 bytes)
copied assets/icons/icon-180.png -> dist/assets/icons/icon-180.png
copied site.webmanifest -> dist/site.webmanifest
EXIT=0
$ python3 build_scripts/verify/check_embedded_data.py
dist/memory-items.html: 11 entries embedded; every entry == memory_items_v4.json; repo data/memory_items.json == v4: True
  v2 -> v4: actions changed on ['mi-vis-06', 'mi-vis-07', 'mi-vis-08', 'mi-vis-10', 'mi-vis-11']; 13 box-break sentinels; relearn flags on ['mi-vis-06', 'mi-vis-07', 'mi-vis-08', 'mi-vis-10', 'mi-vis-11']
  no embedded newlines remain in any action line
dist/limitations.html: 160 items embedded; every item == limitations_v3.json; 148 VERIFIED / 12 UNCLEAR
  refs with backslash-underscore: 0; items with corroboration: 13; with audit: 19
EXIT=0
$ bash build_scripts/verify/node_check_scripts.sh  (tail)
8
EXIT=0
$ python3 build_scripts/verify/static_constraints.py
limitations.html: 62585 bytes (engine, must be < 100000: True); em dash=0, &mdash;=0, localStorage/sessionStorage=0, private-use chars=0, backslash-u / backslash-x in JS=0, external src/href (http, https, protocol-relative)=0, fetch calls other than the relative data fetch=0, raw hex outside the palette block (comments ignored)=0 -> PASS
memory-items.html: 73365 bytes (engine, must be < 100000: True); em dash=0, &mdash;=0, localStorage/sessionStorage=0, private-use chars=0, backslash-u / backslash-x in JS=0, external src/href (http, https, protocol-relative)=0, fetch calls other than the relative data fetch=0, raw hex outside the palette block (comments ignored)=0 -> PASS
dist/limitations.html: 149729 bytes; em dash=0, &mdash;=0, localStorage/sessionStorage=0, private-use chars=0, backslash-u / backslash-x in JS=0, external src/href (http, https, protocol-relative)=0, fetch calls other than the relative data fetch=0, raw hex outside the palette block (comments ignored)=0 -> PASS
dist/memory-items.html: 85807 bytes; em dash=0, &mdash;=0, localStorage/sessionStorage=0, private-use chars=0, backslash-u / backslash-x in JS=0, external src/href (http, https, protocol-relative)=0, fetch calls other than the relative data fetch=0, raw hex outside the palette block (comments ignored)=0 -> PASS
STATIC CONSTRAINTS: ALL PASSED
EXIT=0
$ python3 build_scripts/verify/pass5_polish_checks.py  (tail)
mode segment after Whole procedure: ['true', 'false', 'whole'] PASS
versions: 0.8 0.4 FAIL
POLISH CHECKS: 1 FAILED (stale version expectation in the check itself; fixed and re-run below)
EXIT=1
$ python3 build_scripts/verify/pass4_visual_checks.py  (tail)
[memory-items.html phone] gutter marks after reveal (only the cursor line carries one): ['grade'] PASS
VISUAL CHECKS: ALL PASSED
EXIT=0
$ python3 build_scripts/verify/playwright_smoke.py  (tail)
           ^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError
EXIT=1
$ http server + verify_engine_and_dist.py
[http engine memory-items.html] data=11 (want 11) booted=True console errors=0 [] reveal+grade={'revealed': True, 'counts': {'got': 9, 'missed': 0}, 'idx': 0, 'phase': 'drill'} PASS
[file:// engine limitations.html] card says: 'Data not loadedOpen the standalone build (dist/) for offline use, or serve this folder over http.'
[file:// engine memory-items.html] card says: 'Data not loadedOpen the standalone build (dist/) for offline use, or serve this folder over http.'
ENGINE/DIST CHECKS: ALL PASSED
EXIT=0 (server killed)
$ python3 build_scripts/verify/pass3_runtime.py  (summary)
EXIT=0
**Checks recorded: 2057. Pass: 2057. Fail: 0. States scanned for text integrity and overflow: 2069.**
$ wc -c limitations.html memory-items.html dist/*.html data/limitations.json data/memory_items.json
 62585 limitations.html
 73365 memory-items.html
149729 dist/limitations.html
 85807 dist/memory-items.html
 94921 data/limitations.json
 15485 data/memory_items.json
481892 total
$ git hash-object ...
d1fadb8b96aae873bb22c8694f8a3b24602c3812  limitations.html
d02274c02ed28a84cb5a8a79690a9dfae84fb06e  memory-items.html
b0efd1a1a3cd14fa4c235fcd781d6f7acaf14003  data/limitations.json
b47c02ea5f1351970f9822b35f7e1724100ebd69  data/memory_items.json

$ re-run after updating the two version expectations in the check scripts
versions: 0.8 0.4 PASS
POLISH CHECKS: ALL PASSED
EXIT=0
ALL PLAYWRIGHT CHECKS PASSED
EXIT=0
```


---

# Addendum 2 and envelope recovery (2026-09-02)

Inputs: `data/limitations_ADDENDUM2.json` (5 items), its notes,
`law_pages_VISUAL.md`, `ETOPS_quiz_FOM_CHECK.md`. limitations.html is 0.9.

- `build_scripts/merge_addendum2.py` merged the 5 addendum items into
  `data/limitations_v4.json` (165 items, 153 VERIFIED / 12 UNCLEAR), copied
  to `repo/data/limitations.json`. Adjustments: lim-add-01 (max TO and LDG
  altitude 12,500 ft) upgraded to VERIFIED on the visual read of the rendered
  envelope chart (pdf p3762), corroboration + audit recorded, limit cleaned to
  "12,500 ft"; its source-text slot carries a bracketed visual-read
  transcription because the chart has no extractable text (verbatim null broke
  the harness and rendered an empty source block). lim-add-03/04 (RAT 140 kt,
  APU battery start 25,000 ft) reclassified system "Reference (AFM
  procedures)" with the procedure-note caveat. The addendum's PRC ref carried
  one em dash; stripped to a comma at merge (transport rule).
- Gaps panel: environmental envelope moved to the recovered panel with the
  full corner list; genuinely still missing are the CG envelope and VA only.
  The APU operational envelope bullet stays (still graphics-only).
  Scope bullet and AFM footer line updated for the new sources.
- Provenance lint clean (181 items over 3 banks). Grounding flags 9 items,
  byte-identical to the v3 run: 7 UNCLEAR table items by design plus
  lim-air-02/08 ("Simultaneous use prohibited" paraphrase); all 5 addendum
  items grounded. Nothing new introduced.
- Harness counts (160, 139, 17 chips, x159 walks) now derive from the data.
- memory-items untouched (0.4). ETOPS_quiz_FOM_CHECK.md required no page
  change: it completes the crosscheck's NEEDS FOM CHECK rows and confirms the
  one stale finding already recorded.

## Verification transcript

```
$ python3 build_scripts/merge_addendum2.py
limitations_v4.json: 165 items, 153 VERIFIED / 12 UNCLEAR; copied to repo/data/limitations.json
EXIT=0
$ python3 build_scripts/provenance_lint.py  (tail)
provenance lint: 181 items across 3 files; 0 errors in 0 files.
EXIT=0
$ python3 build_scripts/verify_grounding.py data/limitations.json  (tail)
grounding check: 165 items scanned, 165 with src='manual', 9 ungrounded (threshold 0.60).
EXIT=1 (9 flagged, all pre-existing in v3: 7 UNCLEAR table items by design plus lim-air-02/08 paraphrase; all 5 addendum items grounded)
$ python3 build_scripts/build_standalone.py
limitations.html: 165 entries from data/limitations.json -> dist/limitations.html (155982 bytes)
memory-items.html: 11 entries from data/memory_items.json -> dist/memory-items.html (85807 bytes)
copied assets/icons/icon-180.png -> dist/assets/icons/icon-180.png
copied site.webmanifest -> dist/site.webmanifest
EXIT=0
$ python3 build_scripts/verify/check_embedded_data.py
dist/memory-items.html: 11 entries embedded; every entry == memory_items_v4.json; repo data/memory_items.json == v4: True
  v2 -> v4: actions changed on ['mi-vis-06', 'mi-vis-07', 'mi-vis-08', 'mi-vis-10', 'mi-vis-11']; 13 box-break sentinels; relearn flags on ['mi-vis-06', 'mi-vis-07', 'mi-vis-08', 'mi-vis-10', 'mi-vis-11']
  no embedded newlines remain in any action line
dist/limitations.html: 165 items embedded; every item == limitations_v4.json; 153 VERIFIED / 12 UNCLEAR
  refs with backslash-underscore: 0; items with corroboration: 14; with audit: 22
EXIT=0
$ bash build_scripts/verify/node_check_scripts.sh | grep -c OK
8
$ python3 build_scripts/verify/static_constraints.py
limitations.html: 63435 bytes (engine, must be < 100000: True); em dash=0, &mdash;=0, localStorage/sessionStorage=0, private-use chars=0, backslash-u / backslash-x in JS=0, external src/href (http, https, protocol-relative)=0, fetch calls other than the relative data fetch=0, raw hex outside the palette block (comments ignored)=0 -> PASS
memory-items.html: 73365 bytes (engine, must be < 100000: True); em dash=0, &mdash;=0, localStorage/sessionStorage=0, private-use chars=0, backslash-u / backslash-x in JS=0, external src/href (http, https, protocol-relative)=0, fetch calls other than the relative data fetch=0, raw hex outside the palette block (comments ignored)=0 -> PASS
dist/limitations.html: 155982 bytes; em dash=0, &mdash;=0, localStorage/sessionStorage=0, private-use chars=0, backslash-u / backslash-x in JS=0, external src/href (http, https, protocol-relative)=0, fetch calls other than the relative data fetch=0, raw hex outside the palette block (comments ignored)=0 -> PASS
dist/memory-items.html: 85807 bytes; em dash=0, &mdash;=0, localStorage/sessionStorage=0, private-use chars=0, backslash-u / backslash-x in JS=0, external src/href (http, https, protocol-relative)=0, fetch calls other than the relative data fetch=0, raw hex outside the palette block (comments ignored)=0 -> PASS
STATIC CONSTRAINTS: ALL PASSED
EXIT=0
$ python3 build_scripts/verify/pass5_polish_checks.py  (tail)
POLISH CHECKS: ALL PASSED
EXIT=0
$ python3 build_scripts/verify/pass4_visual_checks.py  (tail)
VISUAL CHECKS: ALL PASSED
EXIT=0
$ python3 build_scripts/verify/playwright_smoke.py  (tail)
ALL PLAYWRIGHT CHECKS PASSED
EXIT=0
$ http fetch check
[file:// dist limitations.html] data=165 (want 165) booted=True console errors=0 [] reveal+grade={'revealed': False, 'counts': {'got': 1, 'missed': 0}, 'idx': 1, 'phase': 'drill'} PASS
[file:// dist memory-items.html] data=11 (want 11) booted=True console errors=0 [] reveal+grade={'revealed': True, 'counts': {'got': 1, 'missed': 0}, 'idx': 0, 'phase': 'drill'} PASS
[http engine limitations.html] data=165 (want 165) booted=True console errors=0 [] reveal+grade={'revealed': False, 'counts': {'got': 1, 'missed': 0}, 'idx': 1, 'phase': 'drill'} PASS
[http engine memory-items.html] data=11 (want 11) booted=True console errors=0 [] reveal+grade={'revealed': True, 'counts': {'got': 7, 'missed': 0}, 'idx': 0, 'phase': 'drill'} PASS
[file:// engine limitations.html] card says: 'Data not loadedOpen the standalone build (dist/) for offline use, or serve this folder over http.'
[file:// engine memory-items.html] card says: 'Data not loadedOpen the standalone build (dist/) for offline use, or serve this folder over http.'
ENGINE/DIST CHECKS: ALL PASSED
EXIT=0 (server killed)
$ pass3_runtime.py  (summary; run above)
**Checks recorded: 2037. Pass: 2037. Fail: 0. States scanned for text integrity and overflow: 2117.**
$ header render check
headSub: A330P FCOM R17, issue 15 MAY 26 · 165 items (153 verified, 12 unclear) · active recall, no multiple choice
recovered panel mentions 12,500 ft and envelope: True
gaps: still missing CG+VA only: True | 12 of the 165: True
footer: Generated 2026-09-01 · page version 0.9 · 165 items from limitations_v4.json, verified FCOM set merged with both AFM addenda, the pass-2 condition audit, the training-document cross-check and the visual envelope read; no limit value changed by any audit; 153 verified, 12 unclear
$ wc -c limitations.html data/limitations.json dist/limitations.html
 63435 limitations.html
100705 data/limitations.json
155982 dist/limitations.html
320122 total
$ git hash-object limitations.html data/limitations.json
f6943e3e0ec14d6497be969997315b0c1c473f1b  limitations.html
d0ba0492a6f7b91efa528dbbc37f84f0f59ab768  data/limitations.json
```

## 2026-09-02: fom-delta.html, the FOM 123.1 to 125.1 delta review page

Third study page. Engine page fetches `data/fom_delta.json` (52 substantive A330-relevant / fleet-common
changes structured from `FOM_DELTA_123.1_to_125.1.md` by `build_scripts/make_fom_delta_dataset.py`;
quotes verbatim from the review, 28 items are Diff only because revisions 124 to 124.2 published no
Revision Highlights). Two modes: Review (grouped by FOM chapter, before/after side by side, search,
scope/source filters) and Drill (the review's 18 recall Q&As, same keys as the sibling pages; V shows
the underlying change). Banner names the diff-plus-highlights method; footer META: FOM 125.1 (8/12/26)
vs 123.1 (4/27/26), generated 2026-09-02, version 0.1. Added to `build_standalone.py` (marker pair
`@@DATA_START fom-delta`), `static_constraints.py`, `node_check_scripts.sh`, `verify_engine_and_dist.py`
(clicks into Drill first; page boots in Review). Own harness: `build_scripts/verify/fom_delta_checks.py`
(dataset schema + grounding, http engine, dist file://, phone 375px, dark, full drill cycle with
re-served misses, offline message on the file:// engine). All checks pass; quote fragments verified
verbatim against the review doc.

```
$ wc -c fom-delta.html data/fom_delta.json dist/fom-delta.html
 45460 fom-delta.html
 69947 data/fom_delta.json
112289 dist/fom-delta.html
$ git hash-object fom-delta.html data/fom_delta.json
1fe275120e4d20ac28b3c95b7957646d68e27eb4  fom-delta.html
b88d87ec0752a98b001a381ad7c0ef07a267d597  data/fom_delta.json
```

## 2026-09-02: index.html, the portal home page and access gate

Single-file portal home served at the repo root by GitHub Pages. Carries the
client-side email gate (honesty layer, not security): any address matching
`^[^@\s]+@alaskaair\.com$` case-insensitively unlocks, one cookie
(`a330portal=ok`, 180 days, path=/, SameSite=Lax) remembers the answer. No
localStorage/sessionStorage anywhere. Unlocked view is the build-order card
menu: three live cards (Limitations Drill, Memory Items Drill, FOM Delta
Review) plus five greyed not-built cards (Flows, Systems Oral Bank with the
"scope: LO Rev 7, 67 areas" subtitle, Triggers, Games, Podcast).

Nothing volatile is hardcoded: card counts are fetched at runtime from
data/limitations.json (165 items / VERIFIED count 153), data/memory_items.json
(procedures counted by [MEM]-stripped title, same merge as the drill page, so
the eleven entries render as 10 procedures), and data/fom_delta.json (52
changes); the footer manual line renders from manuals.json (A330P FCOM,
A330P QRH, FOM). A yellow notice replaces the counts when the fetches cannot
run (file://). Header references assets/icons/icon-180.png with a quiet
hidden-on-404 fallback. Palette is the same inlined Hawaiian token block as
the siblings; coral stays decorative. Generated 2026-09-02, index version 1.0,
20.6 KB.

## Verification transcript

- `node --check` on the page's single script block: clean.
- Static sweep: no em dashes, no private-use characters, no backslash-u
  escapes, no external src/href, no hardcoded revision strings (R17, R35,
  FOM 125.1, manual dates all absent from the HTML).
- Playwright (chromium) over a local http server, 26/26 PASS:
  - Un-cookied visit shows the gate, menu hidden, email field focused with
    no scroll.
  - `ryan@hawaiianair.com` + Enter: blocked, plain error shown, menu stays
    hidden. `test@AlaskaAir.com` + Enter: unlocks (case-insensitive).
  - Cookie `a330portal=ok` set, expiry measured 180.0 days; storage empty.
  - Reload lands on the menu directly (cookie persisted); "Lock this device
    again" clears the cookie and returns to the gate.
  - Fetched counts render: "165 items · 153 verified", "10 procedures,
    FCOM [MEM] verified", "52 changes, 123.1 to 125.1". Footer from
    manuals.json: "A330P FCOM R17 (15 MAY 26) · A330P QRH R35 (26 JUN 26) ·
    FOM 125.1 (8/12/26)"; stamp "Generated 2026-09-02 · index version 1.0".
  - All three live links present, five not-built cards, oral-bank subtitle.
  - Zero console errors desktop-light and phone-dark (390x844); no
    horizontal scroll on phone; dark body background applied.
- Screenshots eyeballed: gate (desktop light) and full menu (phone dark)
  both clean, icon tile renders in the header.

## 2026-09-02: oral-prep.html, the oral-scope study page

Engine page over data/oral_scope.json (67 areas / 278 objectives / 86 numeric
claims from the HAL A330 Student Oral Exam Learning Objectives Rev 7,
04/06/23). WALK mode renders the 67 areas in the file's own order, the exam's
cockpit walk (verified against AREAS order at runtime), each expandable to its
objectives with FCOM refs plus a per-area numeric-claims block; a session-only
progress tick per area (in-memory, banner and status line both say it resets
on reload by design; no storage of any kind). QUIZ mode is active recall over
all 278 objectives: prompt is the area plus an "Explain:" stem with every
number masked to blanks, reveal shows the full objective, its FCOM ref and any
matching claim badges, self-graded, no multiple choice, missed items re-served
by round until clean; pool selector honours the walk ticks (all / not yet
ticked). Claim rendering: VERIFIED CURRENT (23) show their cross-check source;
UNVERIFIED (63) carry "NOT YET VERIFIED against current manuals, treat the
number as suspect"; the three cross-check conflicts (33,000 lb unusable vs QRH
gravity-feed 4,400/inner, 800 psi oxygen gate vs QRH 600/300, 195-min ETOPS
cargo fire pending FOM check) carry a CONFLICT badge with a one-line
explanation, matched by area id + claim substring. Claim-to-objective
attachment is number+unit bigram matching with a bare-number fallback for
otherwise-orphaned claims (85/86 attach by bigram, the last by fallback).
Banner: LO Rev 7 is a three-year-old training reference, FCOM/QRH/FOM win
every conflict, values being verified progressively. Footer META: LO Rev 7
(04/06/23) + FCOM R17 / QRH R35 identity, verified-count line computed from
the data, generated 2026-09-02, page version 0.1. Same inlined Hawaiian
palette, favicon, icon links, keyboard model and file:// fallback as the
siblings. build_standalone.py extended with the oral-prep page and an
entry_count() helper (oral_scope.json is an object with meta + areas, not a
flat list); static_constraints.py now sweeps oral-prep.html and its dist.

## Verification transcript (oral-prep)

- `node --check` on both script blocks: clean.
- Static sweep (static_constraints.py, now 8 files): all PASS; engine
  47,854 bytes (< 100 KB), dist 111,477 bytes, no em dashes, no PUA, no
  backslash-u, no storage, no external src/href, only the data/ fetch,
  no hex outside the palette block.
- Own harness `build_scripts/verify/oral_prep_checks.py`, 114/114 PASS
  across http engine, file:// dist, http phone (375px, no horizontal
  overflow), file:// dist dark (body ground rgb(21,19,28)), and the
  file:// engine offline message. Covers: dataset schema (67/278/86,
  23 verified / 63 unverified, the three conflict claims present), banner
  and footer META text, walk order vs the file, expand/collapse, 278 li,
  badge counts (23 ver / 63 unv / 3 CONFLICT with the 4,400 lb, 600/300
  psi and FOM-check explanations visible), verified claims all show a
  source, tick -> progress + done styling, quiz queue 278, masked prompt,
  reveal shows the full objective + FCOM ref, keyboard reveal/grade, full
  cycle with 2 seeded misses re-served to done (got 278 / missed 2 /
  round 2), restart, unticked pool = 276 after one tick, zero console
  errors on every run.
- Screenshots eyeballed: walk light desktop (FUEL expanded: CONFLICT +
  NOT YET VERIFIED + VERIFIED CURRENT rows all render), quiz phone dark
  (prompt + reveal + footer) both clean.

```
$ wc -c oral-prep.html data/oral_scope.json dist/oral-prep.html
 47854 oral-prep.html
 75130 data/oral_scope.json
111477 dist/oral-prep.html
$ git hash-object oral-prep.html data/oral_scope.json
9218ab5a872b0002b35a4e34c9b0bfd80a044733  oral-prep.html
3dc49de017636fe207ea1088981283c67d0dba33  data/oral_scope.json
```
