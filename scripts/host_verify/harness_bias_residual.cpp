// Independent verification harness #2 (Claude): residual bias on the axes that actually drive the cursor.
#include <stdio.h>
#include <stdint.h>
#include <math.h>
#include <stdlib.h>
#include <initializer_list>
#include "motion_pipeline.h"

static uint32_t g_seed = 777u;
static float frand01(void) { g_seed = g_seed * 1664525u + 1013904223u; return ((g_seed >> 8) + 1) * (1.0f / 16777217.0f); }
static float gauss(float s) { float u1 = frand01(), u2 = frand01(); return s * sqrtf(-2.0f * logf(u1)) * cosf(6.2831853f * u2); }
static const float CAL[3] = {-0.54f, -1.49f, 0.32f};

struct Sim {
    float sigma; uint32_t now; long adx, ady, sdx, sdy; int stat, total;
    Sim(float sg, uint32_t seed) : sigma(sg), now(1000), adx(0), ady(0), sdx(0), sdy(0), stat(0), total(0) {
        g_seed = seed; motion_init(NULL); motion_setBias(CAL[0], CAL[1], CAL[2]);
    }
    mouse_output_t tick(float rx, float ry, float rz) {
        imu_data_t s; s.ax = 0; s.ay = 0; s.az = 0.988f;
        s.gx = CAL[0] + rx + gauss(sigma); s.gy = CAL[1] + ry + gauss(sigma); s.gz = CAL[2] + rz + gauss(sigma);
        mouse_output_t o = motion_process(&s, false, now); now += 10;
        adx += labs(o.delta_x); ady += labs(o.delta_y); sdx += o.delta_x; sdy += o.delta_y;
        stat += o.is_stationary ? 1 : 0; total++;
        return o;
    }
};

int main(void) {
    printf("B2. Nam yen 10 s, nhieu 0.09; bias du tren TRUC YAW (Z); tong |dX|+|dY| va %% mau 'dung yen'\n");
    for (float r : {0.0f, 0.1f, 0.2f, 0.3f, 0.4f, 0.5f, 0.8f}) {
        printf("   residZ=%.1f :", r);
        for (uint32_t seed = 11; seed <= 13; ++seed) {
            Sim s(0.09f, seed);
            for (int i = 0; i < 1000; ++i) s.tick(0, 0, r);
            printf("  [%4ld counts, %3d%% yen]", s.adx + s.ady, 100 * s.stat / s.total);
        }
        printf("\n");
    }
    printf("B3. Bias du dong thoi tren Y va Z (pitch+yaw), moi truc r\n");
    for (float r : {0.1f, 0.2f, 0.3f}) {
        Sim s(0.09f, 5);
        for (int i = 0; i < 1000; ++i) s.tick(0, r, r);
        printf("   r=%.1f : %ld counts / 10 s, %d%% yen\n", r, s.adx + s.ady, 100 * s.stat / s.total);
    }
    printf("H. Bias troi cham theo nhiet: residZ tang tuyen tinh 0 -> R trong 120 s (nam yen); tong counts, %% yen, counts trong 20 s cuoi\n");
    for (float R : {0.3f, 0.6f, 1.0f}) {
        Sim s(0.09f, 9); long last20 = 0;
        for (int i = 0; i < 12000; ++i) {
            long before = s.adx + s.ady;
            s.tick(0, 0, R * i / 12000.0f);
            if (i >= 10000) last20 += (s.adx + s.ady) - before;
        }
        printf("   R=%.1f : tong %ld counts, %d%% yen, 20 s cuoi %ld counts\n", R, s.adx + s.ady, 100 * s.stat / s.total, last20);
    }
    return 0;
}
