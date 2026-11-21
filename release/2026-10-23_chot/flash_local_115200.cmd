@echo off
rem SLOW variant (115200 baud) of flash_local.cmd. Usage: flash_local_115200.cmd COM20
rem Close any program using the port first (e.g. the RFC2217 server: Ctrl+C in its window).
if "%~1"=="" (echo Usage: flash_local_115200.cmd COMx & exit /b 1)
cd /d "%~dp0"
python -m esptool --chip esp32 -p %1 -b 115200 --before default-reset --after hard-reset write-flash -z --flash-mode dio --flash-freq 40m --flash-size 4MB 0x1000 bootloader.bin 0x8000 partitions.bin 0xe000 boot_app0.bin 0x10000 firmware.bin

