// =============================================================================
// Air Mouse bench measurements (runs once after reset, then idles)
//  B1: WHO_AM_I + register readback (same imu_init() as main firmware)
//  B2: time per imu_readData() (12-byte burst) at 400 kHz and 100 kHz
//  B3: static noise of raw gyro/accel LSB (device at rest on the table)
//  B4: die temperature from TEMP_OUT (DS-000189 formula)
//  B5: 10 ms polling-loop period jitter (same scheme as firmware loop())
// =============================================================================
#include <Arduino.h>
#include <Wire.h>
#include <math.h>
#include "pin_definitions.h"
#include "icm20948_registers.h"
#include "icm20948_driver.h"

static void time_burst(uint32_t clock_hz, int n) {
    Wire.setClock(clock_hz);
    imu_data_t d;
    uint32_t tmin = 0xFFFFFFFF, tmax = 0, fails = 0;
    uint64_t tsum = 0;
    for (int i = 0; i < n; ++i) {
        uint32_t t0 = micros();
        bool ok = imu_readData(&d);
        uint32_t dt = micros() - t0;
        if (!ok) { fails++; continue; }
        tsum += dt;
        if (dt < tmin) tmin = dt;
        if (dt > tmax) tmax = dt;
        delayMicroseconds(200);
    }
    uint32_t okn = n - fails;
    Serial.printf("[B2] I2C %lu Hz | N=%d | burst12 us: min=%lu avg=%.1f max=%lu | fails=%lu\n",
                  (unsigned long)clock_hz, n, (unsigned long)tmin,
                  okn ? (double)tsum / okn : 0.0, (unsigned long)tmax, (unsigned long)fails);
}

static void noise_stats(int n) {
    // Raw LSB statistics (Welford) for 6 axes + accel magnitude
    double mean[6] = {0}, m2[6] = {0}, mag_mean = 0;
    int16_t vmin[6], vmax[6];
    for (int k = 0; k < 6; ++k) { vmin[k] = 32767; vmax[k] = -32768; }
    int cnt = 0, fails = 0;
    for (int i = 0; i < n; ++i) {
        uint8_t raw[12];
        if (!imu_readBurst(0, REG_ACCEL_XOUT_H, raw, 12)) { fails++; delay(10); continue; }
        cnt++;
        int16_t v[6];
        for (int k = 0; k < 6; ++k) v[k] = (int16_t)(((uint16_t)raw[2 * k] << 8) | raw[2 * k + 1]);
        for (int k = 0; k < 6; ++k) {
            double delta = v[k] - mean[k];
            mean[k] += delta / cnt;
            m2[k] += delta * (v[k] - mean[k]);
            if (v[k] < vmin[k]) vmin[k] = v[k];
            if (v[k] > vmax[k]) vmax[k] = v[k];
        }
        double mag = sqrt((double)v[0] * v[0] + (double)v[1] * v[1] + (double)v[2] * v[2]);
        mag_mean += (mag - mag_mean) / cnt;
        delay(10);
    }
    const char* name[6] = {"AX", "AY", "AZ", "GX", "GY", "GZ"};
    Serial.printf("[B3] static noise | N=%d | fails=%d | ACCEL +/-4g (8192 LSB/g), GYRO +/-500dps (65.5 LSB/dps)\n", cnt, fails);
    for (int k = 0; k < 6; ++k) {
        double sd = cnt > 1 ? sqrt(m2[k] / (cnt - 1)) : 0.0;
        double scale = (k < 3) ? 8192.0 : 65.5;
        const char* unit = (k < 3) ? "g" : "dps";
        Serial.printf("[B3] %s mean=%+9.1f LSB (%+.4f %s) sd=%6.2f LSB (%.4f %s) min=%d max=%d\n",
                      name[k], mean[k], mean[k] / scale, unit, sd, sd / scale, unit, vmin[k], vmax[k]);
    }
    Serial.printf("[B3] |A| mean=%.1f LSB -> %.4f g (expected ~8192 LSB = 1 g at rest)\n", mag_mean, mag_mean / 8192.0);
}

static void temperature(void) {
    uint8_t raw[2];
    if (!imu_readBurst(0, REG_TEMP_OUT_H, raw, 2)) { Serial.println("[B4] TEMP read FAIL"); return; }
    int16_t t = (int16_t)(((uint16_t)raw[0] << 8) | raw[1]);
    // DS-000189: TEMP_degC = ((TEMP_OUT - RoomTemp_Offset) / 333.87) + 21, offset = 0
    Serial.printf("[B4] TEMP_OUT raw=%d -> %.2f degC (die temperature, not ambient)\n", t, t / 333.87 + 21.0);
}

static void loop_jitter(int n) {
    uint32_t last = micros(), pmin = 0xFFFFFFFF, pmax = 0, over = 0;
    uint64_t psum = 0;
    int got = 0;
    imu_data_t d;
    while (got < n) {
        uint32_t now = micros();
        if (now - last < 10000) continue;    // same polling scheme as firmware loop()
        uint32_t period = now - last;
        last = now;
        imu_readData(&d);
        psum += period; got++;
        if (period < pmin) pmin = period;
        if (period > pmax) pmax = period;
        if (period > 10100) over++;
    }
    Serial.printf("[B5] 10ms polling loop | N=%d | period us: min=%lu avg=%.1f max=%lu | >10.1ms: %lu\n",
                  n, (unsigned long)pmin, (double)psum / n, (unsigned long)pmax, (unsigned long)over);
}

void setup() {
    Serial.begin(115200);
    delay(1500);
    Serial.println("\n[BENCH] Air Mouse bench measurements 2026-10-01 (ESP32 + WCMCU-20948 only)");
    Serial.printf("[BENCH] CPU %lu MHz, APB %lu Hz\n", (unsigned long)getCpuFrequencyMhz(), (unsigned long)getApbFrequency());

    bool ok = imu_init();
    icm20948_diag_t g = imu_getDiagnostics();
    Serial.printf("[B1] imu_init=%s WHO_AM_I=0x%02X PWR_MGMT_1=0x%02X GYRO_CONFIG_1=0x%02X ACCEL_CONFIG=0x%02X GYRO_DIV=%u ACCEL_DIV=%u\n",
                  ok ? "PASS" : "FAIL", g.who_am_i, g.pwr_mgmt_1, g.gyro_config_1, g.accel_config,
                  g.gyro_smplrt_div, ((unsigned)g.accel_smplrt_div_1 << 8) | g.accel_smplrt_div_2);
    if (!ok) { Serial.println("[BENCH] ABORT: IMU init failed"); return; }
    delay(100);

    time_burst(400000, 1000);
    time_burst(100000, 1000);
    Wire.setClock(400000);

    Serial.println("[B3] Keep the board still on the table ...");
    noise_stats(1000);
    temperature();
    loop_jitter(500);
    Serial.println("[BENCH] DONE");
}

void loop() {
    delay(1000);
}
