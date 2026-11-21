#ifndef BUTTON_MAP_H
#define BUTTON_MAP_H

#include <stdint.h>
#include <stdbool.h>
#include "air_config.h"

#ifdef __cplusplus
extern "C" {
#endif

// Button mapping (PORTABLE CORE, tested on the PC: N24). The three physical buttons (debounced) are turned into logical
// buttons according to the user's settings btn_left / btn_right / btn_mode (air_btn_action_t). Several physical buttons
// with the same action are OR-ed: the action is "held" while any of them is down.
typedef struct {
    bool left;
    bool right;
    bool middle;
    bool back;
    bool forward;
    bool mode;       // the Mode logic (clutch / re-center / flick / double-tap scroll) sees this
} logical_buttons_t;

void bm_apply(bool raw_left, bool raw_right, bool raw_mode,
              uint8_t act_left, uint8_t act_right, uint8_t act_mode, logical_buttons_t* out);
// True when any MOUSE button (left, right, middle, back, forward; not Mode) is held: the click guard then freezes the cursor.
bool bm_any_click(const logical_buttons_t* b);
// "NONE", "LEFT", ... "MODE"; "?" for an unknown value.
const char* bm_action_name(uint8_t act);

#ifdef __cplusplus
}
#endif

#endif // BUTTON_MAP_H
