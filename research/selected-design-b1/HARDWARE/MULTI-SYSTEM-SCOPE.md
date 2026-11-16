# B1 installation architecture — multiple dry systems with a shared compressor

**2026-11-16, confidential source handling:** The owner-authorized 2026 annual fire-sprinkler inspection, stored privately in the connected Creative Play email account, documents **more than one individually inspected/trip-tested dry system** on the property. The report itself and its exact facility details, valve makes/models, tested trip pressures, defects, contractor correspondence and address are **not copied to this PUBLIC repository**. Work needs to be rechecked against the original private inspection by the owner and qualified sprinkler contractor. The report's historical readings are **not** approved alarm thresholds.

## Engineering implication

An air transducer at a **shared compressor outlet** is valuable for compressor and common-supply trends, but **cannot establish independent valve-side system air pressure** when check valves, air-maintenance devices, pressure regulators or other trim may separate the pressure domains. Do **not** label common-compressor data as direct proof of any downstream dry-valve state, threshold, or trip margin.

## Credible site installation choices

| Approach | Benefits | Critical drawbacks / questions | Stage |
|---|---|---|---|
| **A. One B1 per contractor-approved system-side air point** (default for separately monitored systems) | Proven single-channel product reused without custom multi-channel PCB; separate sensor and power/network fault domains; per-valve site alarms; easy installer replacement | Multiple installations, transmitters, PoE drops, calibration/cabling, recurring device costs; each system-side tap must be approved | **Preferred preliminary site concept**, not approval |
| B. One network unit with three independently protected pressure channels plus room temperature | Fewer MCUs/PoE connections and one enclosure; may lower cloud and per-unit hardware count | New multi-channel schematic/ADC mux/field protection, longer cables, single point of electronics/network failure across all valves, lower isolation, added QA complexity | Defer pending measured engineering case |
| C. Continue common-compressor-only sensor | No new fire-system tap; already useful for measuring compressor stability/trend | Cannot identify unequal system-side loss, check-valve isolation or which valve is in distress | Keep current R6 as independent supplemental monitor; **never equivalent to per-valve supervision** |

**Preferred product decision:** Ship B1 as **one, self-contained 4–20 mA channel**; support an organization/site containing multiple **separately identified** devices. Add a site rollup that **never reports site NORMAL if any expected device is missing, faulted, offline or thresholds unverified**. Avoid assuming that "three valves" can be read with one transmitter just because one compressor supplies them. **Do not presume a particular device count at another customer's site.**

The main qualification gate is **approved pressure measurement locations and air maintenance topology** for each target system, including confirmation of whether current compressor/gauge reading tracks all domains. The qualified sprinkler contractor defines port, mechanical interface, threshold semantics, installed monitoring type, and any AHJ/code constraints. The product has **no control outputs** and must not supplant required listed supervision or annual inspection.

## Owner-only private follow-up

Separate from product development, the source inspection lists deficiencies and a subsequent contractor proposal. Their **current remediation status has not been verified** by reading the private report or quote; the visible subsequent invoice identified routine inspection rather than repairs. Do not publish shortcomings, test pressures, contractor quote values, or other sensitive site metadata in public GitHub. If the owner needs operational remediation tracking, use an appropriately private system with restricted access and explicit owner decisions.

## Acceptance tests for multi-system aggregation

- No device with assigned expected status → site **INCOMPLETE / NOT PROVEN NORMAL**.
- One device missing/stale/offline → **SITE_OFFLINE_OR_STALE** for affected device and overall site **DEGRADED**, not green even if common compressor PSI remains stable.
- One pressure sensor UNKNOWN with other systems healthy → site **DEGRADED** and explicit device fault.
- One critical condition → **CRITICAL** at site level, preserving which system raised it.
- Unverified thresholds on any required device → site **UNVERIFIED**, never green NORMAL.
- Site NORMAL only with complete expected device set, all fresh, valid, approved and within bands; number of expected systems is an **approved site configuration**, not hard-coded to three.

**No wiring change or hardware quantity decision** until professional and owner confirmation. See `SOFTWARE/site_rollup.py` for a host-only model of these rollup rules.
