# Independent advisory comparison — frozen evaluation rubric

This rubric applies to Claude and Gemini after raw proposals have been committed, with no prior access to the other's response. The coordinator reviews facts and evidence independently; scores are the coordinator's assessment, not claims of actual hardware validation.

## Non-negotiable gates (not scored as optional extras)

1. The device is supplementary warning/monitoring, never a replacement for code-required sprinkler/fire-alarm supervision.
2. No control of dry-valve, sprinkler compressor, heater or piping by default.
3. A single skilled owner can realistically manufacture, assemble, test, program and service 1/5/25/100 units in a workshop (outside bare PCB fabrication and optionally sensible SMT outsourcing).
4. Pressure thresholds and normal range are installation-specific; ~50 PSI is the owner's example, not a universal safe target.
5. Independently detectable site/device outage, invalid/stale sensor values and actionable low-pressure/low-temp warnings.
6. A responsive web/mobile-friendly management dashboard and practical push and/or SMS notification delivery.
7. Commercial safety, field tapping, FCC/EMC and fire equipment/AHJ claims identified as review gates rather than assumed approvals.
8. No fabricated price/field test/certification/fabrication result presented as verified.
9. No external outreach, spending, hardware modifications or commitments authorized by competition.

A proposal failing a non-negotiable requirement receives a documented blocker regardless of total score.

## 100-point rubric

| Category | Max points | Concrete evidence |
|---|---:|---|
| Reliability / measurement validity / fault handling | 25 | Plausible sensing physics; configurable alerts; broken sensor/power/network/cloud paths explicitly fail visibly; protection and independent outage detection; recovery tests |
| Personal workshop manufacturability | 20 | Part accessibility and package sizes; realistic tools, hand assembly time, jigs, calibration, repairability, process from 1 to 100 units |
| Hardware plus recurring operating economics | 20 | Honest part/MOQ sourcing, labor, yield, assembly, sensor install, SMS/push/cloud, warranty and support; scaling from 1/5/25/100 |
| Technical completeness | 15 | 3 credible architectures; chosen BOM/topology/footprints; firmware and backend specifics; validation/testing sequence; exact remaining measurement requirements |
| Installation / service | 10 | Qualified connection boundary, field cabling, weather/condensation/strain relief, technician setup/replacement and simplicity |
| Compliance / security / commercialization | 10 | Scope-limited marketing, FCC/EMC/fire equipment classification, secure provisioning/updates, data/alerts, service ownership and gates |

**Scoring:** 0 points missing; up to 40% for plausible concept without details; 60–80% for well-supported engineering plan; 90–100% only for independently sourced, concrete, testable design with credible economics. Scale each category within its maximum; explain scores, cite specific lines/sections, identify omissions and unverified assumptions.

## Outcome, not model loyalty

Do not declare a winner based on prose polish, model brand, speculative component cost or longest answer. Prefer designs with measurable validation, simpler workshop processes and realistic installation economics. Document where advisors independently agree and where they differ. Present owner with (a) the top recommended architecture, (b) a synthesis if combining ideas improves outcome, (c) safety/regulatory blockers and (d) one prioritized interview question.

**No scoring before both independent raw submissions are committed.** If Gemini is blocked, leave the comparison PENDING and score neither as a competition winner.
