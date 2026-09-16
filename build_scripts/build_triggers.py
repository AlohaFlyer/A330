#!/usr/bin/env python3
"""Build data/triggers.json (A330 Triggers bank) for triggers.html.

Deterministic. Hand-authored records below; where a record names a flows.json
phase, the flow step list is filled from the verified steps in data/flows.json.
Every `src` is a verbatim (whitespace-normalized) substring of the named
extract; run verify_triggers.py after building.

Record shape consumed by the frozen engine:
  {s, who, q, a, tech?, ref, src, flow?:{n, i:[str]}}
`flow.i` items are strings (the engine renders each with <li>${x}</li>, same
as the B787 bank, which carries an inline <span class='role'> tag).
Extra bookkeeping fields the engine ignores: fleet, kind, ext, ident.
  fleet: "pax"   kind: "manual" | "sop" | "technique"
  ext:   which source extract `src` is quoted from (see EXTRACTS)
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.dirname(HERE)
SRC = os.path.normpath(os.path.join(WORK, '..', 'src'))
FLOWS = os.path.join(WORK, 'data', 'flows.json')
OUT = os.path.join(WORK, 'data', 'triggers.json')

EXTRACTS = {
    'FCOM': 'A330P_FCOM_R17_PRO-NOR.md',
    'FCTM': 'A330_FCTM_R6.md',
    'PRC': 'A330_PRC_2026-08-31.md',
    'QuickRef': 'QuickRef.md',
}

flows = json.load(open(FLOWS, encoding='utf-8'))
PHASES = {p['id']: p for p in flows['phases']}


def clean_line(line):
    """'ENG START selector......NORM' -> 'ENG START selector NORM'"""
    line = re.sub(r'^\*\s*', '', line)
    line = re.sub(r'\.{3,}', ' ', line)
    return re.sub(r'\s+', ' ', line).strip()


def flow_from_phase(pid, title=None):
    """Build the engine's flow object from a verified flows.json phase."""
    p = PHASES[pid]
    items = []
    for s in p['steps']:
        f = s.get('fcom') or {}
        if f.get('status') == 'UNVERIFIED':
            continue
        text = s['text']
        line = f.get('line')
        label = text if not line else f"{text}: {clean_line(line)}"
        role = s['who']
        hit = next((it for it in items if it[0] == label), None)
        if hit:
            # same step listed in the PF and PM columns: one line, merged roles
            if role not in hit[1]:
                hit[1].append(role)
            continue
        items.append([label, [role]])
    n = title or f"{p['title']} ({len(items)} items)"
    return {
        'n': n,
        'i': [f"{lab} <span class='role'>{' · '.join(roles)}</span>" for lab, roles in items],
    }


def flow_manual(title, items):
    """Hand-authored flow: items are (text, role)."""
    return {'n': title, 'i': [f"{t} <span class='role'>{r}</span>" for t, r in items]}


R = []


def wbr(text):
    """FCOM procedure lines carry dotted leaders up to 100 dots long, an unbreakable
    token that overflows the Source panel at phone width. Insert <wbr> (a
    zero-width break opportunity, no visible text) every 12 dots inside runs of
    20 or more. verify_triggers.py strips <wbr> before the substring check, so
    the displayed text stays verbatim."""
    return re.sub(r'\.{20,}', lambda m: '<wbr>'.join(m.group(0)[i:i + 12] for i in range(0, len(m.group(0)), 12)), text)


def rec(s, q, a, ref, src, ext, kind, who=None, tech=None, flow=None, ident=None):
    d = {'s': s, 'q': q, 'a': a}
    if who:
        d['who'] = who
    if tech:
        d['tech'] = tech
    d['ref'] = ref
    d['src'] = wbr(src)
    if flow:
        d['flow'] = flow
    d['fleet'] = 'pax'
    d['kind'] = kind
    d['ext'] = ext
    if ident:
        d['ident'] = ident
    R.append(d)


# ---------------------------------------------------------------- PHASE TRIGGERS
PT = 'Phase Triggers'

