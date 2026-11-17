"""Synthetic aggregation tests. No facility air-pressure state inferred or measured."""
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1] / "SOFTWARE"))
from site_rollup import rollup
from alert_engine import View

def v(s):
    return View(s,tuple(),50.0,45.0,1.0)

class MultiSystemTests(unittest.TestCase):
    def test_all_fresh_normal(self):
        x=rollup(["a","b","c"],{"a":v("NORMAL"),"b":v("NORMAL"),"c":v("NORMAL")})
        self.assertEqual(x.state,"NORMAL")

    def test_missing_valve_device_is_not_normal(self):
        x=rollup(["a","b","c"],{"a":v("NORMAL"),"b":v("NORMAL")})
        self.assertEqual(x.state,"DEGRADED")
        self.assertEqual(x.missing_ids,("c",))

    def test_one_valve_offline_overrides_healthy_common_air(self):
        x=rollup(["a","b","c"],{"a":v("NORMAL"),"b":v("OFFLINE"),"c":v("NORMAL")})
        self.assertEqual(x.state,"DEGRADED")
        self.assertEqual(x.degraded_ids,("b",))

    def test_one_valve_fault_never_normal(self):
        x=rollup(["a","b","c"],{"a":v("NORMAL"),"b":v("SENSOR_FAULT"),"c":v("NORMAL")})
        self.assertEqual(x.state,"DEGRADED")

    def test_critical_wins_and_preserves_device_id(self):
        x=rollup(["a","b","c"],{"a":v("STALE"),"b":v("PRESSURE_CRITICAL"),"c":v("NORMAL")})
        self.assertEqual(x.state,"CRITICAL")
        self.assertEqual(x.critical_ids,("b",))
        self.assertEqual(x.degraded_ids,("a",))

    def test_unverified_not_normal(self):
        x=rollup(["a","b"],{"a":v("NORMAL"),"b":v("UNVERIFIED")})
        self.assertEqual(x.state,"UNVERIFIED")
        self.assertEqual(x.unverified_ids,("b",))

    def test_warning_with_unverified(self):
        x=rollup(["a","b"],{"a":v("PRESSURE_WARNING"),"b":v("UNVERIFIED")})
        self.assertEqual(x.state,"WARNING")
        self.assertEqual(x.unverified_ids,("b",))

    def test_unknown_extra_device_is_not_silent(self):
        x=rollup(["a"],{"a":v("NORMAL"),"rogue":v("NORMAL")})
        self.assertEqual(x.state,"DEGRADED")
        self.assertEqual(x.unexpected_ids,("rogue",))

    def test_no_assumed_valve_count(self):
        x=rollup(["only-approved-device"],{"only-approved-device":v("NORMAL")})
        self.assertEqual(x.state,"NORMAL")

    def test_no_expected_devices_rejected(self):
        with self.assertRaises(ValueError): rollup([],{})
        with self.assertRaises(ValueError): rollup([""],{})

    def test_duplicates_rejected(self):
        with self.assertRaises(ValueError): rollup(["same","same"],{})

if __name__=="__main__":
    unittest.main(verbosity=2)
