#ifndef APP_BLE_H
#define APP_BLE_H

#include <stdint.h>
#include "button_map.h"
#include "gesture_detector.h"

// BLE HID mouse output ("AirMouse-ESP32"): buttons, flick gestures (Back / Forward), relative movement and the wheel.
void app_ble_begin(void);
bool app_ble_connected(void);

// Call once per tick with the debounced buttons, this tick's gesture and the (click-guarded) cursor movement.
//  - connected: left/right press+release (hold = drag), MOUSE_BACK / MOUSE_FORWARD clicks, relative move, solid LED;
//  - not connected: nothing is sent, presses are only logged, the LED heartbeat blinks, and the "held" state is
//    forgotten so a button held across a disconnect cannot stay stuck down after reconnecting.
//  wheel / hwheel: vertical / horizontal scroll notches of this tick (+ = scroll up / right); 0 = none.
void app_ble_dispatch(const logical_buttons_t& b, gesture_event_t gesture, int8_t move_x, int8_t move_y,
                      int8_t wheel, int8_t hwheel, uint32_t now_ms);

#endif // APP_BLE_H
