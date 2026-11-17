# B1 design verification report — 2026-11-16

This report distinguishes **verified engineering artifacts** from *unverified safety/fabrication claims*. It is part of the CAD package, not a certification.

## Evidence actually obtained on authorized Arthur

| Verification | Result | Coverage limits |
|---|---|---|
| FreeCAD 1.1.4 solid-generation run | **PASS** — `FREECAD_OK 116 parts` | The enclosure and sensor bodies are dimensioned **surrogates**, not exact OEM geometry |
| Part solid integrity | **PASS** — `Shape.isValid()` for each modeled part | Mathematical solidity is not an assembly collision, thermal or IP seal test |
| FreeCAD native models | **SAVED** — assembled and exploded `.FCStd` | Parametric generator script is the actual reproducible source |
| STEP exchange | **SAVED** — complete and exploded `.step` | STEP contains appearance/clearance surrogate parts |
| Blender 5.3.0 | **PASS** — six revised Cycles renders with corrected exposure | Render plausibility does not verify electronics, connector placement or drill positions |
| Portable 3D | **PASS** — Blender exported `B1_concept_interactive.glb` | Contains presentation materials and appearance geometry |
| KiCad 10.0.8 footprint placement | **PASS** — native `.kicad_pcb` saved/reopened with **21 footprints** | **NO SCHEMATIC, no netlist, no routing**; placement study only |
| KiCad PCB DRC | **FAIL / BLOCKER** — **8 clearance violations** and no schematic parity | Pad spacing of provisional ADS1115 footprint relative to default 0.20 mm clearance; cannot call any DRC pass |
| KiCad "unconnected" count | 0 reported only because **nets were never assigned** | NOT evidence that all electrical nets are wired |
| Native KiCad board render + SVG | **PASS** — physical outline/footprints viewed, text says NOT ROUTED | KiCad drawing and native FreeCAD mechanical model use common dimensions; footprint sizing not qualified |
| Four engineering diagram SVGs | **PASS** — generated and XML parsed | Descriptive diagrams, not an electrically simulated netlist |
| Host-only Python B1 logic/math | **PASS** — **53** synthetic tests (previous checkpoint) | NOT embedded ESP firmware, not current source sensor QA or actual SMS delivery |
| Dashboard proof-of-layout | **PASS** — standalone HTML opened in headless Chrome; desktop/mobile PNG captures | JS states are synthetic; no service deployed or external notification tested |
| Privacy segregation | **PASS** — no personal inspection/vendor quotes/correspondence included | Product architecture is generic and not an installation approval |

## Lock-in decisions for a detailed pre-fab plan

- **Reuse factory WiFi/Ethernet/PoE MCU module** during low-volume development; do not design RJ45/magnetics/PD from scratch.
- **One 2-wire 4–20mA pressure channel** with controlled hardware output current limit and separate protected analog input. Current sensor family/pressure range and physical process connection remain **unselected until qualified review**.
- **100Ω 0.1%** shunt to ADS1115 family; 3.3V ADC and physical input absolute limits respected, ESD/transient and unpowered input behavior unresolved.
- **Factory PoE feeds 5V**, boost to 24V only through verified current/short protection; provisional Pololu 5588 + TPS2662 eFuse **not a released circuit**.
- **One DS18B20 1Wire probe**, CRC and cable-fault detection, external field ingress protection to be calculated/tested.
- **No integral backup battery, no cellular radio, no new mains voltage wiring** in base unit. Offsite independent liveness must detect power/network silence.
- **One channel/unit**, repeat per approved independent pressure domain; software aggregation cannot mark a site NORMAL with missing/stale devices.
- **Hammond clear-lid 1554T2GYCL** concept with *unqualified* 100x160 carrier, 3 external ports; fit/fabrication requires exact OEM mechanical model and in-hand module measurements.

## Required before a true 'fully engineered' fabrication design

1. Obtain OEM enclosure STEP/solid drawing, exact Waveshare module PCB CAD/PoE stack, approved fitting/terminal/glands and 4–20mA transmitter MPN, and measured pin/header/port locations. Update FreeCAD geometry and rerun fit/interference.
2. Select sourceable **continuous-short-safe** 24V current limit, component-tolerance limits, minimum transmitter compliance voltage, thermal/surge/miswire/ESD/backfeeding. Design/peer-review full KiCad native schematic.
3. Run electrical simulation or dedicated lab circuit with deliberate faults, including ADC VDD absent and 24V fed accidentally onto any field terminal.
4. Map actual nets and pin roles to verified KiCad footprints; then route, copper clearances, planes, drill keepouts, EMI/ESD and return paths. Full ERC/DRC must pass with **no waived critical violation**; inspect 3D and CAM/fab. Authorize fabrication **only after** further owner approval.
5. Calibrate industrial pressure transmitter with traceable test instrument, cold/condensation/PoE loaded bench tests, and independent cloud loss/alert delivery end-to-end with site-approved thresholds. No connection to live sprinkler trim outside qualified installer work.
6. Price sourceable BOM tier quantities and validate regulatory electrical, enclosure, emissions, cybersecurity and fire-protection supplemental-equipment boundaries before customer pilots.

## Reproduction record

- `b1_freecad.py`: reconstruct native CAD, 116 solids and export FCStd/STEP/meshes.
- `b1_kicad_placement.py`: reconstruct **UNROUTED** KiCad10 study; run DRC again after schematic and mechanical refinement.
- `b1_blender.py`: import FreeCAD STLs, render six physical views and save editable Blender scene.
- `b1_export_glb.py`: write portable interactive GLB.
- `b1_diagrams.py`: generate vector block/geometry illustrations.
- `b1_contact_sheet.py`: build picture summary.
- `outputs/B1_dashboard_demo.html`: standalone interactive interface with explicitly synthetic state selector and no provider calls.

**Release state as of this package:** Visual design assets **complete and editable**; electrical circuit and manufacturer mechanical interfaces **not yet verified**; manufacturing **NOT APPROVED**.

## Rev B connector status

CAD model now represents 116 valid FreeCAD solids with three exterior removable mating connectors (RJ45/M8/M12) and a solid, undrilled AUX side-wall marker. Ten additional host-only geometry/port-contract tests verify nominal face gap and enclosure edge margins, distinct keyed types, candidate hole diameters and non-drilled AUX. **Neither IP54, actual manufacturer fit, PoE continuity, safe hot-plug nor a working M12 pressure/current-loop electrical interface has been physically verified.** The original KiCad board study is unchanged and unrouted. The connector redesign does not repair its existing 8 DRC issues.

### B1 remote transmitter CAD update

The remote illustrative pressure sender geometry follows ProSense SPTD25-20-0100H **manufacturer dimensional envelope**: OD 18.9mm, total length 66.9mm, 1/4 MNPT and M12 electrical connector. Geometric depiction is approximate (not OEM original STEP). The new sensor identity, pin1/pin2 M12 functions and 0-100psig gain are captured as a provisional bench configuration. Existing sensor-count tests and new vendor-specific current-loop fault tests are synthetic only; no real pressure, PoE, or cable bench testing occurred.
