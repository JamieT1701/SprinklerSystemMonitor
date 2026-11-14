# Device Lab — Sprinkler Monitor R1 industrial assembly concept

**SUPERSEDED VERTICAL FIT MODEL (2026-11-12 correction):** The R1 script used a 1.1 mm Z translation after flipping the approved P4 mesh feet-down. That inadvertently placed its 9 mm mounting feet as low as -7.9 mm, beneath the modeled case floor at 0..2 mm. The R1 3D file is an archived concept only and **must not be used as a physical Z-clearance or standoff reference**. The corrected R2 mechanical layout lifts the rotated original P4 source face to Z=11 mm, seating the foot bottoms at Z=2 mm and locating an 8 mm separate PCB support from plate Z=11 to board Z=19 mm. R2 is source-checked but not yet Fusion-executed; see [R2 engineering handoff](CAD-FUSION-R2-DETAILED-DESIGN.md). The accepted original P4 STL itself was never modified.

**Date:** 2026-11-12 (Eastern)
**Status:** REAL FUSION ASSEMBLY CREATED / EXPORTED / CLOUD-SAVED; **CONCEPT ONLY, NOT FIT-VALIDATED OR FABRICATION-READY**
**Authority:** `JamieT1701/SprinklerSystemMonitor`, draft PR #1, branch `docs/device-lab-2026-11-10-checkpoint`. Do not merge into legacy application as part of enclosure design.

## Overview

This is a service-first, compact, industrial-styled **personal prototype** of the warehouse sprinkler pressure and temperature monitor. The assembly is built inside Autodesk Fusion on Oscar, not a collection of image-only concepts. The generated model has **eight separate named assembly components**, editable solid placeholders for the proposed enclosure and component supports, and **one imported, unchanged P4 reference mesh**. The concept does not replace the previously printed and owner-fit-approved P4 plate.

### Actual Fusion screenshots — not AI-generated renders

- [Fusion R1 top-down component envelope study](assets/fusion-r1-cad-top.png)
- [Fusion R1 isometric assembly envelope study](assets/fusion-r1-cad-isometric.png)

The presentation renders shown in chat are **illustrative industrial design concepts**, not accurate wiring diagrams, print-ready geometries or photographs of assembled hardware. Any discrepancies between those images and this document are resolved in favor of the R6 netlist and physical build instructions.

## Exact vs. estimated geometry

| Item | Footprint / envelope | Provenance | Status |
|---|---|---|---|
| P4 mounting plate | **95.1599 × 142.652 mm** XY; **9 mm** max total Z including feet; main plate **3 mm** thick | Approved P4 STL, source SHA256 below | Verified mesh and reported case fit |
| Board A perfboard | **70 × 50 mm**, component side with ADS1115, R1–R4, C1/C2 | R6 netlist and bench handoff | Footprint verified; mounting/placement proposed |
| Board B perfboard | **70 × 50 mm**, J1/J2 terminals and R5 | R6 netlist | Footprint verified; mounting/placement proposed |
| Waveshare ESP32-S3-ETH PCB | **72.8 × 21 mm** PCB | Waveshare vendor specs / https://www.espboards.dev/esp32/waveshare-esp32-s3-eth/ | PCB envelope; connector and PoE stack height not verified |
| Enclosure shell concept | **112 × 161 × 59 mm** outer modeling envelope, approx. 3 mm walls and 2 mm base | Design study only | **NOT** actual enclosure measurement |
| Mounting supports | Provisional 8 mm height, PCB lower surface at Z≈19 mm; P4 deck positioned with feet downward | Design study only | Requires heat-set/fastener/probe check |
| RJ45, gland sizes, internal harness | Position/clearance indicators only | Concept study | Not final holes, cuts, route/bend or seal specs |

The two recovered original P4 STL downloads were byte-identical. Authoritative P4 SHA-256 is
`1b2c593862eefe328c76ad1b6fe5e358a4fb71e1e7dc10909f55384ac18ff9f2`.
The R1 Fusion script checks that hash before importing the mesh. It rotates the referenced mesh to show feet down; **no geometry/scale modification is applied to the original file**.

## Proposed board placement (reference P4 frame, in millimeters)

X runs across the approximately 95.16 mm plate width; Y runs along its approximately 142.65 mm length. The shapes below are **bounding footprints**, not approved drill-hole locations.

| Component | Min X | Min Y | Max X | Max Y | Z PCB bottom |
|---|---:|---:|---:|---:|---:|
| Board A (70 × 50) | 12 | 6 | 82 | 56 | 19 |
| ESP32-S3-ETH (72.8 × 21) | 11 | 62 | 83.8 | 83 | 19 |
| Board B (70 × 50) | 12 | 86 | 82 | 136 | 19 |

