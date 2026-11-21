// =============================================================================
// Air Mouse - gyro bias drift measurement (viec B, 2026-10-04)
//
// Question: after the 2-second startup calibration, how far does the real gyro
// zero-rate bias wander while the board sits still (die warming up)? The
// simulation says residual bias >= 0.2-0.3 dps on pitch/yaw makes the new
// stationary lock fail and the cursor creep (see docs/FIRMWARE_CHANGELOG_2026-10-03.md).
//
// What it does (same sequence as firmware/firmware.ino):
//   1. imu_init(), motion_init(NULL)
//   2. 200-sample / delay(10) mean calibration -> motion_setBias()   [CAL line]
//   3. For RUN_SECONDS seconds: poll at 10 ms like firmware loop(), feed the REAL
//      production motion_process() (clutch released), and print one [D] line per
//      second. Nothing is sent over BLE.
// Per-second line:
//   rx,ry,rz   mean raw gyro of that second MINUS the startup calibration (dps)
//              (= residual bias the firmware would see if auto-zero did not exist)
//   sx,sy,sz   std-dev of raw gyro within that second (dps)
//   cnt        sum |dX|+|dY| produced by the real pipeline in that second
//   stat       samples in that second where pipeline reported is_stationary
//   fixlock    samples where "30 consecutive |omega|<0.4 dps" held vs the FIXED
//              startup calibration (worst case: no auto-zero)
//   bx,by,bz   pipeline's own bias estimate (moves only via auto-zero)
// =============================================================================
#include <Arduino.h>
#include <Wire.h>
#include <math.h>
#include "pin_definitions.h"
#include "icm20948_registers.h"
#include "icm20948_driver.h"
#include "motion_pipeline.h"

#ifndef RUN_SECONDS
#define RUN_SECONDS 720
#endif

// Same defaults as motion_pipeline.cpp (stat_gyro_thresh, stat_accel_thresh, stat_window_count)
#define LOCK_GYRO_THRESH   0.4f
#define LOCK_ACCEL_THRESH  0.08f
#define LOCK_WINDOW        30

static float    s_cal[3] = {0.0f, 0.0f, 0.0f};
static uint32_t s_last_us = 0;
static uint32_t s_win_start_ms = 0;
static uint32_t s_sec = 0;
static bool     s_done = false;
static uint16_t s_run = 0;

static double   s_sum[3], s_sumsq[3];
static uint32_t s_n, s_fail, s_cnt, s_stat, s_fixlock;

static void reset_window(void) {
    for (int k = 0; k < 3; ++k) { s_sum[k] = 0.0; s_sumsq[k] = 0.0; }
    s_n = 0; s_fail = 0; s_cnt = 0; s_stat = 0; s_fixlock = 0;
}

static float read_temp_c(void) {
    uint8_t raw[2];
    if (!imu_readBurst(0, REG_TEMP_OUT_H, raw, 2)) return NAN;
    int16_t t = (int16_t)(((uint16_t)raw[0] << 8) | raw[1]);
    return (float)(t / 333.87 + 21.0);   // DS-000189: die temperature
}

static void calibrate_like_firmware(void) {
    const int SAMPLES = 200;
    float sum[3] = {0.0f, 0.0f, 0.0f};
    int valid = 0;
    uint32_t t0 = millis();
    for (int i = 0; i < SAMPLES; ++i) {
        imu_data_t d;
        if (imu_readData(&d)) { sum[0] += d.gx; sum[1] += d.gy; sum[2] += d.gz; valid++; }
        delay(10);
    }
    uint32_t elapsed = millis() - t0;
    for (int k = 0; k < 3; ++k) s_cal[k] = valid > 0 ? sum[k] / valid : 0.0f;
    motion_setBias(s_cal[0], s_cal[1], s_cal[2]);
    Serial.printf("[CAL] bias_x=%+.4f bias_y=%+.4f bias_z=%+.4f dps polls=%d elapsed_ms=%lu temp=%.2f\n",
                  s_cal[0], s_cal[1], s_cal[2], valid, (unsigned long)elapsed, read_temp_c());
}

