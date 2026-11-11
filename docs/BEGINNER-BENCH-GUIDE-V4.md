# Build a better sprinkler monitor — beginner workbench guide v4

**Use the two 50 × 70 mm perfboards you already have.** This guide supersedes the older v2/v3 instructions. It is a planned electronics rebuild, **not** a deployed or safety-certified sprinkler monitoring device.

## What's changed in v4

- The DS18B20 temperature probe **does not have a built-in pull-up resistor**. Add **R5 = 4.7 kΩ between 3V3 and DATA** on Board B. Only one pull-up is intended.
- Use the second available **4.7 kΩ as R3**, in the bottom leg of the pressure divider (not 5 kΩ). The new 10 kΩ top / 14.7 kΩ bottom divider factor is **0.5951417**, not 0.6000.
- **Important firmware distinction:** The currently deployed pressure-diagnostic v4 binary was built for factor **0.6000**. It is not recalibrated for the new resistor until a separately built/verified firmware is deployed. The numerical effect around 50 PSI is small (~0.7 PSI) but should still be corrected before acceptance.
- Your pressure transducer stays installed on the warehouse compressor. The monitor circuit can be disconnected and brought to the bench. **Do not touch sprinkler valves, safety controls, pressurized piping or listed alarm wiring.**
- Photo-like assembly mockups are **concept illustrations, not a source for exact pin positions or hidden solder traces**. The written connection table below is authoritative.

## Parts

- 2 × **50 × 70 mm** perfboards, preferably isolated copper pads / 2.54 mm holes.
- Existing Waveshare **ESP32-S3-POE-ETH + PoE module**, mounted beside the boards on nylon standoffs.
- Existing **ADS1115** breakout (I2C address 0x48).
- 2 × three-position terminal blocks (screw or pluggable): **J1 PRESS** and **J2 TEMP**.
- **10 kΩ** resistors: R1 and R2, plus one **extra temporary 10 kΩ** for the bench signal test (3 total if doing the test).
- **4.7 kΩ** resistors: R3 (pressure) and R5 (temperature pull-up), **2 total**.
- **1 kΩ** resistor: R4 (pressure ADC series filter).
- **100 nF** ceramic capacitor: C1 (often marked 104).
- Hookup wire, solder, heat shrink/insulation, labels, nylon standoffs and baseplate, larger plastic enclosure, small screwdriver, wire strippers, multimeter.

### How to recognize resistors (common 4-band markings, check with a meter)
- 10 kΩ: **brown / black / orange / gold**
- 4.7 kΩ: **yellow / violet / red / gold**
- 1 kΩ: **brown / black / red / gold**

## The whole build in plain English

### 1. Unplug and label
Disconnect Ethernet PoE and any USB power. Photograph the current wiring. Unplug only the monitor electronics and bring those to the bench; leave the installed sensor fittings and sprinkler controls alone.

### 2. Dry-fit the three assemblies
The ESP32/PoE main PCB is longer than 70 mm, so mount it **separately**, not on a perfboard. Place Board A (ADS1115 + pressure resistors) and Board B (field terminals + temperature pull-up) on an insulating baseplate with room for a bigger enclosure, RJ45 cable and your fingers.

### 3. Mark Board B's terminal blocks
**J1 PRESS** three screws: **1 +5V (red), 2 GND (black), 3 SIG (green)**.  
**J2 TEMP** three screws: **1 3V3 (red/probe VCC), 2 DATA (probe signal), 3 GND (probe ground)**. The numbering is yours; put labels beside actual screws.

### 4. Add the missing DS18B20 resistor — R5
On Board B, take **one 4.7 kΩ resistor**. Solder **one leg to the 3V3 line feeding J2-1**, and **the other leg to the DATA line feeding J2-2 and ESP GPIO18**. It does **not** go between DATA and GND, and it is **not** in series with the data wire. Leave J2-3 connected directly to ground.

