"""Host-only B1 cloud/UI state evaluator. NO dispatchers, credentials or live alerts.

Intentionally never invents approved pressure bands or temperature thresholds.
Production needs storage, authorization, sequential event state and delivery tests.
"""
from dataclasses import dataclass
from math import isfinite

@dataclass(frozen=True)
class Thresholds:
    pressure_critical_low: float | None = None
    pressure_warn_low: float | None = None
    pressure_warn_high: float | None = None
    pressure_critical_high: float | None = None
    cold_warning_f: float | None = None
    cold_persistence_s: int | None = None
    approved: bool = False
    approval_reference: str = ""

    def accepted(self) -> bool:
        x = (self.pressure_critical_low,self.pressure_warn_low,
             self.pressure_warn_high,self.pressure_critical_high,
             self.cold_warning_f)
        return (self.approved and bool(self.approval_reference.strip())
                and all(v is not None and isfinite(v) for v in x)
                and self.pressure_critical_low < self.pressure_warn_low
                < self.pressure_warn_high < self.pressure_critical_high
                and self.cold_persistence_s is not None
                and self.cold_persistence_s >= 0)

@dataclass(frozen=True)
class Reading:
    received_at_s: float
    pressure_psig: float | None
    temp_f: float | None
    pressure_quality: str
    temp_quality: str

@dataclass(frozen=True)
class View:
    status: str
    events: tuple[str, ...]
    current_pressure_psig: float | None
    current_temp_f: float | None
    age_s: float | None

def view(now_s: float, sample: Reading | None, policy: Thresholds=Thresholds(),
         cold_elapsed_s: float=0, stale_after_s: float=180,
         offline_after_s: float=300) -> View:
    if not (isfinite(now_s) and 0<stale_after_s<offline_after_s):
        raise ValueError("Invalid wall clock or age policy")
    if sample is None:
        return View("OFFLINE",("NO_ACCEPTED_TELEMETRY",),None,None,None)
    age=now_s-sample.received_at_s
    if not isfinite(age) or age < -2:
        return View("TIME_INVALID",("SERVER_RECEIPT_TIME_INVALID",),None,None,None)
    if age > offline_after_s:
        return View("OFFLINE",("INDEPENDENT_DEAD_MAN_REQUIRED",),None,None,age)
    if age > stale_after_s:
        return View("STALE",("LAST_KNOWN_VALUES_ARE_NOT_CURRENT",),None,None,age)
    p=sample.pressure_psig if (sample.pressure_quality=="VALID"
                              and sample.pressure_psig is not None
                              and isfinite(sample.pressure_psig)) else None
    t=sample.temp_f if (sample.temp_quality=="VALID"
                        and sample.temp_f is not None
                        and isfinite(sample.temp_f)) else None
    problems=[]
    if p is None:
        problems.append("PRESSURE_SENSOR_FAULT")
    if t is None:
        problems.append("TEMP_SENSOR_FAULT")
    if not policy.accepted():
        problems.append("THRESHOLDS_UNVERIFIED")
    if problems:
        return View("SENSOR_FAULT" if p is None or t is None else "UNVERIFIED",
                    tuple(problems),p,t,age)
    # A fault in any channel cannot be covered by a green overall status.
    events=[]
    if p <= policy.pressure_critical_low or p >= policy.pressure_critical_high:
        events.append("PRESSURE_CRITICAL")
    elif p <= policy.pressure_warn_low or p >= policy.pressure_warn_high:
        events.append("PRESSURE_WARNING")
    if t <= policy.cold_warning_f:
        if isfinite(cold_elapsed_s) and cold_elapsed_s >= policy.cold_persistence_s:
            events.append("SUSTAINED_COLD_WARNING")
        else:
            events.append("COLD_PENDING_PERSISTENCE")
    if events:
        priority=("PRESSURE_CRITICAL","PRESSURE_WARNING",
                  "SUSTAINED_COLD_WARNING","COLD_PENDING_PERSISTENCE")
        state=next(e for e in priority if e in events)
        return View(state,tuple(events),p,t,age)
    return View("NORMAL",tuple(),p,t,age)
