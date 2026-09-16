# Answers, part 3: workbook items 200 to 327 (sections 6.1.1.4 through Miscellaneous).
DESK = "No published source located, ask the check airman"
A = {}

A[200] = dict(topic="Descent and Approach", q="What goes into descent preparation?",
  a="Weather and landing info, charts, QNH preset on ISIS, ECAM status, landing performance, then the FMS pages",
  detail="The Descent Preparation SOP: obtain weather and landing information for destination and alternate, prepare the Jeppesen charts, preset QNH on the ISIS, check the ECAM STATUS page for any landing capability degradation, request landing performance via ACARS, then complete the FMS: ARRIVAL page, F-PLN A check, RADIO NAV, DES WIND, PERF CRZ and DES, PERF APPR with QNH, temperature, wind, minimum and landing configuration, PERF GO AROUND, FUEL PRED, followed by the approach briefing.",
  ref="FCOM PRO-NOR-SOP-16 P 1/10 Descent Preparation",
  quote="Check the weather reports and runway conditions at destination and alternate airports. Airfield data, if any, should include the runway to be used for arrival. When the aircraft operates in low OAT conditions, consider altitude corrections for low temperature.",
  note="Do not modify the final approach from the FAF to the runway in the F-PLN. Identify the FDP and check the FPA after it; a TOO STEEP PATH message means no FINAL APP guidance.", src="pro")

A[202] = dict(topic="Descent and Approach", q="How do you start the descent?",
  a="Engage DES mode at the FMS top of descent; DES for an early descent, green dot if delayed",
  detail="The standard method is to engage DES at the T/D computed by the FMS. For an early descent from ATC use DES, which guides down at a lower vertical speed to converge with the profile, or about 1000 ft/min in V/S. If ATC delays the descent past T/D, DECELERATE or T/D REACHED appears and you slow toward green dot with ATC permission, then engage DES with managed speed when cleared.",
  ref="FCOM PRO-NOR-SOP-17 P 1/6 Descent Initiation",
  quote="The standard method to initiate the descent is to engage the DES mode at the Top of Descent (T/D) computed by the FMS.",
  note="Monitor with the PF MCDU on PROG for VDEV. In DES mode on or below the path do not use speed brakes, the A/THR will add thrust against them; use OP DES with speed brakes instead.", src="pro")

A[209] = dict(status="desktop", kind="drill", topic="Weather and Minimums", q="Lowest visibility for an SA CAT II approach?",
  a="", detail="The FCOM limitation for SA CAT II gives the minimum decision height, 100 ft, with at least one autopilot in APPR mode and CAT 2 or CAT 3 on the FMA, and without a HUD the landing must be automatic. The controlling RVR sits on the approach briefing cards in the PRC, which the FOM points to and which the text extract does not carry.",
  ref="FCOM LIM-AFS-20 P 1/4 Special Authorization CAT II (SA CAT II)",
  quote="Without HUD, the flight crew must perform an automatic landing.",
  note=DESK + ". Read the RVR off the PRC Approach and Landing Limitations card.", src="fcom")

A[210] = dict(topic="Weather and Minimums", q="Lowest visibility for a CAT III approach?",
  a="75 m RVR, CAT III without DH, fail operational with CAT 3 DUAL",
  detail="FCOM Limitations: ILS Category III fail operational, dual, has an alert height of 200 ft, needs A/THR in selected or managed speed and both autopilots in APPR with CAT 3 DUAL on the FMA, and for CAT III without DH the minimum runway visual range is 75 m. Fail passive, CAT 3 SINGLE, carries a 50 ft minimum decision height.",
  ref="FCOM LIM-AFS-20 P 2/4 ILS Category III Fail Operational (Dual)",
  quote="CAT III without DH: Minimum Runway Visual Range..............................................................................................75 m",
  note="Ops Spec C060 limits the crosswind to 15 kt for CAT II and III; headwind 35 kt, tailwind 10 kt. One-engine CAT III autoland is not authorized (FOM 5.6.17.3).", src="fcom")

A[212] = dict(reuse=True, topic="Descent and Approach",
  a="CAT II or III runways, autoland qualified PIC, within the FCOM autoland envelope",
  detail="FOM 5.6.18 permits autoland only on CAT II or III runways, tells you to advise the tower so the ILS critical area is protected, and requires the PIC to be autoland qualified. The FCOM adds the envelope: CONF 3 or FULL, glide slope between 2.5 and 3.25 degrees, field elevation below 9200 ft, weight above 116 000 kg and below maximum landing weight, wind at most 35 headwind, 10 tailwind, 15 crosswind.",
  ref="FOM 5.6.18 Autoland Operations",
  quote="Autoland approaches and landings are permitted on CAT II/III runways only. Pilots should advise the tower anytime Autoland operations are conducted to ensure the ILS Critical Zone is protected.",
  note="The critical area is protected automatically only below 800 ft or 2 miles. The FCOM allows autoland on a CAT I installation in better weather only with the airline's beam check and CAT 2 capability on the FMA.", src="fom")

A[213] = dict(reuse=True, topic="Descent and Approach", q="When must you autoland?",
  a="CAT II and CAT III approaches, and SA CAT II without a HUD",
  detail="FOM 5.6.17.2 and 5.6.17.3 require CAT II and CAT III approaches to be flown with Autoland, or HGS AIII on the 737 only, so on the A330 every CAT II or III is an autoland. The FCOM SA CAT II limitation says without HUD the flight crew must perform an automatic landing. To be qualified the HA Captain must first complete one automatic landing in the aircraft.",
  ref="FOM 5.6.17.2 CAT II/SA CAT II Operating Limitations",
  quote="CAT II approaches must be flown with either Autoland or (737) HGS AIII procedures. Rollout guidance is not required.",
  note="Currency bites new Captains: without that one automatic landing logged in the aircraft you are not CAT II/III qualified regardless of sim performance (FOM 5.6.17).", src="fom")

