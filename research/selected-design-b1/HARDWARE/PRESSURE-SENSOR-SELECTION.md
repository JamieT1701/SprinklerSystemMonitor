# B1 pressure transmitter selection — design candidate, not installation approval
Date: 2026-11-16
Authority: Device Lab commercial B1, design/claude-b1-engineering-20261116, PR #7 / Issue #3

## Decision
**Preferred precision architecture reference: ProSense SPTD25-20-0100H. CURRENT PURCHASING HOLD: backordered as of 2026-11-16 (projected earliest 2026-12-30, unguaranteed).**
This is a **candidate for engineering and sourcing**, not an owner-approved purchase, field installation or a guarantee that 0-100 psig suits every dry system. The observed existing ~50psi operation makes a 0-100 psig range a sensible first validation configuration **only if** qualified installation pressure and transient limits permit. Store the specific transmitter's range in the unit's signed device configuration, not a global hard-coded threshold.

**Available lower-cost bench alternative: AchieVe LPPT25-20-0100H (supplier showed 295 available as of most recent page).** 0-100psig 4-20mA, M12, 1/4in MNPT, 9-32V, ±1% total error band from 0-85C, ~USD 80 listed. It is a different device with a **different M12 pin assignment**, so do not silently swap it into an SPTD25-wired system.

## Supply-risk qualification gate

The latest supplier page explicitly marks **SPTD25-20-0100H BACKORDERED** with 171 incoming no earlier than **2026-12-30** (not guaranteed). Source: https://www.automationdirect.com/adc/shopping/catalog/process_control_-a-_measurement/pressure_sensors/pressure_transmitters/sptd25-20-0100h . The competing **LPPT25-20-0100H** page showed **295 available**, but its return is on M12 **pin 3 or 4**, not pin 2. Thus the SPTD25 shall remain an electrical baseline and concept CAD model, **NOT the sole production-sourcing plan**. Do not purchase without a confirmed lead time and without verifying installed-range and approved sensor identity. Before paid prototype parts, either secure SPTD stock or independently qualify an available second-source variant and build its dedicated cable contract. A second source sharing a connector is **not** an electrically equivalent replacement. Consider a part with an identical wiring contract to avoid variant harness risk rather than assuming all A-coded M12 transducers are interchangeable.

## Verified manufacturer specs / current public retail
| Attribute | Preferred SPTD25-20-0100H | Lower-cost LPPT25-20-0100H |
| --- | --- | --- |
| Supplier model | ProSense (AutomationDirect) | AchieVe (AutomationDirect) |
| Listed single-piece price 2026-11-16 | **USD 133** | **USD 80** |
| Pressure span | Gauge **0-100 psig** | Gauge **0-100 psig** |
| Accuracy | **±0.5% full scale (~±0.5psi)** at reference/spec conditions; do not claim total installed error is that small | **±1% total error band (~±1psi)** from 0-85C |
| Process fitting | **1/4in MNPT**, stainless wetted parts | **1/4in MNPT**, stainless |
| Electrical | **2-wire 4-20mA**, M12 4 contacts, sensor uses **pin1/+ and pin2/return** | **2-wire 4-20mA**, M12 4 contacts, sensor uses **pin1/+, pin3 or pin4/V-**, **pin2/chassis ground** |
| Power | **8.5-36VDC** | **9-32VDC** |
| Proof/burst for 100psi | **250psig / 2900psig** manufacturer table | **200psig / 500psig** manufacturer table |
| Sensor ingress | **IP67 / IP69K** rating (specific mating conditions to confirm) | **IP67** rating (mated cable requirements to confirm) |
| Sensor temperature | -40..+90C operating/medium | -40..+105C ambient, accuracy TEB degrades outside 0..85C |
| Certification on sensor | cULus (E320431), CE | UL recognized (E311366), CE |
| Supplier/model conclusion | Preferred for bench/fit/cost optimization due to smaller stated error, strong overpressure rating, published failure and EMI specifications, 3-year warranty | Potential volume cost-down with **separate harness profile/bench qualification**; never field interchangeable by blind plug |

Important: an identical M12 mechanical connector does **not** ensure that a replacement sensor is electrically compatible. The M8 temperature connector remains a physically different family, so pressure and temperature cables cannot mate to each other.

Manufacturer sources:
- SPTD product/price: https://www.automationdirect.com/adc/shopping/catalog/process_control_-a-_measurement/pressure_sensors/pressure_transmitters/sptd25-20-0100h
- SPTD manual/data with **physical pinout 1+,2-**, supply/load formula, 100psig 250psi proof / 2900psi burst and under-/overrange transfer: https://cdn.automationdirect.com/static/specs/prosensesptd25transmitters.pdf (2026 edition)
- LPPT product/price: https://www.automationdirect.com/adc/shopping/catalog/process_control_-a-_measurement/pressure_sensors/pressure_transmitters/lppt25-20-0100h
- LPPT different pinout/TEB: https://cdn.automationdirect.com/static/specs/achievelpptprestrans.pdf

## Pressure cable and cabinet socket
**Preferred initial field extension cable: AutomationDirect CDP12-0B-030-AA**, M12 A-coded 4-pole **axial female-to-male** 3m/9.8ft PVC, IP67 specified with proper mates; **USD 12.50 listed**. Its female end mates to the SPTD25 sensor's male M12, its male end to B1's female M12 panel P3. Need to inspect actual pigtail drawings and perform **continuity on all four contacts** before driving the sensor; do not assume factory wiring colors map to cable pin numbers. Shorter cable candidate: CDP12-0B-010-AA (1m, price recheck).
- Product and price: https://www.automationdirect.com/adc/shopping/catalog/cables_%28terminated%29/circular_connection_cables/cdp12-0b-030-aa
- Cable spec family: https://cdn.automationdirect.com/static/catalog/images/product-pdf/SCC-Sensor-Cables-Connectors.pdf
- The P3 panel remains binder **76 4332 0011 00004-0200** female, A-coded; panel wiring and mechanical sealing/gasket must be confirmed against binder mating drawing and imported original STEP.
- Avoid illuminated PNP-series M12 extension cables for analog 4-20mA: manufacturer documentation expressly cautions its LED assemblies are **not for analog output devices**. Source: https://cdn.automationdirect.com/static/specs/m12patchledcbl.pdf

