#ifndef APP_SCROLL_H
#define APP_SCROLL_H

#include <stdint.h>
#include <stdbool.h>

// Scroll mode on the Mode button (scroll_mode.h): tap Mode, press it again quickly and HOLD: the cursor stays still and
// the tilt of the board up / down (relative to the pose when you pressed) sets the scroll speed: hold the tilt = keep scrolling. Settings (scroll_enable, scroll_sens, scroll_invert, hscroll) come
// from the user settings (app_config_store.h).

// Call once per tick BEFORE motion_process() with the debounced Mode button. Returns true while scroll mode is on.
// The pipeline must then be fed `mode_down && !scroll_on` (scroll mode is not a clutch hold). When scroll mode ends it
// schedules the re-center, so this tick's cursor motion is already frozen.
bool app_scroll_update(bool mode_down, uint32_t now_ms);

// Call after motion_process(): while scroll mode is on, computes the wheel notches from the board tilt and zeroes the
// cursor motion. Outside scroll mode it does nothing (wheel = hwheel = 0).
void app_scroll_convert(bool scroll_on, uint32_t now_ms, int8_t* dx, int8_t* dy, int8_t* wheel, int8_t* hwheel);

#endif // APP_SCROLL_H
