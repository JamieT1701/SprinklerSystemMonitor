"""Device Lab R1 provisional 3D assembly layout.

Governing mechanical reference: approved P4 STL, imported EXACTLY as provided.
All enclosure walls, PCB positions, ports, standoffs and component blocks are
PRELIMINARY MOCKUPS, not fabrication drawings. Do not overwrite P4 or claim fit.
"""
import adsk.core
import adsk.fusion
import math
import os
import json
import hashlib
import traceback
from datetime import datetime

HOME = os.path.expanduser("~")
OUT = os.path.join(HOME, "Documents", "DeviceLab", "Fusion")
P4 = os.path.join(OUT, "Project_Plate_P4_M3_Heatset_APPROVED_REFERENCE.stl")
RESULT = os.path.join(OUT, "r1_assembly_result.json")
P4_SHA = "1b2c593862eefe328c76ad1b6fe5e358a4fb71e1e7dc10909f55384ac18ff9f2"
P4_W, P4_L = 95.1599, 142.6520

def p(x,y,z=0):
    return adsk.core.Point3D.create(x/10.0,y/10.0,z/10.0)

def offset(x,y,z):
    mx=adsk.core.Matrix3D.create()
    mx.translation=adsk.core.Vector3D.create(x/10.0,y/10.0,z/10.0)
    return mx

def new_part(root, name, x=0,y=0,z=0):
    occ=root.occurrences.addNewComponent(offset(x,y,z))
    occ.component.name = name
    return occ, occ.component

