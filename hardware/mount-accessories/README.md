# Device Lab — R2 cable-tie saddle, print-fit coupon only

**This is the only independently printable new part in this CAD iteration.** It is **not** an approved electronics board mount or final enclosure part.

### Intent
Provide a low-stress way to hold insulated sensor/control harness wires to the existing P4's perforated mounting plate without drilling the case or relying on adhesive. Use two small zip-tie tails through **nominal** grid holes to secure the saddle to P4 and pass one tie over the wire bundle. The part has two raised side rails to prevent sideward sliding. This is not a pulling/strain-relief fitting for the external sensor cables; real cable glands and strain relief remain a separate design task.

### Artifact
- `R2_P4_10mm_Wire_Tie_Saddle_FIT_TEST_ONLY.stl`: 26 × 16 × 8 mm, 3 mm foot and 5 mm rails.
- Two vertical holes, nominal **3.6 mm** diameter on **10.0 mm** centers. Source of pitch: prior P3 plate perforation grid; **verify against actual P4 holes** before any force or installation.
- Source generator: `generate_tie_saddle.py`, using Python 3 + NumPy, 0.2 mm voxel precision. 0.2 mm stepped hole walls are acceptable for a fit coupon, but not presented as precision bores.
- Receipt `R2_P4_10mm_Wire_Tie_Saddle_FIT_TEST_ONLY.json`: mesh dimensions, checksum, triangle count, independent build receipt.
- STL is a binary, closed, manifold mesh: 75,472 triangles, **zero non-manifold edges in generator topology check**.

### Suggested test print (not yet executed)
PETG with existing working Sally profile, flat face down, no support; 0.2 mm layers and 3–4 walls. Test one saddle first. Check hole alignment to P4, zip-tie size, printed hole clearance, surface contact, and the height above the deck. Do **not** force posts, bore holes in the enclosure, clamp active wiring under load or mount the circuit boards with this saddle. This accessory is low-stress and intended only for retaining insulated harness wires inside the de-energized box.

### Provenance and safety
The P4 STL is never modified. This accessory uses a *nominal grid assumption* from earlier plate design, so the physical trial is mandatory. It does not connect electrically to the sensor circuit. It does not change listed fire protection systems or certify environmental sealing. Use the exact R6 Board A/B pin tables, not concept images, for wiring.
