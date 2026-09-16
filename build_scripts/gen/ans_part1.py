# Answers, part 1: workbook items 0 to 103 (sections 1.2.3 through 3.1.1).
# Keys are indices into scratch/wb_items.json. A record with "reuse": True starts from the
# B787 FOM-grounded record and applies only the listed fields on top.
DESK = "No published source located, ask the check airman"
A = {}

A[0] = dict(topic="Emergency Equipment", q="What flight deck emergency equipment must you check?",
  a="Life vests, crash axe, smoke hoods, extinguisher, oxygen masks, flashlights, escape ropes, PED bag, fire gloves",
  detail="Nine items on the EMER EQPT check of the Preliminary Cockpit Preparation, done by the PM or CM3. Life vests stowed, crash axe stowed, smoke hoods or portable oxygen with full-face masks stowed and ready, portable fire extinguisher lockwired with the gauge in the green, oxygen masks stowed, flashlights, escape ropes, PED Fire Containment Bag and fire gloves stowed.",
  ref="FCOM PRO-NOR-SOP-04 P 13/14 Preliminary Cockpit Preparation, Emergency Equipment",
  quote="EMER EQPT..................................................................................................... CHECK PM-CM3 L2 Check that: ‐ Life vests are stowed ‐ Crash axe is stowed ‐ Smoke hoods and/or portable oxygen equipment and full-face masks is stowed and ready for use ‐ Portable fire extinguisher is lockwired and the pressure gauge indicator is in the green area ‐ Oxygen masks are stowed ‐ Flashlights are stowed ‐ Escape ropes are stowed ‐ PED Fire Containment Bag is stowed ‐ Fire gloves are stowed",
  note="The extinguisher check is two things: lockwire intact and gauge in the green. A missing lockwire means it may have been discharged.",
  src="fcom")

A[1] = dict(reuse=True, topic="International Theaters",
  a="Not named in our manuals; the disinsection certificate is in Comply365",
  detail="The FOM does not name a sanitation certificate. The closest document is the Certificate of Residual Disinsection, which is placed in the Comply365 app under Flying, Regulatory and Operating Docs, International Documents, Europe, and is also carried on the General Declaration.",
  ref="FOM 18.1.10.1 Residual Spraying",
  quote="a Certificate of Residual Disinsection will be placed into the Comply365 app under Flying > Regulatory & Operating Docs > International Documents > Europe.",
  note="Confirm what the Japan ramp inspector calls a sanitation certificate with the check airman before your first Japan turn.",
  src="fom")

A[3] = dict(reuse=True, topic="Security and Doors",
  a="On the EFB, and reproduced in the Pilot Reference Cards",
  note="The A330 Jumpseat Information Card is reproduced in the PRC, so it is also available on the flight deck without the EFB. The Captain still owes the occupant the briefing.")

A[5] = dict(reuse=True, topic="Crew Rest",
  a="FOM 5.1.23, Crew Rest Facility, plus the LDMCR card in the PRC",
  note="On the A330 the primary facility is the Lower Deck Module Crew Rest, LDMCR. Bunks 1 and 4 are the Flight Crew bunks, 2, 3, 5 and 6 belong to the Cabin Crew, and no more than 2 Flight Crew and 4 Cabin Crew may be in it at any time. The PRC reprints the LDMCR information card.")

A[7] = dict(status="desktop", kind="drill", topic="Crew Rest", q="Do you have a crew rest app for long-range flying?",
  a="", detail="No FOM, FCOM, QRH, FCTM or PRC text names a crew rest app. The FOM sets the rest break structure for augmented crews: the PIC determines the length and order of pilot rest breaks, and a double crew may use a 2-4-2 or 4-4 split.",
  ref="FOM 4.3.2.4.4 Augmented Crew (3 Flight Crewmembers)",
  quote="The PIC will determine the length and order of pilot rest breaks.",
  note=DESK + ". Bring the app you use and confirm it is the one the fleet expects.", src="fom")

A[8] = dict(reuse=True, topic="Security and Doors",
  note="The code is not published in the FOM, FCOM or QRH; it is SSI. The A330 keypad code is programmed by the airline as a two to seven digit code, and the keypad is for cabin crew access requests only, never for normal entry.")

