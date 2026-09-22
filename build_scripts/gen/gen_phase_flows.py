#!/usr/bin/env python3
"""Generate WORK/data/phase_flows.json (A330 PAX phase flows) for phase_flows.html.
Scratch generator: every quote is typed from the extract and proven by verify_phase_flows.py."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.abspath(os.path.join(HERE, '..', '..'))  # repo root
FLOWS = json.load(open(os.path.join(WORK, 'data', 'flows.json'), encoding='utf-8'))
MEM = json.load(open(os.path.join(WORK, 'data', 'memory_items_drill.json'), encoding='utf-8'))
LIM = json.load(open(os.path.join(WORK, 'data', 'limitations_drill.json'), encoding='utf-8'))

PN = 'FCOM PRO-NOR'

def box(t, s='', r='B', call=False, quote='', ref='', ext=PN, src='manual', fleet='pax'):
    return {'k': 'box', 't': t, 's': s, 'r': r, 'call': bool(call), 'quote': quote, 'ref': ref, 'ext': ext, 'fleet': fleet, 'src': src}
def fmc(t, s='', r='PF', quote='', ref='', ext=PN, src='manual', fleet='pax'):
    return {'k': 'fmc', 't': t, 's': s, 'r': r, 'quote': quote, 'ref': ref, 'ext': ext, 'fleet': fleet, 'src': src}
def sub(t, c): return {'k': 'sub', 't': t, 'c': c}
def trig(t, r='B'): return {'k': 'trig', 't': t, 'r': r}
def cl(t, w='', bold=False, cc=True): return {'k': 'cl', 't': t, 'w': w, 'bold': bool(bold), 'cc': bool(cc)}
def book(t, s=''): return {'k': 'book', 't': t, 's': s}
def note(t): return {'k': 'note', 't': t}
def S(h, c, items, cite='', appr='all'): return {'h': h, 'c': c, 'items': items, 'cite': cite, 'appr': appr}
def P(id, label, kind, title, src, sections, srck='manual'):
    return {'id': id, 'label': label, 'kind': kind, 'title': title, 'src': src, 'sections': sections, 'fleet': 'pax', 'provenance': srck}

ROLE = {'CM1': 'C', 'CM2': 'F', 'PF': 'PF', 'PM': 'PM', 'BOTH': 'B', None: 'B'}
def fl(pid):
    return next(p for p in FLOWS['phases'] if p['id'] == pid)

# colours (B787 phase palette; brand hexes are remapped by apply_palette at build)
NAVY = '#01426A'; SLATE = '#334e68'; TEAL = '#0a6c8f'; GREEN = '#00805E'; PURP = '#5A4AB7'; GOLD = '#b8860b'
RED = '#b03a2e'; PLUM = '#7a3b8f'; BLUE = '#1864ab'; CYAN = '#0a8fb0'; FOREST = '#2e7d5b'; VIOLET = '#5f3dc4'; AMBER = '#E0A100'
BROWN = '#9c5800'; OCEAN = '#0b7285'

PH = []

# ============================================================ NORMAL
# ---------------------------------------------------------------- PREFLIGHT
PH.append(P('preflight', 'Preflight', 'n', 'PREFLIGHT', 'FCOM PRO-NOR-SOP-03 / SOP-04', [
  S('SAFETY EXTERIOR INSPECTION (CM2)', SLATE, [
    box('General', 'Obstructions near the aircraft · Engineering activity · Refueling activity', 'F', False,
        'When the flight crew arrives at the aircraft, they must check for, or be informed of any obstructions near the aircraft, engineering activity, or refueling activity, etc.',
        'PRO-NOR-SOP-03-A-00010458.0001001'),
    box('Wheel chocks', 'WHEEL CHOCKS ... CHECK', 'F', False,
        'If the wheel chocks are not in position, the flight crew must check that the parking brake is set with sufficient accumulator pressure.',
        'PRO-NOR-SOP-03-A-00010461.0001001'),
    box('Landing gear doors', 'LANDING GEAR DOORS ... CHECK POSITION', 'F', False,
        'If any landing gear door is open, do not pressurize the hydraulic systems until clearance is obtained from ground personnel.',
        'PRO-NOR-SOP-03-A-00010462.0001001'),
    box('APU area', 'APU AREA ... CHECK', 'F', False,
        'Observe that the APU inlet and outlet are clear.', 'PRO-NOR-SOP-03-A-00010463.0001001'),
  ], 'FCOM PRO-NOR-SOP-03'),
  S('PRELIMINARY COCKPIT PREP · CM2 (overhead / pedestal)', TEAL, [
    note('Items marked * are the only steps after a transit stop without flight crew change.'),
    box('ENG masters OFF · ENG START NORM', 'ENG 1, 2 MASTERS LEVERS ... OFF · ENG START selector ... NORM', 'F', False,
        'ENG 1, 2 MASTERS LEVERS ... OFF CM2 ENG START selector ... NORM CM2', 'PRO-NOR-SOP-04-A-00010897.0001001'),
    box('Weather radar OFF *', 'WXR/PWS sw ... OFF · CAPT and F/O DISPLAY mode selectors ... OFF · GAIN ... AUTO · TURB ... AUTO', 'F', False,
        '* WXR/PWS sw ... OFF CM2 * CAPT DISPLAY mode selector ... OFF CM2 * F/O DISPLAY mode selector ... OFF CM2 * GAIN knob ... AUTO CM2 * TURB sw ... AUTO CM2',
        'PRO-NOR-SOP-04-A-00011881.0009001'),
    box('L/G lever DOWN', 'L/G lever ... DOWN', 'F', False, 'L/G lever ... DOWN CM2', 'PRO-NOR-SOP-04-A-00010898.0001001'),
    box('Wipers OFF', 'Both WIPER selectors ... OFF', 'F', False, 'Both WIPER selectors ... OFF CM2', 'PRO-NOR-SOP-04-A-00010899.0001001'),
    box('Batteries check / ELEC', 'Not supplied 6 h or more: BAT 1, BAT 2, APU BAT ... CHECK OFF · VOLTAGE ... CHECK ABOVE 25.5 V · BAT 1, BAT 2, APU BAT pb-sw ... AUTO · EXT PWR pb ... ON · already supplied: BAT pb-sw ... AUTO · voltage ... CHECK ABOVE 23.5 V · EXT PWR pb ... ON', 'F', False,
        'Battery voltage above 25.5 V ensures a charge above 50 %. After the check, the selector should remain on the APU position to avoid discharge of BAT 1 or 2.',
        'PRO-NOR-SOP-04-00010900.0002001'),
    box('RMP 1 and 2 CHECK ON', 'Green NAV light ... CHECK OFF · COM FREQUENCIES ... TUNE · ACP: INT knob ... PRESS OUT/VOLUME CHECK · VHF ... CHECK', 'F', False,
        'Use VHF 1 for ATC (only VHF 1 is available in emergency electrical configuration), VHF 2 for ATIS and company frequencies. VHF 3 is normally devoted to ACARS.',
        'PRO-NOR-SOP-04-C-00025222.0001001'),
    box('APU FIRE pb-sw', 'APU FIRE pb-sw ... CHECK IN and GUARDED · APU AGENT light ... CHECK OFF · APU FIRE TEST pb ... PRESS and MAINTAIN', 'F', False,
        'APU FIRE TEST pb ... PRESS and MAINTAIN CM2', 'PRO-NOR-SOP-04-C-00010902.0001001'),
    box('APU start · bleed', 'APU MASTER SW pb-sw ... ON · APU pb (ECAM control panel) ... PRESS · APU START pb-sw ... ON · when AVAIL: APU BLEED pb-sw ... ON · X-BLEED ... AUTO · COCKPIT / CABIN TEMP ... AS RQRD · * EXT PWR pb ... AS RQRD', 'F', False,
        'Do not use APU BLEED, if the ground personnel confirms that a LP or HP ground air unit is connected to the aircraft.',
        'PRO-NOR-SOP-04-C-00010903.0002001'),
    box('ADIRS * ALL IR MODE selector NAV', 'Complete alignment: first flight of the day · crew change · departure between 2° N and 2° S · GPS not available and poor NAVAID coverage · GPS not available and flight time more than 3 h', 'F', False,
        'A complete IRS alignment must be performed in the following cases: - Before the first flight of the day, or - When there is a crew change, or - When the departure airport is located between latitudes 2 ° north and 2 ° south, or - When the GPS is not available and the NAVAID coverage is poor on the expected route, or - When the GPS is not available and the expected flight time is more than 3 h.',
        'PRO-NOR-SOP-04-00011860.0004001'),
    box('Cockpit lights * AS RQRD', 'Set INT LT, FLOOD LT, INTEG LT (glareshield and FCU)', 'B', False,
        'Set INT LT, FLOOD LT, INTEG LT (included glareshield and FCU).', 'PRO-NOR-SOP-04-00010908.0001001'),
    box('ATIS * OBTAIN', 'ATIS ... OBTAIN', 'F', False, '* ATIS ... OBTAIN CM2-CM3', 'PRO-NOR-SOP-04-00021760.0001001'),
  ], 'FCOM PRO-NOR-SOP-04'),
  S('PRELIMINARY COCKPIT PREP · CM1 / BOTH', NAVY, [
    fmc('MCDU ON (pre-initialization)', 'MCDU ... ON (short press of BRT) · MCDU ANNUNCIATOR LIGHTS ... OFF · A/C STATUS ... CHECK · ACTIVE NAV DATABASE ... CYCLE · FMS DATABASE VALIDITY ... CHECK · NAVAID DESELECTION ... AS RQRD · FLIGHT PLAN UPLINK ... REQUEST', 'C',
        'Short press of the BRT button will switch ON the MCDU, if it is OFF. Use the brightness buttons (BRT and DIM) to adjust the brightness as required.',
        'PRO-NOR-SOP-04-90000080.9000329'),
    box('EFB start (Flysmart)', 'ALL EFB ... START · EFB/eQRH VERSION ... CHECK · * EFB STATUS page ... INSERT/CHECK', 'B', False,
        'On the EFB STATUS page, each flight crewmember inserts and checks: - ACFT TYPE and ACFT REG - FLT NBR and FROM/TO (in agreement with the FMS ACTIVE/INIT page).',
        'PRO-NOR-SOP-04-00021766.0001001'),
    box('RCL pb * PRESS 3 s', 'recalls warnings cleared or cancelled during the last flight', 'C', False,
        'This action recalls all the warnings that the flight crew cleared or cancelled during the last flight.', 'PRO-NOR-SOP-04-00021759.0002001'),
    box('LOGBOOK and MEL/CDL items * CHECK', 'deferred items list · crosscheck with ECAM recall · MEL / CDL acceptability and influence on the flight plan · AIRCRAFT CONFIGURATION SUMMARY ... CHECK (QRH OPS.01A)', 'B', False,
        'Check and discuss the MEL items (including the associated operational procedures, if any) and the CDL items. This includes the acceptability of the MEL and CDL items and the influence on the flight plan',
        'PRO-NOR-SOP-04-00021759.0002001'),
    box('OEB * CHECK', 'all crewmembers review and discuss applicable OEBs', 'B', False,
        'All flight crewmembers review and discuss together all OEBs and associated procedures applicable to the aircraft.', 'PRO-NOR-SOP-04-00021759.0002001'),
    box('AIRCRAFT ACCEPTANCE * PERFORM', 'may be performed later, must be complete by end of Cockpit Preparation', 'C', False,
        'The aircraft acceptance can be performed later, but must be completed at the end of the Cockpit Preparation.', 'PRO-NOR-SOP-04-00021759.0002001'),
    box('Jeppesen charts * PREPARE', '', 'B', False, '* JEPPESEN CHARTS ... PREPARE ALL', 'PRO-NOR-SOP-04-00021760.0001001'),
    box('ACARS * INITIALIZE', '', 'PF', False, '* ACARS ... INITIALIZE PF', 'PRO-NOR-SOP-04-00021760.0001001'),
    box('Preliminary takeoff perf data * OBTAIN', 'per technical condition, NOTAM, runway condition, configuration', 'PF', False,
        'The flight crew computes the preliminary performance data in accordance with the technical condition of the aircraft and/or any other criteria that may affect the aircraft performance (e.g. NOTAM, runway condition, aircraft configuration).',
        'PRO-NOR-SOP-04-00021760.0001001'),
  ], 'FCOM PRO-NOR-SOP-04'),
  S('BEFORE WALKAROUND (PM)', FOREST, [
    box('OXY · HYD · ENG OIL *', 'DOOR SD: OXY ... CHECK PRESSURE · MIN FLT CREW OXY CHART ... CHECK PRESSURE · HYD SD: RESERVOIR FLUID LEVEL ... CHECK WITHIN NORMAL RANGE · ENG SD: ENG OIL QUANTITY ... CHECK', 'PM', False,
        'Check that the oil quantity is above the minimum. Refer to LIM-ENG Oil.', 'PRO-NOR-SOP-04-D-00021790.0002001'),
    box('FLAPS CHECK POSITION · SPEED BRAKE * CHECK RETRACTED and DISARMED', '', 'PM', False,
        'If flight control surface positions do not agree with the control handle positions, check with the maintenance crew before applying hydraulic power.',
        'PRO-NOR-SOP-04-D-00010909.0001001'),
    box('ACCU PRESS * CHECK · PARK BRK * ON · BRAKES PRESS * CHECK', 'ACCU PRESS in the green band; blue electric pump to recharge if required', 'PM', False,
        'The ACCU PRESS indication must be in the green band. If required use the electric pump on blue hydraulic system to recharge the brake accumulator.',
        'PRO-NOR-SOP-04-D-00010910.0001001'),
    box('Alternate braking check', 'first flight of the day: CHOCKS ... CHECK IN PLACE · PARK BRK handle ... OFF · BRAKE PEDALS ... PRESS · BRAKE PRESSURE ... CHECK · BRAKE PEDALS ... RELEASE · PARK BRK handle ... ON', 'PM', False,
        'The purpose of this check is to verify, before the first flight of the day, the efficiency of the alternate braking system (absence of “spongy pedals”).',
        'PRO-NOR-SOP-04-D-00010911.0001001'),
    box('EMER EQPT CHECK', 'Life vests · Crash axe · Smoke hoods / portable oxygen and full-face masks · Portable fire extinguisher lockwired, gauge green · Oxygen masks · Flashlights · Escape ropes · PED Fire Containment Bag · Fire gloves', 'PM', False,
        '- Portable fire extinguisher is lockwired and the pressure gauge indicator is in the green area - Oxygen masks are stowed - Flashlights are stowed - Escape ropes are stowed - PED Fire Containment Bag is stowed - Fire gloves are stowed',
        'PRO-NOR-SOP-04-D-00010919.0001001'),
    box('RAIN RPLNT indicators CHECK PRESSURE and QUANTITY', '', 'PM', False,
        'Never use rain repellent to wash the windshield and never use it on a dry windshield.', 'PRO-NOR-SOP-04-D-00010920.0001001'),
    box('GEAR PINS * CHECK ONBOARD and STOWED', 'three gear pins', 'PM', False,
        'Check that the three gear pins are onboard and stowed.', 'PRO-NOR-SOP-04-D-00010921.0002001'),
    trig('PM: exterior walkaround (PRO-NOR-SOP-05) · PF: cockpit preparation', 'PM'),
  ], 'FCOM PRO-NOR-SOP-04'),
]))

# ---------------------------------------------------------------- COCKPIT PREP
PH.append(P('cockpit-prep', 'Cockpit Prep', 'n', 'COCKPIT PREPARATION', 'FCOM PRO-NOR-SOP-06', [
  S('COCKPIT PREPARATION FLOW', NAVY, [
    box('Overhead panel scan', '* ALL WHITE LIGHTS ... OFF · * RCDR GND CTL pb-sw ... ON · CAPT & PURS/CAPT sw ... CAPT · * STARLINK ... AS RQRD · * RESET BUTTONS (left side) ... CHECK · EXT LT: STROBE ... AUTO · BEACON ... OFF · WING ... OFF · NAV & LOGO ... 1 · NOSE ... OFF · LAND ... OFF · RWY TURN OFF ... OFF · * SIGNS panel ... SET · PROBE/WINDOW HEAT pb-sw ... AUTO · LDG ELEV knob ... AUTO · MAN VALVE SEL ... BOTH · * PACK FLOW ... AUTO · EL/DC pb (ECAM) ... PRESS · BAT 1, BAT 2, APU BAT pb-sw ... OFF then AUTO · T TANK MODE pb-sw ... CHECK AUTO · T TANK FEED selector ... CHECK AUTO · ENG 1 and ENG 2 FIRE pb-sw ... CHECK IN and GUARDED · AGENT 1 and 2 lights ... CHECK OFF · ENG TEST pb ... PRESS and MAINTAIN · ALL LIGHTS ... CHECK · TEMPERATURE selectors ... AS RQRD · FWD COOLING selector ... AS RQRD · PA (3rd occupant) ... RECEPT · CVR TEST pb ... PRESS and MAINTAIN · * RESET BUTTONS (right side) ... CHECK · DATA LOADER ... CHECK OFF', 'PF', False,
        'As a general rule, during the scan sequence of the overhead panel: * ALL WHITE LIGHTS ... OFF PF', 'PRO-NOR-SOP-06-A-00011857.0001001'),
    box('Front instrument panels', '* ISIS ... CHECK (brightness, IAS, altimeter, attitude, no flags) · * NORTH REF ... CHECK (TRUE blue light off) · DMC selector ... CHECK AUTO · ECAM/ND selector ... CHECK NORM · * CLOCK ... CHECK/SET · LDG GEAR GRVTY EXTN selector ... OFF · * A/SKID & N/W STRG sw ... ON', 'PF', False,
        '- Adjust brightness. - Check IAS, altimeter readings, altimeter settings and attitude display. - Check no flags - Reset attitude, if necessary.',
        'PRO-NOR-SOP-06-B-00011875.0001001'),
    box('Center pedestal', 'RMP 1 and 2 ... CHECK ON · Green NAV light ... CHECK OFF · COM FREQUENCIES ... TUNE · ACP: INT knob ... PRESS OUT/VOLUME CHECK · VHF ... CHECK · HF (if required) ... CHECK · * ACCU PRESS indicator ... CHECK · * PARK BRK handle ... CHECK ON · * BRAKE PRESS indicator ... CHECK · ANN LT selector ... TEST then BRT · COCKPIT DOOR ... CHECK CORRECT OPERATION · MECHANICAL OVERRIDE ... CHECK · * COCKPIT DOOR sw ... NORM · ECAM control panel: All selectors ... CHECK NORM · * THRUST levers ... IDLE · * THRUST REVERSER levers ... STOWED · * ENG MASTER levers ... CHECK OFF · * ENG START selector ... NORM · * ATC ... STBY · * TCAS ... STBY · ALT RPTG ... ON · * ATC SYS ... SELECT · ACARS: * MSG ... ERASE · * ADS ... CHECK ARMED', 'PF', False,
        'RMP 1 and 2 ... CHECK ON PF Green NAV light ... CHECK OFF PF COM FREQUENCIES ... TUNE PF', 'PRO-NOR-SOP-06-C-00011889.0001001'),
    fmc('FMS preparation · INIT A', '* IDLE / PERF FACTOR ... CHECK (DATA A/C STATUS) · INIT A: TO/FROM ... CHECK · ALTN ... ENTER · FLT NBR ... CHECK · COST INDEX ... CHECK · CRZ FL/TEMP ... CHECK · TROPO ... AS RQRD · WINDS ... CHECK · F-PLN: DEPARTURE RWY and SID ... ENTER · ENROUTE WAYPOINTS and AIRWAYS ... CHECK · STEP ALTS ... ENTER · ARRIVAL RWY/APPR and STAR ... ENTER · ETP WAYPOINT(S) ... CREATE · FIX INFO REFERENCE POINT(S) ... ENTER · EQUITIME POINT ... ADJUST · SECONDARY FLIGHT PLAN ... AS APPROPRIATE · RADIO NAV ... CHECK · INIT B: TAXI ... CHECK · RTE RSV / % ... ZERO · ALTN/TIME ... ENTER · FINAL/TIME ... CHECK · ZFW/ZFWCG ... ENTER (if not auto-populated) · BLOCK ... ENTER · EXTRA/TIME ... CHECK · PERF TAKE OFF: SHIFT ... INSERT AS RQRD · THR RED/ACC altitude ... SET or CHECK · ENG OUT ACC altitude ... SET or CHECK · PERF CLB and PERF CRZ: PRESEL speed ... AS RQRD · PERF DES: PRESEL speed ... SET · PROG: BRG / DIST TO ... ENTER · * RNP ... SET or CHECK · * DERATED CLIMB ... AS RQRD · * PRESET SPEEDS ... AS RQRD', 'PF',
        'Press the INIT button on the MCDU to display the INIT A page. Check the TO/FROM field [1R] to confirm the correct flight plan uplink occurred.',
        'PRO-NOR-SOP-06-D-90000090.9000245'),
    box('FMS PREPARATION * CROSSCHECK', 'departure route waypoints and constraints · flight plan vs computerized flight plan · initial cruise altitude · total track miles · fuel at destination · performance data · TRANS ALT · SEC F-PLN', 'PM', False,
        'The PM should have the same mental image of the intended departure procedure, trajectory, and constraints as the PF. The PM should check with the PF if anything is not clear.',
        'PRO-NOR-SOP-06-D-00015238.0001001'),
    box('Glareshield · EFIS control panel', '* LOUDSPEAKER knob ... SET · * BAROMETRIC REFERENCE ... SET/CROSSCHECK · * FD ... CHECK ON · * LS ... AS RQRD · * ND MODE and RANGE ... AS RQRD · * ADF/VOR sw ... AS RQRD · FCU: * SPD/MACH window ... DASHED · * HDG-V/S / TRK-FPA pb ... HDG-V/S · * ALT window ... INITIAL EXPECTED CLEARANCE ALTITUDE', 'B', False,
        'The maximum difference is: ±20 ft between both PFDs ±60 ft between ISIS and PFDs, 75 ft between PFDs and airport elevation (Refer to PRO-SPO-50 RVSM for more information).',
        'PRO-NOR-SOP-06-E-00020728.0001001'),
    box('Lateral consoles · OXYGEN MASK TEST PERFORM', 'ECAM DOOR/OXY SD: REGUL LO PR indication ... CHECK NOT DISPLAYED', 'B', False,
        'To prevent hearing damage to the ground crew connected to the intercom system, inform them that a loud noise may be heard in the headset when performing the oxygen mask test.',
        'PRO-NOR-SOP-06-00011910.0001001'),
    box('PFD and ND * CHECK', 'EFIS DMC selector ... CHECK NORM · PFD and ND brightness knob ... AS RQRD · PFD/ND not transferred · IAS, FMA, initial target ALT, altimeter, VSI, heading, attitude · ND heading, initial waypoint, VOR/ADF', 'B', False,
        '- Check IAS, FMA, initial target ALT, altimeter readings, VSI, altimeter settings, heading and attitude display.', 'PRO-NOR-SOP-06-00011911.0002001'),
    box('ECAM control panel', '* PRESS pb ... PRESS (CAB PRESS SD shows LDG ELEV AUTO) · * STS pb ... PRESS (INOP SYS compatible with MEL) · FUEL pb is the quick reference flow (FUEL SD for the FOB check); FCOM SOP-06 lists PRESS and STS', 'PF', False,
        'Check that the CAB PRESS SD page displays LDG ELEV AUTO to confirm correct position of the LDG ELEV knob.', 'PRO-NOR-SOP-06-00011885.0001001'),
    box('IRS ALIGN * CHECK', 'POSITION MONITOR: IRS in NAV, each IRS within 5 NM of FMS position · ND ROSE-NAV or ARC consistent with airport, SID, NAVAIDs', 'PM', False,
        'On the POSITION MONITOR page, check that the IRS are in NAV mode, and check that the distance between each IRS and the FMS position is lower than 5 NM.',
        'PRO-NOR-SOP-06-00011912.0001001'),
    box('RELEASE VERSION / FITNESS / FOB / PDSC ... SENT', 'via OPS CTRL MSG page in ACARS', 'PF', False,
        'Electronically accept latest flight release version fitness for duty, Fuel on Board and PDSC time via OPS CTRL MSG page in ACARS.', 'PRO-NOR-SOP-06-90000100.9000254'),
    box('FUEL ON BOARD * CHECK', 'ECAM FOB = block fuel of the computerized flight plan · FUEL SD: balanced, CG within limits', 'B', False,
        '- Check that ECAM FOB corresponds to the block fuel of the computerized flight plan - On FUEL SD page, check that the fuel is correctly balanced and CG is within operational limits.',
        'PRO-NOR-SOP-06-00024946.0001001'),
    box('ATC clearance CONFIRM', 'VHF, ACARS (PDC) or CPDLC (DCL)', 'PM', True,
        'Obtain ATC clearance via VHF, ACARS (PDC) or via CPDLC (DCL), Refer to PRO-SUP-46 Departure Clearance via CPDLC.', 'PRO-NOR-SOP-06-90000101.9000253'),
    box('DEPARTURE LEGS VERIFICATION PERFORM', 'FMS waypoints vs Dispatch Release, Jeppesen Charts, ATC clearance', 'B', False,
        'The Departure Legs Verification is designed to verify the FMS waypoints against the Dispatch Release, the Jeppesen Charts, and ATC Clearance (if available).',
        'PRO-NOR-SOP-06-90000102.9000255'),
    box('DEPARTURE BRIEFING * PERFORM', 'Threat Based Departure Briefing (FOM Threat Based Departure Briefing/TPC)', 'B', False,
        'Perform a Threat Based Departure Briefing. For more information, refer to FOM "Threat Based Departure Briefing/ TPC".', 'PRO-NOR-SOP-06-00011915.0001001'),
    cl('Cockpit Preparation', 'Departure Briefing complete'),
  ], 'FCOM PRO-NOR-SOP-06'),
  S('EXTERIOR LIGHTS · COCKPIT PREP', CYAN, [
    book('PF sets', 'Strobes AUTO · Nav 1 · All others OFF'),
    note('Lights table per the A330 quick reference (technique); switch states are the FCOM SOP lines quoted in each phase.'),
  ], 'quickref (technique)'),
]))

# ---------------------------------------------------------------- BEFORE PUSH
PH.append(P('before-push', 'Before Push', 'n', 'BEFORE PUSHBACK / START CLEARANCE', 'FCOM PRO-NOR-SOP-07', [
  S('LOAD CLOSEOUT · TAKEOFF DATA', PLUM, [
    fmc('ACARS PERF page ... SELECT “*LOAD FMC”', 'FMS uploads the ACARS final weight data and takeoff performance', 'PF',
        'The PF selects the “*LOAD FMC” prompt when it appears. This will allow the FMS to upload the ACARS final weight data and takeoff performance.',
        'PRO-NOR-SOP-07-A-00021319.9000330'),
    box('LOAD CLOSEOUT (LCO) CHECK', 'Flight number / date · Aircraft · Crew Count · TOF · TOW vs planned (MIN RLS FUEL adjustment?) · TOB · Jumpseat · ZFW/ZFWCG · NOTOC · AVI · FAM', 'B', False,
        'Both crew members carefully check the Load Closeout data is correct: - Flight number / date - Aircraft - Crew Count - Takeoff Fuel (“TOF”)',
        'PRO-NOR-SOP-07-A-00021319.9000330'),
    fmc('ZFW/ZFWCG CHECK/REVISE (PF, then PM)', 'green dot, F, S, VLS are computed from the entered ZFW and ZFWCG', 'B',
        'The characteristic speeds displayed on the MCDU (green dot, F, S, VLS) are computed from the ZFW and ZFWCG entered by the crew on the MCDU. Therefore, this data must be carefully checked before departure.',
        'PRO-NOR-SOP-07-A-00021319.9000330'),
    box('LOAD CLOSEOUT (MACTOW) CG and ECAM CG CHECK', 'difference less than 2 %: rely on ECAM CG · more than 2 %: check ZFW and ZFWCG in the MCDU, then rely on ECAM CG', 'B', False,
        'If there is more than 2 % difference, check that the ZFW and the ZFWCG have been correctly inserted in the MCDU, then rely on ECAM CG.', 'PRO-NOR-SOP-07-A-00021319.9000330'),
    box('LOAD CLOSEOUT VERBAL CROSS-CHECKS', 'CM2: PASSENGER & JUMPSEAT COUNT ... ANNOUNCE · CM1: JETPACK FLIGHT DECK REPORT ... VERIFY · CM2: FLIGHT NUMBER & TAIL NUMBER ... ANNOUNCE · CM1: DISPATCH RELEASE ... VERIFY · CM2: REMARKS ... ANNOUNCE (HAZMAT, pets in cargo) · count discrepancy: contact Central Load Planning', 'B', True,
        'Read out loud the passenger count and jumpseat numbers from the Load Closeout.', 'PRO-NOR-SOP-07-A-00021319.9000330'),
    box('MIN RLS FUEL CHECK', 'ECAM FOB above Minimum Release Fuel', 'B', False,
        'Check that ECAM FOB is above Minimum Release Fuel on the flight plan.', 'PRO-NOR-SOP-07-A-00011914.0001001'),
    fmc('TAKEOFF PERFORMANCE ... UPLINK FLX or UPLINK TOGA', 'FLAPS/THS reminder ... INSERT · manual entry: T.O SHIFT, V1 VR V2, FLX TO TEMP, THR RED/ACC, ENG OUT ACC', 'PF',
        'The PF uplinks the Takeoff Data into the FMS PERF TO page. The crew can select to uplink either FLX or TOGA takeoff data.',
        'PRO-NOR-SOP-07-A-00021320.0001001'),
    box('FINAL TAKEOFF DATA (TPR/TLR) CHECK · FMS TAKEOFF DATA CHECK/REVISE (PF, then PM)', 'Aircraft / Flight number / date · Wind / OAT / QNH · FINAL TPR (or TLR still valid) · Remarks · Takeoff Runway / Intersection · Engine Out Departure Procedure · Air Conditioning on/off · V speeds · Flap Config/THS · Flex / TOGA · GTOW vs MTOW · then each pilot compares the FMS takeoff data with the printed TPR/TLR (an uplink deletes THR RED / ACCEL ALT) · intersection: T.O SHIFT inserted', 'B', False,
        'Both crew members carefully check the Final Takeoff Performance Report (TPR/TLR) data is correct:',
        'PRO-NOR-SOP-07-A-00021320.0001001'),
    fmc('MCDU pages', 'PF: FMS PERF TO page ... SELECT · PM: FMS F-PLN page ... SELECT', 'B',
        'It is recommended to display the PERF TAKEOFF page on the PF side.', 'PRO-NOR-SOP-07-A-00011059.0001001'),
    box('SEATS, SEAT BELTS, HARNESSES, RUDDER PEDALS, ARMRESTS ... ADJUST', 'eyes aligned with the red and white balls', 'B', False,
        'The seat is correctly adjusted when the flight crew’s eyes are aligned with the red and white balls.', 'PRO-NOR-SOP-07-A-00011058.0001001'),
    box('PITOT COVERS REMOVED · AIR CONDITIONING UNITS CHECK DISCONNECTED · EXT PWR', 'EXT PWR pb ... CHECK AVAIL · EXT PWR DISCONNECTION ... REQUEST (before start if needed for pushback/start)', 'PF', False,
        'PITOT COVERS ... REMOVED PF', 'PRO-NOR-SOP-07-A-90000430.9000392'),
    box('PUSHBACK/START CLEARANCE OBTAIN', 'ATC pushback/start clearance and ground crew clearance', 'PM', True,
        'Obtain ATC pushback/start clearance and ground crew clearance.', 'PRO-NOR-SOP-07-B-00011040.0004001'),
  ], 'FCOM PRO-NOR-SOP-07'),
]))

# ---------------------------------------------------------------- BEFORE START
PH.append(P('before-start', 'Before Start', 'n', 'BEFORE START', 'FCOM PRO-NOR-SOP-07', [
  S('BEFORE START FLOW', PLUM, [
    trig('Push / start clearance received', 'B'),
    box('BEACON sw ON', '', 'PF', False, 'When cleared for start or pushback, set the BEACON sw to ON.', 'PRO-NOR-SOP-07-B-00011064.0001001'),
    box('ATC ... SET FOR OPERATION', '', 'PM', False, 'ATC is set in accordance with airport requirements.', 'PRO-NOR-SOP-07-B-00015355.0001001'),
    box('WINDOWS and DOORS CHECK CLOSED', 'sliding window handle fully forward, red indicator not visible · ECAM: all doors closed · cockpit door closed and locked', 'B', False,
        '- Check, on the ECAM lower display, that all the aircraft doors are closed - When required by FOM policies, check that the cockpit door is closed and locked (no cockpit door open/fault indication).',
        'PRO-NOR-SOP-07-B-00011063.0002001'),
    box('SLIDES CHECK ARMED', 'ECAM lower display', 'B', False,
        'Check, on the ECAM lower display, that all slides are armed.', 'PRO-NOR-SOP-07-B-00011063.0002001'),
    box('THRUST LEVERS IDLE', '', 'PF', False,
        'The engines start regardless of the thrust lever position. If the thrust levers are not set to IDLE, then thrust rapidly increases to the corresponding thrust lever position, causing a hazardous situation.',
        'PRO-NOR-SOP-07-B-00011065.0001001'),
    box('PARK BRK handle ON (if pushback not required)', 'ACCU PRESS indicator ... CHECK · BRAKES PRESS indicator ... CHECK', 'PF', False,
        'When one brake temperature is above 300 °C , avoid applying the parking brake, unless operationally necessary.', 'PRO-NOR-SOP-07-B-00011066.0002001'),
    box('Pushback required · PARK BRK handle ON · N/WS DISC MEMO CHECK DISPLAYED', 'tow pin in the tow position shows the N/WS DISC memo · no memo but pin confirmed: do not start engines during pushback', 'PF', False,
        'If the ECAM does not display the N/WS DISC memo, but the ground crew confirms that the tow pin is in the towing position, do not start the engines during pushback in order to avoid possible damage to the nose landing gear upon green hydraulic pressurization.',
        'PRO-NOR-SOP-07-B-00011062.0001001'),
    cl('Before Start', 'Before Start flow complete'),
    box('Pushback · PARK BRK handle OFF on ground crew clearance · no brakes during pushback', 'pushback complete: PARK BRK handle ... ON · BRAKE PRESS indicator ... CHECK · “CLEARED TO DISCONNECT” ... ANNOUNCE', 'PF', True,
        'The parking brake is released upon clearance from the ground crew. For the pushback procedure and communication script, refer to the FOM.', 'PRO-NOR-SOP-07-B-00011062.0001001'),
    note('CA becomes PF if both pilots not trained (quickref).'),
  ], 'FCOM PRO-NOR-SOP-07'),
  S('ENGINE START', TEAL, [
    box('THRUST levers IDLE · ENG START selector IGN START', 'lower ECAM shows the ENGINE SD page · engines start regardless of thrust lever position', 'PF', False,
        'ENG START selector ... IGN START PF', 'PRO-NOR-SOP-08-00011042.0019001'),
    box('PF: “ENGINE 1 START” · ENG 1 MASTER lever ON', 'engine 1 first: powers the blue hydraulic system (parking brake) · after all amber crosses and messages have disappeared on the engine parameters', 'PF', True,
        'Engine 1 is usually started first. It powers the blue hydraulic system, which pressurizes the parking brake.', 'PRO-NOR-SOP-08-00011042.0019001'),
    box('ENG IDLE PARAMETERS CHECK (AVAIL displayed)', 'ISA sea level: EPR about 1.015 · N1 about 22.6 % · N2 about 47 % · N3 about 63 % · EGT about 380 °C · FF about 1 800 lb/h', 'PF', False,
        'ENG IDLE PARAMETERS ... CHECK PF', 'PRO-NOR-SOP-08-00011042.0019001'),
    box('All engine taxi · PF: “ENGINE 2 START” · ENG 2 MASTER lever ON', 'same procedure as engine 1', 'PF', True,
        'Apply the same procedure as indicated for engine 1.', 'PRO-NOR-SOP-08-00011042.0019001'),
  ], 'FCOM PRO-NOR-SOP-08'),
]))

# ---------------------------------------------------------------- AFTER START
PH.append(P('after-start', 'After Start', 'n', 'AFTER START', 'FCOM PRO-NOR-SOP-09', [
  S('AFTER START FLOW', GREEN, [
    trig('PF sets ENG START selector to NORM', 'PF'),
    box('ENG START selector NORM', 'warm-up: idle at least 5 min cold (3 min warm) before high power', 'PF', False,
        'After start, to avoid thermal shock, the engine must be operated at idle, or near idle for at least 5 min when engines are cold (3 min when engines are warm after a stop of 1.5 h or less) before advancing the thrust lever to high power.',
        'PRO-NOR-SOP-09-A-00011043.0004001'),
    box('X BLEED selector AS RQRD', 'all engine taxi: AUTO · one engine taxi: OPEN to supply both packs with engine 1', 'PF', False,
        'For All Engine Taxi, the cross bleed valve remains in AUTO. For One Engine Taxi, open the cross bleed valve in order to supply both packs with engine 1.', 'PRO-NOR-SOP-09-A-C0000281.9001001'),
    box('GND SPLRS ARM', '', 'PM', False, 'GND SPLRS ... ARM PM', 'PRO-NOR-SOP-09-A-00011048.0001001'),
    box('APU BLEED pb-sw OFF', 'avoids ingestion of engine exhaust gases', 'PF', False,
        'This action enables to avoid ingestion of engine exhaust gases.', 'PRO-NOR-SOP-09-A-00011044.0001001'),
    box('RUD TRIM RESET pb PRESS · RUD TRIM CHECK NEUTRAL', 'up to 0.6° residual is normal', 'PM', False,
        'After the reset, the flight crew may observe an indication of up to 0.6 ° (L or R) in the RUD TRIM position indication.', 'PRO-NOR-SOP-09-A-00011049.0001001'),
    box('ENG 1 and 2 ANTI-ICE pb-sw AS RQRD', 'ON for all ground operations in icing conditions', 'PF', False,
        'Engine anti-ice must be set to ON during all ground operations, when icing conditions exist or are anticipated.', 'PRO-NOR-SOP-09-A-00011045.0003001'),
    box('FLAPS lever SET FOR TAKEOFF · FLAPS CHECK POSITION', 'icing with rain, slush or snow: keep flaps retracted until the holding point', 'PM', False,
        'Maintain the flaps retracted until the aircraft reaches the holding point of the takeoff runway. This action prevents contamination of the slats/flaps mechanism.',
        'PRO-NOR-SOP-09-A-00011050.0001001'),
    box('WING ANTI-ICE pb-sw AS RQRD', 'on ground the valves open about 30 s for the self-test, then close while on ground', 'PF', False,
        'On ground when wing anti-ice is switched on, the anti-ice valves open for about 30 s for self-test sequence, then close as long as the aircraft is on ground.', 'PRO-NOR-SOP-09-A-00011046.0001001'),
    box('APU MASTER SW pb-sw OFF (if not required)', '', 'PF', False, 'If the APU is not required: APU MASTER SW pb-sw ... OFF PF', 'PRO-NOR-SOP-09-A-00011047.0001001'),
    box('PITCH TRIM wheel CHECK', 'takeoff CG vs ECAM CG indication', 'PM', False,
        'Check the takeoff CG on the PITCH TRIM wheel using the CG indication on the ECAM.', 'PRO-NOR-SOP-09-A-00011051.0003001'),
    box('ECAM STATUS CHECK', 'PM checks, PF crosschecks: no STS reminder', 'B', False,
        'The PM checks and the PF crosschecks that there is no status reminder (STS) on the E/WD', 'PRO-NOR-SOP-09-A-00011054.0001001'),
    box('N/WS DISC MEMO CHECK NOT DISPLAYED', '', 'PF', False, 'N/WS DISC MEMO ... CHECK NOT DISPLAYED PF', 'PRO-NOR-SOP-09-A-00015237.0001001'),
    box('THRUST SETTING CROSSCHECK', 'E/WD FLEX temperature vs FMS PERF page', 'PF', False,
        'The PF crosschecks the thrust setting (e.g. FLEX temperature) displayed on the E/WD with the FMS PERF page.', 'PRO-NOR-SOP-09-A-00027845.0001001'),
    box('NWS TOWING FAULT LIGHT CHECK OFF', '', 'PF', False, 'NWS TOWING FAULT LIGHT ... CHECK OFF PF', 'PRO-NOR-SOP-09-A-00011052.0001001'),
    cl('After Start', 'salute received'),
  ], 'FCOM PRO-NOR-SOP-09'),
]))

# ---------------------------------------------------------------- TAXI
PH.append(P('taxi', 'Taxi', 'n', 'TAXI', 'FCOM PRO-NOR-SOP-10 · SCO', [
  S('DURING TAXI', RED, [
    box('TAXI clearance OBTAIN', 'PF: NOSE sw TAXI · RWY TURN OFF ON · PARK BRK handle OFF · BRAKES PRESSURE CHECK AT ZERO (slight residual pressure is normal for a short time)', 'PM', False,
        'The flight crew may observe slight residual pressure on the triple indicator for a short period of time.', 'PRO-NOR-SOP-10-A-00011943.0001001'),
    box('PF: “CLEAR LEFT (RIGHT)” · PM: “CLEAR RIGHT (LEFT)”', 'when taxi clearance obtained', 'B', True,
        'When taxi clearance obtained CLEAR LEFT (RIGHT) CLEAR RIGHT (LEFT)', 'PRO-NOR-SCO-D-00011845.0001001'),
    box('PF: “BRAKE CHECK”', 'BRAKE PEDALS ... PRESS · BRAKES ... CHECK · PM: BRAKE FAN AS RQRD · BRAKES PRESSURE ... CHECK AT ZERO', 'PF', True,
        'If the aircraft was parked in wet conditions for a long time, the first brake application at low speed is less effective.', 'PRO-NOR-SOP-10-A-00011946.0002001'),
    box('PF: “FLIGHT CONTROL CHECK”', 'PM: “FULL UP, FULL DOWN, NEUTRAL” · “FULL LEFT, FULL RIGHT, NEUTRAL” · PF: “RUDDER” PM: “FULL LEFT, FULL RIGHT, NEUTRAL” (PM follows pedals with feet)', 'B', True,
        'Check the flight controls at a convenient stage, before or during taxi.', 'PRO-NOR-SOP-10-A-00011948.0001001'),
    box('ATC clearance CONFIRM', 'review before checking the AFS/Flight Instruments', 'PM', False,
        'Review the ATC clearance before checking the AFS/Flight Instruments', 'PRO-NOR-SOP-10-A-00011949.0001001'),
    box('AFS / flight instruments', 'CLEARED ALTITUDE ON FCU ... CHECK · HDG ON FCU ... IF REQUIRED, PRESET · BOTH FD ... CHECK ON · PFD/ND ... CHECK (both): airspeeds, initial target altitude, heading, FMA modes, ND SID per the departure', 'PM', False,
        'If a heading is required by ATC after takeoff, in the case of a radar vector departure, preset the heading on the FCU. NAV mode will be disarmed.', 'PRO-NOR-SOP-10-A-00015138.0001001'),
  ], 'FCOM PRO-NOR-SOP-10 · SCO-D'),
  S('TAXI FLOW', GOLD, [
    trig('AFS / flight instruments checked', 'B'),
    box('TERR ON ND AS RQRD', 'radar on the PF side, TERR ON ND on the PM side', 'B', False,
        'Consider selecting the radar display on the PF side, and TERR ON ND on the PM side only.', 'PRO-NOR-SOP-10-A-00011953.0001001'),
    box('AUTO BRK MAX pb-sw ON', '', 'PM', False, 'AUTO BRK MAX pb-sw ... ON PM', 'PRO-NOR-SOP-10-A-00011954.0001001'),
    box('ATC CODE/MODE CONFIRM/SET FOR TAKEOFF', '', 'PM', False, 'ATC CODE/MODE ... CONFIRM/SET FOR TAKEOFF PM', 'PRO-NOR-SOP-10-A-00011952.0001001'),
    box('ENG START selector AS RQRD', 'IGN/START: heavy rain, moderate or severe turbulence expected after takeoff', 'PM', False,
        'Select IGN/START if: - Heavy rain, or - Moderate turbulence, or - Severe turbulence is expected after takeoff.', 'PRO-NOR-SOP-10-A-00012083.0002001'),
    box('WXR/PWS sw SYS 1(2) · CAPT and F/O DISPLAY ALL', '30 s to fill the radar 3D buffer', 'PM', False,
        '30 s are necessary for the 3D buffer of the radar to be filled.', 'PRO-NOR-SOP-10-A-00015141.0004001'),
    box('T.O CONFIG pb TEST', 'EWD displays T.O CONFIG NORMAL memo', 'PM', False,
        'Press the T.O CONFIG on the ECP, and check that the EWD displays the T.O CONFIG NORMAL memo.', 'PRO-NOR-SOP-10-A-00011956.0001001'),
    box('T.O MEMO CHECK NO BLUE', '', 'PM', False,
        'Check that the EWD does not display any blue line in the T.O memo section.', 'PRO-NOR-SOP-10-A-00011956.0001001'),
    box('Cabin NA/ADVISED · PM PA: “[FLIGHT ATTENDANTS SHOULD NOW] BE SEATED FOR TAKEOFF”', 'no less than two minutes prior to takeoff', 'PM', True,
        'On Pax aircraft, The PM will make the Takeoff PA no less than two minutes prior to takeoff stating "[FLIGHT ATTENDANTS SHOULD NOW] BE SEATED FOR TAKEOFF".',
        'PRO-NOR-SOP-10-A-00011956.0001001'),
    cl('Taxi', 'T.O CONFIG pb pressed and Takeoff Advisory PA complete'),
  ], 'FCOM PRO-NOR-SOP-10'),
  S('DEPARTURE CHANGE (runway, SID or configuration)', PLUM, [
    box('FINAL TAKEOFF PERF DATA RECOMPUTE', 'Aerodata inputs (runway and environmental) correct · new TPR: gross weight into PTOW (LSK 5R) of the AOC TO Conditions page, then SEND (LSK 6R)', 'PM', False,
        'The PM ensures the Aerodata inputs (runway and environmental) are correct and if required, sends for a new TPR.', 'PRO-NOR-SOP-10B-00011950.0001001'),
    fmc('FMS REVISE', 'takeoff data, runway and/or SID · ATC clearance agrees with the FMS if NAV mode is used · any slats/flaps configuration change', 'PM',
        'The PM revises the FMS as necessary, including the takeoff data, runway and/or SID, as applicable.', 'PRO-NOR-SOP-10B-00011950.0001001'),
    fmc('REVISED FMS CROSSCHECK', 'TPR/TLR performance data vs the FMS PERF page', 'PF',
        'The PF crosschecks the revised FMS, as applicable. The PF checks the TPR/TLR performance data with the FMS PERF page.', 'PRO-NOR-SOP-10B-00011950.0001001'),
    box('FLAPS lever SET · FCU ALT SET · T.O CONFIG pb TEST', 'takeoff position · cleared altitude crosschecked on the PFD · EWD shows T.O CONFIG NORMAL', 'PM', False,
        'On the PFD, crosscheck and confirm the cleared altitude.', 'PRO-NOR-SOP-10B-00011950.0001001'),
    box('RE-BRIEFING PERFORM', '', 'B', False, 'RE-BRIEFING ... PERFORM BOTH', 'PRO-NOR-SOP-10B-00011950.0001001'),
    cl('Departure Change', 'revised departure briefing completed'),
  ], 'FCOM PRO-NOR-SOP-10B'),
  S('EXTERIOR LIGHTS · TAXI', CYAN, [
    book('PF (or PM at PF request)', 'Taxi: Nose TAXI · Rwy Turnoff ON · Crossing a runway: Strobes ON · Land ON'),
    box('Crossing a runway', 'STROBE sw ... ON · LAND LIGHT sw ... ON', 'PF', False,
        'When crossing a runway: STROBE sw ... ON PF LAND LIGHT sw ... ON PF', 'PRO-NOR-SOP-21-A-00011013.0001001'),
  ], 'FCOM PRO-NOR-SOP-21 · quickref'),
]))

# ---------------------------------------------------------------- LINE-UP / TAKEOFF
PH.append(P('before-takeoff', 'Line-Up / Takeoff', 'n', 'LINE-UP / TAKEOFF', 'FCOM PRO-NOR-SOP-11 / SOP-12 · SCO', [
  S('LINE-UP FLOW', BLUE, [
    trig('Line-up clearance received', 'B'),
    box('TAKEOFF RUNWAY CONFIRM', 'runway markings · runway lights · ILS signal (LOC centered after line up) · runway symbol on the ND · RAAS', 'B', False,
        'Confirm that the line up is performed on the intended runway and from the intended intersection.', 'PRO-NOR-SOP-11-A-00012077.0001001'),
    box('TCAS Mode selector TA or TA/RA', 'TA/RA is the default; TA ONLY only at airports/procedures identified by Jeppesen 10-7 pages', 'PM', False,
        'The flight crew should use the TA/RA mode as the default mode of the TCAS.', 'PRO-NOR-SOP-11-A-00012069.0001001'),
    box('APPROACH PATH CLEAR OF TRAFFIC', 'visually and on the TCAS display', 'B', False,
        'Check that the approach path is clear of traffic, visually and using TCAS display on ND.', 'PRO-NOR-SOP-11-A-00012070.0001001'),
    box('STROBE sw ON', 'PF may request the PM to set the exterior lights', 'PF', False,
        'Set the STROBE sw to ON to cross or enter a runway. The PF can request the PM to set the exterior lights.', 'PRO-NOR-SOP-11-A-00021962.0001001'),
    box('PACK 1 and PACK 2 pb-sw AS RQRD', 'packs OFF at least 20 s before takeoff thrust · APU bleed not permitted with wing anti-ice · APU bleed ON at least 20 s before takeoff thrust', 'PM', False,
        'If a takeoff is performed with the packs OFF : The packs must be set to OFF at least 20 s before applying takeoff thrust.', 'PRO-NOR-SOP-11-A-00012073.0001001'),
    box('RNP AR departure · GPS 1+2 on GPS MONITOR page CHECK BOTH IN NAV · GPS PRIMARY on PROG page CHECK AVAILABLE', '', 'PM', False,
        'GPS 1+2 on GPS MONITOR page ... CHECK BOTH IN NAV PM GPS PRIMARY on PROG page ... CHECK AVAILABLE PM', 'PRO-NOR-SOP-11-A-00012081.0001001'),
    box('FMA CHECK', 'verify NAV is armed', 'B', False, 'Verify NAV is armed.', 'PRO-NOR-SOP-11-A-00012081.0001001'),
    box('SLIDING TABLE STOW · ALL EFB (with no mounted equipment) STOW', '', 'B', False,
        'SLIDING TABLE ... STOW PF-PM ALL EFB (with no mounted equipment) ... STOW PF-PM', 'PRO-NOR-SOP-11-A-00012079.0001001'),
    cl('Line-Up', 'line-up flow complete'),
    note('Resume normal tasksharing if both pilots not trained (quickref).'),
  ], 'FCOM PRO-NOR-SOP-11'),
  S('TAKEOFF', RED, [
    box('TAKEOFF CLEARANCE OBTAIN', '', 'PM', False, 'TAKEOFF CLEARANCE ... OBTAIN PM', 'PRO-NOR-SOP-12-A-00021964.0001001'),
    box('NOSE sw T.O · LAND sw ON', '', 'PF', False, 'NOSE sw ... T.O PF LAND sw ... ON PF', 'PRO-NOR-SOP-12-A-00021963.0001001'),
    box('PF: “TAKEOFF” · THRUST 1.1 EPR', 'crosswind at or below 20 kt, no tailwind: SIDESTICK HALF FORWARD · tailwind or crosswind above 20 kt: SIDESTICK FULL FORWARD · BRAKES RELEASE · THRUST LEVERS FLX or TOGA', 'PF', True,
        'Once the thrust levers are set to FLX or TOGA detent, the Captain maintains the hand on the thrust levers, until the aircraft reaches V1.', 'PRO-NOR-SOP-12-A-00012071.0016001'),
    box('CHRONO START · PFD/ND MONITOR', 'PF: DIRECTIONAL CONTROL ... USE RUDDER', 'PM', False,
        'If GPS PRIMARY LOST, check on the ND the FMS position: i.e. that the aircraft is on the runway centerline.', 'PRO-NOR-SOP-12-A-00012071.0016001'),
    box('Below 80 kt · PM: “THRUST SET”', 'TAKEOFF THRUST ... CHECK (N1/EPR at rating limit, EGT) · PFD and ENG indications ... MONITOR', 'PM', True,
        'Check that the actual N1/EPR of the individual engines has reached the N1/EPR rating limit, before the aircraft reaches 80 kt. Check EGT.', 'PRO-NOR-SOP-12-A-00012072.0001001'),
    box('At 80 kt · SIDESTICK RELEASE', 'neutral at 100 kt', 'PF', False,
        'Release the sidestick gradually to reach neutral at 100 kt.', 'PRO-NOR-SOP-12-A-00025004.0001001'),
    box('At 100 kt · PM: “ONE HUNDRED KNOTS” · PF: “CHECKED”', 'below 100 kt the Captain may abort depending on circumstances · above 100 kt rejecting is a more serious matter', 'B', True,
        '• Below 100 kt, the Captain may decide to abort the takeoff, depending on the circumstances • Above 100 kt, rejecting the takeoff is a more serious matter.', 'PRO-NOR-SOP-12-A-00012074.0001001'),
    box('At V1 · PM: “V1” (monitor or announce)', 'monitor the synthetic voice; announce if not triggered', 'PM', True,
        'Monitor that the “V1” synthetic voice is triggered when reaching V1. If not, announce “V1”.', 'PRO-NOR-SOP-12-A-00012076.0002001'),
    box('At VR · PM: “ROTATE”', 'PF: continuous rotation about 3°/s toward 15° (12.5° one engine failed) · after lift-off follow SRS', 'B', True,
        '- At VR, initiate the rotation with a positive sidestick input to achieve a continuous rotation rate of about 3 °/s, towards a pitch attitude of 15 ° (12.5 °, if one engine is failed)', 'PRO-NOR-SOP-12-A-00012078.0001001'),
    box('PM: “POSITIVE RATE” · PF: “GEAR UP” · PM: “GEAR UP”', 'L/G lever SELECT UP · AP AS RQRD (above 100 ft AGL) · AP must be engaged for RNP AR below 0.3 NM', 'B', True,
        'Announce “Positive Rate” when the radio height is increasing, and a positive rate of climb is indicated on the altimeter and/or the vertical speed indicator.', 'PRO-NOR-SOP-12-A-00012080.0003001'),
    box('PF: “AP 1(2) ON” (if AP engaged by PM)', 'above 100 ft AGL AP 1 or AP 2 may be engaged', 'PF', True,
        'Above 100 ft AGL, AP 1 or AP 2 may be engaged. The AP must be engaged for RNP AR < 0.3 NM.', 'PRO-NOR-SOP-12-A-00012080.0003001'),
    box('At thrust reduction altitude · THRUST LEVERS CL', 'when LVR CLB flashes · PM: PACK 1 ON after CLB thrust, PACK 2 ON at least 10 s later', 'PF', False,
        'Move the thrust levers to the CL detent, when the flashing LVR CLB prompt appears on the FMA. Autothrust is now active.', 'PRO-NOR-SOP-12-A-00012084.0001001'),
  ], 'FCOM PRO-NOR-SOP-12 · SCO-D'),
  S('EXTERIOR LIGHTS · TAKEOFF', CYAN, [
    book('PF (or PM at PF request)', 'Line up and wait: Strobes ON · Cleared for takeoff: Nose T.O. · Land ON'),
  ], 'FCOM PRO-NOR-SOP-12 · quickref'),
]))

# ---------------------------------------------------------------- AFTER TAKEOFF / CLIMB
PH.append(P('after-takeoff', 'After T/O / Climb', 'n', 'AFTER TAKEOFF / CLIMB', 'FCOM PRO-NOR-SOP-12 / 13 / 14', [
  S('ACCELERATION FLOW', GREEN, [
    trig('Above acceleration altitude (or once in climb phase)', 'B'),
    box('At F speed · PF: “FLAPS 1” · PM: FLAPS 1 SELECT', 'PM: “SPEED CHECKED, FLAPS ONE” after checking the blue number on the ECAM flaps indicator', 'B', True,
        'At F speed FLAPS 1 ... ORDER PF FLAPS 1 ... SELECT PM', 'PRO-NOR-SOP-12-A-00012091.0001001'),
    box('At S speed · PF: “FLAPS 0” · PM: FLAPS 0 SELECT', '', 'B', True,
        'At S speed FLAPS 0 ... ORDER PF FLAPS 0 ... SELECT PM', 'PRO-NOR-SOP-12-A-00012091.0001001'),
    box('GND SPLRS DISARM · L/G CHECK UP · NOSE sw OFF · RWY TURN OFF sw OFF', '', 'PM', False,
        'GND SPLRS ... DISARM PM L/G ... CHECK UP PM NOSE sw ... OFF PM RWY TURN OFF sw ... OFF PM', 'PRO-NOR-SOP-12-A-00012091.0001001'),
  ], 'FCOM PRO-NOR-SOP-12'),
  S('AFTER TAKEOFF', TEAL, [
    box('APU BLEED OFF · APU MASTER SW OFF (if APU supplied air for takeoff)', '', 'PM', False,
        'If the APU was used to supply the air conditioning during takeoff: APU BLEED pb-sw ... OFF PM APU MASTER SW pb-sw ... OFF PM', 'PRO-NOR-SOP-13-A-00010470.0001001'),
    box('ENG START selector AS RQRD', 'IGN/START in severe turbulence or heavy rain', 'PM', False,
        'Select IGN/START, if severe turbulence or heavy rain is encountered.', 'PRO-NOR-SOP-13-A-00010471.0001001'),
    box('TCAS mode selector TA/RA (if takeoff was TA only)', '', 'PM', False,
        'If the takeoff was performed with TA only: TCAS mode selector ... TA/RA PM', 'PRO-NOR-SOP-13-A-00010472.0001001'),
    box('ENG 1 and 2 ANTI ICE AS RQRD · WING ANTI ICE AS RQRD', 'engine anti-ice ON in icing conditions except climb/cruise with SAT below -40 °C', 'PM', False,
        'Engine anti-ice must be set to ON when icing conditions exist or are anticipated, except during climb and cruise when the SAT is below -40 °C (-40 °F).', 'PRO-NOR-SOP-13-A-00010560.0001001'),
  ], 'FCOM PRO-NOR-SOP-13'),
  S('CLIMB', CYAN, [
    fmc('PF MCDU PERF CLB · PM MCDU F-PLN', 'PROG page shows OPT FL and MAX REC FL (0.3 g buffet margin)', 'B',
        'PM MCDU should be showing the F-PLN page (allowing PM to enter any ATC long-term revisions to the lateral or vertical flight plan).', 'PRO-NOR-SOP-14-A-00012131.0001001'),
    fmc('CRZ FL SET AS RQRD', 'if ATC limits cruise below INIT A CRZ FL, insert the lower CRZ FL on PROG page or there is no CRZ phase transition', 'PF',
        'If the ATC limits the CRZ FL to a lower level than the one entered in the INIT A page (or present on the PROG page), the flight crew must insert this lower CRZ FL in the PROG page.', 'PRO-NOR-SOP-14-A-00024912.0001001'),
    box('CLIMB SPEED MODIFICATIONS AS RQRD · RADAR ADJUST AS APPROPRIATE', '', 'PF', False,
        'RADAR ... ADJUST AS APPROPRIATE PF', 'PRO-NOR-SOP-14-A-00012134.0002001'),
    box('Within 1 000 ft of clearance altitude · PF: “[leaving] for [cleared]” · PM: “CHECKED”', 'e.g. “23 for 24”', 'B', True,
        '', ''),
    box('At transition altitude · PF: “SET STANDARD” · PM: “STANDARD CROSS-CHECKED, PASSING FL __ NOW” · PF: “CHECKED”', 'BAROMETRIC REFERENCE ... SET STD/CROSSCHECK', 'B', True,
        '- At the transition altitude, the barometric setting flashes on the PFD. The flight crew should set STD on the EFIS CP and on the standby altimeter.', 'PRO-NOR-SOP-14-A-00024910.0001001'),
  ], 'FCOM PRO-NOR-SOP-14 · SCO'),
  S('CLIMBING 10 000 FT FLOW', PURP, [
    trig('Climbing 10 000 ft MSL', 'B'),
    box('EFIS option: PF CSTR · PM ARPT', '', 'B', False,
        'EFIS Option: The PF will select CSTR The PM will select ARPT', 'PRO-NOR-SOP-14-A-00019949.0001001'),
    box('LAND sw OFF', '', 'PM', False, 'AT 10 000 FT MSL LAND sw ... OFF PM', 'PRO-NOR-SOP-14-A-00012135.0001001'),
    box('NO SMOKING sw ON, wait 3 s, AUTO', 'informs additional occupants of leaving sterile', 'PM', False,
        'Cycle the NO SMOKING sw ON, wait three seconds, then back to AUTO to inform any additional aircraft occupants of leaving sterile, if required.', 'PRO-NOR-SOP-14-A-00012135.0001001'),
    box('ECAM MEMO REVIEW · NAVAIDS CLEAR · SEC F-PLN AS RQRD · OPT FL/REC MAX FL CHECK', 'clear manually tuned VORs from RAD NAV', 'PM', False,
        'Clear manually tuned VORs from RAD NAV page.', 'PRO-NOR-SOP-14-A-00012135.0001001'),
    box('STARLINK * AS RQRD', 'ON passing 10 000 ft AAL when departing a station that does not allow its use', 'PM', False,
        "When departing a destination that does not allow its use, Starlink shall be selected 'ON', passing 10 000 ft AAL.", 'PRO-NOR-SOP-14-A-C0000114.9001001'),
    box('SEAT BELTS sw AS RQRD (after 18 000 ft)', 'first time OFF after takeoff: Seat Belt Advisory PA per FOM', 'PM', False,
        "When the seat belt sign is turned off for the first time after takeoff, Flight crews are required to make a 'Seat Belt Advisory' PA in accordance with FOM policy.", 'PRO-NOR-SOP-14-A-C0000235.9001001'),
  ], 'FCOM PRO-NOR-SOP-14'),
]))
# the altitude callout has its own quote from SCO
PH[-1]['sections'][2]['items'][2].update({'quote': 'When approaching within 1 000 ft of the clearance altitude, the PF will state, for example, "23 for 24" and the PM will calls out "CHECKED".', 'ref': 'PRO-NOR-SCO-00011833.0001001'})

# ---------------------------------------------------------------- CRUISE
PH.append(P('cruise', 'Cruise', 'n', 'CRUISE', 'FCOM PRO-NOR-SOP-15', [
  S('CRUISE', CYAN, [
    note('In cruise, the tasksharing is left to the flight crew appreciation (FCOM).'),
    box('ECAM MEMO REVIEW · SD PAGES REVIEW', 'ENG oil press/temp · BLEED · ELEC GEN loads · HYD quantity · COND duct temps · F/CTL surface positions · FUEL distribution, trim tank, CG · DOOR oxygen pressure', 'B', False,
        'Periodically review the system display pages and, in particular, monitor the following:', 'PRO-NOR-SOP-15-A-00011070.0002001'),
    box('FLIGHT PROGRESS CHECK', 'manually entered waypoint: track/distance to next, wind · every waypoint or at least every 60 min: FUEL check (FOB vs prediction vs CFP · no leak · FOB + FU = departure FOB)', 'B', False,
        'WHEN OVERFLYING A WAYPOINT, OR AT LEAST EVERY 60 MIN Check FUEL: - Check FOB (ECAM) and fuel prediction (FMGEC), and compare with the computerized flight plan - Check that there is no fuel leak', 'PRO-NOR-SOP-15-A-00011071.0001001'),
    box('Fuel leak suspicion', 'FOB + FUEL USED vs departure: abnormally negative = suspect a leak · abnormally positive = suspect overread · check before any FUEL IMBALANCE procedure', 'B', False,
        'This check must also be performed each time a FUEL IMBALANCE procedure is necessary. Perform the check before applying the FUEL IMBALANCE procedure. If a fuel leak is confirmed, apply the FUEL LEAK procedure.', 'PRO-NOR-SOP-15-A-00011071.0001001'),
    box('STEP FLIGHT LEVEL AS APPROPRIATE', '', 'B', False, 'STEP FLIGHT LEVEL ... AS APPROPRIATE PF-PM', 'PRO-NOR-SOP-15-A-00011072.0001001'),
    box('NAVIGATION ACCURACY MONITOR (if GPS PRIMARY LOST)', 'FMS PROGRESS page vs flown airspace', 'B', False,
        'Check on FMS PROGRESS page that the required navigation accuracy is appropriate according to the flown airspace. For more information, Refer to PRO SPO 51 PBN.', 'PRO-NOR-SOP-15-A-00011073.0001001'),
    box('RADAR ADJUST AS APPROPRIATE', '', 'PF', False, 'RADAR ... ADJUST AS APPROPRIATE PF', 'PRO-NOR-SOP-15-A-00011074.0002001'),
    box('OXYGEN MASK CHECK (if used)', 'properly stowed', 'B', False,
        'Check that the oxygen mask has been properly stowed (Refer to DSC-35-10 Description).', 'PRO-NOR-SOP-15-A-00011076.0001001'),
  ], 'FCOM PRO-NOR-SOP-15'),
  S('CALLOUTS · ALL PHASES', NAVY, [
    box('Any FMA change · PF announces · PM: “CHECKED”', 'armed modes with colour (G/S blue, LOC blue), active modes without colour (NAV, ALT)', 'B', True,
        'The PM should check and respond, "CHECKED" to all FMA changes called out by the PF.', 'PRO-NOR-SCO-00011832.0001001'),
    box('Flap selection · PF: “FLAPS ONE” · PM: “SPEED CHECKED, FLAPS ONE”', 'PM checks the blue number on the ECAM flaps indicator', 'B', True,
        'PM selects the FLAPS lever position and replies after checking the blue number on the ECAM flaps indicator to confirm the correct selection has been made.', 'PRO-NOR-SCO-B-00011834.0001001'),
    box('Gear selection · PF: “GEAR UP (DOWN)” · PM: “GEAR UP (DOWN)”', 'PM checks the red lights on the LDG GEAR indicator', 'B', True,
        'The PM selects the L/G lever position and replies after checking the red lights on the LDG GEAR indicator to confirm gear operation.', 'PRO-NOR-SCO-B-00011835.0001001'),
    box('Transfer of control · “YOU HAVE CONTROL” · “I HAVE CONTROL”', '', 'B', True,
        'To give control : The pilot calls out "YOU HAVE CONTROL". The other pilot accepts this transfer by calling out "I HAVE CONTROL", before assuming PF duties.', 'PRO-NOR-SCO-00011838.0001001'),
    box('Parking brake moved · “PARKING BRAKE SET / RELEASED”', 'whichever pilot operates it verbalizes its movement', 'B', True,
        'The flight crew member operating the parking brake must always verbalize its movement so that all flight crew are aware of its status.', 'PRO-NOR-SCO-90000106.9000259'),
    box('Checklist complete · “__ CHECKLIST COMPLETE”', 'interruption: “HOLD CHECKLIST AT ___” then “RESUME CHECKLIST AT ___”', 'B', True,
        'If a checklist needs to be interrupted, announce : “HOLD CHECKLIST AT ___” and “RESUME CHECKLIST AT ___” for the continuation. Upon completion of a checklist announce : “__CHECKLIST COMPLETE”.',
        'PRO-NOR-SCO-00011826.0001001'),
  ], 'FCOM PRO-NOR-SCO'),
]))

# ---------------------------------------------------------------- DESCENT
PH.append(P('descent', 'Descent', 'n', 'DESCENT PREPARATION / DESCENT', 'FCOM PRO-NOR-SOP-16 / SOP-17', [
  S('DESCENT PREPARATION', PURP, [
    box('WEATHER AND LANDING INFORMATION OBTAIN', 'destination and alternate weather, runway conditions · low OAT: altitude corrections · JEPPESEN CHARTS ... PREPARE (all)', 'PM', False,
        'Check the weather reports and runway conditions at destination and alternate airports. Airfield data, if any, should include the runway to be used for arrival.', 'PRO-NOR-SOP-16-A-00021323.0002001'),
    box('BAROMETRIC REFERENCE PRESET', 'preset the QNH on the ISIS', 'PM', False, 'Preset the QNH on the ISIS.', 'PRO-NOR-SOP-16-A-00026519.0002001'),
    box('ECAM STATUS CHECK', 'landing capability degradation, anything affecting approach and landing', 'PM', False,
        '- Check the ECAM status page before completing the approach checks. Take particular note of any degradation in landing capability, or any other aspect affecting the approach and landing.', 'PRO-NOR-SOP-16-A-00011973.0001001'),
    box('LANDING PERFORMANCE CHECK', 'request via ACARS · system failure not on the release: Flysmart landing distance · conditions changed: PM (RE)COMPUTE, PF CROSSCHECK · REV MAX is standard', 'PM', False,
        'Request Landing Performance data via ACARS. For any system failure not listed on the dispatch release which affects landing performance a landing distance calculation must be computed using Flysmart.', 'PRO-NOR-SOP-16-A-00013713.0001001'),
    fmc('FMS · ARRIVAL page COMPLETE/CHECK · F-PLN A page CHECK', 'APPR, STAR, TRANS, APPR VIA · approach and missed approach vs charts (ND PLAN) · speed and altitude constraints · do not modify the final approach · identify FDP and MAP', 'PF',
        '- In all cases, do not modify the final approach (FAF to runway or MAP), including altitude constraints', 'PRO-NOR-SOP-16-A-00020071.0001001'),
    fmc('RADIO NAV page CHECK · SELECTED NAVAIDS CHECK/MODIFY', 'ILS frequency and course · VOR/DME near the field in PROG BRG/DIST for NAV accuracy', 'PF',
        '- For an ILS approach, check the frequency and course', 'PRO-NOR-SOP-16-A-00020074.0002001'),
    fmc('DES WIND · PERF CRUISE · PERF DES CHECK', 'descent winds from cruise FL · cabin descent rate · MANAGED MACH/SPD; 250 kt below 10 000 ft default', 'PF',
        'A speed limit of 250 kt below 10 000 ft is the defaulted speed in the managed speed descent profile. The flight crew may delete or modify it if necessary on the VERT REV at DEST page.', 'PRO-NOR-SOP-16-A-00020072.0001001'),
    fmc('PERF APPR page COMPLETE/CHECK · PERF GO AROUND CHECK/MODIFY', 'guidance mode FLS or FINAL APP · QNH, temperature, average wind (no gust) · minimum · landing CONF FULL or CONF 3 · transition altitude · THR RED ALT and ACC ALT', 'PF',
        'Insert the average wind given by the ATC or ATIS. Do not insert the gust value. During approach, the Ground Speed Mini function (managed speed mode) takes into account the instantaneous gust.', 'PRO-NOR-SOP-16-A-00020073.0012001'),
    fmc('FUEL PRED CHECK · PROG CONSIDER · SEC F-PLN AS RQRD', 'EFOB destination, alternate, extra · BRG/DIST reference for energy management · SEC F-PLN to an alternative runway or circling runway before T/D', 'PF',
        'The SEC F-PLN should be set before the top of descent, either to an alternative runway for destination, or to the landing runway in case of circling. In all cases, the routing to the alternate should be available.', 'PRO-NOR-SOP-16-A-00020076.0002001'),
    box('FMS PREPARATION CROSSCHECK', 'PM checks all data entered by the PF, same mental image of arrival and approach', 'PM', False,
        'After the PF prepares the FMS, the PM checks all the data entered in the FMS. The PM should have the same mental image of the intended arrival and approach procedure, trajectory, and constraints than the PF.', 'PRO-NOR-SOP-16-A-00023628.0001001'),
    box('LDG ELEV CHECK', 'LDG ELEV AUTO on the CRUISE page and its value', 'PF', False,
        'Check that the LDG ELEV AUTO is displayed on the CRUISE page, and check the associated value.', 'PRO-NOR-SOP-16-A-00015234.0001001'),
    box('AUTO BRK AS RQRD', 'MAX not recommended at landing · short or contaminated: MED · long runways: LO', 'PF', False,
        'Use of MAX mode is not recommended at landing. On short or contaminated runways, use MED mode. On long runways, LO mode is recommended', 'PRO-NOR-SOP-16-A-00012251.0001001'),
    box('ARRIVAL LEGS VERIFICATION', 'PF reads from the ND (PLAN, CSTR, F-PLN) · PM verifies against the Jeppesen charts · repeat if the routing changes', 'B', False,
        'The PF reads from the “glass” (ND), and the PM verifies against the “paper” (Jeppesen Charts).', 'PRO-NOR-SOP-16-A-90000104.9000258'),
    box('APPROACH BRIEFING PERFORM', 'Threat Based Approach Briefing (FOM Threat Based Arrival Briefing/TPC)', 'B', False,
        'Perform a Threat Based Approach Briefing. For more information, refer to FOM "Threat Based Arrival Briefing/TPC".', 'PRO-NOR-SOP-16-A-00012249.0001001'),
    box('RADAR ADJUST AS APPROPRIATE', '', 'PF', False, 'RADAR ... ADJUST AS APPROPRIATE PF', 'PRO-NOR-SOP-16-A-00012253.0002001'),
    box('ENG 1 and 2 ANTI ICE AS RQRD · WING ANTI ICE AS RQRD', 'engine anti-ice ON before and during descent even below -40 °C SAT · ANTI ICE ON reduces the idle descent path angle', 'PM', False,
        'Engine anti-ice must be set to ON before and during descent, even if the SAT is below -40 °C (-40 °F).', 'PRO-NOR-SOP-16-A-00012253.0002001'),
    box('DESCENT CLEARANCE OBTAIN · CLEARED ALTITUDE ON FCU SET', 'PM obtains · PF sets, respecting safe altitudes', 'B', False,
        'When the flight crew obtains the ATC clearance, they should set the cleared altitude (FL) on the FCU taking into account the safe altitudes.', 'PRO-NOR-SOP-16-A-00012252.0001001'),
  ], 'FCOM PRO-NOR-SOP-16'),
  S('DESCENT', TEAL, [
    box('DESCENT INITIATE', 'DES mode at the FMS T/D · early descent: DES mode (V/S about 1 000 ft/min) · delayed: reduce toward green dot with ATC permission', 'PF', False,
        'The standard method to initiate the descent is to engage the DES mode at the Top of Descent (T/D) computed by the FMS.', 'PRO-NOR-SOP-17-00011965.0001001'),
    fmc('PF MCDU PROG/PERF DES · PM MCDU F-PLN', 'monitor VERT DEV and the level-off symbol · FPA (°) = ΔFL / DIST (NM)', 'B',
        '- From time to time during stabilized descent, the flight crew may select FPA to check that the remaining distance to destination is approximately the altitude change required divided by the FPA in degrees.', 'PRO-NOR-SOP-17-00011966.0001001'),
    box('RATE OF DESCENT ADJUST, AS RQRD', 'increase speed before speed brakes · in DES mode on or below path do not use speed brakes; use OP DES with speed brakes', 'PF', False,
        'In the DES mode, if the aircraft is on, or below the flight path and the ATC requires a higher rate of descent, do not use the speed brakes because the rate of descent is imposed by the planned flight path.', 'PRO-NOR-SOP-17-A-00011967.0001001'),
    box('TERR ON ND AS RQRD', 'mountainous areas · radar PF side, TERR PM side · not with NAV ACCURACY LOW', 'B', False,
        '- If NAV ACCURACY is LOW, do not use the TERR on ND.', 'PRO-NOR-SOP-17-A-00011971.0001001'),
    box('SEAT BELTS sw ON', 'no later than 18 000 ft on descent (or T/D if cruising lower)', 'PM', False,
        'No later than 18 000 ft on descent (or at top of descent if cruising at lower altitude), turn the Seatbelt Sign ON.', 'PRO-NOR-SOP-17-A-90000464.9000393'),
    box('CABIN PA · PM: “[Flight Attendants], please prepare the cabin for arrival and be seated for landing.”', 'no later than approximately 18 000 ft MSL · near T/D on short segments · when Early Sit Procedures are used', 'PM', True,
        '"[Flight Attendants], please prepare the cabin for arrival and be seated for landing."', 'PRO-NOR-SOP-17-A-C0000234.9001001'),
    box('At transition level · BAROMETRIC REFERENCE SET/CROSSCHECK', 'PF: “SET QNH” · PM: “QNH CROSS-CHECKED, PASSING __ FT NOW” · PF: “CHECKED” · also update the PERF APPR QNH', 'B', True,
        'The flight crew must take into account any QNH change on the EFIS control panels, standby altimeter and on the FMS PERF APPR page.', 'PRO-NOR-SOP-17-A-00011970.0002001'),
    box('STARLINK * AS RQRD', 'OFF approaching 10 000 ft AAL when the destination does not allow its use', 'PM', False,
        "When approaching a destination that does not allow its use, Starlink shall be selected 'OFF', approaching 10 000 ft AAL.", 'PRO-NOR-SOP-17-A-C0000115.9001001'),
  ], 'FCOM PRO-NOR-SOP-17'),
  S('DESCENDING 10 000 FT FLOW', BLUE, [
    trig('Descending 10 000 ft AAL', 'B'),
    box('LAND sw ON · SEAT BELTS sw ON · NO SMOKING sw ON, wait 3 sec, AUTO', '', 'PM', False,
        'AT 10 000 FT AAL LAND sw ... ON PM SEAT BELTS sw ... ON PM NO SMOKING sw ... ON, wait 3 sec, AUTO PM', 'PRO-NOR-SOP-17-A-00011974.0002001'),
    box('EFIS option pb CSTR (both sides)', '', 'B', False, 'Select CSTR on both sides.', 'PRO-NOR-SOP-17-A-00011974.0002001'),
    box('LS pb AS RQRD', 'ILS, GLS · ILS G/S out, LOC only, LOC B/C · FLS · SLS · check deviation scales and IDENT on the PFD', 'B', False,
        'The flight crew checks that: - Deviation scales are displayed on the PFD - The IDENT is properly displayed on the PFD.', 'PRO-NOR-SOP-17-A-00011974.0002001'),
    box('NAVAIDS AS RQRD/CHECK', 'tuned and identified', 'PF', False,
        'Ensure that the appropriate navaids are tuned and identified.', 'PRO-NOR-SOP-17-A-00011974.0002001'),
    box('ENG START selector AS RQRD', 'IGN: standing water on the runway, heavy rain or severe turbulence in the approach or go-around area', 'PM', False,
        'Select IGN if the runway is covered with standing water, or if heavy rain or severe turbulence is expected during approach or go-around area.', 'PRO-NOR-SOP-17-A-00015239.0001001'),
    box('NAVIGATION ACCURACY MONITOR (if GPS PRIMARY LOST)', '', 'PF', False,
        'If GPS PRIMARY LOST: NAVIGATION ACCURACY ... MONITOR PF', 'PRO-NOR-SOP-17-A-00015240.0001001'),
    cl('Approach', 'below 10 000 ft AAL and baro ref set'),
    note('At taxi speed CA becomes PF if both pilots not trained (quickref).'),
  ], 'FCOM PRO-NOR-SOP-17'),
]))

# ---------------------------------------------------------------- APPROACH
PH.append(P('approach', 'Approach', 'n', 'APPROACH · CONFIGURATION', 'FCOM PRO-NOR-SOP-18-B · SCO', [
  S('INITIAL APPROACH', BLUE, [
    fmc('F-PLN SEQUENCING ADJUST', 'TO waypoint on the ND must remain meaningful · NAV sequences automatically · HDG/TRK only when close to the route', 'PF',
        '- A good clue to monitor the proper F-PLN sequencing is the TO waypoint on the upper right side of the ND, which should remain meaningful', 'PRO-NOR-SOP-18-B-A-00014475.0001001'),
    box('APPROACH PHASE CHECK/ACTIVATE · PF: “ACTIVATE APPROACH PHASE” · PM: “APPROACH PHASE ACTIVATED”', 'automatic at DECEL in NAV · in HDG/TRK activate about 15 NM from touchdown on PERF DES', 'B', True,
        '- If the aircraft is in HDG or TRK mode, approximately 15 NM from touchdown activate and confirm APPR phase on the PERF DES page.', 'PRO-NOR-SOP-18-B-A-00014475.0001001'),
    box('MANAGED SPEED CHECK · FLIGHT PATH MONITOR', 'ATC speed: selected, then back to managed · NAV: V/DEV · HDG/TRK: energy circle on the ND', 'PF', False,
        '- In HDG or TRK mode, use the energy circle on ND representing the required distance to land.', 'PRO-NOR-SOP-18-B-A-00014475.0001001'),
    box('SPEED BRAKES lever AS RQRD', 'VLS increases with speed brakes; ensure speed margin before extension and before a turn (Alpha-Floor)', 'PF', False,
        '• If the speed brakes are extended, the flight crew should ensure that appropriate speed margin exists before the beginning of a turn.', 'PRO-NOR-SOP-18-B-A-00014475.0001001'),
    box('PM: “RADIO ALTIMETER ALIVE” · PF: “CHECKED”', 'keep RA in scan to landing', 'PM', True,
        'Flight crew awareness, flight crew should now keep RA in scan to landing.', 'PRO-NOR-SCO-D-00011849.0005001'),
  ], 'FCOM PRO-NOR-SOP-18-B-A'),
  S('INTERMEDIATE / FINAL · CONFIGURATION (DECELERATED)', GREEN, [
    box('At green dot · PF: “FLAPS 1” · PM: FLAPS 1 SELECT', 'more than 3 NM before the FDP · established with FLAPS 1 and S speed at or above 2 500 ft AGL · TCAS TA or TA/RA', 'B', True,
        '- For decelerated approaches, the aircraft must reach or be established on the final descent with FLAPS 1 and S speed at or above 2 500 ft AGL', 'PRO-NOR-SOP-18-B-B-00014480.0001001'),
    box('At 2 500 ft AGL minimum · PF: “FLAPS 2” · PM: FLAPS 2 SELECT', 'intercept below 2 500 ft AGL (2 000 minimum): FLAPS 2 at one dot below the path · high speed: extend the gear, speed brakes not recommended', 'B', True,
        '- For ILS, GLS , SLS , FLS , if the aircraft intercepts the flight path below 2 500 ft AGL (2 000 ft AGL minimum), select FLAPS 2 at one dot below the flight path', 'PRO-NOR-SOP-18-B-B-00014481.0001001'),
    box('When flaps at 2 · PF: “GEAR DOWN” · PM: L/G lever SELECT DOWN', 'AUTO BRK CONFIRM · GROUND SPOILERS ARM · cleared for approach: NOSE TAXI, RWY TURN OFF ON · cleared to land: NOSE T.O', 'B', True,
        'If the runway conditions have changed from the arrival briefing, consider another braking mode.', 'PRO-NOR-SOP-18-B-B-00014482.0001001'),
    box('When gear is down · PF: “FLAPS 3” · PM: FLAPS 3 SELECT', 'ECAM WHEEL SD CHECK: three green, at least one green triangle per strut, LDG GEAR DN memo', 'B', True,
        '- Check for three green indications on the landing gear indicator panel. At least one green triangle on each landing gear strut on the WHEEL SD page is sufficient to indicate that the landing gear is downlocked.', 'PRO-NOR-SOP-18-B-B-00014483.0006001'),
    box('PF: “FLAPS FULL” · PM: FLAPS FULL SELECT', 'decelerates to VAPP · correct TO waypoint on the ND', 'B', True,
        '- Check that the aircraft decelerates to VAPP - Check correct TO waypoint on the ND.', 'PRO-NOR-SOP-18-B-B-00014483.0006001'),
    box('A/THR CHECK IN SPEED MODE OR OFF · WING ANTI ICE OFF · SLIDING TABLE STOW · LDG MEMO CHECK NO BLUE', 'wing anti-ice ON only in severe icing', 'PM', False,
        'Switch the WING ANTI ICE pb-sw ON, only in severe icing conditions.', 'PRO-NOR-SOP-18-B-B-00014483.0006001'),
    cl('Landing', 'LDG CONF set', True),
    box('FLIGHT PARAMETERS MONITOR', 'PM calls: speed below target -5 kt or above +10 kt · pitch below 0° or above +10° · bank more than 7° · descent rate more than 1 000 ft/min', 'PM', False,
        '• The speed goes lower than the speed target -5 kt, or more than the speed target +10 kt • The pitch attitude goes lower than 0 °, or more than +10 ° nose up • The bank angle becomes more than 7 ° • The descent rate becomes more than 1 000 ft/min.', 'PRO-NOR-SOP-18-B-B-00014483.0006001'),
    note('Selected speed if not managed: S after FLAPS 1, F after FLAPS 2, VAPP after LDG FLAPS. Extend flaps at VFE -15 kt when possible.'),
  ], 'FCOM PRO-NOR-SOP-18-B-B'),
  S('STABILIZATION GATES · CALLOUTS', RED, [
    box('Stabilized approach', 'correct lateral and vertical path · landing configuration · thrust stabilized above idle at target speed · no excessive deviation', 'B', False,
        'If one of the above-mentioned conditions is not satisfied, the flight crew must initiate a go-around, unless they estimate that only small corrections are required to recover stabilized approach conditions.', 'PRO-NOR-SOP-18-A-00014471.0001001'),
    box('FAF · PM: “(Fix), (PFD altitude), (altimeter setting), CHECKED” · PF: “CHECKED”', 'criteria not met: PM “UNSTABLE, GO AROUND” · PF “GO AROUND - FLAPS”', 'B', True,
        'FAF (Fix name)_____, (PFD altitude)_____, (altimeter setting)_____, CHECKED', 'PRO-NOR-SCO-D-00011849.0005001'),
    box('1 000 ft AFE (stabilized gate) · PF: “STABLE” · PM: “CHECKED”', 'out of limits: PF “CORRECTING SPEED / VERTICAL SPEED” · config not met: PF “UNSTABLE, GO AROUND - FLAPS” (PM calls it if PF does not)', 'B', True,
        '1 000 ft AFE (Stabilized Gate)(6) If 1 000 ft configuration criteria are met: STABLE', 'PRO-NOR-SCO-D-00011849.0005001'),
    box('500 ft AFE (go-around gate) · PM: “STABLE” · PF: “CHECKED”', 'not met: PM “UNSTABLE, GO AROUND” · PF “GO AROUND - FLAPS”', 'B', True,
        '500 ft AFE (Go-Around Gate)(6) If 500 ft criteria are met: STABLE', 'PRO-NOR-SCO-D-00011849.0005001'),
    box('Deviation callouts (PM) · PF: “CORRECTING”', '“SPEED” +10/-5 kt · “SINK RATE” more than 1 000 ft/min below 1 000 ft · “ALTITUDE” · “LOC” / “GLIDESLOPE” 1/2 dot · “COURSE” · “TRACK” 0.1 NM · “V DEV” 1/2 dot · “LAT DEV” · PAPI', 'B', True,
        '', ''),
  ], 'FCOM PRO-NOR-SOP-18-A · SCO-D'),
]))
PH[-1]['sections'][2]['items'][4].update({'quote': 'The PM calls out if excessive deviation occurs: - LOC: ½ dot - G/S: ½ dot.', 'ref': 'PRO-NOR-SOP-18-C-A-00014490.0001001'})

# ---------------------------------------------------------------- FINAL / LANDING (approach-type toggles live here)
PH.append(P('landing', 'Final / Landing', 'n', 'FINAL APPROACH / LANDING', 'FCOM PRO-NOR-SOP-18-C / SOP-19 · SCO', [
  S('ILS · LOC G/S GUIDANCE', RED, [
    box('APPR pb on FCU PRESS · PF: “ARM APPROACH”', 'when cleared, on the intercept trajectory, LOC deviation available · arms LOC and G/S · capture no sooner than 3 s after arming', 'PF', True,
        '- Press the APPR pb when all of the following is applicable: • The aircraft is cleared for the approach • The aircraft is on the intercept trajectory for the final approach course • LOC deviation is available on the PFD.', 'PRO-NOR-SOP-18-C-A-00014488.0001001'),
    box('BOTH APs ENGAGE', 'above 5 000 ft AGL FMA shows CAT 1 · below 5 000 ft AGL the actual capability', 'PF', False,
        '- When APPR mode is selected, AP1 and AP2 should be engaged - Above 5 000 ft AGL, the FMA displays CAT 1 - Below 5 000 ft AGL, the FMA displays the correct approach capability for the intended approach.', 'PRO-NOR-SOP-18-C-A-00014488.0001001'),
    box('LOC CHECK ARMED · G/S CHECK ARMED · LOC CAPTURE MONITOR · G/S CAPTURE MONITOR', 'PF announces FMA: “LOC blue”, “G/S blue”, “LOC*”, “G/S*”', 'PF', True,
        'LOC ... CHECK ARMED PF G/S ... CHECK ARMED PF LOC CAPTURE ... MONITOR PF G/S CAPTURE ... MONITOR PF', 'PRO-NOR-SOP-18-C-A-00014488.0001001'),
    box('GO-AROUND ALTITUDE SET · PF: “SET GA ALTITUDE __ FT” · PM: “GA ALTITUDE SET”', 'at G/S*, or PF sets: “GA ALTITUDE SET” · PM: “CHECKED”', 'B', True,
        'GO-AROUND ALTITUDE ... SET BOTH', 'PRO-NOR-SOP-18-C-A-00014488.0001001'),
    box('Glide interception from above', 'established on the LOC · gear down, at least CONF 2 · APPR ARM/CHECK ARMED · LOC CHECK ENGAGED · FCU ALTITUDE SET ABOVE A/C ALTITUDE · V/S MODE SELECT (1 500 ft/min initially)', 'PF', False,
        'Select V/S 1 500 ft/min initially. V/S in excess of 2 000 ft/min will result in the speed increasing towards VFE.', 'PRO-NOR-SOP-18-C-A-00014489.0001001'),
    box('FLIGHT PARAMETERS MONITOR · PM: “LOC” / “GLIDESLOPE” at 1/2 dot', '', 'PM', True,
        'The PM calls out if excessive deviation occurs: - LOC: ½ dot - G/S: ½ dot.', 'PRO-NOR-SOP-18-C-A-00014490.0001001'),
    box('At 350 ft RA · LAND mode CHECK ENGAGED/ANNOUNCE', 'no LAND mode: autoland not authorized', 'PF', True,
        'If no LAND mode, autoland is not authorized.', 'PRO-NOR-SOP-18-C-A-00014490.0001001'),
    box('Entered minimum +100 ft · PM: “ONE HUNDRED ABOVE” · PF: “CHECKED”', '', 'PM', True,
        'AT ENTERED MINIMUM +100 ft ONE HUNDRED ABOVE ... MONITOR OR ANNOUNCE PM', 'PRO-NOR-SOP-18-C-A-00014490.0001001'),
    box('At minimum · PM: “MINIMUM” · PF: “CONTINUE” (AP AS RQRD) or “GO-AROUND”', 'below minimum visual references are the primary reference until landing', 'B', True,
        'Below minimum, the visual references must be the primary reference until landing.', 'PRO-NOR-SOP-18-C-A-00014490.0001001'),
  ], 'FCOM PRO-NOR-SOP-18-C-A', 'ILS'),
  S('CAT II / CAT III', VIOLET, [
    box('APPROACH MINIMUM DETERMINE', 'lowest achievable minimum: crew qualification · Operating Manual · aircraft status · airport status · CAT III no DH: enter NO in the DH field', 'PF', False,
        '- For CAT III with no DH, the flight crew should enter NO in the DH field of the MCDU to avoid false "HUNDRED ABOVE" or "MINIMUM" auto callouts which would not be applicable.', 'PRO-NOR-SOP-18-C-A-00020760.0001001'),
    box('APPROACH BRIEFING PERFORM', 'task sharing and callouts · management of degraded guidance · low visibility procedures at the airport', 'B', False,
        'For CAT II, CAT III, approaches, review the following items on top of the usual briefing: - Task sharing and callouts - Management of degraded guidance - Low visibility procedures at the airport.', 'PRO-NOR-SOP-18-C-A-00020760.0001001'),
    box('LAND on FMA (350 ft RA) · PF: “LAND” · PM: “CHECKED”', '', 'B', True,
        'LAND on FMA (350’ RA) "LAND" "CHECKED"', 'PRO-NOR-SCO-D-00011849.0005001'),
    box('CAT II · DA(H) +100 ft · PM: “100 ABOVE” · PF: “CHECKED”', 'DA(H): PM “MINIMUM” · PF “CONTINUE” or “GO AROUND, FLAPS”', 'B', True,
        'DA(H) + 100’ “CHECKED” "100 ABOVE"(1) DA(H) “CONTINUE”, or "MINIMUM"(1) “GO AROUND, FLAPS”', 'PRO-NOR-SCO-D-00011849.0005001'),
    box('CAT III · 200 ft RA (alert height) · PM: “ALERT” · PF: “CONTINUE” or “GO AROUND, FLAPS”', 'no failure at 200 ft', 'B', True,
        'At 200 ft (Alert Height) if no failure ALERT ... ANNOUNCE PM CONTINUE ... ANNOUNCE PF', 'PRO-NOR-SOP-18-C-A-00014490.0001001'),
    box('40 ft RA · PM: “FLARE” or “NO FLARE” · Rollout · PM: “ROLLOUT”', 'no FLARE on the FMA: go-around, or manual landing if visual references are sufficient', 'PM', True,
        'If the FMA does not display FLARE, perform a go-around, or a manual landing if visual references are sufficient.', 'PRO-NOR-SOP-19-B-00020777.0001001'),
    box('Degraded guidance above 1 000 ft AGL', 'ECAM/QRH PROCEDURE COMPLETE · APPROACH AND LANDING CAPABILITY CHECK · REQUIRED EQUIPMENT CHECK · RVR CHECK, DH ADJUST, briefing UPDATE · not complete at 1 000 ft: GO-AROUND', 'B', False,
        'If the flight crew does not complete all the above actions at 1 000 ft: GO-AROUND ... PERFORM PF', 'PRO-NOR-SOP-18-C-A-00020959.0002001'),
    box('Degraded guidance below 1 000 ft AGL · GO-AROUND PERFORM', 'below 200 ft CAT3 DUAL: continue unless AUTOLAND warning · AUTOLAND warning: GO-AROUND', 'PF', False,
        'Below 200 ft (Alert Height) for CAT3 DUAL : The automatic approach may be continued unless the AUTOLAND warning is triggered.', 'PRO-NOR-SOP-18-C-A-00020959.0002001'),
  ], 'FCOM PRO-NOR-SOP-18-C-A · SCO-D', 'ILScat'),
  S('AUTOLAND', TEAL, [
    box('At 350 ft RA · LAND on FMA CHECK/ANNOUNCE · ILS COURSE on PFD CHECK', 'course pointer vs runway track more than 5°: go-around or manual landing', 'PF', True,
        'If the ILS course pointer and the runway track differ by more than 5 °, perform a go-around, or a manual landing if visual references are sufficient.', 'PRO-NOR-SOP-19-B-00020776.9000364'),
    box('At 40 ft RA · FLARE on FMA CHECK/ANNOUNCE · FLARE MONITOR', '', 'PM', True,
        'AT 40 FT RA FLARE ON FMA ... CHECK/ANNOUNCE PM', 'PRO-NOR-SOP-19-B-00020777.0001001'),
    box('At 30 ft RA · THR IDLE on FMA CHECK · THRUST IDLE CHECK', '', 'PM', False,
        'AT 30 FT RA THR IDLE ON FMA ... CHECK PM THRUST IDLE ... CHECK PM', 'PRO-NOR-SOP-19-B-00020786.0001001'),
    box('At 10 ft RA · automatic “RETARD” · ALL THRUST LEVERS IDLE', 'autothrust disconnects · monitor lateral guidance with external references', 'PF', False,
        'Monitor the lateral guidance by using external references.', 'PRO-NOR-SOP-19-B-00020778.0001001'),
    box('At touchdown · ROLL OUT on FMA CHECK/ANNOUNCE · reversers · GND SPLRS · DECEL', 'NWS or anti-skid failure: AP OFF at touchdown', 'PM', True,
        'In the case of NWS or Anti-Skid failure, set the AP OFF at touchdown.', 'PRO-NOR-SOP-19-B-00020779.0015001'),
    box('End of roll out · ALL REVERSER LEVERS STOW · AP OFF', 'before leaving the runway at the latest', 'PF', False,
        'Disengage the APs at the end of the roll out (before leaving the runway at the latest).', 'PRO-NOR-SOP-19-B-00020784.0001001'),
  ], 'FCOM PRO-NOR-SOP-19-B', 'ILS'),
  S('RNP APCH · FLS (F-LOC F-G/S) GUIDANCE', BROWN, [
    note('RNAV(GNSS) with LNAV or LNAV/VNAV minima, VOR/NDB overlay, LOC only, ILS G/S OUT, LOC B/C. FLS is the recommended mode; RNP AR uses FINAL APP.'),
    fmc('PERF APPR page CHECK/SELECT FLS · FLS DATA CHECK', 'anchor point · F-LOC course · F-G/S slope vs chart · F-PLN: 0.1° vertical, 1° lateral tolerance', 'B',
        '- 0.1 degree of difference between the MCDU and the charted final vertical path is acceptable - 1 degree of difference between the MCDU and the charted final lateral track is acceptable', 'PRO-NOR-SOP-18-C-B-00014495.0003001'),
    box('At 10 000 ft AAL · FLS CAPABILITY CHECK (F-APP for RNAV(GNSS)) · BARO SET/CROSSCHECK', 'maximum altimeter difference 100 ft', 'B', False,
        'The vertical guidance requires a precise BARO setting. The maximum acceptable difference between altimeters is 100 ft.', 'PRO-NOR-SOP-18-C-B-00014496.0002001'),
    box('APPR pb on FCU PRESS · PF: “ARM APPROACH”', 'cleared and on the intercept trajectory · arms F-LOC and F-G/S · F-LOC CHECK ARMED · F-G/S CHECK ARMED · capture MONITOR', 'PF', True,
        'Press the APPR pb when all of the following is applicable: - The aircraft is cleared for approach - The aircraft is on the intercept trajectory for the final approach course. This arms the F-LOC and F-G/S modes.', 'PRO-NOR-SOP-18-C-B-00014497.0002001'),
    box('GO-AROUND ALTITUDE SET', 'on the FCU', 'B', True, 'Set the go-around altitude on the FCU.', 'PRO-NOR-SOP-18-C-B-00014497.0002001'),
    box('FLIGHT PARAMETERS MONITOR', 'altitude at FAF vs chart · F-APP + RAW: monitor raw data · PM calls F-LOC or F-G/S 1/2 dot', 'PM', False,
        '- Check altitude crossing at FAF as published on the chart', 'PRO-NOR-SOP-18-C-B-00014499.0002001'),
    box('At minimum · PM: “MINIMUM” · PF: “CONTINUE” · AP OFF when appropriate · FD AS RQRD', 'below 150 ft RA with AP engaged: DISCONNECT AP FOR LDG pulses', 'B', True,
        '- Below 150 ft RA, if the AP is still engaged, the message DISCONNECT AP FOR LDG pulses on the FMA to remind the flight crew that automatic landing is not available.', 'PRO-NOR-SOP-18-C-B-00014500.0005001'),
    box('Degraded navigation (LNAV / LNAV-VNAV)', 'discontinue if F-APP lost · F-LOC more than 1 dot · NAV FM/GPS POS DISAGREE · LNAV/VNAV: F-G/S more than 1/2 dot below the beam', 'B', False,
        '- Discontinue the approach if the F-G/S deviation exceeds ½ dot below the F-G/S beam.', 'PRO-NOR-SOP-18-C-B-00014501.0002001'),
  ], 'FCOM PRO-NOR-SOP-18-C-B', 'RNP'),
  S('RNP APCH · FINAL APP GUIDANCE (incl. RNP AR)', PLUM, [
    fmc('PERF APPR page SELECT FINAL APP · PROG page RNP (RNP AR)', 'not when OAT below chart minimum · remote QNH prohibited · TOO STEEP PATH after the FDP: do not use FINAL APP', 'B',
        '- If a TOO STEEP PATH is displayed after the FDP, do not use FINAL APP guidance for approach. Use NAV FPA, TRK FPA or FLS for approach', 'PRO-NOR-SOP-18-C-C-00014514.0005001'),
    box('At 10 000 ft AAL · NAV ACCURACY CHECK · GPS PRIMARY CHECK · BARO SET/CROSSCHECK', 'RNP AR: GPS PRIMARY on both FMS, both GPS in NAV or SBAS, TERR ON ND both sides', 'B', False,
        '- Both GPS and both FMS must be available, before the IAF. Therefore, if one FMS is inoperative or if one GPS is not in NAV or SBAS before the IAF, RNAV(RNP) is not permitted.', 'PRO-NOR-SOP-18-C-D-00014547.0002001'),
    box('APPR pb on FCU PRESS · APP NAV CHECK ARMED or ENGAGED · FINAL CHECK ARMED', 'cleared and TO waypoint is the FDP · VDEV scale on the PFD · blue arrow on the ND at the FDP', 'PF', True,
        'Press the APPR pb when all of the following conditions are satisfied: - The aircraft is cleared for approach - TO waypoint is the FDP.', 'PRO-NOR-SOP-18-C-C-00014516.0002001'),
    box('At the FDP · FINAL APP CHECK ENGAGED · GO-AROUND ALTITUDE SET', 'RNP below 0.3 NM: one AP engaged', 'B', True,
        'At Final Descent Point: FINAL APP ... CHECK ENGAGED PF GO-AROUND ALTITUDE ... SET BOTH', 'PRO-NOR-SOP-18-C-C-00014516.0002001'),
    box('FLIGHT PARAMETERS MONITOR · PM: “TRACK” XTK more than 0.1 NM · “V DEV” 1/2 dot (50 ft)', 'RNP AR: “LAT DEV” at 1/2 dot · go-around at XTK 1 RNP or V/DEV 3/4 dot below (75 ft)', 'PM', True,
        '- Go-around must be initiated if excessive deviation occurs: • XTK reaches 1 RNP • V/DEV reaches ¾ dot below the vertical profile.', 'PRO-NOR-SOP-18-C-D-00014548.0006001'),
    box('At minimum · PM: “MINIMUM” · PF: “CONTINUE” · AP OFF at the MAP or AP minimum use height (whichever first) · FD AS RQRD', 'after the MAP disregard the FD (reverts to HDG V/S)', 'B', True,
        '- After the MAP, disregard the FD as it reverts to HDG V/S.', 'PRO-NOR-SOP-18-C-C-00014517.0013001'),
    box('Degraded navigation (LNAV / LNAV-VNAV)', 'discontinue: GPS PRIMARY LOST both NDs · XTK more than 0.3 NM · NAV FM/GPS POS DISAGREE · NAV ACCUR DOWNGRAD both · LNAV/VNAV: 75 ft below path (V/DEV more than 3/4 dot)', 'B', False,
        '- Discontinue the approach in the case of deviation of 75 ft below the vertical path (V/DEV > ¾ dot).', 'PRO-NOR-SOP-18-C-C-00014518.0002001'),
  ], 'FCOM PRO-NOR-SOP-18-C-C / 18-C-D', 'RNP'),
  S('NON-PRECISION · FPA GUIDANCE', OCEAN, [
    note('RNAV(GNSS) LNAV with NAV FPA, LP with LOC FPA, VOR/NDB with TRK FPA or NAV FPA, LOC only, ILS G/S OUT, LOC B/C. TRK FPA when not in the database or NAV accuracy LOW.'),
    box('At 10 000 ft AAL · NAV ACCURACY CHECK · GPS PRIMARY CHECK · BARO SET/CROSSCHECK', 'NAV accuracy LOW: TRK mode for the approach', 'B', False,
        'If NAV accuracy is LOW, use TRK mode for approach.', 'PRO-NOR-SOP-18-C-E-00014530.0002001'),
    box('LATERAL GUIDANCE MODE SET FOR APPROACH', 'arm NAV, LOC or LOC B/C · LOC only / G/S OUT / B/C / LP: LOC pb-sw PRESS when cleared, on intercept, LOC deviation available · LATERAL PATH INTERCEPT', 'PF', False,
        'Press the LOC pb-sw when: - Cleared for the approach - On the intercept trajectory for the final approach course - LOC deviation is available.', 'PRO-NOR-SOP-18-C-E-00014531.0001001'),
    box('TRK-FPA pb (Bird) SELECT · FPA FOR FINAL APPROACH SET', 'PF: “BIRD ON” · “FPA MINUS 3° PULL” at 0.3 NM before the FDP', 'PF', True,
        'At 0.3 NM from the Final Descent Point: FPA selector ... PULL PF', 'PRO-NOR-SOP-18-C-E-00014531.0001001'),
    box('POSITION/FLIGHT PATH MONITOR/ADJUST · GO-AROUND ALTITUDE SET (when below it)', '', 'B', True,
        'Set when below the go-around altitude to avoid not expected altitude capture.', 'PRO-NOR-SOP-18-C-E-00014531.0001001'),
    box('FLIGHT PARAMETERS MONITOR', 'distance vs altitude per chart · raw data on conventional NAVAIDs · PM calls: NAV XTK more than 0.1 NM · LOC 1/2 dot · TRK VOR 1/2 dot or 2.5° · NDB 5°', 'PM', False,
        '• Approach using TRK mode: ▪ VOR: ½ dot or 2.5 ° ▪ NDB: 5 °.', 'PRO-NOR-SOP-18-C-E-00014531.0001001'),
    box('At minimum · PM: “MINIMUM” · PF: “CONTINUE” · AP OFF · FD OFF · RUNWAY TRACK CHECK/SET', 'PF orders the PM to set both FDs off and the runway track', 'B', True,
        'The PF orders the PM to set both FDs off.', 'PRO-NOR-SOP-18-C-E-00014532.0007001'),
  ], 'FCOM PRO-NOR-SOP-18-C-E', 'NPA'),
  S('DISCONTINUED APPROACH', SLATE, [
    box('PF: “CANCEL APPROACH” (at or above the FCU altitude)', 'press APPR pb or LOC pb to disarm · lateral mode NAV or HDG · vertical mode · SPEED · below the FCU altitude: GO AROUND procedure', 'PF', True,
        'When the aircraft is below the FCU altitude, the flight crew must apply the GO AROUND procedure.', 'PRO-NOR-SOP-18-A-00015153.0001001'),
  ], 'FCOM PRO-NOR-SOP-18-A'),
  S('LANDING · MANUAL', GREEN, [
    box('AP OFF (manual landing)', '', 'PF', False, 'FOR MANUAL LANDING AP ... OFF PF', 'PRO-NOR-SOP-19-A-00024894.0001001'),
    box('Around 40 ft RA · FLARE PERFORM · ALL THRUST LEVERS IDLE', 'PM: ATTITUDE MONITOR · automatic “RETARD” at 20 ft is a reminder · ground spoilers inhibited with a lever above IDLE', 'PF', False,
        'Move the thrust levers to the IDLE detent, and begin a gentle progressive flare to enable the aircraft to touch down without a prolonged float.', 'PRO-NOR-SOP-19-A-00012003.0022001'),
    box('At touchdown · DEROTATION INITIATE · ALL REVERSER LEVERS REV MAX or REV IDLE', 'reverse immediately after main gear touchdown = full-stop landing · REV MAX: emergency, decel not as expected, failure, long flare, tailwind', 'PF', False,
        'The flight crew must select reverse thrust immediately after main landing gear touchdown.', 'PRO-NOR-SOP-19-A-00012004.0014001'),
    box('PM: “SPOILERS” (or “NO SPOILERS”)', 'no spoilers: thrust levers IDLE detent, both reversers MAX REV, brake pedals fully pressed', 'PM', True,
        '- If no ground spoilers are extended: • Check that all thrust levers are set to IDLE detent • Set both thrust reverser levers to MAX REV, and fully press the brake pedals.', 'PRO-NOR-SOP-19-A-00012004.0014001'),
    box('PM: “REVERSE GREEN” (or “NO REVERSE ENGINE _” / “NO REVERSE”)', '', 'PM', True,
        '- If reverser(s) do not deploy as expected, one of the main deceleration means is lost. The flight crew should consider adapting the available deceleration means to stop the aircraft.', 'PRO-NOR-SOP-19-A-00012004.0014001'),
    box('DIRECTIONAL CONTROL ENSURE', 'rudder pedals · no sidestick inputs · directional problem: REV IDLE · no tiller before taxi speed', 'PF', False,
        '- During rollout, avoid sidestick inputs (either lateral or longitudinal)', 'PRO-NOR-SOP-19-A-00012004.0014001'),
    box('AUTO BRK CHECK/ANNOUNCE · AUTOBRAKE MONITOR', 'BRK LO or BRK MED on the FMA · PM: “AUTOBRAKE OFF” if it disengages · PF: “MANUAL BRAKING”', 'PM', True,
        'During all the rollout, the PM monitors that the FMA displays BRK LO or BRK MED and calls out if the autobrake mode disengages.', 'PRO-NOR-SOP-19-A-00012004.0014001'),
    box('PM: “DECEL” (or “NO DECEL”)', 'felt, and confirmed by the speed trend on the PFD', 'PM', True,
        'The flight crew feels the deceleration. The flight crew checks the speed trend on the PFD to confirm the deceleration.', 'PRO-NOR-SOP-19-A-00012004.0014001'),
    box('At 70 kt · PM: “SEVENTY KNOTS” · PF: “CHECKED” · ALL REVERSER LEVERS IDLE', 'high reverse at low speed only in an emergency', 'B', True,
        'It is recommended to reduce reverse thrust when passing 70 kt . However high levels of reverse thrust may be used in order to control aircraft speed in case of an emergency.', 'PRO-NOR-SOP-19-A-00012007.0001001'),
    box('At taxi speed · ALL REVERSER LEVERS STOW', 'before leaving the runway · no reverse on taxiways except emergency', 'PF', False,
        'When the aircraft reaches the taxi speed, and before it leaves the runway, stow the reversers.', 'PRO-NOR-SOP-19-A-00012008.0001001'),
    box('Before 20 kt · AUTO BRK DISENGAGE', 'use the brake pedals to disengage', 'PF', False,
        'Disengage the autobrake to avoid some brake jerks at low speed. The flight crew should use brake pedals to disengage the autobrake.', 'PRO-NOR-SOP-19-A-00012010.0001001'),
  ], 'FCOM PRO-NOR-SOP-19-A · SCO-D'),
]))

# ---------------------------------------------------------------- AFTER LANDING
PH.append(P('after-landing', 'After Landing', 'n', 'AFTER LANDING', 'FCOM PRO-NOR-SOP-21', [
  S('AFTER LANDING FLOW', OCEAN, [
    trig('Runway vacated · PF disarms GND SPLRS', 'PF'),
    box('GND SPLRS DISARM', 'when the runway is vacated', 'PF', False, 'When the runway is vacated: GND SPLRS ... DISARM PF', 'PRO-NOR-SOP-21-A-00011014.0001001'),
    box('LAND LIGHT sw OFF · WING sw OFF · STROBE sw AUTO · NOSE sw TAXI', 'PF may request the PM to set the exterior lights', 'PF', False,
        'When leaving the runway: LAND LIGHT sw ... OFF PF WING sw ... OFF PF STROBE sw ... AUTO PF NOSE sw ... TAXI PF', 'PRO-NOR-SOP-21-A-00011013.0001001'),
    box('WXR/PWS sw OFF · CAPT and F/O DISPLAY OFF', 'avoids radiating persons at the gate', 'PM', False,
        'Switching the radar and radar display to OFF after landing avoids risk of radiating persons at the gate area.', 'PRO-NOR-SOP-21-A-00012821.0001001'),
    box('ENG START selector NORM', '', 'PM', False, 'ENG START selector ... NORM PM', 'PRO-NOR-SOP-21-A-00011020.0001001'),
    box('FLAPS RETRACT', 'icing approach or slush/snow: do not retract until after shutdown and ground crew confirms clear · OAT above 40 °C: consider CONF 1 during transit', 'PM', False,
        '- If the approach was performed in icing conditions, or if the runway was contaminated with slush or snow, do not retract the flaps until after engine shutdown, and after the ground crew confirmed that flaps and slats are clear of obstruction due to ice.', 'PRO-NOR-SOP-21-A-00011021.0001001'),
    box('TCAS STBY', '', 'PM', False, 'TCAS ... STBY PM', 'PRO-NOR-SOP-21-A-00011022.0001001'),
    box('APU AS RQRD', 'start fails: wait 3 min · three consecutive attempts: wait 60 min · may delay start until before shutdown, check AVAIL first', 'PM', False,
        'If the start attempt fails, wait for 3 min, then set the APU START pb-sw to ON again. This ensures that the fuel feed line of the APU is sufficiently pressurized. After three consecutive start attempts, the flight crew must wait 60 min before they perform a new start attempt.', 'PRO-NOR-SOP-21-A-00011027.0001001'),
    box('ATC AS RQRD', 'per airport requirements', 'PM', False, 'ATC is set in accordance with airport requirements.', 'PRO-NOR-SOP-21-A-00011023.0001001'),
    box('ENG ANTI ICE AS RQRD', 'ground idle is increased: control taxi speed', 'PM', False,
        'If engine anti-ice is used, carefully control taxi speed, particularly on wet or slippery surfaces because ground idle is increased.', 'PRO-NOR-SOP-21-A-00011024.0004001'),
    box('BRAKE TEMPERATURE MONITOR · BRAKE FAN pb-sw AS RQRD', 'WHEEL SD: discrepancies and high temperature · maintenance if two brakes of a gear differ by more than 150 °C with one at or above 600 °C, or one at or below 60 °C', 'PM', False,
        'Check the brake temperature for discrepancies and high temperature on the WHEEL SD page', 'PRO-NOR-SOP-21-A-00011025.0002001'),
    cl('After Landing', 'After Landing flow complete'),
  ], 'FCOM PRO-NOR-SOP-21'),
  S('ENGINE 2 SHUTDOWN DURING TAXI-IN (one engine taxi)', TEAL, [
    box('No less than 1 min after high thrust · PM: “COOLING TIME ELAPSED”', 'idle reverse and normal taxi thrust are not high thrust: cooling starts at the flare · MAX reverse: cooling starts at idle reverse in the rollout', 'PM', True,
        'The flight crew should operate the engines at or near idle thrust for a cooling period of 1 min before engine shutdown, in order to thermally stabilize the engines.', 'PRO-NOR-SOP-21B-00026759.0004001'),
    box('Taxiing in a straight line · PF: ENG 2 SHUTDOWN ORDER', 'slight jerk forward if the brakes are applied while moving', 'PF', True,
        'During engine shutdown, a slight jerk forward may occur if the brakes are applied while the aircraft is moving.', 'PRO-NOR-SOP-21B-00026759.0004001'),
    box('APU START pb CHECK AVAIL (if started before shutdown) · ENG 2 ANTI ICE pb-sw OFF · ENG 2 MASTER lever OFF · ENG 2 PARAMETERS CHECK', 'engine 2 parameters decrease', 'PM', False,
        'Check that the engine 2 parameters decrease.', 'PRO-NOR-SOP-21B-00026759.0004001'),
  ], 'FCOM PRO-NOR-SOP-21B'),
]))

# ---------------------------------------------------------------- PARKING / SECURING
PH.append(P('parking', 'Parking', 'n', 'PARKING / SECURING', 'FCOM PRO-NOR-SOP-22 · PRO-NOR-SUP-SEC', [
  S('PARKING FLOW', VIOLET, [
    box('ACCU PRESS indicator CHECK · PARK BRK handle ON', 'low accumulator pressure: chocks before shutdown · brake above 300 °C: release after chocks', 'PF', False,
        'The ACCU PRESS indication must be in the green band. In case of low accumulator pressure, chocks are required before engine shutdown.', 'PRO-NOR-SOP-22-A-00012189.0005001'),
    box('ANTI ICE OFF', '', 'PM', False, 'ANTI ICE ... OFF PM', 'PRO-NOR-SOP-22-A-00012190.0001001'),
    box('APU BLEED pb-sw AS RQRD', 'ON and wait for the APU BLEED memo, then shut down the engines immediately', 'PM', False,
        '- Shut down the engines immediately after the display of the APU BLEED memo to prevent engine exhaust fumes from entering the air conditioning.', 'PRO-NOR-SOP-22-A-00012191.0002001'),
    box('All ENG MASTER levers OFF', 'no less than 1 min after high thrust · APU START CHECK AVAIL or EXT A(B) ON first', 'PF', False,
        'No less than 1 min after high thrust operations: All ENG MASTER levers ... OFF PF', 'PRO-NOR-SOP-22-A-00012192.0004001'),
    box('FUEL PUMPS OFF', '', 'PM', False, 'FUEL PUMPS ... OFF PM', 'PRO-NOR-SOP-22-A-00012198.0001001'),
    box('WING sw OFF · BEACON sw OFF · other exterior lights AS RQRD (NAV & LOGO 1)', 'beacon off when all engines spooled down · wing lights off with the jetway on', 'PF', False,
        'Turn off the beacon lights when all engines spooled down.', 'PRO-NOR-SOP-22-A-00012195.0003001'),
    box('ATC STBY', '', 'PM', False, 'ATC ... STBY PM', 'PRO-NOR-SOP-22-A-00012199.0001001'),
    box('SEAT BELTS sw OFF', '', 'PF', False, 'SEAT BELTS sw ... OFF PF', 'PRO-NOR-SOP-22-A-00012196.0001001'),
    box('IRS PERFORMANCE CHECK', 'FMS POSITION/MONITOR deviation', 'PM', False,
        'On the FMS POSITION/MONITOR page, check that the deviation does not exceed the following:', 'PRO-NOR-SOP-22-A-00012200.0001001'),
    box('SLIDES CHECK DISARMED', 'warn the cabin crew if any slide is not disarmed', 'PF', False,
        'Check that the slides are disarmed on the DOOR/OXY SD page. Warn the cabin crew, if any slide is not disarmed.', 'PRO-NOR-SOP-22-A-00012194.0001001'),
    box('FUEL QUANTITY CHECK', 'FOB + fuel used = departure FOB; unusual discrepancy = maintenance', 'PM', False,
        'Check that the sum of the fuel on board and the fuel used is consistent with the fuel on board at departure. If the flight crew detects a discrepancy that is not usual, maintenance action is due.', 'PRO-NOR-SOP-22-A-00012201.0001001'),
    box('GROUND CONTACT ESTABLISH · PARK BRK handle ON', '“chocks in” hand signal · release after chocks if a brake is above 300 °C (150 °C with fans)', 'PF', False,
        'The parking brake should be set. If one brake temperature is above 300 °C (or above 150 °C with brake fans ON), the parking brake should be released after chocks are in place.', 'PRO-NOR-SOP-22-A-00012204.0001001'),
    cl('Parking', 'Parking flow complete'),
    box('STATUS page CHECK · LOGBOOK COMPLETE', 'per the STATUS page', 'C', False,
        'Complete the logbook according to the STATUS page.', 'PRO-NOR-SOP-22-A-00012206.0001001'),
    box('DUs DIM', 'EFIS, ECAM and MCDU', 'B', False, 'Dim EFIS, ECAM and MCDU display units.', 'PRO-NOR-SOP-22-A-00012205.0001001'),
  ], 'FCOM PRO-NOR-SOP-22'),
  S('SECURING THE AIRCRAFT', SLATE, [
    box('PARK BRK handle CHECK ON', 'reduces accumulator leak rate', 'B', False,
        'Keep the parking brake on to reduce hydraulic leak rate in the brake accumulator.', 'PRO-NOR-SUP-SEC-A-00011029.0001001', 'FCOM'),
    box('OXYGEN CREW SUPPLY pb OFF', '', 'B', False, 'OXYGEN CREW SUPPLY pb ... OFF', 'PRO-NOR-SUP-SEC-A-00011030.0001001', 'FCOM'),
    box('All IR MODE selectors OFF', 'wait at least 10 s before removing electrical supply · not above 82° N/S during transits', 'B', False,
        'After turning off the ADIRS, wait at least 10 s before turning off the electrical supply, in order to ensure that the ADIRS memorize the latest data.', 'PRO-NOR-SUP-SEC-A-00011031.0001001', 'FCOM'),
    box('EXTERIOR LIGHTS OFF · GND SELECT CTL sw AS RQRD · APU BLEED OFF · EXT PWR AS RQRD · APU MASTER SW OFF', 'APU off after all passengers disembarked', 'B', False,
        'Turn off the APU after all passengers disembarked.', 'PRO-NOR-SUP-SEC-A-00024902.0001001', 'FCOM'),
    box('EMER EXIT LT sw OFF · SIGNS sw OFF', '', 'F', False, 'EMER EXIT LT sw ... OFF CM2 SIGNS sw ... OFF CM2', 'PRO-NOR-SUP-SEC-A-00011036.0002001', 'FCOM'),
    box('BAT 1, BAT 2 and APU BAT pb-sw OFF', 'wait for the APU flap to close (about 2 min after AVAIL out)', 'B', False,
        'Wait until the APU flap is fully closed (about 2 min after APU AVAIL light goes out) before switching off the APU battery. Switching the batteries off before the APU flap is closed may cause smoke in the cabin during the next flight.', 'PRO-NOR-SUP-SEC-A-00011037.0001001', 'FCOM'),
    box('WINDOWS CHECK CLOSED · EFB APPLICATIONS CLOSE', '', 'B', False, 'WINDOWS ... CHECK CLOSED CM1-CM2', 'PRO-NOR-SUP-SEC-A-00026014.0001001', 'FCOM'),
    cl('Securing the Aircraft', 'aircraft left unattended'),
  ], 'FCOM PRO-NOR-SUP-SEC'),
]))

# ============================================================ NON-NORMAL
# ---------------------------------------------------------------- GO-AROUND
PH.append(P('go-around', 'Go-Around', 'a', 'GO-AROUND', 'FCOM PRO-NOR-SOP-20 · SCO-D', [
  S('GO-AROUND · SIMULTANEOUSLY', RED, [
    box('THRUST LEVERS TOGA', 'set TOGA detent even if TOGA thrust is not required, then retard as required (CL for A/THR) · not briefly TOGA: no GO AROUND phase, destination sequences within 7 NM', 'PF', False,
        'If TOGA thrust is not required, set the thrust levers to TOGA detent then retard the thrust levers as required. This enables to engage the GO-AROUND phase, with associated AP/FD modes.', 'PRO-NOR-SOP-20-A-00011082.0008001'),
    box('ROTATION PERFORM', 'toward 15° (about 12.5° one engine out) then follow SRS · near the ground avoid excessive rotation rate (tail strike)', 'PF', False,
        'Initiate rotation towards 15 ° of pitch with all engines operative (approximately 12.5 ° if one engine is out) to get a positive rate of climb then follow SRS Flight Director pitch orders.', 'PRO-NOR-SOP-20-A-00011082.0008001'),
    box('PF: “GO AROUND - FLAPS” · PM: FLAPS RETRACT ONE STEP · “FLAPS __”', 'PM: FLIGHT PARAMETERS MONITOR', 'B', True,
        'GO AROUND ... ANNOUNCE PF FLIGHT PARAMETERS ... MONITOR PM FLAPS ... RETRACT ONE STEP PM', 'PRO-NOR-SOP-20-A-00011082.0008001'),
    box('FMA CHECK/ANNOUNCE', 'MAN TOGA / SRS / GA TRK or NAV / A/THR · RNP AR: NAV engages immediately (minimum 100 ft)', 'PF', True,
        'The following modes are displayed: MAN TOGA / SRS / GA TRK or NAV / A/THR.', 'PRO-NOR-SOP-20-A-00011082.0008001'),
    box('PM: “POSITIVE CLIMB” · PF: “GEAR UP” · PM: L/G UP · “GEAR UP”', 'NAV or HDG mode AS RQRD (PF) · GO AROUND ALTITUDE CHECK (PM)', 'B', True,
        'POSITIVE RATE ... ANNOUNCE PM L/G UP ... ORDER PF L/G ... UP PM NAV or HDG mode ... AS RQRD PF GO AROUND ALTITUDE ... CHECK PM', 'PRO-NOR-SOP-20-A-00011082.0008001'),
    box('At go-around thrust reduction altitude · THRUST LEVERS CL', 'LVR CLB flashing', 'PF', False,
        'AT GO-AROUND THRUST REDUCTION ALTITUDE THRUST LEVERS ... CL PF', 'PRO-NOR-SOP-20-A-00011084.0001001'),
    box('At go-around acceleration altitude · SPEED MONITOR', 'target increases to green dot · if not: FCU ALT CHECK, ALT knob PULL', 'PF', False,
        'Monitor that the target speed increases to Green Dot.', 'PRO-NOR-SOP-20-A-00011085.0001001'),
    box('Acceleration flow · F speed “FLAPS 1” · S speed “FLAPS 0”', 'PM: GND SPLRS DISARM · L/G CHECK UP · NOSE OFF · RWY TURN OFF OFF · other lights AS RQRD (LAND may stay ON)', 'B', True,
        'The flight crew can maintain the LAND sw set to ON, according to airline policy or regulatory recommendations.', 'PRO-NOR-SOP-20-A-00011085.0001001'),
    cl('Approach', 'after the revised approach briefing (Air Turn Back, pattern or go-around)'),
  ], 'FCOM PRO-NOR-SOP-20'),
  S('GO-AROUND DEVIATION CALLOUTS (PM) · PF: “CORRECTING”', PLUM, [
    box('“BANK ANGLE” approaching 7° · “PITCH” above 20° or below 10° nose up · “SINK RATE” no climb rate', '', 'PM', True, '', ''),
    box('Discontinued approach · PF: “CANCEL APPROACH”', 'at or above the FCU altitude only', 'PF', True,
        'DISCONTINUED APPROACH CANCEL APPROACH decision', 'PRO-NOR-SCO-D-00015191.0001001'),
  ], 'FCOM PRO-NOR-SCO-C / SCO-D'),
]))
PH[-1]['sections'][1]['items'][0].update({'quote': 'GO AROUND decision GO AROUND - FLAPS Flaps retraction FLAPS__ Gear retraction POSITIVE CLIMB GEAR UP GEAR UP', 'ref': 'PRO-NOR-SCO-D-00011850.0001001'})

# ---------------------------------------------------------------- DIVERSION
PH.append(P('diversion', 'Diversion', 'a', 'DIVERSION', 'PRC Diversion Guidance · FOM 6.4 / 11.2.7.1', [
  S('DIVERSION GUIDANCE (PRC)', PLUM, [
    box('1 · Complete the non-normal procedure (ECAM / QRH)', '', 'B', False,
        'Failure cases requiring a diversion to the nearest airport (cases leading to a LAND ASAP message on the ECAM and/or in the QRH)', 'FCOM PRO-SPO-40A-00023707.0001001 (PRC p2 Diversion Guidance)', 'FCOM'),
    box('2 · Does the failure require diversion? YES: DIVERT (coordinate with SOCC)', 'failures requiring diversion: LAND ASAP, FIRE, engine failure · insufficient fuel after a component failure · one GEN remaining', 'B', True,
        'Failure cases resulting in increased fuel consumption, exceeding the available fuel reserves ‐ Electrical generation. Diversion is required in the case of: • Only one generator (either one IDG, APU GEN or EMER GEN) remaining available following a multiple failure', 'FCOM PRO-SPO-40A-00023707.0001001 (PRC p2 Diversion Guidance)', 'FCOM'),
    box('3 · If not required: are the risks of continuing higher than the risks of diverting?', 'continue to destination, or DIVERT (coordinate with SOCC)', 'B', False,
        'The technical criteria governing a re-routing or diversion decision can be classified into five categories', 'FCOM PRO-SPO-40A-00023707.0001001 (PRC p2 Diversion Guidance)', 'FCOM'),
    note('No impact on ETOPS operations for amber or green ECAM messages / memos or any single failure other than an engine failure (PRC p2).'),
  ], 'PRC p2 Diversion Guidance · FCOM PRO-SPO-40A'),
  S('DIVERSION DECISION (FOM)', TEAL, [
    box('One engine inoperative · land at the NEAREST SUITABLE airport', '14 CFR 121.565 · Captain judgment after considering all relevant factors · assign PF/PM per TEM', 'C', False,
        '14 CFR 121.565 requires the Captain of a two-engine aircraft with one engine inoperative to land at the nearest suitable airport where, in the Captain’s judgment after considering all relevant factors, a safe landing can be made.', 'FOM 6.4.2', 'FOM'),
    box('Flight crews will', 'maintain awareness of suitable airports · current diversion plan in mind · weather and NOTAMs at the diversion airport · coordinate with Dispatch · include the diversion plan in the brief after a rest period', 'B', False,
        'Flight Crews will: • Maintain awareness of suitable airports • Have a current diversion plan in mind • Keep track of weather and NOTAMs at diversion airport • Be prepared to coordinate with Dispatch in the event of an actual diversion', 'FOM 6.4.1', 'FOM'),
    box('180 turn near a fuel-critical ETP', 'turn time is not in the flight planning fuel or time', 'B', False,
        'If a 180 turn is necessary near a fuel-critical ETP, the Flight Crew should be aware that the time to complete the turn is not factored in the fuel or time calculations by the flight planning system.', 'FOM 6.4.1', 'FOM'),
    box('Nearest suitable: factors', 'configuration, weight, systems, fuel · enroute wind and weather at diversion altitude · minimum altitudes · fuel burn · terrain, weather, wind · runways and surface · navaids and lighting · RFFS · disembarkation facilities · PIC familiarity · geo-political', 'C', False,
        '• Approach navigation aids and lighting available • Rescue and fire fighting services (RFFS) at the diversion airport • Facilities for passenger and crewmember disembarkation and accommodations • PIC’s familiarity with the airport', 'FOM 11.2.7.1', 'FOM'),
    box('Never sufficient to fly beyond the nearest suitable (one engine inop)', 'fuel to fly beyond · passenger accommodation other than safety · maintenance or repair resources', 'C', False,
        'When operating a two-engine aircraft with one engine inoperative, none of the following factors should be considered sufficient justification to fly beyond the nearest suitable airport: • The fuel supply is sufficient to fly beyond the nearest suitable airport • Passenger accommodation other than passenger safety • Availability of maintenance and/or repair resources', 'FOM 11.2.7.1', 'FOM'),
    box('Decision to continue after a system failure', 'coordinate with Dispatch: re-evaluate capabilities, new Flight Plan/Release before the EEP if required', 'B', False,
        'If an updated Flight Plan/Dispatch Release is required and the flight has not passed the EEP, then the new Flight Plan/Dispatch Release must be received prior to the EEP.', 'FOM 6.4.4', 'FOM'),
    box('ATC · advise as soon as practicable, remind of the aircraft type, request expeditious handling', '', 'C', True,
        'If contingency procedures are employed as a result of an engine shutdown or system failure, the Captain should advise ATC as soon as practicable of the situation, reminding ATC of the type of aircraft involved, and make a request for expeditious handling.', 'FOM 6.4.6', 'FOM'),
  ], 'FOM 6.4 · 11.2.7.1'),
]))

# ---------------------------------------------------------------- ETOPS DIVERT
PH.append(P('etops', 'ETOPS Divert', 'a', 'ETOPS DIVERSION', 'FOM 6.3 / 6.4 · PRC p1', [
  S('ENGINE FAILURE DURING CRUISE (PRC)', RED, [
    box('Simultaneously: SET MCT and DISCONNECT AUTOTHRUST', 'instinctive disconnect pb · do not delay the descent · do not decelerate below green dot', 'PF', False,
        'At high flight levels, close to the weight limits, the aircraft speed quickly reduces. Thus, the flight crew should not delay descent. The crew must not decelerate below green dot.', 'PRC p1 Engine Failure During Cruise', 'PRC'),
    box('PULL SPEED - GREEN DOT', 'initially green dot to minimize the rate of descent', 'PF', False,
        'PULL SPEED - GREEN DOT', 'PRC p1 Engine Failure During Cruise', 'PRC'),
    box('Oceanic: ESTABLISH 5 NM OFFSET', 'turn at least 30° L/R to a parallel same-direction track offset 5 NM · pull heading and/or 5 NM offset on the F-PLN · below FL290 (or when cleared) maneuver as required', 'PF', False,
        'Leave the cleared route/track by turning at least 30º to the L/R to establish a parallel same direction track offset by 5NM. Pull heading and/or insert a 5NM L/R offset on MCDU FPLN page.', 'PRC p1 Engine Failure During Cruise', 'PRC'),
    box('PULL FL 200 · START APU', 'FL200 until the final drift down altitude is determined', 'PF', False,
        'Initially set FL200 until the final Drift Down Altitude is determined.', 'PRC p1 Engine Failure During Cruise', 'PRC'),
    box('Exterior lights ON · monitor TCAS · declare MAYDAY on VHF or 121.5 · CPDLC EMERG ADS-C ON', 'non-radar: keep transmitting position and intentions on 121.5 (backup 123.45) until clear of all traffic · consider squawking 7700', 'PM', True,
        'Declare an Emergency (MAYDAY). Transmit position and intentions on current VHF ATC frequency or 121.5.', 'PRC p1 Engine Failure During Cruise', 'PRC'),
    box('ACCOMPLISH ECAM ACTIONS · ATC route clearance when workload permits', 'load the new route and MANAGE NAV', 'B', False,
        'When ATC clearance is received, load the new route into FMS and MANAGE NAV.', 'PRC p1 Engine Failure During Cruise', 'PRC'),
    box('RESET DRIFT DOWN ALTITUDE IN FCU', 'REC MAX EO (PROG 1R) · V/S below 500 ft/min: select V/S -500 and A/THR ON', 'PF', False,
        'When the V/S becomes less than 500 ft/min, select V/S -500 ft/min and A/THR ON.', 'PRC p1 Engine Failure During Cruise', 'PRC'),
    box('ADJUST SPEED · ETOPS and standard strategy: 300 kt / M 0.78', 'obstacle strategy green dot until clear of obstacles', 'PF', False,
        'For ETOPS & Standard Strategy: set 300 kt / M0.78', 'PRC p1 Engine Failure During Cruise', 'PRC'),
    box('Contact company · position report every 80 min or 10° · monitor fuel predictions · landing weight and performance', 'amended release, landing performance, weather, special assistance · overweight: QRH Overweight Landing', 'B', False,
        'Report position every 80 minutes or less / 10º or less, as required by ATC or company.', 'PRC p1 Engine Failure During Cruise', 'PRC'),
  ], 'PRC p1'),
  S('ETOPS DIVERSION (FOM)', TEAL, [
    box('Diversion speed · approved One-Engine-Inoperative Cruise Speed', 'Captain may deviate after assessing the emergency and fuel remaining', 'C', False,
        'The Captain has the authority to deviate from this planned speed profile after assessing the emergency and considering fuel remaining.', 'FOM 6.4.5', 'FOM'),
    box('Pick the field · least time at or near cruise altitude', 'ETPs use planning-time lower-altitude winds · a closer non-ETOPS airport may be better', 'B', False,
        'Since the vast majority of diversions are not due to a mechanical issue requiring a descent well below cruise altitude, the Flight Crew should be continuously aware of the airport that would take the least amount of time to fly to at or near cruise altitude.', 'FOM 6.3.7', 'FOM'),
    box('Fuel · CP/ETP critical fuel is a dispatch requirement only', 'no requirement to divert before the CP if destination fuel is above arrival requirements; Dispatcher adjusts altitude, speed, alternate, routing', 'B', False,
        'Arriving at the CP/ETP with Fuel On Board (FOB) equal to or greater than the fuel required by the critical fuel scenario is only a dispatch requirement.', 'FOM 6.3.6', 'FOM'),
  ], 'FOM 6.3 / 6.4'),
  S('DECOMPRESSION IN ETOPS SEGMENT', RED, [
    box('1 · Turn to offset from the route', 'Special Procedures for In-Flight Contingencies', 'B', False,
        '• Turn to offset from the route utilizing the Special Procedures for In-Flight Contingencies.', 'FOM 6.4.3', 'FOM'),
    box('2 · Emergency descent to 10,000 ft or MOCA/Grid MORA, whichever is higher', '', 'B', True,
        '• Perform an Emergency Descent to 10,000 ft or MOCA/Grid MORA, whichever is higher.', 'FOM 6.4.3', 'FOM'),
    box('3 · Below FL290 (or sooner if cleared) proceed directly to the nearest suitable airport', '', 'B', False,
        '• Below FL290, or sooner if cleared by ATC, proceed directly to the nearest suitable airport.', 'FOM 6.4.3', 'FOM'),
    box('4 · When level · Flight Plan one-engine diversion speed, or LRC for a two-engine decompression', '', 'B', False,
        '• When level, use the Flight Plan one-engine diversion speed or (AS) Long Range Cruise (LRC) for two-engine decompression.', 'FOM 6.4.3', 'FOM'),
  ], 'FOM 6.4.3'),
]))

# ---------------------------------------------------------------- OCEANIC CONTINGENCY
PH.append(P('oceanic', 'Oceanic Contingency', 'a', 'OCEANIC IN-FLIGHT CONTINGENCY', 'FOM 5.7.4 · PRC p3', [
  S('NO ATC CLEARANCE · CONTINGENCY', NAVY, [
    box('Get a revised clearance first, whenever possible', '', 'B', False,
        'If an aircraft is unable to continue the flight in accordance with its ATC clearance, a revised clearance shall be obtained, whenever possible, prior to initiating any action.', 'FOM 5.7.4.2', 'FOM'),
    box('1 · Turn at least 30° left or right · parallel same-direction track offset 5 nm', '', 'B', True,
        'Specifically, the pilot shall leave the cleared track or ATS route by initially turning at least 30° to the right or to the left, in order to establish and maintain a parallel, same direction track or ATS route offset 5 nm.', 'FOM 5.7.4.2', 'FOM'),
    box('Choose the turn direction', 'position vs the track system · adjacent track flight levels · direction to an alternate · any SLOP · terrain', 'B', False,
        '• Aircraft position relative to any organized track or ATS route system • Direction of flights and flight levels allocated on adjacent tracks • Direction to an alternate airport • Any strategic lateral offset being flown • Terrain clearance', 'FOM 5.7.4.2', 'FOM'),
    box('2 · Below FL290 before diverting (unless cleared) · once on the parallel route, 500 ft vertical offset', 'maintain the flight level until 5 nm offset if possible; minimize the rate of descent', 'B', True,
        'Once established on a parallel route, establish a 500-ft vertical offset and proceed as required by the situation, or if an ATC clearance has been obtained, proceed in accordance with the clearance.', 'FOM 5.7.4.3', 'FOM'),
    box('3 · TCAS TA/RA · all exterior lights ON · squawk 7700 when able', '', 'B', True,
        'Turn on all aircraft exterior lights (commensurate with appropriate operating limitations). Keep the transponder on at all times and, when able, squawk 7700, as appropriate.', 'FOM 5.7.4.2', 'FOM'),
    box('4 · Broadcast on the frequency in use and 121.5 (backup 123.45)', 'identification · nature of distress · intentions · position with route or track · flight level · MAYDAY or PAN-PAN three times', 'B', True,
        'Establish communications with and alert nearby aircraft by broadcasting on the frequencies in use and at suitable intervals on 121.5 MHz (or, as a backup, on the inter-pilot air-to-air frequency 123.45 MHz): aircraft identification, the nature of the distress condition, intention of the pilot, position (including the ATS route designator or the track code, as appropriate), and flight level.', 'FOM 5.7.4.2', 'FOM'),
    box('ETOPS · engine shutdown or ETOPS-critical failure', 'advise ATC as soon as practical, remind of type, request expeditious handling', 'C', False,
        'ETOPS – If these contingency procedures are employed as a result of an engine shutdown or failure of an ETOPS-critical system, advise ATC of the situation as soon as practical, remind ATC of the type of aircraft, and request expeditious handling.', 'FOM 5.7.4.2', 'FOM'),
  ], 'FOM 5.7.4.2 / 5.7.4.3'),
  S('WEATHER DEVIATION · OCEANIC', CYAN, [
    box('Request first · “WEATHER DEVIATION REQUIRED” or CPDLC lateral downlink', 'urgency: “PAN-PAN” three times or CPDLC urgency downlink', 'B', True,
        '• Stating “WEATHER DEVIATION REQUIRED” to indicate that priority is desired on the frequency and for ATC response; or • Requesting a weather deviation using a CPDLC lateral downlink message.', 'FOM 5.7.4.4', 'FOM'),
    box('No clearance · Captain exercises emergency authority', 'deviate away from the track system · broadcast on the frequency in use and 121.5 / 123.45 · watch TCAS · exterior lights ON', 'C', False,
        '• If possible, deviate away from an organized track or route system.', 'FOM 5.7.4.6', 'FOM'),
    box('Less than 5 nm · maintain the assigned flight level', '', 'B', False,
        '• For deviations less than 5 nm, maintain assigned flight level.', 'FOM 5.7.4.6', 'FOM'),
    box('5 nm or more · level change at about 5 nm from track', 'EAST (0° to 179° magnetic): LEFT descend 300 ft, RIGHT climb 300 ft · WEST (180° to 359°): LEFT climb 300 ft, RIGHT descend 300 ft', 'B', True,
        'Direction of Flight Deviations ≥5 NM Altitude Change LEFT DESCEND 300 ft EAST (0° to 179° magnetic) RIGHT CLIMB 300 ft LEFT CLIMB 300 ft WEST (180° to 359° magnetic) RIGHT DESCEND 300 ft', 'FOM 5.7.4.6 Table', 'FOM'),
    box('Returning to track · assigned flight level within about 5 nm of centerline', 'keep trying for a clearance', 'B', False,
        'When returning to track or cleared route, be at its assigned flight level when the aircraft is within approximately 5 nm of the centerline, and if contact was not established prior to deviating, continue to attempt to contact ATC to obtain a clearance.', 'FOM 5.7.4.6', 'FOM'),
  ], 'FOM 5.7.4.4 / 5.7.4.6'),
  S('SLOP', GREEN, [
    box('0.0 to 2.0 nm RIGHT of centerline only, 0.1 nm increments', 'no ATC clearance required, ATC need not be advised · offset at the oceanic entry, centerline by the oceanic exit', 'B', False,
        'SLOP will be applied in relation to a route or track; the aircraft may fly zero, up to a maximum of 2 nm right of course only, from 0.0 - 2.0 nm, right of centerline (in 0.1 nm increments). SLOP left of course is not authorized.', 'FOM 5.7.4.7', 'FOM'),
    box('Overtaking · offset to create the least wake for the aircraft overtaken', '', 'B', False,
        'Any aircraft overtaking another aircraft is to offset within the confines of this procedure, if capable, so as to create the least amount of wake turbulence for the aircraft being overtaken.', 'FOM 5.7.4.7', 'FOM'),
  ], 'FOM 5.7.4.7'),
]))

# ---------------------------------------------------------------- DEPRESS (POLYGONS)
PH.append(P('depress', 'Depress (Polygons)', 'a', 'DECOMPRESSION POLYGONS', 'FOM 11.2.8 / 11.2.9', [
  S('DECOMPRESSION POLYGON PROCEDURES', RED, [
    box('Polygons · IFR High and Low charts in Jeppesen FD Pro', 'areas of high terrain where a descent directly to 10,000 ft may not be possible · procedure in the detail drawer (tap the label)', 'B', False,
        'Polygons are located in the IFR High and IFR Low charts in Jeppesen FD Pro and denote areas of high terrain where a descent directly to 10,000 ft may not be possible.', 'FOM 11.2.9', 'FOM'),
    box('A330 initial descent altitude · always 17,000 ft or FL170', '', 'B', True,
        '(737/A330) Initial descent altitude is always 17,000 ft or FL170.', 'FOM 11.2.9', 'FOM'),
    box('Exit Any Direction · “Exit Any Dir.”', '', 'B', False,
        '1. Exit Any Direction polygons are labeled “Exit Any Dir.” and can be exited in any direction.', 'FOM 11.2.9', 'FOM'),
    box('Exit Toward Fix · “Exit Twd” + fix', 'not necessary to fly to the fix', 'B', False,
        '2. Exit Toward Fix polygons are labeled “Exit Twd” followed by the fix to be flown towards to exit the polygon. It is not necessary to fly to the Exit Towards fix.', 'FOM 11.2.9', 'FOM'),
    box('To Fix then Route · fix, then the route', 'FD Pro shows the escape route and fixes', 'B', False,
        '3. To Fix then Route polygons are labeled with the fix that should be flown to, and then the route that should be flown subsequently.', 'FOM 11.2.9', 'FOM'),
    box('Initial turn distance is built in · do not enter another polygon below its altitude unless terrain clearance is assured', '', 'B', False,
        'Do not enter another polygon while navigating at less than the altitude indicated in the polygon detail drawer unless terrain clearance is assured.', 'FOM 11.2.9', 'FOM'),
    box('No Ops Area · never', '', 'B', False,
        'Dispatchers and pilots will not permit flights to proceed through any areas charted as “No Ops Area.”', 'FOM 11.2.9', 'FOM'),
    note('The PIC is expected and encouraged to exercise sound judgment when applying these procedures (FOM 11.2.9).'),
  ], 'FOM 11.2.9'),
  S('EMERGENCY DESCENT (FOM)', PLUM, [
    box('Time of useful consciousness is very limited · quick-don masks within 5 seconds, one hand', '', 'B', False,
        'Flight Crews have a very limited time of useful consciousness at altitude. Quick-don masks are designed to be donned with one hand within 5 seconds.', 'FOM 11.2.8', 'FOM'),
    note('Aircraft procedure: see Emer Descent (QRH 22.02A).'),
  ], 'FOM 11.2.8'),
]))

# ---------------------------------------------------------------- REJECTED TAKEOFF
PH.append(P('rto', 'Rejected T/O', 'a', 'REJECTED TAKEOFF', 'FCTM PR-AEP-MISC-C', [
  S('DECISION (CAPTAIN)', RED, [
    box('Captain decides · hand on the thrust levers until V1, PF or PM', 'decision and stop action must be made prior to V1', 'C', False,
        'It is therefore recommended that the Captain keeps the hand on the thrust levers until the aircraft reaches V1, whether the Captain is Pilot Flying (PF) or Pilot Monitoring (PM).', 'FCTM PR-AEP-MISC-C-00020263.0002001', 'FCTM'),
    box('Captain: “GO” · malfunction before V1 without rejecting', '', 'C', True,
        '- If a malfunction occurs before V1, for which the Captain does not intend to reject the takeoff, the Captain will announce the intention by calling "GO".', 'FCTM PR-AEP-MISC-C-00020263.0002001', 'FCTM'),
    box('Captain: “STOP” · confirms the reject and that the Captain has control', 'the only hand-over of control without “I have control”', 'C', True,
        '- If a decision is made to reject the takeoff, the Captain calls "STOP". This call both confirms the decision to reject the takeoff and also states that the Captain now has control. It is the only time that hand-over of control is not accompanied by the phrase "I have control".', 'FCTM PR-AEP-MISC-C-00020263.0002001', 'FCTM'),
    box('Below 100 kt · Captain discretion', 'seriously consider discontinuing for any ECAM alert', 'C', False,
        'The Captain should seriously consider discontinuing the takeoff, if any ECAM alert is activated.', 'FCTM PR-AEP-MISC-C-00020263.0002001', 'FCTM'),
    box('Above 100 kt and below V1 · go-minded', '1 fire alert or severe damage · 2 sudden loss of engine thrust · 3 unambiguous indications the aircraft will not fly safely · 4 any ECAM alert', 'C', False,
        '1. Fire alert, or severe damage 2. Sudden loss of engine thrust 3. Malfunctions or conditions that give unambiguous indications that the aircraft will not fly safely 4. Any ECAM alert.', 'FCTM PR-AEP-MISC-C-00020263.0002001', 'FCTM'),
    box('Not a reject above 100 kt · EGT red line · nose gear vibration · tire failure V1 minus 20 kt to V1', 'the V1 call has precedence over any other call', 'C', False,
        'Exceeding the EGT red line or nose gear vibration should not result in the decision to reject takeoff above 100 kt.', 'FCTM PR-AEP-MISC-C-00020263.0002001', 'FCTM'),
    box('Above V1 · takeoff must be continued', '', 'C', False,
        'Takeoff must be continued, because it may not be possible to stop the aircraft on the remaining runway.', 'FCTM PR-AEP-MISC-C-00020263.0002001', 'FCTM'),
    note('ECAM inhibits non-essential alerts from 80 kt to 1 500 ft (or 2 min after lift-off); any alert in this period is significant (FCTM).'),
  ], 'FCTM PR-AEP-MISC-C'),
  S('RTO TECHNIQUE', PLUM, [
    box('Autobrake MAX decelerating · Captain avoids pressing the pedals', 'inoperative autobrake or reject prior to 72 kt: reduce thrust and apply maximum pressure on both pedals, hold to the stop', 'C', False,
        '- If the autobrake is inoperative or if the takeoff is rejected prior to 72 kt (autobrake not active and no deployment of spoilers), the captain simultaneously reduces thrust and applies maximum pressure on both pedals.', 'FCTM PR-AEP-MISC-C-00020266.0001001', 'FCTM'),
    box('Brake response not appropriate · FULL manual braking · IF IN DOUBT, TAKE OVER MANUALLY', 'normal braking inoperative: LOSS OF BRAKING memory items', 'C', False,
        '- If the brake response does not seem appropriate for the runway condition, FULL manual braking should be applied and maintained. If IN DOUBT, TAKE OVER MANUALLY.', 'FCTM PR-AEP-MISC-C-00020266.0001001', 'FCTM'),
    box('Full reverse may be used to a complete stop · reduce passing 70 kt if runway permits', '', 'C', False,
        'Full reverse may be used until coming to a complete stop. But, if there is enough runway available at the end of the deceleration, it is preferable to reduce reverse thrust when passing 70 kt.', 'FCTM PR-AEP-MISC-C-00020266.0001001', 'FCTM'),
    box('PM: “DECEL” · deceleration felt and confirmed by the speed trend', 'DECEL light only at 80 % of the selected rate; not proof of autobrake operation', 'PM', True,
        '- Announcing the deceleration means that the deceleration is felt by the crew, and confirmed by the Vc trend on the PFD.', 'FCTM PR-AEP-MISC-C-00020266.0001001', 'FCTM'),
    box('Stopped with autobrake MAX · release the brakes before taxi by disarming the spoilers', 'do not vacate until it is clear an evacuation is not necessary', 'C', False,
        'Do not attempt to vacate the runway, until it is absolutely clear that an evacuation is not necessary and that it is safe to do so.', 'FCTM PR-AEP-MISC-C-00020266.0001001', 'FCTM'),
    box('Takeoff following RTO · reset both FDs, set FCU · restart SOPs from the AFTER START checklist · DEPARTURE CHANGE SOP and checklist', '', 'B', False,
        '- Restart Standard Operating Procedures from the AFTER START checklist and perform the DEPARTURE CHANGE SOP including the associated checklist.', 'FCTM PR-AEP-MISC-C-00020408.0001001', 'FCTM'),
    cl('Departure Change', 'revised departure briefing completed'),
  ], 'FCTM PR-AEP-MISC-C'),
]))

# ---------------------------------------------------------------- ENGINE FAILURE AFTER V1
PH.append(P('eng-fail-to', 'Eng Fail After V1', 'a', 'ENGINE FAILURE AFTER V1', 'FCTM PR-AEP-ENG', [
  S('CONTINUE THE TAKEOFF', RED, [
    box('After V1 · continue · handling first', 'stabilize pitch and airspeed, establish the flight path before the ECAM procedure', 'PF', False,
        'If an engine fails after V1, the flight crew must continue the takeoff. The essential and primary tasks are associated with the aircraft handling.', 'FCTM PR-AEP-ENG-00019578.0001001', 'FCTM'),
    box('On the ground · rudder conventionally to hold the centerline', '', 'PF', False,
        'The flight crew should use the rudder conventionally to maintain the aircraft on the runway centerline.', 'FCTM PR-AEP-ENG-00019578.0001001', 'FCTM'),
    box('At VR · rotate about 3°/s toward 12.5°', 'high FLEX temperatures and low VR need precise handling; 12.5° ensures the aircraft becomes airborne', 'PF', False,
        'At VR, the flight crew should rotate the aircraft using a continuous pitch rate of approximately 3 °/s towards an initial pitch attitude of 12.5 °.', 'FCTM PR-AEP-ENG-00019578.0001001', 'FCTM'),
    box('Safely airborne · follow SRS · center the blue beta target with rudder', 'SRS targets the failure speed (V2 to V2+15) · lateral normal law is stable, no rush on the pedals', 'PF', False,
        'Therefore, laterally, the aircraft is a stable platform and no rush is required to use the rudder pedals.', 'FCTM PR-AEP-ENG-00019578.0001001', 'FCTM'),
    box('PM: “POSITIVE RATE” · PF: “GEAR UP”', '', 'B', True, 'Gear retraction POSITIVE RATE GEAR UP GEAR UP', 'PRO-NOR-SCO-D-00011846.0001001'),
    box('Rudder trim · relieve pedal pressure with the beta target centered · then engage the AP', 'AP engaged: rudder trim managed by the AP, release pedal pressure; a maintained pedal deflection may disengage the AP', 'PF', False,
        'The flight crew should use the rudder trim to gradually relieve the pressure from the rudder pedals while keeping the beta target centered. When the aircraft is properly trimmed, the PF should engage the AP.', 'FCTM PR-AEP-ENG-00019578.0001001', 'FCTM'),
    box('Performance short · confirm gear up · consider TOGA', 'derated takeoff: TOGA below F speed can lead to loss of control · takeoff thrust limited to 10 min', 'PF', False,
        'If the takeoff is performed at derated takeoff thrust, selecting TOGA at a speed below F can lead to loss of control of the aircraft.', 'FCTM PR-AEP-ENG-00019578.0001001', 'FCTM'),
  ], 'FCTM PR-AEP-ENG'),
  S('SECURE · ACCELERATE · CLEAN UP', PLUM, [
    box('Trajectory first · delay acceleration only to secure the engine', 'ENG MASTER OFF (no damage) · AGENT 1 DISCH (damage) · fire out or AGENT 2 DISCH (fire)', 'B', False,
        '"Secure the engine" means that the flight crew should continue the ECAM procedure until: - "ENG MASTER OFF" in the case of an engine failure without damage, or - "AGENT 1 DISCH" in the case of an engine failure with damage, or - Fire extinguished or "AGENT 2 DISCH" in the case of an engine fire.', 'FCTM PR-AEP-ENG-00019578.0001001', 'FCTM'),
    box('EO acceleration altitude · ALT pb or push V/S to level off · flaps on schedule', 'rudder input decreases as speed increases · flap lever at zero: beta target reverts to sideslip · never exceed the EO maximum acceleration altitude', 'PF', False,
        'At the engine-out (EO) acceleration altitude, the flight crew should press the ALT pb or push the V/S knob to level off and to enable the speed to increase.', 'FCTM PR-AEP-ENG-00019578.0001001', 'FCTM'),
    box('Speed trend at green dot · pull ALT for OP CLB · THRUST LEVERS MCT when LVR MCT flashes', 'already in FLX/MCT: CL then back to MCT', 'PF', False,
        'When the speed trend arrow reaches the green dot speed, pull the ALT knob to engage OP CLB. Set the thrust levers to MCT when the LVR MCT message flashes on the FMA (this message appears, when the speed index reaches green dot).', 'FCTM PR-AEP-ENG-00019578.0001001', 'FCTM'),
    box('Established on the final takeoff path · continue ECAM to the STATUS page', 'ensure the Acceleration flow · consider relight if no damage · review STATUS', 'B', False,
        'When the aircraft is established on the final takeoff flight path, the flight crew should continue the ECAM procedure until the STATUS page appears.', 'FCTM PR-AEP-ENG-00019578.0001001', 'FCTM'),
    box('One engine out flight path · per the departure briefing', 'EOSID · SID · radar vector', 'PF', False,
        'The flight crew flies the one engine-out flight path in accordance with the departure briefing performed at the gate: - The EOSID, or - The SID, or - Radar vector, etc.', 'FCTM PR-AEP-ENG-00019578.0001001', 'FCTM'),
    box('Failure during initial climb above V2 · maintain the SRS attitude · minimum speed V2', 'FMGS predictions switch to engine-out; pre-selected speeds deleted', 'PF', False,
        'If the failure occurs above V2 however, maintain the SRS commanded attitude. In any case, the minimum speed must be V2.', 'FCTM PR-AEP-ENG-00019585.0001001', 'FCTM'),
  ], 'FCTM PR-AEP-ENG'),
]))

# ---------------------------------------------------------------- EMERGENCY DESCENT
PH.append(P('emer-descent', 'Emer Descent', 'a', 'EMERGENCY DESCENT (QRH 22.02A)', 'QRH R35 22.02A · FCOM PRO-ABN-MISC', [
  S('EMER DESCENT · MEMORY ITEMS', RED, [
    box('CREW OXY MASKS USE', '', 'B', True, 'CREW OXY MASKS ... USE', 'QRH 22.02A ABN-22-00010585.0001001', 'QRH'),
    box('SIGNS ON', '', 'B', True, 'SIGNS ... ON', 'QRH 22.02A ABN-22-00010585.0001001', 'QRH'),
    box('EMER DESCENT INITIATE', '', 'PF', True, 'EMER DESCENT ... INITIATE', 'QRH 22.02A ABN-22-00010585.0001001', 'QRH'),
    box('If A/THR not active: THR LEVERS IDLE', '', 'PF', True, 'If A/THR not active: THR LEVERS ... IDLE', 'QRH 22.02A ABN-22-00010585.0001001', 'QRH'),
    box('SPD BRK FULL', '', 'PF', True, 'SPD BRK ... FULL', 'QRH 22.02A ABN-22-00010585.0001001', 'QRH'),
  ], 'QRH 22.02A'),
  S('WHEN DESCENT ESTABLISHED', PLUM, [
    box('SPEED MAX/APPROPRIATE', 'structural damage suspected: MANEUVER WITH CARE · CONSIDER L/G EXTENSION (speed to VLO/VLE)', 'PF', False,
        'Landing gear may be extended. In such a case, speed must be reduced to VLO/VLE.', 'PRO-ABN-MISC-00012261.0001001', 'FCOM'),
    box('ENG START SEL IGN', '', 'PM', False, 'ENG START SEL ... IGN', 'QRH 22.02A ABN-22-00010585.0001001', 'QRH'),
    box('ATC NOTIFY', 'nature of the emergency and intentions; voice, or CPDLC if voice is poor', 'PM', True,
        'Notify ATC of the nature of the emergency, and state intention. The flight crew can communicate with the ATC using voice, or CPDLC when the voice contact cannot be established or has poor quality.', 'PRO-ABN-MISC-00012261.0001001', 'FCOM'),
    box('EMER DESCENT (PA) ANNOUNCE', '', 'PM', True, 'The flight crew must inform the cabin of emergency descent on the PA system.', 'PRO-ABN-MISC-00012261.0001001', 'FCOM'),
    box('ATC XPDR 7700 CONSIDER', 'unless otherwise specified by ATC', 'PM', False, 'Squawk 7700 unless otherwise specified by ATC.', 'PRO-ABN-MISC-00012261.0001001', 'FCOM'),
    box('CREW OXY MASKS DILUTION NORM', '100 % may not cover the whole descent profile · avoid continuous interphone use', 'B', False,
        '- If the oxygen diluter selector remains set to 100 %, oxygen quantity may be insufficient to cover the entire emergency descent profile', 'PRO-ABN-MISC-00012261.0001001', 'FCOM'),
    box('MAX FL : 100 / MEA-MORA', 'CAB ALT above 14 000 ft: OXYGEN PAX MASK MAN ON ... PRESS', 'B', True,
        'MAX FL : 100/MEA-MORA If CAB ALT above 14 000 ft: OXYGEN PAX MASK MAN ON ... PRESS', 'QRH 22.02A ABN-22-00010585.0001001', 'QRH'),
    note('Notify the cabin crew when the aircraft reaches a safe flight level and cabin oxygen is no more necessary (FCOM PRO-ABN-MISC).'),
  ], 'QRH 22.02A · FCOM PRO-ABN-MISC'),
]))

# ---------------------------------------------------------------- HOLDING
PH.append(P('holding', 'Holding', 'a', 'HOLDING', 'FOM 5.5.15 · FCTM PR-NP-SP-20 · FCOM PRO-NOR-SRP-01-60', [
  S('US HOLDING SPEED AND TIME (FOM)', TEAL, [
    box('6000 ft or below · 200 KIAS', '', 'B', False, '6000 ft or below 200 KIAS', 'FOM 5.5.15 Table', 'FOM'),
    box('Above 6000 ft through 14,000 ft · 230 KIAS (210 KIAS where charted) · 1 minute', 'Alaska or New York with the 210K symbol · military or joint fields expect 230', 'B', False,
        'Above 6000 ft 230 KIAS 1 minute Through 14,000 ft (210 KIAS)*', 'FOM 5.5.15 Table', 'FOM'),
    box('Above 14,000 ft · 265 KIAS · 1 1/2 minutes', '', 'B', False, 'Above 14,000 ft 265 KIAS 1 1/2 minutes', 'FOM 5.5.15 Table', 'FOM'),
    box('Higher speed for turbulence, icing or configuration · advise ATC', 'pattern protection 280 KIAS / M 0.8 whichever is lower', 'B', False,
        'If higher airspeed is required for turbulence, icing, or aircraft configuration, advise ATC. Holding pattern protection is based on a maximum of 280 KIAS/Mach 0.8, whichever is lower.', 'FOM 5.5.15', 'FOM'),
    box('Speed reduction no earlier than 3 minutes before the fix · standard pattern right turns', '', 'B', False,
        'Flights anticipating holding at an enroute fix or flights that have not received clearance beyond a fix should begin a speed reduction no earlier than three minutes prior to reaching such fix.', 'FOM 5.5.15', 'FOM'),
    box('Dispatch notification · holding fix, EFC time, fuel on board · holding fuel every 15 minutes', '', 'C', False,
        'Through ACARS or radio, the Captain will ensure that Dispatch is contacted with the holding fix, Expected Further Clearance (EFC) time, and fuel on board. Diversion plans should be discussed if applicable.', 'FOM 5.5.15.1', 'FOM'),
    box('Clearance limit reached without further clearance · hold at the last assigned level, standard pattern if none published', 'except radio failure and NAT HLA', 'B', False,
        'Except in the event of two-way radio communications failure, and except during NAT HLA operations, if the clearance limit is reached before further instructions have been received, published holding procedures shall be carried out at the last assigned flight level.', 'FOM 5.5.15.3', 'FOM'),
  ], 'FOM 5.5.15'),
  S('CONFIGURATION AND SPEED (FCTM)', GREEN, [
    box('Clean configuration is optimum · CONF 1 when required', '', 'B', False,
        'Clean configuration is the optimum configuration for a holding circuit. When required (holding pattern or speed limitation), the flight crew may consider the selection of CONF 1.', 'FCTM PR-NP-SP-20-00020413.0001001', 'FCTM'),
    box('Clean · fly green dot', 'optimizes lift-to-drag', 'B', False,
        'In clean configuration, the flight crew should fly at Green Dot speed, in order to optimize the Lift-to-Drag ratio.', 'FCTM PR-NP-SP-20-00020413.0001001', 'FCTM'),
  ], 'FCTM PR-NP-SP-20'),
  S('FMS HOLD', NAVY, [
    fmc('F-PLN key · LAT REV · HOLD prompt', 'CHECK the HOLDING data and MODIFY · CHECK the temporary F-PLN and INSERT', 'PF',
        'PRESS the F-PLN key. SELECT the lateral revision page. SELECT the HOLD prompt. CHECK the HOLDING data, and MODIFY it if necessary. CHECK the temporary flight plan and INSERT the holding pattern in it.', 'PRO-NOR-SRP-01-60-00002499.0001001'),
    note('Holding fix close to DECEL with managed speed: manually activate the approach phase so the target becomes VAPP (FCOM).'),
  ], 'FCOM PRO-NOR-SRP-01-60'),
]))

# ---------------------------------------------------------------- MEMORY ITEMS (from memory_items_drill.json, verbatim)
import re, html as _html
def strip_html(s):
    s = re.sub(r'</?(b|i)>', '', s)
    return _html.unescape(s)
MEM_EXT = {}  # ident -> (ext, quote) proven lines from the extracts
MEM_QUOTE = {
  'PRO-ABN-MISC-00012261.0001001': ('FCOM', 'CREW OXY MASKS ... USE SIGNS ... ON EMER DESCENT ... INITIATE If A/THR not active: THR LEVERS ... IDLE SPD BRK ... FULL'),
  'PRO-ABN-MISC-00013664.0002001': ('FCOM', 'NOSE DOWN PITCH CONTROL ... APPLY This will reduce angle of attack'),
  'PRO-ABN-MISC-00013665.0002001': ('FCOM', 'If stall warnings trigger at liftoff, apply the following immediate actions: THRUST ... TOGA At the same time: PITCH ATTITUDE ... 15 ° BANK ... WINGS LEVEL'),
  'ABN-23-A-00017854.0001001': ('QRH', 'If the safe conduct of the flight is impacted AP ... OFF A/THR ... OFF FD ... OFF PITCH/THRUST Below THRUST RED ALT ... 15° / TOGA Above THRUST RED ALT and Below FL 100 ... 10° / CLB Above THRUST RED ALT and Above FL 100 ... 5° / CLB'),
  'PRO-ABN-BRAKES-00010803.0001001': ('FCOM', 'If no braking: REV ... MAX'),
  'PRO-ABN-SURV-AA-00026795.0001001': ('FCOM', 'During night or IMC conditions: Simultaneously: AP ... OFF PITCH ... PULL UP Pull up to full backstick and maintain in that position. THRUST LEVERS ... TOGA SPEED BRAKE LEVER ... CHECK RETRACTED BANK ... WINGS LEVEL or ADJUST'),
  'PRO-ABN-SURV-00026799.0001001': ('FCOM', 'Simultaneously: AP ... OFF PITCH ... PULL UP Pull up to full backstick and maintain in that position. THRUST LEVERS ... TOGA SPEED BRAKE LEVER ... CHECK RETRACTED BANK ... WINGS LEVEL or ADJUST'),
  'PRO-ABN-SURV-00025042.0001001': ('FCOM', 'Do not perform a maneuver based on a TA alone.'),
  'PRO-ABN-SURV-00011464.0005001': ('FCOM', 'All RA, except any CLIMB RA during approach in CONF 3 or FULL: AP (if engaged) ... OFF BOTH FDs ... OFF Respond promptly and smoothly. VERTICAL SPEED ... ADJUST or MAINTAIN'),
  'PRO-ABN-SURV-00012300.0001001': ('FCOM', 'After V1: THR LEVERS ... TOGA REACHING VR ... ROTATE SRS ORDERS ... FOLLOW'),
}
mem_items = []
for m in MEM:
    steps = []
    for s in m['steps']:
        h = strip_html(s['h'])
        if s['t'] == 'n': steps.append(f"{s['n']} {h}")
        else: steps.append(h)
    ext, q = MEM_QUOTE[m['ident']]
    mem_items.append(box(m['name'], ' · '.join(steps), 'B', True, q, m['ident'], ext))
# Ryan's memorization set (his notes, 2026-09-22): the recite-cold wording is his; every card carries the FCOM/QRH ident it
# comes from, and a "FCOM:" bullet wherever his wording drops or changes something the manual says. The full verbatim
# set stays in memory-items.html (the drill page) and data/memory_items_drill.json.
RYAN_MEM_SET = []   # drill-schema copy of the cards for memory-items.html "My notes" mode (data/memory_items_myset.json)
def rmi(name, steps, ident, ext, q, fcom=None):
    sub = ' · '.join(steps) + (' · FCOM: ' + fcom if fcom else '')
    RYAN_MEM_SET.append({'id': 'rm-' + re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-'), 'name': name, 'ref': ext + ' ' + ident, 'ident': ident, 'cond': '',
        'steps': [{'t': 'n', 'n': str(i + 1), 'h': _html.escape(x)} for i, x in enumerate(steps)] + ([{'t': 'b', 'h': 'FCOM: ' + _html.escape(fcom)}] if fcom else []),
        'fctm': 'Ryan\'s wording (2026-09-22); the FCOM verbatim item is on the FCOM set.'})
    return box(name, sub, 'B', True, q, ident, ext)
ryan_mem = [
  rmi('LOSS OF BRAKING', ['Reverse ... MAX', 'Brake pedals ... RELEASE', 'A/SKID & N/W STEERING ... ORDER OFF', 'Brakes ... PRESS (max 1 000 PSI)', 'Parking brake ... USE'],
      'PRO-ABN-BRAKES-00010803.0001001', 'FCOM', 'If no braking: REV ... MAX'),
  rmi('EMER DESCENT', ['Crew oxygen masks ... USE', 'Signs ... ON', 'Emer descent ... INITIATE: turn and pull (ALT 10 000 or MEA/MORA, HDG, SPD 300)', 'Thrust levers ... IDLE if no A/THR', 'Speed brake ... FULL', 'Confirm FMA'],
      'PRO-ABN-MISC-00012261.0001001', 'FCOM', 'CREW OXY MASKS ... USE SIGNS ... ON EMER DESCENT ... INITIATE If A/THR not active: THR LEVERS ... IDLE SPD BRK ... FULL',
      'the five memory items end at SPD BRK FULL; SPD 300 is your technique, the FCOM line once established is SPEED ... MAX/APPROPRIATE, and MAX FL 100 / MEA-MORA'),
  rmi('STALL RECOVERY', ['Nose down pitch ... APPLY', 'Bank ... WINGS LEVEL', 'Thrust ... INCREASE', 'Speedbrakes ... CHECK RETRACTED', 'Flight path ... RECOVER', 'Below FL 200 ... FLAPS 1'],
      'PRO-ABN-MISC-00013664.0002001', 'FCOM', 'NOSE DOWN PITCH CONTROL ... APPLY This will reduce angle of attack',
      'THRUST ... INCREASE SMOOTHLY AS NEEDED and FLIGHT PATH ... RECOVER SMOOTHLY (the word smoothly is in both lines)'),
  rmi('STALL WARNING AT LIFTOFF', ['Thrust ... TOGA', 'Pitch ... 15°', 'Bank ... WINGS LEVEL'],
      'PRO-ABN-MISC-00013665.0002001', 'FCOM', 'If stall warnings trigger at liftoff, apply the following immediate actions: THRUST ... TOGA At the same time: PITCH ATTITUDE ... 15 ° BANK ... WINGS LEVEL'),
  rmi('UNRELIABLE SPEED INDICATION', ['AP ... OFF', 'A/THR ... OFF', 'FD ... OFF', 'PITCH / THRUST: below THRUST RED ALT ... 15° / TOGA', 'between THRUST RED ALT and FL 100 ... 10° / CLB', 'above FL 100 ... 5° / CLB', 'FLAPS (CONF 0, 1, 2, 3) ... MAINTAIN CONF', 'FLAPS (CONF FULL) ... CONF 3', 'Speed brakes ... CHECK RETRACTED', 'Landing gear ... UP'],
      'ABN-23-A-00017854.0001001', 'QRH', 'If the safe conduct of the flight is impacted AP ... OFF A/THR ... OFF FD ... OFF',
      'the QRH condition is "if the safe conduct of the flight is impacted"; when at or above MSA or circuit altitude, level off for troubleshooting'),
  rmi('SMOKE / FUMES / AVNCS SMOKE', ['Crew oxygen masks ... USE / 100 % / EMERG'],
      'ABN-24-A-00010507.0001001', 'QRH', 'CREW OXY MASKS (if required)..... USE/100%/EMERG',
      'listed as [MEM] SMOKE / FUMES / AVNCS / MD SMOKE (refer to QRH); the QRH line reads CREW OXY MASKS (if required)'),
  rmi('EGPWS (TAWS WARNING)', ['“PULL UP, TOGA”', 'AP ... OFF', 'Pitch ... PULL UP', 'Thrust levers ... TOGA', 'Speed brake ... CHECK RETRACTED', 'Bank ... WINGS LEVEL', 'DO NOT CHANGE CONFIGURATION UNTIL CLEAR'],
      'PRO-ABN-SURV-00026799.0001001', 'FCOM', 'Simultaneously: AP ... OFF PITCH ... PULL UP Pull up to full backstick and maintain in that position. THRUST LEVERS ... TOGA SPEED BRAKE LEVER ... CHECK RETRACTED BANK ... WINGS LEVEL or ADJUST',
      'BANK ... WINGS LEVEL or ADJUST; the same five items are the TAWS CAUTION response at night or in IMC'),
  rmi('TCAS WARNING (RA)', ['“TCAS, I have control”', '“Hawaiian 50, TCAS RA”', 'AP ... OFF', 'FD ... OFF (both)', 'Vertical speed ... ADJUST or MAINTAIN (fly the green band)', 'CLIMB RA in CONF 3 or FULL ... GO-AROUND', '“Hawaiian 50, clear of conflict”'],
      'PRO-ABN-SURV-00011464.0005001', 'FCOM', 'All RA, except any CLIMB RA during approach in CONF 3 or FULL: AP (if engaged) ... OFF BOTH FDs ... OFF Respond promptly and smoothly. VERTICAL SPEED ... ADJUST or MAINTAIN',
      'the third memory item is VERTICAL SPEED ... ADJUST or MAINTAIN; a CLIMB RA on approach in CONF 3 or FULL is GO-AROUND ... PERFORM; ATC ... NOTIFY during the RA and again when clear'),
  rmi('WINDSHEAR', ['Takeoff before V1 ... REJECT', 'After V1: “WINDSHEAR, TOGA” ... TOGA, ROTATE, FOLLOW SRS', 'Airborne or landing: TOGA (set or confirm) · AP (if engaged) KEEP ON · FOLLOW SRS', 'DO NOT CHANGE CONFIGURATION UNTIL CLEAR', 'Landing: “WINDSHEAR AHEAD” (predictive) ... “GO AROUND, FLAPS”', '“WINDSHEAR WINDSHEAR” (reactive) ... “WINDSHEAR, TOGA”'],
      'PRO-ABN-SURV-00012300.0001001', 'FCOM', 'After V1: THR LEVERS ... TOGA REACHING VR ... ROTATE SRS ORDERS ... FOLLOW',
      'airborne or at landing the items are THR LEVERS AT TOGA ... SET OR CONFIRM, AP (if engaged) ... KEEP ON, SRS ORDERS ... FOLLOW; carefully monitor flight path and speed, recover the normal climb smoothly when out of windshear'),
  rmi('OCEANIC ENGINE OUT (PRC, not a [MEM] item)', ['Set MCT, disconnect A/THR', 'Pull speed ... 0.80 / 270', 'Pull HDG 30° away from traffic, parallel course 5 NM', 'Pull FL 200', 'Start APU', 'PRC back page to fine tune'],
      'PRC Engine Failure During Cruise', 'PRC', 'SIMULTANEOUSLY, SET MCT AND DISCONNECT AUTOTHRUST',
      'the PRC says PULL SPEED - GREEN DOT initially, then ADJUST SPEED 300 kt / M0.78 for ETOPS and standard strategy (not 0.80 / 270); turn at least 30° for the 5 NM offset; PULL FL 200; START APU; declare MAYDAY'),
]
PH.append(P('memory-items', 'Memory Items', 'a', 'MEMORY ITEMS (recite cold)', 'Ryan\'s notes · FCOM PRO-ABN · QRH R35 · [MEM]', [
  S('MEMORY ITEMS · YOUR NOTES (FCOM differences flagged)', RED, ryan_mem, 'FCOM PRO-ABN · QRH · PRC'),
  S('[MEM] ITEMS NOT IN YOUR NOTES', SLATE, [
    box('TAWS CAUTION', 'night or IMC: same five actions as the warning · day VMC with terrain in sight: FLIGHT PATH ... ADJUST · SINK RATE, DON’T SINK, TOO LOW GEAR/FLAPS, GLIDESLOPE: adjust flight path, go-around when below 1 000 ft AAL IMC / 500 ft AAL VMC or when configuration is wrong', 'B', False,
        'During night or IMC conditions: Simultaneously: AP ... OFF PITCH ... PULL UP Pull up to full backstick and maintain in that position. THRUST LEVERS ... TOGA SPEED BRAKE LEVER ... CHECK RETRACTED BANK ... WINGS LEVEL or ADJUST', 'PRO-ABN-SURV-AA-00026795.0001001', 'FCOM'),
    box('TCAS CAUTION (TA)', 'no maneuver on a TA alone', 'B', False, 'Do not perform a maneuver based on a TA alone.', 'PRO-ABN-SURV-00025042.0001001', 'FCOM'),
  ], 'FCOM PRO-ABN-SURV'),
]))

# ---------------------------------------------------------------- LIMITATIONS (mem set from limitations_drill.json)
def lim_quote(src):
    # drill src is "<verbatim line> [<ident>]"; strip the trailing ident bracket for the literal quote
    m = re.match(r'^(.*?)\s*\[([^\]]+)\]\s*$', src, re.S)
    return (m.group(1), m.group(2)) if m else (src, '')
sys.path.insert(0, os.path.join(WORK, 'build_scripts')); import verify_phase_flows as V
LIM_DROPPED = []
lim_secs = {}
order = []
for x in LIM:
    if not x.get('mem'): continue
    if x.get('fleet', 'pax') not in ('pax', 'both'): continue   # PAX phase flows: the freighter drill cards (fleet toggle, 2026-09-17) stay out (audit 2026-09-22)
    sec = x['s']
    if sec not in lim_secs: lim_secs[sec] = []; order.append(sec)
    q, ident = lim_quote(x['src'])
    # quotes are proven against the full FCOM extract; a few drill records cite the AFM or a chart (no text); those keep the answer only
    quotable = x['ref'].startswith('FCOM') and 'AFM' not in x['ref'] and not q.startswith('[') and V.norm(q) in V.extract('FCOM')
    if not quotable: LIM_DROPPED.append((x['id'], x['ref']))
    lim_secs[sec].append(box(x['q'].rstrip('?'), x['a'], 'B', False, q if quotable else '', (ident or x['ref']) if quotable else '', 'FCOM'))
LIM_COLORS = [RED, TEAL, NAVY, GREEN, PURP, GOLD, PLUM, BLUE, CYAN, FOREST, VIOLET, AMBER, BROWN, OCEAN, SLATE, RED, TEAL, NAVY]
# Ryan's memorization set (HAL A330 Limitations Summary Rev 13, his notes, 2026-09-22): the structure and the short
# wording are his; every value is the FCOM R17 figure in pounds for the 238 t (-200 PAX) weight variant, and each line
# keeps the FCOM quote of the drill card it maps to. Four lines corrected to the FCOM (MZFW variant note, fuel
# imbalance, F-G/S 200 ft, autoland envelope); seven Rev 13 lines that are not FCOM limitations were dropped with his
# approval (gear extension FL210, -0.26 psi, hydraulic 3 000 psi, APU 41 450 ft, speedbrakes, dimensions, approach
# category). The full FCOM card set stays in limitations.html and data/limitations_drill.json.
LIMBY = {x['id']: x for x in LIM}
RYAN_LIM_IDS = []   # drill cards that make up the Rev 13 set (data/limitations_myset.json)
def L(cid, title, value, note=''):
    RYAN_LIM_IDS.append(cid)
    x = LIMBY[cid]; q, ident = lim_quote(x['src'])
    quotable = x['ref'].startswith('FCOM') and 'AFM' not in x['ref'] and not q.startswith('[') and V.norm(q) in V.extract('FCOM')
    return box(title, value + (' · ' + note if note else ''), 'B', False, q if quotable else '', (ident or x['ref']) if quotable else '', 'FCOM')
def LQ(title, value, q, ident, note=''):
    return box(title, value + (' · ' + note if note else ''), 'B', False, q, ident, 'FCOM')
LIM_LINK = 'https://drive.google.com/file/d/1pZA4z9jN4xrqZ8zRsfyJsOKVL0fZLKZM/view'  # Ryan's HAL A330 Limitations Summary Rev 13 on Drive (training/); the PDF stays out of the public repo
LIM_PDF = ''
ryan_lim = [
  S('WEIGHTS · LOAD · ENVELOPE', RED, [
    note("<a href='" + (LIM_PDF or LIM_LINK) + "' target='_blank' rel='noopener' style='font-weight:800;color:var(--accent);text-decoration:none;border:1.4px solid var(--accent);border-radius:6px;padding:2px 9px;'>Limitations Summary Rev 13 (PDF) &#9656;</a>"),  # single quotes: the page's boldCO turns double quotes into callouts
    L('lim-wght-01', 'Max taxi weight (MTW)', '527k lb'),
    L('lim-wght-02', 'Max takeoff weight (MTOW)', '525k lb'),
    L('lim-wght-03', 'Max landing weight (MLW)', '401k lb'),
    L('lim-wght-04', 'Max zero fuel weight (MZFW)', '370k lb', 'FCOM: 375k lb on the 236 t tails'),
    L('lim-fctl-01', 'Load factor, clean', '-1.0 g to +2.5 g'),
    L('lim-fctl-02', 'Load factor, other configurations', '0 g to +2.0 g'),
    L('lim-afm-03', 'Max altitude', '41 450 ft'),
    L('lim-add-01', 'Max runway altitude', '12 500 ft'),
  ], 'FCOM LIM-AG'),
  S('AIRPORT OPERATIONS', TEAL, [
    L('lim-acgen-02', 'Max runway slope', '±2 %'),
    L('lim-acgen-04', 'Max takeoff crosswind', '32 kt (gust included)'),
    L('lim-acgen-06', 'Max takeoff tailwind', '15 kt'),
    L('lim-acgen-05', 'Max landing crosswind', '45 kt (gust included)'),
    L('lim-acgen-07', 'Max landing tailwind', '10 kt'),
    L('lim-acgen-08', 'Max wind to operate passenger / cargo doors', '40 kt (50 kt nose into wind)'),
    L('lim-acgen-10', 'Max wind with passenger / cargo doors open', '60 kt'),
  ], 'FCOM LIM-AG-OPS'),
  S('SPEEDS', NAVY, [
    L('lim-afm-01', 'VMO / MMO', '330 kt / M 0.86'),
    L('lim-spd-03', 'VFE flap 1 (1+F)', '240 kt (215 kt)'),
    L('lim-spd-06', 'VFE flap 2 (1*)', '196 kt (205 kt)'),
    L('lim-spd-07', 'VFE flap 3', '186 kt'),
    L('lim-spd-08', 'VFE flap FULL', '180 kt'),
    L('lim-fctl-03', 'Max altitude with flaps / slats extended', 'FL 200'),
    L('lim-spd-10', 'VLE / VLO', '250 kt / M 0.55'),
    L('lim-spd-12', 'VLE gravity gear extension', '200 kt'),
    L('lim-spd-16', 'Max windshield wiper speed', '230 kt'),
    L('lim-spd-01', 'Max cockpit window open speed', '230 kt'),
  ], 'FCOM LIM-AG-SPD'),
  S('CABIN PRESSURE · AIR', GREEN, [
    L('lim-air-03', 'Max positive differential', '9.25 psi'),
    L('lim-air-04', 'Max negative differential', '-0.73 psi'),
    L('lim-air-05', 'Safety relief valve setting', '8.85 psi'),
    L('lim-air-08', 'Air conditioning with LP ground unit', 'do not use packs'),
    L('lim-air-02', 'Air conditioning with HP ground unit', 'do not use APU bleed'),
  ], 'FCOM LIM-AIR'),
  S('AUTO FLIGHT', PURP, [
    L('lim-afs-02', 'AP minimum height: takeoff', '100 ft AGL (and 5 s after liftoff)'),
    L('lim-afs-04', 'AP minimum height: approach, not ILS (FINAL APP, V/S, FPA)', '250 ft AGL'),
    L('lim-afs-03', 'AP minimum height: approach with F-G/S', '200 ft AGL', 'FCOM line not on the Rev 13 card'),
    L('lim-afs-06', 'AP minimum height: ILS when CAT 2 or CAT 3 not displayed', '160 ft AGL'),
    L('lim-afs-10', 'AP minimum height: go-around', '100 ft AGL'),
    L('lim-afs-11', 'AP minimum height: all other phases', '500 ft AGL'),
    L('lim-afs-27', 'Max autoland headwind', '35 kt'),
    L('lim-afs-28', 'Max autoland tailwind', '10 kt'),
    L('lim-afs-29', 'Max autoland crosswind', '15 kt'),
    L('lim-afs-30', 'Autoland configuration', 'CONF 3 or CONF FULL'),
    L('lim-afs-31', 'Autoland demonstrated envelope', 'glideslope -2.5° to -3.25° · airfield below 9 200 ft · weight above 256k lb', 'FCOM lines not on the Rev 13 card'),
  ], 'FCOM LIM-AFS'),
  S('FUEL', GOLD, [
    L('lim-fuel-07', 'Max fuel imbalance, outer tanks (inner balanced)', '3k lb at full'),
    L('lim-fuel-06', 'Max fuel imbalance, inner tanks (outer balanced)', '6k lb at full', 'FCOM: rises to 11k lb at 37k lb per tank; the Rev 13 card listed only the outer figure'),
    L('lim-fuel-02', 'Max fuel temperature, JET A / A1', '+55 °C'),
    L('lim-fuel-04', 'Min fuel temperature, inner tank', '-44 °C below 30 000 ft · -54 °C above'),
    L('lim-fuel-09', 'Min fuel quantity for takeoff', '11k lb'),
  ], 'FCOM LIM-FUEL'),
  S('LANDING GEAR · IRS · OXYGEN', PLUM, [
    L('lim-lg-02', 'Max brake temperature for takeoff', '300 °C'),
    LQ('Nosewheel steering angle', '72°', 'The steering handwheels control the nosewheel steering angle up to ±72 ° in either direction.', 'DSC-32-50 (system description)'),
    L('lim-lg-03', 'Braked pivot turns (one main gear fully stopped)', 'not allowed'),
    L('lim-lg-06', 'Max taxi speed, one tire deflated per gear', '7 kt'),
    L('lim-lg-07', 'Max taxi speed, two tires deflated on one gear', '3 kt'),
    L('lim-add-02', 'IRS navigation without GPS (RNP-10)', '6.2 h from alignment'),
    LQ('Min oxygen pressure, 2 crew + 2 observers at 50 °C', '1 000 psi', '2 Crewmembers + 2 OBS 810 850 880 910 940 970 1 000', 'LIM-OXY-00020209.0004001', '2 crew alone: 520 to 640 psi over -10 to 50 °C'),
  ], 'FCOM LIM-LG · LIM-NAV · LIM-OXY'),
  S('APU', BLUE, [
    LQ('LOW OIL LEVEL advisory', 'may start and operate for 15 h', 'The APU may be started and operated for 15 h, if there is no', 'FCOM APU LOW OIL LEVEL'),
    L('lim-apu-01', 'Starter: after 3 consecutive start attempts', 'wait 60 min'),
    L('lim-add-04', 'Max altitude for battery-only start (in flight)', '25 000 ft'),
    L('lim-apu-08', 'Max altitude, one pack bleed and electrics', '22 500 ft'),
    L('lim-apu-07', 'Max altitude, bleed for engine start', '20 000 ft'),
    L('lim-apu-09', 'Max altitude, two pack bleed and electrics', '17 500 ft'),
    L('lim-apu-10', 'Bleed for wing anti-ice', 'not permitted'),
  ], 'FCOM LIM-APU'),
  S('POWER PLANT', CYAN, [
    L('lim-eng-01', 'EGT takeoff and go-around', '920 °C for 20 s · 900 °C for 5 min (10 min with an engine failure)'),
    L('lim-eng-02', 'EGT MCT', '850 °C'),
    L('lim-eng-03', 'EGT starting, ground', '700 °C'),
    L('lim-eng-04', 'EGT starting, in flight', '850 °C'),
    L('lim-eng-10', 'Min oil quantity', '15 qt, or 6 qt + estimated consumption (highest of)'),
    L('lim-eng-12', 'Starter max continuous operation', '5 min'),
    L('lim-eng-14', 'Starter cooling after 5 min continuous or three cycles', '30 min'),
    L('lim-eng-15', 'No running starter engagement above', '10 % N3 ground · 30 % N3 in flight'),
    L('lim-eng-16', 'Reverse selection in flight', 'prohibited'),
    L('lim-eng-17', 'Backing the aircraft with reverse', 'prohibited'),
    L('lim-eng-18', 'Max reverse below 70 kt', 'should not be used'),
    L('lim-eng-19', 'FLEX max temperature', 'ISA + 60 °C'),
    LQ('FLEX min temperature', 'flat rating temperature (TREF) or OAT', 'Lower than the flat rating temperature (TREF).', 'FCOM PRO-NOR-SRP FLEX'),
    L('lim-eng-20', 'FLEX on contaminated runways', 'not permitted'),
  ], 'FCOM LIM-ENG'),
]
PH.append(P('limits', 'Limitations', 'a', 'LIMITATIONS (recite cold)', 'Ryan\'s Rev 13 summary · FCOM LIM R17 · 238 t / -200 PAX · pounds', ryan_lim))

# ============================================================ CHECKLISTS (flows.json, roles PF/PM/BOTH -> PF/PM/B)
CL_TRIG = {
  'Cockpit Preparation': ('PR-NP-CL-00024935.0001001', ''),
  'Before Start': ('PR-NP-CL-00024936.0001001', 'Checklist trigger: - Pushback clearance or start clearance received, and - Before Start flow pattern completed.'),
  'After Start': ('PR-NP-CL-00024937.0001001', 'Checklist trigger: On hand signal (salute) from the ground personnel.'),
  'Taxi': ('PR-NP-CL-00024938.0005001', 'Checklist trigger: - T.O. CONFIG pb pressed, and - Takeoff Advisory PA complete (if applicable).'),
  'Line-Up': ('PR-NP-CL-00024939.0001001', 'Checklist trigger: - Line-up clearance received - Line-Up flow pattern completed.'),
  'Departure Change': ('PR-NP-CL-00024940.0001001', 'Checklist trigger: Revised departure briefing completed.'),
  'Approach': ('PR-NP-CL-00024941.0001001', 'Checklist trigger: - Below 10 000 ft AAL and barometric reference set, or - After the approach briefing is completed, for the case when not leaving the terminal area or climbing above 10 000 ft AAL (Case of an Air Turn Back or Traffic Pattern or Go Around)'),
  'Landing': ('PR-NP-CL-00024942.0002001', 'Checklist trigger: LDG CONF set.'),
  'After Landing': ('PR-NP-CL-00024943.0002001', 'Checklist trigger: After Landing Flow pattern completed.'),
  'Parking': ('PR-NP-CL-00024944.0001001', 'Checklist trigger: After Parking flow pattern completed.'),
  'Securing the Aircraft': ('PR-NP-CL-00024945.0001001', ''),
}
CHECKLISTS = {}
for name, c in FLOWS['checklists'].items():
    ref, q = CL_TRIG[name]
    CHECKLISTS[name] = {'items': [[i['challenge'], i['response'], ROLE[i['who']]] for i in c['items']],
                        'src_card': c['src'], 'ref': 'FCTM ' + ref, 'quote': q, 'ext': 'FCTM', 'fleet': 'pax', 'src': 'manual'}

# ============================================================ NOTES (quick reference panel)
NOTES = [
  {'k': 'ol', 'h': 'CHECKLISTS IN ORDER', 'ec': NAVY, 'items': ['Cockpit Preparation', 'Before Start', 'After Start', 'Taxi', 'Line-Up', '(Departure Change)', 'Approach', 'Landing', 'After Landing', 'Parking', 'Securing the Aircraft'],
   'ref': 'FCTM PR-NP-CL', 'ext': 'FCTM', 'quote': 'NORMAL CHECKLISTS', 'fleet': 'pax', 'src': 'manual'},
  {'k': 'c', 'h': 'CHECKLIST TRIGGERS', 'ec': PURP, 'items': [
     '<b>Cockpit Preparation</b>: Departure Briefing complete', '<b>Before Start</b>: push/start clearance and flow complete', '<b>After Start</b>: salute received',
     '<b>Taxi</b>: T.O CONFIG pb pressed, Takeoff Advisory PA complete', '<b>Line-Up</b>: line-up clearance and flow complete', '<b>Approach</b>: below 10 000 ft AAL and baro ref set',
     '<b>Landing</b>: LDG CONF set', '<b>After Landing</b>: flow complete', '<b>Parking</b>: flow complete'],
   'ref': 'FCTM PR-NP-CL', 'ext': 'FCTM', 'quote': 'Checklist trigger: LDG CONF set.', 'fleet': 'pax', 'src': 'manual'},
  {'k': 'c', 'h': 'EXTERIOR LIGHTS (PF, or PM at PF request)', 'ec': CYAN, 'items': [
     '<b>Cockpit Prep</b>: Strobes AUTO, Nav 1, all others OFF', '<b>Before Push</b>: Beacon ON', '<b>Taxi</b>: Nose TAXI, Rwy Turnoff ON', '<b>Crossing a runway</b>: Strobes ON, Land ON',
     '<b>Line up and wait</b>: Strobes ON', '<b>Cleared for takeoff</b>: Nose T.O, Land ON', '<b>After takeoff (PM)</b>: Nose OFF, Rwy Turnoff OFF', '<b>Climbing 10 000 ft (PM)</b>: Land OFF',
     '<b>Descending 10 000 ft (PM)</b>: Land ON', '<b>Cleared for approach (PM)</b>: Nose TAXI, Rwy Turnoff ON', '<b>Cleared to land (PM)</b>: Nose T.O', '<b>After landing</b>: Land OFF, Strobes AUTO, Nose TAXI', '<b>Parking</b>: all OFF except Nav 1'],
   'ref': 'FCOM PRO-NOR-SOP-21-A-00011013.0001001 · quickref', 'ext': 'FCOM PRO-NOR', 'quote': 'When leaving the runway: LAND LIGHT sw ... OFF PF WING sw ... OFF PF STROBE sw ... AUTO PF NOSE sw ... TAXI PF', 'fleet': 'pax', 'src': 'technique'},
  {'k': 'c', 'h': 'CABIN PAs (PM)', 'ec': '#c05621', 'items': [
     'Takeoff, no less than 2 min prior: <b>“[FLIGHT ATTENDANTS SHOULD NOW] BE SEATED FOR TAKEOFF”</b>',
     'No later than 18 000 ft: <b>“[Flight Attendants], please prepare the cabin for arrival and be seated for landing.”</b>',
     'Seat belt sign OFF first time after takeoff: Seat Belt Advisory PA (FOM)'],
   'ref': 'FCOM PRO-NOR-SOP-10 / SOP-17', 'ext': 'FCOM PRO-NOR', 'quote': '"[Flight Attendants], please prepare the cabin for arrival and be seated for landing."', 'fleet': 'pax', 'src': 'manual'},
  # TAKEOFF CALLOUTS, APPROACH GATES, LANDING CALLOUTS and the go-around / cancel approach / reject trigger lines were dropped from NOTES (Ryan, 2026-09-22); the callouts live in their phases
]

# ---------------------------------------------------------------- SIM NOTES (Ryan's own notes, 2026-09-22; technique, not manual text)
def sn(t, steps, r='B', call=False): return box(t, ' · '.join(steps), r, call, '', '', 'FCOM', 'technique')
PH.append(P('sim-notes', 'SIM Notes', 'a', 'SIM NOTES (technique)', 'Ryan\'s sim notes · not manual text', [
  S('V1 CUT', RED, [
    sn('Call “ENGINE FAILURE”', ['stay on the runway: focus on the centerline, straighten, lock the rudders'], 'PF', True),
    sn('Rotate smooth, elbow and arm not wrist', ['rotate to 12.5°', 'wait for SRS guidance', 'count to 5, then slowly release pressure on the stick']),
    sn('Positive rate, gear up', ['trim the rudder toward the good engine: count to 8', 'control heading with bank, use rudder to center the beta target']),
    sn('Autopilot ON', ['pull heading (“259 on LAS 26”) or RW track', 'fly the special EO procedure']),
    sn('“MAYDAY MAYDAY MAYDAY, Hawaiian 50, engine failure, turning right heading 010”', [], 'PM', True),
    sn('1 000 ft above field: MCDU engine-out acceleration altitude', ['clean up', 'at green dot PULL ALT', 'thrust lever back, then forward to MCT']),
    sn('ECAM sequence', ['ECAM actions', 'STATUS, “STOP ECAM”', 'OEBs', 'QRH summaries', 'computer resets', 'diamond checks', '“CONTINUE ECAM”', 'remove status', '“ECAM ACTIONS COMPLETE”']),
    sn('Landing performance', ['get weather, decide where to go', 'the reference speed the sim asks for (V-REF) is the CONF FULL VLS number']),
    sn('Declare the emergency', ['souls on board, fuel on board', 'talk to your five: ATC, FAs, company, PAX, other pilot', 'TEST: Type of situation, Evacuation likely, Signal to remain seated or evacuate, Time to landing']),
    sn('Fly the single engine arrival and land', []),
  ], 'sim notes'),
  S('GO-AROUND', AMBER, [
    sn('“GO AROUND, FLAPS”', ['TOGA, pitch up', 'read the FMA slowly (huge power change)', 'positive rate, GEAR UP, set the missed approach altitude'], 'PF', True),
    sn('400 ft: manage NAV or pull HDG', ['AP ON', '1 000 ft: push ALT', 'clean up', 'diamond checks', 'PULL SPEED 200, flaps 1', 'exit the GA phase: activate the approach or change destination']),
    sn('Bounced landing', ['“GO AROUND, FLAPS” (no bounce TOGA any more)', 'FCTM PR-NP-SOP-250: light bounce, keep the pitch and land with thrust idle · high bounce, keep the pitch and go around; retract flaps one step and the gear only when established · never pitch up to soften the second touchdown'], 'PF', True),
  ], 'sim notes'),
  S('HOLDING · SLOPE · APPROACH', GOLD, [
    sn('Hold speeds, international (works domestic too)', ['below 6 000 ft: 200 kt', '6 000 to 14 000 ft: 220 kt', 'above 14 000 ft: 240 kt', 'FOM 5.5.15 (US): maximums 200 / 230 (210 where charted) / 265 KIAS; your 220 and 240 sit inside them']),
    sn('Runway slope', ['(difference between end elevations / runway length) x 100']),
    sn('Cleared for the approach: set the FAF altitude immediately', []),
    sn('NPA LOC FPA', ['cleared: set the FAF altitude and descend in the safe area', 'do not set the MDA in the window', 'V/S -700 if needed, FPA -3.0 to get down']),
    sn('Specials', ['simple special: a turn below 1 000 ft (hard tune the VOR if it is based on it, or the DME drops out at 1 000 ft)', 'complex special: cannot be printed on the TLR, see the HAL Jepp supplement (example PDX)']),
  ], 'sim notes'),
  S('GLIDE INTERCEPTION FROM ABOVE', TEAL, [
    sn('LOC ... CHECK ENGAGED', ['slow down: flaps 1, then 2', 'APPR mode: arm when finally cleared', 'FCU altitude: spin to above the current altitude', 'V/S mode: 1 500 to 2 000 fpm down', 'gear down, flaps 3, then FULL', 'capture the G/S', 'never select -2 000 at or below 2 000 ft; then the max is -1 500', 'FCTM PR-NP-SOP-190: only when established on the LOC · gear down and at least CONF 2 before · APPR pb, confirm G/S armed and LOC engaged · FCU altitude above the aircraft · V/S 1 500 initially, above 2 000 the speed runs toward VFE · go-around altitude set at G/S*']),
  ], 'sim notes'),
  S('TCAS · STALL', PLUM, [
    sn('“TCAS, I have control”', ['TA/RA: “Hawaiian 50, TCAS RA”', 'AP and FD OFF, follow the commands', '“Hawaiian 50, clear of conflict”'], 'PF', True),
    sn('“STALL, I have control”', ['lower the nose to the horizon: 5° below 10 000 ft, 10° higher', 'roll wings level', 'check the speed brake retracted', 'increase thrust smoothly', 'below FL 200: flaps 1', 'help with trim if deep in the stall, to 5', 'stall on takeoff: “STALL, TOGA, 15 DEGREES”', 'FCOM PRO-ABN-MISC: the memory item is NOSE DOWN PITCH CONTROL ... APPLY with no target attitude; the 5° / 10° figures are your technique'], 'PF', True),
  ], 'sim notes'),
  S('FUEL JETTISON · EMERGENCIES · ECAM', VIOLET, [
    sn('Fuel jettison', ['can we land overweight on the available runway?', 'permission and start/stop times to ATC', 'consider a hold with legs longer than 10 NM', 'stay away from thunderstorms', 'descend in the hold if forced to short legs', 'follow the QRH checklist', 'climb above 5 000 ft', 'QRH 19.02A: FMS FUEL PRED page SELECT · JETGW FINAL GW ENTER · T TANK MODE CHECK AUTO · JETTISON ARM ON · JETTISON ACTIVE ON · when complete ACTIVE OFF, ARM OFF']),
    sn('Emergencies, in order', ['OEBs first', 'run the memory items', 'after ECAM actions: computer resets and checklists', 'QRH summaries, then FCOM Vol 3 for anything else pertinent']),
    sn('Slats or flaps jammed', ['PULL SPEED']),
    sn('ECAM (Standard Callouts 3.03.90)', ['ECAM title', 'SOS', 'OEBs, memory items', '“I have control, ECAM actions”', 'complete the ECAM top portion', '“X procedure, APPLY” (do it now when on ECAM)', 'STATUS, “STOP ECAM”', 'QRH, computer resets, FCOM 3', 'situational assessment, decision making', 'do not fly too far from a good airport, slow down', '“CONTINUE ECAM”', 'read STATUS', '“X procedure, APPLY”: landing distance, flap setting, noted and done in prep for landing', '“ECAM ACTIONS COMPLETE”']),
  ], 'sim notes'),
]))

json.dump({'ids': RYAN_LIM_IDS, 'label': 'Rev 13 set', 'source': 'HAL A330 Limitations Summary Rev 13, values FCOM R17'}, open(os.path.join(WORK, 'data', 'limitations_myset.json'), 'w', encoding='utf-8'), indent=0)
json.dump(RYAN_MEM_SET, open(os.path.join(WORK, 'data', 'memory_items_myset.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)

# ============================================================ fleet/src on every record, then write
for ph in PH:
    for sec in ph['sections']:
        for it in sec['items']:
            it.setdefault('fleet', 'pax'); it.setdefault('src', 'manual' if it['k'] in ('box', 'fmc', 'cl') else 'sop'); it['provenance'] = it['src']
OUT = {
  'meta': {'title': 'A330 Phase Flows', 'fleet': 'pax', 'generated': '2026-09-16',
           'sources': 'A330P FCOM R17 PRO-NOR / PRO-ABN / PRO-NOR-SUP-SEC; QRH R35 22.02A; FCTM R6 PR-NP-CL, PR-AEP; FOM 125.3 5.5.15, 5.7.4, 6.3, 6.4, 11.2; PRC 8/31/26 p1, p2; FCOM PRO-SPO-40A',
           'builders': 'box(t,s,r,call,q) fmc(t,s,r,q) sub(t,c) trig(t,r) cl(t,w,bold,cc) book(t,s) note(t) S(h,c,items,cite,appr); q = quote + [ref]',
           'roles': 'C=CM1 (CA seat) F=CM2 (FO seat) PF PM B=both; appr: all | ILS | ILScat (CAT II/III) | RNP | NPA',
           'normal_source': 'data/flows.json (quickref order and role) cross-checked to FCOM PRO-NOR idents; quotes are literal extract text'},
  'phases': PH, 'checklists': CHECKLISTS, 'quotes': {}, 'notes': NOTES,
}
json.dump(OUT, open(os.path.join(WORK, 'data', 'phase_flows.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
n = sum(len(s['items']) for p in PH for s in p['sections'])
print('phases', len(PH), 'items', n, 'checklists', len(CHECKLISTS), 'notes', len(NOTES))
print('limitations without a literal quote (answer only):', len(LIM_DROPPED), LIM_DROPPED)

# 2026-09-21: apply Ryan's memorization re-cut on top of the generated shapes (idempotent)
import subprocess
subprocess.run([sys.executable, os.path.join(HERE, 'resection_cockpit_prep.py')], check=True)
subprocess.run([sys.executable, os.path.join(HERE, 'gen_flow_memorization.py')], check=True)  # plan page + md from the phase flows (2026-09-22)
