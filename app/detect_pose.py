#!/usr/bin/env python3
"""
Raspberry Pi 5 + AI HAT+ (Hailo-8L)
USB camera / object detection + pose estimation demo.

This file contains only project-specific glue code.
Hailo Apps, HEF models and Hailo post-process libraries are external dependencies.
"""

import os
import sys
from pathlib import Path

import gi
gi.require_version("Gst", "1.0")
from gi.repository import Gst, GLib

from hailo_apps.python.core.gstreamer.gstreamer_helper_pipelines import (
    INFERENCE_PIPELINE,
    INFERENCE_PIPELINE_WRAPPER,
)

CAMERA = os.getenv("CAMERA", "/dev/video0")
WIDTH = int(os.getenv("WIDTH", "640"))
HEIGHT = int(os.getenv("HEIGHT", "480"))
MIRROR = os.getenv("MIRROR", "1").lower() not in {"0", "false", "no", "off"}

RESOURCE_ROOT = Path("/usr/local/hailo/resources")

DETECTION_HEF = os.getenv(
    "DETECTION_HEF",
    str(RESOURCE_ROOT / "models/hailo8l/yolov8s.hef"),
)
POSE_HEF = os.getenv(
    "POSE_HEF",
    str(RESOURCE_ROOT / "models/hailo8l/yolov8s_pose.hef"),
)
DETECTION_SO = os.getenv(
    "DETECTION_SO",
    str(RESOURCE_ROOT / "so/libyolo_hailortpp_postprocess.so"),
)
POSE_SO = os.getenv(
    "POSE_SO",
    str(RESOURCE_ROOT / "so/libyolov8pose_postprocess.so"),
)


def require_file(path: str, description: str) -> None:
    if not Path(path).is_file():
        print(f"ERROR: {description} not found: {path}", file=sys.stderr)
        sys.exit(2)


for path, desc in (
    (DETECTION_HEF, "Detection HEF"),
    (POSE_HEF, "Pose HEF"),
    (DETECTION_SO, "Detection post-process library"),
    (POSE_SO, "Pose post-process library"),
):
    require_file(path, desc)

if not Path(CAMERA).exists():
    print(f"ERROR: Camera device not found: {CAMERA}", file=sys.stderr)
    sys.exit(2)

Gst.init(None)

detection_inner = INFERENCE_PIPELINE(
    hef_path=DETECTION_HEF,
    post_process_so=DETECTION_SO,
    post_function_name="filter_letterbox",
    batch_size=1,
    name="object_detection",
)

detection_pipeline = INFERENCE_PIPELINE_WRAPPER(
    detection_inner,
    name="object_detection_wrapper",
)

pose_inner = INFERENCE_PIPELINE(
    hef_path=POSE_HEF,
    post_process_so=POSE_SO,
    post_function_name="filter_letterbox",
    batch_size=1,
    name="pose_estimation",
)

pose_pipeline = INFERENCE_PIPELINE_WRAPPER(
    pose_inner,
    name="pose_estimation_wrapper",
)

mirror_stage = "videoflip method=horizontal-flip !" if MIRROR else ""

pipeline_string = f"""
v4l2src device={CAMERA} !
queue max-size-buffers=3 leaky=downstream !
videoconvert !
{mirror_stage}
videoscale !
video/x-raw,format=RGB,width={WIDTH},height={HEIGHT} !
{detection_pipeline} !
{pose_pipeline} !
queue max-size-buffers=3 leaky=downstream !
hailooverlay !
videoconvert !
autovideosink sync=false
"""

print("Raspberry Pi 5 / Hailo-8L Detection + Pose Demo")
print(f"Camera : {CAMERA}")
print(f"Size   : {WIDTH}x{HEIGHT}")
print(f"Mirror : {MIRROR}")

try:
    pipeline = Gst.parse_launch(pipeline_string)
except GLib.Error as exc:
    print(f"ERROR: Failed to create GStreamer pipeline: {exc}", file=sys.stderr)
    sys.exit(1)

loop = GLib.MainLoop()
bus = pipeline.get_bus()
bus.add_signal_watch()


def on_message(_bus, message, main_loop):
    if message.type == Gst.MessageType.EOS:
        main_loop.quit()
    elif message.type == Gst.MessageType.ERROR:
        err, debug = message.parse_error()
        print(f"GStreamer ERROR: {err}", file=sys.stderr)
        if debug:
            print(debug, file=sys.stderr)
        main_loop.quit()


bus.connect("message", on_message, loop)
pipeline.set_state(Gst.State.PLAYING)

try:
    loop.run()
except KeyboardInterrupt:
    pass
finally:
    pipeline.set_state(Gst.State.NULL)
