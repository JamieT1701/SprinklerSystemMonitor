# Dry-pipe riser monitor: independent Round-1 engineering proposal (adviser-claude)

**Status:** This is a design proposal only. Nothing has been built, simulated, bench-tested, priced by a vendor quote or committed to GitHub. Part numbers are early picks made before any schematic exists. Each one still needs checking against the current datasheet, lifecycle status and FCC grant. All costs are engineering estimates and are labelled that way.

---

## 1. TL;DR: recommended architecture

**What the device must do (preliminary):** This is a supplementary monitor. It is not listed and does not replace required devices.
- **Pressure.** It continuously measures the dry-pipe system's air pressure. It warns when pressure is low, high, falling fast, or projected to cross a threshold. It also warns when the readings look like the valve has tripped.
- **Cold.** It measures riser-room air temperature and warns when the room stays cold for a set time.
- **Silence counts as a fault.** If the device stops reporting or reports bad data, that is an alert, not "normal". Stale or invalid values are never displayed or evaluated as normal. An offsite "dead-man" check raises SITE OFFLINE when the device cannot report.

**Recommendation: Architecture A, a wired-first riser monitor (one PCB, two build options).**
- **Processor and network.** An ESP32-S3 module. Wired Ethernet (W5500 chip) is the main link, with optional power over the same cable (802.3af PoE). Wi-Fi is the fallback.
- **Pressure sensor.** An industrial stainless 2-wire 4–20 mA pressure transmitter, 0–150 psig by default.
  - It connects through a current-limited input circuit that diagnoses open wire, short, short-to-ground, leakage and low supply voltage at the sensor.
  - A 16-bit ADC reads it and continuously checks itself against an independent voltage reference.
- **Temperature.** A remote Sensirion temperature/humidity probe for the room. An internal temperature/humidity sensor watches for condensation inside the enclosure. An optional NTC probe can sit at the coldest spot.
- **Power and safety of the firmware.** Input is a Class 2 12–24 VDC supply or PoE. An external hardware watchdog resets the device if it hangs. Firmware uses secure boot and flash encryption. Updates are signed, use two firmware slots and roll back automatically if a new version fails.
- **Cloud and alerts.**
  - The device sends data over HTTPS to a small managed backend.
  - Users get an installable web app (PWA) dashboard.
  - Alerts go out by Web Push, SMS and voice call, and escalate until someone acknowledges them.
  - Two independent offsite "dead-man" checks watch for silence: device→third-party monitor, and backend→third-party monitor.
- **A+ build option.** For sites where the network or power is unreliable, an LTE-M cellular daughterboard plus backup power that tolerates cold. The reason: a site power cut stops the compressor, the room heater and usually the network at the same moment. That is exactly when monitoring matters most.

**Why not the other options first:**
- **B (battery-powered cellular node)** is nearly tied. It wins if the riser room has no dependable network.
- **C (Linux gateway with off-the-shelf I/O modules)** is the fastest bench prototype, but the weakest product to maintain.

**Planned GitHub location** (not created; no repository access this round):
- Branch: `research/independent-adviser-claude`
- Folder: `research/independent-designs/adviser-claude/`
- A draft PR from that branch.

**Work I can do now, without owner answers:**
- Input-circuit schematic, plus SPICE simulation of the fault cases.
- Error and power budgets.
- The alert-engine state machine, with replay tests on synthetic compressor, leak and trip data.
- Backend schema, a PWA skeleton, the test-fixture design and the cost model.

**On hold until answered:**
- Which comms and power parts to fit (question 1).
- Sensor range and alarm thresholds (needs valve data).
- Where the enclosure goes.

**First interview question (§9):** What power and network service actually exist inside the closed riser room, or could practically be installed there?

---

## 2. Measurable product requirements and unknowns

### 2.1 Requirements (proposed targets; owner to confirm)

| ID | Requirement | Proposed target | How verified |
|---|---|---|---|
| P1 | Pressure range | 0–150 psig default. Proof pressure ≥300 psi, so a 200 psi hydrostatic test cannot damage it. 0–300 psig variant for the water-supply side or fire-pump systems. | Datasheet, plus the contractor confirming the maximum system and test pressures |
| P2 | Accuracy | ≤±1.5 psi total from −20 to +50 °C. ≤±0.75 psi at 15–25 °C after calibration. | Pressure-manifold test against a reference gauge at least 4× more accurate |
| P3 | Resolution / noise | ≤0.02 psi resolution; ≤0.05 psi RMS noise on the 1 Hz output | Bench capture |
| P4 | Stability | Drift ≤0.5 psi/year, made visible by annual comparison against the mechanical gauge | Field-check records in the dashboard |
| P5 | Sampling and latency | Raw sampling ≥10 Hz, processed output 1 Hz. Local state change ≤2 s after the persistence timer expires. Cloud has the event ≤15 s later when online. | Timestamp traces |
| T1 | Temperature | Accuracy ±0.5 °C (±1 °F) from −20 to +20 °C; readable from −40 to +60 °C; 0.1° resolution | Ice-point check plus a reference sensor |
| T2 | Cold logic | Threshold, persistence 1 min–24 h, hysteresis and severity all configurable. Shows "below X for hh:mm". | Replay tests |
| A1 | Alert latency | Backend sends the first notification ≤60 s (95th percentile) after a condition is confirmed. Provider delivery time tracked separately. | Weekly synthetic end-to-end test |
| A2 | Offline detection | SITE OFFLINE ≤10 min by default (3–60 min configurable), raised by a path that does not depend on the device | Unplug test |
| A3 | Escalation | Critical alerts repeat and escalate until acknowledged. Quiet hours never suppress them. | Acceptance test |
| A4 | Stale never shown as normal | Any value older than 3× its report interval shows grey "STALE" with its age. Invalid values show as a fault, never as a number. | UI tests |
| D1 | Data retention | ≥7 days buffered on the device; 1-min data kept ≥2 years; events kept ≥7 years (configurable) | Design review |
| E1 | Environment | Operates −20 to +50 °C (goal −30 °C) with condensing humidity outside the box. IP66 enclosure. Inside humidity monitored. | Cold soak and condensation test |
| E2 | ESD/surge immunity (design targets) | IEC 61000-4-2 ±8 kV contact / ±15 kV air on reachable ports. Fast-transient and surge levels (61000-4-4 / -4-5) on field cables. | Pre-compliance lab |
| W1 | Power | 12–24 VDC Class 2 (works 9–30 V; survives −30 V reverse and a 40 V transient) or 802.3af PoE. ≈1.2–1.5 W typical, ≤3.5 W max. | Bench |
| W2 | Field-wiring abuse | Survives ±30 VDC on any field terminal indefinitely. A 120 VAC miswire is out of scope and the label says so. | Fault-injection tests |
| S1 | Security | Unique identity per device; no default passwords; signed boot and updates; TLS 1.2+; multi-factor login for admins; audit log | Review and light penetration test |
| R1 | Device availability | ≥99.9% monthly, excluding site power and network outages | Fleet statistics |
| M1 | DIY build | No BGA chips and no pitch below 0.5 mm. Passives 0603 or larger. RF and PoE parts bought as pre-made modules. Fixture test ≤10 min hands-on. | Time study |
| C1 | Cost | Device and monthly cost targets still to be set with the owner (U8) | — |

