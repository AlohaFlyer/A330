#!/usr/bin/env python3
"""Build the offline search indexes for the Manuals page (manuals/index.html).

Input : the PAX manual text extracts in SRC (page-form-feed separated, one
        form feed per PDF page, so PDF page = form feed index + 1).
Output: manuals/<key>.json per manual, key = the manuals.json key.
        Shape {meta:{key, title, revision, date, pdfPages, drive_url, built},
               toc:[{s, t, p}], docs:[{p, s, t, cp, x}]}
        where p is the PDF page, s the section id as the manual prints it,
        t the section title, cp the manual's own page mark when it has one,
        x the page text (whitespace collapsed, C0 controls dropped, otherwise
        verbatim, see norm_text).
        Big manuals are split: manuals/<key>.<part>.json holds {meta:{key,
        part}, docs:[...]} and manuals/<key>.json holds meta, toc and
        parts:[{part, file, bytes, pages}] with an empty docs list, so a phone
        loads only the part it searches. manuals/manifest.json lists every
        index file with its byte size for the offline tier.
        Nothing outside manuals/ receives manual text.

Freighter content is excluded: the freighter FCOM/QRH/NPC/PERF books are not
read at all, and inside the shared books the pages flagged below are dropped.

Section detection rules, one per manual (each decided after reading 20+ pages
of the extract, see the per-manual function docstrings):

  A330P_FCOM, A330_FCTM, A330_AFM  (Airbus page layout)
      Footer line "HAL A330 FLEET  <ident>  P n/m" carries the documentary unit
      ident (DSC-35-20-30, PRO-NOR-SOP-06, LIM-AFS-10, PR-NP-SOP-160, LIM-WGHT,
      MCDL-32-10). s = ident. Pages without a footer (dividers, blank pages,
      revision summary) inherit the previous page's section; pages before the
      first footer are FRONT. t comes from the running header of the section's
      first page: the first five non-empty lines minus the fixed tokens
      (A330, FLIGHT CREW, OPERATING MANUAL, TECHNIQUES MANUAL, AIRPLANE FLIGHT
      MANUAL) give chapter, subject and title fragments; t is the title when
      it shares a word with the subject, else "subject - title".
  A330P_QRH
      Header line 1 or 2 carries the page code (02.31A, GEN.02A, OPS.10A,
      57.01A): the digits before the letter identify the procedure, the letter
      the page. s = the procedure title printed on the line after
      "QUICK REFERENCE HANDBOOK" (two lines when the title wraps in caps),
      with "(Cont'd)" stripped. Pages sharing the code prefix or the title, and
      pages whose title line is "Continued from the previous page",
      "Intentionally left blank" or an Ident line, continue the section.
      Table-of-contents pages are "<CHAPTER> TABLE OF CONTENTS".
  A330_MEL
      Footer line "System NN: <name>" / "CDL NN: <name>" / "Chapter N: <name>".
      Inside System and CDL chapters an item starts at a line
      "^NN-NN[-N[A]]  <title>" (21-51-1A Pack Flow Control Valves, 53-04 Belly
      Fairing Seal); s = item number, t = title plus its indented wrap lines.
      Pages without an item header inherit (an item runs to "END NN-NN-N").
      Other chapters use the footer label as s and t.
  A330_AFM-SUPP
      Page 1 is the supplements and effectivity index. Pages 16 to 31 are STC
      U10-0720 (Starlink) and 32 to 39 the Lufthansa Technik supplement, keyed
      by the document number in the header or footer. Pages 40 to the end are
      the A330 P2F conversion AFM/FCOM supplement: freighter, excluded.
  A330_PRC
      Header: "A330 Pilot Reference Cards [Page: N]", "Date: d", then the card
      title. The title repeats as a centred heading, so t = the first line that
      appears twice among the first six body lines, else the first body line;
      "cont'd" pages continue the card. Pages carrying the "A330F ONLY" banner
      are freighter cards, excluded. Front pages (index, highlights) are INDEX.
  A330P_PERF
      Two page types. Runway analysis pages: line 1 is "<CITY>  -<IATA>  <RWY>";
      s = IATA, t = "<CITY> (<IATA>) takeoff analysis", one section per airport.
      Handbook pages: header "HAWAIIAN AIRLINES / Performance Handbook /
      <CHAPTER>" (or "AERODATA / ..."); s = chapter as printed; cp = the
      "A330  n.m  date" footer page mark. Other pages inherit.
  A330P_NPC-CB
      Three cards, one per page: s = the card title on line 1.
  FOM, FODM
      Header "Chapter: <code>" on line 1. Numeric chapters: a heading is a line
      "^x.y.z — Title" (em dash; cross references use an en dash), s = x.y.z.
      A page is labelled with the heading in progress at its top (the last
      heading before it, or the heading on its first body line). The toc lists
      every heading at the page it starts, and the page modal shows a section as
      its labelled pages plus its toc start page. Letter
      chapters (SE, RCR, TOC, RH, LES) are one section each, titled from their
      first page's "CODE — Title" line.
"""
import json, os, re, sys, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.abspath(os.path.join(HERE, '..'))
SRC = os.environ.get('A330_SRC', os.path.abspath(os.path.join(WORK, '..', 'src')))
OUT = os.path.join(WORK, 'manuals')
TODAY = datetime.date.today().isoformat()

