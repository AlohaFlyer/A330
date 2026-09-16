#!/usr/bin/env python3
"""Generate WORK/data/flows_trainer.json (FLOWS, XREFS, NORMAL_CHECKLISTS) for the A330 Flows
Trainer page, in the exact B787 flows_quiz.html shapes.

Inputs: WORK/data/flows.json (verified phases), src/A330P_FCOM_R17_PRO-NOR.md (FCOM PRO-NOR slice),
src/A330_FCTM_R5.md (normal checklists PR-NP-CL), img/layout.json (cockpit composite geometry).
Every quoted line in `d`, every XREF body line and every checklist row is taken verbatim from the
extract (whitespace and dot leaders normalized) so verify_flows_trainer.py can prove it.
"""
import json, re, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(HERE, 'work'); SRC = os.environ.get('A330_SRC', os.path.join(WORK, '..', 'src'))  # manual extracts, never in the repo
FCOM = open(os.path.join(SRC, 'A330P_FCOM_R17_PRO-NOR.md'), encoding='utf-8').read()
FCTM = open(os.path.join(SRC, 'A330_FCTM_R5.md'), encoding='utf-8').read()
flows = json.load(open(os.path.join(WORK, 'data', 'flows.json')))
LAY = json.load(open(os.path.join(HERE, 'img', 'layout.json')))

def norm(s):
    s = re.sub(r'[\ue113\ue114]', '▸', s)   # Airbus conditional-branch glyphs (private-use codepoints) -> arrow
    s = re.sub(r'\.{3,}', '......', s)
    return re.sub(r'\s+', ' ', s).strip()

# ---------------------------------------------------------------- FCOM DU index
# The extract is page-form-feed separated; each page = header block, content, footer block.
HDR_END = re.compile(r'OPERATING MANUAL')
FOOT = re.compile(r'^\s*HAL A330 FLEET\b')
PAGE_BREAK = '\x00PAGE\x00'
def page_body(p):
    lines = p.split('\n')
    # drop header: everything up to and including the OPERATING MANUAL line (first 12 lines)
    for i, l in enumerate(lines[:14]):
        if HDR_END.search(l):
            lines = lines[i+1:]; break
    # drop footer from the HAL A330 FLEET line on
    for i, l in enumerate(lines):
        if FOOT.match(l):
            lines = lines[:i]; break
    return lines
BODY = []
for p in FCOM.split('\f'):
    BODY += page_body(p) + [PAGE_BREAK]
IDENT = re.compile(r'^\s*\d?\s*Ident\.: (PRO-NOR-[A-Z0-9.-]+) / ')
DU = {}
cur = None
for l in BODY:
    m = IDENT.match(l)
    if m:
        cur = m.group(1); DU[cur] = []; continue
    if cur: DU[cur].append(l)
STEP = re.compile(r'^\s*(?:L\d\s+)?(\*\s*)?(.+?)\s*\.{4,}\s*(.*?)\s*$')
ROLE = re.compile(r'\s(PF-PM|PF|PM|BOTH|CM1-CM2|CM2-CM3|PM-CM3|CM1|CM2|CM3|ALL)$')
JUNK = re.compile(r'^\s*(\d+|L\d|Applicable to:.*|Criteria:.*|Intentionally left blank)?\s*$')

def du_lines(ident):
    """Cleaned DU content: list of (kind, text). kind: 'title' | 'step' | 'text' | 'break'."""
    out = []
    raw = DU[ident]
    first = True
    for l in raw:
        if l == PAGE_BREAK: out.append(('break', '')); continue
        if JUNK.match(l):
            if l.strip() in ('', 'L1', 'L2'): out.append(('blank', ''))   # a lone L1/L2 marker separates paragraphs
            continue
        if re.match(r'^\s*L\d\s+', l): out.append(('blank', ''))   # an L1/L2 prefix starts a new paragraph
        s = re.sub(r'^\s*L\d\s+', '', l).strip()
        if re.match(r'^[A-Z0-9 /&().,\'-]+$', s) and '....' not in s and len(s) <= 70 and s not in ('WARNING', 'CAUTION'):
            out.append(('title' if first else 'subtitle', s)); first = False; continue
        first = False
        if re.search(r'\.{4,}', s) and not s.startswith('‐'):
            out.append(('step', norm(s)))
        else:
            out.append(('text', s))
    # the next DU's section title is printed before its Ident line: drop trailing all-caps title lines
    while out and (out[-1][0] in ('blank', 'break') or (out[-1][0] == 'text' and re.match(r'^[A-Z0-9 /&().,\'-]+$', out[-1][1]))):
        out.pop()
    return out

