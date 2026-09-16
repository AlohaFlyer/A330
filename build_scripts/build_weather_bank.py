#!/usr/bin/env python3
"""Write data/weather.json, the A330 Weather Requirements bank consumed by weather.html.

Record shape (engine, frozen): {cat, ref, q, a:[html lines], src, tbl?}
  src   = verbatim FOM 125.1 text. Fragments from one passage that the extract prints
          non-contiguously (page breaks, two-column tables) are joined with " ... ";
          verify_weather.py checks every fragment as a literal substring.
  tbl   = list of [label, value, highlight] rows (the engine renders Fleet / Max distance).
Extra fields per the build brief: fleet ("pax"|"both"), srcType ("manual").
Source: src/FOM_125.1.md only. Run verify_weather.py after any edit.
"""
import json, os
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

R = []
def rec(cat, ref, q, a, src, tbl=None, fleet='both'):
    d = {'cat': cat, 'ref': ref, 'q': q, 'a': a, 'src': src, 'fleet': fleet, 'srcType': 'manual'}
    if tbl: d['tbl'] = tbl
    R.append(d)

# ---------------- Takeoff minimums ----------------
rec('Takeoff Minimums', 'FOM 5.4.1.1',
    'Standard takeoff minimums (aircraft with 2 engines or less)?',
    ['<b>1 sm</b> visibility or <b>RVR 5000</b>.'],
    'Defined as 1 sm visibility or RVR 5000 for aircraft having 2 engines or less.')

rec('Takeoff Minimums', 'FOM 5.4.1.2',
    'Published takeoff minimums are higher than 1 sm / RVR 5000 and no special procedure (e.g. RNP departure) is available. May you depart below the published minimums?',
    ['<b>No.</b> Takeoff in weather less than published minimums shall not be made.'],
    'When published takeoff minimums are greater than 1 sm or RVR 5000, and a special procedure (e.g., RNP departure) is not available or prescribed, takeoff in weather less than published minimums shall not be made.')

rec('Takeoff Minimums', 'FOM 5.4.3',
    'At what visibility must the Captain make the takeoff?',
    ['Visibility <b>less than or equal to 1/4 sm or RVR 1600</b>.'],
    'Any time the visibility is less than or equal to 1/4 sm or 1600 RVR, the Captain will make the takeoff.')

rec('Takeoff Minimums', 'FOM 5.4.4',
    'Lowest takeoff RVR authorized for the A330, and the runway equipment it needs?',
    ['<b>RVR 500 (150 m)</b>: TDZ 500, MID 500, Rollout 500, with <b>CL and HIRL</b>.',
     'Below 500 RVR is <b>737/787 only</b> (HGS/HUD takeoff briefing card). No A330 row exists.',
     'At 1200 (350 m) and below, if RVR is reported all 3 control (2 RVR required).'],
    '500 (150 m) CL & HIRL 500 (150 m) 500 (150 m) ... (737/787) <500 ... SEE HGS/HUD TAKEOFF BRIEFING CARD ... If RVR is reported, it controls for the specified runway; otherwise, use prevailing visibility in the absence of RVR.')

# ---------------- Takeoff alternate ----------------
rec('Takeoff Alternate', 'FOM 5.4.2',
    'When is a takeoff alternate required?',
    ['When reported departure weather is <b>below the approach landing minimums for the runway of intended use</b>, excluding any <b>SA CAT I or CAT II/III</b> approaches, or conditions exist that would <b>preclude a return</b>.',
     'Required but not on the release: <b>contact Dispatch before takeoff and amend the release</b>.',
     'Low visibility takeoff table note: when departure conditions reduce to <b>below CAT I landing limits</b>, a takeoff alternate is required (FOM 5.4.4).'],
    'A takeoff alternate is required when the reported weather at the departure airport is below the approach landing minimums for the runway of intended use, excluding any SA CAT I or CAT II/III approaches or conditions that exist that would preclude a return. Should a takeoff alternate be required but is not listed on the Dispatch Release, contact Dispatch prior to takeoff and amend the ... When departure conditions reduce to below CAT I landing limits, a takeoff alternate is required.')

