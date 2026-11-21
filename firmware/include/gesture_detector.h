#ifndef GESTURE_DETECTOR_H
#define GESTURE_DETECTOR_H

#include <stdint.h>
#include <stdbool.h>

#ifdef __cplusplus
extern "C" {
#endif

typedef enum {
    GESTURE_EVENT_NONE = 0,
    GESTURE_EVENT_FLICK_LEFT,   // Quick flick Left + Return -> Browser Back
    GESTURE_EVENT_FLICK_RIGHT   // Quick flick Right + Return -> Browser Forward
} gesture_event_t;

typedef enum {
    SM_GESTURE_IDLE = 0,
    SM_GESTURE_ARMED,
    SM_GESTURE_PEAK_LEFT,
    SM_GESTURE_PEAK_RIGHT,
    SM_GESTURE_RETURN_LEFT,
    SM_GESTURE_RETURN_RIGHT,
    SM_GESTURE_COOLDOWN
} gesture_sm_state_t;

// Biphasic impulse thresholds (peak impulse + opposing return phase, NOT sustained)
// Marked: PROJECT INITIAL VALUE / NEEDS_HARDWARE_TUNING
typedef struct {
    float peak_accel_thresh;    // 1.15g initial flick peak
    float return_accel_thresh;  // 0.35g opposing return deceleration
    float max_gyro_rejection;   // 600 dps rotational rejection
    uint32_t min_duration_ms;   // 60 ms minimum impulse window
    uint32_t max_duration_ms;   // 450 ms maximum impulse window
    uint32_t cooldown_ms;       // 350 ms inter-gesture cooldown
} gesture_config_t;

void gesture_init(const gesture_config_t* cfg);

// Update gesture state machine with gravity-free lateral linear acceleration (in g)
// Only valid within standard holding envelope (pitch within +/-45 deg, roll within +/-30 deg).
gesture_event_t gesture_update(float a_lateral_g, float gyro_norm, bool clutch_btn_pressed, uint32_t now_ms);
gesture_sm_state_t gesture_getState(void);

#ifdef __cplusplus
}
#endif

#endif // GESTURE_DETECTOR_H
