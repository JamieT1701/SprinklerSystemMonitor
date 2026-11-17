"""Regression verification of actual Fusion-executed R2 assembly archive.
Does not represent physical fit, installed PCB or operational acceptance.
"""
import hashlib
import json
import pathlib
import struct
import unittest
import zipfile

ROOT=pathlib.Path(__file__).resolve().parents[1]
F3D=ROOT/"cad/fusion/DeviceLabR2Detail/R2_PROVISIONAL_Assembly_NATIVE.f3d"
RECEIPT=ROOT/"cad/fusion/DeviceLabR2Detail/native-run-receipt.json"
VIEW=ROOT/"docs/assets/fusion-r2-NATIVE-isometric.png"

class TestFusionR2Native(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result=json.loads(RECEIPT.read_text(encoding="utf-8"))

    def test_archive_sha256_and_size(self):
        b=F3D.read_bytes()
        self.assertEqual(len(b),767278)
        self.assertEqual(hashlib.sha256(b).hexdigest(),
            self.result["fusion_artifact_sha256"])
        self.assertEqual(len(b),self.result["fusion_artifact_bytes"])

    def test_valid_fusion_archive_zip_integrity(self):
        self.assertTrue(zipfile.is_zipfile(F3D))
        with zipfile.ZipFile(F3D) as z:
            names=z.namelist()
            self.assertGreater(len(names),0)
            self.assertIsNone(z.testzip(), "Archive CRC failed")

    def test_receipt_records_actual_native_app_run_and_preserved_P4(self):
        r=self.result
        self.assertEqual(r["status"],"FUSION_NATIVE_EXECUTION_VERIFIED")
        self.assertEqual(r["p4_native_mesh_bodies"],1)
        self.assertEqual(r["top_level_components"],9)
        self.assertTrue(r["p4_source_unchanged"])
        self.assertEqual(r["board_y_gaps_mm"],[8,7])
        self.assertEqual(r["field_3position_terminal_blocks"],2)
        self.assertEqual(r["boardA_header"],"P3-P12")
        p4=ROOT/"hardware/project-plate-p4/Project_Plate_P4_M3_Heatset.stl"
        self.assertEqual(hashlib.sha256(p4.read_bytes()).hexdigest(),r["approved_p4_sha256"])

    def test_native_fusion_viewport_image(self):
        blob=VIEW.read_bytes()
        self.assertEqual(blob[:8],b"\x89PNG\r\n\x1a\n")
        width,height=struct.unpack_from(">II",blob,16)
        self.assertGreaterEqual(width,1000)
        self.assertGreaterEqual(height,500)
        self.assertGreater(len(blob),100000)

    def test_physical_fit_still_not_accepted(self):
        r=self.result
        self.assertEqual(r["physical_fit_verified"],False)
        self.assertEqual(r["mounting_holes_release_approved"],False)
        self.assertGreaterEqual(len(r["remaining_gates"]),5)

if __name__=="__main__":
    unittest.main()
