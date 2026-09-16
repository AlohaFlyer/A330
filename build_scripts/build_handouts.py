#!/usr/bin/env python3
"""Build the two drill handout PDFs from the projected banks (reportlab).
A330_QRH_Memory_Items.pdf: the ten [MEM] procedures, boxed lines verbatim.
A330_Memory_Limitations.pdf: the know-cold limitations set, grouped by system."""
import json, os, re, html
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
os.chdir(os.path.join(os.path.dirname(__file__),'..'))
M=json.load(open('manuals.json')); fr=M['A330P_FCOM']['revision']; fd=M['A330P_FCOM']['date']
P=colors.HexColor('#463C8F'); F=colors.HexColor('#CE0C88'); PALE=colors.HexColor('#EAE5F4')
ss=getSampleStyleSheet()
H=ParagraphStyle('h',parent=ss['Title'],fontSize=15,textColor=P,spaceAfter=2,alignment=0)
S=ParagraphStyle('s',parent=ss['Normal'],fontSize=7.5,textColor=colors.HexColor('#6F6B7E'),spaceAfter=6)
N=ParagraphStyle('n',parent=ss['Normal'],fontSize=8.2,leading=10)
T=ParagraphStyle('t',parent=ss['Normal'],fontSize=9,leading=11,textColor=P,fontName='Helvetica-Bold')
foot=f"ha330pilot.app · FCOM {fr} ({fd}) · study aid only, the current manual governs"
def strip(h): return html.unescape(re.sub(r'<[^>]+>','',h))
# memory items
mi=json.load(open('data/memory_items_drill.json'))
doc=SimpleDocTemplate('A330_QRH_Memory_Items.pdf',pagesize=letter,leftMargin=.5*inch,rightMargin=.5*inch,topMargin=.45*inch,bottomMargin=.45*inch,title='A330 Memory Items',author='ha330pilot.app')
story=[Paragraph(f'A330 Memory Items, FCOM {fr} [MEM] procedures',H),Paragraph(f'{len(mi)} procedures. Boxed lines verbatim from the rendered FCOM pages, visually verified. {foot}',S)]
cells=[]
for d in mi:
    lines=[Paragraph(d['name'],T)]
    for s in d['steps']:
        txt=strip(s['h'])
        if s['t']=='n': lines.append(Paragraph(f"<b>{s['n']}.</b> {html.escape(txt)}",N))
        elif s['t']=='s': lines.append(Paragraph(f"<i>{html.escape(txt)}</i>",N))
        else: lines.append(Paragraph(html.escape(txt),N))
    lines.append(Paragraph(f"<font size=6.5 color='#6F6B7E'>{html.escape(d['ref'])} · {html.escape(d['ident'])}</font>",N))
    cells.append(lines)
rows=[cells[i:i+2] for i in range(0,len(cells),2)]
for r in rows:
    while len(r)<2: r.append('')
t=Table(rows,colWidths=[3.75*inch,3.75*inch]); t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('BOX',(0,0),(-1,-1),.5,PALE),('INNERGRID',(0,0),(-1,-1),.5,PALE),('LEFTPADDING',(0,0),(-1,-1),5),('RIGHTPADDING',(0,0),(-1,-1),5),('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4)]))
story.append(t); doc.build(story); print('A330_QRH_Memory_Items.pdf')
# limitations
lim=[d for d in json.load(open('data/limitations_drill.json')) if d['mem']]
doc=SimpleDocTemplate('A330_Memory_Limitations.pdf',pagesize=letter,leftMargin=.5*inch,rightMargin=.5*inch,topMargin=.45*inch,bottomMargin=.45*inch,title='A330 Limitations, know-cold set',author='ha330pilot.app')
story=[Paragraph(f'A330 Limitations, know-cold set, FCOM {fr} LIM',H),Paragraph(f'{len(lim)} limitations. Number, units, condition. {foot}',S)]
by={}
for d in lim: by.setdefault(d['s'],[]).append(d)
data=[[Paragraph('<b>Limitation</b>',N),Paragraph('<b>Value</b>',N),Paragraph('<b>Ref</b>',N)]]
for sname in sorted(by):
    data.append([Paragraph(f'<b>{html.escape(sname)}</b>',ParagraphStyle('sec',parent=N,textColor=F)),'',''])
    for d in by[sname]: data.append([Paragraph(html.escape(d['q'].rstrip('?')),N),Paragraph(html.escape(d['a']),N),Paragraph(html.escape(d['ref'].replace('FCOM ','')),ParagraphStyle('r',parent=N,fontSize=6.5,textColor=colors.HexColor('#6F6B7E')))])
t=Table(data,colWidths=[3.6*inch,2.7*inch,1.2*inch],repeatRows=1)
st=[('VALIGN',(0,0),(-1,-1),'TOP'),('LINEBELOW',(0,0),(-1,-1),.3,PALE),('BACKGROUND',(0,0),(-1,0),PALE),('LEFTPADDING',(0,0),(-1,-1),3),('RIGHTPADDING',(0,0),(-1,-1),3),('TOPPADDING',(0,0),(-1,-1),1.5),('BOTTOMPADDING',(0,0),(-1,-1),1.5)]
for i,r in enumerate(data):
    if r[1]=='' and i>0: st.append(('SPAN',(0,i),(-1,i)))
t.setStyle(TableStyle(st)); story.append(t); doc.build(story); print('A330_Memory_Limitations.pdf')
