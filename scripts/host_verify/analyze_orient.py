# -*- coding: utf-8 -*-
"""
analyze_orient.py - per-phase summary of a firmware_orient log.

  python scripts/host_verify/analyze_orient.py <log> <phases.csv> [--out result.txt]

phases.csv (no header), host clock as in the log prefix "[HH:MM:SS.mmm]":
  name,HH:MM:SS.mmm,HH:MM:SS.mmm
Per phase it prints: lines used, failed I2C reads, mean accelerometer (g), mean gyro (dps, minus bias),
and the gyro INTEGRAL in degrees per axis (sum of mean-gyro * 0.1 s) = how far it turned about each axis.
It only reports numbers; it does not interpret directions.
"""
import argparse
import re
import sys

O_RE = re.compile(r"^\[(\d\d):(\d\d):(\d\d)\.(\d+)\]\s+\[O\]\s+(\d+)\s+"
                  r"([+-]?\d+\.\d+)\s+([+-]?\d+\.\d+)\s+([+-]?\d+\.\d+)\s+"
                  r"([+-]?\d+\.\d+)\s+([+-]?\d+\.\d+)\s+([+-]?\d+\.\d+)\s+(\d+)\s*$")


def secs(h, m, s, ms):
    return int(h) * 3600 + int(m) * 60 + int(s) + float("0." + ms)


def parse_clock(t):
    h, m, rest = t.strip().split(":")
    s, ms = (rest.split(".") + ["0"])[:2]
    return secs(h, m, s, ms)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("log")
    ap.add_argument("phases")
    ap.add_argument("--out")
    a = ap.parse_args()

    rows = []
    cal = None
    with open(a.log, encoding="utf-8", errors="replace") as fp:
        for line in fp:
            if cal is None and "[CAL]" in line:
                cal = line.strip()
            m = O_RE.match(line.strip())
            if m:
                g = m.groups()
                rows.append((secs(*g[:4]), [float(x) for x in g[5:11]], int(g[11])))
    out = [f"log: {a.log}", f"cal: {cal or 'NOT FOUND'}", f"[O] lines parsed: {len(rows)}", ""]
    out.append("phase | n | fail | mean ax ay az (g) | mean gx gy gz (dps) | turned about X Y Z (deg)")
    for ln in open(a.phases, encoding="utf-8"):
        ln = ln.strip()
        if not ln or ln.startswith("#"):
            continue
        name, t0, t1 = [x.strip() for x in ln.split(",")]
        s0, s1 = parse_clock(t0), parse_clock(t1)
        sel = [r for r in rows if s0 <= r[0] <= s1]
        if not sel:
            out.append(f"{name} | 0 | - | NO DATA between {t0} and {t1}")
            continue
        n = len(sel)
        mean = [sum(r[1][k] for r in sel) / n for k in range(6)]
        integ = [sum(r[1][3 + k] for r in sel) * 0.1 for k in range(3)]
        fail = sum(r[2] for r in sel)
        out.append(f"{name} | {n} | {fail} | {mean[0]:+.3f} {mean[1]:+.3f} {mean[2]:+.3f} | "
                   f"{mean[3]:+.2f} {mean[4]:+.2f} {mean[5]:+.2f} | {integ[0]:+.1f} {integ[1]:+.1f} {integ[2]:+.1f}")
    text = "\n".join(out)
    print(text)
    if a.out:
        with open(a.out, "w", encoding="utf-8", newline="\n") as fp:
            fp.write(text + "\n")


if __name__ == "__main__":
    sys.exit(main())
