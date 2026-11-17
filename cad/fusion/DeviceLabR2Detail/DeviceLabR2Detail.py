"""Device Lab R2: detailed service-first industrial sprinkler-monitor CAD concept.
Uses approved P4 STL byte-exact. Mock boards, glands, walls and supports are
VISUAL/PROVISIONAL. No enclosure drilling or mount dimensions are accepted.
"""
import adsk.core, adsk.fusion
import os, json, math, hashlib, traceback
from datetime import datetime

HOME=os.path.expanduser("~")
OUT=os.path.join(HOME,"Documents","DeviceLab","Fusion")
P4=os.path.join(OUT,"Project_Plate_P4_M3_Heatset_APPROVED_REFERENCE.stl")
RESULT=os.path.join(OUT,"r2_detail_result.json")
SHA="1b2c593862eefe328c76ad1b6fe5e358a4fb71e1e7dc10909f55384ac18ff9f2"

def point(x,y,z=0):
    return adsk.core.Point3D.create(x/10,y/10,z/10)

def occ(parent,name,x=0,y=0,z=0,rotX=0):
    matrix=adsk.core.Matrix3D.create()
    if rotX:
        matrix.setToRotation(rotX,adsk.core.Vector3D.create(1,0,0),point(0,0))
    matrix.translation=adsk.core.Vector3D.create(x/10,y/10,z/10)
    obj=parent.occurrences.addNewComponent(matrix)
    obj.component.name=name
    return obj,obj.component

def rectangle(c,name,x0,y0,x1,y1,height,operation=None):
    sk=c.sketches.add(c.xYConstructionPlane)
    sk.name=name+" profile"
    sk.sketchCurves.sketchLines.addTwoPointRectangle(point(x0,y0),point(x1,y1))
    op=operation or adsk.fusion.FeatureOperations.NewBodyFeatureOperation
    feature=c.features.extrudeFeatures.addSimple(sk.profiles.item(0),
        adsk.core.ValueInput.createByString(str(height)+" mm"),op)
    if feature.bodies.count:
        b=feature.bodies.item(0)
        if op==adsk.fusion.FeatureOperations.NewBodyFeatureOperation:
            b.name=name
        return b
    return None

def round_body(c,name,x,y,r,h,operation=None):
    sk=c.sketches.add(c.xYConstructionPlane)
    sk.name=name+" circle"
    sk.sketchCurves.sketchCircles.addByCenterRadius(point(x,y),r/10)
    op=operation or adsk.fusion.FeatureOperations.NewBodyFeatureOperation
    f=c.features.extrudeFeatures.addSimple(sk.profiles.item(0),
        adsk.core.ValueInput.createByString(str(h)+" mm"),op)
    if f.bodies.count:
        b=f.bodies.item(0)
        if op==adsk.fusion.FeatureOperations.NewBodyFeatureOperation:
            b.name=name
        return b
    return None

def opac(body,alpha):
    try: body.opacity=alpha
    except Exception: pass

def material(body,design,names):
    try:
        for n in names:
            a=design.appearances.itemByName(n)
            if a:
                body.appearance=a
                return n
    except Exception:
        pass
    return None

def record(result):
    os.makedirs(OUT,exist_ok=True)
    with open(RESULT,"w",encoding="utf8") as f:json.dump(result,f,indent=2)

