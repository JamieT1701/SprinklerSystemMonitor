# B1 24 V field-current protection — real KiCad 10 schematic checkpoint

**2026-11-16** · Source branch `design/claude-b1-engineering-20261116` · Draft PR #7 · Issue #3

**Current stage:** First *native, editable and electrically connected* KiCad 10 **field-power-path schematic** with source-controlled symbols, internal M12 loop connection, eFuse pins and real ERC/netlist. **This is NOT the whole B1 circuit**, is **not a safety-qualified short-circuit protection assembly**, and is **not a PCB fabrication release**. Both the boost and eFuse values are bench candidates. No real equipment was energized.

## Files and acceptance evidence

| File | Meaning | Verified |
|---|---|---|
| `CAD/electronics/B1_24V_FIELD_POWER_REVIEW.kicad_sch` | Native KiCad 10 A3 field power concept, real electrically connected symbols | Opens via KiCad command line; ERC and XML netlist export succeeded |
| `CAD/electronics/B1_Bench.kicad_sym` | Project-local eight custom engineering symbols with correct TI package pin order, test point, pressure M12/PoE source | Compared against official TPS2662 Rev F pin table |
| `CAD/electronics/sym-lib-table` & `B1_24V_FIELD_POWER_REVIEW.kicad_pro` | Required local symbol library path and project metadata | Library issues cleared by KiCad CLI |
| `CAD/electronics/B1_24V_FIELD_POWER_REVIEW_ERC.rpt` | **Actual KiCad 10 ERC: 0 errors / 0 warnings** | J1 is explicitly marked as an *assumed external bench power source*; this does NOT verify Waveshare PoE headroom |
| `CAD/electronics/B1_24V_FIELD_POWER_REVIEW_NETLIST.xml` | Actual KiCad-exported machine-checkable netlist | 18 real placed symbols, 13 connected nets, 2 marked unconnected P3 contacts |
| `CAD/electronics/B1_24V_FIELD_POWER_REVIEW_net_contract.json` | Generated known-correct point-to-point identities | Verified against native KiCad XML export |
| `CAD/electronics/generate_b1_frontend_schematic.py` | Deterministic schematic/source generator | Rerun and compare before review |
| `CAD/electronics/check_frontend_netlist.py` + `VERIFICATION/test_native_eda_contract.py` | Independent native XML/ERC regression tests | All 87 host-only tests pass (78 previous plus 9 new) |
| `CAD/outputs/drawings/B1_24V_FIELD_POWER_REVIEW.svg` | Rendered *native KiCad* electrical sheet | SVG/XML validated and inspected via Chrome screenshot |

The existing unrelated `CAD/electronics/B1_placement_NOT_ROUTED.kicad_pcb` remains **UNROUTED** and has the previous **eight pad-clearance DRC violations**. Passing the new schematic ERC does **not** clear that PCB DRC or establish 1:1 PCB/schematic net parity.

## Exact connected provisional topology

```text
Bench-only, EXTERNALLY ASSUMED current-limited +5 V / ground
      │
      ▼
U1 Pololu 5588 5 V→24 V (NOT SHORT PROTECTED)
      │
      ├─ C2 1uF 50V input of eFuse, to GND_LOGIC
      ▼
U2 TPS26625DRCR (auto-retry, back-to-back output blocking)
      ├─ IN pin 1 ── BOOST_24V
      ├─ UVLO pin 2 ── 715k / 20k / 30.1k divider (TI nominal 18 V UVLO)
      ├─ OVP pin 3 ── same divider (TI nominal 30 V OVP)
      ├─ SHDN pin 4 ── 10k pull to LOGIC_3V3 (external source NOT qualified)
      ├─ RTN pin 5 ── RTN_EFUSE_ISOLATED local control components
      ├─ GND pin 6 ── GND_LOGIC (separate from RTN by design)
      ├─ ILIM pin 7 ── R4 165k to RTN (40.218mA *theoretical* overload)
      ├─ dVdt pin 8 ── C1 10nF to RTN (startup/ramp TEST REQUIRED)
      ├─ FLT pin 9 ── R6 100k pull to LOGIC_3V3; raw digital interface
      ├─ OUT pin 10 ── FIELD_PROTECTED_LPLUS → C3 1uF/50V → P3 pin 1
      └─ PAD pin 11 ── RTN plane only (NOT tied directly to GND)
                                                     │
SPTD25 transmitter (0–100psig, 4–20mA), P3 pin 2 ◄┘
      │
      ▼
SENSOR_I_RETURN → R5 100 Ω 0.1% ≥0.25W → GND_LOGIC

P3 M12 pins 3/4 — physically separate, expressly NOT CONNECTED.
J2: RAW monitoring pads only (no ADC, no final input protection).
```

### TI manufacturer references and calculated limits

