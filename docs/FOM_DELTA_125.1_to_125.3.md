# FOM Delta, Rev 125.1 (8/12/26) to Rev 125.3 (9/15/26)

Method: difflib on whitespace-normalized lines of `src/_old/FOM_125.1.md` against `src/FOM_125.3.md`, page headers and footers stripped, grouped by the FOM section heading in force at each change. 46 groups changed; the five front-matter groups (cover, LES, RCR, RH, TOC) are excluded below. Rev 125.2 (9/4/26) intervened; the FOM prints no separate 125.2 highlights table, only a "Previous Rev 125.2" line folded into the 125.3 table, and the List of Effective Sections carries no 9/4/26 dates.

Tags: A330-relevant (bannered A330 or ETOPS/oceanic content the A330 flies), fleet-common (un-bannered body text every fleet operates to), other-fleet (bannered 737/717/787/A321/A330F only), editorial (wording, cross-reference, renumbering, admin lists).

## 1. Revision Highlights as the FOM prints them

### Rev 125.3, 9/15/26

| Section | Description of Change |
|---|---|
| 2.3.10.1 Cell Phones | Added cross-reference for additional onboard internet information. |
| 2.5.1 EFB Policies | Removed AS bannering, added cross-reference for electronic device use in the Flight Deck, and changed policy requiring 2GB to 10GB of free memory remaining on EFB after downloading non-Company material. |
| 2.5.2.1 Jeppesen FD Pro Failure | Revised to align AS and HA procedures. |
| 2.5.6.8 EFB Troubleshooting and Lost/Stolen Device | Revised to align AS and HA procedures. |
| 2.8.16 Flight Crew Bag Stowage | Removed AS bannering. |
| 2.8.16.1 Deadhead Crewmembers | Removed AS bannering. |
| 2.9 Phone and Email Lists | Updated list |
| 4.3.2.5 Flight Duty Period Extensions | Removed HA Evidence of FDP Extension Concurrence process. |
| 5.1.22.1.4.11 Cabin Jumpseat, Access | Changed Flight Attendant jumpseat to cabin jumpseat throughout the manual to align with FAM. |
| 5.1.24 Fuel Accumulation on Ramp | Added guidance. |
| 5.2.11.2 Affirmation and Signature Methods (HA) | Changed "OPS CTRL MSG" page to "RLS/FIT FOR Duty" page, and removed the limitation of using only numbers for release version and employee number. |
| 5.2.17 Flight Deck Report (717/737/787/A321/A330P) | Revised to clarify that the information on the Flight Deck Report is from the official flight manifest. |
| 5.2.17.1 Passenger Count Verification | Added fleet-specific guidance. |
| 5.2.18 Load Closeout and Acknowledgment (737) | Added JetPack and revised for clarity. |
| 5.2.24.3 Ramp Communications (external air-start-unit or air-start-bottle) | Revised for clarity. |
| 5.2.24.4 Ramp Communications (APU air or (787) GPU) | Revised for clarity. |
| 5.6.33 Parking Requirements (manual or VDGS) | Revised for clarity. |
| 6.2.2 ETOPS Alternate Airport | Removed HA-specific guidance. |
| 6.2.6 Communication Requirements | Removed "HF Frequency Assignments." |
| 8.1.3 Authorized Airports | Previous Rev 125.2: Changed LGB to regular airport for the 737, effective 9/8/26. |
| 8.1.3 Authorized Airports | Previous Rev 125: Changed YEG to refueling airport for the 737 and updated West Palm Beach, FL, airport information. |
| 8.2.2.1.1 Destination Alternate Airport Weather Requirements After Dispatch | Added guidance. |
| 8.5.1.1 Document Retention | Removed jumpseat forms from the list of paper copies in the flight paperwork. |
| 9.1.2.2 Braking Action Reporting Requirements | Added fleet types. |
| 11.2.9 Decompression | Added guidance. |
| 11.2.9.1 Decompression Polygon Procedures (737/787/A330) | Revised section for clarity. |
| 12.1.1.4 Fuel Spills | Replaced content with a cross-reference to Fuel Accumulation on Ramp. |
| 14.1.14 Load Closeout Message (AS) | Revised for clarity. |
| 14.1.14.1 System Failures | Revised for clarity. |
| 16.1.8.2 Part 91 NRFO Flights | Revised for clarity. |
| 16.1.10 Flight Manifest, NRFO | Revised for clarity and to standardize terminology. |
| 25.8 Remote Radio Sites | Added Arcata (ACV) to California. |
| 26 Abbreviations and Acronyms | Added acronyms. |

