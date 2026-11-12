# P4 PETG project mounting plate — approved print reference

**Status:** Physical case fit reported by owner; **not** validated as a populated electronics assembly. Do not substitute earlier P1–P3 models or speculative P5 dimensions.

## Verified exact artifact

- File: `Project_Plate_P4_M3_Heatset.stl` (ASCII STL from OpenSCAD).
- SHA-256: `1b2c593862eefe328c76ad1b6fe5e358a4fb71e1e7dc10909f55384ac18ff9f2`.
- File size: 5,466,888 bytes, 34,160 triangles.
- Axis bounds in source STL coordinates, in **millimeters**: X `0.0000..95.1599`, Y `0.0000..142.6520`, Z `0.0000..9.0000`.
- Bounding envelope **95.1599 × 142.652 × 9 mm** includes the 6 mm feet and 3 mm plate; it does **not** imply a 9 mm-thick flat plate.
- Two original downloads on Oscar, `Project_Plate_P4_M3_Heatset.stl` and `Project_Plate_P4_M3_Heatset (1).stl`, were independently SHA-256-verified as byte-identical.
- The repository file was copied byte-for-byte and verified against the same hash.

## Fit and assembly boundaries

Jamie previously reported this P4 plate fits the enclosure perfectly. Four feet are intended for M3 heat-set inserts and screws from outside the enclosure. Inserts, actual screw engagement, electronics clearance and connector bend space still need physical verification. The four feet attach the **plate to the case**, not the circuit boards to the plate.

Mount Board A (ADS1115 pressure circuit), Board B (field terminals and temperature pull-up), and the Waveshare ESP32-S3 Ethernet/PoE board with separate insulated supports or appropriate ties **after** dry-fitting their actual components. Do not model electronic board mounting locations as approved until measured. Consult `docs/BUILD-GUIDE.md` for the authoritative R6 electrical build.

This STL is the exact accepted **mesh**, not an editable parametric OpenSCAD/Fusion source. The original P4 OpenSCAD source was not located in the project branch or the searched local directories; do not claim that a CAD reconstruction is the accepted original. Fusion imports can reference this mesh in a separate model without modifying it.

See `docs/CAD-FUSION-P4-REFERENCE.md`.
