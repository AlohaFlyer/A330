# Answers, part 4: edits to reused FOM records that carried B787-specific text.
A = {}

A[29] = dict(reuse=True, topic="Weather and Minimums",
  a="1 sm or RVR 5000 standard; lower than standard down to 500 RVR with CL and HIRL",
  detail="Standard takeoff minimums are 1 sm visibility or RVR 5000. The FOM lower than standard table takes the A330 down to 1600 RVR with any of HIRL, CL, RCLM or adequate visual reference, 1200 with the day or night lighting shown, 1000 with CL or HIRL and RCLM, and 500 RVR with CL and HIRL. Below 500 RVR is 737 and 787 HUD territory only.",
  ref="FOM 5.4.4 IFR Lower than Standard Takeoff Minimum Requirements",
  quote="When RVR ≤ 1600 ft (500 m) or 1/4 sm, the Captain must perform the takeoff.",
  note="Charted SID or obstacle minimums may be more restrictive than the 10-9A. At foreign airports you are held to the higher of the 10-9A and Ops Specs.", src="fom")

A[30] = dict(reuse=True, topic="Weather and Minimums",
  a="At or below 1600 RVR or 1/4 sm, the Captain makes the takeoff",
  detail="Ops Spec C078 authorizes lower than standard takeoff minimums wherever a procedure allows standard minimums. Any time the visibility is at or below 1/4 sm or 1600 RVR, the Captain will make the takeoff. High minimums Captain takeoff requirements are in FOM chapter 3, and initial First Officer restrictions in FOM 3.6.",
  ref="FOM 5.4.3 Captain Required Takeoff",
  quote="Any time the visibility is less than or equal to 1/4 sm or 1600 RVR, the Captain will make the takeoff.",
  note="The A330 floor is 500 RVR with CL and HIRL; the PRC Takeoff Limitations card tabulates the RVR, lighting and takeoff alternate requirements.", src="fom")

A[41] = dict(reuse=True, topic="Dispatch and Release",
  note="On the A330 the closeout arrives by ACARS and drives the Final TPR: AeroData uses the closeout takeoff weight and uplinks the ZFW and ZFWCG and the takeoff data to the FMS with it.")

A[60] = dict(reuse=True, topic="Pushback and Start",
  detail="Normal means is the flight interphone with standard phraseology. The ground crew plugs in at the nose and the flight deck talks on INT; the preliminary cockpit preparation has you check the INT knob is out with volume up so you can hear them. FOM 5.2.24 scripts the exact phraseology for brake release, cleared to start and cleared to disconnect, and the SOP makes the PF the one who handles ground crew communications.",
  note="FCOM PRO-NOR-SOP-01 puts ground crew communications on the PF and ATC on the PM. Before push, the N/WS DISC memo must be displayed or the tow pin is not in.")

A[66] = dict(reuse=True, topic="Pushback and Start",
  note="Same FIRE signal is used for any fire location, not just a tailpipe fire. Pair it with the QRH 17.09A ENGINE TAILPIPE FIRE procedure: master off, bleed pressure, crank.")

A[90] = dict(reuse=True, topic="Cold Weather and Runway Condition",
  note="Aircraft-side cold weather procedures are in FCOM PRO-NOR-SUP-ADVWXR, Supplementary Procedures, Adverse Weather; FOM 9.3 is the policy layer only.")

A[92] = dict(reuse=True, topic="Cold Weather and Runway Condition",
  note="The full runway state definitions and the wet and contaminated crosswind table for the A330 are in FCOM LIM-AG-OPS, keyed to RWYCC. Related: FOM 9.1.13 Degraded Braking uses the Can U StoP mnemonic.")

A[221] = dict(reuse=True, topic="Descent and Approach",
  note="Rev 125 revised LAHSO guidance to prohibit LAHSO on wet runways and require the tailwind to be calm, less than 3 kt. Read the current four factors in 5.6.32.2 before you quote them.")

