#!/bin/bash
set -euo pipefail

HAILO_APPS_DIR="${HAILO_APPS_DIR:-/home/kyohritsu/hailo-apps/hailo-apps}"
CAMERA="${CAMERA:-/dev/video0}"

cd "$HAILO_APPS_DIR"
# shellcheck disable=SC1091
source setup_env.sh

exec hailo-detect \
  --input "$CAMERA" \
  --arch hailo8l \
  --show-fps \
  --horizontal-mirror