rec(PT,
    q='Departure Briefing complete. What does it trigger?',
    a='Cockpit Preparation Checklist',
    who='PF requests the checklist. PM reads the challenge, PF responds. BARO REF and OXY MASKS are BOTH items: PF then PM.',
    ref='FCTM PR-NP-CL (Cockpit Preparation)', ident='PR-NP-CL-00024935.0001001',
    src='Checklist trigger: Departure briefing completed.', ext='FCTM', kind='sop',
    flow=flow_from_phase('cockpit-prep'))

rec(PT,
    q='Push/start clearance received. What does it trigger?',
    a='Before Start flow, then Before Start Checklist',
    who='PM obtains the pushback/start clearance and ground crew clearance. PF: beacon, thrust levers, park brake. Checklist: PF requests, PM reads.',
    tech='QuickRef technique: Flow Trigger is Push/Start Clearance Received; C/L Trigger is Before Start flow complete.',
    ref='FCTM PR-NP-CL (Before Start)', ident='PR-NP-CL-00024936.0001001',
    src='Checklist trigger: ‐ Pushback clearance or start clearance received, and ‐ Before Start flow pattern completed.',
    ext='FCTM', kind='sop',
    flow=flow_from_phase('before-start'))


rec(PT,
    q='Engines started. What event starts the After Start flow?',
    a='PF sets the ENG START selector to NORM',
    who='PF sets the selector and does the overhead (APU bleed, anti-ice, APU master). PM: ground spoilers, rudder trim, flaps, pitch trim.',
    ref='FCOM PRO-NOR-SOP-09-A', ident='PRO-NOR-SOP-09-A-00019960.0001001',
    src='The PF sets the ENG START selector to NORM to permit normal pack operation. At this time, the After Start flow pattern begins.',
    ext='FCOM', kind='manual',
    flow=flow_from_phase('after-start'))

rec(PT,
    q='What triggers the After Start Checklist?',
    a='Hand signal (salute) from the ground personnel',
    who='PF requests, PM reads. First item is SALUTE, PF responds RECEIVED.',
    tech='QuickRef technique: C/L Trigger is Salute received, then TAXI light.',
    ref='FCTM PR-NP-CL (After Start)', ident='PR-NP-CL-00024937.0001001',
    src='Checklist trigger: On hand signal (salute) from the ground personnel.', ext='FCTM', kind='sop')

rec(PT,
    q='During taxi: what has to happen before the Taxi flow starts?',
    a='Brake check, flight control check, ATC clearance confirmed, then AFS/Flight Instruments checked. That check is the flow trigger.',
    who='PM confirms the ATC clearance and checks the FCU altitude and FDs. PFD/ND check is PF-PM.',
    tech='QuickRef technique: Flow Trigger is AFS/Flight Instruments checked.',
    ref='FCOM PRO-NOR-SOP-10-A', ident='PRO-NOR-SOP-10-A-00011949.0001001',
    src='Review the ATC clearance before checking the AFS/Flight Instruments', ext='FCOM', kind='manual',
    flow=flow_from_phase('taxi'))

rec(PT,
    q='What triggers the Taxi Checklist?',
    a='T.O CONFIG pb pressed and Takeoff Advisory PA complete',
    who='PM presses T.O CONFIG, checks T.O memo no blue and makes the PA. Then PF requests the checklist, PM reads.',
    ref='FCTM PR-NP-CL (Taxi)', ident='PR-NP-CL-00024938.0005001',
    src='Checklist trigger: ‐ T.O. CONFIG pb pressed, and ‐ Takeoff Advisory PA complete (if applicable).',
    ext='FCTM', kind='sop')

rec(PT,
    q='Takeoff PA: who, how far ahead, and the words?',
    a='PM, no less than two minutes prior to takeoff: [FLIGHT ATTENDANTS SHOULD NOW] BE SEATED FOR TAKEOFF',
    who='PM (the FO when the CA flies).',
    ref='FCOM PRO-NOR-SOP-10-A', ident='PRO-NOR-SOP-10-A-00011956.0001001',
    src='Advise the cabin that takeoff is imminent. On Pax aircraft, The PM will make the Takeoff PA no less than two minutes prior to takeoff stating "[FLIGHT ATTENDANTS SHOULD NOW] BE SEATED FOR TAKEOFF".',
    ext='FCOM', kind='manual')