A[9] = dict(topic="Emergency Equipment", q="Where is the passenger cabin emergency equipment location chart?",
  a="FCOM PRO-ABN-90, Detailed Cabin and Cockpit Evacuation Procedure",
  detail="The A330 Emergency Equipment Location figure sits in the FCOM abnormal chapter PRO-ABN-90, Detailed Cabin / Cockpit Evacuation Procedure, page 5 of 14. The systems description at DSC-25-30 covers cockpit emergency equipment and sends you to the CCOM for the cabin items and the placard symbol list.",
  ref="FCOM PRO-ABN-90 P 5/14 Emergency Equipment Locations",
  quote="EMERGENCY EQUIPMENT LOCATIONS Ident.: PRO-ABN-90-90000470.9000414 / 27 DEC 23 Applicable to: ALL A330 EMERGENCY EQUIPMENT LOCATION",
  note="Placards in the cabin also mark each item. DSC-25-30 says the symbol list is in CCOM 11-010.", src="fcom")

A[10] = dict(topic="Security and Doors", q="Where is the cockpit door described, with its operation and egress?",
  a="FCOM DSC-52-30, Cockpit Door Security System",
  detail="DSC-52-30-10 describes the door: forward-opening hinged, electrically locked latch controlled by the flight crew, cabin keypad with a two to seven digit code, a mechanical override to open it from the cockpit side, and an evacuation and decompression panel the crew kicks out if the door jams. DSC-52-30-20 covers the Cockpit Door Locking System controls and indications.",
  ref="FCOM DSC-52-30-10 P 1/2 Cockpit Door Description",
  quote="A forward-opening hinge door separates the cockpit from the passenger or courier compartment. It has an electric-locking latch, controlled by the flight crew. In normal conditions, when the door is closed, it remains locked.",
  note="Two failure behaviours to know: rapid cockpit decompression unlocks the door automatically, and an electrical supply failure unlocks it but leaves it closed.", src="fcom")

# FD Pro workflow items: not in any published company manual
for i, qq in [(13, "FD Pro: turn on AUTO UPDATE for every weather layer"), (14, "FD Pro: select the weather layers you want"),
              (15, "FD Pro: REFRESH the Weather Layers pane"), (16, "FD Pro: verify the correct aircraft at top center"),
              (17, "FD Pro: demonstrate a flight plan upload"), (18, "FD Pro: demonstrate a flight plan transfer to another EFB")]:
    A[i] = dict(status="desktop", kind="walkthrough", topic="EFB and FD Pro", q=qq, a="",
      detail="This is a Jeppesen FD Pro workflow step. The FOM sets the currency rule for the EFB and its apps but does not script the FD Pro screens. Demonstrate it on the device during OE.",
      ref="FOM 2.5.1.4 EFB - Prior to Flight", quote="", note=DESK + ". The FD Pro Pubs Quick Reference guide in Comply365 covers the screens.", src="fom")

A[35] = dict(topic="Dispatch and Release", q="Where are the FMS, ACARS, uplink and setup procedures?",
  a="FCOM PRO-NOR-SOP-04 and SOP-06 for the FMS; FCOM PER-ARD for the AeroData ACARS uplinks",
  detail="The MCDU and FMS setup runs through the Preliminary Cockpit Preparation, PRO-NOR-SOP-04, and the Cockpit Preparation, PRO-NOR-SOP-06. The AeroData takeoff and landing performance requests, the OPS CTRL message and the load closeout uplink are described in the FCOM Performance chapter, PER-ARD.",
  ref="FCOM PER-ARD-GEN P 2/4 Overview of AeroData Process",
  quote="The flight crew sends the OPS CTRL MSG (containing the Fuel on Board, Release Version, and flight crew Fitness for duty) via ACARS during the cockpit preparation.",
  note="The Final TPR uplink carries the load closeout ZFW and ZFWCG and the takeoff data into the FMS. An uplink deletes previously entered THR RED and ACCEL altitudes, so re-check them.", src="fcom")

A[36] = dict(topic="Dispatch and Release", q="How do you tell the nav database is current?",
  a="A/C STATUS page: the ACTIVE NAV DATABASE dates and HA3 name cover today",
  detail="On the MCDU DATA, A/C STATUS page, verify the day, month and year of the ACTIVE NAV DATABASE. Line 2L shows the validity dates, for example 26MAR-22APR, and 2R the database name, currently HA3, whose code carries the year, month and sequence. If the active database is out of date the MCDU displays CHECK DATA BASE CYCLE.",
  ref="FCOM PRO-NOR-SOP-04 P 7/14 FMS Database Validity",
  quote="FMS DATABASE VALIDITY............................................................................. CHECK CM1 Verify the Day, Month, and Year is correct for the ACTIVE NAV DATABASE:",
  note="AIRAC cycles change at 0900 UTC in the US and Canada, 0000 UTC ICAO, 1500 UTC Japan and 1600 UTC Australia. If the new cycle becomes effective during your flight, select it before departure.", src="pro")

