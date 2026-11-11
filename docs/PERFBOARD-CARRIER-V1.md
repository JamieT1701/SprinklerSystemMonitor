> **SUPERSEDED FOR PHYSICAL BOARD SIZE (2026-11-11):** Jamie has several existing 50 x 70 mm perfboards. Use [PERFBOARD-CARRIER-V2-50X70.md](./PERFBOARD-CARRIER-V2-50X70.md) instead. This v1 plan is retained only as engineering history; do not purchase or cut a 160 x 100 mm board based on it.

# Device Lab sprinkler monitor - perfboard carrier v1 (2026-11-11)

**State: design only - not built, electrically tested, or accepted.** Supplemental monitoring; no connection to any listed sprinkler supervisory, fire alarm, control, or heating circuit. This design preserves the existing 2024 dashboard and the 2026 working firmware.

## Why
Latest field firmware v4 successfully reads riser-room temperature but reports pressure A0 around **0.0003-0.0004 V** and `LOW_INPUT_OR_OPEN_SHORT`, while the adjacent mechanical gauge reads around 50 PSI (user report). Rebuild the crowded enclosure as a removable and diagnosable perfboard carrier with accessible test points. The pressure transducer stays physically installed on the compressor; the electronic monitor is disconnected and brought to the bench.

## Mechanical / placement
- **160 x 100 mm**, 2.54-mm pitch, double-sided **isolated plated through-hole pads** (NOT continuous stripboard). Individual pads do NOT connect along rows.
- Select a plastic enclosure with **minimum 205 x 135 x 65 mm clear USABLE interior after ribs/bosses**, preferably larger if RJ45 plug/cable bend or glands require. Dry-fit actual enclosure first. Cut glands to real cable diameters; provide strain relief; preserve USB, BOOT, RESET and Ethernet service access.
- Waveshare ESP32-S3-POE-ETH main PCB is about **72.8 x 21 mm**, plus separate PoE daughterboard. Mount mechanically on **15-20 mm nylon standoffs** or adapted 3D-printed cradle, avoiding exposed copper under the daughterboard. Verify exact PoE stack height, connector orientation and board mounting centers by physical measurement; do not drill the WaveShare board.
- Suggested conceptual TOP VIEW: ESP+PoE across upper middle/right, RJ45 pointing toward case's roomy side; ADS1115 lower left, analog divider lower center, J1 pressure and J2 temp lower right, test pads along accessible lower edge. This is **not a drilling template**.
- Keep Ethernet/PoE hardware assembled as supplied. Do not route 48V PoE onto any perfboard rails.

## Device wiring (existing working GPIO, do not change)
| Net | ESP32-S3 board | Destination |
|---|---|---|
| +3V3 | 3V3 | ADS VDD, J2-1 (DS18B20 VCC) |
| GND | GND | ADS GND, J1-2, J2-3, divider ground |
| SDA | GPIO17 | ADS1115 SDA |
| SCL | GPIO16 | ADS1115 SCL |
| DQ | GPIO18 | J2-2 (DS18B20 DATA) |
| Sensor +5V | VSYS (previously measured ~5.097V on PoE) | optional F1 then J1-1 |
| Pressure A0 | -- | ADS1115 A0 through R4 and divider below |

The DS18B20 probe already has a 4.7-kohm DATA-to-3V3 pull-up; **do not add a second** without evidence. ADS1115 address was verified at 0x48, leave its address setting as previously functional. A1, A2, A3 unused. **Never use 3V3_EN as a power output.** Verify VSYS on actual physical board before landing the red sensor wire.

## Sensor screw terminals
- **J1 (PRESS, 3 positions, 5.08-mm pitch)**: 1 = +5V OUT (red wire), 2 = GND (black), 3 = sensor analog SIG (green).
- **J2 (TEMP, 3 positions, 5.08-mm pitch)**: 1 = 3V3, 2 = GPIO18 DATA, 3 = GND. Probe remains in riser room; removable field cable.
- Label the positions on the actual board, not just in a drawing.

## Pressure analog netlist
```text
PoE board VSYS (~5V) -> optional F1 PTC ~200mA hold -> J1-1 sensor RED (+5V)
GND ---------------------------------------------> J1-2 sensor BLACK
J1-3 sensor GREEN (SIG) -> R1 10k -> N_DIV -> R4 1k -> N_A0 -> ADS1115 A0
                                     |                          |
                                   R2 10k                    C1 100nF
                                     |                          |
                                   N_R23                       GND
                                     |
                                   R3 5k
                                     |
                                    GND
```
Use 1% through-hole resistors; 5.0k can be replaced with standard **4.99k** if actual values are recorded for calibration. C1 ceramic >=16V. Nominal divider R1 10k / lower (R2+R3) 15k = **0.6**. The 1k R4 and 100nF C1 are ADC series/filter elements and should have negligible DC effect. This simple circuit is NOT rated for arbitrary field-line overvoltage and must be checked before relying on it. ADS1115 A0 must operate between GND and ADC VDD (~3.3V); selecting the 4.096V PGA range does not permit >VDD at its input.

