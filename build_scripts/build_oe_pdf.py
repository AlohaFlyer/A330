#!/usr/bin/env python3
"""Build A330_OE_Workbook_Answered.pdf from data/oe.json.

Port of the B787 build_ioe_pdf.py for the A330 PAX portal. Organized by topic in flight
order with a table of contents, a Numbers to Know page up front, and key facts set larger
and bold. Manual revision strings come from manuals.json; nothing is hardcoded here.

Usage: build_oe_pdf.py [--bank data/oe.json] [--out A330_OE_Workbook_Answered.pdf]
"""
import json, re, html, os, argparse, datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
                                Spacer, Table, TableStyle, PageBreak, CondPageBreak)
from reportlab.platypus.tableofcontents import TableOfContents

HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.dirname(HERE)

MIDNIGHT = colors.HexColor('#463C8F')   # headings
ATLAS    = colors.HexColor('#CE0C88')
GREEN    = colors.HexColor('#00805E')
AMBER    = colors.HexColor('#8A5A12')
GREY     = colors.HexColor('#5A6B78')
LINE     = colors.HexColor('#D9D3EA')
BAND     = colors.HexColor('#F4F1F9')

TOPIC_ORDER = [
    'Emergency Equipment', 'Security and Doors', 'Crew Rest', 'EFB and FD Pro',
    'Dispatch and Release', 'Fuel Planning', 'Weather and Minimums',
    'Communications and PA', 'Pushback and Start', 'Taxi and Ground',
    'Cold Weather and Runway Condition', 'Takeoff and Departure',
    'Cruise and Diversion', 'ETOPS', 'Oceanic', 'International Theaters',
    'TCAS and Traffic', 'Medical', 'HAZMAT', 'Descent and Approach',
    'Landing and Rollout', 'MEL and Maintenance', 'Abnormals and QRH',
    'CRM and PM Duties', 'General Operations',
]

DESK = "No published source located, ask the check airman"


def esc(s):
    return html.escape(s or '', quote=False)


def is_gold(c):
    """A fact worth knowing cold: short, verified, and it carries a number."""
    return (c['status'] == 'verified' and c['kind'] == 'drill'
            and re.search(r'\d', c['a']) and len(c['a'].split()) <= 12)


