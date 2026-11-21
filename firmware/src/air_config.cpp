#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <cmath>
#include "air_config.h"
#include "click_guard.h"

static_assert(AIR_CFG_CLICK_MS_MAX == CG_MAX_LOOKAHEAD * 10, "click_guard_ms range must match the click guard buffer");

enum { K_GAIN_X, K_GAIN_Y, K_FLICK_DPS, K_FLICK_EN, K_CLICK_MS, K_RECENTER_MS, K_SCROLL_EN, K_SCROLL_SENS, K_SCROLL_DEAD, K_SCROLL_INV, K_HSCROLL, K_SCROLL_REF, K_BTN_LEFT, K_BTN_RIGHT, K_BTN_MODE, K_INVERT_X, K_INVERT_Y, K_COUNT };
static const char* const kKeys[K_COUNT] = { "gain_x", "gain_y", "flick_dps", "flick_enable", "click_guard_ms", "recenter_ms",
                                         "scroll_enable", "scroll_sens", "scroll_dead", "scroll_invert", "hscroll", "scroll_ref",
                                         "btn_left", "btn_right", "btn_mode", "invert_x", "invert_y" };

typedef enum { R_OK, R_FORMAT, R_RANGE } set_result_t;

#define MAX_TOKENS     24
#define MAX_TOKEN_LEN  40

// ------------------------------------------------------------------------------------------------------ helpers

static bool ieq(const char* a, const char* b) {      // case-insensitive equality (ASCII)
    while (*a && *b) {
        char ca = *a, cb = *b;
        if (ca >= 'a' && ca <= 'z') ca = (char)(ca - 'a' + 'A');
        if (cb >= 'a' && cb <= 'z') cb = (char)(cb - 'a' + 'A');
        if (ca != cb) return false;
        ++a; ++b;
    }
    return *a == *b;
}

static bool parse_float(const char* s, float* out) {
    if (!s || !*s) return false;
    char* end = NULL;
    float v = strtof(s, &end);
    if (end == s || *end != '\0') return false;
    if (!std::isfinite(v)) return false;             // "nan", "inf", "1e999"
    *out = v;
    return true;
}

static bool parse_int(const char* s, long* out) {
    if (!s || !*s) return false;
    char* end = NULL;
    long v = strtol(s, &end, 10);
    if (end == s || *end != '\0') return false;      // "12.5", "7x", ""
    *out = v;
    return true;
}

static int find_key(const char* k) {
    for (int i = 0; i < K_COUNT; ++i) if (strcmp(k, kKeys[i]) == 0) return i;
    return -1;
}

static set_result_t set_float(float* dst, const char* v, float lo, float hi) {
    float x;
    if (!parse_float(v, &x)) return R_FORMAT;
    if (!(x >= lo && x <= hi)) return R_RANGE;
    *dst = x;
    return R_OK;
}

static set_result_t set_flag(uint8_t* dst, const char* v) {
    long n;
    if (!parse_int(v, &n)) return R_FORMAT;
    if (n != 0 && n != 1) return R_RANGE;
    *dst = (uint8_t)n;
    return R_OK;
}

static set_result_t set_action(uint8_t* dst, const char* v) {
    long n;
    if (!parse_int(v, &n)) return R_FORMAT;
    if (n < 0 || n >= AIR_BTN_COUNT) return R_RANGE;
    *dst = (uint8_t)n;
    return R_OK;
}

