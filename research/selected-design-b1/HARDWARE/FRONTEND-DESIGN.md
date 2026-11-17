# B1 functional electrical contract — not an approved schematic

**2026-11-16 · Draft architecture/net requirements, not PCB files or wiring instructions.** Use only on an isolated, power-limited bench after independent circuit review. **Never connect this design or test faults directly to an in-service sprinkler line.**

## 1. Simplified architecture

```text
                     [Existing factory-certified PoE hardware]
Ethernet + 802.3af --> [Waveshare ESP32-S3-POE-ETH 28771] -----> [TLS/HTTPS uplink]
                          |  +5V measured / +3V3 logic
                          |             |
                          |             +--> I2C16/17 --> [ADS1115 3.3V]
                          |             |                     AIN0: shunt sense
                          |             |                     AIN1: L+ terminal monitor
                          |             |                     AIN2: loop-source monitor
                          |             |                     AIN3: 2.048V check ref
                          |             +--> GPIO18 --> [Protected 3-wire DS18B20]
                          |
                          +5V -- fuse --> [5->24V BOOST PROPOSAL] --> [CONTINUOUS-SHORT
                                                                         CURRENT LIMIT]
                                                                       |     (unresolved)
                                                               [24V L+ FIELD J1.1]
                                                                       |
                                                       [2-wire 4-20mA transmitter]
                                                                       |
                                                            [RETURN FIELD J1.2]
                                                                       |
                                                      [100 OHM PRECISION SHUNT]
                                                                       |
                                                         ANALOG GROUND (one point)
```

**NO physical circuit is released**; the 24V supply, current limiter, surge/ESD protection and ADC clamps are candidates for schematic review. The above diagram communicates required *functions*, not validated topology, mechanical placement, grounding/isolation or allowable miswire survival.

## 2. Minimum number of external connections

| Connection | Pins/role | Status |
|---|---|---|
| P1 PoE / Ethernet | External female RJ45 panel bulkhead to existing factory Waveshare RJ45 via short interior patch lead | Amphenol LTW RCP-5SPFFH-SCM7002 candidate, actual PoE/EMC/ground/strain/cap testing required |
| P2 TEMP | External female M8 A-coded 3-pin to internal J2, 3.3 V protected / DS18B20 DQ / GND | Binder 76 6518 1111 00003-0200 candidate, male cordset contact numbers TBD |
| P3 PRESS | External female M12 A-coded 4-pin: **P3 contact1 protected +24V, contact2 IRETURN to 100ohm shunt, contacts3/4 NC** for ProSense SPTD25 | Binder 76 4332 0011 00004-0200 candidate; confirm connector cavity orientation/3m cordset pin-to-pin; eFuse/miswire protection NOT qualified |
| No other outputs | **No dry valve, compressor, heater, FACP or supervised fire-alarm connections** | Mandatory boundary |

The original live R6 system has a **different** three-wire pressure terminal and ADC divider; this B1 design is not interchangeable.

## 3. ADC contract (one ADS1115, 3.3V)

**Channels:** AIN0 shunt, AIN1 J1 L+ voltage via protected divider, AIN2 boost/loop supply via separately protected divider, AIN3 stable 2.048V reference check. 16-bit single-ended sampling, proposed PGA ±4.096V, 128–475 samples/sec *shared across multiplexed channels* pending throughput/noise testing. The ADC cannot continuously measure four channels simultaneously; software must time-multiplex with settling checks.

**Electrical limits:** ADS1115 at 3.3V has recommended analog input range **0..3.3V**, absolute maximum approximately **GND−0.3..VDD+0.3V**. Selecting ±4.096 or ±6.144V PGA does **NOT** raise pin voltage tolerance. Manufacturer source: https://www.ti.com/product/ADS1115.

**Current shunt** `R_SHUNT=100 Ohm, 0.1%, <=25 ppm/°C, target >=0.25W`:
- 4mA = 0.400V, 12mA = 1.200V, 20mA = 2.000V, 26mA = 2.600V.
- Nominal resolution at ±4.096V PGA: 0.125mV/count, giving 1.25 microamp/count; 0–150psig equivalent ~0.01172psi/count. **Digitization resolution is not accuracy**. Component tolerance and transmitter total error dominate.
- Heat at 26mA = 0.0676W; **a 24V hard miswire can dissipate 5.76W at 100 Ohm** without upstream protection, destroying a naive shunt.

**Voltage diagnostic divider candidate**: `270k high / 22k low` = ~0.0753425 of monitored source. 24V→1.808V; 36V→2.712V; 40V→3.014V; 44V→3.315V (>ADC VDD). **External fault clamps, RC filtering, divider impedance/ADC loading and PCB isolation must be analyzed and bench validated.** These resistors alone do NOT make an industrial protected input.