S = dict(
    topic = ParagraphStyle('topic', fontName='Helvetica-Bold', fontSize=15, leading=18, textColor=colors.white),
    grp   = ParagraphStyle('grp', fontName='Helvetica-Bold', fontSize=9, leading=12, textColor=ATLAS,
                           spaceBefore=10, spaceAfter=2, keepWithNext=1),
    tag   = ParagraphStyle('tag', fontName='Helvetica-Bold', fontSize=7, leading=9, textColor=GREY,
                           spaceBefore=0, spaceAfter=1, keepWithNext=1),
    coi   = ParagraphStyle('coi', fontName='Helvetica-Bold', fontSize=7, leading=9, textColor=GREEN,
                           spaceBefore=0, spaceAfter=1, keepWithNext=1),
    q     = ParagraphStyle('q', fontName='Helvetica-Bold', fontSize=12.5, leading=16, textColor=MIDNIGHT,
                           spaceBefore=9, spaceAfter=1, keepWithNext=1),
    ans   = ParagraphStyle('ans', fontName='Helvetica-Bold', fontSize=11, leading=14, textColor=GREEN,
                           spaceBefore=2, spaceAfter=3),
    gold  = ParagraphStyle('gold', fontName='Helvetica-Bold', fontSize=14, leading=17, textColor=GREEN,
                           spaceBefore=3, spaceAfter=4),
    ansr  = ParagraphStyle('ansr', fontName='Helvetica-Bold', fontSize=11, leading=14, textColor=AMBER,
                           spaceBefore=2, spaceAfter=3),
    body  = ParagraphStyle('body', fontName='Helvetica', fontSize=9.5, leading=12.5, textColor=colors.black, spaceAfter=2),
    ref   = ParagraphStyle('ref', fontName='Helvetica-Bold', fontSize=8.5, leading=11, textColor=ATLAS, leftIndent=10, spaceBefore=3),
    quote = ParagraphStyle('quote', fontName='Helvetica-Oblique', fontSize=8.5, leading=11,
                           textColor=colors.HexColor('#2E2A45'), leftIndent=21, rightIndent=8, spaceBefore=2),
    note  = ParagraphStyle('note', fontName='Helvetica', fontSize=8.5, leading=11, textColor=GREY, leftIndent=10, spaceBefore=2),
    orig  = ParagraphStyle('orig', fontName='Helvetica-Oblique', fontSize=7, leading=9,
                           textColor=colors.HexColor('#8A86A0'), leftIndent=10, spaceBefore=3),
    h1    = ParagraphStyle('h1', fontName='Helvetica-Bold', fontSize=21, leading=25, textColor=MIDNIGHT, spaceAfter=2),
    h2    = ParagraphStyle('h2', fontName='Helvetica', fontSize=12, leading=16, textColor=ATLAS, spaceAfter=10),
    lead  = ParagraphStyle('lead', fontName='Helvetica', fontSize=9.5, leading=13, textColor=colors.black, spaceAfter=6),
    cell  = ParagraphStyle('cell', fontName='Helvetica', fontSize=9, leading=12),
    cellb = ParagraphStyle('cellb', fontName='Helvetica-Bold', fontSize=9, leading=12),
    numq  = ParagraphStyle('numq', fontName='Helvetica', fontSize=9.5, leading=13),
    numa  = ParagraphStyle('numa', fontName='Helvetica-Bold', fontSize=11, leading=13, textColor=GREEN),
    toch  = ParagraphStyle('toch', fontName='Helvetica-Bold', fontSize=14, leading=18, textColor=MIDNIGHT,
                           spaceBefore=6, spaceAfter=10),
)
TOC_LEVEL = ParagraphStyle('toc0', fontName='Helvetica', fontSize=10.5, leading=16, textColor=MIDNIGHT, leftIndent=4)


class Doc(BaseDocTemplate):
    def afterFlowable(self, fl):
        if getattr(fl, '_toc', None):
            self.notify('TOCEntry', (0, fl._toc, self.page))


def topic_band(title, n, width):
    p = Paragraph('%s  <font size="9">(%d)</font>' % (esc(title), n), S['topic'])
    t = Table([[p]], colWidths=[width])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), MIDNIGHT),
        ('LEFTPADDING', (0, 0), (-1, -1), 9), ('RIGHTPADDING', (0, 0), (-1, -1), 9),
        ('TOPPADDING', (0, 0), (-1, -1), 7), ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
    ]))
    t._toc = title
    return t


def source_block(c, width):
    rows = []
    if c['ref']:
        rows.append(Paragraph(esc(c['ref']), S['ref']))
    if c['quote']:
        qtxt = c['quote']
        opening = '' if qtxt.lstrip().startswith(('"', '“')) else '&ldquo;'
        closing = '' if qtxt.rstrip().endswith(('"', '”')) else '&rdquo;'
        rows.append(Paragraph(opening + esc(qtxt) + closing, S['quote']))
    if c['note']:
        rows.append(Paragraph(esc(c['note']), S['note']))
    if c['qOrig'] and c['qOrig'].strip() != c['q'].strip():
        rows.append(Paragraph('Workbook wording: %s' % esc(c['qOrig']), S['orig']))
    if not rows:
        return None
    t = Table([[rows]], colWidths=[width])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), BAND),
        ('LINEBEFORE', (0, 0), (0, -1), 2, ATLAS),
        ('LEFTPADDING', (0, 0), (-1, -1), 7), ('RIGHTPADDING', (0, 0), (-1, -1), 7),
        ('TOPPADDING', (0, 0), (-1, -1), 5), ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    return t


