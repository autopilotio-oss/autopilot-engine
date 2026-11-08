#!/usr/bin/env bash
# Render a time window of an ink film with its real mix: bash tools/ink/clip.sh <stem> <t0> <t1> <out name> [extra query, e.g. hand=1]
# Expects out/<stem>.wav + words.json already in place (voice.py, or copied from tools/ink/voice + pace.py).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"; K="$ROOT/tools/ink"; EP="$1"; T0="$2"; T1="$3"; NAME="$4"; P=4
python3 "$K/build.py" "$EP" >/dev/null
(cd "$ROOT" && python3 -m http.server 8779 >/dev/null 2>&1 & echo $! > "/tmp/inkc_$EP.pid"); sleep 1
for i in $(seq 0 $((P - 1))); do (cd "$ROOT" && T0=$T0 T1=$T1 RANGE="$i/$P" node tools/ink/render.js "$EP" "$K/out/${NAME}_p$i.mp4" >/dev/null) & done; wait
kill "$(cat "/tmp/inkc_$EP.pid")" 2>/dev/null || true
cp "$K/out/${NAME}_p0.tl.json" "$K/out/${EP}_v.tl.json"
for i in $(seq 0 $((P - 1))); do echo "file '$K/out/${NAME}_p$i.mp4'"; done > "$K/out/${NAME}_p.txt"
ffmpeg -v error -y -f concat -safe 0 -i "$K/out/${NAME}_p.txt" -c copy "$K/out/${NAME}_v.mp4"
python3 "$K/mix.py" "$EP" >/dev/null
mkdir -p "$ROOT/docs/media/ink/tests"
ffmpeg -v error -y -i "$K/out/${NAME}_v.mp4" -ss "$T0" -t "$(python3 -c "print($T1-$T0)")" -i "$K/out/${EP}_mix.wav" -map 0:v -map 1:a \
  -c:v libx264 -preset slow -crf 20 -pix_fmt yuv420p -af "loudnorm=I=-14:TP=-1.5:LRA=9" -c:a aac -b:a 192k -ar 44100 -shortest -movflags +faststart "$ROOT/docs/media/ink/tests/$NAME.mp4"
rm -f "$K/out/${NAME}_p"*
echo "clip ready: docs/media/ink/tests/$NAME.mp4"
