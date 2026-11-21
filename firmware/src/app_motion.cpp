#include <Arduino.h>
#include "app_motion.h"
#include "app_config.h"

static float s_flick_dps = APP_FLICK_DPS_DEFAULT;

void app_motion_init(void) {
    // Initialize Motion Pipeline & Algorithms
    motion_init(NULL);
    motion_setGesturesEnabled(true);
    motion_setYawFlickThresholdDps(s_flick_dps);
    motion_setRecenterSettleMs(APP_RECENTER_SETTLE_MS);
}

float app_flick_threshold(void) {
    return s_flick_dps;
}

float app_flick_set(float dps) {
    s_flick_dps = dps;
    if (s_flick_dps < APP_FLICK_DPS_MIN) s_flick_dps = APP_FLICK_DPS_MIN;
    if (s_flick_dps > APP_FLICK_DPS_MAX) s_flick_dps = APP_FLICK_DPS_MAX;
    motion_setYawFlickThresholdDps(s_flick_dps);
    return s_flick_dps;
}

float app_flick_adjust(float delta_dps) {
    return app_flick_set(s_flick_dps + delta_dps);
}

void app_motion_log(const mouse_output_t& out, bool mode_held) {
    if (out.hold_peak_yaw_dps != 0.0f || out.hold_peak_alat_g != 0.0f) {   // only set on the tick Mode is released
        Serial.printf("[MODE] hold peaks: turn = %+.0f deg/s (+ left, threshold %.0f), lateral accel = %+.2f g (+ right)\n",
                      out.hold_peak_yaw_dps, s_flick_dps, out.hold_peak_alat_g);
    }
    if (out.gesture != GESTURE_EVENT_NONE) {
        Serial.printf("[FLICK] %s detected\n", out.gesture == GESTURE_EVENT_FLICK_LEFT ? "LEFT (Back)" : "RIGHT (Forward)");
    }
    if (out.recentered) {
        Serial.println("[MODE] Recentered: current pose is the new reference");
    }
    static bool s_log_mode = false;
    if (mode_held != s_log_mode) {
        Serial.println(mode_held ? "[MODE] down (cursor frozen)" : "[MODE] up");
        s_log_mode = mode_held;
    }
}
