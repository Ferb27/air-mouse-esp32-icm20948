#ifndef APP_IMU_H
#define APP_IMU_H

#include <stdbool.h>
#include "icm20948_driver.h"

// Sensor access in the PIPELINE axis frame + gyro bias calibration.

// Read one sample and rotate the sensor axes into the pipeline frame.
// Measured 2026-10-08 (docs/ORIENT_MEASUREMENT_2026-10-08.md): board held like a TV remote (USB cable toward the wrist,
// nose toward the screen, chip face up) reads sensor +X = LEFT, +Y = BACKWARD (toward wrist), +Z = UP. The pipeline
// expects X = backward, Y = right, Z = up, so x_p = y_s, y_p = -x_s, z_p = z_s (a proper rotation about Z).
// Applied to accel AND gyro, before calibration and before motion_process().
bool app_imu_read(imu_data_t* d);

// Gyro bias calibration: APP_CAL_SAMPLES samples (2 s) per attempt, each window VALIDATED (|a| ~ 1 g, std-dev and
// first-half vs second-half mean, see bias_checks.h). Returns true if a valid (still) window was found. If none was,
// the last attempt is applied only when apply_if_rejected (startup); runtime callers keep the previous bias.
bool app_imu_calibrate(int max_attempts, bool apply_if_rejected);
void app_imu_calibrate_startup(void);

#endif // APP_IMU_H