FILES = {
    'A330P_FCOM': 'A330P_FCOM_R17.md',
    'A330P_QRH': 'A330P_QRH_R35.md',
    'A330_FCTM': 'A330_FCTM_R6.md',
    'A330_MEL': 'A330_MEL_R59.md',
    'A330_AFM': 'A330_AFM_2026-08-11.md',
    'A330_AFM-SUPP': 'A330_AFM-SUPP_2026-08-05.md',
    'A330_PRC': 'A330_PRC_2026-08-31.md',
    'A330P_PERF': 'A330P_PERF_R26-12.md',
    'A330P_NPC-CB': 'A330P_NPC-CB_2025-08-13.md',
    'FOM': 'FOM_125.3.md',
    'FODM': 'FODM_R0.md',
}
# Parts above this many bytes of page text are split into chapter files.
SPLIT_OVER = 1_500_000

CTRL = re.compile(r'[\x00-\x08\x0b\x0c\x0e-\x1f]')


def pages_of(text):
    """Form-feed split; the extract ends with a form feed so the last piece is empty."""
    parts = text.split('\f')
    if parts and parts[-1].strip() == '':
        parts = parts[:-1]
    return parts


def norm_text(page):
    """Verbatim text with C0 controls dropped, runs of blanks collapsed, blank lines removed."""
    out = []
    for line in CTRL.sub('', page).split('\n'):
        line = re.sub(r'[ \t ]+', ' ', line).strip()
        if line:
            out.append(line)
    return '\n'.join(out)


def lines_of(page):
    return [l for l in norm_text(page).split('\n') if l]


# ---------------------------------------------------------------- Airbus layout
FOOT = re.compile(r'HAL A330 FLEET\s+([A-Z][A-Za-z0-9_-]*)(?:\s+P\s+(\d+)/(\d+))?\s*$')
AIRBUS_TOKENS = ('A330', 'FLIGHT CREW', 'OPERATING MANUAL', 'TECHNIQUES MANUAL', 'AIRPLANE FLIGHT MANUAL')


def airbus_header(lines):
    """chapter, subject, title from the first five header lines."""
    frags = []
    for l in lines[:5]:
        s = l
        for tk in AIRBUS_TOKENS:
            s = s.replace(tk, ' ')
        s = re.sub(r'\s+', ' ', s).strip(' -')
        if s and not re.search(r'[a-z]', s) and not s.startswith('HAL ') and not re.match(r'^(P \d+/\d+|\d{2} [A-Z]{3} \d{2})$', s):
            frags.append(s)
    if not frags:
        return '', '', ''
    chapter = frags[0]
    subject = frags[1] if len(frags) > 1 else ''
    title = ' - '.join(frags[2:]).replace(' -  - ', ' - ').replace('- -', '-').strip(' -')
    return chapter, subject, title


def airbus_title(chapter, subject, title):
    if title and subject:
        sw = set(re.findall(r'[A-Z]{3,}', subject))
        tw = set(re.findall(r'[A-Z]{3,}', title))
        return title if (sw & tw) else subject + ' - ' + title
    return title or subject or chapter or 'FRONT MATTER'


