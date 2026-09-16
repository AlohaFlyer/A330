#!/usr/bin/env python3
"""Deterministic content transform for mcdu_preflight.html.

Input : the freshly cloned, palette- and string-mapped B787 cdu_preflight.html
        (default: ./mcdu_preflight.html, or the path given as argv[1]).
Output: ./mcdu_preflight.html with the A330 MCDU cockpit-preparation page flow
        (FCOM R17 PRO-NOR-SOP-04 FMGS pre-initialization, PRO-NOR-SOP-06 FMGES
        preparation, and the PF/PM split those SOPs state), plus data/mcdu.json,
        the corpus docs [{t, x, r}] with verbatim SOP text for assist.js.

Only text content changes: header .src, the SVG title/desc/node labels, the card
h2/ul blocks and the footer text. Every CSS rule, class, id, attribute and the SVG
geometry (viewBox 680x1156, rect positions, group fills as the palette engine mapped
them) stay identical to the clone. Nothing here hardcodes a manual revision; it is
read from manuals.json.
"""
import json, os, re, sys, html
os.chdir(os.path.join(os.path.dirname(__file__), '..'))
SRC = sys.argv[1] if len(sys.argv) > 1 else 'mcdu_preflight.html'
M = json.load(open('manuals.json', encoding='utf-8'))
FR = M['A330P_FCOM']['revision']            # "R17"
REF = 'PRO-NOR-SOP-04, SOP-06'               # the two SOP sections the page flow spans
S04 = 'FCOM PRO-NOR-SOP-04'
S06 = 'FCOM PRO-NOR-SOP-06'

# ---------------------------------------------------------------- content spec
# Each group: (svg header label, card h2, [nodes]); node = (svg label, svg sub, card li html,
# [corpus docs (t, x, r)]). x is verbatim FCOM text (whitespace-normalized substring), r the ref.
TOP = ('ATIS  (CM2 obtains)', 'RUNWAY IN USE, ALTIMETER SETTING, WEATHER DATA · SOP-04')
BOTTOM = ('DEPARTURE LEGS VERIFICATION  (BOTH)',
          'PF reads the ND (PLAN, CSTR), PM verifies the paper · F-PLN DIST and EFOB vs release · SOP-06')

