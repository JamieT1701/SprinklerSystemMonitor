# Sprinkler Monitor R2 — service-first industrial CAD engineering package

**Date:** 2026-11-12 (Eastern)
**Authority:** `JamieT1701/SprinklerSystemMonitor`, draft PR #1, branch `docs/device-lab-2026-11-10-checkpoint`.
**State:** **R2 EXECUTED, F3D EXPORTED, CLOUD-SAVED AND NATIVE VIEWPORT VERIFIED** on Oscar on 2026-11-12. Fusion produced nine top-level components, one preserved P4 mesh, and a 767,278-byte editable native F3D archive. Saved in **Jamie's Device Lab → Device Lab CAD → Sprinkler Monitor R2 - Detailed Industrial Concept PROVISIONAL**. Native execution receipt and checksum are versioned in `cad/fusion/DeviceLabR2Detail/native-run-receipt.json`. **Physical fit and print release remain NOT ACCEPTED.**

## View on a phone

- **[Interactive R2 3D assembly viewer — rotate, zoom, explode, hide lid](r2-viewer.html)** (no account or browser extensions; public non-operational concept).
- [Verified iPhone-size viewer screenshot](assets/r2-viewer-iphone-viewport-qa.png) and [exploded screenshot](assets/r2-viewer-exploded-iphone-qa.png). These are screenshots from a Chrome mobile-device emulator at 390 × 844 CSS pixels, not a physical iPhone device test.
- **[ACTUAL Autodesk Fusion R2 isometric viewport screenshot](assets/fusion-r2-NATIVE-isometric.png)** — captured on Oscar directly from the real native Fusion assembly after successful execution and cloud save.
- [R2 assembly, isometric, source-derived geometry](assets/fusion-r2-assembly-isometric.png)
- [R2 dimensioned top-down and section study](assets/fusion-r2-layout-top.png)
- [Previous R1 actual Fusion viewport (legacy height error; see below)](assets/fusion-r1-cad-isometric.png)

The actual native Fusion screenshot linked above comes from the model running in Autodesk Fusion on Oscar. The *separate* R2 layout PNGs and browser 3D viewer remain derived from independently checked model data; they are not native Fusion screenshots or photographs of printed hardware. The high-polish image-generation concept from chat is illustrative only and may not match exact sensors/components.

## Why R2 differs from R1

**Critical R1 reference elevation error corrected in R2:** The earlier R1 Fusion script rotated the P4 plate to turn its feet downward, then translated only **+1.1 mm in Z**. With the source plate spanning Z=0..9 mm, this meant the feet descended to **Z=-7.9 mm**, below the modeled 0..2 mm enclosure floor. Thus **R1 is superseded for any vertical fit assessment** even though its original P4 mesh file remained byte-identical.

In R2, the rotated mesh is translated to **Z=11 mm**. The feet now end at **Z=2 mm**, on the estimated case floor top. The plate's main underside is at Z=8, its upper deck at Z=11. Separate 8 mm insulated board risers start at Z=11 and finish at Z=19, level with the proposed lower PCB surfaces. **This is a geometrically corrected concept, not a tested real-world stack height.**

R2 also replaces the arbitrary R1 112×161 mm shell with a **104.4×151.9 mm approximate exterior outline from the historical P2 paper scan**. The existing P4 plate is still the approved, physically fitting part; the historic paper trace has approximately 0.5–1 mm uncertainty and cannot establish the lid height or actual inner ribs. The modeled exterior Z=59 mm is only a design assumption. No new case or resized P4 is proposed.

## Verified source vs proposed dimensions