def tidy(p, cap=520):
    """Split a joined paragraph at its '‐' sub-items (each piece stays a verbatim substring) and cap
    over-long prose at a sentence boundary (a prefix is still a substring)."""
    parts = re.split(r'\s(?=‐ )', p)
    out = []
    for q in parts:
        if len(q) > cap:
            cut = q.rfind('. ', 0, cap)
            q = (q[:cut+1] if cut > 80 else q[:q.rfind(' ', 0, cap)]) + ' …'   # verifier strips the marker
        out.append(q)
    return out

def paragraphs(items):
    """Join consecutive text lines into paragraphs; break on blank, break, step, title."""
    paras = []; buf = []
    def flush():
        if buf: paras.append(norm(' '.join(buf))); buf.clear()
    for k, t in items:
        if k == 'text': buf.append(t)
        else: flush()
    flush()
    return paras

def du_title(ident):
    for k, t in du_lines(ident):
        if k == 'title': return t
    return ''

def du_quote(ident, line=None, max_paras=3):
    """Return the quoted lines for `d`: the DU's step lines (verbatim, leaders normalized) with the
    explanation paragraphs that follow the requested step line. If line is None, the DU's paragraphs."""
    items = du_lines(ident)
    out = []
    if line is None:
        for p in paragraphs(items)[:max_paras]: out += tidy(p)
        return out
    target = norm(line).replace('* ', '')
    steps = [t for k, t in items if k == 'step']
    # all step lines of the DU, the target first-marked
    hit = None
    for t in steps:
        if target.split('......')[0].strip() in t and target.split('......')[-1].strip() in t:
            hit = t; break
    if hit is None:
        raise SystemExit(f'step line not found in {ident}: {line}')
    # explanation: text items directly after the hit until next step/break
    expl = []; on = False; buf = []
    for k, t in items:
        if k == 'step':
            if on: break
            on = (t == hit); continue
        if on:
            if k == 'text': buf.append(t)
            else:
                if buf: expl.append(norm(' '.join(buf))); buf = []
                if k == 'break': continue
    if buf: expl.append(norm(' '.join(buf)))
    out.append('• ' + hit)
    expl = expl[:max_paras]
    while expl and expl[-1].rstrip().endswith(':'): expl.pop()   # a lead-in to step lines we do not quote
    for p in expl: out += tidy(p)
    return out

# ---------------------------------------------------------------- map coordinates
W, H = LAY['W'], LAY['H']
def to_vb(panel, px, py):
    x0, y0, w, h = LAY[panel]
    sw = {'oh': (743, 1421), 'mp': (2273, 738), 'pd': (665, 1103)}[panel]
    if panel == 'mp': px, py = px * 1.1365, py * 1.1365   # coords were read on the 2000 px wide preview
    X = x0 + px * w / sw[0]; Y = y0 + py * h / sw[1]
    return round(X * 300 / W, 1), round(Y * 437 / H, 1)