rec('Takeoff Alternate', 'FOM 5.4.2',
    'Maximum distance from the departure airport to a takeoff alternate for the A330?',
    ['<b>370 nm.</b>'],
    'Takeoff alternates must be within the following distance: A321 360 nm A330 370 nm 717 320 nm 737 350 nm 787 393 nm',
    tbl=[['A321', '360 nm', False], ['A330', '370 nm', True], ['717', '320 nm', False], ['737', '350 nm', False], ['787', '393 nm', False]])

rec('Takeoff Alternate', 'FOM 5.4.2',
    'What weather must a takeoff alternate meet?',
    ['The <b>same requirements as the destination alternate</b> (derived alternate minimums, FOM 8.2.2.1).'],
    'Takeoff alternate airport weather must meet the same requirements as the Alternate for Destination Weather (see 8.2.2.1 – Destination Alternate Airport Weather Requirements).')

# ---------------- Destination alternate ----------------
rec('Destination Alternate', 'FOM 8.2.3',
    'Within the contiguous 48 states, or within the Hawaiian Islands: when is no destination alternate required?',
    ['Destination weather at <b>ETA +/- 1 hour</b> at least <b>2000 ft ceiling and 3 sm</b> visibility (the 1-2-3 rule).',
     'Applies within the contiguous 48, into the contiguous 48 from Alaska / Mexico / Central America / Canada / Caribbean, and <b>within the Hawaiian Islands</b>.'],
    'Within Contiguous 48 States Destination weather reports or forecast or any combination of them indicate at the estimated time of arrival, +/- one ... hour, conditions will be at least 2000 ft ceiling and 3 sm ... visibility. ... Or Within the Hawaiian Islands')

rec('Destination Alternate', 'FOM 8.2.3',
    'Flag operation excluding A012 (e.g. Hawaii to the mainland): no-alternate ceiling and visibility?',
    ['<b>Ceiling</b>, ETA +/- 1 hour: straight-in available, at least <b>1500 ft above the lowest published IAP minimum or 2000 ft above airport elevation, whichever is higher</b>; circling required, <b>1500 ft above the lowest circling MDA</b>.',
     '<b>Visibility: 3 sm or 2 sm more than the applicable minimum, whichever is greater</b>.'],
    'For flag operations, no alternate is required for dispatch if ... for the period from one hour before the flight’s ETA at the destination until one hour after the ETA and the following requirements are met (14 CFR 121.621 [a]): • Ceiling at or above either of the following: – If a circling approach is required, 1500 ft above the lowest circling MDA. – If a straight-in approach is available, at least 1500 ft above the lowest published instrument approach minimum or 2000 ft above airport elevation, whichever is higher. • Three miles visibility or two miles more than the applicable visibility minimum, whichever is greater, for the instrument approach procedure to be used.')

rec('Destination Alternate', 'FOM 8.2.3',
    'Flag flight planned at more than 6 hours, or a planned redispatch to/from Hawaii. Alternate?',
    ['<b>Flag flight planned more than 6 hours</b> flight time on the Flight Plan: an alternate <b>must be listed</b> regardless of forecast.',
     '<b>Planned redispatch to/from Hawaii</b>: must depart with an alternate for the intended destination (FOM 8.5.9).'],
    'Note: For flag operations, an alternate airport for the destination must be listed in the Dispatch Release if the flight is planned for more than 6 hours flight time as calculated on the Flight Plan. Note: For planned redispatch flights to/from Hawaii, flights must depart with an alternate for the intended destination.')

rec('Destination Alternate', 'FOM 8.2.3',
    'Which forecast items require an alternate on the release regardless of ceiling and visibility?',
    ['<b>Thunderstorms or volcanic ash</b> forecast in the TAF at the ETA.',
     'A Dispatcher may add an alternate for other considerations.'],
    'An alternate airport must be listed on the release prior to dispatch when thunderstorms or volcanic ash are forecast in the TAF at the ETA. A Dispatcher may decide an alternate should be added due to other considerations.')

