"""Geometry/spec checks for PROVISIONAL R2 mechanical layout.
These tests do not certify printed fits, electrical connections or hardware.
"""
import hashlib
import json
import math
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
LAYOUT = json.loads((ROOT/"cad/fusion/DeviceLabR2Detail/assembly-layout.json").read_text(encoding="utf8"))
NET = json.loads((ROOT/"hardware/two-terminal-design.json").read_text(encoding="utf8"))

class TestR2Geometry(unittest.TestCase):
    def test_approved_P4_unchanged(self):
        f=ROOT/LAYOUT["evidence"]["P4"]
        self.assertEqual(hashlib.sha256(f.read_bytes()).hexdigest(), LAYOUT["evidence"]["sha256"])
    def test_approved_P4_mesh_bounds(self):
        f=ROOT/LAYOUT["evidence"]["P4"]
        minimum=[float("inf")]*3; maximum=[-float("inf")]*3
        count=0
        with f.open("r",encoding="ascii") as fh:
            for raw in fh:
                fields=raw.split()
                if len(fields)==4 and fields[0]=="vertex":
                    count+=1
                    for i in range(3):
                        v=float(fields[i+1])
                        minimum[i]=min(minimum[i],v)
                        maximum[i]=max(maximum[i],v)
        self.assertEqual(count,34160*3)
        for got,want in zip([maximum[i]-minimum[i] for i in range(3)],LAYOUT["P4"]["bbox_xyz"]):
            self.assertLess(abs(got-want),0.003)
    def test_printed_P4_surface_and_floor_relationship(self):
        p=LAYOUT["P4"];s=LAYOUT["mounts"];floor=LAYOUT["enclosure"]["floor_top_z"]
        self.assertEqual(p["feet_bottom_z"],floor)
        self.assertEqual(p["plate_bottom_z"],floor+p["feet_height"])
        self.assertEqual(p["surface_z"],p["plate_bottom_z"]+p["plate_thickness"])
        self.assertEqual(s["support_bottom_z"],p["surface_z"])
        self.assertEqual(s["support_bottom_z"]+s["support_height"],19)
        for board in LAYOUT["boards"]:self.assertEqual(board["z"],19)
    def test_three_boards_footprints_fit_P4_bounding_envelope(self):
        w,h,_=LAYOUT["P4"]["bbox_xyz"]
        for board in LAYOUT["boards"]:
            x0,y0,x1,y1=board["xy"]
            self.assertGreaterEqual(x0,3,board["id"])
            self.assertGreaterEqual(y0,3,board["id"])
            self.assertGreaterEqual(w-x1,3,board["id"])
            self.assertGreaterEqual(h-y1,3,board["id"])
            self.assertGreater(x1,x0)
            self.assertGreater(y1,y0)
        sizes={"A":(70,50),"B":(70,50),"ESP":(72.8,21)}
        for b in LAYOUT["boards"]:
            a=b["xy"]
            self.assertAlmostEqual(a[2]-a[0],sizes[b["id"]][0],places=3)
            self.assertAlmostEqual(a[3]-a[1],sizes[b["id"]][1],places=3)
    def test_rectangles_do_not_overlap(self):
        boards=LAYOUT["boards"]
        for i,a in enumerate(boards):
            for b in boards[i+1:]:
                u,v=a["xy"],b["xy"]
                x_overlap=max(0,min(u[2],v[2])-max(u[0],v[0]))
                y_overlap=max(0,min(u[3],v[3])-max(u[1],v[1]))
                self.assertEqual(x_overlap*y_overlap,0,(a["id"],b["id"]))
        sorted_boards=sorted(boards,key=lambda item:item["xy"][1])
        gaps=[sorted_boards[i+1]["xy"][1]-sorted_boards[i]["xy"][3] for i in range(2)]
        self.assertEqual(gaps,[8,7])
        # These gaps are small, so this is NOT a service-access approval.
    def test_supports_under_intended_boards_not_inside_gaps(self):
        supports=LAYOUT["mounts"]["locations"]
        boards=LAYOUT["boards"]
        self.assertEqual(len(supports),12)
        for i,(x,y) in enumerate(supports):
            # groups of four in A/ESP/B order
            a=boards[i//4]["xy"]
            self.assertTrue(a[0]<x<a[2] and a[1]<y<a[3],(i,x,y))
    def test_enclosure_study_envelope_and_estimated_lid_clearance(self):
        e=LAYOUT["enclosure"]
        mn=e["outer_min_xyz"];mx=e["outer_max_xyz"]
        self.assertAlmostEqual(mx[0]-mn[0],104.4)
        self.assertAlmostEqual(mx[1]-mn[1],151.9)
        self.assertAlmostEqual(mx[2]-mn[2],59)
        self.assertLessEqual(mx[0],105)
        self.assertLessEqual(mx[1],153)
        highest=max(b["z"]+b["thickness"]+b["component_height_est"] for b in LAYOUT["boards"])
        self.assertLess(highest,mx[2])
        self.assertGreater(mx[2]-highest,15)
        # Enclosure height is a STUDY ASSUMPTION. Real usable headroom unknown.
    def test_external_terminal_blocks_exactly_two_three_position(self):
        field=[c for c in NET["field_connections"] if c["type"]=="terminal_block"]
        self.assertEqual(len(field),2)
        terminal=LAYOUT["boardB"]["terminals"]
        self.assertEqual([x["id"] for x in field],["J1","J2"])
        self.assertEqual([x["id"] for x in terminal],["J1","J2"])
        for item,data in zip(terminal,field):
            self.assertEqual(len(item["pins"]),3)
            self.assertEqual(item["pins"],[data["pins"][str(i)] for i in range(1,4)])
        self.assertEqual(len(LAYOUT["external"]),3)
    def test_R6_components_and_nine_internal_wires(self):
        self.assertEqual(LAYOUT["boardA"]["resistors"],
                         {k:v["ohms"] for k,v in NET["resistors"].items() if v["board"]=="A"})
        self.assertEqual(LAYOUT["boardA"]["capacitors_nf"],{"C1":100,"C2":100})
        self.assertEqual(LAYOUT["boardB"]["pullup_R5_ohms"],4700)
        self.assertEqual(LAYOUT["harness"]["ids"],[x["id"] for x in NET["harness"]])
        self.assertEqual(len(LAYOUT["harness"]["ids"]),9)
    def test_harness_groups_partition_all_nine_wires(self):
        h=LAYOUT["harness"]
        grouped=[wire for group in h["route_groups"].values() for wire in group]
        self.assertEqual(sorted(grouped),sorted(h["ids"]))
        self.assertEqual(h["route_groups"]["right_side_B_to_A"],["W07","W08","W09"])
        self.assertEqual(len(h["route_groups"]["short_ESP_to_B"]),4)
        self.assertEqual(len(h["route_groups"]["short_ESP_to_A"]),2)
    def test_versioned_fusion_script_has_corrected_floor_transform(self):
        source=(ROOT/"cad/fusion/DeviceLabR2Detail/DeviceLabR2Detail.py").read_text(encoding="utf8")
        self.assertIn("m.translation=adsk.core.Vector3D.create(0,142.652/10,11.0/10)",source)
        self.assertNotIn("m.translation=adsk.core.Vector3D.create(0,142.652/10,1.1)",source)
        self.assertIn("Right 6mm W07-W09 B-to-A 3-wire corridor",source)
        self.assertIn("if actual!=expected",source)
    def test_explicitly_unaccepted(self):
        self.assertIn("NOT_FABRICATION_READY",LAYOUT["status"])
        self.assertGreaterEqual(len(LAYOUT["validation_gates"]),7)

if __name__=="__main__":
    unittest.main()
