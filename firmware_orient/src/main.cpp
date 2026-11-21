// =============================================================================
// Air Mouse - sensor axis / direction measurement (2026-10-08)
//
// Question: with the board held the way a person holds a pointer, which sensor axis is "forward",
// "right", "up", and does a right turn / nose-up give a positive or negative gyro reading?
// Nothing else (no motion pipeline, no BLE). Keep the board STILL for the first ~3 s (gyro calibration).
//
// Output, every 100 ms (mean of 10 samples at 100 Hz):
//   [O] t_ms ax ay az gx gy gz fail
//   ax..az  accelerometer in g (resting flat, Z up: az ~ +1)
//   gx..gz  gyro in dps MINUS the startup bias (positive = counter-clockwise looking from +axis toward origin)
//   fail    number of failed I2C reads in that 100 ms (should be 0)
// =============================================================================
#include <Arduino.h>
#include <Wire.h>
#include <math.h>
#include "pin_definitions.h"
#include "icm20948_registers.h"
#include "icm20948_driver.h"

static float    s_cal[3] = {0.0f, 0.0f, 0.0f};
static uint32_t s_last_us = 0;
static double   s_sum[6];
static uint32_t s_n = 0, s_fail = 0, s_win_start_ms = 0;
static bool     s_ok = false;

static void reset_window(void) {
    for (int k = 0; k < 6; ++k) s_sum[k] = 0.0;
    s_n = 0;
    s_fail = 0;
}

void setup() {
    Serial.begin(115200);
    delay(1500);
    Serial.println("\n[ORIENT] Air Mouse axis/direction measurement 2026-10-08");
    s_ok = imu_init();
    icm20948_diag_t g = imu_getDiagnostics();
    Serial.printf("[ORIENT] imu_init=%s WHO_AM_I=0x%02X\n", s_ok ? "PASS" : "FAIL", g.who_am_i);
    if (!s_ok) { Serial.println("[ORIENT] ABORT: IMU init failed (check SDA/SCL/VCC/GND wires)"); return; }

    Serial.println("[ORIENT] Keep the board STILL: calibrating gyro bias (2 s) ...");
    float sum[3] = {0.0f, 0.0f, 0.0f};
    int valid = 0;
    for (int i = 0; i < 200; ++i) {
        imu_data_t d;
        if (imu_readData(&d)) { sum[0] += d.gx; sum[1] += d.gy; sum[2] += d.gz; valid++; }
        delay(10);
    }
    for (int k = 0; k < 3; ++k) s_cal[k] = valid > 0 ? sum[k] / valid : 0.0f;
    Serial.printf("[CAL] bias_x=%+.4f bias_y=%+.4f bias_z=%+.4f dps polls=%d\n", s_cal[0], s_cal[1], s_cal[2], valid);
    Serial.println("[O-HDR] t_ms ax ay az gx gy gz fail   (a in g, g in dps minus bias)");
    reset_window();
    s_last_us = micros();
    s_win_start_ms = millis();
}

void loop() {
    if (!s_ok) { delay(1000); return; }
    uint32_t now_us = micros();
    if (now_us - s_last_us < 10000) return;      // 100 Hz polling like the firmware
    s_last_us = now_us;

    imu_data_t d;
    if (!imu_readData(&d)) { s_fail++; }
    else {
        s_sum[0] += d.ax; s_sum[1] += d.ay; s_sum[2] += d.az;
        s_sum[3] += d.gx - s_cal[0]; s_sum[4] += d.gy - s_cal[1]; s_sum[5] += d.gz - s_cal[2];
        s_n++;
    }

    uint32_t now_ms = millis();
    if (now_ms - s_win_start_ms >= 100) {
        s_win_start_ms = now_ms;
        if (s_n > 0) {
            Serial.printf("[O] %lu %+.3f %+.3f %+.3f %+.2f %+.2f %+.2f %lu\n", (unsigned long)now_ms,
                          s_sum[0] / s_n, s_sum[1] / s_n, s_sum[2] / s_n,
                          s_sum[3] / s_n, s_sum[4] / s_n, s_sum[5] / s_n, (unsigned long)s_fail);
        } else {
            Serial.printf("[O] %lu nan nan nan nan nan nan %lu\n", (unsigned long)now_ms, (unsigned long)s_fail);
        }
        reset_window();
    }
}
