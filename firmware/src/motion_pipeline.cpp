#include "motion_pipeline.h"
#include "yaw_flick.h"
#include <math.h>

#define RAD_PER_DEG 0.017453292519943295f
#define DEG_PER_RAD 57.29577951308232f
#define AUTO_ZERO_MIN_REST_SAMPLES 150

static motion_config_t s_cfg;
static float s_bias_x = 0.0f;
static float s_bias_y = 0.0f;
static float s_bias_z = 0.0f;

static uint16_t s_stat_counter = 0;
static uint16_t s_rest_counter = 0;
static bool s_is_stationary = false;
static bool s_last_clutch_state = false;
static bool s_gesture_occurred_in_clutch = false;
static bool s_gestures_enabled = true;        // settings below survive motion_init()
static uint16_t s_recenter_settle_ms = 0;
static bool s_recenter_pending = false;
static uint32_t s_recenter_due_ms = 0;
// Quick-turn (yaw-rate) flick while the Mode button is held (see yaw_flick.h)
static yaw_flick_t s_yf = { 0.0f, false, 0 };
static float s_hold_peak_yaw = 0.0f;
static float s_hold_peak_alat = 0.0f;
static uint32_t s_last_process_ms = 0;
static bool s_has_last_ms = false;
static float s_rem_x = 0.0f;
static float s_rem_y = 0.0f;

// 6-Axis Estimated Attitude Quaternion: q = [q0, q1, q2, q3]
// q0: scalar (w), [q1, q2, q3]: vector (x, y, z)
// Represents orientation relative to world horizontal plane where +Z points up (gravity reaction).
// NOTE: Pitch & Roll are tilt-corrected by accelerometer; Yaw is purely gyro-integrated (RELATIVE and drifting).
static quat_t s_q = {1.0f, 0.0f, 0.0f, 0.0f};

// Direction cosine vector representing gravity in body frame (unit vector pointing UP in resting pose)
static vec3_t s_body_gravity = {0.0f, 0.0f, 1.0f};

// Linear acceleration in body frame with gravity subtracted (in g)
static vec3_t s_linear_accel = {0.0f, 0.0f, 0.0f};

// Reference gravity vector at clutch release / recenter
static vec3_t s_ref_gravity = {0.0f, 0.0f, 1.0f};

// Low-pass filtered acceleration for quasi-static reference
static vec3_t s_accel_filt = {0.0f, 0.0f, 1.0f};

static float apply_tightening(float val, float threshold) {
    float a = fabsf(val);
    if (a >= threshold) return val;
    return val * (a / threshold);     // = dấu(val) * a*a / threshold
}

static int8_t clamp_i8(int32_t val) {
    if (val > 127) return 127;
    if (val < -127) return -127;
    return (int8_t)val;
}

void motion_init(const motion_config_t* cfg) {
    if (cfg) {
        s_cfg = *cfg;
    } else {
        s_cfg.gyro_deadzone_low  = 0.0f;   // RESERVED, unused since tightening
        s_cfg.gyro_deadzone_high = 1.4f;   // Tightening threshold T in dps
        // Gain = counts per sample per (deg/s); at 100 Hz, 1 deg of rotation = 100 * gain counts.
        // 0.3 -> ~30 counts/deg (was 2.2 -> ~220 counts/deg, far too sensitive in hand tests).
        s_cfg.gain_x             = 0.3f;   // Horizontal gain
        s_cfg.gain_y             = 0.3f;   // Vertical gain
        s_cfg.stat_gyro_thresh   = 0.4f;   // 0.4 dps (stricter stationary threshold)
        s_cfg.stat_accel_thresh  = 0.08f;  // 0.08g deviation from 1g
        s_cfg.stat_window_count  = 30;     // 30 samples (~300 ms @ nominal 100 Hz)
        s_cfg.auto_zero_alpha    = 0.002f; // Slow adaptive auto-zero
    }

    s_bias_x = 0.0f;
    s_bias_y = 0.0f;
    s_bias_z = 0.0f;
    s_stat_counter = 0;
    s_rest_counter = 0;
    s_is_stationary = false;
    s_last_clutch_state = false;
    s_gesture_occurred_in_clutch = false;
    s_recenter_pending = false;
    yf_reset(&s_yf);
    s_hold_peak_yaw = 0.0f;
    s_hold_peak_alat = 0.0f;
    s_last_process_ms = 0;
    s_has_last_ms = false;

    // Reset attitude quaternion to identity
    s_q.q0 = 1.0f;
    s_q.q1 = 0.0f;
    s_q.q2 = 0.0f;
    s_q.q3 = 0.0f;

    s_body_gravity.x = 0.0f;
    s_body_gravity.y = 0.0f;
    s_body_gravity.z = 1.0f;

    s_linear_accel.x = 0.0f;
    s_linear_accel.y = 0.0f;
    s_linear_accel.z = 0.0f;

    s_ref_gravity.x = 0.0f;
    s_ref_gravity.y = 0.0f;
    s_ref_gravity.z = 1.0f;

    s_accel_filt.x = 0.0f;
    s_accel_filt.y = 0.0f;
    s_accel_filt.z = 1.0f;

    s_rem_x = 0.0f;
    s_rem_y = 0.0f;

    gesture_init(NULL);
}

