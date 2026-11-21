#ifndef APP_BUTTONS_H
#define APP_BUTTONS_H

#include <stdint.h>
#include <stdbool.h>

// The three tactile buttons (see pin_definitions.h) with debounce, plus the click guard for the cursor.
// These are the PHYSICAL buttons; what each one does is the user setting btn_left / btn_right / btn_mode (button_map.h).
typedef struct {
    bool left;      // SW2, GPIO25 (default action: left click)
    bool right;     // SW3, GPIO26 (default: right click)
    bool mode;      // SW4, GPIO27 (default: Mode = clutch (freeze) + recenter + flick gestures + double-tap scroll)
} buttons_t;

void app_buttons_init(void);
// Read + debounce (press 5 ms, release 20 ms). Call once per tick.
buttons_t app_buttons_read(uint32_t now_ms);

// Click guard (click_guard.h): delays the cursor by a few samples and drops the jerk that precedes a press; the cursor
// stays frozen while a button is held < 250 ms.
// any_click: a mouse button (left / right / middle / back / forward, after the mapping) is held.
void app_buttons_filter_motion(bool any_click, int8_t dx, int8_t dy, uint32_t now_ms, int8_t* out_dx, int8_t* out_dy);
// Serial log of the physical button edges with their mapped action: "[BTN] LEFT down -> MIDDLE" (+ " (BLE not connected)").
void app_buttons_log(const buttons_t& raw, uint8_t act_left, uint8_t act_right, uint8_t act_mode, bool ble_connected);
// Change the click-guard look-ahead by delta samples (10 ms each, clamped); returns the new look-ahead in samples.
int app_buttons_adjust_lookahead(int delta_samples);
// Click-guard look-ahead in milliseconds (a multiple of 10, clamped to 0..100): get / set.
int  app_buttons_get_lookahead_ms(void);
void app_buttons_set_lookahead_ms(int ms);

#endif // APP_BUTTONS_H