rec(PT,
    q='Line-up clearance received. What does it trigger?',
    a='Line-Up flow, then Line-Up Checklist',
    who='PM obtains the clearance and sets TCAS and packs. TAKEOFF RUNWAY confirm and approach path clear are both pilots. Strobes ON is PF.',
    ref='FCTM PR-NP-CL (Line-Up)', ident='PR-NP-CL-00024939.0001001',
    src='Checklist trigger: ‐ Line-up clearance received ‐ Line-Up flow pattern completed.', ext='FCTM', kind='sop',
    flow=flow_from_phase('line-up'))

rec(PT,
    q='Takeoff clearance received. The two light switches?',
    a='NOSE sw T.O and LAND sw ON (PF)',
    who='PM obtains the takeoff clearance. PF sets the lights (PF can request the PM to set them).',
    ref='FCOM PRO-NOR-SOP-12-A', ident='PRO-NOR-SOP-12-A-00021963.0001001',
    src='NOSE sw................................................................................................................. T.O PF LAND sw...................................................................................................................ON PF',
    ext='FCOM', kind='manual')

rec(PT,
    q='After takeoff: what triggers the Acceleration flow, and is there a checklist behind it?',
    a='Selection of flaps 0 (at S speed). No checklist: the A330 has no After Takeoff checklist.',
    who='PF orders FLAPS 1 at F speed and FLAPS 0 at S speed, PM selects. PM does the four flow items.',
    tech='QuickRef technique: Flow Trigger is Selection of flaps 0.',
    ref='FCOM PRO-NOR-SOP-12-A', ident='PRO-NOR-SOP-12-A-00012091.0001001',
    src='ABOVE ACCELERATION ALTITUDE (OR ONCE IN CLIMB PHASE) L2 The following procedure ensures that the aircraft is correctly accelerating toward climb speed.',
    ext='FCOM', kind='manual',
    flow=flow_from_phase('acceleration'))

rec(PT,
    q='Climbing through 10,000 ft MSL. Who selects which EFIS option?',
    a='PF selects CSTR, PM selects ARPT',
    who='PM does the rest: LAND OFF, NO SMOKING cycle (ON, wait 3 s, AUTO), ECAM memo review, NAVAIDS clear, SEC F-PLN, OPT/REC MAX FL check.',
    ref='FCOM PRO-NOR-SOP-14-A', ident='PRO-NOR-SOP-14-A-00019949.0001001',
    src='EFIS Option: The PF will select CSTR The PM will select ARPT', ext='FCOM', kind='manual',
    flow=flow_from_phase('climb-10000'))

rec(PT,
    q='Cabin preparation PA: who, when, and the words?',
    a='PM, no later than about 18,000 ft MSL (near T/D on short legs, or when Early Sit is used): [Flight Attendants], please prepare the cabin for arrival and be seated for landing.',
    who='PM. Seat belt sign ON goes with it, no later than 18,000 ft.',
    ref='FCOM PRO-NOR-SOP-17-A', ident='PRO-NOR-SOP-17-A-C0000234.9001001',
    src='"[Flight Attendants], please prepare the cabin for arrival and be seated for landing."', ext='FCOM', kind='manual')

rec(PT,
    q='Descending through 10,000 ft AAL. The flow?',
    a='LAND ON, SEAT BELTS ON, NO SMOKING cycle (PM); EFIS CSTR both sides; LS pb as required (PF-PM); NAVAIDS check (PF); ENG START selector as required (PM). Then the Approach Checklist once baro is set.',
    who='PM does the lights and signs. CSTR and LS are both sides. NAVAIDS is PF.',
    ref='FCOM PRO-NOR-SOP-17-A', ident='PRO-NOR-SOP-17-A-00011974.0002001',
    src='L2 Select CSTR on both sides.', ext='FCOM', kind='manual',
    flow=flow_from_phase('descent-10000'))

