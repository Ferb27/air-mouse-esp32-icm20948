#ifndef APP_CONFIG_STORE_H
#define APP_CONFIG_STORE_H

#include "air_config.h"

// The user's settings (air_config.h): load from flash at boot, push into the running firmware, answer the '@' protocol
// commands, save to flash (ESP32 Preferences / NVS, namespace "airmouse", one blob under key "cfg").
// Nothing is written to flash except on "@SAVE" (flash wears out), and an unchanged save is skipped.

// Boot: load the stored settings (or the defaults when nothing valid is stored) and apply them. Call after
// app_motion_init() and app_buttons_init().
void app_config_load_and_apply(void);

// Push the live settings into gain / flick threshold / gestures / recenter time / click guard.
void app_config_apply(void);

// The live settings (read-only view).
const air_config_t* app_config_get(void);

// Write the live settings to flash. Returns false when the flash write failed.
bool app_config_save(void);

// The legacy one-letter serial commands ('+', 'y', '<' ...) change the running firmware directly; this copies those
// values back into the live settings so "@GET" and "@SAVE" see them.
void app_config_sync_from_runtime(void);

// Handle one '@' line (without the '@' and the line end), print the '@...' reply on the serial port.
void app_config_handle_line(const char* line);

#endif // APP_CONFIG_STORE_H
