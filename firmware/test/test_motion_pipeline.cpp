#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>
#include <math.h>
#include <assert.h>

#include "../include/icm20948_registers.h"
#include "../include/icm20948_driver.h"
#include "../include/gesture_detector.h"
#include "../include/motion_pipeline.h"
#include "../include/button_debounce.h"
#include "../include/click_guard.h"
#include "../include/air_config.h"
#include "../include/scroll_mode.h"
#include "../include/button_map.h"
#include "../include/imu_health.h"
#include <string.h>

// Test counter
static int s_tests_passed = 0;

#define TEST_ASSERT(cond, msg) \
    do { \
        if (!(cond)) { \
            fprintf(stderr, "[FAIL] %s:%d: Assertion '%s' failed: %s\n", __FILE__, __LINE__, #cond, msg); \
            exit(1); \
        } \
    } while (0)

#define TEST_PASS(msg) \
    do { \
        s_tests_passed++; \
        printf("[PASS] (%d) %s\n", s_tests_passed, msg); \
    } while (0)

// 1. Verify Register Bitfields
void test_register_bitfields(void) {
    // PWR_MGMT_1: SLEEP=0 (bit 6), LP_EN=0 (bit 5), CLKSEL=001 (bits 2:0) -> 0x01
    TEST_ASSERT(VAL_PWR_MGMT_1_WAKE == 0x01, "VAL_PWR_MGMT_1_WAKE must be 0x01");

    // GYRO_CONFIG_1: FCHOICE=1 (bit 0), FS=500dps (bits 2:1 = 01), DLPF=51.2Hz (bits 5:3 = 011)
    // 0b00011011 = 0x1B
    uint8_t gyro_cfg = (1 << 0) | (0x01 << 1) | (0x03 << 3);
    TEST_ASSERT(gyro_cfg == 0x1B, "GYRO_CONFIG_1 manual bitfield must match 0x1B");
    TEST_ASSERT(VAL_GYRO_CONFIG_1_DEFAULT == 0x1B, "VAL_GYRO_CONFIG_1_DEFAULT must be 0x1B");

    // ACCEL_CONFIG: FCHOICE=1 (bit 0), FS=4g (bits 2:1 = 01), DLPF=50.4Hz (bits 5:3 = 011 per TDK DS-000189 Table 17)
    // Note: ACCEL_DLPFCFG = 010 corresponds to 111.4 Hz. Setting 011 gives 50.4 Hz.
    // 0b00011011 = 0x1B
    uint8_t accel_cfg = (1 << 0) | (0x01 << 1) | (0x03 << 3);
    TEST_ASSERT(accel_cfg == 0x1B, "ACCEL_CONFIG manual bitfield must match 0x1B");
    TEST_ASSERT(VAL_ACCEL_CONFIG_DEFAULT == 0x1B, "VAL_ACCEL_CONFIG_DEFAULT must be 0x1B");

    // ACCEL_SMPLRT_DIV: 12-bit divider for 102.27 Hz ODR (matching Gyro ODR)
    TEST_ASSERT(VAL_ACCEL_SMPLRT_DIV_1_100HZ == 0x00, "ACCEL_SMPLRT_DIV_1 must be 0x00");
    TEST_ASSERT(VAL_ACCEL_SMPLRT_DIV_2_100HZ == 0x0A, "ACCEL_SMPLRT_DIV_2 must be 0x0A");
    TEST_ASSERT(VAL_ACCEL_SMPLRT_DIV_100HZ == 10, "VAL_ACCEL_SMPLRT_DIV_100HZ must be 10");

    TEST_PASS("Register bitfield calculations match TDK DS-000189 datasheet (ACCEL_CONFIG=0x1B, ACCEL_DIV=10)");
}

// 2. Test Driver Semi-Register Functions & Readback Diagnostics
void test_driver_semi_register(void) {
    bool ok = imu_init();
    TEST_ASSERT(ok, "imu_init() must succeed in mock environment");

    icm20948_diag_t diag = imu_getDiagnostics();
    TEST_ASSERT(diag.who_am_i == VAL_WHO_AM_I_EXPECTED, "WHO_AM_I must read 0xEA");
    TEST_ASSERT(diag.pwr_mgmt_1 == 0x01, "PWR_MGMT_1 readback must be 0x01");
    TEST_ASSERT(diag.gyro_config_1 == 0x1B, "GYRO_CONFIG_1 readback must be 0x1B");
    TEST_ASSERT(diag.accel_config == 0x1B, "ACCEL_CONFIG readback must be 0x1B");
    TEST_ASSERT(diag.gyro_smplrt_div == 10, "GYRO_SMPLRT_DIV readback must be 10");
    TEST_ASSERT(diag.accel_smplrt_div_1 == 0x00, "ACCEL_SMPLRT_DIV_1 readback must be 0x00");
    TEST_ASSERT(diag.accel_smplrt_div_2 == 0x0A, "ACCEL_SMPLRT_DIV_2 readback must be 0x0A");

    TEST_PASS("Semi-register driver initialization and readback diagnostics verified");
}

// 3. Test Stationary Detection & Anti-Drift Auto-Zero
void test_stationary_detection(void) {
    motion_init(NULL);
    motion_setBias(5.0f, -3.0f, 2.0f); // Pre-load some initial bias

    imu_data_t stationary_sample = {
        .gx = 5.05f, .gy = -2.95f, .gz = 2.02f, // Tiny residual noise < 0.1 dps
        .ax = 0.0f,  .ay = 0.0f,  .az = 1.01f  // 1.01g gravity
    };

    mouse_output_t out;
    // Feed 35 samples (window threshold is 30)
    for (int i = 0; i < 35; ++i) {
        out = motion_process(&stationary_sample, false, i * 10);
    }

    TEST_ASSERT(out.is_stationary == true, "Device must be detected as STATIONARY");
    TEST_ASSERT(out.delta_x == 0 && out.delta_y == 0, "Cursor movement must be ZERO when stationary");

    TEST_PASS("Stationary detection and anti-drift zero-output verified");
}

// 4. Test Dead-zone and Active Rotation Response
void test_deadzone_and_rotation(void) {
    motion_init(NULL);
    motion_setBias(0.0f, 0.0f, 0.0f);

    // Sub-threshold movement: 0.5 dps (below low threshold 0.8 dps)
    imu_data_t tiny_rot = {
        .gx = 0.0f, .gy = 0.5f, .gz = 0.5f,
        .ax = 0.2f, .ay = 0.0f, .az = 0.98f
    };
    mouse_output_t out = motion_process(&tiny_rot, false, 100);
    TEST_ASSERT(out.delta_x == 0 && out.delta_y == 0, "Sub-threshold movement must be clamped to zero");

    // Deliberate movement: 15 dps (well above threshold)
    imu_data_t fast_rot = {
        .gx = 0.0f, .gy = 15.0f, .gz = -20.0f,   // gz < 0 = clockwise from above = turning RIGHT
        .ax = 0.2f, .ay = 0.0f, .az = 0.98f
    };
    out = motion_process(&fast_rot, false, 110);
    TEST_ASSERT(out.delta_x > 0, "Yaw right rotation must produce positive delta_x");
    TEST_ASSERT(out.delta_y != 0, "Pitch rotation must produce non-zero delta_y");

    TEST_PASS("Deadzone filtering and deliberate rotation response verified");
}

// 5. Test Clutch Freeze & Recenter Transformation
void test_clutch_and_recenter(void) {
    motion_init(NULL);

    imu_data_t rot = {
        .gx = 0.0f, .gy = 10.0f, .gz = 10.0f,
        .ax = 0.0f, .ay = 0.0f, .az = 1.0f
    };

    // When clutch is held, delta must be strictly 0
    mouse_output_t out = motion_process(&rot, true, 200);
    TEST_ASSERT(out.is_clutch_active == true, "Clutch must be active");
    TEST_ASSERT(out.delta_x == 0 && out.delta_y == 0, "Movement must be frozen when clutch is held");

    // Test Pointing Upward: Gravity along X axis (+1.0g on ax)
    imu_data_t upward_pose = {
        .gx = 0.0f, .gy = 0.0f, .gz = 0.0f,
        .ax = 1.0f, .ay = 0.0f, .az = 0.0f
    };
    // Settle the filter in upward pose
    for (int i = 0; i < 20; ++i) {
        motion_process(&upward_pose, true, 210 + i * 10);
    }
    // Release clutch -> recenter triggered
    out = motion_process(&upward_pose, false, 420);
    TEST_ASSERT(out.is_clutch_active == false, "Clutch must be released");

    // In upward pose, yaw around gravity (which is now ax) should drive delta_x
    imu_data_t yaw_upward = {
        .gx = -15.0f, .gy = 0.0f, .gz = 0.0f,   // upward pose: "up" is +X, turning right = negative rotation about it
        .ax = 1.0f,  .ay = 0.0f, .az = 0.0f
    };
    out = motion_process(&yaw_upward, false, 430);
    TEST_ASSERT(out.delta_x > 0, "Yaw rotation in upward pose must drive horizontal delta_x");

    TEST_PASS("Clutch freeze and pointing-upward adaptive reference transform verified");
}

// 6. Test 6-Axis Attitude Estimation & Gravity Removal (P1-A & P1-B)
void test_attitude_and_gravity_removal(void) {
    motion_init(NULL);

    // Verify initial attitude quaternion is normalized identity
    float q0, q1, q2, q3;
    motion_getAttitude(&q0, &q1, &q2, &q3);
    float q_norm = sqrtf(q0*q0 + q1*q1 + q2*q2 + q3*q3);
    TEST_ASSERT(fabsf(q_norm - 1.0f) < 1e-4f, "Initial quaternion must have unit norm");
    TEST_ASSERT(fabsf(q0 - 1.0f) < 1e-4f, "Initial quaternion q0 must be 1.0");

    // Rest flat on table (1.0g along Z)
    imu_data_t static_flat = {
        .gx = 0.0f, .gy = 0.0f, .gz = 0.0f,
        .ax = 0.0f, .ay = 0.0f, .az = 1.0f
    };
    for (int i = 0; i < 20; ++i) {
        motion_process(&static_flat, false, 500 + i * 10);
    }

    // Body gravity should be [0, 0, 1]
    float gx, gy, gz;
    motion_getBodyGravity(&gx, &gy, &gz);
    TEST_ASSERT(fabsf(gx) < 0.05f && fabsf(gy) < 0.05f && fabsf(gz - 1.0f) < 0.05f,
                "Estimated body gravity in flat rest must be approximately [0, 0, 1]");

    // Linear acceleration with gravity removed should be approximately [0, 0, 0]
    float lx, ly, lz;
    motion_getLinearAccel(&lx, &ly, &lz);
    TEST_ASSERT(fabsf(lx) < 0.05f && fabsf(ly) < 0.05f && fabsf(lz) < 0.05f,
                "Linear acceleration at rest must be approximately zero after gravity removal");

    // Integrate continuous yaw rotation (e.g. 90 dps for 1.0s = 100 samples)
    imu_data_t yaw_spin = {
        .gx = 0.0f, .gy = 0.0f, .gz = 90.0f,
        .ax = 0.0f, .ay = 0.0f, .az = 1.0f
    };
    for (int i = 0; i < 100; ++i) {
        motion_process(&yaw_spin, false, 700 + i * 10);
    }
    motion_getAttitude(&q0, &q1, &q2, &q3);
    q_norm = sqrtf(q0*q0 + q1*q1 + q2*q2 + q3*q3);
    TEST_ASSERT(fabsf(q_norm - 1.0f) < 1e-4f, "Quaternion must maintain unit norm during rotation");
    // After 90 deg yaw rotation, q3 should be non-zero (sin(45 deg) ~ 0.707)
    TEST_ASSERT(fabsf(q3) > 0.5f, "Yaw rotation must propagate into quaternion z-component");

    TEST_PASS("6-axis attitude estimation and gravity-free linear acceleration verified (P1-A)");
}

// 7. Test Translational Flick Gesture Recognition Baseline (P1-B)
void test_flick_gesture(void) {
    gesture_init(NULL);

    // Sequence for Left Flick:
    // 1. Armed (Clutch held)
    gesture_event_t ev = gesture_update(0.0f, 20.0f, true, 100);
    TEST_ASSERT(ev == GESTURE_EVENT_NONE, "No gesture on arming");

    // 2. Strong lateral acceleration left (a_lat = -1.5g)
    ev = gesture_update(-1.5f, 50.0f, true, 180);
    TEST_ASSERT(ev == GESTURE_EVENT_NONE, "No event yet on peak phase");
    TEST_ASSERT(gesture_getState() == SM_GESTURE_PEAK_LEFT, "State must be PEAK_LEFT");

    // 3. Return deceleration (a_lat = +0.6g after 100ms)
    ev = gesture_update(+0.6f, 30.0f, true, 280);
    TEST_ASSERT(ev == GESTURE_EVENT_FLICK_LEFT, "Left Flick + Return must trigger GESTURE_EVENT_FLICK_LEFT");

    // Sequence for Right Flick:
    gesture_init(NULL);
    ev = gesture_update(0.0f, 20.0f, true, 400);

    // Peak right (a_lat = +1.6g)
    ev = gesture_update(+1.6f, 40.0f, true, 480);
    TEST_ASSERT(gesture_getState() == SM_GESTURE_PEAK_RIGHT, "State must be PEAK_RIGHT");

    // Return deceleration (a_lat = -0.5g after 90ms)
    ev = gesture_update(-0.5f, 25.0f, true, 570);
    TEST_ASSERT(ev == GESTURE_EVENT_FLICK_RIGHT, "Right Flick + Return must trigger GESTURE_EVENT_FLICK_RIGHT");

    // Test False Positive Rejection: Slow movement (|a_lat| = 0.3g)
    gesture_init(NULL);
    for (int t = 0; t < 20; ++t) {
        ev = gesture_update(0.3f, 15.0f, true, 600 + t * 10);
        TEST_ASSERT(ev == GESTURE_EVENT_NONE, "Slow movement must NEVER trigger a flick gesture");
    }

    TEST_PASS("Translational flick gesture recognition (Left/Right) and false positive rejection verified (P1-B)");
}

// 8. Test Attitude Convergence from Wrong Initial Pose & Physical Consistency (P1-A)
void test_attitude_convergence_p1a(void) {
    motion_init(NULL);

    // Subtest 1: Convergence from wrong initial attitude quaternion
    // Set initial q = [0.7071, 0.7071, 0, 0] (90 deg rotated about X, meaning body gravity begins as [0, 1, 0])
    motion_setAttitude(0.7071f, 0.7071f, 0.0f, 0.0f);

    float q0, q1, q2, q3;
    motion_getAttitude(&q0, &q1, &q2, &q3);
    float q_norm = sqrtf(q0*q0 + q1*q1 + q2*q2 + q3*q3);
    TEST_ASSERT(fabsf(q_norm - 1.0f) < 1e-4f, "Initial set attitude must have unit norm");

    // Static flat input (1.0g along Z, zero gyro rates)
    imu_data_t flat_input = {
        .gx = 0.0f, .gy = 0.0f, .gz = 0.0f,
        .ax = 0.0f, .ay = 0.0f, .az = 1.0f
    };

    // Feed 250 samples (~2.5s @ nominal 100 Hz, tau = 0.5s -> 5*tau = 99.3% convergence)
    for (int i = 0; i < 250; ++i) {
        motion_process(&flat_input, false, 1000 + i * 10);
        motion_getAttitude(&q0, &q1, &q2, &q3);
        q_norm = sqrtf(q0*q0 + q1*q1 + q2*q2 + q3*q3);
        TEST_ASSERT(fabsf(q_norm - 1.0f) < 1e-4f, "Quaternion must maintain unit norm during convergence");
    }

    // Verify attitude converged towards flat horizontal plane:
    float gx, gy, gz;
    motion_getBodyGravity(&gx, &gy, &gz);
    TEST_ASSERT(fabsf(gx) < 0.05f, "Pitch component vg_x must converge to ~0");
    TEST_ASSERT(fabsf(gy) < 0.05f, "Roll component vg_y must converge to ~0");
    TEST_ASSERT(fabsf(gz - 1.0f) < 0.05f, "Vertical component vg_z must converge to ~1.0");

    // Static tilted pose residual linear acceleration must be < 0.05g
    float lx, ly, lz;
    motion_getLinearAccel(&lx, &ly, &lz);
    float lin_norm = sqrtf(lx*lx + ly*ly + lz*lz);
    TEST_ASSERT(lin_norm < 0.05f, "Residual linear acceleration after convergence must be < 0.05g");

    // Subtest 2: Sign check of Roll and Pitch in >= 2 tilt poses
    // Pose A: +30 deg pitch down (nose down, gravity vector projects positively onto X)
    // ax = sin(30 deg) = +0.50g, ay = 0.0g, az = cos(30 deg) = +0.866g
    imu_data_t pitch_down = {
        .gx = 0.0f, .gy = 0.0f, .gz = 0.0f,
        .ax = 0.50f, .ay = 0.0f, .az = 0.866f
    };
    motion_init(NULL);
    for (int i = 0; i < 250; ++i) {
        motion_process(&pitch_down, false, 4000 + i * 10);
    }
    motion_getBodyGravity(&gx, &gy, &gz);
    TEST_ASSERT(gx > 0.45f && gx < 0.55f, "Positive pitch (+30 deg) must produce positive vg_x ~ 0.50");
    TEST_ASSERT(fabsf(gy) < 0.05f, "Pitch tilt should have negligible roll cross-talk");
    TEST_ASSERT(gz > 0.80f && gz < 0.90f, "vg_z must reflect cos(30 deg) ~ 0.866");
    motion_getLinearAccel(&lx, &ly, &lz);
    lin_norm = sqrtf(lx*lx + ly*ly + lz*lz);
    TEST_ASSERT(lin_norm < 0.05f, "Residual linear acceleration in +30 deg pitch must be < 0.05g");

    // Pose B: +20 deg roll right (gravity projects positively onto Y)
    // ax = 0.0g, ay = sin(20 deg) = +0.342g, az = cos(20 deg) = +0.940g
    imu_data_t roll_right = {
        .gx = 0.0f, .gy = 0.0f, .gz = 0.0f,
        .ax = 0.0f, .ay = 0.342f, .az = 0.940f
    };
    motion_init(NULL);
    for (int i = 0; i < 250; ++i) {
        motion_process(&roll_right, false, 7000 + i * 10);
    }
    motion_getBodyGravity(&gx, &gy, &gz);
    TEST_ASSERT(fabsf(gx) < 0.05f, "Roll tilt should have negligible pitch cross-talk");
    TEST_ASSERT(gy > 0.30f && gy < 0.40f, "Positive roll (+20 deg) must produce positive vg_y ~ 0.342");
    TEST_ASSERT(gz > 0.90f && gz < 0.96f, "vg_z must reflect cos(20 deg) ~ 0.940");
    motion_getLinearAccel(&lx, &ly, &lz);
    lin_norm = sqrtf(lx*lx + ly*ly + lz*lz);
    TEST_ASSERT(lin_norm < 0.05f, "Residual linear acceleration in +20 deg roll must be < 0.05g");

    // Subtest 3: Yaw unobservable by gravity: pure yaw rotation does not cause tilt divergence
    motion_init(NULL);
    imu_data_t yaw_rot = {
        .gx = 0.0f, .gy = 0.0f, .gz = 45.0f, // 45 dps yaw
        .ax = 0.0f, .ay = 0.0f, .az = 1.0f
    };
    for (int i = 0; i < 200; ++i) {
        motion_process(&yaw_rot, false, 10000 + i * 10);
        motion_getAttitude(&q0, &q1, &q2, &q3);
        q_norm = sqrtf(q0*q0 + q1*q1 + q2*q2 + q3*q3);
        TEST_ASSERT(fabsf(q_norm - 1.0f) < 1e-4f, "Quaternion norm must remain 1.0 under pure yaw");
    }
    motion_getBodyGravity(&gx, &gy, &gz);
    TEST_ASSERT(fabsf(gx) < 0.05f && fabsf(gy) < 0.05f && fabsf(gz - 1.0f) < 0.05f,
                "Pure yaw rotation must not cause tilt divergence (body gravity stays [0,0,1])");
    motion_getAttitude(&q0, &q1, &q2, &q3);
    TEST_ASSERT(fabsf(q3) > 0.3f, "Yaw angle integrated purely in relative quaternion component q3");

    TEST_PASS("Attitude convergence, tilt sign checks, residual accel < 0.05g, and unobservable yaw verified (P1-A)");
}

// 9. Test Dynamic dt, Time-Invariance, Gyro Integration, and Clamp Timing
void test_dynamic_dt_and_timing(void) {
    // -------------------------------------------------------------------------
    // Subtest A: Time-Invariance of Tilt Correction across Different Cadences
    // Initial wrong attitude: q = [0.7071, 0.7071, 0, 0] (vg = [0, 1, 0])
    // Total duration = 2.5s (2500 ms) for all cadences
    // Cadences: 5ms (500 steps), 10ms (250 steps), 20ms (125 steps), 50ms (50 steps)
    // -------------------------------------------------------------------------
    const uint32_t cadences_ms[] = {5, 10, 20, 50};
    const int num_cadences = sizeof(cadences_ms) / sizeof(cadences_ms[0]);
    float final_vgz[4] = {0};
    float final_vgy[4] = {0};

    imu_data_t static_flat = {
        .gx = 0.0f, .gy = 0.0f, .gz = 0.0f,
        .ax = 0.0f, .ay = 0.0f, .az = 1.0f
    };

    for (int c = 0; c < num_cadences; ++c) {
        uint32_t dt_ms = cadences_ms[c];
        uint32_t total_steps = 2500 / dt_ms;

        motion_init(NULL);
        // Prime last_process_ms at t = 1000
        motion_process(&static_flat, false, 1000);
        // Set wrong initial attitude: 90 deg roll error
        motion_setAttitude(0.707107f, 0.707107f, 0.0f, 0.0f);

        for (uint32_t step = 1; step <= total_steps; ++step) {
            uint32_t now = 1000 + step * dt_ms;
            motion_process(&static_flat, false, now);
        }

        float gx, gy, gz;
        motion_getBodyGravity(&gx, &gy, &gz);
        final_vgy[c] = gy;
        final_vgz[c] = gz;

        // Verify vertical gravity converged within tolerance |v_gz - 1.0| < 0.05
        TEST_ASSERT(fabsf(gz - 1.0f) < 0.05f,
                    "Tilt correction must converge v_gz to ~1.0 regardless of cadence");
        TEST_ASSERT(fabsf(gy) < 0.05f,
                    "Tilt correction must converge v_gy to ~0.0 regardless of cadence");
    }

    // Verify time-invariance: max pairwise difference between any two cadences < 0.02
    for (int i = 0; i < num_cadences; ++i) {
        for (int j = i + 1; j < num_cadences; ++j) {
            float diff_z = fabsf(final_vgz[i] - final_vgz[j]);
            float diff_y = fabsf(final_vgy[i] - final_vgy[j]);
            TEST_ASSERT(diff_z < 0.02f, "Max pairwise difference in v_gz between cadences must be < 0.02");
            TEST_ASSERT(diff_y < 0.02f, "Max pairwise difference in v_gy between cadences must be < 0.02");
        }
    }

    // -------------------------------------------------------------------------
    // Subtest B: Gyro Integration across Total Time (1.0s pure yaw @ 90 dps = 90 deg)
    // Run both Uniform (10ms steps) and Irregular cadences
    // -------------------------------------------------------------------------
    imu_data_t yaw_90dps = {
        .gx = 0.0f, .gy = 0.0f, .gz = 90.0f,
        .ax = 0.0f, .ay = 0.0f, .az = 1.0f
    };

    // 1. Uniform 10ms steps (100 steps = 1000 ms)
    motion_init(NULL);
    motion_process(&yaw_90dps, false, 1000); // prime at 1000ms
    for (int i = 1; i <= 100; ++i) {
        motion_process(&yaw_90dps, false, 1000 + i * 10);
    }
    float q0, q1, q2, q3;
    motion_getAttitude(&q0, &q1, &q2, &q3);
    float angle_uniform = 2.0f * atan2f(fabsf(q3), q0) * (180.0f / 3.14159265f);
    TEST_ASSERT(fabsf(angle_uniform - 90.0f) < 1.5f,
                "Uniform 1.0s @ 90 dps yaw must integrate to 90 deg +/- 1.5 deg");
    TEST_ASSERT(fabsf(q0 - 0.7071f) < 0.02f && fabsf(q3 - 0.7071f) < 0.02f,
                "Quaternion components must match [0.7071, 0, 0, 0.7071] for 90 deg rotation");

    // 2. Irregular steps summing to exactly 1000 ms (50 steps: 10 repetitions of {10, 20, 15, 25, 30} ms)
    motion_init(NULL);
    motion_process(&yaw_90dps, false, 1000); // prime at 1000ms
    const uint32_t dt_pattern[] = {10, 20, 15, 25, 30};
    uint32_t curr_t = 1000;
    for (int rep = 0; rep < 10; ++rep) {
        for (int p = 0; p < 5; ++p) {
            curr_t += dt_pattern[p];
            motion_process(&yaw_90dps, false, curr_t);
        }
    }
    TEST_ASSERT(curr_t == 2000, "Irregular schedule total duration must be exactly 1000ms");
    motion_getAttitude(&q0, &q1, &q2, &q3);
    float angle_irreg = 2.0f * atan2f(fabsf(q3), q0) * (180.0f / 3.14159265f);
    TEST_ASSERT(fabsf(angle_irreg - 90.0f) < 1.5f,
                "Irregular 1.0s @ 90 dps yaw must integrate to 90 deg +/- 1.5 deg");
    TEST_ASSERT(fabsf(q0 - 0.7071f) < 0.02f && fabsf(q3 - 0.7071f) < 0.02f,
                "Irregular schedule quaternion must match [0.7071, 0, 0, 0.7071]");

    // -------------------------------------------------------------------------
    // Subtest C: Clamp Behavior (dt = 200ms clamped to 50ms)
    // -------------------------------------------------------------------------
    motion_init(NULL);
    motion_process(&static_flat, false, 1000); // prime at t = 1000
    // Step at t = 1200ms (dt_raw = 200ms > 50ms clamp) at wz = 90 dps
    motion_process(&yaw_90dps, false, 1200);
    motion_getAttitude(&q0, &q1, &q2, &q3);
    float clamped_angle = 2.0f * atan2f(fabsf(q3), q0) * (180.0f / 3.14159265f);
    // Clamped dt is 0.050s, expected angle = 90 * 0.050 = 4.5 deg (NOT 18.0 deg)
    TEST_ASSERT(fabsf(clamped_angle - 4.5f) < 0.25f,
                "Clamped dt (50ms) @ 90 dps must integrate to 4.5 deg +/- 0.25 deg");
    TEST_ASSERT(clamped_angle < 6.0f,
                "Angle must NOT integrate full 200ms (18.0 deg)");

    // Safety check: non-forward timestamp handled safely without crash
    motion_process(&yaw_90dps, false, 1100);
    motion_getAttitude(&q0, &q1, &q2, &q3);
    float q_norm = sqrtf(q0*q0 + q1*q1 + q2*q2 + q3*q3);
    TEST_ASSERT(fabsf(q_norm - 1.0f) < 1e-4f, "Quaternion must remain unit norm with backward timestamp");

    TEST_PASS("Dynamic dt: tilt time-invariance (5-50ms), yaw integration (1.0s @ 90dps), and 50ms clamp verified");
}

// 10. Test End-to-End Gesture Recognition via motion_process() (P1-B)
void test_motion_process_end_to_end_gestures_p1b(void) {
    motion_init(NULL);

    // Settle attitude filter in flat rest
    imu_data_t flat_rest = { .gx = 0.0f, .gy = 0.0f, .gz = 0.0f, .ax = 0.0f, .ay = 0.0f, .az = 1.0f };
    for (int i = 0; i < 20; ++i) {
        motion_process(&flat_rest, false, 100 + i * 10);
    }

    // Subtest 1: End-to-end Flat Flick Left via motion_process()
    // Step 1a: Press clutch button to arm gesture detection
    imu_data_t clutch_arm = { .gx = 0.0f, .gy = 0.0f, .gz = 0.0f, .ax = 0.0f, .ay = 0.0f, .az = 1.0f };
    mouse_output_t out = motion_process(&clutch_arm, true, 350);
    TEST_ASSERT(out.is_clutch_active == true, "Clutch must be active");
    TEST_ASSERT(out.gesture == GESTURE_EVENT_NONE, "Arming must not trigger gesture");
    TEST_ASSERT(out.delta_x == 0 && out.delta_y == 0, "Cursor must be frozen while clutch is held");

    // Step 1b: Peak left impulse (ay = -1.5g)
    imu_data_t flick_left_peak = { .gx = 0.0f, .gy = 10.0f, .gz = 10.0f, .ax = 0.0f, .ay = -1.5f, .az = 1.0f };
    out = motion_process(&flick_left_peak, true, 400);
    TEST_ASSERT(out.gesture == GESTURE_EVENT_NONE, "Peak phase must not trigger event immediately");
    TEST_ASSERT(out.delta_x == 0 && out.delta_y == 0, "Cursor must be frozen while clutch is held");

    // Step 1c: Return deceleration (ay = +0.5g after 100ms, within 60-450ms window)
    imu_data_t flick_left_return = { .gx = 0.0f, .gy = 5.0f, .gz = 5.0f, .ax = 0.0f, .ay = 0.5f, .az = 1.0f };
    out = motion_process(&flick_left_return, true, 500);
    TEST_ASSERT(out.gesture == GESTURE_EVENT_FLICK_LEFT, "Flat Flick Left must trigger GESTURE_EVENT_FLICK_LEFT");

    // Subtest 2: End-to-end Flat Flick Right via motion_process() (after 350ms cooldown)
    // Step 2a: Arm after cooldown (> 350ms elapsed)
    out = motion_process(&clutch_arm, true, 900); // 400ms after cooldown
    TEST_ASSERT(out.gesture == GESTURE_EVENT_NONE, "Arming must not trigger event");

    // Step 2b: Peak right impulse (ay = +1.5g)
    imu_data_t flick_right_peak = { .gx = 0.0f, .gy = 10.0f, .gz = 10.0f, .ax = 0.0f, .ay = 1.5f, .az = 1.0f };
    out = motion_process(&flick_right_peak, true, 950);
    TEST_ASSERT(out.gesture == GESTURE_EVENT_NONE, "Peak phase right must not trigger event immediately");

    // Step 2c: Return deceleration (ay = -0.5g after 100ms)
    imu_data_t flick_right_return = { .gx = 0.0f, .gy = 5.0f, .gz = 5.0f, .ax = 0.0f, .ay = -0.5f, .az = 1.0f };
    out = motion_process(&flick_right_return, true, 1050);
    TEST_ASSERT(out.gesture == GESTURE_EVENT_FLICK_RIGHT, "Flat Flick Right must trigger GESTURE_EVENT_FLICK_RIGHT");

    // Subtest 3: Tilted Flick within Posture Envelope with Gravity Subtraction
    // Posture: +20 deg pitch (ax = sin 20 deg = 0.342g, az = cos 20 deg = 0.940g) - within +/-45 deg envelope!
    motion_init(NULL);
    imu_data_t pose_pitch20 = { .gx = 0.0f, .gy = 0.0f, .gz = 0.0f, .ax = 0.342f, .ay = 0.0f, .az = 0.940f };
    for (int i = 0; i < 250; ++i) {
        motion_process(&pose_pitch20, false, 2000 + i * 10);
    }
    // Arm clutch in tilted posture
    out = motion_process(&pose_pitch20, true, 4550);
    TEST_ASSERT(out.gesture == GESTURE_EVENT_NONE, "Arming in tilted pose must not trigger gesture");

    // Now perform flick right while holding pitch 20 deg posture:
    // Accelerometer measures tilted gravity PLUS lateral hand flick acceleration:
    // ay_peak = 0.0g + 1.5g = +1.5g
    imu_data_t tilted_flick_peak = { .gx = 0.0f, .gy = 0.0f, .gz = 0.0f, .ax = 0.342f, .ay = 1.5f, .az = 0.940f };
    out = motion_process(&tilted_flick_peak, true, 4600);
    TEST_ASSERT(out.gesture == GESTURE_EVENT_NONE, "Tilted peak phase must not trigger event immediately");

    // ay_return = 0.0g - 0.5g = -0.5g
    imu_data_t tilted_flick_return = { .gx = 0.0f, .gy = 0.0f, .gz = 0.0f, .ax = 0.342f, .ay = -0.5f, .az = 0.940f };
    out = motion_process(&tilted_flick_return, true, 4700); // 100ms return phase
    TEST_ASSERT(out.gesture == GESTURE_EVENT_FLICK_RIGHT, "Tilted flick within posture envelope must trigger valid gesture");

    // Subtest 4: Posture Envelope Rejection (> 45 deg Pitch or > 30 deg Roll)
    // Case A: Pitch = 60 deg (> 45 deg threshold) -> ax = sin(60 deg) = 0.866g, az = 0.500g
    motion_init(NULL);
    imu_data_t pose_pitch60 = { .gx = 0.0f, .gy = 0.0f, .gz = 0.0f, .ax = 0.866f, .ay = 0.0f, .az = 0.500f };
    for (int i = 0; i < 250; ++i) {
        motion_process(&pose_pitch60, false, 6000 + i * 10);
    }
    // Try to flick in invalid pitch pose:
    imu_data_t invalid_flick_peak = { .gx = 0.0f, .gy = 0.0f, .gz = 0.0f, .ax = 0.866f, .ay = 1.5f, .az = 0.500f };
    out = motion_process(&invalid_flick_peak, true, 8600);
    imu_data_t invalid_flick_return = { .gx = 0.0f, .gy = 0.0f, .gz = 0.0f, .ax = 0.866f, .ay = -0.5f, .az = 0.500f };
    out = motion_process(&invalid_flick_return, true, 8700);
    TEST_ASSERT(out.gesture == GESTURE_EVENT_NONE, "Flick when Pitch > 45 deg must be REJECTED (posture envelope)");

    // Case B: Roll = 45 deg (> 30 deg threshold) -> ay = sin(45 deg) = 0.707g, az = 0.707g
    motion_init(NULL);
    imu_data_t pose_roll45 = { .gx = 0.0f, .gy = 0.0f, .gz = 0.0f, .ax = 0.0f, .ay = 0.707f, .az = 0.707f };
    for (int i = 0; i < 250; ++i) {
        motion_process(&pose_roll45, false, 10000 + i * 10);
    }
    // Try to flick in invalid roll pose:
    imu_data_t roll_invalid_peak = { .gx = 0.0f, .gy = 0.0f, .gz = 0.0f, .ax = 0.0f, .ay = 0.707f + 1.5f, .az = 0.707f };
    out = motion_process(&roll_invalid_peak, true, 12600);
    imu_data_t roll_invalid_return = { .gx = 0.0f, .gy = 0.0f, .gz = 0.0f, .ax = 0.0f, .ay = 0.707f - 0.5f, .az = 0.707f };
    out = motion_process(&roll_invalid_return, true, 12700);
    TEST_ASSERT(out.gesture == GESTURE_EVENT_NONE, "Flick when Roll > 30 deg must be REJECTED (posture envelope)");

    // Subtest 5: Static Gravity Tilt without motion -> 0 clicks
    motion_init(NULL);
    imu_data_t static_tilt = { .gx = 0.0f, .gy = 0.0f, .gz = 0.0f, .ax = 0.30f, .ay = 0.20f, .az = 0.93f };
    for (int i = 0; i < 50; ++i) {
        out = motion_process(&static_tilt, true, 14000 + i * 10);
        TEST_ASSERT(out.gesture == GESTURE_EVENT_NONE, "Static gravity tilt must NEVER produce false gesture clicks");
    }

    // Subtest 6: Slow motion & pure high-speed rotation -> 0 clicks
    // Slow lateral movement (ay = 0.4g < 1.15g threshold)
    imu_data_t slow_move = { .gx = 0.0f, .gy = 0.0f, .gz = 0.0f, .ax = 0.0f, .ay = 0.4f, .az = 1.0f };
    for (int i = 0; i < 20; ++i) {
        out = motion_process(&slow_move, true, 15000 + i * 10);
        TEST_ASSERT(out.gesture == GESTURE_EVENT_NONE, "Slow movement must NEVER trigger gesture clicks");
    }

    // Pure high-speed rotation (gyro norm = 700 dps > 600 dps rejection threshold)
    imu_data_t spin_move = { .gx = 0.0f, .gy = 0.0f, .gz = 700.0f, .ax = 0.0f, .ay = 1.5f, .az = 1.0f };
    out = motion_process(&spin_move, true, 16000);
    TEST_ASSERT(out.gesture == GESTURE_EVENT_NONE, "High-speed spin (> 600 dps) must be REJECTED");

    TEST_PASS("End-to-end motion_process() gestures, tilted gestures, and posture/spin rejections verified (P1-B)");
}

// ==============================================================
// POLARITY NOTE (2026-10-08): turning RIGHT = negative gz (right-hand rule, Z up); cursor moves right (+dX).
// Motion inputs below therefore use "gz = bias - w" for "w dps to the right".
// GAIN NOTE (2026-10-08): default gain changed 2.2 -> 0.3 (hand tests: far too sensitive). Every count-based
// bound below was written for gain 2.2 and is scaled by K = 0.3/2.2 = 0.136 (same physical meaning).
// ==============================================================
// NEW TESTS: N1 - N6 (Noise-robust slow-motion and tightening response)
// ==============================================================
static uint32_t s_seed = 12345u;
static float frand01(void) {
    s_seed = s_seed * 1664525u + 1013904223u;
    return ((s_seed >> 8) + 1) * (1.0f / 16777217.0f);
}
static float gauss(float sigma) {
    float u1 = frand01(), u2 = frand01();
    return sigma * sqrtf(-2.0f * logf(u1)) * cosf(6.2831853f * u2);
}

// Nằm yên `samples` mẫu (100 Hz, nhiễu gyro sigma = 0.09 dps) với bias dư (res_y, res_z) so với
// giá trị hiệu chuẩn. Chỉ gz -> dX và gy -> dY mới ra đầu ra con trỏ, nên bias dư PHẢI đặt trên
// hai trục này (gx = roll không điều khiển con trỏ; đặt ở gx thì "0 count" là vô nghĩa).
// Trả về tổng |dX|+|dY|, số mẫu bị khóa "đứng yên" và tổng |dX|+|dY| của 1000 mẫu cuối.
typedef struct {
    int total;
    int stationary;
    int last_1000;
} still_result_t;

static still_result_t run_still_with_residual(float res_y, float res_z, uint32_t seed, int samples) {
    s_seed = seed;
    motion_init(NULL);
    motion_setBias(-0.54f, -1.49f, 0.32f);

    still_result_t r = {0, 0, 0};
    for (int i = 0; i < samples; ++i) {
        imu_data_t imu = {
            .gx = -0.54f + gauss(0.09f),
            .gy = -1.49f + res_y + gauss(0.09f),
            .gz =  0.32f + res_z + gauss(0.09f),
            .ax = 0.0f,
            .ay = 0.0f,
            .az = 0.988f
        };
        mouse_output_t out = motion_process(&imu, false, 1000 + i * 10);
        int mag = abs(out.delta_x) + abs(out.delta_y);
        r.total += mag;
        if (out.is_stationary) r.stationary++;
        if (i >= samples - 1000) r.last_1000 += mag;
    }
    return r;
}

// N1: Nằm yên 1000 mẫu (10 s); bias thật = bias hiệu chuẩn + 0.1 dps trên gy VÀ gz (hai trục điều khiển)
void test_n1_still(void) {
    still_result_t r = run_still_with_residual(0.1f, 0.1f, 12345u, 1000);
    printf("      [N1 measurement] total |dX|+|dY| = %d, stationary = %d%% (limit <= 3, was 20 at gain 2.2)\n",
           r.total, r.stationary / 10);
    TEST_ASSERT(r.total <= 3, "N1: Stationary total |dX|+|dY| must be <= 3");
    TEST_PASS("N1: Stationary drift with 0.1 dps residual bias on gy+gz within limit (<= 3 at gain 0.3)");
}

// N2: Chậm 1.0 dps: 300 mẫu yên rồi 200 mẫu gz += 1.0
void test_n2_slow_1_0(void) {
    s_seed = 12345u;
    motion_init(NULL);
    motion_setBias(-0.54f, -1.49f, 0.32f);

    // 300 samples stationary
    for (int i = 0; i < 300; ++i) {
        imu_data_t imu = {
            .gx = -0.54f + gauss(0.09f),
            .gy = -1.49f + gauss(0.09f),
            .gz =  0.32f + gauss(0.09f),
            .ax = 0.0f,
            .ay = 0.0f,
            .az = 0.988f
        };
        motion_process(&imu, false, i * 10);
    }

    // 200 samples rotating at gz += 1.0 dps
    int sum_dx = 0;
    for (int i = 300; i < 500; ++i) {
        imu_data_t imu = {
            .gx = -0.54f + gauss(0.09f),
            .gy = -1.49f + gauss(0.09f),
            .gz =  0.32f - 1.0f + gauss(0.09f),
            .ax = 0.0f,
            .ay = 0.0f,
            .az = 0.988f
        };
        mouse_output_t out = motion_process(&imu, false, i * 10);
        sum_dx += (int)out.delta_x;
    }
    printf("      [N2 measurement] 200 samples dX = %d (expected ~43, limit [34, 52])\n", sum_dx);
    TEST_ASSERT(sum_dx >= 34 && sum_dx <= 52, "N2: total dX must be in [34, 52]");
    TEST_PASS("N2: Slow rotation 1.0 dps responsiveness verified");
}

// N3: Rất chậm 0.5 dps: như N2 nhưng gz += 0.5
void test_n3_very_slow_0_5(void) {
    s_seed = 12345u;
    motion_init(NULL);
    motion_setBias(-0.54f, -1.49f, 0.32f);

    // 300 samples stationary
    for (int i = 0; i < 300; ++i) {
        imu_data_t imu = {
            .gx = -0.54f + gauss(0.09f),
            .gy = -1.49f + gauss(0.09f),
            .gz =  0.32f + gauss(0.09f),
            .ax = 0.0f,
            .ay = 0.0f,
            .az = 0.988f
        };
        motion_process(&imu, false, i * 10);
    }

    // 200 samples rotating at gz += 0.5 dps
    int sum_dx = 0;
    for (int i = 300; i < 500; ++i) {
        imu_data_t imu = {
            .gx = -0.54f + gauss(0.09f),
            .gy = -1.49f + gauss(0.09f),
            .gz =  0.32f - 0.5f + gauss(0.09f),
            .ax = 0.0f,
            .ay = 0.0f,
            .az = 0.988f
        };
        mouse_output_t out = motion_process(&imu, false, i * 10);
        sum_dx += (int)out.delta_x;
    }
    printf("      [N3 measurement] 200 samples dX = %d (expected ~11, limit [7, 15])\n", sum_dx);
    TEST_ASSERT(sum_dx >= 7 && sum_dx <= 15, "N3: total dX must be in [7, 15]");
    TEST_PASS("N3: Very slow rotation 0.5 dps responsiveness verified");
}

// N4: Không bị bias nuốt: 300 mẫu yên rồi 1000 mẫu gz += 1.0
void test_n4_no_bias_absorption(void) {
    s_seed = 12345u;
    motion_init(NULL);
    motion_setBias(-0.54f, -1.49f, 0.32f);

    // 300 samples stationary
    for (int i = 0; i < 300; ++i) {
        imu_data_t imu = {
            .gx = -0.54f + gauss(0.09f),
            .gy = -1.49f + gauss(0.09f),
            .gz =  0.32f + gauss(0.09f),
            .ax = 0.0f,
            .ay = 0.0f,
            .az = 0.988f
        };
        motion_process(&imu, false, i * 10);
    }

    // 1000 samples rotating at gz += 1.0 dps
    int sum_dx_first100 = 0;
    int sum_dx_last100 = 0;
    for (int i = 300; i < 1300; ++i) {
        imu_data_t imu = {
            .gx = -0.54f + gauss(0.09f),
            .gy = -1.49f + gauss(0.09f),
            .gz =  0.32f - 1.0f + gauss(0.09f),
            .ax = 0.0f,
            .ay = 0.0f,
            .az = 0.988f
        };
        mouse_output_t out = motion_process(&imu, false, i * 10);
        if (i < 400) {
            sum_dx_first100 += (int)out.delta_x;
        } else if (i >= 1200) {
            sum_dx_last100 += (int)out.delta_x;
        }
    }
    printf("      [N4 measurement] first100 = %d, last100 = %d, ratio = %.2f%% (limit >= 90%%)\n",
           sum_dx_first100, sum_dx_last100, (sum_dx_first100 > 0 ? (float)sum_dx_last100 / (float)sum_dx_first100 * 100.0f : 0.0f));
    TEST_ASSERT(sum_dx_last100 >= (int)(0.90f * sum_dx_first100), "N4: last 100 samples dX must be >= 90% of first 100 samples");
    TEST_PASS("N4: Motion not absorbed by auto-zero bias tracking verified");
}

// N5: Tốc độ cao: 1 mẫu gz += 30.0, không nhiễu, không bias dư
void test_n5_high_speed(void) {
    s_seed = 12345u;
    motion_init(NULL);
    motion_setBias(-0.54f, -1.49f, 0.32f);

    imu_data_t imu = {
        .gx = -0.54f,
        .gy = -1.49f,
        .gz =  0.32f - 30.0f,
        .ax = 0.0f,
        .ay = 0.0f,
        .az = 0.988f
    };
    mouse_output_t out = motion_process(&imu, false, 10);
    printf("      [N5 measurement] delta_x = %d (expected 9, range [8, 10])\n", (int)out.delta_x);
    TEST_ASSERT(out.delta_x >= 8 && out.delta_x <= 10, "N5: delta_x must be in [8, 10]");
    TEST_PASS("N5: High speed rate scaling verified");
}

// N6: Bão hòa: 1 mẫu gz += 450.0 (0.3 * 450 = 135 > 127), không nhiễu, không bias dư
void test_n6_saturation(void) {
    s_seed = 12345u;
    motion_init(NULL);
    motion_setBias(-0.54f, -1.49f, 0.32f);

    imu_data_t imu = {
        .gx = -0.54f,
        .gy = -1.49f,
        .gz =  0.32f - 450.0f,
        .ax = 0.0f,
        .ay = 0.0f,
        .az = 0.988f
    };
    mouse_output_t out = motion_process(&imu, false, 10);
    printf("      [N6 measurement] delta_x = %d (expected 127)\n", (int)out.delta_x);
    TEST_ASSERT(out.delta_x == 127, "N6: delta_x must be 127");
    TEST_PASS("N6: Saturation clamp to +127 verified");
}

// N7: GIỚI HẠN ĐÃ BIẾT (KNOWN LIMITATION) — độ nhạy với bias dư khi nằm yên.
// Test này MÔ TẢ hành vi hiện tại, không phải chứng nhận chất lượng. Khóa đứng yên cần 30 mẫu liên
// tiếp có |omega| < 0.4 dps trên cả 3 trục; với nhiễu 0.09 dps/trục, bias dư 0.2-0.3 dps làm chuỗi
// này gãy -> không khóa -> không tự chỉnh bias -> con trỏ trôi mãi (không tự phục hồi).
// Số đo (3 hạt giống 11/12/13, mô phỏng, chưa đo trên board):
//   Gain 2.2: 0.1 dps: 1-3 count/10 s | 0.2: 27-45 | 0.3: 161-171 (khóa 0%, vẫn trôi ở 10 s cuối của 30 s)
//   Gain 0.3 (hiện tại, số đo 08/10): 0.1 dps: 0 | 0.2: <= 5 | 0.3: 21 count/10 s (~2 count/s)
// Nếu sau này chỉnh ngưỡng đứng yên (việc D) hoặc thêm hiệu chuẩn lại (việc C) thì test này sẽ FAIL
// đúng chủ đích: khi đó hãy cập nhật cận và changelog, đừng nới lỏng âm thầm.
void test_n7_residual_bias_limit(void) {
    static const uint32_t seeds[3] = {11u, 12u, 13u};

    // Bias dư đặt trên yaw (gz -> dX): 0.1 chịu được, 0.2 vùng chuyển tiếp, 0.3 vượt ngưỡng.
    int max_01 = 0, max_02 = 0, min_03 = 1 << 30, max_03 = 0, max_03_stat = 0, min_03_late = 1 << 30;
    for (int k = 0; k < 3; ++k) {
        still_result_t r1  = run_still_with_residual(0.0f, 0.1f, seeds[k], 1000);
        still_result_t r2  = run_still_with_residual(0.0f, 0.2f, seeds[k], 1000);
        still_result_t r3  = run_still_with_residual(0.0f, 0.3f, seeds[k], 1000);  // 10 s
        still_result_t r3l = run_still_with_residual(0.0f, 0.3f, seeds[k], 3000);  // 30 s, xem 10 s cuối
        if (r1.total > max_01) max_01 = r1.total;
        if (r2.total > max_02) max_02 = r2.total;
        if (r3.total < min_03) min_03 = r3.total;
        if (r3.total > max_03) max_03 = r3.total;
        if (r3.stationary > max_03_stat) max_03_stat = r3.stationary;
        if (r3l.last_1000 < min_03_late) min_03_late = r3l.last_1000;
    }
    printf("      [N7 measurement] 10 s yaw drift: 0.1 dps max = %d | 0.2 dps max = %d | "
           "0.3 dps = [%d, %d], stationary max = %d%%, last-10s-of-30s min = %d\n",
           max_01, max_02, min_03, max_03, max_03_stat / 10, min_03_late);

    TEST_ASSERT(max_01 <= 3,  "N7: residual 0.1 dps must stay <= 3 counts / 10 s");
    TEST_ASSERT(max_02 <= 14, "N7: residual 0.2 dps must stay <= 14 counts / 10 s");
    TEST_ASSERT(min_03 >= 14 && max_03 <= 41,
                "N7: residual 0.3 dps must drift in [14, 41] counts / 10 s (known limitation)");
    TEST_ASSERT(max_03_stat <= 50, "N7: residual 0.3 dps must keep stationary lock <= 5% of samples");
    TEST_ASSERT(min_03_late >= 14,
                "N7: residual 0.3 dps must NOT self-recover (still >= 14 counts in last 10 s of 30 s)");
    TEST_PASS("N7: [KNOWN LIMITATION] residual bias 0.3 dps on yaw -> ~21 counts/10 s (gain 0.3), no auto-recovery");
}

// N8: Hiệu chuẩn bias chỉ được chấp nhận khi board nằm yên (sự cố 08/10: đo lúc đang cầm -> bias lệch ~1 dps, không tự sửa được)
void test_n8_calibration_validation(void) {
    const float sd_rest[3]   = {0.10f, 0.11f, 0.09f};   // nhiễu thật khi nằm yên trên bàn (bench: ~0.09-0.135)
    const float ma_rest[3]   = {-0.61f, -1.50f, 0.36f};
    const float mb_rest[3]   = {-0.60f, -1.49f, 0.38f};
    TEST_ASSERT(motion_calibration_still(sd_rest, ma_rest, mb_rest), "N8: resting board must be ACCEPTED");

    const float sd_rest_bump[3] = {0.20f, 0.30f, 0.15f}; // bàn hơi rung nhưng vẫn nằm yên
    TEST_ASSERT(motion_calibration_still(sd_rest_bump, ma_rest, mb_rest), "N8: slightly noisy rest must be ACCEPTED");

    const float sd_held[3]   = {0.60f, 0.90f, 0.50f};   // đang cầm tay
    TEST_ASSERT(!motion_calibration_still(sd_held, ma_rest, mb_rest), "N8: held board (large jitter) must be REJECTED");

    const float ma_moved[3]  = {-0.60f, -1.50f, 0.40f};
    const float mb_moved[3]  = {-0.60f, -1.50f, -0.30f}; // nửa sau đã trôi 0.7 dps (vừa được đặt xuống/bị chạm)
    TEST_ASSERT(!motion_calibration_still(sd_rest, ma_moved, mb_moved), "N8: mean change between halves must be REJECTED");

    const float sd_nan[3]    = {NAN, 0.1f, 0.1f};
    TEST_ASSERT(!motion_calibration_still(sd_nan, ma_rest, mb_rest), "N8: NaN must be REJECTED");
    const float sd_frozen[3] = {0.0f, 0.0f, 0.0f};              // sự cố 17/10: cảm biến đơ trả toàn số 0
    const float m0[3] = {0.0f, 0.0f, 0.0f};
    TEST_ASSERT(!motion_calibration_still(sd_frozen, m0, m0), "N8: frozen sensor (sd = 0) must be REJECTED");
    TEST_PASS("N8: calibration window validation (rest accepted; held / moved / frozen / NaN rejected)");
}

// N9: Tự phục hồi bias chỉ khi board nằm yên TRÊN BỀ MẶT mà bias đang sai rõ rệt (không nuốt chuyển động tay)
void test_n9_surface_rest_self_heal(void) {
    const float gsd_rest[3] = {0.12f, 0.10f, 0.09f};
    const float asd_table[3] = {0.002f, 0.002f, 0.003f};      // gia tốc kế trên bàn (bench: ~2 mg)
    const float bias_bad[3] = {-1.30f, 0.56f, -0.66f};         // sự cố 08/10: Z đo sai ~1 dps
    const float mean_real[3] = {-1.30f, 0.56f, 0.37f};         // gyro thật khi nằm yên
    TEST_ASSERT(motion_surface_rest_bias_bad(gsd_rest, asd_table, 0.99f, mean_real, bias_bad),
                "N9: resting on table with a ~1 dps wrong bias must trigger self-heal");

    const float bias_ok[3] = {-1.30f, 0.56f, 0.36f};
    TEST_ASSERT(!motion_surface_rest_bias_bad(gsd_rest, asd_table, 0.99f, mean_real, bias_ok),
                "N9: correct bias must NOT trigger");

    const float asd_hand[3] = {0.030f, 0.025f, 0.040f};        // run tay: gia tốc kế dao động > 5 mg (đo thật: tay giữ vững nhất ~10 mg, bàn ~2 mg)
    TEST_ASSERT(!motion_surface_rest_bias_bad(gsd_rest, asd_hand, 0.99f, mean_real, bias_bad),
                "N9: hand-held (accel jitter) must NOT trigger, slow motion must not be swallowed");

    const float gsd_moving[3] = {0.8f, 0.5f, 0.6f};
    TEST_ASSERT(!motion_surface_rest_bias_bad(gsd_moving, asd_table, 0.99f, mean_real, bias_bad),
                "N9: noisy gyro must NOT trigger");
    TEST_ASSERT(!motion_surface_rest_bias_bad(gsd_rest, asd_table, 1.30f, mean_real, bias_bad),
                "N9: |a| far from 1 g (shake / free fall) must NOT trigger");
    const float mean_small[3] = {-1.30f, 0.56f, -0.40f};       // lệch 0.26 dps < 0.5: để bộ tự chỉnh chậm xử lý
    TEST_ASSERT(!motion_surface_rest_bias_bad(gsd_rest, asd_table, 0.99f, mean_small, bias_bad),
                "N9: small bias error (< 0.5 dps) must NOT trigger");
    TEST_PASS("N9: surface-rest self-heal predicate (triggers only on table + wrong bias)");
}

// N10: Chống dội phím (20 ms): nhấn sạch được nhận, nhiễu/dội ngắn bị bỏ qua, nhả cũng chống dội
void test_n10_button_debounce(void) {
    debounce_t d;
    debounce_init(&d, false);
    uint32_t t = 1000;

    // Không nhấn: giữ nguyên false
    for (int i = 0; i < 10; ++i) { TEST_ASSERT(!debounce_update(&d, false, t, 20), "N10: idle must stay released"); t += 2; }

    // Dội khi nhấn: 1,0,1,0,1 trong 6 ms rồi giữ nhấn
    const bool bounce[5] = {true, false, true, false, true};
    for (int i = 0; i < 5; ++i) { TEST_ASSERT(!debounce_update(&d, bounce[i], t, 20), "N10: bounce must not register"); t += 1; }
    for (int i = 0; i < 9; ++i) { TEST_ASSERT(!debounce_update(&d, true, t, 20), "N10: press must wait 20 ms"); t += 2; }  // ~18 ms
    t += 4;
    TEST_ASSERT(debounce_update(&d, true, t, 20), "N10: clean press held >= 20 ms must register");

    // Nhiễu ngắn 10 ms khi đang nhấn không làm nhả
    TEST_ASSERT(debounce_update(&d, false, t += 2, 20), "N10: glitch start keeps pressed");
    TEST_ASSERT(debounce_update(&d, false, t += 8, 20), "N10: 8 ms glitch keeps pressed");
    TEST_ASSERT(debounce_update(&d, true,  t += 2, 20), "N10: glitch ended, still pressed");
    for (int i = 0; i < 20; ++i) debounce_update(&d, true, t += 2, 20);
    TEST_ASSERT(d.stable, "N10: still pressed after glitch");

    // Nhả sạch >= 20 ms mới được nhận
    for (int i = 0; i < 9; ++i) { TEST_ASSERT(debounce_update(&d, false, t += 2, 20), "N10: release waits 20 ms"); }
    t += 4;
    TEST_ASSERT(!debounce_update(&d, false, t, 20), "N10: clean release must register");

    // Nhấn rất ngắn (5 ms) bị bỏ qua hoàn toàn
    debounce_t e; debounce_init(&e, false); uint32_t u = 5000;
    for (int i = 0; i < 3; ++i) { debounce_update(&e, true, u, 20); u += 2; }
    for (int i = 0; i < 20; ++i) { TEST_ASSERT(!debounce_update(&e, false, u, 20), "N10: 5 ms blip must never register"); u += 2; }
    TEST_PASS("N10: button debounce (clean press/release accepted; bounce and short glitches rejected)");
}

// N11: Click guard: xóa cú giật ngay trước khi nhấn, đóng băng khi giữ nút ngắn, cho kéo-thả khi giữ lâu
void test_n11_click_guard(void) {
    click_guard_t g;
    int8_t ox, oy;
    uint32_t t = 1000;

    // look-ahead 0: đi thẳng
    cg_init(&g, 0);
    cg_update(&g, false, 5, -3, t, &ox, &oy);
    TEST_ASSERT(ox == 5 && oy == -3, "N11: lookahead 0 must pass through");

    // look-ahead 4: xung 7 xuất hiện sau đúng 4 mẫu
    cg_init(&g, 4);
    int8_t outs[8];
    for (int i = 0; i < 8; ++i) { cg_update(&g, false, (i == 0) ? 7 : 0, 0, t += 10, &ox, &oy); outs[i] = ox; }
    TEST_ASSERT(outs[0] == 0 && outs[3] == 0 && outs[4] == 7 && outs[5] == 0, "N11: impulse must be delayed by exactly 4 samples");

    // Cú giật 3 mẫu trước khi nhấn bị xóa (chưa kịp gửi)
    cg_init(&g, 4);
    int sum_before = 0;
    for (int i = 0; i < 20; ++i) { cg_update(&g, false, 0, 0, t += 10, &ox, &oy); sum_before += abs(ox); }
    for (int i = 0; i < 3; ++i) { cg_update(&g, false, 20, 20, t += 10, &ox, &oy); sum_before += abs(ox); }   // jerk, still queued
    cg_update(&g, true, 0, 0, t += 10, &ox, &oy);                                                           // press detected
    int sum_after = 0;
    for (int i = 0; i < 10; ++i) { cg_update(&g, true, 0, 0, t += 10, &ox, &oy); sum_after += abs(ox) + abs(oy); }
    TEST_ASSERT(sum_before == 0, "N11: jerk must not have been sent before the press");
    TEST_ASSERT(sum_after == 0, "N11: queued jerk must be dropped when the press arrives");

    // Giữ nút ngắn (< 250 ms): mọi chuyển động bị bỏ
    cg_init(&g, 4);
    uint32_t t0 = t += 10;
    cg_update(&g, true, 0, 0, t0, &ox, &oy);
    int moved = 0;
    for (int i = 1; i < 20; ++i) { cg_update(&g, true, 10, 10, t0 + i * 10, &ox, &oy); moved += abs(ox) + abs(oy); }  // up to 190 ms
    TEST_ASSERT(moved == 0, "N11: motion must be frozen while a button is held < 250 ms");

    // Giữ lâu (kéo-thả): sau 250 ms chuyển động chạy lại
    int moved_late = 0;
    for (int i = 20; i < 50; ++i) { cg_update(&g, true, 10, 10, t0 + i * 10, &ox, &oy); moved_late += abs(ox); }
    TEST_ASSERT(moved_late > 0, "N11: a hold longer than 250 ms must let the cursor drag");

    // Nhả: chuyển động chạy lại ngay (sau độ trễ look-ahead), không bị kẹt
    cg_init(&g, 4);
    t0 = t += 10;
    cg_update(&g, true, 0, 0, t0, &ox, &oy);
    cg_update(&g, false, 0, 0, t0 + 50, &ox, &oy);
    int after_release = 0;
    for (int i = 0; i < 10; ++i) { cg_update(&g, false, 6, 0, t0 + 60 + i * 10, &ox, &oy); after_release += abs(ox); }
    TEST_ASSERT(after_release > 0, "N11: after release, motion must flow again");
    TEST_PASS("N11: click guard (delay, jerk removal, freeze while clicking, drag after 250 ms, resume on release)");
}

// N12: Chống dội bất đối xứng: nhấn nhận sau 5 ms, nhả sau 20 ms
void test_n12_debounce_asymmetric(void) {
    debounce_t d; debounce_init(&d, false); uint32_t t = 1000;
    debounce_update2(&d, true, t, 5, 20);
    TEST_ASSERT(!debounce_update2(&d, true, t += 3, 5, 20), "N12: press must wait 5 ms");
    TEST_ASSERT(debounce_update2(&d, true, t += 3, 5, 20), "N12: press accepted after 5 ms");
    debounce_update2(&d, false, t += 2, 5, 20);
    TEST_ASSERT(debounce_update2(&d, false, t += 10, 5, 20), "N12: release must still wait 20 ms");
    TEST_ASSERT(!debounce_update2(&d, false, t += 12, 5, 20), "N12: release accepted after 20 ms");
    TEST_PASS("N12: asymmetric debounce (press 5 ms, release 20 ms)");
}

// N13: Nút Mode: giữ = đóng băng, nhả = cân lại vị trí sau 150 ms ổn định; cử chỉ tắt thì không tạo Back/Forward
void test_n13_mode_button_recenter(void) {
    // (a) Cân lại sau thời gian ổn định
    motion_init(NULL);
    motion_setGesturesEnabled(false);
    motion_setRecenterSettleMs(150);
    motion_setBias(0.0f, 0.0f, 0.0f);
    imu_data_t flat   = { .gx = 0.0f, .gy = 0.0f, .gz = 0.0f,   .ax = 0.0f, .ay = 0.0f, .az = 1.0f };
    imu_data_t tilted = { .gx = 0.0f, .gy = 0.0f, .gz = 0.0f,   .ax = 0.5f, .ay = 0.0f, .az = 0.866f };
    imu_data_t rot    = { .gx = 0.0f, .gy = 0.0f, .gz = -20.0f, .ax = 0.5f, .ay = 0.0f, .az = 0.866f };
    uint32_t t = 1000;
    mouse_output_t o;
    for (int i = 0; i < 30; ++i) motion_process(&flat, false, t += 10);
    for (int i = 0; i < 20; ++i) {
        o = motion_process(&tilted, true, t += 10);
        TEST_ASSERT(!o.recentered, "N13: must not recenter while the Mode button is held");
        TEST_ASSERT(o.delta_x == 0 && o.delta_y == 0, "N13: cursor frozen while Mode is held");
    }
    const uint32_t t_rel = t += 10;
    int recenters = 0;
    uint32_t t_recentered = 0;
    int moved_after = 0;
    for (int i = 0; i <= 40; ++i) {
        uint32_t now = t_rel + (uint32_t)i * 10;
        o = motion_process(&rot, false, now);
        if (now - t_rel < 150) {
            TEST_ASSERT(!o.recentered, "N13: must not recenter before the 150 ms settle time");
            TEST_ASSERT(o.delta_x == 0 && o.delta_y == 0, "N13: cursor stays frozen during the settle time");
        }
        if (o.recentered) { recenters++; t_recentered = now; }
        if (now - t_rel > 160) moved_after += abs(o.delta_x);
    }
    TEST_ASSERT(recenters == 1, "N13: exactly one recenter after release");
    TEST_ASSERT(t_recentered - t_rel == 150, "N13: recenter happens exactly 150 ms after release");
    TEST_ASSERT(moved_after > 0, "N13: cursor moves again after the recenter");

    // (b) Cử chỉ tắt: giữ Mode + vuốt không tạo Back/Forward, và nhả vẫn cân lại ngay (settle = 0)
    motion_init(NULL);
    motion_setGesturesEnabled(false);
    motion_setRecenterSettleMs(0);
    motion_setBias(0.0f, 0.0f, 0.0f);
    t = 5000;
    for (int i = 0; i < 30; ++i) motion_process(&flat, false, t += 10);
    imu_data_t arm   = { .gx = 0.0f, .gy = 0.0f, .gz = 0.0f, .ax = 0.0f, .ay = 0.0f,  .az = 1.0f };
    imu_data_t peak  = { .gx = 0.0f, .gy = 10.0f, .gz = 10.0f, .ax = 0.0f, .ay = -1.5f, .az = 1.0f };
    imu_data_t back  = { .gx = 0.0f, .gy = 5.0f, .gz = 5.0f, .ax = 0.0f, .ay = 0.5f,  .az = 1.0f };
    o = motion_process(&arm, true, t += 50);
    TEST_ASSERT(o.gesture == GESTURE_EVENT_NONE, "N13: arming must not produce a gesture");
    o = motion_process(&peak, true, t += 50);
    TEST_ASSERT(o.gesture == GESTURE_EVENT_NONE, "N13: gestures disabled: flick peak ignored");
    o = motion_process(&back, true, t += 100);
    TEST_ASSERT(o.gesture == GESTURE_EVENT_NONE, "N13: gestures disabled: flick must NOT trigger Back/Forward");
    o = motion_process(&flat, false, t += 100);
    TEST_ASSERT(o.recentered, "N13: release without gesture recenters immediately when settle = 0");

    motion_setGesturesEnabled(true);          // restore defaults for any later test
    motion_setRecenterSettleMs(0);
    TEST_PASS("N13: Mode button (hold freezes, release recenters after 150 ms settle, gestures can be switched off)");
}

// N14: Giữ Mode + quay nhanh: trái = Back, phải = Forward (theo tốc độ xoay), cú quay về không kích hoạt cử chỉ ngược
void test_n14_yaw_flick(void) {
    motion_init(NULL);
    motion_setGesturesEnabled(true);
    motion_setYawFlickThresholdDps(150.0f);
    motion_setRecenterSettleMs(0);
    motion_setBias(0.0f, 0.0f, 0.0f);
    imu_data_t flat = { .gx = 0.0f, .gy = 0.0f, .gz = 0.0f, .ax = 0.0f, .ay = 0.0f, .az = 1.0f };
    uint32_t t = 1000;
    mouse_output_t o;
    for (int i = 0; i < 40; ++i) motion_process(&flat, false, t += 10);   // settle attitude

    // Quay chậm 60 dps (chỉnh tư thế): không kích hoạt
    imu_data_t slow = flat; slow.gz = 60.0f;
    for (int i = 0; i < 10; ++i) {
        o = motion_process(&slow, true, t += 10);
        TEST_ASSERT(o.gesture == GESTURE_EVENT_NONE, "N14: slow turn (60 dps) must not trigger a flick");
    }

    // Quay trái nhanh 220 dps (gz > 0 = quay trái) rồi quay về -200 dps trong 120 ms: chỉ ra MỘT cử chỉ: LEFT
    imu_data_t left = flat;  left.gz = 220.0f;
    imu_data_t back = flat;  back.gz = -200.0f;
    int lefts = 0, rights = 0;
    for (int i = 0; i < 4; ++i) { o = motion_process(&left, true, t += 10); lefts += (o.gesture == GESTURE_EVENT_FLICK_LEFT); rights += (o.gesture == GESTURE_EVENT_FLICK_RIGHT); }
    for (int i = 0; i < 3; ++i) { o = motion_process(&flat, true, t += 10); lefts += (o.gesture == GESTURE_EVENT_FLICK_LEFT); rights += (o.gesture == GESTURE_EVENT_FLICK_RIGHT); }
    for (int i = 0; i < 4; ++i) { o = motion_process(&back, true, t += 10); lefts += (o.gesture == GESTURE_EVENT_FLICK_LEFT); rights += (o.gesture == GESTURE_EVENT_FLICK_RIGHT); }
    TEST_ASSERT(lefts == 1, "N14: quick turn LEFT must give exactly one FLICK_LEFT (Back)");
    TEST_ASSERT(rights == 0, "N14: the return swing must NOT fire FLICK_RIGHT");

    // Nhả Mode: có cử chỉ nên KHÔNG cân lại; báo đỉnh quay ~ +220 dps
    for (int i = 0; i < 80; ++i) motion_process(&flat, true, t += 10);     // calm down, wait out the block time
    o = motion_process(&flat, false, t += 10);
    TEST_ASSERT(!o.recentered, "N14: a gesture during the hold must suppress the recenter");
    TEST_ASSERT(o.hold_peak_yaw_dps > 200.0f, "N14: hold peak yaw must be reported on release");

    // Quay phải nhanh (gz < 0) => FORWARD
    for (int i = 0; i < 5; ++i) motion_process(&flat, false, t += 10);
    imu_data_t right = flat; right.gz = -230.0f;
    int fwd = 0;
    motion_process(&flat, true, t += 10);
    for (int i = 0; i < 4; ++i) { o = motion_process(&right, true, t += 10); fwd += (o.gesture == GESTURE_EVENT_FLICK_RIGHT); }
    TEST_ASSERT(fwd == 1, "N14: quick turn RIGHT must give exactly one FLICK_RIGHT (Forward)");

    // Tắt ngưỡng (0): không kích hoạt
    motion_setYawFlickThresholdDps(0.0f);
    for (int i = 0; i < 100; ++i) motion_process(&flat, true, t += 10);
    int none = 0;
    for (int i = 0; i < 4; ++i) { o = motion_process(&left, true, t += 10); none += (o.gesture != GESTURE_EVENT_NONE); }
    TEST_ASSERT(none == 0, "N14: threshold 0 = yaw flick off");

    motion_setYawFlickThresholdDps(0.0f);   // restore defaults for any later test
    motion_setGesturesEnabled(true);
    TEST_PASS("N14: quick-turn flick (left = Back, right = Forward, slow turns and the return swing ignored)");
}

// ---------------------------------------------------------------------------------------------------------------
// N15..N19: user settings + text protocol (air_config.h)
// ---------------------------------------------------------------------------------------------------------------
static air_cfg_action_t run_cmd(air_config_t* c, const char* line, char* reply, size_t n) {
    return air_config_handle(c, line, reply, n);
}

void test_n15_config_defaults(void) {
    air_config_t c;
    air_config_defaults(&c);
    TEST_ASSERT(air_config_valid(&c), "N15: defaults must be valid");

    // The pipeline's own start-up gain must agree with the settings' default (two places hold the number).
    motion_init(NULL);
    float gx = 0, gy = 0;
    motion_getGain(&gx, &gy);
    TEST_ASSERT(gx == c.gain_x && gy == c.gain_y, "N15: pipeline default gain must equal AIR_CFG_GAIN_DEFAULT");

    char text[AIR_CFG_REPLY_MAX];
    air_config_format(&c, text, sizeof text);
    TEST_ASSERT(strcmp(text, "ver=5 gain_x=0.300 gain_y=0.300 flick_dps=150.0 flick_enable=1 click_guard_ms=40 recenter_ms=150 scroll_enable=1 scroll_sens=2.00 scroll_dead=2.5 scroll_invert=0 hscroll=0 scroll_ref=0 btn_left=1 btn_right=2 btn_mode=6 invert_x=0 invert_y=0") == 0,
                "N15: formatted defaults");

    char reply[AIR_CFG_REPLY_MAX];
    TEST_ASSERT(run_cmd(&c, "GET", reply, sizeof reply) == AIR_CFG_ACT_NONE, "N15: GET needs no action");
    TEST_ASSERT(strcmp(reply, "CFG ver=5 gain_x=0.300 gain_y=0.300 flick_dps=150.0 flick_enable=1 click_guard_ms=40 recenter_ms=150 scroll_enable=1 scroll_sens=2.00 scroll_dead=2.5 scroll_invert=0 hscroll=0 scroll_ref=0 btn_left=1 btn_right=2 btn_mode=6 invert_x=0 invert_y=0") == 0,
                "N15: GET reply");
    TEST_ASSERT(strlen(reply) + 32 < AIR_CFG_REPLY_MAX, "N15: longest reply must fit comfortably");
    TEST_PASS("N15: settings defaults valid, match the pipeline default gain, GET formats them");
}

void test_n16_config_set_ok(void) {
    air_config_t c;
    air_config_defaults(&c);
    char reply[AIR_CFG_REPLY_MAX];

    TEST_ASSERT(run_cmd(&c, "SET gain_x=0.45", reply, sizeof reply) == AIR_CFG_ACT_APPLY, "N16: SET asks to apply");
    TEST_ASSERT(strcmp(reply, "OK gain_x=0.450") == 0, "N16: single SET reply");
    TEST_ASSERT(c.gain_x == 0.45f && c.gain_y == 0.3f, "N16: only gain_x changes");

    run_cmd(&c, "set gain_y=1.5 flick_dps=180 flick_enable=0 recenter_ms=200", reply, sizeof reply);   // lower case + several keys
    TEST_ASSERT(strcmp(reply, "OK gain_y=1.500 flick_dps=180.0 flick_enable=0 recenter_ms=200") == 0, "N16: multi SET reply");
    TEST_ASSERT(c.gain_y == 1.5f && c.flick_dps == 180.0f && c.flick_enable == 0 && c.recenter_ms == 200, "N16: values stored");

    run_cmd(&c, "SET click_guard_ms=45", reply, sizeof reply);                 // rounds to the 10 ms step
    TEST_ASSERT(c.click_guard_ms == 50 && strcmp(reply, "OK click_guard_ms=50") == 0, "N16: click_guard_ms rounds to 10 ms");
    run_cmd(&c, "SET click_guard_ms=0", reply, sizeof reply);
    TEST_ASSERT(c.click_guard_ms == 0, "N16: click guard may be switched off");
    run_cmd(&c, "SET click_guard_ms=100 gain_x=0.02 gain_y=3 flick_dps=40 recenter_ms=50", reply, sizeof reply);   // exact limits
    TEST_ASSERT(c.click_guard_ms == 100 && c.gain_x == 0.02f && c.gain_y == 3.0f && c.flick_dps == 40.0f && c.recenter_ms == 50,
                "N16: range limits are inclusive");
    run_cmd(&c, "SET gain_x=0.5 gain_x=0.6", reply, sizeof reply);               // repeated key: last wins, listed once
    TEST_ASSERT(c.gain_x == 0.6f && strcmp(reply, "OK gain_x=0.600") == 0, "N16: repeated key, last wins");
    run_cmd(&c, "  SET\tgain_x=0.31\r\n", reply, sizeof reply);                   // stray white space / line end
    TEST_ASSERT(c.gain_x == 0.31f, "N16: tabs, spaces and CR/LF are tolerated");
    run_cmd(&c, "SET scroll_enable=0 scroll_sens=1.25 scroll_invert=1 hscroll=1", reply, sizeof reply);
    TEST_ASSERT(strcmp(reply, "OK scroll_enable=0 scroll_sens=1.25 scroll_invert=1 hscroll=1") == 0, "N16: scroll keys reply");
    TEST_ASSERT(c.scroll_enable == 0 && c.scroll_sens == 1.25f && c.scroll_invert == 1 && c.hscroll == 1, "N16: scroll keys stored");
    run_cmd(&c, "SET scroll_ref=1 scroll_dead=3.5", reply, sizeof reply);
    TEST_ASSERT(strcmp(reply, "OK scroll_dead=3.5 scroll_ref=1") == 0 && c.scroll_ref == 1 && c.scroll_dead == 3.5f, "N16: scroll_ref and scroll_dead");
    run_cmd(&c, "SET btn_left=3 btn_right=4 btn_mode=0 invert_x=1 invert_y=1", reply, sizeof reply);
    TEST_ASSERT(strcmp(reply, "OK btn_left=3 btn_right=4 btn_mode=0 invert_x=1 invert_y=1") == 0, "N16: button mapping reply");
    TEST_ASSERT(c.btn_left == AIR_BTN_MIDDLE && c.btn_right == AIR_BTN_BACK && c.btn_mode == AIR_BTN_NONE && c.invert_x == 1 && c.invert_y == 1, "N16: button mapping stored");
    TEST_ASSERT(air_config_valid(&c), "N16: config stays valid");

    TEST_ASSERT(run_cmd(&c, "DEFAULTS", reply, sizeof reply) == AIR_CFG_ACT_APPLY, "N16: DEFAULTS applies");
    air_config_t d; air_config_defaults(&d);
    TEST_ASSERT(air_config_equal(&c, &d) && strcmp(reply, "OK defaults") == 0, "N16: DEFAULTS restores everything");
    TEST_PASS("N16: SET accepts valid values (several keys, case, limits, 10 ms rounding), DEFAULTS restores");
}

void test_n17_config_set_rejects(void) {
    air_config_t c;
    air_config_defaults(&c);
    air_config_t before = c;
    char reply[AIR_CFG_REPLY_MAX];

    struct { const char* line; const char* expect; } bad[] = {
        { "SET gain_x=5",                  "ERR range gain_x" },
        { "SET gain_x=0.01",               "ERR range gain_x" },
        { "SET gain_y=-1",                 "ERR range gain_y" },
        { "SET flick_dps=39.9",            "ERR range flick_dps" },
        { "SET flick_dps=601",             "ERR range flick_dps" },
        { "SET flick_enable=2",            "ERR range flick_enable" },
        { "SET click_guard_ms=101",        "ERR range click_guard_ms" },
        { "SET click_guard_ms=-10",        "ERR range click_guard_ms" },
        { "SET recenter_ms=49",            "ERR range recenter_ms" },
        { "SET recenter_ms=501",           "ERR range recenter_ms" },
        { "SET gain_x=abc",                "ERR format gain_x" },
        { "SET gain_x=nan",                "ERR format gain_x" },
        { "SET gain_x=inf",                "ERR format gain_x" },
        { "SET gain_x=1e999",              "ERR format gain_x" },
        { "SET gain_x=0.3x",               "ERR format gain_x" },
        { "SET click_guard_ms=12.5",       "ERR format click_guard_ms" },
        { "SET recenter_ms=1e2",           "ERR format recenter_ms" },
        { "SET gain_x=",                   "ERR format" },
        { "SET gain_x",                    "ERR format" },
        { "SET =0.3",                      "ERR format" },
        { "SET",                           "ERR format" },
        { "SET scroll_sens=0.09",          "ERR range scroll_sens" },
        { "SET scroll_dead=-1",            "ERR range scroll_dead" },
        { "SET scroll_dead=15.1",          "ERR range scroll_dead" },
        { "SET scroll_sens=10.01",         "ERR range scroll_sens" },
        { "SET scroll_sens=x",             "ERR format scroll_sens" },
        { "SET scroll_enable=2",           "ERR range scroll_enable" },
        { "SET scroll_invert=-1",          "ERR range scroll_invert" },
        { "SET hscroll=0.5",               "ERR format hscroll" },
        { "SET scroll_ref=2",              "ERR range scroll_ref" },
        { "SET btn_left=7",                "ERR range btn_left" },
        { "SET btn_mode=-1",               "ERR range btn_mode" },
        { "SET btn_right=abc",             "ERR format btn_right" },
        { "SET btn_right=1.5",             "ERR format btn_right" },
        { "SET invert_x=2",                "ERR range invert_x" },
        { "SET invert_y=-1",               "ERR range invert_y" },
        { "SET volume=11",                 "ERR unknown-key volume" },
        { "SET GAIN_X=0.4",                "ERR unknown-key GAIN_X" },            // keys are lower case
        { "SET gain_y=0.5 gain_x=9",       "ERR range gain_x" },                  // good value + bad value
        { "SET gain_x=0.5 volume=1",       "ERR unknown-key volume" },
        { "FORMAT",                        "ERR unknown-cmd" },
        { "",                              "ERR empty" },
        { "   \r\n",                       "ERR empty" },
    };
    for (size_t i = 0; i < sizeof bad / sizeof bad[0]; ++i) {
        air_cfg_action_t a = run_cmd(&c, bad[i].line, reply, sizeof reply);
        if (strcmp(reply, bad[i].expect) != 0) {
            fprintf(stderr, "line \"%s\": expected \"%s\", got \"%s\"\n", bad[i].line, bad[i].expect, reply);
            TEST_ASSERT(false, "N17: wrong error reply");
        }
        TEST_ASSERT(a == AIR_CFG_ACT_NONE, "N17: a rejected line must ask for no action");
        TEST_ASSERT(air_config_equal(&c, &before), "N17: a rejected line must change NOTHING (all-or-nothing)");
    }

    // Too long / too many tokens
    char longline[500];
    memset(longline, 'a', sizeof longline - 1); longline[sizeof longline - 1] = '\0';
    run_cmd(&c, longline, reply, sizeof reply);
    TEST_ASSERT(strcmp(reply, "ERR too-long") == 0, "N17: over-long line");
    run_cmd(&c, "SET a=1 b=1 c=1 d=1 e=1 f=1 g=1 h=1 i=1 j=1 k=1 l=1 m=1 n=1 o=1 p=1 q=1 r=1 s=1 t=1 u=1 v=1 w=1 x=1", reply, sizeof reply);
    TEST_ASSERT(strcmp(reply, "ERR too-many") == 0, "N17: too many tokens");
    char longtok[100];
    strcpy(longtok, "SET gain_x=0.");
    memset(longtok + strlen(longtok), '3', 60); longtok[13 + 60] = '\0';
    run_cmd(&c, longtok, reply, sizeof reply);
    TEST_ASSERT(strcmp(reply, "ERR format") == 0, "N17: over-long token");
    TEST_ASSERT(air_config_equal(&c, &before), "N17: nothing changed by the oversize lines");
    TEST_PASS("N17: SET rejects out-of-range, malformed, NaN/inf, unknown keys; a bad line changes nothing");
}

void test_n18_config_commands_and_buffers(void) {
    air_config_t c;
    air_config_defaults(&c);
    char reply[AIR_CFG_REPLY_MAX];
    TEST_ASSERT(run_cmd(&c, "SAVE", reply, sizeof reply) == AIR_CFG_ACT_SAVE && strcmp(reply, "OK saved") == 0, "N18: SAVE");
    TEST_ASSERT(run_cmd(&c, "save", reply, sizeof reply) == AIR_CFG_ACT_SAVE, "N18: commands are case-insensitive");
    TEST_ASSERT(run_cmd(&c, "CAL", reply, sizeof reply) == AIR_CFG_ACT_CALIBRATE && strcmp(reply, "OK calibrated") == 0, "N18: CAL");

    // Small reply buffers are never overrun and are always null-terminated
    for (size_t n = 1; n <= 40; ++n) {
        char small[41];
        memset(small, 'Z', sizeof small);
        run_cmd(&c, "SET gain_x=0.45 gain_y=0.5 flick_dps=180 flick_enable=0 click_guard_ms=30 recenter_ms=200", small, n);
        TEST_ASSERT(memchr(small, '\0', n) != NULL, "N18: reply must be null-terminated inside the buffer");
        TEST_ASSERT(small[n] == 'Z' || n == 41, "N18: nothing may be written beyond the buffer");
        run_cmd(&c, "GET", small, n);
        TEST_ASSERT(memchr(small, '\0', n) != NULL, "N18: GET reply must be null-terminated");
    }
    TEST_ASSERT(run_cmd(&c, "GET", NULL, 0) == AIR_CFG_ACT_NONE, "N18: NULL reply buffer is tolerated");
    TEST_ASSERT(run_cmd(NULL, "GET", reply, sizeof reply) == AIR_CFG_ACT_NONE && strcmp(reply, "ERR internal") == 0, "N18: NULL config");

    // The full SET reply with all six keys fits
    run_cmd(&c, "SET gain_x=3 gain_y=3 flick_dps=600 flick_enable=1 click_guard_ms=100 recenter_ms=500 scroll_enable=1 scroll_sens=10 scroll_dead=15 scroll_invert=1 hscroll=1 scroll_ref=1 btn_left=3 btn_right=4 btn_mode=5 invert_x=1 invert_y=1", reply, sizeof reply);
    TEST_ASSERT(strcmp(reply, "OK gain_x=3.000 gain_y=3.000 flick_dps=600.0 flick_enable=1 click_guard_ms=100 recenter_ms=500 scroll_enable=1 scroll_sens=10.00 scroll_dead=15.0 scroll_invert=1 hscroll=1 scroll_ref=1 btn_left=3 btn_right=4 btn_mode=5 invert_x=1 invert_y=1") == 0,
                "N18: widest SET reply");
    TEST_PASS("N18: SAVE / CAL actions, case-insensitive commands, small or NULL reply buffers are safe");
}

void test_n19_config_validity_and_fuzz(void) {
    air_config_t c;
    air_config_defaults(&c);
    air_config_t x = c;
    x.gain_x = NAN;            TEST_ASSERT(!air_config_valid(&x), "N19: NaN gain is invalid");
    x = c; x.gain_y = 0.0f;    TEST_ASSERT(!air_config_valid(&x), "N19: zero gain is invalid");
    x = c; x.flick_enable = 2; TEST_ASSERT(!air_config_valid(&x), "N19: flick_enable 2 is invalid");
    x = c; x.click_guard_ms = 45; TEST_ASSERT(!air_config_valid(&x), "N19: click_guard_ms must be a multiple of 10");
    x = c; x.recenter_ms = 0;  TEST_ASSERT(!air_config_valid(&x), "N19: recenter 0 is invalid");
    x = c; x.scroll_sens = 0.0f; TEST_ASSERT(!air_config_valid(&x), "N19: scroll_sens 0 is invalid");
    x = c; x.scroll_sens = NAN;  TEST_ASSERT(!air_config_valid(&x), "N19: scroll_sens NaN is invalid");
    x = c; x.scroll_dead = -1.0f; TEST_ASSERT(!air_config_valid(&x), "N19: negative dead zone is invalid");
    x = c; x.btn_mode = AIR_BTN_COUNT; TEST_ASSERT(!air_config_valid(&x), "N19: unknown button action is invalid");
    x = c; x.invert_y = 2;       TEST_ASSERT(!air_config_valid(&x), "N19: invert_y 2 is invalid");
    x = c; x.scroll_ref = 2;      TEST_ASSERT(!air_config_valid(&x), "N19: scroll_ref 2 is invalid");
    x = c; x.hscroll = 2;        TEST_ASSERT(!air_config_valid(&x), "N19: hscroll 2 is invalid");
    TEST_ASSERT(!air_config_valid(NULL), "N19: NULL is invalid");

    // Random garbage lines: never crash, and the config is ALWAYS valid afterwards.
    static const char alphabet[] = "SETGAINXYflickdps_enablecguremo=.0123456789-+e \t@ABCDEFxyz";
    uint32_t seed = 12345u;
    char reply[AIR_CFG_REPLY_MAX];
    for (int i = 0; i < 40000; ++i) {
        char line[80];
        seed = seed * 1664525u + 1013904223u;
        int len = (int)((seed >> 24) % 70);
        for (int k = 0; k < len; ++k) {
            seed = seed * 1664525u + 1013904223u;
            line[k] = alphabet[(seed >> 16) % (sizeof alphabet - 1)];
        }
        line[len] = '\0';
        run_cmd(&c, line, reply, sizeof reply);
        TEST_ASSERT(air_config_valid(&c), "N19: random input must never leave an invalid config");
        TEST_ASSERT(strlen(reply) < AIR_CFG_REPLY_MAX, "N19: reply bounded");
    }
    // Structured fuzz: random valid-looking SET lines with random numbers
    int accepted = 0;
    for (int i = 0; i < 20000; ++i) {
        char line[120];
        static const char* keys[] = { "gain_x", "gain_y", "flick_dps", "flick_enable", "click_guard_ms", "recenter_ms", "scroll_enable", "scroll_sens", "scroll_dead", "scroll_invert", "hscroll", "scroll_ref", "btn_left", "btn_right", "btn_mode", "invert_x", "invert_y" };
        seed = seed * 1664525u + 1013904223u;
        int k = (int)((seed >> 16) % 17);
        seed = seed * 1664525u + 1013904223u;
        double v = ((double)(seed >> 8) / 16777216.0) * 1400.0 - 100.0;      // -100 .. 1300
        snprintf(line, sizeof line, "SET %s=%.4f", keys[k], v);
        if (run_cmd(&c, line, reply, sizeof reply) == AIR_CFG_ACT_APPLY) ++accepted;
        TEST_ASSERT(air_config_valid(&c), "N19: random numbers must never leave an invalid config");
    }
    TEST_ASSERT(accepted > 0, "N19: the fuzz must have hit some accepted lines too (sanity)");
    TEST_PASS("N19: invalid configs detected; 60 000 random lines never crash or leave the config invalid");
}

// ---------------------------------------------------------------------------------------------------------------
// N20..N22: scroll mode (scroll_mode.h): double-tap Mode, hold the second press, tilt = wheel
// ---------------------------------------------------------------------------------------------------------------
typedef struct { int started; int ended; int firsts; bool active_seen; bool active_last; } sm_stats_t;

// Hold the button `down` for `ms` (10 ms ticks), advance the clock, collect what the state machine reported.
static void sm_run(scroll_mode_t* s, uint32_t* t, bool down, int ms, sm_stats_t* st, bool enabled = true) {
    for (int i = 0; i < ms / 10; ++i) {
        *t += 10;
        scroll_mode_out_t o = sm_update(s, down, *t, enabled);
        st->started += o.started;
        st->ended += o.ended;
        st->firsts += o.first_press;
        if (o.active) st->active_seen = true;
        st->active_last = o.active;
    }
}

void test_n20_scroll_state_machine(void) {
    scroll_mode_t s; uint32_t t; sm_stats_t st;
    #define SM_RESET() do { sm_init(&s); t = 1000; memset(&st, 0, sizeof st); } while (0)

    // Double-tap, hold the second press: scroll for as long as it is held
    SM_RESET();
    sm_run(&s, &t, true, 100, &st);  sm_run(&s, &t, false, 150, &st);
    TEST_ASSERT(!st.active_seen && st.started == 0, "N20: the first tap alone must not scroll");
    sm_run(&s, &t, true, 500, &st);
    TEST_ASSERT(st.started == 1 && st.active_last, "N20: the second press starts scroll mode (exactly once) and keeps it on");
    sm_run(&s, &t, false, 100, &st);
    TEST_ASSERT(st.ended == 1 && !st.active_last, "N20: releasing the second press ends scroll mode (exactly once)");
    TEST_ASSERT(st.firsts == 1, "N20: only the FIRST press of the double-tap is flagged as first_press");

    // Plain hold = clutch only
    SM_RESET();
    sm_run(&s, &t, true, 600, &st);  sm_run(&s, &t, false, 500, &st);
    TEST_ASSERT(!st.active_seen, "N20: a single long hold must never scroll");

    // Gap too long (360 ms > 350): the second press is a new first press
    SM_RESET();
    sm_run(&s, &t, true, 100, &st);  sm_run(&s, &t, false, 360, &st);  sm_run(&s, &t, true, 500, &st);
    TEST_ASSERT(!st.active_seen, "N20: a second press after more than 350 ms must not scroll");
    TEST_ASSERT(st.firsts == 2, "N20: a too-late second press counts as a new first press");
    // ... and 350 ms is still in time
    SM_RESET();
    sm_run(&s, &t, true, 100, &st);  sm_run(&s, &t, false, 350, &st);  sm_run(&s, &t, true, 300, &st);
    TEST_ASSERT(st.started == 1, "N20: a second press after exactly 350 ms still scrolls");

    // First press too long (260 ms > 250) is not a tap; exactly 250 ms is
    SM_RESET();
    sm_run(&s, &t, true, 260, &st);  sm_run(&s, &t, false, 100, &st);  sm_run(&s, &t, true, 500, &st);
    TEST_ASSERT(!st.active_seen, "N20: a first press longer than 250 ms is not a tap");
    SM_RESET();
    sm_run(&s, &t, true, 250, &st);  sm_run(&s, &t, false, 100, &st);  sm_run(&s, &t, true, 300, &st);
    TEST_ASSERT(st.started == 1, "N20: a first press of exactly 250 ms is still a tap");

    // After a scroll the next press is a NEW first press (no chained scrolling)
    SM_RESET();
    sm_run(&s, &t, true, 100, &st);  sm_run(&s, &t, false, 100, &st);  sm_run(&s, &t, true, 60, &st);   // short scroll
    sm_run(&s, &t, false, 100, &st);
    TEST_ASSERT(st.started == 1 && st.ended == 1, "N20: a very short second press still scrolls briefly");
    sm_run(&s, &t, true, 500, &st);
    TEST_ASSERT(st.started == 1 && !st.active_last, "N20: the press right after a scroll must not start another scroll");
    sm_run(&s, &t, false, 100, &st);

    // Disabled: never active; switching off in the middle of a scroll reports 'ended'
    SM_RESET();
    sm_run(&s, &t, true, 100, &st, false);  sm_run(&s, &t, false, 100, &st, false);  sm_run(&s, &t, true, 500, &st, false);
    TEST_ASSERT(!st.active_seen && st.started == 0, "N20: disabled = no scroll mode");
    SM_RESET();
    sm_run(&s, &t, true, 100, &st);  sm_run(&s, &t, false, 100, &st);  sm_run(&s, &t, true, 200, &st);
    TEST_ASSERT(st.active_last, "N20: scroll on before disabling");
    sm_run(&s, &t, true, 20, &st, false);
    TEST_ASSERT(!st.active_last && st.ended == 1, "N20: disabling during a scroll ends it");
    #undef SM_RESET
    TEST_PASS("N20: scroll mode state machine (double-tap + hold, timing limits 250/350 ms, no chaining, enable switch)");
}

// Gravity (body frame, pipeline axes X = backward, Y = right, Z = up) for a board tilted `pitch_up` degrees nose up and
// `roll_right` degrees right side down.
static void gv_for(float pitch_up, float roll_right, float* vx, float* vy) {
    *vx = -sinf(pitch_up * 0.01745329f);
    *vy = -sinf(roll_right * 0.01745329f);
}

void test_n21_scroll_tilt(void) {
    scroll_tilt_t st;
    uint32_t t = 1000;
    int8_t w = 0, h = 0;
    int sw = 0, sh = 0;

    // Run `ticks` ticks (10 ms) at a fixed tilt and add up the notches.
    auto run = [&](int ticks, float pitch, float roll, float sens, float dead, bool inv, bool hs) {
        float vx, vy;
        gv_for(pitch, roll, &vx, &vy);
        sw = 0; sh = 0;
        for (int i = 0; i < ticks; ++i) {
            t += 10;
            st_update(&st, vx, vy, t, sens, dead, inv, hs, &w, &h);
            sw += w; sh += h;
        }
    };
    #define ST_BEGIN() do { st_start(&st, t); run(40, 0.0f, 0.0f, 1.0f, 4.0f, false, false); TEST_ASSERT(sw == 0 && sh == 0, "N21: nothing scrolls while arming"); } while (0)

    // Hold 15 degrees nose up for 2 s: (15 - 4) deg * 1 notch/s/deg * 2 s = 22 notches, and it KEEPS scrolling while held
    ST_BEGIN();
    run(100, 15.0f, 0.0f, 1.0f, 4.0f, false, false);
    int first = sw;
    run(100, 15.0f, 0.0f, 1.0f, 4.0f, false, false);
    TEST_ASSERT(first >= 10 && first <= 12 && sw >= 10 && sw <= 12, "N21: holding the tilt keeps scrolling at a steady speed (about 11 notches per second)");
    run(100, 0.0f, 0.0f, 1.0f, 4.0f, false, false);
    TEST_ASSERT(sw == 0, "N21: back in the starting pose = no scrolling");

    // Inside the dead zone nothing happens
    ST_BEGIN();
    run(300, 3.5f, 0.0f, 1.0f, 4.0f, false, false);
    TEST_ASSERT(sw == 0, "N21: a tilt inside the dead zone (3.5 deg < 4) does not scroll");
    run(300, -3.5f, 0.0f, 1.0f, 4.0f, false, false);
    TEST_ASSERT(sw == 0, "N21: the dead zone applies to both directions");

    // Nose down = negative; invert flips it; the speed scales with sens and the dead zone is adjustable
    ST_BEGIN();
    run(200, -15.0f, 0.0f, 1.0f, 4.0f, false, false);
    TEST_ASSERT(sw >= -23 && sw <= -21, "N21: nose down scrolls the other way (about -22 per 2 s)");
    ST_BEGIN();
    run(200, -15.0f, 0.0f, 1.0f, 4.0f, true, false);
    TEST_ASSERT(sw >= 21 && sw <= 23, "N21: invert flips the direction");
    ST_BEGIN();
    run(200, 15.0f, 0.0f, 2.0f, 4.0f, false, false);
    TEST_ASSERT(sw >= 43 && sw <= 45, "N21: sens 2 = twice as fast");
    ST_BEGIN();
    run(200, 15.0f, 0.0f, 1.0f, 0.0f, false, false);
    TEST_ASSERT(sw >= 29 && sw <= 31, "N21: dead zone 0 = 15 deg gives 30 notches in 2 s");

    // A slow scroll is not lost: 5 deg (1 deg beyond the dead zone) = 1 notch per second, so 2 s give 2 notches (fractions carried)
    ST_BEGIN();
    run(200, 5.0f, 0.0f, 1.0f, 4.0f, false, false);
    TEST_ASSERT(sw >= 1 && sw <= 2, "N21: a slow scroll still produces its notches");

    // The thumb jerk right after the second press is absorbed: the starting pose is whatever the board has after 150 ms
    st_start(&st, t);
    run(3, 0.0f, 0.0f, 1.0f, 4.0f, false, false);      // press
    run(20, 10.0f, 0.0f, 1.0f, 4.0f, false, false);    // jerked to 10 deg nose up and stays there
    TEST_ASSERT(sw == 0, "N21: the jerk of the press must not scroll");
    run(100, 10.0f, 0.0f, 1.0f, 4.0f, false, false);
    TEST_ASSERT(sw == 0, "N21: the pose after the jerk is the new neutral");
    run(100, 25.0f, 0.0f, 1.0f, 4.0f, false, false);
    TEST_ASSERT(sw >= 10 && sw <= 12, "N21: 15 deg beyond that neutral scrolls about 11 per second");

    // Sideways scroll by rolling the board, only when hscroll is on
    ST_BEGIN();
    run(200, 0.0f, 15.0f, 1.0f, 4.0f, false, false);
    TEST_ASSERT(sw == 0 && sh == 0, "N21: hscroll off = rolling does nothing");
    ST_BEGIN();
    run(200, 0.0f, 15.0f, 1.0f, 4.0f, false, true);
    TEST_ASSERT(sw == 0 && sh >= 21 && sh <= 23, "N21: right side down scrolls right when hscroll is on");
    ST_BEGIN();
    run(200, 0.0f, -15.0f, 1.0f, 4.0f, false, true);
    TEST_ASSERT(sh <= -21 && sh >= -23, "N21: right side up scrolls left");

    // Robustness: huge pauses, impossible gravity values, NaN
    ST_BEGIN();
    t += 5000;
    st_update(&st, -0.7071f, 0.0f, t, 10.0f, 0.0f, false, false, &w, &h);      // 45 deg after a 5 s pause
    TEST_ASSERT(w >= 0 && w <= 24, "N21: a long pause cannot produce a burst of notches (dt is limited)");
    st_update(&st, NAN, NAN, t + 10, 1.0f, 4.0f, false, true, &w, &h);
    TEST_ASSERT(w == 0 && h == 0, "N21: NaN gravity gives no scrolling");
    st_update(&st, -5.0f, 7.0f, t + 20, 1.0f, 4.0f, false, true, &w, &h);      // |component| > 1 is clamped, no crash
    #undef ST_BEGIN
    TEST_PASS("N21: tilt-angle scroll (hold = keep scrolling, dead zone, direction, invert, sens, jerk absorbed, sideways, robust)");
}

void test_n22_scroll_with_pipeline(void) {
    motion_init(NULL);
    motion_setGesturesEnabled(true);
    motion_setYawFlickThresholdDps(150.0f);
    motion_setRecenterSettleMs(150);
    motion_setBias(0.0f, 0.0f, 0.0f);
    imu_data_t flat = { .gx = 0.0f, .gy = 0.0f, .gz = 0.0f, .ax = 0.0f, .ay = 0.0f, .az = 1.0f };
    uint32_t t = 1000;
    for (int i = 0; i < 40; ++i) motion_process(&flat, false, t += 10);   // settle the attitude

    scroll_ctrl_t sc; sc_init(&sc);
    float theta = 0.0f;                    // true nose-up angle in degrees (the simulated hand)
    int wheel_total = 0, gestures = 0;

    // One tick the way the firmware does it (app_scroll.cpp + firmware.ino). The accelerometer reports gravity
    // consistent with theta (a real tilt), the gyro reports the rotation rate gy (+ = nose up) and a yaw rate gz.
    auto tick = [&](bool mode_down, float rate_dps, float gz) {
        theta += rate_dps * 0.01f;
        imu_data_t imu = { .gx = 0.0f, .gy = rate_dps, .gz = gz, .ax = -sinf(theta * 0.01745329f), .ay = 0.0f, .az = cosf(theta * 0.01745329f) };
        t += 10;
        float vx, vy, vz;
        motion_getBodyGravity(&vx, &vy, &vz);
        scroll_mode_out_t so = sc_begin(&sc, mode_down, t, true, vx, vy, true);
        if (so.ended) motion_scheduleRecenter(t);                 // BEFORE the pipeline runs, so this very tick is frozen too
        mouse_output_t o = motion_process(&imu, mode_down && !so.active, t);
        if (so.active) {
            motion_getBodyGravity(&vx, &vy, &vz);
            int8_t w = 0, h = 0;
            sc_wheel(&sc, vx, vy, t, 1.0f, 4.0f, false, false, &w, &h);
            wheel_total += w;
        }
        if (o.gesture != GESTURE_EVENT_NONE) gestures++;
        return o;
    };

    // The hand is calm for 1 s (the comfortable pose), then: tap (100 ms), release (50 ms), press again and hold
    for (int i = 0; i < 100; ++i) tick(false, 0.0f, 0.0f);
    bool frozen_tap = true;
    for (int i = 0; i < 10; ++i) { mouse_output_t o = tick(true, 0.0f, 0.0f); frozen_tap = frozen_tap && o.is_clutch_active && o.delta_y == 0; }
    TEST_ASSERT(frozen_tap, "N22: the first tap still acts as a clutch (cursor frozen)");
    for (int i = 0; i < 5; ++i) tick(false, 0.0f, 0.0f);

    // Second press held: a quiet moment, then tilt up 15 degrees (30 deg/s for 0.5 s) ...
    for (int i = 0; i < 20; ++i) tick(true, 0.0f, 0.0f);
    TEST_ASSERT(wheel_total == 0, "N22: no scrolling right after the press (quiet time)");
    for (int i = 0; i < 50; ++i) tick(true, 30.0f, 0.0f);
    // ... and now keep the board STILL at 15 degrees for 2 s (with one quick yaw turn in the middle): it keeps scrolling
    int before_hold = wheel_total;
    for (int i = 0; i < 200; ++i) tick(true, 0.0f, (i >= 100 && i < 105) ? -250.0f : 0.0f);
    int in_hold = wheel_total - before_hold;
    TEST_ASSERT(in_hold >= 18 && in_hold <= 26, "N22: holding a 15 degree tilt for 2 s keeps scrolling (about 22 notches), page scrolls up");
    TEST_ASSERT(gestures == 0, "N22: no Back/Forward flick during scroll mode");

    // Tilt back to the comfortable pose: the scrolling stops
    for (int i = 0; i < 50; ++i) tick(true, -30.0f, 0.0f);
    for (int i = 0; i < 20; ++i) tick(true, 0.0f, 0.0f);
    int back_at_zero = wheel_total;
    for (int i = 0; i < 100; ++i) tick(true, 0.0f, 0.0f);
    TEST_ASSERT(wheel_total == back_at_zero, "N22: back in the comfortable pose the scrolling stops");

    // Release: scroll ends, the cursor stays frozen for the settle time, then it re-centers exactly once
    int recentered = 0, moved_before_due = 0;
    for (int i = 0; i < 30; ++i) {
        mouse_output_t o = tick(false, 0.0f, 0.0f);
        recentered += o.recentered;
        if (i < 13 && (o.delta_x != 0 || o.delta_y != 0)) moved_before_due++;
    }
    TEST_ASSERT(moved_before_due == 0, "N22: the cursor stays frozen until the recenter is done after a scroll");
    TEST_ASSERT(recentered == 1, "N22: exactly one recenter after the scroll ends");
    TEST_PASS("N22: scroll with the real pipeline (clutch tap, hold tilt = keep scrolling, no flick, stops at neutral, recenter after)");
}

// The hand drifts while pressing the button twice. Reference = pose BEFORE the double-tap: the drift scrolls (TV-remote
// feel, the comfortable pose is the centre); reference = pose at the press: the drifted pose is the centre.
void test_n23_scroll_reference_before_tap(void) {
    for (int ref_before = 1; ref_before >= 0; --ref_before) {
        scroll_ctrl_t c; sc_init(&c);
        uint32_t t = 1000;
        float pitch = 0.0f;
        int total = 0, first300 = 0, first100 = 0, late300 = 0, since_start = -1;
        auto tick = [&](bool down) {
            float vx, vy;
            gv_for(pitch, 0.0f, &vx, &vy);
            t += 10;
            scroll_mode_out_t o = sc_begin(&c, down, t, true, vx, vy, ref_before != 0);
            if (o.started) since_start = 0;
            if (o.active) {
                int8_t w = 0, h = 0;
                sc_wheel(&c, vx, vy, t, 2.0f, 2.5f, false, false, &w, &h);
                total += w;
                if (since_start < 10) first100 += w;
                if (since_start < 30) first300 += w;
                if (since_start >= 100) late300 += w;
                ++since_start;
            }
            return o;
        };
        for (int i = 0; i < 100; ++i) tick(false);                 // calm at 0 degrees (the comfortable pose)
        for (int i = 0; i < 10; ++i) { tick(true); if (i == 3) pitch = 8.0f; }   // first press: the hand drifts to 8 degrees nose up
        for (int i = 0; i < 15; ++i) tick(false);                  // release, still at 8
        for (int i = 0; i < 200; ++i) tick(true);                  // second press, hold still at 8 degrees for 2 s
        if (ref_before) {
            TEST_ASSERT(c.have_pre && fabsf(c.pre_pitch) < 0.5f, "N23: the reference is the pose from before the first press (0 deg)");
            TEST_ASSERT(first100 == 0, "N23: no output in the quiet time right after the press");
            TEST_ASSERT(first300 <= 2, "N23: the first 300 ms are soft (ramped), no sudden burst");
            TEST_ASSERT(late300 >= 10 && late300 <= 12, "N23: later, 8 deg away from the comfortable pose scrolls at (8-2.5)*2 = 11 notches/s (1 s = about 11)");
            TEST_ASSERT(total >= 16 && total <= 24, "N23: about 20 notches in the 2 s hold");
        } else {
            TEST_ASSERT(total == 0, "N23: with the reference at the press, the drifted pose is the centre: no scrolling");
        }
    }

    // A move just BEFORE the press (anticipation, last 150 ms) must not become the reference
    scroll_ctrl_t c; sc_init(&c);
    uint32_t t = 1000;
    float vx, vy;
    for (int i = 0; i < 100; ++i) { gv_for(0.0f, 0.0f, &vx, &vy); sc_begin(&c, false, t += 10, true, vx, vy, true); }
    for (int i = 0; i < 10; ++i) { gv_for(6.0f, 0.0f, &vx, &vy); sc_begin(&c, false, t += 10, true, vx, vy, true); }   // 100 ms at 6 deg
    gv_for(6.0f, 0.0f, &vx, &vy);
    scroll_mode_out_t o = sc_begin(&c, true, t += 10, true, vx, vy, true);
    TEST_ASSERT(o.first_press, "N23: first press flagged");
    TEST_ASSERT(fabsf(c.pre_pitch) < 0.5f, "N23: a move in the last 150 ms before the press is not part of the comfortable pose");

    // Pose history: shorter than asked still works; empty does not
    pose_hist_t hist; ph_init(&hist);
    float p = 0, r = 0;
    TEST_ASSERT(!ph_get(&hist, 25, 10, &p, &r), "N23: empty history gives nothing");
    gv_for(7.0f, -3.0f, &vx, &vy);
    ph_push(&hist, vx, vy);
    TEST_ASSERT(ph_get(&hist, 25, 10, &p, &r) && fabsf(p - 7.0f) < 0.01f && fabsf(r + 3.0f) < 0.01f, "N23: a short history uses what exists");
    for (int i = 0; i < 100; ++i) { gv_for((float)(i % 40), 0.0f, &vx, &vy); ph_push(&hist, vx, vy); }   // wraps the ring many times
    TEST_ASSERT(ph_get(&hist, 0, 1, &p, &r) && fabsf(p - 19.0f) < 0.05f, "N23: the newest sample after wrapping is the last pushed (99 % 40 = 19)");
    TEST_PASS("N23: scroll reference = comfortable pose before the double-tap (drift scrolls, soft start, anticipation ignored, history ring)");
}

// ---------------------------------------------------------------------------------------------------------------
// N24: button mapping (button_map.h)
// ---------------------------------------------------------------------------------------------------------------
void test_n24_button_map(void) {
    logical_buttons_t b;

    // Default mapping: SW2 = left, SW3 = right, SW4 = Mode
    bm_apply(true, false, false, AIR_BTN_LEFT, AIR_BTN_RIGHT, AIR_BTN_MODE, &b);
    TEST_ASSERT(b.left && !b.right && !b.middle && !b.back && !b.forward && !b.mode, "N24: default: SW2 = left click");
    bm_apply(false, true, false, AIR_BTN_LEFT, AIR_BTN_RIGHT, AIR_BTN_MODE, &b);
    TEST_ASSERT(!b.left && b.right && !b.mode, "N24: default: SW3 = right click");
    bm_apply(false, false, true, AIR_BTN_LEFT, AIR_BTN_RIGHT, AIR_BTN_MODE, &b);
    TEST_ASSERT(b.mode && !b.left && !b.right, "N24: default: SW4 = Mode");
    bm_apply(false, false, false, AIR_BTN_LEFT, AIR_BTN_RIGHT, AIR_BTN_MODE, &b);
    TEST_ASSERT(!b.left && !b.right && !b.middle && !b.back && !b.forward && !b.mode && !bm_any_click(&b), "N24: nothing held = nothing logical");

    // Left-handed: swap left and right
    bm_apply(true, false, false, AIR_BTN_RIGHT, AIR_BTN_LEFT, AIR_BTN_MODE, &b);
    TEST_ASSERT(b.right && !b.left, "N24: swapped: SW2 = right click");
    bm_apply(false, true, false, AIR_BTN_RIGHT, AIR_BTN_LEFT, AIR_BTN_MODE, &b);
    TEST_ASSERT(b.left && !b.right, "N24: swapped: SW3 = left click");

    // Middle / Back / Forward on any physical button, Mode on another one
    bm_apply(true, false, false, AIR_BTN_MIDDLE, AIR_BTN_BACK, AIR_BTN_FORWARD, &b);
    TEST_ASSERT(b.middle && !b.back && !b.forward && !b.mode, "N24: SW2 = middle");
    bm_apply(false, true, true, AIR_BTN_MIDDLE, AIR_BTN_BACK, AIR_BTN_FORWARD, &b);
    TEST_ASSERT(b.back && b.forward && !b.middle, "N24: SW3 = Back and SW4 = Forward at the same time");
    bm_apply(true, false, false, AIR_BTN_MODE, AIR_BTN_RIGHT, AIR_BTN_LEFT, &b);
    TEST_ASSERT(b.mode && !b.left, "N24: Mode can be moved to SW2");
    TEST_ASSERT(!bm_any_click(&b), "N24: Mode alone is not a mouse click (the click guard must not freeze the cursor for it)");

    // None, and unknown values, do nothing
    bm_apply(true, true, true, AIR_BTN_NONE, 99, 255, &b);
    TEST_ASSERT(!b.left && !b.right && !b.middle && !b.back && !b.forward && !b.mode, "N24: NONE and unknown actions do nothing");

    // Two physical buttons with the same action: held while either is down (OR)
    bm_apply(true, false, false, AIR_BTN_LEFT, AIR_BTN_LEFT, AIR_BTN_MODE, &b);
    TEST_ASSERT(b.left, "N24: shared action: first button");
    bm_apply(false, true, false, AIR_BTN_LEFT, AIR_BTN_LEFT, AIR_BTN_MODE, &b);
    TEST_ASSERT(b.left, "N24: shared action: second button");
    bm_apply(true, true, false, AIR_BTN_LEFT, AIR_BTN_LEFT, AIR_BTN_MODE, &b);
    TEST_ASSERT(b.left, "N24: shared action: both buttons");

    // Which actions count as a "click" for the click guard
    const uint8_t clicks[] = { AIR_BTN_LEFT, AIR_BTN_RIGHT, AIR_BTN_MIDDLE, AIR_BTN_BACK, AIR_BTN_FORWARD };
    for (size_t i = 0; i < sizeof clicks; ++i) {
        bm_apply(true, false, false, clicks[i], AIR_BTN_NONE, AIR_BTN_NONE, &b);
        TEST_ASSERT(bm_any_click(&b), "N24: every mouse button counts as a click for the click guard");
    }

    // Exhaustive: every action on every physical button gives exactly the expected logical button
    for (int act = 0; act < AIR_BTN_COUNT; ++act) {
        for (int which = 0; which < 3; ++which) {
            uint8_t acts[3] = { AIR_BTN_NONE, AIR_BTN_NONE, AIR_BTN_NONE };
            acts[which] = (uint8_t)act;
            bm_apply(which == 0, which == 1, which == 2, acts[0], acts[1], acts[2], &b);
            int count = b.left + b.right + b.middle + b.back + b.forward + b.mode;
            TEST_ASSERT(count == (act == AIR_BTN_NONE ? 0 : 1), "N24: exactly one logical button for one pressed physical button");
            bool expect = (act == AIR_BTN_LEFT && b.left) || (act == AIR_BTN_RIGHT && b.right) || (act == AIR_BTN_MIDDLE && b.middle) ||
                          (act == AIR_BTN_BACK && b.back) || (act == AIR_BTN_FORWARD && b.forward) || (act == AIR_BTN_MODE && b.mode) || act == AIR_BTN_NONE;
            TEST_ASSERT(expect, "N24: the logical button matches the action");
        }
    }

    // Names (used in the serial log)
    TEST_ASSERT(strcmp(bm_action_name(AIR_BTN_MIDDLE), "MIDDLE") == 0 && strcmp(bm_action_name(AIR_BTN_MODE), "MODE") == 0 &&
                strcmp(bm_action_name(AIR_BTN_NONE), "NONE") == 0 && strcmp(bm_action_name(200), "?") == 0, "N24: action names");

    // The defaults of the settings are the mapping the firmware always had
    air_config_t c; air_config_defaults(&c);
    TEST_ASSERT(c.btn_left == AIR_BTN_LEFT && c.btn_right == AIR_BTN_RIGHT && c.btn_mode == AIR_BTN_MODE && c.invert_x == 0 && c.invert_y == 0,
                "N24: default settings = left / right / Mode, no inversion");
    TEST_PASS("N24: button mapping (default, left-handed swap, middle/back/forward, none, shared actions, exhaustive, names)");
}

// ---------------------------------------------------------------------------------------------------------------
// N25: sensor health monitor (imu_health.h): fast detection of a lost sensor / failing I2C, rate limits, no false alarms
// ---------------------------------------------------------------------------------------------------------------
static uint32_t s_ih_seed = 777u;
static float ih_noise(void) { s_ih_seed = s_ih_seed * 1664525u + 1013904223u; return ((float)(s_ih_seed >> 8) / 16777216.0f) - 0.5f; }
static imu_data_t ih_live(float an = 1.0f) {            // a live sensor: ~an g on Z plus noise, gyro noise
    imu_data_t d;
    d.ax = 0.01f * ih_noise(); d.ay = 0.01f * ih_noise(); d.az = an + 0.01f * ih_noise();
    d.gx = 0.2f * ih_noise();  d.gy = 0.2f * ih_noise();  d.gz = 0.2f * ih_noise();
    return d;
}
static imu_data_t ih_zero(void) { imu_data_t d = { 0.0f, 0.0f, 0.0f, 0.0f, 0.0f, 0.0f }; return d; }

void test_n25_imu_health(void) {
    imu_health_t h; ih_init(&h);
    uint32_t t = 1000;
    imu_data_t d;

    // 1. A healthy sensor: nothing is ever dropped
    int not_ok = 0;
    for (int i = 0; i < 5000; ++i) { d = ih_live(); if (ih_update(&h, t += 10, true, &d) != IH_OK) ++not_ok; }
    TEST_ASSERT(not_ok == 0 && h.reinit_total == 0 && h.fail_total == 0 && h.zero_total == 0, "N25: a healthy sensor is never dropped or re-initialised");

    // 2. The sensor falls asleep (all zeros): dropped at once, re-initialised on the 3rd sample (30 ms, not 500 ms)
    d = ih_zero();
    TEST_ASSERT(ih_update(&h, t += 10, true, &d) == IH_DROP, "N25: first zero sample is dropped (never reaches the pipeline)");
    TEST_ASSERT(ih_update(&h, t += 10, true, &d) == IH_DROP, "N25: second zero sample is dropped");
    TEST_ASSERT(ih_update(&h, t += 10, true, &d) == IH_REINIT && h.reason == IH_WHY_ZERO, "N25: third zero sample asks for a re-initialisation");
    uint32_t t_reinit = t;
    ih_note_reinit(&h, t, true);

    // 3. Start-up time after the re-initialisation: dropped and NOT counted, even zeros
    int settle_ok = 0;
    for (int i = 0; i < 7; ++i) { d = (i % 2) ? ih_zero() : ih_live(); if (ih_update(&h, t += 10, true, &d) != IH_DROP) ++settle_ok; }
    TEST_ASSERT(settle_ok == 0 && h.zero_total == 3, "N25: samples during the 80 ms start-up are dropped and do not count");
    d = ih_live();
    ih_action_t a = IH_DROP;
    for (int i = 0; i < 3 && a != IH_OK; ++i) { d = ih_live(); a = ih_update(&h, t += 10, true, &d); }
    TEST_ASSERT(a == IH_OK, "N25: after the start-up time live samples are used again");

    // 4. The sensor stays dead: the next recovery is not before 300 ms after the last (no spinning), then it comes
    uint32_t t_second = 0; int reinits_early = 0;
    for (int i = 0; i < 100 && !t_second; ++i) {
        d = ih_zero();
        ih_action_t r = ih_update(&h, t += 10, true, &d);
        if (r == IH_REINIT) t_second = t; else if (t - t_reinit < IH_MIN_GAP_OK_MS && r == IH_REINIT) ++reinits_early;
    }
    TEST_ASSERT(t_second != 0 && t_second - t_reinit >= IH_MIN_GAP_OK_MS && t_second - t_reinit <= IH_MIN_GAP_OK_MS + 30 && reinits_early == 0,
                "N25: a dead sensor is re-initialised again no sooner than 300 ms after the previous one");

    // 5. If the re-initialisation FAILED (sensor really missing) the gap grows to 3 s
    ih_note_reinit(&h, t, false);
    uint32_t t_fail = t, t_third = 0;
    for (int i = 0; i < 600 && !t_third; ++i) { d = ih_zero(); if (ih_update(&h, t += 10, true, &d) == IH_REINIT) t_third = t; }
    TEST_ASSERT(t_third != 0 && t_third - t_fail >= IH_MIN_GAP_FAIL_MS && t_third - t_fail <= IH_MIN_GAP_FAIL_MS + 30,
                "N25: after a FAILED re-initialisation the next attempt waits 3 s");
    ih_note_reinit(&h, t, true);
    for (int i = 0; i < 20; ++i) { d = ih_live(); ih_update(&h, t += 10, true, &d); }

    // 6. Failed I2C reads: 2 in a row are only dropped; the 3rd asks for recovery; a good read in between resets the run
    imu_health_t f; ih_init(&f); t = 5000;
    TEST_ASSERT(ih_update(&f, t += 10, false, NULL) == IH_DROP && ih_update(&f, t += 10, false, NULL) == IH_DROP, "N25: two failed reads in a row are dropped");
    d = ih_live();
    TEST_ASSERT(ih_update(&f, t += 10, true, &d) == IH_OK, "N25: a good read after failures is used");
    TEST_ASSERT(ih_update(&f, t += 10, false, NULL) == IH_DROP && ih_update(&f, t += 10, false, NULL) == IH_DROP && f.reinit_total == 0, "N25: the failure run restarts after a good read");
    TEST_ASSERT(ih_update(&f, t += 10, false, NULL) == IH_REINIT && f.reason == IH_WHY_READ_FAIL, "N25: three failed reads in a row ask for bus recovery + re-initialisation");
    TEST_ASSERT(f.fail_total == 5, "N25: failed reads are counted");

    // 7. The older safety net: 100 identical samples; |a| < 0.5 g for 50 samples
    imu_health_t g; ih_init(&g); t = 9000;
    d = ih_live(); imu_data_t same = d;
    int idx_frozen = -1;
    for (int i = 0; i < 150 && idx_frozen < 0; ++i) if (ih_update(&g, t += 10, true, &same) == IH_REINIT) idx_frozen = i;
    TEST_ASSERT(idx_frozen == 100 && g.reason == IH_WHY_FROZEN, "N25: 100 identical samples after the first one = frozen sensor");
    imu_health_t k; ih_init(&k); t = 20000;
    int idx_dead = -1;
    for (int i = 0; i < 80 && idx_dead < 0; ++i) { d = ih_live(0.3f); if (ih_update(&k, t += 10, true, &d) == IH_REINIT) idx_dead = i; }
    TEST_ASSERT(idx_dead == 49 && k.reason == IH_WHY_DEAD, "N25: |a| < 0.5 g for 50 samples = dead sensor");
    imu_health_t ff; ih_init(&ff); t = 30000; int ff_bad = 0;
    for (int i = 0; i < 20; ++i) { d = ih_live(0.2f); if (ih_update(&ff, t += 10, true, &d) != IH_OK) ++ff_bad; }       // brief free fall
    for (int i = 0; i < 500; ++i) { d = ih_live(); if (ih_update(&ff, t += 10, true, &d) != IH_OK) ++ff_bad; }
    TEST_ASSERT(ff_bad == 0, "N25: a short free fall (0.2 g for 200 ms) is not a fault");

    // 8. NaN / infinity count as a bad sample
    imu_health_t nn; ih_init(&nn); t = 40000;
    imu_data_t bad = ih_live(); bad.az = NAN;
    TEST_ASSERT(ih_update(&nn, t += 10, true, &bad) == IH_DROP && ih_update(&nn, t += 10, true, &bad) == IH_DROP && ih_update(&nn, t += 10, true, &bad) == IH_REINIT, "N25: NaN samples are dropped and trigger recovery like zeros");

    // 9. Glitches that never reach 3 in a row never trigger anything, and good samples around them are used
    imu_health_t gl; ih_init(&gl); t = 50000;
    uint32_t seed = 4242u; int wrong = 0, run = 0;
    for (int i = 0; i < 100000; ++i) {
        seed = seed * 1664525u + 1013904223u;
        bool glitch = ((seed >> 20) % 5 == 0) && run < 2;           // about one in five, at most 2 in a row
        run = glitch ? run + 1 : 0;
        ih_action_t r;
        if (glitch) {
            if ((seed >> 12) & 1) r = ih_update(&gl, t += 10, false, NULL);
            else { d = ih_zero(); r = ih_update(&gl, t += 10, true, &d); }
            if (r != IH_DROP) ++wrong;
        } else {
            d = ih_live(); r = ih_update(&gl, t += 10, true, &d);
            if (r != IH_OK) ++wrong;
        }
    }
    TEST_ASSERT(wrong == 0 && gl.reinit_total == 0, "N25: short glitches (1-2 in a row) are dropped one by one, never trigger a re-initialisation");

    // 10. The 32-bit millisecond clock wraps around
    imu_health_t w; ih_init(&w); t = 0xFFFFFF00u;
    d = ih_zero();
    ih_update(&w, t += 10, true, &d); ih_update(&w, t += 10, true, &d);
    TEST_ASSERT(ih_update(&w, t += 10, true, &d) == IH_REINIT, "N25: recovery requested before the clock wraps");
    ih_note_reinit(&w, t, true);
    int w_ok = 0;
    for (int i = 0; i < 60; ++i) { d = ih_live(); if (ih_update(&w, t += 10, true, &d) == IH_OK) ++w_ok; }       // crosses 2^32
    TEST_ASSERT(w_ok >= 50 && w.reinit_total == 1, "N25: the start-up time and the live samples work across the clock wrap");

    // 11. Names and the driver's recovery counter (host build: the stub always succeeds)
    TEST_ASSERT(strlen(ih_reason_name(IH_WHY_ZERO)) > 4 && strlen(ih_reason_name(IH_WHY_READ_FAIL)) > 4 && strcmp(ih_reason_name(IH_WHY_NONE), "none") == 0, "N25: reason names");
    uint32_t before = imu_getBusRecoveries();
    TEST_ASSERT(imu_busRecover() && imu_getBusRecoveries() == before + 1, "N25: bus recovery counter (host stub)");
    TEST_PASS("N25: sensor health (zeros dropped at once, 3 failures/zeros = recover, settle time, rate limits, glitch-proof, clock wrap)");
}

int main(void) {
    printf("==============================================================\n");
    printf(" AIR MOUSE FIRMWARE TEST HARNESS — HYBRID AIR MOUSE\n");
    printf("                  (6-AXIS FUSION ON ICM-20948)\n");
    printf("==============================================================\n");

    test_register_bitfields();
    test_driver_semi_register();
    test_stationary_detection();
    test_deadzone_and_rotation();
    test_clutch_and_recenter();
    test_attitude_and_gravity_removal();
    test_flick_gesture();
    test_attitude_convergence_p1a();
    test_dynamic_dt_and_timing();
    test_motion_process_end_to_end_gestures_p1b();

    // Run new tests N1-N6
    test_n1_still();
    test_n2_slow_1_0();
    test_n3_very_slow_0_5();
    test_n4_no_bias_absorption();
    test_n5_high_speed();
    test_n6_saturation();
    test_n7_residual_bias_limit();
    test_n8_calibration_validation();
    test_n9_surface_rest_self_heal();
    test_n10_button_debounce();
    test_n11_click_guard();
    test_n12_debounce_asymmetric();
    test_n13_mode_button_recenter();
    test_n14_yaw_flick();
    test_n15_config_defaults();
    test_n16_config_set_ok();
    test_n17_config_set_rejects();
    test_n18_config_commands_and_buffers();
    test_n19_config_validity_and_fuzz();
    test_n20_scroll_state_machine();
    test_n21_scroll_tilt();
    test_n22_scroll_with_pipeline();
    test_n23_scroll_reference_before_tap();
    test_n24_button_map();
    test_n25_imu_health();

    printf("==============================================================\n");
    printf(" ALL %d TESTS PASSED (HOST_TESTED - Unit test on host environment,\n", s_tests_passed);
    printf("                     physical sensor & hardware verification pending)\n");
    printf("==============================================================\n");
    return 0;
}
