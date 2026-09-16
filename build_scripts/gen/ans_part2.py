# Answers, part 2: workbook items 104 to 199 (sections 4.1.1 through 8.3.4.26).
DESK = "No published source located, ask the check airman"
A = {}

A[105] = dict(reuse=True, topic="Takeoff and Departure",
  note="Where thrust reduction and acceleration occur relative to the airport is what separates the two profiles. The A330 flies the THR RED and ACC ALT set on the PERF TAKEOFF page, defaulted from the takeoff data.")

A[106] = dict(topic="Takeoff and Departure", q="How do you find max rate of climb speed?",
  a="Between ECON climb and green dot; rule of thumb, use turbulence speed",
  detail="The FCTM says the speed for maximum rate of climb, to reach a given altitude in the shortest time, lies between ECON climb speed and green dot. It is not shown on the PFD, so the rule of thumb is to use the turbulence penetration speed. Select it on the FCU when airborne, or pre-select it on the PERF CLB page on the ground.",
  ref="FCTM PR-NP-SOP-140 P 3/4 Climb, Selected",
  quote="The speed to achieve the maximum rate of climb, i.e. to reach a given altitude in the shortest time, lies between ECON climb speed and green dot. As there is no indication of this speed on the PFD, a good rule of thumb is to use turbulence speed to achieve maximum rate.",
  note="Selected speed spoils the optimum profile, so use it only when ATC or weather requires it.", src="fctm")

A[107] = dict(topic="Takeoff and Departure", q="Severe turbulence penetration speed?",
  a="0.80 Mach at FL370 and above, 260 kt FL250 to 350, 240 kt at FL200 and below",
  detail="The QRH SEVERE TURBULENCE table gives the speed and N1 by flight level and weight: Mach 0.8 from FL370 up, 260 kt from FL250 to FL350, and 240 kt at FL200 and below. Seat belts on, keep the autopilot on, disconnect A/THR only for excessive thrust variations, and consider descending to or below optimum.",
  ref="QRH 22.08A SEVERE TURBULENCE",
  quote="SEVERE TURBULENCE Ident.: ABN-22-00012057.0030001 / 16 MAY 23 Applicable to: ALL SEAT BELTS...........................................................................................................ON SPEED and THRUST..................................................................................... ADJUST",
  note="For the approach the QRH wants A/THR on and managed speed. The FCTM also uses turbulence speed as the max rate of climb rule of thumb.", src="qrh")

A[108] = dict(topic="Takeoff and Departure", q="Where is the max angle of climb speed?",
  a="Green dot, shown on the PFD; PERF CLB page gives time and distance at it",
  detail="The speed for the maximum gradient of climb, altitude in the shortest distance, is green dot. The MCDU PERF CLB page displays the time and distance to reach the selected altitude climbing at green dot. Avoid reducing to green dot at high altitude and heavy weight because the reacceleration to ECON Mach takes a long time.",
  ref="FCTM PR-NP-SOP-140 P 3/4 Climb, Selected",
  quote="The speed to achieve the maximum gradient of climb, i.e. to reach a given altitude in a shortest distance, is green dot.",
  note="A speed below green dot can be selected but gives no operational benefit.", src="fctm")

A[110] = dict(status="desktop", kind="drill", topic="Takeoff and Departure", q="Is a SID for specific runways only?",
  a="", detail="Runway applicability is a Jeppesen chart property. Neither the FOM nor the A330 manuals define it. The FCOM cockpit preparation does require the PM to check each waypoint and constraint against the Jeppesen SID, the release and the ATC clearance.",
  ref="FCOM PRO-NOR-SOP-06 P 26/28 F-PLN check",
  quote="Follow along with the PF by checking each waypoint and constraint against the Jeppesen SID, Dispatch release, and current ATC clearance.",
  note=DESK + ". Read the runway box on the SID plate.", src="pro")

