# memory_items_CROSSCHECK.md

# A330 Memory Items — Cross-check of Personal/Training Docs vs Current Verified Manual Set

**Date:** 2026-09-02
**Ground truth:** `/home/claude/a330/data/memory_items_v3.json` — 11 entries / 10 procedures, every `actions` line transcribed verbatim from rendered A330P FCOM R17 / QRH R35 pages. **The manual always wins.**
**Compared against:**
- HIS DOC — `/home/claude/a330/training/A330_Memory_Items_docx.md` (personal study file, age unknown)
- LO DOC — `/home/claude/a330/training/Student_Oral_Learning_Objectives_Rev_7.md` (Rev 7, 04/06/23)
- 2023 GOUGE — `/home/claude/a330/training/CAPT_UPGRADE_ORAL_2023_20240822_20_19_43.md`

**Method note:** every adjudication below quotes both sides verbatim. Nothing is judged from general Airbus knowledge. Where his doc carries content the verified set does not include (e.g. PF callout wording), it is marked **NOT IN CURRENT VERIFIED SET**, not judged.

Classification key: **IDENTICAL** · **WORDING DRIFT** (same action, different words) · **SUBSTANTIVE CHANGE** (different action, value, order, structure, or condition) · **REMOVED FROM CURRENT** (in his doc, not in current) · **NEW IN CURRENT** (in current, absent from his doc).

---

## 1. Procedure-level reconciliation

| # | Current [MEM] procedure (v3) | Ref | In his doc? | His naming | Verdict |
|---|---|---|---|---|---|
| 1 | [MEM] EMER DESCENT (FCOM PRO-ABN-MISC P1/26 + QRH 22.02A, identical) | PRO-ABN-MISC-00012261.0001001 / ABN-22-00010585.0001001 | YES | "EMERGENCY DESCENT" | Matches, minor drift |
| 2 | [MEM] STALL RECOVERY | PRO-ABN-MISC-00013664.0002001 | YES | "STALL RECOVERY" | Matches, minor drift |
| 3 | [MEM] STALL WARNING AT LIFTOFF | PRO-ABN-MISC-00013665.0002001 | YES | "STALL WARNING AT LIFTOFF" | Matches, minor drift |
| 4 | UNRELIABLE SPEED INDICATION (QRH 23.03A; FCOM TOC lists "[MEM] Unreliable Speed Indication") | ABN-23-A-00017854.0001001 | YES | "UNRELIABLE SPEED INDICATION" | Matches, drift |
| 5 | [MEM] LOSS OF BRAKING | PRO-ABN-BRAKES-00010803.0001001 | YES | "LOSS OF BRAKING" | **2 substantive line changes** |
| 6 | [MEM] TAWS CAUTION | PRO-ABN-SURV-AA-00026795.0001001 | PARTIAL | folded into "EGPWS WARNINGS / CAUTIONS" | **Substantive — his doc has no caution-specific structure at all** |
| 7 | [MEM] TAWS WARNING | PRO-ABN-SURV-00026799.0001001 | PARTIAL | folded into "EGPWS WARNINGS / CAUTIONS" | Substantive (BANK line) + structure |
| 8 | [MEM] TCAS CAUTION - TRAFFIC ADVISORY | PRO-ABN-SURV-00025042.0001001 | **NO** | — | **MISSING from his doc** |
| 9 | [MEM] TCAS WARNING - RESOLUTION ADVISORY | PRO-ABN-SURV-00011464.0005001 | PARTIAL | "TCAS WARNINGS" | **His doc has only the first 2 of ~10 current lines** |
| 10 | [MEM] WINDSHEAR WARNING - REACTIVE WINDSHEAR | PRO-ABN-SURV-00012300.0001001 | YES | "REACTIVE WINDSHEAR WARNING" | **3 current lines missing from his doc** |

### In his doc but NOT a current [MEM] procedure

| His procedure | His content (verbatim) | Verdict |
|---|---|---|
| "SMOKE / FUMES / AVIONICS SMOKE -- No callout -- (QRH-PRO-SMOKE)" | "CREW OXYGEN MASKS ... USE / 100% / EMERG" | **NOT IN CURRENT VERIFIED SET.** The verified v3 set (which claims completeness at 10 [MEM] procedures) contains no smoke/fumes memory item. Do not drill this as a memory item without confirming against the current QRH smoke procedure. |
| PF callouts in every title line ("LOSS OF BRAKING", "PULL UP, TOGA", "STALL, I HAVE CONTROL", "STALL, TOGA 15", "TCAS, I HAVE CONTROL", "UNRELIABLE AIRSPEED", "WINDSHEAR, TOGA") | e.g. `STALL RECOVERY  "STALL, I HAVE CONTROL"` | **NOT IN CURRENT VERIFIED SET.** v3 transcribes FCOM/QRH boxed actions only; it carries no callout column. Callouts are an operator/SOP overlay — verify against current HAL SOPs. The 2023 gouge says the examiner *does* want callouts (see §3). |

**Counts:** Current has 10 procedures. His doc has 9 named procedures, of which 8 map to current ones (his single EGPWS entry maps to two current procedures — TAWS CAUTION + TAWS WARNING — so he effectively covers 8 of 10). **Missing outright: TCAS CAUTION - TA. Missing structurally: TAWS CAUTION. Extra: Smoke/Fumes.**

---

## 2. Line-level diff per procedure (substantive first)

### 2a. [MEM] LOSS OF BRAKING — FCOM R17 PRO-ABN-BRAKES P 1/16 (pdf 2545)

| His line (verbatim) | Current verbatim line(s) | Class |
|---|---|---|
| "PARKING BRAKE……… SHORT & SUCCESSIVE APPLICATIONS" | "If still no braking:" → "PARK BRAKE ... USE" | **SUBSTANTIVE CHANGE.** The current boxed memory line is simply **USE**. "Short & successive applications" is no longer the memory-item wording (it survives as technique guidance in the 2023-era LO doc — see §3 conflict). |
| "ANTI-SKID & NWS……… ORDER OFF" (one line) | Two separate boxed steps with a box break between them: "A/SKID OFF ... ORDER" *(box break)* "A/SKID & N/W STRG ... OFF" | **SUBSTANTIVE CHANGE (structure).** Current splits this into (1) the PF *ordering* A/SKID off, then (2) the switch actually being set OFF — two boxed items, not one merged action. Drilling his one-liner loses the order-then-act sequence. |
| "IF NO BRAKING AVAILABLE:" | "If no braking:" | WORDING DRIFT (condition header) |
| "REVERSE……… MAX" | "REV ... MAX" | WORDING DRIFT |
| "BRAKE PEDALS……… RELEASE" | "BRAKE PEDALS ... RELEASE" | IDENTICAL |
| "BRAKE PEDALS……… PRESS" | "BRAKE PEDALS ... PRESS" | IDENTICAL |
| "MAX BRAKING PRESSURE……… 1,000 PSI" | "MAX BRK PR ... 1000 PSI" | WORDING DRIFT (same value) |
| "IF STILL NO BRAKING:" | "If still no braking:" | IDENTICAL |

### 2b. EGPWS vs [MEM] TAWS CAUTION + [MEM] TAWS WARNING — FCOM R17 PRO-ABN-SURV P 1/8–3/8 (pdf 3209/3211)

His doc has **one** combined procedure:

> `EGPWS WARNINGS / CAUTIONS  "PULL UP, TOGA"  (PRO-ABN-SURV)`
> AP OFF / PITCH PULL UP (full backstick) / THRUST LEVERS TOGA / SPEEDBRAKES CHECK RETRACTED / BANK WINGS LEVEL / DO NOT CHANGE CONFIGURATION (SLATS/FLAPS, GEAR) UNTIL CLEAR OF OBSTACLE

Current has **two** procedures. His block matches the current **[MEM] TAWS WARNING** ("If the TAWS triggers one of the PULL UP alerts:"). Line diff against TAWS WARNING:

| His line | Current verbatim | Class |
|---|---|---|
| "BANK……… WINGS LEVEL" | "BANK ... WINGS LEVEL or ADJUST" | **SUBSTANTIVE CHANGE.** Current permits/directs adjusting bank; his doc locks wings level. |
| (applies his pull-up block to ALL "WARNINGS / CAUTIONS") | Warning block applies only "If the TAWS triggers one of the PULL UP alerts:" | **SUBSTANTIVE CHANGE (condition/structure).** See TAWS CAUTION below. |
| "PITCH……… PULL UP (full backstick)" | "PITCH ... PULL UP" | WORDING DRIFT — "(full backstick)" is his annotation, not in the current boxed line. |
| "AP……… OFF" | "Simultaneously:" → "AP ... OFF" | IDENTICAL (his doc omits the "Simultaneously:" header) |
| "THRUST LEVERS……… TOGA" | "THRUST LEVERS ... TOGA" | IDENTICAL |
| "SPEEDBRAKES……… CHECK RETRACTED" | "SPEED BRAKE LEVER ... CHECK RETRACTED" | WORDING DRIFT |
| "DO NOT CHANGE CONFIGURATION (SLATS/FLAPS, GEAR) UNTIL CLEAR OF OBSTACLE" | "DO NOT CHANGE CONFIGURATION (SLATS/FLAPS, GEAR) UNTIL CLEAR OF OBSTACLE." | IDENTICAL |

**NEW IN CURRENT — the entire [MEM] TAWS CAUTION procedure (nothing in his doc corresponds):**

- Caution alerts ("TERRAIN TERRAIN" – "TOO LOW TERRAIN" – "TERRAIN AHEAD" – "CAUTION TERRAIN" – "OBSTACLE AHEAD" – "CAUTION OBSTACLE"):
  - "During night or IMC conditions:" → the same pull-up block as the warning (AP OFF / PITCH PULL UP / THRUST LEVERS TOGA / SPEED BRAKE LEVER CHECK RETRACTED / BANK WINGS LEVEL or ADJUST / DO NOT CHANGE CONFIGURATION...)
  - "During daylight and VMC conditions, with terrain and obstacles clearly in sight:" → "FLIGHT PATH ... ADJUST" — **NOT a pull-up**.
- "SINK RATE": above 1 000 ft AAL IMC / 500 ft AAL VMC → "FLIGHT PATH ... ADJUST"; below → "GO-AROUND ... CONSIDER"
- "DON'T SINK" → "FLIGHT PATH ... ADJUST"
- "TOO LOW GEAR" or "TOO LOW FLAPS" → "GO-AROUND ... PERFORM"
- "GLIDESLOPE": above 1 000/500 ft → "FLIGHT PATH ... ADJUST"; deliberate below-G/S approach → "G/S MODE ... OFF"; below 1 000/500 ft → "GO-AROUND ... CONSIDER"

Drilling his doc, he would fly a full-backstick TOGA pull-up for a daylight-VMC "SINK RATE" — the current answer is FLIGHT PATH ADJUST (or GO-AROUND, per alert and height).

