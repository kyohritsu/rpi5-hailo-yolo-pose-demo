# Raspberry Pi 5 + AI HAT+ (13 TOPS) YOLO / Pose Demo

Raspberry Pi 5 と Raspberry Pi AI HAT+ 13 TOPS (Hailo-8L)、
USB UVC カメラを使用した展示デモ用リポジトリです。

以下を想定しています。

- 物体検知: Hailo Apps `hailo-detect`
- 姿勢推定: Hailo Apps `hailo-pose`
- 物体検知 + 姿勢推定: `app/detect_pose.py`
- USB カメラ: `/dev/video0`
- 鏡像表示対応
- デスクトップからワンクリック起動

## 重要: ライセンス

このリポジトリ自体は **GNU Affero General Public License v3.0 (AGPL-3.0)** で公開します。

理由:
このデモでは Ultralytics YOLOv8 系モデルを利用する構成を想定しています。
Ultralytics は、AGPL-3.0 の条件で利用する場合、関連するプロジェクトを
AGPL-3.0 の条件に従って公開するよう案内しています。

一方、Hailo Apps は MIT License です。
本リポジトリには Hailo Apps 本体、HailoRT、Hailo TAPPAS、
HEF モデル、学習済み重み、第三者バイナリを含めません。

各依存コンポーネントのライセンス条件はそれぞれの配布元で確認してください。
詳細は `THIRD_PARTY_NOTICES.md` を参照してください。

> このリポジトリの公開だけで、あらゆる商用利用・モデル利用の
> ライセンス条件を自動的に満たすことを保証するものではありません。
> 商用利用の場合は各権利者の最新ライセンス条件を確認してください。

## ハードウェア

- Raspberry Pi 5
- Raspberry Pi AI HAT+ 13 TOPS
  - Hailo-8L
- USB UVC カメラ
- HDMI ディスプレイ
- Raspberry Pi 5 公式 27W USB-C 電源推奨

## 前提ソフトウェア

Hailo Apps が Raspberry Pi にインストール済みであること。

標準想定ディレクトリ:

```text
/home/kyohritsu/hailo-apps/hailo-apps
```

環境有効化:

```bash
cd ~/hailo-apps/hailo-apps
source setup_env.sh
```

確認:

```bash
which hailo-detect
hailo-detect --help
hailo-pose --help
```

AI HAT+ の確認:

```bash
hailortcli fw-control identify
```

USB カメラの確認:

```bash
v4l2-ctl --list-devices
```

## 必要なHailoリソース

本リポジトリにはモデルや `.so` を同梱しません。

標準構成では次のファイルをシステム側で使用します。

```text
/usr/local/hailo/resources/models/hailo8l/yolov8s.hef
/usr/local/hailo/resources/models/hailo8l/yolov8s_pose.hef
/usr/local/hailo/resources/so/libyolo_hailortpp_postprocess.so
/usr/local/hailo/resources/so/libyolov8pose_postprocess.so
```

確認:

```bash
ls -lh /usr/local/hailo/resources/models/hailo8l/yolov8s.hef
ls -lh /usr/local/hailo/resources/models/hailo8l/yolov8s_pose.hef
ls -lh /usr/local/hailo/resources/so/libyolo_hailortpp_postprocess.so
ls -lh /usr/local/hailo/resources/so/libyolov8pose_postprocess.so
```

不足している場合は Hailo Apps の公式手順に従ってリソースを取得・生成してください。

## 1. 姿勢推定だけを実行

```bash
cd ~/hailo-apps/hailo-apps
source setup_env.sh

hailo-pose \
  --input /dev/video0 \
  --arch hailo8l \
  --show-fps \
  --horizontal-mirror
```

## 2. 物体検知だけを実行

```bash
cd ~/hailo-apps/hailo-apps
source setup_env.sh

hailo-detect \
  --input /dev/video0 \
  --arch hailo8l \
  --show-fps \
  --horizontal-mirror
```

## 3. 物体検知 + 姿勢推定を1画面で表示

`app/detect_pose.py` を Hailo Apps リポジトリ直下へコピーするか、
このリポジトリから直接実行します。

```bash
cd ~/hailo-apps/hailo-apps
source setup_env.sh

python /path/to/rpi5_hailo_yolo_pose_demo/app/detect_pose.py
```

設定は環境変数で変更できます。

```bash
CAMERA=/dev/video2 WIDTH=1280 HEIGHT=720 MIRROR=1 \
python app/detect_pose.py
```

利用可能な環境変数:

| 変数 | デフォルト | 内容 |
|---|---:|---|
| `CAMERA` | `/dev/video0` | USBカメラ |
| `WIDTH` | `640` | 表示幅 |
| `HEIGHT` | `480` | 表示高さ |
| `MIRROR` | `1` | `1`で左右反転 |
| `DETECTION_HEF` | system resource | 物体検知 HEF |
| `POSE_HEF` | system resource | 姿勢推定 HEF |
| `DETECTION_SO` | system resource | YOLO後処理SO |
| `POSE_SO` | system resource | Pose後処理SO |

## デスクトップからワンクリック起動

このリポジトリを Raspberry Pi 上で任意の場所へ配置した後、

```bash
cd /path/to/rpi5_hailo_yolo_pose_demo
chmod +x scripts/*.sh
./scripts/install_desktop_shortcuts.sh
```

デスクトップに以下が作成されます。

- `姿勢推定デモ`
- `物体検知デモ`
- `物体検知 + 姿勢推定`

デスクトップ環境によっては、初回実行時に
「信頼して起動」「実行を許可」等の操作が必要です。

## 遅延・電源確認

Raspberry Pi 5 + AI HAT+ + USBカメラでは十分な電源を推奨します。

```bash
vcgencmd get_throttled
```

理想:

```text
throttled=0x0
```

温度:

```bash
vcgencmd measure_temp
```

## GitHubへアップする前の確認

以下をリポジトリへ含めないでください。

- `.hef`
- `.pt`
- `.onnx`
- Hailo SDK / TAPPAS のバイナリ
- `venv_hailo_apps/`
- Hailo Apps 本体をコピーしたもの
- USBカメラ撮影データ
- 個人情報・社内情報
- APIキー・認証情報

`.gitignore` で主なバイナリ・モデル類を除外しています。

## 推奨Gitコマンド

```bash
git init
git add .
git status
git commit -m "Initial public release"
git branch -M main
git remote add origin <YOUR_GITHUB_REPOSITORY_URL>
git push -u origin main
```

## Upstream / References

- Hailo Apps:
  https://github.com/hailo-ai/hailo-apps
- Raspberry Pi AI documentation:
  https://www.raspberrypi.com/documentation/computers/ai.html
- Ultralytics licensing:
  https://www.ultralytics.com/license

## Disclaimer

本ソフトウェアはデモ・検証用途を想定しています。
安全性・性能・特定目的への適合性を保証するものではありません。
