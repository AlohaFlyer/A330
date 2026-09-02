# Visual verification: A330P FCOM R17 rendered pages (law pages + environmental envelope)

Date: 2026-09-02. Source: PNGs in Drive `HA - Airbus A330/working/pages`, viewed at full render.
All seven pages were legible; nothing below is marked UNREADABLE. Transcriptions are from the
images only — no gap filled from general Airbus knowledge.

---

## Page-by-page transcription

### p1344 — DSC-27-PLP-TOC P 2/4 (15 MAY 26) — Table of contents
Confirms current section map:
- DSC-27-20-20-20 Alternate Law (ALT 1 / ALT 2)
- DSC-27-20-20-30 Direct Law (General; Reconfiguration Control Laws - PFD Display)
- DSC-27-20-20-40 **Abnormal Attitude Laws** (General)
- DSC-27-20-20-50 **Mechanical Back Up** (General / Pitch / Lateral)
- DSC-27-20-30 Controls and Indicators (Pedestal, Lateral Consoles, Glareshield, Overhead Panel, Side Stick Indications on PFD, ECAM F/CTL Page, Memo Display)

### p1394 — DSC-27-20-10 P 2/4 (23 JAN 26) — Reconfiguration laws, footnotes + indications
- Footnote (4): "Bank angle limitation remains effective in ALT 1, which uses roll normal. However, since ALT 1 is generally an unprotected law, all protection marks on the PFD are in amber for simplicity."
- Footnote (5): "When both elevators have failed, only pitch mechanical backup is available, by using the manual pitch trim (THS). 'MAN PITCH TRIM ONLY' is displayed in red on the PFDs."
- Note 1: dual RA failure — flare law introduced when landing gear extended and both APs disengaged; the specific normal-law pitch-down effect at 50 ft no longer applies.
- Note 2: a jerk may be felt in case of flight control computers reconfiguration (hydraulic failure, computer failure, electrical transient...).
- INDICATIONS ON THE ECAM:
  - In ALTN Law: `FLT CTL ALTN LAW (PROT LOST)` / A330: `MAX SPEED 330 kt/M 0.82`
  - In Direct Law: `FLT CTL DIRECT LAW (PROT LOST)` / A330: `MAX SPEED 330 kt/M 0.80` / `MAN PITCH TRIM USE`
- INDICATIONS ON THE PFD: protections lost → amber crosses (X) instead of green (=); auto pitch trim lost → amber "USE MAN PITCH TRIM" below the FMA.

### p1403 — DSC-27-20-20-40 P 1/2, Ident. 00000360.0007001 / 27 DEC 23 (page 15 APR 24) — **Abnormal Attitude Laws, GENERAL**
The abnormal attitude law engages when one of the following values is reached:
- **If at least 2 ADCs are valid and consistent: pitch attitude above 50° nose up or below 30° nose down. If not: pitch attitude above 40° nose up or below 20° nose down.**
- **Bank angle is above 125°**
- **Angle of attack is above 40°**
- **Speed is above 440 kt or below 60 kt**
- **Mach is above 0.96 or below 0.1**

When the abnormal attitude law engages:
- The pitch **alternate** law is active
- The roll **direct** law is active
- The yaw **mechanical** law is active
- **Autotrim is not available**; amber `USE MAN PITCH TRIM` displayed on the PFDs, and
- `F/CTL ALTN LAW` is displayed on the ECAM.

When the aircraft returns within the normal flight envelope, the abnormal attitude law disengages and the following conditions remain **for the remainder of the flight**:
- The pitch alternate law is active **with autotrim**
- The roll direct law is active
- The yaw **alternate** law is active
- `F/CTL ALTN LAW` is displayed on the ECAM.

### p1406 — DSC-27-20-20-50 P 2/2, Ident. 00000363.0002001 / 27 DEC 23 (page 09 APR 21) — **Mechanical Back Up, LATERAL**
Full text of section: "The Backup Control Module (BCM) computer provides yaw damping and direct rudder command with pedals. This computer includes its own electrical generator, supplied by the B or Y hydraulic system."
(No "Backup Power System (BPS)" wording on this page; the Mechanical Back Up GENERAL and PITCH pages were not among the rendered set.)

### p1414 — DSC-27-20-30 P 8/16 (23 JAN 26) — Controls and Indicators (PRIM/SEC/TURB DAMP pushbuttons)
- PRIM pb (guarded), controls FCPC. ON provides per computer: normal pitch, normal lateral, MLA, speedbrakes/ground spoilers control logic, pitch alternate, pitch direct, roll direct, yaw alternate, rudder travel, ailerons droop, **abnormal attitude law**, autopilot laws' computation, characteristic speeds computation. OFF: computer not active (reset = OFF then ON). FAULT lt: amber + ECAM caution on failure.
- SEC pb (guarded), controls FCSC. ON provides: pitch direct, roll direct, yaw alternate, rudder trim, rudder travel. Same OFF/FAULT logic; FAULT flashes at end of SEC power-up test.
- TURB DAMP pb on: turbulence damping added to normal-law elevator and yaw damper command.

### p1421 — DSC-27-20-30 P 15/16 (23 JAN 26) — Memo display + NORM CTL
- `NORM CTL` (boxed): "The normal rudder command is lost. **The rudder is then controlled by the Backup Control Module.**"
- Memos: GND SPLRS ARMED (green); SPEED BRK (amber flashing in phases 2-5; green in phase 6, flashing amber after 50 s if an engine above idle; green in phase 7, after 5 s flashes amber + "SPD BRK STILL OUT" ECAM caution regardless of landing configuration); TURB DAMP OFF (green when pb set to OFF).

