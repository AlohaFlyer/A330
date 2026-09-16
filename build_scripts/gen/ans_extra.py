# Extra records: grade-sheet sections and groups in the workbook that carry no bullet question.
# Each is a walkthrough item. `after` names the workbook index the record follows in drill order.
DESK = "No published source located, ask the check airman"
X = []

X.append(dict(after=34, sec="1.1.2.4", secTitle="Know Operational Control (Dispatch) Requirements", group="Supplemental Operations", coi=True,
  kind="walkthrough", topic="Dispatch and Release", q="Supplemental operations: what changes?",
  a="Nothing in fuel or minima: the flight runs under Domestic or Flag rules and the release says which",
  qOrig="Supplemental Operations",
  detail="Supplemental, non-scheduled, operations are authorized within the approved areas and are conducted under Domestic or Flag rules per Ops Spec A030 or Exemption 11047. The Dispatcher notes on the release whether the flight is operated as Part 121 Domestic or Flag, and the fuel and weather rules follow from that.",
  ref="FOM 8.1.1.3 Supplemental Operations",
  quote="Non-scheduled passenger or cargo operations are authorized within the areas approved for enroute operations. Online or Offline Supplemental Operations will be conducted using Domestic or Flag rules as applicable per Ops Spec A030 or Exemption 11047.", note="Read the release remark first: it tells you which rule set you are under for the whole leg.", src="fom", status="verified"))

X.append(dict(after=187, sec="5.1.2.6", secTitle="Know Contingency Plan (i.e., Alternates, WEATHER Monitoring, Fuel, etc.)", group="Discuss Route Diversion scenario", coi=True,
  kind="walkthrough", topic="Cruise and Diversion", q="Talk through a route diversion",
  a="Complete the ECAM or QRH, decide whether the failure requires diversion, weigh continuing against diverting, coordinate with SOCC",
  qOrig="Discuss Route Diversion scenario",
  detail="The PRC Diversion Guidance card: complete the non-normal procedure, then ask whether the failure requires diversion. Failures that do: anything requiring landing such as LAND ASAP, fire or an engine failure, insufficient fuel after a component failure raises consumption, or one generator remaining. Otherwise weigh whether the risks of continuing exceed the risks of diverting, and coordinate the divert with SOCC. Amber or green ECAM messages and any single failure other than an engine have no impact on ETOPS.",
  ref="FCOM PRO-SPO-40A P 5/8 Diversion Decision Making (PRC p2 Diversion Guidance)",
  quote="Failure cases requiring a diversion to the nearest airport (cases leading to a LAND ASAP message on the ECAM and/or in the QRH) ‐ Failure cases resulting in increased fuel consumption, exceeding the available fuel reserves ‐ Electrical generation. Diversion is required in the case of: • Only one generator (either one IDG, APU GEN or EMER GEN) remaining available following a multiple failure",
  note="Then the mechanics: NEW DEST in the FMS, weather and landing performance, fuel prediction, Dispatch and MedLink if medical, and the NTSB brief to the cabin.", src="fcom", status="verified"))

X.append(dict(after=239, sec="9.1.4.1", secTitle="Know Procedures for CAT II/III ILS Autoland Landing", group="", coi=False,
  kind="walkthrough", topic="Descent and Approach", q="Know the CAT II and III autoland procedure",
  a="Lowest achievable minimum, both APs, CAT 2 or CAT 3 on the FMA below 5000 ft, LAND at 350 ft, autoland, degraded guidance strategy above and below 1000 ft",
  qOrig="Know Procedures for CAT II/III ILS Autoland Landing",
  detail="Descent preparation: choose the lowest achievable minimum, limited by crew qualification, the operating manual, aircraft status and airport status, enter NO DH for CAT III without DH, and brief task sharing, degraded guidance and the airport low visibility procedures. Both APs in APPR, capability displayed below 5000 ft AGL. Above 1000 ft a caution or capability loss means complete the procedure and check the required equipment or go around; below 1000 ft go around; below the 200 ft alert height for CAT 3 DUAL continue unless AUTOLAND lights.",
  ref="FCOM PRO-NOR-SOP-18-C P 1/32 Approach Using LOC G/S Guidance, Descent Preparation",
  quote="For CAT II, CAT III, approaches, review the following items on top of the usual briefing: ‐ Task sharing and callouts ‐ Management of degraded guidance ‐ Low visibility procedures at the airport.",
  note="CAT II DH minimum 100 ft, CAT III single 50 ft, CAT III dual no DH with 75 m RVR. Wind limits 35, 10 and 15 kt. Engine-out autoland only in CONF 3 with the procedures done before 1000 ft.", src="pro", status="verified"))

