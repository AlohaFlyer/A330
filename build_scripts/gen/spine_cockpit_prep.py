#!/usr/bin/env python3
"""Re-cut flows 2, 3 and 4 of data/flows_trainer.json (Preliminary Cockpit Prep, Before Walkaround,
Cockpit Preparation) into ONE CM2 spine with ten colored groups, in Ryan's memorization order
(2026-09-21). Run AFTER gen_flows_trainer.py; it only rearranges and relabels the generated items,
so every `d` block stays the verified text. Idempotent: skips if the spine is already present.

Groups (label, color, branch, CM2 count):
  Turn it OFF 4 | Turn it ON 7 | Set it up 4 | PF Box start 2 | PF Panels 3 | PM Before Walkaround 10
  | BOTH Box build and check 4 | PF 2 Checks | PM 3 Checks "CFI" | BOTH Legs, Brief, Checklist 3
CM2 as PF drills 29 items, CM2 as PM drills 35. CM1-only items (MCDU ON, RCL, Aircraft Acceptance,
the CA copies of lights and Jeppesen) stay tagged CA so the CM1 seat view is still complete.
Item fields added: g (group label), gc (group color), gb (branch: '', 'PF', 'PM', 'BOTH').
"""
import json, os, copy
HERE = os.path.dirname(os.path.abspath(__file__)); WORK = os.path.abspath(os.path.join(HERE, '..', '..'))
P = os.path.join(WORK, 'data', 'flows_trainer.json')
D = json.load(open(P, encoding='utf-8'))
F = D['FLOWS']
def sync_from_phase_flows(D):
    """Source of truth is data/phase_flows.json (Ryan, 2026-09-22): every spine item's detail opens with the matching
    Cockpit Prep card item (title + bullets), paired in order; the trainer's two seat-split items (cockpit lights,
    Jeppesen charts) share one phase item. Re-run safe: the block is replaced each time."""
    PF = json.load(open(os.path.join(WORK, 'data', 'phase_flows.json'), encoding='utf-8'))
    cp = next(p for p in PF['phases'] if p['id'] == 'cockpit-prep')
    pitems = [(sec['h'], it) for sec in cp['sections'] for it in sec['items'] if it['k'] in ('box', 'fmc', 'cl')]
    sp = next(f for f in D['FLOWS'] if f.get('spine'))
    pi = 0; prev = None; pairs = []
    for it in sp['items']:
        if prev is not None and it['item'] == prev['item']:
            pairs.append(pairs[-1])
        else:
            pairs.append(pitems[pi]); pi += 1
        prev = it
    assert pi == len(pitems), (pi, len(pitems))
    for it in sp['items']:
        if it['item'].startswith('Cockpit lights') and it['role'] == 'FO': it['x'], it['y'] = 120.2, 356.1   # left side of the pedestal (Ryan, 2026-09-22)
    for it, (h, pit) in zip(sp['items'], pairs):
        d = it['d']
        if d.startswith('[Phase flows'):
            d = d.split('\n\n', 1)[1] if '\n\n' in d else ''
        sub = pit.get('s') or ''
        bullets = [x.strip() for x in (sub if isinstance(sub, list) else sub.split(' · ')) if x.strip()]
        block = '[Phase flows · ' + h + ':]\n' + pit['t'] + ''.join('\n• ' + b for b in bullets)
        it['d'] = block + ('\n\n' + d if d else '')
        it['pf_t'] = pit['t']
        # the drill prompt is the phase flows title (2026-09-22); the action stays unless the title already says it
        it['item'] = pit['t']
        if it.get('act') and it['act'].split(' · ')[0].lower() in pit['t'].lower(): it['act'] = ''
    return len(pairs)
