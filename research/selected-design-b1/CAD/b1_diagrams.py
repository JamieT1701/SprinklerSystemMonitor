#!/usr/bin/env python3
"""Source-generated vector engineering illustrations. These are explanatory
technical drawings, NOT KiCad ERC-tested netlists or fabrication files.
"""
from pathlib import Path
from html import escape
import json
D=Path(__file__).resolve().parent
OUT=D/"outputs"/"drawings"
OUT.mkdir(parents=True,exist_ok=True)
PARAM=json.loads((D/"B1_dimensions.json").read_text())
BG="#0B1321";PANEL="#121E2E";PANEL2="#1C2A3A";TEXT="#E6F1F4"
MUTE="#96ADBE";TEAL="#66DAC2";BLUE="#70A9FF";GOLD="#F6C768";RED="#FA8C89"
def esc(x):return escape(str(x),quote=True)
class SVG:
 def __init__(self,w,h,title,subtitle):
  self.w=w;self.h=h
  self.s=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">',
          f'<rect width="{w}" height="{h}" fill="{BG}"/>',
          '<defs><marker id="arrow" markerWidth="9" markerHeight="9" refX="7.2" refY="4.5" orient="auto" markerUnits="strokeWidth"><path d="M0,0 L9,4.5 L0,9z" fill="#66DAC2"/></marker></defs>']
  self.text(54,67,title,35,TEXT,700)
  self.text(54,107,subtitle,17,MUTE)
  self.line(54,130,w-54,130,MUTE,1,opacity=.23)
 def raw(self,s):self.s.append(s)
 def rect(self,x,y,w,h,fill=PANEL,stroke=None,r=17):
  st=f' stroke="{stroke}" stroke-width="2"' if stroke else ''
  self.raw(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}"{st}/>')
 def text(self,x,y,s,size=16,color=TEXT,weight=400,anchor="start"):
  self.raw(f'<text x="{x}" y="{y}" font-family="Inter,Arial,sans-serif" font-size="{size}" fill="{color}" font-weight="{weight}" text-anchor="{anchor}">{esc(s)}</text>')
 def line(self,x1,y1,x2,y2,color=TEAL,width=2,arrow=False,opacity=1,dash=None):
  a=' marker-end="url(#arrow)"' if arrow else ''
  b=f' stroke-dasharray="{dash}"' if dash else ''
  self.raw(f'<path d="M {x1} {y1} L {x2} {y2}" stroke="{color}" stroke-width="{width}" fill="none" opacity="{opacity}"{a}{b}/>')
 def path(self,d,color=TEAL,width=3,arrow=True,opacity=1,dash=None):
  a=' marker-end="url(#arrow)"' if arrow else ''
  b=f' stroke-dasharray="{dash}"' if dash else ''
  self.raw(f'<path d="{d}" stroke="{color}" stroke-width="{width}" fill="none" opacity="{opacity}" stroke-linejoin="round" stroke-linecap="round"{a}{b}/>')
 def box(self,x,y,w,h,title,lines=(),accent=TEAL):
  self.rect(x,y,w,h,PANEL,accent)
  self.raw(f'<rect x="{x}" y="{y}" width="7" height="{h}" rx="3.5" fill="{accent}"/>')
  self.text(x+23,y+36,title,20,TEXT,700)
  for i,l in enumerate(lines):self.text(x+23,y+66+25*i,l,15,MUTE)
 def foot(self,text):
  self.line(54,self.h-73,self.w-54,self.h-73,MUTE,1,opacity=.3)
  self.text(54,self.h-42,text,15,MUTE)
  self.text(self.w-55,self.h-42,"B1 / CONCEPT RELEASE — NOT FOR FABRICATION",14,GOLD,600,"end")
 def save(self,path):
  (OUT/path).write_text("\n".join(self.s+["</svg>"])+"\n",encoding="utf-8")
  print("SVG_OK",path,(OUT/path).stat().st_size)

