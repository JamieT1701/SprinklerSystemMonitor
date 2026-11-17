"""Host-only synthetic classifier tests. NO live sensor/firmware/hardware exercised."""
import math
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "FIRMWARE"))
from loop_classifier import (Sample, Settings, classify, shunt_voltage_v, ideal_ads1115_counts)

class FaultClassTests(unittest.TestCase):
    def assert_invalid(self, state, i, vplus=24.0, supply=24.0, **flags):
        got = classify(Sample(i, vplus, supply, **flags))
        self.assertEqual(got.quality, "INVALID")
        self.assertEqual(got.state, state)
        self.assertIsNone(got.pressure_psig)

    def test_open_terminal_powered(self):
        self.assert_invalid("LOOP_OPEN", 0, 24)

    def test_short_to_ground_possible(self):
        self.assert_invalid("POSSIBLE_SHORT_TO_GROUND", 0.1, 0.2)

    def test_ambiguous_current_and_terminal(self):
        self.assert_invalid("UNKNOWN_WIRING", 0.1, 10)

    def test_external_backfeed(self):
        self.assert_invalid("UNKNOWN_WIRING", 12, 29)

    def test_power_absent(self):
        self.assert_invalid("LOOP_SUPPLY_FAULT", 0, 0, 0)

    def test_low_supply(self):
        self.assert_invalid("LOOP_SUPPLY_FAULT", 4, 14, 16)

    def test_high_supply(self):
        self.assert_invalid("LOOP_SUPPLY_FAULT", 4, 36, 36)

    def test_low_compliance(self):
        self.assert_invalid("LOOP_COMPLIANCE_LOW", 12, 7)

    def test_fault_below_ne43_low(self):
        self.assert_invalid("SENSOR_FAULT_LOW", 3.5)

    def test_underrange(self):
        self.assert_invalid("UNDER_RANGE", 3.7)
        self.assert_invalid("UNDER_RANGE", 3.99)

    def test_overrange(self):
        self.assert_invalid("OVER_RANGE", 20.1)
        self.assert_invalid("OVER_RANGE", 20.8)

    def test_high_fault_not_called_cable_short(self):
        self.assert_invalid("SENSOR_FAULT_HIGH", 21.0)
        self.assert_invalid("SENSOR_FAULT_HIGH", 25.0)

    def test_adc_and_reference_failure(self):
        self.assert_invalid("ADC_FAULT", 12, adc_ok=False)
        self.assert_invalid("ADC_FAULT", 12, reference_ok=False)
        self.assert_invalid("ADC_FAULT", math.nan)

    def test_negative_measurement_not_trusted(self):
        self.assert_invalid("UNKNOWN_WIRING", -0.2)

    def test_normal_loop_boundaries(self):
        for mA, expected in ((4,0), (12,75), (20,150), (9.76,54)):
            with self.subTest(mA=mA):
                got = classify(Sample(mA,24,24))
                self.assertEqual((got.quality,got.state),("VALID","VALID"))
                self.assertAlmostEqual(got.pressure_psig, expected,places=8)
                self.assertNotIn("normal",got.state.lower())

    def test_range_is_configurable_not_approved(self):
        got=classify(Sample(12,24,24),Settings(pressure_range_psig=100.0))
        self.assertEqual(got.pressure_psig,50.0)

    def test_shunt_100ohm_adc_and_overrange_headroom(self):
        for ma, volts,counts in ((4,0.4,3200),(12,1.2,9600),(20,2.0,16000),(26,2.6,20800)):
            with self.subTest(ma=ma):
                self.assertAlmostEqual(shunt_voltage_v(ma),volts)
                self.assertEqual(ideal_ads1115_counts(ma),counts)
        with self.assertRaises(ValueError):
            ideal_ads1115_counts(36.0)

    def test_input_configuration_rejects_bad(self):
        with self.assertRaises(ValueError):
            classify(Sample(12,24,24),Settings(pressure_range_psig=0))

if __name__=="__main__":
    unittest.main(verbosity=2)
