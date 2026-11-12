#!/usr/bin/env bash
# Rebuilds every PDF and the web app data for every device in devices/. Run from the repo root.
# Pass device ids to build only those, e.g. ./build.sh sp404mk2
set -euo pipefail
cd "$(dirname "$0")/tools"
python3 build.py "$@"
