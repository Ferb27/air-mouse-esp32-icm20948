#!/usr/bin/env bash
# Build and run the host (PC) unit tests. Portable core only: every src/*.cpp EXCEPT the Arduino app layer (app_*.cpp).
# Usage (from the project root):  bash firmware/test/run_host_tests.sh
set -e
OUT="${TMPDIR:-/tmp}/air_mouse_tests"
SRCS=$(ls firmware/src/*.cpp | grep -v '/app_')
g++ -std=gnu++20 -Wall -Wextra -I firmware/include firmware/test/test_motion_pipeline.cpp $SRCS -o "$OUT"
"$OUT"
