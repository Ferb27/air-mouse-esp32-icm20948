#ifndef APP_STATUS_H
#define APP_STATUS_H

#include <stdint.h>
#include "motion_pipeline.h"

// Periodic [STATUS] telemetry (every APP_STATUS_PERIOD_MS):
//   Rate (loops in the last second) | Stat (stationary lock) | Clutch | dX dY (last sample) | BiasZ |
//   Up (seconds since boot) | Frz (sensor re-inits) | Heal (self-heal recalibrations) | Err (failed I2C reads) | Rec (I2C bus recoveries) | Rst (esp_reset_reason)
void app_status_count_loop(void);                                 // once per 100 Hz tick
void app_status_report(uint32_t now_ms, const mouse_output_t& out);
void app_status_resync(void);                                     // restart the 1 s timer after a blocking operation

#endif // APP_STATUS_H