A[223] = dict(topic="Descent and Approach", q="How do you request landing performance?",
  a="ACARS PERFORMANCE page, LDG CONDITIONS, enter wind and runway, then SEND",
  detail="From the ACARS MENU select PERFORMANCE, then LDG CONDITIONS. The airport populates with the destination, ZFW and EFOA uplink from the weight and balance data, the only required entry is the steady wind, and gust, OAT and QNH default to the METAR. Set the RCAM code at 3L, 6 is dry, per runway third if needed, flaps FULL or 3, then SEND at 6R. View the reply under VIEW DATA. Page 3/3 carries anti-ice, fail factor, autoland, reverse credit, A/THR and VAPP additive options.",
  ref="FCOM PER-ARD-ALP P 5/18 Landing Conditions",
  quote="To request landing performance access the LDG CONDITIONS page: PERFORMANCE → LDG CONDITIONS",
  note="HA policy is no credit for reverse thrust. For a failure not on the release that affects landing performance, compute the distance with Flysmart (PRO-NOR-SOP-16).", src="fcom")

A[224] = dict(status="desktop", kind="drill", topic="Descent and Approach", q="What do HXX/TXX and LXX/RXX mean on the landing data printout?",
  a="", detail="The landing data report layout is shown as a printed example figure in the FCOM PER-ARD-ALP section, which the text extract does not reproduce. The same section explains the two distances: SAFO Factored with a 15 percent margin, and Unfactored, the actual distance without margin.",
  ref="FCOM PER-ARD-ALP P 15/18 Printed Example",
  quote="The SAFO Factored Distances include a safety margin of 15% as recommended by SAFO 19001.",
  note=DESK + ". Read the designators off a real printout with the check airman.", src="fcom")

A[225] = dict(topic="Cold Weather and Runway Condition", q="When and why do you apply cold temperature corrections on approach?",
  a="When OAT is well below ISA, because true altitude is lower than indicated; charts flag when required",
  detail="Below ISA the true altitude is lower than indicated, and the error grows with cold and matters most where terrain separation is minimum. In the US the chart briefing strip carries a note when cold temperature corrections apply. The FOM sends you to the fleet manual for the procedure. The A330 SOP: consider altitude corrections for low temperature during descent preparation, and note that managed vertical guidance must not be used below the chart minimum temperature and FINAL APP may not engage when corrections are required.",
  ref="FOM 9.3.3.1 Cold Temperature Altimeter Corrections/Cold Temperature Restricted Airports",
  quote="When the temperature is lower than International Standard Atmosphere (ISA), true altitude is lower than indicated altitude. This temperature effect on indicated altitude becomes extremely important with very cold temperatures and minimum terrain separation.",
  note="For an RNAV(GNSS) approach with LNAV/VNAV minima the FMS profile ignores low OAT: vertical managed guidance must not be used below the chart minimum temperature (PRO-NOR-SOP-18-C).", src="fom")

A[226] = dict(topic="Descent and Approach", q="When in the descent do you set QNH?",
  a="Approaching the transition level, when cleared to an altitude; set it on the EFIS panels and the standby",
  detail="When the aircraft approaches the transition level and is cleared for an altitude, both pilots set the QNH on the EFIS control panel and the standby altimeter and crosscheck the settings and altitudes. The QNH was preset on the ISIS during descent preparation. Any QNH change must also go on the FMS PERF APPR page.",
  ref="FCOM PRO-NOR-SOP-17 P 3/6 Barometric Reference",
  quote="When the aircraft approaches the transition level, and when cleared for an altitude: BAROMETRIC REFERENCE................................................ SET/CROSSCHECK BOTH L2 ‐ Set QNH on the EFIS control panel and on the standby altimeter ‐ Crosscheck the barometric reference settings and the altitude indications.",
  note="A QNH that differs a lot from the one used in the approach preparation is a symptom of a barometric reference error; confirm it from all sources.", src="pro")

A[233] = dict(topic="Descent and Approach", q="Normal flap and gear schedule on approach?",
  a="Flaps 1 at green dot, flaps 2 by 2500 ft AGL, gear down, flaps 3, flaps FULL, stabilized by 1000 ft",
  detail="At green dot select FLAPS 1, more than 3 NM before the final descent point and on the final descent with flaps 1 and S speed by 2500 ft AGL on a decelerated approach. At 2500 ft AGL minimum FLAPS 2, and when the flaps are at 2 gear down, autobrake confirmed and ground spoilers armed. When the gear is down FLAPS 3, then FLAPS FULL, check VAPP, A/THR in SPEED or off, and the landing checklist.",
  ref="FCOM PRO-NOR-SOP-18-B P 3/6 Intermediate/Final Approach",
  quote="‐ For decelerated approaches, the aircraft must reach or be established on the final descent with FLAPS 1 and S speed at or above 2 500 ft AGL",
  note="If you intercept the glide below 2500 ft AGL, 2000 minimum, select FLAPS 2 at one dot below. Gear down early is the way to slow down; speed brakes raise VLS.", src="pro")

A[234] = dict(reuse=True, topic="Descent and Approach",
  a="FCOM PRO-NOR-SOP-18-A stabilization criteria and the SCO gates; the FOM only points there",
  detail="FOM 5.6.5 gives the policy and the warning and sends you to the fleet manual. The A330 criteria live in FCOM PRO-NOR-SOP-18-A, Stabilization Criteria: correct lateral and vertical path, landing configuration, thrust stabilized usually above idle at target speed, no excessive deviation. The gates and callouts are in PRO-NOR-SCO, Flight Parameters, Approach: 1000 ft AFE stabilized gate, 500 ft AFE go-around gate.",
  ref="FCOM PRO-NOR-SOP-18-A P 3/6 Stabilization Criteria",
  quote="In order for the approach to be stabilized, all of the following conditions must be satisfied before, or at the stabilization height: ‐ The aircraft is on the correct lateral and vertical flight path ‐ The aircraft is in the desired landing configuration ‐ The thrust is stabilized, usually above idle, and the aircraft is at target speed for approach ‐ The flight crew does not detect any excessive flight parameter deviation.",
  note="The FOM's one hard number is runway alignment by 500 ft AFE, with 300 ft exceptions on the airport 10-7 page.", src="pro")

