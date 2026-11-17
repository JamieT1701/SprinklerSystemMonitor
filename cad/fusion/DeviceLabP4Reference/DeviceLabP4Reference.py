"""P4 exact-as-printed reference for the sprinkler-monitor Device Lab build.
Preserves the accepted P4 STL as a mesh and performs read-only geometry verification.
No mesh modifications, offsets, booleans or unverified fit placements.
"""
import adsk.core
import adsk.fusion
import os
import json
import hashlib
import traceback
from datetime import datetime

FOLDER = os.path.join(os.path.expanduser("~"), "Documents", "DeviceLab", "Fusion")
SOURCE = os.path.join(FOLDER, "Project_Plate_P4_M3_Heatset_APPROVED_REFERENCE.stl")
RESULT = os.path.join(FOLDER, "p4_fusion_import_result.json")
KNOWN_SHA256 = "1b2c593862eefe328c76ad1b6fe5e358a4fb71e1e7dc10909f55384ac18ff9f2"
EXPECTED_SPAN_MM = (95.1599, 142.652, 9.0)

def write_result(state):
    with open(RESULT, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)

def run(context):
    stage = "startup"
    state = {"timestamp": datetime.now().isoformat(), "source_stl": SOURCE,
             "source_sha256": KNOWN_SHA256, "modified_original_stl": False}
    try:
        with open(SOURCE, "rb") as f:
            sha = hashlib.sha256(f.read()).hexdigest()
        if sha != KNOWN_SHA256:
            raise RuntimeError("Source P4 STL differs from accepted SHA256; import aborted")
        stage = "create_design"
        app = adsk.core.Application.get()
        doc = app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
        design = adsk.fusion.Design.cast(app.activeProduct)
        design.designType = adsk.fusion.DesignTypes.ParametricDesignType
        root = design.rootComponent
        stage = "import_mesh"
        base = root.features.baseFeatures.add()
        if not base.startEdit():
            raise RuntimeError("Could not start mesh base feature edit")
        try:
            bodies = root.meshBodies.add(SOURCE,
                adsk.fusion.MeshUnits.MillimeterMeshUnit, base)
        finally:
            base.finishEdit()
        if not bodies or bodies.count < 1:
            raise RuntimeError("Mesh import returned no bodies")
        body = root.meshBodies.item(root.meshBodies.count - 1)
        body.name = "ACCEPTED P4 mesh - DO NOT MODIFY"
        stage = "validate"
        bounds = body.boundingBox
        span_cm = [bounds.maxPoint.x-bounds.minPoint.x,
                   bounds.maxPoint.y-bounds.minPoint.y,
                   bounds.maxPoint.z-bounds.minPoint.z]
        span_mm = [round(v*10.0,4) for v in span_cm]
        for got, want in zip(span_mm,EXPECTED_SPAN_MM):
            if abs(got-want)>0.06:
                raise RuntimeError("Imported P4 geometry mismatch. Measured %s, expected %s" % (span_mm,EXPECTED_SPAN_MM))
        stage = "export"
        datecode = datetime.now().strftime("%Y%m%d_%H%M%S")
        dest = os.path.join(FOLDER,"P4_Approved_Reference_"+datecode+".f3d")
        options = design.exportManager.createFusionArchiveExportOptions(dest)
        success = design.exportManager.execute(options)
        if not success or not os.path.isfile(dest):
            raise RuntimeError("Failed to export Fusion reference F3D")
        app.activeViewport.fit()
        state.update({"status":"SUCCESS","source_imported_at_original_scale":True,
          "imported_mesh_bodies":root.meshBodies.count,
          "imported_bounds_mm":span_mm,"expected_bounds_mm":EXPECTED_SPAN_MM,
          "f3d":dest,"f3d_bytes":os.path.getsize(dest),
          "document_name":doc.name,"cloud_saved":False,
          "note":"P4 exact mesh reference only. Not a parametric recreation; physical board placement is not approved."})
        write_result(state)
    except Exception:
        state.update({"status":"FAILED","stage":stage,"error":traceback.format_exc()})
        write_result(state)