def rule_airbus(pages):
    """FCOM, FCTM, AFM: footer ident. Returns per-page records (s, t, cp) with inheritance."""
    recs = []
    cur_s, cur_t = 'FRONT', 'Front matter'
    first_title = {}
    for i, page in enumerate(pages):
        lines = lines_of(page)
        if not lines:
            recs.append(None)
            continue
        m = None
        for l in lines[-3:]:
            mm = FOOT.search(l)
            if mm:
                m = mm
        cp = ''
        if m:
            cur_s = m.group(1)
            if m.group(2):
                cp = 'P ' + m.group(2) + '/' + m.group(3)
            if cur_s not in first_title:
                ch, sub, ti = airbus_header(lines)
                first_title[cur_s] = airbus_title(ch, sub, ti)
            cur_t = first_title[cur_s]
        recs.append((cur_s, cur_t, cp))
    return recs


# ---------------------------------------------------------------- QRH
QCODE = re.compile(r'\b((?:[A-Z]{2,3}|\d{2})\.\d{2})([A-Z])\b')


def rule_qrh(pages):
    recs = []
    cur_s, cur_t, cur_code = 'FRONT', 'Front matter', None
    for page in pages:
        lines = lines_of(page)
        if not lines:
            recs.append(None)
            continue
        head = ' '.join(lines[:3])
        m = QCODE.search(head)
        code = m.group(1) if m else None
        cp = (m.group(1) + m.group(2)) if m else ''
        title = ''
        toc = any('TABLE OF CONTENTS' in l for l in lines[:4])
        qi = next((k for k, l in enumerate(lines[:6]) if 'QUICK REFERENCE HANDBOOK' in l), None)
        if qi is not None and qi + 1 < len(lines):
            title = lines[qi + 1]
            nxt = lines[qi + 2] if qi + 2 < len(lines) else ''
            if (nxt and not re.search(r'[a-z]', nxt) and len(nxt) < 60 and '....' not in nxt
                    and not nxt.startswith(('Ident', 'HAL ')) and not re.match(r'^[A-Z]+\d*$', nxt.replace(' ', ''))
                    and not re.search(r'\d/\d|:$', nxt)):
                title = title + ' ' + nxt
        cont = (not title or title.startswith(('Continued from', 'Ident', 'Intentionally left blank', 'HAL A330'))
                or "(Cont'd)" in title or '(Cont’d)' in title)
        title_clean = re.sub(r"\s*\((Cont'd|Cont’d)\)\s*$", '', title).strip()
        lep = any('LIST OF EFFECTIVE PAGES' in l for l in lines[:3])
        if lep:
            cur_s, cur_t, cur_code = 'LIST OF EFFECTIVE PAGES', 'List of effective pages', None
        elif toc:
            chap = ''
            for l in lines[:2]:
                l = re.sub(r'\s*\b(GEN|ABN|NP|OPS|OEBPROC)\s*$', '', l)
                l = re.sub(r'\s*\d/\d\s*$', '', l).strip()
                if l and 'TABLE OF CONTENTS' not in l and l != 'A330':
                    chap += (' ' if chap else '') + l
            cur_s, cur_t = chap + ' TABLE OF CONTENTS', 'Table of contents, ' + chap.title()
            cur_code = None
        elif code and code == cur_code:
            pass
        elif cont and title_clean and title_clean.upper() == cur_t.upper():
            cur_code = code or cur_code
        elif cont:
            cur_code = code or cur_code
        elif title_clean:
            if title_clean.upper() != cur_t.upper():
                cur_s, cur_t = title_clean, title_clean
            cur_code = code
        recs.append((cur_s, cur_t, cp))
    return recs


# ---------------------------------------------------------------- MEL
MEL_ITEM = re.compile(r'^(\d{2}-\d{2}(?:-\d{1,2}[A-Z]?)?)\s+(\S.*)$')
MEL_FOOT = re.compile(r'^(System \d+|CDL \d+|Chapter \d+|Appendix [A-Z]):\s*(.+)$')


