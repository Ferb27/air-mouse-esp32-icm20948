# -*- coding: utf-8 -*-
"""
analyze_bias_drift.py - summarise a firmware_bias_drift log.

  python scripts/host_verify/analyze_bias_drift.py raw_logs/bias_drift_2026-10-04.log [--out result.txt]

Reads the "[D] ..." lines (see firmware_bias_drift/src/main.cpp), ignores any
"[HH:MM:SS.mmm]" host prefix, and prints plain-ASCII tables. It only REPORTS numbers; it
does not decide thresholds for the firmware.
"""
import argparse
import math
import re
import sys

D_RE = re.compile(
    r"\[D\]\s+(\d+)\s+(\S+)\s+(\d+)\s+(\d+)\s+"
    r"([+-]?\d+\.\d+)\s+([+-]?\d+\.\d+)\s+([+-]?\d+\.\d+)\s+"
    r"(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)\s+"
    r"(\d+)\s+(\d+)\s+(\d+)\s+"
    r"([+-]?\d+\.\d+)\s+([+-]?\d+\.\d+)\s+([+-]?\d+\.\d+)\s*$")
CAL_RE = re.compile(r"\[CAL\].*")


def mean(v):
    return sum(v) / len(v) if v else float("nan")


def slope_per_min(ts, ys):
    n = len(ts)
    if n < 3:
        return float("nan")
    mt, my = mean(ts), mean(ys)
    den = sum((t - mt) ** 2 for t in ts)
    return (sum((t - mt) * (y - my) for t, y in zip(ts, ys)) / den) * 60.0 if den else float("nan")


