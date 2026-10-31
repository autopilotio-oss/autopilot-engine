#!/usr/bin/env bash
# bash tools/series/make.sh <ep> [--fake]  ->  docs/media/series/<ep>.mp4 + <ep>-poster.jpg
set -euo pipefail
EP="$1"; ROOT="$(cd "$(dirname "$0")/../.." && pwd)"; S="$ROOT/tools/series"
python3 "$S/tts_ts.py" "$EP" ${2:-}
python3 "$S/build.py" "$EP"; python3 "$S/mix.py" "$EP"
(cd "$ROOT/tools" && python3 -m http.server 8777 >/dev/null 2>&1 & echo $! > /tmp/srv.pid); sleep 1
node "$S/rend.js" "series/$EP.html" "$S/${EP}_silent.mp4"; kill "$(cat /tmp/srv.pid)" || true
mkdir -p "$ROOT/docs/media/series"
ffmpeg -v error -y -i "$S/${EP}_silent.mp4" -i "$S/${EP}_mix.wav" -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest "$ROOT/docs/media/series/$EP.mp4"
ffmpeg -v error -y -ss 1.0 -i "$ROOT/docs/media/series/$EP.mp4" -frames:v 1 -q:v 3 "$ROOT/docs/media/series/$EP-poster.jpg"
rm -f "$S/$EP.wav" "$S/${EP}_mix.wav" "$S/${EP}_silent.mp4" "$S/$EP.html" "$S/$EP.meta.json"
echo "episode ready: $EP"
