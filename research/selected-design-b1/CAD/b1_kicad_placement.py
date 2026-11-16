#!/usr/bin/env python3
"""KiCad 10 native mechanical placement study for B1: NOT a routed/electrically valid PCB.
Unqualified connector and protection footprints remain in the conceptual plan.
Designed to match FreeCAD carrier 100 x 160 and mounting holes +/-44, +/-70 mm.
"""
import json,os
from pathlib import Path
import pcbnew as p
HERE=Path(__file__).resolve().parent
cfg=json.loads((HERE/"B1_dimensions.json").read_text())
OUT=HERE/"electronics"
OUT.mkdir(exist_ok=True,parents=True)
board=p.BOARD()
try:board.SetCopperLayerCount(2)
except Exception:pass
mm=p.FromMM
pt=lambda x,y:p.VECTOR2I(mm(x),mm(y))
def edge(x1,y1,x2,y2):
 s=p.PCB_SHAPE(board)
 s.SetShape(p.SHAPE_T_SEGMENT)
 s.SetStart(pt(x1,y1));s.SetEnd(pt(x2,y2))
 s.SetLayer(p.Edge_Cuts);s.SetWidth(mm(0.05))
 board.Add(s)
# Enclosure XY center in KiCad sheet is (100, 130); board left 50 right 150; top 50 bottom 210.
for a,b,c,d in ((50,50,150,50),(150,50,150,210),(150,210,50,210),(50,210,50,50)):
 edge(a,b,c,d)
LIB="/app/extensions/Library/footprints"
def fp(lib,name,ref,value,x,y,rot=0):
 f=p.FootprintLoad(str(Path(LIB)/(lib+".pretty")),name)
 if f is None: raise RuntimeError("Footprint not found "+lib+":"+name)
 f.SetReference(ref);f.SetValue(value)
 f.SetPosition(pt(x,y))
 if rot:f.SetOrientationDegrees(rot)
 try:
  f.Reference().SetVisible(True)
  f.Value().SetVisible(False)
 except Exception:pass
 board.Add(f)
 return f
def addtext(text,x,y,h=1.6,layer=p.F_SilkS,thick=0.22):
 ob=p.PCB_TEXT(board)
 ob.SetText(text);ob.SetPosition(pt(x,y))
 ob.SetLayer(layer)
 ob.SetTextSize(pt(h,h));ob.SetTextThickness(mm(thick))
 board.Add(ob)
 return ob
for j,(x,y) in enumerate(cfg["carrier_pcb"]["mount_holes_xy_mm"]):
 fp("MountingHole","MountingHole_3.2mm_M3","H"+str(j+1),"M3 mounting",100+x,130+y)
# Mechanical socket rows shown as physically aligned, but actual module pin role numbering is UNVERIFIED.
for j,x in enumerate((100-27-8.9,100-27+8.9)):
 fp("Connector_PinSocket_2.54mm","PinSocket_1x20_P2.54mm_Vertical",
    "JH"+str(j+1),"Waveshare 20pin row",x,130-24.13)
# Industrial 2-wire loop and 3-wire digital probe connector candidates.
fp("TerminalBlock_Phoenix","TerminalBlock_Phoenix_MKDS-1,5-2_1x02_P5.00mm_Horizontal",
   "J1","24V loop OUT / IRETURN",130,64)
fp("TerminalBlock_Phoenix","TerminalBlock_Phoenix_MKDS-1,5-3_1x03_P5.00mm_Horizontal",
   "J2","3V3 / DATA / GND",92,64)
# Correctly counted analog front end packages (schematic/netlist still unqualified).
fp("Package_SO","MSOP-10_3x3mm_P0.5mm","U2","ADS1115",124,164,90)
fp("Resistor_SMD","R_1206_3216Metric","RS1","100R 0.1% current sense",126,141,0)
for ref,x,y,val in (
 ("R2",122,184,"270k L+"),("R3",129,184,"22k L+"),
 ("R4",136,184,"270k supply"),("R5",143,184,"22k supply"),
 ("R6",93,83,"4.7k 1Wire")):
 fp("Resistor_SMD","R_0603_1608Metric",ref,val,x,y,90)
fp("Package_TO_SOT_SMD","SOT-23","D1","LM4040-2.048",140,165,90)
# Boost 3-pin SIP connector is a PLACEMENT ONLY; exact Pololu pad pattern not DFM verified.
fp("Connector_PinHeader_2.54mm","PinHeader_1x03_P2.54mm_Vertical",
   "MOD1","Pololu 5588 PLACEHOLDER",124,124)
# eFuse body is VSON 3x3 mm but no approved PCB land pattern; label placeholder only.
addtext("TPS2662 3x3 VSON - LAND PATTERN TBD",126,104,1.4,p.F_Fab)
for ref,x,y in [("TP1",92,198),("TP2",105,198),("TP3",118,198),("TP4",132,198)]:
 fp("TestPoint","TestPoint_THTPad_D1.5mm_Drill0.7mm",ref,"TEST",x,y)
addtext("B1  /  ENGINEERING PLACEMENT STUDY",100,53,2.0)
addtext("NOT ROUTED   -   NOT FOR PCB FABRICATION",100,205,1.7)
addtext("WAVESHARE ESP32-S3-POE-ETH",78,100,1.5)
addtext("FACTORY POE STACK / KEEP-OUT TBD",80,150,1.25,p.F_Fab)
addtext("24V LOOP / SENSOR",128,77,1.4)
addtext("DS18B20 / 3V3",91,76,1.4)
addtext("ADC / SHUNT / REF",128,174,1.35)
addtext("5V -> 24V BOOST",123,112,1.3)
addtext("TPS2662 EFUSE",126,95,1.3)
addtext("F.CU + B.CU UNROUTED",100,190,1.45,p.Dwgs_User)
addtext("CARRIER 100 x 160 mm / THICKNESS 1.6 mm",100,57,1.25,p.Dwgs_User)
# All library pads are intentionally unassigned/no traces: proof of placement parsing only.
fname=OUT/"B1_placement_NOT_ROUTED.kicad_pcb"
p.SaveBoard(str(fname),board)
reload=p.LoadBoard(str(fname))
if reload is None:raise RuntimeError("KiCad could not re-open saved PCB")
fpcount=len(list(reload.GetFootprints()))
assert fpcount>=18,fpcount
print("B1_KICAD_PLACEMENT_OK",fname,"FOOTPRINTS",fpcount,
      "BOARD_DIMENSIONS_MM",cfg["carrier_pcb"]["width_mm"],cfg["carrier_pcb"]["length_mm"])
