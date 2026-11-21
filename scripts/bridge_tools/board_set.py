import sys, time, os, hashlib
import serial
URL = "rfc2217://<LAPTOP_IP>:4000?ign_set_control"
OUT = sys.argv[1]; CMDS = sys.argv[2:]
if os.path.exists(OUT): print("exists"); sys.exit(2)
log = open(OUT, "w", encoding="utf-8", newline="\n")
def stamp(s): return "[%s.%03d] %s" % (time.strftime("%H:%M:%S"), int(time.time()*1000) % 1000, s)
ser = serial.serial_for_url(URL, do_not_open=True); ser.baudrate = 115200; ser.timeout = 0.2; ser.open(); ser.dtr = False; ser.rts = False
def pump(sec, until=None):
    end = time.time() + sec; buf = b""; lines = []
    while time.time() < end:
        d = ser.read(256)
        if d:
            buf += d
            while b"\n" in buf:
                ln, buf = buf.split(b"\n", 1); s = ln.decode("utf-8", "replace").rstrip("\r"); lines.append(s); log.write(stamp(s) + "\n")
                if until and until in s: return lines
    return lines
l = pump(25, "Main Loop")
for x in l:
    if "[CONFIG] in use" in x or "ACCEPTED" in x or "REJECTED" in x or "Main Loop" in x: print(x)
pump(1.5)
for c in CMDS:
    log.write(stamp(">>> " + c) + "\n"); ser.write(c.encode() + b"\n")
    for x in pump(1.0):
        if x.startswith("@"): print(f"{c:40s} -> {x}")
ser.close(); log.close()
print("SHA-256", hashlib.sha256(open(OUT, "rb").read()).hexdigest())
