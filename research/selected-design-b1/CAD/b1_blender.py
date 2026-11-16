#!/usr/bin/env python3
"""Photorealistic camera views from authoritative FreeCAD part STL geometry.
FreeCAD part names/positions are re-used. This blender file remains editable.
Enclosure is a nominal manufacturer envelope surrogate, no OEM boss or seal proof.
"""
import json, math, sys
from pathlib import Path
import bpy
from mathutils import Vector
HERE=Path(__file__).resolve().parent
OUT=HERE/"outputs"
R=OUT/"renders"
R.mkdir(exist_ok=True,parents=True)
spec=json.loads((HERE/"B1_dimensions.json").read_text())
manifest=json.loads((OUT/"B1_part_manifest.json").read_text())
bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)
for m in list(bpy.data.materials): bpy.data.materials.remove(m)
bpy.context.scene.unit_settings.system="METRIC"
bpy.context.scene.unit_settings.scale_length=.001
SC=bpy.context.scene
SC.render.engine="CYCLES"
SC.cycles.samples=12
SC.cycles.use_denoising=True
SC.render.resolution_percentage=100
SC.render.resolution_x=1600
SC.render.resolution_y=1200
SC.render.image_settings.file_format="PNG"
SC.render.film_transparent=False
SC.world.use_nodes=True
bg=SC.world.node_tree.nodes.get("Background")
bg.inputs["Color"].default_value=(0.13,0.16,0.19,1)
bg.inputs["Strength"].default_value=1.4
SC.view_settings.view_transform="AgX"
def mat(name,color,metal=0,rough=.4,trans=0):
 m=bpy.data.materials.new(name)
 m.diffuse_color=(*color,1)
 m.use_nodes=True
 bs=m.node_tree.nodes.get("Principled BSDF")
 bs.inputs["Base Color"].default_value=(*color,1)
 bs.inputs["Roughness"].default_value=rough
 bs.inputs["Metallic"].default_value=metal
 if trans:
  bs.inputs["Transmission Weight"].default_value=trans
  bs.inputs["Alpha"].default_value=0.82
  m.surface_render_method="DITHERED"
 return m
MAT={
 "case":mat("Hammond polycarbonate — RAL 7035",(.56,.64,.66),rough=.46),
 "clear":mat("Smoky translucent cover — rendering only",(.51,.70,.78),rough=.12,trans=.88),
 "gasket":mat("Dark silicone seal",(.03,.06,.08),rough=.75),
 "pcb":mat("Dark teal ENIG carrier (unrouted)",(.015,.15,.17),rough=.37),
 "controller":mat("Waveshare navy controller PCB",(.028,.070,.14),rough=.32),
 "poe":mat("Factory PoE daughterboard",(.035,.17,.24),rough=.32),
 "metal":mat("Brushed stainless aluminum",(.67,.74,.79),metal=.82,rough=.25),
 "dark":mat("Black industrial thermoplastic",(.026,.045,.070),rough=.41),
 "chip":mat("Semiconductor molded epoxy",(.018,.025,.038),rough=.30),
 "terminal":mat("Loop interface — teal",(.025,.56,.35),rough=.32),
 "gold":mat("ENIG gold connector",(.78,.53,.18),metal=.84,rough=.3),
 "blue":mat("Temperature interface blue",(.055,.32,.68),rough=.30),
 "amber":mat("Amber signal",(.97,.41,.11),metal=.14,rough=.32),
 "red":mat("Red alert",(.97,.22,.14),rough=.3)
}
palette=MAT
PARTS={}
for part in manifest["parts"]:
 path=OUT/part["mesh"]
 if not path.exists(): raise RuntimeError("Missing CAD mesh "+str(path))
 before=set(bpy.data.objects)
 bpy.ops.wm.stl_import(filepath=str(path))
 objects=list(set(bpy.data.objects)-before)
 if len(objects)!=1: raise RuntimeError("STL import yielded "+str(len(objects))+" for "+part["name"])
 obj=objects[0]
 obj.name=part["name"]
 obj.data.materials.clear()
 obj.data.materials.append(MAT[part["material"]])
 obj["engineering_status"]="appearance surrogate; verify component clearance and electrical safety"
 PARTS[part["name"]]=obj
# A physical product card on the cover with explanatory designation, no false UL marking.
def box(name,loc,dims,material, bevel=0):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc)
 obj=bpy.context.object
 obj.name=name
 obj.dimensions=dims
 bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
 obj.data.materials.append(material)
 if bevel:
  mod=obj.modifiers.new("Edge radius","BEVEL")
  mod.width=bevel;mod.segments=3
  obj.modifiers.new("Weighted corner normals","WEIGHTED_NORMAL")
 return obj
