# B1 cloud telemetry, alerts and dashboard contract — NOT DEPLOYED

**Source:** simplified Claude selected architecture + Carbon's useful user-facing cold-duration and QA concepts. **State:** interface specification / host-only demonstration. No production backend, external alerts, customer data, site modifications or sender registration.

## Device-to-cloud outbound payload (proposed)

```json
{
  "schema_version": 1,
  "device_id": "SERIAL_FROM_PROVISIONING",
  "seq": 42,
  "firmware_version": "b1-dev",
  "uptime_s": 300,
  "sampled_at_utc": "2026-11-16T00:00:00Z",
  "pressure": {
    "quality": "VALID",
    "raw_current_ma": 9.76,
    "loop_terminal_v": 23.0,
    "loop_supply_v": 24.0,
    "psi": 54.0,
    "range_psig": 150.0,
    "calibration_version": "not-valid-until-real-acceptance"
  },
  "temperature": {
    "quality": "VALID",
    "fahrenheit": 39.5,
    "sensor": "DS18B20"
  },
  "device_health": {
    "eth_link": "up",
    "poe_power": "present",
    "adc_reference_ok": true,
    "reset_reason": "power_on"
  }
}
```

**Critical:** The example PSI/current numbers are calculated examples, **not a fresh reading from a product**. Do not use a user-supplied sensor value as a certified threshold, valve pressure, or proof of normal fire protection.

## Minimum backend state machine (cloud receipt time is authoritative)

1. Ingest only authenticated device payloads with monotonic per-device sequence, replay protection, defined rate limits and HTTPS/TLS; reject unrecognized devices and duplicate/out-of-order events. Record receipt timestamp independently of the ESP clock.
2. **INVALID pressure** or missing/invalid temperature -> `SENSOR_FAULT`, never a guessed pressure or "normal". Expose last **valid** reading separately with its original timestamp and `LAST_KNOWN`.
3. If no accepted fresh report for **>180s** (proposed 60-second reporting) show `STALE`; for **>300s** show `DEVICE_OR_NETWORK_OFFLINE` and independently dispatch an offline alert from the server. These are **design target values**, not delivery guarantees; log actual observations and choose site-configurable policy.
4. A separate external dead-man service should watch the *backend's* scheduled health heartbeat so that backend scheduler outage doesn't silently suppress alerts. Monitoring service and notification provider failures should be surfaced as `MONITORING_DEGRADED`.
5. Site threshold approval state: `UNVERIFIED` until qualified sprinkler professional/owner approval record supplies valve model, approver, date, approved location, low/high bands and cold-duration policy. With UNVERIFIED thresholds the user sees numbers but **never a green NORMAL label** or "predicted trip" claim.
6. With thresholds approved, apply configurable upper/lower pressure bands, hysteresis, persistence, rapid-decay trend only when an adequate history of valid readings exists. Cold warning after *continuous* below-threshold duration and more urgent floor per site policy. Maintenance/snooze never silently disables an offline or unverified-sensor warning.
7. Event states include `PENDING`, `NOTIFIED`, `ACKNOWLEDGED`, `RECOVERED`. ACK stops repeat escalation, does **not** clear the underlying condition. Store condition, state transition, timestamp, operator action and provider receipt.
8. Critical message dispatch target **≤60s P95 after confirmed event** on healthy backend. Track provider delivery separately; SMS and web push can be delayed or blocked. Independent weekly **real receipt** test required before deployment claim.
9. Site MVP: one owner/site, 24h/7d trend, sensor health, history, warnings, acknowledgement, device link, elapsed cold period, data export. Schema may include org/site/device references but multi-tenant access and contractor portal are not approved.
10. Data access: least privilege, multi-factor admin, tenant/site authorization, no secret keys in browser firmware or telemetry logs; retention policies/notification opt-in.

## Threat cases and acceptance

- Device offline but cloud operational -> independent cloud notifier emits outage, not stale green.
- Backend down -> third-party monitor signals `MONITORING SERVICE DOWN`.
- Malicious/replayed payload -> reject by device signature and sequence; preserve audit.
- Device clock fast/unsynced -> receipt timestamp prevails; record discrepancy.
- Cloud receives `pressure_quality=INVALID` with a plausible `psi` -> invalidate/ignore numeric measurement.
- User hasn't had site thresholds professionally approved -> display `THRESHOLDS UNVERIFIED` even if pressure ~54 psi.
- SMS contact opted out / delivery failure -> alert other approved channel and show notification degraded; no hidden success claim.

## Status

There is **no** hosted B1 service or alert delivery. Testing in this branch is local deterministic model-only. The original R6 remains separately governed.