GROUPS = [
 ('1  -  FMGS PRE-INIT (CM1)', '1 - FMGS Pre-Initialization (CM1, SOP-04)', [
  ('DATA', 'A/C STATUS: model, ENG TRENT772B-60; cycle ACTIVE NAV DATABASE; validity; SEL NAVAIDS',
   '<b>DATA</b> (CM1): MCDU ON (short press BRT); no amber annunciator lights; wait out the 3 min FMGS/FCU power-up tests. A/C STATUS [4L]: model A330-200 or A330-300, ENG type TRENT772B-60. ACTIVE NAV DATABASE: cycle the Second NAV Database [3L] twice to erase pilot and uplinked data, DELETE ALL [5R] if STORED shows anything. FMS DATABASE VALIDITY: day, month, year (HAL8YYMMNN). NAVAID DESELECTION as required: DATA, POSITION MONITOR [1L], SEL NAVAIDS [6R], DESELECT [1R].',
   [('DATA: A/C STATUS', 'Press the DATA button on the MCDU, then press the A/C STATUS [4L] to access the A/C STATUS page. Check of the A/C STATUS page: ‐ Check the model number is A330-200 or A330-300, as applicable. ‐ Check the ENG type: TRENT772B-60', S04 + ' FMGS Pre-Initialization, DATA page'),
    ('DATA: ACTIVE NAV DATABASE cycle', 'Select the Second NAV Database [3L] to activate the non-current database, and then re-select the Second NAV Database [3L] again to activate the current NAV Database. Cycling the FMS Active NAV Database erases all Pilot entered and/or Uplinked data. ‐ Check that all pilot stored data has been erased. If any data is displayed in the STORED field [4R], select the DELETE ALL [5R] prompt.', S04 + ' FMGS Pre-Initialization, DATA page'),
    ('DATA: FMS DATABASE VALIDITY', 'Verify the Day, Month, and Year is correct for the ACTIVE NAV DATABASE: ‐ Month and Day (2L) – e.g., “26MAR-22APR” shows the day and month that the NAV Database is active. ‐ Year (2R) - The Database code shows the two-digit year in the NAV Database name. The naming convention is HAL1YYMMNN where “YY” = Year, “MM” = Month, “NN” = Sequence.', S04 + ' FMGS Pre-Initialization, DATA page'),
    ('DATA: NAVAID DESELECTION', 'If NOTAMs warn of any unreliable or unserviceable DME or VOR/DME, access the SELECTED NAVAIDS page and deselect the related NAVAID using the DESELECT field [1R]. Access the SELECTED NAVAIDS page by beginning on the MCDU DATA page and then selecting POSITION MONITOR [1L] followed by SEL NAVAIDS [6R].', S04 + ' FMGS Pre-Initialization, NAVAID deselection'),
    ('MCDU power-up wait', 'At electrical power-up, the FMGSs and FCU run through various internal tests. Allow enough time (3 min) for tests’ completion, and do not start to press pushbuttons until the tests are over. If the “PLEASE WAIT” message appears, do not press any MCDU key until the message clears.', S04 + ' FMGS Pre-Initialization, Check the MCDU')]),
  ('INIT A  (PART 1)', 'FLT NBR [3L] exactly as on the release, INIT REQUEST* [2R]; do not enter TO/FROM',
   '<b>INIT A (PART 1)</b> (CM1): INIT key. Enter the flight number in FLT NBR [3L] exactly as it appears on the ATC Flight Plan section of the dispatch release (e.g. HAL25), then INIT REQUEST* [2R]. Do not enter TO/FROM [1R] or the INIT REQUEST* prompt will not appear; a wrong TO/FROM is cleared by cycling the NAV database.',
   [('INIT A (Part 1): FLIGHT PLAN UPLINK request', 'Press the INIT button on the MCDU to display the INIT A page. To Request the Flight Plan Uplink: ‐ Enter the flight number in the FLT NBR field [3L] exactly as it appears on the ATC Flight Plan section of the dispatch release/flight plan (e.g., “HAL25”).', S04 + ' FMGS Pre-Initialization, INIT A page (Part 1)'),
    ('INIT A (Part 1): TO/FROM trap', 'Do not enter TO/FROM field [1R] or the INIT REQUEST* prompt will not appear. If the TO/FROM field is already entered, the flight plan can be deleted by cycling the FMS NAV Database.', S04 + ' FMGS Pre-Initialization, INIT A page (Part 1)')]),
 ]),
 ('2  -  INIT A (PF)', '2 - INIT A, Part 2 (PF, SOP-06)', [
  ('INIT A  (PART 2)', 'TO/FROM check, ALTN enter, FLT NBR, COST INDEX, CRZ FL/TEMP check, TROPO as rqrd',
   '<b>INIT A (PART 2)</b> (PF): first IDLE / PERF FACTOR check. INIT key. TO/FROM [1R] confirms the uplink; wrong means cycle the NAV database. ALTN [2L] enter from the release. FLT NBR [3L], COST INDEX [5L], CRZ FL/TEMP [6L] check against the release. TROPO [5R] optional, improves predictions.',
   [('INIT A (Part 2): TO/FROM', 'Press the INIT button on the MCDU to display the INIT A page. Check the TO/FROM field [1R] to confirm the correct flight plan uplink occurred. If the TO/FROM field is incorrect, the flight plan can be deleted by cycling the FMS NAV Database', S06 + ' FMGES Preparation, INIT A page (Part 2)'),
    ('INIT A (Part 2): ALTN', 'Enter the Alternate airport from the dispatch release/flight plan into the ALTN field [2L]. The ALTN route may be defined manually on the F-PLN page', S06 + ' FMGES Preparation, INIT A page (Part 2)'),
    ('INIT A (Part 2): FLT NBR', 'Check the FLT NBR field [3L] to confirm it matches the dispatch release/flight plan.', S06 + ' FMGES Preparation, INIT A page (Part 2)'),
    ('INIT A (Part 2): COST INDEX', 'Check the Cost Index field [5L] to confirm it matches the dispatch release/flight plan.', S06 + ' FMGES Preparation, INIT A page (Part 2)'),
    ('INIT A (Part 2): CRZ FL/TEMP', 'Check the Cruise Flight Level field [6L] to confirm it matches the dispatch release/flight plan.', S06 + ' FMGES Preparation, INIT A page (Part 2)'),
    ('INIT A (Part 2): TROPO', 'Entry of the tropopause altitude into the TROPO field [5R] is optional but improves the precision of the FMS predictions.', S06 + ' FMGES Preparation, INIT A page (Part 2)'),
    ('IDLE / PERF FACTOR', 'Refer to DSC-22_20-10-40-30 Procedure to Modify the PERF and IDLE Factors.', S06 + ' FMGES Preparation, IDLE / PERF FACTOR')]),
  ('WIND', 'WIND [5R]: CLB, CRZ, DES pages; verify the uplink, else WIND REQUEST* or manual entry',
   '<b>WIND</b> (PF): WIND [5R], NEXT PHASE / PREVIOUS PHASE through CLIMB, CRUISE, DESCENT. Verify the automatic wind uplink came with the flight plan. If NO ANSWER TO REQUEST: WIND REQUEST* [2R], or enter the release winds by hand (cruise: initial CRZ waypoint, then waypoints with a 30 kt, 30 deg or 5 deg SAT change or a step). To get an altitude that did not uplink, enter 0/0/350 and send again.',
   [('WIND pages', 'Select WIND [5R] to view the pages for the Climb phase, Cruise phase, and Descent phase. Use the NEXT PHASE [5R] or PREVIOUS PHASE [5L] to cycle through the pages with winds for each phase.', S06 + ' FMGES Preparation, INIT A page (Part 2)'),
    ('WIND uplink', 'Verify the automatic wind uplink occurred. The winds should uplink and insert automatically when the flight plan uplinks into the FMS.', S06 + ' FMGES Preparation, INIT A page (Part 2)'),
    ('WIND request for another altitude', 'The flight crew can request winds for additional altitudes that were not uplinked by first replacing the current winds data with zeros and then sending the wind request again. For example, to request winds for FL 350, enter “0/0/350” for the wind and then send the wind request again.', S06 + ' FMGES Preparation, INIT A page (Part 2)'),
    ('WIND: no uplink', 'If winds do not uplink (“NO ANSWER TO REQUEST”): ‐ Request wind uplink. Select WIND REQUEST* [2R] to manually request a wind uplink.', S06 + ' FMGES Preparation, INIT A page (Part 2)'),
    ('CRUISE WIND page manual entry', 'Enter the winds at the waypoint corresponding to the initial cruise altitude and then at subsequent waypoints which reflect significant wind/temperature changes (30 knot difference, 30 degree wind direction difference, or 5 degree SAT temperature difference) or changes in cruise altituted (step climb/descent).', S06 + ' FMGES Preparation, INIT A page (Part 2)')]),
 ]),
 ('3  -  F-PLN / SEC F-PLN / RAD NAV', '3 - F-PLN, SEC F-PLN, RAD NAV (PF, SOP-06)', [
  ('F-PLN  DEPARTURE', 'LAT REV at the departure airport [1L], DEPARTURE, RWY, SID and transition, TMPY INSERT*',
   '<b>F-PLN DEPARTURE</b> (PF): FPLN key. LAT REV at the departure airport [1L], DEPARTURE [1L], select the RWY, the SID and SID transition; verify RWY [1L], SID and transition [1R] on the top row; TMPY INSERT* [6L]. To change the RWY with a SID already in, slew back to departure page 1.',
   [('F-PLN: DEPARTURE RWY and SID', 'Press the FPLN button on the MCDU to display the FPLN page. ‐ Perform a LAT REV at the departure airport [1L]. ‐ Select DEPARTURE [1L]. ‐ Select the RWY. ‐ Select the SID and SID transition. ‐ Review the top row of the MCDU to verify the correct RWY [1L], SID, SID Transition [1R].', S06 + ' FMGES Preparation, F-PLN page'),
    ('F-PLN: change RWY with SID entered', 'To change a RWY if the SID is already entered, use the Arrow buttons [horizontal slew] to scroll back to the departure page 1, then select a different runway.', S06 + ' FMGES Preparation, F-PLN page')]),
  ('F-PLN  ENROUTE / ARRIVAL', 'waypoints and airways check, STEP ALTS; LAT REV at arrival [6L], ARRIVAL, APPR, STAR, INSERT',
   '<b>F-PLN ENROUTE and ARRIVAL</b> (PF): check ENROUTE WAYPOINTS and AIRWAYS; enter STEP ALTS. LAT REV at the arrival airport [6L], ARRIVAL [1R], select the APPR, the STAR and STAR transition; verify APPR [1L], APPR VIA [2L], STAR [1R], STAR transition [2R]; TMPY INSERT* [6L].',
   [('F-PLN: ARRIVAL RWY/APPR and STAR', '‐ Perform a LAT REV at the arrival airport [6L]. ‐ Select ARRIVAL [1R]. ‐ Select the APPR. ‐ Select the STAR and STAR transition. ‐ Review the top two rows of the MCDU to verify the correct APPR [1L], APPR VIA [2L], STAR, [1R] and STAR Transition [2R].', S06 + ' FMGES Preparation, F-PLN page')]),
  ('ETOPS: STORED WPTS / FIX INFO / EQUITIME', 'ETPs as STORED WAYPOINTS, not in the F-PLN; FIX INFO REF FIX at the FROM wpt; EQUITIME POINT',
   '<b>ETOPS</b> (PF, if an ETOPS segment is planned): DATA, right arrow to DATA INDEX page 2, STORED WAYPOINTS [1R], name ETP1 etc., enter LAT/LONG from the flight plan, STORE [6R]. Do not enter the ETPs as waypoints in the flight plan. FIX INFO: F-PLN, LAT REV at the FROM waypoint [1L], FIX INFO [1R], REF FIX [1L] = the stored ETP (max 4 FIX INFO waypoints). EQUITIME POINT: DATA, EQUITIME POINT, ETOPS alternates in [1L] and [3L] with TRU WIND [2L] and [4L] at CRZ FL.',
   [('ETOPS: ETP waypoints', '‐ Select DATA key. ‐ Select the RIGHT ARROW key to display DATA INDEX page 2. ‐ Select STORED WAYPOINTS key [1R]. ‐ Name the point using the IDENT field (e.g., ETP1). ‐ Enter the LAT/LONG from the flight plan and STORE [6R].', S06 + ' FMGES Preparation, F-PLN page, ETP waypoint(s)'),
    ('ETOPS: ETPs not in the flight plan', 'Do not enter the ETP’s as waypoint into the FMS flight plan.', S06 + ' FMGES Preparation, F-PLN page, ETP waypoint(s)'),
    ('ETOPS: FIX INFO reference points', '‐ Select F-PLAN key. ‐ Make a lateral revision at the FROM waypoint [1L]. ‐ Select FIX INFO [1R]. ‐ Enter desired STORED WPT (i.e., “ETP1”) under REF FIX [1L].', S06 + ' FMGES Preparation, F-PLN page, FIX INFO reference point(s)'),
    ('ETOPS: FIX INFO limit', 'A maximum of 4 FIX INFO database waypoints may exist at any given time.', S06 + ' FMGES Preparation, F-PLN page, FIX INFO reference point(s)'),
    ('ETOPS: EQUITIME POINT', 'Modify the FMS generated EQUITIME POINT. This displays an FMS generated ETP pseudo-waypoint on the ND. ‐ Select DATA key. ‐ Select the EQUITIME POINT prompt. ‐ The EQUITIME POINT page is displayed. The origin and destination airports are used by default. ‐ Enter the ETOPS alternate in the [1L] field. ‐ Enter the associated wind in the TRU WIND [2L] field.', S06 + ' FMGES Preparation, F-PLN page, EQUITIME POINT')]),
  ('SEC F-PLN', 'copy of the active F-PLN; modify for an immediate return, a diversion, or a RWY/SID change',
   '<b>SEC F-PLN</b> (PF): routinely a copy of the active flight plan, but consider: copy and modify at a suitable waypoint for an immediate return (engine failure); if departure weather is below landing minima, the diversion right after takeoff; if a runway or SID change during taxi is likely, copy and pre-modify.',
   [('SEC F-PLN', 'This is routinely a copy of the active flight plan. However, consideration may be given to the following: a. Copy the active F-PLN, but modify it at a suitable WPT for an immediate return to the departure airfield in the event of, for example, engine failure. b. If weather is below landings minima at the departure airfield, the secondary flight plan should be that required for a diversion immediately after takeoff. c. If there is a chance of a change in runway or SID during taxi, prepare for it by copying the active flight plan and making the necessary modifications.', S06 + ' FMGES Preparation, SEC F-PLN page')]),
  ('RAD NAV', 'check the VOR, ILS and ADF the FMGC tuned; modify as rqrd; correct ident on ND and PFD',
   '<b>RAD NAV</b> (PF): check the VOR, ILS and ADF tuned by the FMGC; modify if required and check the correct identifier is displayed on the ND and PFD (VOR, ILS). If unsatisfactory, go through the audio check.',
   [('RAD NAV', '‐ Check the VOR, ILS, and ADF tuned by the FMGC. ‐ Modify them if required, and check that the correct identifier is displayed on the ND and PFD (VOR, ILS). If unsatisfactory, go through the audio check.', S06 + ' FMGES Preparation, RAD NAV page')]),
 ]),
 ('4  -  INIT B (FUEL PRED)', '4 - INIT B, INIT FUEL PRED (PF, SOP-06)', [
  ('INIT B', 'TAXI, RTE RSV / % = 0, ALTN/TIME (greater value), FINAL/TIME, ZFW/ZFWCG, BLOCK, EXTRA/TIME',
   '<b>INIT B</b> (PF): INIT then horizontal slew (labeled INIT FUEL PRED on some FMGS). TAXI [1L] adjust only for a large disparity. RTE RSV / % [3L] = 0 so EXTRA shows the fuel you actually manage (the dispatcher carries route reserve as 10 PCT TIME). ALTN/TIME [4L]: if the release ALTN fuel differs from the FMS value, enter the greater; pilot entries overwrite the FMS and must be cleared or redone when the alternate, routing or altitude changes. FINAL/TIME [5L]: Final Reserve per FOM fuel policy, 30 min holding at 1 500 ft AFL, protected. ZFW/ZFWCG [1R] from the release if not auto-populated, ZFWCG may stay blank. BLOCK [2R]: FOB from the E/WD once fueled, else Ramp Fuel from the release. EXTRA/TIME [6R] check. INIT B is not available after engine start.',
   [('INIT B: display', 'Pressing the INIT button on the MCDU will display the INIT A page. Pressing the left or right arrow button [horizontal slew] will display the INIT B page. On some FMGS, the INIT B page is labeled \'INIT FUEL PRED\' on the ground, but retains all INIT B functions.', S06 + ' FMGES Preparation, INIT B (INIT FUEL PRED) page'),
    ('INIT B: TAXI', 'If there is a large disparity in taxi fuel from the dispatch release/flight plan, then adjust the Taxi Fuel [1L] if desired.', S06 + ' FMGES Preparation, INIT B (INIT FUEL PRED) page'),
    ('INIT B: RTE RSV / %', 'Insert “0” in the RTE RSV / % [3L]. Setting the Route Reserve to zero will adjust the Extra fuel number to more accurately indicate the extra fuel available to the flight crew to manage during the flight. Route reserve is a regulatory planning requirement which the dispatcher accounts for in the “10 PCT TIME” field of the dispatch release/flight plan.', S06 + ' FMGES Preparation, INIT B (INIT FUEL PRED) page'),
    ('INIT B: ALTN/TIME', 'If the ALTN fuel listed on the dispatch release/flight plan is different than the FMS computed ALTN fuel [4L]: Enter the greater of these two values.', S06 + ' FMGES Preparation, INIT B (INIT FUEL PRED) page'),
    ('INIT B: ALTN fuel pilot entry caution', 'Any value the pilot places in the ALTN fuel field will overwrite the FMS computed values. Therefore, to ensure accuracy, if a change occurs (e.g., if a different alternate is selected, or the routing to the alternate changes, or the alternate cruise altitude/speed is updated) then the flightcrew should either overwrite or clear any previous pilot entered data placed in this field.', S06 + ' FMGES Preparation, INIT B (INIT FUEL PRED) page'),
    ('INIT B: FINAL/TIME', 'Check that the FINAL/TIME field [5L], enter the Final Reserve Fuel as established in the FOM Fuel Management policy. This fuel must be protected by the flight crew. Final Reserve Fuel represents', S06 + ' FMGES Preparation, INIT B (INIT FUEL PRED) page'),
    ('INIT B: Final Reserve definition', 'the amount of fuel to fly for 30 min at holding speed at 1 500 ft AFL above the alternate airport (or destination if no alternate is required) in ISA conditions.', S06 + ' FMGES Preparation, INIT B (INIT FUEL PRED) page'),
    ('INIT B: ZFW/ZFWCG', 'Enter the planned Zero Fuel Weight (ZFW) [1R] from the dispatch release/flight plan. If the ZFWCG is unknown, leave the ZFWCG field empty and the FMS will use a default CG from it’s performance database to compute fuel preditions.', S06 + ' FMGES Preparation, INIT B (INIT FUEL PRED) page'),
    ('INIT B: BLOCK', '‐ If the aircraft has been fueled for flight, verify the correct amount is onboard by comparing with the Ramp Fuel on the dispatch release/flight plan, then enter the FOB (from the E/WD) in the Block fuel field [2R]. ‐ If the aircraft fueling has not been completed yet, then initially enter the Ramp Fuel from the dispatch release/flight plan as the Block fuel.', S06 + ' FMGES Preparation, INIT B (INIT FUEL PRED) page'),
    ('INIT B: EXTRA/TIME', 'Check the EXTRA/TIME field [6R] to determine how much extra fuel is available to the flight crew to manage during the flight. Note: The INIT B page is not available after engine start.', S06 + ' FMGES Preparation, INIT B (INIT FUEL PRED) page')]),
 ]),
 ('5  -  PERF / PROG', '5 - PERF and PROG (PF, SOP-06)', [
  ('PERF TAKE OFF', 'SHIFT as rqrd; THR RED/ACC and ENG OUT ACC set or check (default 1 000 ft above the rwy)',
   '<b>PERF TAKE OFF</b> (PF): PERF key. SHIFT: insert a T.O shift for an intersection takeoff even with GPS PRIMARY. THR RED/ACC and ENG OUT ACC: set or check, default 1 000 ft above departure runway altitude, modify for the expected RWY/SID. A takeoff data uplink deletes previously entered THR RED / ACCEL ALT (SOP-07 Takeoff Data). TPR/TLR data goes in later, before pushback.',
   [('PERF TAKE OFF: SHIFT', 'If the aircraft takes off from an intersection, insert a T.O shift value (even when GPS PRIMARY is active) to increase flight crew awareness of the runway length reduction.', S06 + ' FMGES Preparation, PERF page'),
    ('PERF TAKE OFF: THR RED/ACC', 'Default settings will be 1 000 ft above departure runway altitude. Modify if necessary for the anticipated RWY/SID for takeoff.', S06 + ' FMGES Preparation, PERF page'),
    ('PERF TAKE OFF: uplink deletes THR RED/ACC', 'A takeoff data performance uplink will delete previously entered data (THR RED / ACCEL ALT).', S06 + ' FMGES Preparation, PERF page')]),
  ('PERF CLB / CRZ / DES', 'PRESEL as rqrd; DRT CLB D1/D2 as rqrd; DES crossover 300 kt, or the STAR transition speed',
   '<b>PERF CLB, CRZ, DES</b> (PF): NEXT PHASE [6R] through the pages. CLB and CRZ PRESEL speed as required (green dot for a close-in turn or constraint, a CRZ Mach; cancel with ECON before the phase activates). DRT CLB as required: D1 for TOW below 463 000 lb, D2 below 441 000 lb. DES: descent Mach equals end-of-cruise Mach, edit the crossover speed [3L] to 300 kt, or the published STAR transition speed (HAWKZ4 into SEA is 280 kt). SPD LIM 250 kt below 10 000 ft is cleared or changed on the VERT REV page.',
   [('PERF CLB page', 'Pressing the NEXT PHASE [6R] button will display the PERF CLB page.', S06 + ' FMGES Preparation, PERF page'),
    ('PERF DES: crossover speed', 'Ensure the descent Mach number matches the end of cruise Mach number, and edit the crossover speed [3L] to 300 kt.', S06 + ' FMGES Preparation, PERF page'),
    ('PERF DES: STAR transition speed', 'Use caution; certain STARS use a published transition speed to be used at the crossover point, i.e. “HAWKZ4” arrival in SEA calls for 280 kt. In these cases edit the transition speed to the value called for in the STAR.', S06 + ' FMGES Preparation, PERF page'),
    ('DERATED CLIMB', 'If a derated climb is planned, insert the derated climb level (D1 or D2) in the DRT CLB field of the MCDU PERF CLB page. Note: The flight crew may insert: D1 for Takeoff Weights < 463 000 lb. D2 for Takeoff Weights < 441 000 lb.', S06 + ' FMGES Preparation, Derated Climb Level Insertion'),
    ('PRESET SPEEDS', 'If the flight is cleared for a close-in turn or close-in altitude constraint, the flight crew may preselect green dot speed on the PERF CLB page. Once the CLB phase is active, the preselected speed will be displayed in the FCU speed window and on the PFD as a selected speed (blue symbol).', S06 + ' FMGES Preparation, Climb, Cruise, Descent Speed Preselection'),
    ('SPD LIM', 'SPD LIM is defaulted to 250 kt below 10 000 ft in the managed speed profile. This may either be cleared, or modified, on the VERT REV page at the origin (or a climb waypoint).', S06 + ' FMGES Preparation, Climb, Cruise, Descent Speed Preselection')]),
  ('PROG', 'BRG / DIST TO: return rwy, destination or ETP; RNP set or check for an RNP AR departure',
   '<b>PROG</b> (PF): BRG / DIST TO as appropriate: the runway ident for an immediate return, the destination, or an ETP. RNP: for an RNP AR departure, check or insert the RNP.',
   [('PROG: BRG / DIST TO', 'Enter the BRG / DIST TO fix as appropriate. Consideration may be given to the following: a. Ident of runway in case of immediate return b. Destination c. ETP', S06 + ' FMGES Preparation, PROG page'),
    ('PROG: RNP', 'For RNP AR departure, check or insert the RNP.', S06 + ' FMGES Preparation, RNP Insertion (PROG page)')]),
 ]),
 ('6  -  CROSSCHECK (PM)', '6 - Crosscheck (PM, SOP-06)', [
  ('FMS PREPARATION  (PM)', 'waypoints and constraints, CRZ ALT, track miles, dest fuel, THR RED/ACC/EO, TRANS ALT, SEC',
   '<b>FMS PREPARATION CROSSCHECK</b> (PM): after the PF prepares the FMS the PM checks everything entered: departure waypoints with constraints; flight plan waypoints vs the computerized flight plan; initial cruise altitude; total track miles; fuel remaining at destination; performance data including THR RED/ACCEL/EO ACCEL changes; TRANS ALT on the ACTIVE/PERF page; SEC flight plan setup. The PM must hold the same mental picture of the departure as the PF and asks if anything is unclear (FCTM PR-NP-SOP-60).',
   [('FMS PREPARATION crosscheck (PM)', 'After the PF prepares the FMS, the PM checks all the data entered in the FMS. This check includes a crosscheck between: ‐ Waypoints of the expected departure route that include constraints ‐ Waypoints of the flight plan and the computerized flight plan ‐ Initial cruise altitude and the computerized flight plan ‐ Total track miles and the computerized flight plan ‐ Fuel remaining at destination and the computerized flight plan ‐ Performance data including modifications of the THR RED/ACCEL/EO ACCEL settings, if applicable ‐ TRANS ALT in the ACTIVE/PERF page ‐ Setup of the SEC flight plan.', S06 + ' Check of FMGES Preparation'),
    ('PM mental image', 'The PM should have the same mental image of the intended departure procedure, trajectory, and constraints as the PF. The PM should check with the PF if anything is not clear.', S06 + ' Check of FMGES Preparation')]),
 ]),
]

