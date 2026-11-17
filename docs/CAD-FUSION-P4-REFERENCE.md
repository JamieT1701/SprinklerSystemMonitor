# Device Lab — Autodesk Fusion P4 CAD reference

Date: 2026-11-12 (Eastern). This document records completed computer/CAD work only. It does **not** change the sprinkler-monitor wiring, hardware acceptance or safety system status.

## Verified Fusion state on Oscar

- Device: Oscar, Windows 11, Remote Desktop Commander device `JamiePC_HPOmen`.
- Autodesk Fusion Personal installed and interactive, signed into Jamie's personal Autodesk account.
- Hub: **Jamie's Device Lab**; Fusion project: **Device Lab CAD**.
- Basic API smoke test passed: native parametric 80×50×3 mm mounting plate, four 4.5 mm holes; two sketches, two extrusion features, one body. F3D and STL exports created and verified. Test model saved to the hub as **DeviceLab API Test Mounting Plate**.
- Native P4 reference imported and cloud-saved as **P4 APPROVED Mounting Plate - Exact STL Reference** in the same project; import script completed successfully and exported F3D locally.
- Fusion native API is available in-app via **Shift+S → Scripts and Add-Ins**; no Autodesk Desktop Connector, extra purchase or background service is required.

## Approved P4 — unmodified reference

Canonical source: `hardware/project-plate-p4/Project_Plate_P4_M3_Heatset.stl`.

SHA-256: `1b2c593862eefe328c76ad1b6fe5e358a4fb71e1e7dc10909f55384ac18ff9f2`.

Measured mesh envelope: **95.1599 mm (X) × 142.652 mm (Y) × 9.0 mm (Z)**, including the four mounting feet. STL contains **34,160 triangles** and is an ASCII OpenSCAD export. Two Oscar Downloads copies were byte-identical. The repository copy was verified identical.

Fusion imported the mesh with `MillimeterMeshUnit`, into a parametric document using a dedicated base feature. It returned one mesh body. Its bounding box **exactly matched** the measured STL dimensions. The original P4 STL was not modified or rescaled. The imported mesh is a **reference**, not a parametric recreation of the mounting plate.

## Files / recovery

On Oscar:

- `%USERPROFILE%\Documents\DeviceLab\Fusion\Project_Plate_P4_M3_Heatset_APPROVED_REFERENCE.stl` — verified copy.
- `%USERPROFILE%\Documents\DeviceLab\Fusion\P4_Approved_Reference_20261112_001200.f3d` — successfully exported Fusion archive.
- `%USERPROFILE%\Documents\DeviceLab\Fusion\p4_mesh_measurement.json` — source dimensions/hash.
- `%USERPROFILE%\Documents\DeviceLab\Fusion\p4_fusion_import_result.json` — in-app execution receipt.
- Fusion script installed at `%APPDATA%\Autodesk\Autodesk Fusion 360\API\Scripts\DeviceLabP4Reference\`; portable source is in `cad/fusion/DeviceLabP4Reference/`. The source script only produces a new design and local exports; it does **not** auto-save to Autodesk cloud.

The user can find the cloud reference in Fusion → hub **Jamie's Device Lab** → project **Device Lab CAD**. Existing designs must not be overwritten when making a study or derivative.

## Next engineering task / gates

The confirmed-fitting P4 plate is ready to be the *fixed* mechanical reference for an **assembly layout study**, but actual Board A/Board B/controller support positions are not yet physically verified. Preserve the accepted P4 mesh and build any proposed supports in separate editable parametric components, each labelled **PROVISIONAL** until dry-fit. Do not drill or heat-set the enclosure based on an unverified drawing.

Current electrical build remains as recorded in `docs/HANDOFF-2026-11-11-BOARD-A.md`: Board A components soldered, **0/10 underside jumpers confirmed installed**, no continuity measurements or powered acceptance. Next owner physical step is finishing those links in small coordinate-specific groups, unpowered, then testing continuity. Board B and full system bring-up remain open.
