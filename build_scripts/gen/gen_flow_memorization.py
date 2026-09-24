#!/usr/bin/env python3
"""flow_memorization.html and working/A330_FLOW_MEMORIZATION_PLAN.md from data/phase_flows.json (the source of truth,
Ryan 2026-09-22). The ten Cockpit Prep groups, their counts, colours and item titles are generated; the method prose
(NASA framing, practice protocol, failure modes, exception rack, wording traps, resolved questions, sources) lives in
flow_memorization_template.html next to this script. Run after gen_phase_flows.py / resection_cockpit_prep.py."""
import json, os, re, html
HERE = os.path.dirname(os.path.abspath(__file__)); WORK = os.path.abspath(os.path.join(HERE, '..', '..'))
PF = json.load(open(os.path.join(WORK, 'data', 'phase_flows.json'), encoding='utf-8'))
cp = next(p for p in PF['phases'] if p['id'] == 'cockpit-prep')
groups = [s for s in cp['sections'] if s.get('mem')]
assert len(groups) == 10, len(groups)

def who(h):
    if h.startswith('CM2'): return 'CM2'
    if h.startswith('PF'): return 'PF'
    if h.startswith('PM'): return 'PM'
    return 'PF and PM'
def items(sec): return [it for it in sec['items'] if it['k'] in ('box', 'fmc', 'cl')]
def title(it): return it['t'] if it['k'] != 'cl' else it['t'] + ' checklist'

HOOKS = {
 'TURN IT OFF': 'Four things that must be dead before anything else: engines, radar, gear lever position, wipers. Say the four nouns; the state is always OFF, DOWN, NORM.',
 'TURN IT ON': 'Power, talk, fire, air, nav, light, weather: batteries and external power, radios, the APU fire test, APU start and bleed, IRS to NAV, cockpit lights, ATIS. Seven, in the order the airplane comes alive.',
 'SET IT UP': 'The paperwork gate. MCDU pre-init and RCL and acceptance are CM1; EFB, logbook and MEL, OEB, Jeppesen are everyone. Four for CM2.',
 'BOX START': 'The PF opens the box: ACARS, then the preliminary takeoff numbers. Two items and the seats split here.',
 'PANELS': 'Overhead, front, pedestal: top to bottom, the panel geography is the memory. Each scan card carries every FCOM line in scan order.',
 'BEFORE WALKAROUND': 'Three fluids, then the brakes, then the safety gear: OXY HYD OIL, flaps and speed brake, ACCU PARK BRAKES, alternate braking, emergency equipment, rain repellent, gear pins. Ten, then the PM leaves.',
 'BOX BUILD AND CHECK': 'A-DIFSRIPP built by the PF, crosschecked by the PM, then glareshield, lateral consoles, PFD and ND. The airplane is configured for the departure here.',
 '2 CHECKS': 'PF: PRESS and STS on the ECAM, then the release sent. Two.',
 '3 CHECKS "CFI"': 'PM: IRS aligned, fuel on board, ATC clearance. Three.',
 'LEGS, BRIEF, CHECKLIST': 'Legs verified, briefing performed, checklist read. The flow ends in a reported state, never a remembered one.',
}
def key(h):
    return re.sub(r'^(CM2|PF|PM) · ', '', h).split(' · ')[0].strip()

rows = []; lists = []; md_rows = []; md_lists = []
tot_pf = tot_pm = 0
for g in groups:
    its = items(g); k = key(g['h']); w = who(g['h']); n = len(its)
    pf = sum(1 for it in its if (it.get('r') in ('PF', 'B', 'F', None)) or it['k'] == 'cl')
    pm = sum(1 for it in its if (it.get('r') in ('PM', 'B', 'F', None)) or it['k'] == 'cl')
    rows.append(f'<tr><td><span class="sw" style="background:{g["c"]}"></span>{html.escape(k)}</td><td>{w}</td><td>{n}</td></tr>')
    md_rows.append(f'| {k} | {w} | {n} |')
    lis = ''.join(f'<li>{html.escape(title(it))}</li>' for it in its)
    lists.append(f'<h3 style="color:{g["c"]}">{html.escape(g["h"])}</h3><p class="hook">{html.escape(HOOKS[k])}</p><ol>{lis}</ol>')
    md_lists.append(f'### {g["h"]}\n\n{HOOKS[k]}\n\n' + '\n'.join(f'{i+1}. {title(it)}' for i, it in enumerate(its)) + '\n')
total = sum(len(items(g)) for g in groups)

