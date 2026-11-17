# P4 PCB mounting rails V1 — owner-tested coupon geometry

**Checkpoint, 2026-11-13:** The owner says the previously delivered **24 mm left/right test clips work great** on the original P4 plate. This is direct physical fit feedback for the **test coupons only** (not installation acceptance for longer rails or full electronics).

## V1 elongated rails ready to print and physically test

- Source: `hardware/mount-accessories/generate_p4_mount_rails.py` (CadQuery); reproducible two STL exports. A ZIP with both verified STLs, generator, and installation guide was delivered in the Device Lab chat on 2026-11-13.
- Carry forward **exact tested x/z geometry**: 13 mm base width, 8 mm PCB underside elevation, 2.15 mm channel height, 1.4 mm retaining lip.
- Extend Y from 24 to **44 mm**, covering most of a 50 mm perfboard edge. Four M3-form elongated slots at **10 mm centers** (Y = -15, -5, +5, +15); 3.6 mm wide, 5.0 mm total slot length.
- Two mirrored variants: `P4_70mm_PCB_LEFT_44mm_RAIL_V1.stl` and `P4_70mm_PCB_RIGHT_44mm_RAIL_V1.stl`; each 13 x 44 x 11.55 mm bounding envelope. Both exports tested as **watertight, consistent-winding triangle meshes**. This is digital QA, **not** physical installation acceptance.
- Print **2 LEFT, 2 RIGHT** for Board A and B in PETG on Sally (0.2 mm layers, four walls, 25–30% infill, flat base down). **Print just one pair first** to validate 44 mm length in the installed layout; longer rail might overlap access routes even though 24 mm pair fits.
- Unpowered mounting: position paired L/R facing in at matching P4 side holes; use at least two properly aligned bolts per rail (additional slots optional); keep metal fasteners and underside protrusions clear of pads, case floor, and components. Check real screw length, enclosure clearance and RJ45 bend. Do **not** modify P4 or the soldered PCBs.

## Required anti-slide restraint

The rails capture **board side edges**, but their longitudinal channel ends remain **open**. This is NOT complete secure retention on its own. After fit-checking, add a removable, nonconductive longitudinal restraint. A nylon cable tie from an **unused large corner PCB mounting hole** to a P4 opening may work if physically accessible, without contact with copper pads or any soldered parts. Otherwise design a positive, purpose-fit end keeper before accepting or installing electronics. Do not rely on harness wiring, header friction, or adhesive for restraint.

## ESP32 carrier remains separate mechanical gate

The short ESP32 female-socket carrier's real footprint and PoE/RJ45 stack were not independently measured. These 44 mm rails target the confirmed **70 x 50 mm Board A and B**, not an unverified carrier. If the carrier is 70 mm wide, the original proven 24 mm pair may fit, but test RJ45 access and independent cable strain relief separately. The controller should remain unplug-able without flexing its female sockets.

## State and safety

The photo documented in PR #1 shows Board A above the ESP32 and Board B below on the existing P4. Physical A/B component installation and unpowered electrical checks are owner-reported complete. **Inter-assembly W01–W09 is not accepted as wired, no power-on or deployed v5-47k firmware is claimed, and alerts are not operationally accepted.** Preserve the already accepted P4 STL, R6 electrical design, draft PR #1 and active branch. This is a supplementary monitor, not a sprinkler/fire protection controller.