A[37] = dict(topic="Dispatch and Release", q="Can you change the nav database? How?",
  a="Yes, on the ground only: press SECOND NAV DATABASE at 3L and confirm",
  detail="On the A/C STATUS page, pressing the Second Database key at 3L brings up CONFIRM and CANCEL prompts. Confirming swaps the databases. Cycling erases the primary and secondary flight plans and all stored data, so the SOP cycles it twice during preliminary cockpit preparation to clear pilot-entered and uplinked data, and the FCOM says never do it in flight.",
  ref="FCOM DSC-22_20-20-10-25 P 78/154 A/C STATUS page",
  quote="CAUTION Cycling the database erases the primary and secondary flight plans, as well as stored data. The flight crew must never do this in flight.",
  note="The preliminary cockpit preparation cycles the database on purpose: select the non-current one, then re-select the current one, and check STORED shows nothing.", src="fcom")

A[43] = dict(topic="Dispatch and Release", q="No TPR available. How do you get takeoff performance?",
  a="Use the TLR on the release, or have Dispatch calculate and send an updated TLR",
  detail="AeroData takeoff data comes three ways: the TLR in the Dispatch Release, the ACARS TPR, or the Dispatcher, who can calculate an updated TLR and send it to the printer or read it to you. The hierarchy is Final TPR, Preliminary TPR, then TLR.",
  ref="FCOM PER-ARD-GEN P 1/4 Takeoff Performance Data",
  quote="‐ Dispatcher: An updated TLR can be calculated and sent to the aircraft printer or relayed verbally to the flight crew.",
  note="A verbal TLR from Dispatch is legitimate data. Read it back and write it down before it goes in the FMS.", src="fcom")

A[44] = dict(reuse=True, topic="Dispatch and Release",
  a="Yes. It is the tertiary source, valid for the conditions it was built on",
  detail="The TLR is prepared by the dispatcher on anticipated atmospheric conditions and planned payload and rides in the Dispatch Release. The FCOM ranks it third behind the Final and Preliminary TPR. Use it when ACARS data is not available, and confirm it is still valid before takeoff.",
  ref="FCOM PER-ARD-GEN P 1/4 TLR",
  quote="A Takeoff and Landing Report (TLR) is prepared by the dispatcher based on anticipated atmospheric conditions and planned payload. The TLR is provided as part of the Dispatch Release/Flight Plan.",
  note="FOM 5.4.5 says the same thing from the policy side: takeoff data must be available and checked for each takeoff, and invalid data is replaced by ACARS or Dispatch.", src="fcom")

A[45] = dict(topic="Dispatch and Release", q="Concerns using the TLR: temperature and altimeter?",
  a="It was built on forecast conditions and planned weight; confirm it is still valid",
  detail="The TLR uses the environmental conditions the dispatcher considered at dispatch and the takeoff weight the dispatcher planned. The Before Pushback check has both pilots confirm wind, OAT and QNH on the report and, if using the TLR, confirm the TLR is still valid. Actual OAT above the assumed value or a lower QNH invalidates the numbers.",
  ref="FCOM PRO-NOR-SOP-07 P 3/8 Final Takeoff Data",
  quote="‐ Confirm it is the “FINAL” TPR (If using the TLR, confirm the TLR is still valid)",
  note="Each version of takeoff data is valid only for the conditions and weight it was calculated on. If anything moved, request a new TPR by entering the gross weight in PTOW at 5R and SEND at 6R.", src="pro")

A[51] = dict(topic="Communications and PA", q="How do you make a PA with a headset?",
  a="Press and hold the PA transmission key on the ACP, then talk on the boom or mask mike",
  detail="From the cockpit the PA works through the ACP or the handset. With a boomset or mask, press and hold the PA transmission key on the ACP; three green lines come on. With the hand mike, hold the PA key and press the hand mike push to talk. The PA reception knob out lets you hear the PA on the loudspeaker.",
  ref="FCOM DSC-23-20-40 P 1/4 Passenger Address",
  quote="PA Transmission Key Pressed and held : The flight crew may use a boom, mask, or hand mike to make an announcement. Three green lines come on.",
  note="The PA key is a hold key, not a latch. Let go and you are off the PA.", src="fcom")

A[52] = dict(status="desktop", kind="drill", topic="Communications and PA", q="PA PRIO versus PA ALL on the handset?",
  a="", detail="The FCOM describes the cockpit handset only as the pedestal handset used for PA announcements and does not define the PRIO and ALL selections. The FOM names PA+ALL as the selection that reaches the cabin without disturbing the LDMCR.",
  ref="FCOM DSC-23-20-40 P 2/4 Cockpit Handset",
  quote="The cockpit handset at the bottom of the pedestal is used for PA announcements.",
  note=DESK + ". Have the check airman show you PRIO on the handset.", src="fcom")

