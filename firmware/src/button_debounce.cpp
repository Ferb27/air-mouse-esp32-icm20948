#include "../include/button_debounce.h"

void debounce_init(debounce_t* d, bool initial) {
    d->stable = initial;
    d->last_raw = initial;
    d->changed_ms = 0;
}

bool debounce_update(debounce_t* d, bool raw, uint32_t now_ms, uint32_t hold_ms) {
    if (raw != d->last_raw) {
        d->last_raw = raw;
        d->changed_ms = now_ms;                 // restart the timer on every flip (bounce)
    } else if (raw != d->stable && (uint32_t)(now_ms - d->changed_ms) >= hold_ms) {
        d->stable = raw;                        // held long enough: accept
    }
    return d->stable;
}

bool debounce_update2(debounce_t* d, bool raw, uint32_t now_ms, uint32_t press_ms, uint32_t release_ms) {
    return debounce_update(d, raw, now_ms, raw ? press_ms : release_ms);
}