A[235] = dict(reuse=True, topic="Descent and Approach",
  a="1000 ft AFE: gear, final flaps, speed brakes in, thrust set, sink 1000 or less, speed +20/-5, STABLE; 500 ft AFE: go-around gate",
  detail="The SCO approach table sets two gates. At 1000 ft AFE the stabilized gate: gear down, final flaps selected, speed brakes retracted, thrust appropriate for the configuration, vertical speed at or below 1000 ft/min unless briefed, airspeed target +20 and -5 kt. The PF calls STABLE, or CORRECTING SPEED or VERTICAL SPEED, and the PM answers CHECKED; if the configuration criteria are not met the call is UNSTABLE, GO AROUND, FLAPS. At 500 ft AFE the go-around gate applies the same criteria with the PM calling STABLE.",
  ref="FCOM PRO-NOR-SCO P 6/16 Flight Parameters, Approach",
  quote="Stabilized Gate 1 000 ft/min, must be briefed prior callouts, if Go (If 1 000 ft configuration to approach Around called by PF) criteria are not met) ▪ Airspeed: Target +20 kt/-5 kt",
  note="Only speed and vertical speed may be corrected through the 1000 ft gate; every other criterion is mandatory there. Runway alignment exceptions to 300 ft AFE are on the 10-7.", src="pro")

A[236] = dict(reuse=True, topic="Descent and Approach")

A[237] = dict(kind="walkthrough", topic="Descent and Approach", q="Demonstrate the ILS callouts and configuration steps",
  a="ARM APPROACH, LOC blue, G/S blue, LOC star, G/S star, both APs, flaps and gear on schedule, LAND at 350 ft, HUNDRED ABOVE, MINIMUM, CONTINUE or GO-AROUND",
  detail="Cleared, on the intercept and with LOC deviation shown, the PF presses APPR and calls the armed modes with their color, G/S blue and LOC blue, then engages the second AP and sets the go-around altitude. Captures are called without color, LOC, G/S. Configure per the schedule. At 350 ft RA check LAND engaged if autolanding. At minimum plus 100 the PM calls ONE HUNDRED ABOVE, at minimum MINIMUM, and the PF answers CONTINUE or GO-AROUND. The PM calls LOC or GLIDESLOPE at half a dot.",
  ref="FCOM PRO-NOR-SCO P 3/16 FMA",
  quote="‐ All armed modes with their associated color (e.g. blue, magenta): \"G/S blue\", \"LOC blue\" ‐ All active modes without their associated color (e.g. green, white): \"NAV\", \"ALT\". The PM should check and respond, \"CHECKED\" to all FMA changes called out by the PF.",
  note="Above 5000 ft AGL the FMA shows CAT 1 regardless; the real capability appears below 5000 ft. Captures engage no sooner than 3 seconds after arming.", src="pro")

A[239] = dict(topic="Descent and Approach", q="What does the FMA show when the approach is armed?",
  a="LOC and G/S in blue in the armed line; capability CAT 1 above 5000 ft, then CAT 2 or CAT 3",
  detail="Pressing APPR arms LOC and G/S, shown in blue in the armed lines of the FMA, and the PF calls G/S blue, LOC blue. Above 5000 ft AGL the FMA displays CAT 1; below 5000 ft it displays the actual approach capability, CAT 2, CAT 3 SINGLE or CAT 3 DUAL, once both APs are engaged.",
  ref="FCOM PRO-NOR-SOP-18-C P 2/32 Initial/Intermediate Approach",
  quote="‐ When APPR mode is selected, AP1 and AP2 should be engaged ‐ Above 5 000 ft AGL, the FMA displays CAT 1 ‐ Below 5 000 ft AGL, the FMA displays the correct approach capability for the intended approach.",
  note="Arm within the normal capture envelope, inside 10 NM and near the glide path angle. A spurious G/S star from a false beam outside it means AP off, APPR off, re-arm inside the zone.", src="pro")

A[240] = dict(kind="walkthrough", topic="Descent and Approach", q="Fly at least one FLS approach",
  a="FLS is the recommended mode for non-precision approaches except RNP AR; select it on PERF APPR and check F-APP capability",
  detail="FLS, the FMS Landing System, flies F-LOC and F-G/S like an ILS for VOR, NDB, LOC-only and RNAV(GNSS) approaches. It is the default and recommended guidance for a non-precision approach inserted in the F-PLN; RNP AR approaches and cases where FLS is unavailable revert to FINAL APP. The limitation requires F-APP or F-APP+RAW capability on the FMA, with the navaid tuned and monitored in the RAW case.",
  ref="FCOM PRO-NOR-SOP-16 P 5/10 PERF APPR page",
  quote="‐ If a non precision approach is inserted in the F-PLN, the default guidance mode is FLS. Check/select the appropriate guidance mode (FLS or FINAL APP). Note: 1. FLS is the recommended guidance mode for the non precision approaches",
  note="Press LS for an FLS approach and check the deviation scales and ident on the PFD. Discontinue if F-APP capability is lost or F-LOC exceeds one dot.", src="pro")

A[241] = dict(topic="Descent and Approach", q="What are the managed approach guidance modes?",
  a="LOC G/S for ILS, FLS (F-LOC F-G/S), FINAL APP, then selected LOC FPA, NAV FPA and TRK FPA",
  detail="The SOP cross-reference table lists guidance by approach type. Fully managed: LOC G/S for ILS and GLS, FLS for LOC-only, VOR, NDB and RNAV(GNSS), and FINAL APP for RNAV(GNSS), VOR, NDB and RNP AR. Selected vertical: LOC FPA or LOC B/C FPA, NAV FPA and TRK FPA where authorized. RNP AR and RNP(VPT) are FINAL APP only.",
  ref="FCOM PRO-NOR-SOP-18-A P 2/6 Cross-Reference Table",
  quote="The FLS (F-LOC F-G/S) is the recommended guidance mode for this type of approach.",
  note="Flying reference: HDG-V/S with the FD bars in managed vertical modes, TRK-FPA with the bird in selected vertical modes.", src="pro")

A[242] = dict(topic="Descent and Approach", q="Which modes may be used for a non-precision approach?",
  a="FLS or FINAL APP managed; FPA guidance selected where the table authorizes it",
  detail="For VOR, VOR-DME, NDB and NDB-DME the table allows FLS, FINAL APP, NAV FPA and TRK FPA. RNAV(GNSS) with LNAV minima allows FLS, FINAL APP and NAV FPA; with LNAV/VNAV minima only FLS or FINAL APP. LOC-only and LOC back course use LOC with F-G/S or FPA. LPV and LP minima use SLS. RNP AR is FINAL APP only.",
  ref="FCOM PRO-NOR-SOP-18-A P 2/6 Cross-Reference Table",
  quote="RNP is equivalent to RNAV(GNSS). RNP(AR) is equivalent to RNAV(RNP).",
  note="If NAV accuracy is LOW at 10 000 ft use TRK FPA for the approach. A TOO STEEP PATH message after the FDP rules out FINAL APP.", src="pro")