def run(context):
    stage="file"
    result={"date":datetime.now().isoformat(),"status":"RUNNING","type":"R2 DETAILED CONCEPT - NOT A FABRICATION DRAWING"}
    try:
        with open(P4,"rb") as f: verified=hashlib.sha256(f.read()).hexdigest()
        if verified!=SHA:raise RuntimeError("P4 checksum mismatch; do not proceed")
        # Guard against drifting mechanical/electrical layout while running an
        # older installed script. GitHub is authority; halt if plan changes.
        layout_path=os.path.join(HOME,"Documents","DeviceLab", "SprinklerSystemMonitor", "cad", "fusion", "DeviceLabR2Detail", "assembly-layout.json")
        with open(layout_path,"r",encoding="utf8") as lf: layout=json.load(lf)
        if layout["evidence"]["sha256"]!=SHA: raise RuntimeError("Layout P4 reference differs")
        expected=[(12,3,82,53),(11,61,83.8,82),(12,89,82,139)]
        actual=[tuple(b["xy"]) for b in layout["boards"]]
        if actual!=expected: raise RuntimeError("Board layout changed; sync Fusion script before running")
        if layout["P4"]["surface_z"]!=11 or layout["enclosure"]["floor_top_z"]!=2:
            raise RuntimeError("P4 floor transform differs from verified vertical study")
        app=adsk.core.Application.get()
        doc=app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
        design=adsk.fusion.Design.cast(app.activeProduct)
        design.designType=adsk.fusion.DesignTypes.ParametricDesignType
        root=design.rootComponent
        stage="provisional enclosure"
        _,case=occ(root,"01 | PROVISIONAL original enclosure exterior trace 104.4x151.9",0,0,0)
        # P2 scanned exterior is about 104.4 x 151.9 mm (not an exact interior
        # scan). P4 fits this real case; use the scan to avoid upsizing the box.
        base=rectangle(case,"Provisional case floor from exterior paper trace",-4.62,-4.624,99.78,147.276,2.0)
        material(base,design,["Plastic - Matte (Gray)","Plastic - Matte (Light Gray)"])
        for name,corners in [
            ("left enclosure wall",(-4.62,-4.624,-3.42,147.276)),
            ("right enclosure wall",(98.58,-4.624,99.78,147.276)),
            ("front enclosure wall",(-4.62,-4.624,99.78,-3.424)),
            ("back enclosure wall",(-4.62,146.076,99.78,147.276))]:
            b=rectangle(case,name,*corners,59)
            opac(b,0.15)
        stage="verified P4"
        m=adsk.core.Matrix3D.create()
        m.setToRotation(math.pi,adsk.core.Vector3D.create(1,0,0),point(0,0,0))
        # P4 original base is Z=0..3, four mounting feet extend to Z=9.
        # Flipping turns feet down; lifting the original Z=0 face to Z=11 mm
        # seats the lowest feet at Z=2 mm on the case-floor top.
        m.translation=adsk.core.Vector3D.create(0,142.652/10,11.0/10)
        pOcc=root.occurrences.addNewComponent(m)
        plate=pOcc.component
        plate.name="02 | VERIFIED P4 mesh (unchanged, feet down)"
        bf=plate.features.baseFeatures.add()
        if not bf.startEdit():raise RuntimeError("P4 mesh import edit failed")
        try:
            plate.meshBodies.add(P4,adsk.fusion.MeshUnits.MillimeterMeshUnit,bf)
        finally:bf.finishEdit()
        if plate.meshBodies.count!=1:raise RuntimeError("P4 reference not loaded")
        stage="real board A details"
        _,boardA=occ(root,"03 | BOARD A detailed concept ADS1115 + R1-R4 + C1/C2",12,3,19)
        b=rectangle(boardA,"70x50 isolated-pad perfboard A",0,0,70,50,1.6)
        material(b,design,["FR4 - Green","PCB - Green"])
        # Coordinates of holes on user's A-R / 1-24 board. These features
        # are reference models only; they do not alter soldered board.
        pitch=2.54; left=(70-23*pitch)/2; bottom=(50-17*pitch)/2
        def hole(col,row):
            return left+(col-1)*pitch,bottom+(ord(row.upper())-65)*pitch
        # Header P3-P12 is user-confirmed. Visually depict its pins.
        _,header=occ(boardA,"ACTUAL header P3-P12 (10 pins)",0,0,1.6)
        hx0,hy=hole(3,"P");hx1,_=hole(12,"P")
        rectangle(header,"10-way female breakaway socket envelope",hx0-1.3,hy-1.55,hx1+1.3,hy+1.55,5.2)
        for col in range(3,13):
            px,py=hole(col,"P")
            round_body(header,"Header pin P%d"%col,px,py,0.55,6.1)
        # The populated ADS breakout is on removable headers; it is *not* a
        # second PCB on the other solder side and is NOT a field terminal.
        _,ads=occ(boardA,"Removable ADS1115 breakout blue placeholder (10 pins)",0,0,8.8)
        rect=rectangle(ads,"ADS1115 10-pin blue PCB mock",hx0-2.5,hy-10.5,hx1+2.5,hy+2.5,1.6)
        material(rect,design,["Paint - Enamel Glossy (Blue)","Plastic - Glossy (Blue)"])
        _,adsChip=occ(boardA,"ADC silicon IC body",0,0,10.4)
        rectangle(adsChip,"ADS1115 chip mock",hx0+9,hy-6,hx0+14,hy-1,1.1)
        for name,v,col1,col2,row in [
            ("R1 10k",10000,3,7,"D"),("R2 10k",10000,9,13,"D"),
            ("R3 4.7k",4700,15,19,"D"),("R4 1k",1000,9,13,"F")]:
            x0,y0=hole(col1,row);x1,_=hole(col2,row)
            _,res=occ(boardA,name+" (preexisting soldered)",0,0,1.6)
            rectangle(res,name+" resistor body",x0+2,y0-1,x1-2,y0+1,2.4)
        for name,loc in [("C1 100nF 104",("H",14)),
                         ("C2 100nF 104",("N",16))]:
            row,col=loc
            x,y=hole(col,row)
            _,cap=occ(boardA,name+" (preexisting soldered)",0,0,1.6)
            round_body(cap,name+" disk marker",x,y,1.7,2.8)
        stage="controller details"
        _,esp=occ(root,"04 | Waveshare ESP32-S3-ETH/PoE (controller separate)",11,61,19)
        pcb=rectangle(esp,"Waveshare board 72.8x21 reference",0,0,72.8,21,1.6)
        material(pcb,design,["FR4 - Black","Plastic - Matte (Black)"])
        _,jack=occ(esp,"Factory RJ45 Ethernet jack + plug clearance envelope",0,0,1.6)
        rectangle(jack,"RJ45 connector housing (illustrative)",1,2,17,19,12)
        _,chip=occ(esp,"ESP32-S3 RF shield",0,0,1.6)
        rectangle(chip,"RF shield can",25,3,45,18,3.5)
        _,poe=occ(esp,"Existing PoE daughterboard STACK HEIGHT ESTIMATE",0,0,1.6)
        rectangle(poe,"PoE isolated converter region mock",47,1.3,69,19.5,14.6)
        _,usb=occ(esp,"USB test port envelope",0,0,1.6)
        rectangle(usb,"USB port block",18,6,24,15,3.8)
        _,button=occ(esp,"BOOT RESET button group",0,0,1.6)
        rectangle(button,"Two service buttons mock",69,4,72,18,2.5)
        stage="board B details"
        _,boardB=occ(root,"05 | BOARD B J1 pressure + J2 temperature + R5",12,89,19)
        b=rectangle(boardB,"70x50 isolated-pad perfboard B",0,0,70,50,1.6)
        material(b,design,["FR4 - Green","PCB - Green"])
        for idx,(tag,y0) in enumerate([("J1 PRESS +5V GND SIG",4),
                                      ("J2 TEMP +3V3 DATA GND",28)]):
            _,term=occ(boardB,tag+" independent 3-position block",0,0,1.6)
            tb=rectangle(term,tag+" housing",42,y0,60,y0+16,8.5)
            material(tb,design,["Plastic - Glossy (Blue)","Plastic - Matte (Blue)"])
            _,heads=occ(boardB,tag+" three screw heads",0,0,10.1)
            for j,pin in enumerate((1,2,3)):
                round_body(heads,"%s pin %d screw"%(tag,pin),45+j*6,y0+9,1.8,0.7)
        _,pullup=occ(boardB,"R5 4.7k from J2 3V3 to DATA",0,0,1.6)
        rectangle(pullup,"R5 4.7k marker",14,19,27,21,2.4)
        stage="supports and service harness"
        _,stands=occ(root,"06 | 8mm insulated supports mock - holes UNVERIFIED",0,0,11)
        supports=[]
        for name,coords in [
          ("A",[(18,7),(77,7),(18,48),(77,48)]),
          ("ESP",[(16,65),(79,65),(16,78),(79,78)]),
          ("B",[(18,93),(77,93),(18,133),(77,133)])]:
            for n,(x,y) in enumerate(coords):
                round_body(stands,"%s insulated riser %d"%(name,n+1),x,y,2.5,8)
                supports.append((name,x,y))
        _,channel=occ(root,"07 | Service harness guide (not actual conductors)",0,0,12)
        rectangle(channel,"Right 6mm W07-W09 B-to-A 3-wire corridor",86.5,14,92.5,130,1.8)
        rectangle(channel,"Cable restraint lane to Board B",83,91,89,135,2)
        for n,y in enumerate((23,39,55,73,92,111,125)):
            _,tie=occ(channel,"removable nylon tie saddle location %d"%(n+1),0,0,1.8)
            rectangle(tie,"tie saddle marker",85.3,y-1.5,93.7,y+1.5,2.5)
        stage="gland/access concepts"
        # Ports are annotation envelopes only: no holes are drilled in the case.
        _,entries=occ(root,"08 | 3 cable ENTRY ZONES (no cut geometry)")
        for label,cy in [
            ("J1 PRESSURE right wall entry zone",101),
            ("J2 TEMPERATURE right wall entry zone",126)]:
            _,g=occ(entries,label+" UNDRILLED",0,0,20)
            rectangle(g,label+" no-drill highlight",98.58,cy-6,99.78,cy+6,12)
        _,eth=occ(entries,"ETH split-gland / serviceable RJ45 ENTRY concept",0,0,0)
        rectangle(eth,"RJ45 gland zone left wall - DO NOT DRILL",-4.62,62,-3.42,82,23)
        stage="lid/exploded options"
        lidocc,lid=occ(root,"09 | Existing gasket lid mock (hidden for service)",0,0,59)
        lb=rectangle(lid,"Removable lid conceptual silhouette",-4.62,-4.624,99.78,147.276,3.2)
        opac(lb,0.11)
        try:lidocc.isLightBulbOn=False
        except Exception:pass
        stage="CAD validation"
        planned=[("A",(12,3,82,53)),("ESP",(11,61,83.8,82)),("B",(12,89,82,139))]
        gaps=[planned[1][1][1]-planned[0][1][3],planned[2][1][1]-planned[1][1][3]]
        assert min(gaps)>0,("Board footprint overlap",gaps)
        assert planned[2][1][3]<142.652,"Board B protrudes beyond accepted P4 envelope"
        # Centered boards occupy only nominal rectangular envelopes; no full
        # collision/connector/fastener simulation has been performed.
        stage="export"
        tag=datetime.now().strftime("%Y%m%d_%H%M%S")
        f3d=os.path.join(OUT,"R2_Detailed_Industrial_Concept_"+tag+".f3d")
        export=design.exportManager
        if not export.execute(export.createFusionArchiveExportOptions(f3d)):
            raise RuntimeError("Fusion export refused F3D")
        if not os.path.isfile(f3d):
            raise RuntimeError("F3D was not created")
        app.activeViewport.fit()
        result.update({
            "status":"SUCCESS",
            "f3d":f3d,"bytes":os.path.getsize(f3d),
            "exact_p4_sha256":verified,"P4_modified":False,
            "P4_mesh_bodies":plate.meshBodies.count,
            "top_level_components":root.occurrences.count,
            "proposed_board_envelopes":planned,"Y_gaps_mm":gaps,
            "separate_pressure_and_temp_terminal_blocks":2,
            "A_header_map":"P3-P12, 10 pins",
            "installed_resistor_mocks":["R1 10k","R2 10k","R3 4.7k","R4 1k"],
            "capacitor_mocks":["C1 100nF","C2 100nF"],
            "R5_B_pullup":"4.7k between 3V3 and DATA",
            "supports":supports,
            "unknown_before_print":["enclosure internal dimensions/depth","standoff hole anchorage",
                "sensor cable entry glands and enclosure wall structure",
                "RJ45 plugged cable path / bend radius","actual PoE stack height",
                "screwdriver reach to terminal heads","real board populated clearances",
                "P4 plastic hole grid under foot supports"],
            "cloud_saved":False
        })
        record(result)
    except Exception:
        result.update({"status":"FAILED","stage":stage,"error":traceback.format_exc()})
        record(result)