# Named anchors. Coordinates are pixel positions on the three source crops (overhead oh.png 743x1421,
# main panel mp.png read on its 2000 px preview, pedestal pd.png 665x1103), see layout.json.
LOC = {
 # overhead
 'oh_ckpt_door': ('oh', 95, 60), 'oh_adirs': ('oh', 95, 700), 'oh_apu_fire_test': ('oh', 40, 840),
 'oh_wiper_r': ('oh', 600, 1290), 'oh_rain_r': ('oh', 680, 1290), 'oh_bat': ('oh', 330, 990),
 'oh_fuel': ('oh', 370, 900), 'oh_air': ('oh', 370, 1150), 'oh_apu_bleed': ('oh', 330, 1195),
 'oh_anti_ice_eng': ('oh', 278, 1255), 'oh_strobe': ('oh', 205, 1330), 'oh_beacon': ('oh', 240, 1330),
 'oh_rwy_turnoff': ('oh', 240, 1372), 'oh_land': ('oh', 280, 1375), 'oh_nose': ('oh', 320, 1375),
 'oh_apu_master': ('oh', 365, 1325), 'oh_apu_start': ('oh', 365, 1358), 'oh_int_lt': ('oh', 450, 1335),
 'oh_seat_belts': ('oh', 410, 1375), 'oh_no_smoking': ('oh', 450, 1375), 'oh_center_scan': ('oh', 370, 820),
 # main panel + glareshield
 'mp_capt_pfd': ('mp', 415, 295), 'mp_capt_nd': ('mp', 625, 280), 'mp_capt_nd2': ('mp', 625, 345),
 'mp_fo_nd': ('mp', 1360, 280), 'mp_fo_nd2': ('mp', 1360, 345), 'mp_fo_pfd': ('mp', 1560, 295),
 'mp_fcu': ('mp', 1000, 100), 'mp_fcu_alt': ('mp', 1105, 100),
 'mp_efis_capt_cstr': ('mp', 760, 62), 'mp_efis_fo_cstr': ('mp', 1240, 62), 'mp_efis_fo_arpt': ('mp', 1290, 62),
 'mp_efis_capt_ls': ('mp', 720, 138), 'mp_efis_fo_ls': ('mp', 1275, 138),
 'mp_isis': ('mp', 852, 262), 'mp_ewd': ('mp', 975, 270), 'mp_ewd2': ('mp', 1040, 270), 'mp_ewd_memo': ('mp', 1060, 345),
 'mp_sd': ('mp', 1005, 470), 'mp_sd2': ('mp', 1005, 540),
 'mp_ldg_gear': ('mp', 1160, 250), 'mp_gear_lever': ('mp', 1160, 400), 'mp_autobrk': ('mp', 1160, 318),
 'mp_terr_capt': ('mp', 770, 350), 'mp_terr_fo': ('mp', 1225, 355),
 'mp_accu_press': ('mp', 1210, 415), 'mp_brake_press': ('mp', 1245, 450), 'mp_nws_light': ('mp', 1225, 295),
 'mp_dcdu_fo': ('mp', 1180, 560),
 'mp_capt_efb': ('mp', 140, 455), 'mp_capt_charts': ('mp', 140, 510), 'mp_capt_tiller': ('mp', 85, 550), 'mp_capt_console': ('mp', 60, 612),
 'mp_fo_efb': ('mp', 1875, 455), 'mp_fo_charts': ('mp', 1875, 510), 'mp_fo_tiller': ('mp', 1915, 550), 'mp_fo_console': ('mp', 1940, 612),
 'mp_window_capt': ('mp', 110, 175), 'mp_window_fo': ('mp', 1890, 175), 'mp_eye_ref': ('mp', 1000, 25),
 # pedestal
 'pd_mcdu1': ('pd', 115, 130), 'pd_mcdu1_scr': ('pd', 115, 80), 'pd_mcdu1_kb': ('pd', 115, 220),
 'pd_mcdu2': ('pd', 555, 130), 'pd_mcdu2_scr': ('pd', 555, 80), 'pd_mcdu2_kb': ('pd', 555, 220),
 'pd_ecp': ('pd', 330, 135), 'pd_to_config': ('pd', 300, 98), 'pd_rcl': ('pd', 340, 160),
 'pd_rmp1': ('pd', 115, 330), 'pd_rmp2': ('pd', 555, 330), 'pd_thrust': ('pd', 330, 330), 'pd_pitch_trim': ('pd', 225, 350),
 'pd_eng_masters': ('pd', 332, 560), 'pd_eng_start_sel': ('pd', 330, 665), 'pd_wxr': ('pd', 110, 575),
 'pd_flood_r': ('pd', 555, 510), 'pd_atc': ('pd', 555, 585), 'pd_tcas': ('pd', 600, 605),
 'pd_speed_brake': ('pd', 215, 690), 'pd_park_brk': ('pd', 130, 790), 'pd_park_brk2': ('pd', 150, 740),
 'pd_flaps': ('pd', 470, 690), 'pd_rudder_trim': ('pd', 330, 1010), 'pd_printer_top': ('pd', 490, 860), 'pd_printer_bot': ('pd', 490, 950),
}
# (phase id, step index) -> anchor. Step index is the position in flows.json phases[].steps.
PLACE = {
 'safety-exterior': ['mp_fo_console', 'mp_fo_tiller', 'mp_gear_lever', 'oh_apu_master'],
 'prelim-cockpit-prep': ['pd_eng_masters', 'pd_wxr', 'mp_gear_lever', 'oh_wiper_r', 'oh_bat', 'pd_rmp1', 'oh_apu_fire_test',
                         'oh_apu_start', 'oh_apu_bleed', 'oh_adirs', 'oh_int_lt', 'pd_flood_r', 'pd_mcdu1', 'mp_capt_efb',
                         'pd_rcl', 'mp_capt_console', 'mp_fo_console', 'mp_capt_charts', 'pd_mcdu2', 'mp_fo_charts',
                         'pd_mcdu1_kb', 'pd_printer_top'],
 'before-walkaround': ['mp_sd', 'pd_flaps', 'pd_speed_brake', 'mp_accu_press', 'pd_park_brk', 'mp_brake_press', 'pd_park_brk2',
                       'mp_fo_console', 'oh_rain_r', 'mp_gear_lever'],
 'cockpit-prep': ['oh_center_scan', 'mp_fo_tiller', 'mp_isis', 'pd_rmp1', 'pd_mcdu1', 'pd_mcdu2', 'mp_fcu', 'mp_capt_console',
                  'mp_capt_pfd', 'pd_ecp', 'pd_mcdu2_kb', 'pd_mcdu1_kb', 'mp_sd', 'mp_dcdu_fo', 'mp_capt_nd', 'mp_fo_nd'],
 'before-pushback': ['pd_mcdu1', 'pd_mcdu1_scr', 'pd_mcdu2_scr', 'mp_ewd', 'pd_mcdu1_kb', 'pd_printer_top', 'pd_printer_bot',
                     'pd_mcdu2', 'mp_eye_ref', None, 'pd_rmp2'],
 'before-start': ['oh_beacon', 'pd_atc', 'mp_window_capt', 'mp_window_fo', 'mp_sd', 'mp_sd2', 'pd_thrust', 'pd_park_brk'],
 'after-start': ['pd_eng_start_sel', 'pd_speed_brake', 'oh_apu_bleed', 'pd_rudder_trim', 'oh_anti_ice_eng', 'pd_flaps',
                 'oh_apu_master', 'pd_pitch_trim', 'mp_ewd', 'mp_ewd2', 'mp_ewd_memo', 'mp_nws_light'],
 'during-taxi': ['mp_brake_press', 'mp_sd', 'mp_dcdu_fo', 'mp_fcu_alt', 'mp_capt_pfd'],
 'taxi': ['mp_terr_capt', 'mp_autobrk', 'mp_terr_fo', 'pd_atc', 'pd_eng_start_sel', 'pd_wxr', 'pd_to_config', 'mp_ewd_memo'],
 'line-up': ['mp_capt_nd', 'pd_tcas', 'mp_capt_nd2', 'mp_fo_nd', 'oh_strobe', 'mp_fo_nd2', 'oh_air'],
 'acceleration': ['pd_flaps', 'pd_speed_brake', 'mp_ldg_gear', 'oh_rwy_turnoff'],
 'climb-10000': ['mp_efis_capt_cstr', 'oh_land', 'oh_no_smoking', 'mp_efis_fo_arpt', 'mp_ewd_memo', 'pd_mcdu2'],
 'descent-10000': ['mp_efis_capt_cstr', 'oh_land', 'mp_efis_capt_ls', 'oh_no_smoking', 'pd_mcdu1', 'mp_efis_fo_cstr',
                   'mp_efis_fo_ls', 'pd_eng_start_sel'],
 'after-landing': ['pd_speed_brake', 'pd_wxr', 'oh_land', 'pd_eng_start_sel', 'oh_strobe', 'pd_flaps', 'oh_nose', 'pd_tcas',
                   'oh_apu_master', 'oh_anti_ice_eng'],
 'parking': ['mp_accu_press', 'oh_anti_ice_eng', 'pd_park_brk', 'oh_apu_bleed', 'pd_eng_masters', 'oh_fuel', 'oh_beacon',
             'pd_atc', 'oh_seat_belts', 'pd_mcdu2', 'mp_sd', 'mp_sd2'],
}
PHASE_OF = {  # A330 phase -> phase-bar label (the engine's PHASE_COLORS keys are phase-of-flight names)
 'safety-exterior': 'Preflight', 'prelim-cockpit-prep': 'Preflight', 'before-walkaround': 'Preflight', 'cockpit-prep': 'Preflight',
 'before-pushback': 'Before Start & Pushback', 'before-start': 'Before Start & Pushback', 'after-start': 'Engine Start',
 'during-taxi': 'Taxi Out', 'taxi': 'Taxi Out', 'line-up': 'Takeoff', 'acceleration': 'Climb', 'climb-10000': 'Climb',
 'descent-10000': 'Descent', 'after-landing': 'Taxi In', 'parking': 'Shutdown & Secure',
}
ROLE_MAP = {'CM1': 'CA', 'CM2': 'FO', 'PF': 'PF', 'PM': 'PM', 'BOTH': 'BOTH'}
WHO_MAP = {'CM1': 'CA (CM1)', 'CM2': 'FO (CM2)', 'PF': 'PF', 'PM': 'PM'}

