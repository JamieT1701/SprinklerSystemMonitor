"""Export editable Blender B1 assembly to portable glTF binary for web/desktop viewers.
This is the concept/appearance surrogate, not OEM-exact CAD or a manufacturing approval.
"""
import bpy
from pathlib import Path
base=Path(__file__).resolve().parent
out=base/"outputs"
bpy.ops.wm.open_mainfile(filepath=str(out/"B1_visual_assembly.blend"))
bpy.ops.object.select_all(action="DESELECT")
count=0
for obj in bpy.data.objects:
    obj.select_set(False)
    if obj.type not in {"MESH","CURVE","FONT"}:
        continue
    if obj.name.startswith(("Photo backdrop", "Cover line", "Presentation pressure sensor cord", "Presentation DS18B20 cable")):
        continue
    if obj.hide_render:
        continue
    obj.hide_set(False)
    obj.select_set(True)
    count+=1
result=bpy.ops.export_scene.gltf(filepath=str(out/"B1_concept_interactive.glb"),export_format="GLB",use_selection=True,
                                export_apply=True,export_yup=True)
print("GLB_EXPORTED",count,str(result),str(out/"B1_concept_interactive.glb"))