A[53] = dict(topic="Communications and PA", q="How do you make a PA with the flight deck handset?",
  a="Pick up the pedestal handset and press its push to talk; no ACP action needed",
  detail="The cockpit handset at the bottom of the pedestal is dedicated to PA announcements. The PA from cockpit table shows handset use needs no PA transmission key and no PA reception knob action, only the push to talk on the handset.",
  ref="FCOM DSC-23-20-40 P 1/4 Passenger Address",
  quote="Note: The flight crew may use a cockpit handset to make PA announcements without action on the ACPs.",
  note="FOM 5.1.23.8 adds the LDMCR trick: press PA+ALL and use the push to talk on the flight deck handset.", src="fcom")

A[54] = dict(topic="Crew Rest", q="Which PA selection reaches the cabin but not the crew rest?",
  a="PA+ALL with the flight deck handset push to talk",
  detail="FOM 5.1.23.8 tells the Flight Crew how to announce to the cabin without disturbing the LDMCR: press PA+ALL and use the push to talk button on the Flight Deck handset.",
  ref="FOM 5.1.23.8 A330 Crew Rest Facility",
  quote="Flight Crew may make an announcement to the cabin without disturbing the LDMCR by pressing PA+ALL and use the push-to-talk button on the Flight Deck handset.",
  note="This matters on every augmented leg. A seat belt PA through the LDMCR wakes the relief pilot you need rested.", src="fom")

A[57] = dict(kind="walkthrough", topic="Takeoff and Departure", q="Review the engine failure after V1 procedure",
  a="Continue, rotate 3 degrees per second to 12.5 degrees, fly the SRS and beta target, secure the engine, then accelerate",
  detail="If an engine fails after V1 the takeoff continues. Rudder conventionally on the ground, rotate at about 3 degrees per second to 12.5 degrees, then follow SRS which targets the speed at failure, between V2 and V2+15. Center the beta target with rudder, trim it out, engage the AP. Fly the trajectory first, delay the acceleration only to secure the engine, then level at the engine-out acceleration altitude and accelerate.",
  ref="FCTM PR-AEP-ENG P 10/26 Engine Failure After V1",
  quote="At VR, the flight crew should rotate the aircraft using a continuous pitch rate of approximately 3 °/s towards an initial pitch attitude of 12.5 °. The combination of high FLEX temperatures and low VR speeds requires precise handling during the rotation and liftoff.",
  note="Secure the engine means run the ECAM to ENG MASTER OFF, or AGENT 1 DISCH with damage, or fire out or AGENT 2 DISCH for a fire, before you accelerate. A derated takeoff carries a warning: TOGA below F speed can cause loss of control.", src="fctm")

A[58] = dict(topic="Takeoff and Departure", q="Where is the engine failure procedure for a specific runway?",
  a="On the TPR or TLR, as the Engine Out Departure Procedure; check the EOSID on the ND",
  detail="The Final Takeoff Data check has both pilots confirm the Engine Out Departure Procedure printed on the TPR or TLR. The FMS side is the EOSID, shown as the yellow line on the ND in plan mode, and it is checked during the flight plan check.",
  ref="FCOM PRO-NOR-SOP-07 P 3/8 Final Takeoff Data",
  quote="‐ Takeoff Runway / Intersection ‐ Engine Out Departure Procedure ‐ Air Conditioning on/off ‐ V speeds",
  note="To review the EOSID detail, select it as a temporary flight plan, read it, then erase it (PRO-NOR-SRP-01-10 flight plan check).", src="pro")

A[61] = dict(reuse=True, topic="Pushback and Start",
  a="MECH pushbutton on the CALLS panel; hand signals if no interphone",
  detail="From the cockpit, the MECH pushbutton on the overhead CALLS panel lights the blue COCKPIT CALL light on the external power panel and sounds the external horn. The ground crew answers on the flight interphone. Ground to cockpit, a call flashes the MECH light on the ACP.",
  ref="FCOM DSC-23-20-30 P 3/4 Service Interphone System, MECH pb",
  quote="COCKPIT CALL lights up blue on the external power panel. held) An external horn sounds. Released : COCKPIT CALL remains lighted.",
  note="The horn keeps the COCKPIT CALL light on until the mechanic presses HORN RESET on the external power panel. FOM 5.3.12 gives the CONNECT INTERPHONE hand signal for the no-headset case.", src="fcom")