def rule_mel(pages):
    recs = []
    cur_s, cur_t = 'FRONT', 'Front matter'
    for page in pages:
        raw = [l for l in CTRL.sub('', page).split('\n') if l.strip()]
        lines = [re.sub(r'\s+', ' ', l).strip() for l in raw]
        if not lines:
            recs.append(None)
            continue
        foot = lines[-2] if len(lines) >= 2 else ''
        cp = ''
        mp = re.match(r'^Page:\s*(\S+ of \S+)', lines[0]) if lines else None
        if mp:
            cp = mp.group(1)
        fm = MEL_FOOT.match(foot)
        if fm and fm.group(1).startswith(('System', 'CDL')):
            body = raw[3:-2]
            hit = None
            for k, l in enumerate(body):
                m = MEL_ITEM.match(l.strip())
                if m and len(l) - len(l.lstrip()) < 12:
                    hit = (k, m)
                    break
            if hit:
                k, m = hit
                title = re.sub(r'\s+', ' ', m.group(2)).strip()
                title = re.sub(r'\s*\.{3,}.*$', '', title)
                for l in body[k + 1:k + 3]:
                    ind = len(l) - len(l.lstrip())
                    s = l.strip()
                    if ind >= 12 and s and not s.startswith(('Effectivity', 'PROC', 'Quantity', '(')) and len(s) < 80 and not re.match(r'^[A-Z]{1,4}$', s):
                        title += ' ' + s
                    else:
                        break
                cur_s, cur_t = m.group(1), title
            elif not cur_s.startswith(fm.group(1)) and not re.match(r'^\d{2}-\d{2}', cur_s):
                cur_s, cur_t = foot, foot
            elif re.match(r'^\d{2}-\d{2}', cur_s) and cur_s[:2] != fm.group(1).split()[1].zfill(2):
                cur_s, cur_t = foot, foot
        elif foot and not foot.startswith('Uncontrolled') and re.search(r'[A-Za-z]', foot):
            lab = re.sub(r'\s+END$', '', re.sub(r'\s+', ' ', foot).strip())
            cur_s, cur_t = lab, lab
        recs.append((cur_s, cur_t, cp))
    return recs


# ---------------------------------------------------------------- AFM supplement
def rule_afm_supp(pages):
    recs = []
    cur = ('EFFECTIVITY', 'A330 AFM Supplements and Effectivity', '')
    for i, page in enumerate(pages):
        if i >= 39:
            recs.append('EXCLUDED')
            continue
        lines = lines_of(page)
        if not lines:
            recs.append(None)
            continue
        if i == 0:
            recs.append(cur)
            continue
        head = ' '.join(lines[:6])
        m = re.search(r'\b(U10-0720)\b', head)
        if m:
            cur = ('U10-0720', 'AFM Supplement, Starlink Aviation System Installation (STC U10-0720)', '')
        else:
            mm = re.search(r'DOC-NO\.\s*(\S+)', ' '.join(lines))
            if mm or 'Airbus A330 - Series' in head:
                cur = ((mm.group(1) if mm else 'A-33-05/348-AFM'), 'Airplane Flight Manual Supplement, Lufthansa Technik', '')
        pm = re.search(r'Page (\d+ of \d+)', ' '.join(lines[-3:]))
        recs.append((cur[0], cur[1], pm.group(1) if pm else ''))
    return recs


# ---------------------------------------------------------------- PRC
def rule_prc(pages):
    recs = []
    cur_s, cur_t = 'INDEX', 'Pilot Reference Cards index and change highlights'
    for i, page in enumerate(pages):
        lines = lines_of(page)
        if not lines:
            recs.append(None)
            continue
        if any('A330F ONLY' in l for l in lines[:2]):
            recs.append('EXCLUDED')
            continue
        cp = ''
        pm = re.search(r'Page:\s*(\d+)', lines[0])
        if pm:
            cp = 'card page ' + pm.group(1)
        body = [l for l in lines[:12] if not re.search(r'A330 Pilot Reference Cards|^Date:|^FAA Approved$|^Page:|^Issued:', l)]
        if i < 6:
            recs.append((cur_s, cur_t, cp))
            continue
        cand = body[:6]
        title = ''
        for c in cand:
            if cand.count(c) > 1 and len(c) < 90:
                title = c
                break
        if not title and cand:
            title = cand[0]
        title = re.sub(r'\s*\.{3,}.*$', '', title).strip()
        cont = bool(re.search(r"\bcont[’']d\s*$", title, re.I))
        clean = re.sub(r"\s*cont[’']d\s*$", '', title, flags=re.I).strip()
        if cont or clean.lower() == cur_t.lower() or not clean:
            pass
        else:
            cur_s, cur_t = clean, clean
        recs.append((cur_s, cur_t, cp))
    return recs


# ---------------------------------------------------------------- PERF
APT = re.compile(r'^(.+?)\s+-([A-Z]{3})\s+(\S+)(?:\s+.*)?$')


