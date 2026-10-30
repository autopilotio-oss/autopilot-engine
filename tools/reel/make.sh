#!/usr/bin/env bash
# Builds one voiced reel from a spec: bash tools/reel/make.sh <spec>  ->  docs/media/reels/money-<spec>.mp4 + poster
set -euo pipefail
N="$1"; ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
python "$ROOT/scripts/tts.py" "$N"
cd "$ROOT/tools/reel"
python build.py "$N"
python mix.py "$N"
node rend.js "$N"
bash mux.sh "$N" "$N"
mkdir -p "$ROOT/docs/media/reels"
mv "AUTOPILOT.OI $N.mp4" "$ROOT/docs/media/reels/money-$N.mp4"
ffmpeg -v error -y -ss 1.2 -i "$ROOT/docs/media/reels/money-$N.mp4" -frames:v 1 -q:v 3 "$ROOT/docs/media/reels/money-$N-poster.jpg"
rm -f "$N.wav" "${N}_bed.wav" "${N}_silent.mp4" "$N.html" "$N.meta.json"
echo "reel ready: money-$N.mp4"