# ---------------------------------------------------------------- FCTM normal checklists
def fctm_checklists():
    a = FCTM.index('PR-NP-CL-00024935.0001001'); b = FCTM.index('PR-NP-CL-00024945.0001001')
    seg = FCTM[FCTM.rfind('\n', 0, FCTM.rfind('COCKPIT PREPARATION', 0, a)):b]
    cls = {}; name = None; trig = {}; ident = {}
    HEAD = re.compile(r'^\s{20,}(<< DEPARTURE CHANGE >>|[A-Z][A-Z -]+)\s*$')
    ROW = re.compile(r'^\s*([A-Z0-9][A-Za-z0-9 &./\'-]*?)\s*\.{4,}\s*(.+?)\s*$')
    SUB = re.compile(r'^\s*(‐ [A-Z][A-Z ./]+?)\s+([A-Z0-9.]+)\s*$')
    pend_trig = None
    for l in seg.split('\n'):
        m = HEAD.match(l)
        if m and 'NORMAL CHECKLISTS' not in l and 'PROCEDURES' not in l and 'FLIGHT CREW' not in l and 'TECHNIQUES' not in l and 'A330' not in l:
            name = m.group(1).replace('<< ', '').replace(' >>', ''); cls[name] = []; pend_trig = None; continue
        mi = re.match(r'^\s*Ident\.: (PR-NP-CL-[0-9.]+)', l)
        if mi and name: ident[name] = mi.group(1); continue
        if name is None: continue
        if l.strip().startswith('Checklist trigger'):
            pend_trig = [l.strip()]; continue
        if pend_trig is not None and l.strip().startswith('‐'):
            pend_trig.append(l.strip()); continue
        if pend_trig is not None and (ROW.match(l) or not l.strip()):
            trig[name] = pend_trig; pend_trig = None
        m = ROW.match(l)
        if m:
            ch, resp = m.group(1), m.group(2)
            who = 'PF'
            if resp.endswith('(BOTH)'): who = 'BOTH'; resp = resp[:-6].strip()
            cls[name].append([ch, resp, who]); continue
        m = SUB.match(l)
        if m and cls[name] and (cls[name][-1][0] == 'ECAM MEMO' or cls[name][-1][0].startswith('‐')):
            cls[name].append([m.group(1), m.group(2), 'PF'])
    return cls, trig, ident
