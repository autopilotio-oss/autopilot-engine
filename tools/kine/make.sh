#!/usr/bin/env bash
# Kinetic editor: full screen motion graphics cut of a factory reel episode, reusing its saved voice (no voice spend).
#   bash tools/kine/make.sh <stem> [parallel=4]  -> docs/media/$OUT/<id>.mp4 + poster
# Needs: node + playwright, ffmpeg, python3 + numpy. Serves the repo on :8778 while rendering.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"; K="$ROOT/tools/kine"; EP="$1"; P="${2:-4}"
if [ -f "$K/ads/$EP.json" ]; then SRC="$K/ads/$EP.json"; OUT="ads"; [ -f "$K/out/$EP.wav" ] || python3 "$K/voice.py" "$EP" ${FAKE:+--fake}; else SRC="$ROOT/tools/freel/eps/$EP.json"; OUT="kine"; fi
ID=$(python3 -c "import json;print(json.load(open('$SRC'))['id'])")
if python3 -c "import json,sys;sys.exit(0 if 'head' in json.load(open('$SRC'))['beats'][0] else 1)"; then python3 "$K/build_ad.py" "$EP"; else python3 "$K/build.py" "$EP"; fi; python3 "$K/mix.py" "$EP"
(cd "$ROOT" && python3 -m http.server 8778 >/dev/null 2>&1 & echo $! > "/tmp/kine_srv_$EP.pid"); sleep 1
for i in $(seq 0 $((P - 1))); do (cd "$ROOT" && RANGE="$i/$P" node tools/office/rend.js "tools/kine/out/$EP.html" "$K/out/${EP}_c$i.mp4") & done; wait
kill "$(cat "/tmp/kine_srv_$EP.pid")" 2>/dev/null || true
for i in $(seq 0 $((P - 1))); do echo "file '$K/out/${EP}_c$i.mp4'"; done > "$K/out/${EP}_c.txt"
mkdir -p "$ROOT/docs/media/$OUT"
ffmpeg -v error -y -f concat -safe 0 -i "$K/out/${EP}_c.txt" -i "$K/out/${EP}_mix.wav" -map 0:v -map 1:a -c:v libx264 -preset veryfast -crf 21 -pix_fmt yuv420p \
  -af loudnorm=I=-14:TP=-1.5:LRA=11 -c:a aac -b:a 192k -ar 44100 -ac 2 -shortest -movflags +faststart "$ROOT/docs/media/$OUT/$ID.mp4"
ffmpeg -v error -y -ss 0.3 -i "$ROOT/docs/media/$OUT/$ID.mp4" -frames:v 1 -q:v 3 "$ROOT/docs/media/$OUT/$ID-poster.jpg"
rm -f "$K/out/${EP}_c"*.mp4 "$K/out/${EP}_c.txt"
echo "kinetic cut ready: docs/media/$OUT/$ID.mp4"
