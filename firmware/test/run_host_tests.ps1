# Build and run the host (PC) unit tests. Portable core only: every src\*.cpp EXCEPT the Arduino app layer (app_*.cpp).
# Usage (PowerShell, from the project root):  .\firmware\test\run_host_tests.ps1
$srcs = Get-ChildItem firmware\src\*.cpp | Where-Object { $_.Name -notlike 'app_*' } | ForEach-Object { $_.FullName }
$out = Join-Path $env:TEMP 'air_mouse_tests.exe'
g++ -std=gnu++20 -Wall -Wextra -I firmware/include firmware/test/test_motion_pipeline.cpp $srcs -o $out
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
& $out
exit $LASTEXITCODE
