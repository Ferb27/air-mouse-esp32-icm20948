# -*- coding: utf-8 -*-
"""
scripts/gain_tuner.py - keep ONE serial session open to the Air Mouse and let a file act as a remote knob.

  python scripts/gain_tuner.py --port "rfc2217://<LAPTOP_IP>:4000?ign_set_control" --log <log> --cmd <cmdfile>

* Opening the port resets the board once (calibration: keep it still for ~3 s); afterwards the session
  stays open, so sending commands does NOT reset the board or drop its Bluetooth link.
* Every received line is appended to --log as "[HH:MM:SS.mmm] line".
* Commands: append characters to --cmd; the script sends every new byte to the board.
  Firmware understands '+' (gain x1.2), '-' (gain /1.2), '?' (print gain). Stop with the single word STOP.
"""
import argparse
import os
import threading
import time

import serial


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", required=True)
    ap.add_argument("--baud", type=int, default=115200)
    ap.add_argument("--log", required=True)
    ap.add_argument("--cmd", required=True)
    ap.add_argument("--max-seconds", type=float, default=3 * 3600)
    a = ap.parse_args()

    open(a.cmd, "a").close()
    pos = os.path.getsize(a.cmd)

    ser = serial.serial_for_url(a.port, do_not_open=True)
    ser.baudrate = a.baud
    ser.timeout = 0.2
    ser.open()
    ser.dtr = False
    ser.rts = False

    stop = threading.Event()

    def reader():
        with open(a.log, "a", encoding="utf-8", errors="replace", newline="\n") as fp:
            fp.write(f"# gain_tuner start {time.strftime('%Y-%m-%d %H:%M:%S')} port={a.port}\n")
            while not stop.is_set():
                try:
                    raw = ser.readline()
                except Exception as exc:  # link dropped
                    fp.write(f"# serial error: {exc}\n")
                    fp.flush()
                    stop.set()
                    return
                if raw:
                    now = time.time()
                    stamp = time.strftime("%H:%M:%S", time.localtime(now)) + f".{int((now % 1) * 1000):03d}"
                    fp.write(f"[{stamp}] {raw.decode('utf-8', 'replace').rstrip()}\n")
                    fp.flush()

    t = threading.Thread(target=reader, daemon=True)
    t.start()
    t0 = time.time()
    try:
        while not stop.is_set() and time.time() - t0 < a.max_seconds:
            time.sleep(0.2)
            size = os.path.getsize(a.cmd)
            if size > pos:
                with open(a.cmd, "rb") as fp:
                    fp.seek(pos)
                    data = fp.read(size - pos)
                pos = size
                if b"STOP" in data.upper():
                    break
                ser.write(bytes(c for c in data if chr(c) in "+-?"))
    finally:
        stop.set()
        time.sleep(0.4)
        ser.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
