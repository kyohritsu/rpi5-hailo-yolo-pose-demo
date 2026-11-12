# Third-Party Notices

This repository contains project-specific launcher and integration code only.
Third-party software, models and binaries are **not redistributed** in this repository.

## Hailo Apps

Upstream:
https://github.com/hailo-ai/hailo-apps

Hailo Apps is distributed by Hailo under the MIT License according to the
upstream repository.

This project expects Hailo Apps to be installed separately and imports its
Python/GStreamer helper modules at runtime.

No copy of the Hailo Apps source tree is included here.

## HailoRT / TAPPAS / Hailo model resources

HailoRT, Hailo TAPPAS, post-processing shared libraries and HEF model files
are not included.

They must be obtained and installed according to Hailo's official
documentation and applicable license terms.

Typical external runtime resources referenced by this project include:

- `yolov8s.hef`
- `yolov8s_pose.hef`
- `libyolo_hailortpp_postprocess.so`
- `libyolov8pose_postprocess.so`

These names are references only.

## Ultralytics YOLO

Upstream licensing information:
https://www.ultralytics.com/license

The default detection and pose resources used by this demo are based on
YOLOv8 family models.

Ultralytics currently states that its YOLO code/models are offered under
AGPL-3.0 or an Enterprise License, and that projects using the AGPL option
must comply with the AGPL-3.0 open-source requirements.

For that reason, this repository is released under AGPL-3.0.

If an Enterprise License or a differently licensed model is used, consult
the applicable license terms before changing the licensing of this project.

## Raspberry Pi

Raspberry Pi OS, firmware, drivers and AI HAT+ related system components are
installed separately. Their respective licenses remain with their copyright
holders.

## No legal advice

This notice is provided for project hygiene and attribution only and is not
legal advice. Confirm current upstream license terms before redistribution,
commercial deployment, or publication of trained/compiled models.
