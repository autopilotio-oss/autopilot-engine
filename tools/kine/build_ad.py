"""Ad builder (video 2 language): one scene per sentence, headline on top with one lime line, drawn scene in the middle,
mascot, progress bar, captions where the key word drops to a lime second line.
python3 tools/kine/build_ad.py <stem>   (needs tools/kine/out/<stem>.words.json from tools/kine/voice.py)
-> tools/kine/out/<stem>.html + <stem>.meta.json (sfx events for mix.py)"""
import os, sys, json, re
D = os.path.dirname(os.path.abspath(__file__)); ep = sys.argv[1]
E = json.load(open(f"{D}/ads/{ep}.json")); OFF = float(E.get("cold_open", .7))
W = [[w, round(s + OFF, 3), round(e + OFF, 3)] for w, s, e in json.load(open(f"{D}/out/{ep}.words.json"))]
NUM = {"one": "1", "two": "2", "three": "3", "four": "4", "five": "5", "six": "6", "seven": "7", "eight": "8", "nine": "9", "ten": "10", "eleven": "11", "twelve": "12", "twenty": "20", "thirty": "30", "forty": "40", "fifty": "50"}
def clean(w): return re.sub(r"[^a-z0-9$']", "", w.lower())
def ends(w): return w.rstrip('"\')')[-1:] in ".?!"
beats, i, ev, bursts = [], 0, [], []
for bi, b in enumerate(E["beats"]):
    n = len(b["say"].split()); ws = W[i:i + n]; i += n
    s = 0 if bi == 0 else round(ws[0][1] - .12, 3)
    beats.append({"i": bi, "s": s, "head": b["head"], "scene": b["scene"], "agent": b.get("agent", 0), "ws": ws})
for bi, b in enumerate(beats):
    b["e"] = beats[bi + 1]["s"] if bi + 1 < len(beats) else round(b["ws"][-1][2] + 1.6, 3)
dur = beats[-1]["e"]
# captions: per sentence, words accumulate; the sentence's last word (or a number) is the key word on line 2
FIX = [(x.split(), y) for x, y in E.get("cap_fix", {}).items()]
def fixseq(sn):
    out, k = [], 0
    while k < len(sn):
        hit = None
        for words, rep in FIX:
            seg = [clean(w[0]) for w in sn[k:k + len(words)]]
            if seg == words: hit = (len(words), rep); break
        if hit:
            last = sn[k + hit[0] - 1][0]; tail = last[len(last.rstrip(".,?!")):]
            out.append([hit[1] + tail, sn[k][1], sn[k + hit[0] - 1][2]]); k += hit[0]
        else: out.append(sn[k]); k += 1
    return out
caps = []
for b in beats:
    sent, cur = [], []
    for w in b["ws"]:
        cur.append(w)
        if ends(w[0]): sent.append(cur); cur = []
    if cur: sent.append(cur)
    for sn in sent:
        sn = fixseq(sn); words = []
        for k, w in enumerate(sn):
            if w is None: continue
            c = clean(w[0]); txt = w[0]
            if c in NUM and k + 1 < len(sn) and clean(sn[k + 1][0]) in NUM and NUM[c].endswith("0") and len(NUM[clean(sn[k + 1][0])]) == 1:
                txt = NUM[c][:-1] + NUM[clean(sn[k + 1][0])] + sn[k + 1][0][len(clean(sn[k + 1][0])):]; words.append([txt, w[1], k + 1 == len(sn) - 1, True]); sn[k + 1] = None; continue
            if w is None: continue
            key = (k == len(sn) - 1); num = c in NUM or any(ch.isdigit() for ch in w[0])
            words.append([NUM.get(c, txt) if c in NUM else txt, w[1], key, num])
        words = [x for x in words if x]
        caps.append({"s": round(sn[0][1] - .05, 3), "e": round(sn[-1][2] + .9, 3), "w": words})
