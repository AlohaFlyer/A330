# Build data/fom_delta.json from the verified FOM delta review
# (a330/data/FOM_DELTA_123.1_to_125.1.md). Quotes are verbatim from that doc.
import json, sys, re

def I(id, sec, topic, summary, before, after, why, source, scope, rev, ref=None, drill=None):
    d = {
        "id": id, "fom_section": sec, "topic": topic,
        "change_summary": summary, "before": before, "after": after,
        "why_it_matters": why, "source": source, "scope": scope, "rev": rev,
        "src": "manual", "fleet": "both", "ref": ref or ("FOM " + sec),
    }
    if drill: d["drill"] = drill
    return d

NEW = "(none; no corresponding text in Rev 123.1)"

items = [

I("fd-01","2.2.2.1","Operational Control Window, D-180 trigger",
 "The D-180 OCW trigger is no longer a named-route list; it now follows the release-timing list in 8.5.2.1.",
 '''For South Korea and Amazon cargo flights, the OCW starts three hours (D-180).''',
 '''For flights which require the Dispatch Release and ATS Flight Plan to be produced 180 minutes prior to scheduled departure, the OCW starts three hours (D-180), see 8.5.2.1 – Dispatch Release – Preparation.''',
 "The release-timing list in 8.5.2.1 now includes (787/A330) Europe Departures: 180 minutes. If the A330 flies Europe, operational control starts at D-180 on those legs.",
 "both","fleet-common","Rev 125"),

I("fd-02","2.5.1.4","EFB, new 80% battery rule at start of duty",
 "New bullet: minimum EFB battery charge to begin a flight duty day or training event is 80%. The existing 20%-for-departure bullet remains.",
 NEW,
 '''• To begin a flight duty day or training event, the minimum EFB battery charge status required is 80%, unless the pilot carries an external backup battery of sufficient capacity and charge.''',
 "New hard number for showing up to work or to the sim. Not in any highlights.",
 "diff","fleet-common","Rev 124.2",None,
 {"q":"Minimum EFB battery to start a duty day? To depart?",
  "a":"80% to begin a flight duty day or training event (unless carrying an external backup battery of sufficient capacity and charge); 20% minimum for a departure. (FOM 2.5.1.4)"}),

I("fd-03","2.6.3","Alcoholic beverages, jumpseat and containers",
 "A jumpseat boarding pass now carries an explicit no-alcohol-on-board rule; the container rule drops the government-sealed qualifier; a Company-event exception was added.",
 '''• Any individual traveling with a jumpseat ticket (even if they occupy a seat in the cabin) shall not consume alcohol within 10 hours of the flight.
• Government sealed containers such as those purchased in duty free or out of country stores, are allowed in the main cabin or cargo compartments.''',
 '''• Any individual requesting jumpseat access or issued a jumpseat boarding pass (even if occupying a seat in the cabin) shall not consume alcohol within 10 hours of the flight. If issued a jumpseat boarding pass, alcohol shall not be consumed on board.
Unopened sealed containers are allowed in the main cabin or cargo compartments.
Added: unless at a Company-hosted event, or if alcohol is available for purchase when there is not a specific Company event (such as in the bar area at the Global Training Center building).''',
 "A jumpseat boarding pass now carries an explicit no-alcohol-on-board rule even if seated in the cabin; the government-sealed qualifier on containers is gone.",
 "both","fleet-common","Rev 125"),

I("fd-04","2.6.9.1","Uniform guidelines, HA seasonal coat rule deleted",
 "The HA date-window coat rule for international flying is gone; blazers are simply required on international widebody passenger operations. Gloves and (787)/(A330F) identifiers added.",
 '''• (HA) Uniform coats on international flights (excluding interisland, PPG, and PPT) must be worn Nov. 1 - Mar. 31 (Northern Hemisphere) and May 1 - Sept. 30 (Southern Hemisphere). In an effort to represent our premium brand in the Company's international operations, it is recommended that you wear your blazer throughout the year. However, coats are optional on international flights April 1 - Oct. 31 (Northern Hemisphere) and Oct. 1 - April 30 (Southern Hemisphere).''',
 '''– Blazer – will be worn with appropriate metal wings and sleeve rating stripes reflecting current awarded status regardless of seat position being occupied. Blazers are required on international widebody passenger operations.
– Plain black gloves may be worn with outerwear.
(787) Indicates guidance to be followed when a pilot is operating the 787. / (A330F) Indicates guidance to be followed when a pilot is operating the A330F.''',
 "The date-window coat rule for HA international flying is gone; the blazer is simply required on international widebody passenger operations. Not in highlights.",
 "diff","A330","Rev 124"),

I("fd-05","2.6.15","Traveling with Family While on Duty, new section",
 "New section: working crewmembers may have family non-rev on the same flight, but dependents under 13 need another accompanying adult.",
 NEW,
 '''Working crewmembers may have family non-rev on the same operating flight. Family members must adhere to all non-rev travel rules. Working Flight Crews may not bring dependents under the age of 13 on flights unless another adult accompanies the dependent.''',
 "New restriction; not in highlights.",
 "diff","fleet-common","Rev 124.2"),

I("fd-06","2.8.2","Medical certificates, 'at all times' sentence deleted",
 "The explicit fleet-specific mandate to hold a First Class Medical at all times was deleted; only the general Company policy sentence remains.",
 '''expiration policy. All 737, 787, A321, and A330 Flight Crew, including those serving as Second-in-Command, must possess a current FAA First Class Medical Certificate at all times.''',
 '''expiration policy.
(followed by an AS-only Long Term Disability provision)''',
 "The FOM still says Company policy is for all pilots to obtain an FAA First Class Medical Certificate, but the explicit fleet-specific must-possess-at-all-times mandate is gone. Highlights describe only the 2.8.2.1 typo fix; this deletion is not mentioned.",
 "diff","A330","Rev 125"),

I("fd-07","5.1.8.2","APU start timing now all fleets",
 "The (737) banner was removed: the 10-minutes-before-pushback APU start now applies to every fleet, including the A330.",
 '''(737) The APU should be started between 5-10 minutes prior to the anticipated pushback, preferably closer to the 5-minute timeline to save fuel, unless it is required for passenger comfort or equipment (PCA or external power) issues.''',
 '''The APU should be started 10 minutes prior to the anticipated pushback, unless it is required for passenger comfort or equipment (PCA or external power) issues.''',
 "The 737 banner was removed; the 10-minute APU start now applies to the A330. Not in highlights.",
 "diff","A330","Rev 124.2",None,
 {"q":"When should the APU be started before pushback?",
  "a":"10 minutes prior to anticipated pushback, unless required earlier for passenger comfort or PCA/external power issues; use PCA rather than APU at the gate. (FOM 5.1.8.2)"}),

I("fd-08","5.1.12","Cabin door operation, fall protection",
 "New fall-protection rule: on the A330 (and 717/787/A321), cabin doors must not be opened any distance without fall protection in place; the 737 gets a 12-inch allowance.",
 '''(reference to 14 CFR § 121.570 only; no fall-protection text)''',
 '''14 CFR § 121.570, Employee Safety and Health Program Manual
(737) Cabin doors must not be opened more than 12 inches without proper fall protection in place prior to door opening.
(717/787/A321/A330) Cabin doors must not be opened any distance without proper fall protection in place prior to door opening.''',
 "On the A330, zero door opening without fall protection when no cabin crew is aboard (ferry, MCF, charter).",
 "both","A330","Rev 125.1",None,
 {"q":"Cabin door opening on the A330 with no cabin crew aboard: how far without fall protection?",
  "a":"Not any distance; proper fall protection must be in place before opening (737 gets 12 inches). (FOM 5.1.12)"}),

I("fd-09","5.1.14","Potable water, no MEL when drained",
 "The Captain's-discretion factors became a list, and a new provision says no MEL is needed when the water must be drained and cannot be refilled.",
 '''at the Captain's discretion, considering appropriate factors (e.g., flight time, passenger load).''',
 '''at the Captain's discretion, considering appropriate factors such as: • Flight time • Passenger load • Availability of bottled water, wipes, and hand sanitizer  In rare conditions, the water may need to be drained and cannot be refilled (e.g., extreme cold temperatures). In these instances, an MEL does not need to be applied to operate without potable water.''',
 "A drained, unrefillable potable water system no longer needs an MEL to operate.",
 "both","fleet-common","Rev 125"),

I("fd-10","5.1.15","Entertainment System (broadband), new section",
 "New section: a broadband outage that does not recover before the end of the flight gets a Maintenance Logbook write-up. The Starlink country-guidance note moved here from 2.5.1.5.1.",
 NEW,
 '''Broadband connectivity may become intermittent and drop offline (all users lose connection) for short periods of time due to reception issues. If the broadband system drops offline and does not automatically reestablish internet connectivity before the end of the flight, it should be written up in the Maintenance Logbook at the completion of the flight.''',
 "New logbook write-up trigger. Not in highlights.",
 "diff","fleet-common","Rev 124"),

I("fd-11","5.1.20","Wake turbulence rewritten; old 5.4.10 table deleted",
 "The weight-class and mileage/minute separation table (old 5.4.10 Wake Turbulence, Takeoff) is gone; new 5.1.20 is judgment-based and adds explicit go-around guidance for wake encounters.",
 '''Controllers are required to apply no less than minimum separation standards for aircraft operating behind a heavy or super aircraft. ... • Super, Airbus A380 and Antonov An-225 • Heavy > 300,000 lbs • Large > 41,000 lbs ≤ 300,000 lbs • Small ≤ 41,000 lbs ... • Large behind Super – 7 miles • Large behind Heavy jet – 5 miles ... Departing aircraft will be provided separation of 3 minutes behind a super, 2 minutes behind a heavy, or the appropriate radar separation. The Captain may request the applicable time interval or greater be applied in lieu of radar separation. This request should be made as soon as practical on ground control and at least before taxiing onto the runway. Takeoff separation intervals may not be reduced or waived.''',
 '''Wake turbulence separation in the NAS is provided by controllers in both the enroute and terminal environments. For enroute, separation requirements are driven by size classification standards based on aircraft weight. However, for the terminal environments, the requirements that ATC applies are highly variable, include many aircraft categories, and will not always be obvious to the flying pilot. • On departure, pilots may request time-based separation in lieu of distance for added safety margin. This request should be made as early as practicable with the ground controller. • A go-around decision should not be made based on distance criteria alone. The crew should adopt a holistic approach and initiate a go-around when a wake turbulence encounter degrades safety margins to an unacceptable degree.''',
 "The weight-class and mileage/minute table is gone from the FOM; the new text is judgment-based and adds explicit go-around guidance for wake encounters. Not in highlights.",
 "diff","fleet-common","Rev 124/124.2","FOM 5.1.20 (replaces 5.4.10)"),

I("fd-12","5.2.4","Passenger boarding, deplaning decision",
 "New guidance: notify the CSA before deplaning begins so the station can prepare.",
 NEW,
 '''If during the boarding process or prior to departure the decision to deplane is made, the CSA should be notified before deplaning begins to give station time to prepare (e.g., open the flight, coordinate installation of tail stand).''',
 "New coordination step before any deplaning decision is executed. Not in highlights.",
 "diff","fleet-common","Rev 124"),

I("fd-13","5.2.15","CPDLC logon policy, Iceland added",
 "New CPDLC logon table row for Iceland.",
 NEW,
 '''Iceland Climbing through FL100 BIRD''',
 "Log on to BIRD climbing through FL100 for Iceland airspace. Not in highlights.",
 "diff","fleet-common","Rev 124.2"),

I("fd-14","5.2.19","Load Closeout / SABLE, FAMS line removed",
 "The Airbus Load Closeout breakout no longer describes a FAMS seat line; items renumber 24-26.",
 '''25 Cabin seat numbers of individuals in the Federal Air Marshal Service (this line will only appear if FAMS individuals are on board). 26 Additional fuel requested by Dispatch/Captain. 27 If a new Load Sheet edition is sent, a section will be added describing the changes. Items 24-27 and any additional supplemental information will only be reported when present.''',
 '''25 Additional fuel requested by Dispatch/Captain. 26 If a new Load Sheet edition is sent, a section will be added describing the changes. Items 24-26 and any additional supplemental information will only be reported when present.''',
 "Do not expect a FAMS seat line on the ACARS Load Closeout.",
 "both","A330","Rev 125"),

I("fd-15","5.2.20","Cabin safety check, IPSB verification",
 "The pre-taxi/pushback cabin safety check adds verification of the Installed Physical Secondary Barrier where installed.",
 '''Walkaround Check is complete.''',
 '''Walkaround Check is complete. If installed, the Installed Physical Secondary Barrier (IPSB) must be verified stowed and latched.''',
 "New IPSB stowed-and-latched verification on equipped aircraft.",
 "both","fleet-common","Rev 125"),

I("fd-16","5.2.23","Wing-walker exceptions by 10-7 (pushback and parking)",
 "Station-specific exceptions to the two-wing-walker requirement can now be denoted in the airport 10-7, for both pushback (5.2.23) and widebody parking (5.6.33).",
 '''All departures involving the use of a Pushback Tug shall require at least two Wing Walkers. / • (787/A330) Two Wing Walkers and One Marshaler/VDGS Operator''',
 '''Station-specific exceptions to the requirement to have two Wing Walkers will be denoted in the airport 10-7. / • (787/A330) Two Wing Walkers and One Marshaller/VDGS Operator  Station-specific exceptions to the requirement to have two Wing Walkers will be denoted in the airport 10-7.''',
 "The two-wing-walker requirement for widebody parking and pushback can now be waived by 10-7; check the 10-7 rather than refusing the push. LES marks both sections revised 8/12/26 but the Revision Highlights do not list them.",
 "diff","A330","Rev 125.1","FOM 5.2.23, 5.6.33"),

I("fd-17","5.3.13.3","Tarmac delay action tables replaced (TDPM Rev 5)",
 "The tarmac-delay action tables were replaced: :120 ACARS content is now a mandatory five-item list, Contact Dispatch replaces Expect guidance, new :210 and :240 rows add the international 4-hour limit, and all report types become Safety Report.",
 ''':60  Update passengers on reason for delay and send ACARS msg with time update was provided.
:120  Expect BTB guidance from Dispatch (unless NOC/SOCC authorizes continuing). ... Send the following ACARS updates (when applicable): • That service was completed by 120 minutes. • The time passengers were updated on return or reason for delay if continuing. • The time the request was made to Tower/Ramp Control for the return and when return commenced. • If aircraft cannot return because, "Advised by ATC return would disrupt airport operations." Post event, both pilots submit Irregularity Report/Pilot Report of Incident within 72 hrs for any delay over 2 hrs.
:180  Tarmac Delay has exceeded regulatory limit. ... Both pilots submit Irregularity Report/Pilot Report of Incident within 72 hrs. (table ended at :180)''',
 ''':60  Update passengers on reason for delay. Send ACARS message to Dispatch with the following: • Time the Jetpack Tarmac Delay clock was started. • Time the passengers were provided with an updated from the Flight Deck.
:120  Contact Dispatch for BTB guidance (unless NOC/SOCC authorizes continuing). ... Send an ACARS to Dispatch including ALL of the following: • Time at which the 120 min. snack/water service was completed. • Time at which passengers were updated by the Flight Deck. • Time at which the flight crew requested a return to gate with ATC. • When return to gate was commenced (if applicable). • If a return to gate is not possible, provide the reason to Dispatch. Post event, both pilots submit a Safety Report within 72 hrs for any delay over 2 hrs.
:180  Domestic Tarmac Delay has exceeded regulatory limit. Both pilots submit a Safety Report within 72 hrs.
:210  Update Passengers on return or reason for delay if continuing and send ACARS msg with time update was provided.
:240  International Tarmac Delay has exceeded regulatory limit. Both pilots submit a Safety Report within 72 hrs.''',
 "Two new time gates (:210, :240) with the international 4-hour limit now on the card; Contact Dispatch (active) replaces Expect guidance (passive) at :120; the :120 ACARS content is now a mandatory five-item list; all report types are now Safety Report. Same structure applies to the Door Open and Arrivals tables.",
 "both","fleet-common","Rev 125.1","FOM 5.3.13.3 to 5.3.13.5",
 {"q":"Tarmac delay, departure, door closed: what are the regulatory limits on the card and what goes in the :120 ACARS?",
  "a":":180 domestic, :240 international; at :120 the ACARS must include all of: time the 120-min snack/water service was completed, time passengers were updated by the Flight Deck, time the crew requested return to gate with ATC, when the return commenced, and the reason if a return is not possible. Both pilots submit a Safety Report within 72 hrs for any delay over 2 hrs. (FOM 5.3.13.3)"}),

I("fd-18","5.4.10","Rejected takeoff, new speed-based return-to-gate rule",
 "New RTO rule keyed to 100 kts (Airbus) / 80 kts (Boeing): above that speed, return to the gate and make a logbook entry regardless of the reason; at or below it, continuing may be possible but a logbook entry may still be required.",
 '''In the event of a rejected takeoff due to a takeoff/configuration warning horn or for any problem that the Flight Crew can correct (e.g., passenger problem, a configuration problem) a subsequent takeoff may be made if the cause of the problem can be determined and corrected. No Maintenance Logbook entry is necessary. In the event of an RTO due to a problem which the Flight Crew cannot correct or a Flight Crew MEL cannot be obtained, the aircraft will return to the ramp and a Maintenance Logbook entry made if applicable. Consider brake temperature limits prior to another takeoff. If Brake Energy limits are of concern, a Maintenance Logbook entry should be completed and include the aircraft weight, reject speed, and type of braking effort used (maximum, normal, etc.).''',
 '''An RTO initiated at no greater than (Airbus) 100 kts/(Boeing) 80 kts for issues that can be corrected do not require a return to the gate but may require a Maintenance Logbook entry. An RTO initiated at greater than (Airbus) 100 kts/(Boeing) 80 kts requires that the flight returns to the gate and a Maintenance Logbook entry be made regardless of the reason for the RTO. Even below (Airbus) 100 kts/(Boeing) 80 kts, consider total brake temperature limits prior to another takeoff. If brake energy limits are of concern, a Maintenance Logbook entry should be completed and include the aircraft weight, reject speed, and type of braking effort used (maximum, normal, etc.). See 5.6.38.1 – Hot Brakes Suspected. See 12.4.6 – Maintenance Logbook – Required Entries for all write-up requirements.''',
 "The old no-logbook-entry-necessary language is gone. Above 100 kts on the A330 you go back to the gate and write it up no matter why you stopped; at or below 100 kts you may continue if the issue is corrected but a logbook entry may still be required. Note the Airbus/Boeing split (100 vs 80). Not in highlights.",
 "diff","A330","Rev 124",None,
 {"q":"You reject at 105 kts on the A330 for a master caution that clears on the runway. What now?",
  "a":"Return to the gate and make a Maintenance Logbook entry regardless of the reason; the threshold is greater than 100 kts (Airbus) / 80 kts (Boeing). At or below 100 kts you may continue if the issue is corrected, but a logbook entry may still be required, and brake energy must be considered. (FOM 5.4.10)"}),

I("fd-19","5.6.6.3","Visual approach monitoring, 'time permitting' removed",
 "Backing up a visual approach with the navaid/FMS is now 'shall'; the 'time permitting' qualifier was deleted.",
 '''When an instrument approach is available to the runway of intended landing, time permitting, pilots must tune, identify, and monitor the appropriate navigational aid and/or program the FMC/FMS as a backup for guidance.''',
 '''When an instrument approach is available to the runway of intended landing, pilots shall tune, identify, and monitor the appropriate navigational aid and/or program the FMC/FMS as a backup for guidance.''',
 "Tuning and monitoring the backup approach aid on a visual is now mandatory, not workload-permitting.",
 "both","fleet-common","Rev 125",None,
 {"q":"Visual approach with an ILS available: is tuning it optional if you are busy?",
  "a":"No. Pilots shall tune, identify, and monitor the appropriate navigational aid and/or program the FMC/FMS as a backup; the time-permitting qualifier was removed. (FOM 5.6.6.3)"}),

I("fd-20","5.6.22.3","Landing performance, A330 now TALPA-described",
 "The fixed 1000-ft touchdown description now applies only to the 737; A330 in-flight landing distance is described as TALPA-based with a 7-second air distance and a 15% margin.",
 '''5.6.22.3, Landing Performance (HA)  All weight and distance values are based on a touchdown 1000 ft past the threshold at VREF plus gust with the autobrake deceleration setting specified in the request maintained to a complete stop on the runway. Manual braking will result in a shorter ground run. Contaminated runway landing data includes an additional 15% stopping distance safety margin.''',
 '''(717/787/A321/A330) Operational/In-flight landing distance calculations are based on TALPA guidance, using a 7-second air/flare distance (from 50 ft above runway threshold to touchdown). A 15% safety margin is applied to total landing distance, including the air distance, for both maximum manual braking and autobrake configurations. The touchdown point is not a fixed distance but rather a calculated value that varies with landing conditions such as aircraft weight, pressure altitude, temperature, approach speed, and wind.''',
 "The 1000-ft fixed touchdown description no longer applies to the A330 in the FOM. The FOM 125.1 text explicitly banners this paragraph (717/787/A321/A330), so it is A330-applicable as written.",
 "both","A330","Rev 125",None,
 {"q":"How is A330 in-flight landing distance computed per the FOM?",
  "a":"TALPA-based, 7-second air/flare distance from 50 ft to touchdown, 15% safety margin applied to total landing distance including air distance for both max manual braking and autobrake; touchdown point is calculated, not fixed. (FOM 5.6.22.3)"}),

I("fd-21","5.6.24","Non-normal landing data, unfactored = minimum acceptable limit, all fleets",
 "The fleet banner excluding the A330 is gone: unfactored non-normal landing data is now the minimum acceptable limit for every fleet.",
 '''(717/737/787) Non-normal landing data DOES NOT contain added safety factors and should be considered the minimum stopping distance.''',
 '''Non-normal landing data does not typically include the safety factor used to calculate normal landing performance but may still be used for abnormals to determine runway suitability. Unfactored data (with no safety buffer) represents actual aircraft performance and must be considered the minimum acceptable limit.''',
 "The A330 (FlySmart) was previously excluded by banner; now the unfactored-equals-minimum-acceptable-limit statement is fleet-common. Not in highlights.",
 "diff","A330","Rev 124.2",None,
 {"q":"How do you treat non-normal (abnormal) landing data?",
  "a":"Unfactored data with no safety buffer represents actual aircraft performance and must be considered the minimum acceptable limit; it may still be used to determine runway suitability. (FOM 5.6.24)"}),

I("fd-22","5.6.31","Hard landing, logbook wording",
 "The hard-landing write-up must now notate 'hard landing' in the defect description; fleet-manual reference demoted to 'additional information'.",
 '''See the fleet-specific manuals for hard landing guidance. If a hard landing is suspected: • Enter a "hard landing" in the Maintenance Logbook.''',
 '''If a hard landing is suspected: • Make a Maintenance Logbook entry, ensuring that in the defect description it is notated that it was a hard landing. ... See fleet-specific manuals for additional hard landing information.''',
 "The required logbook wording moved into the defect description itself.",
 "both","fleet-common","Rev 125.1"),

I("fd-23","5.6.32.2","LAHSO criteria rewritten",
 "LAHSO limitations were rewritten: 'no tailwind' became calm (less than 3 kts), the below-1000-ft-AGL acceptance criterion and the PLASI exclusion were deleted, and a 10-7 max landing weight check and a rejected-landing-procedure minima variant were added.",
 '''LAHSO is authorized only when the following criteria are met: • Weather – Ceiling of no less than 1500 ft and a visibility of no less than 5 sm. – If a Precision Approach Path Indicator (PAPI) or Visual Approach Slope Indicator (VASI) is installed and operational, the weather conditions may be lowered to a ceiling of no less than 1000 ft and a visibility of no less than 3 sm. – Dry, non-contaminated runways, LAHSO on wet runways is prohibited. ... – Windshear has not been reported at the airport within the previous 20 minutes of the LAHSO clearance being issued. – No tailwind. • The cleared runway has visual or electronic vertical guidance. A Pulsed Light Approach Slope Indicator (PLASI) is not acceptable for vertical guidance. • The aircraft does not have an inoperative system or MEL/CDL item requiring a landing weight penalty or affecting the stopping capability of the aircraft (e.g., ground spoilers, brakes, anti-skid, or thrust reversers). • The aircraft has not descended below 1000 ft Above Ground Level (AGL) on final approach to the landing runway. • At night, LAHSO is only authorized on a runway that has a VGSI (PAPI or VASI) CAUTION Night LAHSO may be conducted only where an approved FAA in-pavement lighting configuration is installed.''',
 '''The following limitations and provisions apply to LAHSO: • Prohibited on wet runways. • Not authorized to a runway that does not have visual or electronic vertical guidance. • Weather minima require a prevailing weather condition consisting of: – A ceiling of no less than 1500 ft. – A visibility of no less than 5 sm. – LAHSO weather minima may be lowered to a ceiling of no less than 1000 ft and a visibility of no less than 3 sm where a Precision Approach Path Indicator (PAPI) or Visual Approach Slope Indicator (VASI) is installed and operational. – At locations where a rejected landing procedure is published, the ceiling and visibility minima will be established in local flying directives and published. • Not authorized if windshear has been reported within the previous 20 minutes prior to the LAHSO clearance being issued. • The tailwind on the hold short runway shall be calm (less than 3 kts). • Night LAHSO will be conducted only where an approved FAA lighting configuration for LAHSO is installed. • Additionally, any Max Allowable Landing Weight limitations listed in the 10-7 must be met and the aircraft must not have any performance limiting MEL/CDL items.''',
 "No-tailwind became calm (less than 3 kts); the not-below-1000-ft-AGL acceptance criterion and the PLASI exclusion were deleted; a 10-7 max landing weight check and a rejected-landing-procedure minima variant were added.",
 "both","fleet-common","Rev 125",None,
 [{"q":"What tailwind is acceptable for LAHSO?",
   "a":"The tailwind on the hold-short runway shall be calm, less than 3 kts. LAHSO is also prohibited on wet runways and not authorized without visual or electronic vertical guidance; 10-7 max landing weight must be met with no performance-limiting MEL/CDL. (FOM 5.6.32.2)"},
  {"q":"LAHSO weather minima?",
   "a":"Ceiling 1500 ft and 5 sm; may be lowered to 1000 ft and 3 sm where a PAPI or VASI is installed and operational; not authorized if windshear was reported in the previous 20 minutes. (FOM 5.6.32.2)"}]),

I("fd-24","5.7.3.16","Waypoint transition, next + 1",
 "The two-minute waypoint check now includes the subsequent waypoint (next + 1), not just the upcoming one.",
 '''• Approximately 2 minutes prior to reaching a waypoint, confirm that the subsequent FMC/FMS waypoint agrees with the Flight Plan/ATC clearance.''',
 '''• Approximately 2 minutes prior to reaching a waypoint, confirm that the upcoming waypoint and the subsequent waypoint (next + 1) agrees with the Flight Plan/ATC clearance.''',
 "Oceanic waypoint checks now cover two waypoints ahead. Not in highlights.",
 "diff","A330","Rev 124.2",None,
 {"q":"Two minutes before an oceanic waypoint, what do you confirm?",
  "a":"That the upcoming waypoint and the subsequent waypoint (next + 1) agree with the Flight Plan/ATC clearance. (FOM 5.7.3.16)"}),

I("fd-25","5.7.3.13","Identical avionics waypoint labels, A330 example",
 "The identical-waypoint-labels section was rewritten with an Airbus-specific example, and 7.1.25.1 gained a full ARINC 424 coordinate-format primer.",
 '''5.7.3.13, Identical Avionics Waypoint Labels for Different Points 30 nm/minutes Apart  With some avionics, unnamed significant points entered as geographic coordinates are given a 7-character display label that does not include minutes.''',
 '''5.7.3.13, Identical Avionics Waypoint Labels for Different Coordinates  Some avionics systems allow waypoint coordinates to display in a compressed 5- or 7-character format ... (A321/A330) For example: manually entered or uplinked coordinates for N55°/W020° and N55°30/W020° could both display as "N55W020." (717/737/787) For example: ... could both compress to "60105" ... For further discussion on waypoint formats, see 7.1.25.1 – ARINC 424.''',
 "New A321/A330 example: N55/W020 and N55 30/W020 can both display as N55W020. 7.1.25.1 now carries the ARINC 424 primer (6295N = 62N095W, 60N05 = 60N105W, H6295 = half-degree).",
 "diff","A330","Rev 124.2","FOM 5.7.3.13, 7.1.25.1"),

I("fd-26","5.7.3.18","Oceanic CPDLC position reporting, SELCAL inop",
 "New requirement: if SELCAL is not functioning while on CPDLC, one crewmember must listen to HF continuously.",
 '''No other HF reports need to be made while using CPDLC due to the direct ATC Data Link Communications capability of the system.''',
 '''... capability of the system. If SELCAL is not functioning, one member of the crew must listen to HF continuously.''',
 "A continuous HF watch is now required on CPDLC when SELCAL is inoperative.",
 "both","A330","Rev 125.1",None,
 {"q":"On CPDLC in oceanic airspace your SELCAL is inoperative. What is required?",
  "a":"One crewmember must listen to HF continuously. Also remember SELCAL codes are not unique; verify callsign before responding. (FOM 5.7.3.18, 20.4.3.1)"}),

I("fd-27","6.2.1","Adequate airport and ETOPS alternate definitions re-pointed",
 "Both definitions now key to the single 8.1.3 Authorized Airports table; the HA reference to Ops Spec B342/C070 is gone.",
 '''6.2.1: FAA-approved adequate airports are listed in 8.2.2 – ETOPS Alternates and Adequate Airports.
6.2.2: An ETOPS alternate airport is an adequate airport that is listed in (AS) 8.2.2 – ETOPS Alternates and Adequate Airports (HA) Ops Spec B342 and/or C070 and is designated on the Flight Plan/Dispatch Release ...''',
 '''6.2.1: Any regular, provisional, refueling, or alternate airport may be used as an adequate airport provided it is listed in 8.1.3 – Authorized Airports.
6.2.2: An ETOPS alternate airport is an adequate airport that is listed in 8.1.3 – Authorized Airports and is designated on the Flight Plan/Dispatch Release ...''',
 "The HA reference to Ops Spec B342/C070 is gone; everything now keys to the single 8.1.3 table.",
 "both","A330","Rev 125","FOM 6.2.1, 6.2.2",
 {"q":"What is an 'adequate airport' for ETOPS planning now?",
  "a":"Any airport designated A, F, R, P, or E in the 8.1.3 Authorized Airports table, provided the 6.2.1 criteria are met and it is within the approved area of operations, unless restricted by F&F or Company NOTAM; an ETOPS alternate must be listed in 8.1.3 and designated on the release. (FOM 6.2.1, 6.2.2, 8.1.3)"}),

I("fd-28","7.1.31","Ops call after landing, 10-7 trigger added",
 "A new bullet adds 10-7 guidance to the list of reasons to call Station Operations after landing.",
 '''(bullet not present in the list of reasons to call Station Operations)''',
 '''• Directed by 10-7 guidance.''',
 "The 10-7 can now direct an ops call after landing.",
 "both","fleet-common","Rev 125.1"),

I("fd-29","7.2.2","Safety reporting, one system for all",
 "Intelex (HA) and Report It! (AS) are no longer named; all safety reports go through the single Safety Reporting System. 7.2.3 adds that the Company may request reports for unlisted items, and the quick-reference table changed.",
 '''(AS) Safety reports can be filed in the Report It! program ... (HA) All safety reports, HSAP, and Fatigue Reports can be filed through Intelex on the EFB or Flight Operations website.''',
 '''Safety reports can be filed in the Safety Reporting System, which can be accessed on the EFB app or by a link on the Pilot web page. Safety reports include items such as fatigue, ASAP, other hazards, issues, concerns, occurrences, incidents, irregularities, and accidents.
7.2.3 added: The Company may also request that Flight Crews submit safety reports for items not listed in the table when additional information is needed. Table: Fatigue (CFR) X X became Fatigue (49 CFR 271.60) X X; Incident/accident X became Incident/accident X X.''',
 "Intelex is no longer named for HA; one system for all. UNCLEAR: the added CFR cite reads 49 CFR 271.60 in the extract, which is a rail regulation; this may be an extraction or manual error, quoted as-is.",
 "both","fleet-common","Rev 124 and 125/125.1","FOM 7.2.2, 7.2.3"),

I("fd-30","8.1.3","Authorized Airports, single table with per-fleet codes",
 "The separate authorized/provisional/refueling/alternate/ETOPS airport tables were merged into one table with per-fleet code columns (R/F/P/E/A) and new notes.",
 '''Separate tables: AIRPORTS AUTHORIZED FOR SCHEDULED OPERATIONS (AIRPORTS AIRCRAFT AUTHORIZED, e.g. PHNL HNL 717/7374/787/A321/A330), 8.1.3.2, Provisional Airports, 8.1.3.3, Domestic Operations Outside the 48 Contiguous United States, 8.1.3.4, Refueling Operations, 8.2.1, Alternate Airports, 8.2.2, ETOPS Alternates and Adequate Airports.''',
 '''One table with columns AIRPORTS 717 737 787 A321 A330 and legend R* Regular ... F* Refueling ... P* Provisional ... E* ETOPS Alternate (B342) ... A Alternate ... * May be used as an ETOPS alternate unless restricted by F&F or Company NOTAM. Adequate Airports: Any airport designated in this table as A, F, R, P, or E may be planned as an adequate airport (to define ETOPS entry and exit points) for all Alaska Airlines fleets provided the adequate airport criteria from 6.2.1 – Adequate Airport is met ... Notes added: 9. Not authorized for use as an ETOPS alternate outside scheduled hours of operation. 10. Provisional for KJFK. etc.
Highlights-confirmed rows: CYEG YEG F F F F, and West Palm Beach, FL  President Donald J. Trump Intl KDJT DJT A.''',
 "The old A330-specific alternate and refueling lists (e.g. KATL, PGUM, PKMJ, NIUE) are now codes inside a five-column table. Column alignment is lost in the text extract, so the A330 column could not be verified airport by airport: read the table in the PDF for any airport you care about.",
 "both","A330","Rev 124 through 125.1"),

I("fd-31","8.2.3","No alternate for destination, CONUS visibility clause deleted",
 "The CONUS no-alternate row now ends at plain 2000/3; the or-2-sm-more-than-lowest-applicable test survives only in the Alaska row.",
 '''hour, conditions will be at least 2000 ft ceiling and 3 sm  Within the Contiguous 48 States visibility (or 2 sm more than the lowest applicable visibility  From: minimums, whichever is greater).''',
 '''hour, conditions will be at least 2000 ft ceiling and 3 sm  Within the Contiguous 48 States visibility.''',
 "The domestic no-alternate test is now plain 2000/3; the 2-sm-more-than-lowest-applicable test no longer applies within CONUS. Verified in FOM_125.1.md. Not in highlights.",
 "diff","fleet-common","Rev 125.1"),

I("fd-32","8.3.2.3","Special fuel reserves (B043), Hawaii-only restriction removed",
 "The note limiting B043 to Hawaii-CONUS legs was deleted; the section banner adds the 737 and drops the 717; fuel-summary flags described.",
 '''8.3.2.3, Special Fuel Reserves in International Operations (717/787/A321/A330) ... Note The use of the B043 is only approved for flights between the Hawaiian Islands and the contiguous United States.''',
 '''8.3.2.3, Special Fuel Reserves in International Operations (737/787/A321/A330) ... (787/A321/A330) The B043 Dispatch Release is the same as the international Dispatch Release, except for the 45 minute and 10% fuel quantities listed in the fuel summary. These appear as "10% RSV" and "30@1500" (standard flag) or "45@CRZ" (B043) on the fuel summary.''',
 "Per the FOM text, B043 is no longer limited to HI-CONUS legs. Not in highlights.",
 "diff","A330","Rev 124.2"),

I("fd-33","8.3.9","Landing, preflight analysis broadened",
 "Dispatch's contaminated-runway analysis became a landing performance analysis covering both anticipated and worst acceptable braking action.",
 '''Dispatch shall also perform a contaminated runway analysis when contamination is anticipated at the destination or alternate.''',
 '''Dispatch shall also perform a landing performance analysis when any contamination is anticipated at the destination or alternate. This analysis should cover both the anticipated and worst acceptable braking action for the planned landing weight.''',
 "The preflight analysis must now bracket the braking-action range for the planned landing weight.",
 "both","fleet-common","Rev 125"),

I("fd-34","8.3.10.1","FICON requirements, alternates and after-hours",
 "FICON at an alternate is no longer required merely for expected contamination; contaminated-runway policy (FICON or PIREP to land on a contaminated runway) governs alternates and all-cargo operations instead.",
 '''... at the origin and destination airports at the time of operation. FICON reporting is required at the alternate airport if there is expected contamination. All-Cargo Operations Runway/Airfield maintenance and FICON reporting are not required for all cargo operations except to comply with the policy for contaminated runways. ... After Airport Hours of Operation An applicable FICON or PIREP for landing, or FICON for takeoff, is required with any of the following conditions:''',
 '''... at the origin and destination airports at the time of operation. Alternate Airports and All-Cargo Operations Runway/Airfield maintenance and FICON reporting are not required at the alternate airport or for all-cargo operations except to comply with the policy for contaminated runways. All policies for contaminated runways apply for alternate airports or for all-cargo operations, including that a FICON or PIREP is required to land on any contaminated runway. After Airport Hours of Operation – an applicable FICON or PIREP for landing, or FICON for takeoff, is required for alternate airports or for all-cargo operations with any of the following conditions:''',
 "FICON at an alternate is no longer required merely because contamination is expected; it is required to land on a contaminated runway. Not in highlights.",
 "diff","fleet-common","Rev 124"),

I("fd-35","8.5.2.1","Dispatch release preparation timing",
 "The release-timing list was rebuilt and now includes (787/A330) Europe Departures at 180 minutes.",
 '''• Inter-island – 70 minutes • South Korea departures & Amazon Cargo – 180 minutes • All other flights – 90 minutes''',
 '''A Dispatch Release and ATS Flight Plan will be generated and made available to the Flight Crew 90 minutes prior to the scheduled flight departure time except as noted below: • Interisland Hawaii: 70 minutes • South Korea Departures: 180 minutes • Amazon Cargo: 180 minutes • (787/A330) Europe Departures: 180 minutes''',
 "A330 Europe departures now get the release 180 minutes out, which also drives the D-180 OCW in 2.2.2.1.",
 "both","A330","Rev 125",None,
 {"q":"Dispatch release timing for an A330 Europe departure?",
  "a":"180 minutes prior (also South Korea and Amazon Cargo); 90 minutes standard; 70 minutes interisland Hawaii. The OCW starts at D-180 for those flights. (FOM 8.5.2.1, 2.2.2.1)"}),

I("fd-36","8.5.7.1","International dispatch release legend rebuilt on an A330 example",
 "The HA international release legend was rebuilt around an A330 (ASA802 PHNL-KLAX) example, defining MIN T/O, MIN RLS, the doubled/tripled PTOW adjustment, weight limit codes, and the ETOPS line.",
 '''(figure captions only, Figure 8.5.7.1(1) through (13); no legend text in the extract)''',
 '''1 ASA802 ATC Callsign PHNL-KLAX ... N361HA Tail number ... 3 A330-243-B Aircraft type TRENT-772B Engine type
17 MIN T/O Minimum Takeoff Fuel, the minimum fuel required at the start of the takeoff roll. Sum of the above fuel requirements. MIN T/O is equal to MIN RLS minus planned taxi fuel.
18 MIN RLS Minimum Release Fuel, the minimum fuel required to commence pushback
23 MIN T/O / MIN RLS ADJUSTMENT… Fuel added to MIN TO and MIN RLS fuel when the actual TOW exceeds the PTOW. The amount is doubled when the ATOW is between 1001 and 2000 lbs more than PTOW, and tripled when the ATOW is between 2001 and 3000 lbs more than PTOW. The Flight Plan is still considered valid as long as the ATOW is no more than 3000 lbs greater than the PTOW.
24 WEIGHT LIMIT CODES S – Structural (AFM limits) P – Performance L – Landing (landing limit + trip fuel burn) I – Inserted limit (Dispatch)
ETOPS 60/180 Planned ETOPS Adequate Airport range in minutes/planned maximum diversion time (minutes)''',
 "This is now the reference for reading your own release; the 3000-lb PTOW validity limit and the doubled/tripled adjustment are testable facts. The HA release sample image itself (8.5.7) could not be compared in the text diff.",
 "both","A330","Rev 125.1",None,
 {"q":"Your actual TOW is 2500 lbs above PTOW on an HA international release. Is the flight plan still valid and what happens to MIN T/O?",
  "a":"Valid as long as ATOW is no more than 3000 lbs over PTOW; the MIN T/O / MIN RLS adjustment is doubled between 1001 and 2000 lbs over and tripled between 2001 and 3000 lbs over. (FOM 8.5.7.1)"}),

I("fd-37","9.1.5","SNOWTAM and millimeter conversion, new",
 "New SNOWTAM guidance with a millimeters-to-inches conversion table; 9.1.6 adds the GRF term for RCAM data.",
 NEW,
 '''ICAO airports may also issue "SNOWTAMS" with runway contamination details as shown below. Note that contaminant depth is reported in millimeters, and will need to be converted to inches for AS policy adherence. ... Table 9.1.5(1): Inches and Millimeter Conversion Table 1/8″ 3.175 mm 1/4″ 6.35 mm 1/2″ 12.7 mm 1″ 25.4 mm ...
9.1.6 adds: ICAO airports may report RCAM data using the term GRF - Global Reporting Format.''',
 "SNOWTAM contaminant depths arrive in millimeters and must be converted to inches for policy adherence. Not in highlights.",
 "diff","fleet-common","Rev 124","FOM 9.1.5, 9.1.6"),

I("fd-38","9.7.6.1","Space weather, significant-event definition changed",
 "The significant-event definition adds Solar Radiation S3, drops the 25% probability qualifier, and the source becomes the TWC Solar Activity Forecast.",
 '''Prior to departure, Dispatchers evaluate the NOAA Space Weather Forecast for radio blackout and geomagnetic storm forecasts of substantial space weather events. ... significant space weather events are defined by Alaska Airlines as Radio Blackout R3 or higher, observed or forecasted with a 25% or higher probability, or geomagnetic storms observed with a G4-G5 intensity''',
 '''Prior to departure, Dispatchers evaluate the TWC Solar Activity Forecast forecasts of significant space weather events. ... significant space weather events are defined by Alaska Airlines as Radio Blackout R3 or greater, Solar Radiation S3 or greater, or Geomagnetic storms G4 or greater.''',
 "Solar Radiation S3 is a new trigger; the 25% probability qualifier is gone.",
 "diff","fleet-common","Rev 124.2",None,
 {"q":"What defines a 'significant space weather event' for dispatch remarks?",
  "a":"Radio Blackout R3 or greater, Solar Radiation S3 or greater, or Geomagnetic storm G4 or greater. (FOM 9.7.6.1)"}),

I("fd-39","11.1.10","PED battery containment bags, fleet banners removed",
 "The BCB and PED Fire Containment Bag subsections lost their fleet banners; the bags are now identified by color (Red = BCB, Yellow = PED Fire Containment Bag).",
 '''(before: subsections bannered) Flight Deck (737), Cabin (737), Upon Arrival (737) for the BCB, and Lithium Battery Fire (717/787/A321/A330), Flight Deck (717/787/A321/A330), Cabin (717/787/A321/A330) for the PED Fire Containment Bag.''',
 '''11.1.10.1, PED Lithium Battery Containment Bag (Red Bag) and 11.1.10.2, PED Fire Containment Bag (Yellow Bag) with no fleet banners.''',
 "The FOM no longer tells you which bag is on the A330 by fleet; it is identified by color (Red = BCB, gloves inside, seal Velcro; Yellow = PED Fire Containment Bag). Know which one your aircraft carries.",
 "both","A330","Rev 125.1"),

I("fd-40","11.2.9","Decompression polygon procedures rewritten; regional procedures deleted",
 "The polygon section was rewritten as judgment-framed guidance with detail-drawer procedures; the Alps (23.17), Canadian Rockies (19.3.1.1) and Greenland (22.6) regional procedures were deleted. The A330 initial descent altitude is unchanged at 17,000 ft / FL170.",
 '''If a decompression occurs within any polygon, the region-specific procedure shall be executed in order to comply with passenger oxygen supply requirements. • Alps Mountain Range (Jeppesen FD Pro) – see 23.17 ... • Canadian Rockies Mountain Range (Jeppesen FD Pro) – see 19.3.1.1 ... • Greenland Mountain Range (Jeppesen FD Pro) – see 22.6 ... Note For areas without polygons in Jeppesen FD Pro, use procedures outlined in fleet-specific manuals. (737/A330) Initial descent altitude is 17,000 ft. (787) Each region has an initial descent altitude specific to that region.
Deleted regional text (A330 version): • Descend at VMO/MMO to 17,000 ft. – If structural integrity is in doubt, limit airspeed and avoid high maneuvering loads. • Maintain 17,000 ft until clear of terrain. • Once terrain clearance is assured, continue descent to 10,000 ft and navigate as necessary without reentering any polygon. ... CAUTION Once terrain clearance is assured, no polygon shall be reentered while navigating at less than 17,000 ft.''',
 '''Decompression polygon procedures provide a calculated safe method for descending to 10,000 ft before passenger oxygen supplies are depleted following a rapid decompression over high terrain. ... The PIC is expected and encouraged to exercise sound judgment when applying these procedures. Polygons are located in the IFR High and IFR Low charts in Jeppesen FD Pro ... each polygon has a specific procedure described in the detail drawer, which can be accessed by clicking on the polygon label. For both Exit Towards Fix and To Fix then Route procedures, the distance required to accomplish the initial turn has been accounted for. As such, the originally initiated procedure remains valid even if the turn to the initial fix temporarily takes the aircraft into an adjacent polygon. Do not enter another polygon while navigating at less than the altitude indicated in the polygon detail drawer unless terrain clearance is assured. (737/A330) Initial descent altitude is always 17,000 ft or FL170. (787) Refer to the detail drawer in Jeppesen FD Pro for the initial descent altitude(s) associated with each polygon.''',
 "The A330 floor is unchanged at FL170, but the explicit descend-at-VMO/MMO and maintain-17,000-until-clear steps now live only in the polygon detail drawer / fleet manuals, not in the FOM. The detail-drawer-altitudes language is 787-specific; do not import it to the A330. Chapters 19, 22, 23 no longer carry decompression procedures.",
 "both","A330","Rev 125.1","FOM 11.2.9 (19.3.1.1, 22.6, 23.17 deleted)",
 {"q":"Decompression inside a polygon on the A330: initial altitude, and can you enter the neighboring polygon?",
  "a":"Initial descent altitude is always 17,000 ft / FL170 (the detail-drawer altitude variation is 787-only). The initial turn's distance is built in, so briefly clipping an adjacent polygon during the turn keeps the procedure valid; otherwise do not enter another polygon below the drawer altitude unless terrain clearance is assured. Goal is 10,000 ft before passenger oxygen is depleted. (FOM 11.2.9)"}),

I("fd-41","12.3.1.2","Maintenance engine run at gate, wording",
 "The #1 engine run restriction now keys to the boarding door(s), not specifically the L2 door.",
 '''• (787/A330) #1 engine runs are not permitted with the L2 door open or the jetway extended to the L2 door.''',
 '''• (787/A330) #1 engine runs are not permitted with the boarding door(s) open or the jetway extended to the boarding door(s).''',
 "The restriction follows whichever door is in use for boarding.",
 "diff","A330","Rev 124.2"),

I("fd-42","12.4.1.1","Maintenance Status Placard (MSP-1) removal",
 "Maintenance may now remove a yellow-side MSP-1, not only the Flight Crew.",
 '''An MSP-1 on the yellow side can only be removed by the Flight Crew after they verify with Maintenance and confirm a clean logbook is on board the aircraft.''',
 '''An MSP-1 on the yellow side can be removed by Maintenance or by the Flight Crew after they verify with Maintenance and confirm a clean logbook is on board the aircraft.''',
 "Removal authority broadened to Maintenance. Not in highlights.",
 "diff","fleet-common","Rev 124"),

I("fd-43","12.4.2","Logbook corrections, HA Employee ID",
 "Logbook correction bullets now accept (HA) Employee ID alongside (AS) PeopleSoft number.",
 '''PeopleSoft number''',
 '''(AS) PeopleSoft number or (HA) Employee ID''',
 "Applies in both the minor-error and void-entry bullets.",
 "diff","A330","Rev 124"),

I("fd-44","14.1.22","A330 eNOTOC legend, radioactive wording",
 "The statement that radioactive material is prohibited on HA was removed from the A330 eNOTOC legend.",
 '''• B. For transport index this unit is associated with the carriage of radioactive substances (prohibited on HA) – not used. 18. RRR CAT – Radioactive category I, II, or III. Not used as radioactive substances are prohibited for carriage on HA.''',
 '''• B. For transport index this unit is associated with the carriage of radioactive substances. 18. RRR CAT – Radioactive category I, II, or III.''',
 "UNCLEAR whether this reflects an acceptance-policy change or legend cleanup; the fleet-common 14.1 acceptance table in 125.1 allows radioactive products on passenger aircraft for research, medical diagnosis, or treatment. Confirm against the HAZMAT manual before assuming the prohibition still exists.",
 "diff","A330","Rev 125.1"),

I("fd-45","15.2.6","Secure Flight Deck and IPSB door procedures",
 "Secure Flight Deck is redefined around the IPSB; equipment-key text is no longer 737-only; widebody galley Option 3 is gone; door procedures split into Without IPSB (15.2.6.6) and With IPSB (15.2.6.7).",
 '''15.2.6.2, Aircraft Equipment Keys (737) Flight Attendants carry aircraft equipment keys on their person. The keys cannot open the Flight Deck Door when the door is automatically secured by the keypad controlled device or deadbolt, but can be used to secure the Flight Deck during ground time.
15.2.6.6: – (787/A330) Arrange carts and Cabin Crew in accordance with Options 1, 2, or 3.''',
 '''15.2.6.1 (new): A Secure Flight Deck is achieved by using a combination of a locked Flight Deck Door and, for aircraft so equipped, an Installed Physical Secondary Barrier (IPSB) ... Any time the Flight Deck Door is opened during the Secure Flight Deck period for aircraft with the IPSB installed, the IPSB shall be deployed before the Flight Deck Door is opened.
15.2.6.2: Flight Attendants carry equipment keys on their person to access the locked compartment where the EMK, EEMK, and AED are stored. The keys cannot open the Flight Deck Door.
15.2.6.6: – (787/A330) Arrange carts and Cabin Crew in accordance with Options 1 or 2.''',
 "Option 3 for widebody galley/cart arrangement is gone. Door-opening procedures are now split into Without IPSB (15.2.6.6, which also governs all ground operations) and With IPSB (15.2.6.7, in flight). The A330 has no IPSB in the text, so 15.2.6.6 is your procedure; the (787) video-surveillance identification line does not apply.",
 "both","A330","Rev 125","FOM 15.2.6.1, 15.2.6.2, 15.2.6.6, 15.2.6.7"),

I("fd-46","18.1.10","Disinsection/agriculture spraying, new procedures",
 "New disinsection procedures (replacing 20.9 South Pacific Operations): Airbus packs off during spraying, a spurious-smoke-warning window, 5-minute saturation, boarding door disarmed for the inspector with all other doors armed, and a 56-day residual treatment.",
 '''18.1.10: The Public Health Service of some foreign governments require arriving international aircraft to be sprayed with insecticide before passengers and crew are allowed to disembark. The Cabin Crew are trained on disinfection requirements.
20.9 (deleted): • After blocking in, the FFA will make an announcement ... The air conditioning packs and recirculation fans will be turned off during the disinsection process. • The FFA will disarm the 1L door to allow the Quarantine Inspector to board. ...''',
 '''18.1.10.2 Pre-Departure: If on board while the cabin spraying takes place, pilots shall (Airbus) turn off the air conditioning packs during the disinsection process or (787) ensure the entire aircraft is powered down including disconnected from ground power. WARNING The smoke detectors (cargo compartments, lavatory, and avionics) may detect the aerosol particulate matter during the spraying process and cause spurious smoke or fire alerts during the spraying process. From the start of spraying until the completion of spraying (including 5-minute saturation time), any lavatory or cargo smoke warnings during this period should be treated as spurious. However, if any smoke warnings trigger outside those times, the crew should follow the associated procedure.
18.1.10.3 Post-Arrival: Keep the seat belt sign ON until spraying is complete. The FFA will disarm the boarding door(s) to allow the Quarantine Inspector to board. After boarding, the door will close and be kept in the DISARM position. All other doors shall remain armed. A period of 5 minutes must be observed to allow the saturation of insecticide before any doors or vents can be opened.
18.1.10.1 Residual: treatment that remains active for up to eight weeks (56 days).''',
 "Airbus-specific pack-off instruction, a spurious-smoke-warning window, the 5-minute saturation, and all-other-doors-shall-remain-armed are new and directly relevant to HA A330 South Pacific/Australasia flying. Highlights do not list 18.1.10 or 20.9.",
 "diff","A330","Rev 125","FOM 18.1.10 (replaces 20.9)",
 {"q":"Pre-departure disinsection spraying on the A330: what do you do with the packs, and what about a cargo smoke warning during spraying?",
  "a":"Airbus: turn off the air conditioning packs during spraying. Lavatory or cargo smoke warnings from start of spraying through completion plus the 5-minute saturation time are treated as spurious; outside that window follow the procedure. Post-arrival: seat belt sign ON, boarding door disarmed for the inspector, all other doors remain armed, 5-minute saturation before opening doors or vents. (FOM 18.1.10)"}),

I("fd-47","18.1.19","Fuel conversion and ORCN/ETOPS reference card deleted",
 "18.1.19 Fuel Conversion (pounds/liters) and the 18.1.27 ORCN/ETOPS Reference Card were deleted; 18.1 renumbered.",
 '''18.1.19, Fuel Conversion – Pounds/Liters Fuel is requested in pounds and delivered in liters. One liter = 0.2642 gallons and one gallon = 3.785 liters. Based on a density of 6.7 lbs per gallon, 1 liter = 1.70 lbs. ... and the full 18.1.27, ORCN/ETOPS Reference Card (preflight/enroute checklist including • Report speed changes of ± 0.02 Mach - Report ETA changes of 3 minutes or greater (non-CPDLC), the 11-item HF position report format, WWV/VOLMET frequencies).''',
 '''(both sections absent; 18.1 renumbered 18.1.19 through 18.1.25)''',
 "The one-page oceanic card you may have used for orals is no longer in the FOM. Its contents remain scattered in 5.7 and the FIR cards.",
 "diff","A330","Rev 124.x","FOM 18.1.19, 18.1.27 (deleted)"),

I("fd-48","20.4.3.1","SELCAL codes not unique, new caution",
 "New text warns that SELCAL codes are not unique and a notification may be intended for another aircraft.",
 NEW,
 '''SELCAL codes are not unique. It is possible to receive a SELCAL notification that is intended for another aircraft. When responding to SELCAL notifications, crews should use proper radio phraseology and pay close attention to callsigns to avoid miscommunication.''',
 "Verify callsigns before responding to a SELCAL notification. Not in highlights.",
 "diff","A330","Rev 124"),

I("fd-49","20.7.2","Agriculture clearance form now digital via EFB",
 "The Plant and Animals Declaration Form is now digital, accessed via an EFB icon.",
 '''complete a "Plant and Animals Declaration Form" prior to arrival.''',
 '''complete a digital "Plant and Animals Declaration Form" prior to arrival. The form can be accessed by crewmembers via the icon on their EFB.''',
 "The Hawaii agriculture form moved to the EFB. Not in highlights.",
 "diff","A330","Rev 124.2"),

I("fd-50","22.2.1","GOTA transition area, mid-airspace OEPs and RCL",
 "New GOTA guidance: OEPs in the middle of the airspace require SLOP procedures halfway through, and eastbound flights send an RCL message to Gander Oceanic.",
 NEW,
 '''a unique feature of the GOTA is that it has OEPs in the middle of the airspace which requires SLOP procedures halfway through the transition area. Also, eastbound flights through the GOTA are to send an RCL message to Gander Oceanic.''',
 "NAT-qualified A330 crews pick up SLOP-at-mid-airspace and eastbound RCL requirements in the GOTA.",
 "both","A330","Rev 125","FOM 22.2.1, 22.2.2"),

I("fd-51","22.4","SELCAL check qualified by VHF coverage",
 "The per-OCA SELCAL check is now required only when operating outside of VHF coverage.",
 '''Prior to entering each individual OCA, the crew must perform a SELCAL check on the designated HF frequencies provided in the briefing packet''',
 '''When operating outside of VHF coverage, prior to entering each individual OCA, the crew must perform a SELCAL check on the designated HF frequencies''',
 "No SELCAL check needed for an OCA crossed inside VHF coverage. Not in highlights.",
 "diff","A330","Rev 124.2"),

I("fd-52","22.12.1","Iceland customs, new crew restrictions",
 "New Iceland customs guidance for crews.",
 NEW,
 '''crews are not permitted to bring the following into Iceland: • Alcohol • Tobacco products • Cash over $15,000''',
 "No alcohol, tobacco products, or cash over $15,000 into Iceland.",
 "highlights","A330","Rev 125"),
]

# ---- integrity checks before writing ----
ids = [x["id"] for x in items]
assert len(ids) == len(set(ids)), "duplicate ids"
drills = 0
for x in items:
    for k in ("before","after","ref","fom_section","topic","change_summary","why_it_matters"):
        assert x.get(k), (x["id"], k)
    assert x["source"] in ("highlights","diff","both"), x["id"]
    assert x["scope"] in ("A330","fleet-common"), x["id"]
    d = x.get("drill")
    if d: drills += len(d) if isinstance(d, list) else 1
blob = json.dumps(items, ensure_ascii=False, indent=1)
assert "—" not in blob, "em dash found"
assert "\\u" not in blob, "backslash-u escape found"
assert not any(0xE000 <= ord(c) <= 0xF8FF or 0xF0000 <= ord(c) <= 0x10FFFD for c in blob), "private-use char"
open("/home/claude/a330/repo/data/fom_delta.json","w",encoding="utf-8").write(blob + "\n")
print(f"wrote {len(items)} items, {drills} drill Q&As, {len(blob)} chars")