X.append(dict(after=239, sec="9.1.4", secTitle="Perform CAT I/II/III ILS Autoland Landing", group="", coi=False,
  kind="walkthrough", topic="Descent and Approach", q="Perform an autoland",
  a="Both APs, APPR, LAND at 350 ft, FLARE, ROLL OUT, reversers, then AP off and log it on the ACARS Autoland Report",
  qOrig="Perform CAT I/II/III ILS Autoland Landing",
  detail="Fly the ILS with both autopilots engaged after APPR. At 350 ft RA check LAND engaged and announce it; if no LAND mode, autoland is not authorized. The AP flies FLARE and ROLL OUT, the PM checks and announces ground spoilers, reversers and autobrake, and the AP comes off at taxi speed. Every autoland attempt is reported on the ACARS Autoland Report page per FOM 5.6.21.2.",
  ref="FCOM PRO-NOR-SOP-18-C P 3/32 Final Approach",
  quote="AT 350 ft RA LAND mode.............................................................. CHECK ENGAGED/ANNOUNCE PF L2 If no LAND mode, autoland is not authorized.",
  note="A CAT I autoland is only for practice on a CAT II or III runway with the tower advised, or on a CAT I beam under the FCOM precautions. Check the tower wind against 35, 10 and 15 kt.", src="pro", status="verified"))

CRM = [
 ("12.3.5", "Demonstrate and Apply Principles of Team Effectiveness", "Demonstrate team effectiveness",
  "Captain sets the tone, uses every crewmember, mentors with credibility, and solicits feedback",
  "FOM 10.1.1.3 Leadership Command, Mentoring Teamwork",
  "The Captain sets an approachable and responsive tone for the Flight Deck to optimize team performance by acknowledging the importance of and utilizing all applicable crewmembers in task accomplishment.",
  "Assess the crew elements, proficiency, experience and recency, and modify roles as the situation dictates. On an augmented crew that includes the relief pilot's briefing before the rest break."),
 ("12.1.8", "Demonstrate Situational Awareness and Management of Information", "Demonstrate situational awareness",
  "Continuously monitor, state and remain aware of conditions; verbalize the plan for actual, expected and contingent situations",
  "FOM 10.1.1.2 Workload Management, Situational Assessment",
  "Continuously monitor, state, and remain aware of conditions that affect operations.",
  "The FOM standard is stated aloud: verbalizing the assessment is how the PM knows you have it. Vigilance scales with the workload condition."),
 ("12.1.3", "Demonstrate Effective Communication (Including Briefings)", "Demonstrate effective communication and briefings",
  "Open interactive communication, seek information, scalable assertiveness: Ask, Say, Command, Assume Control",
  "FOM 10.1.1.1 Communication",
  "The Captain is responsible for setting the overall tone and stating minimal acceptable performance standards for safe operations when not specifically defined in the SOP.",
  "Briefings review threats and management strategies and assign specific PM duties. Do not mitigate your speech in a high-risk situation."),
 ("12.3.2", "Demonstrate and Apply Leadership Concepts", "Demonstrate leadership",
  "Accept PIC authority, balance command with crew participation, decide and state the decision, resolve conflicts on what is right",
  "FOM 10.1.1.3 Leadership Command, Decision Making",
  "After technical and/or CRM input is considered, the Captain makes a decision and clearly states it to the crew.",
  "Immediate decisions when time or operational restrictions dictate; otherwise methodical threat, risk, course of action. Resolutions are command, collaborate or accommodate."),
 ("12.1.7", "Demonstrate Problem Solving and Decision Making including Threat Error Management", "Demonstrate TEM and decision making",
  "Anticipate, recognize, recover: identify threats, build strategies, trap errors with SOPs and checklists, mitigate any undesired aircraft state",
  "FOM 10.1.2.3 Anticipate/Recognize/Recover",
  "Anticipation is at the heart of TEM. It is essentially a two-step process: (1) identify relevant threats and (2) develop management strategies for each utilizing various resources.",
  "See it, Say it obligates the PF to respond. If the PF does not react to a UAS the PM commands the correction in one or two words, and as a last resort takes control."),
 ("12.1.9", "Demonstrate Workload Management", "Demonstrate workload management",
  "Fly the aircraft first, prioritize by risk, manage time, use and manage automation, report overload",
  "FOM 10.1.1.2 Workload Management, Prioritize Tasks",
  "‐ Fly the aircraft first. ‐ When the aircraft is stable and safe, navigate while properly analyzing the situation. ‐ Prioritize operational tasks based upon risk/criticality to safety of flight.",
  "Automation is a workload tool: use it in high-density traffic, drop it when it raises workload or lowers awareness, and when hand flying have the PM make the automation inputs."),
]
for sec, title, q, a, ref, quote, note in CRM:
    X.append(dict(after=293, sec=sec, secTitle=title, group="", coi=True, kind="walkthrough", topic="CRM and PM Duties",
      q=q, a=a, qOrig=title, detail="Graded CRM dimension on the OE grade sheet. The standard is the FOM CRM and TEM chapter: Communication, Workload Management, Leadership and Flight Discipline as core skills, with TEM as the framework for preventing, trapping and mitigating threats and errors.",
      ref=ref, quote=quote, note=note, src="fom", status="verified"))

