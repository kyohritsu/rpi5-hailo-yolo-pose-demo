#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
DESKTOP_DIR="${HOME}/Desktop"

mkdir -p "$DESKTOP_DIR"

make_desktop() {
    local src="$1"
    local dst="$2"
    sed "s|@REPO_DIR@|$REPO_DIR|g" "$src" > "$dst"
    chmod +x "$dst"
}

make_desktop "$REPO_DIR/desktop/PoseDemo.desktop.in" "$DESKTOP_DIR/PoseDemo.desktop"
make_desktop "$REPO_DIR/desktop/DetectDemo.desktop.in" "$DESKTOP_DIR/DetectDemo.desktop"
make_desktop "$REPO_DIR/desktop/DetectPoseDemo.desktop.in" "$DESKTOP_DIR/DetectPoseDemo.desktop"

echo "Desktop shortcuts installed to: $DESKTOP_DIR"