rec('Destination Alternate', 'FOM 8.4.1.4',
    'Extended overwater flag flight, destination forecast below minimums at ETA. Can Dispatch release it?',
    ['<b>Yes, ETOPS flights only</b>: if the destination alternate is forecast at or above <b>derived alternate minimums</b> at the ETA.',
     'Domestic and overland flag flights may not be dispatched unless destination visibility or ceiling (if required) will be at or above minimums at ETA.'],
    'Extended overwater Flag flights may be dispatched or released when required weather forecasts indicate that at the destination, weather may be below minimums at the ETA, as long as weather forecasts indicate the destination alternate weather will be at or above derived alternate minimums at the ETA. Per Alaska Airlines policy, this may only be done on extended overwater flights operated under ETOPS regulations.')

rec('Destination Alternate', 'FOM 8.4.1.4',
    'Forecast wind at the destination exceeds Company limits. Dispatch requirement?',
    ['An <b>alternate must be listed</b> that is forecast to <b>remain within wind limits</b> at the ETA at the alternate.'],
    'If the forecast wind at the destination airport exceeds Company limits (9.2 – Takeoff and Landing Restrictions), an alternate airport must be listed that is forecast to remain within wind limits at the flights ETA at the alternate airport.')

# ---------------- Alternate minimums ----------------
rec('Alternate Minimums', 'FOM 8.2.2.1',
    'Derived alternate minimums, ONE navigational facility (straight-in non-precision, CAT I, or circling). Additives?',
    ['Add <b>400 ft</b> to the MDA(H) or DA(H), and add <b>1 sm (1600 m)</b> to the landing minimum.'],
    'At least one operational navigational facility providing a straight-in non-precision approach procedure, or Add 400 ft to MDA(H) or Add 1 sm or 1600 m to A CAT I precision approach procedure, DA(H), as applicable landing minimum')

rec('Alternate Minimums', 'FOM 8.2.2.1',
    'Derived alternate minimums, TWO facilities to different suitable runways (two approach ends). Additives?',
    ['Add <b>200 ft</b> to the higher DA(H)/MDA(H) of the two, and add <b>1/2 sm (800 m)</b> to the higher authorized landing minimum of the two.'],
    'At least two operational navigational ... Add 200 ft to higher ... Add 1/2 sm or 800 m ... DA(H) or MDA(H) ... to higher authorized ... landing minimum of ... of two approaches used ... two approaches used')

rec('Alternate Minimums', 'FOM 8.2.2.1',
    'Jeppesen "For Filing As Alternate" minimums, additive rounding, and wind at the alternate?',
    ['Jeppesen 10-9/10-9A alternate minimums <b>do not apply</b>; use the derived table.',
     'Additives apply only to the <b>height (H) value, rounded up to the next 100 ft</b>.',
     '<b>Wind including gust</b> must be forecast within operating limits (including reduced visibility limits) and should be within the manufacturer maximum demonstrated crosswind.'],
    'wind including gust must be forecast to be within operating limits, including reduced visibility limits, and should be within the manufacturer’s maximum demonstrated crosswind value. ... Additives are applied only to the height value (H) rounded up to the next 100-ft value (if not a multiple of 100) to determine the required ceiling. ... The minimums depicted in “For Filing As Alternate” listed on the Jeppesen 10-9/10-9A pages do not apply to our operations.')