BOOKENDS_CARD = [
 '<b>ATIS</b> (CM2, CM3): obtain before the pre-initialization. Runway in use, altimeter setting and weather data feed the system initialization and the preliminary takeoff performance. ACARS INIT (PF): departure, destination, flight number, date. Preliminary takeoff perf (PF): from the AeroData TPR or TLR review RWY, intersection, flaps, anti-ice, packs, FLEX or TOGA.',
 '<b>Tasksharing</b>: the PF prepares the overhead panel, center instrument panel and pedestal while the PM does the walkaround; when both are seated and the PM has checked the FMS, both continue the cockpit preparation. Pre-initialization items in SOP-04 are CM1, the FMGES preparation in SOP-06 is PF, the crosscheck is PM.',
 '<b>IRS ALIGN</b> (PM): POSITION MONITOR, IRS in NAV, each IRS within 5 NM of the FMS position; ND in ROSE-NAV or ARC, position consistent with the airport, SID and navaids. <b>FUEL ON BOARD</b> (PF, PM): ECAM FOB matches the block fuel, balanced, CG in limits. <b>ATC clearance</b> (PM): VHF, ACARS PDC or CPDLC DCL.',
 '<b>DEPARTURE LEGS VERIFICATION</b> (BOTH): after the FMGS preparation and before the Departure Briefing; repeat after any routing change. PF reads from the glass: PLAN mode, CSTR on, F-PLN, each departure and enroute waypoint and constraint aloud, UP arrow after each; non-defined and user-defined waypoints by LAT REV full lat/long. PM verifies against the flight plan, Jeppesen charts and ATC clearance and resolves any discrepancy. Last step: total F-PLN DIST and destination EFOB agree with the release.',
 '<b>Gates</b>: aircraft acceptance complete by the end of the cockpit preparation; FMS pre-initialization done before the FMGES preparation continues; INIT B is not available after engine start; Departure Legs Verification before the Departure Briefing, then the COCKPIT PREPARATION C/L.',
]
BOOKENDS_DOCS = [
 ('ATIS (CM2)', 'The CM2 (CM3) should attain the ATIS. Obtain data needed for initializing the system, preparing the cockpit and for preliminary takeoff performance computation. The airfield data should include: RUNWAY IN USE, ALTIMETER SETTING, and WEATHER DATA.', S04 + ' Preliminary Performance Determination'),
 ('ACARS initialize (PF)', 'Initialize and check the ACARS. On the ACARS INIT page input/check the departure airport, destination airport, flight number and date.', S04 + ' Preliminary Performance Determination'),
 ('Preliminary takeoff perf data (PF)', 'From the AeroData TPR (or TLR) the PF reviews the following: ‐ RWY to be used ‐ RWY intersection ‐ Flaps setting ‐ Use of anti-ice ‐ Use of packs ‐ Takeoff thrust setting options (FLEX, TOGA).', S04 + ' Preliminary Performance Determination'),
 ('Cockpit preparation tasksharing', 'The PF prepares the overhead panel, the center instrument panel and the pedestal while the PM performs the external walkaround. When both flight crewmembers are seated and the PM checked the FMS, both flight crewmembers continue the cockpit preparation.', S06 + ' General'),
 ('FMS PREPARE gate', 'If not already completed in the Preliminary Cockpit Preparation, accomplish the FMS Pre-Initialization (Refer to PRO-NOR-SOP-04 FMGS PRE-INITIALIZATION) before continuing with the FMS preparation.', S06 + ' FMGES Preparation, FMS Prepare'),
 ('IRS ALIGN check (PM)', 'On the POSITION MONITOR page, check that the IRS are in NAV mode, and check that the distance between each IRS and the FMS position is lower than 5 NM. Select ND in ROSE-NAV or ARC mode, and confirm that the aircraft position is consistent with the position of the airport, the SID and the surrounding NAVAIDs.', S06 + ' ADIRS'),
 ('FUEL ON BOARD check', '‐ Check that ECAM FOB corresponds to the block fuel of the computerized flight plan ‐ On FUEL SD page, check that the fuel is correctly balanced and CG is within operational limits.', S06 + ' Fuel On Board'),
 ('ATC clearance (PM)', 'Obtain ATC clearance via VHF, ACARS (PDC) or via CPDLC (DCL), Refer to PRO-SUP-46 Departure Clearance via CPDLC.', S06 + ' ATC Clearance'),
 ('Departure Legs Verification: when', 'will be accomplished after the FMGS preparation and before accomplishing the Departure Briefing. The Departure Legs Verification should be repeated if the routing is changed, for example, after ATC issues a change of Runway/SID during taxi out. The Departure Legs Verification includes a check of each waypoint and constraint on the Departure (SID) and Enroute segment.', S06 + ' Departure Legs Verification'),
 ('Departure Legs Verification: roles', 'The PF reads from the “glass” (ND), and the PM verifies against the “paper” (Flight Plan/ Navigation Log, Jeppesen Charts and ATC Clearance).', S06 + ' Departure Legs Verification'),
 ('Departure Legs Verification: PF reads from ND', '‐ Select PLAN mode on EFIS Control Panel. ‐ Select CSTR pb ON, on EFIS Control Panel, to display speed/altitude constraints. ‐ Select F-PLN on MCDU. ‐ Read aloud each Departure and Enroute waypoint and corresponding speed/altitude constraint (if any) off the ND. ‐ After each waypoint, select the ‘UP’ arrow key on the MCDU to display the next waypoint.', S06 + ' Departure Legs Verification'),
 ('Departure Legs Verification: non-defined waypoints', '• Select the left LSK next to the non-defined waypoint to display the LAT REV page. • Read aloud the full Latitude and Longitude located at the top of the LAT REV page. • Select the left LSK next to < RETURN.', S06 + ' Departure Legs Verification'),
 ('Departure Legs Verification: PM', '‐ Follow along with the PF by checking each waypoint and constraint against the Jeppesen SID, Dispatch release, and current ATC clearance. ‐ Resolve any discrepancy.', S06 + ' Departure Legs Verification'),
 ('Departure Legs Verification: F-PLN DIST and EFOB', 'The final step is to confirm that the total F-PLN distance (DIST) and the Estimated Fuel On Board (EFOB) at the destination agree with the Dispatch Release. Resolve any large discrepancies.', S06 + ' Departure Legs Verification'),
 ('Aircraft acceptance gate', 'The aircraft acceptance can be performed later, but must be completed at the end of the Cockpit Preparation.', S04 + ' Aircraft Acceptance'),
]

