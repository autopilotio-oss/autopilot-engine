"""python tools/master_film/build.py <cut>  -> <cut>.html + <cut>.meta.json from script.json, truth.json, <cut>.words.json"""
import os, sys, json, re
D = os.path.dirname(os.path.abspath(__file__)); cut = sys.argv[1]
S = json.load(open(f"{D}/script.json"))["cuts"][cut]; W = json.load(open(f"{D}/{cut}.words.json")); TR = json.load(open(f"{D}/truth.json"))
norm = lambda x: re.sub(r"[^a-z0-9]", "", x.lower())
beats, i = [], 0
for b in S:
    n = len(b["say"].split()); ws = W[i:i + n]; i += n
    beats.append({"scene": b["scene"], "s": ws[0][1], "e": ws[-1][2]})
show = [["Autopilot", "O.I.", "AUTOPILOT.OI"], ["Autopilot", "OI", "AUTOPILOT.OI"]]
cap, k = [], 0
while k < len(W):
    for m in show:
        seq = m[:-1]
        if [norm(w[0]) for w in W[k:k + len(seq)]] == [norm(x) for x in seq]:
            tail = W[k + len(seq) - 1][0]; p = tail[-1] if tail[-1] in ".,!?" else ""
            cap.append([m[-1] + p, W[k][1], W[k + len(seq) - 1][2]]); k += len(seq); break
    else:
        cap.append(W[k]); k += 1
tail = {"master": 6.0, "c60": 4.0, "c30": 3.5}[cut]
dur = round(beats[-1]["e"] + tail, 2)
data = {"beats": beats, "words": cap, "dur": dur, "truth": TR, "cut": cut}
open(f"{D}/{cut}.html", "w").write(open(f"{D}/engine.html").read().replace("/*DATA*/null", json.dumps(data)))
json.dump({"dur": dur, "cuts": [b["s"] for b in beats[1:]], "beats": beats}, open(f"{D}/{cut}.meta.json", "w"))
print("built", cut, dur, "s,", len(beats), "beats")
