#ifndef IMU_HEALTH_H
#define IMU_HEALTH_H

#include <stdint.h>
#include <stdbool.h>
#include "icm20948_driver.h"

#ifdef __cplusplus
extern "C" {
#endif

// Sensor health monitor (PORTABLE CORE, tested on the PC: N25). Decides, once per 10 ms tick, whether the sample is
// usable and when the ICM-20948 / the I2C bus must be recovered.
//
// What was seen on the real board (logs 17/10 and 22/10/2026): touching, pressing or shaking the breadboard made the
// sensor lose its state (it falls back to sleep and returns all zeros) and the I2C read failed ("Error -1" / "Error 263").
// The old watchdog needed 50 samples (0.5 s) of |a| < 0.5 g to notice, during which the zeros went into the pipeline
// ((0 - bias) is a constant ~1.3 dps) and the cursor drifted; a failing bus was not noticed at all because the watchdog
// only ran after a SUCCESSFUL read. Now:
//   * a failed read is dropped at once; 3 failed reads in a row -> recover the bus and re-initialise the sensor;
//   * a sample whose accelerometer is exactly 0,0,0 (impossible for a live sensor: it always sees ~1 g plus noise) is
//     dropped at once; 3 in a row -> re-initialise;
//   * the older slow rules stay as a safety net: 100 identical samples, or |a| < 0.5 g for 50 samples;
//   * after a re-initialisation the sensor needs a moment to start (gyro ~35 ms): samples are dropped for IH_SETTLE_MS
//     without counting, and the next recovery is not allowed before IH_MIN_GAP_OK_MS (IH_MIN_GAP_FAIL_MS if the last
//     re-initialisation FAILED, so a really missing sensor does not make the loop spin).
#define IH_FAIL_RUN          3
#define IH_ZERO_RUN          3
#define IH_SAME_RUN          100
#define IH_DEAD_RUN          50
#define IH_SETTLE_MS         80
#define IH_MIN_GAP_OK_MS     300
#define IH_MIN_GAP_FAIL_MS   3000

typedef enum { IH_OK = 0, IH_DROP, IH_REINIT } ih_action_t;
typedef enum { IH_WHY_NONE = 0, IH_WHY_READ_FAIL, IH_WHY_ZERO, IH_WHY_FROZEN, IH_WHY_DEAD } ih_reason_t;

typedef struct {
    uint8_t  fail_run;
    uint8_t  zero_run;
    uint16_t same_run;
    uint16_t dead_run;
    float    last[6];
    bool     have_last;
    uint32_t settle_until_ms;
    uint32_t last_reinit_ms;
    bool     last_reinit_ok;
    bool     ever_reinit;
    ih_reason_t reason;          // why the last IH_REINIT was requested
    uint32_t fail_total;         // failed reads since boot
    uint32_t zero_total;         // dropped all-zero samples since boot
    uint32_t reinit_total;       // IH_REINIT requests since boot
} imu_health_t;

void ih_init(imu_health_t* h);
// Call once per tick. read_ok = the I2C read succeeded (d is then valid; d may be NULL when read_ok is false).
// IH_OK: use the sample. IH_DROP: ignore this sample. IH_REINIT: recover the bus + re-initialise the sensor now, then
// call ih_note_reinit(); this sample is dropped too.
ih_action_t ih_update(imu_health_t* h, uint32_t now_ms, bool read_ok, const imu_data_t* d);
// Tell the monitor the outcome of the re-initialisation that IH_REINIT asked for (now_ms = time after it finished).
void ih_note_reinit(imu_health_t* h, uint32_t now_ms, bool ok);
const char* ih_reason_name(ih_reason_t r);

#ifdef __cplusplus
}
#endif

#endif // IMU_HEALTH_H
