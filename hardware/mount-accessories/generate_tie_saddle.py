"""Generate a small no-drill, cable-only PETG wire-saddle fit prototype.
This is not a circuit board mount or a validated case component.
Geometry is created as a watertight 0.20 mm voxel solid, no external CAD dependency.
"""
import argparse, collections, hashlib, json, math, pathlib, struct
import numpy as np

PITCH=0.2
X,Y,Z=26.0,16.0,8.0
BASE_Z=3.0
HOLE_R=1.8
HOLE_CENTERS=[(8.0,8.0),(18.0,8.0)]
OUT=pathlib.Path(__file__).with_name("R2_P4_10mm_Wire_Tie_Saddle_FIT_TEST_ONLY.stl")

# Each occupied voxel is solid; a pair of 3.6-mm through holes align to
# a nominal 10-mm hole pitch on the accepted P4. Slotted-tie geometry still
# needs actual print and hand-fit with the owner's PETG profile.
def make_occupancy():
    nx,ny,nz=[round(s/PITCH) for s in (X,Y,Z)]
    gx=(np.arange(nx)+0.5)*PITCH
    gy=(np.arange(ny)+0.5)*PITCH
    gz=(np.arange(nz)+0.5)*PITCH
    xx=gx[:,None,None]
    yy=gy[None,:,None]
    zz=gz[None,None,:]
    holes=np.zeros((nx,ny,1),dtype=bool)
    for hx,hy in HOLE_CENTERS:
        holes|=(xx-hx)**2+(yy-hy)**2<HOLE_R**2
    lower=(zz<BASE_Z)&~holes
    # Open-top rails stop wires rolling sideways, while a zip tie through
    # the two separate holes retains the bundle; PETG is not load-bearing.
    rails=(zz>=BASE_Z)&((xx<3.0)|(xx>=23.0))
    return lower|rails

# Face vertices are integer grid indices. Quads are split consistently into
# triangles, which makes all shared edges count twice in a manifold surface.
FACES=[
((-1,0,0),[ (0,0,0),(0,0,1),(0,1,1),(0,1,0)]),
((1,0,0), [ (1,0,0),(1,1,0),(1,1,1),(1,0,1)]),
((0,-1,0),[ (0,0,0),(1,0,0),(1,0,1),(0,0,1)]),
((0,1,0), [ (0,1,0),(0,1,1),(1,1,1),(1,1,0)]),
((0,0,-1),[ (0,0,0),(0,1,0),(1,1,0),(1,0,0)]),
((0,0,1), [ (0,0,1),(1,0,1),(1,1,1),(0,1,1)]),
]

def generate():
    solid=make_occupancy()
    nx,ny,nz=solid.shape
    tri_count=0
    quad_count=0
    # Stream to temp and then write finalized header.
    temp=OUT.with_suffix(".tmp")
    edges=collections.Counter()
    with temp.open("wb") as handle:
        handle.write(b"DEVICE LAB R2 P4 WIRE SADDLE - FIT TEST ONLY".ljust(80,b" "))
        handle.write(struct.pack("<I",0))
        for i,j,k in np.argwhere(solid):
            i=int(i);j=int(j);k=int(k)
            for normal,offsets in FACES:
                ni=i+normal[0];nj=j+normal[1];nk=k+normal[2]
                if (0<=ni<nx and 0<=nj<ny and 0<=nk<nz and solid[ni,nj,nk]):
                    continue
                quad=[(i+dx,j+dy,k+dz) for dx,dy,dz in offsets]
                for a,b,c in ((quad[0],quad[1],quad[2]),(quad[0],quad[2],quad[3])):
                    edges[tuple(sorted((a,b)))]+=1
                    edges[tuple(sorted((b,c)))]+=1
                    edges[tuple(sorted((c,a)))]+=1
                    vertices=[n*PITCH for vertex in (a,b,c) for n in vertex]
                    handle.write(struct.pack("<12fH",*normal,*vertices,0))
                    tri_count+=1
                quad_count+=1
    with temp.open("r+b") as handle:
        handle.seek(80);handle.write(struct.pack("<I",tri_count))
    nonmanifold=sum(1 for v in edges.values() if v!=2)
    if nonmanifold:
        temp.unlink()
        raise RuntimeError(f"Non-manifold test: {nonmanifold} edges do not have exactly 2 triangle faces")
    if not (tri_count>100 and tri_count<500000):
        raise RuntimeError("Unexpected triangle count")
    temp.replace(OUT)
    data=OUT.read_bytes()
    assert len(data)==84+50*tri_count
    assert data[0:80].startswith(b"DEVICE LAB R2")
    sha=hashlib.sha256(data).hexdigest()
    receipt={
        "status":"MANIFOLD_BINARY_STL_CREATED",
        "validation":"GEOMETRY_VERIFIED_ONLY - physical fit not verified",
        "filename":OUT.name,
        "bytes":len(data),
        "triangles":tri_count,
        "quads":quad_count,
        "edge_manifold_errors":nonmanifold,
        "size_mm":[X,Y,Z],
        "resolution_mm":PITCH,
        "through_hole_diameter_nominal_mm":2*HOLE_R,
        "hole_center_pitch_mm":10.0,
        "source_assumption":"P4 grid-hole spacing 10mm from prior P3 design; visually align against P4 before use",
        "use":"Low-stress wire management only; bench fit-test. NOT for mounting boards or sprinkler safety controls.",
        "sha256":sha
    }
    OUT.with_suffix(".json").write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf8")
    return receipt

if __name__=="__main__":
    print(json.dumps(generate(),indent=2))
