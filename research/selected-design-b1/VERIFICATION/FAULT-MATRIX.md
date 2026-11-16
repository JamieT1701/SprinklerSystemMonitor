# B1 fault-injection and release acceptance matrix

**No physical tests run.** The tests below apply to a *future isolated/current-limited bench DUT* with no connection to a real sprinkler system. No intentional shorts on live facility systems or PoE network.

| Test | Bench method after independent schematic review | Expected safety/telemetry outcome | Current status |
|---|---|---|---|
| Current 4, 12, 20mA | Calibrated loop source + reference DMM | 0 / midpoint / full-scale on configured transmitter range within error budget | Host math only |
| Current 3.5, 3.7, 20.8, 21.5mA | Source fault-mode simulation | Fault / under-range / over-range / high fault; never NORMAL | Host classifier tests pass |
| Open sensor return or source wire | Controlled open test | PRESSURE UNKNOWN; probable open when high L+ and no return | Host classifier tests pass |
| L+ shorted to GND | Current-limited fault injection + thermal camera | Supply survives continuously; probable grounded fault and invalid PSI | **No hardware design/test; BLOCKER** |
| L+ shorted to return | Controlled current-limited test | Hardware protection prevents unsafe dissipation/brownout; state cannot be falsely valid | **No hardware design/test; BLOCKER** |
| Reversed 2-wire transmitter | Polarity test with compatible transmitter | No injury; invalid/unknown until corrected | Not designed |
| Return pin +24V miswire | External limited injection on unpowered and powered board | ADC pins/rail survive and no backfeed/destruction | **No hardware design/test; BLOCKER** |
| Wet/corroded cable leakage | Switched resistor to shield/earth | Diagnostic should classify UNKNOWN/leak only if actual measured channels can distinguish | Not designed |
| EMI and field surge | Ground-referenced bench transients then qualified pre-compliance lab | No loss of measurement integrity or permanent damage at target rating | Not designed |
| ADS1115 disconnected/hung | Remove I2C ACK / hold bus low | SENSOR_FAULT; bounded recovery/reset; cloud updated | Only host flags |
| ADC reference fails | Replace reference with out-of-band voltage | ADC_FAULT; stale/unknown, not zero or normal | Host classifier tests pass |
| DS18B20 missing, CRC bad, 85°C | Disconnect cable, scripted response / simulator | TEMP_FAULT or INVALID; not fake cold/normal | Not yet coded for B1 |
| PoE cable unplugged | Safe controlled power-off after prototype assembly | Device stops; independent cloud dead-man alerts within approved window | Not tested |
| Network router down | Isolate network in bench lab | Offline alert independent of device and facility | Not tested |
| Backend scheduler dead | Stop dev scheduler in test env | External monitor-of-monitor alerts | Not implemented |
| Web Push/SMS delayed/rejected | Provider sandbox with consent | Accurate delivery logs, alternate channel, retries/escalation | Not implemented |
| OTA invalid signature/rollback | Staged dev unit only | Reject bad image; valid previous image remains bootable | Not implemented |
| Cold room/condensation | Isolated thermal chamber | Measured sensor accuracy; no false NORMAL; safe operating electronics | Not tested |
| Physical gauge calibration | NIST traceable or otherwise qualified pressure source + certified reference | 0/25/50/75/100/150 as rated; error/error drift recorded | Not tested |
| PCB assembly and electrical QA | Fixture, serial and bench burn-in | Documented per-unit pass, yield and serviceability | Not designed |

## Acceptance gates

**G1:** Site/pressure-tap and threshold approval; **G2:** reviewed complete schematic and 24V hardware current-limiter, ADC pin protections, power and thermal math; **G3:** KiCad ERC/DRC and independently reviewed fabrication data; **G4:** isolated bench electrical/pneumatic tests; **G5:** source-controlled firmware/host tests, realistic offline and actual notification delivery proof; **G6:** qualified shadow pilot + regulator/insurer classification. No stage may claim approval from previous AI concept scores alone.

Host-side regression on Arthur:
```sh
python3 -m unittest discover -s research/selected-design-b1/VERIFICATION -p 'test_*.py' -v
```

## Multi-device site health tests (synthetic only)

Add acceptance for explicit configured expected devices and alert identity: one missing device => site DEGRADED, one offline/faulted => site DEGRADED, any critical pressure alert => site CRITICAL with specific device ID, one UNVERIFIED => never site NORMAL, additional unrecognized device => configuration warning, and only a complete verified set may report site NORMAL. This behavior is host-tested by `VERIFICATION/test_site_rollup.py`, **not** demonstrated on multiple physical sprinklers.


### Revision B external port test matrix

P1 RJ45: PoE startup, full controller/loop power, link continuity, loss-of-link dead-man, grounding/shield/EMC, sealed mating cable and dust cap. P2 M8: correct 3-wire DS18B20 mapping, CRC, invalid/open, wet/short and power-off injection. P3 M12: true two-wire 4-20mA cable continuity, two NC contacts, limited 24 V short/reversal/overcurrent, failed sender and sensor absence. Physical: gasket/cap/connector wall clearance, 120 mm front-flange spacing, cable bend and strain, sealed assembly IP54 splash/dust proof. AUX: no hole, powered cable, or live output. **All physical items currently untested.**
