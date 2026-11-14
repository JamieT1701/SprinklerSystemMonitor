# Sprinkler Monitor - authoritative two-terminal bench design (R6)

Date: 2026-11-11. Electrical design R6; mounting information updated after P4 fit confirmation. Replaces the earlier v1/v2/v3/v4 build instructions.
Design reviewed and arithmetic checked; hardware is not built/validated/accepted by this record.

## Exactly three external connections
1. Ethernet/PoE cable -> factory RJ45 on existing Waveshare controller.
2. Pressure sensor cable -> J1, a single 3-position terminal block on Board B.
3. Temperature probe cable -> J2, a single 3-position terminal block on Board B.
No additional external power input, sensor block or test socket is required.

## Two field terminal blocks, both on Board B
| Terminal | Function | External wire |
|---|---|---|
| J1-1 | +5V from ESP VSYS | Pressure red |
| J1-2 | Common GND | Pressure black |
| J1-3 | PRESS_SIG to R1 | Pressure green |
| J2-1 | +3V3 | Temperature VCC |
| J2-2 | DATA to ESP GPIO18 | Temperature DATA |
| J2-3 | Common GND | Temperature GND |

Number from left to right, looking at screw heads with wire mouths toward the accessible edge. Label actual parts. Do not infer probe colors from a generic picture. Pressure colors follow the user's historical documentation. Internal wires solder to pads rather than sharing field screw clamps.

## Confirmed enclosure and plate (P4)
- **P4 is the selected project plate**: Jamie physically checked its fit in the plastic enclosure and reported it fits perfectly. Do **not** substitute speculative P5 or older plate outlines. P4 is approximately **95.2 mm wide x 142.7 mm tall**; its PETG plate is **3 mm thick**, with **four 6 mm integral mounting feet**.
- P4's four feet contain holes intended for **M3 brass heat-set inserts**. Install heat-set inserts into the bottoms of the feet, only after testing one insert against its printed socket. Actual insert outer diameter and length are not independently measured; check the fit before heating all four. Use a soldering-iron insert tip with the part supported on a heat-safe surface. Do not insert an iron into the enclosure.
- To mount, turn the plate so the **feet face the case floor**. Align feet with case holes and install screws **from outside the case into the brass inserts**. **M3 x 6 mm plus flat washers** is a starting combination from the owner's on-hand hardware, not a verified final length. Verify actual case wall (~1.2 mm estimate), washer, insert depth, screw engagement, and clearance so screws neither bottom out nor puncture the plate. Hand-tighten; do not crack the plastic box.
- The four P4 feet hold the **project plate to the enclosure**. They are **NOT** stand-offs for soldered circuit boards. Mount the ESP32/PoE assembly and both perfboards above the plate with their own insulated spacers, screws or zip ties through suitable perforations. Keep solder joints and conductive component undersides isolated from the plate and any metal fasteners.
- P4's hole pattern provides flexible mounting, **not prelocated exact PCB mounting holes**. Dry-fit the actual controller, ADS1115, terminal blocks, wiring, Ethernet bend and lid before drilling or securing electronic boards. Avoid the divider rail/recess and keep the two 3-wire sensor blocks reachable.
- No electronic assembly has been physically fit-tested on P4 yet; the enclosure fit report does not verify cable or PoE clearance.

## Placement
- Board A (50x70): ADS1115, R1-R4, C1, C2. No field terminal blocks.
- Board B (50x70): exactly J1, J2 and R5. Labeled +5V/+3V3/GND/DATA/SIG solder-pad groups.
- Controller: separate insulated supports; factory PoE daughterboard intact; USB/BOOT/RESET/RJ45 accessible.
- Use the **confirmed-fitting P4 PETG project plate** (approximately 95.2 x 142.7 mm) instead of the earlier notional 170 x 120 mm baseplate. Dry-fit the real boards, PoE stack, connector footprint, cable bend and lid; plate fit alone does not prove component clearance.
- Use isolated-pad perfboard, not unmodified stripboard. Short insulated jumpers create deliberate connections; adjacent pads are not automatically connected.

