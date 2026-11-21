#include <math.h>
#include <string.h>
#include "../include/imu_health.h"

void ih_init(imu_health_t* h) {
    memset(h, 0, sizeof *h);
    h->last_reinit_ok = true;
}

const char* ih_reason_name(ih_reason_t r) {
    switch (r) {
        case IH_WHY_READ_FAIL: return "I2C read failed";
        case IH_WHY_ZERO:      return "sensor returns all zeros (it fell asleep / lost power)";
        case IH_WHY_FROZEN:    return "100 identical samples (frozen)";
        case IH_WHY_DEAD:      return "|a| < 0.5 g for 0.5 s";
        default:               return "none";
    }
}

static ih_action_t request_reinit(imu_health_t* h, uint32_t now_ms, ih_reason_t why) {
    uint32_t gap = h->last_reinit_ok ? IH_MIN_GAP_OK_MS : IH_MIN_GAP_FAIL_MS;
    if (h->ever_reinit && (uint32_t)(now_ms - h->last_reinit_ms) < gap) return IH_DROP;   // too soon: keep dropping
    h->reason = why;
    h->reinit_total++;
    h->fail_run = 0; h->zero_run = 0; h->same_run = 0; h->dead_run = 0; h->have_last = false;
    return IH_REINIT;
}

ih_action_t ih_update(imu_health_t* h, uint32_t now_ms, bool read_ok, const imu_data_t* d) {
    if (h->ever_reinit && (int32_t)(now_ms - h->settle_until_ms) < 0) {
        h->have_last = false;                               // the sensor is starting up: ignore, do not count
        return IH_DROP;
    }

    if (!read_ok || !d) {
        h->fail_total++;
        if (h->fail_run < 255) h->fail_run++;
        if (h->fail_run >= IH_FAIL_RUN) return request_reinit(h, now_ms, IH_WHY_READ_FAIL);
        return IH_DROP;
    }
    h->fail_run = 0;

    float v[6] = { d->ax, d->ay, d->az, d->gx, d->gy, d->gz };
    bool bad_number = false;
    for (int i = 0; i < 6; ++i) if (!(v[i] > -1000.0f && v[i] < 1000.0f)) bad_number = true;   // NaN / infinity
    float an = bad_number ? 0.0f : sqrtf(v[0] * v[0] + v[1] * v[1] + v[2] * v[2]);

    // 1. all-zero accelerometer: a live sensor always shows ~1 g
    if (bad_number || (v[0] == 0.0f && v[1] == 0.0f && v[2] == 0.0f)) {
        h->zero_total++;
        if (h->zero_run < 255) h->zero_run++;
        if (h->zero_run >= IH_ZERO_RUN) return request_reinit(h, now_ms, IH_WHY_ZERO);
        return IH_DROP;
    }
    h->zero_run = 0;

    // 2. slower safety net (as before)
    bool identical = h->have_last && memcmp(v, h->last, sizeof v) == 0;
    memcpy(h->last, v, sizeof v);
    h->have_last = true;
    if (identical) { if (h->same_run < 65535) h->same_run++; } else h->same_run = 0;
    if (an < 0.5f) { if (h->dead_run < 65535) h->dead_run++; } else h->dead_run = 0;
    if (h->same_run >= IH_SAME_RUN) return request_reinit(h, now_ms, IH_WHY_FROZEN);
    if (h->dead_run >= IH_DEAD_RUN) return request_reinit(h, now_ms, IH_WHY_DEAD);
    return IH_OK;
}

void ih_note_reinit(imu_health_t* h, uint32_t now_ms, bool ok) {
    h->ever_reinit = true;
    h->last_reinit_ms = now_ms;
    h->last_reinit_ok = ok;
    h->settle_until_ms = now_ms + IH_SETTLE_MS;
}
