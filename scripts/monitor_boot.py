# -*- coding: utf-8 -*-
"""
scripts/monitor_boot.py
Monitors COM8 at 115200 baud, prints incoming bytes and logs to raw_logs/com8_boot.log
"""

import sys
import time
import os
import serial

PORT = 'COM8'
BAUD = 115200
TIMEOUT = 0.2
LOG_FILE = 'raw_logs/com8_boot.log'
DURATION = 60 # seconds

def main():
    duration = DURATION
    if len(sys.argv) > 1:
        try:
            duration = float(sys.argv[1])
        except ValueError:
            pass

    print(f"Opening {PORT} at {BAUD} baud (Duration: {duration}s)...")
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    
    try:
        ser = serial.Serial(PORT, BAUD, timeout=TIMEOUT)
    except Exception as e:
        print(f"ERROR: Could not open {PORT}: {e}")
        sys.exit(1)

    print(f"{PORT} opened successfully. Listening for data...")
    start_time = time.time()
    total_bytes = 0

    with open(LOG_FILE, 'w', encoding='utf-8', errors='replace') as log_fp:
        log_fp.write(f"--- COM8 Monitor Started at {time.strftime('%Y-%m-%d %H:%M:%S')} ---\n")
        log_fp.flush()

        while (time.time() - start_time) < duration:
            try:
                line = ser.readline()
                if line:
                    total_bytes += len(line)
                    now_str = time.strftime('%H:%M:%S')
                    try:
                        text = line.decode('utf-8', errors='replace')
                    except Exception:
                        text = repr(line)
                    sys.stdout.write(f"[{now_str}] {text}")
                    sys.stdout.flush()
                    log_fp.write(f"[{now_str}] {text}")
                    log_fp.flush()
            except serial.SerialException as e:
                print(f"\nSerial exception: {e}")
                break
            except Exception as e:
                print(f"\nUnexpected error: {e}")
                break

        log_fp.write(f"\n--- Monitor finished. Total bytes received: {total_bytes} ---\n")
        log_fp.flush()

    ser.close()
    print(f"\nMonitor closed. Total bytes received: {total_bytes}. Saved to {LOG_FILE}")

if __name__ == '__main__':
    main()
