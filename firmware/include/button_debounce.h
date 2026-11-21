#ifndef BUTTON_DEBOUNCE_H
#define BUTTON_DEBOUNCE_H

#include <stdint.h>
#include <stdbool.h>

#ifdef __cplusplus
extern "C" {
#endif

// Time-based debouncer: the stable state only changes after the raw input has held the new value
// for hold_ms without flipping (mechanical tactile switches bounce for a few ms).
typedef struct {
    bool     stable;      // debounced state (true = pressed)
    bool     last_raw;
    uint32_t changed_ms;  // time of the last raw flip
} debounce_t;

void debounce_init(debounce_t* d, bool initial);
bool debounce_update(debounce_t* d, bool raw, uint32_t now_ms, uint32_t hold_ms);
// Asymmetric version: a press is accepted after press_ms, a release after release_ms (short press time = less latency).
bool debounce_update2(debounce_t* d, bool raw, uint32_t now_ms, uint32_t press_ms, uint32_t release_ms);

#ifdef __cplusplus
}
#endif

#endif // BUTTON_DEBOUNCE_H
