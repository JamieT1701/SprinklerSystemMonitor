"""Tests of exact candidate source pin roles and conservative pressure-quality math.

No hardware, gauge, ADC, actual field cables, PoE or life-safety system tested.
"""
import math
import sys
import unittest
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"FIRMWARE"))
from loop_classifier import Sample, ideal_ads1115_counts, shunt_voltage_v
from sensor_profiles import (
    SPTD25_0100, LPPT25_PINOUT, sptd25_bench_settings, classify_sptd25,
    nominal_efuse_limit_ma, minimum_required_loop_source_v,
    pressure_from_nominal_current, nominal_transmitter_uncertainty_psig
)

class SPTD25CandidateTests(unittest.TestCase):
    def sample(self,ma, terminal_v=24.0, supply_v=24.0):
        return Sample(ma,terminal_v,supply_v)

    def test_mpn_and_nominal_range(self):
        self.assertEqual(SPTD25_0100.mpn,"SPTD25-20-0100H")
        self.assertEqual(SPTD25_0100.full_scale_psig,100)
        self.assertEqual(sptd25_bench_settings().transmitter_min_v,8.5)

    def test_pressure_pinout_manufacturer_verified(self):
        self.assertEqual(SPTD25_0100.supply_contact,1)
        self.assertEqual(SPTD25_0100.current_return_contact,2)
        self.assertEqual(SPTD25_0100.unused_contacts,(3,4))

    def test_low_cost_alternative_is_not_pin_compatible(self):
        self.assertEqual(LPPT25_PINOUT["supply_contact"],1)
        self.assertEqual(LPPT25_PINOUT["ground_contact"],2)
        self.assertEqual(LPPT25_PINOUT["current_return_contact_choices"],(3,4))
        self.assertNotIn(SPTD25_0100.current_return_contact,
                         LPPT25_PINOUT["current_return_contact_choices"])

    def test_nominal_pressure_conversion(self):
        for ma,psi in ((4,0),(8,25),(12,50),(16,75),(20,100)):
            with self.subTest(ma=ma):
                self.assertAlmostEqual(pressure_from_nominal_current(ma),psi)
                x=classify_sptd25(self.sample(ma))
                self.assertEqual(x.quality,"VALID")
                self.assertAlmostEqual(x.pressure_psig,psi)

    def test_sender_overrange_through_25ma_is_not_a_diagnostic_error_code(self):
        for ma in (20.0001,21,21.5,24.9,25):
            with self.subTest(ma=ma):
                x=classify_sptd25(self.sample(ma))
                self.assertEqual((x.quality,x.state),("INVALID","OVER_RANGE"))
                self.assertIsNone(x.pressure_psig)

    def test_beyond_sender_documented_overrange(self):
        for ma in (25.01,26,35):
            with self.subTest(ma=ma):
                x=classify_sptd25(self.sample(ma))
                self.assertEqual(x.state,"SENSOR_FAULT_HIGH")
                self.assertIsNone(x.pressure_psig)

    def test_sender_under_range_3_to_4ma(self):
        for ma in (3,3.2,3.5,3.6,3.9,3.999):
            with self.subTest(ma=ma):
                x=classify_sptd25(self.sample(ma))
                self.assertEqual(x.state,"UNDER_RANGE")
                self.assertIsNone(x.pressure_psig)

    def test_below_three_ma_not_reported_as_pressure(self):
        x=classify_sptd25(self.sample(2.9))
        self.assertEqual(x.state,"SENSOR_FAULT_LOW")
        self.assertIsNone(x.pressure_psig)

    def test_power_fault_and_open_never_valid(self):
        for sample,state in ((self.sample(0,24,24),"LOOP_OPEN"),
                             (self.sample(0,0,0),"LOOP_SUPPLY_FAULT"),
                             (self.sample(12,6,24),"LOOP_COMPLIANCE_LOW")):
            with self.subTest(state=state):
                x=classify_sptd25(sample)
                self.assertEqual(x.state,state)
                self.assertEqual(x.quality,"INVALID")

    def test_shunt_and_adc_at_transmitter_overrange(self):
        self.assertAlmostEqual(shunt_voltage_v(25),2.5)
        self.assertEqual(ideal_ads1115_counts(25),20000)

    def test_ti_efuse_r_ilim_math_is_illustrative(self):
        self.assertAlmostEqual(nominal_efuse_limit_ma(165),40.218181818,places=5)
        with self.assertRaises(ValueError): nominal_efuse_limit_ma(0)
        with self.assertRaises(ValueError): nominal_efuse_limit_ma(math.nan)

    def test_supply_and_shunt_at_datasheet_load_formula(self):
        self.assertAlmostEqual(minimum_required_loop_source_v(),10.65)
        self.assertAlmostEqual(minimum_required_loop_source_v(extra_series_ohm=10,voltage_drop_budget_v=1.0),11.865)
        with self.assertRaises(ValueError): minimum_required_loop_source_v(current_ma=-1)

    def test_24v_nominal_loop_voltage_margin(self):
        budget=minimum_required_loop_source_v(extra_series_ohm=10,voltage_drop_budget_v=1.0)
        self.assertGreater(24.0-budget,12.0)

    def test_individual_sensor_error_not_combined_system_error(self):
        self.assertAlmostEqual(nominal_transmitter_uncertainty_psig(),0.5)

    def test_no_pressure_extrapolation_to_invalid_current(self):
        for ma in (0,3,3.99,20.01,25,26):
            with self.subTest(ma=ma):
                with self.assertRaises(ValueError):
                    pressure_from_nominal_current(ma)

if __name__=="__main__":
    unittest.main(verbosity=2)
