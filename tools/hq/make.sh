#!/usr/bin/env bash
# bash tools/hq/make.sh [--fake]  ->  docs/media/hq/hq.mp4 + hq-poster.jpg
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"; H="$ROOT/tools/hq"
python3 "$H/voice.py" ${1:-}; python3 "$H/build.py"; python3 "$H/mix.py"
(cd "$ROOT/tools" && python3 -m http.server 8777 >/dev/null 2>&1 & echo $! > /tmp/srv.pid); sleep 1
node "$ROOT/tools/series/rend.js" "hq/hq.html" "$H/hq_silent.mp4"; kill "$(cat /tmp/srv.pid)" || true
for i in $(seq 1 30); do [ -f "$H/hq_silent.mp4" ] && break; sleep 1; done
mkdir -p "$ROOT/docs/media/hq"
ffmpeg -v error -y -i "$H/hq_silent.mp4" -i "$H/hq_mix.wav" -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart "$ROOT/docs/media/hq/hq.mp4"
ffmpeg -v error -y -ss 0.5 -i "$ROOT/docs/media/hq/hq.mp4" -frames:v 1 -q:v 3 "$ROOT/docs/media/hq/hq-poster.jpg"
rm -f "$H/hq.wav" "$H/hq_mix.wav" "$H/hq_silent.mp4" "$H/hq.html" "$H/hq.meta.json"
echo "hq video ready"
