#!/usr/bin/env bash
# Master ecosystem film. Each step runs alone (CI renders chunks in parallel):
#   bash tools/master_film/make.sh prep <cut> [--fake]      -> voice + <cut>.html + <cut>_mix.wav
#   CUT=<cut> RANGE=k/n bash tools/master_film/make.sh chunk -> tools/master_film/<cut>_chunk_k.mp4
#   bash tools/master_film/make.sh final <cut>               -> tools/master_film/out/<cut>_4k.mp4, <cut>_1080.mp4, poster
# cuts: master (about 3 min), c60, c30. 3840x2160, 24 fps.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"; H="$ROOT/tools/master_film"; MODE="${1:-}"
serve(){ (cd "$ROOT" && python3 -m http.server 8778 >/dev/null 2>&1 & echo $! > /tmp/srv.pid); sleep 1; }
case "$MODE" in
  prep) python3 "$H/voice.py" "$2" ${3:-}; python3 "$H/build.py" "$2"; python3 "$H/mix.py" "$2";;
  chunk) serve; K="${RANGE%/*}"; node "$H/rend.js" "tools/master_film/$CUT.html" "$H/${CUT}_chunk_$K.mp4"; kill "$(cat /tmp/srv.pid)" || true;;
  final) C="$2"; mkdir -p "$H/out"
    ls "$H"/${C}_chunk_*.mp4 | sort -V | sed "s#^#file '#; s#\$#'#" > "$H/chunks.txt"
    ffmpeg -v error -y -f concat -safe 0 -i "$H/chunks.txt" -c copy "$H/${C}_silent.mp4"
    ffmpeg -v error -y -i "$H/${C}_silent.mp4" -i "$H/${C}_mix.wav" -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -shortest -movflags +faststart "$H/out/${C}_4k.mp4"
    ffmpeg -v error -y -i "$H/out/${C}_4k.mp4" -vf scale=1920:1080:flags=lanczos -c:v libx264 -preset veryfast -crf 21 -c:a copy -movflags +faststart "$H/out/${C}_1080.mp4"
    ffmpeg -v error -y -ss 9 -i "$H/out/${C}_4k.mp4" -frames:v 1 -q:v 3 "$H/out/${C}_poster.jpg"
    echo "film ready: $C";;
esac
