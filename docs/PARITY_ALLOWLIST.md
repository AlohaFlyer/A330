# Parity allowlist

Each line is a substring; a CSS or DOM diff line containing it is an accepted, documented
deviation from the B787 original. Anything else parity_diff.py reports is a defect.

- --goodtext
- ${d.cond?
- data:image/svg+xml
- assets/icons/
- assets/A330_hero.jpg
- <tbody>

The last five cover the placeholder logo SVG (an inline data URI) and the sixth footer row (AFM), which the B787 table does not have.
- +svg 
- +text 
- +tr 
- +td 
- +a 

Content-level deviations inside engines, reviewed 2026-09-16 (each is an A330 fact replacing a B787 SOP claim, or a source-name swap):

- data-a="RNP"
- data-a="NPA"
- PM: __ CHECKLIST COMPLETE
- PRO-NOR-SUP-
- FCTM R5 Normal Checklists
- see FCTM Normal Checklists
- </i>FMS</span>
- data/oe.json
- FOM, FCOM, QRH, FCTM, PRC
- FCOM PRO-NOR-SOP &middot; FCTM PR-NP-CL
- href="podcast.html"
- Open 2-page handout
- assets/a330_cockpit.jpg
- data/flows_trainer.json
- data/phase_flows.json
- __mk
- +rect 
- -rect 
- -text 

The rect/text lines are the MCDU page-flow SVG, which has 14 nodes where the B787 CDU diagram had a different count; same viewBox, same group styling.
- +h2 
- -h2 
- +ul 
- -ul 
- +li 
- -li 
- +b 
- -b 

The h2/ul/li/b lines are the MCDU page cards (7 cards, 19 items) versus the CDU page (6 cards, 17 items); same card markup.
- let seat = "FO"
- seat:'F',duty:'PM'
- seatIRO
- CM1 (CA)
- CM2 (FO)
- CM3 (IRO)
- seat!=="IRO"
- seat==="IRO"
- broad ? 30 : 8
- CORPUS.source
- Contact</div>
- Questions, corrections, requests
- mailto:
- apple-touch-icon
- rel="manifest"

Contact line moved from every footer into Portal Settings (Ryan, 2026-09-16), and the Manuals tile added above ALPA:

- font-size:11px;color:#FF9080;font-family:inherit;text-decoration:none
- font-size:11px;color:#463C8F;font-family:inherit;text-decoration:none
- font-size:11px;color:#6F6B7E;font-family:inherit;text-decoration:none
- color:#CE0C88;font-weight:700;text-decoration:none
- -a 
- -a contact
- +span 
- +small 
- +span arrow
- var LOG_URL = ''

Flows Trainer and Phase Flows additions (Ryan, 2026-09-16): exterior flows hide the cockpit map (noflow), items may carry a per-seat map position (pos:{CA,FO}) or mir:true (x,y drawn for CM1, mirrored across the centerline for CM2), and Phase Flows gets a QUICK REF overlay for Ryan's A330 OEM Quick Reference card (Back, Day/Night, PDF link):

- .layout.noflow
- classList.toggle("noflow"
- seatPt
- .qref
- qrefBtn
- qrefBack
- qrefTheme
- QUICK REF
- a330qrefdark
- assets/quickref/
- A330_OEM_Quick_Reference.pdf
- +div qref
- +div qbar
- +div qpages
- +img 
