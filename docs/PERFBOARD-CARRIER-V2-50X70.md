> **UPDATED 2026-11-11 - USE V4 INSTEAD:** The DS18B20 probe has **NO built-in 4.7k pull-up**. The correct design puts **R5 4.7k between 3V3 and GPIO18/DATA on Board B** and uses a second **4.7k as R3** instead of 5k for the pressure divider. See [BEGINNER-BENCH-GUIDE-V4.md](./BEGINNER-BENCH-GUIDE-V4.md) and [the interactive web guide](./index.html). This v2 document is retained only for history; do not assemble the older uncorrected temperature circuit.

# Sprinkler Monitor - two 50 x 70 mm perfboard carrier (v2)
**Design status: planned; not assembled, electrically verified or accepted.**
**Supersedes v1's 160 x 100 mm board/enclosure arrangement.** No firmware modification, sprinkler-controls modification or live alert activation.

## Mechanical
Jamie has several **50 x 70 mm** perfboards. Use **two** for accessible assembly; attach both individually to an insulating baseplate on nylon standoffs. Waveshare ESP32-S3-POE-ETH main board is ~72.8 x 21 mm, so it must mount **beside/above the perfboards on its own standoffs**, not span a 70 mm board. Preserve the factory PoE module, isolate its underside from bare conductors and provide RJ45/USB/BOOT/RESET clearance. Plan enclosure after dry-fit; ~205 x 150 x 75 mm **clear interior** is a planning envelope, not proven minimum.

- **Board A (analog)**: existing ADS1115 breakout, R1/R2/R3 divider, R4 input series resistor, C1 filter, TP-SIG and TP-A0.
- **Board B (field)**: 3-way J1 pressure terminal (+5V, GND, SIG), 3-way J2 DS18B20 terminal (3V3, DATA, GND), TP5V / TP3V3 / TPGND, optional correctly-rated PTC.
- Insulated point-to-point wiring between boards; do NOT solder perfboard edges together.
- Perfboard must have **isolated pads** on 2.54 mm pitch; not stripboard/common copper rows. Inspect actual ADS module footprint before final mounting.

## Existing controller wiring (preserve)
| ESP / net | Destination |
| --- | --- |
| 3V3 | ADS VDD / Board B J2-1 |
| GND | ADS GND / divider return / J1-2 / J2-3 |
| GPIO17 | ADS SDA |
| GPIO16 | ADS SCL |
| GPIO18 | J2-2 DS18B20 DATA |
| PoE-powered VSYS (~5V historical; reverify correct pin) | J1-1 PRESS red (+5V), optional properly rated PTC |
| Board B J1-3 PRESS green SIG | Board A R1 input / TP-SIG |
| Board A ADS A0 | Board A R4 output / TP-A0 |

DS18B20 field probe already has a 4.7 kohm DATA-to-3V3 pull-up; do **not** add another without evidence. **3V3_EN is not a power output**. Never route 48V PoE conductors onto these boards.

## Board A analog netlist
```
J1-3 GREEN SIG -- R1 10k -- N_DIV -- R4 1k -- N_A0 -- ADS1115 A0
                            |                       |
                          R2 10k                  C1 100nF
                            |                       |
                          N_R23                    GND
                            |
                          R3 5k
                            |
                           GND
```
Nominal signal divider 10k / (10k+5k) => 0.6. Historical unverified transducer model 0-150 PSI, 0.5-4.5V output at 5V supply. At ~50 PSI mechanical gauge, predicted SIG ~1.83V and A0 ~1.10V; neither is yet electrically established. ADS analog input constrained by its powered 3.3V rail, not the 4.096V ADC PGA setting.

### Component-side coordinates (only analog subassembly; not whole-board drill template)
70 mm dimension horizontal, grid C01..C26 from left to right and R01..R18 top to bottom; 2.54mm pitch. For each component, place the leads at:
| Component | Lead A | Lead B |
| --- | --- | --- |
| R1 10k | C03-R04 | C07-R04 |
| R2 10k | C08-R06 | C08-R10 |
| R3 5k | C08-R11 | C08-R15 |
| R4 1k | C10-R04 | C14-R04 |
| C1 100nF | C14-R06 | C14-R10 |

Connect with **insulated deliberate jumpers**:
- N_DIV: C07-R04, C08-R04, C08-R06, C10-R04.
- R2/R3 midpoint: C08-R10 and C08-R11.
- N_A0: C14-R04 and C14-R06, then ADS A0.
- Ground: C08-R15 and C14-R10 to the common GND.
- J1-3 SIG from Board B -> C03-R04 and TP-SIG. TP-A0 at C14-R04.
The actual ADS breakout mounting and connector hole centers require physical dry fit; do not blindly drill from conceptual shading. Check mirroring when soldering from underside.

## Bench/field acceptance
1. Disconnect PoE and unplug electronics field cables before bringing the enclosure back to bench. **Do not disturb the pressure transducer mounted on sprinkler piping, listed fire equipment or pressurized connections**.
2. Dry-fit ESP32/PoE, two boards, standoffs, lid, cable glands, RJ45 bend clearance. Assemble with insulated wire and labels; keep analog wiring away from PoE components.
3. Unpowered continuity check of all intended nets; verify no A0-GND, 3V3-GND or 5V-GND shorts.
4. Powered bench test with real pressure sensor **unplugged**: I2C ADS1115 detection at 0x48, TP5V/TP3V3, DS18B20 where present. Near-zero A0 with field transducer unplugged can be normal due to grounded divider.
5. Isolate ADC test: power **OFF**; connect 3V3 through a temporary 10k resistor to Board B J1-3 SIG with field sensor unplugged; power ON. Expected A0 ~= 3.3*15/(10 test+10 R1+15 lower)=**1.41V**, provisional PSI ~**69.6**. This is a divider/ADC test, **not** pressure calibration; power OFF and remove simulator.
6. Power OFF, reconnect field wires at warehouse; measure TP5V, TP-SIG, TP-A0 while powered using accessible safe test loops. If SIG ~0V with healthy 5V, investigate transducer/cable/ground. If SIG ~1.83V but A0 ~0V, inspect divider/A0 connection. Gauge comparison required to accept pressure.
7. Verify stable DS18B20 and ADC readings. Freeze alerts, low-pressure alerts, missing-heartbeat alerts, and delivery remain **not operationally accepted**.

## Existing evidence / source
- Field pressure diagnostic v4 read A0 ~0.0003-0.0004V, pressure input LOW_INPUT_OR_OPEN_SHORT, while adjacent mechanical gauge approximately 50 PSI (user report).
- Original 2024 dashboard must remain intact; sensor firmware and rollback remain unchanged by this hardware design.
- Waveshare board and PoE docs: https://docs.waveshare.com/ESP32-S3-ETH
- TI ADS1115: https://www.ti.com/lit/ds/symlink/ads1115.pdf

User-facing **revised** 4-page PDF, editable SVG layout, BOM.csv and detailed assembly guide generated in conversation. **No claim of a manufactured PCB or validated enclosure dimensions.**