| Item | Source/dimensions | Status |
|---|---|---|
| P4 plate | Actual original STL, SHA-256 `1b2c593862eefe328c76ad1b6fe5e358a4fb71e1e7dc10909f55384ac18ff9f2`, 95.1599×142.652×9 mm incl. feet | Source byte-verified; owner reported case fit |
| Board A | 70×50 mm; ADS1115, R1–R4, C1/C2; P3–P12 ADS header | Footprint / pins grounded; other component models illustrative |
| Waveshare | nominal 72.8×21 mm PCB | PCB footprint used; actual PoE module, RJ45 plug and service height unmeasured |
| Board B | 70×50 mm, J1 and J2 separate 3-position blocks, R5 pull-up | Design spec grounded; board not physically built |
| Enclosure | Approx. exterior 104.4×151.9 mm; Z assumed 59 mm, nominal wall 1.2 mm | Historical drawing/exterior paper trace, NOT verified interior/cut geometry |
| PCB underside | Z=19 mm with 8 mm isolated supports above P4 | Proposed; anchor holes not verified |
| Cable tie corridor | 6 mm-wide right-side service concept | Proposed; actual wire bundle, ties and sensor entry not verified |

Reference P4 coordinate origin: bottom left of the original STL bounding XY footprint. PCB positions are **not** hole-drilling coordinates.

| Part | Min X | Min Y | Max X | Max Y | Gap to preceding board along Y |
|---|---:|---:|---:|---:|---|
| Board A | 12 | 3 | 82 | 53 | — |
| Controller | 11 | 61 | 83.8 | 82 | 8 mm |
| Board B | 12 | 89 | 82 | 139 | 7 mm |

**What passed:** no pairwise 2D PCB rectangle overlap, minimum plate bounding-box margins of 3 mm, correct relative Z floor/plate/riser/PCB levels, matching PCB nominal footprints and R6 field terminal nets.

**What does not follow from those tests:** real PCBs can overhang their nominal outline with connectors, solder leads, heat-set inserts and cable strain relief. The 8/7 mm end gaps are too tight to assume fingertip/screwdriver access. Board B ends 3.65 mm from the top of the plate bounding box, and no physical gland/tool reach has been accepted.

## Wiring and service architecture — unchanged R6

Exactly three field cable functions:

- **Factory RJ45 / Ethernet/PoE** (no added PoE terminal).
- **J1 PRESS** on Board B: `+5V`, `GND`, `PRESS_SIG` pins 1/2/3.
- **J2 TEMP** on Board B: `+3V3`, `DATA`, `GND` pins 1/2/3.

No 4–20 mA interface, PT100/NTC conversion, high voltage, compressor control, extra sensor block or relay is added. R5 remains 4.7k between Board B +3V3 and GPIO18 DATA, not on the probe cable. Pressure network is R1 10k, R2 10k, R3 4.7k, R4 1k, C1 100nF; C2 100nF supply bypass. ADS power is 3V3. Board A header is exactly **P3–P12** in the owner's component-side coordinate system, never R3–R12.

Internal harness groups are not combined into one nine-wire channel:

| Group | Wires | Proposed route |
|---|---|---|
| Controller → Board B | W01–W04 | Short branch near adjacent 7 mm separation |
| Controller → Board A | W05–W06 | Short I²C branch near 8 mm separation |
| Board B → Board A | W07–W09 | Long three-wire run on right-side perimeter |

The R2 CAD still shows *routing envelopes*, not soldered wires or a fully measured harness. External strain relief and gland cut positions are not drill instructions. No live device or firmware action occurred.

## Deliverables and execution status

