#ifndef MOTION_PIPELINE_H
#define MOTION_PIPELINE_H

#include <stdint.h>
#include <stdbool.h>
#include "icm20948_driver.h"
#include "gesture_detector.h"
#include "bias_checks.h"   // motion_calibration_still(), motion_surface_rest_bias_bad()

#ifdef __cplusplus
extern "C" {
#endif

typedef struct {
    float gyro_deadzone_low;    // RESERVED, unused since tightening
    float gyro_deadzone_high;   // tightening threshold T in dps (default 1.4)
    float gain_x;               // sensitivity gain, counts/sample per dps (default 0.3)
    float gain_y;               // sensitivity gain, counts/sample per dps (default 0.3)
    float stat_gyro_thresh;     // default 0.4 dps
    float stat_accel_thresh;    // g (e.g. 0.08)
    uint16_t stat_window_count; // samples (e.g. 30 samples @ 100Hz = 300ms)
    float auto_zero_alpha;      // adaptation factor (e.g. 0.002)
} motion_config_t;

typedef struct {
    int8_t delta_x;             // Clamped mouse X increment (-127 to +127)
    int8_t delta_y;             // Clamped mouse Y increment (-127 to +127)
    bool is_stationary;         // True when device is stationary
    bool is_clutch_active;      // True when clutch button is held (cursor frozen)
    gesture_event_t gesture;    // Detected flick gesture
    float filtered_gx;          // Filtered & compensated dps
    float filtered_gy;
    float filtered_gz;
    bool recentered;            // True on the tick when the reference orientation was re-centered (Mode button)
    float hold_peak_yaw_dps;    // Set on the tick the Mode button is released: largest turning rate during the hold (+ = left)
    float hold_peak_alat_g;     // ... and largest lateral acceleration during the hold (+ = right), for threshold tuning
} mouse_output_t;

// Quaternion 4D for 6-axis attitude representation
typedef struct {
    float q0; // Scalar (w)
    float q1; // x
    float q2; // y
    float q3; // z
} quat_t;

// Vector 3D for reference frame and spatial vectors
typedef struct {
    float x;
    float y;
    float z;
} vec3_t;

void motion_init(const motion_config_t* cfg);
void motion_setBias(float bx, float by, float bz);
void motion_getBias(float* bx, float* by, float* bz);

// Runtime sensitivity tuning (counts per sample per deg/s; default 0.3)
void motion_setGain(float gx, float gy);
void motion_getGain(float* gx, float* gy);

// Mode / Clutch button options.
// Flick gestures (Back/Forward while the button is held): enabled by default; the user setting flick_enable switches them off.
void motion_setGesturesEnabled(bool enabled);
// Quick-turn flick while the Mode button is held: turning rate above this (deg/s) = flick LEFT (Back) when turning
// left, flick RIGHT (Forward) when turning right. 0 = off (default). Works alongside the lateral-acceleration flick.
void motion_setYawFlickThresholdDps(float dps);
// After the Mode button is RELEASED, wait this long (cursor frozen) before re-centering, so the thumb's own
// press/release jerk does not tilt the new reference. 0 = re-center immediately (default).
void motion_setRecenterSettleMs(uint16_t settle_ms);

// Recenter current orientation as reference frame
void motion_recenter(const imu_data_t* imu);
// Re-center after the settle time (motion_setRecenterSettleMs), cursor frozen meanwhile. Used when scroll mode ends,
// where the Mode button never went through the clutch release.
void motion_scheduleRecenter(uint32_t now_ms);

// Main pipeline processing tick
mouse_output_t motion_process(const imu_data_t* imu, bool clutch_pressed, uint32_t now_ms);

// Retrieve 6-axis estimated attitude quaternion (Pitch/Roll tilt-corrected; Yaw relative)
void motion_getAttitude(float* q0, float* q1, float* q2, float* q3);

// Explicitly set estimated attitude quaternion (test/diagnostic API, exposed on host test environments)
#if !defined(ARDUINO) || defined(HOST_TEST) || defined(UNIT_TEST)
void motion_setAttitude(float q0, float q1, float q2, float q3);
#endif

// Retrieve estimated gravity vector in body coordinates
void motion_getBodyGravity(float* gx, float* gy, float* gz);

// Retrieve linear acceleration in body coordinates (gravity subtracted)
void motion_getLinearAccel(float* ax, float* ay, float* az);

#ifdef __cplusplus
}
#endif

#endif // MOTION_PIPELINE_H
