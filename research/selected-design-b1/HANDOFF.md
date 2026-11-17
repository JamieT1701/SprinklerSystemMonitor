# B1 engineering continuation / release gates

**Checkpoint:** 2026-11-16 · Design branch `design/claude-b1-engineering-20261116`
**Owner:** Jamie. **Authority:** Repo `JamieT1701/SprinklerSystemMonitor`; experiment [Issue #3](https://github.com/JamieT1701/SprinklerSystemMonitor/issues/3) and [Round 1 decision](../independent-designs/COMPARISON.md). Physical R6 and Rev A carrier remain governed by [Issue #2](https://github.com/JamieT1701/SprinklerSystemMonitor/issues/2). Do not assume `main` is canonical for the current Device Lab hardware.

## Completed and verified in this workstream

- Separate draft engineering branch from the **coordinator's latest Round 1 comparison** (never overwrote Claude/Gemini submissions).
- Source-only decisions, requirements, analog channel/field interface contract, sourced **candidate** BOM, reproducible shunt/power/divider computations, host-only 4–20mA fault and cloud anti-stale state models, multi-system bench test matrix, shop QA plan.
- **78 Python standard-library synthetic tests passing** on Arthur (`jamie-home-dev`), with exact command in README; no secrets or outside services used.
- Manufacturer datasheet/official source evidence linked (Waveshare PoE board, TI ADS1115 limits, Pololu 24V booster, Beckhoff NE43, WIKA comparator part).

## Deliberately not claimed or done

- No KiCad native project/schematic/PCB/3D STEP, SPICE verified circuit, ERC/DRC, Gerber fabrication release, ordered parts, assembly, real 4–20mA transducer or calibrated sensor, actual pressure/temperature bench reading, field work, FCC/UL listing or any other commercial regulatory approval.
- No firmware flash, PoE settings change, cloud deployment, outbound SMS, customer communication, purchasing, sprinkler valve/trim modification or production security fuse.
- No compliance with a pressure alarm or dry-pipe trip pressure. **Current gauge approximately 54psi is an observed physical baseline only**, not a setpoint.

## Highest-priority next non-destructive engineering actions

1. **Site design input (qualified contractor gate):** The private recent annual inspection independently documents multiple dry systems and historical test pressures (sensitive details withheld from public GitHub). Recover system-specific make/model from **private record**, then contractor-confirm valve/AMD topology, approved process-side pressure tap for each monitored domain, manufacturer air band and max temperature/pressure exposure; choose qualified 4–20mA sensor range and exact MPN **without** assuming shared compressor-outlet reading represents every dry-pipe valve.
2. **Electrical design, independent reviewer:** Build and calculate a **hardware continuous-short-safe 24V loop-current limiter** with low-side 100Ω sense, source/terminal diagnostic dividers, appropriately rated ESD/reverse/miswire clamps and ADC power-off safeguards. Select exact sourceable protective devices and evaluate fault heating/boost supply sag. A Pololu U3V9F24 booster is **only a bench candidate**, never a field-current limiter. TI TPS2662 is a promising **unqualified** 25mA-minimum programmable eFuse family candidate; exact variant, VSON assembly and safe indefinite short response need independent design/test.
3. **Actual module current/pin budget:** With proper isolation and approval, measure Waveshare PoE 5V output at startup, Ethernet active and worst loop current; check pinouts, module mounting and connector height for commercial carrier. Do not disturb working site unit.
4. **Native EDA after above:** Use KiCad 9 or compatible EDA environment. Arthur currently does **not** have `kicad-cli` installed; do not claim ERC/DRC. Create complete hierarchical electrical schematic, run ERC, independent review, then PCB with measured enclosure/connector geometry and DRC. Confirm full qualified BOM and second-source parts.
5. **Bench proof and safety:** Bounded current source 4/12/20mA plus fault-injection (open, ground, return short, reverse, 24V field miswire, ADC unpowered, sensor/hardware lock, thermal), pneumatic reference, cold/condensation and outage/alert tests. Only isolated rigs, no live sprinkler connection.
6. **End-to-end software validation:** Build **real** edge firmware and cloud from the test contracts, field gateway and third-party monitor; verify silent outages, retries, message delivery, hysteresis, duplicate events and approval records.
7. **Earnings and commercial gate:** Matched supplier MPN quotes at 1/5/25/100, shop time study, exact legal/regulatory installation/fire-protection classifications/insurance, owner-approved spending and release.

**First material owner input if needed:** The actual dry-valve/air-maintenance equipment model and installer/inspection report; one question at a time. Contractor/AHJ approval must precede an approved pressure tap or alert threshold. Research may continue on independent bench source without changing sprinkler infrastructure.

## Privacy-safe new finding

Private owner inspection (not committed) shows multiple individual dry-system trip tests. The preferred B1 product remains **single-channel per approved tap**; one site may require multiple B1 devices with common dashboard rollup. Newly added `HARDWARE/MULTI-SYSTEM-SCOPE.md`, `SOFTWARE/site_rollup.py` and its host-only tests preserve individual fault identity. Do not disclose the actual private report or valve/trip/deficiency details in public GitHub. A later invoice located in owner mail concerns the prior routine inspection, **not independently verified remediation**.

## 2026-11-16 follow-on vendor selection and sensor-specific contract

Exactly sourced **ProSense SPTD25-20-0100H 0-100psig** is now the preferred **bench-design** pressure transmitter, not ordered or site-approved. Supplier confirms **M12 pin 1 +, pin 2 return, pins3/4 unused** (invalidates earlier tentative pin3 return); `CDP12-0B-030-AA` non-LED 3m female-to-male cord is a low-cost qualified-to-test candidate. LPPT25-20-0100H is a non-interchangeable $80 alternative with a **different contact function**. The real rated proof 250psig, supply 8.5-36V and permitted 3-4/20-25mA nonlinear over/under range are encoded in sources; 100psig must be installer-approved for each application. TI TPS26625DRCR (auto-retry reverse-blocking) and E96 165kOhm ILIM ~40mA **arithmetic only**, NOT a verified output stage. [Sensor selection](HARDWARE/PRESSURE-SENSOR-SELECTION.md) is the source of truth. **78 synthetic host tests pass** (63 prior + 15). Still no KiCad released netlist, 24V short-safe circuit, qualified sensor/pressure tests, PO, or live system changes.

### Stock update (2026-11-16)

AutomationDirect now explicitly lists SPTD25-20-0100H **backordered, projected earliest 2026-12-30**, while alternative LPPT25-20-0100H is marked **295 available**, source links in HARDWARE/PRESSURE-SENSOR-SELECTION.md. This changes procurement timing, not the completed B1 host circuit verification. SPTD is a bench-design baseline only; do not assume quick availability or substitute LPPT without independent connector pinout and calibration approval.