CLS, CLTRIG, CLIDENT = fctm_checklists()
# Securing the Aircraft: single reference row, performed by the PM (FCTM PR-NP-CL-00024945.0001001)
CLS['SECURING THE AIRCRAFT'] = [['Refer to /FCOM/PRO-NOR-SUP-SEC Securing the Aircraft - General', '', 'PM']]
CLIDENT['SECURING THE AIRCRAFT'] = 'PR-NP-CL-00024945.0001001'
NORMAL_CHECKLISTS = {k + ' CHECKLIST': v for k, v in CLS.items()}
CL_KEY = {'Cockpit Preparation': 'COCKPIT PREPARATION CHECKLIST', 'Before Start': 'BEFORE START CHECKLIST',
          'After Start': 'AFTER START CHECKLIST', 'Taxi': 'TAXI CHECKLIST', 'Line-Up': 'LINE-UP CHECKLIST',
          'Approach': 'APPROACH CHECKLIST', 'After Landing': 'AFTER LANDING CHECKLIST', 'Parking': 'PARKING CHECKLIST'}
for k in CL_KEY.values(): assert k in NORMAL_CHECKLISTS, k

# ---------------------------------------------------------------- XREFS (FCOM supplementary procedures)
XREF_RE = re.compile(r'\b(PRO-NOR-SUP-[A-Z]+)\b')
def sup_body(key):
    """First DU paragraphs + step lines of the supplementary procedure section `key`."""
    idents = [i for i in DU if i.startswith(key + '-') or i.startswith(key + '-A-')]
    if key == 'PRO-NOR-SUP-SEC':
        idents = [i for i in DU if i.startswith('PRO-NOR-SUP-SEC-A-')]
        title = 'FCOM PRO-NOR-SUP-SEC - Securing the Aircraft'
        lines = []
        for i in idents:
            for k, t in du_lines(i):
                if k == 'step': lines.append('• ' + t)
        intro = paragraphs(du_lines(idents[0]))[:2]
        return title, '\n'.join(intro + lines)
    if key == 'PRO-NOR-SUP-ADVWXR':   # the only ADVWXR reference in a quoted step is Engine Ice Shedding on Ground
        i = 'PRO-NOR-SUP-ADVWXR-00009179.0006001'
        title = 'FCOM PRO-NOR-SUP-ADVWXR - Engine Ice Shedding on Ground'
        lines = []
        for para in paragraphs(du_lines(i))[:2]: lines += tidy(para)
        return title, '\n'.join(lines)
    return None, None
