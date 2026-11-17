#!/usr/bin/env python3
"""Issue #8: HOST-ONLY simulated heat-request indicator. No heater, GPIO or IO imports."""
from dataclasses import dataclass
from enum import Enum
import math

class State(str, Enum):
    REQUEST = "HEAT_REQUEST"
    IDLE = "IDLE"
    FAULT = "SENSOR_FAULT"
    DISABLED = "MANUAL_DISABLED"

@dataclass(frozen=True)
class Result:
    state: State
    led_on: bool
    reason: str
    feedback_fault: bool = False

class MockHeaterDemand:
    """No physical heater switching permitted by this model."""
    def __init__(self, request_at=48.0, release_at=52.0, max_age_seconds=120.0):
        if not request_at < release_at:
            raise ValueError("hysteresis boundaries must be ordered")
        self.request_at = request_at
        self.release_at = release_at
        self.max_age_seconds = max_age_seconds
        self._request = False

    def reset(self):
        self._request = False

    def tick(self, temp_f, sample_age_seconds, sensor_ok=True, manual_disabled=False,
             network_ok=True, mock_feedback=None, ds18b20_startup_sentinel=False):
        # network_ok is intentionally irrelevant: local bench indication is autonomous.
        del network_ok
        if manual_disabled:
            self._request = False
            state, reason = State.DISABLED, "manual_disable"
        elif (not sensor_ok or ds18b20_startup_sentinel or temp_f is None
              or not isinstance(temp_f, (int, float)) or not math.isfinite(temp_f)
              or not -40 <= temp_f <= 125
              or sample_age_seconds is None or not isinstance(sample_age_seconds, (int, float))
              or not math.isfinite(sample_age_seconds)
              or not 0 <= sample_age_seconds <= self.max_age_seconds):
            self._request = False
            state, reason = State.FAULT, "invalid_or_stale_sensor"
        else:
            if temp_f <= self.request_at:
                self._request = True
            elif temp_f >= self.release_at:
                self._request = False
            state = State.REQUEST if self._request else State.IDLE
            reason = "valid_sample"
        led_on = self._request and state == State.REQUEST
        return Result(state, led_on, reason,
                      mock_feedback is not None and bool(mock_feedback) != led_on)
