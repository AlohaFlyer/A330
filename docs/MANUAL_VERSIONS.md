# Manual Version Registry

Seeded from `manuals.json` on 2026-09-01. `manuals.json` is the source of truth;
this table is the human readable view of it. When they disagree, the JSON wins.

`revision` is `null` where the publisher prints no revision number on the
document. Those manuals are identified by issue date alone. Do not invent a
revision number to fill the column.

`Last vetted` is the date a human last re-verified portal content against that
revision, not the date the file was downloaded. `never` means the sweep in
`REVISION_PROCESS.md` has not been run against it yet.

| Manual code | Title | Revision | Issue date | Fleet | Last vetted |
| --- | --- | --- | --- | --- | --- |
| `A330P_FCOM` | A330 Passenger FCOM | R17 | 15 MAY 26 | pax | never |
| `A330P_NPC-CB` | A330 Passenger Normal Procedures and Checklist Card Book | _none published_ | 8/13/25 | pax | never |
| `A330P_PERF` | A330 Passenger Performance Manual | R26-10 | Aug 12 2026 | pax | never |
| `A330P_QRH` | A330 Passenger QRH | R35 | 26 JUN 26 | pax | never |
| `A330F_FCOM` | A330 Freighter FCOM | R10 | 15 MAY 26 | frtr | never |
| `A330F_NPC-CB` | A330 Freighter Normal Procedures and Checklist Card Book | _none published_ | 8/13/25 | frtr | never |
| `A330F_PERF` | A330 Freighter Performance Manual | R26-10 | Aug 12 2026 | frtr | never |
| `A330F_QRH` | A330 Freighter QRH | R5 | 26 JUN 26 | frtr | never |
| `A330_AFM` | A330 Airplane Flight Manual | _none published_ | 11 AUG 26 | both | never |
| `A330_AFM-SUPP` | A330 AFM Supplement | _none published_ | 05 AUG 26 | both | never |
| `A330_FCTM` | A330 Flight Crew Training Manual | R5 | 27 MAR 26 | both | never |
| `A330_MEL` | A330 Minimum Equipment List | R59 | 4/1/26 | both | never |
| `A330_PRC` | A330 Pilot Reference Cards | _none published_ | 3/9/26 | both | never |
| `FODM` | Flight Operations Data Manual | R0 | 5/20/26 | shared | never |
| `FOM` | Flight Operations Manual | 125.1 | 8/12/26 | shared | never |

15 manuals tracked: 4 pax, 4 frtr, 5 both, 2 shared.

## Fleet values

| Value | Meaning |
| --- | --- |
| `pax` | A330 passenger aircraft only. This is the default study scope. |
| `frtr` | A330 P2F freighter only. Available behind a toggle, never deleted, never mixed into PAX content. |
| `both` | One book covers both aircraft. |
| `shared` | Fleet-common manual, not A330 specific. |

Never cross-cite. A PAX fact cites an A330P book. A freighter fact cites an
A330F book. A `both` or `shared` book can serve either.

## Manuals with no published revision number

- `A330P_NPC-CB` (issue 8/13/25)
- `A330F_NPC-CB` (issue 8/13/25)
- `A330_AFM` (issue 11 AUG 26)
- `A330_AFM-SUPP` (issue 05 AUG 26)
- `A330_PRC` (issue 3/9/26)

For these, the issue date IS the version. File them as
`<FLEET>_<MANUAL>_<YYYY-MM-DD>.pdf`.

Related trap: the A330 FCOM and FCTM DO carry a revision number, but not on
the cover. The cover shows only an issue date. The number is on the Revision
Summary page, around page 45. Do not conclude "no revision number" from the
cover alone.
