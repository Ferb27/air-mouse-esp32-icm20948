#include <Arduino.h>
#include "app_serial_cmd.h"
#include "app_config.h"
#include "app_config_store.h"
#include "app_imu.h"
#include "app_motion.h"
#include "app_buttons.h"
#include "app_timing.h"
#include "click_guard.h"
#include "motion_pipeline.h"

// '@' starts a protocol line (see air_config.h): everything up to the line end is collected, then handled as a whole.
// A line that never ends (cable pulled in the middle) is dropped after 2 s so the one-letter commands work again.
#define LINE_TIMEOUT_MS 2000UL
static char     s_line[AIR_CFG_LINE_MAX + 1];
static int      s_len = -1;            // -1 = not inside a line
static bool     s_too_long = false;
static uint32_t s_last_char_ms = 0;

void app_serial_poll(void) {
    while (Serial.available() > 0) {
        int c = Serial.read();
        if (s_len >= 0) {
            s_last_char_ms = millis();
            if (c == '\n' || c == '\r') {
                s_line[s_len] = '\0';
                if (s_too_long) Serial.println("@ERR too-long");
                else            app_config_handle_line(s_line);
                s_len = -1;
                s_too_long = false;
                continue;
            }
            if (s_len < AIR_CFG_LINE_MAX) s_line[s_len++] = (char)c;
            else                          s_too_long = true;
            continue;
        }
        if (c == '@') {
            s_len = 0;
            s_too_long = false;
            s_last_char_ms = millis();
            continue;
        }
        if (c == 'c') {                       // recalibrate gyro bias now (board must rest still)
            app_imu_calibrate(APP_CAL_RUNTIME_ATTEMPTS, false);
            app_resync();
            continue;
        }
        if (c == 'y' || c == 'Y') {           // flick threshold: 'y' = more sensitive (-20 deg/s), 'Y' = less (+20)
            float v = app_flick_adjust((c == 'Y') ? APP_FLICK_DPS_STEP : -APP_FLICK_DPS_STEP);
            Serial.printf("[FLICK] quick-turn threshold = %.0f deg/s (lower = easier to trigger)\n", v);
            continue;
        }
        if (c == '<' || c == '>') {           // click-guard look-ahead: '>' +10 ms, '<' -10 ms (0..100 ms)
            int n = app_buttons_adjust_lookahead(c == '>' ? 1 : -1);
            Serial.printf("[CLICK] look-ahead = %d ms, freeze while held < %d ms\n", n * 10, CG_DRAG_MS);
            continue;
        }
        if (c != '+' && c != '-' && c != '?') continue;
        float gx, gy;
        motion_getGain(&gx, &gy);
        if (c == '+') { gx *= APP_GAIN_STEP; gy *= APP_GAIN_STEP; }
        if (c == '-') { gx /= APP_GAIN_STEP; gy /= APP_GAIN_STEP; }
        if (gx < APP_GAIN_MIN) { gx = APP_GAIN_MIN; gy = APP_GAIN_MIN; }
        if (gx > APP_GAIN_MAX) { gx = APP_GAIN_MAX; gy = APP_GAIN_MAX; }
        motion_setGain(gx, gy);
        Serial.printf("[GAIN] x=%.3f y=%.3f (~%.0f counts per degree)\n", gx, gy, gx * 100.0f);
    }
    if (s_len >= 0 && millis() - s_last_char_ms > LINE_TIMEOUT_MS) {
        s_len = -1;
        s_too_long = false;
        Serial.println("@ERR timeout");
    }
}
