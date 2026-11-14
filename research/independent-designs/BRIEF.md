
# Clean-room engineering challenge — dry-pipe sprinkler monitoring product

**Purpose:** An independent AI advisor should engineer a NEW practical product without seeing the existing prototype's circuitry, chosen electronics, mechanical design, firmware, or other advisors' proposals. The only permitted input is this brief, answers from the owner, original public technical sources, and repository governance. The repository is an administrative output destination, not design reference material.

## Real operating problem

The owner has a commercial warehouse **dry-pipe sprinkler system**. Its compressor maintains air pressure to hold the dry-pipe valve closed and keep water out of the downstream sprinkler piping under normal conditions. The owner's system typically operates around **50 PSI**, but this is a site-specific observation, **not a universal setpoint, allowed pressure band, trip threshold, or alert threshold**. If air pressure falls too far, the dry valve can trip and admit water into the pipes; this is NOT synonymous with sprinklers discharging, since heat-operated sprinkler heads remain closed unless activated. The owner reports a site-specific external diverter/drain that can expel water outside during a trip; independently verify the installation and do not generalize this arrangement.

**Primary objective:** Continuously observe pressure and alert reliably when it trends toward an abnormal or potentially trip-inducing level, or when sensor/device monitoring fails, ideally before an unnecessary water admission event. Detect high pressure too where technically appropriate. No automatic actuation, compressor or valve control. Qualified sprinkler professionals must approve pressure taps, site-specific normal bands, fault thresholds, and any work on the fire-protection installation.

The riser room is attached to the warehouse but sealed off from the conditioned warehouse interior and exposed to outside cold. An ambient temperature sensor should warn if the room becomes too cold, **particularly if the condition lasts long enough** to warrant the owner manually installing or operating a heater. No heater or thermostat control required. Thresholds and persistence are installation-specific.

This is initially **supplementary monitoring and early warning**, not a replacement for required supervisory devices, listed fire alarm, fire-protection controls, inspection or compliance procedures.

## Product experience

Keep the product straightforward and dependable. The user wants an intuitive **browser-based responsive dashboard** on computer, tablet, iPhone/Android or other modern platform. Show current pressure PSI, riser-room ambient temperature, timestamps/sample freshness, sensor/network/device status, event history and simple trends. Configure site-appropriate pressure and cold-duration thresholds, hysteresis/persistence, severity, contacts, acknowledgement and recovery.

Support practical **push notifications and/or SMS** for low/high pressure, sustained cold, sensors missing/faulty, device/site offline, recovery and other significant status. Research practical mobile web-push support and SMS providers; expose recurring message costs and delivery limitations. Never present stale/invalid measurements as normal. Device/site outages require **independent offsite heartbeat monitoring**, since a failed or disconnected device cannot send its own alert. Start single-site and provide a sensible path to multi-site and contractor management without bloated complexity.

## Workshop manufacturing requirement

The designer must create something that **one technically capable DIY workshop operator can personally manufacture, assemble, program, calibrate, test, diagnose and repair**. The owner is proficient with electronics, soldering, test instruments, CAD and FDM 3D printing. Buying standard parts, commercially fabricated *bare* PCBs, ready-made modules, a suitable enclosure and fixtures is allowed. Optional outsourced SMT assembly is allowed only when it saves meaningful cost or improves quality while preserving realistic small-workshop final production. Do not assume access to industrial pick-and-place, injection molding, industrial test labs in the shop, or proprietary factory lines.

Estimate actual total materials, manual labor, tooling, test/rework yield and ongoing service cost for quantities of **1, 5, 25 and 100 units**. Include a repeatable bench fixture and per-unit QA process.

## Independent architecture / engineering assignment

Do not assume any particular sensor technology, analog/digital interface, ADC, processor, power supply, Ethernet/Wi-Fi/cellular path, enclosure, PCB layout, communication protocol or backend platform. Evaluate **at least three credible, meaningfully different designs** against pressure accuracy, environmental reliability, power and connectivity, cable faults, supply chain, field maintenance, DIY assembly difficulty, unit cost and compliance.

Design protections against wiring errors, shorted/disconnected sensor cables, ESD/transients, out-of-range analog inputs, power issues, condensation, sensor drift, watchdog and reset faults, network/service loss, insecure credentials/updates and missed notifications. State concrete detection behavior. Research applicable US fire protection, AHJ, listing/classification, FCC/EMC, electrical and environmental product requirements and use qualified review before commercial claims or customer installs. Never claim that component certifications transfer automatically to the finished product.