for j, c in enumerate(caps[:-1]): c["e"] = min(c["e"], caps[j + 1]["s"])
# sfx + per scene timing
for b in beats:
    s, e, sc = b["s"], b["e"], b["scene"]; L = max(.8, e - s); T = lambda f: round(s + f * L, 3); k = sc["type"]
    off = max(sc.get("clip_in", 0), 4.95 - L); rate = min(1, (4.95 - off) / L); CT = lambda ct: round(s + max(.15, ct - off) / rate, 3)
    ev.append(["slam", s, b["i"]]); ev.append(["trans", s, 0]) if b["i"] else None
    if k == "inbox":
        for q in range(sc["n"]): ev.append(["blip", T(.04 + .6 * (q / sc["n"]) ** 1.4), q % 4])
        ev.append(["impact", T(.66), 2]); bursts.append({"t": T(.67), "x": 540, "y": 900, "n": 40, "seed": 2})
    elif k == "lock":
        for q in range(len(sc["chips"])): ev.append(["deny", T(.25 + q * .14), q])
        ev.append(["stamp_no", T(.72), 0]); ev.append(["impact", T(.72), 1])
    elif k == "term":
        for q, _ in enumerate(sc.get("files", [])): ev.append(["drop", T(.04 + q * .08), q])
        n = len(sc["text"]); t0, t1 = .2, .8; b["type_t"] = [T(t0), T(t1)]
        for c in range(n):
            if sc["text"][c] != " ": ev.append(["key", T(t0 + (t1 - t0) * (c + 1) / n), c])
        ev.append(["send", T(t1 + .04), 0]); b["send_t"] = T(t1 + .04)
    elif k == "grid":
        n = len(sc.get("items", E["agents"])); b["lit"] = [T(.12 + .7 * q / n) for q in range(n)]
        for q, t in enumerate(b["lit"]): ev.append(["tick", t, q])
        ev.append(["win", T(.86), 0]); bursts.append({"t": T(.86), "x": 540, "y": 930, "n": 50, "seed": 7})
    elif k == "work":
        n = len(sc["lines"]); b["steps"] = [[T(.08 + .8 * q / (n + .3)), T(.08 + .8 * (q + .8) / (n + .3))] for q in range(n)]
        for q, (a, d) in enumerate(b["steps"]): ev.append(["blip", a, q]); ev.append(["tick", d, q])
    elif k == "phone":
        b["q_t"], b["a_t"], b["pill_t"] = T(.06), T(.3), T(.76); ev.append(["msg", b["q_t"], 0]); b["st_t"] = [T(.08), T(.3), T(.76)]
        for q, t in enumerate(b["st_t"]): ev.append(["blip", t, q])
        if not sc["q"]: b["a_t"] = T(.2)
        n = len(sc["a"])
        for c in range(0, n, 2): ev.append(["key", T(.3 + .38 * c / n), c])
        ev.append(["stamp_ok", b["pill_t"], 0])
    elif k == "quote":
        n = len(sc["lines"]); b["st_t"] = [T(.06), T(.4), T(.78)]; b["l_t"] = [T(.18 + .45 * q / n) for q in range(n)]; b["tot_t"] = T(.7)
        for q, t in enumerate(b["st_t"]): ev.append(["blip", t, q])
        for q, t in enumerate(b["l_t"]): ev.append(["row", t, q])
        ev.append(["stat", b["tot_t"], 0]); ev.append(["stamp_ok", T(.86), 0])
    elif k == "result":
        b["count_t"] = T(.05); ev.append(["stat", T(.05), 0]); b["rows_t"] = [T(.42 + q * .14) for q in range(len(sc["rows"]))]
        for q, t in enumerate(b["rows_t"]): ev.append(["row", t, q])
        bursts.append({"t": T(.5), "x": 540, "y": 760, "n": 50, "seed": 9})
    elif k == "brief":
        b["lines_t"] = [T(.1 + q * .11) for q in range(7)]
        for q, t in enumerate(b["lines_t"]): ev.append(["row", t, q])
        ev.append(["cta", T(.8), 0])
    elif k == "quiz":
        n = len(sc["qs"]); b["q_t"] = [T(.04 + .8 * q / n) for q in range(n)]
        for q, t in enumerate(b["q_t"]): ev.append(["msg", t, q]); ev.append(["tick", t + .3, q])
    elif k == "setup":
        n = len(sc["lines"]); b["l_t"] = [T(.1 + .7 * q / n) for q in range(n)]
        for q, t in enumerate(b["l_t"]): ev.append(["row", t, q])
        ev.append(["stamp_ok", T(.86), 0])
    elif k == "big":
        ev.append(["stat", T(.05), 0]); bursts.append({"t": T(.08), "x": 540, "y": 860, "n": 60, "seed": 13})
    elif k in ("screenchat", "draft"):
        b["q_t"], b["a_t"], b["pill_t"] = T(.06), T(.32), T(.8); b["st_t"] = [T(.04), T(.3), T(.8)]
        if k == "draft" or not sc.get("q"): b["a_t"] = T(.18)
        ev.append(["msg", b["q_t"], 0])
        for q, t in enumerate(b["st_t"]): ev.append(["blip", t, q])
        n = len(sc["a"])
        for c in range(0, n, 2): ev.append(["key", round(b["a_t"] + (b["pill_t"] - .1 - b["a_t"]) * c / n, 3), c])
        ev.append(["stamp_ok", b["pill_t"], 0])
    elif k == "quizrow":
        n = len(sc["qs"]); b["q_t"] = [T(.05 + .85 * q / n) for q in range(n)]
        for q, t in enumerate(b["q_t"]): ev.append(["row", t, q]); ev.append(["tick", t + .35, q])
    elif k == "tiles":
        b["lab_t"] = [CT(2.6 + q * .2) for q in range(len(sc["tiles"]["labels"]))]
        for q, t in enumerate(b["lab_t"]): ev.append(["tick", t, q])
        bursts.append({"t": b["lab_t"][-1] + .1, "x": 540, "y": 700, "n": 40, "seed": 17})
    elif k == "approve":
        b["draft_t"], b["tap_t"] = T(.08), T(.55); ev.append(["msg", b["draft_t"], 0]); ev.append(["send", b["tap_t"], 0]); ev.append(["stamp_ok", b["tap_t"] + .15, 0])
    elif k == "cardprice":
        b["kw_t"] = CT(2.75); ev.append(["cta", s + .05, 0]); ev.append(["impact", b["kw_t"], 1]); bursts.append({"t": b["kw_t"] + .03, "x": 540, "y": 1050, "n": 70, "seed": 41})
    elif k == "plain":
        pass
    elif k == "drafts":
        b["d_t"] = [T(.12 + .22 * q) for q in range(3)]
        for q, t in enumerate(b["d_t"]): ev.append(["msg", t, q])
    elif k == "comment":
        b["c_t"] = [T(.05), T(.38), T(.5), T(.62)]
        for c in range(len(sc["kw"])): ev.append(["key", round(b["c_t"][0] + .3 + c * .08, 3), c])
        ev.append(["send", b["c_t"][1], 0]); ev.append(["msg", b["c_t"][2], 0]); ev.append(["cta", b["c_t"][3], 0])
    elif k == "cta":
        b["kw_t"] = T(.12); ev.append(["impact", b["kw_t"], 1]); ev.append(["cta", s + .05, 0]); bursts.append({"t": b["kw_t"] + .03, "x": 540, "y": 820, "n": 70, "seed": 41})
    b.pop("ws")
