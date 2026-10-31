#!/usr/bin/env bash
# Office video. Steps (each can run alone, CI runs render chunks in parallel):
#   bash tools/office/make.sh prep [--fake]   -> voice + hq.html + hq_mix.wav
#   RANGE=k/n bash tools/office/make.sh chunk -> tools/office/chunk_k.mp4
#   bash tools/office/make.sh final           -> docs/media/office/office.mp4 + poster
#   bash tools/office/make.sh all [--fake]    -> everything in one go
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"; H="$ROOT/tools/office"; MODE="${1:-all}"
prep(){ python3 "$H/voice.py" ${1:-}; python3 "$H/build.py"; python3 "$H/mix.py"; }
serve(){ (cd "$ROOT" && python3 -m http.server 8778 >/dev/null 2>&1 & echo $! > /tmp/srv.pid); sleep 1; }
chunk(){ serve; K="${RANGE%/*}"; node "$H/rend.js" "tools/office/hq.html" "$H/chunk_$K.mp4"; kill "$(cat /tmp/srv.pid)" || true; }
final(){
  ls "$H"/chunk_*.mp4 | sort -V | sed "s#^#file '#; s#\$#'#" > "$H/chunks.txt"
  ffmpeg -v error -y -f concat -safe 0 -i "$H/chunks.txt" -c copy "$H/hq_silent.mp4"
  mkdir -p "$ROOT/docs/media/office"
  ffmpeg -v error -y -i "$H/hq_silent.mp4" -i "$H/hq_mix.wav" -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart "$ROOT/docs/media/office/office.mp4"
  ffmpeg -v error -y -ss 1.0 -i "$ROOT/docs/media/office/office.mp4" -frames:v 1 -q:v 3 "$ROOT/docs/media/office/office-poster.jpg"
  echo "office video ready"; }
case "$MODE" in
  prep) prep "${2:-}";; chunk) chunk;; final) final;;
  all) prep "${2:-}"; RANGE=0/1 chunk; final;;
esac