A[112] = dict(status="desktop", kind="drill", topic="Takeoff and Departure", q="Red boxed notes on the SID, such as speed restrictions?",
  a="", detail="Chart symbology is Jeppesen material, not manual text. The FOM departure briefing framework is where the notes get covered: the PM names the threats first from the Crew Briefing Reference Card and the airport 10-7, then the PF briefs the plan.",
  ref="FOM 5.2.7 Threat-Based Departure Briefing/TPC", quote="",
  note=DESK + ". Jeppesen chart legend in FD Pro covers the boxed notes.", src="fom")

A[113] = dict(status="desktop", kind="drill", topic="Takeoff and Departure", q="SID top altitude on a climb via clearance?",
  a="", detail="The FOM uses climb via only in the Mexico theater, where the controller expects the pilot to fly the published lateral routing and altitudes, and it notes Central America does not use the phrase at all. The US definition of top altitude is AIM material, not FOM.",
  ref="FOM 21.3.3.5 Mexico Phraseology for Climbs and Descents",
  quote="Typically, the controller will issue a “Descend Via” or “Climb Via” clearance to keep the radio transmission short and concise.",
  note=DESK + ". Know the top altitude on every SID you brief.", src="fom")

A[116] = dict(topic="Takeoff and Departure", q="Minimum altitude to engage the autopilot after takeoff?",
  a="100 ft AGL and at least 5 seconds after liftoff",
  detail="FCOM Limitations, Autopilot Function: the autopilot can be used at takeoff from 100 ft AGL and at least 5 s after liftoff. After a manual go-around it is 100 ft AGL. In all other phases the minimum is 500 ft AGL. The takeoff SOP adds that AP must be engaged for RNP AR below 0.3 NM.",
  ref="FCOM LIM-AFS-10 P 2/8 Autopilot Function",
  quote="At takeoff 100 ft AGL and at least 5 s after liftoff",
  note="Trim first. With an engine failed the FCTM wants the aircraft trimmed with the beta target centered before you engage the AP, and pedal pressure held after engagement can disengage it.", src="fcom")

A[130] = dict(status="desktop", kind="drill", topic="ETOPS", q="APU shut down before descent, then fails to start after landing. Does the verification stand?",
  a="", detail="FOM 6.5.10 judges the APU verification on the in-flight cold-soak start within one hour of top of descent and requires the Captain to detail the result in the logbook. The FOM does not say whether a later ground start failure changes that result.",
  ref="FOM 6.5.10 ETOPS APU Verification Flight",
  quote="After an APU verification attempt, the Captain must detail the results in an Aircraft Maintenance Logbook entry.",
  note=DESK + ". Write up the ground start failure as its own discrepancy and let Maintenance Control decide.", src="fom")

A[132] = dict(topic="Communications and PA", q="How do you call the cabin on the headset, and on the handset?",
  a="CALLS panel pushbutton to ring the station, then CAB key on the ACP; or use the handset",
  detail="Cockpit to cabin: press the station pushbutton on the CALLS panel, FLT REST, CAB REST, PURS, FWD, MID, EXIT or AFT, or ALL. A pink light comes on at that area call panel, CAPTAIN CALL shows on the attendant indication panel and a high-low chime sounds. Then talk with the CAB transmission key pressed on the ACP, using the boom, mask or hand mike. The pedestal handset can also be used.",
  ref="FCOM DSC-23-20-20 P 2/4 Cabin Call System, Call from the Cockpit",
  quote="FLT REST /CAB REST /PURS/FWD/MID/EXIT/AFT pb When pressed: ‐ A steady pink lights come on, on the corresponding area call panel ‐ “CAPTAIN CALL” message appears on the corresponding AIP, and a green light comes on ‐ A high-low chime sounds through corresponding loudspeaker.",
  note="EMER, guarded, is the priority call: flashing pink lights, CALL PRIO CAPT on all panels and three chimes. A cabin call to you flashes ATT on the ACP with a buzzer.", src="fcom")

