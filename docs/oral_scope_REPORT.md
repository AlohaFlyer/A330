# Oral Scope Dataset Report

**Dataset:** `/home/claude/a330/repo/data/oral_scope.json`
**Source:** A330 Student Oral Exam Learning Objectives Rev 7, Hawaiian Airlines training department, 04/06/23 (41 pages), extracted at `/home/claude/a330/training/Student_Oral_Learning_Objectives_Rev_7.md`
**Numeric adjudication source:** `/home/claude/a330/data/limitations_CROSSCHECK.md` section 1B (2026-09-02)
**Built:** 2026-09-02

## Counts

- **Areas:** 67, in the document's own order (the oral's cockpit walk, starting at the left upper corner of the overhead panel and ending at the pedestal/rudder trim). Every area has at least one printed FCOM/QRH/FCTM reference; none needed a "none printed" marker.
- **Objectives:** 278 (faithful summaries of the doc's bullets; numbers kept exactly as the doc states them).
- **Numeric claims:** 86
  - UNVERIFIED: 63 (mostly FCOM DSC systems-chapter values not in the local verified slice)
  - VERIFIED-CURRENT: 23 (adjudicated by the cross-check against limitations_v3 / AFM / QRH / FCTM / PRC extracts)
  - STALE: 0 - the cross-check found no LO-doc value that contradicts current sources. The only stale item in that whole cross-check pass was in the ETOPS quiz (OpSpec B342/C070 adequate-airport pointer), which is not part of this document.
- **maps_to:** systems_quiz 57, flows 5 (RCDR, LIGHTS, CVR Panel, ACP 3, TRIPLE INDICATOR), limitations 4 (WIPERS, APU, MAINTENANCE PANEL oil, CHRONO), memory_items 1 (PARKING BRAKE / LOSS OF BRAKING).

## Densest panels (objectives + numeric claims)

1. **FUEL** (oral-26): 13 objectives, 7 claims - tank capacities, filling and feed order, trim tank transfer logic, manual transfer Pbs, imbalance limits.
2. **APU** (oral-20): 11 objectives, 8 claims - the full operating envelope ladder plus starter, oil, and fuel-supply logic; the most limitation-dense area.
3. **AIR** (oral-24): 10 objectives, 7 claims - bleed logic, pack/zone controller failure values, both pack-flow-selector fleets, hot air, RAM AIR.
4. **ELECTRICAL** (oral-25): 11 objectives, 5 claims - power hierarchy, battery voltage checks, IDG, hot battery bus.
5. **HYDRAULICS** (oral-27): 11 objectives, 4 claims - three-system architecture, electric pump auto-run logic, RAT.
6. **ADIRS** (oral-03): 9 objectives, 5 claims - alignments, IR faults, GPIRS bias, IRS-only RNP time limits.
7. **APU Fire Panel** (oral-04): 8 objectives, 4 claims.
8. **EMER ELEC PWR** (oral-11): 7 objectives, 4 claims - Big Green / Little Green bus and display ladders.
9. **FMA** (oral-37) and **MODE REVERSIONS** (oral-38): 8 objectives each - the doc's autoflight behavioral core.
10. **FLAPS** (oral-64): 4 long objectives, 4 claims - ARS, load relief, alpha/speed lock, aileron droop, all number-heavy.

## Ten areas a requalifying FO most plausibly gets probed on first

Justified from the document itself: its intro names five "basic parameters" (find answers on the iPad, know all Limitations, know all Memory Items, know OEBs big-picture, know the flight control laws), it states the exam walks the cockpit starting at the left upper overhead corner, and its own emphasis shows in where it spends pages.

1. **ADIRS (oral-03)** - the first substantive panel in the stated walk order and one of the longest treatments in the doc (alignment types, IR fault types, GPIRS bias logic, the RNP 6.2/5.7 hr limits). An examiner following the doc's own sequence lands here within the first minutes.
2. **APU (oral-20)** - the doc's densest pure-limitations area (the whole altitude envelope, starter limits, low-oil allowance), squarely inside basic parameter 2, "know all Limitations."
3. **EMER ELEC PWR (oral-11)** - the doc devotes two full pages to Big Green / Little Green, surviving busses, and surviving displays; classic emergency-config probe and the doc explicitly ties it to the QRH summary.
4. **ELECTRICAL (oral-25)** - power hierarchy recitation plus three battery-voltage gates the doc frames as preflight checks; feeds both systems knowledge and the preflight flow.
5. **FUEL (oral-26)** - the single largest area in the doc (capacities, feed sequence, trim tank CG logic, imbalance limits); imbalance is also a limitations-chart item, hitting basic parameter 2's "charts: just know how to use them."
6. **HYDRAULICS (oral-27)** - the doc's electric-pump auto-run logic (green 25 s, blue rudder case, yellow flap/cargo-door case) is exactly the kind of "why did that pump start" question the write-up is built to answer, and the RAT ties into the emergency-generator story.
7. **Flight Control Computers + TURB DAMP (oral-06, oral-05)** - basic parameter 5 is "know the flight control laws"; the doc's law content lives in the PRIM/SEC area (Normal/Alternate/Direct, one computer to land).
8. **FIRE (oral-28)** - fire loop logic, Pb consequences, and the counted test indications (12 lights plus CRC) are formatted as recite-back answers; parallels the APU fire panel asked earlier in the walk.
9. **PARKING BRAKE (oral-66)** - basic parameter 3 is "know all Memory Items," and this is the doc's one explicit memory-item hook (LOSS OF BRAKING: accumulator, 7 applications, delay braking).
10. **FMA / MODE REVERSIONS (oral-37, oral-38)** - eight objectives each of exact FMA recitation and reversion triggers; the doc's "triple click = Look Look Look" mnemonic marks it as an emphasized teach point for anyone re-qualifying on autoflight behavior.

## Caveats carried into the dataset

- The meta caveat states it plainly: scope is authoritative, values are not. 63 of 86 numeric claims are UNVERIFIED because they live in FCOM DSC systems chapters not present in the current verified local slice.
- Two UNVERIFIED claims carry explicit conflict flags to resolve at the next FCOM pass: the doc's **33,000 lbs unusable with center pumps inoperative** (QRH gravity-feed summary shows a different figure, 4,400 lbs per inner tank) and the doc's **800 psi oxygen mask-check gate** (current QRH advisory gates are 600/300 psi; the 800 figure is a PRO-NOR-SOP-06 preflight criterion, not yet sighted).
- The **195 min ETOPS** cargo-fire figure is UNVERIFIED pending a FOM check (the 260 min bottle-discharge time itself is AFM-verified).
- One verified item carries a nuance note: takeoff alert inhibition (oral-52) - the manual starts the inhibit at 80 kt, the LO doc says "from takeoff thrust."
- The doc is Rev 7 (04/06/23) and pre-dates FOM 125.1, but nothing in it contradicted current sources in the cross-check.
