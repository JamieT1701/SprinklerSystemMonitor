#include <Arduino.h>
#include <ETH.h>
#include <SPI.h>
#include <Wire.h>
#include <Network.h>
#include <ArduinoOTA.h>
#include <OneWire.h>
#include <DallasTemperature.h>
#include <math.h>
#include "ota_secret.h"

// Device Lab - 2026 sprinkler monitor sensor diagnostics.
// SUPPLEMENTAL monitoring only. Not an approved fire supervisory controller.
// RAW A0 and calculated pressure are DIAGNOSTIC ONLY: no onsite voltage check or gauge calibration yet.
// Firmware cannot protect ADS1115 from miswiring/overvoltage; onsite electrical verification still required.
// ADS1115 SCL->GPIO16, SDA->GPIO17. DS18B20 DATA->GPIO18; proposed Board B R5=4.7k from GPIO18 DATA to 3V3.
constexpr int I2C_SCL = 16;
constexpr int I2C_SDA = 17;
constexpr int TEMP_DATA = 18;
constexpr int ETH_SCK = 13, ETH_MISO = 12, ETH_MOSI = 11, ETH_CS = 14;
constexpr int ETH_IRQ = 10, ETH_RST = 9;
constexpr uint8_t ADS_ADDR = 0x48;
// V5 proposed hardware: R_UP=10k, R_DOWN=10k+4.7k=14.7k -> ratio 14.7/24.7.
// Design-only until rebuilt and electrically measured. DO NOT treat PSI as calibrated.
constexpr float VOLT_DIVIDER_RATIO = 14.7f / 24.7f;
constexpr float PRESSURE_RANGE_PSI = 150.0f;

OneWire oneWire(TEMP_DATA);
DallasTemperature temperatureSensors(&oneWire);
NetworkServer server(80);
static volatile bool ethLink = false;
static volatile bool ethIp = false;
static bool webReady = false;
static bool otaReady = false;
static bool adcPresent = false;
static bool tempPresent = false;
static bool tempValid = false;
static bool pressureVoltageValid = false;
static float tempC = NAN;
static float pressureNodeV = NAN;
static float provisionalPsi = NAN;
static uint32_t lastTempOkMs = 0;
static uint32_t lastTempSampleMs = 0;
static uint32_t lastPressureSampleMs = 0;
static uint32_t lastScanMs = 0;
static String i2cDevices = "not_scanned";

void scanI2C() {
  String found = "";
  bool adsFound = false;
  for (uint8_t addr=8; addr<=0x77; ++addr) {
    Wire.beginTransmission(addr);
    if (Wire.endTransmission() == 0) {
      if (found.length()) found += ",";
      char buf[8]; snprintf(buf,sizeof(buf),"0x%02X", addr);
      found += buf;
      if (addr == ADS_ADDR) adsFound=true;
    }
  }
  i2cDevices = found.length() ? found : "none";
  adcPresent = adsFound;
  Serial.printf("I2C %s ADS1115=%s\n",i2cDevices.c_str(),adcPresent?"FOUND":"NOT_FOUND");
}

bool readADS1115A0(float &volts) {
  if (!adcPresent) return false;
  // 0xC383 = single-shot AIN0/GND, +/-4.096V, 128SPS, comparator disabled.
  Wire.beginTransmission(ADS_ADDR);
  Wire.write(0x01);
  Wire.write(0xC3);
  Wire.write(0x83);
  if (Wire.endTransmission() != 0) return false;
  delay(10);
  Wire.beginTransmission(ADS_ADDR);
  Wire.write(0x00);
  if (Wire.endTransmission() != 0) return false;
  if (Wire.requestFrom((int)ADS_ADDR,2) != 2) return false;
  uint16_t packed=((uint16_t)Wire.read()<<8) | Wire.read();
  int16_t code=(int16_t)packed;
  volts = ((float)code) * (4.096f/32768.0f);
  // 4.096V is the programmable ADC range, NOT the allowed analog pin voltage.
  // Anything above VDD may be clipped by the ADC; always require physical voltage check.
  return isfinite(volts) && volts >= -0.01f && volts <= 3.31f;
}

