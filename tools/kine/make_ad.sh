#!/usr/bin/env bash
# Ad pipeline: voice -> build -> mix -> alpha graphics (parallel) -> composite over the Seedance plates.
#   bash tools/kine/make_ad.sh <stem> [parallel=4]   (FAKE=1 for a silent timing preview, no voice spend)
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"; K="$ROOT/tools/kine"; EP="$1"; P="${2:-4}"
mkdir -p "$K/out"
if [ -z "${FAKE:-}" ] && [ -f "$K/voice/$EP.wav" ]; then cp "$K/voice/$EP.wav" "$K/voice/$EP.words.json" "$K/out/"; echo "reusing saved voice"
else python3 "$K/voice.py" "$EP" ${FAKE:+--fake}; fi
python3 "$K/build_ad.py" "$EP"; python3 "$K/mix.py" "$EP"
(cd "$ROOT" && python3 -m http.server 8778 >/dev/null 2>&1 & echo $! > "/tmp/kad_$EP.pid"); sleep 1
for i in $(seq 0 $((P - 1))); do (cd "$ROOT" && RANGE="$i/$P" node tools/kine/rend_alpha.js "tools/kine/out/$EP.html" "$K/out/${EP}_a$i.mov") & done; wait
kill "$(cat "/tmp/kad_$EP.pid")" 2>/dev/null || true
for i in $(seq 0 $((P - 1))); do echo "file '$K/out/${EP}_a$i.mov'"; done > "$K/out/${EP}_a.txt"
ffmpeg -v error -y -f concat -safe 0 -i "$K/out/${EP}_a.txt" -c copy "$K/out/${EP}_ov.mov"
mkdir -p "$ROOT/docs/media/ads"
python3 "$K/compose.py" "$EP" "$K/out/${EP}_ov.mov" "$ROOT/docs/media/ads/$EP.mp4"
ffmpeg -v error -y -ss 0.2 -i "$ROOT/docs/media/ads/$EP.mp4" -frames:v 1 -q:v 3 "$ROOT/docs/media/ads/$EP-poster.jpg"
rm -f "$K/out/${EP}_a"*.mov "$K/out/${EP}_a.txt" "$K/out/${EP}_ov.mov"
echo "ad ready: docs/media/ads/$EP.mp4"
