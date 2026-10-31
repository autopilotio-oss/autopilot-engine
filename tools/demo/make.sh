#!/usr/bin/env bash
# Robot demo video for one agent (tools/demo/eps/<ep>.json).
#   bash tools/demo/make.sh prep <ep> [--fake]   -> voice + html + mix
#   RANGE=k/n bash tools/demo/make.sh chunk <ep> -> tools/demo/<ep>_chunk_k.mp4
#   bash tools/demo/make.sh final <ep>           -> docs/media/demo/<ep>.mp4 + poster
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"; H="$ROOT/tools/demo"; MODE="$1"; EP="$2"
case "$MODE" in
 prep) python3 "$H/voice.py" "$EP" ${3:-}; python3 "$H/build.py" "$EP"; python3 "$H/mix.py" "$EP";;
 chunk) (cd "$ROOT" && python3 -m http.server 8778 >/dev/null 2>&1 & echo $! > /tmp/srv.pid); sleep 1
   K="${RANGE%/*}"; node "$ROOT/tools/office/rend.js" "tools/demo/$EP.html" "$H/${EP}_chunk_$K.mp4"; kill "$(cat /tmp/srv.pid)" || true;;
 final) ls "$H"/${EP}_chunk_*.mp4 | sort -V | sed "s#^#file '#; s#\$#'#" > "$H/chunks.txt"
   ffmpeg -v error -y -f concat -safe 0 -i "$H/chunks.txt" -c copy "$H/${EP}_silent.mp4"; mkdir -p "$ROOT/docs/media/demo"
   ffmpeg -v error -y -i "$H/${EP}_silent.mp4" -i "$H/${EP}_mix.wav" -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart "$ROOT/docs/media/demo/$EP.mp4"
   ffmpeg -v error -y -ss 1.5 -i "$ROOT/docs/media/demo/$EP.mp4" -frames:v 1 -q:v 3 "$ROOT/docs/media/demo/$EP-poster.jpg"; echo "demo ready: $EP";;
esac
