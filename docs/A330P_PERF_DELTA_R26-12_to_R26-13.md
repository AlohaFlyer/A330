# A330 Passenger Performance Handbook delta: R26-12 to R26-13

Sweep run 16 OCT 26 (Hark, branch `hark/sweep-2026-10-16`) per `docs/REVISION_PROCESS.md` steps 3 to 7.
New: `A330P_PERF_R26-13.pdf` (Drive id `1y6j1RSkUquoKJQhhgPJyM2unRxHu5Chh`, 436 PDF pages), revision date
October 02, 2026. Prior: `A330P_PERF_R26-12` (Drive `.md` extract `10zWZlP5vFpCKfDzKbTB5wP9NDcAkrnk0`, PDF in
`_superseded`). PAX book only; nothing here is applied to freighter content.

Method: the book's own Permanent Revision #26-13 Transmittal Page, then a whitespace-normalized line diff of the
R26-12 and R26-13 extracts for chapters 0 to 4 and a per-airport page comparison for the runway analysis section.
Extracts stayed outside the repo.

## 1. Transmittal highlights (#26-13, verbatim summary)

| Pages | Highlight |
|---|---|
| LEP 1 / LEP 4 | replaced |
| 0.1 to 0.2 | Updated table of contents. |
| 2.1 to 2.16 | Added crosswind assumptions. |
| ANC, AKL, AUS, BOS, BNE, FUK, ITO, OGG, KOA, LAS, LIH, LAX, JFK, OAK, MCO, PHX, PDX, SMF, SAN, SFO, SJC, SLC, CTS, SDJ, SYD, HND, NRT runway pages | NOTAM. |
| ADD | HNL 08L-E5360F, 26R-E5360F |
| DESTROY | SJC 12L CRANE, 12R CRANE; SYD 16R-N1738M; NRT 16L CRANE, 34R CRANE |

## 2. What the diff found

### 2.1 General, Takeoff (p2.1) **PAX**
New text after the Flap Retraction Altitude paragraph:

> AeroData engine failure procedures (EFPs) are designed based on the obstacle and wind accountability requirements
> of FAA Advisory Circular 120-91A. The primary EFP design criteria used by AeroData is the Area Analysis Method of
> AC 120-91A which includes margins to account for crosswind effects as well as possible instrument error and
> flight technical error. ... Unless otherwise noted, "climb straight ahead" means climb via runway heading (fly the
> track if able) ... At selected mountainous airports (e.g., RNO, EGE, ASE), a maximum crosswind value or crosswind
> chart is applied based on terrain along the flight path.

Pages 2.2 to 2.16 re-paginated (an INTENTIONALLY BLANK page dropped, table header re-flow). No number in chapters
2 or 4 changed. The runway analysis pages changed only at the airports the transmittal lists (NOTAM lists and the
dependent weight tables), plus the two added HNL intersection pages and the destroyed pages.

## 3. Re-verify checklist

- Citation index rebuilt 16 OCT 26: `A330P_PERF` has **no citations** in the index.
  `python3 build_scripts/manual_diff.py A330P_PERF ...` exits 3 (manual not in index) -> **0 items**.
- Belt-and-braces grep of every `data/*.json`, `*.html` and `*.js` for AeroData, Performance Handbook, takeoff
  report, radio revision, EFP, engine failure procedure, climb straight ahead, V1std, AC 120-91A. Every hit cites the
  FCOM (PER-ARD, PRO-NOR-SOP) or the FOM, not this book. Nearest content: oe-055 (sop, EOSID on the TPR/TLR), oe-105
  (sop, FOM 5.4.5 runway analysis), oe-092 note (`what AeroData uses`, wet/contaminated crosswind table, FCOM
  LIM-AG-OPS). None conflicts with the new p2.1 text.

Corrections: none. Flags: none.

## 4. Podcast (330 Flight Deck Notes)

Scripts ep1 to ep20 and `podcast.html` grepped for performance handbook facts. The only related lines (ep7 line 122
`Off the AeroData T-P-R or T-L-R`; ep3/ep5/ep6 `preliminary takeoff performance`) are FCOM SOP facts and still
correct. Nothing to flag.

## 5. Stamp

`last_vetted` for `A330P_PERF` set to `16 OCT 26`: 0 checklist items, no open flags.
Follow-up for Ryan: rebuild the Manuals search index from `A330P_PERF_R26-13.md` (`build_manuals_index.py` now
points at it) and re-upload to R2.
