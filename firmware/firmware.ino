

#include <Arduino.h>

#include "include/app_boot.h"
#include "include/app_buttons.h"
#include "include/app_config_store.h"
#include "include/button_map.h"
#include "include/app_ble.h"
#include "include/app_imu.h"
#include "include/app_imu_guard.h"
#include "include/app_motion.h"
#include "include/app_scroll.h"
#include "include/app_serial_cmd.h"
#include "include/app_status.h"
#include "include/app_timing.h"
#include "include/motion_pipeline.h"

void setup() {
    app_boot();
}

void loop() {
    app_serial_poll();

    uint32_t now_ms;
    if (!app_loop_due(&now_ms)) return;              // strict 10 ms (100 Hz) period
    app_status_count_loop();

    // 1. Read the sensor (already rotated into the pipeline axes)
    imu_data_t imu_data = {};
    bool read_ok = app_imu_read(&imu_data);

    // 1a. Sensor health: a failed read, an all-zero sample or a lost sensor is dropped at once; 3 in a row recover the
    //     I2C bus and re-initialise the sensor (a few tens of ms). While the sensor is unusable the cursor does not move
    //     but the buttons and the telemetry keep working (clicks must not die with the sensor).
    bool sensor_ok = app_imu_health_step(read_ok, imu_data, now_ms);
    // 1b. Self-heal of a wrong bias (may block ~2 s)
    if (sensor_ok && app_imu_self_heal(imu_data)) {
        app_resync();
        return;
    }

    // 2. Buttons (debounced), then the user's mapping: what each physical button does (button_map.h)
    buttons_t btn = app_buttons_read(now_ms);
    const air_config_t* cfg = app_config_get();
    logical_buttons_t lb;
    bm_apply(btn.left, btn.right, btn.mode, cfg->btn_left, cfg->btn_right, cfg->btn_mode, &lb);
    app_buttons_log(btn, cfg->btn_left, cfg->btn_right, cfg->btn_mode, app_ble_connected());

    mouse_output_t out = {};                         // no motion, no gesture (used while the sensor is unusable)
    int8_t wheel = 0, hwheel = 0;
    if (sensor_ok) {
        // 2b. Scroll mode: tap Mode, press again and hold. It is not a clutch hold, so the pipeline only sees Mode in the other cases.
        bool scroll_on = app_scroll_update(lb.mode, now_ms);
        bool clutch = lb.mode && !scroll_on;

        // 3. Motion pipeline (bias, stationary lock, reference frame, Mode clutch/recenter, flick gestures)
        out = motion_process(&imu_data, clutch, now_ms);
        app_motion_log(out, clutch);

        // 3a0. Reverse the cursor direction if the user asked for it (the pipeline clamps to +-127, so negating is safe)
        if (cfg->invert_x) out.delta_x = (int8_t)-out.delta_x;
        if (cfg->invert_y) out.delta_y = (int8_t)-out.delta_y;

        // 3a. While scrolling, the tilt of the board becomes the wheel speed and the cursor stays still
        app_scroll_convert(scroll_on, now_ms, &out.delta_x, &out.delta_y, &wheel, &hwheel);
    }

    // 3b. Click guard: drop the jerk that precedes a press, freeze the cursor while a button is held
    int8_t move_x = 0, move_y = 0;
    app_buttons_filter_motion(bm_any_click(&lb), out.delta_x, out.delta_y, now_ms, &move_x, &move_y);

    // 4. BLE HID output
    app_ble_dispatch(lb, out.gesture, move_x, move_y, wheel, hwheel, now_ms);

    // 5. Periodic telemetry
    app_status_report(now_ms, out);
}