void setup() {
    Serial.begin(115200);
    delay(1500);
    Serial.println("\n[DRIFT] Air Mouse gyro bias drift measurement 2026-10-04 (ESP32 + WCMCU-20948 only)");
    Serial.printf("[DRIFT] RUN_SECONDS=%d. Keep the board STILL on the table. Nothing is sent over BLE.\n", RUN_SECONDS);

    bool ok = imu_init();
    icm20948_diag_t g = imu_getDiagnostics();
    Serial.printf("[DRIFT] imu_init=%s WHO_AM_I=0x%02X PWR_MGMT_1=0x%02X GYRO_CONFIG_1=0x%02X ACCEL_CONFIG=0x%02X\n",
                  ok ? "PASS" : "FAIL", g.who_am_i, g.pwr_mgmt_1, g.gyro_config_1, g.accel_config);
    if (!ok) { Serial.println("[DRIFT] ABORT: IMU init failed"); s_done = true; return; }

    motion_init(NULL);
    calibrate_like_firmware();

    Serial.println("[D-HDR] t_s temp_C n fail rx ry rz sx sy sz cnt stat fixlock bx by bz  (rx..rz = mean raw gyro - startup cal, dps)");
    reset_window();
    s_last_us = micros();
    s_win_start_ms = millis();
}

void loop() {
    if (s_done) { delay(1000); return; }

    uint32_t now_us = micros();
    if (now_us - s_last_us < 10000) return;      // same 10 ms polling scheme as firmware loop()
    s_last_us = now_us;
    uint32_t now_ms = millis();

    imu_data_t d;
    if (!imu_readData(&d)) { s_fail++; return; }

    mouse_output_t out = motion_process(&d, false, now_ms);
    s_cnt  += (uint32_t)(abs((int)out.delta_x) + abs((int)out.delta_y));
    s_stat += out.is_stationary ? 1u : 0u;

    float rx = d.gx - s_cal[0], ry = d.gy - s_cal[1], rz = d.gz - s_cal[2];
    float gnorm = sqrtf(rx * rx + ry * ry + rz * rz);
    float anorm = sqrtf(d.ax * d.ax + d.ay * d.ay + d.az * d.az);
    if (gnorm < LOCK_GYRO_THRESH && fabsf(anorm - 1.0f) < LOCK_ACCEL_THRESH) {
        if (s_run < 65535) s_run++;
    } else {
        s_run = 0;
    }
    if (s_run > LOCK_WINDOW) s_fixlock++;

    double g3[3] = {d.gx, d.gy, d.gz};
    for (int k = 0; k < 3; ++k) { s_sum[k] += g3[k]; s_sumsq[k] += g3[k] * g3[k]; }
    s_n++;

    if (now_ms - s_win_start_ms >= 1000) {
        s_win_start_ms = now_ms;
        s_sec++;
        double m[3], sd[3];
        for (int k = 0; k < 3; ++k) {
            m[k] = s_n ? s_sum[k] / s_n : 0.0;
            double var = s_n > 1 ? (s_sumsq[k] - s_n * m[k] * m[k]) / (s_n - 1) : 0.0;
            sd[k] = var > 0.0 ? sqrt(var) : 0.0;
        }
        float bx, by, bz;
        motion_getBias(&bx, &by, &bz);
        Serial.printf("[D] %lu %.2f %lu %lu %+.4f %+.4f %+.4f %.4f %.4f %.4f %lu %lu %lu %+.4f %+.4f %+.4f\n",
                      (unsigned long)s_sec, read_temp_c(), (unsigned long)s_n, (unsigned long)s_fail,
                      m[0] - s_cal[0], m[1] - s_cal[1], m[2] - s_cal[2], sd[0], sd[1], sd[2],
                      (unsigned long)s_cnt, (unsigned long)s_stat, (unsigned long)s_fixlock, bx, by, bz);
        reset_window();
        if (s_sec >= RUN_SECONDS) {
            Serial.printf("[DRIFT] DONE seconds=%lu\n", (unsigned long)s_sec);
            s_done = true;
        }
    }
}