# Full electrical/data architecture including the independent offsite cloud.
a=SVG(1820,1070,"B1 • SYSTEM ARCHITECTURE","One protected pressure channel per B1, remote room temperature, independent loss-of-monitoring alerts")
a.rect(47,165,1250,805,"#0F1E2B","#385D68",24);a.text(75,209,"PHYSICAL B1 UNIT  •  ISOLATED FROM FIRE ALARM / VALVE CONTROLS",18,TEAL,700)
a.rect(1330,165,448,805,"#101B2D","#426494",24);a.text(1352,209,"OFFSITE SERVICES",18,BLUE,700)
a.box(90,260,230,125,"IEEE 802.3af",("RJ45 / factory PoE","W5500 Ethernet"),BLUE)
a.box(397,250,325,156,"Waveshare ESP32-S3",("Authenticated outbound TLS","Watchdog / OTA rollback","Source + quality diagnostics"),TEAL)
a.box(90,470,230,125,"5V → 24V boost",("Pololu U3V9F24","Bench candidate only"),GOLD)
a.box(397,470,325,125,"24V field eFuse",("TPS2662 family candidate","Short/miswire TEST REQUIRED"),GOLD)
a.box(810,470,435,125,"4–20 mA pressure sender",("Qualified 2-wire industrial MPN","Tap / range approved by contractor"),GOLD)
a.box(397,690,325,125,"ADS1115 @ 3.3V",("100Ω current shunt + diagnostics","Terminal / rail / reference"),TEAL)
a.box(90,690,230,125,"DS18B20 probe",("Remote room temperature","CRC + cable failure"),BLUE)
a.box(810,690,435,125,"LOCAL VALIDATION",("Pressure UNKNOWN on bad inputs","Freshness + approved thresholds"),TEAL)
a.box(1363,250,380,140,"Hosted ingestion",("Authenticated device sequence","Store received-at, quality, trends"),BLUE)
a.box(1363,467,380,140,"Cloud-side dead man",("Offline / backend-down independent","Escalation via verified providers"),RED)
a.box(1363,697,380,140,"Phone + desktop PWA",("Pressure / temperature / events","ACK, history, tested notifications"),BLUE)
a.path("M320 320 H395",BLUE);a.path("M320 530 H395",GOLD)
a.path("M722 530 H807",GOLD);a.path("M940 595 V635 H724 V747",GOLD)
a.path("M397 747 H322",BLUE);a.path("M560 690 V408",TEAL)
a.path("M811 745 H726",TEAL)
a.path("M722 320 H1330",BLUE)
a.path("M1553 390 V464",BLUE);a.path("M1553 607 V693",RED)
a.text(77,913,"NO direct control outputs • No fire alarm panel connection • No certified supervisory replacement",17,GOLD,600)
a.foot("Wired-first commercial candidate • source of truth: GitHub design/claude-b1-engineering-20261116")
a.save("B1_system_architecture.svg")

# Electrical analog domain with reference voltages and fail-safe interpretation.
b=SVG(1750,1020,"B1 • ANALOG CHAIN / CIRCUIT REVIEW","Functionally correct measurement intent; the field protection stage has not passed schematic review or fault tests")
b.box(65,250,275,135,"PoE + 5V rail",("Factory PD & MCU module","PoE rail measured separately"),BLUE)
b.box(420,250,300,135,"24V booster",("Pololu U3V9F24","NO output-short protection"),GOLD)
b.box(805,250,360,135,"TPS2662 eFuse",("25mA minimum limit family","Exact variant + limit TBD"),GOLD)
b.box(1235,250,440,135,"2-wire pressure transmitter",("Provisional 0–150 psig ONLY","No live tap approved"),GOLD)
b.path("M340 319 H417",BLUE);b.path("M720 319 H802",GOLD);b.path("M1165 319 H1232",GOLD)
b.rect(1145,470,530,160,PANEL,TEAL);b.text(1171,507,"Return current measured at shunt",22,TEAL,700)
b.text(1170,548,"100 Ω ±0.1%, ≥0.25 W",20,TEXT)
b.text(1170,584,"4 mA = 0.400 V  •  20 mA = 2.000 V",17,MUTE)
b.path("M1450 385 V466",GOLD)
b.box(805,480,292,150,"ADS1115 @ 3.3V",("AIN0 → shunt V","AIN1 → terminal L+","AIN2 → 24V rail","AIN3 → 2.048V check"),TEAL)
b.path("M1145 545 H1100",TEAL)
b.box(420,480,300,150,"ESP32 diagnostic",("I²C GPIO16/17","Quality + fault classifier","Local event state"),TEAL)
b.path("M805 550 H723",TEAL)
b.box(65,480,275,150,"DS18B20 1-Wire",("3-wire, CRC, 4.7k pull-up","Separate GPIO18","Cold warning policy TBD"),BLUE)
b.path("M340 550 H417",BLUE)
b.rect(65,710,1610,145,"#271E24","#7B4A4A",20)
b.text(93,749,"CURRENT DESIGN STOP: 24V FIELD OUTPUT + ADC PROTECTION",22,RED,700)
b.text(93,787,"No approved reverse/short/miswire, TVS thermal, backfeed, power-off clamp or PCB clearance analysis.",18,TEXT)
b.text(93,818,"This sheet is NOT an installable schematic, code-compliant design, tested limiter or order-ready Gerber.",18,TEXT)
b.foot("KiCad contains a 21-footprint mechanical placement PCB; copper routing intentionally absent.")
b.save("B1_electrical_review.svg")

