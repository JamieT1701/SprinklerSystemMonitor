"""No external message dispatch; synthetic server-side anti-stale/fault tests only."""
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"SOFTWARE"))
from alert_engine import Reading, Thresholds, view

def policy():
    # Synthetic test-only values, NOT site-safe thresholds or valve trip hints!
    return Thresholds(10, 20, 80, 90, 40, 1800, True, "SYNTHETIC-TEST-ONLY")

def reading(ts=1000,p=50,t=50,pq="VALID",tq="VALID"):
    return Reading(ts,p,t,pq,tq)

class CloudViewTests(unittest.TestCase):
    def test_no_sample_offline(self):
        got=view(1100,None,policy())
        self.assertEqual(got.status,"OFFLINE")
        self.assertIsNone(got.current_pressure_psig)

    def test_silence_offline_from_server(self):
        got=view(1400,reading(),policy())
        self.assertEqual(got.status,"OFFLINE")
        self.assertIsNone(got.current_temp_f)

    def test_stale_never_normal(self):
        got=view(1200,reading(),policy())
        self.assertEqual(got.status,"STALE")
        self.assertEqual(got.current_pressure_psig,None)

    def test_recent_value_with_no_approval_never_normal(self):
        got=view(1050,reading())
        self.assertEqual(got.status,"UNVERIFIED")
        self.assertIn("THRESHOLDS_UNVERIFIED",got.events)

    def test_approval_without_reference_rejected(self):
        p=Thresholds(10,20,80,90,40,1800,True,"")
        self.assertEqual(view(1050,reading(),p).status,"UNVERIFIED")

    def test_invalid_threshold_order_rejected(self):
        p=Thresholds(30,20,80,90,40,1800,True,"TEST")
        self.assertEqual(view(1050,reading(),p).status,"UNVERIFIED")

    def test_bad_pressure_quality_cannot_be_normal(self):
        got=view(1050,reading(p=50,pq="INVALID"),policy())
        self.assertEqual(got.status,"SENSOR_FAULT")
        self.assertIsNone(got.current_pressure_psig)

    def test_bad_temperature_quality_cannot_be_normal(self):
        got=view(1050,reading(t=50,tq="INVALID"),policy())
        self.assertEqual(got.status,"SENSOR_FAULT")
        self.assertIsNone(got.current_temp_f)

    def test_approved_and_nominal(self):
        got=view(1050,reading(),policy())
        self.assertEqual(got.status,"NORMAL")

    def test_critical_pressure(self):
        got=view(1050,reading(p=9.9),policy())
        self.assertEqual(got.status,"PRESSURE_CRITICAL")

    def test_high_warning(self):
        got=view(1050,reading(p=85),policy())
        self.assertEqual(got.status,"PRESSURE_WARNING")

    def test_cold_persistence_not_yet_met(self):
        got=view(1050,reading(t=35),policy(),cold_elapsed_s=1799)
        self.assertEqual(got.status,"COLD_PENDING_PERSISTENCE")

    def test_cold_persistence_met(self):
        got=view(1050,reading(t=35),policy(),cold_elapsed_s=1800)
        self.assertEqual(got.status,"SUSTAINED_COLD_WARNING")

    def test_simultaneous_critical_and_cold(self):
        got=view(1050,reading(p=5,t=35),policy(),cold_elapsed_s=1800)
        self.assertEqual(got.status,"PRESSURE_CRITICAL")
        self.assertIn("SUSTAINED_COLD_WARNING",got.events)

    def test_receipt_time_from_future_not_normal(self):
        got=view(1000,reading(ts=1100),policy())
        self.assertEqual(got.status,"TIME_INVALID")

    def test_invalid_age_policy_raises(self):
        with self.assertRaises(ValueError):
            view(1100,reading(),policy(),stale_after_s=300,offline_after_s=180)

if __name__=="__main__":
    unittest.main(verbosity=2)