rec('Alternate Minimums', 'FOM 8.2.2.2',
    'When is a second (marginal weather) alternate required?',
    ['Destination ceiling (if required) <b>and/or</b> visibility <b>at or below CAT I minimums</b> for the intended runway and approach, <b>and</b> the first alternate is <b>at alternate minimums</b> (ceiling <b>or</b> visibility).',
     'Also for a flag or supplemental flight to an <b>international airport missing METAR information</b>; both alternates need a complete METAR and TAF.'],
    'Destination airport weather has a ceiling (if required) AND/OR the visibility is at or below CAT I minimums for the intended runway and approach to be used. • Alternate airport weather is considered marginal when either the ceiling OR visibility is at alternate minimums ... A second alternate is required for a flag or supplemental flight if dispatching to an international airport that is missing information in the Aviation Routine Weather Report (METAR) per Ops Spec A010(e). Both destination alternates must have a complete METAR and TAF.')

rec('Alternate Minimums', 'FOM 8.2.2.3',
    'Exemption 20108 (conditional TAF language): what does it allow, and does it apply to flag operations?',
    ['Domestic dispatch when <b>TEMPO / PROB</b> language says destination and/or first alternate may be below minimums at ETA.',
     'Conditional weather not less than <b>1/2 the lowest visibility minimum</b> at destination, not less than <b>1/2 the alternate ceiling and visibility</b> at the first alternate; a <b>second alternate is always listed</b>.',
     '<b>Not authorized for flag operations</b>, nor for international destinations flown under domestic rules.'],
    'The term “conditional language” refers to the change indicators TEMPO and PROB. ... Second alternate airport – When a flight is dispatched under Exemption 20108, a second alternate airport must always be listed on the Dispatch Release. ... Exemption 20108 is not authorized for flag operations.')

# ---------------- ETOPS ----------------
rec('ETOPS Alternate', 'FOM 6.2.2',
    'Weather required to list an ETOPS alternate on the release, and over what window?',
    ['At or above the <b>Ops Spec C055 alternate minima</b> (derived alternate minimums, FOM 8.2.2) for the <b>earliest to latest possible landing time</b> at that airport.',
     'Field condition reports must indicate a safe landing can be made. Earliest and latest arrival times are printed on the release.'],
    'The Dispatcher will not list an airport as an ETOPS alternate airport on the Dispatch Release unless: • The appropriate weather reports or forecasts, or any combination thereof, indicate that the weather conditions will be at or above the ETOPS alternate airport minima specified in Ops Spec ... C055 (see 8.2.2 – Alternate Weather Requirements – Domestic/Flag) when it might be used (from the earliest to the latest possible landing time). ... • Field condition reports indicate that a safe landing can be made.')

rec('ETOPS Alternate', 'FOM 6.3.5',
    'In flight, what weather must an ETOPS alternate meet before the EEP, and what if it goes below that after the EEP?',
    ['<b>Before the EEP</b>: alternate weather at or above the <b>crew operating minima</b> (less restrictive than the dispatch criteria). If an ETOPS alternate is no longer available, a <b>turnback is required</b>.',
     '<b>After the EEP</b>: turnback <b>not required</b>; establish a new ETOPS alternate with Dispatch. No METAR obtainable for the alternate: a new alternate must be designated.'],
    'Alternates’ weather must be at or above crew’s operating minima (this is the weather required for the operating crew to conduct the approach, given the crew’s minima and any applicable MEL). ... A turnback is required if an ETOPS alternate is no longer available. After the EEP: • A turnback is not required if weather at the ETOPS alternate is below the crew’s operating minima or the runway is unusable.')

# ---------------- Contaminated runway / wind ----------------
rec('Prohibited', 'FOM 9.2.1',
    'Takeoff and landing prohibited: wind, crosswind, braking action, and the A330 contaminated prepared width?',
    ['Steady-state wind <b>greater than 50 kt</b>.',
     'Crosswind exceeding <b>fleet-specific manual limits</b> (A330: FCOM).',
     'Braking action <b>NIL</b> or <b>RWYCC 0</b> on any portion of the runway.',
     'Contaminated runway prepared surface width <b>less than 45 m / 148 ft</b> (A330).'],
    'Takeoffs and landings are prohibited when: • Steady-state wind velocity is greater than 50 kts. • Crosswinds exceed limits in fleet-specific manuals. • Braking action is NIL or the RWYCC is 0 on any portion of the runway. • Contaminated runway preparation results in an available prepared surface width of less than: ... A330 45 m 148 ft')

