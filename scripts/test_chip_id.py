# -*- coding: utf-8 -*-
"""
scripts/test_chip_id.py
Runs esptool chip-id with extended connect attempts (30 attempts ~ 45s).
Logs output to raw_logs/esptool_chip_id.log
"""

import subprocess
import sys
import os

LOG_FILE = 'raw_logs/esptool_chip_id.log'

def main():
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    cmd = ['esptool', '--port', 'COM8', '--connect-attempts', '30', 'chip-id']
    print(f"Executing: {' '.join(cmd)}")
    print("Waiting for ESP32 bootloader sync...")
    
    proc = subprocess.run(cmd, capture_output=True, text=True)
    
    with open(LOG_FILE, 'w', encoding='utf-8', errors='replace') as fp:
        fp.write("=== STDOUT ===\n")
        fp.write(proc.stdout)
        fp.write("\n=== STDERR ===\n")
        fp.write(proc.stderr)
        fp.write(f"\nExit code: {proc.returncode}\n")
        
    print(proc.stdout)
    if proc.stderr:
        print(proc.stderr)
    print(f"Finished with exit code: {proc.returncode}. Log saved to {LOG_FILE}")
    sys.exit(proc.returncode)

if __name__ == '__main__':
    main()
