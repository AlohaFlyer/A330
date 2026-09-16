# A330 FCTM delta: R5 (27 MAR 26) to R6 (14 SEP 26)

Method: both extracts (`src/_old/A330_FCTM_R5.md`, `src/A330_FCTM_R6.md`) cut into pages at the
`HAL A330 FLEET <ident> P n/m` footers, lines whitespace-normalized, `difflib.SequenceMatcher` per ident. Script:
`scratchpad/sweep/fctm_diff.py`, raw output `scratchpad/sweep/fctm_rawdiff.txt`. Tags: **PAX** = A330 PAX-relevant,
**FRTR** = freighter-only, **ED** = editorial (rename, punctuation, ident date, page re-flow).

R6 is based on the Airbus FCTM revision dated 26 MAY 26 (Transmittal Letter). The airline name is now "The Company"
throughout (Hawaiian Airlines / Alaska Airlines references replaced). A new tail, N7019K (MSN 1359, 330-343), joins the
Aircraft Allocation Table and the Rockwell Collins radar / NAV effectivity lists. **FRTR** for the tail.

## 1. The manual's own revision record

The Summary of Highlights pages (PLP-SOH, GI-PLP-SOH, AOP-PLP-SOH, AS-PLP-SOH, PR-PLP-SOH) are listed in the Filing
Instructions but their body text is not in either extract, so the only revision record available is the List of
Effective Sections (PLP-LESS) evolution codes. Sections marked R (revised) or E (effectivity) at 14 SEP 26:

GI (General Information), AOP-10-30-20 (FBW Utilization Principles), AOP-20 (Tasksharing Rules and Communication),
AOP-30-30 (Handling of ECAM/QRH/OEB), AOP-30-50 (Spurious Caution), AS-FG-10-2 (Autothrust), AS-FM-10 (Use of FMS),
AS-TCAS, AS-WXR, PR-NP-SOP-50 (Exterior Walkaround), PR-NP-SOP-60 (Cockpit Preparation), PR-NP-SOP-70 E (Before
Pushback or Start), PR-NP-SOP-120 (Takeoff), PR-NP-SOP-140 (Climb), PR-NP-SOP-150 (Cruise), PR-NP-SOP-160 (Descent
Preparation), PR-NP-SOP-190-GUI (Guidance Management), PR-NP-CL (Normal Checklists), PR-NP-SP-10-10-1 (Cold Weather
Operations and Icing Conditions), PR-NP-SP-20 (Green Operating Procedures), PR-AEP-ELEC, PR-AEP-ENG, PR-AEP-F_CTL,
PR-AEP-LG, PR-AEP-MISC, PR-AEP-NAV, PR-AEP-SMOKE E. Also re-dated 14 SEP 26 without an R code and with no body
change in the diff: PR-NP-GEN, PR-NP-SOP-170 (Descent), PR-NP-SP-10-10-2 (Windshear), PR-NP-SP-30 (RF Legs).

The List of Modifications adds 34-3338 04 (26 MAY 26, RDR-4000 STEP2 hazard features on N5827K, N5843K, N5869K,
N5879K, N5881K, N5897K) and updates 31-3314 02 (T11 FWC standard, 20 JAN 26, most of the fleet). **ED / FRTR**

## 2. Body changes the diff found, by section

### AOP-20 Tasksharing Rules and Communication **PAX**
FMS entries via MCDU, note on low operational risk: the list of tasks the PF may hand control to the PM for now
starts with `the preparation of the Terrain Escape Procedures`, then departure/arrival and approach preparation and
threat-based briefings. Verbatim R6: `During low operational risk periods, transferring control to the PM so the PF
may accomplish the preparation of the Terrain Escape Procedures, departure/arrival and approach preparation, and
threat-based briefings, is at flight crew discretion.` Briefing technique: `The Company uses a threat based briefing
model.` **ED** for the name.

### AOP-30-30 Handling of ECAM/QRH/OEB **PAX**
New sentence under Handling of QRH, General: `The notes associated to the actions provide the flight crew with
additional technical information. The flight crew must read the notes before they perform the action.`

### AS-FG-10-2 Autothrust **ED**
`thrust will increase to MAX CLB` (was `MAX CL`).

### AS-FM-10 Use of FMS **PAX**
New DU `UPLINKED F-PLN CHECK` (AS-FM-10-00027724.0001001 / 14 SEP 26): before activating a SEC F-PLN created from an
uplinked F-PLN (AOC or connected EFB) the crew must verify all modified flight plan data, in particular waypoints
not in the navigation database: Lat/Long, PBD, PD and PB/PB waypoints.

### AS-TCAS, AS-WXR **ED / FRTR**
Criteria and applicability strings only (T11 FWC criteria; radar effectivity now `Criteria: LR`, N7019K added).

