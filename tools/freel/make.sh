#!/usr/bin/env bash
# Factory reels (split screen: 3D factory on top, the agent's work below).
#   bash tools/freel/make.sh prep <stem> [--fake]   -> voice + <stem>.html + <stem>_mix.wav
#   RANGE=k/n bash tools/freel/make.sh chunk <stem> -> tools/freel/<stem>_chunk_k.mp4
#   bash tools/freel/make.sh final <stem>           -> docs/media/freel/<id>.mp4 + poster (TikTok safe audio)
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"; H="$ROOT/tools/freel"; MODE="$1"; EP="$2"
ID=$(python3 -c "import json;print(json.load(open('$H/eps/$EP.json'))['id'])")
prep(){ python3 "$H/voice.py" "$EP" ${1:-}; python3 "$H/build.py" "$EP"; python3 "$H/mix.py" "$EP"; }
chunk(){ (cd "$ROOT" && python3 -m http.server 8778 >/dev/null 2>&1 & echo $! > /tmp/srv_$EP.pid); sleep 1
  K="${RANGE%/*}"
  node "$ROOT/tools/office/rend.js" "tools/freel/$EP.html" "$H/${EP}_chunk_$K.mp4"; kill "$(cat /tmp/srv_$EP.pid)" || true; }
final(){
  ls "$H"/${EP}_chunk_*.mp4 | sort -V | sed "s#^#file '#; s#\$#'#" > "$H/${EP}_chunks.txt"
  ffmpeg -v error -y -f concat -safe 0 -i "$H/${EP}_chunks.txt" -c copy "$H/${EP}_silent.mp4"
  mkdir -p "$ROOT/docs/media/freel"
  ffmpeg -v error -y -i "$H/${EP}_silent.mp4" -i "$H/${EP}_mix.wav" -map 0:v -map 1:a -c:v copy -af loudnorm=I=-14:TP=-1.5:LRA=11 -c:a aac -b:a 192k -ar 44100 -ac 2 -shortest -movflags +faststart "$ROOT/docs/media/freel/$ID.mp4"
  ffmpeg -v error -y -ss 0.6 -i "$ROOT/docs/media/freel/$ID.mp4" -frames:v 1 -q:v 3 "$ROOT/docs/media/freel/$ID-poster.jpg"
  echo "reel ready: docs/media/freel/$ID.mp4"; }
case "$MODE" in prep) prep "${3:-}";; chunk) chunk;; final) final;; esac
