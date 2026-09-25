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
- stepIdx = -1
- stepIdx < 0
- "Cockpit Prep":"#463C8F"
- in-bar
- .ps-homebar:empty
- .tinted
- data-pc
- CL_COLORS
- --pc:${pc}
- -@media (max-width:480px){.ps-homebar{padding:6px 0 0 8px;}.ps-home{width:40px;height:40px;}}
- get-identity
- padding-right:150px;min-height:40px

Hidden-until-built tiles and buttons (Ryan, 2026-09-16): Systems Quiz (no bank), Podcast (no episodes).

- .menu a[hidden]
- .navbtn[hidden]

Memorization groups (Ryan, 2026-09-21): flows_quiz.html renders g / gc / gb item fields and a flow's `groups` (legend, colored group headers, per-group step counter); phase_flows.html paints a section header in its color when the section carries mem:true. Data re-cut by build_scripts/gen/spine_cockpit_prep.py and resection_cockpit_prep.py, chained after the generators.

- .grp, .grpq, .grplegend, .step.gstep, .fl-item.gitem
- grpInfo / grpHeader / grpLegend
- ioe.html #origLink (Original OE Workbook, Drive link)

## 2026-09-22 additions (v3.0 to v4.3)

phase_flows.html transforms (build_scripts/page_phase_flows.py):
- (k) phone reads vertically at 16 px, FIT toggle on wider screens (X-with-arrows SVG, persisted a330fit); FIT off on Mac/iPad locks the height and continues columns to the right; sparse pages column-width, left-justified
- (l) checklist popup shows every row under MINE, BOTH rows carry PF and PM chips
- (n) phase bar 44 px buttons, scroll-snap, wheel scrolls sideways, 52 px pagers
- (o) exterior light switch actions as sky-blue chips (.lt); (q) whole row light blue (.it.lights)
- (p) 18 000 ft / 10 000 ft highlight; height tokens do not match inside larger numbers
- (r) items with more than 6 bullets fold to 5 with a tap-for-full-list cue

page_fixups.py additions:
- phase_flows.html: dark mode lightens phase colours used as text (--pcl from CL_COLORS), checklist rows and FMC titles in Jeppesen yellow
- flows_quiz.html: Step button, fixed Reveal slot (wide screens), group filter chips, centred no-map flows, poster zoom, item rendering without a dangling dash
- limitations.html: Passenger/Freighter toggle (was hand-edited 2026-09-17) and Rev 13 set toggle (data/limitations_myset.json)
- memory-items.html: My notes / FCOM verbatim toggle (data/memory_items_myset.json)

Generators: gen/spine_cockpit_prep.py syncs trainer spine prompts and details from data/phase_flows.json (verify_spine_sync.py); gen/gen_flow_memorization.py builds flow_memorization.html and docs/A330_FLOW_MEMORIZATION_PLAN.md from phase_flows.json; gen_phase_flows.py emits limitations_myset.json and memory_items_myset.json. Memory items, limitations and SIM Notes phases are Ryan's sets with FCOM/QRH/PRC chips (docs/PHASE_FLOWS_FCOM_AUDIT_2026-09-22.md for the SOP audit).

## 2026-09-25 addition (v5.0 to v5.1)

phase_flows.html transform (build_scripts/page_phase_flows.py):
- (t) bottom-nav slider + phase picker: a thin drag slider under the phase row mirrors and drives
  nav's scrollLeft (touch-and-mouse pointer events, follows swipes of the row too); a grid button
  at the left of the row opens all 26 phases (id="pkroot"/"pkbody") in three groups, NORMAL /
  NON-NORMAL / REFERENCE (memory-items, limits, sim-notes split out of the existing ABN set just
  for this grouping), current phase highlighted, one tap jumps and closes. Same button/data-p
  pattern as #nav/#rail so styling and phase colors match.
