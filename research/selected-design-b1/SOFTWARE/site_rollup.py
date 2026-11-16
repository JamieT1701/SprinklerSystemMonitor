"""Host-only B1 multi-system status aggregation, not a deployed safety signal.

Only the site configuration determines expected device identifiers.
A healthy common compressor does NOT imply that every dry-system valve is healthy.
"""
from dataclasses import dataclass
from typing import Mapping, Sequence
from alert_engine import View

DANGER = frozenset({"PRESSURE_CRITICAL"})
WARNING = frozenset({"PRESSURE_WARNING", "SUSTAINED_COLD_WARNING",
                     "COLD_PENDING_PERSISTENCE"})
FAILED = frozenset({"OFFLINE", "STALE", "SENSOR_FAULT", "TIME_INVALID"})

@dataclass(frozen=True)
class SiteRollup:
    state: str
    expected_ids: tuple[str, ...]
    missing_ids: tuple[str, ...]
    critical_ids: tuple[str, ...]
    warning_ids: tuple[str, ...]
    degraded_ids: tuple[str, ...]
    unverified_ids: tuple[str, ...]
    unexpected_ids: tuple[str, ...]

def rollup(expected_device_ids: Sequence[str],
           views: Mapping[str, View]) -> SiteRollup:
    """Never report site NORMAL unless every required device is NORMAL."""
    expected = tuple(expected_device_ids)
    if not expected or any(not i or not i.strip() for i in expected):
        raise ValueError("Site must specify at least one nonblank device ID")
    if len(set(expected)) != len(expected):
        raise ValueError("Expected device IDs must be unique")
    expected_set = set(expected)
    unknown = tuple(sorted(set(views) - expected_set))
    missing = tuple(i for i in expected if i not in views)
    critical = tuple(i for i in expected if i in views and
                     views[i].status in DANGER)
    warning = tuple(i for i in expected if i in views and
                    views[i].status in WARNING)
    degraded = tuple(i for i in expected if i in views and
                     views[i].status in FAILED)
    unverified = tuple(i for i in expected if i in views and
                       views[i].status not in (DANGER | WARNING | FAILED | {"NORMAL"}))
    if critical:
        state = "CRITICAL"
    elif missing or degraded or unknown:
        state = "DEGRADED"
    elif warning:
        state = "WARNING"
    elif unverified:
        state = "UNVERIFIED"
    else:
        state = "NORMAL"
    return SiteRollup(state,expected,missing,critical,warning,
                      degraded,unverified,unknown)