A[134] = dict(status="desktop", kind="drill", topic="Cruise and Diversion", q="Where in Comply365 is the AIREP form?",
  a="", detail="No FOM, FCOM or PRC text names an AIREP form or its Comply365 location. The PRC Oceanic References card carries the ten-item HF position report format, which includes the temperature, wind and significant weather elements of a meteorological report.",
  ref="PRC p38 Oceanic References, Position Report", quote="10 - Any Significant WX (If none, report smooth)",
  note=DESK + ". Confirm the Comply365 path with the check airman.", src="prc")
A[135] = dict(status="desktop", kind="drill", topic="Cruise and Diversion", q="Must you complete the AIREP form on every flight?",
  a="", detail="No FOM requirement for an AIREP form was located. The FOM does require meteorological reports with oceanic position reports and reports of adverse weather to Dispatch and ATC.",
  ref="FOM 7.1.12 Reports to Dispatch",
  quote="Relay adverse weather reports to Dispatch and Air Traffic Control.",
  note=DESK, src="fom")
A[136] = dict(status="desktop", kind="drill", topic="Cruise and Diversion", q="Must you save the AIREP form after each flight?",
  a="", detail="No retention requirement for an AIREP form appears in the FOM.",
  ref="FOM 7.1.12 Reports to Dispatch", quote="", note=DESK, src="fom")

A[137] = dict(reuse=True, topic="Cruise and Diversion")

A[143] = dict(topic="Cruise and Diversion", q="Departing the lower 48: how early do you log on for a CPDLC departure clearance?",
  a="During preflight: ETD minus 30 minutes with DCL, minus 5 without, logon KUSA",
  detail="The PRC CPDLC card: in CONUS log on to KUSA during preflight, at ETD minus 30 minutes if the airport has Departure Clearance service, ETD minus 5 minutes if it does not. International logons are by FIR: climbing through 10 000 ft for most Pacific FIRs, 15 to 45 minutes prior to the oceanic FIR for KZAK and RJJJ.",
  ref="PRC p33 Controller Pilot Data Link Communication (CPDLC)",
  quote="CONUS (lower 48) During Preflight KUSA i ETD—30’ if DCL i ETD—5’ if no DCL",
  note="Manual entry of the SID with its runway and enroute transition is required when loading the DCL. Load and review any route change in the SEC F-PLN before you accept.", src="prc")

A[144] = dict(reuse=True, topic="Oceanic",
  a="Not the same for every FIR; KZAK and RJJJ want 15 to 45 minutes before the oceanic FIR",
  detail="The FOM sets the policy: log on during preflight or after takeoff above 10 000 ft, or as the FIR or OCA Pilot Reference Card requires. The PRC CPDLC card then gives the window by FIR: Hawaii, climbing through 10 000 ft and 15 to 45 minutes prior to the oceanic FIR, KZAK; Japan the same for RJJJ; Alaska, Australia, New Zealand and Tahiti climbing through 10 000 ft.",
  ref="PRC p33 Controller Pilot Data Link Communication (CPDLC)",
  quote="Hawaii Climbing through 10k and 15’ KZAK to 45’ prior to Oceanic FIR",
  note="Use FD Pro ROUTE INFO for the specific FIR logon window and code. For the NAT HLA FIRs use the Europe Airway Manual ATC data.", src="prc")

A[145] = dict(topic="Oceanic", q="How do you log on for a departure clearance, and enroute?",
  a="MCDU ATC COMM, ATC MENU, LSK 5L NOTIFICATION, verify flight number and ATC, then NOTIFY",
  detail="On the MCDU select ATC COMM, then ATC MENU, then LSK 5L to bring up the NOTIFICATION page. Verify the flight number and the ATC center code, KUSA for a domestic departure clearance, then select NOTIFY. Enroute the session is transferred automatically between US domestic airspace and the international FIR when CPDLC is in use in both; otherwise log on to the next FIR in its window.",
  ref="PRC p33 Controller Pilot Data Link Communication (CPDLC), Logon Procedures",
  quote="On the MCDU: select ATC COMM / ATC MENU / LSK 5L to bring up the NOTIFICATION page. i VERIFY correct Flight Number and ATC; select NOTIFY *",
  note="If ATC CTR shows KUSA and you get NO COMM, do not re-log on; wait for reconnection and use voice. If it does not show KUSA, attempt a re-logon.", src="prc")

