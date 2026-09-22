# Phase Flows vs FCOM audit, 2026-09-22

Scope: data/phase_flows.json normal phases (Preflight through Parking) against A330P FCOM R17 PRO-NOR-SOP-03 to SOP-22 (extract A330P_FCOM_R17_PRO-NOR.md). Three loops as agreed: (1) automated coverage diff plus phase-by-phase read, fixes in build_scripts/gen/gen_phase_flows.py; (2) re-run diff, fix residue; (3) re-run diff, role scan, render sweep, hand read of every new item. Portal build v3.2.

Method: every FCOM action line of the form ITEM ...... ACTION ROLE was extracted (744 lines, 551 in scope after dropping the SOP-05 exterior walkaround inspection list) and matched against the portal item titles, sub bullets and quotes of the mapped phase. Roles compared PF / PM / PF-PM / CM1 / CM2 against the portal r field. Every added quote is proven literal by verify_phase_flows.py (550 quotes, 0 failures).

## Result

Loop 1: 162 FCOM lines had no portal match, 45 matched the item but not the action. Loop 2 after fixes: 13 unmatched, all wording artifacts (checklist rows rendered as cl items, FCOM typo ANNUCIATOR, items present in sub bullets). Loop 3: 0 unclassified mismatches, 0 role mismatches after reading the 48 automated flags (all first-hit artifacts), 0 verify failures, 0 console errors across 208 checklist and 3 viewport sweeps.

## Fixed (gen_phase_flows.py)

Cockpit Preparation (SOP-04 / SOP-06)
- Batteries: added EXT PWR pb ON and the already-supplied case (23.5 V).
- RMP: added ACP INT knob PRESS OUT/VOLUME CHECK and VHF CHECK.
- APU FIRE: added APU AGENT light CHECK OFF and APU FIRE TEST pb PRESS and MAINTAIN.
- APU start: added APU pb (ECAM) PRESS and EXT PWR pb AS RQRD.
- MCDU pre-initialization (CM1): was only MCDU ON; now carries ANNUNCIATOR LIGHTS OFF, A/C STATUS CHECK, ACTIVE NAV DATABASE CYCLE, FMS DATABASE VALIDITY CHECK, NAVAID DESELECTION AS RQRD, FLIGHT PLAN UPLINK REQUEST.
- Logbook: added AIRCRAFT CONFIGURATION SUMMARY CHECK.
- Before walkaround: added MIN FLT CREW OXY CHART CHECK PRESSURE; ALTN BRAKING now lists the six-step FCOM sequence.
- Overhead panel scan: was one line (ALL WHITE LIGHTS OFF); now every SOP-06-A line in FCOM order (RCDR GND CTL through DATA LOADER, 30 items).
- Front instrument panels: added DMC AUTO, ECAM/ND NORM, CLOCK, LDG GEAR GRVTY EXTN OFF, A/SKID & N/W STRG ON.
- Center pedestal: added ACP, HF, brakes triple indicator, ANN LT, cockpit door, ECAM control panel selectors, thrust and reverser levers, ENG MASTER and START, ATC/TCAS/ALT RPTG/ATC SYS, ACARS MSG ERASE and ADS CHECK ARMED.
- FMS preparation: was INIT A only; now IDLE/PERF FACTOR, INIT A, F-PLN (departure, enroute, step alts, arrival, ETP, FIX INFO, equitime), SEC F-PLN, RADIO NAV, INIT B, PERF TAKE OFF / CLB / CRZ / DES, PROG BRG/DIST, RNP, DERATED CLIMB, PRESET SPEEDS.
- Glareshield: added LOUDSPEAKER knob and the FCU (SPD/MACH dashed, HDG-V/S, ALT window).
- PFD and ND: added brightness knob.
- PRESS / STS card: noted that FUEL pb is the quick reference flow; FCOM SOP-06 lists PRESS and STS.

