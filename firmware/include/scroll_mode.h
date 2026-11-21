#ifndef SCROLL_MODE_H
#define SCROLL_MODE_H

#include <stdint.h>
#include <stdbool.h>

#ifdef __cplusplus
extern "C" {
#endif

// Scroll mode of the Mode button (SW4, GPIO27). PORTABLE CORE (no Arduino), tested on the PC (N20..N22).
//
//   Mode held alone               -> clutch (cursor frozen), as before
//   tap Mode, then press again    -> the SECOND press is scroll mode for as long as it is held: the cursor stays
//   quickly and HOLD it              still and the tilt of the board up / down sets the scroll speed
//
// "Tap" = pressed and released within SM_TAP_MAX_MS; the second press must start within SM_GAP_MAX_MS of the
// release (like double-tap-and-drag on a touchpad). The values are first guesses to be tuned by hand.

#define SM_TAP_MAX_MS   250
#define SM_GAP_MAX_MS   350

typedef enum { SM_IDLE = 0, SM_PRESS1, SM_WAIT2, SM_SCROLL } sm_state_t;

typedef struct {
    sm_state_t state;
    uint32_t   t_ms;        // time of the last press (SM_PRESS1) or release (SM_WAIT2)
    bool       last_down;
} scroll_mode_t;

typedef struct {
    bool active;            // scroll mode is on during this tick
    bool started;           // ... turned on during this tick
    bool ended;             // ... turned off during this tick
    bool first_press;       // this tick is the FIRST press of a possible double-tap (the pose before it is the "comfortable" one)
} scroll_mode_out_t;

void sm_init(scroll_mode_t* s);
// Call once per tick with the DEBOUNCED Mode button. enabled=false keeps the state machine idle.
scroll_mode_out_t sm_update(scroll_mode_t* s, bool mode_down, uint32_t now_ms, bool enabled);

// Joystick-style scroll: the ANGLE you tilt the board away from the pose it had when scroll mode started sets the
// scroll SPEED. Hold the tilt and the page keeps scrolling; go back to the starting pose and it stops. So a small
// tilt (10..15 degrees) is enough, no matter how long the page is.
//   speed [notches/s] = sens * (|tilt| - dead zone)      (0 inside the dead zone)
//   nose UP -> wheel > 0 (page scrolls up);  tilt right (right side down) -> hwheel > 0 (scrolls right, only if hscroll)
// Right after the second press the thumb jerks the board, so the starting pose is only locked after ST_ARM_MS
// (until then the reference follows the board and nothing scrolls).
#define ST_ARM_MS     150     // reference = pose at the press: the reference follows the board this long
#define ST_QUIET_MS   100     // reference = pose BEFORE the double-tap: no output for this long after the press (thumb jerk)
#define ST_RAMP_MS    200     // then the speed ramps from 0 to full over this long (no sudden burst)

typedef struct {
    uint32_t start_ms;
    uint32_t last_ms;
    uint32_t live_ms;        // scrolling may produce output from this time on (then it ramps in over ST_RAMP_MS)
    bool     armed;          // the starting pose is locked
    float    ref_pitch;      // starting pose, degrees (nose up +)
    float    ref_roll;       // starting pose, degrees (right side down +)
    float    rem_v;          // fractions of a notch carried to the next tick
    float    rem_h;
} scroll_tilt_t;

// Reference = the pose at the moment of the second press (locked after ST_ARM_MS).
void st_start(scroll_tilt_t* t, uint32_t now_ms);
// Reference given (the comfortable pose from before the double-tap): active at once, starts after ST_QUIET_MS.
void st_start_ref(scroll_tilt_t* t, uint32_t now_ms, float ref_pitch_deg, float ref_roll_deg);
// Call once per tick while scroll mode is on. vg_x / vg_y: x and y components of the pipeline's body gravity vector
// (motion_getBodyGravity; the pipeline frame is X = backward, Y = right, Z = up, so nose up gives vg_x < 0 and the
// right side down gives vg_y < 0). Writes this tick's wheel notches (hwheel is 0 unless hscroll).
void st_update(scroll_tilt_t* t, float vg_x, float vg_y, uint32_t now_ms,
               float sens, float dead_deg, bool invert, bool hscroll, int8_t* wheel, int8_t* hwheel);

// ---- Comfortable pose ------------------------------------------------------------------------------------------------
// Pressing a button twice moves the hand away from the pose it was comfortably held in. So the scroll reference should
// not be the pose at the press, but the pose a moment BEFORE the first press: the history keeps the last 320 ms of
// (pitch, roll) and the reference is its average from 250 ms to 150 ms before the first press (like a TV remote: the
// comfortable pose is the centre, tilt away from it = scroll).
#define PH_LEN              32
#define SC_PRE_BACK_TICKS   25      // 250 ms before the first press ...
#define SC_PRE_AVG_TICKS    10      // ... averaged over 100 ms

typedef struct {
    float   pitch[PH_LEN];
    float   roll[PH_LEN];
    uint8_t head;           // next slot to write
    uint8_t count;
} pose_hist_t;

void ph_init(pose_hist_t* h);
void ph_push(pose_hist_t* h, float vg_x, float vg_y);
// Average pose over `avg` ticks ending `back` ticks ago (0 = newest); uses what exists when the history is shorter.
// Returns false when the history is empty.
bool ph_get(const pose_hist_t* h, int back, int avg, float* pitch_deg, float* roll_deg);

// Everything in one place (the firmware and the tests call the same two functions per tick).
typedef struct {
    scroll_mode_t sm;
    pose_hist_t   hist;
    scroll_tilt_t tilt;
    float         pre_pitch, pre_roll;
    bool          have_pre;
} scroll_ctrl_t;

void sc_init(scroll_ctrl_t* c);
// Call once per tick BEFORE the motion pipeline. vg_x / vg_y: body gravity of the latest estimate.
// ref_before_tap: true = reference is the comfortable pose before the first press, false = the pose at the second press.
scroll_mode_out_t sc_begin(scroll_ctrl_t* c, bool mode_down, uint32_t now_ms, bool enabled,
                           float vg_x, float vg_y, bool ref_before_tap);
// Call once per tick while scroll mode is on, AFTER the pipeline: this tick's wheel notches.
void sc_wheel(scroll_ctrl_t* c, float vg_x, float vg_y, uint32_t now_ms,
              float sens, float dead_deg, bool invert, bool hscroll, int8_t* wheel, int8_t* hwheel);

#ifdef __cplusplus
}
#endif

#endif // SCROLL_MODE_H
