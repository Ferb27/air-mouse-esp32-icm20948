#include <math.h>
#include "../include/scroll_mode.h"

void sm_init(scroll_mode_t* s) {
    s->state = SM_IDLE;
    s->t_ms = 0;
    s->last_down = false;
}

scroll_mode_out_t sm_update(scroll_mode_t* s, bool mode_down, uint32_t now_ms, bool enabled) {
    scroll_mode_out_t out = { false, false, false, false };
    bool was_scrolling = (s->state == SM_SCROLL);

    if (!enabled) {                                  // switched off (also in the middle of a scroll)
        s->state = SM_IDLE;
        s->last_down = mode_down;
        out.ended = was_scrolling;
        return out;
    }

    bool press = mode_down && !s->last_down;
    bool release = !mode_down && s->last_down;

    switch (s->state) {
        case SM_IDLE:
            if (press) { s->state = SM_PRESS1; s->t_ms = now_ms; out.first_press = true; }
            break;
        case SM_PRESS1:                              // first press: short = a tap, long = plain clutch
            if (release) {
                if ((uint32_t)(now_ms - s->t_ms) <= SM_TAP_MAX_MS) { s->state = SM_WAIT2; s->t_ms = now_ms; }
                else s->state = SM_IDLE;
            }
            break;
        case SM_WAIT2:                               // waiting for the second press
            if (press) {
                if ((uint32_t)(now_ms - s->t_ms) <= SM_GAP_MAX_MS) { s->state = SM_SCROLL; out.started = true; }
                else { s->state = SM_PRESS1; s->t_ms = now_ms; out.first_press = true; }     // too late: this is a new first press
            } else if ((uint32_t)(now_ms - s->t_ms) > SM_GAP_MAX_MS) {
                s->state = SM_IDLE;
            }
            break;
        case SM_SCROLL:
            if (release) { s->state = SM_IDLE; out.ended = true; }
            break;
    }
    s->last_down = mode_down;
    out.active = (s->state == SM_SCROLL);
    return out;
}

static float clampf(float x, float lo, float hi) { return x < lo ? lo : (x > hi ? hi : x); }

static float angle_deg(float s) {
    if (!(s > -1000.0f && s < 1000.0f)) return 0.0f;     // NaN / infinity: treat as "no tilt"
    return asinf(clampf(s, -1.0f, 1.0f)) * 57.29578f;
}

// Speed (notches per second) for a tilt of x degrees: nothing inside the dead zone, linear beyond it.
static float tilt_speed(float x, float dead, float sens) {
    if (x > dead)  return (x - dead) * sens;
    if (x < -dead) return (x + dead) * sens;
    return 0.0f;
}

static int8_t take_notches(float* rem, float add) {
    float v = *rem + add;
    int n = (int)v;                                  // toward zero: whole notches only
    *rem = v - (float)n;
    if (n > 127)  { n = 127;  *rem = 0.0f; }
    if (n < -127) { n = -127; *rem = 0.0f; }
    return (int8_t)n;
}

void st_start(scroll_tilt_t* t, uint32_t now_ms) {
    t->start_ms = now_ms;
    t->last_ms = now_ms;
    t->live_ms = now_ms + ST_ARM_MS;
    t->armed = false;
    t->ref_pitch = 0.0f;
    t->ref_roll = 0.0f;
    t->rem_v = 0.0f;
    t->rem_h = 0.0f;
}

void st_start_ref(scroll_tilt_t* t, uint32_t now_ms, float ref_pitch_deg, float ref_roll_deg) {
    st_start(t, now_ms);
    t->armed = true;
    t->ref_pitch = ref_pitch_deg;
    t->ref_roll = ref_roll_deg;
    t->live_ms = now_ms + ST_QUIET_MS;
}