### 2.2 Unknowns, in priority order

| # | Unknown | Why it matters | Working assumption until answered |
|---|---|---|---|
| U1 | Power, network and cellular signal inside the riser room | Decides A vs A+ vs B, PoE, and where the enclosure goes | A 120 VAC outlet exists; Ethernet uncertain |
| U2 | Valve make and model; manufacturer's required air band; trip point; compressor or air-maintenance-device type and cut-in/cut-out pressures | Thresholds, trip-signature logic, sensor range | Thresholds left unset; the dashboard shows "UNVERIFIED" |
| U3 | Approved tap point, port size, contractor involvement | Fittings, isolation valve, flow-limiting orifice, whether a trip can be detected | 1/4" NPT on the system-side air, through a tee the contractor installs |
| U4 | Room's temperature history, heater, exterior walls or doors | Cold-alert defaults and the device's temperature rating | Down to −20 °C is possible |
| U5 | Cable runs: tap→enclosure and enclosure→network switch | Cable type; whether PoE reaches | Sensor ≤10 m; Ethernet ≤90 m |
| U6 | Existing listed supervisory switch, fire alarm panel and central station | Avoid duplicate or confusing alarms; must not interfere | A listed low-air switch exists and is monitored |
| U7 | Who gets alerts, after-hours escalation, contractor's role | Escalation policy | Owner plus one backup contact |
| U8 | Acceptable device price and monthly cost | Architecture choice and transmitter grade | Device ≤$500, ≤$10/month |
| U9 | Plans to sell commercially, and multi-site timing | How much to spend on compliance; when multi-tenant features are needed | Single site now; small pilot later |
| U10 | Workshop equipment on hand (reflow, microscope, calibrated pressure reference, loop calibrator) | Tooling budget | None assumed |
| U11 | Interest in a water-supply pressure channel or compressor run-current sensing | Second input channel; leak analytics | Hardware provided for, not required |
| U12 | Backup-power preference; is there a generator? | Battery design | None |

### 2.3 Interview record (receipts)

| Q | Topic | Status |
|---|---|---|
| Q1 | Riser-room power, network and cellular (U1) | **Asked (§9) – awaiting answer** |
| Q2 | Valve and compressor data, plus contractor-confirmed normal and trip pressures (U2) | Queued |
| Q3 | Approved tap point and contractor engagement (U3) | Queued |
| Q4 | Temperature history and heater (U4) | Queued |
| Q5–Q8 | Recipients, costs, commercialization intent, tools (U7–U10) | Queued |

---

## 3. Three architectures and the weighted comparison

### 3.1 The options

| | **A – Wired-first ESP32 monitor** | **B – Battery-powered cellular node** | **C – Linux gateway with off-the-shelf I/O** |
|---|---|---|---|
| Core | ESP32-S3 module + W5500 Ethernet (optional PoE), Wi-Fi fallback | Low-power cellular chip (nRF9151-class) or a small MCU plus an LTE-M module | Industrial Raspberry-Pi-class DIN-rail controller |
| Pressure | 2-wire 4–20 mA transmitter; full loop diagnostics | Voltage-output (0.5–4.5 V) transmitter switched on for about 30 ms every 10 s | Bought 4–20 mA / Modbus analog input module |
| Temperature | Remote SHT45 temp/humidity probe + internal sensor + optional NTC | Sensor on the board (no self-heating) | USB or RS-485 probe |
| Power | Class 2 DC or PoE; external backup optional (A+) | Lithium (Li-SOCl₂) D-cell pack, or 12 V with lead-acid backup | Mains + UPS add-on board |
| Backhaul | Site network over HTTPS (A+: LTE-M fallback) | LTE-M / NB-IoT on an IoT SIM | Site network + outbound tunnel |
| Reporting / offline detection | 60 s reports / alert after 5–10 min | 5–15 min reports + immediate events / alert after 15–45 min | 60 s / 5–10 min |
| Electronics cost excl. transmitter at qty 100 *(est.)* | $60–110 | $90–160 | $200–400 |
| Typical power | ≈1.2–1.5 W | <1 mW average | 4–8 W |
| Keeps working through a site power + network outage | Only with UPS-backed PoE and network, or A+ | Yes | Only with UPS and network |
| Main risks | Depends on the site network | Weak cellular signal indoors; battery behaviour in cold; carrier certification; leadless RF module to solder | SD/OS maintenance; cold rating; slow boot; patching burden |

**Benchmark, not a candidate:** a listed low/high air-pressure supervisory switch (for example the Potter PS40 series; verify) on a listed fire-alarm communicator. That is the compliant baseline the owner may already have. It gives a yes/no alarm but no trends.

### 3.2 Weighted scoring (1–5 scale; engineering judgment, not measurement)

| Criterion | Weight | A | B | C | A+ |
|---|---|---|---|---|---|
| Alert dependability, including self-failure detection | 20 | 4 | 4 | 3 | 5 |
| Pressure accuracy and sensor diagnostics | 15 | 5 | 4 | 4 | 5 |
| Cold and condensation robustness | 10 | 4 | 4 | 3 | 4 |
| Power and connectivity resilience | 15 | 3 | 5 | 3 | 5 |
| DIY build, test and repair | 15 | 4 | 3 | 5 | 3 |
| Device + recurring cost | 10 | 4 | 3 | 3 | 3 |
| Supply chain and second sources | 5 | 4 | 3 | 3 | 4 |
| Security and maintainability | 5 | 4 | 4 | 2 | 4 |
| Compliance path | 5 | 3 | 3 | 3 | 2 |
| **Weighted total (out of 100)** | | **79** | **76** | **68** | **83** |

