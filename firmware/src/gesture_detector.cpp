#include "gesture_detector.h"

static gesture_config_t s_cfg;
static gesture_sm_state_t s_state = SM_GESTURE_IDLE;
static uint32_t s_state_start_ms = 0;
static uint32_t s_cooldown_start_ms = 0;

void gesture_init(const gesture_config_t* cfg) {
    if (cfg) {
        s_cfg = *cfg;
    } else {
        // Safe default parameters (Tuned for biphasic hand flick impulse)
        // PROJECT INITIAL VALUE / NEEDS_HARDWARE_TUNING
        s_cfg.peak_accel_thresh   = 1.15f;   // 1.15g peak impulse
        s_cfg.return_accel_thresh = 0.35f;   // 0.35g opposing deceleration
        s_cfg.max_gyro_rejection  = 600.0f;  // Reject violent spins
        s_cfg.min_duration_ms     = 60;
        s_cfg.max_duration_ms     = 450;
        s_cfg.cooldown_ms         = 350;
    }
    s_state = SM_GESTURE_IDLE;
    s_state_start_ms = 0;
    s_cooldown_start_ms = 0;
}

gesture_event_t gesture_update(float a_lateral_g, float gyro_norm, bool clutch_btn_pressed, uint32_t now_ms) {
    // If clutch button is not pressed, gesture recognition is disarmed
    if (!clutch_btn_pressed) {
        s_state = SM_GESTURE_IDLE;
        return GESTURE_EVENT_NONE;
    }

    // Check cooldown
    if (s_state == SM_GESTURE_COOLDOWN) {
        if (now_ms - s_cooldown_start_ms >= s_cfg.cooldown_ms) {
            s_state = SM_GESTURE_ARMED;
        } else {
            return GESTURE_EVENT_NONE;
        }
    }

    // Reject if rotational speed is excessively high (pure spinning wrist, not translational flick)
    if (gyro_norm > s_cfg.max_gyro_rejection) {
        s_state = SM_GESTURE_ARMED;
        return GESTURE_EVENT_NONE;
    }

    uint32_t elapsed = now_ms - s_state_start_ms;

    switch (s_state) {
        case SM_GESTURE_IDLE:
            if (clutch_btn_pressed) {
                s_state = SM_GESTURE_ARMED;
                s_state_start_ms = now_ms;
            }
            break;

        case SM_GESTURE_ARMED:
            // Check for initial acceleration peak
            if (a_lateral_g < -s_cfg.peak_accel_thresh) {
                // Flick Left detected (negative lateral acceleration)
                s_state = SM_GESTURE_PEAK_LEFT;
                s_state_start_ms = now_ms;
            } else if (a_lateral_g > s_cfg.peak_accel_thresh) {
                // Flick Right detected (positive lateral acceleration)
                s_state = SM_GESTURE_PEAK_RIGHT;
                s_state_start_ms = now_ms;
            }
            break;

        case SM_GESTURE_PEAK_LEFT:
            if (elapsed > s_cfg.max_duration_ms) {
                // Timeout without return phase
                s_state = SM_GESTURE_ARMED;
            } else if (a_lateral_g > s_cfg.return_accel_thresh && elapsed >= s_cfg.min_duration_ms) {
                // Return/deceleration phase detected -> Valid Left Flick (Back)
                s_state = SM_GESTURE_COOLDOWN;
                s_cooldown_start_ms = now_ms;
                return GESTURE_EVENT_FLICK_LEFT;
            }
            break;

        case SM_GESTURE_PEAK_RIGHT:
            if (elapsed > s_cfg.max_duration_ms) {
                // Timeout without return phase
                s_state = SM_GESTURE_ARMED;
            } else if (a_lateral_g < -s_cfg.return_accel_thresh && elapsed >= s_cfg.min_duration_ms) {
                // Return/deceleration phase detected -> Valid Right Flick (Forward)
                s_state = SM_GESTURE_COOLDOWN;
                s_cooldown_start_ms = now_ms;
                return GESTURE_EVENT_FLICK_RIGHT;
            }
            break;

        default:
            s_state = SM_GESTURE_IDLE;
            break;
    }

    return GESTURE_EVENT_NONE;
}

gesture_sm_state_t gesture_getState(void) {
    return s_state;
}
