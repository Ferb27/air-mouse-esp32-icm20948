#include <Arduino.h>
#include "app_timing.h"
#include "app_config.h"
#include "app_status.h"

static uint32_t s_last_loop_us = 0;

bool app_loop_due(uint32_t* now_ms) {
    uint32_t now_us = micros();
    // Maintain strict 10 ms (100 Hz) loop interval
    if (now_us - s_last_loop_us < APP_LOOP_PERIOD_US) {
        return false;
    }
    s_last_loop_us = now_us;
    *now_ms = millis();
    return true;
}

void app_resync(void) {
    s_last_loop_us = micros();
    app_status_resync();
}

void app_timing_start(void) {
    app_resync();
}