### PR-NP-SOP-50 Exterior Walkaround **ED**
`The Company employees will refuse to transport`, `Pat-down searches by company crewmembers`, `The Company will use
only disposable batteries` (name changes only).

### PR-NP-SOP-60 Cockpit Preparation **PAX**
The `FMGES CROSSCHECK` paragraph (`When the PF finishes the FMGES preparation, the PM must check the PF's entries ...
in the same order as the FMGES preparation ... the PM should achieve the same mental image as the PF`) was removed
from this DU. The cross-check survives only in the departure briefing DU of the same section (`The FMS cross-check is
performed by checking each FMS page in the same order as the FMS ...`, PR-NP-SOP-60 P 7/8 in R6). No bank quoted the
removed paragraph.

### PR-NP-SOP-120 Takeoff **ED**
`The Company uses 1 500 ft AFE as thrust reduction altitude for NADP 1` (name only).

### PR-NP-SOP-140 Climb **ED**
`ZZZ/-10 waypoint`, `10 NM` (was `ZZZ,-10`, `10 N.m`), `MCDU F-PLN page` (was `FPLN`).

### PR-NP-SOP-150 Cruise **PAX**
New DU `DECOMPRESSION PROCEDURE` (PR-NP-SOP-150-C0000346.9001001 / 14 SEP 26): 14 CFR 121.329 oxygen rules; over
mountainous terrain the aircraft must descend to an altitude that keeps the 2 000 ft obstacle clearance margin;
aircraft crossing terrain above 8 000 ft must carry oxygen to hold terrain clearance until able to descend to
10 000 ft; the Decompression Procedures are in the FOM (Decompression procedures) and FCTM PR-AEP-MISC (EMER DESCENT in
Mountainous Terrain); `When overflying mountainous regions, the flight crew should prepare and monitor the appropriate
decompression procedure (Refer to FCOM/PRO-NOR-SOP-15 Cruise - ECAM).` The PR TOC gains `Decompression Procedure`
under Cruise (E) and shifts Altitude Considerations, Step Climb and Fuel Temperature to F, G, H. `"ALT CRZ "` spacing
fix **ED**.

### PR-NP-SOP-160 Descent Preparation **ED**
`landing performance is not allowed per company policy` (name only); the 15 % factored landing distance rule is
unchanged.

### PR-NP-SOP-190-GUI Guidance Management, low visibility **PAX** (largest procedural change)
DU renamed `APPROACH USING LOC G/S - LOW VISIBILITY OPERATIONS` (was `... FOR CATII / CATIII`). Changes:
- `For CATII approaches, autoland is required.` R5 said autoland recommended and, if a manual landing was preferred,
  `the PF will take-over at 80 ft at the latest`. The manual-landing option is gone from the FCTM.
- `For CAT III operations, auto-brakes are required.` (appended to the autobrake sentence).
- LVP wording: `that LVP procedures are in force (i.e. Critical area protected).`
- Autoland maximum altitude now carries its FCOM pointer (`Refer to FCOM/LIM-AFS-20 Automatic Landing - Glide
  Slope/Airport Elevation`).
- Capability paragraph rewritten around the QRH pointer `Refer to QRH/OPS Required Equipment for CAT2 and CAT3`;
  the FMA capability appears `when the flight crew presses the APPR pb`.
- Conditions table re-set: CAT I `Manual or AP/FD, with or without A/THR`, CAT II `AP/FD and Autoland, with or
  without A/THR`, CAT III `AP/FD + A/THR and Autoland`; minima `DA or DH (Baro ref) Visibility`, `DH with RA RVR`,
  `RVR`; Autoland `Possible with precautions`, `Mandatory`. The `(HAL policy)` tag on CAT II autoland is gone because
  the requirement is now in the text.
- Go-around strategy and approach briefing paragraphs reworded (same content: failures above 1 000 ft RA handled
  before 1 000 ft RA or go around; brief flight crew qualification, tasksharing, callouts, go-around strategy).
No portal bank quotes the CAT II manual-landing sentence; the FCOM LIM-AFS-20 80 ft AP-disconnect limitation quoted
in phase_flows (limits) is unchanged FCOM text.

### PR-NP-CL Normal Checklists **ED**
Criteria strings; the SECURING THE AIRCRAFT reference row now prints `Refer to FCOM/FCOM/PRO-NOR-SUP-SEC Securing the
Aircraft - General` (doubled prefix, a typo in R6). flows_trainer quotes it verbatim.

### PR-NP-SP-10-10-1 Cold Weather Operations and Icing Conditions **PAX**
Taxi-out factors: `At speeds below 20 kt, the antiskid is deactivated.` (R5: `below 10 kt`). No bank quotes this line
(the phase_flows antiskid mentions are FCOM landing and LOSS OF BRAKING text).