A[64] = dict(topic="Pushback and Start", q="Which ECAM alerts can you get during engine start?",
  a="ENG 1(2) START FAULT, for starter time, stall, EGT overlimit, no light up, low N1, or levers not at idle",
  detail="The A330 start is automatic. The EEC aborts and the ECAM presents ENG 1(2) START FAULT when the starter time is exceeded, on a stall, an EGT overlimit, no light up, low N1, or thrust levers not at idle. Ignition and start valve faults have their own alerts, ENG 1(2) IGN A(B) FAULT and ENG 1(2) IGN A+B FAULT.",
  ref="FCOM PRO-ABN-ENG P 91/114 ENG 1(2) START FAULT",
  quote="This alert triggers when one of the following conditions is detected: ‐ Starter time exceeded, or ‐ Stall, or ‐ EGT overlimit, or ‐ No light up, or ‐ Low N1, or ‐ THR levers not at idle.",
  note="On a hot engine the EEC dry cranks before it introduces fuel: EGT above 100 C on the first automatic start, above 150 C on the second (PRO-NOR-SOP-08).", src="fcom")

A[65] = dict(topic="Abnormals and QRH", q="Is there a QRH procedure for a tailpipe fire?",
  a="Yes. ENGINE TAILPIPE FIRE, QRH 17.09A",
  detail="ENG MASTER of the affected engine OFF, establish air bleed pressure, beacon ON, then when N3 is below 30 percent ENG START selector to CRANK and ENG MAN START pushbutton ON to motor the engine. When the fire stops, MAN START OFF and selector NORM. The caution says external fire agents are corrosive, so use them only if the procedure does not stop the fire.",
  ref="QRH 17.09A ENGINE TAILPIPE FIRE",
  quote="ENGINE TAILPIPE FIRE Ident.: ABN-17-00010574.0004001 / 16 MAY 23 Applicable to: ALL CAUTION External fire agents can cause severe corrosive damage.",
  note="A tailpipe fire is a fuel fire in the exhaust with no fire warning. Do not pull the fire push button; you need bleed air to crank it out.", src="qrh")

A[67] = dict(topic="Abnormals and QRH", q="Is there a QRH procedure for an engine fire on the ground?",
  a="No. It is an ECAM procedure, ENG 1(2) FIRE (ON GROUND), in FCOM PRO-ABN-ENG",
  detail="The QRH abnormal section carries only the non-ECAM procedures. An engine fire on the ground is handled by ECAM as ENG 1(2) FIRE (ON GROUND), listed in the FCOM abnormal chapter alongside ENG 1(2) FIRE (IN FLIGHT) and the FIRE DET FAULT variants. The tailpipe fire is the QRH item, at 17.09A.",
  ref="FCOM PRO-ABN-PLP-TOC P 7/16 ENG procedures list",
  quote="ENG 1(2) FIRE (ON GROUND) ............................................................................................................ X",
  note="Ground fire means the fire push button, both agents and the evacuation decision. Tailpipe fire means crank it with the master off. Do not mix the two.", src="fcom")

A[75] = dict(topic="Taxi and Ground", q="Breakaway thrust for taxi?",
  a="A little above idle, applied symmetrically; no N1 number is published",
  detail="The FCTM says the crew needs a little power above idle to move the aircraft, that excessive thrust risks jet blast damage and FOD, and that thrust should normally be used symmetrically. No breakaway N1 figure is published for the A330.",
  ref="FCTM PR-NP-SOP-100 P 3/8 Taxi Roll and Steering, Thrust Use",
  quote="The flight crew will need a little power above idle thrust to move the aircraft. Excessive thrust application can result in exhaust-blast damage or Foreign Object Damage (FOD). Thrust should normally be used symmetrically.",
  note="Avoid stopping in a turn, because it takes excessive thrust to get moving again.", src="fctm")

A[76] = dict(reuse=True, topic="Taxi and Ground",
  a="30 kt straight, one smooth application back to 10 kt; under 10 kt in a 90 degree turn",
  detail="FCTM: on long straight taxiways with no constraints, let the aircraft accelerate to 30 kt, then use one smooth brake application to decelerate to 10 kt, avoiding continuous braking. Use the ND ground speed. For turns of 90 degrees or more, be below 10 kt. FOM 5.3.3 sets the same 30 kt cap and about 10 kt in congested areas.",
  ref="FCTM PR-NP-SOP-100 P 1/8 Taxi Speed and Braking",
  quote="the PF should allow the aircraft to accelerate to 30 kt, and should then use one smooth brake application to decelerate to 10 kt. The PF should avoid continuous brake applications. The GS indication on the ND should be used to assess taxi speed.",
  note="Carbon brake wear depends on the number of applications, not the pressure or duration, so fewer firmer applications are the technique.", src="fctm")

