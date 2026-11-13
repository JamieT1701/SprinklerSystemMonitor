# Device Lab sprinkler monitor — Monday 2026-11-16 bring-up checkpoint

**Recorded:** Friday, November 13, 2026, after owner reported "all connections made" and departed for the weekend.  
**Authority:** `JamieT1701/SprinklerSystemMonitor`, branch `docs/device-lab-2026-11-10-checkpoint`, draft PR #1. R6 design: `docs/BUILD-GUIDE.md` and `hardware/two-terminal-design.json`.  
**Read this before resuming Monday.** This record supersedes the 2026-11-11 Board-A-only *assembly status* but NOT its verified coordinate/netlist design. Do not merge this draft PR or assume `main` is current.

## Critical status distinction

**OWNER-REPORTED PHYSICAL BUILD:** On November 13 the owner stated **"all connections made"** after completing the three assembled, JST-connected subassemblies. Treat all board wiring and connector work as *reported assembled*, **NOT** as a full end-to-end, unpowered electrical verification, powered bring-up, pressure measurement, pressure calibration, or operational acceptance. Do not infer specific JST harness conductors were verified end-to-end just because the user said all connections made. **Keep PoE/USB and external sensors disconnected until pre-power checks.**

**NOT COMPLETE:** Unpowered full system/connector mapping verification, mechanical anti-slide and RJ45 strain relief validation, powered PoE bench check, ADS detection, DS18B20 temp test, simulated pressure check, installed gauge comparison/calibration, prepared v5-47k firmware deployment, history/alerts and offsite outage acceptance.

## Physical components

- Board A: 70×50 mm isolated-pad perfboard. ADS1115 removable on ten male pins at **P3–P12**, female sockets on module. R1=10k D3–D7; R2=10k D9–D13; R3=4.7k D15–D19; R4=1k F9–F13; C1=100nF H13–H15; C2=100nF N15–N17. All ten original underside circuit links were reported soldered and basic board tests passed in conversation. 
- Board B: 70×50 mm perfboard; pressure terminal J1=E4 (+5V), E6 (GND), E8 (SIG); temperature terminal **J2**=E15 (+3.3V), E17 (DATA), E19 (GND). R5=4.7k M13–M19, links E15→M13, E17→M19. Circuit points: B.P4=+5V, P14/P15=+3V3, P6/P19=GND, P8=SIG, P17=DATA; links to the sensor blocks and between ground/power pads were owner-reported assembled and tested in earlier steps.
- Waveshare ESP32-S3-ETH / PoE board with soldered male headers, removable from a smaller female-header perfboard carrier. Do not solder wires directly to controller.
- Accepted **P4 PETG** enclosure plate stays unchanged. Owner says original **24mm left/right test rails are perfect size for ESP carrier**; longer **44mm mirrored rails** are planned for Board A and B. Actual long-rail placement, anti-slide clips, screw projection, lid closing and RJ45 strain relief not explicitly accepted. Do NOT redesign P4, use P5, or assume friction headers bear Ethernet cable strain.

## Final JST header hole coordinates and logical net assignments

Coordinate system on both perfboards: **A–R rows bottom-to-top, columns 1–24 left-to-right**, from component side; underside mirrored. Each pad electrically isolated.

| Board | JST header | Header hole → intended net | Jumper to established circuit |
|---|---|---|---|
| A | **H2, 2-way** | G4 SDA; G5 SCL | G4→A.P9, G5→A.P10 |
| A | **H3, 3-way** | G20 +3V3; G21 GND; G22 pressure SIG | G20→A.N15 (also P12); G21→A.N17 (also P11); G22→A.D3 |
| B | **H1, 4-way** | J2 +5V; K2 +3V3; L2 GND; M2 TEMP_DATA | J2→B.P4; K2→B.P14; L2→B.P6; M2→B.P17 |
| B | **H3, 3-way** | K20 +3V3; K21 GND; K22 pressure SIG | K20→B.P15; K21→B.P19; K22→B.P8 |

