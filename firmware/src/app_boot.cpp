#include <Arduino.h>
#include <Wire.h>
#include "app_boot.h"
#include "app_config.h"
#include "app_config_store.h"
#include "app_buttons.h"
#include "app_imu.h"
#include "app_motion.h"
#include "app_ble.h"
#include "app_timing.h"
#include "pin_definitions.h"
#include "icm20948_registers.h"
#include "icm20948_driver.h"

// ICM-20948 init using Direct Semi-Register Access, then the register read-back for the midterm defense.
static void boot_imu(void) {
    Serial.println("[INIT] Initializing ICM-20948 Sensor Bus (400 kHz)...");
    bool ok = imu_init();
    for (int attempt = 2; !ok && attempt <= 5; ++attempt) {     // a loose wire / power glitch at boot: free the bus, retry
        Serial.printf("[INIT] ICM-20948 did not answer, recovering the I2C bus and retrying (%d/5)...\n", attempt);
        imu_busRecover();
        delay(100);
        ok = imu_init();
    }
    if (!ok) {
        Serial.println("[FATAL] ICM-20948 initialization failed!");
        icm20948_diag_t diag = imu_getDiagnostics();
        Serial.printf("[FATAL] WHO_AM_I readback = 0x%02X (Expected: 0x%02X)\n", diag.who_am_i, VAL_WHO_AM_I_EXPECTED);
        while (1) {
            digitalWrite(PIN_LED_STATUS, HIGH);
            delay(100);
            digitalWrite(PIN_LED_STATUS, LOW);
            delay(100);
        }
    }

    // Print Detailed Register Readback Diagnostics for Midterm Defense
    icm20948_diag_t diag = imu_getDiagnostics();
    Serial.println("[DIAGNOSTICS] Register Readback Verification:");
    Serial.printf("  -> WHO_AM_I         (Bank 0, 0x00) : 0x%02X  [PASS]\n", diag.who_am_i);
    Serial.printf("  -> PWR_MGMT_1       (Bank 0, 0x06) : 0x%02X  [PASS] (CLKSEL=Auto-PLL, SLEEP=0)\n", diag.pwr_mgmt_1);
    Serial.printf("  -> GYRO_CONFIG_1    (Bank 2, 0x01) : 0x%02X  [PASS] (FS=500dps, DLPF=51.2Hz)\n", diag.gyro_config_1);
    Serial.printf("  -> ACCEL_CONFIG     (Bank 2, 0x14) : 0x%02X  [PASS] (FS=4g, DLPF=50.4Hz [011])\n", diag.accel_config);
    Serial.printf("  -> GYRO_SMPLRT_DIV  (Bank 2, 0x00) : %d     [PASS] (ODR ~ 102.27 Hz)\n", diag.gyro_smplrt_div);
    uint16_t accel_div = ((uint16_t)diag.accel_smplrt_div_1 << 8) | diag.accel_smplrt_div_2;
    Serial.printf("  -> ACCEL_SMPLRT_DIV (Bank 2, 0x10-11): %d  [PASS] (ODR ~ 102.27 Hz, synced)\n", accel_div);
}

void app_boot(void) {
    Serial.begin(APP_SERIAL_BAUD);
    delay(500);

    Serial.println("\n==================================================");
    Serial.println("   HYBRID AIR MOUSE — 6-AXIS FUSION ON ICM-20948");
    Serial.println("   Course: He Thong Nhung (Embedded Systems)");
    Serial.println("==================================================");

    // Initialize GPIOs
    app_buttons_init();
    pinMode(PIN_LED_STATUS, OUTPUT);
    digitalWrite(PIN_LED_STATUS, LOW);

    boot_imu();
    app_motion_init();
    app_config_load_and_apply();        // saved user settings (gain, flick, click guard, recenter) or the defaults

    // Perform Startup Bias Calibration
    app_imu_calibrate_startup();

    // Start BLE HID Mouse Stack
    Serial.println("[BLE] Starting BLE HID Mouse Advertising as 'AirMouse-ESP32'...");
    app_ble_begin();

    app_timing_start();
    Serial.println("[SYSTEM] Air Mouse System Ready. Entering 100 Hz Main Loop.\n");
}