A[146] = dict(topic="Oceanic", q="What can you request through CPDLC?",
  a="Direct to a fix, altitudes, climb or descent, block altitude, voice contact, emergency messages",
  detail="Pilot-initiated CPDLC requests on the PRC card: REQUEST DIRECT TO a position that is on the current ATC assigned route, REQUEST an altitude, CLIMB TO, DESCENT TO, BLOCK altitude to altitude, VOICE CONTACT, and emergency messages. Do not send multiple requests in one message, do not repeat a request of the same type before the first is answered, and avoid free text except for MAYDAY or PAN PAN.",
  ref="PRC p34 Pilot-Initiated REQUEST Messages Using CPDLC",
  quote="Voice is always the backup to CPDLC and PRIMARY for emergencies.",
  note="Lateral offsets and weather deviations are also datalink requests in the ATC LAT REQ page. Voice is always the backup and primary for emergencies.", src="prc")

A[153] = dict(topic="Cruise and Diversion", q="OPT versus REC MAX altitude?",
  a="OPT FL is the most economic level for cost index and weight; REC MAX is the highest the aircraft can hold with margins",
  detail="OPT FL is the most economic flight level for the cost index, weight and weather data, a compromise between fuel and time, shown on the PROG page and updated through cruise. REC MAX is the lowest of the altitudes at which the aircraft keeps a 0.3 g buffet margin, can fly level at MAX CRZ, can hold 300 ft/min at MAX CLB, stays between green dot and VMO/MMO, and is certified. Anti-ice is not included in REC MAX.",
  ref="FCOM DSC-22_20-10-40-30 P 10/16 Recommended Maximum Altitude (REC MAX)",
  quote="The recommended maximum altitude is the lowest of the maximum altitude that: ‐ The aircraft can reach with a 0.3 g buffet margin ‐ The aircraft can fly in level flight at MAX CRZ rating ‐ The aircraft can maintain a V/S of 300 ft/min at MAX CLB thrust",
  note="The FCTM says PROG page MAX REC and OPT are what you use to answer CAN YOU CLIMB TO FL XXX. With an engine out the PROG page shows EO REC MAX instead.", src="fcom")

A[160] = dict(status="desktop", kind="drill", topic="Cruise and Diversion", q="When would you save a screenshot of your plotted route?",
  a="", detail="FOM 5.7.3.15 requires the electronic plotting chart on ORCN segments and the full cleared route loaded into the charting app. It sets no save or screenshot requirement.",
  ref="FOM 5.7.3.15 Electronic Plotting Chart",
  quote="", note=DESK + ". A screenshot after a deviation or a position doubtful event is common practice, not policy.", src="fom")

A[161] = dict(reuse=True, topic="Dispatch and Release",
  note="The mandatory triggers are in FOM 7.1.12 Reports to Dispatch: 3000 lb fuel deviation on the A330, 100 nm lateral, 4000 ft altitude, 15 minute arrival delay, weather, moderate or greater turbulence, safety of flight, abnormalities, diversions, mechanical irregularities and ETOPS reroutes.")

A[163] = dict(topic="Communications and PA", q="How do you place a SATCOM call?",
  a="MCDU MAIN MENU, SAT, pick the number from the DIRECTORY or MANUAL DIAL, then the SATCOM key on the ACP",
  detail="The ACPs set up and end the call, the MCDU picks the number. Select SAT on the MCDU MAIN page, then 6R for the SATCOM DIRECTORY, choose a category, press the line key of the number to dial it, or use MANUAL DIAL at 5R. Press the SATCOM transmission key on the ACP: green flashing while the call establishes, steady green connected. The MCDU status line reads DIALING, then CONNECTED.",
  ref="FCOM DSC-23-30-20-20 P 1/6 SATCOM MCDU Interface",
  quote="The crew accesses this page by selecting SAT on the MCDU MAIN page.",
  note="An incoming ground call flashes the SATCOM key on the ACP and shows INCOMING CALL on the MCDU. SELCAL/CALL RESET cancels the buzzer.", src="fcom")

