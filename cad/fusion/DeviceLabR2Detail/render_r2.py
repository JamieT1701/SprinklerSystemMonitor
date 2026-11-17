"""Generate precise R2 CONCEPT presentations from assembly-layout.json (no Fusion GUI).
All boards are provisional placement envelopes, not production drill models.
"""
from pathlib import Path
import json,math,hashlib
from PIL import Image, ImageDraw, ImageFont
ROOT=Path(__file__).resolve().parents[3]
LAYOUT=json.loads((ROOT/"cad/fusion/DeviceLabR2Detail/assembly-layout.json").read_text(encoding="utf8"))
OUT=ROOT/"docs/assets"
OUT.mkdir(exist_ok=True,parents=True)

INK="#EBF3FD"; MUTED="#A5B6CA"; BG="#0B1525"; PANEL="#122338"; EDGE="#2B4662"
CYAN="#40C8E9"; GREEN="#2F9C6B"; DARKGREEN="#1E674E"; BLACKPCB="#263542"
ORANGE="#F6B25C"; BLUE="#3477CF"; BLUE_DARK="#19487D"; RED="#F27668"

def font(size,bold=False):
    candidates=[r"C:\Windows\Fonts\segoeuib.ttf" if bold else r"C:\Windows\Fonts\segoeui.ttf",
                r"C:\Windows\Fonts\arialbd.ttf" if bold else r"C:\Windows\Fonts\arial.ttf"]
    for p in candidates:
        try:return ImageFont.truetype(p,size)
        except OSError:pass
    return ImageFont.load_default()

def panel(draw,rect,title):
    draw.rounded_rectangle(rect,radius=25,fill=PANEL,outline=EDGE,width=2)
    draw.text((rect[0]+22,rect[1]+18),title,font=font(27,True),fill=INK)

def txt(draw,pos,text,size=25,color=INK,bold=False):
    draw.text(pos,text,font=font(size,bold),fill=color)

def border_badge(draw,x,y,label,color=CYAN):
    tw=draw.textbbox((0,0),label,font=font(23,True))[2]
    draw.rounded_rectangle((x,y,x+tw+30,y+44),radius=12,fill=PANEL,outline=color,width=2)
    txt(draw,(x+15,y+7),label,23,color,True)

def project_xy(x,y,scale=8.2,ox=395,oy=315):
    e=LAYOUT["enclosure"]
    return (round(ox+(x-e["outer_min_xyz"][0])*scale),
            round(oy+(e["outer_max_xyz"][1]-y)*scale))

def rectangle_xy(d,rect,fill,outline=EDGE,width=2):
    x0,y0,x1,y1=rect
    lt=project_xy(x0,y1);rb=project_xy(x1,y0)
    d.rectangle((*lt,*rb),fill=fill,outline=outline,width=width)
    return lt,rb

