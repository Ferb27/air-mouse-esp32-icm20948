// Independent verification harness (Claude). Not part of the project.
// Build twice: against the OLD (backup) and NEW motion_pipeline.cpp, compare output.
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
    float resid[3];
    float sigma;
    uint32_t now;
    long sdx, sdy;       // signed sums
    long adx, ady;       // absolute sums
    Sim(float rx, float ry, float rz, float sg, uint32_t seed) : sigma(sg), now(1000), sdx(0), sdy(0), adx(0), ady(0) {
        resid[0] = rx; resid[1] = ry; resid[2] = rz;
        g_seed = seed;
        motion_init(NULL);
        motion_setBias(CAL[0], CAL[1], CAL[2]);
    }
    // one tick with extra motion (mx,my,mz) in dps; returns output
    mouse_output_t tick(float mx, float my, float mz) {
        imu_data_t s;
        s.ax = 0.0f; s.ay = 0.0f; s.az = 0.988f;
        s.gx = CAL[0] + resid[0] + mx + (sigma > 0 ? gauss(sigma) : 0.0f);
        s.gy = CAL[1] + resid[1] + my + (sigma > 0 ? gauss(sigma) : 0.0f);
        s.gz = CAL[2] + resid[2] + mz + (sigma > 0 ? gauss(sigma) : 0.0f);
        mouse_output_t o = motion_process(&s, false, now);
        now += 10;
        sdx += o.delta_x; sdy += o.delta_y;
        adx += labs(o.delta_x); ady += labs(o.delta_y);
        return o;
    }
    void rest(int n) { for (int i = 0; i < n; ++i) tick(0, 0, 0); }
};

int main(void) {
    printf("A. 50 yen (khong nhieu) + 100 mau quay deu quanh truc dung; tong dX\n");
    float ws[] = {0.3f, 0.5f, 1.0f, 1.5f, 5.0f, 30.0f};
    for (float w : ws) {
        Sim s(0, 0, 0, 0, 1); s.rest(50);
        long b = s.sdx; for (int i = 0; i < 100; ++i) s.tick(0, 0, w);
        printf("   w=%5.1f  dX=%6ld\n", w, s.sdx - b);
    }

    printf("B. Nam yen 10 s, nhieu sigma=0.09, bias du tren truc X; tong |dX|+|dY| (3 hat giong)\n");
    float rs[] = {0.0f, 0.1f, 0.2f, 0.3f, 0.5f};
    for (float r : rs) {
        printf("   resid=%.1f :", r);
        for (uint32_t seed = 11; seed <= 13; ++seed) {
            Sim s(r, 0, 0, 0.09f, seed); s.rest(1000);
            printf("  %5ld", s.adx + s.ady);
        }
        printf("\n");
    }

    printf("C. Nhich tay thuc te: 3 s yen, buoc van toc sin^2 (dinh Vpk, T s), 1.5 s yen sau; dX trong luc nhich / sau khi dung / counts moi do\n");
    struct P { float vpk, T; } ps[] = {{3.0f, 0.5f}, {1.5f, 1.0f}, {1.0f, 1.5f}, {0.6f, 2.0f}};
    for (auto p : ps) {
        Sim s(0.05f, 0, 0, 0.09f, 21); s.rest(300);
        long b = s.sdx; int n = (int)(p.T * 100); double theta = 0;
        for (int i = 0; i < n; ++i) {
            float v = p.vpk * powf(sinf(3.14159265f * (i + 0.5f) / n), 2.0f);
            theta += v * 0.01; s.tick(0, 0, v);
        }
        long during = s.sdx - b; long b2 = s.sdx; s.rest(150);
        printf("   Vpk=%.1f T=%.1fs goc=%.2fdeg : trong=%5ld  sau=%4ld  counts/do=%.0f\n", p.vpk, p.T, theta, during, s.sdx - b2, theta > 0 ? during / theta : 0);
    }

    printf("D. Quanh nguong khoa 0.4: quay deu w (+nhieu), 5 s sau 3 s yen; dX tong va dX/s\n");
    float ds[] = {0.3f, 0.35f, 0.4f, 0.45f, 0.5f, 0.7f};
    for (float w : ds) {
        Sim s(0, 0, 0, 0.09f, 31); s.rest(300); long b = s.sdx;
        for (int i = 0; i < 500; ++i) s.tick(0, 0, w);
        printf("   w=%.2f  dX=%5ld  (%.1f counts/s)\n", w, s.sdx - b, (s.sdx - b) / 5.0);
    }

    printf("E. Duoi sau khi dung: quay w=2 deg/s 1 s roi 0; dX trong 100 mau dau sau khi dung\n");
    for (float w : {2.0f, 5.0f}) {
        Sim s(0, 0, 0, 0, 1); s.rest(50);
        for (int i = 0; i < 100; ++i) s.tick(0, 0, w);
        long b = s.sdx; s.rest(100);
        printf("   w=%.1f : dX sau dung = %ld\n", w, s.sdx - b);
    }

    printf("F. Doi xung: gz=-1.0 (dX), gy=+1.0 (pitch len -> dY)  100 mau\n");
    { Sim s(0, 0, 0, 0, 1); s.rest(50); long b = s.sdx; for (int i = 0; i < 100; ++i) s.tick(0, 0, -1.0f); printf("   gz=-1.0 : dX=%ld\n", s.sdx - b); }
    { Sim s(0, 0, 0, 0, 1); s.rest(50); long b = s.sdy; for (int i = 0; i < 100; ++i) s.tick(0, 1.0f, 0); printf("   gy=+1.0 : dY=%ld\n", s.sdy - b); }
    return 0;
}