rec('Prohibited', 'FOM 9.2.1',
    'Takeoff and landing prohibited: thunderstorms, freezing rain, icing?',
    ['<b>TS at or near the airport</b> unless the runway and flight path, including missed approach, are clear of the storms.',
     '<b>Moderate or greater freezing rain</b> (takeoff still allowed with an LWE-derived HOT, absent another prohibiting factor).',
     '<b>Severe icing</b> reported by a similar type or larger aircraft.'],
    'Takeoffs, approaches, and landings should not be attempted when TS are reported at or near the airport unless runway of intended operation and the flight path, including missed approach, are clear of the storms. ... There is moderate or greater freezing rain. ... When the METAR or ATIS reports moderate or greater freezing rain, takeoff is still allowed if an LWE-derived HOT is available, unless another prohibiting factor exists. • Severe icing is reported by a similar type or larger aircraft.')

rec('Prohibited', 'FOM 9.2.1',
    'Takeoff prohibited: contaminant depth and tailwind?',
    ['Contaminant depth <b>greater than 1/2 inch</b> wet snow, slush, or water, or <b>greater than 4 inches</b> dry snow.',
     'Steady-state <b>tailwind over 10 kt</b> on a contaminated runway.'],
    'Takeoffs are prohibited when: • Contaminant depth is greater than 1/2 inch for wet snow, slush, or water or greater than 4 inches for dry snow. • Steady-state tailwind component exceeds 10 kts on a contaminated runway.')

rec('Prohibited', 'FOM 9.2.1',
    'Landing prohibited on a contaminated runway: which conditions?',
    ['Contaminated runway <b>without a PIREP or FICON</b>.',
     '<b>LDA less than 7000 ft and braking action less than GOOD</b>, with any of: <b>tailwind over 5 kt</b>, any <b>inoperative thrust reverser</b>, <b>antiskid inoperative</b>, or <b>compact snow/ice with drizzle or rain</b> of any intensity.',
     'Not recommended (logbook entry and damage inspection if done): water/slush/wet snow over 1/2 inch, dry snow over 4 inches (9.2.1.1).'],
    'A contaminated runway without a braking action report (PIREP) or Field Condition (FICON) NOTAM. – Landing Distance Available (LDA) is less than 7000 ft and braking action less than GOOD, and • Tailwind is greater than 5 kts, or • Any inoperative thrust reverser, or • Antiskid system is inoperative, or • Compact snow/ice with drizzle or rain of any intensity.')

rec('Contaminated Runway', 'FOM 9.1.1.1',
    '(HA) definition of a contaminated runway?',
    ['More than 25% of the runway area in use covered by <b>frost, ice, compact snow, more than 1/8 inch (3 mm) of liquid water, or any depth of slush, dry snow, or wet snow</b>.',
     '(AS) wording differs: more than 1/8 inch of water, slush, dry snow, or wet snow. (HA) treats any depth of slush or snow as contaminated.'],
    'covered by frost, ice, compact snow, or more than 1/8 inch (3 mm) depth of liquid water or any depth of slush, dry snow, or wet snow.')

rec('Contaminated Runway', 'FOM 9.1.6.1',
    'RWYCC range, where the A330 RCAM lives, and FLEX on a contaminated runway?',
    ['RWYCC runs <b>0 (NIL) to 6 (dry)</b>.',
     'A330 RCAM (with runway-condition wind limits): <b>FCOM In-Flight Performance</b>.',
     'Reduced thrust by assumed temperature (<b>FLEX</b>) is <b>not authorized</b> on a contaminated runway.'],
    '(A330) See FCOM – In-Flight Performance ... Runway Condition Code values range from 0 (NIL) to 6 (dry). ... Reduced thrust using assumed temperature, labeled AT or FLEX, is not authorized on a contaminated runway.')