A[230] = dict(reuse=True, topic="Descent and Approach",
  note="On the A330 the FCOM covers QFE under LIM-NAV Operations with QFE Barometric Reference and the MCDU approach minima insertion table. Where charted altitudes are built on QFE, use the correction tables on the chart.")

A[285] = dict(reuse=True, topic="ETOPS",
  detail="FOM 6.3.2 lists what is required before crossing the EEP. For the A330 the applicable items are forecast weather at the ETOPS alternate at or above the operating crew's minima, accounting for crew minima and any MEL, and completion of any ETOPS verification flight checks. After the EEP monitor distance from the ETOPS alternate; at the EXP and before top of descent complete any APU verification or in-flight start steps.",
  quote="• (787/A321/A330) Complete any ETOPS verification flight checks.")

A[286] = dict(reuse=True, topic="ETOPS",
  a="60 minutes from an adequate airport at .82M/290 KIAS, 408 nm; airports listed on the release",
  detail="Per FOM 6.3.3 the EEP is the point 60 minutes from an adequate airport at the approved one-engine-inoperative cruise speed in still air under standard conditions. For the A330-200 that is 408 nm at .82M/290 KIAS from the FOM 6.2.3 table. The EXP is the same fixed distance leaving the area. The adequate airports used must be listed on the Dispatch Release and crew and Dispatch must use the same ones.",
  ref="FOM 6.3.3 ETOPS Entry/Exit Point/Equal Time Point",
  quote="(HA) The adequate airports used to define EEP and EXP during dispatch planning must be listed on the Dispatch Release.",
  note="Enter and monitor the ETOPS waypoints with fleet procedures and crosscheck them against the route or the range rings. Identify arrival at EEP, ETP and EXP aloud.")

A[287] = dict(reuse=True, topic="ETOPS",
  a="A330-200: 803 nm at 120 minutes, 1200 nm at 180 minutes",
  detail="Table 6.2.3(1) in FOM 6.2.3 lists the A330-200 at .82M/290 KIAS single engine speed: 408 nm for 60 minutes, 803 nm for 120 minutes and 1200 nm for 180 minutes. These are Maximum Diversion Distances from the approved one-engine-inoperative cruise speed.",
  ref="FOM 6.2.3 ETOPS Area of Operation, Table 6.2.3(1)",
  quote="A330-200 .82M/290 KIAS 408 nm 803 nm 1200 nm",
  note="A reroute in an ETOPS segment must be coordinated with Dispatch so you do not fly beyond the MDD. The MDT is a planning number, not an operational time limit for the diversion itself.")

A[288] = dict(reuse=True, topic="ETOPS",
  a=".82M/290 KIAS, the approved one-engine-inoperative cruise speed",
  detail="FOM 6.4.5 ties the diversion speed to the approved One-Engine-Inoperative Cruise Speed in FOM 6.2.3, which for the A330 is .82M/290 KIAS at a 470 000 lb reference weight and FL350. The critical fuel scenario, the EEP and EXP distances and the MDD are all built on it. The PRC engine failure card (8/31/26) no longer repeats it: for ETOPS and standard strategy it now says set 300 kt or M 0.78; the FOM 125.3 table still reads .82M/290 KIAS.",
  ref="FOM 6.2.8 One-Engine-Inoperative Cruise Speed",
  quote="A330 .82M/290 KIAS 470,000 350",
  note="The Captain may deviate from the planned speed profile after assessing the emergency and fuel remaining. ETOPS and standard strategy on the PRC card (8/31/26) are 300 kt or M 0.78, obstacle strategy green dot; confirm which speed Dispatch planned with.")

A[289] = dict(reuse=True, topic="HAZMAT",
  detail="Dangerous goods policy lives in FOM Chapter 14, HAZMAT, section 14.1 Dangerous Goods, starting with 14.1.1 Regulatory Compliance under Ops Spec A055, 49 CFR Parts 171 to 175 and the IATA DGR. Key HA subsections: 14.1.4 eNOTOC, 14.1.6 Captain Responsibilities, 14.1.8 acceptable NOTOC versions, 14.1.17 rejected shipments, 14.1.20 ICAO ERG drill codes and 14.1.26 damaged or leaking DG.")