# ---------------------------------------------------------------- transform
t = open(SRC, encoding='utf-8').read()
def esc(s): return html.escape(s, quote=False)
def must(a): assert a in t, f'anchor missing in clone: {a[:70]}'

# 1. header .src line (revision from manuals.json)
old_src = re.search(r'<span class="src">[^<]*</span>', t).group(0)
t = t.replace(old_src, f'<span class="src">FCOM {FR} {REF} &middot; page flow</span>')

# 2. SVG: same geometry, same attributes, same fills; only the text nodes change.
svg_m = re.search(r'<svg [^>]*viewBox="0 0 680 1156"[^>]*>.*?</svg>', t, re.S); assert svg_m
svg = svg_m.group(0)
open_tag = svg[:svg.index('>')+1]
title_tag = re.search(r'<title id="t">[^<]*</title>', svg).group(0)
desc_tag = re.search(r'<desc id="d">[^<]*</desc>', svg).group(0)
banner = re.search(r'<rect x="40" y="18".*?</text><text[^>]*>[^<]*</text>', svg, re.S).group(0)   # banner rects + 2 texts
hdr_fills = re.findall(r'<rect x="40" y="\d+" width="600" height="26" rx="5" fill="(#[0-9A-Fa-f]{6})"/>', svg)
hdr_text_fills = re.findall(r'height="26" rx="5" fill="#[0-9A-Fa-f]{6}"/><text[^>]*fill="(#[0-9A-Fa-f]{6})">', svg)
assert len(hdr_fills) == 6 == len(hdr_text_fills), 'six numbered groups expected'
bk = re.search(r'<rect x="40" y="76" width="600" height="50" rx="10" fill="(#[0-9A-Fa-f]{6})" stroke="(#[0-9A-Fa-f]{6})" stroke-width="1"/><rect x="40" y="76" width="7" height="50" rx="0" fill="(#[0-9A-Fa-f]{6})"/>', svg)
BK_FILL, BK_STROKE, BK_BAR = bk.groups()
n_nodes = sum(len(g[2]) for g in GROUPS); assert n_nodes == 14, f'{n_nodes} nodes; the 1156 viewBox holds 14'

