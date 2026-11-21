#ifndef YAW_FLICK_H
#define YAW_FLICK_H

#include <stdint.h>
#include <stdbool.h>
#include "gesture_detector.h"

#ifdef __cplusplus
extern "C" {
#endif

// Quick-turn flick detector (used while the Mode button is held). Input: turning rate about "up" in deg/s
// (+ = turning left, - = right). Fires FLICK_LEFT / FLICK_RIGHT on the first sample above the threshold, then stays
// locked until the rate drops below 35 % of the threshold, and ignores the return swing for YF_BLOCK_MS after any gesture.
#define YF_BLOCK_MS 600

typedef struct {
    float    thresh_dps;       // 0 = detector off
    bool     locked;
    uint32_t block_until_ms;
} yaw_flick_t;

void yf_init(yaw_flick_t* y, float thresh_dps);
void yf_set_threshold(yaw_flick_t* y, float thresh_dps);
void yf_reset(yaw_flick_t* y);                 // clear lock and block time (keeps the threshold)
void yf_on_press(yaw_flick_t* y);              // Mode button just pressed: unlock
gesture_event_t yf_update(yaw_flick_t* y, float yaw_dps, uint32_t now_ms);
void yf_note_gesture(yaw_flick_t* y, uint32_t now_ms);   // any gesture fired (this or the accel detector): start the block

#ifdef __cplusplus
}
#endif

#endif // YAW_FLICK_H