void motion_setBias(float bx, float by, float bz) {
    s_bias_x = bx;
    s_bias_y = by;
    s_bias_z = bz;
}

void motion_getBias(float* bx, float* by, float* bz) {
    if (bx) *bx = s_bias_x;
    if (by) *by = s_bias_y;
    if (bz) *bz = s_bias_z;
}

void motion_setGesturesEnabled(bool enabled) {
    s_gestures_enabled = enabled;
}

void motion_setYawFlickThresholdDps(float dps) {
    yf_set_threshold(&s_yf, dps);
}

void motion_setRecenterSettleMs(uint16_t settle_ms) {
    s_recenter_settle_ms = settle_ms;
}

void motion_setGain(float gx, float gy) {
    s_cfg.gain_x = gx;
    s_cfg.gain_y = gy;
}

void motion_getGain(float* gx, float* gy) {
    if (gx) *gx = s_cfg.gain_x;
    if (gy) *gy = s_cfg.gain_y;
}

void motion_recenter(const imu_data_t* imu) {
    s_rem_x = 0.0f;
    s_rem_y = 0.0f;
    if (!imu) return;

    // Use current low-pass filtered acceleration vector to re-establish reference vertical
    float norm = sqrtf(s_accel_filt.x * s_accel_filt.x +
                       s_accel_filt.y * s_accel_filt.y +
                       s_accel_filt.z * s_accel_filt.z);
    if (norm > 0.5f) {
        float inv_norm = 1.0f / norm;
        s_ref_gravity.x = s_accel_filt.x * inv_norm;
        s_ref_gravity.y = s_accel_filt.y * inv_norm;
        s_ref_gravity.z = s_accel_filt.z * inv_norm;
        s_body_gravity = s_ref_gravity;

        // Snap attitude quaternion tilt to match current reference gravity vector
        // Rotation aligning [0, 0, 1] with s_ref_gravity
        float dot = s_ref_gravity.z;
        if (dot > -0.999f) {
            s_q.q0 = 1.0f + dot;
            s_q.q1 = -s_ref_gravity.y;
            s_q.q2 =  s_ref_gravity.x;
            s_q.q3 = 0.0f; // Relative yaw is reset to 0 at recenter
            float qn = sqrtf(s_q.q0*s_q.q0 + s_q.q1*s_q.q1 + s_q.q2*s_q.q2);
            if (qn > 1e-6f) {
                float inv_qn = 1.0f / qn;
                s_q.q0 *= inv_qn;
                s_q.q1 *= inv_qn;
                s_q.q2 *= inv_qn;
                s_q.q3 = 0.0f;
            }
        }
    }
}

void motion_scheduleRecenter(uint32_t now_ms) {
    s_rem_x = 0.0f;
    s_rem_y = 0.0f;
    s_recenter_pending = true;
    s_recenter_due_ms = now_ms + s_recenter_settle_ms;
}

