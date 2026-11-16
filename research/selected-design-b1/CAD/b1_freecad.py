#!/usr/bin/env python3
"""B1 dimension-driven concept mechanical assembly in FreeCAD 1.1.
Native editable FCStd + STEP + part meshes. Hammond enclosure is a surrogate
envelope, NOT the manufacturer's exact molded body or certified modified box.
No electronic drawing here is suitable for fabrication or field installation.
Run FreeCADCmd b1_freecad.py from the CAD directory (see README).
"""
import os, json, math
from pathlib import Path
import FreeCAD as App
import Part

HERE=Path(__file__).resolve().parent
P=json.loads((HERE/"B1_dimensions.json").read_text())
OUT=HERE/"outputs"
(OUT/"meshes").mkdir(parents=True,exist_ok=True)
(OUT/"drawings").mkdir(parents=True,exist_ok=True)
V=App.Vector
DOC=App.newDocument("B1_SprinklerMonitor")
PARTS=[]
MESH=[]
C={
 "case":(0.69,0.74,0.77),
 "clear":(0.62,0.79,0.87),
 "gasket":(0.10,0.17,0.19),
 "pcb":(0.06,0.28,0.28),
 "controller":(0.07,0.18,0.22),
 "poe":(0.11,0.26,0.35),
 "metal":(0.78,0.83,0.86),
 "dark":(0.13,0.18,0.22),
 "chip":(0.07,0.10,0.15),
 "terminal":(0.09,0.55,0.37),
 "gold":(0.82,0.62,0.25),
 "blue":(0.09,0.44,0.69),
 "amber":(0.96,0.53,0.12),
 "red":(0.95,0.20,0.20)
}
GROUPS={}
def group(name):
 if name not in GROUPS:
  GROUPS[name]=DOC.addObject("App::DocumentObjectGroup",name)
 return GROUPS[name]
def add(name,shape,category,color=None,transparency=0):
 obj=DOC.addObject("PartDesign::Feature",name)
 obj.Label=name.replace("_"," ")
 obj.Shape=shape
 if obj.ViewObject is not None:
  obj.ViewObject.ShapeColor=C[color or "case"]
  obj.ViewObject.LineColor=(0.10,0.12,0.16)
  obj.ViewObject.Transparency=transparency
 group(category).addObject(obj)
 PARTS.append(obj)
 MESH.append((name,obj,color or "case",transparency))
 return obj
def box(sx,sy,sz,x=0,y=0,z=0):
 return Part.makeBox(sx,sy,sz,V(x-sx/2,y-sy/2,z))
def cyl(rad,depth,x,y,z,axis=None):
 return Part.makeCylinder(rad,depth,V(x,y,z),axis or V(0,0,1))
def ring(rectx,recty,thick,z,h):
 outer=box(rectx,recty,h,0,0,z)
 inner=box(rectx-2*thick,recty-2*thick,h+1,0,0,z-0.5)
 return outer.cut(inner)
# Origin: bottom of enclosure at Z=0. 180 mm long Y, 120 mm wide X.
# Manufacturing outside 180x120x90.5 mm (manufacturer profile only).
W=float(P["enclosure"]["external_width_mm"])
L=float(P["enclosure"]["external_length_mm"])
Hbase=float(P["enclosure"]["base_height_mm"])
Hlid=float(P["enclosure"]["lid_height_mm"])
Wi=108.06
Li=172.13
shell=box(W,L,Hbase,0,0,0)
inside=box(Wi,Li,Hbase-6+2,0,0,6)
shell=shell.cut(inside)
ports=P["ports"]
for port in ports:
 hole=cyl(port["cutout_diameter_mm"]/2,12,
          port["x_mm"],-96,port["z_mm"],V(0,1,0))
 shell=shell.cut(hole)
add("01_Polycarbonate_enclosure_surrogate",shell,"A_Enclosure","case")
# Clear cover, top plate 3mm thick with downturned rim: not OEM mold geometry.
cover=box(W,L,Hlid,0,0,Hbase)
cover=cover.cut(box(Wi,Li,Hlid-3+1,0,0,Hbase-1))
add("02_Clear_polycarbonate_lid",cover,"A_Enclosure","clear",72)
# Rubber silicone seal in the original Hammond design; our ring is just clearance visualization.
add("03_Lid_seal_visual_marker",ring(111,175,1.5,73.6,1.7),"A_Enclosure","gasket")
for x in (-52,52):
 for y in (-81,81):
  add("04_Lid_screw_%s_%s"%(str(x).replace("-","m"),str(y).replace("-","m")),
      cyl(2.3,8,x,y,82),"A_Enclosure","metal")