# Mechanical nominal orthographic layout and labeling.
c=SVG(1760,1180,"B1 • ENCLOSURE & CARRIER DIMENSIONS","Hammond 1554T2GYCL nominal outside envelope; actual OEM bosses and cable clearance require factory STEP/physical fit check")
# top view scale 3px/mm: outer 360x540, PCB 300x480
ox,oy=240,245
c.rect(ox,oy,360,540,"#53676F","#AFD1D5",18)
c.rect(ox+17,oy+15,326,510,"#142E35","#7A9CA5",6)
c.rect(ox+30,oy+30,300,480,"#096568",TEAL,4)
for dx in (18,282):
 for dy in (30,450):
  xx=ox+30+dx;yy=oy+30+dy
  c.raw(f'<circle cx="{xx}" cy="{yy}" r="9" fill="{BG}" stroke="#F9D575" stroke-width="2"/>')
# Modules on PCB: map from model x/y origin nominal, y positive down.
def module(cx,cy,sw,sh,title,accent):
 x0=ox+30+150+cx*3-sw*1.5
 y0=oy+30+240+cy*3-sh*1.5
 c.rect(x0,y0,sw*3,sh*3,PANEL2,accent,7)
 c.text(x0+sw*1.5,y0+sh*1.5,title,14,TEXT,600,"middle")
module(-27,0,21,72.8,"ESP32 / W5500",BLUE)
module(25,30,16,14,"ADC",TEAL)
module(25,-8,14,14,"24 V",GOLD)
module(25,-35,18,9,"eFUSE",GOLD)
module(29,-63,23,12,"J1 LOOP",TEAL)
module(-8,-63,25,12,"J2 TEMP",BLUE)
# bounding dimensions
c.line(ox,oy-24,ox+360,oy-24,TEAL,2)
c.line(ox,oy-32,ox,oy-16,TEAL,1)
c.line(ox+360,oy-32,ox+360,oy-16,TEAL,1)
c.text(ox+180,oy-39,"120 mm outside width",18,TEXT,700,"middle")
c.line(ox-28,oy,ox-28,oy+540,TEAL,2)
c.text(ox-45,oy+268,"180 mm outside length",18,TEXT,700,"middle")
c.rect(700,246,920,640,PANEL,"#335666",22)
c.text(747,297,"ENVELOPE & COMPONENT PLACEMENT",26,TEAL,700)
for i,(head,detail) in enumerate([
 ("Enclosure","Hammond 1554T2GYCL • 180 × 120 × 90.5 mm"),
 ("Manufacturer maximum PCB","167.13 × 106.68 mm (length × width)"),
 ("Carrier study","160 × 100 × 1.6 mm • mounting centres ±70 / ±44 mm"),
 ("Controller board","Waveshare ESP32-S3-POE-ETH, approximate 72.8 × 21 mm"),
 ("Cable entry","3 ports along short side: PoE cable, DS18B20, 4–20 mA loop"),
 ("Assembly height","Controller/PoE stack plus lid clearance must be measured"),
 ("CAD integrity","102-part FreeCAD assembly + native STEP exports"),
 ("PCB drawing","21 KiCad footprints • placement only • NOT ROUTED")]):
  yy=355+i*63
  c.text(755,yy,head,17,MUTE,600)
  c.text(755,yy+27,detail,17,TEXT)
c.text(235,851,"DRAWING TOP VIEW  /  NOMINAL SCALE 3 px / mm",16,MUTE,600)
c.rect(240,930,1380,100,"#201D24","#8F704D",14)
c.text(272,969,"FIT ACCEPTANCE REQUIRED",20,GOLD,700)
c.text(272,1005,"OEM lid/boss/port wall geometry, 20-pin module fit, RJ45 cable bend and M12 connector sourcing not verified.",17,TEXT)
c.foot("Manufacturer source: hammfg.com/part/1554T2GYCL • illustration not a certified enclosure rating after modifications")
c.save("B1_mechanical_layout.svg")

# Multipoint site topology not repeating sensitive private inspection.
d=SVG(1700,860,"B1 • MULTIPLE DRY SYSTEMS","One reusable single-channel device per approved independent measurement domain — no shared-failure multi-channel PCB")
for i,px in enumerate((73,617,1161),1):
 d.box(px,237,466,174,f"System {i} • approved tap",("Independent 4–20 mA transmitter","B1 local invalid/offline detection","Valve/air maintenance topology verified"),TEAL if i==1 else BLUE)
 d.box(px,518,466,125,f"B1 device {i}",("Factory PoE + remote DS18B20","Distinct device + calibration identity"),TEAL)
 d.path(f"M{px+233} 411 V515",TEAL)
 d.path(f"M{px+233} 643 V706",BLUE)
d.rect(467,712,768,80,PANEL2,GOLD,18)
d.text(851,748,"SITE ROLLUP  •  NEVER GREEN IF ONE DEVICE IS MISSING",20,GOLD,700,"middle")
d.text(851,776,"Software interface only — qualified site design decides actual device count",15,TEXT,500,"middle")
d.foot("Common compressor outlet alone cannot prove pressure independently on every downstream dry-system valve")
d.save("B1_multi_system_coverage.svg")
print("ENGINEERING_SVGS_DONE")