**Prepared / versioned:**
- `cad/fusion/DeviceLabR2Detail/DeviceLabR2Detail.py`: real Autodesk Fusion Python API geometry construction script; checks layout file against expected board bounds before creating new document; preserves P4 exact source.
- `cad/fusion/DeviceLabR2Detail/DeviceLabR2Detail.manifest`: manual-run Fusion script registration.
- `cad/fusion/DeviceLabR2Detail/assembly-layout.json`: machine-checkable dimensions, origins, net references and provisional gates.
- `cad/fusion/DeviceLabR2Detail/render_r2.py`: independently runnable, source-derived PNG top and isometric renderer using Pillow.
- `cad/fusion/DeviceLabR2Detail/make_3d_viewer.py`: reproducible, dependency-free (Python standard library) HTML generator from `assembly-layout.json`. Generated public page `docs/r2-viewer.html` has a real touch-drag/pinch/scroll 3D browser canvas; the P4 is represented by its bounding envelope, not re-triangulated as the exact STL mesh. JavaScript is standalone and does not call a remote service.
- The two PNGs under `docs/assets/` linked above.
- `hardware/mount-accessories/R2_P4_10mm_Wire_Tie_Saddle_FIT_TEST_ONLY.stl`: one optional no-drill, nonstructural PETG wire-saddle fit coupon, 26×16×8 mm, two nominal 3.6 mm pass-through holes at 10 mm center spacing. Its mesh was generated and independently checked manifold. **Not** a board mount or externally loaded strain relief. See accessory README.
- `tests/test_r2_layout.py` and `tests/test_r2_saddle.py` verification suites.

**Native Fusion R2 successfully executed and saved (2026-11-12):** The owner unlocked Oscar. Using the live Fusion UI, `Shift+S` → **Scripts and Add-Ins** → `DeviceLabR2Detail` → **Run** completed. The Fusion-generated `r2_detail_result.json` reported `status: SUCCESS`, nine top-level components, exactly one P4 reference mesh, two independent 3-position terminal blocks, correct P3–P12 Board A header, and 8/7 mm bounding-box Y gaps. The exported F3D `R2_Detailed_Industrial_Concept_20261112_014931.f3d` is 767,278 bytes; the byte-identical Git version is `cad/fusion/DeviceLabR2Detail/R2_PROVISIONAL_Assembly_NATIVE.f3d`, SHA-256 `2b3eb380e6fcd351692ce06c4403cbdfe799a1ebbdfc53a696b56477d1762319`. The Fusion Save dialog selected **Device Lab CAD**, and the window title subsequently displayed **Sprinkler Monitor R2 - Detailed Industrial Concept PROVISIONAL (Jamie's Device Lab)** with no unsaved indicator. A native Fusion isometric viewport image was captured and versioned at `docs/assets/fusion-r2-NATIVE-isometric.png`. See the sanitized `native-run-receipt.json` for repeatable evidence.

The earlier temporary Windows GUI accessibility failure is **resolved** for this run; R2 no longer requires a manual Fusion execution gate. Remaining gates are **physical measurements, actual board assembly, dry fit, and verification of print/installation dimensions**, not CAD script execution.

## Physical gates before printing installed mounts or modifying the real case

1. Finish the unpowered Board A build. Authoritative handoff still says **0/10 underside jumper links user-confirmed**, despite all 4 resistors + 2 capacitors and ADS header soldered.
2. Assemble Board B with exactly two 3-position blocks, measure its actual installed components and screw-access direction.
3. Dry-fit controller with factory PoE daughterboard, a plugged RJ45 and both populated perfboards on the existing P4 plate. Record maximum Z including wiring.
4. Check P4 insert size, actual M3 screw projection, enclosure ribs/lid gasket clearance, gland wall thickness and permissible cable entries.
5. Select separate safe PCB standoff anchorage only where P4 perforations and actual PCBs allow. Do not use arbitrary R2 mock riser coordinates as drill marks.
6. Print only the standalone wire-saddle coupon if desired; inspect its tie-hole pitch on P4 without forcing. No final installed mount can be designated mechanically accepted yet.
7. Resume electronics, power diagnostics and independent offsite notification acceptance under the existing safety and operational gates, **never** using this supplemental monitor in place of listed sprinkler controls, fire alarms, heating, or inspections.

## Verification limitations

The R2 layout and accessory test scripts are software acceptance only. They do not validate electrostatic isolation, heat dissipation, connector stack height, watertightness, physical vibration, long-term PETG creep or compliance with any fire-protection equipment standard. Tests should be repeated whenever dimensions or component placement change.
