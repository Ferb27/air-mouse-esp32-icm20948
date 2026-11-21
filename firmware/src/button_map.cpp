#include "../include/button_map.h"

static void add(logical_buttons_t* o, uint8_t act, bool down) {
    if (!down) return;
    switch (act) {
        case AIR_BTN_LEFT:    o->left = true; break;
        case AIR_BTN_RIGHT:   o->right = true; break;
        case AIR_BTN_MIDDLE:  o->middle = true; break;
        case AIR_BTN_BACK:    o->back = true; break;
        case AIR_BTN_FORWARD: o->forward = true; break;
        case AIR_BTN_MODE:    o->mode = true; break;
        default: break;       // AIR_BTN_NONE or an unknown value: nothing
    }
}

void bm_apply(bool raw_left, bool raw_right, bool raw_mode,
              uint8_t act_left, uint8_t act_right, uint8_t act_mode, logical_buttons_t* out) {
    out->left = out->right = out->middle = out->back = out->forward = out->mode = false;
    add(out, act_left, raw_left);
    add(out, act_right, raw_right);
    add(out, act_mode, raw_mode);
}

bool bm_any_click(const logical_buttons_t* b) {
    return b->left || b->right || b->middle || b->back || b->forward;
}

const char* bm_action_name(uint8_t act) {
    switch (act) {
        case AIR_BTN_NONE:    return "NONE";
        case AIR_BTN_LEFT:    return "LEFT";
        case AIR_BTN_RIGHT:   return "RIGHT";
        case AIR_BTN_MIDDLE:  return "MIDDLE";
        case AIR_BTN_BACK:    return "BACK";
        case AIR_BTN_FORWARD: return "FORWARD";
        case AIR_BTN_MODE:    return "MODE";
        default:              return "?";
    }
}
