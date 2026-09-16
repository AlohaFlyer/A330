# Parity allowlist

Each line is a substring; a CSS or DOM diff line containing it is an accepted, documented
deviation from the B787 original. Anything else parity_diff.py reports is a defect.

- --goodtext
- ${d.cond?
- data:image/svg+xml
- assets/icons/
- assets/A330_hero.svg
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