rec(PT,
    q='What triggers the Approach Checklist?',
    a='Below 10,000 ft AAL and barometric reference set (or after the approach briefing when staying in the terminal area)',
    who='PF requests, PM reads. BARO REF is a BOTH item: PF then PM read the setting.',
    ref='FCTM PR-NP-CL (Approach)', ident='PR-NP-CL-00024941.0001001',
    src='Checklist trigger: ‐ Below 10 000 ft AAL and barometric reference set, or ‐ After the approach briefing is completed, for the case when not leaving the terminal area or climbing above 10 000 ft AAL (Case of an Air Turn Back or Traffic Pattern or Go Around)',
    ext='FCTM', kind='sop')

rec(PT,
    q='Flaps at 2. What comes next, and who does it?',
    a='PF orders L/G DOWN; PM selects the lever down, confirms AUTO BRK, arms GROUND SPOILERS',
    who='PF orders, PM acts. Then FLAPS 3 when the gear is down, then FLAPS FULL.',
    ref='FCOM PRO-NOR-SOP-18-B-B', ident='PRO-NOR-SOP-18-B-B-00014482.0001001',
    src='L/G DOWN........................................................................................................ORDER PF L/G lever..............................................................................................SELECT DOWN PM AUTO BRK....................................................................................................CONFIRM PM',
    ext='FCOM', kind='manual')

rec(PT,
    q='Cleared for approach, then cleared to land: the exterior lights?',
    a='Cleared for approach: NOSE TAXI, RWY TURN OFF ON. Cleared to land: NOSE T.O. All PM.',
    who='PM',
    ref='FCOM PRO-NOR-SOP-18-B-B', ident='PRO-NOR-SOP-18-B-B-00014482.0001001',
    src='NOSE sw.....................................................................................................TAXI PM RWY TURN OFF sw......................................................................................ON PM',
    ext='FCOM', kind='manual')

rec(PT,
    q='What triggers the Landing Checklist?',
    a='LDG CONF set (landing flaps selected, LDG MEMO checked no blue)',
    who='PF orders FLAPS FULL (or 3), PM selects and checks LDG MEMO no blue. PF requests the checklist, PM reads, PF responds LANDING NO BLUE.',
    ref='FCTM PR-NP-CL (Landing)', ident='PR-NP-CL-00024942.0002001',
    src='Checklist trigger: LDG CONF set.', ext='FCTM', kind='sop')

rec(PT,
    q='Runway vacated. First action, and what does it trigger?',
    a='PF disarms GND SPLRS. That starts the After Landing flow, then the After Landing Checklist.',
    who='PF: ground spoilers, LAND OFF, WING OFF, STROBE AUTO, NOSE TAXI. PM: radar OFF, ENG START NORM, flaps retract, TCAS STBY, ATC, APU, anti-ice, brake temps.',
    tech='QuickRef technique: Flow Trigger is PF disarms Gnd Splrs.',
    ref='FCOM PRO-NOR-SOP-21-A', ident='PRO-NOR-SOP-21-A-00011014.0001001',
    src='GND SPLRS..............................................................................................DISARM PF', ext='FCOM', kind='manual',
    flow=flow_from_phase('after-landing'))


rec(PT,
    q='At the gate: how long before the ENG MASTER levers come off, and who?',
    a='No less than 1 min after high thrust operations; PF sets all ENG MASTER levers OFF',
    who='PF. With the APU: APU BLEED ON and wait for the APU BLEED memo first (PM).',
    ref='FCOM PRO-NOR-SOP-22-A', ident='PRO-NOR-SOP-22-A-00012192.0004001',
    src='The flight crew must operate the engines at or near idle thrust for a cooling period of 1 min before engine shutdown, in order to thermally stabilize the engines.',
    ext='FCOM', kind='manual',
    flow=flow_from_phase('parking'))

rec(PT,
    q='What triggers the Parking Checklist?',
    a='Parking flow pattern completed',
    who='PF requests, PM reads. PF responds PARKING BRAKE SET or CHOCKS SET.',
    ref='FCTM PR-NP-CL (Parking)', ident='PR-NP-CL-00024944.0001001',
    src='Checklist trigger: After Parking flow pattern completed.', ext='FCTM', kind='sop')

