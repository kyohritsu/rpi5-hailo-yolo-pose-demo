#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

HAILO_APPS_DIR="${HAILO_APPS_DIR:-/home/kyohritsu/hailo-apps/hailo-apps}"
CAMERA="${CAMERA:-/dev/video0}"
WIDTH="${WIDTH:-640}"
HEIGHT="${HEIGHT:-480}"
MIRROR="${MIRROR:-1}"

cd "$HAILO_APPS_DIR"
# shellcheck disable=SC1091
source setup_env.sh

export CAMERA WIDTH HEIGHT MIRROR
exec python "$REPO_DIR/app/detect_pose.py"
