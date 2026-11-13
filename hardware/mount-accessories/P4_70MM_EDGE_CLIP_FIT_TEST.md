# P4 70 mm PCB edge-clip mounting test pair — NOT mechanically accepted

**Status (2026-11-13):** standalone left/right fit coupons generated, mesh verified watertight, **not yet printed or physically fitted**. This is a mechanical correction for missed PCB-to-P4 mounting-hole alignment. Do not replace, resize, drill or reprint the owner's already fitting **P4** plate. Do not unsolder the finished PCBs.

## Source and observed physical layout

- Owner's overhead photo shows **Board A at the top, ESP32/PoE in the middle with RJ45 projecting right, and Board B at the bottom**. This reverses A/B vertical order in the older provisional R2 CAD; the **actual photo governs assembly position**. Board A and B are nominal 70×50 mm boards.
- Source artifact: the checksum-accepted `hardware/project-plate-p4/Project_Plate_P4_M3_Heatset.stl`, examined on Oscar.
- The existing P4 small hole columns were measured geometrically in the STL at X approximately **7.5799 mm** and **87.5799 mm**, at Y approximately **26.3262 + 10n mm (n = 0..9)**, hole diameter **3.4 mm**. These are independent of the four external enclosure-mounting feet.
- Photo confirms the two 70mm perfboards lie between the columns, but exact position and module stack height still require real-fit checks.

## Prototype bracket pair

- Parametric generator: `generate_p4_70mm_edge_clip_test.py` (Python + CadQuery); outputs mirrored `P4_70mm_PCB_LEFT_EDGE_CLIP_TEST_ONLY.stl` and `...RIGHT_...stl`.
- Each coupon is **13×24×11.55 mm**, with 2 mounting slots **10 mm apart**, 3.6 mm wide / 5.0 mm long, above P4's corresponding holes.
- Retaining channel allows **2.15 mm** nominal PCB thickness clearance; shelf raises PCB underside **8.0 mm** above the P4 top. Actual perfboard nominal 1.6 mm.
- Printed halves should face inward toward one another and be aligned to **matching left/right hole rows**. Designed for ~70mm nominal PCB width, with minor adjustment possible at bolt slots.
- Only suitable as a **fit test**. Small 24mm coupons are not a full-length board mount; design final rails/retention AFTER testing.

## Test procedure

1. With PoE/USB unplugged and sensor cables disconnected, print one left+one right coupon in PETG on Sally: 0.2mm layers, 3–4 walls, 20–30% infill, flat base down. Inspect the small retaining lip; supports may be needed if it droops.
2. Position the two brackets at any matching **adjacent** pairs of existing P4 side holes along one perfboard's accessible edge. Check both slots align freely; don't force.
3. Dry-fit a nominal 70mm board edge between the two opposing channels. Its underside should be elevated ~8mm and PCB should fit without bending, scraping solder, contacting live metal, or pressing on terminal blocks.
4. For a fastener trial, **M3×16 screws, M3 nuts, and underside washers** are a starting combination, not verified against on-hand hardware or case clearance. Two per bracket. The P4 plate is ~3mm thick with ~6mm feet; verify screw protrusion, underside clearance and enclosure fit before tightening.
5. If width/slot/height fit, scale up to separate full-span rails for Board A, Board B and a properly retained ESP32 socket carrier; dry-fit RJ45 bend and lid clearance. Do not depend on the removable header friction for RJ45 load.

**Do not call these test coupons final mounting, do not use adhesive alone, and do not power device or claim operational acceptance.** Hardware wiring R6, firmware and the P4 reference STL remain unchanged.