## Installed parts
- R1=10k and R2=10k (Board A).
- R3=4.7k (Board A pressure lower leg).
- R4=1k (Board A ADC input filter).
- R5=4.7k (Board B temperature pull-up).
- C1=100nF ceramic between A0 and GND.
- C2=100nF ceramic across ADS VDD and GND, close to module (added supply bypass; any existing module bypass remains).
- One EXTRA temporary 10k is used for a bench test, then removed.
- Mechanical mounting: confirmed-fitting **P4 PETG plate**, four **M3 heat-set inserts** (dimensions to verify), four on-hand **M3 screws** (try M3x6 and washers only after checking engagement), insulated electronic-board spacers, cable strain relief. These are not additional field electrical connectors.

## Temperature: it does NOT go through the ADS1115
R5 bridges J2-1 (+3V3) to J2-2 (GPIO18/DATA). Exactly one pull-up on this cable; the probe itself does not contain one. No resistor in series with DATA; no DATA pull-up to +5V or GND.

## Pressure circuit
```text
J1-3 SIG -- R1 10k -- DIV -- R4 1k -- A0 -- ADS A0
                       |              |
                     R2 10k        C1 100nF
                       |              |
                      MID            GND
                       |
                     R3 4.7k
                       |
                      GND

ADS VDD (+3V3) -- C2 100nF -- GND
```
DIV and MID are solder joints, not connectors. Raw SIG must not bypass the divider. ADS VDD stays at 3.3V. ADDR stays grounded for 0x48; preserve an existing strap, otherwise connect the exposed unconnected ADDR pin to GND. Leave ADS A1/A2/A3/ALERT unused and leave ESP 3V3_EN unconnected.

## Nine inter-assembly wires
These are INSIDE the case; on-board short links are additional. They are not external ports.
| ID | From | To | Purpose |
|---|---|---|---|
| W01 | ESP VSYS | B +5V pad / J1-1 | Pressure power only |
| W02 | ESP 3V3 | B +3V3 pad / J2-1 | Temperature and ADS supply |
| W03 | ESP GND | B GND pad | Common return |
| W04 | ESP GPIO18 | B DATA pad / J2-2 | Temperature data only |
| W05 | ESP GPIO17 | A ADS SDA | I2C data |
| W06 | ESP GPIO16 | A ADS SCL | I2C clock |
| W07 | B +3V3 pad | A +3V3 pad / ADS VDD | Never connect ADS VDD to +5V |
| W08 | B GND pad | A GND pad / ADS GND | Also the divider/capacitor return |
| W09 | B SIG pad / J1-3 | A SIG pad / R1 input | Raw signal goes to R1, not directly to A0 |

GPIO16/17/18 refer to silkscreen GPIO names, not 40-pin header position numbers. Only use the known VSYS rail as pressure +5V; no PoE high-voltage pins on perfboard.

## Assemble in this order
1. Disconnect PoE/USB; label existing sensor cables. Bring electronics to bench, not the pressurized sensor fitting.
2. Dry-fit actual parts and insulated supports. Label J1/J2 and every terminal before turning board over.
3. Build Board B: J1-1->+5V; J1-2 and J2-3->GND; J1-3->SIG; J2-1->+3V3; J2-2->DATA; R5 bridges +3V3 and DATA.
4. Build Board A: R1 SIG-DIV; R2 DIV-MID; R3 MID-GND; R4 DIV-A0; C1 A0-GND; ADS A0 to A0; ADS VDD to +3V3; ADS GND to GND; C2 +3V3-GND. Preserve 0x48 address.
5. Add W01-W09 and label both ends. Inspect and continuity-test while unpowered. Check intended nets, no power-rail shorts, no crossed signals, no solder whiskers and PoE underside clearance.
6. On the bench, field cables disconnected: power by existing PoE. Verify +3V3/+5V pads, Ethernet and ADS 0x48. An unplugged temperature probe must be fault/unavailable; undriven A0 near zero is expected.
7. Power OFF. With actual pressure sensor disconnected, add spare 10k from B +3V3 to J1-3 SIG. Power on: calculated A0 ~1.398V for 3.30V supply. Prepared v5-47k gives ~69.34 provisional PSI; old v4 ~68.62. This is a fake signal, not real pressure. Power OFF; remove spare resistor.
8. When temperature probe is available, connect J2 while off; confirm plausible temperature, hand-warming response, missing-sensor detection and recovery using power-off reconnections.
9. Reinstall; connect the two field cables while PoE is off, secure strain relief, restore PoE. Compare current gauge and readings, not a stale assumed 50 PSI.
10. Do not change sprinkler air pressure to create test points. Verify sensor identity and calibration without disturbing listed system operation. Complete notification/outage tests before operational acceptance.

