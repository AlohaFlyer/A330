# A330 Freighter Performance Handbook delta: R26-10 to R26-13

Sweep run 16 OCT 26 (Hark, branch `hark/sweep-2026-10-16`) per `docs/REVISION_PROCESS.md` steps 3 to 7.
New: `A330F_PERF_R26-13.pdf` (Drive id `1oQcAHEGuh3LKVM4_w2_lYPerbjFXuAMe`, 222 PDF pages), revision date
October 02, 2026. Prior on file: `A330F_PERF_R26-10` (Drive `.md` extract `14eP_b3JgtSFQXopDNqP159m1lJHki3C8`,
PDF in `_superseded`). Freighter book only; nothing here is applied to PAX content.

Gap: this jump spans three revisions. The R26-13 book carries only the #26-13 transmittal. No transmittal for
#26-11 or #26-12 is in Drive, so their changes were found by diffing R26-10 against R26-13, not read off the
publisher's list.

## 1. Transmittal highlights (#26-13, verbatim summary)

| Pages | Highlight |
|---|---|
| LEP 1 / LEP 2 | replaced |
| 0.1 to 0.2 | Updated table of contents. |
| 2.1 to 2.16 | Added crosswind assumptions. |
| AUS, CVG, ITO, IAH, OGG, KOA, LIH, JFK, ONT, PDX, RFD, SMF runway pages | NOTAM. |
| ADD | IAH 33L CRANE |
| DESTROY | ONT 08L CRANE, 08R CRANE |

## 2. What the R26-10 to R26-13 diff found

### p2.1 General, Takeoff **FRTR**
Same new paragraph as the PAX book: AeroData EFPs built to AC 120-91A (Area Analysis Method with crosswind, instrument
and flight technical error margins; Flight Track Analysis when required); "climb straight ahead" means runway heading
(fly the track if able); at selected mountainous airports (RNO, EGE, ASE) a maximum crosswind value or chart applies.

### p2.8 V1STD DEFINITION (added in #26-11 or #26-12) **FRTR**
> AeroData uses a V1 policy called V1std when a range of V1 is available for selection between V1min and V1max for a
> given takeoff weight. V1std is defined as V1max minus 5 knots, not to go below V1min.

The PAX book already carried this paragraph at R26-12.

### Runway analysis pages **FRTR**
Pages differ at AUS, CVG, HNL, IAH, ILN, ITO, JFK, KOA, LIH, OGG, ONT, PDX, RFD, RIV, SAT, SBD, SEA, SMF (NOTAM
lists, `Rules FAA` dates, dependent weight and speed tables). Crane page add/destroy per the transmittal.

## 3. Re-verify checklist

- Citation index rebuilt 16 OCT 26: `A330F_PERF` has **no citations** in the index.
  `python3 build_scripts/manual_diff.py A330F_PERF ...` exits 3 (manual not in index) -> **0 items**.
- Belt-and-braces grep of `data/*.json`, `*.html`, `*.js` for V1std, AC 120-91A, climb straight ahead, EFP and
  AeroData: no `fleet: frtr` item states a freighter performance handbook fact.

Corrections: none. Flags: none.

## 4. Podcast (330 Flight Deck Notes)

Ep4 (Limitations, Freighter Numbers) states freighter FCOM R10 / AFM crosswind limits (32 kt takeoff, 40 kt demonstrated
landing), not performance handbook facts. Nothing to flag.

## 5. Stamp

`last_vetted` for `A330F_PERF` set to `16 OCT 26`: 0 checklist items, no open flags. Caveat above: #26-11 and
#26-12 were scoped by diff, not by transmittal.
