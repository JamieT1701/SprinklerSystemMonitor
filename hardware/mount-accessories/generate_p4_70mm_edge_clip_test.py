"""P4 70mm perfboard edge-clip FIT-TEST coupons. Does not modify P4.

P4 approved STL measured on Oscar 2026-11-13:
  left hole center x=7.579925 mm, right x=87.579900 mm
  y=26.3262 + 10*n mm (n=0..9), approx 3.4mm hole diameter.
Design supports nominal 70 x 50mm boards, 1.6mm thickness.
These 24mm coupons are NOT a final PCB retention system; print and test
physical fit before sizing full mounting rails.

Requirements: Python 3 + cadquery.
Usage: python generate_p4_70mm_edge_clip_test.py
"""
from pathlib import Path
import cadquery as cq

OUTPUT = Path(__file__).resolve().parent
BASE_X0, BASE_X1 = -4.2, 8.8
Y_LENGTH = 24.0
STANDOFF = 8.0
WALL_X0, WALL_X1 = 3.4, 4.6
SLOT_Z = 2.15
LIP_X1 = 7.2
LIP_Z = 1.4


def box(x0, x1, y0, y1, z0, z1):
    return (cq.Workplane("XY")
            .box(x1-x0, y1-y0, z1-z0, centered=(False, False, False))
            .translate((x0, y0, z0)))


def make_clip(side):
    if side not in ("left", "right"):
        raise ValueError(side)
    y0, y1 = -Y_LENGTH/2, Y_LENGTH/2
    base = box(BASE_X0, BASE_X1, y0, y1, 0, STANDOFF)
    wall = box(WALL_X0, WALL_X1, y0, y1, STANDOFF, STANDOFF+SLOT_Z)
    lip = box(WALL_X0, LIP_X1, y0, y1,
              STANDOFF+SLOT_Z, STANDOFF+SLOT_Z+LIP_Z)
    part = base.union(wall).union(lip)
    # Two elongated M3 bolt slots at 10.0mm centers matching P4's hole pitch.
    for y in (-5.0, 5.0):
        through = (cq.Workplane("XY").center(0,y).slot2D(5.0,3.6,0)
                   .extrude(STANDOFF+0.2).translate((0,0,-0.1)))
        part = part.cut(through)
    if side == "right":
        part = part.mirror("YZ", union=False)
    return part


if __name__ == "__main__":
    for side in ("left", "right"):
        item = make_clip(side)
        target = OUTPUT / ("P4_70mm_PCB_" + side.upper() + "_EDGE_CLIP_TEST_ONLY.stl")
        cq.exporters.export(item, str(target), tolerance=0.03,
                            angularTolerance=0.1)
        print(target)