def rule_perf(pages):
    recs = []
    cur_s, cur_t = 'FRONT', 'Front matter'
    for page in pages:
        lines = lines_of(page)
        if not lines:
            recs.append(None)
            continue
        cp = ''
        m = APT.match(lines[0])
        if m and len(lines) > 3 and 'Engine Failure' in ' '.join(lines[:3]):
            city = re.sub(r'\s+', ' ', m.group(1)).strip()
            cur_s, cur_t = m.group(2), city + ' (' + m.group(2) + ') takeoff analysis'
            cp = 'RWY ' + m.group(3)
        elif len(lines) > 2 and lines[1].strip() == 'Performance Handbook':
            chap = lines[2].strip()
            if chap.startswith(('Prepared by', 'Aircraft / Manual')):
                chap = 'FRONT'
            cur_s, cur_t = chap, chap if chap != 'FRONT' else 'Front matter'
            fm = re.match(r'^A330\s+(\S+)\s+\d{2} [A-Z]{3} \d{2}$', lines[-1])
            if fm:
                cp = 'page ' + fm.group(1)
        elif lines[0].startswith('REVISION RECORD'):
            cur_s, cur_t = 'REVISION RECORD', 'Revision Record'
        recs.append((cur_s, cur_t, cp))
    return recs


# ---------------------------------------------------------------- NPC card book
def rule_npc(pages):
    recs = []
    for page in pages:
        lines = lines_of(page)
        if not lines:
            recs.append(None)
            continue
        t = lines[0].strip()
        recs.append((t, t, ''))
    return recs


# ---------------------------------------------------------------- FOM / FODM
FOM_HEAD = re.compile(r'^(\d{1,2}(?:\.\d{1,3}){0,4})\s+—\s+(\S.*?)\s*$')


def rule_fom(pages):
    """Returns recs plus an explicit toc built from every heading."""
    recs = []
    toc = []
    seen = {}
    cur_s, cur_t = 'FRONT', 'Front matter'
    letter_title = {}
    for i, page in enumerate(pages):
        lines = lines_of(page)
        if not lines:
            recs.append(None)
            continue
        cm = re.match(r'^Chapter:\s*(\S+)', lines[0])
        chap = cm.group(1) if cm else None
        cp = lines[-1] if re.match(r'^\d+$', lines[-1]) else ''
        if chap and not chap.isdigit():
            if chap not in letter_title:
                tm = next((re.match(r'^' + re.escape(chap) + r'\s+—\s+(.+)$', l) for l in lines[3:6] if l.startswith(chap)), None)
                letter_title[chap] = tm.group(1).strip() if tm else chap
                toc.append({'s': chap, 't': letter_title[chap], 'p': i + 1})
                seen[chap] = 1
            cur_s, cur_t = chap, letter_title[chap]
            recs.append((cur_s, cur_t, cp))
            continue
        if chap:
            # label = the heading in progress at the top of the page, unless the first
            # body line is itself a heading; then advance to the last heading on the page
            label = (cur_s, cur_t)
            body = lines[3:]
            for k, l in enumerate(body):
                m = FOM_HEAD.match(l)
                if m:
                    s, t = m.group(1), m.group(2)
                    if k == 0:
                        label = (s, t)
                    if s not in seen:
                        seen[s] = 1
                        toc.append({'s': s, 't': t, 'p': i + 1})
                    cur_s, cur_t = s, t
            recs.append((label[0], label[1], cp))
            continue
        recs.append((cur_s, cur_t, cp))
    return recs, toc


# ---------------------------------------------------------------- parts
def part_fcom(s):
    top = s.split('-')[0]
    if top == 'DSC':
        m = re.match(r'^DSC-(\d{2})', s)
        return 'DSC-' + m.group(1) if m else 'DSC'
    if top == 'PRO':
        return '-'.join(s.split('-')[:2]) if s.count('-') >= 1 else 'PRO'
    if top in ('LIM', 'PER'):
        return top
    return 'FRONT'


def part_mel(s):
    m = re.match(r'^(\d{2})-', s)
    if not m:
        m = re.match(r'^(?:System|CDL) (\d+)', s)
    if not m:
        return 'GEN'
    n = int(m.group(1))
    if n <= 24:
        return 'ATA21-24'
    if n <= 28:
        return 'ATA25-28'
    if n <= 33:
        return 'ATA29-33'
    if n <= 49:
        return 'ATA34-49'
    return 'ATA50-80'


