"""Host-only behavioral tests. No GPIO, imports of field firmware, or real heater."""
import unittest
from tools.heater_controller_sim import MockHeaterDemand, State

class TestMockHeaterDemand(unittest.TestCase):
    def setUp(self): self.c = MockHeaterDemand()
    def test_hysteresis(self):
        self.assertEqual([self.c.tick(t, 1).led_on for t in
                          (55, 50, 48, 46, 50, 52, 55)],
                         [False, False, True, True, True, False, False])
    def test_cold_sensor_fault_clears_request(self):
        self.c.tick(46, 0)
        for kw in (dict(sensor_ok=False),dict(sample_age_seconds=121),
                   dict(temp_f=float('nan')),dict(temp_f=185),
                   dict(ds18b20_startup_sentinel=True)):
            args = dict(temp_f=46, sample_age_seconds=0)
            args.update(kw)
            r=self.c.tick(**args)
            self.assertEqual(r.state, State.FAULT)
            self.assertFalse(r.led_on)
            self.c.tick(46,0)
    def test_no_network_dependency(self):
        self.assertTrue(self.c.tick(46, 1, network_ok=False).led_on)
    def test_power_reset_safe(self):
        self.c.tick(46,1)
        self.c.reset()
        self.assertFalse(self.c.tick(None,None).led_on)
        self.assertTrue(self.c.tick(46,1).led_on)
    def test_manual_disable(self):
        self.c.tick(46,1)
        r=self.c.tick(46,1,manual_disabled=True)
        self.assertEqual(r.state,State.DISABLED)
        self.assertFalse(r.led_on)
    def test_mock_welded_on_off_feedback(self):
        self.assertTrue(self.c.tick(55,1,mock_feedback=True).feedback_fault)
        self.assertTrue(self.c.tick(46,1,mock_feedback=False).feedback_fault)
        self.assertFalse(self.c.tick(46,1,mock_feedback=True).feedback_fault)
    def test_invalid_config(self):
        with self.assertRaises(ValueError): MockHeaterDemand(52,48)
    def test_boundary(self):
        self.assertFalse(self.c.tick(52,1).led_on)
        self.assertTrue(self.c.tick(48,1).led_on)
        self.assertFalse(self.c.tick(52,1).led_on)
    def test_stale_and_disconnect(self):
        self.c.tick(46,1)
        self.assertFalse(self.c.tick(46,999).led_on)
        self.assertFalse(self.c.tick(None,0,sensor_ok=False).led_on)

if __name__ == '__main__': unittest.main()
