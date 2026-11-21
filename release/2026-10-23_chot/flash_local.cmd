@echo off
rem Flash the Air Mouse firmware (built 2026-10-23 (code review final, firmware.bin SHA-256 starts 46B47DBC53252988)) directly over USB. Usage: flash_local.cmd COM20
rem Close any program using the port first (e.g. the RFC2217 server: Ctrl+C in its window).
if "%~1"=="" (echo Usage: flash_local.cmd COMx & exit /b 1)
cd /d "%~dp0"
python -m esptool --chip esp32 -p %1 -b 460800 --before default-reset --after hard-reset write-flash -z --flash-mode dio --flash-freq 40m --flash-size 4MB 0x1000 bootloader.bin 0x8000 partitions.bin 0xe000 boot_app0.bin 0x10000 firmware.bin