[TI TPS2662 family datasheet Rev F](https://www.ti.com/lit/ds/symlink/tps2662.pdf), especially pp. 4 (pin 1–10 and thermal pad), 24 (RTN vs GND), 25 (TI reference eFuse circuit), 26 (UVLO/OVP divider and current-limit design), and pp. 20–22 (fault limiting / overtemp/auto-retry). The chosen protection variant is **TPS26625DRCR**; pin 11 is the exposed PowerPAD connected to RTN copper, **not** direct to logic GND.

- **Current-limit setting:** `I_LIMIT_nominal_A=6.636 / R_ILIM_kΩ`. With `165kΩ`, `40.218mA` calculated. TI only specifies tight ±5% at its **880mA** setting, so no actual 40mA distribution/min/max can be claimed until component testing.
- **Nominal shunt:** `100Ω × 20mA = 2.00V`; `100Ω × 25mA = 2.50V`; `100Ω × 40.218mA = 4.022V`. **The last exceeds 3.3V ADC input safety**, even if ADS1115 PGA is set to ±4.096V. A field return miswire to external +24V could dissipate `24²/100 = 5.76W` in an unprotected 100Ω resistor, destroying it.
- **Short dissipation upper illustration:** `24V×0.040218A ≈0.965W` in the eFuse during a full output short *before thermal shutdown/auto-retry*. 3×3 mm VSON thermal design is not solved by math. Must test repeated faults at max ambient including temperature of eFuse and Pololu.
- **Booster current at 5 V** (assumed 80% efficiency): `24V×0.025A/(5V×0.8)≈150mA` for 25mA transmitter over-range and `≈241mA` at nominal 40.218mA limit, **in addition** to ESP32/W5500/PoE transients. Actual efficiency, voltage and available PoE source budget must be measured.
- **Voltage window network:** R1 715k from 24V input to UVLO, R2 20k from UVLO to OVP, R3 30.1k OVP to RTN; based on TI Figure 10-1 nominal ~18V UVLO and ~30V OVP. The actual tolerance, GPIO interface and RTN offsets under reverse/miswire need full bench checks.
- **M12 P3** SPTD-specific contact 1 protected +24V, contact 2 loop current return; 3/4 NC. The AchieVe LPPT25 has another return/ground contact assignment and is not a field drop-in.
- **Boost input:** custom J1 source pin types are marked `power_out` solely to tell ERC that a *bench supply exists upstream*. No direct connection to verified Waveshare factory 5V rail and no conclusion about Ethernet/PoE compliance.

### Important missing circuitry (intentional, **blocking**)

1. **ADC powered and unpowered input protection:** Clamp/sense path for `SENSOR_I_RETURN`, `FIELD_PROTECTED_LPLUS` and `BOOST_24V`, including 24V+ input, unpowered ADS input, no rail backfeed, filter accuracy and input impedance at ADS1115. **No raw J2 signal may go directly to an ADC pin.**
2. **Field P3 cable and surge network:** ESD/TVS, 24V reverse/short on either M12 contact including externally injected voltage, and thermal/current rating of shunt under a cable miswire and wet connector.
3. **eFuse hot/fault behavior:** Actual RILIM trip distribution, thermal shutoff/cooldown auto-retry, loop supply compliance during over-range and restarts, fault output and 3.3V domain voltage limits.
4. **PoE power-stage validation:** Factory Waveshare PoE module may not supply adequate 5V startup margin for Pololu boost; assess cold start, 802.3af classification/switch capacity, modems/routers and repeated short. Pololu product explicitly does not tolerate direct output shorts.
5. **True mechanical footprint and netlist match:** Exact TPS26625 VSON footprint and PowerPAD thermal via pattern to be independently sourced from TI package drawing, not guessed. No manufacturing footprint currently assigned to U2, and this schematic is **not synchronized to the prior unrouted KiCad placement board**.
6. **3.3V logic and P2 temperature**, reference/ADC I2C, actual PoE RJ45 bulkhead and OTA/software/cloud: absent from this **power-stage-only** KiCad sheet. The schematic is intentionally a *subset*, not the full product.
7. **Qualified sprinkler system tap/range and sensor availability:** SPTD25 is currently backordered. No pressure transducer or connector hardware purchased. All independent installers/site approvals remain explicit.

## Remaining acceptance route

A. Obtain a qualified **available** manufacturer transmitter sharing the exact P3 pinout or approve a separately labeled/isolated harness configuration for a second source; do not silently substitute M12-compatible LPPT25.

B. Complete a true protected field input/ADC analog schematic, with exact parts/verified clamps and power-off behavior; incorporate eFuse package/thermal and exact shield strategy, then expand the native KiCad project to the full B1 electronics.

C. Re-run native KiCad ERC (no unrelated suppression), generate actual BOM/netlist, recreate the carrier PCB using matching symbols/netlist/footprints, and run actual KiCad PCB DRC; no fab output until physical DFM and independent review.

D. Only after owner-approved part scope, set up **isolated, current-limited low-voltage bench** with oscilloscope/programmable loads, temperature and smoke-protected setup, verified test records. The real installed sprinkler system, dry valve, heater controller and operating R6 device remain isolated and untouched.

**No component sourcing order, drilled box, production firmware or field pressure-tap work is authorized by a clean schematic ERC.**