A[243] = dict(topic="Descent and Approach", q="Which approaches are flown managed lateral, selected vertical?",
  a="LOC-only, LOC back course, VOR, NDB and RNAV with LNAV minima, using LOC FPA or NAV FPA",
  detail="Managed lateral with selected vertical is LOC FPA, LOC B/C FPA or NAV FPA. The table authorizes it for LOC-only, ILS glide slope out and back course approaches, for VOR, VOR-DME, NDB and NDB-DME, and for RNAV(GNSS) with LNAV minima. It is not authorized for LNAV/VNAV minima, LPV, or RNP AR.",
  ref="FCOM PRO-NOR-SOP-18-A P 3/6 Flying Reference",
  quote="‐ In vertical managed modes: HDG-V/S reference associated with the FD crossbars ‐ In vertical selected modes: TRK-FPA reference associated with FPD.",
  note="FPA needs the bird. Push HDG-V/S to TRK-FPA before the final descent point.", src="pro")

A[245] = dict(topic="Landing and Rollout", q="Is autothrust required for approach and landing?",
  a="Recommended, not required, except CAT III where A/THR must be used",
  detail="The FCTM recommends A/THR for the entire flight and for approaches because of its accurate speed control, with the PF's hand on the levers. It becomes a limitation for CAT III: fail passive and fail operational both require A/THR in selected or managed speed. The QRH severe turbulence procedure also wants A/THR on for the approach.",
  ref="FCOM LIM-AFS-20 P 1/4 ILS Category III Fail Passive (Single)",
  quote="A/THR must be used in selected or managed speed. One autopilot must be engaged in APPR mode, and CAT 3 SINGLE or CAT 3 DUAL must be displayed on the FMA.",
  note="The Before Landing check is A/THR in SPEED mode or off; not in THR mode.", src="fcom")

A[246] = dict(topic="Landing and Rollout", q="What do you weigh before turning autothrust off for the approach?",
  a="Unsatisfactory A/THR performance, loss of autotrim, then disconnect by 1000 ft AAL",
  detail="Use manual thrust if the A/THR performance is unsatisfactory, checked against the ground speed on the ND, or when the autotrim function is lost, to avoid large thrust changes. If you plan manual thrust for landing, disconnect the A/THR at 1000 ft AAL at the latest so the approach is stable through the gate.",
  ref="FCTM PR-NP-SOP-190-CONF P 4/6 Use of A/THR",
  quote="If the A/THR performance is unsatisfactory, the PF should disconnect it and control the thrust manually. If the PF uses manual thrust for landing, the PF should disconnect the A/THR at 1 000 ft AAL at the latest.",
  note="Disconnect with the instinctive pushbutton, not the FCU. A thrust lock after an A/THR failure leaves thrust frozen until you move the levers.", src="fctm")

A[247] = dict(topic="Landing and Rollout", q="Where is the crosswind landing guidance?",
  a="FCTM PR-NP-SOP-250 Landing: de-crab in the flare, wings near level, partial crab up to 5 degrees",
  detail="The FCTM landing chapter gives the technique: rudder to align with the runway in the flare, roll to hold the centerline, and in strong crosswind be ready for small bank into wind. Land with a partial de-crab, up to about 5 degrees of residual crab, rather than excessive bank, to protect the wingtip and nacelle. On the rollout do not hold stick into wind, and be ready to bring reversers to idle if directional control is a problem.",
  ref="FCTM PR-NP-SOP-250 P 4/12 Landing, Crosswind Conditions",
  quote="The aircraft may be landed with a partial de-crab (residual crab angle up to about 5 °) to prevent excessive bank. This technique prevents wingtip (or engine nacelle) strike caused by an excessive bank angle.",
  note="Limits: 32 kt certified crosswind takeoff, 45 kt demonstrated landing, and the wet or contaminated table cuts both. CAT II and III autoland is 15 kt.", src="fctm")

A[248] = dict(topic="Landing and Rollout", q="Is max reverse required on landing?",
  a="REV MAX is standard; REV IDLE is allowed on dry, and on wet with a MEDIUM TO POOR no-credit assessment",
  detail="The selection of REV MAX is the standard practice for landing. On DRY runways the crew may select REV IDLE. On WET runways with GOOD condition REV IDLE is allowed only if the landing distance was assessed at MEDIUM TO POOR with no reverser credit and the result is within the LDA.",
  ref="FCOM PRO-NOR-SOP-16 P 2/10 Landing Performance",
  quote="The selection of REV MAX is the standard practice for landing. However, on DRY runways the flight crew may select REV IDLE.",
  note="HA performance policy gives no credit for reverse thrust, so REV IDLE on a dry runway does not change the numbers.", src="pro")

A[249] = dict(topic="Landing and Rollout", q="When do you stow the reversers?",
  a="Idle reverse at 70 kt, stow at taxi speed before leaving the runway",
  detail="At 70 kt the PM calls SEVENTY KNOTS and the PF brings all reverser levers to idle, because high reverse at low speed can re-ingest exhaust and stall the engine. At taxi speed, before leaving the runway, stow the reversers. Reverse on taxiways ingests sand and debris and recirculates snow into the inlets.",
  ref="FCOM PRO-NOR-SOP-19 P 3/6 At 70 Knots, At Taxi Speed",
  quote="When the aircraft reaches the taxi speed, and before it leaves the runway, stow the reversers.",
  note="Disengage the autobrake with the pedals before 20 kt to avoid brake jerks. High reverse may be held below 70 kt only in an emergency.", src="pro")

A[251] = dict(topic="Landing and Rollout", q="Braking technique with carbon brakes?",
  a="Fewer, firmer applications; wear depends on the number of applications, not pressure or duration",
  detail="Carbon brake wear depends on the number of brake applications and on brake temperature, not on the pressure applied or the duration. The only way to reduce wear is fewer applications: on a straight taxiway accelerate to 30 kt, one smooth application to 10 kt, no riding the brakes.",
  ref="FCTM PR-NP-SOP-100 P 1/8 Carbon Brake Wear",
  quote="Carbon brake wear depends on the number of brake applications and on brake temperature. It does not depend on the applied pressure, or the duration of the braking.",
  note="On landing, autobrake gives one continuous application. If braking manually, one firm application is kinder to carbon than several light ones.", src="fctm")