A[77] = dict(reuse=True, topic="Taxi and Ground",
  note="The FCTM says to use the GS indication on the ND to assess taxi speed. There is no taxi speed readout anywhere else.")

A[78] = dict(reuse=True, topic="Taxi and Ground",
  a="Less than 10 kt for a turn of 90 degrees or more",
  detail="The FCTM taxi chapter sets the number: for turns of 90 degrees or more the aircraft speed should be less than 10 kt. With a deflated main gear tire it is 7 kt with one tire and 3 kt with two, with steering limited to 30 degrees.",
  ref="FCTM PR-NP-SOP-100 P 5/8 Taxi Roll and Steering",
  quote="For turns of 90 ° or more, the aircraft speed should be less than 10 kt.",
  note="The inside main gear cuts the corner and tracks inside the nosewheel, so oversteer and slow down before the turn, not in it.", src="fctm")

A[79] = dict(status="desktop", kind="walkthrough", topic="Taxi and Ground", q="Demonstrate differential braking when one side's brakes are much hotter",
  a="", detail="No published A330 procedure calls for differential braking to balance brake temperatures. The FCTM notes differential braking stays available with antiskid off and warns against using it to stop one gear for a pivot turn; the FCOM BRAKES HOT procedure says delay takeoff until below 300 C, or 150 C with the fans on.",
  ref="FCOM PRO-ABN-BRAKES P 7/16 BRAKES HOT",
  quote="Delay takeoff until the brake temperature is below 300 °C (or 150 °C with the brake fans on).",
  note=DESK + ". The green arc marks the hottest wheel above 100 C, amber above 300 C.", src="fcom")

A[80] = dict(topic="Taxi and Ground", q="Where are the gear geometry and turning radius figures?",
  a="FCOM DSC-20-30 Ground Handling, Taxiing, minimum turning radii",
  detail="The Taxiing page for the A330 PAX fleet tabulates the minimum turning radii at the 72 degree nosewheel steering limit: Y 12 m, A 44 m, R3 25 m, R4 43 m, R5 31 m and R6 37 m, assuming symmetric thrust and no differential braking. The cockpit cut-off angle is 20 degrees with a 53 ft obscured segment.",
  ref="FCOM DSC-20-30 P 1/2 Taxiing - A330 PAX Fleet, Minimum Turning Radii",
  quote="The above figure assume symmetric thrust and no differential braking.",
  note="The FCTM adds the visual rule: start the turn before an obstacle reaches the 53 ft obscured segment, for wing and tail clearance.", src="fcom")

A[81] = dict(topic="Taxi and Ground", q="Where is the oversteer technique for turns?",
  a="FCTM PR-NP-SOP-100, Taxi Roll and Steering",
  detail="The FCTM explains that the main gear on the inside of a turn always cuts the corner and tracks inside the nosewheel track, so over-steer must be used. Anticipate the steer out and let the aircraft roll forward a short distance after a tight turn to relieve the main gear.",
  ref="FCTM PR-NP-SOP-100 P 5/8 Taxi Roll and Steering",
  quote="The flight crew should be aware that the main gear on the inside of a turn will always cut the corner and track inside of the nosewheel track. For this reason, over-steer must be used.",
  note="Nosewheel skidding in a turn means slow down or open the radius.", src="fctm")

A[82] = dict(topic="Taxi and Ground", q="Normal 180 degree turn width on the runway?",
  a="About 41 m (133 ft) for the A330-200, 48 m (156 ft) for the -300, dry, no margin",
  detail="With the recommended 180 degree turn technique on a dry runway and 72 degrees of nosewheel steering, the approximate turn width is 41 m for the A330-200 and 48 m for the A330-300, without margin. Add margin when the runway is wet or contaminated. The technique itself is in FCTM PR-NP-SOP-100.",
  ref="FCOM DSC-20-30 P 2/2 180 Degrees Turn on Runway",
  quote="With the recommended 180 ° turn technique, on dry runway, with the maximum nosewheel steering of 72 °, the approximate turn width is: ‐ For the A330-200, 41 m (133 ft) without margin ‐ For the A330-300, 48 m (156 ft) without margin.",
  note="Technique: taxi on the far side, 5 to 10 kt, diverge 20 degrees, and when you are physically over the runway edge turn with full tiller, using asymmetric thrust or differential braking only to hold a constant speed.", src="fcom")

