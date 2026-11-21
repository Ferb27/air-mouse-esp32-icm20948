#ifndef APP_CONFIG_H
#define APP_CONFIG_H

// =============================================================================
// Air Mouse - tunable constants of the APPLICATION layer (app_*.cpp). One place to look when tuning.
// (Algorithm constants of the portable core live in motion_pipeline.cpp / gesture_detector.cpp / bias_checks.cpp.)
// The values the user can change from the PC (gain, flick threshold, click guard, recenter time) have their defaults and
// limits in air_config.h (portable core); the names below only point there, so there is one place for each number.
// =============================================================================

#include "air_config.h"

// --- Timing ---
#define APP_SERIAL_BAUD              115200
#define APP_LOOP_PERIOD_US           10000UL   // 100 Hz main loop
#define APP_STATUS_PERIOD_MS         1000UL    // [STATUS] telemetry

// --- Buttons (active-low, internal pull-ups) ---
#define APP_BTN_PRESS_MS             5         // a press is accepted after this long (low latency)
#define APP_BTN_RELEASE_MS           20        // a release after this long (contact bounce)
#define APP_CLICK_LOOKAHEAD_DEFAULT  (AIR_CFG_CLICK_MS_DEFAULT / 10)   // click guard: delay in 10 ms samples (4 = 40 ms), '<' '>' over serial

// --- Mode button: clutch + recenter + flick ---
#define APP_RECENTER_SETTLE_MS       AIR_CFG_RECENTER_DEFAULT   // wait after releasing Mode before re-centering (thumb jerk)
#define APP_FLICK_DPS_DEFAULT        AIR_CFG_FLICK_DEFAULT      // quick-turn flick threshold, 'y' / 'Y' over serial
#define APP_FLICK_DPS_MIN            AIR_CFG_FLICK_MIN
#define APP_FLICK_DPS_MAX            AIR_CFG_FLICK_MAX
#define APP_FLICK_DPS_STEP           20.0f

// --- Gyro calibration ---
#define APP_CAL_SAMPLES              200       // 200 samples @ 10 ms = 2 s per attempt
#define APP_CAL_STARTUP_ATTEMPTS     5         // at boot (the last attempt is applied even if never still)
#define APP_CAL_RUNTIME_ATTEMPTS     5         // 'c' over serial (a rejected result keeps the old bias)

// --- Sensitivity ('+' / '-' over serial) ---
#define APP_GAIN_MIN                 AIR_CFG_GAIN_MIN
#define APP_GAIN_MAX                 AIR_CFG_GAIN_MAX
#define APP_GAIN_STEP                1.2f

#endif // APP_CONFIG_H