At nominal 50 PSI using unverified historical transducer specifications (0-150 PSI, 5V supply, 0.5-4.5V analog), expected **SIG ~1.83V, A0 ~1.10V**. At 0 PSI A0 ~0.30V; at 150 PSI A0 ~2.70V. These are predictions, not observed voltages.

## Accessible test loops
| Test | Net | Typical expectation |
|---|---|---|
| TP5V | After F1 / J1-1 | ~5V with PoE |
| TP3V3 | ESP 3V3 / ADS VDD | ~3.3V |
| TPGND | Common ground | 0V |
| TPSIG | J1-3 (before R1) | ~1.83V at gauge ~50 PSI |
| TPA0 | ADS A0 (after R4) | ~1.10V at gauge ~50 PSI |

## Optional analog perfboard hole-map (component side)
Use isolated 2.54mm grid labeled columns C01..C16 and rows R01..R14, installed in the designated analog area; verify resistor body lengths, avoid PoE keep-out. These are prototype solder-pad coordinates **not an exact PCB drill drawing**.

| Part | Lead 1 pad | Lead 2 pad |
|---|---|---|
| R1 10k | C02-R02 | C06-R02 |
| R2 10k | C07-R04 | C07-R08 |
| R3 5k | C07-R09 | C07-R13 |
| R4 1k | C09-R02 | C14-R02 |
| C1 100nF | C14-R04 | C14-R06 |

Insulated intentional jumpers / nodes:
- DIV: join C06-R02, C07-R02, C07-R04 and C09-R02.
- MID: join C07-R08 to C07-R09.
- A0: join C14-R02 to C14-R04.
- Sensor SIG from J1-3 to C02-R02.
- Common GND connections from C07-R13 and C14-R06.
- ADS A0 wire to C14-R02.
Do not accidentally connect adjacent copper pads beyond these deliberate jumpers. Insulate any crossing jumpers.

## Bench assembly and acceptance sequence
1. **Power down/disconnect PoE** and all field wiring. Do not loosen the pressure transducer or any sprinkler pressurized fitting. Take only electronic enclosure/board back to bench.
2. Verify enclosure, RJ45 clearance, PoE underside, standoffs, gland positions and cable bends by dry-fit; then drill only the perfboard/enclosure as needed.
3. Solder +3V3/GND distribution, J1/J2, R1-R4, C1 and optional F1; use insulated point-to-point wires. Verify every network with a meter while unpowered, especially no +5V/+3V3/GND shorts or A0-to-GND short.
4. Attach ESP / PoE and ADS module on standoffs/sockets with insulation. Wire GPIO17 SDA, GPIO16 SCL, GPIO18 J2 DATA, power and ground. Preserve existing probe pull-up.
5. Bench test PoE and TP3V3 / TP5V. **With J1 sensor disconnected, A0 near zero is expected** due to the lower-leg resistors; that alone is not ADC failure.
6. **Simulated signal test, field sensor completely unplugged:** power OFF, connect ESP 3V3 through a **temporary 10k resistor** to TPSIG/J1-3. Re-power. Nominal A0 = `3.3 * 15/(10 simulated + 10 R1 + 15 lower) ~1.41V`; provisional firmware may show ~69.6 PSI. This tests ADC signal path, **not transducer accuracy**. Power OFF and remove resistor.
7. With power disconnected, attach real transducer field wires. Reinstall enclosure and verify powered **TP5V, TPSIG, TPA0** safely using test loops. Compare with adjacent mechanical gauge (~50 PSI reported). If TPSIG ~0V, diagnose sensor power/wiring/return before changing firmware. If TPSIG ~1.83V but A0 ~0V, inspect divider or A0 joint.
8. Verify DS18B20 remains healthy, pressure plausibility and fault detection. No freeze, low-pressure or outage notifications are configured or accepted yet.

## References
- Waveshare ESP32-S3-ETH/PoE: https://docs.waveshare.com/ESP32-S3-ETH
- Texas Instruments ADS1115 datasheet: https://www.ti.com/lit/ds/symlink/ads1115.pdf
- Existing Device Lab PR #1: pressure v4 and sensor diagnostics; historical hardware handoff.

**Review gate:** Actual ADS breakout outline, carrier standoffs, enclosure usable dimensions and cable routing must be measured with hardware in hand. Treat this as a bench-buildable prototype guide, NOT a fabricated PCB layout or life-safety monitoring system.