GROUPS = f'''<h2 id="groups">1. The ten groups (generated from the phase flows)</h2>
<p>These are the Cockpit Prep sections of <a href="phase_flows.html" style="color:#FF9080">Phase Flows</a>, in the order you memorize them. The trainer drills the same ten groups in the same colours; the counts in the group headers are the CM2 card items, the lists below are every card item in the group ({total} in all, {len(groups)} groups). Both are generated from data/phase_flows.json, so when the phase flows change after an FCOM revision this page and the trainer change with them.</p>
<table><thead><tr><th>Group</th><th>Who</th><th>Items</th></tr></thead><tbody>{''.join(rows)}</tbody></table>
<h2>2. Why ten, and why these</h2>
<p>Four gates that read as verbs (OFF, ON, SET UP, START) carry the whole of preliminary prep for CM2 with nothing to count; the verb tells you the state of every switch in the group. The seats split at BOX START: from there the PF works the panels and the box while the PM clears the aircraft to walk. Two short check groups close each branch (2 for PF, 3 for PM), and the flow ends in a triple every crew already says out loud: legs, brief, checklist. Ten names, in one physical direction through the cockpit, is inside the four-to-seven item span working memory can hold, and each name regenerates its own items.</p>
'''
HOOKSH = '<h2>3. The groups, item by item, with the hook for each</h2>' + ''.join(lists)
H1 = f'''<h1>Cockpit Preparation - Flow Memorization Plan</h1>
<p class="sub">How to commit the Cockpit Preparation flow to memory as ten colored groups, and how to practise it so it survives the thing that actually breaks it. Source of truth: data/phase_flows.json (A330P FCOM R17 PRO-NOR-SOP-03 / 04 / 06, audited against the FCOM 22 Sep 2026). Method is sourced; where a technique is one pilot's opinion rather than documented practice, it says so.</p>
<p>Target: Cockpit Preparation, {total} card items in {len(groups)} groups, CM2 drilling 29 as PF and 35 as PM. The groups, their counts and their item names on this page are generated from the phase flows; the trainer drills the same data.</p>'''
tpl = open(os.path.join(HERE, 'flow_memorization_template.html'), encoding='utf-8').read()
page = tpl.replace('{{H1}}', H1).replace('{{GROUPS}}', GROUPS).replace('{{HOOKS}}', HOOKSH)
page = page.replace('</style>', '.sw{display:inline-block;width:12px;height:12px;border-radius:3px;margin-right:7px;vertical-align:-1px}.hook{color:#C3BED0;font-style:italic}table{border-collapse:collapse;width:100%;margin:8px 0 14px}th,td{font-size:13.5px;text-align:left;padding:6px 8px;border-bottom:1px solid #453F58;color:#E4E0EC}th{color:#fff;background:#463C8F}ol{margin:0 0 13px 22px}ol li{font-size:14px;line-height:1.55;color:#E4E0EC;margin-bottom:4px}\n</style>', 1)
open(os.path.join(WORK, 'flow_memorization.html'), 'w', encoding='utf-8').write(page)

# ---- markdown twin for Drive working/
def strip(s): return html.unescape(re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', s))).strip()
def sec(a, b):
    i = tpl.index(a); j = tpl.index(b, i); return tpl[i:j]
def md_of(fragment):
    out = []
    for m in re.finditer(r'<(h2|h3|p|li|tr)[^>]*>(.*?)</\1>', fragment, re.S):
        tag, inner = m.group(1), strip(m.group(2))
        if not inner: continue
        if tag == 'h2': out.append('\n## ' + inner + '\n')
        elif tag == 'h3': out.append('\n### ' + inner + '\n')
        elif tag == 'li': out.append('- ' + inner)
        elif tag == 'tr': out.append('| ' + ' | '.join(strip(c) for c in re.findall(r'<t[hd][^>]*>(.*?)</t[hd]>', m.group(2), re.S)) + ' |')
        else: out.append(inner + '\n')
    return '\n'.join(out)
md = ['# Cockpit Preparation - Flow Memorization Plan', '', strip(H1.split('</h1>')[1]), '', md_of(sec('<h2>0.', '{{GROUPS}}')),
      '\n## 1. The ten groups (generated from the phase flows)\n', '| Group | Who | Items |', '|---|---|---|', *md_rows, '',
      strip(GROUPS.split('<h2>2.')[1].split('</h2>')[1]) and '\n## 2. Why ten, and why these\n\n' + strip(GROUPS.split('<h2>2.')[1].split('</h2>')[1]),
      '\n## 3. The groups, item by item, with the hook for each\n', *md_lists,
      md_of(tpl[tpl.index('{{HOOKS}}'):])]
open(os.path.join(WORK, 'docs', 'A330_FLOW_MEMORIZATION_PLAN.md'), 'w', encoding='utf-8').write('\n'.join(md))
print('flow_memorization.html and docs/A330_FLOW_MEMORIZATION_PLAN.md written:', total, 'items,', len(groups), 'groups')