## Pin contract — explicitly REPLACES earlier assumed P3 pin 3 return
For the **SPTD25-specific OEM harness** (view numbered from actual manufacturer contact-face drawings; do not infer the mirrored solder-face mapping):
- Sensor/P3 **contact 1** -> **+24V current-limited field source** after verified hardware eFuse, and after optional TVS/protection.
- Sensor/P3 **contact 2** -> **4-20mA loop return**, passing the protected **100ohm** low-side sense resistor, to the proper common return domain.
- Contacts **3 and 4** -> **NO CONNECT** at B1 end and no exposed auxiliary voltage.
- The SPTD manufacturer lists cable colors **brown=pin1, white=pin2, blue=pin3 unused, black=pin4 unused**, for its specified cable assemblies. Our chosen CDP patch cable may use different conductor colors or internal crossovers; prove by DMM and actual mating connector pin numbers before energizing.
- An owner-installed 3-wire voltage-output sensor **must never** be connected to this B1 interface, notwithstanding similar physical sensor body shapes.

**Do not copy this wiring to LPPT**: that sensor lists pin1 V+, pin2 Ground, pin3 OR pin4 V-! Difference can cause malfunction and unexpected return current. Treat a substitute as a separate qualified assembly and approved BOM revision. Cable labels and unit firmware sensor identity must match the hardware.

## Transmitter behavior that affects firmware
- Nominal **4.0-20.0mA** corresponds to **0-100psig**.
- Manufacturer documents under-range **3.0-4.0mA non-linear** and over-range **20.0-25.0mA non-linear**. These are not valid calibrated pressure readings, but **cannot categorically be called NE43 sensor failures**.
- **Below 3.0mA or above 25.0mA**: suspected loop, output/transmitter fault or wiring condition; classifier must fail UNKNOWN, never report healthy. The boundary is diagnostic policy, not an asserted manufacturer-fault-code definition.
- Open circuit near 0mA, supply collapse, terminal rail, ADC failure, stale sample and output stage fault remain independent invalid states.
- Never extrapolate PSI in non-linear regions, allow a panel miswire to masquerade as low pressure, or carry old sensor values into a NORMAL dashboard state.
- The precise alert thresholds remain installer/owner approved **per monitored air domain**, separate from sensor technical range.

## Supply/compliance arithmetic
- With **100ohm** shunt at **21.5mA**, shunt = **2.15V**; SPTD manufacturer maximum load `Rmax=(Vsupply-8.5V)/0.0215A`. With nominal **24V** the maximum loop resistance is ~720.9ohm, leaving ample budget for a 100ohm shunt if eFuse/cable drops are kept reasonable.
- At **25mA** possible over-range, shunt = **2.5V** and is within ADS1115 3.3V supply **under normal qualified conditions only**.
- For protected 24V output, proposed TI **TPS26625DRCR** (auto-retry, output reverse protection) with a **nominal 165kΩ R_ILIM** yields `IOL=6.636 / 165 = 0.04022A` (A, kΩ units from TI datasheet). This is **a theoretical 40.2mA design target**, NOT a verified current-limit accuracy at that low setting. The data sheet only explicitly quotes ±5% at 880mA; the actual trip, thermal cycling and booster survivability must be measured at cold/hot and indefinitely shorted. A latch-off TPS26624 is an alternate with human/power-reset tradeoff.
- TI: https://www.ti.com/lit/ds/symlink/tps2662.pdf ; TPS26625 listing https://www.digikey.com/en/products/detail/texas-instruments/TPS26625DRCR/9692673 (USD 3.04 each, recent).
- Pololu 5588 at $3.75 is a **boost development module only** and can be destroyed by output shorts, even if it has input current limit. https://www.pololu.com/product/5588.

## DFM/failure-mode gates BEFORE purchase or PCB release
1. **Selected range suitability**: approved system max air pressure and process port/mechanical/tap compatibility; 0-100psi is a design choice, not site-wide safe claim.
2. **Correct sensor identity**: physical cable/mating/point-to-point P3 contact 1/2 pinout, unique SKU label and service instructions; alternative LPPT must not silently plug into the same harness profile.
3. **Real current-limit stage**: authoritative exact 10-pin TPS26625 pin mapping/footprint, correct RTN/GND/PowerPAD connections, protection network and power-off ADC survivability. TI explicitly warns NOT to connect RTN directly to GND or reverse-polarity protection is defeated.
4. **Electrical lab**: SPTD supply compliance from 5V PoE rail through booster/eFuse under 25mA, continuous shorts (field +24V to return/GND; external 24V backfeed; reverse), open contacts, low-temp startup, wire/water short, repeated auto-retry heating.
5. **Bench current/pressure calibration**: current source 0/3/3.5/4/12/20/20.5/21.5/25/27mA, independent calibrated pneumatic test source, verify no false normal and quality status.
6. **Hardware revision control**: no live R6 3-wire signal/firmware changes, no sensor order, no field tapping, no claims of UL-listed finished B1 product.

**Maturity: component and cable specified for a bench-grade prototype BOM, electrical current-limit plan remains unproven; NOT fabrication-ready.**
