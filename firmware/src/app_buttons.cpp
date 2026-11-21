#include <Arduino.h>
#include "app_buttons.h"
#include "app_config.h"
#include "pin_definitions.h"
#include "button_debounce.h"
#include "click_guard.h"
#include "button_map.h"

static debounce_t s_deb_l, s_deb_r, s_deb_mode;
static click_guard_t s_cg;

void app_buttons_init(void) {
    pinMode(PIN_BTN_LEFT, INPUT_PULLUP);
    pinMode(PIN_BTN_RIGHT, INPUT_PULLUP);
    pinMode(PIN_BTN_MODE, INPUT_PULLUP);
    debounce_init(&s_deb_l, false);
    debounce_init(&s_deb_r, false);
    debounce_init(&s_deb_mode, false);
    cg_init(&s_cg, APP_CLICK_LOOKAHEAD_DEFAULT);
}

buttons_t app_buttons_read(uint32_t now_ms) {
    // Press is accepted after 5 ms (low latency), release after 20 ms (contact bounce).
    buttons_t b;
    b.left  = debounce_update2(&s_deb_l,    digitalRead(PIN_BTN_LEFT)  == LOW, now_ms, APP_BTN_PRESS_MS, APP_BTN_RELEASE_MS);
    b.right = debounce_update2(&s_deb_r,    digitalRead(PIN_BTN_RIGHT) == LOW, now_ms, APP_BTN_PRESS_MS, APP_BTN_RELEASE_MS);
    b.mode  = debounce_update2(&s_deb_mode, digitalRead(PIN_BTN_MODE)  == LOW, now_ms, APP_BTN_PRESS_MS, APP_BTN_RELEASE_MS);
    return b;
}

void app_buttons_filter_motion(bool any_click, int8_t dx, int8_t dy, uint32_t now_ms, int8_t* out_dx, int8_t* out_dy) {
    cg_update(&s_cg, any_click, dx, dy, now_ms, out_dx, out_dy);
}

void app_buttons_log(const buttons_t& raw, uint8_t act_left, uint8_t act_right, uint8_t act_mode, bool ble_connected) {
    static bool s_last_l = false, s_last_r = false, s_last_m = false;
    const char* tail = ble_connected ? "" : " (BLE not connected)";
    if (raw.left != s_last_l)   Serial.printf("[BTN] LEFT %s -> %s%s\n",  raw.left  ? "down" : "up", bm_action_name(act_left),  tail);
    if (raw.right != s_last_r)  Serial.printf("[BTN] RIGHT %s -> %s%s\n", raw.right ? "down" : "up", bm_action_name(act_right), tail);
    if (raw.mode != s_last_m)   Serial.printf("[BTN] MODE %s -> %s%s\n",  raw.mode  ? "down" : "up", bm_action_name(act_mode),  tail);
    s_last_l = raw.left; s_last_r = raw.right; s_last_m = raw.mode;
}

int app_buttons_adjust_lookahead(int delta_samples) {
    int n = (int)s_cg.lookahead + delta_samples;
    if (n < 0) n = 0;
    if (n > CG_MAX_LOOKAHEAD) n = CG_MAX_LOOKAHEAD;
    cg_set_lookahead(&s_cg, (uint8_t)n);
    return n;
}

int app_buttons_get_lookahead_ms(void) {
    return (int)s_cg.lookahead * 10;
}

void app_buttons_set_lookahead_ms(int ms) {
    int n = (ms + 5) / 10;
    if (n < 0) n = 0;
    if (n > CG_MAX_LOOKAHEAD) n = CG_MAX_LOOKAHEAD;
    cg_set_lookahead(&s_cg, (uint8_t)n);
}