def part_perf(s):
    if len(s) == 3 and s.isupper() and s.isalpha():
        if s[0] <= 'K':
            return 'APT-A-K'
        if s[0] <= 'R':
            return 'APT-L-R'
        return 'APT-S-Z'
    return 'HANDBOOK'


PARTS = {'A330P_FCOM': part_fcom, 'A330_MEL': part_mel, 'A330P_PERF': part_perf}
RULES = {
    'A330P_FCOM': rule_airbus, 'A330_FCTM': rule_airbus, 'A330_AFM': rule_airbus,
    'A330P_QRH': rule_qrh, 'A330_MEL': rule_mel, 'A330_AFM-SUPP': rule_afm_supp,
    'A330_PRC': rule_prc, 'A330P_PERF': rule_perf, 'A330P_NPC-CB': rule_npc,
    'FOM': rule_fom, 'FODM': rule_fom,
}


def dump(path, obj):
    s = json.dumps(obj, ensure_ascii=False, separators=(',', ':'))
    with open(path, 'w', encoding='utf-8') as f:
        f.write(s)
    return len(s.encode('utf-8'))


def build(key, manuals):
    fn = FILES[key]
    text = open(os.path.join(SRC, fn), encoding='utf-8').read()
    pages = pages_of(text)
    res = RULES[key](pages)
    toc = None
    if isinstance(res, tuple):
        recs, toc = res
    else:
        recs = res
    docs, excluded, empty = [], [], []
    for i, r in enumerate(recs):
        if r is None:
            empty.append(i + 1)
            continue
        if r == 'EXCLUDED':
            excluded.append(i + 1)
            continue
        s, t, cp = r
        x = norm_text(pages[i])
        d = {'p': i + 1, 's': s, 't': t, 'cp': cp, 'x': x}
        docs.append(d)
    if toc is None:
        toc = []
    seen = {}
    for e in toc:
        seen[e['s']] = 1
    for d in docs:                       # every label a doc carries is browsable
        if d['s'] not in seen:
            seen[d['s']] = 1
            toc.append({'s': d['s'], 't': d['t'], 'p': d['p']})
    toc.sort(key=lambda e: e['p'])
    m = manuals[key]
    meta = {
        'key': key, 'title': m['title'], 'revision': m['revision'], 'date': m['date'],
        'pdfPages': len(pages), 'drive_url': m['drive_url'], 'built': TODAY,
        'source': fn, 'pages': len(docs), 'sections': len(toc),
        'emptyPages': len(empty), 'excludedPages': excluded,
    }
    files = []
    total_x = sum(len(d['x']) for d in docs)
    if key in PARTS and total_x > SPLIT_OVER:
        groups = {}
        for d in docs:
            groups.setdefault(PARTS[key](d['s']), []).append(d)
        parts = []
        for part in sorted(groups):
            fname = key + '.' + part + '.json'
            n = dump(os.path.join(OUT, fname), {'meta': {'key': key, 'part': part}, 'docs': groups[part]})
            parts.append({'part': part, 'file': fname, 'bytes': n, 'pages': len(groups[part])})
            files.append((fname, n))
        n = dump(os.path.join(OUT, key + '.json'), {'meta': meta, 'toc': toc, 'parts': parts, 'docs': []})
        files.append((key + '.json', n))
    else:
        n = dump(os.path.join(OUT, key + '.json'), {'meta': meta, 'toc': toc, 'docs': docs})
        files.append((key + '.json', n))
    return meta, files


def main():
    os.makedirs(OUT, exist_ok=True)
    manuals = json.load(open(os.path.join(WORK, 'manuals.json'), encoding='utf-8'))
    manifest = {'built': TODAY, 'files': []}
    for key in FILES:
        meta, files = build(key, manuals)
        for fname, n in files:
            manifest['files'].append({'file': fname, 'bytes': n, 'key': key})
        print('%-14s pages %5d  docs %5d  sections %5d  excluded %3d  files %2d  %6.2f MB' % (
            key, meta['pdfPages'], meta['pages'], meta['sections'], len(meta['excludedPages']), len(files),
            sum(n for _, n in files) / 1e6))
    manifest['files'].sort(key=lambda f: f['file'])
    manifest['totalBytes'] = sum(f['bytes'] for f in manifest['files'])
    dump(os.path.join(OUT, 'manifest.json'), manifest)
    print('manifest: %d files, %.1f MB' % (len(manifest['files']), manifest['totalBytes'] / 1e6))


if __name__ == '__main__':
    main()