def box(comp, name, x0,y0,x1,y1, thickness):
    sk=comp.sketches.add(comp.xYConstructionPlane)
    sk.name=name+" footprint"
    sk.sketchCurves.sketchLines.addTwoPointRectangle(p(x0,y0),p(x1,y1))
    ext=comp.features.extrudeFeatures.addSimple(
        sk.profiles.item(0),
        adsk.core.ValueInput.createByString(str(thickness)+" mm"),
        adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    b=ext.bodies.item(0)
    b.name=name
    return b

def disk(comp,name,x,y,radius,height):
    sk=comp.sketches.add(comp.xYConstructionPlane)
    sk.sketchCurves.sketchCircles.addByCenterRadius(p(x,y),radius/10.0)
    ext=comp.features.extrudeFeatures.addSimple(
        sk.profiles.item(0),
        adsk.core.ValueInput.createByString(str(height)+" mm"),
        adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    b=ext.bodies.item(0);b.name=name
    return b

def fade(body, amount):
    try: body.opacity=amount
    except Exception: pass

def write_result(result):
    os.makedirs(OUT,exist_ok=True)
    with open(RESULT, "w", encoding="utf-8") as stream:
        json.dump(result,stream,indent=2)

def run(context):
    stage="setup"
    state={"started_at":datetime.now().isoformat(),
           "approved_plate_sha256":P4_SHA,
           "status":"RUNNING","safety":"EXPERIMENTAL CONCEPT ONLY; NO FABRICATION"}
    try:
        with open(P4,"rb") as f:
            actual=hashlib.sha256(f.read()).hexdigest()
        if actual!=P4_SHA:
            raise RuntimeError("Accepted P4 STL hash changed; aborting")
        app=adsk.core.Application.get()
        doc=app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
        design=adsk.fusion.Design.cast(app.activeProduct)
        if not design: raise RuntimeError("No Fusion design")
        design.designType=adsk.fusion.DesignTypes.ParametricDesignType
        root=design.rootComponent
        root.name if root else None
        stage="shell"
        o,shell=new_part(root,"PROVISIONAL Existing Box Envelope 112x161x59")
        box(shell,"Enclosure floor (provisional)",-8.5,-9,103.5,152,2)
        for name,geo in [
            ("LEFT wall",(-8.5,-9,-5.5,152)),
            ("RIGHT wall",(100.5,-9,103.5,152)),
            ("LOWER wall",(-8.5,-9,103.5,-6)),
            ("UPPER wall",(-8.5,149,103.5,152))]:
            b=box(shell,name,*geo,59)
            fade(b,0.18)
        stage="P4 exact"
        flip=adsk.core.Matrix3D.create()
        flip.setToRotation(math.pi,adsk.core.Vector3D.create(1,0,0),
                           adsk.core.Point3D.create(0,0,0))
        flip.translation=adsk.core.Vector3D.create(0,P4_L/10.0,1.1)
        occ=root.occurrences.addNewComponent(flip)
        plate=occ.component
        plate.name="APPROVED P4 plate - unchanged mesh 95.1599x142.652"
        base=plate.features.baseFeatures.add()
        if not base.startEdit(): raise RuntimeError("Cannot edit P4 import base feature")
        try:
            added=plate.meshBodies.add(P4,adsk.fusion.MeshUnits.MillimeterMeshUnit,base)
        finally:
            base.finishEdit()
        if not added or plate.meshBodies.count!=1:
            raise RuntimeError("Expected one P4 reference mesh")
        plate.meshBodies.item(0).name="ACCEPTED P4 STL - exact, flipped for feet down"
        stage="PCB layout"
        # Two full-size isolated-pad perfboards, 70x50, plus the Waveshare 72.8x21 PCB.
        occA,A=new_part(root,"Board A PROVISIONAL - ADC/pressure 70x50",12,6,19)
        box(A,"Perfboard A 70x50",0,0,70,50,1.6)
        # ADS1115 breakout and resistors are representation-only; installed parts
        # remain according to authoritative hole coordinates on the real board.
        box(A,"ADS1115 breakout placeholder",24,15,49,33,2.8)
        box(A,"R1-R4 and C1-C2 placement envelope",5,5,22,40,3)
        occB,B=new_part(root,"Board B PROVISIONAL - field terminals 70x50",12,86,19)
        box(B,"Perfboard B 70x50",0,0,70,50,1.6)
        box(B,"J1 PRESS 3-position +5V GND SIG",47,5,64,22,8.5)
        box(B,"J2 TEMP 3-position +3V3 DATA GND",47,29,64,46,8.5)
        box(B,"R5 pullup envelope",12,18,29,30,2)
        occC,C=new_part(root,"Waveshare ESP32-S3-ETH PROVISIONAL 72.8x21",11,62,19)
        box(C,"Waveshare PCB 72.8x21",0,0,72.8,21,1.6)
        box(C,"RJ45 and magnetics envelope",0,2,17,19,11)
        box(C,"PoE expansion module envelope",31,1,54,20,16)
        stage="standoffs"
        _,stands=new_part(root,"PROVISIONAL removable support spacers",0,0,11)
        for prefix,coords in [("A",[(15,9),(79,9),(15,53),(79,53)]),
                              ("B",[(15,89),(79,89),(15,133),(79,133)]),
                              ("ETH",[(15,66),(80,66),(15,79),(80,79)])]:
            for i,(x,y) in enumerate(coords):
                disk(stands,"%s standoff mock %d"%(prefix,i+1),x,y,2.2,8)
        stage="harness"
        _,chan=new_part(root,"Cable management concepts - not actual wires",0,0,12)
        box(chan,"Harness tie channel RIGHT",86,15,92,133,1.2)
        box(chan,"RJ45 cable entry service envelope LEFT",-3,65,9,82,1.2)
        box(chan,"Pressure and temp cable entry service envelope RIGHT",91,94,99,137,1.2)
        stage="lid"
        lid_occ,lid=new_part(root,"REMOVABLE LID - hidden for service view",0,0,59)
        panel=box(lid,"Gasketed cover outline PROVISIONAL",-8.5,-9,103.5,152,3)
        # Hide the lid so the saved default view shows actual internal mockups.
        try: lid_occ.isLightBulbOn=False
        except Exception: fade(panel,0.05)
        stage="verify"
        # In mm, via nonoverlapping envelope estimates. No physical fit claims.
        board_boxes=[
          {"name":"A","rect_xy_mm":[12,6,82,56],"z_base_mm":19},
          {"name":"Waveshare","rect_xy_mm":[11,62,83.8,83],"z_base_mm":19},
          {"name":"B","rect_xy_mm":[12,86,82,136],"z_base_mm":19}]
        for i in range(len(board_boxes)):
            for j in range(i+1,len(board_boxes)):
                a=board_boxes[i]["rect_xy_mm"]
                b=board_boxes[j]["rect_xy_mm"]
                overlap=max(0,min(a[2],b[2])-max(a[0],b[0]))*max(0,min(a[3],b[3])-max(a[1],b[1]))
                if overlap>0: raise RuntimeError("PCB bounding boxes overlap: %s/%s"%(i,j))
        stage="export"
        stamp=datetime.now().strftime("%Y%m%d_%H%M%S")
        path=os.path.join(OUT,"R1_PROVISIONAL_Fusion_Assembly_"+stamp+".f3d")
        manager=design.exportManager
        if not manager.execute(manager.createFusionArchiveExportOptions(path)):
            raise RuntimeError("Fusion F3D export returned false")
        if not os.path.isfile(path): raise RuntimeError("Export file not found")
        app.activeViewport.fit()
        state.update({
            "status":"SUCCESS",
            "file":path,"bytes":os.path.getsize(path),
            "source_plate_preserved":True,
            "mesh_count":plate.meshBodies.count,
            "component_count":root.occurrences.count,
            "board_envelopes":board_boxes,
            "xy_board_overlap_mm2":0,
            "known_limitations":[
                "Enclosure interior/walls and wall depth estimated, not measured",
                "Actual PoE module height, RJ45 plug, gland size and bending radii require dry-fit",
                "Exact Board A/B mounting holes and wire paths not measured",
                "P4 reference is preserved mesh; shell and boards are separate editable concept components",
                "No pressure-control or listed sprinkler system modification",
                "Not a bill of materials or fabrication-ready part"],
            "cloud_saved":False
        })
        write_result(state)
    except Exception:
        state.update({"status":"FAILED","stage":stage,"error":traceback.format_exc()})
        write_result(state)
