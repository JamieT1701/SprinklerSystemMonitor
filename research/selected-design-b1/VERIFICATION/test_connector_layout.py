"""Host-only B1 enclosure/connector design contract checks.

NOT real IP certification, drill fixture, ingress test, 802.3af test or electrical fault test.
"""
import json
import unittest
from pathlib import Path

DATA = json.loads((Path(__file__).resolve().parents[1] / "CAD" / "B1_dimensions.json").read_text())

class ConnectorRevisionBTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.enclosure = DATA["enclosure"]
        cls.ports = DATA["ports"]
        cls.byname = {p["name"]: p for p in cls.ports}

    def test_three_external_port_connections(self):
        self.assertEqual(set(self.byname), {"POE_ETH", "TEMP", "LOOP_4_20MA"})
        self.assertEqual(len(self.ports), 3)

    def test_no_sensor_port_is_generic_unkeyed_entry(self):
        self.assertIn("RJ45", self.byname["POE_ETH"]["connector"])
        self.assertIn("M8", self.byname["TEMP"]["connector"])
        self.assertIn("M12", self.byname["LOOP_4_20MA"]["connector"])
        self.assertEqual(len({p["equipment_gender"] for p in self.ports}), 3)

    def test_revised_manufacturer_cutout_candidates(self):
        self.assertAlmostEqual(self.byname["POE_ETH"]["cutout_diameter_mm"], 20.8)
        self.assertAlmostEqual(self.byname["TEMP"]["cutout_diameter_mm"], 12.0)
        self.assertAlmostEqual(self.byname["LOOP_4_20MA"]["cutout_diameter_mm"], 16.0)

    def test_short_wall_overmold_face_spacing(self):
        ports = sorted(self.ports,key=lambda p:p["x_mm"])
        gaps = [ports[i+1]["x_mm"]-ports[i]["x_mm"]-
                (ports[i+1]["face_diameter_mm"]+ports[i]["face_diameter_mm"])/2
                for i in range(len(ports)-1)]
        self.assertGreaterEqual(min(gaps), 5.0)

    def test_enclosure_edge_flange_clearance(self):
        half = self.enclosure["external_width_mm"]/2
        margins = [half-abs(p["x_mm"])-p["face_diameter_mm"]/2 for p in self.ports]
        self.assertGreaterEqual(min(margins), 5.0)

    def test_all_connectors_on_front_short_wall(self):
        self.assertEqual({p["y_mm"] for p in self.ports},{-90})
        self.assertTrue(all(18<=p["z_mm"]<=55 for p in self.ports))

    def test_no_drilled_aux_port_or_live_expansion(self):
        self.assertFalse(DATA["reserved_aux"]["panel_hole_drilled"])
        self.assertIn("none",DATA["reserved_aux"]["electronic_capability"])
        self.assertTrue(all("AUX" not in p["name"] for p in self.ports))

    def test_m12_current_loop_is_not_m8_temperature(self):
        self.assertNotEqual(self.byname["TEMP"]["equipment_gender"],
                            self.byname["LOOP_4_20MA"]["equipment_gender"])
        self.assertNotEqual(self.byname["TEMP"]["cutout_diameter_mm"],
                            self.byname["LOOP_4_20MA"]["cutout_diameter_mm"])

    def test_no_manufacturer_exact_fit_claim(self):
        self.assertTrue(self.enclosure["geometric_surrogate"])
        self.assertTrue(any("illustrative" in s for s in DATA["source_limitations"]))

    def test_remain_single_channel_monitored_pressure(self):
        self.assertEqual(len(DATA["modules"]["adc"]), 3)
        self.assertNotIn("pressure2",DATA["modules"])

if __name__=="__main__":
    unittest.main(verbosity=2)
