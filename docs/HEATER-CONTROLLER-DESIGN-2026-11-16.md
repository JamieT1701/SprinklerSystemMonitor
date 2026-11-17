# Heater controller — isolated architecture, electrical gates and bench plan (Issue #8)

**Status:** DESIGN / SOFTWARE-SIMULATION ONLY — NO MAINS CIRCUIT, NO FIELD HOOKUP, NO CERTIFICATION
**Date:** 2026-11-16 (America/New_York)
**Branch:** design/heater-controller-20261116, branched at verified prototype-documentation commit 518570b13e3ca09257d97a275e3f89867cd026f6 (not legacy main)
**Ownership:** dedicated heater-controller workstream. Source issue: #8. Related but independent: monitor prototype #2 / draft PR #1; design competition #3; SFOS monitoring #880; SFOS forecast #893.

## 1. Verified facts and evidence limits

- Morristown Sprinkler provided a **minimum 40°F** riser-room temperature requirement. This is a **floor**, not an acceptable thermostat turn-on target. Existing SFOS warns when ambient temperature falls below 40°F, sends owner-only critical email below 30°F, and sends sensor/offline alerts. No alert/config changes under this issue.
- SFOS Issue #880 documents live monitoring on a Waveshare ESP32-S3 PoE + ADS1115 + DS18B20, V6. The hardware engineering repository's R6 historical build instructions predate V6; do not mistake old bring-up status for today's live status. No modification to V6, its enclosure, PoE cable, sensors, data endpoint, pressure input, or SFOS service is authorized.
- Owner reports an **'oil heater'** currently set to run in the riser room; prior ambient approximately 54–55°F. **No heater photo, make, model, voltage, wattage, current, electrical connection, factory thermostat, over-temperature limit, tip-over protection, automatic restart or manual has been verified.** 'Oil heater' may mean electric oil-filled radiator or fuel-burning heater. The architecture cannot assume either.
- Repo tree on verified active docs branch contains NO AGENTS.md or formal heater inventory. R6 parts and Waveshare/ADS geometry belong to the separate monitor; they are **not** free stock for a new board. Prior user purchase history indicates additional USB ESP32 boards and passives, but **remaining on-hand stock is unverified**. No relay, SSR, contactor, mains enclosure, mains cable, breaker or heater load rating is approved.
- The physically accepted P4 PETG plate belongs to the existing monitor. **Do not reuse or alter it.** No live heater/sprinkler wiring changes, purchases, or tests are authorized here.

## 2. Selected approach (safe path first)

**Stage A — monitoring-only / independent heater (recommended now).** Existing heater continues under *its manufacturer-approved controls*. Separate test-only ESP32 indicates a hypothetical heating demand with a small LED. Software failure has no electrical path into the heater. SFOS remains independent. First confirm whether the heater's *existing unattended duty* and installation are actually approved by the manufacturer, electrical professional, insurer/AHJ and facility rules; do not equate 'currently working' with approved safety.

**Stage B — possible manufacturer-approved supplementary interface (conditional).** If the *exact* model is permanently installed or has a manufacturer-listed low-voltage enable/thermostat terminal specifically designed for remote control, a qualified professional can evaluate a **galvanically isolated** dry-contact interface. Existing independent mechanical/approved thermostat, high-limit, short-cycle and other internal safeties remain effective. Software shall not be the sole source of heat-demand in a room required to stay above 40°F; topology must be shown to preserve a qualified standalone heat source through network/MCU/sensor failures. No connection currently specified.

**Stage C — if the current heater is a portable plug-in radiator or prohibited for unattended/remote switching.** Do **not** add a smart plug, inline timer, exposed relay, custom mains controller or software-cycled contactor. Instead obtain professional review of a correctly sized **listed, permanently installed fixed heater and standalone listed line-voltage thermostat/control** suitable for the room. A permitted remote control input or monitoring signal can be added only when designed and rated for it. Some oil-filled radiator manuals forbid any external automatic on/off switching because it may restart a thermal limiter; the actual heater manual governs.

If it is an oil-fired/combustion device, STOP electrical-interface design and obtain a qualified heating technician's model-specific controls/ventilation/CO requirements. A generic relay cannot be specified.

