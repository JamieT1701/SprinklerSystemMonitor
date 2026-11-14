> **CURRENT BUILD AUTHORITY - TWO-TERMINAL R6 (2026-11-11):** Use [BUILD-GUIDE.md](./BUILD-GUIDE.md) and [the web guide](./index.html). One PoE Ethernet cable plugs into the controller's factory RJ45; the two three-wire sensor cables land on exactly TWO three-position terminal blocks, BOTH on Board B. Board A contains ADS1115 and pressure conditioning, not another field connector. R5=4.7k from 3V3 to GPIO18/DATA is on Board B; the probe has no pull-up. R3=4.7k is a separate pressure resistor, giving ratio 14.7/24.7. Temperature and pressure-v4 OTA deployment were verified in later PR comments, but pressure remained near zero/invalid. Prepared v5-47k is compiled, not deployed. The rebuild, calibration, history and alerts are not accepted. Earlier entries below are historical and must not override this current guide. No firmware changed during R6 review.

> **Later assembly correction (2026-11-11):** The new 50 × 70 mm perfboard build will **not** rely on a resistor attached to the temperature probe. Install exactly one **4.7 kΩ pull-up (R5) between ESP 3V3 and GPIO18/DATA on Board B**. Use a second **4.7 kΩ resistor as pressure-divider R3** instead of the earlier planned 5 kΩ; new divider ratio is **14.7/(10+14.7) = 0.5951417**. Earlier references below reflect the old wiring checkpoint and are retained for historical evidence. Source of truth for the rebuild: [v4 beginner guide](./BEGINNER-BENCH-GUIDE-V4.md) and [live bench website](./index.html). **No hardware change has been bench-verified yet.**

# 2026 Device Lab sprinkler monitor - verified checkpoint (2026-11-10)

**Status:** hardware wiring assembled; user will reconnect PoE on 2026-11-11. New DS18B20 readings, pressure readings, alerting and remote firmware updates have **not** been verified as operational.

## Purpose and safety
Supplemental environmental and common-air-pressure monitoring on an existing three-zone dry sprinkler system using one common compressor (nominal pressure about 50 PSI). The riser room is separate, accessed from outside, and vulnerable to cold. This device **must not** control, defeat, or replace the listed sprinkler/alarm/freeze protection or inspections. Any alarm thresholds are suggestions pending appropriate validation.

## Hardware and confirmed pins
- Waveshare **ESP32-S3-POE-ETH** + PoE daughterboard; W5500 Ethernet SPI SCK13, MISO12, MOSI11, CS14, IRQ10, RESET9.
- ADS1115 at **3.3 V**, connected **SCL=IO16, SDA=IO17**; actual I2C detection **0x48** passed on USB and PoE before new wiring.
- Three-wire **DS18B20** temperature probe: user reports wired on **3V3**, **GND**, **DATA=IO18**; the probe has an existing 4.7 kΩ DATA-to-3V3 pull-up. **Not yet read/tested**; no extra pull-up planned. Do NOT connect to **3V3_EN**; it's not 3.3V power.
- DHT22 and DHT11 were considered then set aside. A detachable probe connector was rejected; probe cable will pass directly through block wall to riser room. Position near vulnerable valves, away from heaters and pipe surface. Seal any penetrations appropriately.
- Pressure sensor from earlier project: **0-150 PSI, nominal 0.5-4.5 V signal on 5 V supply**, wires reportedly red supply / black ground / green signal. Actual manufacturer/part number not verified. VSYS at PoE measured **5.097 V** by user.
- **Do not assert pressure sensor is currently connected.** Proposed ADC A0 divider: sensor green -> 10 kΩ -> A0 junction; junction -> 10 kΩ + 5 kΩ in series -> common ground (equivalent 15 kΩ; factor 0.6). Ensure wiring electrically correct before powering. Never feed raw 0.5-4.5 V signal into ADS1115 powered at 3.3 V.
- Historical 2024 measurements used a *different* 10k/22k divider and do not map directly to the new ADC; nominal new divider predicts A0 ~0.30V @ 0 PSI, 1.10V @50 PSI, 2.70V @150 PSI. Compare to an independent pressure gauge.

