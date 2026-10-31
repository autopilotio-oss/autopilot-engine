"""python tools/demo/build.py <ep>  ->  tools/demo/<ep>.html + <ep>.meta.json  (needs <ep>.words.json)"""
import os, sys, json, re
D = os.path.dirname(os.path.abspath(__file__)); ep = sys.argv[1]
E = json.load(open(f"{D}/eps/{ep}.json")); W = json.load(open(f"{D}/{ep}.words.json"))
beats, i = [], 0
for b in E["beats"]:
    n = len(b["say"].split()); ws = W[i:i + n]; i += n
    beats.append({k: v for k, v in b.items() if k != "say"} | {"s": ws[0][1], "e": ws[-1][2]})
dur = round(beats[-1]["e"] + 2.2, 2)
cta = beats[-1]["s"]
data = {"beats": beats, "dur": dur, "cta": cta, "ep": {k: v for k, v in E.items() if k != "beats"}}
html = open(f"{D}/engine.html").read().replace("/*DATA*/null", json.dumps(data))
open(f"{D}/{ep}.html", "w").write(html)
json.dump({"dur": dur, "cuts": [b["s"] for b in beats[1:]], "beats": beats}, open(f"{D}/{ep}.meta.json", "w"))
print("built", ep, dur, "s")