rec(PT,
    q='Securing the Aircraft: who does it, and what kind of procedure is it?',
    a='PM. It is a Supplementary Procedure (FCOM PRO-NOR-SUP-SEC), read and do.',
    who='PM alone. The NPC card just says REFER TO FCOM.',
    ref='FCTM PR-NP-CL (General)', ident='PR-NP-CL-00019512.0001001',
    src='Securing the Aircraft is performed by the PM and is a Supplementary Procedure. Refer to FCOM/PRO-NOR-SUP-SEC.',
    ext='FCTM', kind='sop')


# ---------------------------------------------------------------- APPROACH SETUP
AS = 'Approach Setup'


rec(AS,
    q='Descent preparation: the FMS pages in FCOM order?',
    a='ARRIVAL, F-PLN A, RADIO NAV, SELECTED NAVAIDS, DES WIND, PERF CRUISE, PERF DES, PERF APPR, PERF GO AROUND, FUEL PRED, PROG, SEC F-PLN. Then PM crosschecks. Then LDG ELEV and AUTO BRK.',
    who='PF builds every page. PM crosschecks the whole FMS preparation afterwards.',
    ref='FCOM PRO-NOR-SOP-16-A', ident='PRO-NOR-SOP-16-A-00023628.0001001',
    src='After the PF prepares the FMS, the PM checks all the data entered in the FMS. The PM should have the same mental image of the intended arrival and approach procedure, trajectory, and constraints than the PF.',
    ext='FCOM', kind='manual',
    flow=flow_manual('Descent preparation (FCOM PRO-NOR-SOP-16-A order)', [
        ('Weather and landing information: OBTAIN', 'PM'),
        ('Jeppesen charts: PREPARE', 'ALL'),
        ('Barometric reference: PRESET (QNH on the ISIS)', 'PM'),
        ('ECAM STATUS: CHECK', 'PM'),
        ('Landing performance: CHECK', 'PM'),
        ('ARRIVAL page: COMPLETE/CHECK', 'PF'),
        ('F-PLN A page: CHECK', 'PF'),
        ('RADIO NAV page: CHECK', 'PF'),
        ('SELECTED NAVAIDS page: CHECK/MODIFY', 'PF'),
        ('DES WIND page: CHECK', 'PF'),
        ('PERF CRUISE page: CHECK', 'PF'),
        ('PERF DES page: CHECK', 'PF'),
        ('PERF APPR page: COMPLETE/CHECK', 'PF'),
        ('PERF GO AROUND page: CHECK/MODIFY', 'PF'),
        ('FUEL PRED page: CHECK', 'PF'),
        ('PROG page: CONSIDER (BRG/DIST reference)', 'PF'),
        ('SEC F-PLN page: AS RQRD', 'PF'),
        ('FMS PREPARATION: CROSSCHECK', 'PM'),
        ('LDG ELEV: CHECK', 'PF'),
        ('AUTO BRK: AS RQRD', 'PF'),
        ('Arrival Legs Verification: PERFORM', 'BOTH'),
        ('Approach Briefing: PERFORM', 'BOTH'),
        ('Radar: ADJUST AS APPROPRIATE', 'PF'),
        ('Anti-ice: AS RQRD', 'PM'),
        ('Descent clearance: OBTAIN', 'PM'),
        ('Cleared altitude on FCU: SET', 'PF'),
    ]))

rec(AS,
    q='PERF APPR page: what goes in?',
    a='Guidance mode for a non-precision approach (FLS or FINAL APP), QNH, temperature and wind at destination, the minimum, the landing configuration (CONF FULL or CONF 3), the transition altitude/level',
    who='PF',
    ref='FCOM PRO-NOR-SOP-16-A', ident='PRO-NOR-SOP-16-A-00020073.0012001',
    src='‐ Check or modify the landing configuration. Always select the landing configuration on the PERF APPR page:',
    ext='FCOM', kind='manual')

rec(AS,
    q='PERF APPR wind entry when the ATIS reads 15020G35KT?',
    a='150/20. Average wind only, never the gust. Ground Speed Mini handles the gust.',
    who='PF',
    ref='FCOM PRO-NOR-SOP-16-A', ident='PRO-NOR-SOP-16-A-00020073.0012001',
    src='Insert the average wind given by the ATC or ATIS. Do not insert the gust value.', ext='FCOM', kind='manual')

