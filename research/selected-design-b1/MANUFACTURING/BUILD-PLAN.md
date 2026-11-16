# B1 solo-workshop assembly + service concept

**Status:** DFM/workflow plan only. No physical build, shop tooling order, board order or sales margin approved.

## First article strategy — minimize DIY complexity

**Buy / reuse:** factory Waveshare ESP32-S3-PoE-ETH development module; factory ADS1115 breakout during safe isolated bench proof; precision components; qualified 2-wire transmitter once selected; externally qualified pressure hose/fittings, sturdy weather-resistant box and strain-relief glands. Do **not** fabricate PoE magnetics or redesign W5500 before the simpler development path is proven.

**Make:** source-reviewed carrier PCB only after complete KiCad schematic and **fault-current protection**; hand-assemble test/terminal parts; print drill template and internal mounting fixtures in PETG/ASA; flash/test/provision; cold/thermal and pneumatic QA.

**Component limits for low-volume workshop:** passives preferably 0805/1206+, accessible QFP/SOIC or pluggable modules; no home BGA assembly. If 24V boost module uses microscopic package, keep it as a bought module during first article, or outsource SMT with verified unit/test cost.

## Fixture plan

- Current-loop precision simulator 0, 3.5, 4, 12, 20, 20.8, 21.5 and (protected) 26mA.
- A **separate** calibrated digital reference gauge, low-volume rated pneumatic manifold, bleed/relief, and hose fitting for 0, 25, 50, 75, 100 and 150 psig (only within actual transmitter and fixture ratings), with clean dry air/N2 and physical safety shield. No live fire-system pressure tests.
- Isolated power test, PoE switch on bench, insulated fault-injection jig for normal/open/short/miswire with energy limiting; qualify test jig itself before use.
- USB provisioning test host, label/serial and calibration repository, pass/fail CSV, fixture revision recorded.

## Proposed manufacturing traveler (not executed)

1. Inspect controller module, installed factory PoE, PCB, connectors and exact transmitter MPN certificate.
2. Assemble analog front end/current limit; inspect solder/cleaning/ESD safe work; no field wires connected.
3. First power-on through current-limited isolated bench supply; measure rails against expected budget.
4. Verify 24V loop short survival and protect ADC under miswire fault; **stop immediately if these are not approved designs**.
5. Flash known version; provision device-unique identity in a test service; do not irreversibly burn secure-boot/flash-encryption fuses on development units.
6. Run electrical test currents and known-reference comparison; reject bad loop quality and ADC reference behavior.
7. Pneumatic sensor check (0/25/50/75/100/150 only if rated) with shop-approved pressure manifold; store sensor serial and calibration.
8. Test physical DS18B20, network link and power-off cloud dead-man with a *test* backend.
9. Conformal coat with correct connector/sensor masking; final drill jig/glands, strain relief, mounted electrical clearance and label.
10. Cold soak, condensation return, burn-in, reboot and actual notification receipt tests; final sign-off and pack spare/repair documentation.

## Cost model — do not convert Round 1 estimates into selling prices

Claude's Round 1 100-unit **$275–455** materials+labor allowance is **not a quote** and excludes material tooling, regulatory qualification, installed labor, warranty and insurance. Carbon's cheaper numbers assumed an unusually inexpensive industrial transmitter and incorrect battery/power promise. Verified parts will be priced only after qualified exact MPNs.

Cost tracking for 1/5/25/100 quantities requires: actual supplier tier cost, taxes, shipping, substitute part QA, PCB assembly, pressure sender and cable, enclosure, AC/PoE supply, 5V/24V converter and protection, hardware fixture amortization, hands-on assembly minutes, burn-in capacity, yield/rework, compliance pretests, warranty and annual service. A single-person workshop cannot imply 15–30-minute finished product labor until measured during a real batch.

**Commercial gate:** do not advertise "fire alarm", "NFPA compliant", "UL listed" or "prevents trips" without substantiation and legal/AHJ/regulatory review. Professional field install and existing fire-system requirements remain mandatory.
