# Device Lab — Sprinkler Pressure Monitor — Physical Build Handoff
**Checkpoint:** November 11, 2026 (evening)  
**Authority:** `JamieT1701/SprinklerSystemMonitor`, active branch `docs/device-lab-2026-11-10-checkpoint`, draft PR #1. Do NOT assume `main` is current or merge this branch as part of assembly.

## User's instruction
Resume the electronics build **exactly where it was left**, without restarting the engineering process. Give TL;DR guidance, practical hole coordinates, few steps at a time; do not ask repeated questions already answered. User photos in the original chat show the actual board with resistors, capacitors and soldered header installed. Photos may not carry into new conversation; owner can send new ones when necessary.

## Verified-to-date current physical stage
- P4 3D-printed PETG 95.2 x 142.7 mm project plate, 3mm thick, four 6mm feet for M3 heat-set inserts is the **selected geometry**; owner reported P4 perfect fit. P5 speculative redesign was rejected. At the time of this build sequence, P4 full plate was printing. No drilled case, heat-set installation, screw-engagement check or full populated enclosure acceptance was reported.
- Two **50 x 70mm isolated-pad perfboards**. Board A = ADS1115 + pressure input circuit. Board B = two three-position field terminals + temp pull-up. Waveshare ESP32-S3-POE/ETH controller and factory PoE module mount separately.
- **Board A:** Owner mounted a 10-pin **male header in row P, columns 3 through 12** of Board A, soldered it to the perfboard. ADS1115 breakout has female sockets underneath and plugs onto those header pins, removable. Owner **explicitly corrected** photo interpretation: header is **P3-P12**, absolutely **NOT** R3-R12. Row A is bottom, R top; column 1 left, 24 right. All coordinates are always **component-side coordinates**; physically turning board over mirrors columns and rows.
- Owner installed and soldered all 4 resistors + 2 capacitors in their assigned holes and provided top and underside photos. Photos show soldered leads and some lumpy header solder joints; visual review alone was insufficient to certify no bridges. **No actual jumper wiring, resistance measurements, continuity testing, or power-on was yet confirmed by the user**. Do not advance the accepted build state beyond that.
- Owner instruction immediately preceding handoff: assistant gave ten **underside insulated jumper** connections and pre/post checks. Owner has not yet confirmed jumper completion.

## Definitive Board A ADS1115 silkscreen/pin map
| Hole | Pin | Net |
|---|---|---|
| P3 | A3 | unused |
| P4 | A2 | unused |
| P5 | A1 | unused |
| P6 | A0 | A0 pressure input |
| P7 | ALRT | unused |
| P8 | ADDR | GND (address 0x48; confirm existing strap where applicable) |
| P9 | SDA | ESP GPIO17 |
| P10 | SCL | ESP GPIO16 |
| P11 | GND | common GND |
| P12 | VDD | +3V3 ONLY |

## Board A component hole positions (user has installed/soldered)
| Component | Electrical value | Leg 1 | Leg 2 |
|---|---|---|---|
| R1 | 10 kΩ | D3 | D7 |
| R2 | 10 kΩ | D9 | D13 |
| R3 | 4.7 kΩ | D15 | D19 |
| R4 | 1 kΩ | F9 | F13 |
| C1 | 100 nF, marking 104 | H13 | H15 |
| C2 | 100 nF, marking 104 | N15 | N17 |

They are **isolated pads**, not stripboard. None of these coordinates connect electrically without wires/intentional bridge.

## Ten pending underside insulated jumper links (per previous answer)
1. D7 → D9 (DIV)
2. D9 → F9 (DIV)
3. D13 → D15 (MID)
4. F13 → H13 (A0)
5. H13 → P6 (ADS A0)
6. D19 → H15 (GND)
7. H15 → N17 (GND)
8. N17 → P11 (ADS GND)
9. P11 → P8 (ADDR to GND)
10. N15 → P12 (+3V3 ADS supply)

**Resulting nodes:** DIV = D7 / D9 / F9; MID = D13 / D15; A0 = F13 / H13 / P6; GND = D19 / H15 / N17 / P11 / P8; +3V3 = N15 / P12; pressure signal input D3 (R1 input) is unconnected until the Board B harness arrives.

## Next action / bench safety
1. With **PoE and USB disconnected** and **ADS1115 module unplugged from socket**, inspect/reflow any suspicious solder joints; inspect clipped metal tails and header pins for bridges. Work under magnification if available. Keep all wiring unpowered.
2. If owner has not yet installed the 10 links, guide them carefully using the ten connections above, one small group at a time; coordinate markings are component-side labels while solder side appears mirrored. Insulated links should have no long exposed sections.
3. Basic resistance checks prior to wiring: D3 ↔ D7 ≈10k, D9 ↔ D13 ≈10k, D15 ↔ D19 ≈4.7k, F9 ↔ F13 ≈1k. Inspect nonadjacent pads to rule out shorts. After ten links with ADS unplugged: D3 ↔ D19 ≈24.7k; P8 ↔ P11 ≈0Ω; P11 ↔ P12 must have no **steady low-ohm** short (C2 may briefly charge); P6 ↔ P11 must NOT be hard short (nominal expected circuit 15.7k, subject to measurement topology). This is not powered device acceptance.
4. Ask for a new **underside photo only after the soldering/continuity phase**, then inspect. Do not declare the board electrically correct solely from images.
5. Follow the authoritative R6 wiring in `docs/BUILD-GUIDE.md` and `hardware/two-terminal-design.json` when connecting ESP32 and Board B. Board B has only two 3-screw terminals: J1 PRESS +5V/GND/SIG, J2 TEMP +3V3/DATA/GND. R5 4.7k between +3V3 and DATA goes on Board B. W01–W09 are nine inter-assembly connections, **separate** from the ten Board A on-board links.
6. For inter-assembly connections: W05 ESP GPIO17→Board A P9 SDA; W06 ESP GPIO16→A P10 SCL; W07 Board B +3V3→A N15; W08 Board B GND→A P11; W09 Board B PRESS SIG→A D3. W01–W04 handle Board B VSYS/GND/temp. Do not miswire +5V into ADS VDD.
7. Later do bench simulator/diagnostics (pressure earlier failed ~0.0003V while gauge ~50psi); v5-47k only compiled, not deployed, and full alerts/history/offsite outage service are **not operationally accepted**. This remains supplementary sensing, not fire-alarm or sprinkler safety control.

## Source pointers
- Public guide: https://jamiet1701.github.io/SprinklerSystemMonitor/
- Draft PR: https://github.com/JamieT1701/SprinklerSystemMonitor/pull/1
- R6 bench: `docs/BUILD-GUIDE.md`
- Design netlist: `hardware/two-terminal-design.json`
- Earlier GitHub PR comment ids: corrected header mapping `6810182230`; Board A assembled/photo inspection and net map `6810559179`; physical P4 fit `6809203718`.

## Important status distinctions
The authoritative wiring is documented; Board A **components are physically soldered**; Board A jumpers and continuity have **not been user-confirmed**; Board B assembly, power testing, calibration and alarms remain open. Never substitute prior conceptual diagrams or obsolete P2 PDF with R3=5k for R6 values.
