# Visual verification pass 2: A330P FCOM R17 rendered pages — closing the open flight-control-law rows

Date: 2026-09-02. Source: PNGs in Drive `HA - Airbus A330/working/pages` (FCOM_R17_p<page>-<page>.png),
rendered coverage: pdf pages 1344, 1345, 1390-1422 (DSC-27). Pages newly viewed at full render this pass:
p1391, p1393, p1401, p1402, p1405. All were legible. Transcriptions are from the images only; no
general-knowledge adjudication. Open rows refer to `/home/claude/a330/data/flight_control_laws_CROSSCHECK.md`;
prior pass: `law_pages_VISUAL.md`.

Page map confirmed this pass: 1391-1392 = DSC-27-20-10-80 (Aircraft Trimming, last Normal Law DU);
1393-1396 = DSC-27-20-20-10 (Reconfiguration general, P1/4-4/4); 1397-1400 = Alternate Law;
1401-1402 = DSC-27-20-20-30 Direct Law P1/2-2/2; 1403-1404 = Abnormal Attitude; 1405-1406 =
DSC-27-20-20-50 Mechanical Back Up P1/2-2/2; 1407-1422 = DSC-27-20-30 Controls & Indicators P1/16-16/16.
Consequence: DSC-27-20-10-20 (protections DU) lies **before p1390** and DSC-27-20-40 (Speedbrakes)
**after p1422** — both proven absent from the rendered range.

---

## New page transcriptions

### p1393 — DSC-27-20-20-10 P 1/4, Ident. 00000324.0001001 / 27 DEC 23 (page 23 JAN 26) — Reconfiguration table (the graphic that never survived text extraction)

Text above figure: "Depending on the type of failures affecting the flight control system, or its
peripherals, there are 3 possible reconfiguration levels: Alternate law (ALT 1 or ALT 2) / Direct law, or / Mechanical."

Figure, transcribed:

| | ALT 1 | ALT 2 | DIRECT |
|---|---|---|---|
| Trigger failures | THS JAM; THS POS.LOST; ONE ELEV FAULT; YAW DAMP ACT.LOST; SLATS or FLAPS POS LOST; SINGLE ADR FAULT (\*) | ALL ENG OUT; DOUBLE IR FAULT; DOUBLE ADR FAULT; ADR DISAGREE; ALL SPLRS FAULT; ALL INR AIL FAULT; PEDALS TRANSD. FAULT | TRIPLE IR FAIL; TRIPLE PRIM FAIL; TWO ELEV FAULT (5); ALL ENG OUT + PRIM 1 INOP |
| PITCH | ALT | ALT | DIR |
| LAT | NORM | ROLL DIR / YAW ALT | ROLL DIR / YAW ALT |
| PROT — LOAD FACTOR | YES | YES | LOST |
| PROT — PITCH ATT | LOST | LOST | LOST |
| PROT — HIGH AOA | ALT (1) | ALT (1) (2) | LOST |
| PROT — HIGH SPD | ALT | ALT (3) | LOST |
| PROT — BANK ANGLE | YES (4) | LOST | LOST |
| PROT — LOW ENERGY | LOST | LOST | LOST |

"**AUTOPILOT LOST**" (top left) has an arrow attached to a boxed cluster of the trigger-failure lists.
Box geometry at 3x zoom: the box(es) enclose THS JAM, THS POS.LOST, ONE ELEV FAULT, YAW DAMP ACT.LOST
(ALT 1 column), the entire ALT 2 list, and the entire DIRECT list. **Outside** the box, below it:
"SLATS or FLAPS POS LOST" and "SINGLE ADR FAULT \*". (Interpretation from geometry only: those two
ALT 1 triggers do not by themselves lose the autopilot; all other listed failures do.)

Footnotes on this page: (\*) "Only in case the AOA, of the remaining ADRs, disagrees with the AOA (as
computed by the PRIM's)." (1) "Protection is totally lost, in case of VS 1g computation failure (loss of
weight, or slat/flap position)." (2) "Protection is lost, in case of a dual ADR failure (or ADR DISAGREE)."
(3) "Protection is lost, in case of a triple ADR failure (or ADR DISAGREE)."

