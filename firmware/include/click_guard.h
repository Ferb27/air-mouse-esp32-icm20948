#ifndef CLICK_GUARD_H
#define CLICK_GUARD_H

#include <stdint.h>
#include <stdbool.h>

#ifdef __cplusplus
extern "C" {
#endif

// Click guard for an air mouse: pressing a button with the thumb jerks the whole board, so the cursor slides off
// the target before the button-up arrives (Windows only clicks if down and up land on the same object).
//  1) look-ahead delay: cursor deltas are delayed by `lookahead` samples (10 ms each); when a press is detected the
//     delayed (not yet sent) deltas are DROPPED, which removes the jerk that preceded the press;
//  2) freeze: while a button is held, deltas are discarded for the first CG_DRAG_MS; a longer hold is a drag and
//     the cursor moves again.
#define CG_MAX_LOOKAHEAD 10
#define CG_DRAG_MS 250

typedef struct {
    int8_t   qx[CG_MAX_LOOKAHEAD];
    int8_t   qy[CG_MAX_LOOKAHEAD];
    uint8_t  lookahead;     // delay in samples (0 = off)
    bool     pressed;
    uint32_t press_ms;
} click_guard_t;

void cg_init(click_guard_t* g, uint8_t lookahead);
void cg_set_lookahead(click_guard_t* g, uint8_t lookahead);
// Call once per 10 ms tick. `pressed` = any of left/right currently down (debounced).
void cg_update(click_guard_t* g, bool pressed, int8_t dx, int8_t dy, uint32_t now_ms, int8_t* out_dx, int8_t* out_dy);

#ifdef __cplusplus
}
#endif

#endif // CLICK_GUARD_H