A[83] = dict(topic="Taxi and Ground", q="Pivot turn radius for a 180?",
  a="Not published. The FCTM says avoid braked pivot turns",
  detail="Airbus publishes no pivot turn radius. The FCTM 180 degree turn note says to avoid using differential braking to fully stop one main landing gear, the braked pivot turn technique, because of stress and fatigue in the main gear.",
  ref="FCTM PR-NP-SOP-100 P 6/8 180 Degrees Turn on Runway",
  quote="In order to avoid stress and fatigue in the main landing gear, the flight crew should avoid using differential braking to fully stop one main landing gear (braked pivot turn technique)",
  note="If a runway is too narrow for the published width, you back-taxi to a turn pad or ask for a tow, not pivot.", src="fctm")

A[86] = dict(reuse=True, topic="Taxi and Ground",
  a="Recompute the takeoff data, revise and crosscheck the FMS, flaps, FCU ALT, T.O CONFIG, re-brief, Departure Change checklist",
  detail="The FCOM Departure Change procedure: the PM checks the AeroData inputs and sends for a new TPR if required, revises the FMS takeoff data, runway and SID, and the PF crosschecks the revised FMS against the TPR or TLR. Then flaps set, FCU altitude set, T.O CONFIG test, a re-briefing by both, and the Departure Change checklist.",
  ref="FCOM PRO-NOR-SOP-10B P 1/2 Departure Change",
  quote="FINAL TAKEOFF PERF DATA...............................................................RECOMPUTE PM L2 The PM ensures the Aerodata inputs (runway and environmental) are correct and if required, sends for a new TPR.",
  note="Watch the slat and flap configuration on the new data. A different runway can mean a different CONF, and the T.O CONFIG test only proves the levers agree with the FMS.", src="pro")

A[88] = dict(topic="Cold Weather and Runway Condition", q="Active precipitation or contaminated surface: what check before departure regardless of holdover?",
  a="A Pre-Takeoff Check from the seat, always, whenever icing conditions exist",
  detail="If takeoff will occur within the holdover time, a Pre-Takeoff Check must always be done when icing conditions exist. It is done seated in the cockpit and has two parts: a visual check of the representative surfaces, the portion of the wing visible from the flight deck window, and a judgment that the holdover time is still adequate given changes in precipitation type, intensity, temperature and wind.",
  ref="FCOM PRO-NOR-SUP-ADVWXR P 4/24 Pre-Takeoff Check",
  quote="A Pre-Takeoff Check must always be accomplished when icing conditions exist. It is accomplished by the flight crew from the seated position inside the cockpit, and consists of two parts.",
  note="The outcome is one of three: go, get deiced and anti-iced again, or perform a Contamination Check.", src="pro")

A[89] = dict(topic="Cold Weather and Runway Condition", q="Holdover time expired. What check before takeoff?",
  a="A Contamination Check from the cabin within five minutes of takeoff",
  detail="If takeoff will occur after the holdover time expires, or in heavy snow, a Contamination Check must be done within five minutes before beginning the takeoff. A pilot assigned to the flight goes to the cabin and visually checks both wings and the engine nacelles for any ice or snow. It may be repeated to meet the five minute window.",
  ref="FCOM PRO-NOR-SUP-ADVWXR P 4/24 Contamination Check",
  quote="A Contamination Check must be accomplished within five minutes prior to beginning takeoff if the holdover time has expired or if heavy snow is occurring.",
  note="The FODM Contamination Check Requirements section carries the detail. The PRC Cold Weather Card lists the same two checks.", src="pro")

A[95] = dict(reuse=True, topic="Cold Weather and Runway Condition",
  a="A 0 to 6 code for expected braking action, 0 NIL through 6 dry",
  detail="Runway Condition Code values run from 0, NIL, to 6, dry. The RCAM ties each code to the descriptive terms GOOD through NIL. Airport operators use the RCAM to generate the RWYCC for the runways in use, and the FICON reports it per runway third.",
  ref="FOM 9.1.6.1 Runway Condition Code (RWYCC)",
  quote="Runway Condition Code values range from 0 (NIL) to 6 (dry).",
  note="For the A330 the FOM sends you to the FCOM In-Flight Performance chapter for the RCAM in the fleet format, including the wind limits that depend on runway condition.", src="fom")

A[96] = dict(topic="Takeoff and Departure", q="Maximum takeoff crosswind?",
  a="32 kt gust included, certified, dry; less on wet or contaminated runways",
  detail="The maximum certified crosswind for takeoff on the A330 PAX fleet is 32 kt gust included, an AFM engine limitation. On wet and contaminated runways the FCOM table drops it by runway condition code: 32 kt at RWYCC 5, 27 kt at 4, 20 kt at 3 and 2, and 15 kt on ice at RWYCC 1. Maximum tailwind for takeoff is 15 kt.",
  ref="FCOM LIM-AG-OPS P 2/4 Crosswind Takeoff and Landing - A330 PAX Fleet",
  quote="Maximum certified crosswind for takeoff........................................................... 32 kt (gust included)",
  note="The landing figure is different: 45 kt demonstrated, not a limitation. The wet and contaminated table applies to both, and it is what AeroData uses.", src="fcom")