rec(AS,
    q='Autobrake mode for landing: how do you choose?',
    a='LO on long runways. MED on short or contaminated runways. MAX is not recommended at landing.',
    who='PF selects during descent preparation. PM confirms it when the gear comes down.',
    ref='FCOM PRO-NOR-SOP-16-A', ident='PRO-NOR-SOP-16-A-00012251.0001001',
    src='Use of MAX mode is not recommended at landing. On short or contaminated runways, use MED mode. On long runways, LO mode is recommended',
    ext='FCOM', kind='manual')

rec(AS,
    q='Arrival Legs Verification: when, and who reads from what?',
    a='After the FMGS descent preparation and before the Approach Briefing. PF reads from the ND (glass), PM verifies against the Jeppesen charts (paper).',
    who='PF: PLAN mode, CSTR on, F-PLN page, reads each waypoint and constraint. PM: follows on the charts and resolves discrepancies.',
    ref='FCOM PRO-NOR-SOP-16-A', ident='PRO-NOR-SOP-16-A-90000104.9000258',
    src='The Arrival Legs Verification will be accomplished after the FMGS descent preparation and before accomplishing the Approach Briefing.',
    ext='FCOM', kind='manual')

rec(AS,
    q='Approach Briefing: the Plan items on the Crew Briefing Card?',
    a='Route (STAR, Approach, Approach Mode); Missed Approach, Fuel/route to alternate; Landing Runway Assessment, Exit, Taxi; Autobrakes; Flaps, Approach/Target Speed. Threats first (PM, PF), Considerations after.',
    who='Both. Threats are called by PM then PF.',
    ref='PRC p24 Crew Briefing Card',
    src='• Route (STAR, Approach, Approach Mode)', ext='PRC', kind='sop')


rec(AS,
    q='ILS: the three conditions before APPR pb, and what follows?',
    a='Cleared for the approach, on the intercept trajectory for the final approach course, LOC deviation available on the PFD. Then APPR pb press, BOTH APs engage (PF).',
    who='PF presses APPR and engages both APs.',
    ref='FCOM PRO-NOR-SOP-18-C-A', ident='PRO-NOR-SOP-18-C-A-00014488.0001001',
    src='Press the APPR pb when all of the following is applicable: • The aircraft is cleared for the approach • The aircraft is on the intercept trajectory for the final approach course • LOC deviation is available on the PFD.',
    ext='FCOM', kind='manual')

rec(AS,
    q='Decelerated ILS: when is FLAPS 1 called, and when FLAPS 2?',
    a='FLAPS 1 at green dot, more than 3 NM before the FDP. FLAPS 2 at 2,500 ft AGL minimum.',
    who='PF orders, PM answers SPEED CHECKED then selects.',
    ref='FCOM PRO-NOR-SOP-18-B-B', ident='PRO-NOR-SOP-18-B-B-00014480.0001001',
    src='‐ FLAPS 1 should be selected more than 3 NM before the Final Descent Point', ext='FCOM', kind='manual')

# ---------------------------------------------------------------- GO-AROUND BRIEF
GA = 'Go-Around Brief'

rec(GA,
    q='Go-around: the three simultaneous actions?',
    a='THRUST LEVERS TOGA, ROTATION toward 15 deg, announce GO AROUND (callout: GO AROUND - FLAPS)',
    who='All three are PF. PM monitors flight parameters and retracts flaps one step.',
    ref='FCOM PRO-NOR-SOP-20-A', ident='PRO-NOR-SOP-20-A-00011082.0008001',
    src='Simultaneously apply the following three actions:', ext='FCOM', kind='manual',
    flow=flow_manual('Go-around (FCOM PRO-NOR-SOP-20-A order)', [
        ('THRUST LEVERS: TOGA', 'PF'),
        ('ROTATION: PERFORM (15 deg, about 12.5 deg one engine out, then SRS)', 'PF'),
        ('GO AROUND: ANNOUNCE', 'PF'),
        ('FLIGHT PARAMETERS: MONITOR', 'PM'),
        ('FLAPS: RETRACT ONE STEP', 'PM'),
        ('FMA: CHECK/ANNOUNCE (MAN TOGA / SRS / GA TRK or NAV / A/THR)', 'PF'),
        ('POSITIVE RATE: ANNOUNCE', 'PM'),
        ('L/G UP: ORDER', 'PF'),
        ('L/G: UP', 'PM'),
        ('NAV or HDG mode: AS RQRD', 'PF'),
        ('GO AROUND ALTITUDE: CHECK', 'PM'),
        ('At thrust reduction altitude, THRUST LEVERS: CL (LVR CLB flashing)', 'PF'),
        ('At acceleration altitude, SPEED: MONITOR (target to green dot)', 'PF'),
        ('Acceleration flow: FLAPS 1 at F, FLAPS 0 at S, GND SPLRS disarm, L/G check up, lights', 'PM'),
    ]))