A[252] = dict(reuse=True, topic="Landing and Rollout",
  a="Factored adds the SAFO 15 percent margin; unfactored is the actual distance with no margin",
  detail="The AeroData landing report gives SAFO Factored Distances with a 15 percent safety margin per SAFO 19001, and Unfactored Distances equal to the actual landing distance without failure and without margin, provided so crews know the real capability in an emergency. FOM 5.6.22.3 sets the A330 model: TALPA, a 7 second air distance, 15 percent on the total distance for max manual and autobrake.",
  ref="FCOM PER-ARD-ALP P 16/18 Landing Data Report",
  quote="The Unfactored Distances are equivalent to the actual landing distances without failure and without a safety margin. Unfactored Distances are provided so that flightcrews can know the actual performance capability of the aircraft in case of emergency conditions.",
  note="Except in an emergency do not land where the SAFO Factored Distance exceeds the LDA; dashes replace a factored distance that does not fit.", src="fcom")

A[253] = dict(topic="Landing and Rollout", q="Key to a bounced landing recovery without a tail strike?",
  a="Hold the pitch attitude; do not increase it; go around from a high bounce",
  detail="Light bounce: maintain the pitch attitude and complete the landing with thrust at idle, and do not let pitch increase, especially after a firm touchdown with a high pitch rate. High bounce: maintain the pitch attitude and go around, without trying to avoid the second touchdown, which will be soft enough if the attitude is held.",
  ref="FCTM PR-NP-SOP-250 P 10/12 Bouncing at Touch Down",
  quote="In case of high bounce, maintain the pitch attitude and initiate a go-around. Do not try to avoid a second touch down during the go-around.",
  note="The tail strike setup is pitching up to soften the second touchdown. Pitch stays where it is.", src="fctm")

A[254] = dict(kind="walkthrough", topic="Landing and Rollout", q="What are the after landing procedures?",
  a="Spoilers disarmed, lights, radar off, start selector NORM, flaps up, TCAS standby, transponder, APU, anti-ice, brake temps, checklist",
  detail="After Landing flow: ground spoilers disarmed once the runway is vacated; land and wing lights off, strobes AUTO, nose light TAXI; WXR and PWS off and both display selectors off; ENG START selector NORM; flaps 0 unless icing or slush, then wait for engine shutdown and a ground crew check; TCAS STBY; transponder per airport; APU as required; engine anti-ice as required; brake temperatures monitored; After Landing checklist once clear of the runway.",
  ref="FCOM PRO-NOR-SOP-21 P 1/4 After Landing",
  quote="GROUND SPOILERS When the runway is vacated: GND SPLRS..............................................................................................DISARM PF",
  note="Brake temperature splits drive maintenance action: more than 150 C between two brakes on a gear with one at or above 600 C or at or below 60 C, 200 C between gear averages, or any brake over 800 C.", src="pro")

A[255] = dict(reuse=True, topic="Taxi and Ground",
  a="FCOM PRO-NOR-SOP-21B for arrival, FCTM PR-NP-SOP-102 and 280 for the considerations",
  detail="FOM 5.3.3 makes single engine taxi the standard procedure when feasible and defers the procedure to the fleet manual. The A330 arrival procedure is FCOM PRO-NOR-SOP-21B One Engine Taxi at Arrival, and the FCTM carries the considerations at PR-NP-SOP-102 for departure and PR-NP-SOP-280 for arrival. The FCTM revision added the departure unit and lets the PM act on the engine master lever.",
  ref="FCOM PRO-NOR-SOP-21B P 1/2 One Engine Taxi at Arrival",
  quote="When taxiing in a straight line: ENG 2 SHUTDOWN...................................................................................... ORDER PF",
  note="Taxi on engine 1 so the blue system keeps the brake accumulator up; on engine 2 check ACCU PRESS. Open the crossbleed for one engine taxi at departure so both packs run.", src="pro")

A[256] = dict(topic="Taxi and Ground", q="Engine cooling requirement before shutdown?",
  a="At or near idle for 1 minute after high thrust operations",
  detail="Operate the engines at or near idle for a cooling period of 1 minute before shutdown to thermally stabilize them. Idle reverse and normal taxi thrust do not count as high thrust, so with idle reverse the clock starts at the flare when the levers are retarded, and with max reverse it starts when the levers come back to idle reverse on the rollout. The PM announces COOLING TIME ELAPSED.",
  ref="FCOM PRO-NOR-SOP-21B P 1/2 One Engine Taxi at Arrival",
  quote="The flight crew should operate the engines at or near idle thrust for a cooling period of 1 min before engine shutdown, in order to thermally stabilize the engines.",
  note="Routine short cooling degrades the engine. The same 1 minute rule applies to both engines at the gate in the Parking SOP.", src="pro")

A[257] = dict(topic="Taxi and Ground", q="What do you weigh before a single engine taxi?",
  a="Systems redundancy, jet blast, fuel imbalance, icing at +1 C or below, active runway crossings, slope, slippery surface, weight",
  detail="One engine taxi is always the crew's decision. Consider the reduced systems redundancy and the aircraft status, the higher thrust needed and the FOD and jet blast risk, fuel imbalance against the takeoff limit, that it is not permitted in icing conditions at OAT +1 C or below, not recommended across an active runway, and that uphill slope, a slippery taxiway or high gross weight may make it impractical. Taxi on engine 1 for the brake accumulator.",
  ref="FCTM PR-NP-SOP-102 P 1/2 One Engine Taxi at Departure",
  quote="‐ One engine taxi is not permitted in icing conditions with OAT at +1 °C (34 °F) or below (due to ice accretion and the required engine acceleration during the ice shedding procedure). ‐ One engine taxi is not recommended in the case of crossing an active runway.",
  note="Green policy is not a mandate. If any of these bite, taxi on two engines and say why.", src="fctm")