Before Push / Before Start (SOP-07 / SOP-08)
- Added LOAD CLOSEOUT (MACTOW) CG vs ECAM CG check (2 % rule).
- Added LOAD CLOSEOUT VERBAL CROSS-CHECKS (passenger and jumpseat count, JetPack flight deck report, flight and tail number, dispatch release, remarks).
- FINAL TAKEOFF DATA check now lists the twelve TPR/TLR items and the PF then PM FMS TAKEOFF DATA CHECK/REVISE.
- Added PITOT COVERS REMOVED, AIR CONDITIONING UNITS CHECK DISCONNECTED, EXT PWR CHECK AVAIL / DISCONNECTION REQUEST.
- Park brake item now includes ACCU PRESS CHECK.
- Added the pushback sequence: PARK BRK ON, N/WS DISC MEMO CHECK DISPLAYED, checklist, PARK BRK OFF on ground crew clearance, PARK BRK ON and BRAKE PRESS CHECK when complete, CLEARED TO DISCONNECT.
- New ENGINE START section (SOP-08): THRUST levers IDLE, ENG START IGN START, ENGINE 1 START announce and MASTER ON, ENG IDLE PARAMETERS CHECK with the ISA sea level values, ENGINE 2 START.

After Start (SOP-09)
- Added X BLEED selector AS RQRD (one engine taxi) and WING ANTI-ICE pb-sw AS RQRD.

Taxi (SOP-10 / SOP-10B)
- Added TAXI clearance OBTAIN with NOSE TAXI, RWY TURN OFF ON, PARK BRK OFF, BRAKES PRESSURE CHECK AT ZERO.
- PFD/ND check now states what to check.
- New DEPARTURE CHANGE section: FINAL TAKEOFF PERF DATA RECOMPUTE, FMS REVISE, REVISED FMS CROSSCHECK, FLAPS lever SET, FCU ALT SET, T.O CONFIG TEST, RE-BRIEFING, Departure Change checklist.

Line-Up (SOP-11)
- Added RNP AR departure GPS checks, FMA CHECK (NAV armed), SLIDING TABLE and EFB STOW.

Climb (SOP-14) and Descent Preparation (SOP-16)
- Added CLIMB SPEED MODIFICATIONS AS RQRD and RADAR ADJUST AS APPROPRIATE (climb and descent prep).

After Landing (SOP-21 / SOP-21B)
- Added ATC AS RQRD, BRAKE TEMPERATURE MONITOR with the maintenance thresholds, BRAKE FAN AS RQRD.
- New ENGINE 2 SHUTDOWN DURING TAXI-IN section: COOLING TIME ELAPSED, ENG 2 SHUTDOWN order, APU START CHECK AVAIL, ENG 2 ANTI ICE OFF, ENG 2 MASTER OFF, ENG 2 PARAMETERS CHECK.

Limitations phase (found by the audit, not a FCOM procedure item)
- gen_phase_flows.py was pulling the freighter drill cards (fleet toggle added 2026-09-17) into the PAX limitations phase, doubling every section on a rebuild. Now filtered to fleet pax or both. The committed data had been generated before the toggle, so the live page was unaffected until the next regeneration.

## Deliberate omissions and known deviations

- SOP-05 exterior walkaround inspection list (193 lines) is not a flight deck flow; the walkaround stays a trigger in Before Walkaround.
- Cockpit Preparation order follows Ryan's ten memorization groups, not the FCOM page order; every FCOM line is inside one of the groups.
- FUEL ON BOARD is FCOM PF-PM; the portal tags it PM inside the PM 3 CHECKS group (memorization structure, 2026-09-21).
- FUEL pb in the PF 2 CHECKS card comes from the quick reference flow card, not FCOM SOP-06.
- Approach and landing phases cite PRO-NOR-SOP-18 (not in the SOP-03 to SOP-22 line extract) and were read by hand: no gaps found.
- Freighter-only lines ([A330F]) are excluded, portal is PAX.

Verification: verify_phase_flows.py failures 0 (550 quotes); verify_flows_trainer.py fail 0 (788 quotes); resection asserts unchanged (CM2 4/7/4, PF 2, PF 3, PM 10, 4, PF 2, PM 3, 3); checklist sweep 208 checks clean; viewport sweep 390/1180/1280 px 0 console errors.
