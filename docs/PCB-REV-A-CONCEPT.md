# Sprinkler Monitor — single-board PCB Rev A concept (NOT fabrication released)

**Date:** 2026-11-13  
**Stage:** exploratory **engineering design brief only**, prompted by the owner's question about a self-soldered PCB and a possible eventual Morristown Sprinkler offering. This is **not a KiCad schematic, routed board, approved PCB, fabrication Gerber, marketing authorization, or commercial/installation commitment**.

## Intent / decision

Assuming the current hand-wired three-board R6 system passes Monday's diagnostics, propose **one two-layer custom carrier PCB** that replaces Board A, Board B and the miniature ESP32 socket perfboard/JST internal interconnects. The owner could hand-solder common through-hole parts and plug in their **existing removable Waveshare ESP32-S3-POE-ETH + factory PoE module** and **ADS1115 breakout**. Avoid designing our own PoE electronics in the first PCB spin. **Keep accepted enclosure/P4 mounting plate unchanged** for prototype unless actual fit requires an explicit new decision.

## Concept Rev A PCB form factor and physical arrangement

- **Approximate board envelope:** 88 × 120 mm, 1.6 mm FR-4 two-layer (size provisional). P4 top-view overall envelope 95.1599 × 142.652 mm; exact fit to be measured in populated case before PCB layout release.
- **Mounting:** four M3 clearance holes intended to align to the measured P4 hole columns X~7.5799 and X~87.5799 mm, and measured Y rows ~26.3262 and ~116.3262 mm (in P4 reference XY). Choose actual PCB origin, shape and holes only after confirming screw/washer/insulated standoff accessibility and lid/rib/cable clearance. Do **not** repeat the missed perfboard mounting-hole alignment. P4 hole centers are from its mesh, not a fabricated PCB design.
- **Upper zone:** ADS1115 *removable* single row 1×10 socket in the same logical order as current A.P3–P12 header; R1/R2/R3/R4 and C1/C2 grouped nearby, analog net short; accessible labeled pressure-signal and A0 test points.
- **Middle zone:** 2×20 female sockets for exact Waveshare ESP32-S3-ETH board and existing PoE daughterboard, USB/BOOT/RESET accessible. Respect antenna, mechanical screw, RJ45, header stack, PoE/module height and Ethernet plug bend clearance. Native Pico-compatible header labels must be confirmed against the actual module footprint before CAD/ordering.
- **Bottom/service zone:** J1 pressure sensor 3-position terminal (+5V/GND/SIG), J2 temperature sensor 3-position (+3V3/DATA/GND), R5 4.7k pull-up and suitable label area; both terminals must be reachable after installation. Use existing RJ45 on Waveshare — only three external cable functions (Ethernet/PoE, pressure, temperature).
- **Diagnostics:** labeled test pads for +5V, +3V3, GND, raw SIG, ADS A0, temperature DATA, SDA, SCL; optional power LED and unpopulated development-only protection footprints subject to electrical review. Two-layer grounded copper and tidy routing reduce jumper faults, but do not automatically provide fault/surge protection.
- **Assembly:** favor through-hole axial resistors R1–R5, two 100nF through-hole ceramics, 2×20 female headers, 1×10 female socket and two 3-position PCB screw terminals (actual pitch must match chosen footprints). No assembly house required for Rev A; later a mostly SMT assembly-service variant may lower manufacturing variability.

## Electrical contract — clone R6 without silently changing it

| Feature | Function / net requirement |
|---|---|
| J1 pressure terminal | pin 1 ESP VSYS (+5V), pin 2 GND, pin 3 PRESS_SIG |
| Divider | J1 SIG → R1 10k → DIV → R2 10k → MID → R3 4.7k → GND |
| Filter | DIV → R4 1k → ADS A0; C1 100nF from ADS A0 to GND |
| ADC supply | ADS VDD +3.3V, GND common; C2 100nF across VDD/GND; ADDR to GND for 0x48 |
| I²C | ESP GPIO17 to ADS SDA, ESP GPIO16 to ADS SCL |
| J2 temperature | pin 1 +3.3V, pin 2 ESP GPIO18 / DATA, pin 3 GND; R5 4.7k from DATA to +3.3V |
| Reserved / unused | ADS A1/A2/A3/ALRT unused; ESP 3V3_EN NOT wired |