# Bottom standoffs: positions are deliberate PCB concept; OEM bosses must be checked against STEP.
for x,y in P["carrier_pcb"]["mount_holes_xy_mm"]:
 standoff=cyl(4.5,20,x,y,6).cut(cyl(1.65,20.2,x,y,5.9))
 add("10_Standoff_%s_%s"%(str(x).replace("-","m"),str(y).replace("-","m")),
     standoff,"B_Mounting","case")
# PCB 100 x 160 x 1.6 mm within manufacturer maximum 106.68 x 167.13.
pc=P["carrier_pcb"]
board=box(pc["width_mm"],pc["length_mm"],pc["thickness_mm"],0,0,pc["z_bottom_mm"])
for x,y in pc["mount_holes_xy_mm"]:
 board=board.cut(cyl(pc["mount_hole_diameter_mm"]/2,3,x,y,25.5))
add("20_Main_B1_carrier_PCB_NOT_ROUTED",board,"C_PCB_and_rails","pcb")
# PCB visual copper-like pads and service test points. NOT authoritative KiCad copper routing.
for x,y in ((-35,-64),(-22,-64),(-6,63),(16,63),(32,63),(42,-10),(40,7)):
 add("21_Testpad_%s_%s"%(str(x).replace("-","m"),str(y).replace("-","m")),
     cyl(2.0,0.14,x,y,27.65),"C_PCB_and_rails","gold")
for x,y in pc["mount_holes_xy_mm"]:
 # PCB M3 pan head with visible clearance; holes remain visible in STEP.
 screw=cyl(2.7,1.4,x,y,28)
 add("22_M3_PCB_fastener_%s_%s"%(str(x).replace("-","m"),str(y).replace("-","m")),
     screw,"B_Mounting","metal")
# Selected controller: Waveshare ESP32-S3-POE-ETH nominal module outline; pin header 2 x 20.
cx,cy=P["controller"]["center_xy_mm"]
board_mcu=box(21,72.8,1.6,cx,cy,48)
add("30_Waveshare_ESP32_S3_ETH_surrogate",board_mcu,"D_Controller","controller")
for x in (cx-8.9,cx+8.9):
 for j in range(20):
  y=cy-24.13+j*2.54
  if abs(y-cy)>37:continue
  add("31_Controller_header_pin_%s_%02d"%("L" if x<cx else "R",j),
      box(0.6,0.6,20,x,y,29),"D_Controller","gold")
add("32_ESP32_RF_chip",box(13,16,3,cx,cy+7,49.7),"D_Controller","chip")
add("33_RJ45_socket",box(20,19,14,cx,cy-28,49.7),"D_Controller","metal")
add("34_USBC_socket",box(9,7,3,cx,cy+38,49.7),"D_Controller","metal")
# Existing factory PoE subassembly below microcontroller; actual mating geometry not yet measured.
add("40_PoE_factory_module_PCB_surrogate",box(30,35,1.6,cx,cy+12,31),
    "E_PoE_factory","poe")
add("41_PoE_magnetics",box(20,19,12,cx,cy+12,33),"E_PoE_factory","dark")
for x in (cx-9,cx+9):
 add("42_PoE_cap_%s"%("L" if x<cx else "R"),
     cyl(3.4,7,x,cy-1,33),"E_PoE_factory","metal")
# Right side: ADS, booster, eFuse footprints; NO authentic KiCad nets.
add("50_ADS1115_IC_body",box(5.3,3.2,1.4,24,34,27.7),"F_Analog","chip")
for dy in (-2,2):
 for dx in (-3.5,-2.1,-0.7,0.7,2.1,3.5):
  add("51_ADS_pad_%s_%s"%(str(dx).replace("-","m"),str(dy).replace("-","m")),
      box(0.75,0.8,0.10,24+dx,34+dy,27.7),"F_Analog","gold")
add("52_100ohm_precision_shunt",box(6.2,3.2,0.8,27,11,27.7),"F_Analog","metal")
add("53_LM4040_2V048_reference",box(3,3,1.4,37,34,27.7),"F_Analog","chip")
add("54_Pololu_5588_24V_boost_surrogate",box(8.6,13.6,2.8,25,-8,29),
    "G_24V_Power","blue")
add("55_Boost_coil",box(5.0,5.0,3.4,25,-8,32.0),"G_24V_Power","metal")
add("56_TPS2662_candidate_VSON",box(3,3,1.0,26,-35,27.7),
    "G_24V_Power","chip")