### Rev 125.2, 9/4/26

No separate table is printed. The only 125.2 item the FOM identifies is the 8.1.3 LGB line above ("Previous Rev 125.2"). The Revision Control Record lists 125.2 dated 9/4/26 with no highlights date.

## 2. Body changes the diff found, with tags

Every 125.3 highlight was confirmed in the body diff. The diff also found the items marked "not in highlights".

### A330-relevant

| Section | What changed (125.1 to 125.3) | In highlights? |
|---|---|---|
| 6.2.2 ETOPS Alternate Airport | The 30-minute firefighting response sentence now reads "Airports listed in 8.1.3 – Authorized Airports meet this requirement." The old split reference "(AS) 8.2.2 ... (HA) Ops Spec B342 and/or C070" is gone. | Yes |
| 6.2.7 HF Frequency Assignments (deleted) | The whole section is gone: the JetPack "HF Frequencies" tab, radio.arinc.net/pacific, the FD Pro path, and the five ARINC VHF frequencies (131.95 HI/SOCAL/NORCAL, 131.8 PNW, 130.4 NORCAL alt, 128.9 SOCAL alt, 129.4 Vancouver/Anchorage). MEL Policy renumbers 6.2.8 to 6.2.7 and One-Engine-Inoperative Cruise Speed renumbers 6.2.9 to 6.2.8. Remaining FOM sources for HF frequencies: 20.4.3 (Jeppesen FD Pro) and 20.4.3.3 (communications boxes on enroute charts). | Partly (listed under 6.2.6 as a removal; the renumbering is not mentioned) |
| 9.1.2.2 Braking Action Reporting Requirements | "The ACARS FLT SUMMARY may be used to report braking action to Dispatch" is now bannered (737/787/A321/A330), was (737) only. | Yes |
| 11.2.9 Decompression / 11.2.9.1 Polygon Procedures | New parent section 11.2.9 Decompression: passenger oxygen is designed to supply oxygen while descending to a safe altitude; crews may use weather, visibility, ATC, grid MORAs and polygon procedures; "Flight Crews should plan to be at 10,000 ft before passenger oxygen supplies are depleted." The polygon procedures move to 11.2.9.1 (figures renumbered 11.2.9.1(1) to (4)); the sentence about weather/visibility/ATC/grid MORAs was removed from the polygon section because it moved up. The (737/A330) 17,000 ft or FL170 initial descent altitude is unchanged. 22.11 Greenland cross-reference now points to 11.2.9.1. | Yes |
| 5.2.17 / 5.2.17.1 Flight Deck Report and Passenger Count Verification | Flight Deck Report information now stated to come "from the official flight manifest"; Total Souls is "the manifested souls on board". Passenger Count Verification splits by fleet: (737) JetPack primary method; (717/787/A321/A330P) the First Officer reads the passenger count and jumpseat numbers from the Load Closeout and the Captain verifies they match the Flight Deck Report provided in JetPack or via alternate means. | Yes |

### Fleet-common

