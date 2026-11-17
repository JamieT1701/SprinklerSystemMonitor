"""B1 native KiCad 10 electrical-connectivity regression tests.

These exercise archived **actual KiCad XML netlist/ERC outputs**. No hardware,
PoE, DS18B20, installed valve or true short-circuit fault was tested.
"""
import json
import sys
import unittest
from pathlib import Path

EDA=Path(__file__).resolve().parents[1]/"CAD"/"electronics"
sys.path.insert(0,str(EDA))
from check_frontend_netlist import check, actual_nets

class KiCadTrueNetlistContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.actual=actual_nets()
        cls.contract=json.loads((EDA/"B1_24V_FIELD_POWER_REVIEW_net_contract.json").read_text())

    def test_exported_real_netlist_is_complete(self):
        check()

    def test_efuse_all_11_pins_defined(self):
        self.assertEqual(set(self.contract["components"]["U2"]["pins"]),
                         set(map(str,range(1,12))))

    def test_ti_silicon_pin_order(self):
        pins=self.contract["components"]["U2"]["pins"]
        expected={"1":"IN","2":"UVLO","3":"OVP","4":"SHDN","5":"RTN","6":"GND",
                  "7":"ILIM","8":"dVdT","9":"FLT","10":"OUT","11":"PAD=RTN"}
        self.assertEqual({i:cfg["signal"] for i,cfg in pins.items()},expected)

    def test_rtn_not_short_to_ground(self):
        self.assertIn("U2.5",self.actual["RTN_EFUSE_ISOLATED"])
        self.assertIn("U2.11",self.actual["RTN_EFUSE_ISOLATED"])
        self.assertIn("U2.6",self.actual["GND_LOGIC"])
        self.assertNotEqual(self.actual["GND_LOGIC"],self.actual["RTN_EFUSE_ISOLATED"])

    def test_uvlo_ovp_voltage_network_topology(self):
        self.assertIn("U2.2",self.actual["UVLO_NODE"])
        self.assertIn("R1.1",self.actual["BOOST_24V"])
        self.assertEqual(self.contract["components"]["R1"]["value"],"715k_1pct_UV_TOP")
        self.assertEqual(self.contract["components"]["R2"]["value"],"20k_1pct_UV_MID")
        self.assertEqual(self.contract["components"]["R3"]["value"],"30.1k_1pct_OV_BOTTOM")

    def test_correct_sptd_m12_and_nc(self):
        self.assertIn("P3.1",self.actual["FIELD_PROTECTED_LPLUS"])
        self.assertIn("P3.2",self.actual["SENSOR_I_RETURN"])
        self.assertEqual(self.actual["unconnected-(P3-P3_3_NC-Pad3)"],["P3.3"])
        self.assertEqual(self.actual["unconnected-(P3-P3_4_NC-Pad4)"],["P3.4"])

    def test_nominal_limit_shunt_physical_constraints_unqualified(self):
        self.assertTrue(self.contract["components"]["R4"]["value"].startswith("165k"))
        self.assertTrue(self.contract["components"]["R5"]["value"].startswith("100R"))
        # At even the nominal eFuse current limit the shunt becomes 4.02V,
        # ABOVE the ADC's 3.3V recommended input. Direct connection unsafe.
        self.assertGreater(100*(6.636/165),3.3)
        self.assertTrue(any("ADC" in risk for risk in self.contract["risk_gates"]))

    def test_poE_output_power_unverified(self):
        self.assertTrue(any("PoE" in risk for risk in self.contract["risk_gates"]))
        self.assertIn("J1.1",self.actual["PSE_5V_UNVERIFIED"])

    def test_real_erc_report_exposes_qualification_limit(self):
        report=(EDA/"B1_24V_FIELD_POWER_REVIEW_ERC.rpt").read_text()
        self.assertIn("ERC messages: 0  Errors 0  Warnings 0",report)
        self.assertTrue(any("physical hardware" in s for s in self.contract["risk_gates"]) or
                        any("PoE" in s for s in self.contract["risk_gates"]))

if __name__=="__main__":
    unittest.main()