void motion_getAttitude(float* q0, float* q1, float* q2, float* q3) {
    if (q0) *q0 = s_q.q0;
    if (q1) *q1 = s_q.q1;
    if (q2) *q2 = s_q.q2;
    if (q3) *q3 = s_q.q3;
}

#if !defined(ARDUINO) || defined(HOST_TEST) || defined(UNIT_TEST)
void motion_setAttitude(float q0, float q1, float q2, float q3) {
    float norm = sqrtf(q0 * q0 + q1 * q1 + q2 * q2 + q3 * q3);
    if (norm > 1e-6f) {
        float inv = 1.0f / norm;
        s_q.q0 = q0 * inv;
        s_q.q1 = q1 * inv;
        s_q.q2 = q2 * inv;
        s_q.q3 = q3 * inv;
    }
    // Synchronize body gravity with newly set attitude
    s_body_gravity.x = 2.0f * (s_q.q1 * s_q.q3 - s_q.q0 * s_q.q2);
    s_body_gravity.y = 2.0f * (s_q.q0 * s_q.q1 + s_q.q2 * s_q.q3);
    s_body_gravity.z = s_q.q0 * s_q.q0 - s_q.q1 * s_q.q1 - s_q.q2 * s_q.q2 + s_q.q3 * s_q.q3;
}
#endif

void motion_getBodyGravity(float* gx, float* gy, float* gz) {
    if (gx) *gx = s_body_gravity.x;
    if (gy) *gy = s_body_gravity.y;
    if (gz) *gz = s_body_gravity.z;
}

void motion_getLinearAccel(float* ax, float* ay, float* az) {
    if (ax) *ax = s_linear_accel.x;
    if (ay) *ay = s_linear_accel.y;
    if (az) *az = s_linear_accel.z;
}