**Why A wins:** A is the platform and A+ is a set of parts you fit to the same board. Most of A's strengths come from the 4–20 mA loop: the 4 mA "live zero" lets broken wiring be detected, wire resistance doesn't affect the reading, and transmitters from many vendors are interchangeable. Its other strengths are an Ethernet path the user doesn't have to maintain, a low parts count, no recurring SIM fee, and a security surface small enough to audit.

**What would change the result:** If question 1 shows there is no practical Ethernet and only weak Wi-Fi, B (or A+ on cellular only) becomes the winner. C is still useful as a one-week throwaway bench rig for checking the alert logic.

---

## 4. Recommended design (A / A+): block-level detail

### 4.1 Block diagram

```
FIELD (Class 2)                       MAIN BOARD                                   NETWORK
PT1 4–20 mA ──L+/L−──► Loop input ×2: PTC→TVS→back-feed diode←26 mA limiter←24V boost
(PT2 optional)         sensor terminals → 100Ω 0.1% shunt → ADS1115 #1 (I2C0)
                       high-side current monitor (leakage) ─────────┘
SHT45 probe ─I2C1(470Ω+ESD)─►         ESP32-S3-WROOM-1 ◄─SPI─► W5500 ─► PoE-capable RJ45 ──► switch on UPS
NTC (optional) ─► ADS1115 #2 (2.048 V reference check, supply rails, NTC)
                                       ext. watchdog (TPS3823)  │ UART header ─► LTE-M daughterboard (A+)
DC IN 12–24V ─eFuse(OVP/UVLO/reverse)─TVS─┐                     │ USB-C service (inside box only)
PoE PD module 12V ────────────────────────┴─OR→ bus ─► 3.3V SIP regulator ; ─► 24V loop boost
LEDs: PWR / NET / ALARM   Button: wake / test / provisioning   Optional: button-woken 1.3" OLED
```

### 4.2 Key parts (to verify before the schematic)

| Function | Primary choice | Second source / fallback | Notes |
|---|---|---|---|
| MCU and radio | ESP32-S3-WROOM-1 (N8/N16, rated −40 to +85 °C) | -1U version (external antenna); ESP32-WROOM-32E redesign | Some octal-PSRAM versions are rated only to +65 °C, so avoid them. Use the module's FCC modular approval. |
| Ethernet | WIZnet W5500 (LQFP-48, hand-solderable) + 25 MHz crystal | Davicom DM9051 or Microchip KSZ8851SNL (Espressif has Ethernet drivers for all three) | Lay out an alternate footprint. |
| RJ45 jack | 10/100 jack with built-in magnetics and PoE centre taps | ≥2 vendors | Pinouts differ between vendors, so lock the footprint early. |
| PoE | Silvertel Ag99xx 12 V isolated 802.3af module (through-hole) | Off-the-shelf PoE splitter feeding DC IN | Optional part. Request Class 2. |
| Input protection | 60 V eFuse with over-voltage, under-voltage and reverse-polarity protection (TI TPS2660 class) + SMBJ33A TVS + LC filter | Discrete P-FET protection circuit | |
| 3.3 V supply | SIP-3 switching regulator rated ≥36 V input (e.g., Traco TSR 1-2433) | Other pin-compatible SIP-3 parts; check their maximum input voltage | 1 A |
| 24 V loop supply | MC34063A boost (made by several vendors) + LC filter | TPS61170-class boost | If the input is above 24 V, the loop gets roughly the input voltage instead (≤30 V); fine for transmitters. |
| Loop current limit | LM317L set as a ≈26 mA current limiter (47 Ω) | Two-transistor limiter footprint | Several vendors; has thermal shutdown. |
| Leakage detection | High-side current-sense amplifier rated ≥40 V common-mode (TI INA190 class; verify) with ≈5 Ω sense resistor | Leave unfitted (loses leakage detection only) | |
| ADC | TI ADS1115 ×2 (addresses 0x48, 0x49), 16-bit | ADS1015 is pin-compatible (12-bit, ≈0.1 psi steps: an emergency substitute); MCP3424 on an alternate footprint | Don't use the ESP32's own ADC for pressure. It is only a coarse cross-check. |
| Self-check reference | LM4040-2.048 0.1% reference | Equivalent from another vendor | Read continuously by an ADC channel. |
| Shunt resistor | 100 Ω, 0.1%, ≤25 ppm/°C thin film, ≥0.5 W (2010 or 2512 size) | Multiple vendors | Sized to survive a miswire until the fuse trips. |
| Room temperature/humidity | Sensirion SHT45 with factory PTFE filter membrane, on the remote probe | SHT41 (same footprint); TI HDC3022 (has a filter) | Every reading is CRC-checked. |
| Internal temperature/humidity | SHT40 | HDC302x | Detects condensation inside the enclosure. |
| Watchdog | TI TPS3823-33 (≈1.6 s timeout, reset supervisor) | TPS3828 or another vendor's part | |
| Secure element (optional) | Microchip ATECC608B (SOIC-8) | Leave unfitted; keep the key in encrypted flash | |
| ESD protection | Low-capacitance TVS arrays (RClamp0524P / TPD4E05 class); USBLC6-2 on USB | Equivalents | |
| Connectors | Pluggable terminal blocks; M12 A-coded 4-pin panel jacks for sensors | Multiple vendors | Lets a technician swap a sensor in the field. |

### 4.3 Pressure sensor and tap

**Why 4–20 mA:**
- A healthy loop never reads below about 3.8 mA, so a broken wire shows as a fault instead of looking like 0 psi.
- Cable resistance doesn't change the reading.
- The 4–20 mA standard is itself the second source: transmitters from many vendors are interchangeable.

Voltage-output (ratiometric) sensors are kept for B. Digital RS-485/Modbus transmitters are a possible future option.

**Transmitter specification:**
- 316L stainless wetted parts, welded or sealed, 1/4" NPT male.
- 0–150 psig; proof pressure ≥300 psi.
- 2-wire 4–20 mA, supply 9–30 V, reverse-polarity protected.
- Accuracy ≤±0.25% of full scale (best-fit line). Total error band ≤±0.5% of full scale over a compensated range that includes −20 °C.
- IP65 or better with an M12 connector; electronics insulated from the case; serial-numbered calibration certificate.
- Candidate families to qualify: WIKA A-10, Danfoss MBS 3000, TE M3200, Gems 3100, Dwyer 626. Check current part numbers, temperature compensation and lead time.

