#include <Arduino.h>
#include <ETH.h>
#include <SPI.h>
#include <Wire.h>
#include <Network.h>
#include <ArduinoOTA.h>
#include "ota_secret.h"

// Device Lab - sprinkler monitor electronics diagnostics v2.
// Monitoring-only: no sprinkler controls, no pressure thresholds/alarms yet.
// User's VERIFIED wiring: ADS1115 SCL->IO16, SDA->IO17.
// Leave sensor analog A0 unconnected until safe voltage-divider is installed.
static constexpr int I2C_SCL_PIN = 16;
static constexpr int I2C_SDA_PIN = 17;
static constexpr int ETH_SCK = 13;
static constexpr int ETH_MISO = 12;
static constexpr int ETH_MOSI = 11;
static constexpr int ETH_CS = 14;
static constexpr int ETH_IRQ = 10;
static constexpr int ETH_RST = 9;

static volatile bool hasEthernetLink = false;
static volatile bool hasEthernetIP = false;
static bool webReady = false;
static bool otaReady = false;
static bool ads1115Present = false;
static String foundI2C = "";
NetworkServer server(80);

void scanI2C() {
  String found = "";
  bool foundADC = false;
  for (uint8_t address = 0x08; address <= 0x77; ++address) {
    Wire.beginTransmission(address);
    if (Wire.endTransmission() == 0) {
      char hex[7];
      snprintf(hex, sizeof(hex), "0x%02X", address);
      if (found.length()) found += ",";
      found += hex;
      if (address >= 0x48 && address <= 0x4B) foundADC = true;
    }
  }
  ads1115Present = foundADC;
  foundI2C = found.length() ? found : "none";
  Serial.printf("I2C devices=%s ADS1115=%s SDA=%d SCL=%d\n",
    foundI2C.c_str(), ads1115Present ? "FOUND" : "NOT_FOUND",
    I2C_SDA_PIN, I2C_SCL_PIN);
}

void onNetworkEvent(arduino_event_id_t event, arduino_event_info_t info) {
  switch (event) {
    case ARDUINO_EVENT_ETH_START:
      ETH.setHostname("sprinkler-monitor-lab");
      Serial.println("ETH_START");
      break;
    case ARDUINO_EVENT_ETH_CONNECTED:
      hasEthernetLink = true;
      Serial.println("ETH_LINK_UP");
      break;
    case ARDUINO_EVENT_ETH_GOT_IP:
      hasEthernetIP = true;
      Serial.printf("ETH_GOT_IP address=%s mac=%s\n",
        ETH.localIP().toString().c_str(), ETH.macAddress().c_str());
      break;
    case ARDUINO_EVENT_ETH_LOST_IP:
      hasEthernetIP = false;
      Serial.println("ETH_LOST_IP");
      break;
    case ARDUINO_EVENT_ETH_STOP:
    case ARDUINO_EVENT_ETH_DISCONNECTED:
      hasEthernetIP = false;
      hasEthernetLink = false;
      Serial.println("ETH_LINK_DOWN");
      break;
    default: break;
  }
}

void setup() {
  Serial.begin(115200);
  delay(1100);
  Serial.println();
  Serial.println("DEVICE_LAB_SPRINKLER_ADC_DIAGNOSTIC_V2");
  Serial.printf("Chip=%s flash=%u psram=%u\n",
    ESP.getChipModel(), ESP.getFlashChipSize(), ESP.getPsramSize());

  Wire.begin(I2C_SDA_PIN, I2C_SCL_PIN, 100000);
  scanI2C();

  Network.onEvent(onNetworkEvent);
  SPI.begin(ETH_SCK, ETH_MISO, ETH_MOSI, ETH_CS);
  bool ok = ETH.begin(ETH_PHY_W5500, 1, ETH_CS, ETH_IRQ, ETH_RST, SPI, 8);
  Serial.printf("ETH_INIT=%s\n", ok ? "OK" : "FAILED");
}

void loop() {
  static unsigned long lastLogMs = 0;
  static unsigned long lastScanMs = 0;
  const unsigned long now = millis();

  if (now - lastScanMs >= 15000UL) {
    lastScanMs = now;
    scanI2C();
  }

  if (hasEthernetIP && !otaReady) {
    ArduinoOTA.setHostname("sprinkler-monitor-lab");
    ArduinoOTA.setPassword(SPRINKLER_OTA_PASSWORD);
    ArduinoOTA.begin();
    otaReady = true;
    Serial.println("AUTHENTICATED_OTA_READY");
  }
  if (otaReady) ArduinoOTA.handle();
  if (hasEthernetIP && !webReady) {
    server.begin();
    webReady = true;
    Serial.println("HTTP_ADC_DIAGNOSTIC_READY");
  }
  if (webReady) {
    NetworkClient client = server.accept();
    if (client) {
      client.setTimeout(150);
      const unsigned long t = millis();
      while (client.connected() && !client.available() && millis() - t < 400) delay(1);
      while (client.available()) client.read();
      String body = String("sprinkler-adc-diagnostic\nuptime_s=")
        + String(millis() / 1000UL)
        + "\nip=" + ETH.localIP().toString()
        + "\nlink=" + (hasEthernetLink ? "up" : "down")
        + "\ni2c_sda=17\ni2c_scl=16"
        + "\ni2c_devices=" + foundI2C
        + "\nads1115=" + (ads1115Present ? "FOUND" : "NOT_FOUND")
        + "\npressure_psi=NOT_CONFIGURED"
        + "\n";
      client.print("HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nConnection: close\r\nContent-Length: ");
      client.print(body.length());
      client.print("\r\nCache-Control: no-store\r\n\r\n");
      client.print(body);
      client.stop();
    }
  }
  if (now - lastLogMs >= 5000) {
    lastLogMs = now;
    Serial.printf("HEALTH uptime_s=%lu eth_link=%d eth_ip=%d adc=%s heap=%u\n",
       now / 1000UL, hasEthernetLink, hasEthernetIP,
       ads1115Present ? "FOUND" : "NOT_FOUND", ESP.getFreeHeap());
  }
  delay(10);
}