add("57_eFuse_programming_resistor",box(3,1.6,0.7,33,-35,27.7),
    "G_24V_Power","metal")
# Field connector blocks on PCB, pressure 2-pos and temperature 3-pos.
add("60_J1_PRESSURE_LOOP_2PIN",box(23,12,10,29,-63,29),"H_Field_terminals","terminal")
add("61_J2_TEMPERATURE_3PIN",box(25,12,10,-8,-63,29),"H_Field_terminals","blue")
# Three case wall penetrations: RJ45 gland and two M12 bulkhead ports are surrogate.
for port in ports:
 x,z=port["x_mm"],port["z_mm"]
 od=10 if "POE" in port["name"] else 8.5
 collar=cyl(od,17,x,-105,z,V(0,1,0))
 core=cyl(4.8 if "POE" not in port["name"] else 6.4,17.2,
          x,-105.1,z,V(0,1,0))
 add("70_"+port["name"]+"_case_bulkhead",
     collar.cut(core),"I_Case_ports","dark")
 add("71_"+port["name"]+"_metal_nut",
     cyl(od+1.5,2.5,x,-100,z,V(0,1,0)).cut(
     cyl(od-2,2.6,x,-100.1,z,V(0,1,0))),
     "I_Case_ports","metal")
# Remote illustrative, not mechanically part of the enclosure: pressure sender and DS18B20.
sx,sy=151,-13
add("80_Pressure_transmitter_body_illustrative",
    cyl(9.4,47,sx,sy,22),"J_External_sensors","metal")
add("81_Pressure_transmitter_M12_cap",
    cyl(10,13,sx,sy,69),"J_External_sensors","dark")
add("82_Pressure_process_thread_illustrative",
    cyl(4.8,13,sx,sy,9),"J_External_sensors","gold")
add("83_DS18B20_probe_stainless",
    cyl(3.0,47,-154,0,10),"J_External_sensors","metal")
# Model provenance metadata for documentation.
DOC.recompute()
invalid=[]
for ob in PARTS:
 try:
  if not ob.Shape.isValid():invalid.append(ob.Name)
 except Exception:invalid.append(ob.Name)
if invalid: raise RuntimeError("Invalid solid geometry: "+", ".join(invalid))
# Save editable FreeCAD native project; script remains parametric re-generator.
DOC.saveAs(str(OUT/"B1_assembled.FCStd"))
# Separate STEP for open mechanical solids and component placement.
Part.export(PARTS,str(OUT/"B1_complete_reference_assembly.step"))
for name,obj,color,transparency in MESH:
 try:
  obj.Shape.exportStl(str(OUT/"meshes"/(name+".stl")))
 except Exception as ex:
  print("STL_EXPORT_FAIL",name,str(ex))
# Separate working file for exploded/section inspection.
assembled=[(o,o.Placement.Base.z) for o in PARTS]
for ob in PARTS:
 if "02_Clear" in ob.Name or "03_Lid_seal" in ob.Name or "04_Lid" in ob.Name:
  ob.Placement.Base.z += 67
 elif ob.Name.startswith("20_Main") or any(ob.Name.startswith(prefix) for prefix in
       ("21_","22_","30_","31_","32_","33_","34_","40_","41_","42_","50_","51_","52_","53_","54_","55_","56_","57_","60_","61_")):
  ob.Placement.Base.z += 15
DOC.recompute()
DOC.saveAs(str(OUT/"B1_exploded.FCStd"))
Part.export(PARTS,str(OUT/"B1_exploded_reference_assembly.step"))
# JSON parts manifest consumed by Blender with identical names and material categories.
manifest={
 "design_id":P["design_id"],
 "units":"mm","native_FreeCAD":"1.1.4",
 "part_count":len(MESH),
 "parts":[{"name":n,"mesh":"meshes/"+n+".stl","material":mat,
           "transparency_percent":trans} for n,o,mat,trans in MESH],
 "notes":P["source_limitations"]
}
(OUT/"B1_part_manifest.json").write_text(json.dumps(manifest,indent=2)+"\n")
(OUT/"B1_CAD_README.txt").write_text(
 "B1 DIMENSIONAL DESIGN SURROGATE ONLY. Not manufacturer-exact molded STEP, not real circuit,"
 " not qualified for drilling, electrical fabrication or sprinkler installation.\\n"
 "Editable parametric source: ../b1_freecad.py + ../B1_dimensions.json.\\n")
print("FREECAD_OK",len(MESH),"parts",
      "bounds",W,L,Hbase+Hlid,
      "pcb",pc["width_mm"],pc["length_mm"])
App.closeDocument(DOC.Name)