### 2c. TCAS — [MEM] TCAS CAUTION - TA and [MEM] TCAS WARNING - RA — FCOM R17 PRO-ABN-SURV P 3/8–5/8 (pdf 3211/3212)

His entire entry:

> `TCAS WARNINGS  "TCAS, I HAVE CONTROL"  (PRO-ABN-SURV)`
> AP (if engaged) OFF / BOTH FDs OFF

| Item | Current verbatim | Class |
|---|---|---|
| (absent) | **[MEM] TCAS CAUTION - TRAFFIC ADVISORY:** "Do not perform a maneuver based on a TA alone." | **NEW IN CURRENT / MISSING FROM HIS DOC** (entire procedure; single unboxed line per v3 note). |
| (absent) | RA conditional header: "All RA, except any CLIMB RA during approach in CONF 3 or FULL:" | **NEW IN CURRENT.** His two lines carry no condition. |
| "AP (if engaged)……… OFF" | "AP (if engaged) ... OFF" | IDENTICAL |
| "BOTH FDs……… OFF" | "BOTH FDs ... OFF" | IDENTICAL |
| (absent) | "VERTICAL SPEED ... ADJUST or MAINTAIN" | **NEW IN CURRENT.** The actual RA maneuver line — his doc stops before it. |
| (absent) | "Any CLIMB RA during approach in CONF 3 or FULL:" → "GO-AROUND ... PERFORM" → "VERTICAL SPEED ... MONITOR" | **NEW IN CURRENT.** A whole conditional branch his doc lacks. |
| (absent) | "ATC ... NOTIFY" | NEW IN CURRENT |
| (absent) | "When the "CLEAR OF CONFLICT" aural alert sounds:" → "ATC ... NOTIFY" / "LATERAL AND VERTICAL GUIDANCE ... ADJUST" / "AP/FD ... AS RQRD" | NEW IN CURRENT |
| `"TCAS, I HAVE CONTROL"` callout | — | NOT IN CURRENT VERIFIED SET (no callout column in v3). |

### 2d. [MEM] WINDSHEAR WARNING - REACTIVE WINDSHEAR — FCOM R17 PRO-ABN-SURV P 6/8–7/8 (pdf 3214)

| His line | Current verbatim | Class |
|---|---|---|
| (absent) | "DO NOT CHANGE CONFIGURATION (SLATS/FLAPS, GEAR) UNTIL OUT OF WINDSHEAR." | **NEW IN CURRENT / MISSING FROM HIS DOC.** Boxed configuration lock — safety-critical. |
| (absent) | "CAREFULLY MONITOR FLIGHT PATH AND SPEED." / "WHEN OUT OF WINDSHEAR, SMOOTHLY RECOVER NORMAL CLIMB." | **NEW IN CURRENT / MISSING FROM HIS DOC.** |
| "THRUST LEVERS……… TOGA" (airborne/landing case) | "THR LEVERS AT TOGA ... SET OR CONFIRM" | WORDING DRIFT — same action; current phrasing acknowledges levers may already be at TOGA ("SET OR CONFIRM"). |
| "PRIOR TO V1: SIGNIFICANT VARIATIONS IN AIRSPEED……REJECT TAKEOFF" | "At Takeoff:" / "Before V1:" / "If there are significant variations in airspeed, and in airspeed trend below the indicated V1, reject the takeoff." | WORDING DRIFT — current adds "and in airspeed trend below the indicated V1". |
| "AFTER V1: THRUST LEVERS……… TOGA" | "After V1:" → "THR LEVERS ... TOGA" | IDENTICAL (abbreviation only) |
| "REACHING VR……… ROTATE" | "REACHING VR ... ROTATE" | IDENTICAL |
| "SRS ORDERS……… FOLLOW" (both cases) | "SRS ORDERS ... FOLLOW" | IDENTICAL |
| "AIRBORNE, INITIAL CLIMB or LANDING:" | "When airborne, during initial climb, or at landing:" | WORDING DRIFT (header) |
| "AP (if engaged)……… KEEP ON" | "AP (if engaged) ... KEEP ON" | IDENTICAL |

### 2e. EMERGENCY DESCENT — FCOM PRO-ABN-MISC P1/26 (pdf 3065) / QRH 22.02A (pdf 144)

| His line | Current verbatim | Class |
|---|---|---|
| "CREW OXYGEN MASKS……… USE" | "CREW OXY MASKS ... USE" | WORDING DRIFT |
| "SIGNS……… ON" | "SIGNS ... ON" | IDENTICAL |
| "EMERGENCY DESCENT……… INITIATE" | "EMER DESCENT ... INITIATE" | WORDING DRIFT |
| "IF A/THR NOT ACTIVE:" → (indented) "THRUST LEVERS……… IDLE" | "If A/THR not active:" → "THR LEVERS ... IDLE" (its own box) | IDENTICAL in structure |
| "SPEEDBRAKES……… FULL" | "SPD BRK ... FULL" (its own box, **after** and outside the A/THR box) | WORDING DRIFT — **with an important structural confirmation**: in his flat-text doc the SPEEDBRAKES line sits un-indented after the conditional, which is ambiguous on a quick read. Current v3 boxes prove **SPD BRK ... FULL is UNCONDITIONAL** — it is NOT under "If A/THR not active" (only THR LEVERS IDLE is). If he has been mentally grouping speedbrakes under the A/THR condition, that is wrong: speedbrakes go FULL regardless of A/THR state. |

### 2f. STALL RECOVERY — FCOM PRO-ABN-MISC P2/26 (pdf 3066)

| His line | Current verbatim | Class |
|---|---|---|
| "NOSE DOWN PITCH CONTROL……… APPLY" | "NOSE DOWN PITCH CONTROL ... APPLY" | IDENTICAL |
| "BANK……… WINGS LEVEL" | "BANK ... WINGS LEVEL" | IDENTICAL |
| "WHEN OUT OF STALL:" | "When out of stall (no longer stall indications) :" | WORDING DRIFT — current adds the defining parenthetical. |
| "THRUST……… INCREASE SMOOTHLY AS NEEDED" | "THRUST ... INCREASE SMOOTHLY AS NEEDED" | IDENTICAL |
| "SPEEDBRAKES……… CHECK RETRACTED" | "SPEEDBRAKES ... CHECK RETRACTED" | IDENTICAL |
| "FLIGHT PATH……… RECOVER SMOOTHLY" | "FLIGHT PATH ... RECOVER SMOOTHLY" | IDENTICAL |
| "IF IN CLEAN CONFIG & BELOW 20,000 FT:" | "If in clean configuration and below 20 000 ft :" | WORDING DRIFT |
| "FLAPS 1……… SELECT" | "FLAPS 1 ... SELECT" | IDENTICAL |

### 2g. STALL WARNING AT LIFTOFF — FCOM PRO-ABN-MISC P3/26 (pdf 3067)

| His line | Current verbatim | Class |
|---|---|---|
| "THRUST LEVERS……… TOGA" | "THRUST ... TOGA" | WORDING DRIFT |
| (no header) | "At the same time:" (unboxed condition over next two lines) | NEW IN CURRENT (header only; same actions) |
| "PITCH……… 15°" | "PITCH ATTITUDE ... 15 °" | WORDING DRIFT |
| "BANK……… WINGS LEVEL" | "BANK ... WINGS LEVEL" | IDENTICAL |

### 2h. UNRELIABLE SPEED INDICATION — QRH R35 23.03A (pdf 157)

| His line | Current verbatim | Class |
|---|---|---|
| "IF THE SAFE CONDUCT OF THE FLIGHT IS IMPACTED:" | "If the safe conduct of the flight is impacted" | IDENTICAL |
| "AP / A/THR / FD……… OFF" (one line) | "AP ... OFF" / "A/THR ... OFF" / "FD ... OFF" (three lines, same order) | WORDING DRIFT (merged; same actions, same order) |
| "BELOW THRUST RED ALT……… 15° / TOGA" | "Below THRUST RED ALT ... 15° / TOGA" | IDENTICAL |
| "ABOVE THRUST RED ALT & BELOW 10,000………. 10° / CLIMB" | "Above THRUST RED ALT and Below FL 100 ... 10° / CLB" | WORDING DRIFT — current says **FL 100**, his says "10,000". Same intent; drill the FL 100 phrasing. |
| "ABOVE THRUST RED ALT & ABOVE 10,000……….. 5° / CLIMB" | "Above THRUST RED ALT and Above FL 100 ... 5° / CLB" | WORDING DRIFT (same) |
| "IF FLAPS CONF 0, 1, 2, 3: FLAPS……… MAINTAIN CURRENT CONF" | "FLAPS (if CONF 0(1)(2)(3)) ... MAINTAIN CURRENT CONF" | WORDING DRIFT |
| "IF FLAPS CONF FULL: FLAPS……… SELECT CONF 3 & MAINTAIN" | "FLAPS (if CONF FULL) ... SELECT CONF 3 AND MAINTAIN" | WORDING DRIFT |
| "SPEEDBRAKES……… CHECK RETRACTED" | "SPEEDBRAKES ... CHECK RETRACTED" | IDENTICAL |
| "LANDING GEAR……… UP" | "L/G ... UP" | WORDING DRIFT |
| "WHEN AT OR ABOVE MSA OR CIRCUIT ALTITUDE……LEVEL OFF FOR TROUBLESHOOTING" | "When at or above MSA or Circuit Altitude: Level off for troubleshooting" | IDENTICAL |

### 2i. SMOKE / FUMES / AVIONICS SMOKE (his doc only)

His: "CREW OXYGEN MASKS ... USE / 100% / EMERG" (ref "QRH-PRO-SMOKE"). **NOT IN CURRENT VERIFIED SET** — no smoke/fumes procedure exists among the 10 verified [MEM] procedures. Not adjudicated; verify separately against current QRH before drilling.

---

## 3. What the LO doc and the 2023 gouge demand — verbatim

**LO doc (Rev 7, 04/06/23), p.2 "Some basic parameters":**
> "3. Know all Memory Items"

**LO doc, PARKING BRAKE section (p.41) — CONFLICTS with current wording:**
> "During the LOSS OF BRAKING memory item procedure, it calls for short and successive applications to stop the aircraft:
> o The accumulator will provide at least 7 full brake applications.
> o If possible, delay until as low speed as possible to avoid tire burst."

⚠ **CONFLICT:** the current verified line is "PARK BRAKE ... USE" (FCOM R17 PRO-ABN-BRAKES-00010803.0001001). The 2023-era LO doc describes the older "short and successive applications" wording that also appears in his personal doc. The systems facts (accumulator, 7 applications, tire-burst risk) may remain valid technique knowledge, but the *memory-item wording* it attributes is no longer what the manual prints. Expect an examiner using Rev 7 to possibly still ask it the old way — answer with the current line, then the technique.

**LO doc, Oxygen section (p.10)** (context, not a conflict):
> "MASK MAN ON – manually drops passenger O2 masks. o Part of the Emergency Descent Checklist."