### PR-NP-SP-20 Green Operating Procedures **ED**
`Company is responsible for the decision of what costs/parameters to reduce`.

### PR-AEP-ENG, PR-AEP-F_CTL, PR-AEP-ELEC **ED**
`A/SKID` (was `A-SKID`), `ECAM F/CTL page` (was `FCTL`), criteria strings.

### PR-AEP-LG L/G **PAX**
Loss of nosewheel steering: new sentence `During rollout, the directional control can be achieved via rudder pedals
and differential braking, if necessary.` then `During taxi, the flight crew can steer the aircraft with differential
braking technique ...` (was `If the NWS is lost for taxiing ...`). Towing advice unchanged.

### PR-AEP-MISC EMER DESCENT in Mountainous Terrain **PAX** (rewritten)
- The `Western US Depress Strategy` quick reference, its three components, Oxygen Time Requirements Table and
  Recommended Diversion Airports paragraphs are deleted.
- Replaced by: `The Company may develop decompression strategies for specific mountainous regions; these are
  identified by polygons, which are displayed on the FD Pro IFR en-route view. In the absence of polygons over
  mountainous terrain, the general strategy will apply.` and two new DUs: `EXECUTING THE DECOMPRESSION POLYGON
  PROCEDURE` (1. apply the EMER DESCENT memory items, QRH procedure or CAB PR EXCESS CAB ALT ECAM; 2. full description
  in the FOM) and `EXECUTING THE GENERAL STRATEGY WHEN NO POLYGONS ARE IDENTIFIED` (the former four-step general
  strategy; step 3 is now `the crew may set an altitude target of (e.g., 18 000 ft.)`, was `shall set ... 18 000 ft`).
- Oxygen: passenger generators `designed to sustain life until descent to 10 000 ft can be` (was 14 000 ft); the
  minute-by-minute `AIRBUS OXYGEN SYSTEM ENDURANCE PROFILE` is deleted; the 121.329 rule (up to 14 000 ft cabin
  altitude for 30 min without passenger oxygen, then 10 000 ft, masks off level at 10 000 ft) is kept as prose.
- `On the A330 Freighter, the courier module and lavatories are supplied by a plumbed system ... fed by an oxygen
  tank` **FRTR**.
- `IF USING THE FMS FOR DIVERSION PREPARATION / EXECUTION` (was `USE THE FMS ...`); the crew `may choose to enter` the
  diversion airport as SEC F-PLN destination (was `should enter`).
The phase_flows `depress` phase is grounded on FOM 11.2.9 Decompression Polygon Procedures and needed no change.

### PR-AEP-MISC EMER EVAC **PAX / ED**
`the captain calls "I HAVE CONTROL"` (was `"I HAVE CONTROLS"`); `defer or cancel the passengers' evacuation` (was
`courier area occupants'`, a freighter phrase); `Notifies the cabin crew or the additional aircraft occupants`;
`builds up the decision` (was `his/her decision`).

### PR-AEP-MISC Rejected Takeoff **PAX** (wording, same rule)
`the ECAM inhibits the alerts that are not essential from 80 kt to 1 500 ft ... any alert received during this period
must be considered as significant`; `The Captain should seriously consider discontinuing the takeoff, if any ECAM
alert is activated.`; above 100 kt list item 1 `Fire alert, or severe damage`. (R5: warning/caution, Fire warning.)
phase_flows RTO quotes and step text refreshed to R6.

### GI Abbreviations **ED**
Several entries dropped or re-set (A/BRK, A/P, AA, AAR, AB, ABN, ABV, ACARS, ACMS, ACN, ACP, ACQ, ADIRU, ADM, ADS-B,
ADV, AEVC ...) and `ACC Active Clearance Control` added. Extract-level list churn, no procedure content.

## 3. What an A330 FO must relearn from R6

1. CAT II is an autoland. The FCTM no longer offers a manual landing with AP off by 80 ft on a CAT II approach, and CAT
   III requires autobrake.
2. Decompression over terrain is now polygon-based (FD Pro IFR en-route view, FOM procedures); the Western US Depress
   Strategy quick reference is gone. General strategy applies only where no polygon exists. Prepare and monitor the
   applicable procedure when overflying mountainous regions (new Cruise DU).
3. RTO decision language is `ECAM alert` and `Fire alert` (the FWC T11 vocabulary); the rule set is unchanged.
4. Read the ECAM/QRH notes before performing the action.
5. Antiskid deactivates below 20 kt (cold weather taxi factors), not 10 kt.
6. Uplinked flight plans: verify every modified waypoint, especially Lat/Long, PBD, PD, PB/PB, before activating the SEC.
7. During low-risk periods the PF may hand control to the PM to prepare Terrain Escape Procedures as well as
   departure/arrival/approach and briefings.
8. Nosewheel steering lost: rudder and differential braking during rollout, differential braking or a tow for taxi.
