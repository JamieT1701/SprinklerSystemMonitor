"""Generate internal/exploded variants for the public B1 3D viewer.

Uses the exact same validated source Blender assembly as the closed model;
only render selection/rigid object positions change. No new fabricated
geometry is claimed. Exports GLB using Blender 5.3.
"""
import bpy, json, struct
from pathlib import Path

cad=Path(__file__).resolve().parent
out=cad/"outputs"
bpy.ops.wm.open_mainfile(filepath=str(out/"B1_visual_assembly.blend"))
allowed={"MESH","CURVE","FONT"}
base={o.name:o.location.copy() for o in bpy.data.objects}
record={}

def category(o):
    n=o.name
    if n.startswith(("Photo backdrop", "Cover line")): return "STAGE"
    if n.startswith(("Presentation pressure sensor cord","Presentation DS18B20 cable")): return "SENSOR_CABLES"
    if n.startswith(("Exterior decal","Cover title","Cover subtitle","Cover policy","Cover warning")):return "LID_LABEL"
    if n.startswith(("02_","03_","04_")):return "LID"
    if n.startswith(("01_","70_","71_")):return "CASE"
    if n.startswith(("80_","81_","82_","83_")):return "SENSORS"
    if n.startswith(("10_",)):return "MOUNT"
    if n.startswith(("20_","21_","22_","30_","31_","32_","33_","34_","40_","41_","42_","50_","51_","52_","53_","54_","55_","56_","57_","60_","61_")):return "ELECTRONICS"
    if n in {"Board code","PoE legend","Loop label","Temp label","Boost label","AFE label","Branch label"}:return "SILK"
    return "OTHER"

config=[
  ("B1_lid_off.glb",{"CASE","MOUNT","ELECTRONICS","SILK"},{}),
  ("B1_exploded_assembly.glb",{"CASE","MOUNT","ELECTRONICS","SILK","LID","LID_LABEL"},{"LID":(0,0,148),"LID_LABEL":(0,0,148),"MOUNT":(0,0,10),"ELECTRONICS":(0,0,64),"SILK":(0,0,64)}),
  ("B1_electronics_only.glb",{"ELECTRONICS","SILK"},{}),
]
for filename,include,delta in config:
    bpy.ops.object.select_all(action="DESELECT")
    count=0
    names=[]
    for ob in bpy.data.objects:
        if ob.name in base:ob.location=base[ob.name].copy()
        if ob.type not in allowed:continue
        cat=category(ob)
        select=cat in include
        ob.hide_render=not select
        ob.hide_set(False)
        ob.select_set(select)
        if select:
            names.append(ob.name)
            shift=delta.get(cat,(0,0,0))
            for idx,v in enumerate(shift):ob.location[idx]+=v
            count+=1
    dest=out/filename
    bpy.ops.export_scene.gltf(filepath=str(dest),export_format="GLB",
              export_apply=True,use_selection=True,export_yup=True)
    raw=dest.read_bytes()
    magic,version,length=struct.unpack("<4sII",raw[:12])
    assert magic==b"glTF" and version==2 and length==len(raw)
    size,chunk=struct.unpack("<I4s",raw[12:20])
    assert chunk==b"JSON"
    data=json.loads(raw[20:20+size])
    observed=[n.get("name","") for n in data["nodes"]]
    assert count>60 and len(observed)>60, (filename,count,len(observed))
    if "lid_off" in filename or "electronics_only" in filename:
        assert not any(s.startswith(("02_","03_","04_","Cover title","Exterior decal")) for s in observed)
    if "exploded" in filename:
        assert "02_Clear_polycarbonate_lid" in observed
        assert "20_Main_B1_carrier_PCB_NOT_ROUTED" in observed
    if "electronics_only" in filename:
        assert not any(s.startswith(("01_","70_","71_")) for s in observed)
    record[filename]={"components":count,"nodes":len(observed),"bytes":len(raw),"included_categories":sorted(include)}
    print("B1_VARIANT_OK",filename,"objects",count,"nodes",len(observed),"bytes",len(raw),flush=True)
(out/"B1_viewer_variants.json").write_text(json.dumps(record,indent=2)+"\n",encoding="utf-8")
print("ALL_VARIANTS_EXPORTED",len(config),flush=True)
