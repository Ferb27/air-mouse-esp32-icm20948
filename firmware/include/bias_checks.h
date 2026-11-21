#ifndef BIAS_CHECKS_H
#define BIAS_CHECKS_H

#include <stdbool.h>

#ifdef __cplusplus
extern "C" {
#endif

// Pure decision functions for the gyro bias protections (portable: unit-tested on the PC).

// Calibration window check: sd = per-axis std-dev over the window, mean_a / mean_b = per-axis mean of the first /
// second half (dps). True when the board looks like it was RESTING on a surface: sd in [0.005, 0.35] dps (a live gyro
// always has noise; sd ~ 0 means a frozen sensor) and the two halves agree within 0.25 dps on every axis.
bool motion_calibration_still(const float sd[3], const float mean_a[3], const float mean_b[3]);

// Self-heal check on a 1 s window of raw samples: true when the board is resting ON A SURFACE (gyro sd <= 0.35 dps,
// accelerometer sd <= 0.005 g on every axis, |a| within 0.08 g of 1 g) yet the stored bias is clearly wrong
// (|gyro_mean - bias| > 0.5 dps), i.e. the stationary lock can never engage. Hand-held tremor fails the accel test.
bool motion_surface_rest_bias_bad(const float gyro_sd[3], const float accel_sd[3], float accel_norm,
                                  const float gyro_mean[3], const float bias[3]);

#ifdef __cplusplus
}
#endif

#endif // BIAS_CHECKS_H