rec('Contaminated Runway', 'FOM 5.6.22.3',
    'A330 in-flight landing distance: what assumptions does the TALPA calculation use?',
    ['<b>7-second air/flare distance</b> from 50 ft over the threshold to touchdown, plus a <b>15% safety margin</b> on total landing distance (air distance included), for both max manual braking and autobrake.'],
    '(717/787/A321/A330) Operational/In-flight landing distance calculations are based on TALPA guidance, using a 7-second air/flare distance (from 50 ft above runway threshold to touchdown). A 15% safety margin is applied to total landing distance, including the air distance, for both maximum manual braking and autobrake configurations.')

# ---------------- Approach / controlling report ----------------
rec('Approach', 'FOM 5.6.11',
    'When may you begin the final approach segment, and what if a below-minimums report arrives after that?',
    ['Only when the latest reported <b>RVR, visibility, or ceiling (if required)</b> is at or above the authorized minimums.',
     'Below-minimums report after the final segment has begun: <b>continue to DA/DH or MDA</b>.',
     'Non-precision and CAT I: <b>TDZ RVR controls</b>; Mid may substitute if TDZ is unavailable. Visibility below <b>1/2 sm</b> is not authorized for approach minimums.'],
    'Do not begin the final approach segment of an instrument approach procedure unless the latest reported RVR, visibility, or ceiling (if required) is at or above the authorized minimums. If a weather report is obtained after the final approach segment of an instrument approach has been initiated, and it indicates below minimum conditions, the pilot may continue the approach to DA/DH or MDA.')

rec('Approach', 'FOM 5.6.17',
    'A330 CAT II / CAT III: crosswind limit, and one-engine-inoperative autoland?',
    ['Crosswind <b>less than the AFM limit or 15 kt, whichever is more restrictive</b>.',
     '<b>One-engine-inoperative CAT II autoland is authorized</b> by Ops Spec; <b>one-engine CAT III autoland is not authorized</b>.',
     'The PIC must be Autoland qualified.'],
    'Landing runway crosswind component less than AFM crosswind limitations or 15 kts, whichever is more restrictive. ... (A321/A330) Ops Spec authorization allows for one-engine inoperative CAT II Autoland. ... (A321/A330) One-engine CAT III Autoland is not authorized.')

rec('Controlling Report', 'FOM 9.2.1',
    'Which weather report is controlling?',
    ['The <b>most recent report</b>, including Remarks or conditional language.',
     'A <b>verbal tower report</b> of visibility, RVV, or RVR takes precedence over METAR or ATIS.'],
    'The controlling visibility for an airport, or if a particular runway is identified, is the most recent report, including Remarks or conditional language. A verbal report from a control tower that includes a visibility value, Runway Visibility (RVV) or Runway Visual Range (RVR), is controlling and will take precedence over a METAR or ATIS.')

# ---------------- A330 specific ----------------
rec('A330 Specific', 'FOM 11.2.9',
    'Decompression polygon: A330 initial descent altitude?',
    ['<b>Always 17,000 ft or FL170</b> (737 and A330). The 787 uses the altitude in the polygon detail drawer.',
     'Never proceed through a charted No Ops Area.'],
    '(737/A330) Initial descent altitude is always 17,000 ft or FL170.')

rec('A330 Specific', 'FOM 5.1.3',
    'Narrow runway: definition, and is the A330 allowed?',
    ['Nominal paved width <b>less than 100 ft (30 m)</b>.',
     '<b>Not authorized</b> for A330 takeoff or landing (717/787/A321/A330). Only the 737 has narrow-runway restrictions.'],
    'the definition of a narrow runway is when the nominal paved runway width is less than 100 ft (30 m). ... (717/787/A321/A330) Takeoff and landing are not authorized on any narrow runway.')

json.dump(R, open('data/weather.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('data/weather.json', len(R), 'records')