A[164] = dict(topic="Communications and PA", q="Where are the preprogrammed telephone numbers?",
  a="MCDU SATCOM DIRECTORY page, four priority lists: EMERGENCY, SAFETY, NON-SAFETY, PUBLIC",
  detail="From the SATCOM MAIN MENU, 6R opens the SATCOM DIRECTORY, which holds four phone number lists by priority: 1L EMERGENCY for distress numbers, 2L SAFETY for regulatory and flight safety numbers, 3L NON-SAFETY and 4L PUBLIC. Each category page lists the titles and numbers; pressing a line dials it. Protected numbers are green, unprotected blue in brackets.",
  ref="FCOM DSC-23-30-20-20 P 2/6 SATCOM Directory Page",
  quote="This page provides access to 4 phone number lists, where phone numbers can be memorized, according to their priority.",
  note="Type the first three letters of a title in the scratchpad and press 5R to search a category. MedLink and Dispatch live in the SAFETY list.", src="fcom")

A[167] = dict(topic="Cruise and Diversion", q="Rule of thumb for HF frequencies and the sun?",
  a="Not published; reception varies with time of day, and ARINC gives the day's primary and secondary",
  detail="The FOM does not state the daytime-high, nighttime-low rule. It says HF reception varies greatly with time of day, atmospheric variations, sunspots and distance, that ARINC provides the primary and secondary frequencies predicted for the day, and that you may need to try several listed frequencies, trying several times on one before changing.",
  ref="FOM 20.4.3.3 Frequency Selection",
  quote="HF reception varies greatly with time of day, atmospheric variations, sunspots, and distance. It is normal for HF radio to be unable to receive on all the listed frequencies at all times. The primary and secondary frequencies predicted to be in use for the day are provided by ARINC.",
  note="Frequencies print in the communications boxes on the enroute charts. Ionospheric disturbance from solar activity hits HF hardest near the poles (FOM 9.7.2.1).", src="fom")

A[170] = dict(reuse=True, topic="Oceanic",
  note="Tell ATC when the deviation is over and you are back on the cleared route. On the A330 the datalink route is the ATC LAT REQ page on the MCDU, and the PRC oceanic card says broadcast on 121.5 and 123.45 if no clearance can be had.")

A[171] = dict(topic="Oceanic", q="How do you insert the offset in the FMS?",
  a="LAT REV at the FROM waypoint, OFFSET, type the value and side such as 5L or L5, INSERT",
  detail="The OFFSET page is reached from the Lateral Revision at the FROM waypoint or any downpath waypoint except the destination. An offset of 1 to 50 NM in one mile steps, left or right, immediate or deferred, ending by default or at a planned waypoint. The PRC FMS Guide: F-PLN key, 1L, type the offset and direction, for example L5 or 5L, insert at 2L, then 6R INSERT. Clear it with CLR or 0.",
  ref="FCOM DSC-22_20-10-30-12 P 32/60 Offset",
  quote="The OFFSET page is accessed from the Lateral Revision (LAT REV) page at the FROM waypoint or at any waypoint downpath the flight plan, except the destination airport. An offset may be defined between 1 and 50 NM in one-nautical-mile steps.",
  note="The PRC engine failure card uses the same page for the 5 NM contingency offset: pull heading or insert a 5 NM left or right offset on the F-PLN page.", src="fcom")

A[174] = dict(reuse=True, topic="Weather and Minimums",
  note="The same section adds two you will use often. Call when actual fuel differs from planned by 3000 lb on the A330, and any time you are in moderate or greater turbulence.")

