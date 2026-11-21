#include <Arduino.h>
#include <math.h>
#include <string.h>
#include "app_imu_guard.h"
#include "app_imu.h"
#include "app_timing.h"
#include "imu_health.h"
#include "motion_pipeline.h"     // motion_getBias(), motion_surface_rest_bias_bad()

static imu_health_t s_health;
static bool s_health_init = false;
static uint16_t s_cnt_heal = 0;

uint16_t app_imu_frozen_count(void)    { return (uint16_t)s_health.reinit_total; }
uint16_t app_imu_heal_count(void)      { return s_cnt_heal; }
uint32_t app_imu_read_fail_count(void) { return s_health.fail_total; }
uint32_t app_imu_bus_recover_count(void) { return imu_getBusRecoveries(); }

bool app_imu_health_step(bool read_ok, const imu_data_t& d, uint32_t now_ms) {
    if (!s_health_init) { ih_init(&s_health); s_health_init = true; }
    ih_action_t a = ih_update(&s_health, now_ms, read_ok, &d);
    if (a == IH_OK) return true;
    if (a == IH_REINIT) {
        uint32_t t0 = millis();
        bool bus = imu_busRecover();
        bool ok = imu_init();
        ih_note_reinit(&s_health, millis(), ok);
        Serial.printf("[IMU] sensor lost (%s) -> I2C bus recover %s, imu_init %s, %lu ms (old bias kept; fails %lu, re-inits %lu)\n",
                      ih_reason_name(s_health.reason), bus ? "OK" : "FAILED (a line is stuck low)", ok ? "PASS" : "FAIL",
                      (unsigned long)(millis() - t0), (unsigned long)s_health.fail_total, (unsigned long)s_health.reinit_total);
        app_resync();                                    // the re-initialisation took a while: restart the 10 ms schedule
    }
    return false;
}

bool app_imu_self_heal(const imu_data_t& d) {
    static double sum[6], sumsq[6];
    static int n = 0;
    static uint8_t hits = 0;

    const double v[6] = {d.gx, d.gy, d.gz, d.ax, d.ay, d.az};
    for (int k = 0; k < 6; ++k) { sum[k] += v[k]; sumsq[k] += v[k] * v[k]; }
    if (++n < 100) return false;

    float mean[6], sd[6];
    for (int k = 0; k < 6; ++k) {
        mean[k] = (float)(sum[k] / n);
        double var = (sumsq[k] - n * (double)mean[k] * mean[k]) / (n - 1);
        sd[k] = var > 0.0 ? (float)sqrt(var) : 0.0f;
        sum[k] = 0.0; sumsq[k] = 0.0;
    }
    n = 0;

    float bias[3];
    motion_getBias(&bias[0], &bias[1], &bias[2]);
    float anorm = sqrtf(mean[3] * mean[3] + mean[4] * mean[4] + mean[5] * mean[5]);
    if (!motion_surface_rest_bias_bad(sd, sd + 3, anorm, mean, bias)) { hits = 0; return false; }
    if (++hits < 3) return false;
    hits = 0;

    Serial.printf("[HEAL] Resting on a surface but bias is off by %.2f/%.2f/%.2f dps -> recalibrating\n",
                  mean[0] - bias[0], mean[1] - bias[1], mean[2] - bias[2]);
    s_cnt_heal++;
    app_imu_calibrate(1, false);
    return true;
}