A[258] = dict(kind="walkthrough", topic="Taxi and Ground", q="Gate arrival procedures",
  a="Two wing walkers and a marshaller or VDGS operator, correct aircraft type on the VDGS, stop on WAIT or STOP, follow the marshaller over the VDGS",
  detail="For the A330 the required personnel are two wing walkers and one marshaller or VDGS operator, with station exceptions on the 10-7. Under manual marshalling the signals must stay visible to the Captain the whole way. With a VDGS confirm the correct aircraft type before entering the gate area, see the centerline guidance before the nose passes the jet bridge, and stop on WAIT or STOP. If both a marshaller and the VDGS give guidance, follow the marshaller.",
  ref="FOM 5.6.33 Parking Requirements (manual or VDGS)",
  quote="• (787/A330) Two Wing Walkers and One Marshaller/VDGS Operator",
  note="You may stop and ask for wing walkers at any point if clearance is in question. Poor lead-in line visibility at night or in weather justifies requesting manual marshalling.", src="fom")

A[259] = dict(reuse=True, topic="Taxi and Ground",
  note="Also confirm the required personnel are in place, two wing walkers plus the marshaller or VDGS operator for the A330, that the Circle of Safety is clear, and that the 1 minute engine cooling period will be satisfied.")

A[260] = dict(reuse=True, topic="Taxi and Ground",
  detail="FOM 5.6.33 lists one marshaller or VDGS operator and two wing walkers as required personnel for the A330, and under manual procedures requires the marshalling signals to be clearly visible to the Captain at all times. If nobody is marshalling, stop and ask for guidance; the FOM does not name a stop point.")

A[261] = dict(kind="walkthrough", topic="Taxi and Ground", q="Perform or discuss the securing procedure",
  a="Parking flow first, then the Securing the Aircraft checklist: ADIRS off, external power, lights, batteries",
  detail="The Parking SOP runs the shutdown: ACCU pressure, parking brake per brake temperature, anti-ice off, APU bleed, engines off after the 1 minute cool, beacon off when spooled down, fuel pumps off, transponder standby, IRS performance and fuel quantity checks, slides disarmed on the DOOR page, chocks by hand signal, logbook from the STATUS page, then the Parking checklist. Securing the Aircraft follows when the aircraft is left, per the PRO-NOR-SUP-SEC procedure and its checklist.",
  ref="FCOM PRO-NOR-SOP-22 P 6/6 Parking, Logbook",
  quote="STATUS page................................................................................................... CHECK CM1 L2 Press the STS pb (ECAM control panel). L1 LOGBOOK..................................................................................................COMPLETE CM1 L2 Complete the logbook according to the STATUS page.",
  note="If one brake is above 300 C, 150 C with fans, release the parking brake once chocks are in. Wing lights off before the jet bridge comes on; they can heat-damage it.", src="pro")

A[266] = dict(status="desktop", kind="drill", topic="MEL and Maintenance", q="White HAL 46-1333 versus yellow 46-1333b placard?",
  a="", detail="The FOM describes HAL 46-1333 as the Project Operation and Maintenance Information Form placed in the logbook to notify the crew of special installations or engineering modifications, and the APU in-flight start request uses the same form as a placard card. The yellow 46-1333b variant is MEL introduction material, not in the FOM.",
  ref="FOM 12.4.12.7 HAL Project Operation and Maintenance Information Form",
  quote="When required, a Project Operation and Maintenance Information Form (HAL 46-1333) will be placed in the Aircraft Maintenance Logbook (HAL M258) to notify Flight Crew of special installations or engineering modifications that have been accomplished on an aircraft.",
  note=DESK + ". The MEL general section carries the placard color rules.", src="fom")

A[274] = dict(status="desktop", kind="walkthrough", topic="EFB and FD Pro", q="Review the FD Pro Pubs Quick Reference guide in Comply365",
  a="", detail="Vendor guide, not manual text. The FOM sends you into FD Pro Pubs for State Rules and Procedures and the regional Emergency sections, which is what the quick reference walks you through.",
  ref="FOM 5.5.15.4 International Holding Procedures", quote="",
  note=DESK + ". Open the guide in Comply365 before OE.", src="fom")

A[280] = dict(topic="ETOPS", q="How does the release tell you which APU procedure applies?",
  a="ACI on the release plus MIC sheet and placard means the In-Flight Start Program; the verification flight is the ETOPS release logbook entry",
  detail="The routine APU In-Flight Start Program arrives as an Administrative Control Item from MEL section 05, reflected on the Dispatch Release, with an open item on the MIC sheet and the HAL-46-1333 placard card in the logbook. An ETOPS Verification Flight is a repair follow-up: MIC sheet item, verbal notification, the logbook entry AIRCRAFT RELEASED TO ETOPS SERVICE for verification flight, and your verbal acknowledgment with Dispatch.",
  ref="FOM 6.5.6 APU In-Flight Start Program (HA)",
  quote="The Flight Crew will be notified of an APU start request through an open item on the MIC sheet and an aircraft placard card (form HAL-46-1333) in the Aircraft Maintenance Logbook.",
  note="Check for a conflicting MEL first. If an MEL requires the APU to run the whole flight, the MEL wins and there is no in-flight start test.", src="fom")

A[283] = dict(reuse=True, topic="MEL and Maintenance",
  a="Max thrust takeoff, autoland, and APU in-flight start",
  detail="FOM 12.4.12.5: Maintenance may request a max thrust takeoff, and on the 787, A321 and A330 an autoland or an APU in-flight start. Each request is an Administrative Control Item from Section 05 of the fleet MEL, applied to the aircraft and reflected on the Dispatch Release, and the crew follows the ACI procedure in the MEL.",
  ref="FOM 12.4.12.5 Maintenance Requests",
  quote="• (787/A321/A330) Autoland, APU in-flight start",
  note="A completed ACI may still show on a later release that was generated before you finished it.", src="fom")

A[294] = dict(kind="walkthrough", topic="Communications and PA", q="Show where the ACARS functions live",
  a="ACARS MENU: PRE-FLIGHT, IN-FLIGHT and POST-FLIGHT pages, with PERFORMANCE and DELAYS off the main menu",
  detail="The AeroData performance pages hang off the ACARS main menu: MENU PRE-FLIGHT 1/2 then PERFORMANCE for takeoff and landing requests and VIEW DATA, with the same path from IN-FLIGHT and POST-FLIGHT. The PRC ACARS Delay Guide adds that the DELAYS prompt is line select key 4R on the main menu for pre-flight, in-flight or post-flight delays.",
  ref="FCOM PER-ARD-ALP P 12/18 Landing Data - Received Uplinks",
  quote="Page access : MENU PRE-FLIGHT 1/2 → PERFORMANCE → VIEW DATA MENU IN-FLIGHT 1/2 → PERFORMANCE → VIEW DATA MENU POST-FLIGHT 1/2 → PERFORMANCE → VIEW DATA",
  note="ACARS and ATSU traffic normally goes over VHF 3 and switches to SATCOM when VHF 3 is unavailable, so do not use VHF 3 for voice unless 1 and 2 are dead.", src="fcom")

