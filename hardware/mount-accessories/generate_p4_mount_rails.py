"""P4 70mm perfboard mount rails v1, derived from owner-fit-tested coupon.

Keep exact coupon channel section, wall offsets, underside elevation and M3
mount slot shape. Increase running length for 50mm side of Boards A/B.

Run: python generate_p4_mount_rails.py
Requires cadquery. This DOES NOT create or change the accepted P4 plate.
No physical fit approval is implied for elongated rails.
"""
from pathlib import Path
import cadquery as cq

OUT=Path(__file__).resolve().parent
# Tested coupon profile (unchanged)
BODY_X=(-4.2,8.8)
SHELF_H=8.0
WALL_X=(3.4,4.6)
SLOT_HEIGHT=2.15
LIP_END_X=7.2
LIP_H=1.4
# New elongated feature. Target nominal 50mm PCB edge, allow 3mm each end.
RAIL_Y_LENGTH=44.0
# P4 has 10 mm hole spacing. Position slots 7 mm in from rail ends.
BOLT_Y=(-15.0,-5.0,5.0,15.0)
SLOT_L=5.0
SLOT_D=3.6


def block(x0,x1,y0,y1,z0,z1):
    return (cq.Workplane('XY')
            .box(x1-x0,y1-y0,z1-z0,centered=(False,False,False))
            .translate((x0,y0,z0)))


def make(side):
    if side not in ('left','right'):
        raise ValueError(side)
    ymin,ymax=-RAIL_Y_LENGTH/2,RAIL_Y_LENGTH/2
    part=block(BODY_X[0],BODY_X[1],ymin,ymax,0,SHELF_H)
    part=part.union(block(WALL_X[0],WALL_X[1],ymin,ymax,SHELF_H,SHELF_H+SLOT_HEIGHT))
    part=part.union(block(WALL_X[0],LIP_END_X,ymin,ymax,
                          SHELF_H+SLOT_HEIGHT,SHELF_H+SLOT_HEIGHT+LIP_H))
    for y in BOLT_Y:
        cut=(cq.Workplane('XY').center(0,y).slot2D(SLOT_L,SLOT_D,0)
             .extrude(SHELF_H+0.2).translate((0,0,-0.1)))
        part=part.cut(cut)
    if side=='right':
        part=part.mirror('YZ',union=False)
    return part

if __name__=='__main__':
    for name in ('left','right'):
        part=make(name)
        dest=OUT/f'P4_70mm_PCB_{name.upper()}_44mm_RAIL_V1.stl'
        cq.exporters.export(part,str(dest),tolerance=0.03,angularTolerance=0.1)
        bounds=part.val().BoundingBox()
        print(name,dest.name,'bbox',tuple(round(x,2) for x in (bounds.xlen,bounds.ylen,bounds.zlen)))