**Reference**: 2.048V shunt reference (LM4040 class) at AIN3 is a proposed reference-check signal. Its output current, bias resistor, 3.3V rail behavior and ADC error budget require current datasheet verification. A reference on the **same** ADC is not a fully independent redundant channel.

## 4. Loop-supply power path — critical open circuit-design item

- Factory Waveshare PoE/RJ45 module already supplies the development board; owner previously measured around 5.097V at prototype VSYS, which is a one-site observation, **not a production guaranteed rail/load limit**.
- A candidate **Pololu U3V9F24, item 5588** is a 24V **boost module** from 5V, not a safe, short-proof industrial field interface. Published input 2.6–20V; 24V output; reverse input protection **no**. Current limit on the **switch input** does not constitute **26mA continuous current limit on J1 L+**. Its datasheet/stock/thermal behavior require evaluation: https://www.pololu.com/product/5588/specs.
- 24V×26mA = **0.624W** loop output maximum target. If boost efficiency were 80% at 5V, this draws an *additional* **156mA** at 5V, before controller, Ethernet and transients. **80% is an assumption, not a measurement**.
- **Hard release blocker:** Select/draw a separate output-stage current limiter, potentially hardware sense/disable and thermally safe short-fault response, protecting both PoE rail and sensor. It must keep the supply safe with J1+ tied to J1− or GND **indefinitely at max rated ambient**, and after reverse/24V miswire (subject to defined tested service envelope). Do not rely on a PPTC fuse alone or ESP firmware to make the hardware safe.
- At low rail 18V, illustrative 3V limiter loss + 0.5V cable + 2.0V shunt + 8V transmitter minimum leaves ~4.5V margin. Real figures are vendor-MPN and current/temperature dependent; remeasure.
- Use independent source rail, field L+ and current diagnostics to detect undervoltage, open, probable short-to-ground or measurement faults. Do **not** promise unique fault classification in every short condition.

## 5. Device GPIO and validation contract

| Logical function | ESP32-S3 | Source | Risk |
|---|---|---|---|
| Ethernet SPI | SCK13, MISO12, MOSI11, CS14, reset9, IRQ10 | Waveshare product docs | Reserved factory wiring; do not reuse |
| ADS SDA, SCL | GPIO17, GPIO16 respectively | Existing prototype wiring known; confirm manufacturer pin availability | Confirm no other onboard resource interference in B1 |
| DS18B20 DQ | GPIO18 | Existing prototype | Field protection, pull-up and signal integrity to be designed |
| 24V loop-enable | **TBD** | No fixed GPIO yet | Hardware short-limiter must work without firmware |
| Power-loss detect | **TBD** | 5V rail sensing/ADC or dedicated circuit | A dead PoE device cannot send power-loss alert; cloud detects silence |

PoE module sourcing, 2x20 pin socket pitch, RJ45 cable bend radius and enclosure stack are to be *measured* before KiCad footprints or mechanical fitting. Do not assume the current P4 mount fits the added industrial loop electronics.

## 6. Fault-classification requirements

Current-only thresholds follow NE43 ranges as a guideline, subject to **actual transmitter configuration** (some transmitters do not implement the same failure signalling). Logic should err toward **PRESSURE UNKNOWN** rather than mislabel 0psi or "normal".

- `I <0.5mA` and near-full L+ terminal voltage: **loop open/unpowered transmitter suspected**, not proven cut.
- `I <0.5mA` and collapsed L+ (loop rail itself healthy): **possible grounded cable**.
- `0.5–3.6mA`: **invalid low-fault**.
- `3.6–4.0mA`: **under-range** flagged; not a certified valid 0psi.
- `4–20mA`: nominal current-to-PSI range where *transmitter/ADC/system quality checks pass*.
- `20–21mA`: over-range flagged; do not display normal.
- `>=21mA`: **high-fault**, NOT automatically a physical short.
- Transmitter differential below minimum: **compliance/voltage fault**.
- ADC/reference/loop rail/temperature stale: **INVALID**, never normal.

The executable [host-only prototype classifier](../FIRMWARE/loop_classifier.py) and [synthetic tests](../VERIFICATION/test_loop_classifier.py) validate the logic's branch coverage only. The actual circuit may produce different symptoms; test against real faults before accepting any classifier.

## 7. Remaining schematic/ECO gate before board order