XREFS = {}

# ---------------------------------------------------------------- build FLOWS
FLOWS = []
gaps = []
for ph in flows['phases']:
    pid = ph['id']; places = PLACE[pid]
    steps = ph['steps']
    assert len(places) == len(steps), (pid, len(places), len(steps))
    items = []
    idents = set()
    for si, st in enumerate(steps):
        if places[si] is None:
            gaps.append(f"{ph['title']}: '{st['text']}' ({st['fcom']['status']}) omitted, no FCOM PRO-NOR step")
            continue
        f = st['fcom']; ident = f['ident']; line = f['line']
        idents.add(ident.rsplit('-', 1)[0] if re.search(r'-\d{8}\.\d+$', ident) else ident)
        role = ROLE_MAP[st['who']]
        panel, px, py = LOC[places[si]]; x, y = to_vb(panel, px, py)
        dl = [f"[FCOM {ident} · {du_title(ident)}:]" if du_title(ident) else f"[FCOM {ident}:]"]
        if ident == 'PRO-NOR-SOP-07-A-00011058.0001001':
            q = ['• SEATS, SEAT BELTS, HARNESSES, RUDDER PEDALS, ARMRESTS...... PF-PM ...... ADJUST'] + [p for p in paragraphs(du_lines(ident)) if p != 'PF-PM']
            item, act = 'SEATS, SEAT BELTS, HARNESSES, RUDDER PEDALS, ARMRESTS', 'ADJUST'
        elif line is None:
            q = du_quote(ident, None)
            item, act = st['text'], 'Check' if pid == 'safety-exterior' else 'Perform'
            if pid == 'cockpit-prep':  # exterior walkaround: the schematic DU lists the 24 stations
                q = ['Refer to PRO-NOR-SOP-05 Exterior Walkaround']
                item, act = 'EXTERIOR WALKAROUND', 'PERFORM (PRO-NOR-SOP-05)'
            elif pid == 'safety-exterior':
                item, act = 'General', 'check for obstructions, engineering and refueling activity'
        else:
            q = du_quote(ident, line)
            hit = q[0][2:]
            m = ROLE.search(hit); body = hit[:m.start()] if m else hit
            ch, resp = body.split('......', 1)
            item, act = ch.strip().lstrip('* ').strip(), resp.strip()
            if pid == 'cockpit-prep' and st['text'] in ('Overhead Panels', 'Front Instr Panels', 'Center Pedestal', 'A-DIFSRIPP'):
                item, act = st['text'] + ' scan', f'{item} {act}'
        dl += q
        d = '\n'.join(dl)
        # card wording vs FCOM wording (flows.json CONFLICT records)
        if f['status'] == 'CONFLICT':
            d += f"\n[Card vs FCOM:] the quick reference card prints '{st['text']}'; the FCOM step is the line quoted above."
        it = {'item': item, 'act': act, 'role': role, 'x': x, 'y': y, 'd': d}
        items.append(it)
    # flow-level extras on the first item: exterior lights from the quick reference (technique)
    if ph.get('lights') and items:
        L = ph['lights']
        items[0]['d'] += f"\n[Exterior lights, quick reference (technique):] {L['who']}: " + ' · '.join(L['settings'])
    # checklist call on the last item
    if ph.get('cl_trigger') and items:
        key = CL_KEY[ph['cl_trigger']['checklist']]
        fname = key.replace(' CHECKLIST', '')
        last = items[-1]
        last['cl'] = key; last['clWho'] = 'PF requests · PM reads · PF responds'
        tq = CLTRIG.get(fname)
        last['d'] += f"\n[FCTM {CLIDENT[fname]} · {fname}:]\n" + '\n'.join(tq) if tq else ''
        last['d'] += f"\n✅ {key}: PF requests it, PM reads the challenge, PF responds after checking the aircraft. Card trigger: {ph['cl_trigger']['text']}. (FCTM {CLIDENT[fname]})"
    flow = {'n': f"{ph['order']}. {ph['title']}", 'who': ' / '.join(WHO_MAP.get(c, c) for c in ph['columns']),
            'ref': '', 'phase': PHASE_OF[pid], 'items': items}
    # ref: the FCOM section (PRO-NOR-SOP-nn) shared by the steps
    secs = sorted({re.match(r'(PRO-NOR-SOP-\d+)', i).group(1) for i in idents if re.match(r'PRO-NOR-SOP-\d+', i)})
    flow['ref'] = ', '.join(secs)
    if ph.get('flow_trigger'): flow['trig'] = ph['flow_trigger']['text']
    FLOWS.append(flow)

