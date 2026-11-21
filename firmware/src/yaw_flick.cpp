#include "../include/yaw_flick.h"
#include <math.h>

void yf_init(yaw_flick_t* y, float thresh_dps) {
    y->thresh_dps = thresh_dps > 0.0f ? thresh_dps : 0.0f;
    y->locked = false;
    y->block_until_ms = 0;
}

void yf_set_threshold(yaw_flick_t* y, float thresh_dps) {
    y->thresh_dps = thresh_dps > 0.0f ? thresh_dps : 0.0f;
}

void yf_reset(yaw_flick_t* y) {
    y->locked = false;
    y->block_until_ms = 0;
}

void yf_on_press(yaw_flick_t* y) {
    y->locked = false;
}

gesture_event_t yf_update(yaw_flick_t* y, float yaw_dps, uint32_t now_ms) {
    if (!(y->thresh_dps > 0.0f)) return GESTURE_EVENT_NONE;
    if ((int32_t)(now_ms - y->block_until_ms) < 0) return GESTURE_EVENT_NONE;   // return swing of a recent gesture

    float a = fabsf(yaw_dps);
    if (y->locked) {
        if (a < 0.35f * y->thresh_dps) y->locked = false;
        return GESTURE_EVENT_NONE;
    }
    if (a >= y->thresh_dps) {
        y->locked = true;
        return yaw_dps > 0.0f ? GESTURE_EVENT_FLICK_LEFT : GESTURE_EVENT_FLICK_RIGHT;
    }
    return GESTURE_EVENT_NONE;
}

void yf_note_gesture(yaw_flick_t* y, uint32_t now_ms) {
    y->block_until_ms = now_ms + YF_BLOCK_MS;
    y->locked = true;
}