typeface=mat("Printed black/charcoal text",(.01,.03,.05),rough=.85)
print_white=mat("White legend ink",(.91,.97,.98),rough=.85)
print_light=mat("Silk pale cyan",(.48,.87,.84),rough=.90)
print_green=mat("Green LED",(.11,1.0,.44),rough=.15)
def label(name,text,loc,size,material,rot=None):
 cu=bpy.data.curves.new(name,"FONT")
 cu.body=text;cu.size=size;cu.extrude=.013;cu.bevel_depth=.001;cu.align_x="CENTER"
 ob=bpy.data.objects.new(name,cu)
 bpy.context.collection.objects.link(ob)
 ob.location=loc
 if rot is not None:ob.rotation_euler=rot
 ob.data.materials.append(material)
 return ob
LABELS=[]
face=box("Exterior decal — not product certification",(0,12,90.92),(74,58,.20),
         mat("Deep ink blue label",(.045,.086,.122),rough=.53),bevel=1.6)
LABELS.append(face)
LABELS.append(label("Cover title","B1 / RISER",(0,30,91.1),5.8,print_white))
LABELS.append(label("Cover subtitle","AIR + TEMPERATURE",(0,15,91.1),2.65,print_light))
LABELS.append(label("Cover policy","SUPPLEMENTARY MONITOR",(0,0,91.1),2.6,print_white))
LABELS.append(label("Cover warning","NOT A LISTED FIRE ALARM",(0,-13,91.1),2.25,print_light))
LABELS.append(label("Cover line","ETHERNET  |  PoE  |  4-20mA",(0,-31,91.1),2.45,typeface))
# Provisional PCB labels at z28; component geometry shadows the print intentionally.
SILK=[]
for name,txt,x,y,sz in [
 ("Board code","B1 / ADC + LOOP",18,68,3.2),
 ("PoE legend","WAVESHARE / PoE",-27,-54,2.2),
 ("Loop label","PRESSURE 4-20mA",28,-51,2.2),
 ("Temp label","TEMP / 1-WIRE",-8,-52,2.2),
 ("Boost label","24V BOOST",27,4,2.4),
 ("AFE label","ADS1115",25,44,2.5),
 ("Branch label","NOT ROUTED / R&D",0,75,2.8)]:
 SILK.append(label(name,txt,(x,y,27.82),sz,print_light))
# Curved presentation-only field sensor cables.
def cable(name,pts,radius,material):
 c=bpy.data.curves.new(name,'CURVE')
 c.dimensions='3D'
 c.resolution_u=24
 c.bevel_depth=radius
 c.bevel_resolution=4
 s=c.splines.new("BEZIER")
 s.bezier_points.add(len(pts)-1)
 for bp,p in zip(s.bezier_points,pts):
  bp.co=p;bp.handle_left_type="AUTO";bp.handle_right_type="AUTO"
 o=bpy.data.objects.new(name,c)
 bpy.context.collection.objects.link(o)
 o.data.materials.append(material)
 return o
CABLES=[
 cable("Presentation pressure sensor cord (not scale cable length)",
       [(35,-125,35),(70,-160,32),(136,-95,60),(151,-14,82)],1.7,
       mat("Pressure cable industrial black",(.036,.043,.05))),
 cable("Presentation DS18B20 cable (not scale cable length)",
       [(0,-125,35),(-40,-145,28),(-111,-108,45),(-154,0,58)],1.55,
       mat("Temperature cable dark gray",(.11,.17,.20))),
 cable("Presentation PoE Ethernet cord (not scale cable length)",
       [(-35,-125,35),(-57,-165,25),(-112,-187,20),(-170,-205,22)],2.6,
       mat("Ethernet cable jacket blue",(.02,.14,.3)))
]
# Exterior field interface labels sit above each external female socket.
FRONT_LABELS=[]
for label_name,textval,x in (("Front_PoE","PoE",-35),
                              ("Front_Temp","TEMP",0),
                              ("Front_Press","PRESS",35)):
 FRONT_LABELS.append(label(label_name,textval,(x,-90.3,57),3.1,
                           print_white,rot=(math.pi/2,0,0)))
# Printed side-wall legend for undrilled expansion reservation (NOT an active port).
FRONT_LABELS.append(label("Side_Aux_Bracket","AUX FUTURE",
                    (60.8,18,47),2.3,print_light,rot=(0,math.pi/2,math.pi/2)))

# Reset must restore original label/silkscreen coordinates as well as mesh parts.
# Previous script only restored mesh transforms, leaking exploded-view offsets
# into the final .blend and GLB (floating lid decal and PCB silk text).
STATIC_COORDS={ob.name:ob.location.copy() for ob in LABELS+SILK+FRONT_LABELS}
# Standalone matte stage helps cast realistic shadows; not part of CAD package.
stage=mat("Studio floor",(0.052,.071,.089),rough=.72)
FLOOR=box("Photo backdrop floor",(0,0,-18),(680,540,6),stage,bevel=3)
def area(name,location,power,size,color=(1,1,1)):
 data=bpy.data.lights.new(name,"AREA")
 data.energy=power;data.shape="DISK";data.size=size;data.color=color
 obj=bpy.data.objects.new(name,data)
 bpy.context.collection.objects.link(obj)
 obj.location=location
 direction=Vector((0,0,30))-obj.location
 obj.rotation_euler=direction.to_track_quat("-Z","Y").to_euler()
