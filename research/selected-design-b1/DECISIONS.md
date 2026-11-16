# B1 design decisions — selected, conditional and deferred

**Date 2026-11-16**. These are reversible **research architecture selections** (not product, procurement or installation approvals).

| ADR | Selected direction | Alternative rejected or deferred | Reason / gate |
|---|---|---|---|
| B1-01 | Reuse **Waveshare ESP32-S3-POE-ETH SKU 28771** as the B1 electronics development module; W5500 already aboard | Designing our own Ethernet and 802.3af PoE PD immediately | Reduces RF/power/board risk and reuses demonstrated existing hardware; must verify actual spare capacity and production-life/source |
| B1-02 | **One** current-loop pressure channel, **two-wire 4–20 mA** | Commercially standardizing the original three-wire 0.5–4.5 V sensor | Better loop open/fault observability and flexible cable resistance; physical transmitter range **not yet qualified** |
| B1-03 | **100 Ω 0.1%** sense resistor to 3.3V-supplied ADS1115 at ±4.096V PGA | Carbon's 150 Ω sense shunt; raw 0.5–4.5 V direct ADC | 20mA -> 2.0V; 26mA -> 2.6V. Still requires real analog voltage/current/transient protection. |
| B1-04 | Separate 24V-loop L+ voltage and 24V rail diagnostics via 270k/22k provisional dividers; ADC reference check | Declaring cable short from current alone | Distinguish probable open/grounded cable vs supply/under-compliance where physically observable. 40V divider ~3.014V; above 40V needs reviewed clamp. |
| B1-05 | PoE/5V primary and modular **5V→24V regulator candidate** for a single test channel | DIY onboard lithium UPS, 24VAC input, homemade PoE front end | No unverified cold charging/backup claim. Offsite watchdog sends offline alerts when site power/network dies. See Pololu 5588 candidate, not a qualified field module. |
| B1-06 | Remote protected **DS18B20 3-wire** plus on-board pull-up | Remote I2C SHT45/humidity board, dual room probes | Reuses known cable/probe; remote bus failure is independent of ADC I2C. Ambient placement and cable interference must be qualified. |
| B1-07 | One cloud-side offsite liveness monitor, plus separate check of monitoring service | Full multi-provider/cellular backhaul and always-on device UPS in v1 | Simple when no independent upstream backup exists; cloud liveness must not depend on device to report its death |
| B1-08 | PWA, 1 site first; leave org/site/device IDs in schema | Fully featured contractor fleet/tenant SaaS initially | Fewer user touches and lower maintenance while preserving future migration |
| B1-09 | Qualified professional owns tap/threshold/fire system decisions, no control outputs | AI-generated trip pressures or sprinkler system changes | Supplementary monitoring only, no listed device replacement |
| B1-10 | Author source-only schematic/test artifacts here, in separate branch from competition results | Modifying R6, merging competitors, committing secrets or vendor raw sessions | Immutable comparator and live-system safety |
| B1-11 | **No native KiCad schema/board yet** until loop supply/protection and actual module pins/MPNs are credible | A visually plausible but unsafe fabricated PCB | Electrical blockers demand schematic review; no ERC/DRC and fab claims at this checkpoint |

## Key corrections to Claude

- Simplify its dual ADS1115 and second current loop to **one** ADS1115 and one channel, reserving optional upgrade only if measured need.
- Use DS18B20 on a tested separate digital pin rather than long outdoor/room I2C.
- Keep dual independent offsite checks concept, but avoid complex multi-provider alarm infrastructure until first site proof.
- Distinguish *supply/terminal voltage* observed as evidence from an absolute claim to differentiate all shorts. A short to ground, broken wire or disabled loop can have overlapping symptoms.
- Design and test total equipment power and upstream switch/router availability; a PoE device and Ethernet network can share a failure mode.
- Defer cellular/UPS. No reason to compromise cold storage and workshop serviceability for an unproven 24h onboard battery spec.

## Manufacturer sources (review dates 2026-11-16)

- Waveshare ESP32-S3-ETH/PoE module and W5500: https://docs.waveshare.com/ESP32-S3-ETH
- TI ADS1115 datasheet / analog abs max: https://www.ti.com/product/ADS1115
- Pololu U3V9F24 (item 5588) candidate 24V regulator **is not** a safe current-limited output stage by itself: https://www.pololu.com/product/5588/specs
- Beckhoff summary of NAMUR NE43 current bands: https://infosys.beckhoff.com/content/1033/ioanalogmanual/3904850187.html
- Specific commercial transmitter reference only, NOT selected range: WIKA A-10 0–200psig 4–20mA 1/4NPT product record https://shop.wika.com/en-us/a_10.WIKA?itemId=50398083

## Candidate refinement — hardware limiting (not released)
TI **TPS2662** eFuse family now identified as a possible 24V high-side limiter because its documented current-limit range begins at **25mA**. Its VSON package and short-circuit thermal behavior make it an **unqualified B1 candidate**, not an approved/verified 35mA field supply. See `HARDWARE/FRONTEND-DESIGN.md` §8. The first PCB cannot be released until an actual reviewed schematic, limit tolerance and sustained short test exist.