A[99] = dict(topic="Takeoff and Departure", q="Maximum altitude with slats or flaps extended?",
  a="20 000 ft",
  detail="FCOM Limitations, Flight Controls: the maximum operating altitude with slats and or flaps extended is 20 000 ft.",
  ref="FCOM LIM-F_CTL P 1/2 Maximum Operating Altitude with Slats and/or Flaps Extended",
  quote="Maximum operating altitude with slats and/or flaps extended..................................................20 000 ft",
  note="Holding with CONF 1 is limited to 240 kt, and the FCTM cold weather card says hold clean when able.", src="fcom")

A[100] = dict(topic="Takeoff and Departure", q="Normal rotation rate?",
  a="About 3 degrees per second, liftoff near 10 degrees after 4 to 5 seconds",
  detail="A positive backward stick input starts the rotation and the crew holds a rate of approximately 3 degrees per second for a continuous pitch increase. Liftoff occurs at about 10 degrees, typically 4 to 5 seconds after starting, then the PF targets the required pitch. A slow rotation or under-rotation lengthens the takeoff run and reduces obstacle clearance.",
  ref="FCTM PR-NP-SOP-120 P 2/14 Rotation Technique",
  quote="the flight crew achieves a rotation rate of approximately 3 °/s resulting in a continuous pitch increase. During the rotation, the aircraft liftoff occurs at approximately 10 ° of pitch, typically around 4 to 5 s after the initiation of the rotation.",
  note="Monitor the rotation with outside references, then fly the pitch target on the PFD once airborne. An abrupt rate increase near liftoff is the tail strike setup.", src="fctm")

A[101] = dict(topic="Takeoff and Departure", q="Normal takeoff pitch target?",
  a="15 degrees, then follow the SRS bar",
  detail="At VR, initiate the rotation with a positive sidestick input to a continuous rate of about 3 degrees per second towards 15 degrees of pitch, 12.5 degrees with an engine failed. Minimize lateral inputs to avoid spoiler extension, and after liftoff follow the SRS pitch command bar.",
  ref="FCOM PRO-NOR-SOP-12 P 3/6 Takeoff, Rotation",
  quote="‐ At VR, initiate the rotation with a positive sidestick input to achieve a continuous rotation rate of about 3 °/s, towards a pitch attitude of 15 ° (12.5 °, if one engine is failed)",
  note="Deviation callout on takeoff climb: PITCH if greater than 20 degrees up or less than 10 degrees up (PRO-NOR-SCO).", src="pro")

A[102] = dict(topic="Takeoff and Departure", q="Pitch target after an engine failure at or after V1?",
  a="12.5 degrees, then SRS",
  detail="With one engine failed the rotation target is 12.5 degrees at about 3 degrees per second. The FCTM explains the 12.5 degree target ensures the aircraft becomes airborne despite high FLEX temperatures and low VR speeds. Once safely airborne follow SRS, which targets the speed at failure, no lower than V2.",
  ref="FCTM PR-AEP-ENG P 10/26 Engine Failure After V1",
  quote="The 12.5 ° pitch target will ensure the aircraft becomes airborne.",
  note="If the failure occurs above V2, maintain the SRS commanded attitude; minimum speed is always V2 (FCTM engine failure during initial climb).", src="fctm")

A[103] = dict(topic="Takeoff and Departure", q="What are the callouts during a rejected takeoff?",
  a="Captain calls STOP, or GO to continue; STOP also transfers control",
  detail="The decision and the stop action belong to the Captain and must come before V1, hand on the thrust levers until V1 whether PF or PM. For a malfunction before V1 the Captain calls GO to continue, or STOP to reject. STOP both confirms the rejection and states the Captain now has control; it is the only handover not accompanied by I have control. The PM rollout checks follow the FCTM RTO task-sharing figure.",
  ref="FCTM PR-AEP-MISC P 25/38 Rejected Takeoff, Decision Callouts",
  quote="‐ If a decision is made to reject the takeoff, the Captain calls \"STOP\". This call both confirms the decision to reject the takeoff and also states that the Captain now has control.",
  note="Above 100 kt be go-minded: fire or severe damage, sudden thrust loss, unambiguous evidence the aircraft will not fly, or any ECAM alert. EGT red line or nose gear vibration are not reasons above 100 kt.", src="fctm")