mouse_output_t motion_process(const imu_data_t* imu, bool clutch_pressed, uint32_t now_ms) {
    mouse_output_t out;
    out.delta_x = 0;
    out.delta_y = 0;
    out.is_stationary = false;
    out.is_clutch_active = clutch_pressed;
    out.gesture = GESTURE_EVENT_NONE;
    out.filtered_gx = 0.0f;
    out.filtered_gy = 0.0f;
    out.filtered_gz = 0.0f;
    out.recentered = false;
    out.hold_peak_yaw_dps = 0.0f;
    out.hold_peak_alat_g = 0.0f;

    if (!imu) return out;

    // 1. Low-pass filter accelerometer data for quasi-static tracking (alpha = 0.1)
    s_accel_filt.x += 0.1f * (imu->ax - s_accel_filt.x);
    s_accel_filt.y += 0.1f * (imu->ay - s_accel_filt.y);
    s_accel_filt.z += 0.1f * (imu->az - s_accel_filt.z);

    // 2. Subtract Zero-rate Gyro Bias
    float gx_c = imu->gx - s_bias_x;
    float gy_c = imu->gy - s_bias_y;
    float gz_c = imu->gz - s_bias_z;

    // 3. Check Stationary Condition
    float gyro_norm = sqrtf(gx_c * gx_c + gy_c * gy_c + gz_c * gz_c);
    float accel_norm = sqrtf(imu->ax * imu->ax + imu->ay * imu->ay + imu->az * imu->az);
    float accel_err = fabsf(accel_norm - 1.0f);

    if (gyro_norm < s_cfg.stat_gyro_thresh && accel_err < s_cfg.stat_accel_thresh) {
        if (s_rest_counter < 65535) s_rest_counter++;
        if (s_stat_counter < s_cfg.stat_window_count) {
            s_stat_counter++;
        } else {
            s_is_stationary = true;
            if (s_rest_counter >= AUTO_ZERO_MIN_REST_SAMPLES) {
                s_bias_x += s_cfg.auto_zero_alpha * gx_c;
                s_bias_y += s_cfg.auto_zero_alpha * gy_c;
                s_bias_z += s_cfg.auto_zero_alpha * gz_c;
            }
        }
    } else {
        s_stat_counter = 0;
        s_rest_counter = 0;
        s_is_stationary = false;
    }
    out.is_stationary = s_is_stationary;

    // 4. 6-Axis Attitude Estimation: Gyroscope Propagation + Accelerometer Tilt Correction
    // Calculate expected gravity vector in body frame from current attitude quaternion:
    // v_g = R(q)^T * [0, 0, 1]^T
    float vg_x = 2.0f * (s_q.q1 * s_q.q3 - s_q.q0 * s_q.q2);
    float vg_y = 2.0f * (s_q.q0 * s_q.q1 + s_q.q2 * s_q.q3);
    float vg_z = s_q.q0 * s_q.q0 - s_q.q1 * s_q.q1 - s_q.q2 * s_q.q2 + s_q.q3 * s_q.q3;
    s_body_gravity.x = vg_x;
    s_body_gravity.y = vg_y;
    s_body_gravity.z = vg_z;

    // Tilt error: cross product between normalized accelerometer measurement and estimated gravity
    float e_tilt_x = 0.0f;
    float e_tilt_y = 0.0f;
    float e_tilt_z = 0.0f;
    if (accel_norm > 0.75f && accel_norm < 1.25f) {
        float inv_anorm = 1.0f / accel_norm;
        float ax_n = imu->ax * inv_anorm;
        float ay_n = imu->ay * inv_anorm;
        float az_n = imu->az * inv_anorm;
        // e = a_meas x v_g
        // NOTE: e_tilt has ZERO component along v_g; therefore tilt correction CANNOT observe or correct Yaw!
        // Yaw remains strictly relative and subject to slow unreferenced gyro drift.
        e_tilt_x = ay_n * vg_z - az_n * vg_y;
        e_tilt_y = az_n * vg_x - ax_n * vg_z;
        e_tilt_z = ax_n * vg_y - ay_n * vg_x;
    }

    // Dynamic dt calculation from now_ms with safe min/max clamping [0.001s, 0.050s]
    float dt = 0.01f; // Nominal 100 Hz fallback (10 ms)
    if (s_has_last_ms && now_ms > s_last_process_ms) {
        dt = (float)(now_ms - s_last_process_ms) * 0.001f;
        if (dt < 0.001f) dt = 0.001f; // Minimum clamp 1 ms
        if (dt > 0.050f) dt = 0.050f; // Maximum clamp 50 ms
    }
    s_last_process_ms = now_ms;
    s_has_last_ms = true;

    // Continuous-time tilt correction rate gain: tilt_correction_rate_s_inv = 2.0 s^-1.
    // Yields small-error tilt convergence time constant tau = 1/K = 0.5s.
    // Integrated over dt: dtheta_corr = tilt_correction_rate_s_inv * e_tilt * dt.
    // PROJECT INITIAL VALUE / NEEDS_HARDWARE_TUNING
    const float tilt_correction_rate_s_inv = 2.0f; // s^-1
    float wx = (gx_c * RAD_PER_DEG) + (tilt_correction_rate_s_inv * e_tilt_x);
    float wy = (gy_c * RAD_PER_DEG) + (tilt_correction_rate_s_inv * e_tilt_y);
    float wz = (gz_c * RAD_PER_DEG) + (tilt_correction_rate_s_inv * e_tilt_z);

    // Quaternion numerical integration (dynamic dt, nominal target 100 Hz [0.001s, 0.050s])
    float dq0 = 0.5f * (-s_q.q1 * wx - s_q.q2 * wy - s_q.q3 * wz) * dt;
    float dq1 = 0.5f * ( s_q.q0 * wx + s_q.q2 * wz - s_q.q3 * wy) * dt;
    float dq2 = 0.5f * ( s_q.q0 * wy - s_q.q1 * wz + s_q.q3 * wx) * dt;
    float dq3 = 0.5f * ( s_q.q0 * wz + s_q.q1 * wy - s_q.q2 * wx) * dt;

    s_q.q0 += dq0;
    s_q.q1 += dq1;
    s_q.q2 += dq2;
    s_q.q3 += dq3;

    // Quaternion normalization
    float q_norm = sqrtf(s_q.q0 * s_q.q0 + s_q.q1 * s_q.q1 + s_q.q2 * s_q.q2 + s_q.q3 * s_q.q3);
    if (q_norm > 1e-6f) {
        float inv_qnorm = 1.0f / q_norm;
        s_q.q0 *= inv_qnorm;
        s_q.q1 *= inv_qnorm;
        s_q.q2 *= inv_qnorm;
        s_q.q3 *= inv_qnorm;
    }

    // Update body gravity with newly normalized attitude
    s_body_gravity.x = 2.0f * (s_q.q1 * s_q.q3 - s_q.q0 * s_q.q2);
    s_body_gravity.y = 2.0f * (s_q.q0 * s_q.q1 + s_q.q2 * s_q.q3);
    s_body_gravity.z = s_q.q0 * s_q.q0 - s_q.q1 * s_q.q1 - s_q.q2 * s_q.q2 + s_q.q3 * s_q.q3;

    // 5. Compute Gravity-Free Linear Acceleration
    // Subtract estimated 1.0g gravity vector in body coordinates
    s_linear_accel.x = imu->ax - s_body_gravity.x;
    s_linear_accel.y = imu->ay - s_body_gravity.y;
    s_linear_accel.z = imu->az - s_body_gravity.z;

    // 6. Handle Clutch State Transitions (Recenter upon button release)
    if (clutch_pressed && !s_last_clutch_state) {
        // Clutch just pressed: arm gestures, pause cursor
        s_gesture_occurred_in_clutch = false;
        s_recenter_pending = false;
        yf_on_press(&s_yf);
        s_hold_peak_yaw = 0.0f;
        s_hold_peak_alat = 0.0f;
    } else if (!clutch_pressed && s_last_clutch_state) {
        out.hold_peak_yaw_dps = s_hold_peak_yaw;
        out.hold_peak_alat_g = s_hold_peak_alat;
        // Clutch just released: re-establish reference vertical if no gesture occurred
        if (!s_gesture_occurred_in_clutch) {
            if (s_recenter_settle_ms == 0) {
                motion_recenter(imu);
                out.recentered = true;
            } else {
                // Wait for the hand to settle (the press/release itself jerks the board), cursor stays frozen
                s_recenter_pending = true;
                s_recenter_due_ms = now_ms + s_recenter_settle_ms;
            }
        }
    }
    s_last_clutch_state = clutch_pressed;
    if (s_recenter_pending && (int32_t)(now_ms - s_recenter_due_ms) >= 0) {
        motion_recenter(imu);
        s_recenter_pending = false;
        out.recentered = true;
    }

    // 7. Lateral Gesture Detection with Gravity Removal & Posture Envelope Gating (P1-B)
    // Lateral user control axis is perpendicular to Forward [1, 0, 0] and Body Gravity:
    // lat_vec = [1, 0, 0] x v_g = [0, -v_gz, v_gy]
    // For flat resting pose (v_gz=1, v_gy=0): lat_vec points left (-Y), so +Y_lateral = [0, v_gz, -v_gy]
    float lat_len = sqrtf(s_body_gravity.y * s_body_gravity.y + s_body_gravity.z * s_body_gravity.z);
    float a_lateral = 0.0f;

    // Posture validation: Gestures are only valid within standard handheld posture
    // (|vg_x| < 0.707f => pitch within +/-45 deg; |vg_y| < 0.50f => roll within +/-30 deg)
    bool is_pose_valid_for_gestures = (fabsf(s_body_gravity.x) < 0.707f) &&
                                     (fabsf(s_body_gravity.y) < 0.50f) &&
                                     (lat_len > 0.35f);

    if (is_pose_valid_for_gestures) {
        // Project gravity-free linear acceleration onto lateral horizontal axis
        float lat_y = s_body_gravity.z / lat_len;
        float lat_z = -s_body_gravity.y / lat_len;
        a_lateral = s_linear_accel.y * lat_y + s_linear_accel.z * lat_z;
    } else {
        // Outside calibrated holding posture envelope: disarm gestures to prevent false triggers
        a_lateral = 0.0f;
    }

    if (clutch_pressed) {
        // Turning rate about "up" (+ = left) and lateral acceleration (+ = right), peaks kept for tuning
        float yaw_dps = gx_c * s_body_gravity.x + gy_c * s_body_gravity.y + gz_c * s_body_gravity.z;
        if (fabsf(yaw_dps) > fabsf(s_hold_peak_yaw)) s_hold_peak_yaw = yaw_dps;
        if (fabsf(a_lateral) > fabsf(s_hold_peak_alat)) s_hold_peak_alat = a_lateral;

        if (s_gestures_enabled) {
            gesture_event_t gest = gesture_update(a_lateral, gyro_norm, true, now_ms);
            // The yaw flick is ignored for 600 ms after any gesture (the return swing must not fire the opposite one)
            if (gest == GESTURE_EVENT_NONE) {
                gest = yf_update(&s_yf, yaw_dps, now_ms);
            }
            if (gest != GESTURE_EVENT_NONE) {
                out.gesture = gest;
                s_gesture_occurred_in_clutch = true;
                yf_note_gesture(&s_yf, now_ms);
            }
        }
        // When clutch is active, mouse cursor is frozen
        s_rem_x = 0.0f;
        s_rem_y = 0.0f;
        return out;
    }

    // Waiting for the hand to settle before re-centering: keep the cursor frozen
    if (s_recenter_pending) {
        s_rem_x = 0.0f;
        s_rem_y = 0.0f;
        return out;
    }

    // If stationary, freeze cursor output completely to eliminate any creeping
    if (s_is_stationary) {
        s_rem_x = 0.0f;
        s_rem_y = 0.0f;
        return out;
    }

    // 8. Apply Tightening (replaces dead-zone) to raw gyro rates
    float clean_gx = apply_tightening(gx_c, s_cfg.gyro_deadzone_high);
    float clean_gy = apply_tightening(gy_c, s_cfg.gyro_deadzone_high);
    float clean_gz = apply_tightening(gz_c, s_cfg.gyro_deadzone_high);

    out.filtered_gx = clean_gx;
    out.filtered_gy = clean_gy;
    out.filtered_gz = clean_gz;

    // 9. Adaptive Reference Frame Projection (Relative Rate-Control)
    // Horizontal control rate (Yaw): component of angular velocity along reference vertical
    float omega_horizontal = clean_gx * s_ref_gravity.x +
                             clean_gy * s_ref_gravity.y +
                             clean_gz * s_ref_gravity.z;

    // Vertical control rate (Pitch): component along lateral horizontal axis
    float ref_lat_len = sqrtf(s_ref_gravity.y * s_ref_gravity.y + s_ref_gravity.z * s_ref_gravity.z);
    float omega_vertical = 0.0f;
    if (ref_lat_len > 0.20f) {
        float ref_lat_y = s_ref_gravity.z / ref_lat_len;
        float ref_lat_z = -s_ref_gravity.y / ref_lat_len;
        omega_vertical = clean_gy * ref_lat_y + clean_gz * ref_lat_z;
    } else {
        // Pointing straight up/down: Pitch rate directly maps to transverse Y
        omega_vertical = clean_gy;
    }

    // 10. Gain Scaling & Clamping to 8-bit Signed Relative HID Report (NOT an absolute pointer)
    // Screen X: Yaw right -> Delta X > 0
    // Screen Y: Pitch up -> Delta Y < 0 (Screen origin (0,0) is top-left)
    // omega_horizontal is rotation about "up" (right-hand rule: counter-clockwise seen from above = positive),
    // so turning RIGHT gives a NEGATIVE value; negate it so turning right moves the cursor right.
    float fx = -s_cfg.gain_x * omega_horizontal + s_rem_x;
    float fy = -s_cfg.gain_y * omega_vertical   + s_rem_y;
    int32_t dx = (int32_t)roundf(fx);
    int32_t dy = (int32_t)roundf(fy);
    s_rem_x = fx - (float)dx;
    s_rem_y = fy - (float)dy;
    if (dx > 127 || dx < -127) s_rem_x = 0.0f;   // bão hòa: bỏ phần dư để không dồn tích
    if (dy > 127 || dy < -127) s_rem_y = 0.0f;
    out.delta_x = clamp_i8(dx);
    out.delta_y = clamp_i8(dy);

    return out;
}
