#include <Arduino.h>
#include <Preferences.h>
#include <string.h>
#include "app_config_store.h"
#include "app_config.h"
#include "app_buttons.h"
#include "app_imu.h"
#include "app_motion.h"
#include "app_timing.h"
#include "motion_pipeline.h"

static const char* const NVS_NAMESPACE = "airmouse";
static const char* const NVS_KEY       = "cfg";

// What is stored: the version first, so settings written by a firmware with a different layout are ignored.
typedef struct {
    uint32_t     version;
    air_config_t cfg;
} stored_t;

static air_config_t s_cfg;               // live settings
static air_config_t s_saved;             // what the flash holds (valid only when s_have_saved)
static bool         s_have_saved = false;

const air_config_t* app_config_get(void) {
    return &s_cfg;
}

void app_config_apply(void) {
    motion_setGain(s_cfg.gain_x, s_cfg.gain_y);
    app_flick_set(s_cfg.flick_dps);
    motion_setGesturesEnabled(s_cfg.flick_enable != 0);
    motion_setRecenterSettleMs(s_cfg.recenter_ms);
    app_buttons_set_lookahead_ms(s_cfg.click_guard_ms);
}

void app_config_load_and_apply(void) {
    air_config_defaults(&s_cfg);
    s_have_saved = false;

    Preferences p;
    if (!p.begin(NVS_NAMESPACE, false)) {              // read-write so the namespace exists on the very first boot
        Serial.println("[CONFIG] flash storage (NVS) not available -> defaults, settings cannot be saved");
    } else {
        size_t len = p.isKey(NVS_KEY) ? p.getBytesLength(NVS_KEY) : 0;     // isKey first: no NVS error line on a fresh board
        if (len == 0) {
            Serial.println("[CONFIG] nothing stored yet -> defaults");
        } else if (len != sizeof(stored_t)) {
            Serial.printf("[CONFIG] stored settings have another size (%u, expected %u) -> defaults\n", (unsigned)len, (unsigned)sizeof(stored_t));
        } else {
            stored_t st;
            p.getBytes(NVS_KEY, &st, sizeof st);
            if (st.version == AIR_CONFIG_VERSION && air_config_valid(&st.cfg)) {
                s_cfg = st.cfg;
                s_saved = st.cfg;
                s_have_saved = true;
                Serial.println("[CONFIG] loaded the saved settings from flash");
            } else {
                Serial.println("[CONFIG] stored settings are invalid or from another version -> defaults");
            }
        }
        p.end();
    }
    app_config_apply();

    char text[AIR_CFG_REPLY_MAX];
    air_config_format(&s_cfg, text, sizeof text);
    Serial.printf("[CONFIG] in use: %s\n", text);
}

bool app_config_save(void) {
    if (s_have_saved && air_config_equal(&s_cfg, &s_saved)) return true;   // identical: do not wear the flash
    Preferences p;
    if (!p.begin(NVS_NAMESPACE, false)) return false;
    stored_t st;
    memset(&st, 0, sizeof st);                          // padding bytes become 0, not stack garbage
    st.version = AIR_CONFIG_VERSION;
    st.cfg = s_cfg;
    size_t n = p.putBytes(NVS_KEY, &st, sizeof st);
    p.end();
    if (n != sizeof st) return false;
    s_saved = s_cfg;
    s_have_saved = true;
    return true;
}

void app_config_sync_from_runtime(void) {
    motion_getGain(&s_cfg.gain_x, &s_cfg.gain_y);
    s_cfg.flick_dps = app_flick_threshold();
    s_cfg.click_guard_ms = (uint16_t)app_buttons_get_lookahead_ms();
}

void app_config_handle_line(const char* line) {
    app_config_sync_from_runtime();                     // the one-letter commands may have changed things since the last line

    char reply[AIR_CFG_REPLY_MAX];
    air_cfg_action_t act = air_config_handle(&s_cfg, line, reply, sizeof reply);
    switch (act) {
        case AIR_CFG_ACT_APPLY:
            app_config_apply();
            break;
        case AIR_CFG_ACT_SAVE:
            if (!app_config_save()) snprintf(reply, sizeof reply, "ERR nvs");
            break;
        case AIR_CFG_ACT_CALIBRATE: {
            bool ok = app_imu_calibrate(APP_CAL_RUNTIME_ATTEMPTS, false);   // blocks ~2 s per attempt; board must rest
            app_resync();
            if (!ok) snprintf(reply, sizeof reply, "ERR not-still");
            break;
        }
        case AIR_CFG_ACT_NONE:
        default:
            break;
    }
    Serial.printf("@%s\n", reply);
}
