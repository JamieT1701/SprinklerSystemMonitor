"""Tests for non-deployed V6 pressure supply diagnostic hypothesis.

Confirms expected numerical behavior for the documented pressure-divider wiring
and Walfront 150 PSI nominal 0.5-4.5 V transfer. These are NOT evidence that the
vendor guarantees ratiometric behavior; pressure outputs remain uncalibrated.
"""
import math
from pathlib import Path
import unittest

RATIO = 14.7 / 24.7
SUPPLY_OBSERVED_V = 4.751
FULL_SCALE_PSI = 150.0


def psi_nominal_5v(sensor_signal_v):
    return (sensor_signal_v - 0.5) * (FULL_SCALE_PSI / 4.0)


def psi_if_ratiometric(sensor_signal_v, actual_supply_v):
    return (sensor_signal_v / actual_supply_v - 0.1) * (FULL_SCALE_PSI / 0.8)


class PressureSupplyStudyTest(unittest.TestCase):
    def test_field_signal_matches_adc_divider(self):
        self.assertAlmostEqual(1.802 * RATIO, 1.07244534, places=6)

    def test_field_supply_hypothesis(self):
        self.assertAlmostEqual(psi_nominal_5v(1.802), 48.825, places=3)
        self.assertAlmostEqual(
            psi_if_ratiometric(1.802, SUPPLY_OBSERVED_V), 52.366607, places=4
        )

    def test_ratiometric_endpoints_at_nominal_supply(self):
        for psi, sensor_v in [(0, 0.5), (75, 2.5), (150, 4.5)]:
            with self.subTest(psi=psi):
                self.assertAlmostEqual(psi_nominal_5v(sensor_v), psi, places=7)
                self.assertAlmostEqual(
                    psi_if_ratiometric(sensor_v, 5.0), psi, places=7
                )

    def test_supply_scaled_endpoints_are_hypothesis_only(self):
        for psi, fraction in [(0, 0.1), (75, 0.5), (150, 0.9)]:
            with self.subTest(psi=psi):
                self.assertAlmostEqual(
                    psi_if_ratiometric(fraction * SUPPLY_OBSERVED_V, SUPPLY_OBSERVED_V),
                    psi,
                    places=7,
                )

    def test_source_marks_study_as_provisional_and_alerts_disabled(self):
        source_path = (
            Path(__file__).resolve().parents[1]
            / "firmware"
            / "2026"
            / "pressure_diagnostics_supply_study"
            / "pressure_diagnostics_supply_study.ino"
        )
        source = source_path.read_text(encoding="utf-8")
        self.assertIn("PRESSURE_SUPPLY_LAST_MANUALLY_MEASURED_V = 4.751f", source)
        self.assertIn("pressure_psi_if_ratiometric_provisional", source)
        self.assertIn("pressure_supply_measurement_live=no", source)
        self.assertIn("pressure_supply_ratiometric_model=UNVERIFIED", source)
        self.assertIn("pressure_notifications=NOT_CONFIGURED", source)
        self.assertIn("freeze_notifications=NOT_CONFIGURED", source)


if __name__ == "__main__":
    unittest.main()