def top_view():
    im=Image.new("RGB",(1800,2250),BG);d=ImageDraw.Draw(im)
    txt(d,(80,55),"SPRINKLER SYSTEM MONITOR",72,INK,True)
    txt(d,(84,144),"DEVICE LAB   /   R2 SERVICE-FIRST ASSEMBLY STUDY",29,CYAN,True)
    border_badge(d,1340,143,"NOT PRINT-READY",ORANGE)
    panel(d,(62,216,1744,1665),"TOP VIEW  |  ALL DIMENSIONS IN MM")
    # Bound envelope from scanned outer shell
    e=LAYOUT["enclosure"]
    external=(e["outer_min_xyz"][0],e["outer_min_xyz"][1],e["outer_max_xyz"][0],e["outer_max_xyz"][1])
    rectangle_xy(d,external,"#1A3047",CYAN,4)
    # Approved P4 bounding plate. Shape is envelope, not a claim of exact outline.
    p=LAYOUT["P4"]["bbox_xyz"]; plate=(0,0,p[0],p[1])
    rectangle_xy(d,plate,"#1B4554","#54D7E8",5)
    # P4 grid simplified for readability. Not a hole drilling template.
    for x in [17.58+i*10 for i in range(7)]:
        for y in [6.326+j*10 for j in range(14)]:
            if x<p[0]-5 and y<p[1]-5:
                px,py=project_xy(x,y)
                d.ellipse((px-2,py-2,px+2,py+2),fill="#52858E")
    for x,y in LAYOUT["P4"]["feet_centers"]:
        xx,yy=project_xy(x,y)
        r=round(4.5*8.2)
        d.ellipse((xx-r,yy-r,xx+r,yy+r),fill="#214655",outline=ORANGE,width=3)
        d.ellipse((xx-8,yy-8,xx+8,yy+8),outline=ORANGE,width=3)
    # Main board layout
    for b in LAYOUT["boards"]:
        color=BLACKPCB if b["id"]=="ESP" else DARKGREEN
        rectangle_xy(d,b["xy"],color,"#C7E3DB" if b["id"]!="ESP" else "#A5B4BD",3)
        x0,y0,x1,y1=b["xy"]
        cx,cy=project_xy((x0+x1)/2,(y0+y1)/2)
        label=("BOARD A" if b["id"]=="A" else "ESP32-S3 PoE" if b["id"]=="ESP" else "BOARD B")
        txt(d,(cx-89,cy-23),label,28,INK,True)
        if b["id"]=="A":
            txt(d,(cx-140,cy+17),"ADS1115 + R1–R4 + C1/C2",21,"#B9EBCF")
            # Removable 10-pin header reference, top edge
            hy=y0+(50-17*2.54)/2+15*2.54
            for col in range(3,13):
                hx=x0+(70-23*2.54)/2+(col-1)*2.54
                px,py=project_xy(hx,hy)
                d.ellipse((px-6,py-6,px+6,py+6),fill="#F4D18A")
        elif b["id"]=="ESP":
            txt(d,(cx-118,cy+14),"FACTORY RJ45 / POE",20,CYAN)
            rectangle_xy(d,(x0+1,y0+2,x0+17,y0+19),"#8796A4","#C5D3DB",2)
        else:
            txt(d,(cx-120,cy+19),"J1 / J2 + R5 pull-up",20,"#C2E9D3")
            for block in LAYOUT["boardB"]["terminals"]:
                lx0,ly0,lx1,ly1=block["local_xy"]
                rectangle_xy(d,(x0+lx0,y0+ly0,x0+lx1,y0+ly1),BLUE_DARK,BLUE,3)
                for j in range(3):
                    px,py=project_xy(x0+lx0+3+j*6,y0+ly0+9)
                    d.ellipse((px-9,py-9,px+9,py+9),fill="#C6D2DE",outline="#556374",width=2)
    # Wire harness right-hand channel, no actual wires depicted
    rectangle_xy(d,LAYOUT["harness"]["provisional_corridor_xy"],"#30485A",CYAN,2)
    # Vertical scale/dimensions: P4 142.65 mm and 95.16mm
    a=project_xy(0,0);b=project_xy(95.1599,0);top=project_xy(0,142.652)
    d.line((a[0],1580,b[0],1580),fill=INK,width=3)
    d.line((a[0],1571,a[0],1593),fill=INK,width=3)
    d.line((b[0],1571,b[0],1593),fill=INK,width=3)
    txt(d,((a[0]+b[0])/2-136,1593),"P4 WIDTH   95.16",25,CYAN,True)
    d.line((314,top[1],314,a[1]),fill=INK,width=3)
    d.line((303,top[1],325,top[1]),fill=INK,width=3)
    d.line((303,a[1],325,a[1]),fill=INK,width=3)
    txt(d,(100,800),"P4 LENGTH",26,CYAN,True)
    txt(d,(127,845),"142.65",27,INK,True)
    # Right side readout
    panel(d,(1304,307,1723,973),"DESIGN COMPONENTS")
    entries=[
      ("01","P4 PLATE","Exact original mesh"),
      ("02","BOARD A","Pressure + ADS1115"),
      ("03","ETHERNET","ESP32-S3 + PoE"),
      ("04","BOARD B","J1 / J2 / R5"),
      ("05","HARNESS","Proposed tie corridor"),
      ("06","CASE","Exterior scan estimate")
    ]
    y=370
    for no,h,s in entries:
        txt(d,(1335,y),no,27,CYAN,True)
        txt(d,(1400,y),h,24,INK,True)
        txt(d,(1400,y+37),s,21,MUTED)
        y+=97
    panel(d,(1304,1001,1723,1505),"FIT STATUS")
    txt(d,(1335,1068),"PASS",34,GREEN,True)
    txt(d,(1335,1116),"No PCB envelope",23,INK)
    txt(d,(1335,1147),"overlap (2D only)",23,INK)
    txt(d,(1335,1220),"OPEN",34,ORANGE,True)
    for j,s in enumerate(["Actual enclosure Z","RJ45 cable bend","Terminal screwdriver","PCB support anchors","Gland sealing"]):
        txt(d,(1335,1271+j*39),s,21,MUTED)
    # Bottom section and legend
    panel(d,(63,1690,1170,2156),"SIDE SECTION  |  MODELED Z (PROVISIONAL)")
    x0=180
    z0=2070
    def zline(z,textlabel,color):
        yy=z0-round(z*5.3)
        d.line((x0+100,yy,980,yy),fill=color,width=8 if z in (2,11,19) else 3)
        txt(d,(105,yy-14),f"{z:.1f}",23,color,True)
        txt(d,(1000,yy-17),textlabel,22,INK)
    zline(2,"Case floor",MUTED)
    zline(8,"Plate underside",CYAN)
    zline(11,"P4 upper deck",CYAN)
    zline(19,"PCB underside",GREEN)
    zline(35.2,"Max estimated PoE envelope",ORANGE)
    zline(59,"Study lid plane",MUTED)
    panel(d,(1196,1690,1743,2156),"R6 FIELD CONNECTIONS")
    for i,(title,details) in enumerate([
        ("ETHERNET / POE","Factory RJ45, no extra port"),
        ("J1  PRESSURE","+5V   •   GND   •   SIG"),
        ("J2  TEMPERATURE","+3V3   •   DATA   •   GND")]):
        y=1770+i*120
        txt(d,(1225,y),title,25,CYAN,True)
        txt(d,(1225,y+43),details,23,INK)
    txt(d,(84,2192),"CONCEPT R2  /  P4 IS REAL  /  BOARD MOUNTS & CASE CLEARANCE REQUIRE DRY-FIT",22,ORANGE,True)
    path=OUT/"fusion-r2-layout-top.png"
    im.save(path,optimize=True)
    return path

