# -*- coding: utf-8 -*-
"""
scripts/capture_serial.py - capture a serial port to a NEW raw log, optionally from boot.

  python scripts/capture_serial.py --port COM3 --out raw_logs/bias_drift_2026-10-04.log \
         --seconds 800 --reset --stop-on "[DRIFT] DONE"

* --port also accepts a pyserial URL, e.g. rfc2217://<LAPTOP_IP>:4000 (board plugged into
  another machine that runs esp_rfc2217_server); DTR/RTS control is then relayed over the network.
* Refuses to overwrite an existing file (raw logs are never edited).
* Opens the port with DTR/RTS OFF; --reset then pulses RTS ~150 ms (EN low) so the
  board restarts and the log starts at the boot banner (see memory: air-mouse-bench-setup).
* Every received line is stored as "[HH:MM:SS.mmm] <line>" (PC clock).
* Stops after --seconds, or as soon as a line contains --stop-on.
* Prints the SHA-256 of the finished log.
"""
import argparse
import hashlib
import os
import sys
import time

import serial


def main() -> int:
    # Windows consoles (cp1252) crash on the binary junk the ESP32 prints at boot; never let printing kill the capture.
    try:
        sys.stdout.reconfigure(errors="replace")
    except Exception:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", default="COM3")
    ap.add_argument("--baud", type=int, default=115200)
    ap.add_argument("--out", required=True)
    ap.add_argument("--seconds", type=float, required=True, help="hard time limit")
    ap.add_argument("--reset", action="store_true", help="pulse RTS to reset the board after opening")
    ap.add_argument("--stop-on", default=None, help="stop when a line contains this text")
    args = ap.parse_args()

    if os.path.exists(args.out):
        print(f"ERROR: {args.out} already exists. Raw logs are never overwritten; pick a new name.")
        return 2
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)

    try:
        ser = serial.serial_for_url(args.port, do_not_open=True)
        ser.baudrate = args.baud
        ser.timeout = 0.5
        ser.open()
        ser.dtr = False   # after open: also valid for rfc2217:// links
        ser.rts = False
    except Exception as exc:  # port busy, missing, network unreachable, ...
        print(f"ERROR: cannot open {args.port}: {exc}")
        return 1

    if args.reset:
        time.sleep(0.1)
        ser.rts = True
        time.sleep(0.15)
        ser.rts = False
        print(f"RTS reset pulse sent on {args.port}")

    start = time.time()
    nbytes = 0
    nlines = 0
    stopped_by = "timeout"
    with open(args.out, "w", encoding="utf-8", errors="replace", newline="\n") as fp:
        fp.write(f"# capture_serial.py port={args.port} baud={args.baud} reset={args.reset} "
                 f"seconds={args.seconds} start={time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        try:
            while time.time() - start < args.seconds:
                raw = ser.readline()
                if not raw:
                    continue
                nbytes += len(raw)
                nlines += 1
                text = raw.decode("utf-8", errors="replace").rstrip("\r\n")
                now = time.time()
                stamp = time.strftime("%H:%M:%S", time.localtime(now)) + f".{int((now % 1) * 1000):03d}"
                fp.write(f"[{stamp}] {text}\n")
                fp.flush()
                if nlines <= 12 or nlines % 60 == 0:
                    print(f"[{stamp}] {text}")
                if args.stop_on and args.stop_on in text:
                    stopped_by = "stop-on"
                    break
        except serial.SerialException as exc:
            stopped_by = f"serial-error: {exc}"
        fp.write(f"# end elapsed_s={time.time() - start:.1f} lines={nlines} bytes={nbytes} stopped_by={stopped_by}\n")
    ser.close()

    h = hashlib.sha256()
    with open(args.out, "rb") as fp:
        h.update(fp.read())
    print(f"done: {args.out} lines={nlines} bytes={nbytes} stopped_by={stopped_by}")
    print(f"SHA-256 {h.hexdigest()}")
    return 0 if stopped_by in ("timeout", "stop-on") else 1


if __name__ == "__main__":
    sys.exit(main())