**No 5V to ADS VDD, no pressure SIG bypass of divider, no +5V to temperature pin 1.** The sensor model is still unverified. R6 divider assumes a historical 0–150 PSI, 0.5–4.5V sensor and requires actual bench and field validation. Protection against reverse polarity, ESD, cable transients and divider lower-leg failure requires a deliberate design review before commercial use.

## Gates before real PCB fabrication

1. Finish **Monday 2026-11-16 hand-built unit checks** from `docs/HANDOFF-2026-11-13-WIRING-COMPLETE-MONDAY-BRINGUP.md`. Diagnose old pressure near-0V fault, verify PoE, ADS 0x48, sensor temperature, bench simulator and actual gauge. Prepared v5-47k binary is **not deployed** at this checkpoint.
2. Verify ESP32 module exact row spacing, pin numbering, female-socket height, PoE stack and field terminal footprints; measure actual enclosure lid/gland/RJ45 access and confirm four actual mounting points. Save photos/measurement receipt.
3. Create a **real electrical CAD project** in KiCad: symbols, tested footprints, board outline with exact mounting holes, DRC/ ERC, BOM, assembly and silk drawings, and Gerbers/drills. Independent review before purchase. Do not mistake an AI rendering for manufacturing data.
4. Order a **small evaluation batch** (for example 3–5 boards, after approval), assemble one, compare electrical behavior with the proven perfboard and repeat all bench sensor, fault, restart, PoE brownout and reconnection tests. Label Rev A as engineering evaluation only.
5. Only if evaluating commercial use: design review for input protection, power and grounding, enclosure environmental protection, cable strain relief, EMC/FCC, applicable fire-protection equipment codes/listings, cybersecurity/update support, provisioning, remote data retention and independent site outage notifications. Determine installed system classification and AHJ/insurer expectations with qualified professionals. It must remain a **supplementary monitor**, not a replacement for listed sprinkler control, fire alarm signaling or required inspection.

## Draft product approach

Prototype (Rev A): one board + existing removable modules, two field terminals, PoE Ethernet. Reuse P4 for minimum scope and cost. Proposed optional co-branding/silk area is **not** approval for a Morristown Sprinkler-branded product, marketing, sale or outreach. Future Rev B might substitute onboard ADC, SMT resistors, industrial-input protection and manufacturing QA after proof of Rev A. Commercial hardware and operational cloud/alert service require separate acceptance.

**Status:** CONCEPT ONLY. No source schematic/PCB design files, physical Rev A PCB, fabrication purchase, product approval or operational alert service claimed.


---

## Design review supplement: architecture, protection and commercial readiness (2026-11-13)

**Current stage:** exploratory engineering requirements, NOT an implemented schematic, routed board, protection circuit or approved product. Morristown Sprinkler offering is only a possibility; there is no authorization for customer contact, purchasing, sales or production use.

### Tooling and licensing verified