A[295] = dict(topic="Communications and PA", q="Where is a directory of ACARS functions?",
  a="FCOM PER-ARD for the AeroData pages, and the PRC ACARS Delay Guide for delays",
  detail="The AeroData chapter of the FCOM, PER-ARD, documents the ACARS performance pages key by key: the PERFORMANCE page, T/O CONDITIONS, LDG CONDITIONS, RCAM CODE, received uplinks and message display. The PRC ACARS Delay Guide covers the DELAYS pages and the delay codes. There is no single ACARS function directory in the FOM.",
  ref="FCOM PER-ARD-ALP P 1/18 Performance Page",
  quote="Page access : MENU PRE-FLIGHT 1/2 → PERFORMANCE Screen to access all performance related input/output pages, requested takeoff and landing runways, and load takeoff data in the FMS once available.",
  note="A password at 6R is downlinked with every performance request; it is server side, not something you type.", src="fcom")

A[296] = dict(status="desktop", kind="drill", topic="General Operations", q="Where is the spare ACARS paper on the flight deck?",
  a="", detail="The FOM authorizes the crew to replace ACARS printer paper as a consumable and, for HA, wants an Info to Maintenance logbook entry when you do so the spare gets restocked. It does not say where the spare is stowed on the A330.",
  ref="FOM 12.2.6 Consumables Replacement - Flight Deck",
  quote="(HA) If ACARS printer paper is replaced, the Flight Crew should enter an “Info to Maintenance” logbook entry to ensure spare printer paper is restocked.",
  note=DESK, src="fom")

A[297] = dict(status="desktop", kind="drill", topic="General Operations", q="Where are the instructions for changing the ACARS paper?",
  a="", detail="The FOM covers the policy, crew may replace expended consumables, and the HA logbook note, but no loading instructions are in the FOM, FCOM or PRC extracts.",
  ref="FOM 12.2.6 Consumables Replacement - Flight Deck",
  quote="Consumable items such as light bulbs, ACARS printer paper, tissue boxes, and trash bags are provided to the Flight Crew and may be replaced by the Flight Crew when they are expended during normal operations.",
  note=DESK + ". The printer usually carries a loading diagram inside the door.", src="fom")

A[298] = dict(kind="walkthrough", topic="Cruise and Diversion", q="PM: select a new destination in the FMS",
  a="LAT REV at a waypoint, NEW DEST, insert; then runway, approach, weather and landing data",
  detail="As PM you build the diversion: lateral revision at a waypoint other than FROM and TO, new destination into NEW DEST, insert the temporary flight plan, then load the runway and approach, request the weather and the landing performance, and update the fuel prediction. The PRC Diversion Guidance card frames the decision: complete the ECAM or QRH procedure, then weigh the risk of continuing against diverting and coordinate with SOCC.",
  ref="FCOM PRO-NOR-SOP-18-A P 5/6 Approach General",
  quote="Perform a LAT REV at the last waypoint and redefine the destination in the NEW DEST field.",
  note="Failures that require a diversion per the PRC: LAND ASAP, fire, engine failure, insufficient fuel after a component failure, or one generator remaining.", src="pro")

A[299] = dict(kind="walkthrough", topic="Cruise and Diversion", q="PM: demonstrate the backup navigation system",
  a="MCDU MENU, NAV B/UP, with FM source selector in NORM; fly selected modes to the stored F-PLN",
  detail="Select NAV B/UP on the MCDU MENU page with the FM source selector at NORM. The MCDU links to its IRS and shows the memorized F-PLN on the ND with sequencing, bearing and distance to the TO waypoint, and time estimates from IRS ground speed. Use AP or FD selected modes if one FG remains. It can be selected temporarily on one side after a single FM failure to prove it is available on that side.",
  ref="FCOM DSC-22_20-40-20 P 1/10 MCDU Back Up Navigation, General",
  quote="The MCDU NAV B/UP is to be used in case of FM 1 + 2 failure. It can be selected temporarily in case of FM 1 or 2 only failure, in order to ensure that the function is available on the failed side.",
  note="MCDU 3 cannot run back up navigation even when it replaces MCDU 1 or 2.", src="fcom")

A[305] = dict(topic="TCAS and Traffic", q="What is a TA?",
  a="Traffic Advisory: a potential collision threat, TAU about 40 seconds, amber circle and TRAFFIC TRAFFIC",
  detail="TCAS sorts intruders into other, proximate, TA and RA. A Traffic Advisory is a potential collision threat with a TAU, time to closest point of approach, of about 40 seconds. It shows as an amber circle on the ND with the TRAFFIC, TRAFFIC aural, and no vertical order on the PFD.",
  ref="FCOM DSC-34-20-60-10 P 5/10 TCAS Description",
  quote="Traffic Advisory (TA) ‐ Potential collision threat ‐ ND: Intruder position ‐ TAU is about 40 s ‐ Aural messages",
  note="A proximate intruder is within 6 NM and 1200 ft with no threat, shown as a filled white diamond. TCAS sees 30 NM laterally and 9900 ft above and below.", src="fcom")

A[306] = dict(topic="TCAS and Traffic", q="What is an RA?",
  a="Resolution Advisory: a real collision threat, TAU about 25 seconds, red square with vertical orders on the PFD",
  detail="A Resolution Advisory is a real collision threat with a TAU of about 25 seconds. The intruder is a red square on the ND, aural messages sound, and the PFD shows vertical speed orders: maintain the current vertical speed for a preventive advisory, or change it for a corrective advisory. FOM 2.3.17 requires compliance with an RA unless the pilot considers it unsafe.",
  ref="FCOM DSC-34-20-60-10 P 5/10 TCAS Description",
  quote="Resolution Advisory ‐ Real collision threat ‐ ND: Intruder position (RA) ‐ TAU is about 25 s ‐ Aural messages ‐ PFD: Vertical orders",
  note="TA mode converts every RA into a TA; the panel says use it for degraded performance such as an engine failure, gear down, or parallel runway approaches where the 10-7 calls for it.", src="fcom")

