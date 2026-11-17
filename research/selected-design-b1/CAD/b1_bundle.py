#!/usr/bin/env python3
"""Reproducible, privacy-safe source + native CAD + render handoff ZIP.
All architecture content is public-repo safe, no private sprinkler inspections.
"""
import hashlib,json,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
CAD=ROOT/"CAD"
OUT=CAD/"outputs"
ZIP=OUT/"B1_FULL_DESIGN_CONCEPT_2026-11-16.zip"
PREFIX="B1_Engineering_Concept_2026-11-16/"
SOURCE_EXT={".md",".json",".csv",".py"}
RENDER_NAMES={
 "01_b1_closed_product.png","02_b1_service_open.png","03_b1_exploded.png",
 "04_b1_pcb_component_top.png","05_b1_field_ports.png","06_b1_wall_install_view.png",
 "07_b1_kicad_board_top.png","08_b1_dashboard_desktop.png",
 "09_b1_dashboard_mobile.png","B1_design_review_contact_sheet.png"}
BINARY_NAMES={
 "B1_assembled.FCStd","B1_exploded.FCStd","B1_complete_reference_assembly.step",
 "B1_exploded_reference_assembly.step","B1_visual_assembly.blend",
 "B1_concept_interactive.glb","B1_lid_off.glb","B1_exploded_assembly.glb","B1_electronics_only.glb","B1_viewer_variants.json","B1_dashboard_demo.html",
 "B1_part_manifest.json","B1_CAD_README.txt","B1_placement_DRC_UNQUALIFIED.txt"}
files=[]
for f in ROOT.rglob("*"):
 if not f.is_file():
  continue
 rel=f.relative_to(ROOT)
 parts=rel.parts
 if "__pycache__" in parts or "node_modules" in parts or f.name.endswith((".pyc",".log",".zip",".blend1")):
  continue
 if f.name=="b1_blender_preview.py" or f.name.startswith("PREVIEW_"):
  continue
 if "outputs" not in parts:
  if (f.suffix in SOURCE_EXT or f.suffix in {".kicad_pcb",".kicad_sch",".kicad_sym",".kicad_pro",".xml",".rpt"} or f.name=="sym-lib-table"):
   files.append((f,rel))
 elif "meshes" in parts and f.suffix==".stl":
  files.append((f,rel))
 elif "renders" in parts and f.name in RENDER_NAMES:
  files.append((f,rel))
 elif "drawings" in parts and f.suffix==".svg" and f.name.startswith("B1_"):
  files.append((f,rel))
 elif f.name in BINARY_NAMES:
  files.append((f,rel))
files.sort(key=lambda v:str(v[1]))
assert len(files)>130, len(files)
manifest={"package":"B1 full source, visual concept, native CAD and source-limited design records",
          "date":"2026-11-16",
          "scope":"Source-only design. No electrical schematic, routed netlist, built PCB or physical validation",
          "files":{}}
for f,rel in files:
 blob=f.read_bytes()
 manifest["files"][str(rel)]={"bytes":len(blob),"sha256":hashlib.sha256(blob).hexdigest()}
names=[str(rel) for f,rel in files]
required=["CAD/outputs/B1_assembled.FCStd",
 "CAD/outputs/B1_visual_assembly.blend",
 "CAD/outputs/B1_concept_interactive.glb",
 "CAD/outputs/B1_lid_off.glb",
 "CAD/outputs/B1_exploded_assembly.glb",
 "CAD/outputs/B1_electronics_only.glb",
 "CAD/outputs/B1_complete_reference_assembly.step",
 "CAD/electronics/B1_placement_NOT_ROUTED.kicad_pcb",
 "CAD/electronics/B1_24V_FIELD_POWER_REVIEW.kicad_sch",
 "CAD/electronics/B1_Bench.kicad_sym",
 "CAD/electronics/B1_24V_FIELD_POWER_REVIEW_NETLIST.xml",
 "CAD/electronics/B1_24V_FIELD_POWER_REVIEW_ERC.rpt",
 "CAD/outputs/drawings/B1_24V_FIELD_POWER_REVIEW.svg",
 "CAD/outputs/B1_dashboard_demo.html",
 "CAD/outputs/renders/B1_design_review_contact_sheet.png",
 "CAD/outputs/B1_placement_DRC_UNQUALIFIED.txt"]
assert all(p in names for p in required)
doc=json.dumps(manifest,ensure_ascii=False,indent=2).encode("utf-8")+b"\n"
def write(z,name,data):
 info=zipfile.ZipInfo(PREFIX+str(name))
 info.date_time=(2026,11,16,12,0,0)
 info.compress_type=zipfile.ZIP_DEFLATED
 info.external_attr=0o644<<16
 z.writestr(info,data,compress_type=zipfile.ZIP_DEFLATED,compresslevel=6)
with zipfile.ZipFile(ZIP,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=6,allowZip64=True) as archive:
 write(archive,"B1_INTEGRITY_MANIFEST.json",doc)
 for f,rel in files:
  write(archive,rel,f.read_bytes())
with zipfile.ZipFile(ZIP) as archive:
 assert archive.testzip() is None
 assert len(archive.namelist())==len(files)+1
 for f,rel in files:
  p=PREFIX+str(rel)
  assert hashlib.sha256(archive.read(p)).hexdigest()==manifest["files"][str(rel)]["sha256"]
checksum=hashlib.sha256(ZIP.read_bytes()).hexdigest()
(OUT/"B1_FULL_DESIGN_CONCEPT_SHA256.txt").write_text(checksum+"  "+ZIP.name+"\n")
print("B1_BUNDLE_OK","files",len(files),"bytes",ZIP.stat().st_size,"sha256",checksum)
print("B1_BUNDLE_PATH",ZIP)