def rev(man, key, label):
    m = man.get(key, {})
    r = m.get('revision')
    return '%s %s' % (label, r) if r else '%s %s' % (label, m.get('date', ''))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--bank', default=os.path.join(WORK, 'data', 'oe.json'))
    ap.add_argument('--out', default=os.path.join(WORK, 'A330_OE_Workbook_Answered.pdf'))
    ap.add_argument('--manuals', default=os.path.join(WORK, 'manuals.json'))
    ns = ap.parse_args()

    cards = json.load(open(ns.bank, encoding='utf-8'))
    man = json.load(open(ns.manuals, encoding='utf-8'))
    fcom, qrh, fctm, fom = (rev(man, 'A330P_FCOM', 'FCOM'), rev(man, 'A330P_QRH', 'QRH'),
                            rev(man, 'A330_FCTM', 'FCTM'), rev(man, 'FOM', 'FOM'))
    prc = 'PRC ' + man.get('A330_PRC', {}).get('date', '')
    revline = ', '.join([fcom, qrh, fctm, fom])
    footer = 'ha330pilot.app · %s · study aid only, the current manuals govern' % revline

    nv = sum(1 for c in cards if c['status'] == 'verified')
    nd = len(cards) - nv
    ncoi = sum(1 for c in cards if c['coi'])
    nw = sum(1 for c in cards if c.get('kind') == 'walkthrough')

    by_topic = {}
    for c in cards:
        by_topic.setdefault(c['topic'], []).append(c)
    order = [t for t in TOPIC_ORDER if t in by_topic] + [t for t in sorted(by_topic) if t not in TOPIC_ORDER]

    doc = Doc(ns.out, pagesize=letter,
              leftMargin=0.62*inch, rightMargin=0.62*inch, topMargin=0.72*inch, bottomMargin=0.62*inch,
              title='A330 OE Workbook Answered', author='ha330pilot.app',
              subject='787/A321/A330 Fleets OE Workbook, A330 PAX items answered',
              creator='ha330pilot.app', keywords='A330, OE, OE Workbook, FOM, FCOM, QRH, FCTM, PRC')
    W = doc.width

    def deco(canv, d):
        canv.saveState()
        canv.setFont('Helvetica', 8)
        canv.setFillColor(GREY)
        canv.drawString(d.leftMargin, letter[1] - 0.47*inch, 'A330 OE Workbook, Answered')
        canv.drawRightString(letter[0] - d.rightMargin, letter[1] - 0.47*inch, revline.replace(', ', '  |  '))
        canv.setStrokeColor(LINE)
        canv.setLineWidth(0.5)
        canv.line(d.leftMargin, letter[1] - 0.55*inch, letter[0] - d.rightMargin, letter[1] - 0.55*inch)
        canv.line(d.leftMargin, 0.55*inch, letter[0] - d.rightMargin, 0.55*inch)
        canv.setFont('Helvetica', 7.5)
        canv.drawString(d.leftMargin, 0.40*inch, footer)
        canv.drawRightString(letter[0] - d.rightMargin, 0.40*inch, 'Page %d' % canv.getPageNumber())
        canv.restoreState()

    doc.addPageTemplates([PageTemplate(id='main',
                          frames=[Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id='f')],
                          onPage=deco)])
    st = []

    # ---- Cover ----
    st.append(Paragraph('A330 OE Workbook', S['h1']))
    st.append(Paragraph('Answered, in flashcard form', S['h2']))
    st.append(Paragraph('Source: 787/A321/A330 Fleets OE Workbook, Version 2, January 2026. '
                        'A330 PAX items only: items marked (330), (330/321), (787/330), and the fleet-common items. '
                        'Items marked (787) only, (A321) only, and the Freighter Operations group are left out.', S['lead']))
    rows = [
        ['Workbook items', str(len(cards))],
        ['Answered from the manuals', str(nv)],
        ['No published source, ask the check airman', str(nd)],
        ['Critical Observable Items', str(ncoi)],
        ['Drill cards / walkthrough items', '%d / %d' % (len(cards) - nw, nw)],
        ['Manuals used', '%s (%s), %s (%s), %s (%s), %s (%s), %s' % (
            fcom, man['A330P_FCOM']['date'], qrh, man['A330P_QRH']['date'], fctm, man['A330_FCTM']['date'],
            fom, man['FOM']['date'], prc)],
        ['Compiled', datetime.date.today().strftime('%B %Y')],
    ]
    t = Table([[Paragraph(a, S['cell']), Paragraph(b, S['cellb'])] for a, b in rows],
              colWidths=[2.5*inch, W - 2.5*inch])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), BAND), ('LINEBELOW', (0, 0), (-1, -2), 0.4, colors.white),
        ('LEFTPADDING', (0, 0), (-1, -1), 9), ('TOPPADDING', (0, 0), (-1, -1), 4), ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    st.append(t)
    st.append(Spacer(1, 14))
    st.append(Paragraph('How to read this document', S['q']))
    st.append(Paragraph(
        'Each question carries the answer in green, and nothing else. That green line is what you should be able '
        'to say cold. Key numbers are set larger so they land at a glance. Everything under the answer is the backup: '
        'the full answer, the manual location, a verbatim quote from the extract, and a note.', S['body']))
    st.append(Paragraph(
        'Questions are grouped by topic in roughly the order you meet them on a trip, preflight to shutdown, with the '
        'long-haul topics in the middle. The tag above each question carries the grade sheet item it came from. '
        'Walkthrough items are things you perform on the line rather than recite.', S['body']))
    st.append(Paragraph(
        'An item in amber has no published answer in the FOM, FCOM, QRH, FCTM or PRC. The card says so and tells '
        'you to ask the check airman. Nothing was guessed.', S['body']))
    st.append(Paragraph(
        'The flight deck door entry code is deliberately not recorded. It is security sensitive information and does '
        'not belong in a study document.', S['body']))

    # ---- Numbers to Know ----
    gold = [c for c in cards if is_gold(c)]
    trank = {t: i for i, t in enumerate(TOPIC_ORDER)}
    gold.sort(key=lambda c: trank.get(c['topic'], 99))
    st.append(PageBreak())
    st.append(Paragraph('Numbers to Know', S['h1']))
    st.append(Paragraph('The facts on these cards worth knowing cold before the first leg.', S['h2']))
    nrows = [[Paragraph(esc(c['q']), S['numq']), Paragraph(esc(c['a']), S['numa'])] for c in gold]
    nt = Table(nrows, colWidths=[W * 0.55, W * 0.45])
    nt.setStyle(TableStyle([
        ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.white, BAND]), ('LINEBELOW', (0, 0), (-1, -1), 0.3, LINE),
        ('LEFTPADDING', (0, 0), (-1, -1), 6), ('TOPPADDING', (0, 0), (-1, -1), 5), ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    st.append(nt)

    # ---- Contents ----
    st.append(PageBreak())
    st.append(Paragraph('Contents', S['toch']))
    toc = TableOfContents()
    toc.levelStyles = [TOC_LEVEL]
    st.append(toc)

    # ---- Cards, by topic ----
    for topic in order:
        group = by_topic[topic]
        if topic == order[0]:
            st.append(PageBreak())
        else:
            st.append(Spacer(1, 14))
            st.append(CondPageBreak(2.2*inch))
        st.append(topic_band(topic, len(group), W))
        last_grp = None
        for c in group:
            blk = []
            if c['group'] and c['group'] != last_grp:
                blk.append(Paragraph(esc(c['group']), S['grp']))
                last_grp = c['group']
            if c['coi']:
                blk.append(Paragraph('CRITICAL OBSERVABLE ITEM', S['coi']))
            meta = c['sec'] + '  ' + c['secTitle']
            if c.get('kind') == 'walkthrough':
                meta += '   WALKTHROUGH ITEM, PERFORM RATHER THAN RECALL'
            blk.append(Paragraph(esc(meta).upper(), S['tag']))
            blk.append(Paragraph(esc(c['q']), S['q']))
            if c['status'] == 'verified':
                blk.append(Paragraph(esc(c['a']), S['gold'] if is_gold(c) else S['ans']))
            else:
                blk.append(Paragraph(esc(DESK), S['ansr']))
            if c['detail']:
                blk.append(Paragraph(esc(c['detail']), S['body']))
            sb = source_block(c, W)
            if sb is not None:
                blk.append(sb)
            st.extend(blk)

    doc.multiBuild(st)
    print('built %s  (%d cards, %d gold, %d topics)' % (ns.out, len(cards), len(gold), len(order)))


if __name__ == '__main__':
    main()