void samplePressure() {
  float volts;
  if (readADS1115A0(volts)) {
    pressureVoltageValid = true;
    pressureNodeV=volts;
    float sensorV = volts / VOLT_DIVIDER_RATIO;
    provisionalPsi = (sensorV - 0.5f) * (PRESSURE_RANGE_PSI / 4.0f);
  } else {
    pressureVoltageValid=false;
    pressureNodeV=NAN;
    provisionalPsi=NAN;
  }
}

void sampleTemperature() {
  // Discovery each sample also handles an intermittently unplugged probe.
  tempPresent = temperatureSensors.getDeviceCount() > 0;
  if (!tempPresent) temperatureSensors.begin();
  tempPresent = temperatureSensors.getDeviceCount() > 0;
  if (!tempPresent) {tempValid=false; tempC=NAN; return;}
  temperatureSensors.requestTemperatures();
  const float value = temperatureSensors.getTempCByIndex(0);
  // -127C indicates disconnected; +85C is the unconverted power-up sentinel.
  if (isfinite(value) && value > -55.0f && value < 125.0f &&
      fabsf(value - DEVICE_DISCONNECTED_C) > 0.001f &&
      fabsf(value - 85.0f) > 0.001f) {
    tempC=value;
    tempValid=true;
    lastTempOkMs=millis();
  } else {
    tempValid=false;
    tempC=NAN;
  }
}

void networkEvent(arduino_event_id_t event, arduino_event_info_t info) {
  switch(event) {
    case ARDUINO_EVENT_ETH_START:
      ETH.setHostname("sprinkler-monitor-lab"); break;
    case ARDUINO_EVENT_ETH_CONNECTED:
      ethLink=true; break;
    case ARDUINO_EVENT_ETH_GOT_IP:
      ethIp=true; Serial.printf("ETH_IP=%s\n", ETH.localIP().toString().c_str());break;
    case ARDUINO_EVENT_ETH_LOST_IP:
      ethIp=false; break;
    case ARDUINO_EVENT_ETH_DISCONNECTED:
    case ARDUINO_EVENT_ETH_STOP:
      ethLink=false;ethIp=false;break;
    default:break;
  }
}

void setup() {
  Serial.begin(115200);
  delay(900);
  Serial.println("SPRINKLER_PRESSURE_DIAGNOSTICS_V5_47K");
  Wire.begin(I2C_SDA,I2C_SCL,100000);
  scanI2C();
  temperatureSensors.begin();
  temperatureSensors.setResolution(12);
  sampleTemperature();
  samplePressure();
  lastTempSampleMs=lastPressureSampleMs=millis();

  Network.onEvent(networkEvent);
  SPI.begin(ETH_SCK,ETH_MISO,ETH_MOSI,ETH_CS);
  bool ethStarted = ETH.begin(ETH_PHY_W5500,1,ETH_CS,ETH_IRQ,ETH_RST,SPI,8);
  Serial.printf("ETH_INIT=%s DS18B20=%s tempF=%.2f pressure_A0=%.4fV PROVISIONAL\n",
    ethStarted?"OK":"FAILED",tempValid?"OK":"INVALID",
    tempValid?(tempC*1.8f+32.0f):NAN, pressureNodeV);
}