static set_result_t set_field(air_config_t* c, int key, const char* v) {
    long n;
    switch (key) {
        case K_GAIN_X:    return set_float(&c->gain_x, v, AIR_CFG_GAIN_MIN, AIR_CFG_GAIN_MAX);
        case K_GAIN_Y:    return set_float(&c->gain_y, v, AIR_CFG_GAIN_MIN, AIR_CFG_GAIN_MAX);
        case K_FLICK_DPS: return set_float(&c->flick_dps, v, AIR_CFG_FLICK_MIN, AIR_CFG_FLICK_MAX);
        case K_FLICK_EN:  return set_flag(&c->flick_enable, v);
        case K_SCROLL_EN: return set_flag(&c->scroll_enable, v);
        case K_SCROLL_SENS: return set_float(&c->scroll_sens, v, AIR_CFG_SCROLL_SENS_MIN, AIR_CFG_SCROLL_SENS_MAX);
        case K_SCROLL_DEAD: return set_float(&c->scroll_dead, v, AIR_CFG_SCROLL_DEAD_MIN, AIR_CFG_SCROLL_DEAD_MAX);
        case K_SCROLL_INV:  return set_flag(&c->scroll_invert, v);
        case K_HSCROLL:     return set_flag(&c->hscroll, v);
        case K_SCROLL_REF:  return set_flag(&c->scroll_ref, v);
        case K_BTN_LEFT:    return set_action(&c->btn_left, v);
        case K_BTN_RIGHT:   return set_action(&c->btn_right, v);
        case K_BTN_MODE:    return set_action(&c->btn_mode, v);
        case K_INVERT_X:    return set_flag(&c->invert_x, v);
        case K_INVERT_Y:    return set_flag(&c->invert_y, v);
        case K_CLICK_MS:
            if (!parse_int(v, &n)) return R_FORMAT;
            if (n < 0 || n > AIR_CFG_CLICK_MS_MAX) return R_RANGE;
            c->click_guard_ms = (uint16_t)(((n + 5) / 10) * 10);    // the guard works in 10 ms steps
            return R_OK;
        case K_RECENTER_MS:
            if (!parse_int(v, &n)) return R_FORMAT;
            if (n < AIR_CFG_RECENTER_MIN || n > AIR_CFG_RECENTER_MAX) return R_RANGE;
            c->recenter_ms = (uint16_t)n;
            return R_OK;
        default: return R_FORMAT;
    }
}

static void fmt_field(const air_config_t* c, int key, char* out, size_t n) {
    switch (key) {
        case K_GAIN_X:    snprintf(out, n, "gain_x=%.3f", (double)c->gain_x); break;
        case K_GAIN_Y:    snprintf(out, n, "gain_y=%.3f", (double)c->gain_y); break;
        case K_FLICK_DPS: snprintf(out, n, "flick_dps=%.1f", (double)c->flick_dps); break;
        case K_FLICK_EN:  snprintf(out, n, "flick_enable=%u", (unsigned)c->flick_enable); break;
        case K_CLICK_MS:  snprintf(out, n, "click_guard_ms=%u", (unsigned)c->click_guard_ms); break;
        case K_RECENTER_MS: snprintf(out, n, "recenter_ms=%u", (unsigned)c->recenter_ms); break;
        case K_SCROLL_EN:   snprintf(out, n, "scroll_enable=%u", (unsigned)c->scroll_enable); break;
        case K_SCROLL_SENS: snprintf(out, n, "scroll_sens=%.2f", (double)c->scroll_sens); break;
        case K_SCROLL_DEAD: snprintf(out, n, "scroll_dead=%.1f", (double)c->scroll_dead); break;
        case K_SCROLL_INV:  snprintf(out, n, "scroll_invert=%u", (unsigned)c->scroll_invert); break;
        case K_HSCROLL:     snprintf(out, n, "hscroll=%u", (unsigned)c->hscroll); break;
        case K_SCROLL_REF:  snprintf(out, n, "scroll_ref=%u", (unsigned)c->scroll_ref); break;
        case K_BTN_LEFT:    snprintf(out, n, "btn_left=%u", (unsigned)c->btn_left); break;
        case K_BTN_RIGHT:   snprintf(out, n, "btn_right=%u", (unsigned)c->btn_right); break;
        case K_BTN_MODE:    snprintf(out, n, "btn_mode=%u", (unsigned)c->btn_mode); break;
        case K_INVERT_X:    snprintf(out, n, "invert_x=%u", (unsigned)c->invert_x); break;
        case K_INVERT_Y:    snprintf(out, n, "invert_y=%u", (unsigned)c->invert_y); break;
        default: if (n) out[0] = '\0'; break;
    }
}

// Append " text" to reply (truncating safely).
static void put(char* buf, size_t size, size_t* len, const char* text) {
    if (*len + 1 >= size) return;
    int w = snprintf(buf + *len, size - *len, " %s", text);
    if (w < 0) return;
    *len += ((size_t)w < size - *len) ? (size_t)w : (size - *len - 1);
}

// ------------------------------------------------------------------------------------------------------ public

