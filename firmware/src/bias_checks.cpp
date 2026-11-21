#include "../include/bias_checks.h"
#include <math.h>

bool motion_surface_rest_bias_bad(const float gyro_sd[3], const float accel_sd[3], float accel_norm,
                                  const float gyro_mean[3], const float bias[3]) {
    for (int k = 0; k < 3; ++k) {
        if (!(gyro_sd[k] <= 0.35f)) return false;
        if (!(accel_sd[k] <= 0.005f)) return false;      // table noise is ~0.002 g; hand-held steadiest measured 0.010 g (08/10 orient log); table raw ~0.002 g
    }
    if (!(fabsf(accel_norm - 1.0f) <= 0.08f)) return false;
    float r2 = 0.0f;
    for (int k = 0; k < 3; ++k) {
        float d = gyro_mean[k] - bias[k];
        r2 += d * d;
    }
    return r2 > 0.5f * 0.5f;
}

bool motion_calibration_still(const float sd[3], const float mean_a[3], const float mean_b[3]) {
    for (int k = 0; k < 3; ++k) {
        if (!(sd[k] >= 0.005f)) return false;                     // a live gyro always has noise (~0.09 dps): sd ~ 0 = frozen sensor
        if (!(sd[k] <= 0.35f)) return false;                       // jitter far above sensor noise (~0.1 dps)
        if (!(fabsf(mean_a[k] - mean_b[k]) <= 0.25f)) return false; // mean moved during the window
    }
    return true;
}