## Interview requirement

**Interview the owner, one consequential question at a time**, to establish the unknown real design inputs: exact sprinkler valve and compressor behavior, normal setpoint/deadband and verified minimums, approved pressure measurement location, pressure sensor range, temperature condition, sensor run length, available power and Ethernet/Wi-Fi/cellular, whether backup power is warranted, push/SMS recipient/escalation preferences, multi-site needs, acceptable device and operating costs, available workshop tools and installation environment.

Do not repeat details stated here. Keep an ongoing Q&A/assumptions record. Continue safe research and reversible design tasks between questions; do not freeze irreversible design choices on guesses. Site-specific pressure thresholds must be confirmed with a qualified sprinkler professional.

## Durable GitHub protocol — required

**Owner-controlled repository: JamieT1701/SprinklerSystemMonitor.** It already contains an existing prototype. **DO NOT** read the existing netlists, schematics, circuits, sensors, source code, mechanical CAD, prototype documents, existing concept notes, related issues/PRs or other advisors' results until YOUR OWN independent proposal has been frozen, committed and explicitly opened for comparison by the owner.

1. Verify GitHub connection and repository ownership. Read only necessary repository governance (e.g. root AGENTS.md if present) and this BRIEF as internal context; these governance reads are not permission to inspect the existing solution. Verify the correct base/canonical branch; do not assume main.
2. Choose a distinct adviser identifier such as adviser-claude, adviser-gemini, adviser-grok, adviser-openai-1. Create a separate branch named research/independent-<advisor-id>, avoiding collision with any other agent branch.
3. Save ALL work under **research/independent-designs/<advisor-id>/**: REQUIREMENTS.md with interview and assumptions, ARCHITECTURES.md, DECISIONS.md, HARDWARE/ (schematics, editable PCB files, BOM, component sources), MECHANICAL/ (CAD and printable parts), FIRMWARE/, SOFTWARE/, MANUFACTURING/ (QA, costed assembly, calibration and valid fab exports), BUSINESS/ (costs and compliance), and HANDOFF.md with latest checkpoint.
4. Commit incrementally in GitHub and open a **DRAFT PR** unique to your advisor, without touching current prototype content. Optionally create your own advisor-specific Issue. Do not merge, contact customers, spend, place fabrication orders or deploy live services without approval.
5. Whenever reporting progress, provide exact verified commit/branch/PR links and distinguish planned versus actually created, simulated, tested or manufactured. If GitHub tools are unavailable, prepare portable deliverables and push instructions, disclose the inability to persist them, and never claim GitHub durability without a verified commit.
6. Do not view peers' branches/PRs/issues or existing design work until the owner authorizes comparative review. Maintain an auditable independent recommendation. This is a **clean-room instruction**, not a technical guarantee of isolation inside a shared repository.

## Required deliverables

- Detailed measurable product requirements, prioritized unknowns and interview receipts.
- At least three complete architecture options, quantitative tradeoffs and a reasoned winner.
- Real electronic schematics, component MPNs, protected field interfaces, power budgets, PCB/footprint design, native editable EDA projects, verified outputs where possible, second sources and costed BOM.
- Enclosure and installation design including environmentally suitable materials, routing/strain relief, mounting, workshop-assembly drawings and field service.
- Embedded firmware, secure provisioning and remote updates/rollback, watchdog, sensor validation, dashboard architecture, push/SMS, event history, multi-site expansion and independent offline alerts.
- Repeatable DIY workshop build, flashing, calibration, QA/test fixture, serial numbers, production acceptance and repair procedures.
- Sourced economics at 1/5/25/100 units, hands-on assembly and testing time, rework, sensor/enclosure/cables, cloud/SMS costs, support, and compliance gates.
- Concrete path from engineering prototype to pilot. Independently review electrically safety-critical faults; do not portray concept art as real PCB manufacturing data.

**Execution:** Research and design as far as authorized safe tools permit, ask one material question at a time, retain outcomes in GitHub. No spending or external commitments without approval. Start with a succinct TL;DR describing the preliminary problem definition, the first high-priority interview question, the GitHub location where work will be saved, and the work you can already do.

**Central challenge:** What is the simplest dependable, secure, maintainable, affordable supplementary device a skilled single-person electronics workshop can make to monitor dry-system air pressure and cold exposure in a sprinkler riser room, with actionable remote dashboard and push/SMS alerts, and how can it be built, tested and responsibly commercialized?