PM = [
 ("11.1.1", "Perform PM Duties During Taxi", "PM duties during taxi", "Airport diagram out and followed, ATC and company comms, flight control check calls, taxi flow items, runway crossing dual acknowledgment"),
 ("11.1.2", "Perform PM Duties during Takeoff", "PM duties during takeoff", "THRUST SET, ONE HUNDRED KNOTS, V1 monitor, ROTATE, POSITIVE RATE, gear, PFD and engine monitoring"),
 ("11.1.3", "Perform PM Duties During Departure and Climb", "PM duties during departure and climb", "Flap retraction on schedule, after takeoff flow, altitude and speed deviation callouts, FMA CHECKED responses"),
 ("11.1.4", "Perform PM Duties During Cruise", "PM duties during cruise", "Waypoint checks, fuel score, position reports, weather and dispatch communication, altimeter crosschecks"),
 ("11.1.5", "Perform PM Duties During Descent and Arrival", "PM duties during descent and arrival", "Weather and landing information, ECAM status, landing performance, 10 000 ft flow, transition level QNH"),
 ("11.1.5.2", "Monitor and Respond to ATC/Company Communications", "Monitor and respond to ATC and company communications", "PM handles ATC and company on VHF 1 and 2, dual acknowledgment of runway clearances, written complex taxi instructions"),
 ("11.1.7", "Perform PM Duties During Approach", "PM duties during approach", "Flap and gear selections on order, LOC and GLIDESLOPE half dot calls, ONE HUNDRED ABOVE, MINIMUM, stabilized gate calls"),
 ("11.1.9", "Perform PM Duties During Landing", "PM duties during landing", "SPOILERS, REVERSERS, AUTO BRK, DECEL, SEVENTY KNOTS announced from the ECAM and PFD"),
 ("11.1.8", "Perform PM Duties During Go-Around/Missed Approach", "PM duties during go-around", "FLAPS on order, POSITIVE RATE, gear up, FMA and altitude monitoring, ATC notification"),
 ("11.1.10", "Perform PM Duties following Landing", "PM duties after landing", "After landing flow: radar off, start selector NORM, flaps up, TCAS standby, APU, anti-ice, brake temperatures"),
]
for sec, title, q, a in PM:
    X.append(dict(after=299, sec=sec, secTitle=title, group="", coi=False, kind="walkthrough", topic="CRM and PM Duties",
      q=q, a=a, qOrig=title,
      detail="Task sharing is defined phase by phase in FCOM PRO-NOR-TSK and in each SOP chapter with the PF, PM, PF-PM and BOTH labels. PF or PM means a single crewmember does it, PF-PM means both do it but not necessarily together, BOTH means at the same time because coordination is needed. The FOM adds the PM's flight discipline standard: monitor the flight path first and never let secondary tasks interfere.",
      ref="FCOM PRO-NOR-TSK P 1/26 Tasksharing, General Information",
      quote="PF or PM is used for individual actions. The actions should be completed by a single crew member, the PF or the PM. This rule also applies for CM1 or CM2.",
      note="FOM 10.1.1.4: the PM assesses and communicates threats, holds the shared mental model, and uses Ask, Say, Command to restore safety margins.", src="pro", status="verified"))