rec(GA,
    q='Go-around callouts in order, PF and PM?',
    a='PF: GO AROUND - FLAPS. PM: FLAPS __. PM: POSITIVE CLIMB. PF: GEAR UP. PM: GEAR UP.',
    who='PF calls the go-around and the gear. PM answers the flap setting and calls positive climb.',
    ref='FCOM PRO-NOR-SCO-D', ident='PRO-NOR-SCO-D-00011850.0001001',
    src='GO AROUND decision GO AROUND - FLAPS Flaps retraction FLAPS__ Gear retraction POSITIVE CLIMB GEAR UP GEAR UP',
    ext='FCOM', kind='manual')

rec(GA,
    q='FMA after TOGA on the go-around?',
    a='MAN TOGA / SRS / GA TRK or NAV / A/THR',
    who='PF checks and announces the FMA.',
    ref='FCOM PRO-NOR-SOP-20-A', ident='PRO-NOR-SOP-20-A-00011082.0008001',
    src='The following modes are displayed: MAN TOGA / SRS / GA TRK or NAV / A/THR.', ext='FCOM', kind='manual')

rec(GA,
    q='Why must the thrust levers touch TOGA even when TOGA thrust is not needed?',
    a='To engage the GO AROUND phase. Otherwise, within 7 NM of the airport the FMS sequences the destination waypoint. Set TOGA, then retard as required (CL keeps A/THR).',
    who='PF',
    ref='FCOM PRO-NOR-SOP-20-A', ident='PRO-NOR-SOP-20-A-00011082.0008001',
    src='If the thrust levers are not set briefly to TOGA detent, the FMS does not engage the GO AROUND phase, and flying over, or close to the airport (less than 7 NM) will sequence the Destination waypoint in the F-PLN.',
    ext='FCOM', kind='manual')


rec(GA,
    q='Go-around thrust reduction and acceleration altitudes: what happens at each?',
    a='Thrust reduction: THRUST LEVERS CL when LVR CLB flashes (PF). Acceleration: monitor target speed increases to green dot; if not, check FCU ALT and pull the ALT knob. Then the Acceleration flow.',
    who='PF. PM runs the Acceleration flow after FLAPS 0.',
    ref='FCOM PRO-NOR-SOP-20-A', ident='PRO-NOR-SOP-20-A-00011085.0001001',
    src='Monitor that the target speed increases to Green Dot.', ext='FCOM', kind='manual')

rec(GA,
    q='Discontinued approach or go-around: which one, and when?',
    a='At or above the FCU altitude: either the GO AROUND procedure or the discontinued approach (announce CANCEL APPROACH, press APPR or LOC pb to disarm, select modes and speed). Below the FCU altitude: GO AROUND procedure, mandatory.',
    who='PF decides and announces.',
    ref='FCOM PRO-NOR-SOP-18-A', ident='PRO-NOR-SOP-18-A-00015153.0001001',
    src='When the aircraft is below the FCU altitude, the flight crew must apply the GO AROUND procedure.', ext='FCOM', kind='manual')

# ---------------------------------------------------------------- CHECKLIST ORDER
CO = 'Checklist Order'

