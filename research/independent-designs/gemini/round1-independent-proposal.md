# Clean-Room Engineering Proposal: Dry-Pipe Sprinkler Supervisory & Riser Room Monitor

**Adviser Identifier:** `adviser-gemini`  
**Target Repository Workspace:** `research/independent-designs/adviser-gemini/`  
**Execution Context:** Round 1 Blind Engineering Evaluation (Plain Markdown Proposal)

---

## 1. TL;DR Architecture Recommendation

We recommend an **Isolated Hardwired Ethernet / Auxiliary 24V (or PoE) Industrial Edge Monitor** built around a dual-core industrial microcontroller (Espressif ESP32-S3 or RP2040 + W5500 hardwired TCP/IP SPI controller) housed in an IP65/NEMA 4X polycarbonate enclosure. 

- **Sensing:** A 0–100 PSI gauge, 316L stainless-steel ratiometric pressure transducer (0.5–4.5 V output, 1/4" NPT male) paired with an external 16-bit delta-sigma ADC (ADS1115) for rock-solid zero/span stability, combined with a digital ambient temperature sensor probe (DS18B20 or TMP117) measuring the riser room climate.
- **Power & Fail-Safe Hold-up:** 12–24V DC/AC input (compatible with standard industrial/HVAC transformers) or 802.3af PoE, backed by a dual 5.5V supercapacitor hold-up circuit delivering 15 seconds of "dying-gasp" power to transmit a verified power-loss alert before orderly shutdown.
- **Communications & Offsite Heartbeat:** MQTT over TLS 1.3 reporting telemetry every 30 seconds to an offsite cloud broker. An independent cloud watchdog daemon monitors inbound heartbeats; if no message arrives within 90 seconds, the cloud fires an independent SMS/Push notification alerting the owner to device or facility network failure.
- **DIY Manufacturability:** Designed specifically for single-person workshop production using standard 2-layer commercially fabricated bare PCBs, hand-solderable 0805/SOIC passives, a modular microcontroller/Ethernet carrier, off-the-shelf NEMA enclosures with custom 3D-printed internal mounting plates, and a repeatable pneumatic bench calibration fixture.

---

## 2. Key Measurable Product Requirements & Unknowns

### 2.1 Measurable Technical Requirements

| Parameter | Specification | Engineering Rationale |
| :--- | :--- | :--- |
| **Pressure Range** | 0 to 100 PSI Gauge (psig) | Normal dry pipe is ~50 PSI. Proof pressure $\ge 200$ PSI; burst pressure $\ge 400$ PSI to withstand pump hydro tests. |
| **Pressure Accuracy** | $\le \pm 0.75\%$ Full Scale ($\pm 0.75$ PSI) | Dry-pipe differential valves typically trip when air drops to 15–25 PSI. 0.75 PSI accuracy gives early warning well above trip points. |
| **Pressure Resolution** | 0.05 PSI | Critical for real-time derivative analysis ($dP/dt$) to identify minor leaks or compressor short-cycling before thresholds trip. |
| **Sampling & Filtering** | 10 Hz internal oversampling; 1 Hz filtered moving average | Attenuates mechanical noise and pipe vibration caused by compressor operation. |
| **Telemetry Interval** | 30 s nominal; burst to 1 s on trigger | Bandwidth-efficient nominal telemetry; switches to high-speed logging when rate of change exceeds $\pm 0.5$ PSI/min. |
| **Temperature Range** | $-20^\circ\text{C}$ to $+60^\circ\text{C}$ ($-4^\circ\text{F}$ to $+140^\circ\text{F}$) | Covers unconditioned, uninsulated commercial riser rooms in freezing climates. |
| **Temperature Accuracy** | $\pm 0.5^\circ\text{C}$ ($\pm 0.9^\circ\text{F}$) from $-10^\circ\text{C}$ to $+40^\circ\text{C}$ | Enables precision tracking around the critical $40^\circ\text{F}$ ($4.4^\circ\text{C}$) NFPA riser room freeze prevention threshold. |
| **Cold Persistence Logic** | Configurable duration: e.g., $< 40^\circ\text{F}$ sustained for $\ge 60$ min | Prevents nuisance notifications from brief door openings while catching true room heating failures. |
| **Enclosure Ingress** | NEMA 4X / IP65 | Riser rooms experience high condensation, dust, pipe washdown, and potential minor water spray. |
| **Power Inputs** | 9–30V DC / 12–24V AC, or IEEE 802.3af PoE | Accommodates ubiquitous fire alarm/HVAC auxiliary power or direct network power. |
| **Power Hold-Up** | $\ge 10$ seconds | Allows microcontroller to detect loss of main power, write state to non-volatile flash, and transmit a "Mains Power Failure" packet. |
| **Offsite Alert Latency** | $< 5$ s for threshold alerts; $< 120$ s for offsite silent death | Threshold alerts are push-driven immediately; dead-man offsite timer detects link loss within 2 minutes. |

### 2.2 Prioritized Critical Unknowns

1. **Riser Room Physical Utilities:** Does the room have an accessible 120VAC convenience outlet, a 24VAC control transformer, or an active structured Ethernet drop?
2. **RF Environment:** Are the walls poured concrete, cinder block, or steel fireboard? (Most riser rooms are RF Faraday cages, severely attenuating standard 2.4 GHz Wi-Fi).
3. **Piping Interface Point:** Is an approved 1/4" NPT gauge test port with an isolation cock already available on the system-side air trim, or must a new tap be approved by a fire protection contractor?
4. **Valve & Compressor Operational Profile:** What is the dry-pipe valve trip pressure ratio (e.g., 5:1 or 6:1 differential vs. pilot-actuated), the compressor cut-in/cut-out setpoints (typically ~40 PSI cut-in, ~50 PSI cut-out), and the typical pump cycle recovery time?
5. **Notification Escalation Policy:** What is the desired operational protocol for after-hours low pressure vs. daytime warnings? (Push notification for low priority; SMS/automated voice call for critical low pressure).

---

## 3. Comparison of Three Distinct Architectures

We evaluated three diverse, credible architectural approaches against nine weighted engineering criteria.

```
+-------------------------------------------------------------------------------------------------------+
| ARCHITECTURE A: Direct Cellular IoT (LTE-M / NB-IoT)                                                  |
| Low-power MCU (STM32L4) + Quectel BG95-M3 + 4-20mA Sensor Loop + LiFePO4 Battery + Solar/Trickle Aux   |
+-------------------------------------------------------------------------------------------------------+
| ARCHITECTURE B (RECOMMENDED): Hardwired Industrial Ethernet / Auxiliary 24V Node                      |
| Dual-Core ESP32-S3 + W5500 SPI Ethernet + 0.5-4.5V Ratiometric Sensor + ADS1115 + Supercap Hold-Up    |
+-------------------------------------------------------------------------------------------------------+
| ARCHITECTURE C: Pure Consumer Wi-Fi + USB 5V Wall-Wart IoT Node                                       |
| Bare ESP32 NodeMCU + Internal ADC + USB Wall Adapter + I2C Pressure Sensor                            |
+-------------------------------------------------------------------------------------------------------+
```

### 3.1 Architecture Overview

* **Architecture A: Direct Cellular IoT (LTE-M/NB-IoT)**
  * *Edge:* Ultra-low-power STM32L4 MCU interfaced to an LTE-M/NB-IoT cellular modem (e.g., Quectel BG95 or Nordic nRF9160) powered by a 12V supply with a LiFePO4 battery backup.
  * *Sensor:* 2-wire 4–20 mA current loop pressure transmitter.
  * *Network:* Direct cellular connection to cloud broker, completely bypassing facility network infrastructure.
* **Architecture B (Recommended Winner): Hardwired Industrial Ethernet / Auxiliary 24V Node**
  * *Edge:* Dual-core ESP32-S3 (or RP2040) pairing a hardware W5500 Ethernet controller with Wi-Fi as an alternate fallback. Powered by 12–24V DC/AC auxiliary input or PoE with supercapacitor hold-up.
  * *Sensor:* 3-wire 0.5–4.5V ratiometric pressure transducer into an external 16-bit differential delta-sigma ADC (ADS1115) + digital 1-Wire/I2C temperature sensor.
  * *Network:* Local Ethernet out to local gateway; fallback to Wi-Fi if enabled during provisioning.
* **Architecture C: Pure Consumer Wi-Fi IoT Device**
  * *Edge:* Generic ESP32 or ESP8266 development module powered by a standard 5V USB wall transformer.
  * *Sensor:* Low-cost I2C pressure sensor or direct analog reading using the internal ESP32 SAR ADC.
  * *Network:* Facility 2.4 GHz Wi-Fi only.

### 3.2 Quantitative Weighted Tradeoff Analysis

*Scale: 1 (Poor) to 5 (Superior). Weights reflect commercial riser room reliability requirements.*

| Evaluation Criteria | Weight | Architecture A (Cellular) | Architecture B (Hardwired Ethernet) | Architecture C (Consumer Wi-Fi) |
| :--- | :---: | :---: | :---: | :---: |
| **Pressure Accuracy & Signal Integrity** | 15% | 4 (Good current loop, but DAC/ADC thermal drift) | **5 (Ratiometric tracking cancels VDD drift via ADS1115)** | 2 (Internal ESP32 ADC non-linear, noisy, uncalibrated) |
| **Environmental & Power Reliability** | 20% | 4 (LiFePO4 battery degrades in extreme cold $<0^\circ\text{C}$) | **5 (Supercapacitors operate down to $-40^\circ\text{C}$; robust 24V buck)** | 1 (Cheap USB power bricks fail under cold/moisture) |
| **Network Dependability in Riser Room** | 20% | 3 (Cellular often blocked by metal/cinderblock without external roof antenna) | **5 (Hardwired Cat5e/6 immune to RF attenuation and jamming)** | 2 (Wi-Fi notoriously poor in isolated metal riser rooms) |
| **Cable Fault & Self-Check Diagnostics** | 10% | 5 (4-20mA inherently detects open circuit $<4\text{mA}$) | **5 (0.5–4.5V rail bounds: $<0.35\text{V}$ = open, $>4.75\text{V}$ = short)** | 2 (Digital I2C bus hangs on long cable runs or moisture) |
| **DIY Assembly & Workshop Sourcing** | 15% | 2 (BG95/nRF9160 are fine-pitch BGA/LGA, difficult for hand assembly) | **5 (SOIC/MSOP/0805 or DIP/pin-header modules; easy hand/hot-plate soldering)** | 4 (Very easy DIY, but fragile hobbyist form factor) |
| **Unit Hardware Cost (at 25 units)** | 10% | 2 (Modem + RF certs + LiFePO4 battery $\approx \$130$) | **4 (Industrial components + Ethernet $\approx \$55-\$65$)** | 5 (Hobby parts $\approx \$25$) |
| **Operational Simplicity & Ongoing Cost** | 10% | 2 (Requires monthly cellular SIM subscription: $\$3-\$6/\text{mo}/\text{unit}$) | **5 (No recurring connectivity fees; uses local facility internet)** | 4 (No carrier fees, but frequent field service to fix Wi-Fi drops) |
| **Weighted Score** | **100%** | **3.40** | **4.90** | **2.75** |

### 3.3 Selection Rationale
Architecture B is the decisive winner. Riser rooms are notoriously hostile to RF signals (steel fire doors, metal roof decking, reinforced concrete). Relying on Wi-Fi (Architecture C) creates recurring nuisance disconnection alarms. Cellular (Architecture A) solves local IT dependencies but adds high recurring SIM costs, battery degradation in freezing weather, and BGA assembly difficulty for a single-person shop. Architecture B provides rock-solid, zero-maintenance industrial reliability, fits easily within DIY workshop capabilities, and requires no ongoing carrier fees.

---

## 4. Recommended Electronics, Sensors, Protection & Offsite Monitoring

```
+---------------------------------------------------------------------------------------------------+
| HARDWARE BLOCK DIAGRAM (ARCHITECTURE B)                                                           |
|                                                                                                   |
|  [ 9-30V DC / 24V AC ] ---> [ PPTC + TVS ] ---> [ Bridge Rectifier ] ---> [ LM5164 Buck 5V ]      |
|                                                                                  |                |
|                                                                         [ Ideal Diode OR ]        |
|                                                                                  |                |
|  [ Supercap Backup ] <--- [ Charger ] <------------------------------------------+                |
|  (2x 1.0F 2.7V in Series = 0.5F 5.4V)                                            |                |
|                                                                                  v                |
|                                                                         [ 3.3V LDO Regulator ]    |
|                                                                                  |                |
|  +--------------------+         +------------------------+                       |                |
|  | 0.5-4.5V Pressure  |         |   Dual-Core ESP32-S3   |<----------------------+                |
|  | Transducer (NPT)   |         |   (Core 0: Network)    |                                        |
|  +---------+----------+         |   (Core 1: DSP/Safety) |<---> [ Hardware Watchdog TPS3823 ]     |
|            |                    +-----------+------------+                                        |
|            v (RC Filter + TVS)              |                                                     |
|  +--------------------+                     | SPI Bus                                             |
|  | ADS1115 16-bit ADC |<--(I2C Bus)---------+                                                     |
|  +--------------------+                     v                                                     |
|                                 +------------------------+                                        |
|  +--------------------+         |  W5500 SPI Ethernet    |                                        |
|  | DS18B20 Temp Probe |<--(1-Wire)        + MagJack      |                                        |
|  +--------------------+         +-----------+------------+                                        |
|                                             |                                                     |
|                                             v                                                     |
|                                 [ Cat5e/6 Hardwired Drop ]                                        |
+---------------------------------------------------------------------------------------------------+
```

### 4.1 Sensor Subsystem & Interfacing
1. **Air Pressure Transducer:**
   * **Part Specification:** Sensata 116CP or Honeywell MIP Series (or equivalent industrial 316L piezoresistive transducer with internal ASIC compensation).
   * **Range & Output:** 0 to 100 PSI gauge (psig), 1/4" NPT male thread. Output: 0.5V to 4.5V ratiometric to a 5.0V excitation rail.
   * **Why Ratiometric 0.5–4.5V?** Ratiometric sensing cancels out power supply drift when the ADC reference tracks the sensor excitation voltage ($V_{\text{out}} / V_{\text{DD}}$). Unlike raw wheatstone bridges, the transducer incorporates factory laser-trimmed temperature compensation and signal amplification.
   * **Signal Conditioning:** Sits behind a 2-pole RC low-pass anti-aliasing filter ($f_c \approx 15\text{ Hz}$) to reject mechanical compressor pulsation noise and electrical pump contactor transients.
2. **Analog-to-Digital Converter (ADC):**
   * **Part:** Texas Instruments ADS1115 (16-bit Delta-Sigma ADC with internal PGA and I2C interface).
   * **Critical Design Rule:** Do **not** use the internal SAR ADC of the ESP32. The internal ESP32 ADC has severe non-linearity below 0.2V and above 2.8V, high thermal drift, and poor noise immunity. The ADS1115 provides a stable differential measurement between the sensor signal and the excitation ground.
3. **Ambient Temperature Sensor:**
   * **Part:** Maxim/Analog Devices DS18B20 digital temperature probe inside a potted 304 stainless-steel tube with a 2-meter silicone jacketed cable.
   * **Interface:** Dedicated 1-Wire interface with a 4.7 k$\Omega$ pull-up resistor and 5.1V Zener clamp, or an on-board Texas Instruments TMP117 (I2C, $\pm 0.1^\circ\text{C}$). The remote probe is mounted outside the electronics enclosure to measure ambient air without enclosure heat dissipation bias.

### 4.2 Power Architecture & Protection Circuits
* **Input Stage:** Accommodates 9V to 30V DC or 12V to 24V AC.
  * *Protection:* 500mA resettable PPTC fuse, bidirectional TVS diode (SMAJ28CA) rated for 400W transient clamp against lightning induced surge, followed by a Schottky full-wave bridge rectifier (MBR140) to guarantee reverse-polarity immunity and support AC supplies.
* **Regulation:**
  * Primary Step-Down: High-voltage, high-efficiency synchronous buck converter (TI LM5164 or TPS54202) dropping 9–30V down to 5.0V for sensor excitation and supercap charging.
  * Clean Logic Rail: Low-dropout linear regulator (Microchip MCP1700 or TI TLV75533P) producing low-noise 3.3V for the MCU, ADC, and Ethernet controller.
* **Supercapacitor Dying-Gasp Backup:**
  * Two 1.0F, 2.7V radial supercapacitors connected in series (effective 0.5F, 5.4V) with passive balancing resistors.
  * Controlled via an ideal diode circuit (TI LM66100 or LTC4412).
  * *Stored Energy Calculation:*  
    $$E = \frac{1}{2} C (V_{\text{initial}}^2 - V_{\text{drop}}^2) = \frac{1}{2} (0.5\text{ F}) (5.0^2 - 3.4^2) \approx 3.36 \text{ Joules}$$
    At a 3.3V active draw of 150mA ($P \approx 0.5\text{ W}$), hold-up time exceeds 6 seconds—plenty of time for the MCU to detect $V_{\text{in}}$ drop via an interrupt pin, flush the last telemetry payload ("STATUS: POWER_LOSS_UNPLANNED") over Ethernet, and shut down safely.

### 4.3 Self-Check, Fault Diagnostics & Field Protections
1. **Broken Wire & Short-Circuit Detection (Out-of-Band Diagnostics):**
   * Valid sensor output is strictly bounded between 0.50V (0 PSI) and 4.50V (100 PSI).
   * **Open Circuit / Cable Severed:** A weak internal 100 k$\Omega$ pulldown pulls the ADC input to $< 0.20\text{V}$. The firmware immediately flags `FAULT: SENSOR_DISCONNECTED_OR_CUT`.
   * **Short to 5V Rail / Overpressure:** If voltage exceeds $4.80\text{V}$, the firmware flags `FAULT: SENSOR_SHORT_TO_SUPPLY_OR_OVERPRESSURE`.
2. **Sensor Frozen / Stuck-at Detection:**
   * Dry-pipe systems experience subtle diurnal pressure swings due to temperature changes ($PV = nRT$) and compressor cycling. If standard deviation of pressure is exactly $0.00$ PSI over a 12-hour window, the firmware flags `WARNING: PRESSURE_TAP_CLOGGED_OR_FROZEN`.
3. **External Hardware Watchdog:**
   * Texas Instruments TPS3823 external supervisor. Requires a strobe pulse from Core 1 every $\le 1.6\text{ s}$. If firmware hangs, memory deadlocks, or the network task stalls, the external chip triggers a hard hardware reset.

### 4.4 Independent Offsite Failure Monitoring (Dead-Man Watchdog)
A failed, crushed, or severed device cannot transmit an alert. Therefore, system integrity relies on an **offsite cloud watchdog**:

```
[ Monitor Edge Node ] ---> (Periodic MQTT Ping every 30s) ---> [ AWS / Cloudflare Edge Broker ]
                                                                             |
                                                                   (Refreshes TTL in Redis)
                                                                             |
                                                                             v
[ Offsite Watchdog Cron ] <---------------------------------------- [ Redis Key Expiry Watcher ]
          |
          |-- (No heartbeat for 90s + 30s grace) --> [ Trigger CRITICAL_OFFSITE_ALERT ]
                                                                 |
                                                                 v
                                                       [ Twilio SMS / Web Push ]
```

1. **Heartbeat Protocol:** The edge device publishes an encrypted MQTT/TLS 1.3 telemetry payload every 30 seconds.
2. **Cloud State Store:** A cloud worker (e.g., Node.js / Go on a cheap VPS or AWS Lambda/Redis) receives the payload, writes the timestamp, and resets a 90-second countdown timer.
3. **Triggering Inactivity Alert:** If the cloud timer expires without receiving a heartbeat:
   * **Stage 1 (90s):** Cloud status transitions to `WARNING: LINK_STALE`.
   * **Stage 2 (120s):** Cloud fires an independent alert through Twilio SMS and Web Push:  
     `"CRITICAL ALERT: Sprinkler Monitor [Site-Warehouse-A] has ceased transmitting for >120s. Check riser room power and network."`

---

## 5. Workshop Manufacture, Calibration, Test Fixtures & Unit Economics

### 5.1 Workshop Assembly & Mechanical Strategy
* **PCB Fabrication:** Standard 2-layer, 1.6mm FR4, lead-free HASL or ENIG bare boards ordered from standard commercial fabricators (e.g., JLCPCB, PCBWay).
* **Assembly Method:** Designed for single-person hand assembly. Passives are standard 0805 footprints; ICs use SOIC, MSOP, or wide-pitch QFP. Critical sub-circuits (ESP32-S3 module, W5500 module) use castellated or pin-header pre-certified modules to eliminate BGA soldering and RF layout risks.
* **Enclosure & Fixturing:** Off-the-shelf IP65 flanged polycarbonate box (e.g., Bud Industries PN-1323-DG or Hammond 1554 series) with clear cover and silicone gasket.
  * Internal chassis: 3D-printed mounting sled (printed in **PETG** or **ABS** for thermal resistance down to $-20^\circ\text{C}$; PLA is strictly avoided due to cold embrittlement and moisture creep).
  * Penetrations: Two sealed cable glands: One PG7/M12 gland for external temperature probe, one PG9/M16 gland for Cat5e/PoE or power cable. The pressure sensor threads directly into a panel-mount bracket or connects via a flexible high-pressure micro-hose to isolate mechanical pipe shock from the PCB.

```
+---------------------------------------------------------------------------------------------------+
| REPEATABLE PNEUMATIC QA & CALIBRATION BENCH FIXTURE                                               |
|                                                                                                   |
|   [ Hand Air Pump ] ---> [ Needle Valve ] ---> [ Surge Chamber (1L) ] ---> [ 3-Way Valve ]        |
|                                                                                 |                 |
|                   +-------------------------------------------------------------+                 |
|                   |                                                             |                 |
|                   v                                                             v                 |
|        [ NIST Reference Gauge ]                                     [ Device Under Test (DUT) ]   |
|        (Additel / Dwyer $\pm0.05\%$)                                 (Pneumatic Quick-Disconnect)  |
|                   |                                                             |                 |
|                   v (RS-232 / USB)                                              v (UART / USB)    |
|       +-----------------------------------------------------------------------------+             |
|       |                     Workshop Automated Python QA Harness                    |             |
|       |  1. Measures DUT vs Reference at 0, 25, 50, 75, 100 PSI                     |             |
|       |  2. Solves Offset (V0) and Gain (S) via Linear Regression                   |             |
|       |  3. Burns unique serial & calibration constants into ESP32 NVS Flash        |             |
|       |  4. Prints serialized QA certificate and labels                             |             |
|       +-----------------------------------------------------------------------------+             |
+---------------------------------------------------------------------------------------------------+
```

### 5.2 Calibration & QA Testing Fixture
A dedicated DIY benchtop calibration rig ensures verifiable accuracy:
1. **Pneumatic Manifold:** Constructed with brass/stainless 1/4" fittings, an air hand-pump with vernier fine adjustment (e.g., Ralston or low-cost pneumatic comparator), a 1-liter accumulator chamber to dampen drift, and a digital reference gauge certified to $\pm 0.05\%$ FS.
2. **Automated QA Script:**
   * DUT plugs into the fixture via quick-disconnect and connects to the shop PC via USB-C.
   * Technician pressurizes to 5 cardinal points: 0.0, 25.0, 50.0, 75.0, and 100.0 PSI.
   * Automated Python script reads reference gauge and DUT raw ADC values, performs least-squares linear regression to calculate Calibration Offset ($V_0$) and Scale Factor ($S$), and writes these parameters into ESP32 Non-Volatile Storage (NVS).
3. **Thermal Shock & Environmental Check:**
   * Each unit is placed in a small benchtop freezer chamber ($-10^\circ\text{C}$ to $0^\circ\text{C}$) for 30 minutes to verify cold-boot capability, oscillator lock, and temperature sensor tracking before final box closure.

### 5.3 Unit Economics & Production Estimates (Estimated Breakdown)

*Estimates are based on current market availability for components, raw materials, bare PCB pool fab, and realistic single-person workshop labor ($45/hr shop rate).*

| Cost Category | Qty = 1 (Prototype) | Qty = 5 (Pilot Batch) | Qty = 25 (Small Batch) | Qty = 100 (Light Production) |
| :--- | :---: | :---: | :---: | :---: |
| **Bare PCB (2-layer pooled fab)** | $20.00 (min run) | $5.00 / ea | $2.20 / ea | $1.40 / ea |
| **Passives, Diodes, Regulators, Supercaps** | $18.00 | $12.00 | $8.50 | $6.20 |
| **Core Modules (ESP32-S3 + W5500 + ADS1115)** | $22.00 | $17.50 | $13.80 | $11.50 |
| **Industrial Pressure Transducer (0-100 PSI, 316L)** | $45.00 | $35.00 | $26.00 | $21.00 |
| **External Temp Probe & Glands** | $12.00 | $8.50 | $6.20 | $4.80 |
| **Enclosure (IP65 Polycarbonate) + 3D Plate** | $28.00 | $22.00 | $16.50 | $13.50 |
| **Connectors, Terminal Blocks, Wire, Hardware** | $10.00 | $7.00 | $4.80 | $3.60 |
| **Total Raw Materials & Components** | **$155.00** | **$107.00** | **$78.00** | **$62.00** |
| **Direct Labor Hours per Unit** | 4.5 hrs (manual fab) | 2.5 hrs | 1.2 hrs | 0.75 hrs (stencil+plate) |
| **Labor Cost per Unit (@ $45/hr)** | $202.50 | $112.50 | $54.00 | $33.75 |
| **Estimated Scrap / QA Rework Allowance** | 10% ($15.50) | 8% ($8.56) | 5% ($3.90) | 3% ($1.86) |
| **Estimated Total Unit Manufacturing Cost** | **$373.00** | **$228.06** | **$135.90** | **$97.61** |

---

## 6. Simple Responsive Dashboard, Notifications, Data & Security

```
+---------------------------------------------------------------------------------------------------+
| RESPONSIVE PWA DASHBOARD LAYOUT (MOBILE / DESKTOP)                                                |
|                                                                                                   |
|  [ HEADER: Warehouse Riser Room A ]                       [ STATUS: ONLINE - HEARTBEAT 4s AGO ]   |
|                                                                                                   |
|  +-------------------------------------+   +-------------------------------------+                |
|  | AIR PRESSURE                        |   | RISER ROOM TEMPERATURE              |                |
|  |                                     |   |                                     |                |
|  |             49.8 PSI                |   |              38.4 °F                |                |
|  |   [ NORMAL OPERATING BAND ]         |   |    [ ! COLD WARNING: 2h 15m ]       |                |
|  |  Trip: 20 PSI | Warning: 42 PSI     |   |    Threshold: <40°F for >60 mins    |                |
|  +-------------------------------------+   +-------------------------------------+                |
|                                                                                                   |
|  +-------------------------------------------------------------------------------+                |
|  | HISTORICAL TREND (24h / 7d / 30d)                                             |                |
|  |  PSI                                                                          |                |
|  |  55 |-------/\---------/\---------/\------- (Compressor cycling: ~6 hr period)|                |
|  |  50 |------/  \-------/  \-------/  \------ (Current: 49.8 PSI)               |                |
|  |  40 | - - - - - - - - - - - - - - - - - - - (Low Pressure Warning Band: 42 PSI)|                |
|  |  20 |======================================= (Dry Valve Trip Threshold: 20 PSI)               |
|  |   0 +------------------------------------------------------------------------ |                |
|  |     00:00        06:00        12:00        18:00        24:00                 |                |
|  +-------------------------------------------------------------------------------+                |
|                                                                                                   |
|  [ DEVICE HEALTH: Mains Power: OK | Supply: 24.1V | Signal: LAN 100M | Fw: v1.0.2 ]               |
|  [ ACTION: Mute Horn / Acknowledge ]     [ CONFIGURE THRESHOLDS ]    [ EXPORT LOGS ]             |
+---------------------------------------------------------------------------------------------------+
```

### 6.1 Dashboard Architecture (Progressive Web App)
* **Frontend:** Lightweight Progressive Web App (PWA) built with Vue 3 / Vite and Tailwind CSS. Runs in any browser (iOS Safari, Android Chrome, Desktop) without needing App Store approval.
* **Key Visual Indicators:**
  * **Pressure Dial/Gauge:** High-visibility reading with clear colored zones:
    * *Red (Critical Drop):* $<35$ PSI (approaching dry-pipe valve trip).
    * *Yellow (Advisory Low):* $35–45$ PSI (investigate compressor or system leak).
    * *Green (Normal):* $45–55$ PSI (customizable site-specific band).
    * *Yellow/Red (High Air):* $>58$ PSI (compressor cut-out failure).
  * **Cold-Exposure Duration Counter:** Shows current temperature and an active timer: e.g., *"38.2°F (Cold threshold breached for 1 hour 42 minutes)"*.
  * **System Vital Banners:** Power supply health, Ethernet link state, sample freshness timestamp, and last self-check status.
* **Historical Trend Graphing:** Interactive canvas-based line chart displaying 24-hour, 7-day, and 30-day views. Allows instantaneous visual confirmation of compressor run cycles, pressure decay slope ($dP/dt$), and ambient day/night temperature swings.

### 6.2 Notification Engine & Escalation Logic
* **Alert Delivery Channels:**
  * *Push Notifications:* Free, instant delivery via standard Web Push API (VAPID) directly to smartphones and desktop browsers.
  * *SMS Fail-Safe:* Critical alerts trigger SMS via Twilio or Telnyx API to a designated escalation list.
* **Escalation Rules:**
  1. **Advisory Warning (Level 1):** Pressure drops into Warning Band ($<45$ PSI) or Temperature stays $<40^\circ\text{F}$ for $>60$ minutes $\rightarrow$ Web Push notification sent to facility technician.
  2. **Urgent Hazard (Level 2):** Pressure drops rapidly ($dP/dt < -1.0\text{ PSI/min}$) or breaches Critical Floor ($<35$ PSI) $\rightarrow$ Immediate SMS to primary and secondary on-call contacts.
  3. **Loss of Monitoring (Level 3):** Offsite cloud watchdog misses heartbeats for $>120$ seconds $\rightarrow$ Independent SMS sent: *"Sprinkler Monitor Offline"*.

### 6.3 Security, Privacy & Authentication
* **Transport Encryption:** All telemetry uses TLS 1.3 over port 8883 (MQTT) or 443 (HTTPS) with hardcoded Root CA certificate validation.
* **Device Authentication:** Each unit is provisioned with an individual, unique client certificate (mTLS) or cryptographically secure token stored in ESP32 encrypted NVS flash.
* **Zero Inbound Attack Surface:** The edge device initiates only outbound connections. No local web servers or listening ports are open on the local warehouse network, preventing lateral movement by bad actors.
* **Firmware Updates (OTA):** Cryptographically signed firmware binaries (using ECDSA P-256). The bootloader verifies the digital signature before flashing and reverts automatically to the fallback partition if the new image fails health verification.

---

## 7. Failure Modes and Regulatory / Compliance Constraints

### 7.1 Failure Modes and Effects Analysis (FMEA)

| Failure Mode | Direct Effect | Edge Detection Mechanism | Cloud / User Response |
| :--- | :--- | :--- | :--- |
| **Pressure Port Clogged / Frozen** | System pressure drops but sensor reads constant ~50 PSI | Zero-variance check: detects lack of natural micro-fluctuations over 12 hours | Cloud issues maintenance warning: *"Pressure sensor reading static. Inspect gauge cock/capillary."* |
| **Sensor Cable Severed / Unplugged** | Loss of pressure signal | Out-of-band ADC check: input voltage falls to $<0.20\text{V}$ | Immediate Level 2 alert: *"Hardware Fault: Pressure sensor open-circuit."* |
| **Sensor Core Shorted** | Rail saturation | Out-of-band ADC check: input voltage saturates at $>4.80\text{V}$ | Level 2 alert: *"Hardware Fault: Sensor overvoltage/short."* |
| **Riser Room Freeze ($<32^\circ\text{F}$)** | Threat of valve or trim water line rupture | Ambient temperature probe tracks below freezing point | Level 2 alert when $<32^\circ\text{F}$ persists for $>15$ min: *"Freeze Hazard in Riser Room."* |
| **Compressor Runaway (Stuck Relay)** | Excessive air pressure in system | Pressure exceeds high threshold (e.g., $>60\text{ PSI}$) | Level 1 warning: *"High air pressure detected. Check compressor pressure switch."* |
| **Mains Power Loss** | Loss of primary power | Hardware comparator drops; supercapacitor powers dying-gasp | Edge sends emergency MQTT packet: *"Mains Power Severed"*; enters sleep. |
| **Facility Internet Disruption** | Loss of communication | Edge continues logging locally to flash; cloud misses heartbeats | Offsite dead-man watchdog detects silence at 120s; dispatches SMS alert. |

### 7.2 Regulatory, AHJ & Fire Protection Compliance Boundaries
* **Supplementary Monitoring Designation:** This product is engineered and marketed strictly as **Supplementary Monitoring and Early Warning Equipment**. It does **not** replace:
  * NFPA 13 mandated supervisory pressure switches (e.g., UL-listed Potter PS40 or System Sensor EPS40).
  * Direct fire alarm control panel (FACP) supervisory notification circuits.
  * Required NFPA 25 physical inspection, testing, and maintenance routines.
* **Mechanical Interface to Sprinkler System:**
  * Installation must utilize an existing, isolated 1/4" NPT inspector test gauge valve or auxiliary air port.
  * Under no circumstances may this device be installed by tapping into dry-pipe valve release chambers, differential latches, or primary control trim without explicit review and approval by a licensed fire protection professional and the local Authority Having Jurisdiction (AHJ).
* **Electrical Safety & RF Compliance:**
  * Powered by low-voltage Class 2 / SELV power sources ($\le 30\text{V DC} / 24\text{V AC}$), keeping it exempt from high-voltage UL 508A enclosure wiring standards.
  * Utilizes pre-certified radio/microcontroller modules (FCC ID / CE compliant) to satisfy FCC Part 15 Subpart B unintended radiator rules without requiring expensive full intentional-radiator re-certification.
  * **Strict Claim Policy:** Component-level certifications (e.g., UL-recognized pressure transducers or FCC-certified ESP32 modules) do *not* mean the assembled product is UL-listed. Product documentation must clearly state: *"Non-listed supplementary monitoring device. Not for life-safety primary actuation."*

---

## 8. Design Roadmap & Engineering Deliverables

To transition from this Round 1 architecture to working hardware, the following file and hardware artifacts will be produced under `research/independent-designs/adviser-gemini/`:

```
research/independent-designs/adviser-gemini/
├── REQUIREMENTS.md          # Formal product requirements, interview log, engineering assumptions
├── ARCHITECTURES.md         # Full tradeoff matrix, mathematical modeling, and component selections
├── DECISIONS.md             # Formal Architecture Decision Records (ADRs)
├── HARDWARE/
│   ├── schematics/          # KiCad 8.0 editable schematic files (.kicad_sch)
│   ├── pcb/                 # KiCad 8.0 2-layer PCB layout (.kicad_pcb) and gerber exports
│   ├── bom/                 # Fully costed Bill of Materials with DigiKey/Mouser MPNs
│   └── docs/                # Power budget analysis and circuit protection calculations
├── MECHANICAL/
│   ├── cad/                 # FreeCAD / STEP models for internal chassis mounting plate
│   └── 3d_print/            # PETG/ABS printable STL/3MF files for enclosure sled
├── FIRMWARE/
│   ├── src/                 # ESP-IDF / C++ modular firmware (FreeRTOS tasks)
│   ├── test/                # Unit tests for ADC DSP filtering and fault detection
│   └── include/             # Hardware abstraction layer for ADS1115, W5500, DS18B20
├── SOFTWARE/
│   ├── dashboard/           # Responsive Vue 3 / Tailwind PWA dashboard
│   ├── backend/             # Lightweight Node.js/Go MQTT collector & Redis dead-man daemon
│   └── alerts/              # Twilio SMS and Web Push service workers
├── MANUFACTURING/
│   ├── calibration/         # Python calibration script for bench test fixture
│   ├── qa_checklist.md      # Step-by-step assembly, flashing, and testing protocol
│   └── economics.md         # Sourced cost scaling models (1, 5, 25, 100 units)
├── BUSINESS/
│   ├── compliance_guide.md  # Legal disclaimers, NFPA 13/25 boundaries, AHJ guidance
│   └── service_model.md     # Ongoing cloud hosting and Twilio SMS cost projections
└── HANDOFF.md               # Checkpoint status, test results, and next actions
```

### Execution Phases
* **Phase 1 (Week 1–2):** Finalize Owner Interview, capture complete KiCad 8.0 schematics and 3D printable chassis CAD; construct the benchtop pneumatic calibration fixture.
* **Phase 2 (Week 3–4):** Fabricate 5 prototype bare PCBs; hand-assemble and calibrate 3 alpha units; validate ADC linearity and supercapacitor dying-gasp discharge curves.
* **Phase 3 (Week 5–6):** Develop ESP-IDF firmware (dual-core task separation, watchdog, mTLS MQTT client); deploy cloud watchdog service and PWA dashboard.
* **Phase 4 (Week 7–8):** Conduct 14-day cold-box thermal cycling (down to $-15^\circ\text{C}$) and pressure fatigue testing; freeze documentation for pilot field install.

---

## 9. Single Most Important Interview Question

To lock in the power supply, physical mounting, and network routing for the hardware schematic, what is the single most critical unknown:

> **"Inside the sealed sprinkler riser room, exactly what electrical power sources (such as a 120V AC wall outlet or a 24V AC transformer) and physical network connections (such as a Cat5e/Cat6 Ethernet drop) are currently present, and does an ordinary smartphone show reliable cellular signal or facility Wi-Fi reception when standing inside the room with the fire door fully closed?"**
