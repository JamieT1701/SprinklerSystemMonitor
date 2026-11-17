# B1 — Complete Visual Design Package

**Device Lab / Sprinkler Monitor — 16 November 2026**

**Status: complete engineering *concept visualization* and reproducible CAD package. NOT a released PCB, certified product, or installation design.**

The product images and editable CAD represent a proposed **supplementary** monitoring product, not a listed fire-alarm device. The physical R6 prototype, all site sprinkler equipment, and existing approved electronics remain unchanged.

## Software — fully free and authorized for commercial design work

| Application | Version verified on Arthur | Role |
|---|---|---|
| FreeCAD | **1.1.4** | Editable solid assembly and full assembly STEP export |
| Blender | **5.3.0** | Materials, exploded/closed renders, editable .blend, interactive GLB |
| KiCad | **10.0.8** | Native 2-layer PCB *mechanical placement study*, footprints, silk and board render; **not routed** |
| Python | **3.14.4** | Source-controlled model generation, engineering diagram SVGs, host-only verification |

All three applications were installed via free user-level Flatpak on Arthur. Fusion Personal remains separate and was **not used**.

## Living 3D viewer (retained for future B1 revisions)

The permanent [interactive B1 review page](https://jamiet1701.github.io/SprinklerSystemMonitor/b1-viewer.html) now resolves all four GLB modes from the **active B1 engineering branch**, rather than freezing an old commit. When a reviewed revision regenerates and commits those GLBs, reloading the same viewer URL displays its new version. **The CAD-to-GLB export is an explicit QA/publishing step, not an unattended background process.** See [VIEWER-LIFECYCLE.md](VIEWER-LIFECYCLE.md) and run `python3 check_viewer_models.py` after exports. Before retiring or merging the B1 branch, re-point the viewer assets to the new durable source branch so the public URL remains usable.

## Open the deliverables

### For immediate review
- `outputs/renders/01_b1_closed_product.png` — closed clear-lid product with three plug-in cords (PoE, pressure, temperature).
- `outputs/renders/02_b1_service_open.png` — actual FreeCAD-source geometry rendered open.
- `outputs/renders/03_b1_exploded.png` — lid separated and PCB electronics exposed.
- `outputs/renders/04_b1_pcb_component_top.png` — detailed electronics-side concept layout.
- `outputs/renders/05_b1_field_ports.png` — three external panel-connectable sockets on the short wall.
- `outputs/renders/06_b1_wall_install_view.png` — opposite viewing direction.
- `outputs/renders/07_b1_kicad_board_top.png` — KiCad's **native** placement study, 21 footprints, marked unrouted.
- `outputs/renders/08_b1_dashboard_desktop.png` and `09_b1_dashboard_mobile.png` — responsive dashboard conceptual UI based on **synthetic** data only.
- `outputs/renders/B1_design_review_contact_sheet.png` — six-view review spread.

### To edit the physical design
- `outputs/B1_assembled.FCStd` — native editable FreeCAD assembly, 116 solid components.
- `outputs/B1_exploded.FCStd` — exploded/native FreeCAD scene.
- `outputs/B1_complete_reference_assembly.step` — neutral solid exchange format for many CAD packages.
- `outputs/B1_exploded_reference_assembly.step` — exploded neutral STEP.
- `outputs/B1_visual_assembly.blend` — editable Blender scene with material and studio lights.
- `outputs/B1_concept_interactive.glb` — portable interactive glTF binary; open in any GLB-capable viewer.
- `outputs/B1_lid_off.glb` — case open (cover removed) to inspect the carrier and electronic modules.
- `outputs/B1_exploded_assembly.glb` — lid raised and populated carrier lifted from base for individual assembly viewing.
- `outputs/B1_electronics_only.glb` — close examination of PCB, sockets, controller, ADC and field terminals with the enclosure removed.
- **Published web viewer:** https://jamiet1701.github.io/SprinklerSystemMonitor/b1-viewer.html — select Closed, Lid Off, Exploded, or Electronics Only; drag to rotate, scroll/pinch to zoom. All views use the same source Blender model and remain design surrogates.
- `b1_export_assembly_variants.py` — reproducibly exports all three alternate geometry-based GLBs from the native Blender scene.
- `outputs/B1_dashboard_demo.html` — standalone **interactive UI demonstration** (no backend, no network traffic, synthetic data and scenarios ONLY). Open locally in a browser.
- `electronics/B1_placement_NOT_ROUTED.kicad_pcb` — **KiCad PCB layout study**, not a board design.
- `outputs/meshes/` — FreeCAD-generated STL geometry for all 116 individual model pieces (provided in the packaged ZIP, not necessarily committed individually).
- `outputs/drawings/*.svg` — dimensioned mechanical view, block architecture, electrical review and multiple-device topology; editable vector illustrations.

### Source/reproducibility
- `B1_dimensions.json` — single source of nominal enclosure, carrier, module and port locations.
- `b1_freecad.py` — native solid generation.
- `b1_blender.py` — material/camera/render generation.
- `b1_kicad_placement.py` — **actual KiCad 10 pcbnew** footprint placement + 2-layer outline; no netlist/routing.
- `b1_diagrams.py` — technical presentation SVGs including the SPTD25 vendor-specific M12 pin 1+/pin 2-return warning.
- `b1_export_glb.py` — GLB export from Blender's native scene.
- `b1_contact_sheet.py` — printable visual summary generator.
- `outputs/B1_placement_DRC_UNQUALIFIED.txt` — real KiCad DRC report proving schematic/parity and clearance gates remain open.

## Actual geometry locked for the *visual concept only*

| Property | Value | Design maturity |
|---|---|---|
| Enclosure family | **Hammond 1554T2GYCL**, polycarbonate, clear lid | Manufacturer product family; its **molded internal geometry is represented as a simplified surrogate**, not an imported exact OEM STEP |
| Nominal outside | **180 × 120 × 90.5 mm** (length Y, width X, height Z) | From enclosure product family specifications, confirm exact variant with OEM drawing |
| Nominal maximum PCB allowance | **167.13 × 106.68 mm** | Manufacturer mechanical guideline; OEM screw boss geometry must be verified |
| Proposed carrier outline | **160 × 100 × 1.6 mm** | Native FreeCAD and KiCad study agree |
| Carrier Z lower face | **26 mm above modeled bottom** | Provisional standoff / PoE stacking, fit test required |
| Proposed M3 carrier holes | X = **±44 mm**, Y = **±70 mm** | Intentional pattern in both CAD & KiCad; **NOT manufacturer-confirmed boss alignment** |
| PoE cable entrance | X = **−35 mm**, Y near front wall, Z = **35 mm** | Candidate 20.8mm RJ45 bulkhead cutout, Amphenol LTW, cap/PoE/cable fit UNQUALIFIED |
| Remote temperature port | X = **0 mm**, Z = **35 mm**, candidate 12mm hole | M8 A-coded 3 pin DS18B20 bulkhead, final panel fit/cordset not qualified |
| Pressure loop port | X = **+35 mm**, Z = **35 mm**, candidate 16mm hole | M12 A-coded 4 pin pressure bulkhead, two poles NC, no actual process tapping on enclosure |
| Factory ESP module | Waveshare ESP32-S3-PoE-ETH, SKU **28771**, ~21 × 72.8 mm nominal | 2×20 pin socket location and module clearance are **surrogates** until exact board/header checked |
| Pressure ADC | **ADS1115 @ 3.3 V**, provisional 100 Ω current shunt | Functional concept, not electrically verified circuit |

The rendered pressure transducer, DS18B20 tip, connectors, PoE board, resistor and surge parts are **dimensionally illustrative substitutes**. They must be replaced or reconciled against selected manufacturer 3D STEP/footprints before any procurement, enclosure drilling, routing or tool production. The 3D scene cannot validate electrical fault safety.

## Selected electrical direction (not an approved netlist)

- One process-isolated two-wire **4–20 mA** current loop per B1; **no** direct fire-alarm, sprinkler valve, compressor or heating outputs.
- Preferred manufacturer-based **ProSense SPTD25-20-0100H 0–100 psig** 4-20mA/2-wire/8.5-36V M12 candidate; qualified site max range and pressure tap **not** approved. Physical housing model approximates manufacturer 18.9mm diameter × 66.9mm total length; not OEM imported STEP.
- **100 Ω 0.1%** shunt into protected 3.3 V **ADS1115**: 4 mA→0.400 V, 20 mA→2.000 V, 26 mA→2.600 V. ±4.096 V PGA **does not** allow analog input above 3.3 V supply.
- Three remaining ADS channels provisionally measure protected field L+, loop rail and 2.048 V reference-check source. Divider concept 270 kΩ / 22 kΩ; external miswire/ESD/backfeed clamp and loading not designed.
- Remote protected **DS18B20**, 3-wire, 4.7 kΩ pull-up to 3.3 V, with CRC and invalid/sentinel checks.
- Factory Waveshare PoE/Ethernet W5500 and ESP32-S3.
- **Pololu U3V9F24** as a provisional 5V→24V boost component, explicitly **not short-circuit protected**; the separate **TI TPS2662** adjustable eFuse family is a candidate high-side fault-current limiter, *not* selected/set/tested. This is the primary electrical fabrication blocker.
- Base revision has **no onboard lithium battery** or unverified dying-gasp supercapacitor. Cloud-side dead-man handles powered-off silence.

Read `../HARDWARE/FRONTEND-DESIGN.md`, `../HARDWARE/BOM-CANDIDATES.csv` and `../HARDWARE/calculation-receipt.json` before evolving the circuit. All code and tests are **host-only**.

## What prevents a real fabrication release

1. No installed sensor's actual approved MPN/range, source voltage, process/wetted materials, manufacturer 3D model and approved air-side tap requirements.
2. No real independent calculation/schematic review of the 24 V **indefinite-short-safe** boost + current limiter, ADC field miswire and ESD/surge/probe protections; no input-current/temperature testing.
3. No authentic KiCad electrical schematic, ERC, assigned pad netlist, routed PCB, **passing DRC**, Gerber or manufacturing drawing. A real KiCad 10 placement DRC was attempted: **8 pad-clearance violations** (provisional ADS1115 footprint vs stock board rules), no usable schematic parity check, and zero tracked unconnected nets only because **no electrical net assignments exist**. The DRC result is in `outputs/B1_placement_DRC_UNQUALIFIED.txt` and is **NOT A PASS**.
4. No OEM-accurate enclosure STEP/boss/gasket/port clearance and actual Waveshare mating/header mechanical measurements.
5. No complete quoted production BOM, safety/regulatory classification, calibrated pressure source or genuine network/alert reliability testing.

**Therefore no PCB, drilled enclosure, pressure transmitter or field installation may be ordered from this package.** Fabrication/field installation require physical and qualified review gates. It is honest to call the **visualization complete and source-editable**, not the product released.

## Regenerate on Arthur

Existing repo worktree: `/home/jamiet1701/.local/share/device-lab-advisor-competition/engineering-b1`.

```sh
cd /home/jamiet1701/.local/share/device-lab-advisor-competition/engineering-b1/research/selected-design-b1/CAD
flatpak run --user --filesystem="$PWD" --command=FreeCADCmd org.freecad.FreeCAD "$PWD/b1_freecad.py"
flatpak run --user --filesystem="$PWD" --command=python3 org.kicad.KiCad "$PWD/b1_kicad_placement.py"
flatpak run --user --filesystem="$PWD" --command=blender org.blender.Blender --background --factory-startup --python "$PWD/b1_blender.py"
flatpak run --user --filesystem="$PWD" --command=blender org.blender.Blender --background --factory-startup --python "$PWD/b1_export_glb.py"
python3 b1_diagrams.py
python3 b1_contact_sheet.py
```

The FreeCAD script checks solid-shape validity and prints `FREECAD_OK`, KiCad script re-opens the board and prints `B1_KICAD_PLACEMENT_OK`, SVG generator validates content. All native model files and images belong to the **draft** `design/claude-b1-engineering-20261116` branch. Never merge without electrical, mechanical and safety review.

## Official source links

- [Hammond 1554T2GYCL enclosure](https://www.hammfg.com/part/1554T2GYCL)
- [Waveshare ESP32-S3 Ethernet/PoE](https://docs.waveshare.com/ESP32-S3-ETH)
- [Texas Instruments ADS1115](https://www.ti.com/product/ADS1115)
- [Pololu 24 V step-up regulator #5588](https://www.pololu.com/product/5588/specs)
- [Texas Instruments TPS2662 family](https://www.ti.com/product/TPS2662)
- [Analog Devices DS18B20](https://www.analog.com/en/products/ds18b20.html)
- [KiCad free open-source EDA](https://www.kicad.org)
- [FreeCAD free parametric mechanical CAD](https://www.freecad.org)
- [Blender free 3D rendering](https://www.blender.org)

**Design/validation boundary:** Owner selected the future commercial candidate. This package does **not** change the separately maintained existing monitor or fire-protection system and makes **no** certification, product-accuracy, cost or installed-performance claim.

## B1 Rev B plug-in I/O (2026-11-16)

Three distinct external user service ports: **PoE Ethernet P1 (shielded RJ45 bulkhead)**, **remote temperature P2 (M8 A-coded 3)**, and **industrial two-wire 4-20mA pressure P3 (M12 A-coded 4)**. Open the lid only for true factory electronics service, not routine sensor/cable swaps. **AUX FUTURE** on right side wall is a non-drilled, non-connected marking, not a fourth powered sensor port. Connector shells in FreeCAD/Blender are approximate MPN-based envelopes and **not approved drill geometry**. The case's original manufactured wall must accept sealed panel sockets and strain relief; actual RJ45 with cap can require panel thickness below the nominal 3.94mm local CAD wall, so physical OEM STEP/spotface design is a release blocker. See [CONNECTOR-REDESIGN](../HARDWARE/CONNECTOR-REDESIGN.md) for exact candidate parts, NC pins, PoE and environmental gates. IP54 is an unverified *whole-product target* only.

### B1 selected pressure-sensor revision: manufacturer-based remote model

Source design now names **SPTD25-20-0100H**, 0-100psig, 1/4in MNPT, two-wire 4-20mA, 8.5-36V. The illustrated remote sender has a **66.9mm overall envelope and 18.9mm outer diameter** based on the AutomationDirect vendor 2D drawing, with approximate M12 top cap and hexagonal tool flats. This is **not genuine supplier 3D CAD**, a production dimensional drawing, or an approved process tap. The cabinet P3 M12 4-contact uses **sensor pin1 +, sensor pin2 return, contacts3/4 NC**. The proposed cable is `CDP12-0B-030-AA` 3m female-to-male M12, with pin continuity and fit to verify. Check [full sensor decision](../HARDWARE/PRESSURE-SENSOR-SELECTION.md).

## Native KiCad 24 V field-power schematic — 2026-11-16

**Verified KiCad 10 ERC = 0 errors / 0 warnings** for the *limited field-power/loop path only*, with the **upstream 5V supply explicitly assumed as an external bench source**. The real KiCad exported netlist has 18 custom-sourced electrical symbols, 13 intentionally connected nets, and P3 contacts 3/4 separately no-connected. The source is `electronics/B1_24V_FIELD_POWER_REVIEW.kicad_sch`, with local symbols `electronics/B1_Bench.kicad_sym`, project `electronics/B1_24V_FIELD_POWER_REVIEW.kicad_pro`, `electronics/sym-lib-table`, deterministic generator `electronics/generate_b1_frontend_schematic.py`, ERC report, exported XML netlist, `electronics/check_frontend_netlist.py` and drawable native `outputs/drawings/B1_24V_FIELD_POWER_REVIEW.svg`. **The unresolved ADC powered-off/surge/miswire protection means this is NOT a complete B1 circuit or PCB fabrication approval**. Existing unrouted placement board has unrelated eight physical clearance DRC failures; not resolved by a field-power ERC. See [formal review](../HARDWARE/EFUSE-SCHEMATIC-REVIEW.md).
