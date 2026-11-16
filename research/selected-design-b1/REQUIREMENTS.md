# B1 requirements, provenance and unresolved site input

**Only proposed requirements; no release, field trip thresholds or certified claims.** Evidence classes: OWNER_REPORTED (not independently certified); MANUFACTURER_VERIFIED (linked datasheet/spec); DESIGN_ASSUMPTION (open); BENCH_VERIFIED (real recorded electrical observations — **none** for B1).

## Known context

- Owner has a commercial three-zone dry sprinkler air system with one compressor; normal gauge around **54 psi** during a stable period (owner's Nov 16 observation), not an approved trip pressure.
- Current pressure sensor is at **compressor outlet** beside the gauge; location may be upstream of an air maintenance device/check valve. Therefore it cannot be assumed to read the actual system-side pressure used for trip warnings.
- Owner has functioning PoE cabling to existing ESP32-S3-PoE-ETH; the riser room DS18B20 cable extends through/into the room. This is experience with **prototype**, not verification of planned commercial installations.
- Safety boundary: B1 is additional, unlisted telemetry. It never operates a valve, compressor or heater or replaces alarm/inspection. Installer-approved mechanical interface and AHJ review are required before any new site tap.

## Candidate acceptance requirements

| ID | Priority | Proposed behavior | Evidence needed before acceptance |
|---|---|---|---|
| P-01 | P0 | Pressure is measured in the **actual dry system-side air domain** with an approved tap and manufacturer pressure band | Sprinkler professional's valve/AMD/tap determination |
| P-02 | P0 | 2-wire 4–20 mA pressure transmitter; **provisional** 0–150 psig; exact range set by qualified review | Match transmitter MPN/proof/burst/port/environment; pneumatic calibration |
| P-03 | P0 | Target total pressure accuracy ≤±1.5 psig in declared operating temperature band (not yet validated) | Transducer total-error specification, calibration/test manifold, cold soak |
| P-04 | P0 | Missing/invalid sensor or ADC is **PRESSURE UNKNOWN**, not valid 0 psi, a green indicator or inferred valve state | Fault-injection and UI/backend tests |
| P-05 | P0 | Open, short to ground, overrange, low compliance/supply, and backfeed classified **to the granularity supported by measured channels** | Individually rated/verified front-end and recorded simulated + real faults |
| T-01 | P0 | Separate room ambient DS18B20, digital CRC, missing probe/85°C sentinel rejection; site temperature limits approved | Cable length/room placement, cold reference, disconnect/CRC tests |
| H-01 | P0 | One manufacturer's known-safe 5V→24V source with hardware current limiting; ADC remains at 3.3V with analog pins in range | Full short/miswire/transient tests plus actual PoE 5V rail-current budget |
| N-01 | P0 | Wired Ethernet/PoE, outbound TLS authenticated with per-device identity | Physical power/network test, firmware secure configuration |
| N-02 | P0 | **Offsite independent heartbeat** detects device/network/power silence, regardless of ability to send a dying gasp | Power pull + network pull + backend outage; observer independence |
| N-03 | P0 | Normal measurement freshness shown explicitly; stale, faulted or unapproved thresholds never shown as NORMAL | UI and backend tests with missing/stale data |
| A-01 | P0 | Configurable low/high/rapid pressure-loss alarms and sustained cold, hysteresis, acknowledgement/escalation | Pressure bands and cold policies approved by qualified site professionals; replay tests |
| A-02 | P0 | Critical notifications via consented SMS/voice backup + Web Push, delivery/acknowledgement tracked | Sender registration/opt-in, on-device tests, end-to-end delivery receipts |
| S-01 | P0 | Signed OTA with rollback, unique credentials, authenticated updates, no inbound firewall exception | Threat review, firmware/OTA rollback and leak tests |
| M-01 | P1 | One-workshop repairable board + pre-made PoE module, standardized external connectors, replacement service flow | Native KiCad and assembly/fit test, hardware source/second source |
| M-02 | P1 | Serial and transmitter traceability, electrical + pneumatic QA and burn-in records | Completed test fixture, measured time and 3–5 pilot build traveler |
| C-01 | P1 | Real quoted BOM/labor/support at 1/5/25/100 units; no assumed $100 cost | Exact MPN supplier quotes, tooling/NRE, warranty, SMS/provider cost model |
| G-01 | P0 | Qualified installer determines whether new equipment and its installation need permits/listing/AHJ review | Contractor/fire authority/electrical/FCC and insurance counsel where appropriate |

## Intentionally unresolved

1. Exact sprinkler valve **make/model**, manufacturer minimum/high air band, regulator/AMD arrangement, and whether current compressor outlet is system-side — **critical**.
2. Accepted tap point, fitting and protection, mechanical approval for installation, system pressure proof/burst and hydrostatic exposure risk.
3. Actual 4–20mA transmitter range (100 vs 150 vs 200 psi), part number, thread, environmental ratings and digital/analog failure behavior.
4. True PoE module **5V rail available current** while network active plus 24V loop converter at worst load.
5. Qualified, continuous-short-tolerant current-limiting and input protection design; no safe physical connection recommended without this.
6. Room temperature profile and location of wet valve/trim; approved cold warning/critical persistence, not arbitrary 40°F delays.
7. User's desired default alert contacts/escalation, SMS consent, support model and price limit.

**Priority question for the owner, only if records cannot supply the answer:** Is the actual sprinkler valve/air-maintenance-device make and model known from an inspection report? That information is needed before product pressure sensor/tap specs can be frozen.

## Acceptance distinction

A passing software test in this branch validates **synthetic classification arithmetic only**. It cannot demonstrate sensor accuracy, safe connection to any pressure system, electronics fault tolerance, 24h operation, alarm delivery or legal compliance.

## 2026-11-16 private inspection input — public-safe summary

A read-only review of the owner's recent **private annual fire sprinkler inspection** confirms that multiple dry systems were **individually tested**, despite their reported shared compressor. Exact valve models, test air pressures, trip pressures and deficiency data are restricted to the owner's private inspection record and are **not reproduced here**. The report **does not establish** that the common compressor port represents the protected system-side air pressure at each valve; nor does it authorize historical trip points as alert settings.

Add P0 site acceptance requirement **P-06:** For each required protected system, identify a qualified contractor-approved system-side measurement domain, independent transmitter ID, calibrated range and per-valve threshold record. **One B1 monitor per approved valve-side tap** is the preliminary modular choice; multi-channel shared gateway is deferred. A healthy common-compressor sensor must not allow an unmonitored required valve to appear NORMAL on the site dashboard. See `HARDWARE/MULTI-SYSTEM-SCOPE.md` and synthetic `SOFTWARE/site_rollup.py`.

**Remaining unresolved despite the inspection:** Whether individual valve-side pressure ports are accessible/approved, which compressor/regulator/air-maintenance elements separate pressure domains, whether historical conditions and alarm bands still match present equipment, and what remediation of any inspection observations has actually occurred. Only owner/qualified contractor can verify these.


### B1 Rev B service-connector acceptance

X-01 (P0): All three field cables can be replaced from outside closed enclosure. X-02 (P0): Distinct key/size prevents erroneous cross-plug. X-03 (P0): Correct per-connector manufacturer cutouts, mating/anti-corrosion caps, internal patch and harness strain relief validated physically. X-04 (P0): assembled enclosure IP54 target **unverified**; no rating claim until tested. X-05 (P0): 24 V loop remains current-limited/fault protected, safe sensor disconnect/miswire/power-off, real M8/M12 contact numbers verified. X-06 (P1): AUX is undrilled and unpowered, no fourth sensor channel promised. Full plan HARDWARE/CONNECTOR-REDESIGN.md.