X.append(dict(after=299, sec="8.3.5.27", secTitle="Know Contingency Approach Procedures for RNP-AR Operations Following System Malfunction, Weather Deviation or ATC Mandate", group="", coi=False,
  kind="walkthrough", topic="Descent and Approach", q="RNP AR contingency: when do you continue and when do you go around?",
  a="Continue after a single GPS, FMGS, DU, MCDU or AP failure; discontinue for no FINAL APP, dual GPS PRIMARY LOST or NAV ACCUR DOWNGRAD, position disagree, XTK at 1 RNP",
  qOrig="Know Contingency Approach Procedures for RNP-AR Operations Following System Malfunction, Weather Deviation or ATC Mandate",
  detail="Management of degraded navigation for RNAV(RNP): the approach may continue after a single failure of a GPS, FMGS, EFIS DU, MCDU or AP. Discontinue if FINAL APP does not engage, GPS PRIMARY LOST on both NDs, dual NAV ACCUR DOWNGRAD, FM/GPS POSITION DISAGREE, FMS1/FMS2 POS DIFF, dual FMGC or FINAL APP loss, dual AP failure with RNP below 0.3, loss of the GPWS terrain function, or NAV ALT DISCREPANCY. Go around if XTK reaches 1 RNP or V/DEV reaches three quarters of a dot below the path.",
  ref="FCOM PRO-NOR-SOP-18-C P 18/32 Management of Degraded Navigation",
  quote="Discontinue the approach in the following cases: ‐ FINAL APP does not engage ‐ GPS PRIMARY LOST on both NDs ‐ Dual NAV ACCUR DOWNGRAD ‐ FM/GPS POSITION DISAGREE ‐ FMS1/FMS2 POS DIFF ‐ Dual loss of FMGC or dual loss of FINAL APP mode ‐ Dual AP failure if the RNP < 0.3 NM",
  note="Both GPS in NAV and both FMS available before the IAF or RNP AR is not permitted. Baro difference between altimeters no more than 100 ft. Brief the degraded navigation chapter as part of the go-around strategy.", src="pro", status="verified"))

X.append(dict(after=299, sec="11.1.10.4", secTitle="Know Airplane Shutdown and Securing Procedures", group="", coi=False,
  kind="walkthrough", topic="Taxi and Ground", q="Know the shutdown and securing procedures",
  a="Parking SOP: 1 minute cool, APU bleed, masters off, beacon off when spooled down, pumps off, slides disarmed, chocks, logbook from STATUS; then Securing the Aircraft",
  qOrig="Know Airplane Shutdown and Securing Procedures",
  detail="Parking: ACCU pressure in the green or chocks before shutdown, parking brake on unless a brake is above 500 C, anti-ice off, APU bleed on and wait for the memo, engines off no less than 1 minute after high thrust, wing lights off before the jet bridge, beacon off once spooled down, fuel pumps off, transponder standby, IRS performance and fuel quantity checks, slides disarmed on the DOOR/OXY page, chocks confirmed by hand signal, logbook completed from the ECAM STATUS page, Parking checklist. Securing the Aircraft follows per PRO-NOR-SUP-SEC when the aircraft is left.",
  ref="FCOM PRO-NOR-SOP-22 P 3/6 Parking, Exterior Lights",
  quote="Turn off the beacon lights when all engines spooled down.",
  note="With a hot brake above 300 C, 150 C with fans, release the parking brake after chocks are in. The fuel used plus fuel on board must reconcile with departure fuel or maintenance action is due.", src="pro", status="verified"))

X.append(dict(after=308, sec="Misc", secTitle="Miscellaneous, not associated with grade sheet tasks", group="Megaphone (remove/use/replace)", coi=False,
  kind="walkthrough", topic="Emergency Equipment", q="Remove, use and replace the megaphone",
  a="", qOrig="Megaphone (remove/use/replace)",
  detail="The megaphone is cabin emergency equipment. FCOM DSC-25-30 covers the cockpit items and refers the cabin equipment description to the CCOM, and the location figure is at PRO-ABN-90. No operating steps for the megaphone are in the pilot manuals.",
  ref="FCOM DSC-25-30 P 2/2 Cabin Emergency Equipment",
  quote="For the description of the cabin emergency equipment, Refer to CCOM/EMERGENCY EQUIPMENT/PORTABLE EMERGENCY EQUIPMENT.",
  note=DESK + ". Have a flight attendant show you the stowage and the trigger.", src="fcom", status="desktop"))
