# **Response: Clean-Room Engineering Proposal: Dry-Pipe Sprinkler Riser Room Monitor (Round 1\)**

**Advisor Identifier:** adviser-gemini

**Target Repository Path (for coordinator persistence):** research/independent-designs/adviser-gemini/

**Disclosure Statement:** This Round 1 document is generated in a clean-room environment with zero access to the target GitHub repository (JamieT1701/SprinklerSystemMonitor), existing prototypes, or competing advisor outputs. No direct GitHub commits have been made by this model instance; all cost figures, component prices, and regulatory notes are engineering estimates based on standard industry data and require vendor quote verification and qualified regulatory review prior to procurement or installation.

## **1\. TL;DR Architecture Recommendation**

> * **Problem Statement:** Commercial dry-pipe fire sprinkler systems rely on pressurized air or nitrogen (observed around 50 PSI at the owner's site, though site-specific) to hold the dry-pipe clapper valve closed against municipal water pressure, while the unconditioned riser room itself faces freezing risks that can rupture the wet supply side or freeze condensed moisture in the air manifold. A silent compressor failure, slow air leak, or sustained freeze event can result in an unintended valve trip—flooding the cold piping network and activating an external diverter/drain—or freezing the supply main before a human notices.  
> * **Recommended Architecture (Architecture B — Industrial 4–20 mA \+ Dual-Path Ethernet/Wi-Fi \+ LiFePO4 UPS):** A single-board carrier PCB hosting an **ESP32-S3-WROOM-1** module paired with a **WIZnet W5500 hardwired SPI Ethernet controller** (providing deterministic wired connectivity with Wi-Fi fallback), reading an industrial **0–100 PSIG 4–20 mA stainless-steel pressure transducer** via an externally protected **TI ADS1118 16-bit ADC** with a high-precision low-drift current sense resistor, and a digital **Sensirion SHT40 / DS18B20** ambient temperature probe. Power is supplied by an external UL-listed 12V DC wall adapter backed by an onboard single-cell **3.2V LiFePO4 (18650/26650) UPS circuit** capable of 24+ hours of runtime during a riser room power outage (critical because compressor failure and room freeze often coincide with AC power loss).  
> * **Offsite Heartbeat & Cloud:** The device publishes telemetry over TLS (MQTT or HTTPS POST) every 60 seconds to a lightweight serverless backend (Cloudflare Workers \+ D1 SQLite \+ Cron Triggers). An independent server-side cron job runs every 2 minutes to evaluate sample freshness; if a device misses 3 consecutive check-ins, the cloud directly dispatches an offline alert via **Twilio SMS** and **Web Push (PWA VAPID)** without relying on the dead device.  
> * **Target Repository Path:** research/independent-designs/adviser-gemini/ (to be committed by the experiment coordinator on branch research/independent-adviser-gemini).  
> * **Immediate First Interview Question:** See Section 9 (establishes the physical/mechanical boundary at the riser manifold, compressor cut-in/cut-out behavior, and available AC power/network drops in the riser room).

## **2\. Key Measurable Product Requirements & Prioritized Unknowns**

### **2.1 Measurable System Requirements (Preliminary Baseline)**

| Requirement ID | Category | Parameter | Target Specification | Verification Method |
| :---- | :---- | :---- | :---- | :---- |
| **REQ-PRS-01** | Pressure Sensing | Operating & Overpressure Range | 0 to 100 PSIG working range; \>= 200 PSIG proof pressure; \>= 300 PSIG burst pressure | Transducer datasheet \+ hydrostatic/pneumatic bench test |
| **REQ-PRS-02** | Pressure Sensing | Total System Accuracy | \<= \+/- 1.0% Full Scale (+/- 1.0 PSI) across 0°C to 50°C; resolution \<= 0.1 PSI | 3-point deadweight or NIST-traceable digital gauge comparison |
| **REQ-PRS-03** | Pressure Sensing | Fault Detection (Loop Integrity) | Detect open wire (I\_loop \< 3.6 mA) and short circuit (I\_loop \> 21.0 mA) within 2 seconds | Bench fault-injection switch matrix (open/short/reverse) |
| **REQ-PRS-04** | Analytics | Trend & Rate-of-Change Detection | Compute 15-min and 60-min rolling linear regression slope (PSI/hr) to detect slow leaks or compressor duty-cycle failure before crossing hard low-pressure alarm | Simulated pressure decay ramp in firmware test harness |
| **REQ-TMP-01** | Temperature Sensing | Range & Accuracy | \-20°C to \+70°C (-4°F to \+158°F); accuracy \<= \+/- 0.5°C between \-10°C and \+40°C | Ice-bath (0°C) and ambient reference thermometer verification |
| **REQ-TMP-02** | Temperature Sensing | Persistence / Soak Timer | Configurable degree-minute or continuous duration timer (e.g., \< 40°F / 4.4°C continuously for \>= 30 minutes) with 2°F hysteresis | Thermal chamber or ice-pack step-response test |
| **REQ-PWR-01** | Power & UPS | Primary Input & Battery Backup | 12V DC nominal input (9–24V wide input); onboard LiFePO4 battery backup providing \>= 24 hours autonomous monitoring \+ AC-loss telemetry flag | Full discharge runtime test at 60s reporting interval |
| **REQ-ENV-01** | Environmental | Enclosure & Condensation | IP65 / NEMA 4X polycarbonate enclosure with Gore-Tex breather vent, conformal-coated PCB, operating \-10°C to \+55°C at up to 95% RH non-condensing | Visual inspection, water spray test, thermal soak |
| **REQ-NET-01** | Connectivity | Heartbeat & Offline Detection | 60s normal telemetry interval; 10s fast-publish on threshold crossing; independent cloud dead-man switch triggers offline alert within \<= 180s of silence | Pull power \+ network cable; measure time to SMS receipt |
| **REQ-SEC-01** | Security | Transport & Provisioning | TLS 1.3 with device-unique client certificates or rotatable bearer tokens; signed OTA firmware updates with automatic A/B partition rollback on boot failure | Corrupt OTA image test \+ expired cert rejection test |

### **2.2 Prioritized Unknowns Log (To Be Resolved via Owner Interview)**

> 1. **UNK-01 (Mechanical/Hydraulic Interface):** How is the supervisory pressure tap going to be plumbed? Is there an existing spare plugged NPT port on the dry-pipe valve trim (system air side, above the clapper/check valve), and what thread size is it (typically 1/4" NPT)? What does the site's fire sprinkler contractor permit?  
> 2. **UNK-02 (Pneumatic Dynamics):** What is the exact dry-pipe valve model, differential ratio (typically \~5.5:1 to 6:1 against water supply pressure), air maintenance device (AMD) configuration, and compressor cut-in / cut-out behavior? Does the compressor cycle automatically via a pressure switch, or is it manually topped off?  
> 3. **UNK-03 (Riser Room Utilities):** Is there an unswitched 120V AC receptacle inside the riser room? Is it on the same breaker as the air compressor? What is the Wi-Fi signal strength (RSSI) inside the closed riser room, or can an Ethernet cable be pulled through the wall into the conditioned warehouse?  
> 4. **UNK-04 (Sensor Cable Run & Environment):** How far will the control enclosure be mounted from the pressure tap and from the coldest spot in the riser room (e.g., near the exterior wall/door or main water entry)?  
> 5. **UNK-05 (External Diverter/Drain Behavior):** How is the owner's external diverter/drain plumbed (e.g., connected to the intermediate chamber / alarm line drain), and is there any desire for a future auxiliary contact/wetness sensor on that drain line?  
> 6. **UNK-06 (Commercial Scale & Budget Targets):** Is the initial goal strictly internal deployment (1–5 units) with potential sales to neighboring warehouse owners (25–100 units), and what target BOM cost and monthly SaaS/SMS budget does the owner consider acceptable?

## **3\. Comparison of Three Credible Architectures**

To avoid premature convergence, three genuinely distinct hardware/communications architectures are evaluated below.

### **Architecture A: Ultra-Low-Cost Wi-Fi \+ Ratiometric 0.5–4.5V Analog Sensor**

> * **Concept:** An off-the-shelf or simple carrier with an ESP32-C3/S3 using only 2.4 GHz Wi-Fi, powered by a standard 5V USB-C wall adapter (with an optional 18650 Li-ion powerbank IC). Uses a low-cost automotive-style 0.5–4.5V ratiometric pressure sensor (3-wire: 5V, GND, Signal) read by an external 12/16-bit I2C ADC, and a 1-Wire DS18B20 temperature probe.  
> * **Pros:** Lowest BOM cost (\~$38–$50 at qty 1); simplest schematic; minimal SMT component count; uses inexpensive 3-wire sensors.  
> * **Cons:**  
  * **High vulnerability to EMI and cable voltage drop:** Riser rooms contain high-inrush AC compressor motors. Voltage output sensors suffer ground-loop offsets and capacitive coupling over long cables.  
  * **Ratiometric supply dependency:** A 0.5–4.5V sensor's output scales directly with its 5.0V excitation rail. If the 5V regulator drifts by 2%, the pressure reading drifts by 2% unless the ADC uses the exact sensor supply as its reference rail.  
  * **Wi-Fi attenuation:** Riser rooms are frequently constructed with concrete block (CMU) or fire-rated gypsum/steel doors, causing severe 2.4 GHz attenuation and intermittent dropouts.

### **Architecture B: Industrial 4–20 mA Loop \+ Dual-Path Ethernet/Wi-Fi \+ LiFePO4 UPS (RECOMMENDED)**

> * **Concept:** Custom 2-layer or 4-layer carrier PCB built around an **ESP32-S3-WROOM-1**, paired with a hardwired **WIZnet W5500 Ethernet controller** (RJ45 with PoE splitter option or 12–24V DC barrel jack) AND built-in 2.4 GHz Wi-Fi fallback. Drives an industrial **2-wire 4–20 mA current-loop pressure transducer** from an isolated/boosted 18V–24V excitation rail, measured across a 150 Ohm 0.1% 25ppm/°C sense resistor into a **TI ADS1118 (16-bit SPI ADC with internal PGA and voltage reference)**. Includes a single-cell **3.2V LiFePO4 (26650) battery backup** and a digital I2C/1-Wire temperature sensor with TVS protection.  
> * **Pros:**  
  * **Bulletproof signal integrity:** A 4–20 mA current loop is virtually immune to compressor motor EMI and wire resistance drops up to hundreds of feet.  
  * **Built-in live zero & cable fault diagnostics:** 0 PSIG \= 4.00 mA; 100 PSIG \= 20.00 mA. If a rodent chews the cable or a terminal vibrates loose, current drops to 0.00 mA—immediately distinguishable from 0 PSIG\! If the cable is pinched/shorted, current hits the hardware current limiter (\>22 mA)—instantly flagged as a wiring short.  
  * **Dual-path connectivity \+ safe chemistry UPS:** Hardwired Ethernet solves the concrete riser-room RF barrier while keeping Wi-Fi for easy retrofit. LiFePO4 chemistry withstands cold warehouse temperatures down to \-20°C (with charge inhibit below 0°C) and will not thermally run away.  
> * **Cons:** Slightly higher BOM (\~$75–$95 at qty 1\) due to industrial 4–20 mA transducer and Ethernet \+ boost/UPS circuitry.

### **Architecture C: Cellular IoT (LTE-M / NB-IoT) \+ Industrial RS-485 Modbus Sensors**

> * **Concept:** A cellular-first board (e.g., Nordic nRF9160 SiP or ESP32 \+ SIM7080G LTE-M/CAT-M1 modem) communicating with an RS-485 Modbus RTU pressure transmitter and RS-485 temperature/humidity node, powered by a 12V SLA (Sealed Lead-Acid) battery box and AC charger.  
> * **Pros:** Zero dependency on customer IT networks, warehouse Wi-Fi passwords, or firewall rules; works out-of-the-box at remote or third-party client warehouses; RS-485 supports daisy-chaining multiple digital sensors over 1,000+ ft.  
> * **Cons:**  
  * **Recurring cellular SIM cost & deep-indoor penetration issues:** Even LTE-M (700/800 MHz) can struggle inside windowless steel/concrete riser rooms without an external antenna penetration.  
  * **Higher sensor & modem cost:** Industrial RS-485 pressure transmitters and cellular modules increase unit BOM by $45–$80+ and complicate FCC modular/host compliance if co-locating radios.  
  * **SLA battery bulk:** Lead-acid batteries require larger enclosures and periodic replacement every 3–4 years.

### **3.1 Quantitative Tradeoff Matrix**

*(Scoring: 1 \= Poor, 5 \= Excellent. Weights total 100%.)*

| Evaluation Criterion | Weight | Arch A (Wi-Fi \+ 0.5–4.5V) | Arch B (Eth/Wi-Fi \+ 4–20 mA \+ LiFePO4) | Arch C (LTE-M \+ RS-485 \+ SLA) |
| :---- | :---- | :---- | :---- | :---- |
| **Pressure Accuracy & Drift Immunity** | 15% | 2.5 | **4.8** | 4.8 |
| **Cable Fault & EMI Diagnostics** | 15% | 3.0 | **5.0** | 4.5 |
| **Connectivity Reliability in Riser Room** | 15% | 2.5 | **4.5** | 4.0 |
| **Power Outage / Cold Temp Resilience** | 10% | 2.5 | **4.8** | 4.2 |
| **Supply Chain & Multi-Sourcing** | 10% | 4.5 | **4.8** | 3.5 |
| **DIY Workshop Manufacturability** | 15% | 4.8 | **4.5** | 3.2 |
| **Unit Hardware Cost (1 to 100 qty)** | 10% | **4.8** | 4.0 | 2.5 |
| **Ongoing Operating Cost (Cloud/Comms)** | 5% | **4.8** | **4.8** | 2.8 |
| **Compliance & Regulatory Simplicity** | 5% | 4.5 | **4.5** | 3.0 |
| **WEIGHTED TOTAL SCORE** | **100%** | **3.51 / 5.0** | **4.66 / 5.0 (WINNER)** | **3.80 / 5.0** |

**Winner Rationale:** **Architecture B** wins decisively (4.66 vs 3.80 and 3.51). While a 0.5–4.5V ratiometric sensor uses a simpler circuit, 4–20 mA current loops are the gold standard in industrial fluid/pneumatic monitoring for good reason: immunity to compressor motor noise, long cable runs without voltage drop errors, 2-wire non-polarized simplicity (with a bridge or protection diode), and unambiguous detection of broken vs. shorted vs. 0 PSI states. Pairing Ethernet \+ Wi-Fi on a single board (via ESP32-S3 \+ W5500) ensures the owner can plug into a warehouse switch or PoE injector if the riser room blocks Wi-Fi, while keeping an unpopulated Footprint/UART header for an optional plug-in LTE-M daughterboard for future contractor deployments.

## **4\. Recommended Block-Level Electronics, Sensors, Power & Self-Check**

### **4.1 System Block Diagram (ASCII)**

`+-----------------------------------------------------------------------------------+`  
`|                     SPRINKLER RISER ROOM (DRY-PIPE MANIFOLD)                      |`  
`|                                                                                   |`  
`|  [0-100 PSIG 4-20mA Transducer]        [Remote Ambient Temp Probe (DS18B20/SHT40)]|`  
`|    (1/4" NPT, 316L SS, IP67)              (Mounted at Coldest Wall / Pipe Entry)  |`  
`+----------------+-----------------------------------------+------------------------+`  
                 `| 2-Wire Shielded Cable                   | 3/4-Wire Shielded Cable`  
                 `v                                         v`  
`+================+=========================================+========================+`  
`| [M12 / Spring Terminal Block]             [M12 / Spring Terminal Block]           |`  
`|                |                                         |                        |`  
`|  [TVS SMBJ28A + Polyfuse 50mA]             [TVS PESD5V0 + RC Filter + Polyfuse]   |`  
`|  [Reverse Polarity Schottky]                             |                        |`  
`|                |                                         |                        |`  
`|  [24V Loop Excitation Boost]                             |                        |`  
`|  (TPS61040 / Current-Limited 32mA)                       |                        |`  
`|                |                                         |                        |`  
`|  [150 Ohm 0.1% 15ppm Sense Resistor]                     |                        |`  
`|  [Op-Amp Clamp / RC Anti-Alias Filter]                   |                        |`  
`|                |                                         |                        |`  
`|        +-------+-------+                                 |                        |`  
`|        |  TI ADS1118   | (16-Bit SPI ADC + Internal Temp)|                        |`  
`|        +-------+-------+                                 |                        |`  
`|                | SPI                                     | 1-Wire / I2C           |`  
`|        +-------+-----------------------------------------+-------+                |`  
`|        |                  ESP32-S3-WROOM-1-N16R8                 |                |`  
`|        |       (Dual-Core MCU + 2.4GHz Wi-Fi + BLE Provision)    |                |`  
`|        +-------+-------------------+---------------------+-------+                |`  
`|                | SPI               | I2C / GPIO          | UART (Exp Header)      |`  
`|        +-------+-------+   +-------+-------+     +-------+-------+                |`  
`|        | WIZnet W5500  |   | Ext Watchdog  |     | Optional Slot |                |`  
`|        |  + RJ45 Mag   |   |  (TPL5010)    |     | (LTE-M Modem) |                |`  
`|        +-------+-------+   +---------------+     +---------------+                |`  
`|                |                                                                  |`  
`|  +-------------+---------------------------------------------------------------+  |`  
`|  | POWER & UPS SUBSYSTEM                                                       |  |`  
`|  | [12V Wall Adapter / PoE Splitter] -> [TVS + P-FET Reverse Prot]             |  |`  
`|  |   -> [INA219 Power/Battery Monitor (I2C)]                                   |  |`  
`|  |   -> [CN3058E / BQ25606 LiFePO4 Charger (NTC Cold-Charge Inhibit < 0°C)]    |  |`  
`|  |   -> [3.2V 26650 LiFePO4 Cell (3500 mAh)] -> [TPS63020 Buck-Boost 3.3V Rail]|  |`  
`|  +-----------------------------------------------------------------------------+  |`  
`|                     CUSTOM CARRIER PCB IN NEMA 4X / IP65 ENCLOSURE                |`  
`+===================================================================================+`

### **4.2 Concrete Component Selection & Multi-Sourcing**

> 1. **Pressure Transducer (Field Sensor):**  
   * **Primary Specification:** 0 to 100 PSIG, 4–20 mA 2-wire loop-powered, 1/4" NPT male process connection, 316L stainless steel wetted parts, \+/- 0.5% FS accuracy (BFSL), IP67 weatherproof Packard Metri-Pack or M12 4-pin connector, 9–30V DC excitation.  
   * **Candidate MPNs:** **TE Connectivity / Measurement Specialties M3251-000005-100PG** (Microfused silicon strain gauge, industrial grade) or **Sensata / Kavlico PTE5000 / PT500** series, or **Omega PX309-100GI**, or **Dwyer 626-10-GH-P1-E1-S1** (0–100 PSIG). For lower-cost evaluation prototypes, **DFRobot SEN0257 / YB-131 series (4–20mA industrial variant)** can be bench-tested against a reference gauge, though industrial TE/Sensata transducers are strongly recommended for field durability.  
   * *Why 0–100 PSIG?* For a system operating around 50 PSIG, 0–100 PSIG places normal operation right at the midpoint (50% FS \= 12.00 mA), giving 2x headroom for compressor overshoot/high-pressure alarms while maintaining high resolution down to 0 PSIG and surviving 200+ PSIG water hammer if the valve trips and water enters the gauge line (though a check/snubber should be used).  
> 2. **Analog Front-End (4–20 mA Receiver & ADC):**  
   * **ADC:** **Texas Instruments ADS1118IDGSR** (VSSOP-10, hand-solderable with flux and drag soldering, or **ADS1115IDGSR** I2C variant). Features an integrated precision programmable gain amplifier (PGA), low-drift internal voltage reference (2.048V or 4.096V range), and a built-in on-die temperature sensor (used to verify PCB enclosure internal temperature and compensate resistor drift).  
   * **Sense Resistor:** **Bourns / Vishay 150 Ohm, 0.1% tolerance, \+/- 15 ppm/°C** precision thin-film resistor (0805 or 1206 package, e.g., Susumu RG2012P-151-B-T5).  
   * **Signal Math:**  
     * At 0 mA (Open Loop Fault): *Vsense*​\=0.00 V  
     * At 4.00 mA (0.0 PSIG): *Vsense*​\=0.004 A×150 Ω=0.600 V  
     * At 12.00 mA (50.0 PSIG): *Vsense*​\=0.012 A×150 Ω=1.800 V  
     * At 20.00 mA (100.0 PSIG): *Vsense*​\=0.020 A×150 Ω=3.000 V  
     * At 22.00 mA (Over-range / Short Fault): *Vsense*​\=3.300 V  
   * Using the ADS1118/1115 on the \+/- 4.096V full-scale PGA setting (1 LSB \= 0.125 mV), the 4–20 mA span (2.400V) covers **19,200 discrete ADC counts**, yielding an electrical resolution of **0.0052 PSI per count**—far exceeding the transducer's mechanical accuracy and eliminating quantization noise.  
> 3. **Ambient Temperature Sensor (Riser Room):**  
   * **Primary:** **Maxim/Analog Devices DS18B20+** in a stainless-steel waterproof probe with PTFE/PVC jacketed cable (3-wire active parasitic-free mode: 3.3V, GND, DQ with 4.7k pull-up), OR **Sensirion SHT40-AD1B** (I2C temperature \+ relative humidity sensor on an external probe housing).  
   * **Recommendation:** Support **both** on the terminal block—use a ruggedized **DS18B20+ stainless probe** for external wall/pipe-entry ambient sensing (1-Wire tolerates 10–30 ft cables easily with an RC slew-rate filter), AND mount an **SHT40** inside the breather-vented enclosure (or short probe) to track both temperature and relative humidity/dew point margin.  
> 4. **Microcontroller & Dual-Network Interface:**  
   * **MCU:** **Espressif ESP32-S3-WROOM-1-N16R8** (16 MB Quad-SPI Flash for generous A/B OTA partitions \+ local ring-buffer flash logging; 8 MB PSRAM). Built-in USB-JTAG/Serial simplifies single-cable workshop flashing without an external UART bridge chip.  
   * **Wired Ethernet:** **WIZnet W5500** hardwired TCP/IP SPI Ethernet controller \+ **HanRun HR911105A** RJ45 MagJack (or drop-in W5500 Lite module header for super-fast DIY assembly).  
   * **Hardware Watchdog:** **Texas Instruments TPL5010DDCR** nano-power hardware watchdog timer connected to the ESP32-S3 EN (hard reset) pin. Even if the ESP32 RTOS locks up completely in a peripheral driver or Brownout state, the TPL5010 physically toggles EN if not petted every 30 seconds.  
> 5. **Power Path, LiFePO4 UPS & Cold-Temperature Charging Protection:**  
   * **Primary Input:** External UL-listed 12V DC, 1.5A wall adapter (or 802.3af PoE splitter outputting 12V DC).  
   * **Why LiFePO4 (3.2V nominal) instead of standard 3.7V Li-Ion/LiPo?**  
     1. Standard Li-ion cells degrade rapidly when float-charged continuously at 4.2V for years; LiFePO4 thrives in standby float applications for 5–8+ years (2,000+ cycles).  
     2. LiFePO4 is chemically and thermally stable (no thermal runaway/fire risk inside a fire-protection riser room).  
     3. LiFePO4 voltage (3.2V nominal, 3.6V full, 2.8V empty) feeds efficiently into a buck-boost regulator (**TI TPS63020** or **TPS63070**) to generate a rock-solid 3.3V logic rail.  
   * **Cold-Temperature Charge Protection (Critical Riser Room Detail):** Charging *any* lithium battery below 0°C (32°F) causes metallic lithium plating on the anode, permanently damaging the cell. Discharging down to \-20°C (-4°F) is completely safe for LiFePO4. Therefore, our charger IC (**Consonance CN3058E** or **TI BQ25606** configured for LiFePO4, or MCU-gated P-MOSFET charge enable) includes a **10k NTC thermistor strapped to the 26650 cell**. If cell temperature drops below \+2°C (35.6°F), charging is inhibited automatically while battery backup discharge remains fully active.  
   * **Power & Battery Health Telemetry:** An onboard **TI INA219** or dual ADC divider monitors both the 12V DC input rail (detecting AC power outage within \< 1 second) and the LiFePO4 battery voltage/current.  
   * **Switched 24V Loop Boost Supply:** A small boost converter (**TI TPS61040** or **MT3608**) steps 3.3V/5V up to **18V–24V DC** at up to 35 mA specifically to excite the 4–20 mA pressure transducer, allowing the pressure loop to continue operating seamlessly when running on the 3.2V LiFePO4 battery during a blackout.

### **4.3 Field Interface Protection Circuits & Concrete Fault Detection Behavior**

Riser rooms present real electrical hazards: miswiring during installation, induced surges from compressor contactors, ESD, and rodent-damaged cables. Every external terminal passes through dedicated protection:

  `[Field Terminal +24V_LOOP_OUT] <--- [PTC Polyfuse 50mA (Bourns MF-MSMF005)] <--- [Current Limit ~28mA] <--- +24V Boost`  
                                                `|`  
                                        `[TVS Diode SMBJ28A]`  
                                                `|`  
                                               `GND`

  `[Field Terminal 4-20mA_IN] -------> [Series 47 Ohm Surge Resistor]`  
                                                `|`  
                                        `[TVS Diode SMBJ15A to GND]`  
                                                `|`  
                                        `[Schottky Clamp BAT54S to 3.3V & GND]`  
                                                `|`  
                                        `[150 Ohm 0.1% Sense Resistor to GND] ---> [1k + 100nF RC Filter] ---> ADS1118 AIN0`

#### **Concrete Detection Table for Field & Internal Faults**

| Fault / Anomaly Condition | Physical / Electrical Signature | Concrete Firmware & Cloud Detection Behavior |
| :---- | :---- | :---- |
| **Pressure Cable Cut / Unplugged** | *Iloop*​\<3.60 mA (*Vsense*​\<0.540 V) | Flag SENSOR\_FAULT\_OPEN\_WIRE after 3 consecutive samples (1.5s). Suppress false "0 PSI" low-pressure alarm; emit immediate high-priority **Sensor Disconnected / Cut Cable** push/SMS alert. Never display 0.0 PSI as a valid reading. |
| **Pressure Cable Shorted / Miswired** | *Iloop*​\>21.00 mA (*Vsense*​\>3.150 V) & PTC / current limiter engages | Flag SENSOR\_FAULT\_OVERCURRENT\_SHORT. MCU disables 24V boost converter for 10s to cool protection circuitry, retries once, and sends **Sensor Wiring Short / Overrange** alert. |
| **Transducer Out-of-Cal / Negative Drift** | 3.60 mA≤*Iloop*​\<3.90 mA (-0.6 to \-2.5 PSIG equivalent) | Flag SENSOR\_WARN\_ZERO\_DRIFT. Display raw reading with a yellow warning badge (Zero Calibration Drift Detected). |
| **ADC Stuck / SPI Bus Failure** | ADS1118 returns identical raw hex across 60 samples (zero thermal/LSB noise) OR fails SPI CRC/readback of config register | Firmware cross-checks ADS1118 internal die temperature register against expected range and toggles PGA gain in a diagnostic cycle. If stuck, triggers HW\_FAULT\_ADC\_FAILURE and alerts owner. |
| **Temp Probe Disconnected / Shorted** | DS18B20 returns no presence pulse, 0xFFFF,CRC mismatch, or power-on reset default (+85.0°C) | Firmware rejects \+85.0°C power-on value and any reading failing 8-bit Dallas CRC. After 3 failed reads, marks temperature INVALID and sends **Temperature Probe Fault** alert. |
| **AC Power Loss (Compressor Outage Risk)** | *Vin*\_12*V*​\<8.5 V while *Vbatt*​≥3.0 V | Immediately transmits POWER\_EVENT\_AC\_LOST alert ("Riser room AC power lost — running on LiFePO4 battery backup"). Switches sampling/reporting to power-save profile if outage exceeds 4 hours. |
| **Slow Air Leak / Compressor Failing to Keep Up** | Pressure remains above static low threshold (e.g., 42 PSI) but exhibits continuous negative slope (e.g., \<−1.5 PSI/hr for 3 hours) or fails to reach compressor cut-out | Firmware calculates 15-min and 60-min rolling slopes and tracks time-since-last-recharge peak. Raises an **Early Warning: Abnormal Pressure Decay Trend** before reaching critical low-pressure threshold. |
| **Device Frozen / Wi-Fi+Eth Lost / Destroyed** | Cloud backend receives zero HTTPS/MQTT heartbeats for \>180 seconds | Independent Cloudflare Worker Cron job transitions site state to SITE\_OFFLINE, records last known PSI/Temp, and dispatches **Site/Device Unreachable** SMS \+ Push via Twilio. |

## **5\. Workshop Manufacturing, Calibration/Test Fixture & Multi-Tier Economics**

### **5.1 Design for Single-Operator Workshop Manufacturing (DFM)**

To ensure a single proficient operator can build, test, and repair units without an industrial line:

> 1. **PCB Layout Constraints:**  
   * **2-Layer FR4 PCB**, 1.6 mm thickness, 1 oz copper, HASL or ENIG finish, sized to fit standard **Hammond 1554 / Polycase / Bud Industries** NEMA 4X flanged polycarbonate enclosures (e.g., 120 mm x 80 mm board footprint).  
   * **Minimum SMT Passive Size:** **0805** (imperial) for all resistors, capacitors, and ferrite beads. Zero 0402 or 0201 parts, and zero hidden-pad BGAs (except the pre-certified ESP32-S3-WROOM-1 castellated module, which has large edge castellations).  
   * **Clear Silkscreen & Test Points:** Every power rail (+12V\_IN, \+24V\_LOOP, \+3V3, VBAT), SPI/I2C line, and VSENSE node has a labeled **1.5 mm plated through-hole test loop** or surface test pad on the top side for pogo-pin or multimeter probing.  
> 2. **Enclosure & Cable Entry Strategy:**  
   * Use an off-the-shelf **IP65/IP67 polycarbonate enclosure with a clear or opaque hinged/screw lid** and molded wall-mounting flanges (never drill mounting holes through the back inside the dry box cavity).  
   * Drill step-bit holes in the bottom face only (so gravity sheds water away from seals) using a **3D-printed drill jig** that snaps over the bottom of the enclosure for 100% repeatable hole spacing.  
   * Install **IP68 nylon PG7/M12 cable glands** (for low-cost permanent wiring) OR **panel-mount M12 4-pin aviation circular connectors** (for plug-and-play field replacement of sensors without opening the enclosure in the riser room).  
   * Include a **vented M12 pressure-equalization breather plug (ePTFE membrane)** on the bottom face to prevent barometric pressure differentials from sucking moist riser-room air past the gasket during rapid temperature swings.  
   * Apply a brush/spray **silicone conformal coating (MG Chemicals 422C)** to the high-impedance analog and power sections of the PCB, masking terminal blocks, connectors, and breather sensors with 3D-printed silicone/TPU masks.

### **5.2 Repeatable Bench QA & Calibration Fixture**

A single operator cannot afford 2 hours of manual jumper-wiring per board. We design a **3D-Printed \+ Custom PCB Bench Test & Calibration Jig** that validates a unit in **under 4 minutes**:

> 1. **Electrical Current-Loop Simulator Sub-Circuit (on the Test Jig):**  
   * Includes a rotary switch or precision resistor ladder switched by relays/toggle switches that injects **4 exact reference currents** into the unit's pressure terminal block:  
     * **Pos 1 (Open Fault):** 0.00 mA (verifies SENSOR\_FAULT\_OPEN\_WIRE triggers within 2s)  
     * **Pos 2 (Zero Point):** 4.000 mA \+/- 0.05% (calibrates/verifies 0.0 PSIG)  
     * **Pos 3 (Mid-Scale):** 12.000 mA \+/- 0.05% (verifies 50.0 PSIG linearity)  
     * **Pos 4 (Full-Scale):** 20.000 mA \+/- 0.05% (calibrates/verifies 100.0 PSIG)  
     * **Pos 5 (Short Fault):** Direct shunt across loop terminals (verifies current limiter & SENSOR\_FAULT\_OVERCURRENT\_SHORT)  
> 2. **Pneumatic Verification Manifold (Physical End-to-End Test):**  
   * A desktop aluminum 4-port 1/4" NPT manifold connected to a shop air regulator (or bicycle shock pump with fine bleed valve), a **NIST-traceable digital reference gauge** (e.g., Dwyer DPG-000 or Fluke 700G, \+/- 0.25% or better), and 2 quick-disconnect ports for the actual 4–20 mA transducers being shipped with the units.  
   * The operator pressurizes the manifold to **0 PSI, 30 PSI, 50 PSI, and 80 PSI**, runs a single Python script (qa\_calibrate.py) over USB-C, and the script:  
     1. Reads the ESP32-S3 MAC address and assigns a monotonic Serial Number (SSM-YYYYMM-XXXX).  
     2. Records the two-point linear calibration constants (*m*,*b*) into the ESP32-S3 NVS (Non-Volatile Storage) partition and logs a signed JSON/PDF calibration certificate locally.  
     3. Verifies AC power cutover to LiFePO4 battery backup via INA219 telemetry.  
     4. Prints a Brother P-Touch / Zebra thermal laminated label with Serial Number, MAC, QR Provisioning Code, and Calibration Date.

### **5.3 Estimated Material, Labor, Tooling & Service Economics (1, 5, 25, 100 Units)**

*Note: All numbers below are transparent engineering estimates in USD (2026 baseline) based on typical catalog pricing from DigiKey, Mouser, JLCPCB/PCBWay, and industrial sensor suppliers. Exact prices must be verified with live distributor carts prior to purchasing.*

#### **Bill of Materials (BOM) Breakdown per Unit (Estimated USD)**

| Subsystem / Item | Qty 1 (Hand-Built) | Qty 5 (Small Batch) | Qty 25 (Turnkey PCBA) | Qty 100 (Pilot Prod) | Notes / Representative Source |
| :---- | :---- | :---- | :---- | :---- | :---- |
| **Bare PCB \+ SMT Assembly** | \$8.00 (bare) | \$3.50 (bare) | \$14.50 (PCBA) | \$9.80 (PCBA) | Qty 1–5 hand-soldered or stencil; Qty 25–100 turnkey SMT PCBA |
| **ESP32-S3-WROOM-1 \+ W5500 \+ MagJack** | \$9.50 | \$8.80 | \$7.60 | \$6.80 | LCSC / DigiKey / Mouser |
| **ADS1118 \+ 0.1% Sense R \+ TPL5010 \+ INA219** | \$7.80 | \$7.00 | \$5.80 | \$4.90 | TI / Bourns precision analog & watchdog |
| **Power / Boost / LiFePO4 Charger \+ TVS \+ Passives** | \$9.20 | \$8.10 | \$6.40 | \$5.20 | TPS63020, TPS61040, SMBJ TVS, PTCs, terminals |
| **3.2V LiFePO4 26650 Cell (3500mAh) \+ Holder** | \$7.50 | \$6.80 | \$5.90 | \$5.00 | UL1642 recognized cell \+ heavy-duty clips/strap |
| **0–100 PSIG 4–20 mA Stainless Transducer \+ Cable** | \$45.00 | \$40.00 | \$32.00 | \$24.00 | Industrial 316L SS 1/4" NPT (major BOM driver; varies by brand) |
| **Waterproof DS18B20 Probe \+ SHT40 Sensor** | \$6.50 | \$5.50 | \$4.20 | \$3.40 | Stainless 3m probe \+ internal humidity/temp |
| **NEMA 4X / IP65 Enclosure \+ Glands \+ Breather \+ DIN** | \$18.50 | \$16.50 | \$14.00 | \$11.50 | Polycase / Hammond \+ IP68 glands \+ ePTFE vent |
| **UL-Listed 12V DC Power Supply \+ Mounting Hardware** | \$9.50 | \$8.50 | \$7.50 | \$6.50 | Level VI DOE / UL 62368-1 external wall adapter |
| **ESTIMATED HARDWARE BOM / UNIT** | **\$121.50** | **\$104.70** | **\$97.90** | **\$77.10** | *(Includes industrial sensor, battery, enclosure, PSU)* |

#### **Total Program Economics: Labor, Tooling, Rework & Ongoing Service**

*(Assumes internal workshop labor valued at an opportunity/shop rate of **\$50.00/hr** for transparency; if the owner views their own labor on Qty 1–5 as \$0 cash outlay, both Cash Outlay and Fully Burdened Cost are shown.)*

| Cost Category | Qty 1 | Qty 5 | Qty 25 | Qty 100 | Assumptions & Scaling Method |
| :---- | :---- | :---- | :---- | :---- | :---- |
| **Unit Hardware BOM** | \$121.50 | \$104.70 | \$97.90 | \$77.10 | Qty 25 & 100 include turnkey SMT PCBA fee inside BOM |
| **One-Time NRE / Bench Fixture / Tooling (Total)** | \$180.00 | \$240.00 | \$350.00 | \$500.00 | Reference digital gauge ($110),pneumaticmanifold($45), test jig PCB \+ 3D prints |
| **Amortized Tooling per Unit** | \$180.00 | \$48.00 | \$14.00 | \$5.00 | Total NRE divided by batch size |
| **Hands-On Labor Time per Unit** | 3.0 hrs | 1.5 hrs | 0.45 hrs | 0.35 hrs | Qty 1–5: stencil/solder \+ drill \+ test; Qty 25–100: THT/box-build \+ 4-min QA jig |
| **Labor Cost per Unit (@ \$50/hr)** | \$150.00 | \$75.00 | \$22.50 | \$17.50 | Mechanical assembly, flashing, pneumatic QA, labeling |
| **Scrap / Rework Yield Allowance** | 10% (\$12.15) | 6% (\$6.28) | 3% (\$2.94) | 2% (\$1.54) | Accounts for spare boards, damaged glands, or failed QA |
| **Cash Out-of-Pocket per Unit (Excl. Owner Labor)** | **\$313.65** | **\$158.98** | **\$114.84** | **\$83.64** | Pure material \+ amortized tooling \+ yield allowance |
| **Fully Burdened Unit Cost (Incl. \$50/hr Labor)** | **\$463.65** | **\$233.98** | **\$137.34** | **\$101.14** | Complete economic cost per finished, calibrated unit |
| **Total Batch Cash Outlay** | **\$313.65** | **\$794.90** | **\$2,871.00** | **\$8,364.00** | Total capital required before labor |

#### **Ongoing Cloud & Notification Operating Costs (Estimated)**

> * **Cloud Backend & Offsite Heartbeat Monitor (Cloudflare Workers \+ D1 \+ Cron):**  
  * **1 to 25 Units:** **\$0.00 to \$5.00 / month total** (1 unit checking in every 60s \= 43,200 requests/month; 25 units \= 1.08M requests/month, well within Cloudflare's Free or \$5/mo Workers Paid tier).  
  * **100 Units:** **\$5.00 / month total** (\~4.32M requests/month).  
> * **Mobile Web Push (PWA W3C VAPID):** **\$0.00 / message** (completely free across iOS 16.4+ Home Screen Web Apps, Android Chrome, and Desktop browsers).  
> * **SMS & Voice Escalation (Twilio / AWS End User Messaging):**  
  * US 10DLC Phone Number Rental \+ Campaign Registration: **\~$1.15/mopernumber+~$15 one-time 10DLC brand/campaign registration** (Plus \~$4–$15/mo low-volume campaign fee depending on carrier tier).  
  * Per-SMS Segment Cost (US): **\~$0.0079+~$0.003 carrier pass-through fee \= \~\$0.011 per SMS**.  
  * *Practical Reality:* Even if a site sends 50 SMS alerts/tests per month, usage is **\~\$0.55/mo per site**, plus the shared \~$3–$15/mo platform/10DLC base fee.

## **6\. Responsive Dashboard, Mobile Notifications & Security Architecture**

### **6.1 End-to-End Software & Offsite Heartbeat Architecture**

A device inside a riser room cannot alert anyone if its power fails AND its battery dies, or if the warehouse internet router goes down. Therefore, **state evaluation is split cleanly between the Edge Device and the Independent Cloud Watchdog**:

> 1. **Edge Device Responsibilities (ESP32-S3):**  
   * Samples pressure (10 Hz oversampled and boxcar-filtered to 1 Hz) and temperature (every 5 seconds).  
   * Publishes a signed/authenticated JSON telemetry packet every **60 seconds** over HTTPS POST (or MQTT over TLS) containing: device\_id, seq\_num, uptime\_s, pressure\_psig, loop\_current\_ma, pressure\_slope\_psi\_hr, temp\_ambient\_c, temp\_enclosure\_c, rh\_percent, vin\_12v, vbatt\_v, ac\_power\_ok, sensor\_fault\_flags.  
   * **Immediate Fast-Publish Interrupt:** If any threshold or hardware fault state changes, the device does not wait for the 60-second timer—it transmits immediately within \< 2 seconds.  
   * **Local NVS Ring Buffer:** If the internet connection is down, the ESP32-S3 stores up to **7 days of 1-minute summaries** in flash and backfills the timeline upon reconnection.  
> 2. **Independent Offsite Heartbeat Monitor (Serverless Cron Watchdog):**  
   * A scheduled cloud job executes **every 60 seconds** independently of incoming device traffic.  
   * It queries the sites table for any active device where now() \- last\_seen\_at \> offline\_timeout\_seconds (default: 180 seconds \= 3 missed heartbeats).  
   * If exceeded, the backend transitions connectivity\_status to OFFLINE, logs an immutable audit event, and immediately dispatches **Device/Site Offline** notifications via Web Push and SMS, explicitly noting the last known pressure, temperature, and AC power status prior to loss of contact (e.g., *"Site A Offline at 03:14 AM. Last known status: AC Power LOST, Pressure 49.2 PSI, Temp 36.1°F"*).

### **6.2 Browser-Based Responsive Dashboard (PWA)**

Built as a lightweight, fast-loading **Progressive Web App (PWA)** (TypeScript \+ Preact/React or Svelte \+ Tailwind CSS) that works identically on desktop browsers, iPads, Android phones, and iPhones:

> * **At-a-Glance Hero Status Banner:**  
  * Color-coded semantic state (NORMAL \= Green, WARNING / TREND ADVISORY \= Amber, CRITICAL ALARM \= Red, STALE / OFFLINE / SENSOR FAULT \= High-Contrast Purple/Striped Warning).  
  * **Strict Anti-Stale UI Rule:** If sample age exceeds 180 seconds or a sensor fault flag is active, the primary PSI or Temperature number is **visually crossed out / dimmed with an explicit STALE (14m ago) or SENSOR WIRE FAULT badge**. The UI is strictly forbidden from displaying a stale or faulted value in normal green typography.  
> * **Live Telemetry Cards:**  
  * **Dry-Pipe Air Pressure:** Current PSIG (to 0.1 PSI), raw loop current (11.98 mA), 1-hour trend slope (-0.2 PSI/hr), and normal operating band indicator bar.  
  * **Riser Room Ambient Temperature:** Current °F / °C, time spent below cold warning threshold (e.g., Below 40°F for 12m / 30m threshold), and enclosure internal dew-point margin.  
  * **System & Power Health:** AC Mains status (12.1V OK vs ON BATTERY BACKUP), LiFePO4 State of Charge (3.32V / 95%), Network path (Ethernet Active / Wi-Fi Standby), and Last Sample Counter (Updated 14s ago).  
> * **Interactive Trend Charts & Event History:**  
  * **24-Hour / 7-Day / 30-Day Zoomable Chart:** Plots Pressure (PSIG) and Temperature (°F) on dual axes with shaded horizontal bands showing the configured High/Low Pressure thresholds and Cold Exposure threshold. Clearly visualizes compressor saw-tooth cycling (cut-in to cut-out frequency)—allowing the owner to spot a leaking system by seeing the compressor cycle 5x more often even before pressure drops below the cut-in point\!  
> * **Threshold, Persistence & Escalation Configuration:**  
  * **Pressure Rules:** High Warning, High Critical, Low Warning (early warning), Low Critical (pre-trip danger), Rapid Decay Rate (PSI/hr), plus hysteresis (e.g., must recover by \+2.0 PSI for 2 minutes to clear).  
  * **Cold Riser Room Rules:** Temperature threshold (e.g., 38°F) \+ **Persistence Duration Timer** (e.g., must remain \< 38°F continuously for 45 minutes before alerting to install/turn on heater) \+ Emergency Freeze Floor (e.g., \< 33°F alerts after 5 minutes).  
  * **Alert Acknowledgement & Escalation:** Users can click **"Acknowledge & Snooze Repeats for X Hours"** directly from the dashboard or via SMS reply (ACK). If a critical alarm is not acknowledged within 15 minutes, the backend escalates to secondary contacts.  
> * **Multi-Site & Contractor Path:**  
  * Database schema uses a clean organization\_id \-\> site\_id \-\> device\_id hierarchy from Day 1\. A single-site owner sees their riser room immediately upon login; a multi-warehouse owner or sprinkler service contractor sees a **Fleet Rollup Grid** sorted by worst status first, with role-based access (Owner, Maintenance Manager, View-Only Technician).

### **6.3 Practical Mobile Web-Push & SMS Realities**

| Channel | Technical Implementation | Practical Limitations & Mitigation |
| :---- | :---- | :---- |
| **Mobile Web Push (W3C VAPID)** | Standard Service Worker \+ Web Push API. Supported on Desktop (Chrome/Edge/Firefox/Safari), Android (Chrome), and **iOS 16.4+ Safari** | **iOS Caveat:** Apple requires the user to tap Share \-\> Add to Home Screen for Web Push to function on iPhone, and Web Push respects iOS Focus/Do Not Disturb modes unless configured. **Mitigation:** The dashboard includes a 2-step visual onboarding wizard for iPhone users AND a "Send Test Notification" button, while pairing Web Push with SMS for critical alarms. |
| **SMS & Automated Voice Call (Twilio / AWS)** | REST API triggered by cloud alert engine; supports SMS text \+ optional automated text-to-speech voice call for unacknowledged critical low-pressure alarms | **10DLC & Carrier Filtering:** US cellular carriers block unregistered A2P SMS traffic. Requires registering a Toll-Free Verified number or 10DLC campaign. **Mitigation:** Include a backup email-to-push path (or Pushover / ntfy.sh webhook integration) alongside SMS so delivery never depends on a single carrier path, and allow optional automated voice call (Twilio Voice) so the owner can save the number in their phone's **"Emergency Bypass" (rings even on Silent/DND)** contact list. |

### **6.4 Security & Provisioning**

> * **Zero Hardcoded Shared Secrets:** During the 4-minute bench QA script (qa\_calibrate.py), the fixture generates a **unique device cryptographic token / ECDSA keypair** and writes it to the ESP32-S3 flash encryption / NVS partition while registering the public key/hash in the backend.  
> * **Local BLE / Captive Portal Wi-Fi Provisioning:** If Ethernet is not used, the owner holds a physical recessed PROVISION button inside the enclosure for 3 seconds to enable BLE/SoftAP provisioning for 10 minutes (auto-shutoff thereafter).  
> * **Signed OTA with Automatic Rollback:** Firmware uses ESP-IDF's dual ota\_0 / ota\_1 partition table with RSA-3072 / ECDSA signature verification and CONFIG\_BOOTLOADER\_APP\_ROLLBACK\_ENABLE. New firmware must successfully boot, read the ADC, and complete one TLS checkin to the cloud before calling esp\_ota\_mark\_app\_valid\_cancel\_rollback(). If a bad update crashes, the bootloader automatically reverts to the previous working image.

## **7\. Failure Modes (FMEA) & Regulatory / Compliance Constraints**

### **7.1 Failure Modes and Effects Analysis (FMEA)**

| Failure Mode | Potential Cause | Local / Remote Effect | Design Mitigation & Detection |
| :---- | :---- | :---- | :---- |
| **Water/Moisture Entry into Pressure Sensor during Trip** | If the dry valve trips, water enters the system piping and can reach the transducer port; freezing water in a dead-leg port can rupture a sensor diaphragm | Sensor reading shift or permanent overpressure damage | Use 316L stainless steel welded/microfused diaphragm rated to \>= 200 PSIG proof; plumb transducer vertically upward with a pigtail/drip loop or brass snubber so air remains trapped at the diaphragm and sediment cannot settle inside. |
| **Pneumatic Leak Introduced by Our Own Tap** | Poor thread sealing or vibration on the new 1/4" NPT transducer port causes the exact air leak we are trying to prevent | Accelerated compressor cycling or unintended dry-valve trip | Require installation by/under guidance of a licensed sprinkler technician using UL-classified pipe thread sealant/PTFE tape; install a dedicated **quarter-turn brass isolation ball valve \+ bleed port** (supervised open or lockwired) so the sensor can be soap-bubble leak-tested and replaced without depressurizing the dry-pipe system. |
| **Condensation Short on Carrier PCB** | Cold riser room warms rapidly on a humid spring day, condensing moisture on cold electronics | Leakage currents corrupt high-impedance analog signals or corrode pins | Apply MG Chemicals 422C silicone conformal coating to the PCB; use IP65 enclosure with an ePTFE breathable vent membrane; keep \~0.5W of normal ESP32/W5500 self-heating inside the sealed box (keeps internal PCB 2–4°C above ambient dew point). |
| **LiFePO4 Cell Charged Below Freezing** | Riser room drops to 20°F (-6°C) during a power restoration event | Permanent lithium anode plating and capacity loss | Dedicated 10k NTC thermistor on the battery cell inhibits charging hardware when *Tcell*​\<+2∘C while allowing uninterrupted backup discharge down to −20∘C. |
| **Alert Storm / Notification Fatigue** | Pressure hovers right at 40.0 PSI threshold, bouncing between 39.9 and 40.1 PSI every 10 seconds | Owner receives 100 SMS messages in an hour and mutes the number | Mandatory configurable **Hysteresis Band** (e.g., trip at 40.0 PSI, clear only at 42.0 PSI), **Persistence Timer** (must stay below threshold for *N* seconds), and **Per-Incident Rate Limiter** (1 initial alert \+ configurable reminder interval until acknowledged). |

### **7.2 Applicable US Fire Protection, Electrical & Regulatory Constraints**

*Transparency Note: Component certifications (such as an FCC-modular-certified ESP32-S3-WROOM-1 or a UL-listed external power adapter) reduce risk and cost, but **never automatically transfer full product listing or fire-protection compliance to the finished assembly**. Before making commercial claims or installing at third-party customer facilities, qualified engineering and AHJ review is mandatory.*

> 1. **NFPA 13 & NFPA 25 (Fire Protection Boundary & AHJ Jurisdiction):**  
   * Under **NFPA 13** (*Standard for the Installation of Sprinkler Systems*) and **NFPA 25** (*Standard for the Inspection, Testing, and Maintenance of Water-Based Fire Protection Systems*), required supervisory devices connected to the building's life-safety fire alarm panel must be **UL 346 / FM Approved** supervisory pressure switches (e.g., Potter PS40 / System Sensor EPS40).  
   * **Crucial Boundary for This Product:** This device MUST be positioned, labeled, and documented strictly as a **Non-Required Supplementary Maintenance & Early-Warning Telemetry System**—never as a life-safety supervisory switch or fire alarm component.  
   * **Mechanical Connection Rule:** Any attachment to the dry-pipe valve trim or supervisory air piping must be approved by a qualified sprinkler contractor and the local **Authority Having Jurisdiction (AHJ)** where applicable, so that it cannot obstruct required supervisory switches, quick-opening devices (accelerators/exhausters), or alarm line checks. Best practice is teeing off the auxiliary air gauge port or compressor supply trim via a lockable/supervised isolation valve as approved by the sprinkler professional.  
> 2. **Electrical Safety (UL 61010-1 / UL 62368-1 & NEC Article 725):**  
   * Keep 120V AC mains **strictly outside our enclosure** by using an off-the-shelf **UL-Listed, Class 2 (NEC Article 725\) 12V DC wall adapter**. Because the entire custom device operates inside a Class 2 Limited Energy envelope (\< 30V DC and \< 100 VA), shock and fire hazards are dramatically reduced, and low-voltage sensor cabling qualifies as Class 2 wiring under the National Electrical Code (NEC / NFPA 70).  
   * The internal 3.2V LiFePO4 cell should use a **UL 1642 / IEC 62133 recognized cell** with an integrated PCM (Protection Circuit Module) in addition to the carrier board's PTC polyfuse and charger protections.  
> 3. **FCC Part 15 Subpart B & Subpart C (EMC / Intentional & Unintentional Radiators):**  
   * Using the pre-certified **ESP32-S3-WROOM-1** module (which holds an FCC Modular Grant under Subpart C) avoids the \~$10k–$20k cost of intentional radiator RF certification, **provided** we follow Espressif's antenna keep-out layout rules, do not co-locate another transmitting radio simultaneously without evaluation, and include the required *"Contains FCC ID: 2AC7Z-ESP32S3WROOM1"* label on the enclosure exterior.  
   * However, the finished carrier PCB (containing switching regulators, the W5500 25 MHz crystal, and Ethernet magnetics) is still subject to **FCC Part 15 Subpart B (Unintentional Radiator — Class A for commercial/industrial warehouse environments, or Class B for residential)** verification/SDoC testing prior to commercial sale. Good PCB layout (solid ground plane, common-mode chokes on Ethernet/power, series damping resistors on SPI) is essential to pass radiated/conducted emissions on the first try.

## **8\. Concrete Design Roadmap & Next Deliverable Files**

Once the repository coordinator commits this Round 1 proposal to research/independent-designs/adviser-gemini/ and the owner answers the initial interview questions, work will proceed through five auditable phases:

### **Phase 1: Requirements Lock & Hydraulic/Site Verification (Current \-\> Round 2\)**

> * Record owner interview receipts in REQUIREMENTS.md and DECISIONS.md.  
> * Lock exact transducer thread/pressure range, cable lengths, and power/network path.

### **Phase 2: Detailed Hardware Engineering & Native KiCad 8 Project (HARDWARE/)**

> * Create native, human-readable **KiCad 8.0** schematic (sprinkler\_monitor.kicad\_sch) and 2-layer PCB layout (sprinkler\_monitor.kicad\_pcb) with verified footprints:  
  * Sheet 1: Power Input, TVS Protection, LiFePO4 Charger (with NTC Cold Inhibit), 3.3V Buck-Boost, INA219 Monitor.  
  * Sheet 2: ESP32-S3-WROOM-1, USB-C Native JTAG/Serial, TPL5010 Hardware Watchdog, Status LEDs, Provisioning Button.  
  * Sheet 3: 24V Current-Limited Loop Boost, Protected 4–20 mA Front-End, Precision 150 Ohm 0.1% Sense Network, ADS1118 SPI ADC, Protected 1-Wire/I2C Temperature Port.  
  * Sheet 4: WIZnet W5500 SPI Ethernet \+ RJ45 MagJack \+ Auxiliary UART Expansion Header.  
> * Export fabrication-ready Gerbers, Drill files, Pick-and-Place (cpl.csv), and multi-sourced BOM.csv with exact LCSC, Mouser, and DigiKey MPNs.

### **Phase 3: Mechanical CAD & Workshop Jigs (MECHANICAL/ & MANUFACTURING/)**

> * Create parametric **OpenSCAD / STEP** models for:  
  1. Internal PCB mounting carrier plate \+ 26650 LiFePO4 battery retention cradle.  
  2. Snap-on enclosure bottom drill template for PG7/M12 glands and ePTFE vent.  
  3. Bench QA pogo-pin / terminal test fixture enclosure.  
> * Write step-by-step assembly, conformal coating, and qa\_calibrate.py calibration scripts in MANUFACTURING/.

### **Phase 4: Embedded Firmware & Serverless Cloud/PWA (FIRMWARE/ & SOFTWARE/)**

> * Write complete **ESP-IDF / PlatformIO** firmware (FIRMWARE/) implementing:  
  * Oversampled ADS1118 4–20 mA loop acquisition \+ open/short fault state machine.  
  * Rolling 15-min and 60-min least-squares pressure slope calculation.  
  * Dual-interface network manager (W5500 Ethernet primary, Wi-Fi failover) \+ NVS offline ring buffer \+ TPL5010 hardware watchdog servicing.  
> * Write **Cloudflare Worker \+ D1 SQLite** backend (SOFTWARE/backend/) including the 60-second independent cron dead-man switch, Twilio SMS/Voice integration, and W3C Web Push VAPID dispatcher.  
> * Build the responsive **PWA Dashboard** (SOFTWARE/dashboard/) with strict anti-stale display enforcement and acknowledgement workflows.

### **Phase 5: Pilot Validation, Fault-Injection Testing & Commercialization Gate (BUSINESS/)**

> * Execute bench fault-injection test matrix (open wire, shorted wire, AC power pull, network pull, cold soak, corrupt OTA image).  
> * Complete regulatory checklist (AHJ / sprinkler contractor signoff on tap location, FCC Part 15A/B pre-compliance scan plan) in BUSINESS/COMPLIANCE.md.

## **9\. Single Most Important Interview Question (Question \#1)**

To establish the most critical physical, pneumatic, and utility baselines before freezing the schematic and sensor selection, please answer the following regarding your warehouse riser room:

**Question 1 (Riser Manifold, Compressor Behavior & Room Utilities):**

Looking at your dry-pipe riser room today:

> 1. **Pressure Tap & Compressor:** How is the air system currently maintained and gauged (e.g., automatic compressor with cut-in/cut-out pressure switch or air maintenance device, and what is the typical pressure swing around 50 PSI), and is there an existing spare/gauge port (such as a 1/4" NPT port on the air side) that your sprinkler service professional would approve teeing into with an isolation valve?  
> 2. **Power & Connectivity in the Room:** Is there an unswitched 120V AC outlet inside the riser room (and is it on the same circuit breaker as the compressor), and do you have reliable Wi-Fi signal inside the closed riser room or the ability to pass an Ethernet/low-voltage cable through the wall into the main warehouse?

---

