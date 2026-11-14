# Engineering reconciliation - two-terminal build R6

2026-11-11. Reviewed against PR #1 at 0a38e77afbd322c740a741dc18a7c1933436ef57, the Oscar handoff/firmware, prior field receipts and manufacturer documents. Active execution and GitHub Pages source branch: docs/device-lab-2026-11-10-checkpoint. Main remains the unchanged legacy base; no new canonical production branch is declared.

## Findings corrected in the guide
1. External vs internal connections were visually ambiguous. The design has exactly ONE Ethernet connection and TWO 3-position field blocks, both on Board B. No extra sensor block exists on A.
2. Generated assembly pictures showed unreliable component/pin arrangements and extra colored posts. They are withdrawn as assembly instructions and replaced with labeled vector circuit and placement drawings.
3. Earlier replies alternated between one and two perfboards. Exactly two existing 50x70 boards are used, plus the separate ESP/PoE assembly.
4. Probe pull-up assumption was corrected by the owner: install ONE R5=4.7k on Board B between 3V3 and GPIO18/DATA. No resistor is assumed inside the probe cable.
5. R3=4.7k replaces the 5k lower-leg component. The 0.5951417004 ratio and simulator predictions are now consistent with the prepared v5-47k source.
6. The ground/power distribution is explicit: a Board B GND node feeds both sensors and A through W08; +5V only feeds J1, while +3V3 feeds J2 and ADS.
7. C1 is A0 filtering; C2 is a separate 100nF supply bypass at the ADS. The added bypass does not alter nominal divider gain.
8. Historical local handoff and public PR description lagged actual temperature/pressure diagnostic deployment. Historical evidence is retained, but current-guide pointers and an updated PR summary prevent treating old statuses as current.
9. GPIO numbers are not header position numbers. Manufacturer pin-label reference replaces invented physical pin placement.
10. Bench A0 near zero with the sensor unplugged is not evidence of failure. A0 near zero with a driven simulator or live sensor at ~50 PSI requires diagnosis; no calibration offset should hide it.

## What has been checked in software
- Machine-readable connector/parts/net list: exactly two terminal blocks, three pins each; each pin has exactly one net; no conflicting rail assignment.
- Internal harness has exactly nine inter-assembly wires; every endpoint is accounted for.
- Sensor DATA goes to GPIO18, not the ADC. R5 connects 3V3 to DATA; ADC VDD is 3V3.
- Pressure resistor topology, ratio, 0/50/150 PSI predictions, independent resistor-network simulator calculation, and ADS 0xC383 register settings.
- HTML uses one internally consistent data set for connector and harness tables. Browser QA must be recorded separately after rendering.
These tests verify the specified design, NOT the physical soldering, real module, sensors, cable installation or overall safety certification.

## Physical and operational gates not claimed complete
Actual breakout/header/terminal footprint and perfboard copper pattern, enclosure fit/PoE clearance, sensor identity, cable voltage drop/noise, resistor measurement, power integrity, insulation/strain relief, field surge protection requirements, ADC and temperature disconnect/reconnect tests, gauge calibration, history service, notifications, missing-heartbeat service and explicit operational acceptance.
The passive input is not a surge-protected industrial interface. The transducer model and environment must be checked before operational reliance.

## Firmware review (no device write in this work)
The existing v5-47k binary compiled successfully in the prior turn, but field testing is absent. The sensor code uses a fixed delay after requesting ADS conversion rather than validating its ready bit/config readback; sample-age output zero on invalid temperature can be misread; absent/present distinction can depend on cached discovery; a successful I2C address probe is not proof of a valid sensor. Reconnect, stale data, unusual temperatures including the 85C power-on value, input rail faults and network recovery need targeted tests/hardening before release. Do not mistake this revision's wiring tests for firmware fault-injection tests. No firmware changed or uploaded in this revision.

## Why the previous images are not used
They were conceptual AI-generated composites, not CAD renders from a verified netlist or photos of the real assembly. Labeling them conceptual was insufficient for a soldering guide. No hidden wiring can be inferred from them. Current drawings deliberately show connector counts and named connections without pretending to know actual mounting hole locations.

## Scope exclusions
No 2024 dashboard modification; no new external sensor or compressor control; no main-branch promotion; no OTA secret retrieval/publication; no device flashing; no production fire-protection/control changes; no notification delivery claims.

## R6 verification receipts
- Design tests: 24/24 pass in isolated authoring container and on Oscar using Python standard-library unittest. Tests cover the specified netlist and arithmetic, not physical components.
- Chromium/Playwright in-memory browser review: desktop 1440x1100 and mobile 390x844; no page-level horizontal overflow; diagrams scroll horizontally on mobile; exactly two external sensor blocks and two blocks in the Board B detail; checklist counter works; no JavaScript errors. Browser-storage persistence was not tested at the in-memory origin.
- Visually checked connection, Board B, circuit, and harness views. Drawings show no extra sensor blocks, banana sockets or invented power connector.
- Existing firmware v5 source on Oscar reviewed: pins 16/17/18 and divider 14.7/24.7 agree with this design. Previous compile receipt re-read; no compile/upload or installed-device-state claim is made by these documentation checks.
- GitHub Pages release verification must name the deployed revision after publication; a local browser preview alone is not a deployment receipt.