**Tap (contractor's decision and work):**
- Place it on the system-side air: a tee at the dry-valve air gauge port, keeping the existing gauge, or the air line downstream of the air-maintenance device.
- Include an isolation valve and a restricting orifice or snubber. If the transmitter ever fails catastrophically, the orifice keeps the leak smaller than the air supply can replace.
- Mount it so no condensate can sit and freeze on the diaphragm. Leak-test after installation.
- If the tap is upstream of the air-supply check valve, trip detection won't work (only low/high).
- Never hang loads on the sprinkler piping: NFPA 13 prohibits supporting non-system parts from it.

### 4.4 Loop input circuit and fault classification

**Loop voltage budget:**

| Item | Voltage |
|---|---|
| Supply | 24 V |
| Current limiter (in dropout) | −≈3 V |
| Sense resistor, protection | −≈0.6 V |
| Shunt (2.0 V at 20 mA) | −2.0 V |
| 100 m of 22 AWG cable | −≈0.2 V |
| **Left at the transmitter** | **≈18 V** (typical transmitters need 8–12 V) |

**What the device measures on each channel:**
- Shunt current (I_ls), via a 10 kΩ + 100 nF filter with BAT54S clamp diodes.
- Voltage at the L+ terminal (V_L+), via a ÷11 divider.
- High-side current (I_hs).
- Loop supply voltage.

**Classification** (each state must hold ≥2 s before the device changes state, and every transition is logged with its raw values):

| Condition | State | User-facing meaning |
|---|---|---|
| I_ls < 0.5 mA, V_L+ ≈ supply | OPEN | "Pressure sensor disconnected – pressure UNKNOWN" (high priority) |
| I_ls < 0.5 mA, V_L+ < 2 V, supply OK | L+ SHORTED TO GROUND | "Sensor cable fault – pressure UNKNOWN" |
| 0.5 ≤ I < 3.6 mA | SENSOR FAULT LOW | Transmitter is signalling a failure |
| 3.6–3.8 mA | UNDER-RANGE | Value suspect; shown flagged |
| 3.8–20.5 mA | VALID | Linear scaling; 3.8–4.0 mA clamped to 0 |
| 20.5–21.0 mA | OVER-RANGE | Read as "≥ full scale" and treated as high (valid but saturated) |
| 21–24 mA | SENSOR FAULT HIGH | — |
| ≥24 mA (at the current limit) | LOOP SHORT (L+ to L−) | — |
| (V_L+ − V_L−) < transmitter minimum + 1 V | LOOP VOLTAGE LOW | Value marked suspect |
| \|I_hs − I_ls\| > max(0.1 mA, 1%) for 60 s | LOOP LEAKAGE | Moisture or damaged insulation |
| σ > 0.5 psi over 5 min while the compressor is idle | NOISY SIGNAL | Loose connection or interference |
| Zero change in raw counts for 30 min, or no compressor recharge for longer than m× the learned interval | STUCK / NO CYCLE | Isolation valve closed? Measurement frozen? |
| Reference-check channel off by >0.2%; I2C failures; ESP32 coarse reading disagrees by >5% of full scale | MEASUREMENT FAULT | — |

**Pressure-specific alert logic** (all thresholds are relative to the contractor-approved band and are stored with who approved them):
- **LOW WARN:** below the normal minimum minus a warning margin, held for t_W.
- **LOW CRITICAL:** below the contractor-set critical level (above trip pressure with margin), OR the projected time to reach it is under H minutes. The projection uses a robust 15-minute slope that excludes compressor run periods.
- **RAPID LOSS:** pressure falling faster than R psi/min for ≥2 min.
- **HIGH WARN / HIGH CRITICAL:** above the normal maximum plus a margin. Too much air can delay valve trip and water delivery in a real fire. For listed supervisory devices, NFPA 72 signals at ±10 psi from the required pressure; a supplementary early-warning band will usually be tighter.
- **TRIP SUSPECTED (critical):** pressure fell below the trip hint and then rose to water-supply level, or simply exceeds the water-level hint. Whether this works depends on the tap location. Validate it during the annual trip test with maintenance mode on.
- **LEAK TREND (info/warning):** the pressure-decay rate while the compressor is off, or recharge cycles per day, exceeds k× the 30-day baseline. For context, NFPA 13 accepts at most a 1.5 psi loss over 24 h in its 40 psi new-system air test.

### 4.5 Temperature

- **Probe placement:** at valve height, away from the compressor, any heater and door drafts.
- **Cable:** 1–3 m, 4-core shielded. I2C at 20–50 kHz on its own bus, so a cable fault can't take down the internal sensors. 470 Ω series resistors plus a TVS array at both ends survive a 24 V miswire. Nine-clock bus recovery after a hang.
- **Fault detection:**
  - The NTC reads open above 1 MΩ and short below 100 Ω.
  - More than 3 consecutive CRC failures → "temperature sensor fault".
  - Implausible values (outside −45 to +130 °C, or a change >10 °C/min) → "invalid".
- **Cold alert placeholders** (owner and contractor must approve):
  - Warning: ≤45 °F for ≥30 min.
  - Critical: ≤40 °F for ≥15 min. NFPA 25 uses 40 °F as the minimum for dry-valve enclosures.
  - Recovery: ≥10 min above the threshold plus 2 °F.
  - Also shown: projected time to 40 °F, and the running total "time below threshold".
- **Inside the enclosure:** humidity >85% for 1 h → warning; >95% → condensation risk.

### 4.6 Power path and budget

**Inputs:** DC IN goes through the eFuse; PoE comes through the isolated PD module. The two are diode-ORed onto a 12–30 V bus. Each source's voltage is measured, so "power source changed" is reported as an event.

| Load | Typical | Maximum |
|---|---|---|
| ESP32-S3 (Ethernet in use, Wi-Fi off) | 0.2 W | ≈1 W peaks with Wi-Fi |
| W5500 at 100 Mb/s | ≈0.43 W | ≈0.45 W |
| ADCs, sensors, LEDs, watchdog | 0.05 W | 0.1 W |
| Loop channel 1 at 12 mA (including limiter loss) | 0.29 W | 0.64 W (shorted, at the limit) |
| Loop channel 2 (optional) | 0.29 W | 0.64 W |
| Conversion losses | ≈0.2 W | ≈0.5 W |
| **Total** | **≈1.2–1.5 W** | **≈3.5 W** |

- **PoE:** request Class 2 (≤6.49 W) to leave headroom.
- **Last-gasp message:** an optional supercap footprint, to be evaluated in early prototypes. It would let the device send "input power lost" before shutting down.
- **Backup power (A+):** 1.5 W for 24 h is about 36 Wh. A 12 V 7 Ah AGM battery gives roughly 24–30 h after cold derating. Lithium packs (Li-ion or LiFePO₄) must not be charged below 0 °C. So either keep lithium in the heated warehouse, or use AGM with temperature-compensated charging, as fire-alarm panels do. Backup only helps if the network gear is also on a UPS, which is why A+ adds the LTE-M fallback.

### 4.7 Protection by port

| Port | Protection | Design target |
|---|---|---|
| DC IN | eFuse (over-voltage, under-voltage, current limit, reverse polarity), SMBJ33A, LC filter | Survives −30 V reverse and 40 V transients |
| PoE / Ethernet | Module isolation (1500 V), magnetics, standard termination, ESD array | 802.3af; ESD ±8 kV |
| Loop L+ / L− | PTC fuse (50 mA hold), TVS, back-feed diode, 26 mA current limit, RC filter and clamps into the ADC | ±30 V on any pair, indefinitely |
| I2C probe / NTC | Series resistors, TVS arrays, separate bus | ESD; survives a 24 V miswire |
| USB (inside the box) | USBLC6-2 | ESD |
| Board | Acrylic conformal coat (mask sensors and connectors), vented enclosure | Condensation |

### 4.8 Firmware self-checks and watchdogs

- **Platform:** ESP-IDF v5.x / FreeRTOS. Separate tasks for sensing, alarm evaluation, uplink, OTA, provisioning, a health supervisor, a flash ring log and config.
- **Watchdogs:**
  - Task watchdog at 5 s.
  - The external TPS3823 is fed only after every critical task has checked in on time.
  - Brownout detector enabled; the reset reason is reported on every boot.
- **Reset handling:**
  - More than 3 unexpected resets in 24 h → DEVICE UNSTABLE.
  - More than 5 resets in 10 min → safe mode (sensing and uplink only) plus an OTA rollback check.
- **Local alarm evaluation:** the device evaluates alarms itself (sending events immediately) and the cloud evaluates the same data independently. Events carry IDs and sequence numbers and are re-sent until the cloud acknowledges them.
- **Config:** versioned and CRC-checked. On error the device falls back to the last good config and reports which version it is running.
- **Time:** NTP, with a fallback to the HTTPS Date header (many corporate networks block NTP). If the clock isn't synced within 10 min → TIME UNSYNCED, and the cloud stamps data with receipt time.
- **Local buffer:** about 46 days of 10-second samples in an 8 MB flash ring, sent later with "delayed" flags after an outage.

### 4.9 Communications and offsite failure monitoring

- **Normal reporting:** outbound HTTPS only, port 443. One-minute summaries (min/mean/max/last plus quality flags). Every 10 s while an alert is pending or active, and every 5 s in "live view". Config and commands ride back on the responses, so there are no inbound ports.
- **On LTE-M (A+):** 5-minute summaries plus events (about 2 MB/month estimated). Full-rate data is backfilled once Ethernet returns.
- **Layer 1 – backend staleness check (runs every 60 s):** STALE at 3× the report interval; SITE OFFLINE at 10 min by default.
- **Layer 2 – device→third-party dead-man check:** every 5 min the device pings an external service such as Healthchecks.io (hosted or self-hosted), Cronitor or Dead Man's Snitch. That service alerts through its own channels even if our backend is down.
- **Layer 3 – monitor of the monitor:** the backend pings its own external check every minute. If the backend dies, the owner is told the monitoring service is down.
- **Human confirmation:** a daily "all normal" digest. If the digest doesn't arrive, that absence is itself a signal. Plus a weekly end-to-end test notification with "tap to confirm".

---

## 5. Workshop manufacturing, calibration fixture and costs

### 5.1 Make vs buy

- **Buy:** transmitter, ESP32 / PoE / regulator modules, bare PCBs (4-layer) and stencils, polycarbonate NEMA 4X/IP66 enclosure, cable glands, breather vent, M12 cordsets, Class 2 power supply or PoE injector.
  - Enclosure families to evaluate: Hammond 1554/1555, Bud NBF, Fibox, Polycase. Verify UL 50E and UL 94 ratings.
  - Breather vent: ePTFE membrane type.
- **Make:**
  - Stencil-print, place and reflow; then through-hole soldering.
  - Probe board and cable.
  - Conformal coat.
  - Drill the enclosure using a 3D-printed jig.
  - 3D-print internal parts in ASA or PETG (not PLA, which goes brittle in cold and creeps): mounting plate with heat-set inserts, probe housing, cable comb.
  - Flash, provision, calibrate, burn in, label.
- **Optional outsourcing:** at 25–100 units, have the main board's SMT side assembled by a PCB house. Through-hole work, test, calibration and final assembly stay in-house.

### 5.2 Build traveler (per unit)

1. Incoming inspection; parts from authorized distributors only.
2. SMT assembly, then microscope inspection.
3. Through-hole: terminals, RJ45 jack, PoE module, SIP regulators.
4. Clean, then current-limited first power-up.
5. Flash the test image over USB. The device generates its own key pair. Record the serial number and public key in the production database.
6. Fixture test (§5.3).
7. Store calibration constants on the device, with a matching record in the cloud.
8. Conformal coat with masking.
9. Enclosure: glands at the bottom, vent fitted, labels applied.
   - Labels: serial QR, ratings, "Contains FCC ID …", and "Supplementary monitor – not a listed fire-alarm device".
10. Burn-in, 24–48 h, reporting to a test backend while fed a simulated sensor current.
11. Final production image. Burn the secure-boot and flash-encryption fuses; this is **irreversible**, so it happens only after all tests pass. Development units are left unlocked.
12. Final check that the device appears in the cloud, then pack with its pre-verified transmitter.

**Serial number format:** `SSM1-YYMM-NNNN` plus a device UUID, printed on a cold-rated polyester QR label.

### 5.3 Test fixture "FX-1" and calibration

**Fixture hardware:**
- 3D-printed nest with pogo pins.
- Relays select the input: 9, 12, 24 or 30 V, reverse polarity, PoE injector.
- Two programmable current sinks (DAC + op-amp + 0.01% resistor), read back by the fixture's own 24-bit ADC with a reference that is checked annually against a calibrated DMM.
- Fault relays: open, L+–L− short, L+ to ground, and a 100 kΩ leakage resistor (≈0.24 mA).
- Reference temperature sensor, test network switch, test Wi-Fi access point, USB.
- Python/pytest host with esptool. Results go to SQLite/CSV and produce a printed certificate.

**Automated checks (≤10 min hands-on):**
- Supply rails and loop supply.
- Calibration at 4 and 20 mA on both channels; verify at 3, 12, 20.8 and 22 mA. Pass if error ≤0.02 mA.
- Every fault state in §4.4.
- Temperature reading against the reference.
- Ethernet link and HTTPS; Wi-Fi signal strength; PoE startup.
- Watchdog fires when the firmware deliberately stops feeding it.
- Brownout ramp.
- LEDs and button.

**Transmitter verification:**
- A 4–6 port manifold with a calibrated reference gauge (at least 4× more accurate than the tolerance), a hand pump or regulated nitrogen with a fine needle valve, a relief valve and a shield.
- Points: 0 / 25 / 50 / 75 / 100 / 150 psi, 60 s settling at each.
- Accept within the transmitter's specification.
- Safety: compressed gas stores energy. Use rated fittings and minimal volume, and keep pneumatic tests at or below working range.

**Temperature check:** ice-point (0 °C) plus a comparison against the reference sensor.

**Environmental screening:** freezer cold-soak at −18 °C for 4 h, then return to room temperature while powered and watching humidity. 100% of pilot units; later a sample per lot. ESD and EMC go to an outside lab.

**Field repair:**
- Transmitters swap via M12. The cloud asks for the new transmitter's serial number and a re-verification.
- Boards swap on plug-in terminals. A "replace device" step in the cloud carries over the site config and history.
- Keep 1 spare board and 1 spare transmitter per 10–20 installed units.

### 5.4 Cost estimates

These are estimates, not quotes, in USD as of late 2026. Tariffs and distributor pricing are volatile.

**Materials per unit** (one pressure channel, SHT45 probe, PoE fitted, mid-grade transmitter):

| Subassembly | Qty 1 | Qty 5 | Qty 25 | Qty 100 |
|---|---|---|---|---|
| Main board parts + PCB/stencil share (qty 100 includes ≈$8–20 outsourced SMT) | 110–150 | 75–100 | 60–80 | 55–80 |
| Temperature probe (PCB, SHT45, housing, cable) | 25–35 | 18–25 | 14–20 | 10–15 |
| Pressure transmitter (mid-grade industrial) | 90–220 | 85–200 | 75–180 | 65–160 |
| Enclosure, glands, vent, M12 jacks, hardware, printed parts | 55–90 | 45–75 | 40–65 | 32–55 |
| Cordsets and cables | 25–45 | 22–40 | 18–35 | 15–30 |
| Class 2 power supply or PoE injector | 15–35 | 15–35 | 15–30 | 15–28 |
| Labels, packaging, documents | 6–10 | 5–8 | 4–6 | 3–5 |
| **Materials total** | **≈330–590** | **≈265–485** | **≈225–415** | **≈195–375** |

Not included: the contractor-specified tap kit (tee, valve, orifice; ≈$30–80, est.).

A budget variant (imported transmitter at ≈$25–50 that must be qualified first, no PoE) is ≈$120–170 at qty 100.

**Hands-on labor per unit** (minutes; labor rate $60/h assumed):

| Step | Qty 1 | Qty 5 | Qty 25 | Qty 100 |
|---|---|---|---|---|
| Kitting and inspection | 30 | 15 | 6 | 3 |
| SMT (both boards) | 150 | 75 | 35 | 5 (inspection only) |
| Through-hole and cleaning | 40 | 33 | 23 | 15 |
| Flashing, fixture test, calibration | 65 | 30 | 15 | 12 |
| Transmitter manifold check (batched) | 30 | 15 | 6 | 4 |
| Conformal coat | 20 | 12 | 6 | 4 |
| Enclosure machining and final assembly | 75 | 45 | 26 | 17 |
| Burn-in handling, final QA, packing | 45 | 23 | 12 | 9 |
| Debug allowance | 120 | 45 | 15 | 8 |
| **Total** | **≈9.6 h** | **≈4.9 h** | **≈2.4 h** | **≈1.3 h** |
| First-pass yield / rework per unit (assumed) | 80% / +12 min | 88% / +7 | 93% / +3 | 96% / +1 |

**All-in per unit** (materials + labor + rework + scrap allowance; excludes tooling, design time and compliance):

| | Qty 1 | Qty 5 | Qty 25 | Qty 100 |
|---|---|---|---|---|
| Total | ≈$920–1,180 | ≈$570–790 | ≈$375–570 | ≈$275–455 |

**One-time tooling** if not already owned (estimate ≈$1.8k–7.6k):

| Item | Estimate |
|---|---|
| Reflow (hot plate or benchtop oven) | $150–1,500 |
| Stencil jig | $50–150 |
| Microscope | $150–800 |
| Hot-air rework station | $100–400 |
| FX-1 fixture build | $300–800 |
| Pressure manifold with relief valve | $150–400 |
| Calibrated reference gauge with accredited certificate | $400–1,500 |
| Hand pump / regulator | $100–500 |
| Loop calibrator or precision current source | $150–800 |
| Label printer | $100–300 |
| Drill jigs | $50–150 |
| Freezer for cold soak | $0–300 |

Amortized: a $3k tooling budget adds $3,000 / $600 / $120 / $30 per unit at qty 1 / 5 / 25 / 100.

**Compliance placeholders (not quotes; get lab quotes):**
- FCC Part 15B emissions testing plus pre-compliance: ≈$2k–8k.
- Optional nationally recognized testing lab (NRTL) safety evaluation: ≈$10k–40k+.
- Product-liability insurance and legal review are extra.

**Recurring costs (estimates; verify current provider pricing):**
- **Platform, fixed:** ≈$40–150/month at pilot scale. Covers managed database and hosting, SMS number and US A2P 10DLC campaign fees, email, and the dead-man service.
- **Per site per month:**
  - Hosting share: ≈$0.5–5, falling with fleet size.
  - SMS/voice: ≈$0.1–2 in a normal month. SMS runs roughly 1–2¢ per segment all-in; calls a few cents per minute.
  - Cellular (A+ or B): ≈$2–8.
- **Support:** about 0.25–1 h per site per year once stable. Annual on-site verification is billed separately.

---

## 6. Dashboard, notifications, data, security and privacy

### 6.1 Dashboard (installable PWA, mobile-first)

**Home screen:**
- **Pressure card:** value in psi, state as text plus icon (never colour alone), "updated 14 s ago (14:03:12)", 24-hour sparkline with threshold bands.
- **Temperature card:** value, plus "below 40 °F for 1 h 12 m" when applicable.
- **Device card:** connection type, last heartbeat, power source, firmware version, calibration date.
- **Active alerts:** with an Acknowledge button.

**Display rules:**
- Green only when the value is fresh, valid, inside its band, and the thresholds have been approved.
- Grey "STALE / OFFLINE – last known 50.2 psi at 14:03" otherwise.
- A red fault badge, with no number, when a sensor is invalid.
- An amber "THRESHOLDS UNVERIFIED" banner until the approval record is complete: approver, firm, date, valve model and document reference.

**Other pages:**
- **Trends:** 24 h / 7 d / 30 d / 1 y, min/max shading, compressor recharge markers and event overlays.
- **Events:** history with filters, acknowledgement and notes.
- **Settings:** thresholds, hysteresis and persistence, all validated (low < normal < high; hysteresis ≥ 5× noise).
- **Contacts and escalation policy.**
- **Maintenance mode:** auto-expires (default 2 h, maximum 8 h), shows a banner and logs who enabled it. Used for the annual trip test.
- **"Record gauge reading":** for drift checks.
- **"Send test alert"** button.
- **Audit log.**

**Roles:** Owner/Admin, Viewer, Installer, Contractor.

**Multi-site:** the data model includes organizations, sites and devices from day one. Version 1 shows one site. Version 2 adds a contractor fleet view sorted by severity, with access delegated per site. Each site's thresholds are still approved individually.

### 6.2 Notifications

- **Channels:** Web Push, SMS, voice call (text-to-speech, "press 1 to acknowledge"), email. ntfy- or Pushover-style apps are optional for power users; verify whether they support iOS critical alerts.
- **Default escalation policy:**
  - Critical:
    - T+0: push, SMS and email to tier 1.
    - T+5 min unacknowledged: voice call to tier 1, SMS to tier 2.
    - T+15 min: voice call to tier 2 and the contractor.
    - Repeats every 30 min until acknowledged.
    - Reminder 4 h after acknowledgement if the condition is still active.
  - Warnings: push and email, SMS optional; quiet hours allowed.
  - Recovery notices go to whoever was alerted.
- **Acknowledging:** through the PWA, an SMS reply ("ACK 123"), or a keypress on the voice call. Acknowledging stops escalation; it does not clear the alarm.
- **Flapping:** rate limits per condition per hour.
- **Web Push facts:**
  - Standards: RFC 8030 / 8291, VAPID per RFC 8292.
  - iOS and iPadOS 16.4+ support it only for web apps added to the Home Screen. No Critical Alerts; Focus modes can silence it; no delivery guarantee.
  - Android and desktop browsers support it, but power management can delay it.
  - Dead subscriptions (HTTP 404/410) are detected and the admin is warned.
- **SMS facts:**
  - US application-to-person texting needs 10DLC brand and campaign registration, or toll-free verification.
  - Need documented opt-in consent (TCPA/CTIA) and STOP/HELP handling.
  - Delivery receipts aren't guaranteed and carriers may filter messages. Keep texts ≤160 GSM-7 characters and avoid public URL shorteners.
  - If a contact replies STOP, the dashboard shows "Contact X opted out of SMS".
  - Candidate providers: Twilio, Telnyx, Vonage, Plivo, Bandwidth, AWS End User Messaging. Add a secondary provider later.
- **Advice to users:** save the alert number as a contact and allow it through Focus / Do Not Disturb, so that repeated calls break through.

### 6.3 Backend

**Candidate stack** (pending owner preference): managed Postgres with authentication, row-level security, scheduled jobs and edge functions (e.g., Supabase), with the PWA on a static/edge host (e.g., Vercel or Cloudflare). An AWS IoT Core / Lambda / RDS stack is the alternative.

**Tables:**
- orgs, memberships, sites
- devices (serial, public key, firmware, calibration)
- channels (range, transmitter serial)
- threshold_sets (versioned, with provenance)
- readings_1m (with quality bitmask), raw_snippets (±10 min around each event)
- events, notifications (provider message ID, delivery status)
- contacts (consent, verification), escalation_policies, maintenance_windows
- audit_log, heartbeats

**Interfaces:**
- Ingest is signed and batched, with sequence numbers. Out-of-range values and timestamps more than 5 min in the future are rejected.
- Config fetch uses ETags.
- An OTA manifest endpoint.

**Testing:** the alert engine is tested by replaying recorded and synthetic traces: compressor cycles, slow leak, rapid loss, trip, sensor faults, outages.

### 6.4 Security

**Device:**
- Secure Boot v2 and flash encryption in release mode. Encrypted on-device config storage. JTAG and plain serial download disabled in production.
- Its own key pair: in the ATECC608B (ECC), or in the ESP32-S3's digital-signature peripheral (RSA).
- It signs short-lived tokens over server-authenticated TLS 1.2/1.3. No shared secrets are stored on the server.

**Provisioning:**
- Scan the QR label, enter the single-use claim code, and the device is bound to the site.
- Wi-Fi is set up over BLE using ESP-IDF provisioning security scheme 2, with a proof-of-possession code printed on the label.
- Ethernet needs no setup (DHCP), or static IP / proxy can be set during provisioning.

**Updates:**
- Signed images in two slots. A new version is marked good only after self-tests pass and it reaches the cloud; otherwise it rolls back.
- Anti-rollback counter.
- Staged rollout: one unit, then 10%, then all. Never during an active alarm.
- Signing keys kept offline on a hardware token, with a revocation plan.

**Accounts and operations:** passkeys or TOTP for admins, least-privilege service keys, point-in-time backups with tested restores, a software bill of materials for the firmware, and a vulnerability-disclosure policy.

### 6.5 Privacy

- The only personal data is contact names, phone numbers and emails, plus optional site addresses.
- Encrypted at rest and separated by row-level security; redacted from logs. The device holds none.
- Configurable retention, with export and delete.
- Consent records are kept for SMS.

---

## 7. Failure modes and regulatory constraints

### 7.1 System-level failure modes

| Failure | Detection | Result |
|---|---|---|
| Sensor cable cut, shorted or grounded; moisture leakage | Loop classifier (§4.4) | Pressure UNKNOWN or leakage alert; never shown as 0 psi |
| Isolation valve left closed / frozen reading | Raw counts frozen; no recharge cycles | STUCK / NO CYCLE warning |
| Transmitter drift | Annual gauge comparison; recharge-pattern shift; optional second transmitter | Drift warning; re-verify |
| ADC or reference failure | Reference-check channel; coarse ADC cross-check; I2C errors | MEASUREMENT FAULT |
| Temperature probe missing or damaged | NACK, CRC failure, plausibility checks | TEMP FAULT |
| Firmware hang or reboot loop | Internal and external watchdogs; reset counter | Reset, safe mode, rollback; cloud sees the gap |
| Site power loss (compressor and heater also down) | Power-source events; last-gasp option; dead-man | ON BATTERY (A+) or SITE OFFLINE |
| Network or backend outage | Cloud staleness check; device→external ping; backend→external ping | SITE OFFLINE / MONITORING DOWN by an independent path |
| Notification provider outage or ignored alerts | Delivery status; escalation; multiple channels; weekly test | Escalate to other channels and other people |
| Wrong thresholds configured | Validation rules; approval record; UNVERIFIED banner | Change blocked or warned |
| Condensation inside the enclosure | Internal humidity sensor | Warning |
| Stolen credentials or a malicious update | Per-device keys with revocation; signed images | Device revoked; image rejected |
| **The pressure tap itself leaks and causes a trip** | Leak test at install; restricting orifice; decay-rate trend | Hazard reduced by design; professional install |

### 7.2 Hazard review (independent of convenience)

- The electronics are low-voltage only (SELV / Class 2), using a listed power supply. The main physical hazard is the **added tap**, which is mitigated as described in §4.3.
- The biggest system risk is **false reassurance**. It is countered by stale-means-fault display rules, the dead-man layers, positive daily confirmation, and labelling the product as supplementary.
- The device has no control outputs. It must not draw power from or connect to the fire-alarm panel. It must not obstruct the valve, gauges or inspection access, or sit in drain discharge paths.

### 7.3 Regulatory and compliance constraints (to be confirmed by qualified reviewers)

| Area | Constraint | Action |
|---|---|---|
| NFPA 13 / NFPA 25 / NFPA 72, IFC as adopted | Changes to the sprinkler system and its trim need a qualified contractor and possibly a permit. Inspection, testing and maintenance continue unchanged. NFPA 25's interval relaxations tied to *supervised* low-air or low-temperature alarms do not automatically apply to an unlisted device. | AHJ and contractor review; check which code editions are adopted |
| Listing | This device is not a listed supervisory device or fire-alarm component (UL 864 / FM) and must not replace one. | Marketing and labelling discipline |
| Electrical safety | NEC Class 2 / PoE wiring rules. OSHA expects "approved" (often NRTL-listed) electrical equipment in workplaces. A UL 61010-1 or UL 62368-1 evaluation may be expected commercially. | Decide on an NRTL evaluation before selling |
| FCC | Part 15 Subpart B emissions (Class A if marketed only for commercial use), via a Supplier's Declaration of Conformity. Follow the modular-radio integration rules (KDB 996369) and the "Contains FCC ID" label. The module's grant does **not** cover the finished product. A+ adds cellular grants and possibly carrier certification. | Pre-compliance scan, then a lab |
| Cybersecurity | California SB-327 (no default passwords). The voluntary US Cyber Trust Mark (check its current status). NISTIR 8259A baseline. | Design to it now |
| Messaging and privacy | TCPA, CTIA, 10DLC; state privacy laws if thresholds are met | Consent records |
| Batteries (A+/B) | UN38.3 for shipping lithium; UL 2054/62133 if cells are built into the product | Prefer listed external UPS or AGM |
| Insurance | The insurer may have requirements | Owner informs the insurer |

**Words to avoid in any marketing:** "prevents trips", "fire alarm", "NFPA-compliant", "listed", "approved".

---

## 8. Roadmap and the files I would create next

### 8.1 Gated roadmap (durations are estimates)

| Gate | What happens | Exit criteria |
|---|---|---|
| **G0** | Owner answers Q1–Q4. Baseline the requirements. | — |
| **G1 (≈2–3 weeks)** | Breadboard prototype using dev boards and a real transmitter: ESP32-S3 DevKit, W5500 module, ADS1115 board, loop circuit, SHT45. | **Measured** noise and accuracy; every fault state detected; end-to-end alert in under 60 s; dead-man test passes |
| **G2 (≈3–4 weeks)** | KiCad hierarchical schematic and 4-layer layout. ERC and DRC clean. BOM with MPNs and second sources. Fab outputs (Gerber X2, drill, position file, IPC-2581). STEP model checked for fit. | **Owner approval required before any fab order or spending** |
| **G3** | Build 3–5 Rev A units. FX-1 fixture v1. Cold soak and condensation tests. | — |
| **G4** | 30–60 day shadow pilot at the owner's site, running alongside the existing gauges and supervision, on a contractor-approved tap. | — |
| **G5** | Rev B. Pre-compliance EMC scan. Security review. Field documentation. | — |
| **G6** | 2–3 friendly pilot sites. | — |
| **G7** | Commercialization decision: compliance, insurance, terms of service. | — |

### 8.2 Files (planned, not yet created)

Under `research/independent-designs/adviser-claude/`:
- `REQUIREMENTS.md` (with the interview log), `ARCHITECTURES.md`, `DECISIONS.md` (decision records), `HANDOFF.md`.
- `HARDWARE/`
  - `kicad/ssm-main/` with sheets for power, loop channels, MCU, Ethernet/PoE, sensors and I/O.
  - `kicad/ssm-probe/`.
  - `bom/bom.csv` (MPN, manufacturer, second source, distributor part numbers).
  - `calcs/` (loop-voltage, power and error budgets with Monte Carlo, in Python).
  - `sim/` (ngspice / LTspice runs of limiter, fault, TVS and boost behaviour).
- `MECHANICAL/`: CadQuery / build123d scripts (text files that diff cleanly in git), plus STEP and 3MF exports for the mounting plate, probe housing, drill jig and fixture nest; an installation drawing.
- `FIRMWARE/`: ESP-IDF project with host-run unit tests of the classifier and alarm logic; partition table; signing procedure.
- `SOFTWARE/`: SQL migrations with row-level-security tests, OpenAPI spec, alert engine with replay tests, PWA (Playwright tests), dead-man configuration.
- `MANUFACTURING/`: traveler, FX-1 design and pytest scripts, calibration procedure, QA checklist, serial scheme, test-report template.
- `BUSINESS/`: cost model (CSV), compliance matrix, SMS and push cost model.

---

## 9. The single most important interview question

> **What power and network service actually reach the inside of the closed riser room today, or could practically be installed there?**

Specifically:
- Is there a 120 VAC outlet, and is it on a generator or UPS?
- Could an Ethernet cable be run there from a network switch that is on a UPS, and roughly how far?
- How many Wi-Fi and cellular signal bars does a phone show inside the room with the door closed, and on which carrier?

This answer is the only one that changes the PCB and BOM now: A (Ethernet/PoE), A+ (cellular plus backup power) or B (autonomous cellular). Valve thresholds are configurable and must be approved by a qualified sprinkler professional regardless of which architecture is chosen.