if any(f.get('spine') for f in F):
    n = sync_from_phase_flows(D)
    json.dump(D, open(P, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    print('spine already present; details re-synced from phase_flows.json:', n); raise SystemExit
prelim, walk, prep = F[1], F[2], F[3]
assert prelim['n'].startswith('2. Preliminary') and walk['n'].startswith('3. Before Walkaround') and prep['n'].startswith('4. Cockpit Preparation'), [f['n'] for f in F[1:4]]

def pick(flow, item, role=None):
    for it in flow['items']:
        if it['item'] == item and (role is None or it['role'] == role):
            return copy.deepcopy(it)
    raise KeyError(item)

G = {
 'OFF':  ('Turn it OFF', '#b03a2e', 'CM2'),
 'ON':   ('Turn it ON', '#00805E', 'CM2'),
 'SET':  ('Set it up', '#463C8F', 'CM2'),
 'BOX':  ('Box start', '#CE0C88', 'PF'),
 'PAN':  ('Panels', '#B8860B', 'PF'),
 'WALK': ('Before Walkaround', '#0F6E8C', 'PM'),
 'BUILD':('Box build and check', '#5f3dc4', ''),
 'PF2':  ('2 Checks', '#9c5800', 'PF'),
 'PM3':  ('3 Checks "CFI"', '#7a3b8f', 'PM'),
 'LEGS': ('Legs, Brief, Checklist', '#831A57', ''),
}
def tag(it, g):
    it['g'], it['gc'], it['gb'] = G[g]; return it

items = []
# ---- Turn it OFF (4)
eng = pick(prelim, 'ENG 1, 2 MASTERS LEVERS'); eng['item'] = 'ENG 1, 2 MASTERS LEVERS · ENG START selector'; eng['act'] = 'OFF · NORM'
eng['d'] += '\n[FCOM PRO-NOR-SOP-04-A-00010897.0001001 · ENG:]\n• ENG START selector......NORM CM2'
items.append(tag(eng, 'OFF'))
items.append(tag(pick(prelim, 'WXR/PWS sw'), 'OFF'))
items.append(tag(pick(prelim, 'L/G lever'), 'OFF'))
items.append(tag(pick(prelim, 'Both WIPER selectors'), 'OFF'))
# ---- Turn it ON (7)
bat = pick(prelim, 'BAT 1 pb-sw, BAT 2 pb-sw and APU BAT pb-sw'); bat['item'] = 'BATTERIES check / ELEC'; bat['act'] = 'CHECK (BAT 1, BAT 2, APU BAT AUTO)'
items.append(tag(bat, 'ON'))
items.append(tag(pick(prelim, 'RMP 1 and 2'), 'ON'))
fire = pick(prelim, 'APU FIRE TEST pb'); fire['item'] = 'APU FIRE pb-sw · TEST'; fire['act'] = 'CHECK IN and GUARDED · PRESS and MAINTAIN'
fire['d'] = '[FCOM PRO-NOR-SOP-04-C-00010902.0001001 · APU FIRE:]\n• APU FIRE pb-sw......CHECK IN and GUARDED CM2\n' + fire['d']
items.append(tag(fire, 'ON'))
apu = pick(prelim, 'APU START pb-sw'); bleed = pick(prelim, 'APU BLEED pb-sw')
apu['item'] = 'APU START · APU BLEED'; apu['act'] = 'ON · ON when AVAIL'; apu['d'] = apu['d'] + '\n' + bleed['d']
items.append(tag(apu, 'ON'))
items.append(tag(pick(prelim, 'ALL IR MODE selector'), 'ON'))
cl_fo = pick(prelim, 'COCKPIT LIGHTS', 'FO'); cl_fo['x'], cl_fo['y'] = 120.2, 356.1   # FO lighting panel: left side of the pedestal, below the RMP (Ryan, 2026-09-22)
items.append(tag(cl_fo, 'ON'))
items.append(tag(pick(prelim, 'COCKPIT LIGHTS', 'CA'), 'ON'))
items.append(tag(pick(prelim, 'ATIS'), 'ON'))
# ---- Set it up (4 for CM2; CM1 extras tagged CA)
items.append(tag(pick(prelim, 'MCDU'), 'SET'))
items.append(tag(pick(prelim, 'ALL EFB'), 'SET'))
items.append(tag(pick(prelim, 'RCL pb'), 'SET'))
items.append(tag(pick(prelim, 'AIRCRAFT ACCEPTANCE'), 'SET'))
items.append(tag(pick(prelim, 'LOGBOOK AND MEL/CDL ITEMS'), 'SET'))
oeb = {'item': 'OEB', 'act': 'CHECK', 'role': 'BOTH', 'x': 21.0, 'y': 258.0, 'pos': {'CA': [32.0, 250.0], 'FO': [270.0, 250.0]},
       'd': '[FCOM PRO-NOR-SOP-04-00021759.0002001 · OEB:]\nAll flight crewmembers review and discuss together all OEBs and associated procedures applicable to the aircraft.'}
items.append(tag(oeb, 'SET'))
items.append(tag(pick(prelim, 'JEPPESEN CHARTS', 'FO'), 'SET'))
items.append(tag(pick(prelim, 'JEPPESEN CHARTS', 'CA'), 'SET'))
# ---- PF Box start (2)
items.append(tag(pick(prelim, 'ACARS'), 'BOX'))
tpr = pick(prelim, 'PRELIMINARY TAKEOFF PERF DATA'); tpr['item'] = 'PRELIMINARY TAKEOFF PERF DATA (TPR)'
items.append(tag(tpr, 'BOX'))
# ---- PF Panels (3)
items.append(tag(pick(prep, 'Overhead Panels scan'), 'PAN'))
items.append(tag(pick(prep, 'Front Instr Panels scan'), 'PAN'))
items.append(tag(pick(prep, 'Center Pedestal scan'), 'PAN'))
# ---- PM Before Walkaround (10)
for it in walk['items']:
    items.append(tag(copy.deepcopy(it), 'WALK'))
items[-1]['trg'] = 'PM: Exterior Walkaround (PRO-NOR-SOP-05) · PF: continue Cockpit Preparation'
items[0 if False else len(items)-10]['item'] = 'OXY · HYD · ENG OIL (3)'
items[-1]['item'] = 'GEAR PINS (3)'
# ---- BOTH Box build and check (4)
items.append(tag(pick(prep, 'A-DIFSRIPP scan'), 'BUILD'))
items.append(tag(pick(prep, 'FMS PREPARATION (check DIFSRIPP)'), 'BUILD'))
gl = pick(prep, 'BAROMETRIC REFERENCE'); gl['item'] = 'GLARESHIELD · EFIS control panel'; gl['act'] = 'BARO REF SET/CROSSCHECK · FD ON · LS as rqrd'
items.append(tag(gl, 'BUILD'))
lat = pick(prep, 'OXYGEN MASK TEST'); lat['item'] = 'LATERAL CONSOLES · OXYGEN MASK TEST'; lat['act'] = 'PERFORM'
items.append(tag(lat, 'BUILD'))
items.append(tag(pick(prep, 'PFD and ND'), 'BUILD'))
# ---- PF 2 Checks
items.append(tag(pick(prep, 'PRESS, STS, FUEL pb'), 'PF2'))
rls = pick(prep, 'RELEASE VERSION #__/ FITNESS/ FOB/ PDSC'); rls['item'] = 'RLS VERSION / FITNESS / FOB / PDSC'
items.append(tag(rls, 'PF2'))
# ---- PM 3 Checks "CFI"
items.append(tag(pick(prep, 'IRS ALIGN'), 'PM3'))
items.append(tag(pick(prep, 'FUEL ON BOARD'), 'PM3'))
items.append(tag(pick(prep, 'ATC clearance'), 'PM3'))
# ---- BOTH Legs, Brief, Checklist (3)
items.append(tag(pick(prep, 'DEPARTURE LEGS VERIFICATION'), 'LEGS'))
br = pick(prep, 'DEPARTURE BRIEFING'); br.pop('cl', None); br.pop('clWho', None)
br['trg'] = 'Cockpit Preparation Checklist'
items.append(tag(br, 'LEGS'))
cl = {'item': 'COCKPIT PREPARATION CHECKLIST', 'act': 'PF requests · PM reads · PF responds', 'role': 'BOTH', 'x': 100.0, 'y': 246.0, 'mir': True,
      'cl': 'COCKPIT PREPARATION CHECKLIST', 'clWho': 'PF requests · PM reads · PF responds',
      'd': '[FCTM PR-NP-CL-00024935.0001001 · COCKPIT PREPARATION:]\nChecklist trigger: Departure briefing completed.'}
items.append(tag(cl, 'LEGS'))

def count(duty, seat='FO'):
    n = 0
    for it in items:
        r = it['role']
        if r == 'BOTH' or r == seat or r == duty: n += 1
    return n
assert count('PF') == 29, count('PF')
assert count('PM') == 35, count('PM')

spine = {'n': '2. Preliminary + Cockpit Prep (CM2 spine)', 'who': 'CM2 (FO) · PF and PM branches', 'ref': 'PRO-NOR-SOP-04, SOP-05, SOP-06',
         'phase': 'Cockpit Prep', 'spine': True, 'items': items,
         'groups': [{'g': v[0], 'gc': v[1], 'gb': v[2]} for v in G.values()]}
new = [F[0], spine] + F[4:]
for i, f in enumerate(new, 1):
    f['n'] = str(i) + '.' + f['n'].split('.', 1)[1]
D['FLOWS'] = new
sync_from_phase_flows(D)
json.dump(D, open(P, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print('spine written:', len(items), 'items; PF', count('PF'), 'PM', count('PM'), '; flows now', len(new))