- Oscar (JamiePC_HPOmen) is online, Autodesk Fusion 360 is running, and its local Device Lab SprinklerSystemMonitor clone exists. **KiCad was not installed** on Oscar at the check.
- Existing project records indicate **Autodesk Fusion Personal**. Autodesk restricts Personal to non-commercial work, **2 signal layers and 80 cm²** PCB area. Provisional 88 × 120 mm PCB = **105.6 cm²**. See [Autodesk](https://www.autodesk.com/products/fusion-360/personal) and [Autodesk Electronics limits](https://help.autodesk.com/view/fusion360/ENU/?caas=caas%2Fsfdcarticles%2Fsfdcarticles%2FFusion-360-Free-License-Changes.html).
- **Recommended:** KiCad for commercializable electrical schematic, board, ERC/DRC, Gerber/Excellon and BOM; a properly licensed commercial Fusion seat only if Fusion mechanical/ECAD is required for commercial design, otherwise use available mechanical reference without licensing cost. See [KiCad](https://www.kicad.org/about/kicad/), [KiCad library use](https://www.kicad.org/libraries/license/), [Fusion CAM outputs](https://help.autodesk.com/cloudhelp/ENU/Fusion-ECAD/files/ECD-PREP-MFG-DATA.htm). No license purchase authorized.

### Three architecture options

| Version | PCB approach | Advantages | Limits / disposition |
|---|---|---|---|
| **A: evaluation** | **Socketed Waveshare ESP32-S3-POE-ETH + socketed existing ADS1115 breakout; PCB traces and labeled sensor blocks, through-hole passives** | Minimal deviation from known R6 design; owner can hand-solder, modules replaceable | Headers add connection points; highest manual labor. **Build first** |
| **B: low-volume commercial candidate** | **Socketed Waveshare with genuine ADS1115 IC and passives/protection factory-SMT-assembled** | Eliminates 10-pin ADC breakout/socket, reduces hand soldering and connection failure risk | Needs professional footprint, outsourcing and test; **preferred after A proves circuit** |
| **C: integrated electronics** | ESP32 module + Ethernet interface + PoE + ADC integrated into custom PCB | Potentially lower unit materials and repeatable SMT at high volume | Much higher first-design RF/EMC, PoE, software and production engineering. **Defer** |

Keep an external ADC for pressure (ADS1115 IC or breakout), not ESP32 internal ADC by default: noise and calibration requirements must be met by evidence. **Cost benchmark**: TI ADS1115IDGSR indicative distributor price **$5.28 at one unit, $3.37 at 100 units** as checked November 2026: [DigiKey](https://www.digikey.com/en/products/detail/texas-instruments/ADS1115IDGSR/2231567). Full BOM unknown until modules/sensors/connectors/assembly vendors chosen. Bare PCB unit price does not capture assembly, enclosure, certified sensors, cable glands, installation, tests, hosting, support, warranty or compliance.

### Electrical additions for a commercial-pilot design

These describe **protection functions**, not verified resistor/component selections; do not add them blindly to the current unpowered R6 assembly.

1. **PoE-derived +5V sensor branch:** measure real Waveshare VSYS when PoE-powered and validate sensor load current. Current-limit the **external pressure-sensor +5V** with appropriate load switch/eFuse (or reviewed equivalent), avoiding a field-cable short taking down the entire ESP32. Add local filtering/bulk capacitance, voltage and sensor-power fault measurement. Leave factory isolated PoE circuitry unchanged.
2. **PRESS_SIG entry:** low-leakage TVS/ESD transient element and current limiting near J1. Preserve accurate 0.5–4.5V raw sensor range through divider/filter. Protect ADS A0 against **negative signals, +5V wiring fault, divider lower-leg open, powered-off backfeeding and field transients**. Test clamp leakage and current over operating temperature and under power-off conditions. A TVS by itself is not continuous DC overvoltage protection; an ADC-side clamp/OVP network requires explicit engineering.
3. **Temperature J2:** low-capacitance ESD protection, protected +3V3 sensor supply and small, validated series impedance if needed. Keep R5=4.7k pull-up to 3.3V pending actual DS18B20 cable-length/timing tests. Fault-detect missing, shorted and implausible temperature data.
4. **ADC accuracy / self-health:** retain R1=10k, R2=10k, R3=4.7k, R4=1k, C1/C2=100nF for design comparison. Consider precision divider resistors, selected I2C pull-ups if the modules do not already supply them, supply decoupling and spare ADS channels for scaled VSYS/3V3 readback. Verify resistor tolerance, calibration and actual sensor model first; any new current limiting/filter may change transfer function and needs recalibration.
5. **EMC/grounding:** connector-edge ESD termination, suitable copper returns and analog routing, mounting screw isolation, enclosure strain relief. Test with installed field cable lengths; consider 4 layers only if interference analysis shows a reason. PoE module stays the factory part, with RJ45/cable-bend clearance checked.
6. **Serviceability & QA:** pressure/temperature connectors differentiated to prevent swap; labeled test pads (5V, 3V3, GND, PRESS_SIG, A0, TEMP_DATA, SDA, SCL); power/status indicators; revision+serial/QR; accessible USB/BOOT/RESET; installation and test procedures. Require fixture-based continuity and fault injection on every commercial unit.

**ADC limitation:** TI ADS1115 analog inputs must stay **between GND and VDD in normal operation**; the absolute max is GND-0.3V to VDD+0.3V. A selectable PGA range of ±4.096 or ±6.144V does NOT authorize those pin voltages on a 3.3V-supplied chip. See [TI ADS1115 data sheet](https://www.ti.com/lit/ds/symlink/ads1115.pdf). Protection concepts: [Analog Devices IEC input protection](https://www.analog.com/en/resources/analog-dialogue/articles/solving-iec-system-protection-for-analog-inputs.html) and [TI TIDA-010008](https://www.ti.com/tool/TIDA-010008).

### Mechanical manufacturing gate — avoid repeating P4 hole error

Retain existing approved P4 plate, ~95.16 × 142.65mm, unchanged. From the accepted P4 STL, candidate plate side-hole columns are **X≈7.58 and 87.58mm**; possible matching mounting rows **Y≈26.33 and 116.33mm** (80mm horizontal, 90mm vertical separation), all measured in original plate coordinates. These are **unverified physical PCB drilling coordinates** until board origin, standoffs, washer clearance, plated/nonplated holes, screw reach, PoE height, RJ45 opening, lid gasket and field terminal access are validated on real components. The previous 88 × 120mm concept is an **envelope only**.

### Operational acceptance / product responsibility

- Hardware needs controlled power, voltage measurements, positive pressure simulator and actual sensor comparison, startup, cable disconnect, reversed/miswired sensor, sensor outage, overheating/condensation, PoE flaps, Ethernet link loss and recovery tests.
- Firmware/service needs authenticated provisioning, unique identity, TLS, signed OTA with rollback, device watchdog, real sample age and quality, deterministic sensor-fault states, adjustable thresholds/hysteresis, recovery logic, independent offsite heartbeat, durable timestamped history and delivery-tested alerts. A failed site network must not silently imply normal status.
- Do not replace required dry-pipe/preaction air-pressure supervisory wiring or fire alarm controls. [NFPA notes](https://www.nfpa.org/news-blogs-and-articles/blogs/2021/06/25/a-guide-to-fire-alarm-basics-supervision) such supervision may be required on particular systems; qualified fire protection/AHJ/compliance reviewers must assess installation claims and any listing requirements. [UL 864 certified signaling example](https://www.ul.com/news/certified-dialer-capture-modules-fire-alarm-systems) illustrates why life-safety monitoring cannot be assumed from ordinary IoT operation. FCC/EMC host testing and any radio module conditions must also be reviewed; environmental safety and installation responsibilities matter.

### Implementation and order gates

**G0 (current):** owner reports all hand-assembled JST connections complete. **Final end-to-end harness mapping and no-short tests remain pending**, device has not been powered in rebuilt configuration, firmware v5-47k not deployed, and no alerts accepted.

**G1:** complete Monday November 16 unpowered electrical verification and controlled PoE bench tests, pressure sensor diagnosis/simulator and temperature validation; no changes to listed fire system or pressure.

**G2:** measure actual module socket geometries, selected component manufacturer part numbers and footprints, installed cable lengths, supply currents, sensor part number, mounting holes and connector exit. Complete protection/fault specification and peer electrical review; select architecture A or B for prototype.

**G3:** Create native KiCad schematic + PCB, tested local footprints, BOM and test plan, pass electrical rules check, layout rules check, board manufacturer's DFM rules, and independent pin-by-pin design review. **Only then** generate/review Gerber copper, solder mask, silkscreen, outline, Excellon PTH/NPTH drill files, assembly drawing and SMT pick/place if applicable; zip/order pack with revision hash. No manufacturing-ready files claimed today.

**G4:** Obtain an actual prototype fab/assembly quote and owner authorization for spending before ordering 3–5 evaluation boards; hand-assemble as applicable, compare to established perfboard, complete miswire/surge and long-run tests.

**G5:** Any pilot with a sprinkler contractor requires technical, liability, field procedure, permitted marketing claims, compliance, service and support review. No sale or partner communication has been authorized.

**Supplement status:** Research and architecture only; Oscar Fusion installed/running, KiCad not yet installed, no ECAD/PCB design created, no Gerber files, no ordered prototype, no deployed firmware and no product compliance acceptance.
