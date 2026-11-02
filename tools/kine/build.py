"""Kinetic editor: full screen motion graphics cut for factory reel episodes.
Reuses the episode script (tools/freel/eps/<stem>.json) and its saved voice + word timings, so no new voice spend.
  python3 tools/kine/build.py <stem>  -> tools/kine/out/<stem>.html + <stem>.meta.json
Cut: a cold open that shows the payoff on frame 0, the voice's hook as slammed kinetic type,
then each agent step as one big full screen card, light streak transitions, word captions."""
import os, sys, json, re
D = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(D)); FR = f"{ROOT}/tools/freel"
ep = sys.argv[1]; E = json.load(open(f"{FR}/eps/{ep}.json"))
wf = f"{FR}/{ep}.words.json" if os.path.exists(f"{FR}/{ep}.words.json") else f"{FR}/voice/{ep}.words.json"
OFF = float(E.get("cold_open", 0.85))  # seconds of silent payoff before the voice starts
W = [[w, round(s + OFF, 3), round(e + OFF, 3)] for w, s, e in json.load(open(wf))]
NUMW = {"one": "1", "two": "2", "three": "3", "four": "4", "five": "5", "six": "6", "seven": "7", "eight": "8", "nine": "9", "ten": "10",
        "eleven": "11", "twelve": "12", "fifteen": "15", "twenty": "20", "thirty": "30", "fifty": "50", "hundred": "100"}
star = set()
for ln in E.get("hook_lines", []):
    for m in re.findall(r"\*([^*]+)\*", ln): star |= {x.lower() for x in re.findall(r"[a-z0-9$']+", m.lower())}
star |= {x.lower() for x in E.get("emph", [])}
def clean(w): return re.sub(r"[^a-z0-9$'.]", "", w.lower()).strip(".")
def hi(w):
    c = clean(w)
    return bool(c) and (c in NUMW or any(ch.isdigit() for ch in c) or c in star or (len(c) > 4 and any(c.startswith(s[:max(5, len(s) - 2)]) for s in star if len(s) > 4)))
def disp(w):
    c = re.sub(r"[^A-Za-z0-9$'%.,]", "", w).rstrip(".,")
    return NUMW.get(c.lower(), c).upper()
def ends(w): return w[-1:] in ".?!,"

# beats on the shifted clock
beats, i = [], 0
for b in E["beats"]:
    n = len(b["say"].split()); ws = W[i:i + n]; beats.append({"b": b, "ws": ws, "s": ws[0][1], "e": ws[-1][2]}); i += n
dur = round(beats[-1]["e"] + 1.5, 2)

def phrases(ws, maxw=3, iso=True):
    out, cur = [], []
    k = 0
    while k < len(ws):
        w = ws[k]
        if iso and hi(w[0]):
            if cur: out.append(cur); cur = []
            grp = [w]
            if clean(w[0]) in NUMW and k + 1 < len(ws) and not ends(w[0]): grp.append(ws[k + 1]); k += 1
            out.append(grp); k += 1; continue
        cur.append(w)
        if len(cur) >= maxw or ends(w[0]): out.append(cur); cur = []
        k += 1
    if cur: out.append(cur)
    return out

shots, caps, ev, trans, bursts = [], [], [], [], []
first = beats[0]["ws"]
# split beat 0: kinetic type for every sentence but the last, the ask screen for the last one
sent, cur = [], []
for w in first:
    cur.append(w)
    if w[0][-1:] in ".?!": sent.append(cur); cur = []