### p1401 — DSC-27-20-20-30 P 1/2, Ident. 00000353.0001001 / 27 DEC 23 (page 09 APR 21) — Direct Law GENERAL + PFD display figure
GENERAL text matches the slice verbatim (direct stick-to-elevator; max elevator deflection varies with CG;
no automatic trim → manual trim, amber "USE MAN PITCH TRIM" on PFD; "All protections are inoperative.";
α floor inoperative; "As per alternate law, overspeed and stall warnings are available."). **The Direct Law
DU contains no lateral/yaw paragraph at all** — its second identified section is "RECONFIGURATION CONTROL
LAWS - PFD DISPLAY" (Ident. 00000354.0003001 / 27 DEC 23): a PFD figure with callouts (1)-(5).
Footnotes (1)-(2) on this page: "(1) Bank angle and pitch limitation is replaced by an amber X.
(2) Overspeed protection symbol (=) disappears."

### p1402 — DSC-27-20-20-30 P 2/2 (page 09 APR 21) — remaining PFD-display footnotes
"(3) Vα prot and Vα max are replaced by Vsw. (4) USE MAN PITCH TRIM (amber) displayed in direct law, or
in flare law without RA. (5) MAN PITCH TRIM ONLY (red) displayed, if a L + R elevator fault is detected."
No other content — so Direct Law's two pages are fully read; no yaw text exists in this DU.

### p1405 — DSC-27-20-20-50 P 1/2 — Mechanical Back Up GENERAL + PITCH
GENERAL (Ident. 00000361.0001001 / 27 DEC 23), full text: "The purpose of the backup is to achieve all
safety objectives in MMEL dispatch condition: To manage a temporary and total electrical loss, the
temporary loss of five fly-by-wire computers, the loss of both elevators, or the total loss of ailerons
and spoilers. It must be noted that it is very unlikely that the backup will be used, due to the
fly-by-wire architecture. For example, in case of electrical emergency configuration, or an all-engine
flameout, alternate law remains available."
PITCH (Ident. 00000362.0001001 / 27 DEC 23): "Pitch mechanical control is achieved through the THS, using
manual trim control. «MAN PITCH TRIM ONLY» is displayed in red on the PFDs." (+ PFD figure showing red
MAN PITCH TRIM ONLY banner.)

### p1391 — DSC-27-20-10-80 P 1/2, Ident. 00001960.0002001 / 27 DEC 23 (page 09 APR 21) — Aircraft Trimming
(Read only to fix the page map.) In normal cruise, straight flight, AP engaged, symmetric thrust/fuel:
rudder trim should stay between 1.9° right and 1.6° left; note: true rudder deflection within ±1°, given
permanent rudder-trim indication offset in cruise (0.9° right, 0.6° left). Confirms Normal Law DU ends
here; protections DU is earlier than the rendered range.

---

## Resolution of the remaining open rows