A[179] = dict(reuse=True, topic="Fuel Planning",
  note="On the release the special reserve shows as 10 percent of the oceanic and remote continental time plus 45 minutes at normal cruise consumption at the top of descent weight and altitude. A standard flag release carries 30 minutes at 1500 ft instead.")

A[184] = dict(topic="Weather and Minimums", q="Airborne, what weather do you need at destination, alternate and ETOPS alternates, and to start an approach?",
  a="Crew operating minima once airborne; to begin the final approach segment, reported RVR or visibility at or above minimums",
  detail="After takeoff the standard is the crew's operating minima: the weather required for the operating crew to fly the approach given their minima and any MEL. FOM 6.3.5 says that for ETOPS alternates and states it is less restrictive than the Dispatch planning criteria. Before beginning the final approach segment the latest reported RVR, visibility, and ceiling if required, must be at or above the authorized minimums; a report received after that point does not stop the approach.",
  ref="FOM 6.3.5 In-Flight ETOPS Alternate Airport Weather Requirements",
  quote="Forecast weather at the ETOPS alternate must be at or above crew’s operating minima (this is the weather required for the operating crew to conduct the approach, given the crew’s minima and any applicable MEL). Note that these weather requirements are less restrictive than the criteria used by Dispatch in planning.",
  note="Do not apply the derived alternate minimums table to an in-flight divert. That table is for Dispatch. FOM 5.6.11 governs beginning the approach.", src="fom")

A[187] = dict(topic="Cruise and Diversion", q="How do you get updated enroute and descent winds?",
  a="WIND/TEMP REQUEST at 2R on the CRUISE or DESCENT WIND page, an ACARS uplink",
  detail="On the wind pages, pressing WIND/TEMP REQUEST at 2R sends a request for ACARS winds and temperature. The DES WIND page is reached from NEXT PHASE on the CRUISE WIND page or the WIND prompt on the VERT REV page and takes winds at five altitudes. The descent preparation SOP has the PF check the DES WIND page and enter winds from cruise level down.",
  ref="FCOM DSC-22_20-20-10-25 P 13/154 Descent Wind Page",
  quote="[ 2R ] WIND/TEMP Pressing this key sends a request for ACARS winds and temperature. REQUEST (Refer to DSC-22_20-30-80 Wind Data - Request for Wind Data)",
  note="During cruise DIR TO is not available while uplinked wind data sits uninserted on the CRUISE WIND page. Insert or cancel it.", src="fcom")

A[188] = dict(topic="Cruise and Diversion", q="Engine failure over the western US or other terrain critical regions. What is the plan?",
  a="Fly the release's terrain clearance plan: zero net gradient or driftdown segment to the listed airport",
  detail="The Enroute Terrain Clearance Program limits takeoff weight so the aircraft clears enroute terrain with an engine failed, and the plan is described on the Flight Plan. A Zero Net Gradient Segment keeps a net climb gradient 1000 ft above terrain; a Driftdown Segment clears terrain by 2000 ft on the routing to the indicated airport from the point of failure. HA releases carry the remark TERRAIN MORA CHECK PERFORMED, ONE ENG OUT DRIFTDOWN, PASSED. The PRC Engine Failure During Cruise card gives the flying: MCT, A/THR off, green dot, FL200 initially, then REC MAX EO.",
  ref="FOM 8.3.7 Enroute Terrain Clearance Program (ETCP)",
  quote="A Driftdown Segment (Method 2) is one along which the aircraft can, with one engine inoperative, clear terrain by 2000 ft as it proceeds to the indicated airport. The plan indicates the routing to the chosen airport from the point of engine failure that ensures terrain clearance.",
  note="For the obstacle strategy the PRC says hold green dot until clear of obstacles. Depressurization escape routes are a separate product, the decompression polygons in FOM 11.2.9.", src="fom")

A[189] = dict(reuse=True, topic="Oceanic",
  note="Squawk 7700, exterior lights on, and broadcast identification, condition, position and intentions on 121.5. The PRC engine failure card adds the A330 speeds: 290 kt or M 0.82 for ETOPS, 300 kt or M 0.82 standard strategy, green dot for obstacles.")