### p3762 — LIM-AG-OPS P 1/4, Ident. LIM-AG-OPS-ENV-00021654.0013001 / 27 DEC 23 (page 15 MAY 26) — **Environmental envelope**
Chart fully readable (Pressure Altitude vs OAT °C):
- Ceiling: **41,450 ft** between **-78°C and -32°C** (top edge)
- Left edge steps: -78°C at 32,500 ft; -68°C at 25,000 ft; -54°C at 6,000 ft; **-54°C at -2,000 ft** (bottom-left corner)
- Right side: point at **17°C/22°C, 16,600 ft** (kink on the sloping right edge); bottom-right corner **55°C at -2,000/0 ft**
- **TO & LDG band: 12,500 ft down to -2,000 ft** (labeled with yellow arrow), with **-38°C at 12,500 ft** on its left end — so **12,500 ft appears and is the max takeoff/landing pressure altitude**; minimum is -2,000 ft
- ISA reference line drawn diagonally
- Below chart (Ident. 00020116.0001001 / 27 DEC 23): **Minimum TAT ... -53°C**

---

## Resolution of open cross-check rows (`flight_control_laws_CROSSCHECK.md`)

| Row | Topic | Resolution |
|---|---|---|
| 4 | "MAN PITCH TRIM ONLY" PFD message (mech backup) | **CONFIRMED HANDOUT CORRECT** with context nuance: p1394 footnote (5) — displayed in red on the PFDs **when both elevators have failed** (pitch mechanical backup case). |
| 7 | ECAM "none" for Normal/Abn-attitude/Mechanical | **HANDOUT STALE** for abnormal attitude: p1403 — while engaged **and** after recovery, `F/CTL ALTN LAW` is displayed on the ECAM (handout: "none"). Normal/mechanical: no ECAM law line seen on these pages (benign). |
| 46 | Abnormal attitude entry conditions | **HANDOUT STALE** (three deltas). Handout: pitch >50°NU / >30°ND; bank >125°; AOA >30° or <-10°; IAS >440/<60 kt; Mach >0.96 or <0.01. FCOM R17 (p1403): pitch **>50°NU / <30°ND only if ≥2 ADCs valid & consistent, else >40°NU / <20°ND**; bank >125° (match); **AOA >40°** (not 30; **no negative-AOA trigger**); IAS >440/<60 kt (match); Mach >0.96 or **<0.1** (not 0.01). |
| 47 | Laws during/after abnormal attitude recovery | **HANDOUT STALE** on yaw. Handout: "Pitch Alt, Yaw Alt, Roll Dir" during recovery. FCOM: while engaged — pitch alternate, roll direct, **yaw mechanical**, autotrim NOT available (USE MAN PITCH TRIM); after return to normal envelope — pitch alternate **with autotrim**, roll direct, **yaw alternate**, for the remainder of the flight (that latter part matches the handout's "remain in effect" claim). |
| 48 | Mech backup entry = failure of all PRIMs+SECs; controls = pitch trim + rudder | **PARTIALLY CONFIRMED / entry STILL UNVERIFIED.** Controls confirmed: lateral = rudder via BCM (p1406, p1421 NORM CTL); pitch = manual pitch trim (p1394 fn 5; FCTM). **No mention of differential braking on any rendered page.** The entry-condition statement lives on DSC-27-20-20-50 P 1 (GENERAL) / PITCH pages, which were not rendered. |
| 49 | BCM powered by "BPS" driven by Y or B hyd | **CONFIRMED IN SUBSTANCE, NAME STALE/UNSUPPORTED.** p1406: BCM provides yaw damping and direct rudder command with pedals and "includes **its own electrical generator, supplied by the B or Y hydraulic system**". The FCOM page does not use the name "Backup Power System (BPS)". |
| 50 | Mech backup op rec "restore electrical power to PRIMs+SECs" | **STILL UNVERIFIED** — not on any rendered page. |
| 44 | Direct law yaw (manual rudder + yaw damping/turn coordination) | **STILL UNVERIFIED** — Direct Law P 2 was not among the rendered pages. (p1414 SEC functions include "yaw alternate", consistent but not the Direct Law DU text.) |
| 8 | Reconfiguration failure-mapping table | **STILL UNVERIFIED** — the reconfiguration table graphic page was not rendered. |
| 11, 26, 27, 14("25° at low spd") | AP availability, high-AOA AP disengage, speedbrake inhibit, 25° pitch limit | **STILL UNVERIFIED** — outside the rendered set (DSC-22 / other DUs). |

### Environmental envelope answers (task 2)
- Max takeoff/landing pressure altitude: **12,500 ft** (yes, 12,500 ft appears, labeling the top of the TO & LDG band); min **-2,000 ft**.
- Max flight altitude on chart: **41,450 ft** (from -78°C to -32°C).
- Readable corners: (-78°C, 41,450), (-32°C, 41,450), (-78°C, 32,500), (-68°C, 25,000), (-54°C, 6,000), (-54°C, -2,000), (55°C, -2,000), kink (17°C/22°C, 16,600), TO&LDG left end (-38°C, 12,500).
- Minimum TAT: **-53°C**.