def node_svg(y, fill, label, sub):
    return (f'<rect x="40" y="{y}" width="600" height="44" rx="6" fill="#ffffff" stroke="#d7d7d7" stroke-width="1"/>'
            f'<rect x="40" y="{y}" width="7" height="44" rx="0" fill="{fill}"/>'
            f'<text x="60" y="{y+19}" font-family="sans-serif" font-size="13" font-weight="700" fill="#1a1a1a">{esc(label)}</text>'
            f'<text x="60" y="{y+36}" font-family="sans-serif" font-size="11" fill="#555">{esc(sub)}</text>')
def bookend_svg(y, label, sub):
    return (f'<rect x="40" y="{y}" width="600" height="50" rx="10" fill="{BK_FILL}" stroke="{BK_STROKE}" stroke-width="1"/>'
            f'<rect x="40" y="{y}" width="7" height="50" rx="0" fill="{BK_BAR}"/>'
            f'<text x="60" y="{y+21}" font-family="sans-serif" font-size="13" font-weight="700" fill="#333">{esc(label)}</text>'
            f'<text x="60" y="{y+39}" font-family="sans-serif" font-size="11" fill="#555">{esc(sub)}</text>')

banner = re.sub(r'(<text x="54" y="40"[^>]*>)[^<]*(</text>)', lambda m: m.group(1)+'MCDU Preflight (PF)'+m.group(2), banner)
banner = re.sub(r'(<text x="54" y="57"[^>]*>)[^<]*(</text>)', lambda m: m.group(1)+esc(f'FCOM {FR} {REF}')+m.group(2), banner)
parts = [open_tag, '<title id="t">MCDU Preflight page flow</title>',
         '<desc id="d">MCDU page flow for the pilot flying, six numbered groups bookended by the ATIS and the Departure Legs Verification.</desc>',
         banner, bookend_svg(76, *TOP)]