| Section | What changed (125.1 to 125.3) | In highlights? |
|---|---|---|
| 2.5.1 EFB Policies | Free-memory note: "ensure a minimum of 10GB of free memory will remain on the EFB after the download" (was 2GB). AS banner removed from the customization paragraph, which now also cites 2.3.10. | Yes |
| 2.5.2.1 Jeppesen FD Pro Failure | One procedure for AS and HA: "Trip Kit is available via a web clip on the EFB home screen." The HA SharePoint path ("On the Line" then "Jeppesen Trip Kit") is deleted. Offline coverage EJEP03 is now un-bannered. | Yes |
| 2.5.6.8 EFB Troubleshooting | ITS Service Desk (1-877-238-1077) is the single 24/7 EFB support path. The HA block (Hawaiian Airlines IT, EFB Locker loaner, eConnect ticket, forgotpassword.hawaiianair.com, (808) 838-6720) is deleted. | Yes |
| 2.8.16 / 2.8.16.1 Bag Stowage | Gate-check with a claim-at-gate tag (crew bags, and deadhead bags when cabin space is unavailable) now applies to HA as well; AS banner removed. | Yes |
| 4.3.2.5.3 Evidence of FDP Extension Concurrence (HA) | Body deleted (heading remains empty). The HA-only ACARS "AOC OPS CTRL MSG" / "EXTEND FDP" concurrence record is gone. What remains for everyone is 4.3.2.5.1: the agreed extension is documented "via a recorded verbal communication or acknowledgment of an ACARS message specifying the length of the extension." | Yes |
| 5.1.24 Fuel Accumulation on Ramp (new) | Incidental accumulation: less than 5 gallons (smaller than one baggage cart), no injuries, health not threatened; report to Station Ops to coordinate cleanup. Significant accumulation: over 5 gallons, or a fire hazard exists, or injuries/health threatened; the PIC informs Station Ops and/or the Ramp and decides whether to deplane (the "A" F/A or FFA if no pilot is on board). Deplane through a boarding bridge or, if on ground level, on the side opposite the spill. Ground air conditioning unit is terminated; contaminated cabin air means deplane and the whole crew stays off until fumes dissipate. | Yes |
| 12.1.1.4 Fuel Spills | Body replaced by "See 5.1.24 – Fuel Accumulation on Ramp." Note the deplaning wording changed in the move: 125.1 said "on the side of the aircraft opposite the fuel spill"; 125.3 says "through a boarding bridge or, if on ground level, on the side of the aircraft opposite the fuel spill." | Yes |
| 5.2.11.2 Affirmation and Signature Methods (HA) | Primary method now goes "via ACARS on the RLS/FIT FOR DUTY page" (was OPS CTRL MSG page). The note that the page must not be used once airborne now names RLS/FIT FOR DUTY. The numbers-only rule and the "1/8672" example are deleted. | Yes |
| 5.2.24.3 / 5.2.24.4 Ramp Communications | Trigger line renamed "When Engine(s) Started and Ready to Disconnect Electric" (air-start) and "After Engine is Started and Ready to Disconnect Electric" (APU/GPU). Phraseology itself unchanged. | Yes |
| 5.6.33 Parking Requirements | "If at any time both the VDGS and a Marshaller are providing conflicting guidance, follow the Marshaller." (125.1: "providing guidance"). | Yes |
| 8.2.2.1.1 Destination Alternate Airport Weather Requirements After Dispatch (new) | After dispatch the destination alternate must continue to meet the minimums it was dispatched under; if it drops below, Dispatch files a new alternate that does; the alternate may be removed entirely if the destination does not require one; if no alternate meets minimums the flight must divert unless, in the interest of safety, the PIC continues to the destination using emergency authority. | Yes |
| 8.5.1.1 Document Retention | Jumpseat forms removed from the paper-copy example list; no paper retention of jumpseat forms. | Yes |
| 16.1.8.2 Part 91 NRFO Flights | Passengers on Part 91 flights without Flight Attendants are now "restricted to working crewmembers unless authorization for additional passengers (e.g., deadheads, non-revenues, guest riders) is received from the Director of Operations, FODO, or NRFO Management." 125.1 said "restricted to Alaska Air Group employees unless authorization for non-employees". | Yes |
| 16.1.10 Flight Manifest, NRFO | "Guest Rider Request Form" is now the "Part 91 Passenger Request Form" in Comply; all NRFO passengers "including deadheads, non-revenue employees, and guest riders" need a PNR; Flight Crew confirms with CLP that all passengers are on the manifest before takeoff. | Yes |
| 14.1.14 / 14.1.14.1 Load Closeout Message (AS) | "ACARS" dropped: "The number of items on the Load Closeout must be equal to the number of shipments listed on the NOTOC"; "Certain computer system problems can cause the HAZMAT Load Closeout information to be..." Rule unchanged, wording changed (quotes had to be refreshed). | Yes |
| 5.1.22.1.4.1 / 5.1.22.1.4.11 / 8.5.5.2 | "Flight Attendant jumpseat" renamed "cabin jumpseat" (jumpseat authorization list, section title, JSX legend). Terminology only. | Yes |