void st_update(scroll_tilt_t* t, float vg_x, float vg_y, uint32_t now_ms,
               float sens, float dead_deg, bool invert, bool hscroll, int8_t* wheel, int8_t* hwheel) {
    float dt = (float)(now_ms - t->last_ms) * 0.001f;
    t->last_ms = now_ms;
    dt = clampf(dt, 0.001f, 0.05f);
    *wheel = 0;
    *hwheel = 0;

    float pitch = angle_deg(-vg_x);                  // nose up +
    float roll  = angle_deg(-vg_y);                  // right side down +
    if (!t->armed) {                                 // the reference follows the board while the thumb settles
        t->ref_pitch = pitch;
        t->ref_roll = roll;
        if ((uint32_t)(now_ms - t->start_ms) >= ST_ARM_MS) t->armed = true;
        return;
    }
    if ((int32_t)(now_ms - t->live_ms) < 0) return;                  // quiet time right after the press
    float ramp = clampf((float)(now_ms - t->live_ms) / (float)ST_RAMP_MS, 0.0f, 1.0f);   // soft start
    float dir = (invert ? -1.0f : 1.0f) * ramp;
    *wheel = take_notches(&t->rem_v, tilt_speed(pitch - t->ref_pitch, dead_deg, sens) * dir * dt);
    if (hscroll) *hwheel = take_notches(&t->rem_h, tilt_speed(roll - t->ref_roll, dead_deg, sens) * dir * dt);
    else         t->rem_h = 0.0f;
}

// ---- pose history ----------------------------------------------------------------------------------------------------
void ph_init(pose_hist_t* h) {
    h->head = 0;
    h->count = 0;
    for (int i = 0; i < PH_LEN; ++i) { h->pitch[i] = 0.0f; h->roll[i] = 0.0f; }
}

void ph_push(pose_hist_t* h, float vg_x, float vg_y) {
    h->pitch[h->head] = angle_deg(-vg_x);
    h->roll[h->head]  = angle_deg(-vg_y);
    h->head = (uint8_t)((h->head + 1) % PH_LEN);
    if (h->count < PH_LEN) h->count++;
}

bool ph_get(const pose_hist_t* h, int back, int avg, float* pitch_deg, float* roll_deg) {
    if (h->count == 0 || avg < 1 || back < 0) return false;
    if (back > h->count - 1) back = h->count - 1;                     // history shorter than asked: use the oldest
    float sp = 0.0f, sr = 0.0f;
    int n = 0;
    for (int k = back; k < back + avg && k < h->count; ++k) {
        int idx = ((int)h->head - 1 - k + 2 * PH_LEN) % PH_LEN;
        sp += h->pitch[idx];
        sr += h->roll[idx];
        ++n;
    }
    *pitch_deg = sp / (float)n;
    *roll_deg = sr / (float)n;
    return true;
}

// ---- controller ------------------------------------------------------------------------------------------------------
void sc_init(scroll_ctrl_t* c) {
    sm_init(&c->sm);
    ph_init(&c->hist);
    st_start(&c->tilt, 0);
    c->pre_pitch = 0.0f;
    c->pre_roll = 0.0f;
    c->have_pre = false;
}

scroll_mode_out_t sc_begin(scroll_ctrl_t* c, bool mode_down, uint32_t now_ms, bool enabled,
                           float vg_x, float vg_y, bool ref_before_tap) {
    ph_push(&c->hist, vg_x, vg_y);
    scroll_mode_out_t o = sm_update(&c->sm, mode_down, now_ms, enabled);
    if (o.first_press) c->have_pre = ph_get(&c->hist, SC_PRE_BACK_TICKS, SC_PRE_AVG_TICKS, &c->pre_pitch, &c->pre_roll);
    if (o.started) {
        if (ref_before_tap && c->have_pre) st_start_ref(&c->tilt, now_ms, c->pre_pitch, c->pre_roll);
        else                               st_start(&c->tilt, now_ms);
    }
    return o;
}

void sc_wheel(scroll_ctrl_t* c, float vg_x, float vg_y, uint32_t now_ms,
              float sens, float dead_deg, bool invert, bool hscroll, int8_t* wheel, int8_t* hwheel) {
    st_update(&c->tilt, vg_x, vg_y, now_ms, sens, dead_deg, invert, hscroll, wheel, hwheel);
}
