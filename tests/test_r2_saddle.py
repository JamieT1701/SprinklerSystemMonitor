"""Independent checks for the no-drill R2 PETG wire-saddle fit coupon.
Geometric printability checks only, NOT an installed fit or safety acceptance.
"""
import collections
import hashlib
import json
import pathlib
import struct
import unittest

ROOT=pathlib.Path(__file__).resolve().parents[1]
DIR=ROOT/"hardware/mount-accessories"
STL=DIR/"R2_P4_10mm_Wire_Tie_Saddle_FIT_TEST_ONLY.stl"
RECEIPT=STL.with_suffix(".json")

class TestR2Saddle(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=STL.read_bytes()
        cls.receipt=json.loads(RECEIPT.read_text(encoding="utf8"))
        cls.count=struct.unpack_from("<I",cls.data,80)[0]
    def test_binary_stl_record_and_sha256(self):
        self.assertEqual(len(self.data),84+50*self.count)
        self.assertEqual(self.count,75472)
        self.assertTrue(self.data.startswith(b"DEVICE LAB R2"))
        self.assertEqual(hashlib.sha256(self.data).hexdigest(),self.receipt["sha256"])
    def test_mesh_bounds_xyz_and_triangle_finiteness(self):
        mn=[float("inf")]*3;mx=[float("-inf")]*3
        for raw in struct.iter_unpack("<12fH",self.data[84:]):
            normal=raw[:3]
            self.assertAlmostEqual(sum(n*n for n in normal),1.0,places=4)
            for j in (3,6,9):
                for k in range(3):
                    v=raw[j+k];mn[k]=min(mn[k],v);mx[k]=max(mx[k],v)
        self.assertEqual([round(mx[k]-mn[k],4) for k in range(3)],[26,16,8])
        self.assertEqual([round(x,4) for x in mn],[0,0,0])
    def test_manifold_edges_independently(self):
        edges=collections.Counter()
        for raw in struct.iter_unpack("<12fH",self.data[84:]):
            vv=[]
            for i in (3,6,9):
                vv.append(tuple(round(raw[i+j]*5) for j in range(3)))
            for a,b in ((0,1),(1,2),(2,0)):
                edges[tuple(sorted((vv[a],vv[b])))]+=1
        self.assertGreater(len(edges),100)
        errors=sum(1 for n in edges.values() if n!=2)
        self.assertEqual(errors,0)
    def test_fixture_scope_and_hole_spacing(self):
        self.assertEqual(self.receipt["hole_center_pitch_mm"],10)
        self.assertEqual(self.receipt["through_hole_diameter_nominal_mm"],3.6)
        self.assertEqual(self.receipt["size_mm"],[26,16,8])
        self.assertIn("physical fit not verified",self.receipt["validation"])
        self.assertIn("NOT for mounting boards",self.receipt["use"])

if __name__=="__main__":
    unittest.main()
