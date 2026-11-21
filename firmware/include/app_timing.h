#ifndef APP_TIMING_H
#define APP_TIMING_H

#include <stdint.h>
#include <stdbool.h>

// 100 Hz main-loop pacing.
void app_timing_start(void);               // call once at the end of setup()
bool app_loop_due(uint32_t* now_ms);       // true once every APP_LOOP_PERIOD_US; returns the current millis()
void app_resync(void);                     // call after a BLOCKING operation (calibration, re-init) so timers restart

#endif // APP_TIMING_H