A[190] = dict(kind="walkthrough", topic="Abnormals and QRH", q="Review the PRC immediate actions for an engine failure in cruise",
  a="MCT and A/THR off together, pull green dot, 5 NM offset oceanic, pull FL200, start APU, then ECAM",
  detail="As soon as the failure is recognized: simultaneously set MCT and disconnect autothrust with the instinctive disconnect button, pull speed to green dot, for oceanic operations turn at least 30 degrees to establish a 5 NM parallel offset, pull FL200 until the final driftdown altitude is known, start the APU. Exterior lights on, monitor TCAS, declare MAYDAY, then accomplish ECAM actions. Later reset REC MAX EO in the FCU and adjust speed for the strategy.",
  ref="PRC p6 Engine Failure During Cruise Procedure",
  quote="SIMULTANEOUSLY, SET MCT AND DISCONNECT AUTOTHRUST Use the Instinctive Disconnect P/B. PULL SPEED - GREEN DOT",
  note="The crew must not decelerate below green dot; at high level close to the weight limit the speed decays fast, so do not delay the descent.", src="prc")

A[191] = dict(reuse=True, topic="Oceanic",
  note="The PRC engine failure card: leave the cleared track by turning at least 30 degrees left or right to a parallel same-direction track offset 5 NM, and once below FL290 or cleared by ATC maneuver as required. Direction weighs adjacent tracks, the alternate, any SLOP and terrain.")

A[194] = dict(topic="Oceanic", q="What is ITP?",
  a="In Trail Procedure: a CPDLC climb or descent through an occupied level using ADS-B reference aircraft",
  detail="An ITP is a flight level change through the level of one or two reference aircraft in trail, using qualified ADS-B data, TCAS and ADS-B combined. The PRC card lists the criteria: no more than two reference aircraft, altitude difference at or below 2000 ft, ITP distance at least 15 NM with a closing ground speed differential at or below 20 kt or 20 NM with 30 kt, climb or descent at 300 ft/min minimum, same direction, and the ITP aircraft able to hold its Mach.",
  ref="FCOM DSC-34-20-20-20 P 2/2 ATSA In Trail Procedure (ATSA ITP)",
  quote="The ITP enables aircraft in oceanic areas or areas that do not have radar coverage to change flight levels on a more frequent basis with a longitudinal separation that is temporarily reduced during the climb",
  note="ATC remains responsible for separation. If anything goes wrong during the maneuver apply the regional contingency procedures from the AIP. The criteria list is on PRC p35.", src="fcom")

A[195] = dict(topic="Oceanic", q="When would you use an ITP?",
  a="When a standard climb or descent is blocked by traffic in trail and the MCDU says ITP POSSIBLE",
  detail="Use it when you want a level change in procedural oceanic airspace and the only conflict is one or two same-direction aircraft ahead or behind at the intervening levels. First check REC MAX FL on the PROG page, then MCDU MENU, TRAF at 5R, IN TRAIL PROCEDURE, enter the desired flight level and check ITP POSSIBLE with its time limit and the reference aircraft in green.",
  ref="PRC p35 CPDLC In-Trail Procedures, Procedure",
  quote="MCDU PROG page…………………………………………….…SELECT REC MAX FL...………………………………………………...…..CHECK MCDU MENU page..………………………......................SELECT TRAF prompt (LSK 5R)...…………………......................SELECT IN TRAIL PROCEDURE prompt (LSK 5R)……………....SELECT DESIRED FL (LSK 1L)…………………………………………....ENTER ITP POSSIBLE or NOT………….……………………………....CHECK",
  note="If ITP is no longer possible when the clearance arrives, send UNABLE. If still possible send WILCO and perform it without delay, holding current Mach and at least 300 ft/min.", src="prc")

