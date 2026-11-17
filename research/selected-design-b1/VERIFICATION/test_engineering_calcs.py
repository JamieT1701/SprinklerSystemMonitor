"""Host-only budget assertions; engineering arithmetic is not hardware acceptance."""
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"HARDWARE"))
from engineering_calcs import make_receipt

class MathChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.x=make_receipt()

    def test_shunt_count(self):
        adc=[v for v in self.x["shunt_cases"] if v["current_mA"]==20][0]
        self.assertEqual(adc["nominal_positive_adc_codes"],16000)
        self.assertEqual(adc["sense_V"],2.0)

    def test_adc_overrange_margin_before_fault(self):
        cases=self.x["shunt_cases"]
        twenty_six=next(x for x in cases if x["current_mA"]==26)
        self.assertLess(twenty_six["sense_V"],3.3)
        self.assertEqual(twenty_six["sense_V"],2.6)

    def test_24v_terminal_voltage_at_270_22k_divider(self):
        self.assertAlmostEqual(self.x["divider_samples_V"]["24"],1.80822,delta=0.00001)
        self.assertLess(self.x["divider_samples_V"]["40"],3.3)

    def test_above_40v_needs_clamp(self):
        self.assertGreater(self.x["divider_samples_V"]["44"],3.3)

    def test_54psi_nominal_scale(self):
        self.assertAlmostEqual(self.x["examples"]["pressure_54psig_adc_V"],0.976,places=4)

    def test_power_range(self):
        self.assertAlmostEqual(self.x["examples"]["required_24V_loop_output_W_at_26mA"],0.624)
        self.assertAlmostEqual(self.x["examples"]["extra_5V_input_A_at_80pct_efficiency"],0.156)

    def test_low_rail_voltage_compliance(self):
        self.assertAlmostEqual(self.x["examples"]["headroom_above_8V_transmitter_requirement_V"],4.5)

    def test_no_fabrication_claim(self):
        self.assertIn("no KiCad",self.x["stage"])
        self.assertGreater(len(self.x["blockers"]),3)

if __name__=="__main__":
    unittest.main(verbosity=2)