**2023 gouge, Memory Items section — verbatim:**
> "Memory Items:
> (*know callout and procedure)
>
> LOSS OF BRAKING: what checking on triple indicator
>
> STALL & STALL ON TAKEOFF: then will ask… if you get a stall coming in for landing and you have flaps full out do you retract to 1 like memory item says? No, when low to the ground the flaps provide lift. So don't retract to 1 until in safe condition and safe altitude
>
> UNRELIABLE AIRSPEED: make sure to say "if safe conduct of flight impacted" then memory items would be applicable"

Adjudication vs current:
- "*know callout and procedure" — callouts are **NOT IN CURRENT VERIFIED SET**; his doc's callout column ("STALL, I HAVE CONTROL", "WINDSHEAR, TOGA", etc.) cannot be verified from v3. Verify against current HAL SOPs before relying on them.
- The stall/flaps-full trap is **consistent with the current wording**: the FLAPS 1 line is conditioned "If in clean configuration and below 20 000 ft :" — with flaps full you are not in clean configuration, so the current memory item never orders flaps retraction there. The gouge's phrase "like memory item says" overstates; the current condition already answers the examiner's trap.
- "if safe conduct of flight impacted" — matches the current boxed condition verbatim ("If the safe conduct of the flight is impacted", QRH 23.03A).
- "LOSS OF BRAKING: what checking on triple indicator" — systems question; the triple indicator/accumulator background is in the LO doc (p.32/33, p.41). No conflict with the memory item itself.

---

## 4. Relearn list — lines where drilling his doc is now WRONG

Each entry: what his doc drills → the current verbatim replacement → ref.