def iso():
    im=Image.new("RGB",(2200,1560),BG);d=ImageDraw.Draw(im)
    txt(d,(75,55),"SPRINKLER MONITOR",75,INK,True)
    txt(d,(78,157),"R2  /  ORTHOGRAPHIC ASSEMBLY STUDY  /  MODEL-DERIVED",30,CYAN,True)
    border_badge(d,1680,159,"CONCEPT ONLY",ORANGE)
    # Isometric projection: P4 long direction extends down-left, PCB z goes up.
    def pr(x,y,z):
        ox=1340;oy=590;ss=5.4
        return (round(ox+(x-0)*ss-(y-0)*ss*.72),
                round(oy+x*ss*.33+y*ss*.38-z*ss*1.14))
    def poly(vertices,fill,edge=None):
        points=[pr(*v) for v in vertices]
        d.polygon(points,fill=fill)
        if edge:d.line(points+[points[0]],fill=edge,width=3,joint="curve")
    def cuboid(rect,z,height,top,side,right=None):
        x0,y0,x1,y1=rect;u=z;v=z+height
        # rear sides first, top last (suitable for this camera)
        poly([(x0,y1,u),(x1,y1,u),(x1,y1,v),(x0,y1,v)],side)
        poly([(x1,y0,u),(x1,y1,u),(x1,y1,v),(x1,y0,v)],right or side)
        poly([(x0,y0,v),(x1,y0,v),(x1,y1,v),(x0,y1,v)],top,"#8DA8B8")
    # Case base surface; walls shown as fine outlines to expose electronics.
    e=LAYOUT["enclosure"];case=(e["outer_min_xyz"][0],e["outer_min_xyz"][1],e["outer_max_xyz"][0],e["outer_max_xyz"][1])
    cuboid(case,0,2,"#203249","#263C51")
    for x,y in LAYOUT["P4"]["feet_centers"]:
        # feet are below P4 main deck
        cuboid((x-4.5,y-4.5,x+4.5,y+4.5),2,6,"#4D98A3","#2A6674")
    cuboid((0,0,95.1599,142.652),8,3,"#2F7A88","#225A67")
    # P4 10 mm perforation grid as markers, not drill-location claims.
    for x in [17.58+i*10 for i in range(7)]:
        for y in [6.326+j*10 for j in range(14)]:
            if y<141.0:
                px,py=pr(x,y,11.04); d.ellipse((px-2,py-2,px+2,py+2),fill="#5AC9CF")
    for x,y in LAYOUT["mounts"]["locations"]:
        cuboid((x-1.8,y-1.8,x+1.8,y+1.8),11,8,"#DEE4EB","#8E9EAA")
    # board A / ESP / B; draw from back to front by world y descending
    for b in sorted(LAYOUT["boards"],key=lambda b:b["xy"][1],reverse=True):
        is_esp=b["id"]=="ESP";color="#313D4C" if is_esp else "#278560"
        cuboid(b["xy"],b["z"],b["thickness"],color,"#1A4A42" if not is_esp else "#253041")
        x0,y0,x1,y1=b["xy"]
        if b["id"]=="B":
            for t in LAYOUT["boardB"]["terminals"]:
                tx0,ty0,tx1,ty1=t["local_xy"]
                cuboid((x0+tx0,y0+ty0,x0+tx1,y0+ty1),b["z"]+1.6,8.5,"#277CB9","#17477A")
                for j in range(3):
                    px,py=pr(x0+tx0+3+j*6,y0+ty0+9,30)
                    d.ellipse((px-6,py-6,px+6,py+6),fill="#D3DCE4")
        elif b["id"]=="A":
            cuboid((x0+20,y0+26,x0+49,y0+42),20.6,8,"#2778C5","#204E84")
            for x in (x0+12,x0+36,x0+56):
                cuboid((x,y0+9,x+9,y0+12),20.6,3,"#EAC78D","#A9825D")
        else:
            cuboid((x0+1,y0+2,x0+17,y0+19),20.6,12,"#7C96AB","#4B5A6A")
            cuboid((x0+25,y0+3,x0+45,y0+18),20.6,3.5,"#B6C2CC","#67788B")
            cuboid((x0+47,y0+1.3,x0+69,y0+19.5),20.6,14.6,"#525F6F","#34485B")
    # Harness corridor
    ch=LAYOUT["harness"]["provisional_corridor_xy"]
    cuboid(ch,12,1.8,"#477789","#2E4A5D")
    # Wireframe case walls, visible outlines only
    xx0,yy0,xx1,yy1=case
    for a,b in [((xx0,yy0,2),(xx0,yy0,59)),
                ((xx0,yy1,2),(xx0,yy1,59)),
                ((xx1,yy0,2),(xx1,yy0,59)),
                ((xx1,yy1,2),(xx1,yy1,59))]:
        d.line([pr(*a),pr(*b)],fill="#7491A4",width=2)
    d.line([pr(xx0,yy0,59),pr(xx1,yy0,59),pr(xx1,yy1,59),pr(xx0,yy1,59),pr(xx0,yy0,59)],fill="#54758B",width=2)
    # Callouts on left with precise reference point connectors
    callouts=[
        ("BOARD B","3-position J1 + J2 on 70x50",(48,115,30),(145,360)),
        ("ESP32-S3 POE","Factory Ethernet + PoE PCB",(50,71,31),(145,570)),
        ("BOARD A","ADS1115 + pressure filter R1-R4",(45,27,29),(145,780)),
        ("P4 MOUNTING PLATE","Approved, unchanged print mesh",(45,10,11),(145,990)),
    ]
    for title,desc,wpt,xy in callouts:
        tx,ty=xy;px,py=pr(*wpt)
        d.line((tx+440,ty+45,px,py),fill=CYAN,width=3)
        d.ellipse((px-7,py-7,px+7,py+7),fill=CYAN)
        d.rounded_rectangle((tx-18,ty-18,tx+445,ty+100),radius=16,fill=PANEL,outline=EDGE,width=2)
        txt(d,(tx,ty),title,30,CYAN,True)
        txt(d,(tx,ty+47),desc,22,INK)
    panel(d,(1500,1050,2110,1433),"ENGINEERING GATES")
    notes=["Envelope model only","Actual lid height unknown","RJ45 bend unverified","Terminal access unverified","Support anchorage unverified","No machining/holes approved"]
    for i,s in enumerate(notes):
        txt(d,(1530,1118+i*47),"•  "+s,24,INK if i<3 else MUTED)
    txt(d,(86,1496),"P4 FEET Z=2  /  P4 TOP Z=11  /  PCB Z=19  /  ENCLOSURE HEIGHT IS ASSUMED",23,ORANGE,True)
    path=OUT/"fusion-r2-assembly-isometric.png"
    im.save(path,optimize=True)
    return path

if __name__=="__main__":
    for p in [top_view(),iso()]:
        with Image.open(p) as image:
            print(p, "size",image.size,"bytes",p.stat().st_size,"sha256",hashlib.sha256(p.read_bytes()).hexdigest())