void air_config_defaults(air_config_t* cfg) {
    cfg->gain_x = AIR_CFG_GAIN_DEFAULT;
    cfg->gain_y = AIR_CFG_GAIN_DEFAULT;
    cfg->flick_dps = AIR_CFG_FLICK_DEFAULT;
    cfg->flick_enable = 1;
    cfg->click_guard_ms = AIR_CFG_CLICK_MS_DEFAULT;
    cfg->recenter_ms = AIR_CFG_RECENTER_DEFAULT;
    cfg->scroll_enable = 1;
    cfg->scroll_sens = AIR_CFG_SCROLL_SENS_DEFAULT;
    cfg->scroll_dead = AIR_CFG_SCROLL_DEAD_DEFAULT;
    cfg->scroll_invert = 0;
    cfg->hscroll = 0;
    cfg->scroll_ref = 0;
    cfg->btn_left = AIR_BTN_LEFT;
    cfg->btn_right = AIR_BTN_RIGHT;
    cfg->btn_mode = AIR_BTN_MODE;
    cfg->invert_x = 0;
    cfg->invert_y = 0;
}

bool air_config_valid(const air_config_t* cfg) {
    if (!cfg) return false;
    return cfg->gain_x >= AIR_CFG_GAIN_MIN && cfg->gain_x <= AIR_CFG_GAIN_MAX &&
           cfg->gain_y >= AIR_CFG_GAIN_MIN && cfg->gain_y <= AIR_CFG_GAIN_MAX &&
           cfg->flick_dps >= AIR_CFG_FLICK_MIN && cfg->flick_dps <= AIR_CFG_FLICK_MAX &&
           cfg->flick_enable <= 1 &&
           cfg->click_guard_ms <= AIR_CFG_CLICK_MS_MAX && (cfg->click_guard_ms % 10) == 0 &&
           cfg->recenter_ms >= AIR_CFG_RECENTER_MIN && cfg->recenter_ms <= AIR_CFG_RECENTER_MAX &&
           cfg->scroll_enable <= 1 && cfg->scroll_invert <= 1 && cfg->hscroll <= 1 && cfg->scroll_ref <= 1 &&
           cfg->btn_left < AIR_BTN_COUNT && cfg->btn_right < AIR_BTN_COUNT && cfg->btn_mode < AIR_BTN_COUNT &&
           cfg->invert_x <= 1 && cfg->invert_y <= 1 &&
           cfg->scroll_sens >= AIR_CFG_SCROLL_SENS_MIN && cfg->scroll_sens <= AIR_CFG_SCROLL_SENS_MAX &&
           cfg->scroll_dead >= AIR_CFG_SCROLL_DEAD_MIN && cfg->scroll_dead <= AIR_CFG_SCROLL_DEAD_MAX;
}

bool air_config_equal(const air_config_t* a, const air_config_t* b) {
    return a->gain_x == b->gain_x && a->gain_y == b->gain_y && a->flick_dps == b->flick_dps &&
           a->flick_enable == b->flick_enable && a->click_guard_ms == b->click_guard_ms &&
           a->recenter_ms == b->recenter_ms && a->scroll_enable == b->scroll_enable &&
           a->scroll_sens == b->scroll_sens && a->scroll_dead == b->scroll_dead && a->scroll_invert == b->scroll_invert && a->hscroll == b->hscroll && a->scroll_ref == b->scroll_ref &&
           a->btn_left == b->btn_left && a->btn_right == b->btn_right && a->btn_mode == b->btn_mode &&
           a->invert_x == b->invert_x && a->invert_y == b->invert_y;
}

int air_config_format(const air_config_t* cfg, char* buf, size_t size) {
    return snprintf(buf, size,
                    "ver=%d gain_x=%.3f gain_y=%.3f flick_dps=%.1f flick_enable=%u click_guard_ms=%u recenter_ms=%u "
                    "scroll_enable=%u scroll_sens=%.2f scroll_dead=%.1f scroll_invert=%u hscroll=%u scroll_ref=%u "
                    "btn_left=%u btn_right=%u btn_mode=%u invert_x=%u invert_y=%u",
                    AIR_CONFIG_VERSION, (double)cfg->gain_x, (double)cfg->gain_y, (double)cfg->flick_dps,
                    (unsigned)cfg->flick_enable, (unsigned)cfg->click_guard_ms, (unsigned)cfg->recenter_ms,
                    (unsigned)cfg->scroll_enable, (double)cfg->scroll_sens, (double)cfg->scroll_dead, (unsigned)cfg->scroll_invert, (unsigned)cfg->hscroll, (unsigned)cfg->scroll_ref,
                    (unsigned)cfg->btn_left, (unsigned)cfg->btn_right, (unsigned)cfg->btn_mode, (unsigned)cfg->invert_x, (unsigned)cfg->invert_y);
}

