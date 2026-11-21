#include <Arduino.h>
#include <math.h>
#include "app_imu.h"
#include "app_config.h"
#include "pin_definitions.h"
#include "motion_pipeline.h"     // motion_setBias(), bias_checks.h

bool app_imu_read(imu_data_t* d) {
    if (!imu_readData(d)) return false;
    float ax = d->ax, gx = d->gx;
    d->ax = d->ay;  d->ay = -ax;
    d->gx = d->gy;  d->gy = -gx;
    return true;
}

bool app_imu_calibrate(int max_attempts, bool apply_if_rejected) {
    const int SAMPLES = APP_CAL_SAMPLES;
    float bx = 0.0f, by = 0.0f, bz = 0.0f;
    bool accepted = false;

    Serial.println("\n[CALIBRATION] Commencing Gyro Bias Calibration (2 s per attempt)...");
    Serial.println("[CALIBRATION] Please leave the device completely STATIONARY on the table.");
    digitalWrite(PIN_LED_STATUS, HIGH);

    for (int attempt = 1; attempt <= max_attempts && !accepted; ++attempt) {
        double sum[3] = {0, 0, 0}, sumsq[3] = {0, 0, 0}, sum_a[3] = {0, 0, 0}, sum_b[3] = {0, 0, 0}, acc[3] = {0, 0, 0};
        int n = 0, n_a = 0, n_b = 0;
        uint32_t t_start = millis();

        for (int i = 0; i < SAMPLES; ++i) {
            imu_data_t data;
            if (app_imu_read(&data)) {
                const double g[3] = {data.gx, data.gy, data.gz};
                acc[0] += data.ax; acc[1] += data.ay; acc[2] += data.az;
                for (int k = 0; k < 3; ++k) {
                    sum[k] += g[k];
                    sumsq[k] += g[k] * g[k];
                    if (i < SAMPLES / 2) sum_a[k] += g[k]; else sum_b[k] += g[k];
                }
                n++;
                if (i < SAMPLES / 2) n_a++; else n_b++;
            }
            if ((i % 25) == 0) {
                digitalWrite(PIN_LED_STATUS, !digitalRead(PIN_LED_STATUS));
            }
            delay(10);
        }
        uint32_t elapsed_ms = millis() - t_start;

        float mean[3] = {0, 0, 0}, sd[3] = {0, 0, 0}, ma[3] = {0, 0, 0}, mb[3] = {0, 0, 0};
        if (n > 1 && n_a > 0 && n_b > 0) {
            for (int k = 0; k < 3; ++k) {
                mean[k] = (float)(sum[k] / n);
                double var = (sumsq[k] - n * (double)mean[k] * mean[k]) / (n - 1);
                sd[k] = var > 0.0 ? (float)sqrt(var) : 0.0f;
                ma[k] = (float)(sum_a[k] / n_a);
                mb[k] = (float)(sum_b[k] / n_b);
            }
        }
        bx = mean[0]; by = mean[1]; bz = mean[2];
        // Gravity must read ~1 g: a dead/frozen sensor returns 0 g and would otherwise "calibrate" a bogus bias of 0.
        float anorm = (n > 0) ? (float)(sqrt(acc[0] * acc[0] + acc[1] * acc[1] + acc[2] * acc[2]) / n) : 0.0f;
        bool still = (n >= SAMPLES * 9 / 10) && fabsf(anorm - 1.0f) <= 0.15f && motion_calibration_still(sd, ma, mb);

        Serial.printf("[CALIBRATION] Attempt %d: %lu ms, %d polls, |a| = %.3f g, sd = %.2f/%.2f/%.2f dps, half-mean diff = %.2f/%.2f/%.2f dps -> %s\n",
                      attempt, (unsigned long)elapsed_ms, n, anorm, sd[0], sd[1], sd[2],
                      fabsf(ma[0] - mb[0]), fabsf(ma[1] - mb[1]), fabsf(ma[2] - mb[2]),
                      still ? "ACCEPTED" : "REJECTED (board not still), retrying");
        accepted = still;
    }
    if (!accepted) {
        if (apply_if_rejected) {
            Serial.println("[CALIBRATION][WARN] Board never held still; using the last attempt. It will recalibrate by itself once it rests on a surface (or send 'c').");
        } else {
            Serial.println("[CALIBRATION][WARN] Board not still; keeping the previous bias.");
        }
    }

    if (accepted || apply_if_rejected) {
        motion_setBias(bx, by, bz);
        Serial.printf("[CALIBRATION] Zero-Rate Bias: X = %+6.2f dps | Y = %+6.2f dps | Z = %+6.2f dps\n", bx, by, bz);
    }
    digitalWrite(PIN_LED_STATUS, LOW);
    return accepted;
}

void app_imu_calibrate_startup(void) {
    app_imu_calibrate(APP_CAL_STARTUP_ATTEMPTS, true);
}
