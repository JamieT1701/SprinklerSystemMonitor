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