def rolling(v, w):
    return [mean(v[i:i + w]) for i in range(0, len(v) - w + 1)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("log")
    ap.add_argument("--out", default=None)
    a = ap.parse_args()

    rows, cal_line = [], None
    with open(a.log, encoding="utf-8", errors="replace") as fp:
        for line in fp:
            if cal_line is None:
                m = CAL_RE.search(line)
                if m:
                    cal_line = m.group(0).strip()
            m = D_RE.search(line)
            if not m:
                continue
            g = m.groups()
            try:
                temp = float(g[1])
            except ValueError:
                temp = float("nan")
            rows.append(dict(t=int(g[0]), temp=temp, n=int(g[2]), fail=int(g[3]),
                             r=[float(g[4]), float(g[5]), float(g[6])],
                             sd=[float(g[7]), float(g[8]), float(g[9])],
                             cnt=int(g[10]), stat=int(g[11]), fix=int(g[12]),
                             b=[float(g[13]), float(g[14]), float(g[15])]))
    out = []
    P = out.append
    P(f"log: {a.log}")
    P(f"cal: {cal_line or 'NOT FOUND'}")
    if len(rows) < 30:
        P(f"ERROR: only {len(rows)} [D] lines parsed (need >= 30). Run is too short or log is malformed.")
        text = "\n".join(out)
        print(text)
        return 1

    ts = [r["t"] for r in rows]
    gaps = sum(1 for x, y in zip(ts, ts[1:]) if y - x != 1)
    ns = [r["n"] for r in rows]
    P(f"seconds parsed: {len(rows)} (t={ts[0]}..{ts[-1]}), non-consecutive jumps: {gaps}")
    P(f"samples/second: mean={mean(ns):.1f} min={min(ns)} max={max(ns)} (expect ~100); "
      f"total failed reads={sum(r['fail'] for r in rows)}")
    P("")

    names = ["rx(roll,no cursor)", "ry(pitch->dY)", "rz(yaw->dX)"]
    P("PER-MINUTE TABLE (residual = mean raw gyro - startup calibration, dps; averaged over the minute)")
    P("min | temp_end | rx      ry      rz     | max|10s-mean| rx   ry   rz  | cnt(sum) | stat%  | fixlock%")
    for m0 in range(0, len(rows), 60):
        blk = rows[m0:m0 + 60]
        if len(blk) < 20:
            break
        ravg = [mean([r["r"][k] for r in blk]) for k in range(3)]
        mx = []
        for k in range(3):
            roll = rolling([r["r"][k] for r in blk], 10)
            mx.append(max(abs(x) for x in roll) if roll else float("nan"))
        ntot = sum(r["n"] for r in blk)
        P(f"{m0 // 60 + 1:>3} | {blk[-1]['temp']:>8.2f} | {ravg[0]:+.3f} {ravg[1]:+.3f} {ravg[2]:+.3f} | "
          f"{mx[0]:.3f} {mx[1]:.3f} {mx[2]:.3f} | {sum(r['cnt'] for r in blk):>8} | "
          f"{100.0 * sum(r['stat'] for r in blk) / ntot:>5.1f}  | {100.0 * sum(r['fix'] for r in blk) / ntot:>5.1f}")
    P("")

    P("SUMMARY")
    t_first = mean([r["temp"] for r in rows[:10]])
    t_last = mean([r["temp"] for r in rows[-10:]])
    P(f"die temperature: first 10 s avg {t_first:.2f} C -> last 10 s avg {t_last:.2f} C (delta {t_last - t_first:+.2f} C)")
    for k in range(3):
        series = [r["r"][k] for r in rows]
        r10 = rolling(series, 10)
        imax = max(range(len(r10)), key=lambda i: abs(r10[i]))
        early = mean(series[:30])
        late = mean(series[-60:])
        P(f"{names[k]:<20} first-30s avg {early:+.3f} | last-60s avg {late:+.3f} | change {late - early:+.3f} dps | "
          f"max |10s mean| {abs(r10[imax]):.3f} at t~{rows[imax]['t'] + 5}s | slope {slope_per_min(ts, series):+.4f} dps/min")
    sdm = [mean([r["sd"][k] for r in rows]) for k in range(3)]
    P(f"noise (mean per-second std-dev): gx {sdm[0]:.3f}  gy {sdm[1]:.3f}  gz {sdm[2]:.3f} dps (bench 2026-10-01: ~0.09)")

    ctrl10 = [max(abs(x), abs(y)) for x, y in zip(rolling([r["r"][1] for r in rows], 10),
                                                 rolling([r["r"][2] for r in rows], 10))]
    for thr in (0.1, 0.2, 0.3):
        n_over = sum(1 for x in ctrl10 if x >= thr)
        P(f"windows (10 s mean) where max(|ry|,|rz|) >= {thr}: {n_over} of {len(ctrl10)}")
    P(f"largest max(|ry|,|rz|) of any 10 s mean: {max(ctrl10):.3f} dps")
    noisy = [r["t"] for r in rows if max(r["sd"]) > 0.25]
    P(f"possible disturbance (any per-second std-dev > 0.25 dps, i.e. touch/vibration): {len(noisy)} s"
      + (f", at t = {noisy[:15]}{' ...' if len(noisy) > 15 else ''}" if noisy else ""))
    P("")
    ntot = sum(ns)
    P(f"REAL PIPELINE (production motion_process, clutch released): total |dX|+|dY| = {sum(r['cnt'] for r in rows)} counts "
      f"in {len(rows)} s; reported stationary {100.0 * sum(r['stat'] for r in rows) / ntot:.1f}% of samples")
    P(f"WORST CASE (fixed startup calibration, no auto-zero): stationary lock would hold {100.0 * sum(r['fix'] for r in rows) / ntot:.1f}% of samples")
    P(f"pipeline bias estimate: start ({rows[0]['b'][0]:+.3f},{rows[0]['b'][1]:+.3f},{rows[0]['b'][2]:+.3f}) -> "
      f"end ({rows[-1]['b'][0]:+.3f},{rows[-1]['b'][1]:+.3f},{rows[-1]['b'][2]:+.3f}) dps")
    P("")
    P("REFERENCE SCALE (simulation, noise 0.09 dps, residual on yaw, counts per 10 s of resting): "
      "0.1 -> 1-3 | 0.2 -> 27-45 | 0.3 -> 161-171 | 0.5 -> ~415 (docs/FIRMWARE_CHANGELOG_2026-10-03.md, section 6)")

    text = "\n".join(out)
    print(text)
    if a.out:
        with open(a.out, "w", encoding="utf-8", newline="\n") as fp:
            fp.write(text + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
