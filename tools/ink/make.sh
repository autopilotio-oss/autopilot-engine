#!/usr/bin/env bash
# Ink film: voice -> build -> render (parallel) -> sound -> mux. Output docs/media/ink/<stem>.mp4 + poster jpg.
#   bash tools/ink/make.sh <stem> [parallel=4]   (FAKE=1 for a silent timing preview, no voice spend)
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"; K="$ROOT/tools/ink"; EP="$1"; P="${2:-4}"
mkdir -p "$K/out" "$ROOT/docs/media/ink"
if [ -z "${FAKE:-}" ] && [ -f "$K/voice/$EP.wav" ]; then cp "$K/voice/$EP.wav" "$K/voice/$EP.words.json" "$K/out/"; echo "reusing saved voice"
else python3 "$K/voice.py" "$EP" ${FAKE:+--fake}; fi
python3 "$K/build.py" "$EP"
(cd "$ROOT" && python3 -m http.server 8779 >/dev/null 2>&1 & echo $! > "/tmp/ink_$EP.pid"); sleep 1
for i in $(seq 0 $((P - 1))); do (cd "$ROOT" && RANGE="$i/$P" node tools/ink/render.js "$EP" "$K/out/${EP}_p$i.mp4") & done; wait
kill "$(cat "/tmp/ink_$EP.pid")" 2>/dev/null || true
cp "$K/out/${EP}_p0.tl.json" "$K/out/${EP}_v.tl.json"
for i in $(seq 0 $((P - 1))); do echo "file '$K/out/${EP}_p$i.mp4'"; done > "$K/out/${EP}_p.txt"
ffmpeg -v error -y -f concat -safe 0 -i "$K/out/${EP}_p.txt" -c copy "$K/out/${EP}_v.mp4"
python3 "$K/mix.py" "$EP"
ffmpeg -v error -y -i "$K/out/${EP}_v.mp4" -i "$K/out/${EP}_mix.wav" -map 0:v -map 1:a -c:v libx264 -preset slow -crf 22 -maxrate 3500k -bufsize 7000k -pix_fmt yuv420p \
  -af "loudnorm=I=-14:TP=-1.5:LRA=9" -c:a aac -b:a 192k -ar 44100 -shortest -movflags +faststart "$ROOT/docs/media/ink/$EP.mp4"
ffmpeg -v error -y -ss 0.4 -i "$ROOT/docs/media/ink/$EP.mp4" -frames:v 1 -q:v 3 "$ROOT/docs/media/ink/$EP-poster.jpg"
rm -f "$K/out/${EP}_p"*
echo "ink film ready: docs/media/ink/$EP.mp4"