for args in (
 ("Key softbox",(-140,-160,310),230000,350,(.83,.91,1)),
 ("Warm rim",(170,90,240),250000,250,(1,.91,.75)),
 ("Front fill",(140,-240,160),125000,280,(.70,.88,1))
):area(*args)
def camera(name,xyz,look,scale):
 if bpy.data.objects.get(name): bpy.data.objects.remove(bpy.data.objects[name],do_unlink=True)
 c=bpy.data.cameras.new(name)
 o=bpy.data.objects.new(name,c)
 bpy.context.collection.objects.link(o)
 o.location=xyz
 look=Vector(look)
 o.rotation_euler=(look-o.location).to_track_quat("-Z","Y").to_euler()
 c.type="ORTHO";c.ortho_scale=scale;c.lens=60
 SC.camera=o
 return o
def reset():
 for ob in PARTS.values():
  ob.location=(0,0,0);ob.hide_render=False
 for ob in LABELS+SILK+FRONT_LABELS:
  ob.location=STATIC_COORDS[ob.name].copy()
  ob.hide_render=False
 for ob in CABLES: ob.hide_render=False
 FLOOR.hide_render=False
def invisible(prefixes,yes=True):
 for name,obj in PARTS.items():
  if any(name.startswith(p) for p in prefixes):obj.hide_render=yes
def render(name,cam_pos,look,scale,res=(1600,1200)):
 SC.render.resolution_x=res[0]
 SC.render.resolution_y=res[1]
 camera(name+"_camera",cam_pos,look,scale)
 SC.render.filepath=str(R/(name+".png"))
 bpy.ops.render.render(write_still=True)
 print("RENDERED",name,R/(name+".png"))
# Closed presentation: pressure and DS18B20 remotely placed beside housing, illustrative cables.
reset()
for ob in SILK:ob.hide_render=True
render("01_b1_closed_product",(270,-290,275),(0,-4,48),435)
# Lid off close-in assembly: cover translated next to case; expose B1 board and real clearance surrogate.
reset()
for ob in PARTS.values():
 if ob.name.startswith(("02_","03_","04_")):
  ob.location.x += 152
  ob.location.z += 19
for ob in LABELS:
 ob.location.x += 152
 ob.location.z += 19
for ob in CABLES:ob.hide_render=True
invisible(("80_","81_","82_","83_"))
render("02_b1_service_open",(260,-290,285),(45,-5,57),335)
# Exploded: enclosure body below, board group displaced +35 mm, cover +105 mm.
reset()
for ob in PARTS.values():
 if ob.name.startswith(("02_","03_","04_")):
  ob.location.z += 115
 elif ob.name.startswith(("20_","21_","22_","30_","31_","32_","33_",
                         "34_","40_","41_","42_","50_","51_","52_","53_",
                         "54_","55_","56_","57_","60_","61_")):
  ob.location.z += 38
for ob in LABELS:ob.location.z+=115
for ob in SILK:ob.location.z+=38
for ob in CABLES:ob.hide_render=True
invisible(("80_","81_","82_","83_"))
render("03_b1_exploded",(290,-280,315),(0,0,102),425)
# Top board; remove enclosure/lid, standoffs, port hardware and remote probes.
reset()
for ob in LABELS:ob.hide_render=True
for ob in CABLES:ob.hide_render=True
invisible(("01_","02_","03_","04_","10_","70_","71_","80_","81_","82_","83_"))
FLOOR.hide_render=True
render("04_b1_pcb_component_top",(1,-6,500),(0,0,35),204,(1200,1740))
# Tight service wiring/port view with cover off; concentrate on front short wall.
reset()
for ob in LABELS:ob.hide_render=True
for ob in CABLES:ob.hide_render=True
invisible(("02_","03_","04_","80_","81_","82_","83_"))
render("05_b1_field_ports",(205,-295,156),(0,-39,31),240)
# rear/bottom angled shape.
reset()
for ob in CABLES:ob.hide_render=True
for ob in SILK:ob.hide_render=True
render("06_b1_wall_install_view",(-245,235,275),(0,0,48),285)
# Persist Blender master scene in assembled state, cover transparent with all source mesh components.
reset()
for ob in SILK:ob.hide_render=True
camera("MASTER_CAMERA",(270,-290,275),(0,-4,48),435)
SC.render.resolution_x=1600;SC.render.resolution_y=1200
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/"B1_visual_assembly.blend"))
print("BLENDER_OK",bpy.app.version_string,"parts",len(PARTS),"views",len(list(R.glob("*.png"))))