A[196] = dict(topic="Oceanic", q="How do you request an ITP climb or descent?",
  a="ATC VERT REQ page: CLB TO or DES TO the flight level, then FREE TEXT with ITP and the reference aircraft",
  detail="From the ATC VERT REQ page enter CLB TO or DES TO the desired level at 1L or 2L, then add the ITP information in the free text: line 1 ITP, line 2 the ITP distance NM AHEAD or BEHIND and the flight ID of the first reference aircraft, line 3 AND plus the second reference aircraft if there is one. The flight IDs must exactly match the ITP TRAFFIC LIST page.",
  ref="PRC p36 CPDLC In-Trail Procedures cont'd",
  quote="Request an ITP clearance to ATC by CPDLC in the ATC VERT REQ",
  note="Write ITP, not In Trail, and do not add slashes or extra spaces; ATC's system parses the text.", src="prc")

A[197] = dict(topic="Cruise and Diversion", q="How do you change to a new destination in the FMS?",
  a="LAT REV at a waypoint, type the new destination into NEW DEST, then INSERT",
  detail="From the F-PLN page take a lateral revision at a waypoint other than the FROM and TO, type the new destination into the scratchpad and put it in the NEW DEST field, then insert the temporary flight plan. The approach SOP uses the same field when the F-PLN has lost its destination after a missed approach: perform a LAT REV at the last waypoint and redefine the destination in NEW DEST.",
  ref="FCOM PRO-NOR-SOP-18-A P 5/6 Approach General",
  quote="Perform a LAT REV at the last waypoint and redefine the destination in the NEW DEST field.",
  note="The PRC FMS Guide has the keystrokes under NEW DESTINATION (DIVERT). Load the diversion runway and approach next, then the weather and landing performance request.", src="pro")

A[198] = dict(topic="Cruise and Diversion", q="What is backup navigation?",
  a="MCDU NAV B/UP: the MCDU navigates from its stored flight plan and the onside IRS when both FMGECs fail",
  detail="The MCDU continuously memorizes the active flight plan downloaded from the FMGEC. If both FMGECs fail, the crew selects the back up navigation mode on the MCDU MENU page and recovers flight planning, aircraft position from the onside IRS or IRS 3, the F-PLN on the ND with automatic sequencing, limited lateral revision, but no AP or FD NAV mode. MCDU 3 cannot do it.",
  ref="FCOM DSC-22_10-30 P 6/6 Back Up Navigation Mode",
  quote="If both FMGECs fail, the back up navigation provides the following functions: ‐ Flight Planning ‐ Aircraft position using onside IRS or IRS 3 ‐ F-PLN display on ND ‐ No AP/FD NAV mode ‐ Limited lateral revision ‐ F-PLN automatic sequencing.",
  note="It is also the answer to a permanent MAP NOT AVAIL on both NDs after a failed FM reset. The PRC Oceanic References card counts one FMGEC plus one BACK UP NAV as meeting RNP 4 and RNP 10 entry equipment.", src="fcom")

A[199] = dict(topic="Cruise and Diversion", q="How do you navigate with backup navigation to a point or destination?",
  a="Select NAV B/UP on the MCDU MENU, fly the stored F-PLN with selected modes, using bearing and distance to the TO waypoint",
  detail="Activate NAV B/UP from the MCDU MENU page with the FM source selector in NORM. It gives you the memorized F-PLN, its display on the ND, automatic sequencing, AP and FD selected modes if one FG remains, limited lateral revisions, magnetic or true bearing and distance from the aircraft to the TO waypoint, true track between waypoints, time estimates from the onside IRS ground speed, and total time and distance to destination.",
  ref="FCOM DSC-22_20-40-20 P 1/10 MCDU Back Up Navigation, General",
  quote="‐ MAG (True) bearing depending on the pilot selection, from aircraft position to the TO WPT and associated distance ‐ True track between waypoints ‐ Time estimates computed with current GS from onside IRS ‐ Total time and distance to destination",
  note="Fly heading or track to the bearing it gives you; there is no managed NAV. With NAV B/UP on both sides at least one FG must be available to engage AP and A/THR.", src="fcom")