### Other-fleet

| Section | What changed | In highlights? |
|---|---|---|
| 5.2.18 Load Closeout and Acknowledgment (737) | JetPack added as a Load Closeout delivery method; read-back required only when received by a method other than JetPack or ACARS; acknowledgment "by ACARS or over voice". | Yes |
| 5.2.17.1 (737) block | JetPack Closeout tab "Identification Valid" and "Passenger Count Valid" primary method. | Yes |
| 8.1.3 Authorized Airports, KLGB row | Row changed from "A, E / E / R / A, E" to "R / E / R / A, E" (first column). Highlights say LGB became a regular airport for the 737 effective 9/8/26 (Rev 125.2). A330 column unchanged. | Yes |
| 6.2.7 (old) VHF ARINC frequencies | Deleted with the HF section (see A330-relevant above). | Partly |

### Editorial

| Section | What changed | In highlights? |
|---|---|---|
| 2.3.10.1 Cell Phones | Added "See 2.5.1.5.1 – Onboard Internet for additional information." | Yes |
| 2.9 Phone and Email Lists | Contacts updated: Quick Reference contact now Captain Duncan Wooster (810) 449-1353; LAX Base Chief Pilot line and Captain Hunter Taylor removed (TBD); Heidi Landry replaces Bernie Davis; training records to HAtraining.records@alaskaair.com; HA pilot pay to HA.pilotpay@alaskaair.com; FOTechPubs address lower-cased. | Yes |
| 5.2.11.1 (AS) | "Jetpack" spelled "JetPack". | No |
| 5.2.15 CPDLC Logon Policy | Table header whitespace only; no content change. | No |
| 5.3.13.5 Arrivals | Table date stamp 8/12/26 to 9/15/26 only. | No |
| 6.2.3 ETOPS Area of Operation | Cross-reference renumbered 6.2.9 to 6.2.8. | No |
| 6.2.8 One-Engine-Inoperative Cruise Speed | Table header row "Fleet Driftdown/Cruise Reference Weight (LB) Reference FL" now extracts as text; values unchanged (A330 .82M/290 KIAS, 470,000 lb, FL350). | No |
| 15.3.6.5 Prisoner chart | "U.S." to "US". | No |
| 22.11 Greenland | Cross-reference 11.2.9 to 11.2.9.1. | No |
| 25.8 Remote Radio Sites | Arcata (ACV) 132.0 moved from the Alaska list into California; column letters re-extracted. | Yes |
| 26 Abbreviations | Added "1L" door naming convention (door number then side; interchangeable with L1). | Yes |

## 3. What an A330 pilot must relearn (plain words)