data = {"dur": dur, "off": OFF, "agents": E["agents"], "beats": beats, "caps": caps, "bursts": bursts,
        "slams": sorted(e[1] for e in ev if e[0] in ("slam", "impact", "stat", "stamp_ok", "stamp_no"))}
os.makedirs(f"{D}/out", exist_ok=True)
open(f"{D}/out/{ep}.html", "w").write(open(f"{D}/" + E.get("template", "ad.html")).read().replace("/*DATA*/null", json.dumps(data)))
ev = sorted([x for x in ev if x and 0 <= x[1] < dur], key=lambda x: x[1])
plates = []
for bb in beats:
    sc = bb["scene"]
    if sc.get("plate"):
        L = bb["e"] - bb["s"]; off = max(sc.get("clip_in", 0), 4.95 - L); rate = min(1, (4.95 - off) / L)
        plates.append({"s": bb["s"], "e": bb["e"], "plate": sc["plate"], "off": round(off, 4), "rate": round(rate, 5)})
    elif sc.get("plates"):
        n = len(sc["plates"]); L = (bb["e"] - bb["s"]) / n
        for j, pl in enumerate(sc["plates"]):
            s0 = bb["s"] + j * L; off = sc.get("clip_ins", {}).get(pl, min(1.2, max(0, 4.95 - L))); rate = min(1, (4.95 - off) / L)
            plates.append({"s": round(s0, 3), "e": round(s0 + L, 3), "plate": pl, "off": round(off, 4), "rate": round(rate, 5)})
json.dump({"dur": dur, "off": OFF, "voice": f"{D}/out/{ep}.wav", "events": ev, "plates": plates}, open(f"{D}/out/{ep}.meta.json", "w"))
print("built ad", ep, dur, "s,", len(beats), "scenes,", len(caps), "captions,", len(ev), "sfx")