String makeBody() {
  String s="sprinkler-pressure-diagnostics-v5-47k\n";
  s += "uptime_s=" + String(millis()/1000UL) + "\n";
  s += "ip=" + ETH.localIP().toString() + "\n";
  s += "link=" + String(ethLink?"up":"down") + "\n";
  s += "i2c_sda=17\ni2c_scl=16\n";
  s += "i2c_devices=" + i2cDevices + "\n";
  s += "ads1115=" + String(adcPresent?"FOUND":"NOT_FOUND") + "\n";
  s += "ds18b20_gpio=18\n";
  s += "ds18b20=" + String(tempValid?"OK":(tempPresent?"INVALID_READING":"NOT_FOUND")) + "\n";
  s += "temperature_f=" + (tempValid?String(tempC*1.8f+32.0f,2):String("INVALID")) + "\n";
  s += "temperature_c=" + (tempValid?String(tempC,2):String("INVALID")) + "\n";
  s += "temp_sample_age_ms=" + String(tempValid?(millis()-lastTempOkMs):0) + "\n";
  String cold="SENSOR_FAULT";
  if (tempValid) {
    const float f=tempC*1.8f+32.0f;
    cold=f<40?"URGENT_UNDER_40F":f<45?"EARLY_WARNING_UNDER_45F":"NORMAL";
  }
  s += "freeze_state=" + cold + "\n";
  s += "freeze_notifications=NOT_CONFIGURED\n";
  s += "pressure_a0_v=" + (pressureVoltageValid?String(pressureNodeV,4):String("INVALID")) + "\n";
  // Input plausible range is diagnostic; it does NOT establish that an overvoltage
  // is absent, because the ADC's PGA range does not override VDD pin limits.
  const bool plausible = pressureVoltageValid && pressureNodeV >= 0.20f && pressureNodeV <= 2.95f;
  const String inputState = !pressureVoltageValid ? "ADC_ERROR" :
    pressureNodeV < 0.20f ? "LOW_INPUT_OR_OPEN_SHORT" :
    pressureNodeV > 2.95f ? "HIGH_INPUT_OR_WIRING_FAULT" :
    "VOLTAGE_PLAUSIBLE_UNCALIBRATED";
  s += "pressure_input_state=" + inputState + "\n";
  s += "pressure_psi_provisional=" + (plausible ? String(provisionalPsi,2) : String("INVALID")) + "\n";
  s += "pressure_electrical_check=PENDING_MULTIMETER_A0_TO_GND\n";
  s += "pressure_calibration=UNVERIFIED_DIVIDER_AND_GAUGE\n";
  s += "pressure_notifications=NOT_CONFIGURED\n";
  s += "ota_installed=" + String(otaReady?"yes":"no") + "\n";
  return s;
}

void loop() {
  const uint32_t now=millis();
  if (now-lastTempSampleMs>=4000U) {
    lastTempSampleMs=now;sampleTemperature();
    Serial.printf("TEMP DS18B20=%s F=%.2f\n",tempValid?"OK":"ERROR",tempValid?tempC*1.8f+32.0f:NAN);
  }
  if (now-lastPressureSampleMs>=4000U) {
    lastPressureSampleMs=now;
    samplePressure();
    Serial.printf("A0_V=%.4f PSI_PROVISIONAL=%.2f CHECK_NOT_COMPLETED\n",pressureNodeV,provisionalPsi);
  }
  if (now-lastScanMs>=60000UL) {lastScanMs=now;scanI2C();}
  if (ethIp && !otaReady) {
    ArduinoOTA.setHostname("sprinkler-monitor-lab");
    ArduinoOTA.setPassword(SPRINKLER_OTA_PASSWORD);
    ArduinoOTA.begin();
    otaReady=true;
  }
  if (otaReady) ArduinoOTA.handle();
  if (ethIp && !webReady) {server.begin();webReady=true;}
  if (webReady) {
    NetworkClient client=server.accept();
    if (client) {
      client.setTimeout(150);
      uint32_t t=millis();
      while(client.connected()&&!client.available()&&millis()-t<400) delay(1);
      while(client.available()) client.read();
      String body=makeBody();
      client.print("HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nConnection: close\r\nCache-Control: no-store\r\nContent-Length: ");
      client.print(body.length());
      client.print("\r\n\r\n");
      client.print(body);
      client.stop();
    }
  }
  delay(10);
}
