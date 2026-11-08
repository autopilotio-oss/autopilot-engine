"""Spread a voiced film to a target length by adding equal pauses between beats (never stretching the voice itself).
python3 tools/ink/pace.py <stem> <voice_end_seconds>   reads out/<stem>.wav + words.json, rewrites both in place."""
import json, sys, wave, os, numpy as np
D = os.path.dirname(os.path.abspath(__file__)); stem, target = sys.argv[1], float(sys.argv[2])
F = json.load(open(f"{D}/films/{stem}.json")); W = json.load(open(f"{D}/out/{stem}.words.json"))
w = wave.open(f"{D}/out/{stem}.wav"); sr = w.getframerate(); x = np.frombuffer(w.readframes(w.getnframes()), np.int16).copy(); w.close()
counts = [len(b["say"].split()) for b in F["beats"]]; cuts = []; i = 0
for n in counts[:-1]:
    i += n; cuts.append((W[i - 1][2] + W[i][1]) / 2)
extra = max(0.0, target - W[-1][2]); gap = extra / max(1, len(cuts))
segs, out_words, prev, shift, i = [], [], 0.0, 0.0, 0
bounds = cuts + [len(x) / sr]
for k, c in enumerate(bounds):
    segs.append(x[int(prev * sr):int(c * sr)])
    while i < len(W) and W[i][1] < c: out_words.append([W[i][0], round(W[i][1] + shift, 3), round(W[i][2] + shift, 3)]); i += 1
    if k < len(cuts): segs.append(np.zeros(int(gap * sr), np.int16)); shift += gap
    prev = c
y = np.concatenate(segs)
o = wave.open(f"{D}/out/{stem}.wav", "wb"); o.setnchannels(1); o.setsampwidth(2); o.setframerate(sr); o.writeframes(y.tobytes()); o.close()
json.dump(out_words, open(f"{D}/out/{stem}.words.json", "w"))
print(f"paced {stem}: +{gap:.2f}s x {len(cuts)} gaps, voice now ends {out_words[-1][2]:.2f}s, file {len(y)/sr:.2f}s")