1. EFB free memory rule is 10GB, not 2GB, before you download personal material.
2. FD Pro fails: Trip Kit web clip on the EFB home screen, internet required, import to an approved reader, never reuse a Trip Kit. No more HA SharePoint path.
3. EFB trouble or lost device: ITS Service Desk 1-877-238-1077, for HA too.
4. HA release acceptance and Fit-For-Duty go out on the ACARS RLS/FIT FOR DUTY page (not OPS CTRL MSG) and it must not be used airborne. The numbers-only entry rule is gone. The HA "EXTEND FDP" ACARS concurrence record is gone; the extension is documented by recorded verbal agreement or ACARS acknowledgment.
5. Fuel on the ramp: 5 gallons (one baggage cart) is the line between incidental (call Station Ops for cleanup) and significant (PIC informs Station Ops/Ramp, decides on deplaning). Deplane via the bridge, or on the side opposite the spill if on ground level. Kill the ground air unit.
6. Passenger count verification on the A330P: FO reads the passenger and jumpseat count from the Load Closeout, Captain matches it to the Flight Deck Report (JetPack or alternate means). The Flight Deck Report is the official manifest.
7. Destination alternate after dispatch: it must keep meeting the minimums it was dispatched under; Dispatch swaps it or drops it (if the destination needs none); no legal alternate means divert unless the PIC invokes emergency authority to continue.
8. Braking action worse than good: the A330 may now report it to Dispatch through the ACARS FLT SUMMARY.
9. ETOPS alternate RFFS response: any 8.1.3 Authorized Airport meets the 30-minute requirement. The FOM HF Frequency Assignments section (JetPack tab, radio.arinc.net, ARINC VHF frequencies) is gone; use Jeppesen FD Pro ARINC Services and the enroute chart communication boxes. Renumbering: MEL Policy is 6.2.7, OEI Cruise Speed is 6.2.8.
10. Decompression: 11.2.9 is now the general section (plan to be at 10,000 ft before passenger oxygen runs out; use weather, ATC, grid MORAs and polygons); the polygon procedure is 11.2.9.1. 17,000 ft or FL170 initial descent altitude for the A330 is unchanged.
11. Part 91 ferry with no F/As: only working crewmembers ride unless the DO, FODO or NRFO Management authorizes additional passengers (deadheads, non-revs, guest riders), each on a Part 91 Passenger Request Form and a PNR.
12. VDGS plus Marshaller giving conflicting guidance: the Marshaller wins.

## 4. Records changed per bank

- `data/fom_delta.json`: 18 records appended (fd-53 to fd-70, rev "Rev 125.3"; 5 scope A330, 13 scope fleet-common).
- FOM Quizzer (`build_fom_bank.py`, output `fom_q/*.json`, `data/fom_questions.json`, `data/fom_all.json`): 459 to 474 records. 15 existing records changed (5 quote fixes for text that moved or reworded: fuel spill, Load Closeout NOTOC crosscheck x2, Part 91 NRFO passengers x2; 3 fact changes: fuel spill exits, Part 91 passengers x2; 6 reference renumbers: 6.2.7, 6.2.8, 11.2.9.1 x4; 2 answer/note refreshes: ETOPS alternate RFFS 8.1.3, parking conflicting guidance) and 15 records added (2.5.1, 2.5.2.1, 2.5.6.8, 2.8.16, 4.3.2.5.1, 5.1.24, 5.2.11.2, 5.2.17.1, 5.6.33, 20.4.3 HF, 8.2.2.1.1, 8.5.1.1, 9.1.2.2, 11.2.9, 16.1.10). Manifest `generated` reads "FOM Rev 125.3 (9/15/26)" from manuals.json.
- Weather bank (`build_weather_bank.py`, `data/weather.json`, handout `A330_Weather_Requirements.pdf`): 32 to 34 records. 1 changed (decompression: ref 11.2.9.1, 10,000 ft line added), 2 added (8.2.2.1.1 alternate after dispatch, 9.1.2.2 braking action reporting).
- OE workbook (`data/oe.json`): 8 FOM-sourced records changed. Quote refreshes where only the page break moved: oe-040 (5.2.19), oe-134 (5.5.6.3). Fact changes: oe-159 (HF frequencies re-sourced to 20.4.3 / 20.4.3.3, JetPack tab and radio.arinc.net no longer FOM-citable), oe-027 (destination alternate in flight now governed by 8.2.2.1.1, not the ETOPS crew operating minima). Reference renumbers and note refreshes: oe-272 (11.2.9.1), oe-283 (6.2.8), oe-025 (8.1.3 RFFS note), oe-253 (conflicting guidance).

## 5. Not grounded / gaps

- The FOM no longer states where the JetPack "HF Frequencies" tab or radio.arinc.net/pacific are referenced. OE record oe-159 was re-sourced to FOM 20.4.3 and 20.4.3.3; the JetPack tab and the ARINC web address are no longer FOM-citable.
- FCOM PER-ARD (OE record oe-035, FCOM-owned) still calls the HA ACARS page "OPS CTRL MSG"; FOM 125.3 calls it "RLS/FIT FOR DUTY". Flag for the FCOM owner.
- The 8.1.3 LGB column change is stated as a 737 change in the highlights; the text extract cannot prove which column holds which fleet, so it is tagged other-fleet on the highlights' word.