air_cfg_action_t air_config_handle(air_config_t* cfg, const char* line, char* reply, size_t reply_size) {
    if (!reply || reply_size == 0) return AIR_CFG_ACT_NONE;
    reply[0] = '\0';
    if (!cfg || !line) { snprintf(reply, reply_size, "ERR internal"); return AIR_CFG_ACT_NONE; }

    // Work on a copy of the line, split into tokens at spaces / tabs / line ends.
    char buf[AIR_CFG_LINE_MAX + 1];
    if (strlen(line) > AIR_CFG_LINE_MAX) { snprintf(reply, reply_size, "ERR too-long"); return AIR_CFG_ACT_NONE; }
    strcpy(buf, line);
    char* tok[MAX_TOKENS];
    int nt = 0;
    char* p = buf;
    while (*p) {
        while (*p == ' ' || *p == '\t' || *p == '\r' || *p == '\n') *p++ = '\0';
        if (!*p) break;
        if (nt >= MAX_TOKENS) { snprintf(reply, reply_size, "ERR too-many"); return AIR_CFG_ACT_NONE; }
        tok[nt++] = p;
        while (*p && *p != ' ' && *p != '\t' && *p != '\r' && *p != '\n') ++p;
    }
    if (nt == 0) { snprintf(reply, reply_size, "ERR empty"); return AIR_CFG_ACT_NONE; }
    for (int i = 0; i < nt; ++i) {
        if (strlen(tok[i]) > MAX_TOKEN_LEN) { snprintf(reply, reply_size, "ERR format"); return AIR_CFG_ACT_NONE; }
    }

    const char* cmd = tok[0];

    if (ieq(cmd, "GET")) {
        char text[AIR_CFG_REPLY_MAX];
        air_config_format(cfg, text, sizeof text);
        snprintf(reply, reply_size, "CFG %s", text);
        return AIR_CFG_ACT_NONE;
    }
    if (ieq(cmd, "DEFAULTS")) {
        air_config_defaults(cfg);
        snprintf(reply, reply_size, "OK defaults");
        return AIR_CFG_ACT_APPLY;
    }
    if (ieq(cmd, "SAVE")) {
        snprintf(reply, reply_size, "OK saved");
        return AIR_CFG_ACT_SAVE;
    }
    if (ieq(cmd, "CAL")) {
        snprintf(reply, reply_size, "OK calibrated");
        return AIR_CFG_ACT_CALIBRATE;
    }
    if (ieq(cmd, "SET")) {
        if (nt < 2) { snprintf(reply, reply_size, "ERR format"); return AIR_CFG_ACT_NONE; }
        air_config_t work = *cfg;                       // all-or-nothing: edit a copy, commit at the end
        bool touched[K_COUNT] = { false };
        for (int i = 1; i < nt; ++i) {
            char* eq = strchr(tok[i], '=');
            if (!eq || eq == tok[i] || eq[1] == '\0') { snprintf(reply, reply_size, "ERR format"); return AIR_CFG_ACT_NONE; }
            *eq = '\0';
            const char* key = tok[i];
            const char* val = eq + 1;
            int k = find_key(key);
            if (k < 0) { snprintf(reply, reply_size, "ERR unknown-key %.24s", key); return AIR_CFG_ACT_NONE; }
            set_result_t r = set_field(&work, k, val);
            if (r != R_OK) { snprintf(reply, reply_size, "ERR %s %s", r == R_RANGE ? "range" : "format", kKeys[k]); return AIR_CFG_ACT_NONE; }
            touched[k] = true;
        }
        *cfg = work;
        snprintf(reply, reply_size, "OK");
        size_t len = strlen(reply);
        for (int k = 0; k < K_COUNT; ++k) {
            if (!touched[k]) continue;
            char piece[48];
            fmt_field(cfg, k, piece, sizeof piece);
            put(reply, reply_size, &len, piece);
        }
        return AIR_CFG_ACT_APPLY;
    }
    snprintf(reply, reply_size, "ERR unknown-cmd");
    return AIR_CFG_ACT_NONE;
}
