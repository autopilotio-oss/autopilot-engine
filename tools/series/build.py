"""Build tools/series/<ep>.html from eps/<ep>.json + <ep>.words.json"""
import json, sys, os, re
D = os.path.dirname(os.path.abspath(__file__)); ep = sys.argv[1]
spec = json.load(open(f"{D}/eps/{ep}.json")); W = json.load(open(f"{D}/{ep}.words.json"))
norm = lambda w: re.sub(r"[^a-z0-9$]", "", w.lower())
beats, k, em = [], 0, []
for b in spec["beats"]:
    n = len(b["say"].split()); w0, w1 = k, k + n; k = w1
    ems = {norm(x) for x in b.get("em", [])}
    em += [norm(W[i][0]) in ems for i in range(w0, min(w1, len(W)))]
    beats.append({"w0": w0, "w1": w1, "scene": b["scene"]})
assert k == len(W), f"word count mismatch: script {k} vs voice {len(W)}"
for i, b in enumerate(beats):
    b["s"] = 0 if i == 0 else max(0, W[b["w0"]][1] - 0.12)
dur = round(W[-1][2] + 1.6, 2)
for i, b in enumerate(beats): b["e"] = beats[i + 1]["s"] if i + 1 < len(beats) else dur
data = {"dur": dur, "day": spec["day"], "words": W, "beats": beats, "em": em}
html = open(f"{D}/engine.html").read().replace("/*DATA*/", json.dumps(data))
open(f"{D}/{ep}.html", "w").write(html); json.dump({"dur": dur, "cuts": [b["s"] for b in beats[1:]], "types": [b["scene"]["type"] for b in beats],
  "typing": [[b["s"], b["e"]] for b in beats if b["scene"]["type"] == "prompt"]}, open(f"{D}/{ep}.meta.json", "w"))
print(ep, "dur", dur, "beats", len(beats))
