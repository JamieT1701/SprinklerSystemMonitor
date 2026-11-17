#!/usr/bin/env python3
"""B1 detailed six-view contact sheet from FreeCAD-authored Blender renders.
Reference visualization only, not manufacturer true-to-scale component models.
"""
from pathlib import Path
from PIL import Image, ImageOps, ImageDraw, ImageFont
D=Path(__file__).resolve().parent
R=D/"outputs/renders"
OUTPUT=R/"B1_design_review_contact_sheet.png"
W,H=2820,2030
canvas=Image.new("RGB",(W,H),(13,25,35))
dr=ImageDraw.Draw(canvas)
def font(size,bold=False):
 for f in (
  "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
  "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf"
 ):
  try:return ImageFont.truetype(f,size)
  except OSError:continue
 return ImageFont.load_default()
dr.rectangle((0,0,W,194),fill=(17,33,44))
dr.rectangle((60,66,74,146),fill=(72,215,179))
dr.text((94,57),"B1  /  RISER MONITOR",font=font(69,True),fill=(229,247,250))
dr.text((99,135),"FULL CAD DESIGN REVIEW   •   FREECAD 1.1   /   BLENDER 5.3   /   KICAD 10",font=font(29),fill=(152,188,199))
views=[
 ("01_b1_closed_product.png","01  FINISHED EXTERIOR","Clear-lid enclosure and remote sensors"),
 ("02_b1_service_open.png","02  FIELD-SERVICE ACCESS","Transparent lid removed; maintenance view"),
 ("03_b1_exploded.png","03  EXPLODED ASSEMBLY","Enclosure, carrier, controller and lid"),
 ("04_b1_pcb_component_top.png","04  INTERNAL HARDWARE","ESP32-S3 PoE / ADC / protected-loop concept"),
 ("05_b1_field_ports.png","05  CABLE INTERFACES","Power/Ethernet, temperature and current loop"),
 ("06_b1_wall_install_view.png","06  ALTERNATE ANGLE","Industrial enclosure geometry")
]
cols=3
cardw,cardh=860,786
marginx=64; row0=240; colgap=48; rowgap=36
for idx,(name,title,desc) in enumerate(views):
 col=idx%cols;row=idx//cols
 x=marginx+col*(cardw+colgap);y=row0+row*(cardh+rowgap)
 dr.rounded_rectangle((x,y,x+cardw,y+cardh),radius=19,fill=(26,43,55),outline=(70,100,112),width=2)
 im=Image.open(R/name).convert("RGB")
 top=ImageOps.fit(im,(cardw-24,cardh-166),method=Image.Resampling.LANCZOS,centering=(0.5,0.5))
 canvas.paste(top,(x+12,y+12))
 dr.rectangle((x+13,y+cardh-155,x+cardw-13,y+cardh-18),fill=(20,34,44))
 dr.text((x+34,y+cardh-139),title,font=font(29,True),fill=(230,248,247))
 dr.text((x+34,y+cardh-91),desc,font=font(22),fill=(156,185,197))
dr.rectangle((65,H-94,W-65,H-92),fill=(75,111,124))
dr.text((65,H-74),"CONCEPT-LEVEL REFERENCE ASSEMBLY",font=font(26,True),fill=(235,193,108))
dr.text((710,H-72),"Electrical fault protection, genuine OEM clearances and PCB netlist remain unverified.",font=font(25),fill=(196,212,220))
canvas.save(OUTPUT,optimize=True)
print("SHEET_CREATED",str(OUTPUT),canvas.size,OUTPUT.stat().st_size)