**Automated XY footprint collision check passed:** A–controller gap **6 mm**; controller–B gap **3 mm**. These gaps are *tight* and must not be described as validated service clearance. Actual cables, populated component overhangs, mounting screws, sidewall distances and screwdriver access could invalidate this layout. Physical dry-fit is mandatory before designing/printing board supports or case drilling templates.

### Correct R6 electrical interfaces, not render labels

Exactly **three external connections**:
1. Ethernet/PoE cable to the factory Waveshare RJ45.
2. Pressure sensor 3-wire cable to **Board B J1: +5V, GND, PRESS_SIG** in that order (screw positions 1–3).
3. Temperature DS18B20 3-wire cable to **Board B J2: +3V3, DATA, GND** in that order (screw positions 1–3).

These are **two physically distinct 3-position terminal blocks on Board B**. No fourth field port. No 4–20 mA current-input path, PT100/NTC interface, high-voltage field terminal, control relay or pressure-control function is specified or implemented. The pressure sensor's historical 0.5–4.5 V/0–150 PSI model remains **unverified**, not a product label or calibration claim.

The rest of the wiring is defined by the existing R6 design: Board A has ten pending insulated underside jumper links; W01–W09 are nine **additional** inter-assembly harness connections. ADS1115 input stays on A0 after the divider, VDD at +3V3 only; ESP GPIO17 SDA, GPIO16 SCL, GPIO18 DS18B20 DATA. The actual perfboard coordinates and the board's confirmed physical stage remain in `docs/HANDOFF-2026-11-11-BOARD-A.md`; **0/10 Board A links installed as last user-confirmed**. This CAD study changes none of that.

## Engineering intent and validation gates

- Lid-off accessibility for the two screw terminal blocks, ESP32 USB/BOOT/RESET, ADS1115 module and mounting hardware.
- Separate three wire entry areas (PoE vs pressure vs temperature). Waterproof cable gland style shown in art only; no hole machining coordinates or ingress rating established.
- Removable internal electronic supports; approved P4 enclosure mount uses existing four heat-set feet and separately verified M3 fasteners.
- Low-voltage signal harness grouped along one side with strain relief/ties. Verify actual bundle size and keep field signal runs away from the PoE subassembly.
- No additional expansion PCB assumed in the CAD. Reserve area only if the physical layout leaves room.
- Confirm true enclosure inside dimensions, usable Z height, lid screw bosses, gasket track, P4 installed Z, cable gland wall thickness and drill positions.
- Bench/dry-fit the *actual* Waveshare + PoE daughterboard and both fully populated 70 × 50 perfboards with RJ45 plug connected.
- Ensure no PCB solder underside touches conductive screws, plate inserts, the enclosure, or other components.
- Verify screwdriver access to J1/J2 and that unplugging the ADC module / servicing a terminal does not require removing another board.
- Only after fit approval, separately design parametric mounts, case drill template and wire clips, 3D print prototypes, check actual geometry, and document acceptance.
- This is **supplemental monitoring**, not a replacement for listed sprinkler controls, alarms, heat or inspections. Firmware/pressure calibration/alert service remain unaccepted.

## Reproducibility and recovery

- Local Fusion script: `%APPDATA%\Autodesk\Autodesk Fusion 360\API\Scripts\DeviceLabR1Assembly\DeviceLabR1Assembly.py`
- Versioned source: `cad/fusion/DeviceLabR1Assembly/DeviceLabR1Assembly.py`
- Versioned F3D export: `cad/fusion/DeviceLabR1Assembly/R1_PROVISIONAL_Assembly.f3d`
- Local result receipt: `%USERPROFILE%\Documents\DeviceLab\Fusion\r1_assembly_result.json`
- Fusion cloud: **Jamie's Device Lab → Device Lab CAD → Sprinkler Monitor R1 - Industrial Concept PROVISIONAL**. Saved and manually marked editable.
- Run manually with **Shift+S → Scripts and Add-Ins**. Script always creates a **new** Fusion document and a timestamped local F3D export. Does not overwrite existing hub designs, start a service, or change production hardware.
- On 2026-11-12, the script executed in the real Fusion runtime and recorded `status: SUCCESS`, 8 component occurrences, one original P4 mesh, and zero pairwise XY board-envelope overlaps. Local archive size: **511,795 bytes**. The in-app model and actual screenshots were visually inspected.

This is an experimental layout deliberately kept separate from **mechanical release acceptance**, **electrical board assembly**, and **operational sprinkler-monitor acceptance**.
