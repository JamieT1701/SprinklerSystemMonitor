# Project plate P2 - scan-informed fit prototype

Prepared from Jamie's `11112026.pdf`, page 1, for the selected parts-storage case. Not printed, screw-tested, enclosure-fit-tested or accepted. P1 remains in history; P2 has a DIFFERENT case screw pattern. No electrical design, firmware or printer action is part of this change.

## Scale and limitations
The embedded 3382 x 4398 raster maps to 214.757 x 279.273 mm in the PDF: approximately 400 dpi in each direction. The stated Letter sheet is 215.9 x 279.4 mm, so the file is slightly cropped or has a small scale discrepancy. Use the embedded PDF physical mapping rather than stretching the page to Letter. Forced Letter scaling would increase trace width by about 0.56 mm.

Smoothed pen-centerline exterior bounds: approximately 104.4 W x 151.9 H mm. Visible left-side recess: approximately 2.6 mm deep, roughly 56-95 mm down from the top. Paper calibration supports 2D contour measurement, NOT interior wall thickness, taper, rib positions or depth. Practical tracing/scale uncertainty is assumed around 0.5-1 mm, not certified.

The exterior tracing was fitted to the owner's PREVIOUSLY REPORTED 97 W x 150 H mm interior envelope, treated as the pre-rail wall-to-wall limit. This is an inferred interior shape, not an independently scanned inner wall. The shape is then offset inward by 3.4 mm on all edges: 3.0 mm rail allowance plus 0.4 mm sliding allowance. Final bounds approximately 90.2 W x 143.2 H mm. Minimum computed inset after curve simplification: 3.364 mm. Preserve the notch, but test its interior fit rather than assuming the outside notch exactly matches the inside.

## Hardware and print
PETG, existing tuned printer profile, 100% scale, 0.20 mm layer, 4 walls, 5 top/bottom layers, 25% infill, no supports. Flat face down, posts UP during printing; install inverted with posts DOWN against the case floor. Electronics require separate insulating PCB spacers.

Plate 3 mm thick; 106 holes of 3.4 mm diameter on 10 mm pitch; four 6 mm posts (9 mm total height). Posts 10 mm diameter, reinforced bases 14 mm. Blind pilot 2.5 mm diameter x 7 mm deep, closed floor 2 mm. Trial pilot for approximately 3 mm plastic/self-tapping screws; actual screw remains unknown. Maximum screw projection beyond case INNER wall: 5 mm. Hand-tighten only.

Post centres in model XY, from bounding-box bottom-left: (10,10), (80.17162,10), (10,133.17417), (80.17162,133.17417). Centre spacing approximately 70.17 x 123.17 mm. Do not reuse the P1 drilling pattern.

## Print the fit frame first
In OpenSCAD select `part="fit_frame"`. It has the SAME outer contour, 3 mm base, post positions and post height, but an open centre. Modeled solid volume is about 21% of the full plate. Check rails, floor ribs, post seating, orientation and lid clearance without forcing the frame. Then print `part="plate"`. An optional `part="post_test"` is a 20 x 20 mm screw-test coupon.

## Validation
All three exported meshes: one connected body, watertight, consistent winding and positive volume. Full plate bounds 90.1716 x 143.1740 x 9 mm; 106 through-grid holes; four blind pilots confirmed by cross-sections (107 loops at z=1, 111 at z=2.5, 8 at z=8.5). Source blob was re-fetched and verified identical to exported source.

Main STL SHA256: `e70463af40930f7ee5226aa47b4767016a3d1c034fa098273693229d3970d6f1`

Fit-frame STL SHA256: `e71852abac3c1b52253e4cde725940907710271a401903dd26a8b9d8202c7913`

SCAD SHA256: `0a4ec66e75bdf23a8fc59c49190d33637551d714d9bb3ae5526f67fb63f52c9d`

Conversation package also contains a 1:1 fit template PDF (print Actual size, check 50 mm bar), real CAD/scan comparison PNG, detailed measurement JSON and mesh receipts. The original uploaded scan was not published to GitHub. No current device or alert status is claimed by this mechanical review.