| Row | Topic | Resolution |
|---|---|---|
| 8 | Reconfiguration failure mapping ("ALT 1 = single serious failure; ALT 2 = double serious failures; Direct = double/triple serious failures") | **HANDOUT STALE (oversimplified)** — the R17 table (p1393, transcribed above) is a specific failure list, not a single/double/triple rule. ALT 1 triggers are indeed single failures (THS jam/pos lost, one elev fault, yaw damper actuator lost, slats-or-flaps pos lost, single ADR fault\*). But ALT 2 includes non-"double" triggers: ADR DISAGREE, ALL SPLRS FAULT, ALL INR AIL FAULT, PEDALS TRANSD. FAULT, ALL ENG OUT. DIRECT adds "ALL ENG OUT + PRIM 1 INOP" and "TWO ELEV FAULT". Human page: FCOM DSC-27-20-20-10 P 1/4 (pdf p1393). |
| 11 | A/P availability by law | **Alternate "Maybe, depending on the type of failure" — CONFIRMED HANDOUT CORRECT**; **Direct "No" — CONFIRMED** (p1393: "AUTOPILOT LOST" boxes every ALT 2 and DIRECT trigger and four of six ALT 1 triggers; "SLATS or FLAPS POS LOST" and "SINGLE ADR FAULT \*" sit outside the box). **Normal "Yes" / Abn "No" / Mech "No" cells STILL UNVERIFIED** — AP engagement conditions live in FCOM DSC-22_30 (not in the rendered range); human should open DSC-22_30-30 "AP/FD Engagement". |
| 44 | Direct law yaw: "Manual rudder contol only / Yaw damping and minimum turn coordination" | **CONFIRMED HANDOUT CORRECT (via the reconfiguration table, not a Direct-Law paragraph)** — p1393 DIRECT column: LAT = "ROLL DIR / YAW ALT"; the yaw-alternate description (DSC-27-20-20-20, 00000344, already verified) is dutch-roll damping with ±4° (CONF 0) / ±15° rudder authority plus turn coordination *except in CONF 0*. The Direct Law DU itself (p1401-1402, both pages now fully read) contains **no yaw text** — cite DSC-27-20-20-10 P 1/4 (pdf p1393), not DSC-27-20-20-30. |
| 48 (entry) | Mech backup entry "Failure of all PRIM + SECs" | **HANDOUT STALE (incomplete)** — FCOM GENERAL (p1405, quoted in full above) frames it as design cases, of which "the temporary loss of five fly-by-wire computers" (= 3 PRIM + 2 SEC) is only one; the others are "a temporary and total electrical loss", "the loss of both elevators", "the total loss of ailerons and spoilers". FCOM adds that in ELEC EMER CONFIG or all-engine flameout, **alternate law remains available** (backup use "very unlikely"). Controls side stays CONFIRMED (pitch = manual THS trim, red MAN PITCH TRIM ONLY, p1405; lateral = rudder via BCM, p1406). "SS inoperative" is implied, not stated, on these pages. Human page: FCOM DSC-27-20-20-50 P 1/2 (pdf p1405). |
| 50 | Mech backup op rec "Restore electrical power to PRIMs+SECs" | **STILL UNVERIFIED as an FCOM statement — and now proven absent from FCOM DSC-27-20-20-50** (both pages of the Mechanical Back Up DU read: p1405 this pass, p1406 prior pass; no operational-recommendation text exists there). If it survives anywhere current, it is FCTM/QRH territory — closest current text remains FCTM AOP-10-30-20 BACKUP "…while reconfiguring the systems". Human: check FCTM AOP-10-30-20 and QRH; no FCOM DSC-27 page carries it. |
| 26 | "Autopilot disengages" in high AOA protection | **STILL UNVERIFIED — proven absent from the rendered range.** The rewritten high-AOA DU text (00000280.0005001, 23 JAN 26, in the text slice) does not state it, and DSC-27-20-10-20 pages fall before pdf p1390. Human should open FCOM **DSC-22_30 (AP disengagement conditions)**. |
| 27 | "Speed brakes automatically retracted/inhibited" in high AOA | **STILL UNVERIFIED — proven absent from the rendered range.** The natural home, DSC-27-20-40 (Speedbrakes), begins after pdf p1422; DSC-27-20-10-20 is before p1390. Human should open FCOM **DSC-27-20-40** (and the high-AOA DU figure at DSC-27-20-10-20). |
| 14 ("25° at low spd") | Pitch attitude 30° NU reduced to 25° at low speed | **STILL UNVERIFIED — proven absent from the rendered range.** The pitch-attitude-protection DU/figure (DSC-27-20-10-20) is before pdf p1390. Human should open FCOM **DSC-27-20-10-20 (Pitch Attitude Protection)**. 30°NU/15°ND themselves were already confirmed from the text slice. |

Bonus corroborations picked up this pass (no rows reopened): row 4/handout "MAN PITCH TRIM ONLY" —
p1402 footnote (5) restates the red message tied to "a L + R elevator fault"; row 7 — Mechanical Back Up
DU (p1405-1406) shows no ECAM law-line, consistent with handout "none" for mechanical; row 43 — Direct
Law GENERAL confirmed on the actual rendered page (p1401), previously text-slice only.

Every open item from `law_pages_VISUAL.md` is now either resolved against a rendered R17 page or proven
outside pdf pages 1344-1345 / 1390-1422 with the exact FCOM section a human should open.