**Decision:** NO mains switching component chosen; no hardware purchase recommended until exact heater is identified and suitability reviewed. A normally-closed contactor is not a universal 'fail-on' solution: welded contacts, upstream breaker trips, overheated loads, manual reset and controller power loss each require analysis. Prefer existing independent thermostat over software series control.

## 3. Architecture / electrical boundaries

Power / safety boundaries:

    Existing heater → existing manufacturer-designed thermostat/high-limit/protections → room heat
    Room ambient → existing independent V6 DS18B20 → SFOS telemetered read/alerts (read-only in this lane)
    [SEPARATE 5V USB bench PSU] → [spare ESP32] → [3.3V LED + 330Ω resistor] (mock heat-request only)
                                 ↘ [optional separate DS18B20 + 4.7k pull-up] (or injected simulator temperatures)
    MCU/network/bench harness  -X-  existing heater, V6, PoE, sprinkler piping, fire panel

Bench schematic (ALL low voltage; no AC/mains):

    USB 5V → spare ESP32 USB connector (board's approved internal regulation)
    ESP32 GND ---------------------- GND
    ESP32 GPIO_OUT --- 330Ω --- LED anode ; LED cathode --- GND
    Optional standalone DS18B20: VDD→3V3; GND→GND; DATA→chosen GPIO_SENSOR
                                4.7kΩ pull-up between DATA and 3V3
    Optional physical switch: GPIO_DISABLE → normally-open button → GND, MCU internal pull-up
    **GPIO pins require physical pinout confirmation on the actual spare board before connection.**
    **Never attach a relay coil directly to ESP32 GPIO. No mains, heater, 48V PoE, contactor, SSR or test bulb.**

Future interface block (NOT a wiring diagram or bill of materials):

    independent approved heat source and thermostat (no dependence on MCU)
                   [only a manufacturer-provided listed auxiliary interface, if documented]
      separate controller logic → isolated driver → properly designed interposing device
                   [industrial enclosure, service disconnect, protection and competent review]

Never put the ESP32 or its carrier PCB inside a mains contactor enclosure without independently reviewed creepage/clearance, insulation and protection. The preferred field design, *if one is ever needed*, is separate SELV controller and professionally installed listed HVAC/heat-control equipment; not a hobbyist mains PCB.

## 4. Bench controller behavioral contract (not deployed)

A provisional **visual indication** state machine used only to validate hysteresis and failure recovery, not a heater thermostat specification:

- Mock temperatures: 'HEAT_REQUEST' at **T <= 48°F**; release request at **T >= 52°F**. Between thresholds retain last stable demand. Values are test assumptions, not Morristown requirements or approved heater settings.
- Valid finite temperature, plausible range (-40…125°F), and sensor-present status required. DS18B20 disconnected/bad CRC, power-on 85°C sentinel (185°F), stale samples, parse errors and MCU reset must be distinguishable from healthy reading.
- Sensor invalid/stale: output LED **OFF**, fault asserted, preexisting heater remains unaffected. Runtime reboot initializes LED OFF and only resumes requests after a valid fresh reading. Network offline: continue local bench decision from local sensor; nothing reaches the heater.
- Soft manual-disable makes mock output OFF regardless of demand. A test-only 'force request' shall **not** become a field heater override or safety bypass.
- In any proposed field design, no automatic remote safety bypass; feedback is required to *diagnose* a stuck contactor, never assumed from commanded GPIO. For this bench, 'welded ON/OFF' means explicitly injected LED feedback mismatch, not an actual line-voltage fault.

## 5. Failure / dependency matrix

| Fault/condition | Mock LED/request | Existing heater (all stages before hookup) | Risk / investigation |
|---|---|---|---|
| Valid cold T <=48°F | ON | Independently thermostated | Candidate *request*, not permission to energize |
| Valid hot T >=52°F | OFF | Independently thermostated | Heating still governed by heater |
| 48<T<52°F | Previous accepted state | Independently thermostated | Hysteresis avoids chattering |
| DS18B20 disconnected / invalid / stale | OFF + sensor fault | Independently thermostated | Critical reason never to series-switch actual heater |
| ESP reboot / supply interruption | OFF until fresh valid sample | Independently thermostated | Separate hardware; do not share V6 PoE |
| Network / SFOS outage | Local bench logic only | Independently thermostated | SFOS outage alerts remain its own responsibility |
| Software/manual disable | OFF | Independently thermostated | Cannot disable required facility heat |
| Mock output stuck ON / feedback mismatch | Fault; cannot clear physical fault in software | Independently thermostated | Proper interface must have electrical protection and tested diagnosis |
| Mock output stuck OFF / feedback mismatch | Fault | Independently thermostated | No lost primary heat on bench |
| Heater internal thermal cutout / tip-over | Unknown, need heater alarm/inspection | Manufacturer safety acts | NO BYPASS; physical repair/replacement |
| Branch circuit breaker trip / heater unplugged | May show demand | No heat: independent heater also unavailable | ESP32 cannot guarantee heating; independent monitoring/inspection essential |
| Room <40°F | No change to SFOS production policy | Existing heater per controls | Immediate facility response per sprinkler-service instructions |
| Room <30°F | No change to owner-critical email | Existing heater per controls | Critical escalation already owned by SFOS |

The matrix makes one key distinction: *resilience to software failure* is not the same as resilience to the heater's own power, thermostat or heating-element failure. Dedicated installed heat capacity and independent inspections/alarms remain required.

## 6. Proposed bill of materials — **bench-only**

| Item | Qty | Verified basis | State |
|---|---:|---|---|
| Spare ESP32 dev board powered from isolated standard USB supply | 1 | Previously purchased ESP-WROOM-32/ESP-32S / Mini/DevKitC families; NOT the live PoE S3 | Stock count and selected board pinout to confirm |
| USB cable and reputable low-voltage USB source | 1 | Generic engineering bench equipment | Confirm present and in good order |
| 330 Ω resistor (typical 1/4 W) | 1 | Limits small indicator LED GPIO current | Stock unverified |
| Low-current indicator LED | 1 | ONLY simulated heater-request load | Stock unverified |
| Temporary isolated-pad breadboard/perfboard and jumper leads | 1 | No high voltage on prototype | Stock unverified |
| Optional extra genuine DS18B20 probe | 1 | Alternate real sensor input; NO sharing V6 probe | Stock unverified |
| 4.7 kΩ resistor for optional DS18B20 DATA pull-up | 1 | Prior project uses 4.7k 1Wire pull-up, not necessarily surplus | Stock unverified |
| DMM + labeled low-voltage cable | 1 | Polarity/continuity bench validation | DMM presumed available from prototype history, condition unverified |
| **Contactor/SSR/mains relay/smart plug** | **0** | Heater unknown and no independent electrical clearance | Intentionally **NOT SELECTED** |

No material purchasing authorization. An optional 3D-printed low-voltage cover may be designed after the chosen ESP32 footprint is measured; never treat PETG as a listed mains enclosure.

## 7. Enclosure and later field-path options

Bench: transparent small **LOW VOLTAGE ONLY — SIMULATED HEAT REQUEST** labeled enclosure with USB access, protected LED, one recessed disable button and optional 3-wire sensor entry; no exposed metal connected to anything but safe extra-low-voltage electronics; strain-relieved USB/sensor cable. Not mechanically or electrically attached to the riser heater, V6 case, or fire equipment.

Future, only if applicable and professionally approved: separate SELV box, independent listed heater controller installed in appropriately rated listed enclosure, serviceable disconnect, properly protected supply and grounding, evaluated contact/load temperature and duty, routing/separation, fault indication and accessible operating instructions. No specified NEMA/IP, cable AWG, fuse, breaker, actuator MPN, contactor pole count, service clearances or wall mounting until heater + site electrical system are measured and AHJ/electrician consulted.

## 8. Test strategy and concrete acceptance

**Host-only executable simulator** in tools/heater_controller_sim.py with tests in tests/test_heater_controller_sim.py. The simulator covers logic contracts but does not exercise electrical, thermal or mechanical hardware. Acceptable host test: all tests pass locally and transcript commit recorded, no production/device connections.

**Physical bench checklist for November 17, after model photo / safe test board selection:**
1. Photo heater entire unit + manufacturer/nameplate + front controls + power connection *without disturbing its operation*. Record exact MPN, V, W/A, AC phase/frequency, thermostat, hi-limit, tip-over, restart instructions, installed vs portable, certification marks, manual and recall check.
2. Confirm with facilities/sprinkler professional that existing room heating arrangement is suitable, permanent as required and 40°F minimum is protected; don't intentionally cool room to test.
3. Separate from live V6/PoE/sprinkler/heater, inspect a spare ESP32, USB cable, low-voltage supply, LED polarity, resistance and board pinout with DMM; no connection to any mains.
4. Power bench ESP32 alone and verify correct 3V3/GND, then add 330Ω+LED mock load; verify LED OUT turns on/off and no overcurrent/hot components.
5. Inject temperatures 55, 50, 48, 46, 50, 52, 55°F and verify rising/falling thresholds, no chatter within hysteresis. Use software injection or **separate** ambient probe, not live room cooling.
6. Inject sensor disconnect, CRC failure, stale sample, 185°F DS18B20 startup sentinel, implausible values. Require LED OFF plus distinct fault reason.
7. Disconnect bench network, reset MCU, remove and restore USB power; require safe initialization and fresh reading before valid indication.
8. Apply mock disable and simulate a welded-on or failed-open output with *separate simulated feedback*, verifying mismatch detection. Do NOT actually weld or short hardware.
9. Record video, DMM measurement, firmware hash, board ID, physical breadboard photo, test dates and outcomes in Issue #8. Anything not performed is **UNTESTED**.
10. Restore bench to power-off. Existing riser heater and installed monitor remain unchanged and working.

Acceptance for physical prototype requires every case above with evidence, qualified review of exact heater manual and safety features; any failure or missing heater model halts mains integration.

## 9. Hard release gates / rollback

- **G0:** identify heater and room installation; confirm heater is acceptable for unattended/freezing-duty operation; manufacturer manual and any external switching prohibition; smoke/CO precautions if combustion; applicable NFPA/NEC, fire marshal/AHJ.
- **G1:** pass host simulation, isolated low-voltage-only bench with physical electrical measurements. No field sensors attached.
- **G2:** independent signed electrical/HVAC review of a model-specific scheme (rated inductive/resistive current + inrush; supply/branch duty; fail states; listed device; disconnect, grounding, overcurrent, insulation, enclosure/strain relief, heat clearances, automatic restart/thermal limit; manufacturer warranty and permission), and qualified sprinkler professional's winter-heating requirements.
- **G3:** owner explicitly approves field design, budget, supervised installation, rollback and safety plan; professional performs mains work where appropriate; no automatic use of prototype code as safety control.
- **G4:** observed supervised end-to-end installed testing and restoration of normal operation, including independent thermostat behavior when controller unpowered, alarm/sensor fail tests without induced room freeze, inspection signoff and operations SOP. Production acceptance is separate from hardware readiness.

**Rollback:** until G3 nothing touches heater; stop/delete mock GPIO or unplug USB and heater remains unaltered. For a later approved installation, physical rollback needs a detailed electrician-approved design restoring the *manufacturer-specified* original control/power routing and verifying room heat; never use generic jumper bypasses or defeat thermal safeties.

## 10. External primary references to validate by exact heater type

- CPSC space heater guidance: https://www.cpsc.gov/Newsroom/News-Releases/2023/CPSC-Warns-Consumers-to-be-Cautious-When-Using-Space-Heaters-Furnaces-and-Fireplaces-This-Winter (plug direct; clearances; don't leave portable heaters running unattended).
- NFSA freeze protection guidance: https://nfsa.org/the-cold-reminder-about-sprinkler-systems/ (40°F wet valve areas; inspections and low-temperature alarms).
- Dry riser room heat and permanent installation discussion: https://www.fhca.org/focusonflorida/entry/dry_sprinkler_riser_rooms (NFPA 13 interpretation; portable heat limitations).
- Example *different* oil-filled heater manual with external timer/remote-switch prohibition (illustrative only; **not evidence about owner's model**): https://device.report/manuals/oil-filled-radiator-operating-instructions
- **Code adoption and enforceable details must be confirmed for the property with the AHJ and knowledgeable tradesperson.**

## 11. Next required input (only heater identity is a human gate)

Photo of manufacturer/nameplate and front controls, plus one overall photo showing power source, mounting and nearby combustibles; no disconnection. Engineer records data, retrieves the **correct** factory instructions and recall status, and only then proposes a qualified mains architecture or a safer fixed-heater alternative.

**Explicit non-accomplishments:** no heater model verification; no load/actuator rating; no electrical hookup; no field relay; no independent electrical review; no real heater bench tests; no production firmware; no sprinkler system modification; no SFOS policy changes.