\`\`\`text
ESP 3V3 ----+----------------> J2-1 TEMP VCC
             |
           R5 4.7 kΩ
             |
ESP GPIO18 --+----------------> J2-2 TEMP DATA

ESP GND ----------------------> J2-3 TEMP GND
\`\`\`

### 5. Install ADS1115 on Board A
Wire ADS **VDD → ESP 3V3**, **GND → common GND**, **SDA → ESP GPIO17**, **SCL → ESP GPIO16**. Later connect ADS **A0** to the filtered divider output. A1/A2/A3 unused. Never use ESP **3V3_EN** as a supply.

### 6. Build the pressure resistor section on Board A
Solder **R1 10 kΩ** between J1-3 SIG and a small copper node labeled **DIV**. From DIV to GND, solder **R2 10 kΩ in series with R3 4.7 kΩ** (end-to-end). From DIV through **R4 1 kΩ**, make a node labeled **A0** connected to ADS A0. Solder **C1 100 nF** between A0 and GND. Add separate labeled safe probe loops **TP-SIG** and **TP-A0**.

\`\`\`text
J1-3 GREEN SIG -- R1 10k -- DIV --- R4 1k ---- A0 ---- ADS1115 A0
                              |                  |
                            R2 10k           C1 100nF
                              |                  |
                            R3 4.7k             GND
                              |
                             GND
\`\`\`

### 7. Run the rest of the wires
| Wire from | Wire to |
|---|---|
| ESP **3V3** | ADS VDD and Board B **J2-1 TEMP 3V3** (and R5 upper leg) |
| ESP **GND** | ADS GND; Board A divider ground; Board B **J1-2**, **J2-3** |
| ESP **GPIO17** | ADS SDA |
| ESP **GPIO16** | ADS SCL |
| ESP **GPIO18** | Board B **J2-2 DATA** (and R5 lower leg) |
| Verified PoE **VSYS 5V** | Board B **J1-1 PRESS +5V** |
| Board B **J1-3 PRESS SIG** | Board A **R1 input / TP-SIG** |
| Board A **A0 node** | ADS1115 **A0** |

Never route the 48V Ethernet/PoE side through perfboard. Keep metal and jumper wires from touching the PoE daughterboard.

### 8. Check with power OFF
Use continuity mode to check intended connections. Verify no direct 5V-to-GND or 3V3-to-GND short, no shorts across R5, no unintended bridge from A0 to another pin, and no long component legs touching the PoE underside.

### 9. Power up without field sensors
With J1 pressure and J2 temperature **empty**, power the ESP32 from one supported supply only. ADS1115 should still appear at I2C address **0x48**. The DS18B20 may correctly say **NOT_FOUND** while unplugged. A0 near zero with J1 empty can be normal. Power OFF before adding/removing wires.

### 10. Optional bench pressure simulation
Keep the real pressure sensor **disconnected**. With power OFF, connect a **spare 10 kΩ resistor** from ESP 3V3 to J1-3 SIG. Power up and read A0. Expect approximately **1.40V**; current v4 software may display roughly **69 PSI**. This is **not a real pressure measurement**. Power OFF and remove the temporary resistor.

### 11. Reinstall & compare to gauge
With power OFF reconnect J1 and J2 field cables, secure strain relief, and restore PoE. At the reported gauge pressure ~50 PSI, expect sensor SIG about **1.83V** and ADS A0 about **1.09V** with the new divider. **Do not assume these values prove sensor safety or calibration.** Measure accessible test points and compare the reading to the actual gauge. The prior live A0 was ~0.0003–0.0004V and invalid; we must diagnose it rather than claim pressure is fixed.

### 12. Alerts are separate
Freeze, low-pressure, sensor-failure and independent heartbeat/outage notifications are **not yet configured or tested**. The device is a **supplementary monitor only**, never a replacement for listed controls, heating or required inspections.

## Quick troubleshooting
- Temperature NOT_FOUND after reconnecting J2: check **R5 bridging 3V3 to DATA**, GPIO18 to DATA, J2-3 GND, and probe cable.
- ADS not found: check ADS 3V3/GND, SDA GPIO17, SCL GPIO16.
- A0 about 0 with J1 unplugged: **expected** for a grounded divider.
- A0 about 0 with 10 kΩ temporary simulator: inspect Board A signal route, GND, R1/R2/R3/R4, A0 joint.
- Simulator works, actual sensor gives ~0: check actual transducer 5V supply, ground, green signal wire, and field cable.
- Plausible A0 but wrong PSI: verify **R3 actual 4.7 kΩ**, physical sensor specifications, firmware ratio, mechanical gauge, and calibration.

## Source reference
Waveshare https://docs.waveshare.com/ESP32-S3-ETH and Texas Instruments ADS1115 https://www.ti.com/lit/ds/symlink/ads1115.pdf.

**On-bench rule:** the conceptual photos are useful for component placement, **not** trustworthy instructions for precise wiring. Follow the labeled schematic and table.