## What is *actually* verified
- Prior ESP32-S3 USB firmware flashed and hash-verified; 16MB flash, 8MB OPI PSRAM, ESP32 Arduino core 3.3.8; partitions `default_8MB` with OTA slots.
- Live repeated I2C detection: **ADS1115 FOUND** address **0x48**, SDA17/SCL16.
- PoE, Ethernet, DHCP and HTTP diagnostics previously worked. Device hostname `sprinkler-monitor-lab`; network address is DHCP-managed, not fixed.
- Authenticated ArduinoOTA support included in flashed diagnostics, but an OTA firmware **upload has not yet been exercised**.
- The code copied to `firmware/2026/adc_diagnostics/adc_diagnostics.ino` here is a snapshot of the *verified flashed* diagnostic firmware, not a new DS18B20-reading firmware.
- The sketch refers to `ota_secret.h`; intentionally excluded from public repository. Do not put the real secret in GitHub. Use a local file defining `SPRINKLER_OTA_PASSWORD` from a locally managed secret when compiling.

## Resume 2026-11-11
1. User reconnects PoE. Verify device via its hostname and HTTP diagnostic endpoint; do not repeat old USB/I2C tests without a failure.
2. Prepare DS18B20 readout on GPIO18 in a separately tracked firmware revision, compile using established ESP32 board config, and deploy with authenticated OTA if it works; preserve existing firmware rollback.
3. Confirm live DS18B20 temperature in °F, proper disconnection/error handling (including DS18B20 -127°C and 85°C sentinel cases), sensible trend and communication watchdog. **No freeze-alert service exists yet.**
4. Verify pressure transducer divider electrically and its wiring status before enabling pressure ADC measurements and calibrating against mechanical gauge.
5. Build/test out-of-band alerting for low temperature, low pressure, sensor errors, and device/power/network outages. The ESP32 cannot itself alert while powered down; use independent heartbeat monitoring. Only claim operational after end-to-end alert verification.

## Local source and secrets
On Oscar: `C:\Development\Device-Lab\Sprinkler-Monitor\firmware\adc_diagnostics\adc_diagnostics.ino`. The unredacted operational handoff and evidence live at `C:\Development\Device-Lab\Sprinkler-Monitor\HANDOFF-2026-11-10.md` and `README-current-state.md`. The OTA password and header are stored **only locally**, outside public version control. This repo also contains a legacy 2024 dashboard which must not be overwritten.

**Authority note:** This is a checkpoint branch for review; it does not mean the new board firmware has been deployed, and is not an instruction to modify the original 2024 application.

## Field visit: 2026-11-11
- User connected PoE; DS18B20 temperature probe is in riser room, pressure sensor attached to compressor air outlet.
- Live HTTP diagnostics from the **old** firmware: HTTP 200, uptime increasing, link=up, ADS1115 FOUND at 0x48, SDA=17/SCL=16. Pressure remains NOT_CONFIGURED.
- New firmware source `firmware/2026/sensor_diagnostics/sensor_diagnostics.ino` reads GPIO18 DS18B20 and ADC A0 voltage / provisional PSI with diagnostic freeze-state labels. Compiled on Oscar with OneWire v2.3.8 and DallasTemperature v4.0.6, ESP32 core 3.3.8, exit code 0, 658786 bytes flash, 34056 bytes globals. The real OTA secret remains on Oscar.
- **NOT DEPLOYED**: attempt to invoke authenticated remote OTA was blocked by safety checks before execution. Old firmware remained online and responsive afterward; temperature and pressure have not been measured. Do not imply live sensor validation or alerting.
- Last local code: `C:\Development\Device-Lab\Sprinkler-Monitor\firmware\sensor_diagnostics\sensor_diagnostics.ino`; existing known-working compiled binary preserved in `firmware\adc_diagnostics\build_ota`.
- Next: use a permitted firmware-upload path, then confirm DS18B20 temperature, ADC pressure voltage, gauge match, and fault handling. Actual freeze/pressure notifications are not implemented.