**CAUTION:** B **hole J2** is not temperature **terminal block J2**; **A.P6** is ADS pressure A0 while **B.P6** is common GND; **A.P8** is ADS ADDR strapped to GND while **B.P8** is raw pressure SIG. Header slot/pin order is logical plan, NOT confirmed keyed face/manufacturer pin numbering. 
The owner briefly said **"Wait board A locations make no sense"**, then later reported completion. This remains a focused **pre-power remap/inspect priority**, especially A.H3 G20/G21/G22.

**Three cable/harness functions:** 
- H1: ESP carrier ↔ B H1, **VSYS(+5V), 3V3, GND, GPIO18(DATA)**. 
- H2: ESP carrier ↔ A H2, **GPIO17 (SDA), GPIO16 (SCL)**.
- H3: B H3 ↔ A H3, **+3V3, GND, PRESS_SIG**.
The physically keyed JST plug directions, conductor order, pin numbering and their final actual wire continuity are NOT separately documented as verified. Check every conductor with a DMM (do not trust cable color/position).

**Waveshare GPIO reference:** Manufacturer-derived previous bench map with USB end first on controller's left header: physical 40 VBUS, 39 VSYS, 38 GND, 37 3V3_EN (**not supply**), 36 3V3, 35 GPIO21, 34 GPIO17 (SDA), 33 GND, 32 GPIO16 (SCL), 31 GPIO18 (temperature DATA). Confirm actual controller orientation and pins/sockets with DMM before energizing. These are not hole coordinates on the smaller carrier (not recorded). Keep ESP's **3V3_EN** unconnected.

## Monday startup procedure — small steps, no assumption of power readiness

1. Physically inspect the assembled unit, rails, retaining clips, connector housings/keying and ESP/PoE underside clearances. Check no solder whiskers, conductive rail/screw contact or a slide-out risk. Ensure Ethernet plug can be inserted/removed without load on header sockets. Dry-fit enclosure/lid and strain relief before installed use.
2. **Leave PoE/USB/sensors disconnected.** For resistance checks, unplug the ESP32 and ADS1115 modules and unplug JST harnesses as needed. Verify each JST jack **pin-to-its-assigned circuit pad**: 2 A.H2, 3 A.H3, 4 B.H1, 3 B.H3. Explicitly recheck A.H3 SIG→D3 and no +3V3↔GND short. Expect B.H1 3V3 to temp DATA ~4.7k; A raw pressure SIG→GND ~24.7k; A ADS A0→GND ~15.7k.
3. **Individually map each cable pin-to-pin with DMM** against actual keyed/mating plugs; never assume visual left-to-right matches when flipped. Ensure the assembled harnesses preserve H1 VSYS→B +5V; H1 3V3→B +3V3; H1 GND→B GND; H1 GPIO18→B DATA; H2 GPIO17→ADS SDA; H2 GPIO16→ADS SCL; H3 B +3V3/GND/SIG→respective A counterparts. Verify no crossed wires, no raw +5V to ADS VDD or ADC input, and no rail shorts before restoring controller.
4. Inspect/reseat ADS and ESP modules with correct orientation; confirm full-assembly low-ohm shorts absent. Only after safe inspection/tests and dry-fit, controlled bench **PoE** power; measure actual voltage at B +5V, B/A +3V3 and GND (ensure PoE hardware and Ethernet are connected appropriately; no high-voltage PoE test points).
5. Verify expected ADS I²C 0x48, temp-sensor detection/fault, and bench pressure-input simulator per **R6 guide**. Do not connect to the live sprinkler sensor or interfere with sprinkler piping/controls until verified. Previously v4 reported ADS pressure ~0.0003–0.0004V while gauge ~50PSI — unresolved. Prepared **v5-47k firmware was compiled but NOT deployed**. No live alerts/history/offsite heartbeat acceptance.

## Status summary

**Physical build:** OWNER-REPORTED FULLY CONNECTED as of Friday Nov 13.  
**Bench electrical verification:** earlier per-board checks owner-reported passed; **final JST/harness system verification PENDING**.  
**Power applied to rebuilt assembly:** NOT REPORTED.  
**Firmware v5-47k deployed:** NO.  
**Monitoring/alerts accepted:** NO.  
**Next user action:** Rejoin Monday November 16; begin with the above unpowered visual + continuity checks, not another design review or firmware deployment.

Do not treat this supplementary monitor as certified protection for sprinkler/fire alarm systems.
