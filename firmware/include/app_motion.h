#ifndef APP_MOTION_H
#define APP_MOTION_H

#include <stdbool.h>
#include "motion_pipeline.h"

// Configuration and logging around the portable motion pipeline (motion_pipeline.h).

// motion_init() plus the project settings: gestures on, quick-turn flick threshold, 150 ms recenter settle time.
//  Mode button = Clutch + Recenter: hold = freeze the cursor, release = re-center after the settle time.
//  Hold Mode + quick turn LEFT = Back, quick turn RIGHT = Forward (turning-rate flick, threshold tunable with 'y' / 'Y').
void app_motion_init(void);

// Quick-turn flick threshold (deg/s): get, or change by delta (clamped to APP_FLICK_DPS_MIN..MAX); both return the value.
float app_flick_threshold(void);
float app_flick_adjust(float delta_dps);
// Set the threshold directly (clamped); returns the value in use.
float app_flick_set(float dps);

// Serial log of the Mode button and flick events for this tick:
// [MODE] down/up, [MODE] hold peaks (on release; for threshold tuning), [FLICK] LEFT/RIGHT detected, [MODE] Recentered.
void app_motion_log(const mouse_output_t& out, bool mode_held);

#endif // APP_MOTION_H
