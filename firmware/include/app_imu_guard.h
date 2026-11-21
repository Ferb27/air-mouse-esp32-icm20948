#ifndef APP_IMU_GUARD_H
#define APP_IMU_GUARD_H

#include <stdint.h>
#include <stdbool.h>
#include "icm20948_driver.h"

// Protections against a bad / dead gyro, run every tick from loop(). The self-heal returns true when it ran a (possibly
// blocking) action, in which case the caller should skip the rest of this tick and call app_resync().

// Sensor health step (imu_health.h), once per tick right after the read: read_ok = the I2C read succeeded.
// Returns true when the sample is usable. Otherwise the sample must be skipped (return from this tick): it was a failed
// read, an all-zero sample from a sensor that lost its state, or a re-initialisation was just done (bus recovery +
// imu_init, a few tens of ms, the old bias is kept; the 10 ms schedule is restarted by this function).
bool app_imu_health_step(bool read_ok, const imu_data_t& d, uint32_t now_ms);

// Self-heal: if the board rests on a surface (very still accelerometer, quiet gyro) for 3 consecutive 1 s windows but
// the stored bias is clearly wrong (so the stationary lock can never engage), recalibrate once, validated.
bool app_imu_self_heal(const imu_data_t& d);

// Counters since boot (shown in [STATUS] as Frz / Heal / Err / Rec): sensor re-initialisations, self-heal
// recalibrations, failed I2C reads, I2C bus recoveries.
uint16_t app_imu_frozen_count(void);
uint16_t app_imu_heal_count(void);
uint32_t app_imu_read_fail_count(void);
uint32_t app_imu_bus_recover_count(void);

#endif // APP_IMU_GUARD_H
