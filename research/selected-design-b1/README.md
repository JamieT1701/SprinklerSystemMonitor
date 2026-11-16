# B1 — Selected Claude-derived sprinkler pressure / cold monitor

**Engineering status: DESIGN DEVELOPMENT ONLY — NOT FABRICATION READY, NOT INSTALLED OR TESTED.**
**Last updated:** 2026-11-16
**Owning branch:** `design/claude-b1-engineering-20261116`, derived from the contest **coordinator branch**, not repository `main`.

## Purpose and scope

Advance [Issue #3's independent review](../independent-designs/COMPARISON.md) into a **simplified**, repairable, single-person-workshop **supplementary** dry-pipe air-pressure and riser-room air-temperature monitor. This is a new commercial **candidate**, not the current working device, and must never claim to replace required listed fire supervisory equipment, fire-alarm signalling, inspection or heating.

**Selected baseline:** Ethernet-first ESP32-S3 / W5500, factory PoE hardware, one industry-standard **two-wire 4–20 mA** pressure transmitter (range **provisional**, not selected), protected 16-bit ADC/loop diagnostics, remote DS18B20 probe, and offsite monitoring/alerts. No onboard battery, cellular radio, second pressure channel, custom PoE circuitry, or automatic control of compressor, valves or heaters in B1.

## What has actually been created

- `REQUIREMENTS.md`: proposed verification matrix, known facts vs site-required approvals.
- `DECISIONS.md`: tradeoffs and explicit rejected complexity.
- `HARDWARE/FRONTEND-DESIGN.md`: functional net/channel contract, candidate current-loop power, analog and miswire interfaces; **not a schematic**.
- `HARDWARE/engineering_calcs.py` and `calculation-receipt.json`: reproducible arithmetic, all inputs/assumptions explicit.
- `HARDWARE/BOM-CANDIDATES.csv`: source-linked candidate manufacturer parts, unresolved qualified specifications.
- `FIRMWARE/loop_classifier.py`: host-only reference classification for recorded current/voltage samples; **not deployable firmware or fire protection controls**.
- `VERIFICATION/test_*.py`: synthetic regression tests only; no electronics or real sensor verified.
- `VERIFICATION/FAULT-MATRIX.md`: bench, system, security and installation release gates.
- `SOFTWARE/ALERT-CONTRACT.md`: backend/alerts and anti-stale expectations.
- `HARDWARE/MULTI-SYSTEM-SCOPE.md` and `SOFTWARE/site_rollup.py`: confidential-source-safe multi-valve installation options and synthetic site rollup (one B1 channel per approved tap remains the preferred unit architecture).
- `MANUFACTURING/BUILD-PLAN.md`: single-workshop build strategy, fixture, traceability.
- `HANDOFF.md`: status and next blocked/unblocked steps.

## Never conflate with the currently deployed R6 prototype

The physical R6 currently uses an existing **Waveshare ESP32-S3-POE-ETH + ADS1115 + three-wire 0.5–4.5V pressure sensor** mounted at the compressor and a separate DS18B20 room probe. Owner reported PoE connected, gauge around **54 psi**, and a stable relative signal. **Current R6 calibration/notifications have not been fully accepted.** Its software, current perfboard, P4 mounting and existing physical sensor remain governed by **[Issue #2](https://github.com/JamieT1701/SprinklerSystemMonitor/issues/2)** and **draft PR #1**. No existing R6 files or live controller were changed for B1.

## Engineering release position

As of this checkpoint:
- **Executed:** 53 Python host-side tests pass (software arithmetic and synthetic loop fault classifications only).
- **Not created:** genuine native KiCad schematic/PCB, reviewed parts/footprints, ERC/DRC, SPICE/power simulation, fab exports, assembly drawings, actual test fixture, flashable ESP-IDF, cloud alert service, a working B1 sensor, supplier-quoted BOM or regulatory signoffs.
- **Critical blockers:** qualified sprinkler tap and valve data; correct pressure-transmitter MPN/range/process rating; protected **24V current-limited loop-source circuit**, analog/miswire/ESD/ADC front end, measured PoE power and exact connector fit. See `HARDWARE/FRONTEND-DESIGN.md`.

No board order, safety-critical installation, sale, product-compliance claim, customer contact, irreversible security fusing or field deployment is authorized.

## Reproduce work on Arthur (Ubuntu, Python 3)

```sh
cd /home/jamiet1701/.local/share/device-lab-advisor-competition/engineering-b1
python3 research/selected-design-b1/HARDWARE/engineering_calcs.py
python3 -m unittest discover -s research/selected-design-b1/VERIFICATION -p 'test_*.py' -v
```

These are bench-model tests, **not** proof of true pressure sensor faults, exact ADC behavior, electrical survivability or provider delivery.

[Round 1 scoring](../independent-designs/COMPARISON.md) · [technical audit](../independent-designs/TECHNICAL-AUDIT.md) · [contest Issue #3](https://github.com/JamieT1701/SprinklerSystemMonitor/issues/3)

## New inspection-informed scope (privacy protected)

The owner's privately held current annual inspection records **multiple individually tested dry systems**. A shared compressor reading does not prove the air pressure at each valve. B1 remains a single-channel modular product; a multi-system site may need one professionally approved independent sensor per valve-side air domain. No exact valve models, tested trip points, inspection deficiencies, price quotes, facility address or confidential report were copied to public GitHub. See `HARDWARE/MULTI-SYSTEM-SCOPE.md`.
