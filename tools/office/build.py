"""Build tools/hq/hq.html (+ hq.meta.json for the mix) from script.json + hq.words.json"""
import os, json, re
D = os.path.dirname(os.path.abspath(__file__))
S = json.load(open(f"{D}/script.json")); W = json.load(open(f"{D}/hq.words.json"))
norm = lambda x: re.sub(r"[^a-z0-9]", "", x.lower())
beats, i = [], 0
for b in S["beats"]:
    n = len(b["say"].split()); ws = W[i:i + n]; i += n
    beats.append({"cam": b["cam"], "s": ws[0][1], "e": ws[-1][2]})
# caption words with display replacements (longest match first)
maps = sorted(S["show"], key=lambda m: -len(m))
cap, k = [], 0
while k < len(W):
    for m in maps:
        seq = m[:-1]
        if [norm(w[0]) for w in W[k:k + len(seq)]] == [norm(x) for x in seq]:
            tail = W[k + len(seq) - 1][0]; p = tail[-1] if tail[-1] in ".,!?" and "." not in m[-1] else ""
            cap.append([m[-1] + p, W[k][1], W[k + len(seq) - 1][2]]); k += len(seq); break
    else:
        cap.append(W[k]); k += 1
cta = next((w[1] for w in W if norm(w[0]) == "want" and w[1] >= beats[-1]["s"]), beats[-1]["e"] - 4)
dur = round(beats[-1]["e"] + 2.6, 2)
data = {"beats": beats, "words": cap, "cta": cta, "dur": dur, "title": S["title"]}
html = open(f"{D}/engine.html").read().replace("/*DATA*/null", json.dumps(data))
open(f"{D}/hq.html", "w").write(html)
json.dump({"dur": dur, "cuts": [b["s"] for b in beats[1:]] + [cta], "beats": beats}, open(f"{D}/hq.meta.json", "w"))
print("built hq.html", dur, "s,", len(beats), "beats")
