#include <Arduino.h>
#include <esp_system.h>
#include "app_status.h"
#include "app_config.h"
#include "app_imu_guard.h"

static uint32_t s_last_diag_ms = 0;
static uint32_t s_loop_count = 0;

void app_status_count_loop(void) {
    s_loop_count++;
}

void app_status_resync(void) {
    s_last_diag_ms = millis();
    s_loop_count = 0;          // otherwise the next "Rate" would count the loops of more than one second (seen as 169-172 Hz)
}

void app_status_report(uint32_t now_ms, const mouse_output_t& out) {
    if (now_ms - s_last_diag_ms < APP_STATUS_PERIOD_MS) return;
    s_last_diag_ms = now_ms;
    float bx, by, bz;
    motion_getBias(&bx, &by, &bz);
    Serial.printf("[STATUS] Rate: %d Hz | Stat: %d | Clutch: %d | dX: %+4d, dY: %+4d | BiasZ: %+5.2f | Up: %lus | Frz: %u | Heal: %u | Err: %lu | Rec: %lu | Rst: %d\n",
                  s_loop_count, out.is_stationary, out.is_clutch_active, out.delta_x, out.delta_y, bz,
                  (unsigned long)(now_ms / 1000), (unsigned)app_imu_frozen_count(), (unsigned)app_imu_heal_count(),
                  (unsigned long)app_imu_read_fail_count(), (unsigned long)app_imu_bus_recover_count(), (int)esp_reset_reason());
    s_loop_count = 0;
}
