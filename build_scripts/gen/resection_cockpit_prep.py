#!/usr/bin/env python3
"""Re-section the Preflight and Cockpit Prep phases of data/phase_flows.json into Ryan's ten colored
memorization groups (2026-09-21), the same groups and colors as spine_cockpit_prep.py uses for the
Flows Trainer. Items are moved and relabelled only; every quote/ref stays as generated. Run AFTER
gen_phase_flows.py. Idempotent (skips when the TURN IT OFF section already exists).
"""
import json, os, copy
HERE = os.path.dirname(os.path.abspath(__file__)); WORK = os.path.abspath(os.path.join(HERE, '..', '..'))
P = os.path.join(WORK, 'data', 'phase_flows.json')
D = json.load(open(P, encoding='utf-8'))
ph = {p['id']: p for p in D['phases']}
pre, prep = ph['preflight'], ph['cockpit-prep']
if any(s['h'].startswith('TURN IT OFF') for s in pre['sections']):
    print('already re-sectioned'); raise SystemExit
C = {'OFF':'#b03a2e','ON':'#00805E','SET':'#463C8F','BOX':'#CE0C88','PAN':'#B8860B','WALK':'#0F6E8C','BUILD':'#5f3dc4','PF2':'#9c5800','PM3':'#7a3b8f','LEGS':'#831A57'}
cm2, cm1, walk = pre['sections'][1], pre['sections'][2], pre['sections'][3]
allpre = cm2['items'] + cm1['items']
def take(prefix, pool=None):
    pool = allpre if pool is None else pool
    for it in pool:
        if it.get('t', '').startswith(prefix): return copy.deepcopy(it)
    raise KeyError(prefix)
def S(h, c, items, cite='FCOM PRO-NOR-SOP-04'):
    return {'h': h, 'c': c, 'items': items, 'cite': cite, 'appr': 'all', 'mem': True}
note = take('Items marked')
off = [take('ENG masters'), take('Weather radar'), take('L/G lever'), take('Wipers')]
on = [take('Batteries'), take('RMP 1 and 2'), take('APU FIRE'), take('APU start'), take('ADIRS'), take('Cockpit lights'), take('ATIS')]
setup = [take('EFB start'), take('LOGBOOK'), take('OEB'), take('Jeppesen'), take('MCDU ON'), take('RCL pb'), take('AIRCRAFT ACCEPTANCE')]
box = [take('ACARS'), take('Preliminary takeoff perf')]
for it in box: it['r'] = 'PF'
pre['sections'] = [pre['sections'][0],
    S('TURN IT OFF · 4', C['OFF'], [note] + off),
    S('TURN IT ON · 7', C['ON'], on),
    S('SET IT UP · 4', C['SET'], setup),
    S('PF · BOX START · 2', C['BOX'], box)]
# ---- Before Walkaround: split the merged boxes into the ten card items
w = walk['items']
def clone(src, t, s=None):
    it = copy.deepcopy(src); it['t'] = t
    if s is not None: it['s'] = s
    return it
oxy = take('OXY', w); fl = take('FLAPS', w); acc = take('ACCU', w); alt = take('Alternate', w); em = take('EMER', w); rain = take('RAIN', w); pins = take('GEAR PINS', w); trig = [it for it in w if it['k'] == 'trig'][0]
walk10 = [clone(oxy, 'OXY · HYD · ENG OIL (3)'),
          clone(fl, 'FLAPS CHECK POSITION', ''), clone(fl, 'SPEED BRAKE * CHECK RETRACTED and DISARMED', ''),
          clone(acc, 'ACCU PRESS * CHECK', 'in the green band; blue electric pump to recharge if required'), clone(acc, 'PARK BRK * ON', ''), clone(acc, 'BRAKES PRESS * CHECK', ''),
          clone(alt, 'ALTN BRAKING CHECK'), clone(em, 'EMER EQPT CHECK'), clone(rain, 'RAIN RPLNT CHECK PRESSURE and QUANTITY'), clone(pins, 'GEAR PINS (3) * CHECK ONBOARD and STOWED'), copy.deepcopy(trig)]
# ---- Cockpit Preparation groups
cp = prep['sections'][0]['items']
def tk(prefix): return take(prefix, cp)
panels = [tk('Overhead panel'), tk('Front instrument'), tk('Center pedestal')]
build = [tk('FMS preparation · INIT A'), tk('FMS PREPARATION * CROSSCHECK'), tk('Glareshield'), tk('Lateral consoles'), tk('PFD and ND')]
build[0]['t'] = 'A-DIFSRIPP · FMS preparation (PF)'; build[1]['t'] = 'A-DIFSRIPP check · FMS PREPARATION * CROSSCHECK (PM)'
pf2 = [tk('ECAM control panel'), tk('RELEASE VERSION')]
pf2[0]['t'] = 'PRESS · STS · FUEL pb PRESS (ECAM control panel)'; pf2[1]['t'] = 'RLS VERSION / FITNESS / FOB / PDSC ... SENT'
pm3 = [tk('IRS ALIGN'), tk('FUEL ON BOARD'), tk('ATC clearance')]
pm3[1]['r'] = 'PM'
legs = [tk('DEPARTURE LEGS'), tk('DEPARTURE BRIEFING'), [it for it in cp if it['k'] == 'cl'][0]]
legs[1]['t'] = 'DEPARTURE BRIEFING * PERFORM (TRIGGER: Cockpit Preparation checklist)'
cite6 = 'FCOM PRO-NOR-SOP-06'
prep['sections'] = [S('PF · PANELS · 3', C['PAN'], panels, cite6),
    S('PM · BEFORE WALKAROUND · 10', C['WALK'], walk10, 'FCOM PRO-NOR-SOP-04'),
    S('BOTH · BOX BUILD AND CHECK · 4', C['BUILD'], build, cite6),
    S('PF · 2 CHECKS', C['PF2'], pf2, cite6),
    S('PM · 3 CHECKS', C['PM3'], pm3, cite6),
    S('BOTH · LEGS, BRIEF, CHECKLIST · 3', C['LEGS'], legs, cite6)] + prep['sections'][1:]
D['meta']['resectioned'] = '2026-09-21 cockpit prep memorization groups (spine_cockpit_prep.py colors)'
json.dump(D, open(P, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print('re-sectioned:', [(s['h'], len(s['items'])) for s in pre['sections'] + prep['sections']])