y = 138
for gi, (glabel, _, nodes) in enumerate(GROUPS):
    parts.append(f'<rect x="40" y="{y}" width="600" height="26" rx="5" fill="{hdr_fills[gi]}"/>'
                 f'<text x="52" y="{y+18}" font-family="sans-serif" font-size="12.5" font-weight="700" fill="{hdr_text_fills[gi]}">{esc(glabel)}</text>')
    y += 32
    for (label, sub, _, _) in nodes:
        parts.append(node_svg(y, hdr_fills[gi], label, sub)); y += 52
    y += 6   # 44 + 14 to the next header = node y + 58
assert y == 1094, y
parts.append(bookend_svg(1094, *BOTTOM)); parts.append('</svg>')
t = t.replace(svg, ''.join(parts))

# 3. cards
card_m = re.search(r'(<div class="card">\n    \n)(.*?)(\n  </div>\n</div>\n<footer>)', t, re.S); assert card_m
cards = []
for (_, h2, nodes) in GROUPS:
    cards.append(f'<h2>{esc(h2)}</h2>\n<ul>\n' + '\n'.join(f'<li>{li}</li>' for (_, _, li, _) in nodes) + '\n</ul>')
cards.append('<h2>Bookends and gates</h2>\n<ul>\n' + '\n'.join(f'<li>{li}</li>' for li in BOOKENDS_CARD) + '\n</ul>')
t = t[:card_m.start(2)] + '\n'.join(cards) + '\n' + t[card_m.end(2):]

# 4. footer text (Ver token left for stamp_versions.py)
fm = re.search(r'<footer>(.*?)(&middot; Ver [0-9.]+)</footer>', t); assert fm
t = t[:fm.start(1)] + f'FCOM {FR} {REF} &middot; PF prepares, PM crosschecks ' + t[fm.start(2):]
assert '—' not in t, 'em dash'
open('mcdu_preflight.html', 'w', encoding='utf-8').write(t)

# 5. corpus docs
docs = []
for (_, _, nodes) in GROUPS:
    for (_, _, _, ds) in nodes:
        docs += [{'t': a, 'x': b, 'r': c} for (a, b, c) in ds]
docs += [{'t': a, 'x': b, 'r': c} for (a, b, c) in BOOKENDS_DOCS]
os.makedirs('data', exist_ok=True)
json.dump(docs, open('data/mcdu.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(f'mcdu_preflight.html written from {SRC}; data/mcdu.json {len(docs)} docs')