1. **LOSS OF BRAKING, park brake.** His: "PARKING BRAKE……… SHORT & SUCCESSIVE APPLICATIONS" → Current: "If still no braking:" / **"PARK BRAKE ... USE"** — FCOM R17 PRO-ABN-BRAKES P 1/16, ref PRO-ABN-BRAKES-00010803.0001001. (The LO doc Rev 7 still teaches his old wording — be ready for both, answer with the current.)
2. **LOSS OF BRAKING, anti-skid.** His: "ANTI-SKID & NWS……… ORDER OFF" (one action) → Current: **"A/SKID OFF ... ORDER"** then, as a separate boxed step, **"A/SKID & N/W STRG ... OFF"**, then "BRAKE PEDALS ... PRESS" / "MAX BRK PR ... 1000 PSI" — same ref.
3. **EGPWS/TAWS, bank.** His: "BANK……… WINGS LEVEL" → Current: **"BANK ... WINGS LEVEL or ADJUST"** — FCOM R17 PRO-ABN-SURV, refs PRO-ABN-SURV-AA-00026795.0001001 (caution) and PRO-ABN-SURV-00026799.0001001 (warning).
4. **EGPWS/TAWS, when to pull up.** His doc drills one pull-up for all "WARNINGS / CAUTIONS" → Current **[MEM] TAWS WARNING** pull-up applies "If the TAWS triggers one of the PULL UP alerts:"; **[MEM] TAWS CAUTION** pull-up applies only "During night or IMC conditions:" — "During daylight and VMC conditions, with terrain and obstacles clearly in sight:" the action is **"FLIGHT PATH ... ADJUST"** — refs above.
5. **TAWS CAUTION mode responses (all NEW to him).** "SINK RATE" → "FLIGHT PATH ... ADJUST" above 1 000 ft AAL IMC / 500 ft AAL VMC, "GO-AROUND ... CONSIDER" below; "DON'T SINK" → "FLIGHT PATH ... ADJUST"; "TOO LOW GEAR" or "TOO LOW FLAPS" → **"GO-AROUND ... PERFORM"**; "GLIDESLOPE" → "FLIGHT PATH ... ADJUST" / "G/S MODE ... OFF" (deliberate below-G/S) / "GO-AROUND ... CONSIDER" below 1 000/500 ft — ref PRO-ABN-SURV-AA-00026796–98.
6. **TCAS TA (entire procedure NEW to him).** **"Do not perform a maneuver based on a TA alone."** — ref PRO-ABN-SURV-00025042.0001001.
7. **TCAS RA, everything after the FDs.** His stops at "BOTH FDs OFF" → Current continues: **"VERTICAL SPEED ... ADJUST or MAINTAIN"**; and for **"Any CLIMB RA during approach in CONF 3 or FULL:" → "GO-AROUND ... PERFORM"** / "VERTICAL SPEED ... MONITOR"; then "ATC ... NOTIFY"; and at "CLEAR OF CONFLICT": "ATC ... NOTIFY" / "LATERAL AND VERTICAL GUIDANCE ... ADJUST" / "AP/FD ... AS RQRD". Note also the opening condition **"All RA, except any CLIMB RA during approach in CONF 3 or FULL:"** — ref PRO-ABN-SURV-00011464.0005001.
8. **WINDSHEAR, missing tail lines.** Add: **"DO NOT CHANGE CONFIGURATION (SLATS/FLAPS, GEAR) UNTIL OUT OF WINDSHEAR."** / "CAREFULLY MONITOR FLIGHT PATH AND SPEED." / "WHEN OUT OF WINDSHEAR, SMOOTHLY RECOVER NORMAL CLIMB." Also airborne case is "THR LEVERS AT TOGA ... SET OR CONFIRM", and the reject criterion includes "and in airspeed trend below the indicated V1" — ref PRO-ABN-SURV-00012300.0001001.
9. **EMER DESCENT, speedbrake condition (confirm, don't relearn).** **"SPD BRK ... FULL" is unconditional** — a separate box after, not inside, "If A/THR not active:" (only "THR LEVERS ... IDLE" is conditional) — refs PRO-ABN-MISC-00012261.0001001 / ABN-22-00010585.0001001.
10. **UNRELIABLE SPEED, phrasing.** "Above THRUST RED ALT and Below/Above **FL 100**" (his "10,000"); pitch/thrust "10° / CLB", "5° / CLB" — ref ABN-23-A-00017854.0001001.

---

## 5. Sources and honesty

- Every "Current verbatim" cell above is copied character-for-character from `memory_items_v3.json` `actions`/`boxes` (themselves transcribed from rendered FCOM R17 / QRH R35 pages, refs cited per procedure). Box structure (breaks, unboxed conditions) taken from the v3 `boxes` arrays and `""` break markers.
- Every "His line" cell is copied from `A330_Memory_Items_docx.md`; dot leaders compressed to "………".
- LO doc and gouge quotes are verbatim from their files.
- Nothing was adjudicated from general Airbus knowledge. Items outside the verified set (his Smoke/Fumes entry; all PF callouts) are marked **NOT IN CURRENT VERIFIED SET** and left unjudged.
- v3 contains 11 entries for 10 procedures (EMER DESCENT appears in both FCOM and QRH with identical boxed lines).

# limitations_CROSSCHECK.md

# A330 Limitations Cross-check — Study Documents vs Current Verified Set

**Date:** 2026-09-02
**Current baseline:** `/home/claude/a330/data/limitations_v3.json` (160 items, A330P FCOM R17 limitations chapter + AFM-sourced items), cross-referenced against `FCOM_LIM.md`, `AFM.md`, `QRH.md`, `FCTM.md`, `PRC.md`, `PERF.md`, `FOM_DELTA_123.1_to_125.1.md`.
**His documents checked:**
- Limitations sheet: `/home/claude/a330/training/pages_limitations/` — `preview.jpg` (page 1 of his Apple Pages doc) + 6 screenshots (3 full-size tables + 3 low-res thumbnails of the same tables)
- `Student_Oral_Learning_Objectives_Rev_7.md` (Rev 7, 04/06/23)
- `A330_OEM_Quick_Reference_MyVersion1.md`
- `ETOPS_Quiz.md`

Rule applied: the manual wins. v3 item numbers refer to the 0-indexed order in `limitations_v3.json`.

---

## 1. Every quantitative claim, checked

### 1A. His limitations sheet (page-1 preview + table screenshots)

| # | Claimed value | Current dataset / manual value (ref) | Verdict |
|---|---|---|---|
| S1 | Maneuvering load, clean: -1 g to +2.5 g | Same (v3 #98, LIM-AG-F_CTL-00020995) | MATCHES |
| S2 | Maneuvering load, other config: 0 g to +2 g | Same (v3 #99) | MATCHES |
| S3 | Minimum TAT -53 °C | Same (v3 #18, LIM-AG-OPS-ENV-00020116) | MATCHES |
| S4 | Runway slope (mean) ±2 % | Same (v3 #19) | MATCHES |
| S5 | **Runway altitude 12 500 ft** | Not in the 160-item set. Looked in FCOM_LIM.md (environmental envelope LIM-AG-OPS-ENV-00021654 survives only as "Minimum TAT -53 °C" — the envelope is a chart that did not survive text extraction), AFM.md, QRH.md, FCTM.md, PRC.md, PERF.md — no 12 500 ft runway/airport altitude anywhere in text | NOT IN CURRENT SET — candidate addition, see §3 |
| S6 | Nominal runway width 148 ft / 45 m | Same (v3 #20) | MATCHES |
| S7 | Max certified crosswind takeoff 32 kt gust incl., "engine limitation" | Same, incl. the engine-limitation note (v3 #21; FCOM_LIM ident 23 JAN 26 — value unchanged in R17) | MATCHES |
| S8 | Max demonstrated crosswind landing 45 kt gust incl. | Same (v3 #22) | MATCHES |
| S9 | Max tailwind takeoff 15 kt | Same (v3 #23) | MATCHES |
| S10 | Max tailwind landing 10 kt | Same (v3 #24) | MATCHES |
| S11 | Pax door wind 40 kt (50 kt nose into wind) | Same (v3 #25) | MATCHES |
| S12 | FWD/AFT cargo door 40 kt (50 kt into wind or doors downwind) | Same (v3 #26). Note: his sheet omits the companion value — doors must be **closed before wind exceeds 60 kt** (v3 #27) | MATCHES (60 kt value absent from his sheet) |
| S13 | Cockpit window open max 230 kt; cannot open with packs ON | Same (v3 #137) | MATCHES |
| S14 | Flaps 1 — 240 kt (holding) | Same (v3 #139) | MATCHES |
| S15 | Flaps 1+F — 215 kt (takeoff) | Same (v3 #140) | MATCHES |
| S16 | Flaps 2 — 205 kt (approach) | Same — CONF 1* (v3 #141) | MATCHES |
| S17 | Flaps 2 — 196 kt (takeoff/approach) | Same (v3 #142) | MATCHES |
| S18 | Flaps 3 — 186 kt | Same (v3 #143) | MATCHES |
| S19 | FULL — 180 kt | Same (v3 #144) | MATCHES |
| S20 | VLE 250 kt / M0.55 | Same (v3 #145) | MATCHES |
| S21 | VLO 250 kt / M0.55 | Same (v3 #146) | MATCHES |
| S22 | Gravity extension 200 kt | Same (v3 #147) | MATCHES |
| S23 | Max tire speed 204 kt | Same (v3 #148; also FCOM_LIM "Maximum ground speed 204 kt", AFM) | MATCHES |
| S24 | VMCL 118 kt | Same (v3 #149) | MATCHES |
| S25 | Wipers max 230 kt | Same (v3 #151) | MATCHES |
| S26 | Max taxi weight 526.6 (thousand lb) | 238 900 kg / 526 684 lb (v3 #154) | MATCHES |
| S27 | MTOW (brake release) 524.7 (thousand lb) | 238 000 kg / 524 700 lb (v3 #155) | MATCHES |
| S28 | EGT table: TO/GA 920 °C for 20 s; 900 °C 5 min AEO / 10 min OEI | Same values (v3 #73, currently flagged UNCLEAR for column pairing — his image **confirms the pairing**: 20 s→920 °C, 5/10 min→900 °C) | MATCHES (corroborates v3 UNCLEAR) |
| S29 | EGT MCT 850 °C not limited | Same (v3 #74) | MATCHES |
| S30 | EGT start on ground 700 °C | Same (v3 #75) | MATCHES |
| S31 | EGT start in flight 850 °C | Same (v3 #76) | MATCHES |
| S32 | Fuel imbalance, inner (outer balanced): Full→2 900 kg (6 393 lb); 17 000 kg→4 800 kg; 7 500 kg→7 500 kg | Same values (v3 #107, flagged UNCLEAR for interleave — his image **confirms the row/column pairing**) | MATCHES (corroborates) |
| S33 | Fuel imbalance, outer (inner balanced): Full→1 480 kg (3 261 lb); 2 400 kg→1 580 kg; 1 730 kg→1 730 kg | Same (v3 #108 UNCLEAR — image confirms pairing) | MATCHES (corroborates) |
| S34 | No limitation below 7 500 kg inner / 1 730 kg outer; linear between values | Same (v3 #109) | MATCHES |
| S35 | Crew oxygen MIN bottle pressure: 2 crew 520–640 PSI; +1 OBS 660–810; +2 OBS 810–1 000, over REF temp -10 to 50 °C | Same (v3 #131, flagged UNCLEAR for temp-column mapping — his image **confirms the full grid**: -10/0/10/20/30/40/50 °C → 520/540/560/580/600/620/640 etc.) | MATCHES (corroborates) |
| S36 | Thumbnails `…11.29-25.png`, `…11.48-27.png`, `…12.03-29.png` | Low-resolution duplicates of the three full-size tables above; text not legible at that size, but the full-size counterparts are | UNREADABLE (duplicates — content recovered from full-size versions; nothing lost) |

### 1B. Student Oral Learning Objectives Rev 7 (04/06/23)

Limitations-relevant claims first, then systems-description numbers (FCOM DSC chapters, which are not in the local source slice — those cannot be verified locally and are marked as such, not guessed).

| # | Claimed value | Current dataset / manual value (ref) | Verdict |
|---|---|---|---|
| L1 | IRS-only in RNP airspace: < 6.2 h from IRS ground alignment, or 5.7 h from last FM position update (PRO-SPO-51 / OpSpec B036-1) | **Verified current** in PRC.md: "6.2 hr from the time of IRS ground alignment, or 5.7 hr from the time of the last FM position update"; 5.7 hr also in the GPS PRIMARY LOST continuation rule | MATCHES manual — NOT IN CURRENT SET (lives in PRO-SPO, not the LIM chapter; candidate, §3) |
| L2 | APU: 3 start attempts then 60 min cooldown | Same (v3 #0) | MATCHES |
| L3 | APU start limit / electrical use 41 450 ft | Ceiling 41 450 ft (v3 #33); AFM NORM-49: "Use main electrical power supply up to 41 450 ft" (starting in flight) | MATCHES |
| L4 | APU start using batteries — 25 000 ft | AFM NORM-49: "In the case of APU TR not available use APU battery below 25 000 ft". Not in the 160-item set (v3 #5's 25 000 ft is the JET B/JP4 fuel limit — a different item) | MATCHES manual — NOT IN CURRENT SET (candidate, §3) |
| L5 | Electrical + APU bleed 1 pack — 22 500 ft | Same (v3 #7; AFM NORM-49 "Air bleed extraction in flight: up to 22 500 ft") | MATCHES |
| L6 | Engine start using APU bleed — 20 000 ft | Same (v3 #6) | MATCHES |
| L7 | Electrical + APU bleed 2 packs — 17 500 ft | Same (v3 #8) | MATCHES |
| L8 | APU bleed for wing anti-ice not permitted | Same (v3 #9; AFM note) | MATCHES |
| L9 | APU LOW OIL LEVEL: may operate 15 h | QRH 01.01A ECAM advisory: "The APU may be started and operated for 15 h, if there is no oil leak" | MATCHES manual (QRH) — not a LIM-chapter item |
| L10 | Engine oil: 15 qt or 6 qt + est. consumption (0.7 qt/h), whichever higher | Same (v3 #82; FCOM_LIM "Average estimated consumption = 0.7 qt/h") | MATCHES |
| L11 | Chrono/EGT: 900 °C for 5 min normal, 10 min engine failed | Same (v3 #73, confirmed by sheet EGT table) | MATCHES |
| L12 | Wipers 230 kt | Same (v3 #151) | MATCHES |
| L13 | Minimum RAT speed 140 kt | AFM (multiple procedures): "Minimum RAT speed: 140 kt". Not in the 160-item set | MATCHES manual (AFM) — NOT IN CURRENT SET (candidate, §3) |
| L14 | Cargo fire: 2nd bottle fully discharges in 260 min | AFM: "The time capability of the cargo fire suppression system is 260 min" | MATCHES manual (AFM) — NOT IN CURRENT SET (candidate, §3) |
| L15 | Cargo fire "ETOPS requirement (195 minutes)" | Not found in AFM/QRH/FCTM/PRC/FCOM_LIM/FOM delta | NEEDS FOM CHECK |
| L16 | Fuel imbalance advisory at 6 600 lb | QRH 01.01A: advisory when L/R difference > 3 000 kg (6 614 lb) | MATCHES manual (QRH; his 6 600 is a rounding of 6 614) |
| L17 | "Start checking imbalance chart around 3 200 lb" | Rule of thumb keyed to the outer-tank full limit 1 480 kg (3 261 lb) (v3 #108) | MATCHES (rule of thumb, consistent) |
| L18 | Ground spoilers/autobrake: no deployment below 72 kt on RTO | FCTM: "Below 72 kts, the ground spoilers will not deploy and the auto brake will not activate" | MATCHES manual (FCTM) |
| L19 | Gear red arrow at 750 ft RA | QRH/FCTM: L/G NOT DOWN alert below 750 ft RA | MATCHES manual |
| L20 | T/O warnings inhibited until 1 500 ft or 2 min after liftoff | FCTM: inhibited "from 80 kt to 1 500 ft (or 2 min after lift-off, whichever occurs first)" — LO says "from takeoff thrust"; the manual says from 80 kt | MATCHES manual (minor nuance: starts at 80 kt) |
| L21 | ARS activates through 200 kt; 1+F limit 215 kt | FCTM: "in Conf 1+F and IAS reaches 200 kt, the ARS is activated"; 215 kt = VFE CONF 1+F (v3 #140) | MATCHES |
| L22 | Flap load relief: retract on overspeed by 2.5 kt, re-extend 2.5 kt below VFE | FCTM describes FLRS at VFE but gives no ±2.5 kt figure; the number is FCOM DSC-27 detail, not in local slice | NOT IN CURRENT SET (looked FCTM/QRH/FCOM_LIM; DSC not local) |
| L23 | Alpha/speed lock: inhibit <148 kt or α>8.5°; release α<8.2° and >154 kt | FCTM describes the function, no numbers; DSC-27 not local | NOT IN CURRENT SET (DSC not local) |
| L24 | Aileron droop 5° (1+F) / 10° (2–FULL) | DSC-27 not local | NOT IN CURRENT SET (DSC not local) |
| L25 | Fuel jettison rate 2 200 lb/min + burn | QRH 19.02A has the procedure but no rate; DSC-28 not local | NOT IN CURRENT SET (looked QRH/AFM; AFM LIM-28 says only "may be jettisoned throughout the flight envelope") |
| L26 | Jettison auto-stops at 22 000 lb combined inner tank | Not in QRH 19.02A text; DSC-28 not local | NOT IN CURRENT SET (DSC not local) |
| L27 | Center tank pumps inop: 33 000 lb unusable | Not found (QRH shows a different figure — 4 400 lb unusable per inner tank in the gravity-feed summary); PRO-ABN-FUEL detail not in local slice | NOT IN CURRENT SET (DSC/ABN not local — flag for FCOM check) |
| L28 | Tank capacities: outer 6 500×2, inner 72 000×2, trim 11 000, center 72 000, total ≈240 000 lb | DSC-28-10-20 not local | NOT IN CURRENT SET (DSC not local) |
| L29 | Tank filling: trim starts ~80 500 lb, center ~166 500 lb | DSC-28-10-110 not local | NOT IN CURRENT SET (DSC not local) |
| L30 | Trim transfer: aft passing FL 255; forward FL 245 or 35 min to destination | DSC-28-10-90 not local | NOT IN CURRENT SET (DSC not local) |
| L31 | Hydraulics 3 000 psi normal / 2 500 psi RAT; green reservoir tick 17 L / 4.5 USG; RAT flow 15–45 % of EDP; green elec pump runs 25 s after gear up | DSC-29 not local | NOT IN CURRENT SET (DSC not local) |
| L32 | Batteries only: minimum 30 min | Certification design value, DSC-24 not local | NOT IN CURRENT SET (DSC not local) |
| L33 | Battery ≥25.5 V (=50 %); charge 20 min if lower; APU bat <23.5 V risks aborted battery start; charge limiter <60 A within 10 s | PRO-NOR-SOP-04 / DSC-24 not in local slice | NOT IN CURRENT SET (not local) |
| L34 | IDG disconnect: hold ≤3 s | DSC-24 not local | NOT IN CURRENT SET (DSC not local) |
| L35 | Emergency exit lights auto-on above 9 550 ft cabin altitude | DSC-33 not local | NOT IN CURRENT SET (DSC not local) |
| L36 | Manual pressurization: each V/S CTL toggle ≈150–200 fpm | DSC-21 not local | NOT IN CURRENT SET (DSC not local) |
| L37 | Pack controller fail: outlet 48–59 °F; zone controller fail: 68 °F; LOW=80 % flow (<60 % economy, ≤200 pax); HIGH=120 %; 125 % with APU bleed or single pack; CIDS range 5.4 °F; RAM AIR opens if ΔP<1 psi | DSC-21 not local | NOT IN CURRENT SET (DSC not local) |
| L38 | APU bleed auto-closes climbing 25 000 ft, reopens descending 23 000 ft | DSC-36 not local | NOT IN CURRENT SET (DSC not local) |
| L39 | APU cooldown: AVAIL up to 2 min after MASTER off | DSC-49 not local | NOT IN CURRENT SET (DSC not local) |
| L40 | ADIRS: quick align 30 s; full align 7–10 min; ATT-mode heading update every 10 min | FCTM describes complete alignment without durations; DSC-34/PRO-NOR-SUP-NAV detail not local | NOT IN CURRENT SET (not local) |
| L41 | Fire loops: warning if both loops break within 5 s; 1 APU bottle; 2 bottles per engine; 2 cargo bottles, 1st discharges in 60 s | DSC-26 not local (260-min total verified, L14) | NOT IN CURRENT SET (DSC not local) |
| L42 | Oxygen preflight: pressure drop below 800 psi → maintenance | PRO-NOR-SOP-06 not in local slice (QRH advisory uses different gates: CKPT OXY pulses green <600 PSI, amber <300 PSI) | NOT IN CURRENT SET (not local — note the QRH gates differ; verify SOP-06 at next FCOM pass) |
| L43 | Recorders run 5 min after power-up on ground | DSC-31 not local | NOT IN CURRENT SET (DSC not local) |
| L44 | Sidestick lockout: hold red pb >40 s | DSC-27 not local | NOT IN CURRENT SET (DSC not local) |
| L45 | Autoland lights active below 200 ft RA | DSC-22 not local | NOT IN CURRENT SET (DSC not local) |
| L46 | A/THR instinctive disconnect: hold 15 s removes A/THR for flight | DSC-22 not local | NOT IN CURRENT SET (DSC not local) |
| L47 | Parking brake: accumulator holds 12 h; ≥7 full brake applications | FCTM confirms "short successive parking brake applications" technique but gives no counts; DSC-32 not local | NOT IN CURRENT SET (DSC not local) |
| L48 | TURB DAMP active >200 kt | DSC-27 not local | NOT IN CURRENT SET (DSC not local) |
| L49 | Igniters auto-on if master cycled with N3 >50 % | DSC-70 not local | NOT IN CURRENT SET (DSC not local) |
| L50 | SRS: V2+10 normal takeoff | FCTM/AFM corroborate V2+10 kt | MATCHES manual |
| L51 | RAT ineffective below 140 kt (batteries only) | AFM minimum RAT speed 140 kt | MATCHES manual (AFM) |

### 1C. OEM Quick Reference (MyVersion1)

Reviewed in full: it is a flows/checklist card. It contains **no aircraft-limitation values**. The only numbers are procedural (10,000 ft AAL flow/light triggers, RCL held 3 s, "IRS Perf <5" at parking, gear pins ×3). Nothing to cross-check against the limitations set; nothing stale.

### 1D. ETOPS Quiz

Aircraft-limitation numbers first; FOM/OpSpec policy values that cannot be verified from local sources are listed and marked NEEDS FOM CHECK, per instructions — not guessed.

| # | Claimed value (quiz answer content) | Local check | Verdict |
|---|---|---|---|
| Q1 | HAL max 180 min ETOPS (Q1, Q27) | FOM 125.1 delta release legend: "ETOPS 60/180 … planned maximum diversion time"; delta Q&A confirms 180-min max diversion | MATCHES (FOM 125.1) |
| Q2 | ETOPS area begins 60 min from adequate airport (Q27) | Same FOM 125.1 "ETOPS 60/180" legend | MATCHES (FOM 125.1) |
| Q3 | **Adequate airports listed in OpSpec B342 and/or C070** (Q24, Q25A) | FOM 125.1 changed both definitions: adequate airport = any airport designated R/F/P/A/E in **FOM 8.1.3 Authorized Airports** (criteria in 6.2.1); ETOPS alternate must be listed in 8.1.3 and designated on the release. B342/C070 wording removed | **STALE** — see §2 |
| Q4 | International reserves: most distant alternate + 30 min holding + 10 % of destination time (Q37) | FOM 125.1 fuel-summary legend confirms "10% RSV" and "30@1500" (standard flag) | MATCHES (FOM 125.1) |
| Q5 | B043 special reserves: 10 % on ORCA portion; 45 min normal cruise after alternate (Q38) | FOM 125.1 legend confirms "45@CRZ" (B043) vs "30@1500"; note the **HI–CONUS-only restriction on B043 was deleted in Rev 124.2** | MATCHES; adjacent policy changed — see §2 |
| Q6 | RVSM: 1 000 ft separation FL290–FL410 (Q6) | Not verifiable locally (PRC metric-RVSM tables only) | NEEDS FOM CHECK |
| Q7 | Class I nav: VOR service range 130 nm, NDB 75 nm (Q7) | Not in local sources | NEEDS FOM CHECK |
| Q8 | RCP 400 s or 240 s (Q12) | Not in local sources | NEEDS FOM CHECK |
| Q9 | RSP 400 s or 180 s (Q13) | Not in local sources | NEEDS FOM CHECK |
| Q10 | IFSD rate ≤0.03/1 000 h beyond 120 up to 180 min (Q19) | AC 120-42B value; not in local sources | NEEDS FOM CHECK |
| Q11 | PDSC valid 4 h (Q21) | Not in local sources | NEEDS FOM CHECK |
| Q12 | ETOPS alternate RFFS Category 4+, or brought in within 30 min (Q26) | Not in local sources | NEEDS FOM CHECK |
| Q13 | Adequate airport: stop within 60 % of effective runway length from 50 ft (Q23C) | FAR 121.195 value; not in local sources | NEEDS FOM CHECK |
| Q14 | C055 alternate minima: 1 facility +400 ft / +1 sm; 2 facilities +200 ft / +½ sm (Q36) | Not in local sources | NEEDS FOM CHECK |
| Q15 | Critical fuel scenarios: descent to 10 000 ft; alternate at 1 500 ft hold 15 min; ±5 % wind error (Q29–Q30) | Not in local sources | NEEDS FOM CHECK |
| Q16 | Flag alternate rule: >6 h needs alternate; else ceiling 2 000 ft/1 500 ft rules, vis 3 mi/2 mi, ±1 h (Q34) | Not in local sources | NEEDS FOM CHECK |
| Q17 | No-alternate flag route: destination + 2 h fuel (Q35; quiz's own answer: HAL has no such routes) | Not in local sources | NEEDS FOM CHECK |
| Q18 | B043 reports: ETE +15 min; 100 nm off route; ±4 000 ft cruise (Q39) | Not in local sources | NEEDS FOM CHECK |
| Q19 | GNE: 25 nm worldwide, 10 nm NAT/HLA (Q48) | Not in local sources | NEEDS FOM CHECK |
| Q20 | Max diversion distance 1 168 NM (A321) / 1 200 NM (A330) (IOE Q18) | Not in local sources | NEEDS FOM CHECK |
| Q21 | 2 HF radios required for extended overwater dispatch; SATVOICE substitution per MEL (Q46) | Not in local sources (MEL not local). Related current LIM item: Starlink prohibited as SATVOICE/ATS substitute (v3 #70) | NEEDS FOM CHECK |
| Q22 | Overwater transponder: 2000 oceanic, 7700/7600/7500 (Q45) | Standard codes; not in local sources | NEEDS FOM CHECK |
| Q23 | Lowest ETOPS-alternate approach capability "Cat II, Cat III (787)" (Q43B) | The "(787)" reference is from another fleet's version of this quiz — A330 applicability unverified | NEEDS FOM CHECK (also flag the 787 reference as a copy-over) |
| Q24 | Overwater ops >50 nm from shoreline (Q5, FAR 121.339) | Regulatory; not in local sources | NEEDS FOM CHECK |

---

## 2. Changed since you learned it (most operationally significant first)

1. **Where ETOPS adequate/alternate airports live — FOM 125.1 (his quiz teaches Rev-123-era policy).** The quiz's answers for Q24/Q25 say adequate airports are "listed in OpSpec B342 and/or C070." FOM 125.1 re-pointed both definitions: an **adequate airport is now any airport designated R, F, P, A, or E in the FOM 8.1.3 Authorized Airports table** (meeting 6.2.1 criteria, unless restricted by F&F or Company NOTAM), and an **ETOPS alternate must be listed in 8.1.3** and designated on the release. If he answers B342/C070 on an oral he is quoting the superseded structure. (Source: `FOM_DELTA_123.1_to_125.1.md` §6.2.1/6.2.2/8.1.3.)
2. **B043 special fuel reserves no longer restricted to Hawaii–CONUS legs** (Rev 124.2 deleted the "only approved for flights between the Hawaiian Islands and the contiguous United States" note). His quiz doesn't state the restriction outright, but anyone taught B043 alongside that note should relearn it. The 45-min/10 % mechanics themselves are unchanged ("45@CRZ", "10% RSV").
3. **No stale aircraft-limitation values found.** Every readable number on his limitations sheet and every LO-doc value that maps to the 160-item set matches FCOM R17/AFM exactly — including all weights, speeds, EGT, APU envelope, fuel imbalance, and oxygen tables. His sheet is old (Jan 2025 capture) but the numbers have not moved.

---

## 3. Candidate additions — values his docs drill that the 160-item set lacks

| Candidate | Value per his docs | Where a future pass should verify |
|---|---|---|
| Maximum runway (airport) altitude | 12 500 ft (his sheet, page 1) | FCOM **LIM-AG-OPS-ENV-00021654** environmental envelope **chart** (graphic; did not survive text extraction — needs the PDF page), cross-check AFM environmental envelope |
| IRS-only RNP time limits | 6.2 h from IRS ground alignment / 5.7 h from last FM position update | FCOM **PRO-SPO-51** (already verified verbatim in PRC.md; OpSpec B036-1) — an operational limitation the set could carry with a PRO-SPO ref |
| Minimum RAT speed | 140 kt | **AFM** emergency procedures (verified, multiple occurrences); consider FCOM LIM-29/DSC-29 for the FCOM-side ref |
| APU battery start in flight (APU TR unavailable) | below 25 000 ft | **AFM NORM-49-00005815** (verified verbatim) — distinct from the JET B/JP4 25 000 ft item already in the set (v3 #5) |
| Cargo fire suppression time capability | 260 min | **AFM** (verified verbatim: "time capability of the cargo fire suppression system is 260 min"); the companion "195 min ETOPS requirement" claim needs the FOM |
| APU LOW OIL LEVEL dispatch/ops allowance | 15 h if no leak | **QRH 01.01A** ECAM advisory (verified) — arguably advisory not limitation; editorial call |
| Fuel imbalance ECAM advisory threshold | 3 000 kg (6 614 lb) | **QRH 01.01A** (verified) — advisory threshold, pairs naturally with v3 #107–109 |

Also worth noting for the dataset (not additions): his three table screenshots independently **confirm the column pairings** for the three v3 items flagged UNCLEAR — #73 (EGT time pairing), #107/#108 (imbalance interleave), #131 (oxygen temp columns). His images are from an earlier revision capture, so treat as corroboration; clear the UNCLEAR flags only after sighting the R17 PDF pages.

## 4. Method and honesty notes

- **What was actually readable of his sheet.** Only page 1 of his Apple Pages limitations doc is available (`preview.jpg`), plus three full-size table screenshots (EGT, fuel imbalance, crew oxygen) and three thumbnail duplicates of the same tables. Page 1 ends mid-list at MTOW 524.7 — **his MLW, MZFW, VMO/MMO, ceiling, pressurization, AFS/autoland minima, and all remaining pages were not in the folder and are unchecked.** Nothing was guessed from the thumbnails; they were read from their full-size counterparts.
- **Verification scope.** Every claim was checked first against `limitations_v3.json`, then by regex search of FCOM_LIM.md, AFM.md, QRH.md, FCTM.md, PRC.md, PERF.md, and the FOM 123.1→125.1 delta. FCOM **systems** chapters (DSC-xx) and the full FOM are not in the local slice, so LO-doc systems numbers (fire loops, tank capacities, hydraulic details, battery voltages, etc.) are marked "not local," not judged wrong. They are training-department teaching values, most of them consistent with type-standard figures, but I could not prove them here.
- **NEEDS FOM CHECK items (16):** rows Q6–Q24 in §1D above — RVSM band, VOR/NDB ranges, RCP/RSP times, IFSD rate, PDSC 4 h, RFFS Cat 4/30 min, 60 %/50 ft, C055 minima deltas, critical-fuel scenario details, flag alternate rules, no-alternate 2-h fuel, B043 report triggers, GNE 25/10 nm, 1 168/1 200 NM diversion distances, HF/SATVOICE dispatch rule, transponder codes — plus the LO doc's "195 min ETOPS" cargo-fire figure (L15) and the quiz's stray "(787)" approach-capability reference (Q23). Verify against FOM 125.1 and current OpSpecs before drilling.
- **Dates.** His sheet screenshots: Jan 2025. LO doc: Rev 7, 04/06/23 (pre-dates FOM 125.1 — but nothing in it contradicted current sources). Quiz: undated, references the pre-125.1 OpSpec airport structure (the one confirmed stale item). Current FCOM_LIM pages carry idents through 23 JAN 26 / prints to 15 MAY 26; QRH prints 26 JUN 26.
- **Counts.** 36 sheet claims (35 readable + 3 duplicate thumbnails), 51 LO-doc claim rows, 24 quiz rows, 0 quick-reference limitation values = **111 claim rows checked**. Matches against dataset or a local manual: 60. Stale: 1 confirmed (adequate-airport OpSpec pointer), plus 1 adjacent policy change (B043 scope). Unverifiable locally: 34 (DSC/systems + SOP values). NEEDS FOM CHECK: 16 quiz/FOM items + 2 flagged oddities.

# flight_control_laws_CROSSCHECK.md

# Cross-check: HA A330 training handout "Flight Control Laws Rev 4" (18 Jan 2018) vs A330P FCOM R17

Date: 2026-09-02.
Handout: `/home/claude/a330/training/Flight_Control_Laws_Rev_4.md` (Rev 4, 18Jan2018; cites "FCOM 1.27.20~30, 1.27.10 P11" — old numbering).
Primary reference: **A330P FCOM R17** slice `A330P_FCOM_R17_FLIGHT_CONTROL_LAWS.md` (Drive, `HA - Airbus A330/working`, file id `1BJ3uvfaZMFHj_uRKdkkBxcz8euAmQFXr`, 50,299 chars). The slice covers DSC-27-10-20 (last page) through **DSC-27-20-20-30 P 1/2 only**. It **ends at Direct Law page 1** — the Abnormal Attitude Law and Mechanical Backup pages (and Direct Law yaw) are **not in the slice**; those rows below are marked accordingly.
Corroboration: FCTM R5 (`/home/claude/a330/data/FCTM.md`), QRH R35 (`/home/claude/a330/data/QRH.md`), and the prior AFM hunt (`/home/claude/a330/data/vmo_mmo_HUNT.md`). `/home/claude/a330/fcom.txt` is a memory-items extract and does not contain DSC-27.

Ground rules honored: verdicts come only from the quoted current-manual text. No gap was filled from general Airbus knowledge (A330 protections differ from other Airbus types). The FCOM wins every conflict. Note the handout's PDF layout garbles column alignment in text extraction; where a cell's column was ambiguous I quote the raw text.

---

## 1. Claim-by-claim table

Verdicts: **MATCHES** / **STALE** / **NOT FOUND IN SLICE** (with where to look) / **UNVERIFIABLE FROM TEXT** (figure/table did not survive extraction).

### Indications

| # | Handout claim | Current FCOM R17 statement (ident) | Verdict |
|---|---|---|---|
| 1 | Normal law PFD: "Green pitch/bank/Vmo symbols (=) displayed" | "Specific symbols... indicate which protection are available. When protections are lost, amber crosses (X) appear, instead of the green protection symbols (=)." — DSC-27-20-20-10, Ident. 00000324.0001001 / 27 DEC 23 (page 23 JAN 26) | **MATCHES** |
| 2 | Alternate PFD: "Amber pitch/bank limit symbols (X) displayed" | Same ident as #1; plus footnote (4): "since ALT 1 is generally an unprotected law, all protection marks on the PFD are in amber for simplicity." | **MATCHES** |
| 3 | Direct PFD: "USE MANUAL PITCH TRIM" | "The 'USE MAN PITCH TRIM' amber message is displayed on the PFD." — DSC-27-20-20-30, Ident. 00000353.0001001 / 27 DEC 23. Also "amber 'USE MAN PITCH TRIM' message below the FMA" (00000324). Exact string is "USE MAN PITCH TRIM". | **MATCHES** (wording) |
| 4 | Mechanical backup PFD: "MAN PITCH TRIM ONLY" | Slice has it only as footnote (5): "When both elevators have failed, only pitch mechanical backup is available... 'MAN PITCH TRIM ONLY' is displayed in red on the PFDs." (00000324). The mechanical-backup page itself is not in the slice. | **NOT FOUND IN SLICE** (message exists per footnote; confirm context in FCOM DSC-27-20-20 Mechanical Backup pages) |
| 5 | Alternate ECAM: "FLT CTRL ALTN LAW (PROT LOST)" | "In ALTN Law: FLT CTL ALTN LAW (PROT LOST) / A330 : **MAX SPEED 330 kt/M 0.82**" (00000324). QRH ABN-16-SUM status corroborates "MAX SPD : 330/.82". | **STALE** — title is "FLT CTL..." and the ECAM now carries a MAX SPEED 330/M 0.82 line the handout omits |
| 6 | Direct ECAM: "FLT CTRL DIRECT LAW (P L)" | "In Direct Law: FLT CTL DIRECT LAW (PROT LOST) / A330 : **MAX SPEED 330 kt/M 0.80** / MAN PITCH TRIM USE" (00000324). | **STALE** — handout omits MAX SPEED 330/M 0.80 and the MAN PITCH TRIM USE line |
| 7 | Normal/Abn-attitude/Mechanical ECAM: "none" | No contrary statement in slice; slice lists ECAM indications only for ALTN and Direct. | **NOT FOUND IN SLICE** (benign; confirm on FCOM recon pages/figure) |

### Law entry conditions / sidestick orders / AP

| # | Handout claim | Current FCOM R17 statement (ident) | Verdict |
|---|---|---|---|
| 8 | Sys failures: Alternate = "Single/double serious failures"; Direct = "Double/triple serious failures"; ALT 1 = "Single serious failure", ALT 2 = "Double serious failures" | Reconfiguration levels listed ("Alternate law (ALT 1 or ALT 2), Direct law, or Mechanical" — 00000324) but the failure-mapping **table is a graphic** that did not survive extraction (only footnotes (\*),(1)-(5) remain). | **UNVERIFIABLE FROM TEXT** — a human must read the reconfiguration table figure at FCOM DSC-27-20-20-10 P 1/4 |
| 9 | SS fore/aft: load factor (Normal, Alternate, Abn); elevator control (Direct) | Normal: "load factor demand law with auto trim" (DSC-27-20-10-20-A-00000271 / 27 DEC 23). ALT 1 pitch: "load factor demand law, similar to normal law" (00000329.0002001). Direct: "direct stick to elevator relationship" (00000353). Abn-attitude pitch: not in slice. | **MATCHES** for Normal/ALT/Direct; Abn column **NOT FOUND IN SLICE** |
| 10 | SS left/right: roll rate (Normal, ALT 1); aileron control (ALT 2, Direct, Abn) | Normal: "roll rate requested... proportional to sidestick deflection, with a maximum rate of 15 °/s" (00000312.0002001 / 15 APR 24). ALT 1 lateral: "similar to normal law" (00000330). ALT 2: "ROLL DIRECT LAW... direct stick-to-surface position relationship" (00000344). Direct/Abn roll: not in slice text beyond the above. Note tension: FCTM AOP-10-30-20 (01 MAY 24) says in reconfiguration law "the roll control law will always be in direct law", while FCOM footnote (4) says ALT 1 "uses roll normal" — **FCOM wins**. | **MATCHES** (FCOM basis) |
| 11 | A/P available: Normal Yes / Alternate "Maybe, depending on the type of failure" / Direct No / Abn No / Mech No | Not stated in the slice (AP engagement conditions live in DSC-22). Slice only notes AP disconnect events (bank >45°, high speed prot). | **NOT FOUND IN SLICE** — check FCOM DSC-22_30 (AP engagement conditions) |

### Load factor limitation

| # | Handout claim | Current FCOM R17 statement (ident) | Verdict |
|---|---|---|---|
| 12 | Max clean CONF: +2.5g/-1.0g; Max Slat/Flap CONF: +2.0g/-0.0g (Normal and Alternate) | "The load factor is automatically limited to : +2.5 g to -1 g, slats retracted / +2 g to 0, slats extended" (DSC-27-20-10-20-B-00000276 / 27 DEC 23). Alternate: "alternate law does not maintain any of the protections, except maneuver protection" (00001949.0004001). | **MATCHES** |
| 13 | "THS is limited (current setting to 2°ND) >1.3g" | "when the load factor is higher than 1.3 g, **or when the bank angle is outside ± 33 °**, the THS is limited between the actual setting and 2 ° nose down" (00000271). | **MATCHES**, but handout omits the bank-angle-outside-±33° trigger |

### Pitch attitude protection

| # | Handout claim | Current FCOM R17 statement (ident) | Verdict |
|---|---|---|---|
| 14 | "Max Nose Up=30° (25° at low spd); Nose Down=15°" | "pitch attitude protection limits pitch attitude to plus 30 °/minus 15 °" (00000278 / 27 DEC 23). The "25° at low speed" figure is not in the slice text (likely in a figure or another DU). | **MATCHES** for 30/15; "25° at low spd" **NOT FOUND IN SLICE** — check the pitch attitude protection figure on FCOM DSC-27-20-10-20 P 5 area / PFD chapter DSC-31 |
| 15 | Pitch protection "Lost" in Alternate | "PITCH ATTITUDE PROTECTION: Lost." (ALT 1 protections, 00000331.0002001). | **MATCHES** |

### High speed protection

| # | Handout claim | Current FCOM R17 statement (ident) | Verdict |
|---|---|---|---|
| 16 | "PRIMs adjust elevator nose up" | "a permanent nose-up order is applied to aid recovery" (00000281 / 27 DEC 23). | **MATCHES** |
| 17 | "AP disconnects" (no value given) | "The autopilot disconnects at **VMO +12 kt and MMO + 0.03**." (00000281). | **MATCHES** (FCOM now gives explicit values the handout lacks) |
| 18 | "THS is frozen at current position" | "When it is activated, the pitch trim is frozen." (00000281); also auto trim frozen "In high speed protection" (00000271). | **MATCHES** |
| 19 | "Rolls to wings level w/ stick free (spiral stability)" | "Positive spiral static stability is introduced to 0 ° bank angle (instead of 33 ° in normal law), so that with the sidestick released, the aircraft always returns to a bank angle of 0 °. The bank angle limit is reduced from 67 ° to 45 °." (00000281). | **MATCHES** |
| 20 | "Vmo=330 kts / Mmo=M0.86" | Not in slice. AFM LIM-SPD (per `vmo_mmo_HUNT.md`): "VMO = 330 kt IAS / MMO = M 0.86"; PRC: "must not intentionally exceed VMO/MMO (330 kt/M 0.86)". | **MATCHES** (via AFM/PRC, not the slice) |
| 21 | "Green overspeed symbol (=) on PFD at Vmo+4" | ALT 1: "The high speed protection symbol (VMO + 4) disappears." (00000331) — i.e. in normal law the symbol exists at VMO+4. | **MATCHES** (inferred from ALT 1 text; symbol color is in the PFD figure) |
| 22 | "ECAM OVERSPEED warning at Vmo+4/Mmo+0.006" (Normal, Alternate, Direct) | "An OVERSPEED ECAM warning is provided at VMO + 4 kt and MMO + 0.006." (00000281 note). ALT 1: "the overspeed warning (VMO + 4 or MMO + 0.006) remains available" (00000331). Direct: "As per alternate law, overspeed and stall warnings are available." (00000353). | **MATCHES** |
| 23 | "Max speed=Vmo+15/Mmo+0.04 **with stick free**" | "If there is **no sidestick input**, the aircraft will **slightly overshoot** VMO/MMO and fly back towards the envelope. If the sidestick is **maintained full forward**, the aircraft will significantly overshoot VMO/MMO. At approximately **VMO +16/MMO +0.04**, the pitch nose-down authority smoothly reduces to zero (which does not mean that the aircraft stabilizes at that speed)." (00000281). | **STALE** — figure is now VMO+16 (not +15), and it applies to *full-forward stick* (nose-down authority reaching zero), not "max speed with stick free"; stick-free overshoot is described only as "slight" |

### High AOA protection (FCOM section revised 23 JAN 26)

| # | Handout claim | Current FCOM R17 statement (ident) | Verdict |
|---|---|---|---|
| 24 | "Sidestick fore/aft commands AOA" (when protection active) | "When the High AOA protection is activated... the side stick input is an angle-of-attack demand, instead of a load factor demand." (DSC-27-20-10-20-B-00000280.**0005001 / 23 JAN 26**). | **MATCHES** |
| 25 | "VαProt (top black/amber band) is stick-free max AOA; VαMax (top of red band) is stick-back max AOA" | "Without the flight crew input, the F/CTL computers will maintain the angle-of-attack equal to αPROT. The AOA can be further increased by the flight crew input, up to a maximum value equals to αMAX... If the flight crew releases the sidestick, the angle-of-attack returns to the αPROT and stays there. As the aircraft enters the protection at the amber and black strip (αPROT)..." (00000280.0005001). | **MATCHES** |
| 26 | "Autopilot disengages" (high AOA) | Not stated in the slice's high-AOA section. | **NOT FOUND IN SLICE** — check FCOM DSC-22_30 (AP disengagement conditions) |
| 27 | "Speed brakes automatically retracted/inhibited" (high AOA) | Not in slice (FCTM mentions auto speedbrake retraction only at TOGA go-around). | **NOT FOUND IN SLICE** — check FCOM DSC-27 Speedbrakes / DSC-27-20 protections pages not in slice |
| 28 | "THS is limited (current setting to 2°ND)" (high AOA) | "When the angle of attack protection is active, the THS is limited between setting at entry in protection and 2 ° nose down" (00000271); "the system inhibits further nose-up trim beyond the point already reached. The nose-down trim remains available" (00000280.0005001). | **MATCHES** |
| 29 | "Alpha Floor protection engages (at variable α): A/THR engages in TOGA even if off (not armed)" | Slice: "Between αPROT and αMAX, the αfloor protection may automatically set go-around thrust... Refer to DSC-22_30-50-50 ALPHA FLOOR" and "Vα PROT, Vα MAX, and αfloor condition... vary with configuration, weight and load factor" (00000280.0005001). FCTM AS-FG-10-2 (27 MAR 26): "A/THR activates automatically and orders TOGA thrust, **regardless of the thrust lever position**... ALPHA floor is available, when the flight controls are in NORMAL LAW, from lift off to 100 ft RA at landing. It is inhibited in some cases of engine failure." | **MATCHES** (variable α + auto TOGA); availability window/inhibits are added current detail |
| 30 | "Low Energy warning 'Speed, Speed, Speed' in CONF 2/3/FULL from 100'-2000'RA at low speed" | "A low energy aural alert 'SPEED SPEED SPEED' repeated every 5 s... It is available in configuration 2, 3 and full between 100 and 2 000 ft... It comes immediately before the ALPHA Floor." (00000282 / 27 DEC 23). Inhibited when: TOGA selected, <100 ft RA, >2 000 ft RA, alpha floor or GPWS triggered, in alternate or direct law, both RA failed. | **MATCHES** (handout omits inhibition list and 5-s repeat) |
| 31 | Alternate high AOA: "PRIMs adjust elevator nose down... At low speed (Vsw+5~10), not AOA, down elevator is commanded to provide low-speed stability" | ALT 1 LOW SPEED STABILITY: "a nose down demand is introduced **in reference to IAS, instead of angle of attack**, and alternate law changes to direct law... active from about 5 kt up to about 10 kt above the stall warning speed... The pilot can override this demand... The α floor protection is inoperative." (00000331.0002001). | **MATCHES** (handout omits: pilot can override; α floor inoperative; "alternate law changes to direct law") |
| 32 | Alternate: "The PFD speed tape displays only Vsw (stall warning) as the top of a black/red band" (also Direct) | "VLS remains, but Vα PROT and Vα MAX disappear, replaced by a single black and red strip, the top of which is stall warning speed. Unlike VLS, which is stable, VSW is g sensitive" (00001949.0004001); "Vα prot and Vα max are replaced by Vsw (stall warning speed)" (00000331). | **MATCHES** |
| 33 | "An audio 'Stall, Stall' warning is available" (Alternate, Direct) | "stall alerts ('STALL, STALL' synthetic voice then cricket and 'STALL STALL' red message on PFD) are triggered at an appropriate margin from the stall condition" (00000331); Direct: "overspeed and stall warnings are available" (00000353). | **MATCHES** |

### Bank angle protection

| # | Handout claim | Current FCOM R17 statement (ident) | Verdict |
|---|---|---|---|
| 34 | "Bank 0°-33° stick free: bank angle automatically maintained; pitch trim automatically applied" | "Up to 33 °, the system holds the roll attitude constant when the sidestick is at neutral." (DSC-27-20-10-30-00000313.0002001 / 27 DEC 23); auto trim is the normal pitch law (00000271). | **MATCHES** |
| 35 | "33°-67°: stick free automatic roll back to 33°; stick full side 67° maintained" | "positive spiral static stability for bank angles above 33 °. If the pilot releases the sidestick at a bank angle greater than 33 °, the bank angle automatically reduces to 33 °... If the pilot holds full lateral sidestick deflection, the bank angle goes to 67 ° and no further." (00000313). Also: "When bank angle protection is active, auto trim is inoperative." | **MATCHES** (handout omits: auto trim inoperative when bank protection active) |
| 36 | "FD bars disappear when bank > 45°" | "If the bank angle exceeds 45 °, the **autopilot disconnects** and the FD bars disappear. The FD bars return when the bank angle decreases to less than 40 °." (00000313). | **MATCHES** (handout omits AP disconnect >45° and FD return <40°) |
| 37 | "Max bank angle=67° reduced to 45° when High Speed or High AOA protection active" | "If angle-of-attack protection, or high speed protection, **or negative pitch attitude protection** is operative, the bank angle will not go beyond 45 °" (00000313). | **STALE/incomplete** — third trigger (negative pitch attitude protection) missing |
| 38 | ALT 1: "Adjusts/restricts ailerons; amber bank limit symbols (x); bank 0-33 stick free stability; automatic pitch trim avail; max bank 67° with automatic roll back to 33°" | "Lateral control is similar to normal law, except that alterations of positive spiral static stability will not occur due to the loss of high AOA and high speed protection." (00000330); footnote (4): "Bank angle limitation remains effective in ALT 1, which uses roll normal. However... all protection marks on the PFD are in amber" (00000324). | **MATCHES** |
| 39 | ALT 2: "Direct Law: Stick→Aileron; amber bank limit symbols (x); yaw damper provides limited dutch roll damping; yaw damper provides turn coordination except clean" | ALT 2: "ROLL DIRECT LAW... maximum roll rate is approximately 20 to 25 °/s... **Spoilers 2, 3 and 6 are inhibited**... YAW ALTERNATE LAW: dutch roll damping function is available, and damper authority is limited to ± 4 ° rudder (CONF 0) and ± 15 ° (other configuration). Turn coordination is also provided, except in CONF 0." (00000344). Protections: "no bank angle protection in ALT 2 law; In case of failure of 2 ADRs, there is no low speed stability; In case of failure of 3 ADRs, there is no high speed stability." (00000345). | **MATCHES** (handout omits spoiler inhibits, roll-rate, rudder authority values, and ADR-failure carve-outs). Note: "no bank angle protection in ALT 2" makes the handout's amber bank-limit-symbol cell for ALT 2 consistent with crosses replacing symbols |

### Alternate high speed stability

| # | Handout claim | Current FCOM R17 statement (ident) | Verdict |
|---|---|---|---|
| 40 | "Above Vmo/Mmo up elevator is commanded to provide high-speed stability"; "Green overspeed symbol on PFD lost" | "Above VMO/MMO, a nose up demand is introduced to avoid an excessive increase in speed. The pilot can override this demand. The high speed protection symbol (VMO + 4) disappears. In addition, the overspeed warning... remains available." (00000331). | **MATCHES** (handout omits: pilot can override; and that **alternate law reduces MMO to 0.82** — "Alternate law reduces MMO to 0.82", 00001949.0004001) |

### MLA and turbulence damping

| # | Handout claim | Current FCOM R17 statement (ident) | Verdict |
|---|---|---|---|
| 41 | "MLA uses splrs+ails+elevs... when >+2.0g and in clean config and IAS>250kts" (Normal + Alternate); "Lost" in Direct | "MLA utilises spoilers 4, 5, and 6 and the ailerons... becomes active when the **sidestick is pulled more than 8 °, and the load factor is more than 2 g**... An elevator demand is simultaneously applied... only available, when: speed above 250 kt; FLAPS lever in the 0 position; In normal or alternate law flight mode." (DSC-27-20-10-40-00000320 / 27 DEC 23). | **MATCHES** (handout omits sidestick >8° condition; "lost in direct" consistent with the normal/alternate-only availability) |
| 42 | "Turbulence damping... if TURB DAMP pb ON and IAS>200kts **with AP ON**"; "Lost" in Alternate and Direct | "only available if: Aircraft in flight; speed greater than 200 kt; **Autopilot engaged or normal law active**; Aircraft within the normal flight envelope... may be manually inhibited by switching off the TURB DAMP pushbutton." (DSC-27-20-10-60-00000322 / 27 DEC 23). | **STALE/imprecise** — condition is "AP engaged **OR** normal law active" (not "with AP ON"), plus "within the normal flight envelope"; the pb inhibits (default on). The handout's flat "Lost in alternate" is not what the FCOM condition says (in alternate with AP engaged the availability condition can still be met) — FCOM wording controls; quote both when studying |

### Direct law

| # | Handout claim | Current FCOM R17 statement (ident) | Verdict |
|---|---|---|---|
| 43 | "PRIMs and/or SECs command aileron/elevator/rudder movement directly per SS/rudder pedal order"; "All protections lost"; "Manual THS pitch trim only" | "Pitch direct law is a direct stick to elevator relationship... the maximum elevator deflection varies as a function of the CG... As there is no automatic trim, the pilot has to use manual trim... All protections are inoperative. The α floor function is inoperative." (DSC-27-20-20-30-00000353 / 27 DEC 23). | **MATCHES** (handout omits CG-dependent elevator deflection) |
| 44 | Direct yaw: "Manual rudder contol only / Yaw damping and minimum turn coordination" | Direct law yaw/lateral page (DSC-27-20-20-30 P 2/2 onward) is not in the slice. | **NOT FOUND IN SLICE** — check FCOM DSC-27-20-20-30 P 2 (lateral/yaw in direct law) |
| 45 | Direct operational rec: "Avoid thrust changes & S/B use" | FCTM AOP-10-30-20 (01 MAY 24): "DIRECT LAW: The PF must avoid performing large thrust changes, or sudden speedbrake movements, particularly if the center of gravity is aft. If the speedbrakes are out... gently retract... to avoid a large nose down trim change." | **MATCHES** (via FCTM) |

### Abnormal attitude law

| # | Handout claim | Current FCOM R17 statement (ident) | Verdict |
|---|---|---|---|
| 46 | Entry when: Pitch >50°NU, or Pitch >30°ND, or Bank >125°, or AOA >30°, or AOA <-10°, or IAS >440 kt, or IAS <60 kt, or Mach >0.96, or Mach <0.01 | **Not in the slice** (it ends before the abnormal attitude law pages). Nothing in FCTM R5 text either. These nine trigger values are exactly the kind of numbers a revision can move — **do not trust them until read against R17**. | **NOT FOUND IN SLICE** — a human must check FCOM DSC-27-20-20 (Abnormal Attitude Law DU, after Direct Law) in the full R17 PDF |
| 47 | "During recovery: Pitch is Alt Law, Yaw is Alt Law, Roll is Dir Law"; "After recovery the above flight control laws remain in effect for the rest of the flight" | Not in slice; same section as #46. | **NOT FOUND IN SLICE** — same place to look |

### Mechanical backup

| # | Handout claim | Current FCOM R17 statement (ident) | Verdict |
|---|---|---|---|
| 48 | Entry: "Failure of all PRIM+SECs"; controls: manual pitch trim + rudder; SS inoperative | Not in slice. FCTM AOP-10-30-20 BACKUP (01 MAY 24) corroborates the technique: "backup enables the PF to safely stabilize the aircraft, **using the rudder and manual pitch trim**, while reconfiguring the systems... The pitch trim wheel is used to control pitch... The rudder provides lateral control, and induces a significant roll with a slight delay." | **NOT FOUND IN SLICE** for the entry condition; technique **MATCHES** FCTM. Check FCOM DSC-27-20-20 Mechanical Backup DU |
| 49 | "Manual rudder contol & yaw damper provided by the Backup Control Module (BCM) which is powered by the Backup Power System (BPS) which is driven by the Y or B hyd sys" | Not in slice; FCTM text only defines the abbreviation "BCM Back-up Control Module". | **NOT FOUND IN SLICE** — check FCOM DSC-27-10 (architecture) and DSC-27-20-20 Mechanical Backup pages, incl. which hydraulic systems drive the BPS |
| 50 | Mechanical operational rec: "Restore electrical power to PRIMs+SECs" | Not stated in slice/FCTM text found. | **NOT FOUND IN SLICE** (FCTM's "while reconfiguring the systems" is consistent in spirit) |

### Operational recommendations row

| # | Handout claim | Current FCOM R17 statement (ident) | Verdict |
|---|---|---|---|
| 51 | Alternate/Direct: "Descend to approximately REC MAX ALT - 4000'. REC MAX ALT is on PROG page." | FCTM AOP-10-30-20 (01 MAY 24): "When the aircraft is in reconfiguration law... At high altitude, descend to a lower altitude to increase the margin to buffet... **The maximum Flight Level (FL) is displayed on ECAM** and is associated to the failure mode that led to the re-configured control law." | **STALE** — current guidance is the failure-specific max FL on the ECAM, not "REC MAX − 4 000 ft from the PROG page". (Slice itself has no such row; FCTM is the current text source.) |
| 52 | Header reference "FCOM 1.27.20~30, 1.27.10 P11" | Current chapter is DSC-27-20-10 (Normal Law), DSC-27-20-20 (Reconfiguration Laws). | **STALE** (numbering scheme changed) |

---

## 2. Changed since Rev 4 (most significant first)

1. **High speed protection numbers/behavior (row 23).** Handout: "Max speed=Vmo+15/Mmo+0.04 with stick free." FCOM R17: stick free gives only a *slight* overshoot; with **full forward stick** nose-down authority reduces to zero at approx **VMO+16 / MMO+0.04**; and **AP disconnects at VMO+12 / MMO+0.03** (value absent from handout). Ident. 00000281 / 27 DEC 23.
2. **Alternate/Direct law speed limits (rows 5-6, 40).** "Alternate law reduces MMO to 0.82" (00001949) and the ECAM now shows **MAX SPEED 330 kt/M 0.82** (ALTN) and **330 kt/M 0.80** (Direct) (00000324); QRH status pages carry "MAX SPD : 330/.82". The handout has none of this.
3. **Reconfiguration descent guidance (row 51).** "REC MAX ALT − 4000' from the PROG page" is replaced by "the maximum Flight Level (FL) is displayed on ECAM and is associated to the failure mode" (FCTM AOP-10-30-20, 01 MAY 24).
4. **High AOA protection section rewritten 23 JAN 26** (00000280.0005001): explicit exit conditions (sidestick >8° forward; >0° forward for 1 s when α<αMAX; neutral/forward 0.5 s when α<αPROT), **αPROT = αMAX for 8 s at takeoff**, "This High AOA protection has **priority over all other protections**", and Mach-reduced αPROT at high altitude (buffet protection). None are in the handout.
5. **45° bank cap has a third trigger** — negative pitch attitude protection (00000313); handout lists only high speed / high AOA. Also new: AP disconnects at bank >45°, FD bars return <40°.
6. **THS 1.3 g limitation also applies with bank outside ±33°** (00000271); handout gives only the >1.3 g trigger.
7. **Turbulence damping availability** is "Autopilot engaged **or normal law active**" plus normal-envelope condition (00000322) — not "with AP ON", and the pb *inhibits* rather than arms.
8. **Alternate low-speed stability**: FCOM adds that the demand is overridable, "alternate law changes to direct law" at low speed, and **α floor is inoperative in alternate** (00000331).
9. **MLA activation now stated as sidestick >8° pull AND >2 g**, using spoilers 4/5/6 + ailerons with elevator compensation (00000320).
10. Minor: ECAM title spelling "FLT CTL ..." (handout: "FLT CTRL"); PFD message string "USE MAN PITCH TRIM".

## 3. FCOM emphases the handout omits entirely

- **Protections are not structural-limit protections** and "the PF must not deliberately exceed the normal flight envelope" (DSC-27-20-10-10, 00000268) — a stated oral-question favorite of the chapter.
- **Auto pitch trim frozen cases**: manual trim order; RA <100 ft (flare); load factor <0.5 g; high speed protection (00000271).
- **Ground mode and flare mode**: rotation is flown in direct law; at 100 ft RA THS freezes and flare mode (quasi-direct) begins; at 50 ft a slight pitch-down order requires a gentle nose-up flare (00000269, 00000273). Dual RA failure: flare law introduced at gear extension with both APs off; the 50-ft pitch-down effect no longer applies (00000324 note 1).
- **High AOA exit conditions, 8-s takeoff αPROT=αMAX, protection priority, Mach-varying αPROT** (00000280.0005001, 23 JAN 26).
- **Low energy alert mechanics**: repeated every 5 s; computed from configuration/deceleration/FPA; trigger examples (VLS−8 at FPA −3°); full inhibition list incl. "in alternate or direct law" (00000282).
- **Normal-law roll rate 15 °/s max**; ALT 2 roll direct rate 20-25 °/s; **spoilers 2, 3, 6 inhibited in ALT 2**; rudder damper authority ±4° (CONF 0)/±15° (00000312, 00000344).
- **ALT 2 ADR carve-outs**: 2 ADRs failed → no low speed stability; 3 ADRs failed → no high speed stability (00000345); recon-table footnotes on VS1g computation failure and ADR DISAGREE (00000324).
- **Direct law elevator deflection varies with CG** (00000353); FCTM handling advice for reconfiguration laws (small inputs; roll always direct — AOP-10-30-20).
- **"MAN PITCH TRIM ONLY" in red is specifically the dual-elevator-failure case** (00000324 footnote 5).
- Alpha floor availability window (lift-off to 100 ft RA at landing) and engine-failure inhibits; TOGA LK and cancellation via A/THR instinctive disconnect (FCTM AS-FG-10-2, 27 MAR 26).

## 4. Coverage note / honesty

The Drive slice ends at DSC-27-20-20-30 P 1/2. Everything about the **Abnormal Attitude Law entry values (rows 46-47), Direct-law yaw (44), and Mechanical Backup/BCM/BPS (48-50)** is UNVERIFIED here: no verdict on those numbers was inferred from memory of other Airbus types, because A330 protections differ. The reconfiguration failure table (row 8) and the PFD symbol figures are graphics that do not survive text extraction (UNVERIFIABLE FROM TEXT) — verify on the R17 PDF pages cited above.