rec(CO,
    q='Recite the A330 normal checklists in order',
    a='Cockpit Preparation, Before Start, After Start, Taxi, Line-Up, (Departure Change), Approach, Landing, After Landing, Parking, Securing the Aircraft',
    who='PF requests each one. PM reads, PF responds.',
    ref='FCTM PR-NP-CL',
    src='Cockpit Preparation................................................................................................................................................. B Before Start..............................................................................................................................................................C After Start.................................................................................................................................................................D Taxi...........................................................................................................................................................................E Line-Up..................................................................................................................................................................... F << Departure Change >>........................................................................................................................................G Approach..................................................................................................................................................................H Landing...................................................................................................................................................................... I After Landing............................................................................................................................................................ J Parking..................................................................................................................................................................... K Securing the Aircraft................................................................................................................................................ L',
    ext='FCTM', kind='sop')

rec(CO,
    q='Who requests the checklist, who reads, who responds?',
    a='PF requests. PM reads the challenge (left side). PF responds after checking the actual aircraft status.',
    who='As FO in the right seat: when the CA flies you read; when you fly you call for it and respond.',
    ref='FCTM PR-NP-CL (General)', ident='PR-NP-CL-00019512.0001001',
    src='The Pilot Flying (PF) requests the normal checklist.', ext='FCTM', kind='sop')


rec(CO,
    q='Which checklist follows Line-Up?',
    a='Approach. There is no after-takeoff or descent checklist on the A330.',
    who='The next time the PF asks for a checklist is below 10,000 ft AAL on arrival.',
    ref='FCTM PR-NP-CL (Approach)', ident='PR-NP-CL-00024941.0001001',
    src='Checklist trigger: ‐ Below 10 000 ft AAL and barometric reference set, or', ext='FCTM', kind='sop')

rec(CO,
    q='What kind of checklist is an Airbus normal checklist?',
    a='Non-action. Every action is done from memory (the flow) first; the checklist only confirms.',
    who='The Captain ensures the checklist is used on every flight, every phase, without exception.',
    ref='FCTM PR-NP-CL (General)', ident='PR-NP-CL-00019512.0001001',
    src='Airbus normal checklists are of a “non-action” type (i.e. all actions should be completed from memory before the flight crew performs the checklist).',
    ext='FCTM', kind='sop')

rec(CO,
    q='Checklist complete and checklist interrupted: the words?',
    a='PM: __ CHECKLIST COMPLETE. If interrupted: HOLD CHECKLIST AT ___, then RESUME CHECKLIST AT ___.',
    who='PM announces completion, e.g. LANDING CHECKLIST COMPLETE.',
    ref='FCOM PRO-NOR-SCO', ident='PRO-NOR-SCO-00011826.0001001',
    src='If a checklist needs to be interrupted, announce : “HOLD CHECKLIST AT ___” and “RESUME CHECKLIST AT ___” for the continuation. Upon completion of a checklist announce : “__CHECKLIST COMPLETE”.',
    ext='FCOM', kind='manual')

rec(CO,
    q='Landing Checklist when the LDG MEMO does not appear below 2,000 ft RA?',
    a='Use the expanded LDG MEMO section: LDG GEAR DN, SEAT BELTS ON, SPLRS ARM, FLAPS LDG. PM reads each challenge, PF responds each item.',
    who='PM reads, PF responds, once fully configured for landing.',
    ref='FCTM PR-NP-CL (General)', ident='PR-NP-CL-00019512.0001001',
    src='If the ECAM LDG MEMO does not annunciate below 2 000 ft RA, the expanded LDG MEMO section of the Landing Checklist is used by the flight crew. Once fully configured for landing, the PM must read the challenge and the PF must respond for each item.',
    ext='FCTM', kind='sop')


def main():
    for d in R:
        for k in ('s', 'q', 'a', 'ref', 'src', 'fleet', 'kind', 'ext'):
            assert d.get(k), (k, d.get('q'))
        assert d['s'] in ('Phase Triggers', 'Approach Setup', 'Go-Around Brief', 'Checklist Order')
        assert d['ext'] in EXTRACTS
    with open(OUT, 'w', encoding='utf-8') as f:
        json.dump(R, f, ensure_ascii=False, indent=1)
        f.write('\n')
    from collections import Counter
    c = Counter(d['s'] for d in R)
    print(f'wrote {OUT}: {len(R)} records', dict(c))


if __name__ == '__main__':
    main()
