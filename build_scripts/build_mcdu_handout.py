#!/usr/bin/env python3
"""Build A330_MCDU_Preflight_Handout.pdf (reportlab, one US-letter page).
Content comes from the same spec as the page (page_mcdu_preflight.GROUPS / TOP / BOTTOM), so the
handout and the page cannot drift. Revision string from manuals.json."""
import json, os, sys, re, html
sys.argv = sys.argv[:1] + ['/dev/null']            # import the spec without running its transform
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
_src = open('build_scripts/page_mcdu_preflight.py', encoding='utf-8').read()
spec = {'__file__': os.path.abspath('build_scripts/page_mcdu_preflight.py')}
exec(_src[:_src.index('# ---------------------------------------------------------------- transform')], spec)
GROUPS, TOP, BOTTOM, FR, REF = spec['GROUPS'], spec['TOP'], spec['BOTTOM'], spec['FR'], spec['REF']
M = json.load(open('manuals.json', encoding='utf-8')); fd = M['A330P_FCOM']['date']

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
P = colors.HexColor('#463C8F'); F = colors.HexColor('#CE0C88'); PALE = colors.HexColor('#EAE5F4'); GREY = colors.HexColor('#6F6B7E')
ss = getSampleStyleSheet()
H = ParagraphStyle('h', parent=ss['Title'], fontSize=14, leading=16, textColor=P, alignment=0, spaceAfter=1)
S = ParagraphStyle('s', parent=ss['Normal'], fontSize=7.2, leading=9, textColor=GREY, spaceAfter=4)
G = ParagraphStyle('g', parent=ss['Normal'], fontSize=9.2, leading=11.5, textColor=P, fontName='Helvetica-Bold', spaceBefore=3, spaceAfter=1)
N = ParagraphStyle('n', parent=ss['Normal'], fontSize=8, leading=10, leftIndent=10, firstLineIndent=-10)
B = ParagraphStyle('b', parent=N, textColor=colors.HexColor('#333333'), leftIndent=0, firstLineIndent=0, backColor=colors.HexColor('#F1EEF6'), borderPadding=(2, 3, 2, 3))
foot = f'ha330pilot.app · FCOM {FR} · study aid only, the current FCOM governs'
def who(h2):
    m = re.search(r'\((CM1|PF|PM|BOTH)', h2); return m.group(1) if m else ''
def strip(s): return html.unescape(re.sub(r'<[^>]+>', '', s))

doc = SimpleDocTemplate('A330_MCDU_Preflight_Handout.pdf', pagesize=letter, leftMargin=.45*inch, rightMargin=.45*inch,
                        topMargin=.4*inch, bottomMargin=.4*inch, title='A330 MCDU Preflight (PF)', author='ha330pilot.app')
story = [Paragraph(f'A330 MCDU Preflight (PF), page flow', H),
         Paragraph(f'FCOM {FR} ({fd}) {REF}. Pre-initialization is CM1 (SOP-04), the FMGES preparation is PF, the crosscheck is PM, '
                   f'the Departure Legs Verification is both (SOP-06). Numbers in brackets are MCDU line-select keys.', S),
         Paragraph(f'<b>Before:</b> {html.escape(TOP[0].replace("  ", " "))}. {html.escape(TOP[1].split(" · ")[0])} (SOP-04).', B), Spacer(1, 3)]
n = 0
for (glabel, h2, nodes) in GROUPS:
    story.append(Paragraph(f'{html.escape(h2)}', G))
    for (label, sub, li, _) in nodes:
        n += 1
        txt = strip(li)
        m = re.match(r'(.+?) \((CM1|PF|PM|BOTH)(?:, [^)]*)?\): (.*)', txt, re.S)
        if m: name, role, body = m.groups()
        else: name, role, body = label, who(h2), txt
        story.append(Paragraph(f'<b>{n}. {html.escape(name)}</b> <font color="#CE0C88"><b>{role}</b></font> {html.escape(body)}', N))
story.append(Spacer(1, 3))
story.append(Paragraph(f'<b>After:</b> {html.escape(BOTTOM[0].replace("  ", " "))}. {html.escape(BOTTOM[1].split(" · SOP")[0])} (SOP-06), then the Departure Briefing and the COCKPIT PREPARATION C/L.', B))

def _foot(c, d):
    c.saveState(); c.setFont('Helvetica', 6.5); c.setFillColor(GREY)
    c.drawRightString(letter[0]-.45*inch, .25*inch, foot); c.restoreState()
doc.build(story, onFirstPage=_foot, onLaterPages=_foot)
from pypdf import PdfReader
pages = len(PdfReader('A330_MCDU_Preflight_Handout.pdf').pages)
assert pages == 1, f'handout is {pages} pages, must be 1'
print(f'A330_MCDU_Preflight_Handout.pdf 1 page, {n} steps')
