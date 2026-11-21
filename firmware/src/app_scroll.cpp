#include <Arduino.h>
#include "app_scroll.h"
#include "app_config_store.h"
#include "motion_pipeline.h"
#include "scroll_mode.h"

static scroll_ctrl_t s_sc;
static bool          s_init = false;

bool app_scroll_update(bool mode_down, uint32_t now_ms) {
    if (!s_init) {
        sc_init(&s_sc);
        s_init = true;
    }
    const air_config_t* cfg = app_config_get();
    float vgx, vgy, vgz;
    motion_getBodyGravity(&vgx, &vgy, &vgz);       // the pipeline's latest attitude estimate: the tilt of the board
    scroll_mode_out_t o = sc_begin(&s_sc, mode_down, now_ms, cfg->scroll_enable != 0, vgx, vgy, cfg->scroll_ref == 0);
    if (o.started) {
        Serial.printf("[SCROLL] on (centre = %s pose; hold the tilt: up = scroll up, down = scroll down)\n",
                      (cfg->scroll_ref == 0 && s_sc.have_pre) ? "the comfortable" : "the current");
    }
    if (o.ended) {
        motion_scheduleRecenter(now_ms);          // like the clutch release: wait for the hand, then re-center
        Serial.println("[SCROLL] off");
    }
    return o.active;
}

void app_scroll_convert(bool scroll_on, uint32_t now_ms, int8_t* dx, int8_t* dy, int8_t* wheel, int8_t* hwheel) {
    *wheel = 0;
    *hwheel = 0;
    if (!scroll_on) return;
    const air_config_t* cfg = app_config_get();
    float vgx, vgy, vgz;
    motion_getBodyGravity(&vgx, &vgy, &vgz);
    sc_wheel(&s_sc, vgx, vgy, now_ms, cfg->scroll_sens, cfg->scroll_dead, cfg->scroll_invert != 0, cfg->hscroll != 0, wheel, hwheel);
    *dx = 0;                                       // the cursor stays still while scrolling
    *dy = 0;
}