if cur: sent.append(cur)
if len(sent) == 1: h = max(1, len(first) // 2); sent = [first[:h], first[h:]]
kin = [w for s in sent[:-1] for w in s]; tail = sent[-1]

# payoff for the cold open (episode field wins, else the biggest money figure on screen)
po = E.get("payoff")
if not po:
    big, src = None, ""
    for b in E["beats"]:
        sc = b["screen"]; txt = sc.get("foot", "") + " " + sc.get("text", "")
        for m in re.findall(r"\$[\d,]+(?:\.\d+)?", txt): big, src = m, txt
    po = {"big": (big or "").split(".")[0], "lines": [re.sub(r"\*", "", E.get("hook_lines", E["hook"])[-1])], "tag": "sample data"}
shots.append({"type": "cold", "s": 0, "e": kin[0][1] if kin else tail[0][1], "po": po})
ev.append(["impact", 0.0, 0]); bursts.append({"t": 0.02, "x": 540, "y": 800, "n": 46, "seed": 3})

ph = phrases(kin)
for j, p in enumerate(ph):
    s = p[0][1] - .03; e = ph[j + 1][0][1] - .03 if j + 1 < len(ph) else tail[0][1] - .12
    shots.append({"type": "phrase", "s": round(s, 3), "e": round(e, 3), "words": [[disp(w[0]), hi(w[0])] for w in p], "j": j})
    ev.append(["slam", s, j]);
    if any(hi(w[0]) for w in p) and any(ch.isdigit() for w in p for ch in disp(w[0])): bursts.append({"t": s + .04, "x": 540, "y": 860, "n": 30, "seed": 11 + j})

def screen_shot(sc, s, e, bi):
    L = max(.6, e - s); T = lambda f: round(s + f * L, 3); k = sc["type"]; sh = {"type": k, "s": round(s, 3), "e": round(e, 3), "sc": sc, "bi": bi}
    if k == "ask":
        nf = len(sc.get("files", [])); sh["files_t"] = [T(.04 + i * .08) for i in range(nf)]
        for t in sh["files_t"]: ev.append(["drop", t, 0])
        t0, t1 = (.22 if nf else .06), .78; sh["type_t"] = [T(t0), T(t1)]; n = len(sc["text"])
        for c in range(n):
            if sc["text"][c] != " ": ev.append(["key", T(t0 + (t1 - t0) * (c + 1) / n), c])
        sh["send_t"] = T(t1 + .05); ev.append(["send", sh["send_t"], 0])
        sh["hl"] = [hi(x) for x in sc["text"].split(" ")]
    elif k == "work":
        n = len(sc["lines"]); sh["steps"] = [[T(.1 + .8 * i / (n + .3)), T(.1 + .8 * (i + .8) / (n + .3))] for i in range(n)]
        for i, (a, d) in enumerate(sh["steps"]): ev.append(["blip", a, i]); ev.append(["tick", d, i])
    elif k == "table":
        n = len(sc["rows"]); sh["rows_t"] = [T(.05 + i * .5 / n) for i in range(n)]
        for i, t in enumerate(sh["rows_t"]): ev.append(["row", t, i])
        if sc.get("foot"):
            sh["total_t"] = T(.6); ev.append(["stat", sh["total_t"], 0]); ev.append(["win", sh["total_t"] + .7, 0])
            bursts.append({"t": sh["total_t"] + .72, "x": 540, "y": 1010, "n": 60, "seed": 21})
    elif k == "checks":
        n = len(sc["rows"]); sh["rows_t"] = [T(.08 + i * .55 / n) for i in range(n)]
        for i, t in enumerate(sh["rows_t"]): ev.append(["tick" if sc["rows"][i][2] else "deny", t, i])
        sh["stamp_t"] = T(.72); ev.append(["stamp_ok" if sc.get("ok") else "stamp_no", sh["stamp_t"], 0])
    elif k == "doc":
        n = len(sc["text"]); sh["type_t"] = [T(.06), T(.74)]
        for c in range(0, n, 3): ev.append(["key", T(.06 + .68 * c / n), c])
        sh["stamp_t"] = T(.8); ev.append(["stamp_ok", sh["stamp_t"], 0]); bursts.append({"t": sh["stamp_t"] + .05, "x": 760, "y": 1330, "n": 34, "seed": 31})
    elif k == "dm":
        n = len(sc["msgs"]); sh["msgs_t"] = [T(.08 + i * .6 / n) for i in range(n)]
        for i, t in enumerate(sh["msgs_t"]): ev.append(["msg", t, i])
    elif k == "cta":
        sh["kw_t"] = T(0) + .32; ev.append(["cta", s + .05, 0]); ev.append(["impact", sh["kw_t"], 1]); bursts.append({"t": sh["kw_t"] + .03, "x": 540, "y": 860, "n": 70, "seed": 41})
    return sh

# beat 0 tail = ask screen; later beats = their screens
for bi, b in enumerate(beats):
    s = (tail[0][1] - .12) if bi == 0 else b["s"] - .15
    e = beats[bi + 1]["s"] - .15 if bi + 1 < len(beats) else dur
    shots.append(screen_shot(b["b"]["screen"], s, e, bi)); trans.append(round(s, 3)); ev.append(["trans", s, bi])
    for p in phrases([w for w in b["ws"] if w[1] >= s], 3, False):
        caps.append({"s": p[0][1] - .02, "e": p[-1][2] + .12, "w": [[w[0].strip(), w[1], hi(w[0])] for w in p]})
for j, c in enumerate(caps[:-1]): c["e"] = min(c["e"], caps[j + 1]["s"])

data = {"dur": dur, "off": OFF, "agent": E["agent"], "id": E["id"], "nb": len(beats), "shots": shots, "caps": caps, "trans": trans, "bursts": bursts,
        "slams": [e[1] for e in ev if e[0] in ("slam", "impact", "stat", "stamp_ok", "stamp_no")]}
os.makedirs(f"{D}/out", exist_ok=True)
html = open(f"{D}/kine.html").read().replace("/*DATA*/null", json.dumps(data))
open(f"{D}/out/{ep}.html", "w").write(html)
ev = sorted([e for e in ev if 0 <= e[1] < dur], key=lambda x: x[1])
json.dump({"dur": dur, "off": OFF, "voice": wf.replace(".words.json", ".wav"), "events": ev}, open(f"{D}/out/{ep}.meta.json", "w"))
print("built", ep, dur, "s,", len(shots), "shots,", len(ev), "sfx")
