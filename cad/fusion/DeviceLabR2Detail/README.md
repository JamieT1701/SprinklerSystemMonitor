# DeviceLabR2Detail — Fusion model, checked layout and source-derived illustrations

**Status:** Autodesk Fusion R2 Python script installed but **not yet executed** because Oscar's foreground GUI session became unavailable remotely. Unlike R1, there is **no verified R2 Fusion export or hub save**. This directory is a durable handoff, not a completion claim.

## Source files

- `DeviceLabR2Detail.py` / `DeviceLabR2Detail.manifest`: Autodesk Fusion `adsk` Python API script. It imports the approved P4 STL as an unchanged mesh, constructs separate editable concept components for enclosure, Board A, ESP32, Board B, wiring supports, cable-entry location zones, and a hidden service lid, then creates a timestamped local F3D archive and JSON receipt. A successful run creates a NEW document; it does not overwrite R1/P4.
- `assembly-layout.json`: verified PCB/enclosure envelopes, R6 terminal metadata, corrected P4 Z placement, route grouping and open-fit gates. Fusion script preflights this data.
- `render_r2.py`: reproducible high-resolution 2D and 3D-style projective **model-derived engineering illustrations**, generated using Pillow, not claimed as native Fusion viewport screenshots.
- Artwork files are in `docs/assets/fusion-r2-*`.
- `make_3d_viewer.py` builds an interactive, static `docs/r2-viewer.html` directly from `assembly-layout.json`. No JavaScript libraries or cloud API are required. Browser QA on Oscar used headless Chrome CDP with 390×844 CSS-pixel iPhone-style emulation: no horizontal page overflow, all three boards visible, view mode toggles, lid/support toggles and exploded slider verified. This is not a test on an actual iPhone.

## Reproduce on Oscar

1. Confirm the approved STL is at `%USERPROFILE%\Documents\DeviceLab\Fusion\Project_Plate_P4_M3_Heatset_APPROVED_REFERENCE.stl`.
2. Confirm GitHub clone remains at `%USERPROFILE%\Documents\DeviceLab\SprinklerSystemMonitor`. Script deliberately stops if this clone's `assembly-layout.json` does not match the expected board elevations.
3. Open an **unlocked** Windows desktop, launch Autodesk Fusion, select workspace `Jamie's Device Lab → Device Lab CAD`.
4. Press **Shift+S** → **Scripts and Add-Ins** → **DeviceLabR2Detail** → **Run**.
5. Check `%USERPROFILE%\Documents\DeviceLab\Fusion\r2_detail_result.json` for `status: SUCCESS`; verify the timestamped F3D archive, viewport geometry and lid visibility.
6. Save only this newly created model to cloud as **Sprinkler Monitor R2 - Detailed Industrial Concept PROVISIONAL**.
7. Run new independent validation checks and update this handoff with runtime screenshots, saved receipt, and any corrected mistakes. **Do not mark mechanically accepted without actual dry-fit.**

To regenerate the renderings without opening Fusion:

```powershell
py -3 .\cad\fusion\DeviceLabR2Detail\render_r2.py
```

Pillow is required for PNG rendering; the electrical and mechanical JSON checks use Python standard library. The small accessory STL generator requires NumPy. The confirmed Oscar environment currently has both NumPy and Pillow.

## Mechanical safety and scope

The project is supplemental monitoring only. The exact P4 source file is hash-checked before R2 script execution and remains preserved. The original R1 assembly used an **incorrect reference Z translation** for the rotated plate and is superseded for vertical fit. R2 corrects it; see `docs/CAD-FUSION-R2-DETAILED-DESIGN.md`.

No mounting/drilling coordinates, case entry holes, screw sizes or physical clearance are approved from this study. One optional printed wire-saddle prototype in `hardware/mount-accessories` is the only new printable test piece, and it is not structural.