1. Select exact sensor with **range/proof/burst/port/wetted parts/power/current**, contractor-approved system-side port and max safe transient conditions.
2. Qualify factory PoE module 5V available budget at startup, low-temperature, network load, with and without boosted current loop.
3. Draw **genuine** current limiter / eFuse, return sense, ESD/transient and reverse wiring protection; simulate test current and component failure **including power-off and ADC unpowered**.
4. Show ADC pin current and voltage safety under **every external field short, overvoltage and 24V miswire**; include TVS clamp leakage/thermal, rail backfeeding, resistor power and capacitor ratings.
5. Choose reference, resistor/TVS exact MPN and second sources. Produce KiCad native hierarchical schematic; independent ERC and peer review.
6. Then board outline/footprints with physical measurements, DRC, fab view and actual measured QA. **No fabrication release** until independent review and owner spending approval.

## 8. New manufacturer-supported current-limiter candidate (research only)

TI's **TPS2662** family is an active **4.5–60V, 25mA–880mA adjustable** eFuse with overvoltage, reverse protection and multiple fault-response variants: https://www.ti.com/product/TPS2662. This is a **credible candidate for a dedicated J1 L+ high-side output stage**, unlike the TPS2660 family which has a 100mA minimum limit. However, the TPS2662 comes in a small **10-pin VSON (3x3mm)**, not a hand-friendly through-hole package. A prospective workshop design should use a bought evaluation board for bench proof or outsource SMT for the tiny device.

**Not designed/accepted:** Exact TPS2662 variant, current-limit programming R, input/output reverse/backfeed behavior, eFuse fault latch/auto-retry configuration, thermals and rail behavior under continuous short. A 35-45mA setpoint is a **candidate engineering study**, not a final device rating; even 35mA x 24V represents up to 0.84W being dissipated by the limiting path if output is shorted. A thermal-shutdown or foldback circuit may provide protective behavior, but it must be proven with a short-duration and sustained worst-case fault matrix, downstream converter brownout and nearby electronics. **No supplier order or physical prototype is authorized by this note.**

## 9. Exterior connector redesign B1 Revision B (2026-11-16)

The owner chose plug-in external service rather than feeding cables through glands into the case: **P1 RJ45 PoE, P2 M8 A-coded 3-pin room sensor, P3 M12 A-coded 4-pin industrial current-loop pressure sensor**. Distinct fittings prevent accidental pressure (+24 V current-limited loop) to 3.3 V digital temperature misconnection. Internal J1/J2 screw terminals remain factory/service only; never need to open the lid for normal sensor swap. The future **AUX** is an undrilled reserve on the right wall without power/wiring. See [CONNECTOR-REDESIGN.md](CONNECTOR-REDESIGN.md).

Mating cable male ends, manufacturer contact numbers, RJ45 full PoE and shield behavior, IP mated/cap details, actual Hammond OEM wall thickness/spotface, cable bend radius, surge/ESD/power-off backfeed and current-loop output short protection are **NOT electrically or physically accepted**. Do not hot-unplug sensors under load until the connector vendor's instructions and fault testing allow it. Target overall IP54 only **after** complete assembly test. NPT process fittings apply to the remote pressure transducer/tap; no plumbing fittings are proposed on the B1 electronic enclosure.

## 10. Preferred manufacturer-qualified **sensor identity** — not installed

Preferred design sensor model: **ProSense SPTD25-20-0100H**, 0-100psig 4-20mA 2-wire 8.5-36V, 1/4 MNPT, M12 male; external 3m M12 female-to-male patch cord **CDP12-0B-030-AA** and proposed B1 P3 female. For this particular SPTD25 model, verified **pin1+ / pin2 current-return / pin3 NC / pin4 NC** (NOT generic 1+/3-). Other 4-pin M12 devices have different pin assignments even when they fit; notably LPPT25 has pin2 ground, pin3 or pin4 V-. **NO substitution without full separate harness qualification.**

SPTD manufacturer permits **3-4mA non-linear under-range** and **20-25mA non-linear over-range**: these currents cannot automatically be labeled NE43 sensor fault. Host-only profile in `../FIRMWARE/sensor_profiles.py` handles these as pressure UNKNOWN without inventing PSI or false healthy states. Verified bench-only interface minimum supply is 8.5V and max rated pressure 100psig (proof 250psig), but a qualified sprinkler installer must still approve site's range/tap.

Power-stage candidate refined: TI **TPS26625DRCR** 24V high-side eFuse (auto-retry and output reverse blocking) with **165kΩ nominal R_ILIM (~40.22mA theory)**; its quoted ±5% limit specification is at 880mA, not at 40mA. Does **not** establish safe indefinite-short operation or PoE boost protection. Need real exact schematic/pinout, derating, thermal/fault instrumentation and ADS power-off protection before fab. [Source evidence](PRESSURE-SENSOR-SELECTION.md).