## Predicted pressure values (not field measurements)
Historical sensor model is 0-150 PSI and 0.5-4.5V at 5V supply; make/model remains unverified.
Ratio = (10000+4700)/(10000+10000+4700) = 0.5951417004.
- 0 PSI -> raw SIG 0.500V -> A0 ~0.298V.
- 50 PSI -> SIG 1.833V -> A0 ~1.091V.
- 150 PSI -> SIG 4.500V -> A0 ~2.678V.
Capacitors are open at DC; R4 produces a small real loading error with the non-ideal ADC and must not be assumed perfect calibration. Actual resistor tolerances, sensor supply/ratiometry, cable drops, ADC loading and gauge uncertainty remain measurement factors.
The divider is not surge/reverse-polarity protection. A broken lower leg or wiring error can still overdrive A0. Keep applied A0 within GND..ADC VDD; gain range +/-4.096V is not a pin-voltage permission. Bench checks cannot certify arbitrary industrial field transients.

## Firmware and project completion
Prepared v5-47k source has the correct nominal ratio and had a successful compile on Oscar; binary SHA256 D3F957B5E8270F30B8140F8035E28D7978764D8BC5FAEDED081825FF4A9F36E7. It has NOT been deployed/validated on the new board. Old v4 field reading was ~0.0003-0.0004V with user gauge ~50 PSI; that fault remains undiagnosed. Do not use the old pressure-v4 launcher expecting the new ratio.
Before an operational release, test/harden ADC-ready and I2C fault handling, truthful sample age, sensor recovery, network recovery and stale data. Use existing verified always-on office infrastructure for UTC-stamped history and an independent offsite heartbeat receiver for site/collector outages. Services and message destinations still require implementation and validation. This guide does not create a monitoring runtime.
Proposed 45F early / under40F urgent cold thresholds need site validation; low-pressure thresholds must not be assumed from nominal 50 PSI. Add persistence, hysteresis, reminder/escalation, missing-sensor, prolonged-condition and recovery handling; test actual delivery. No notifications are active/accepted yet.
The guide is a public static build page, not the sensor dashboard. Keep all live device data/credentials off it.

## Manufacturer sources
- Waveshare board: https://docs.waveshare.com/ESP32-S3-ETH
- Waveshare schematic: https://files.waveshare.com/wiki/ESP32-S3-ETH/ESP32-S3-ETH-Schematic.pdf
- Waveshare pin labels: https://docs.waveshare.com/assets/files/ESP32-S3-ETH-details-15-b9d2e97a5122db37da6be5bac19e29b4.webp
- ADS1115 datasheet: https://www.ti.com/lit/ds/symlink/ads1115.pdf
- DS18B20 datasheet: https://www.analog.com/media/en/technical-documentation/data-sheets/ds18b20.pdf
- DS18B20 pull-up confirmation: https://support.analog.com/en-US/knowledgebase/article/000094969

The original 2024 dashboard and known-working firmware binaries remain unchanged. Do not alter listed sprinkler/fire alarm/heating controls, valves, regulator or piping. This remains supplementary monitoring.
