#include "../include/click_guard.h"

static void clear_queue(click_guard_t* g) {
    for (int i = 0; i < CG_MAX_LOOKAHEAD; ++i) { g->qx[i] = 0; g->qy[i] = 0; }
}

void cg_init(click_guard_t* g, uint8_t lookahead) {
    g->lookahead = lookahead > CG_MAX_LOOKAHEAD ? CG_MAX_LOOKAHEAD : lookahead;
    g->pressed = false;
    g->press_ms = 0;
    clear_queue(g);
}

void cg_set_lookahead(click_guard_t* g, uint8_t lookahead) {
    g->lookahead = lookahead > CG_MAX_LOOKAHEAD ? CG_MAX_LOOKAHEAD : lookahead;
    clear_queue(g);
}

void cg_update(click_guard_t* g, bool pressed, int8_t dx, int8_t dy, uint32_t now_ms, int8_t* out_dx, int8_t* out_dy) {
    if (pressed && !g->pressed) {            // press edge: drop the delayed motion that preceded it
        g->pressed = true;
        g->press_ms = now_ms;
        clear_queue(g);
    } else if (!pressed && g->pressed) {
        g->pressed = false;
    }

    bool frozen = g->pressed && (uint32_t)(now_ms - g->press_ms) < CG_DRAG_MS;
    int8_t in_x = frozen ? 0 : dx;
    int8_t in_y = frozen ? 0 : dy;

    if (g->lookahead == 0) {
        *out_dx = in_x;
        *out_dy = in_y;
        return;
    }
    *out_dx = g->qx[0];                      // oldest pending sample goes out
    *out_dy = g->qy[0];
    for (int i = 0; i + 1 < g->lookahead; ++i) {
        g->qx[i] = g->qx[i + 1];
        g->qy[i] = g->qy[i + 1];
    }
    g->qx[g->lookahead - 1] = in_x;
    g->qy[g->lookahead - 1] = in_y;
}
