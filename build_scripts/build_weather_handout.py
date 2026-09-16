#!/usr/bin/env python3
"""Build A330_Weather_Requirements.pdf from data/weather.json (reportlab, letter).
Same information as the bank, grouped by category, in the order the bank drills.
One page does not hold 32 rows at a readable size (6.6 pt); the table flows to page 2 with the header repeated.
Purple #463C8F headings, fuchsia #CE0C88 category accents. Revision string from manuals.json."""
import json, os, re, html
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

M = json.load(open('manuals.json'))
FOM = M['FOM']; frev = FOM['revision']; fdate = FOM['date']
P = colors.HexColor('#463C8F'); F = colors.HexColor('#CE0C88'); PALE = colors.HexColor('#EAE5F4'); GREY = colors.HexColor('#6F6B7E')
ss = getSampleStyleSheet()
H = ParagraphStyle('h', parent=ss['Title'], fontSize=14, leading=16, textColor=P, spaceAfter=1, alignment=0)
S = ParagraphStyle('s', parent=ss['Normal'], fontSize=7, leading=8.5, textColor=GREY, spaceAfter=4)
N = ParagraphStyle('n', parent=ss['Normal'], fontSize=6.6, leading=7.7)
Q = ParagraphStyle('q', parent=N, textColor=P, fontName='Helvetica-Bold')
CAT = ParagraphStyle('cat', parent=N, fontSize=7, leading=8.4, textColor=F, fontName='Helvetica-Bold')
REF = ParagraphStyle('r', parent=N, fontSize=5.8, leading=7, textColor=GREY)
foot = f'ha330pilot.app · FOM {frev} · study aid only, the current FOM governs'

def clean(h):
    """Bank answer html -> reportlab mini-html: keep <b>, drop the rest, unescape entities."""
    h = re.sub(r'<(?!/?b>)[^>]+>', '', h)
    h = h.replace('&nbsp;', ' ')
    parts = re.split(r'(</?b>)', h)
    out = ''.join(p if p in ('<b>', '</b>') else html.escape(html.unescape(p), quote=False) for p in parts)
    return out

bank = json.load(open('data/weather.json', encoding='utf-8'))
doc = SimpleDocTemplate('A330_Weather_Requirements.pdf', pagesize=letter, leftMargin=.4 * inch, rightMargin=.4 * inch,
                        topMargin=.35 * inch, bottomMargin=.33 * inch, title='A330 Weather Requirements', author='ha330pilot.app')
story = [Paragraph(f'A330 Weather Requirements, FOM {frev}', H),
         Paragraph(f'{len(bank)} dispatch and weather rules from FOM {frev} ({fdate}), grouped as the quiz drills them. '
                   f'Fleet-common FOM text; A330 rows quoted where the FOM banners fleets. {foot}', S)]
rows = [[Paragraph('<b>Item</b>', N), Paragraph('<b>Requirement</b>', N), Paragraph('<b>FOM</b>', N)]]
spans = []
seen = []
for d in bank:
    if d['cat'] not in seen:
        seen.append(d['cat'])
        spans.append(len(rows)); rows.append([Paragraph(html.escape(d['cat']), CAT), '', ''])
    ans = clean(' '.join(d['a']))
    if d.get('tbl'):
        ans += ' ' + ' · '.join(('<b>%s %s</b>' if r[2] else '%s %s') % (html.escape(r[0]), html.escape(r[1])) for r in d['tbl'])
    rows.append([Paragraph(html.escape(d['q']), Q), Paragraph(ans, N), Paragraph(html.escape(d['ref'].replace('FOM ', '')), REF)])
t = Table(rows, colWidths=[2.1 * inch, 5.05 * inch, .55 * inch], repeatRows=1)
st = [('VALIGN', (0, 0), (-1, -1), 'TOP'), ('LINEBELOW', (0, 0), (-1, -1), .3, PALE), ('BACKGROUND', (0, 0), (-1, 0), PALE),
      ('LEFTPADDING', (0, 0), (-1, -1), 3), ('RIGHTPADDING', (0, 0), (-1, -1), 3), ('TOPPADDING', (0, 0), (-1, -1), 1.2), ('BOTTOMPADDING', (0, 0), (-1, -1), 1.2)]
for i in spans:
    st += [('SPAN', (0, i), (-1, i)), ('LINEBELOW', (0, i), (-1, i), .6, F), ('TOPPADDING', (0, i), (-1, i), 3)]
t.setStyle(TableStyle(st)); story.append(t)

def on_page(c, d):
    c.saveState(); c.setFont('Helvetica', 6); c.setFillColor(GREY)
    c.drawString(.45 * inch, .2 * inch, foot); c.drawRightString(letter[0] - .45 * inch, .2 * inch, 'page %d' % d.page); c.restoreState()

doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
print('A330_Weather_Requirements.pdf', len(bank), 'records')
