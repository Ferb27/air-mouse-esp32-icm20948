#include <Arduino.h>
#include <BleMouse.h>
#include "app_ble.h"
#include "pin_definitions.h"

// BLE Mouse Device Configuration
static BleMouse bleMouse("AirMouse-ESP32", "EmbeddedSystemsGroup", 100);

// What the host currently sees as held (edge-detected): left, right, middle, back, forward
static bool s_held[5] = { false, false, false, false, false };
static bool s_was_connected = false;

void app_ble_begin(void) {
    bleMouse.begin();
}

bool app_ble_connected(void) {
    return bleMouse.isConnected();
}

static void sync_button(uint8_t code, bool want, bool* held) {
    if (want && !*held) bleMouse.press(code);
    else if (!want && *held) bleMouse.release(code);
    *held = want;
}

void app_ble_dispatch(const logical_buttons_t& b, gesture_event_t gesture, int8_t move_x, int8_t move_y,
                      int8_t wheel, int8_t hwheel, uint32_t now_ms) {
    if (bleMouse.isConnected()) {
        // Solid LED when connected
        digitalWrite(PIN_LED_STATUS, HIGH);

        s_was_connected = true;

        // Handle Flick Gestures (Back / Forward). press + release, NOT click(): click() overwrites the whole button state
        // and would release a button the user is holding (a drag).
        if (gesture == GESTURE_EVENT_FLICK_LEFT) {
            Serial.println("[GESTURE] >>> Flick Left Detected -> Sending MOUSE_BACK (History Back)");
            bleMouse.press(MOUSE_BACK);
            bleMouse.release(MOUSE_BACK);
        } else if (gesture == GESTURE_EVENT_FLICK_RIGHT) {
            Serial.println("[GESTURE] >>> Flick Right Detected -> Sending MOUSE_FORWARD (History Forward)");
            bleMouse.press(MOUSE_FORWARD);
            bleMouse.release(MOUSE_FORWARD);
        }

        // Mapped mouse buttons (press / release on the edges; hold = drag)
        sync_button(MOUSE_LEFT,    b.left,    &s_held[0]);
        sync_button(MOUSE_RIGHT,   b.right,   &s_held[1]);
        sync_button(MOUSE_MIDDLE,  b.middle,  &s_held[2]);
        sync_button(MOUSE_BACK,    b.back,    &s_held[3]);
        sync_button(MOUSE_FORWARD, b.forward, &s_held[4]);

        // Dispatch Relative Mouse Movement and the wheel
        if (move_x != 0 || move_y != 0 || wheel != 0 || hwheel != 0) {
            bleMouse.move(move_x, move_y, wheel, hwheel);
        }
    } else {
        // Slow heartbeat blink when waiting for BLE connection
        digitalWrite(PIN_LED_STATUS, ((now_ms / 500) % 2) == 0 ? HIGH : LOW);
        // Not connected: nothing is sent. The library keeps its own button bits and puts them in EVERY report, so a
        // button held when the link dropped would be "stuck down" after reconnecting: clear them (it only sets the bits
        // when not connected, nothing is sent). The presses are logged by app_buttons_log.
        if (s_was_connected) {
            bleMouse.release(MOUSE_LEFT | MOUSE_RIGHT | MOUSE_MIDDLE | MOUSE_BACK | MOUSE_FORWARD);
            s_was_connected = false;
        }
        for (int i = 0; i < 5; ++i) s_held[i] = false;
    }
}
