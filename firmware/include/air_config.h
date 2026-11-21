#ifndef AIR_CONFIG_H
#define AIR_CONFIG_H

#include <stdint.h>
#include <stdbool.h>
#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

// User-adjustable settings of the Air Mouse and the text protocol a PC tool uses to read / change them.
// PORTABLE CORE: plain C/C++, no Arduino, tested on the PC (test_motion_pipeline.cpp, N15..N19).
// Storing the settings in flash is the job of the application layer (app_config_store.cpp).
//
// Protocol (one line per command, sent over the serial port; the board answers with one line starting with '@'):
//   @GET                              -> @CFG ver=2 gain_x=0.300 gain_y=0.300 flick_dps=150.0 flick_enable=1 click_guard_ms=40
//                                           recenter_ms=150 scroll_enable=1 scroll_sens=2.00 scroll_dead=2.5 scroll_invert=0 hscroll=0 scroll_ref=0 btn_left=1 btn_right=2 btn_mode=6 invert_x=0 invert_y=0   (one line)
//   @SET gain_x=0.45 flick_dps=180    -> @OK gain_x=0.450 flick_dps=180.0     (applied now, NOT yet saved)
//   @SAVE                             -> @OK saved                            (written to flash)
//   @DEFAULTS                         -> @OK defaults                         (applied now, NOT yet saved)
//   @CAL                              -> @OK calibrated  |  @ERR not-still    (re-measure the gyro bias, board at rest)
//   errors                            -> @ERR range gain_x | @ERR format gain_x | @ERR unknown-key foo | @ERR unknown-cmd
// A @SET line is all-or-nothing: if any value is wrong nothing changes.

#define AIR_CONFIG_VERSION   5

// Ranges and defaults (single source of truth; app_config.h and the pipeline defaults must agree, see test N15)
#define AIR_CFG_GAIN_DEFAULT        0.3f
#define AIR_CFG_GAIN_MIN            0.02f
#define AIR_CFG_GAIN_MAX            3.0f
#define AIR_CFG_FLICK_DEFAULT       150.0f
#define AIR_CFG_FLICK_MIN           40.0f
#define AIR_CFG_FLICK_MAX           600.0f
#define AIR_CFG_CLICK_MS_DEFAULT    40        // click-guard look-ahead; the guard works in 10 ms steps
#define AIR_CFG_CLICK_MS_MAX        100
#define AIR_CFG_RECENTER_DEFAULT    150       // wait after releasing Mode before re-centering
#define AIR_CFG_RECENTER_MIN        50
#define AIR_CFG_RECENTER_MAX        500
#define AIR_CFG_SCROLL_SENS_DEFAULT 2.0f      // scroll speed: wheel notches per second for each degree of tilt beyond the dead zone (first guess)
#define AIR_CFG_SCROLL_SENS_MIN     0.1f
#define AIR_CFG_SCROLL_SENS_MAX     10.0f
#define AIR_CFG_SCROLL_DEAD_DEFAULT 2.5f      // dead zone around the starting pose, degrees (first guess)
#define AIR_CFG_SCROLL_DEAD_MIN     0.0f
#define AIR_CFG_SCROLL_DEAD_MAX     15.0f

#define AIR_CFG_LINE_MAX     400      // longest command line (characters, without the leading '@')
#define AIR_CFG_REPLY_MAX    512      // size of the reply buffer callers should provide

// What a physical button does (btn_left / btn_right / btn_mode). Several buttons may share an action (any of them counts).
typedef enum {
    AIR_BTN_NONE = 0,       // nothing
    AIR_BTN_LEFT,           // left mouse button (hold = drag)
    AIR_BTN_RIGHT,          // right mouse button
    AIR_BTN_MIDDLE,         // middle mouse button
    AIR_BTN_BACK,           // browser Back (mouse button 4)
    AIR_BTN_FORWARD,        // browser Forward (mouse button 5)
    AIR_BTN_MODE,           // Mode: hold = clutch (cursor frozen) + re-center + flick Back/Forward; tap, press again and hold = scroll
    AIR_BTN_COUNT
} air_btn_action_t;

typedef struct {
    float    gain_x;            // cursor speed per deg/s, horizontal (~gain*100 counts per degree)
    float    gain_y;            // ... vertical
    float    flick_dps;         // quick-turn threshold for Back / Forward while Mode is held
    uint8_t  flick_enable;      // 1 = Back/Forward gestures on, 0 = off (Mode stays a clutch)
    uint16_t click_guard_ms;    // 0..100, multiple of 10
    uint16_t recenter_ms;       // 50..500
    uint8_t  scroll_enable;     // 1 = double-tap Mode, hold the 2nd press and tilt = scroll the page
    float    scroll_sens;       // notches per second per degree of tilt beyond the dead zone (0.1..10)
    float    scroll_dead;       // dead zone in degrees around the pose where scrolling started (0..15)
    uint8_t  scroll_invert;     // 1 = reverse the scroll direction
    uint8_t  hscroll;           // 1 = rolling the board left/right while scrolling also scrolls sideways
    uint8_t  btn_left;          // action of the physical button SW2 (GPIO25), default AIR_BTN_LEFT
    uint8_t  btn_right;         // action of SW3 (GPIO26), default AIR_BTN_RIGHT
    uint8_t  btn_mode;          // action of SW4 (GPIO27), default AIR_BTN_MODE
    uint8_t  invert_x;          // 1 = reverse the horizontal cursor direction
    uint8_t  invert_y;          // 1 = reverse the vertical cursor direction
    uint8_t  scroll_ref;        // 0 = scroll centre is the comfortable pose from BEFORE the double-tap (default), 1 = the pose at the second press
} air_config_t;

// What the caller must do after air_config_handle() returned.
typedef enum {
    AIR_CFG_ACT_NONE = 0,       // nothing (reply is the whole answer)
    AIR_CFG_ACT_APPLY,          // *cfg changed: push it into the running firmware
    AIR_CFG_ACT_SAVE,           // write *cfg to flash; replace the reply with "ERR nvs" on failure
    AIR_CFG_ACT_CALIBRATE       // re-measure the gyro bias; replace the reply with "ERR not-still" on failure
} air_cfg_action_t;

void air_config_defaults(air_config_t* cfg);
// True when every field is inside its range (also false for NaN).
bool air_config_valid(const air_config_t* cfg);
bool air_config_equal(const air_config_t* a, const air_config_t* b);
// "ver=1 gain_x=0.300 ..." (no leading '@'). Returns the length it wanted to write (like snprintf).
int  air_config_format(const air_config_t* cfg, char* buf, size_t size);

// Handle ONE protocol line (without the leading '@', without the line end). Always writes a null-terminated reply
// (no '@' prefix, no newline) into `reply` (size >= 1; AIR_CFG_REPLY_MAX is enough for every reply).
air_cfg_action_t air_config_handle(air_config_t* cfg, const char* line, char* reply, size_t reply_size);

#ifdef __cplusplus
}
#endif

#endif // AIR_CONFIG_H