A[307] = dict(status="desktop", kind="drill", topic="TCAS and Traffic", q="What is a phantom TA?",
  a="", detail="Neither the FOM nor the FCOM uses the term. The FCOM TCAS description does note the display limits behind spurious-looking traffic: only the eight most threatening intruders are shown, an intruder without range is not displayed, and one without bearing appears as digital data at the bottom of the ND.",
  ref="FCOM DSC-34-20-60-20 P 2/8 ND Indications",
  quote="The traffic is displayed in all ROSE modes and ARC mode whatever NM range is selected. Only the eight most threatening intruders are displayed.",
  note=DESK, src="fcom")

A[308] = dict(topic="TCAS and Traffic", q="Where are the TCAS symbols defined?",
  a="FCOM DSC-34-20-60-20 ND Indications: white diamond other, filled diamond proximate, amber circle TA, red square RA",
  detail="The TCAS Controls and Indicators section defines the ND symbols: an empty white diamond for other intruders, a filled white diamond for proximate, an amber circle for a TA with the TRAFFIC TRAFFIC aural, a red square for an RA with PFD vertical orders. Relative altitude in hundreds of feet and a vertical speed arrow above 500 ft/min appear in the intruder's color, and a 2.5 NM white range ring shows on the 10 and 20 NM ranges.",
  ref="FCOM DSC-34-20-60-20 P 3/8 ND Indications",
  quote="RA intruder Indicated by a red square. Associated with vertical orders displayed on the PFD and aural messages.",
  note="TRAFFIC selector: THRT shows others only during a TA or RA within 2700 ft; ALL shows them always; ABV and BLW extend the band to 9900 ft above or below.", src="fcom")

A[316] = dict(topic="Cold Weather and Runway Condition", q="Definition of icing conditions?",
  a="OAT on the ground or TAT in flight at or below 10 C with visible moisture, or ground contamination at or below 10 C",
  detail="Icing conditions exist when the OAT on the ground or after takeoff, or the TAT in flight, is at or below 10 C and visible moisture in any form is present: clouds, fog with visibility 1 sm or less, rain, snow, sleet or ice crystals. They also exist when the OAT on the ground and for takeoff is at or below 10 C and the aircraft operates on surfaces where snow, standing water or slush may be ingested or freeze on the engines, nacelles or probes.",
  ref="FCOM LIM-ICE_RAIN P 1/2 Definition of Icing Conditions",
  quote="Icing conditions exist when the OAT (on ground or after takeoff) or the TAT (in flight) is at or below 10 °C and visible moisture in any form is present (such as clouds, fog with visibility of 1 sm (1 600 m) or less, rain, snow, sleet or ice crystals).",
  note="Severe ice accretion is about 5 mm, 0.2 in, on the airframe. Thin hoarfrost is thin enough to read markings through.", src="fcom")

A[317] = dict(topic="Cold Weather and Runway Condition", q="Where are the aircraft de-ice and anti-ice procedures?",
  a="FCOM PRO-NOR-SUP-ADVWXR, Adverse Weather, with the FODM for the ground deicing rules",
  detail="The A330 supplementary procedures for adverse weather carry the cold weather work: the ground deicing and anti-icing procedure, the pre-takeoff check, the contamination check, engine ice shedding on ground, and the cold soak items. The FCOM refers to the Flight Operations Deicing Manual for the pre-takeoff check and contamination check requirements. The PRC Cold Weather and Deicing cards summarize both.",
  ref="FCOM PRO-NOR-SUP-ADVWXR P 4/24 Pre-Takeoff Check",
  quote="For more information, refer to Flight Operations Deicing Manual (FODM) \"Pre-Takeoff Check Requirements.\"",
  note="The FOM policy layer is chapter 9.3; the airplane steps are in the FCOM supplementary procedures, not the FOM.", src="pro")

A[319] = dict(topic="Cold Weather and Runway Condition", q="When must engine anti-ice be on?",
  a="Whenever icing conditions exist or are anticipated, except in climb and cruise with SAT below -40 C",
  detail="Engine anti-ice must be ON during all ground operations when icing conditions exist or are anticipated, and in flight when icing conditions exist or are anticipated, except during climb and cruise when the SAT is below -40 C. The caution in every phase: turn it on in icing conditions and do not wait to see ice build up.",
  ref="FCOM PRO-NOR-SOP-13 P 1/2 After Takeoff, Anti Ice",
  quote="Engine anti-ice must be set to ON when icing conditions exist or are anticipated, except during climb and cruise when the SAT is below -40 °C (-40 °F).",
  note="On the ground engine anti-ice raises ground idle, so watch taxi speed on wet or slippery surfaces. Descent and approach have no -40 exemption.", src="pro")

A[320] = dict(topic="Cold Weather and Runway Condition", q="When must wing anti-ice be on?",
  a="Whenever there is evidence of ice accretion: the visual indicator, the wipers, or SEVERE ICE DETECTED; may be on earlier to prevent it",
  detail="In icing conditions the crew may turn on wing anti-ice to prevent ice on the wing leading edge, and must turn it on when there is evidence of accretion such as ice on the visual indicator or the wipers or the SEVERE ICE DETECTED alert, to remove the accumulation. On approach it goes OFF for landing unless severe icing.",
  ref="FCOM PRO-NOR-SOP-13 P 1/2 After Takeoff, Anti Ice",
  quote="‐ The flight crew must turn on the wing anti-ice if there is evidence of ice accretion, such as ice on the visual indicator, or on the wipers, or with the SEVERE ICE DETECTED alert. This is to remove any ice accumulation from the wing leading edge.",
  note="ICE NOT DET appears in green if no ice is detected for 130 s after you switch it on. Wing anti-ice inhibits the bleed temperature reduction and can trigger BLEED LO TEMP.", src="pro")

A[322] = dict(reuse=True, topic="Cold Weather and Runway Condition",
  detail="The FOM does not list cold weather steps. It sends you to the fleet books and to the FODM, which carries the deicing procedures, holdover times and the post-deicing check. For the A330 the procedures are in FCOM PRO-NOR-SUP-ADVWXR, Supplementary Procedures, Adverse Weather, summarized on the PRC Cold Weather and Deicing cards.")