# XREFS wherever a quoted line references a supplementary procedure
for f in FLOWS:
    for it in f['items']:
        for k in XREF_RE.findall(it['d']):
            if k not in XREFS:
                t, b = sup_body(k)
                if t: XREFS[k] = {'title': t, 'body': b}
# The Parking flow closes with Securing the Aircraft (PM, supplementary procedure)
park = FLOWS[-1]['items'][-1]
park['d'] += "\n[FCTM PR-NP-CL-00019512.0001001 · SECURING THE AIRCRAFT:]\nSecuring the Aircraft is performed by the PM and is a Supplementary Procedure. Refer to FCOM/PRO-NOR-SUP-SEC."
if 'PRO-NOR-SUP-SEC' not in XREFS:
    t, b = sup_body('PRO-NOR-SUP-SEC'); XREFS['PRO-NOR-SUP-SEC'] = {'title': t, 'body': b}

out = {'FLOWS': FLOWS, 'XREFS': XREFS, 'NORMAL_CHECKLISTS': NORMAL_CHECKLISTS}
json.dump(out, open(os.path.join(WORK, 'data', 'flows_trainer.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
n_items = sum(len(f['items']) for f in FLOWS)
print('flows', len(FLOWS), 'items', n_items, 'xrefs', list(XREFS), 'checklists', len(NORMAL_CHECKLISTS),
      'rows', sum(len(v) for v in NORMAL_CHECKLISTS.values()))
for g in gaps: print('GAP:', g)
