"""Join a film spec with its voice timings -> tools/ink/out/<stem>.film.json
python3 tools/ink/build.py <stem>"""
import json, os, sys
D = os.path.dirname(os.path.abspath(__file__))
stem = sys.argv[1]
F = json.load(open(f"{D}/films/{stem}.json"))
W = json.load(open(f"{D}/out/{stem}.words.json"))
i = 0
for b in F["beats"]:
    n = len(b["say"].split())
    b["words"] = W[i:i + n]; i += n
if i != len(W): print(f"warning: {len(W)} voiced words, {i} in the script")
F["dur"] = round(W[-1][2] + F.get("tail", 3.0), 3)
json.dump(F, open(f"{D}/out/{stem}.film.json", "w"))
print("film", stem, "dur", F["dur"], "beats", len(F["beats"]), "words", len(W))