A[291] = dict(reuse=True, topic="HAZMAT",
  a="Select ACCEPT on the MCDU eNOTOC uplink",
  detail="FOM 14.1.6 requires the HA Captain to acknowledge the eNOTOC by selecting ACCEPT* on the MCDU, the Airbus method, or ACKNOWLEDGE NOTOC on the Comm page on the 787. The eNOTOC uplinks at departure minus 30 minutes for trans-Pacific and international flights and minus 15 for inter-island, and prints automatically.",
  note="If digital acknowledgment is impossible, acknowledge by voice to Dispatch and note it; the acknowledgment is the record that you saw the load. Hand edits to the eNOTOC are not permitted at HA.")

A[304] = dict(reuse=True, topic="TCAS and Traffic",
  note="The FOM carries policy only. The system, symbols and TA or RA logic are in FCOM DSC-34-20-60, and the traffic avoidance maneuver is the ECAM and FCOM abnormal procedure. Oceanic TCAS guidance is at FOM 5.7, TA/RA whenever possible.")

A[313] = dict(reuse=True, topic="Medical",
  detail="FOM 11.1.9.3 has you go to MedLink first, not Dispatch. With operational cabin SATCOM handsets the F/As call MedLink directly. With SATCOM but no cabin handset the A330 Flight Crew calls MedLink at (602) 282-4910 and relays information between the cabin and MedLink. Only with no operational SATCOM does the call route through ARINC for a patch, and Dispatch is conferenced in or called afterward when a diversion is possible.",
  quote="(A321/A330) The Flight Crew will relay info between cabin and MedLink.")

A[314] = dict(reuse=True, topic="Medical",
  detail="Per FOM 11.1.9.3, with operational SATCOM the Flight Crew calls MedLink Inflight Medical Assistance at (602) 282-4910 and, on the A330, relays information between the cabin and MedLink. Without SATCOM, contact ARINC for a phone patch to the same number. On the A330 the number sits in the SATCOM DIRECTORY SAFETY list; dial from the MCDU and talk on the ACP SATCOM key.",
  note="The A330 has no cabin headset conference like the 787: you are the relay, so have the F/A pass vitals to you before you dial. Ground Medical Assistance is (602) 282-6613 or (800) 961-4847.")

A[149] = dict(reuse=True, topic="Oceanic",
  detail="Time and fuel remaining from the FMS are recorded on the Flight Plan/Dispatch Release, or alternatively on the ACARS HOWGOZIT/Flight Plan Review, and compared against the estimates. On the A330 read fuel remaining from the FUEL PRED page, not the ECAM tank total, and keep the same source at every waypoint.")

A[125] = dict(reuse=True, topic="ETOPS", status="desktop", a="",
  detail="FOM 6.5.10 says the aircraft cannot proceed beyond the EEP if the item being verified is not operating normally. It does not address a failure after the EEP. Treat a post-EEP failure as an in-flight system failure under FOM 6.4.4 and the diversion logic in 6.4.1, with Dispatch.",
  note="No published source located, ask the check airman. Have the contingency plan agreed with Dispatch and Maintenance Control before departure, as the FOM verification flight section recommends.")

A[203] = dict(reuse=True, topic="Descent and Approach", status="desktop", a="",
  note="No published source located, ask the check airman. The FOM uses descend via only in the Mexico theater and says Central America does not use it at all; the US definition lives in the AIM.")

A[231] = dict(reuse=True, topic="Descent and Approach",
  note="The only PBN autopilot mandate in the FOM is 5.1.4.1, RNP AR with RNP below 0.3 or RF legs, and the FCOM takeoff SOP repeats it: the AP must be engaged for RNP AR below 0.3 NM. Nothing requires the autopilot on an RNAV 1 STAR.")
