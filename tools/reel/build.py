import json, re, subprocess, sys, wave, numpy as np, os, importlib
name = sys.argv[1]; spec = importlib.import_module(name)
wav = f"{name}.wav"
w = wave.open(wav); sr = w.getframerate(); a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(float) / 32768; w.close()
DUR = len(a) / sr
# speech segments
out = subprocess.run(["ffmpeg", "-i", wav, "-af", "silencedetect=noise=-38dB:d=0.12", "-f", "null", "-"], capture_output=True, text=True).stderr
ss = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", out)]; se = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", out)]
sil = list(zip(ss, se + [DUR] * (len(ss) - len(se))))
segs = []; cur = 0.0
for s0, s1 in sil:
    if s0 > cur + 0.05: segs.append((cur, s0))
    cur = s1
if cur < DUR - 0.05: segs.append((cur, DUR))
# first speech onset
env = np.abs(a); fr = int(sr * 0.01); en = np.array([env[i:i + fr].max() for i in range(0, len(env), fr)])
onset = np.argmax(en > 0.02) * 0.01; segs[0] = (max(segs[0][0], onset), segs[0][1])
S = sum(b - a_ for a_, b in segs)
def sp2t(x):  # speech-time -> real time
    for a_, b in segs:
        if x <= b - a_: return a_ + x
        x -= b - a_
    return segs[-1][1]
phr = spec.PHRASES
words = [(i, wd) for i, (txt, _) in enumerate(phr) for wd in txt.split()]
wt = [len(re.sub(r"[^A-Za-z0-9]", "", wd)) + 1.5 for _, wd in words]; tot = sum(wt)
T = [{"t": 0, "e": 0, "words": []} for _ in phr]; c = 0
for (i, wd), x in zip(words, wt):
    t0 = sp2t(c / tot * S); c += x; t1 = sp2t(c / tot * S)
    T[i]["words"].append({"w": wd, "t": round(t0, 3), "e": round(t1, 3)})
# snap phrase starts to segment starts (monotonic), then re-spread words inside each phrase
starts = [s for s, _ in segs]; prev = -1; snapped = []
for i, p in enumerate(T):
    t0 = p["words"][0]["t"]
    if i == 0: snapped.append(starts[0]); prev = 0; continue
    cands = [(abs(s - t0), k) for k, s in enumerate(starts) if k > prev and abs(s - t0) < 1.0]
    if cands: k = min(cands)[1]; snapped.append(starts[k]); prev = k
    else: snapped.append(t0)
for i, p in enumerate(T):
    a0 = snapped[i]; nxt = snapped[i + 1] if i + 1 < len(T) else DUR
    ends = [e for s_, e in segs if a0 <= s_ < nxt - 0.01]; b0 = max(ends) if ends else nxt
    ws = [len(re.sub(r"[^A-Za-z0-9]", "", x["w"])) + 1.5 for x in p["words"]]; tw = sum(ws); c2 = 0
    for x, wv in zip(p["words"], ws):
        x["t"] = round(a0 + c2 / tw * (b0 - a0), 3); c2 += wv; x["e"] = round(a0 + c2 / tw * (b0 - a0), 3)
    p["t"] = p["words"][0]["t"]; p["e"] = p["words"][-1]["e"]
P = [p["t"] for p in T]
# mouth
hop = sr // 30; rms = np.array([np.sqrt(np.mean(a[i:i + hop] ** 2)) for i in range(0, len(a), hop)])
rms = rms / np.percentile(rms[rms > 0.005], 95); rms = np.clip(rms, 0, 1)
MO = [round(float(v), 3) for v in np.convolve(rms, [.25, .5, .25], "same")]
TOTAL = round(DUR + spec.TAIL, 2)
def tt(m):
    v = P[int(m.group(1))] + (float(m.group(2)) if m.group(2) else 0); return f"{v:.2f}"
scenes = []
for k, (pi, label, html) in enumerate(spec.SCENES):
    a_ = P[pi] - 0.05 if k else 0; b_ = (P[spec.SCENES[k + 1][0]] - 0.05) if k + 1 < len(spec.SCENES) else TOTAL
    scenes.append(f'<div class="sc" data-a="{a_:.2f}" data-b="{b_:.2f}"><div style="position:absolute;inset:0;transform:scale(1.12);transform-origin:50% 0">' + re.sub(r"@(\d+)([+-][\d.]+)?", tt, html) + "</div></div>")
SEC = [[0 if k == 0 else P[pi] - 0.05, f"{k + 1:02d} · {label}"] for k, (pi, label, _) in enumerate(spec.SCENES)]
GR = spec.GROUPS
EM = {i: [x.lower() for x in e] for i, (_, e) in enumerate(phr)}
MOODS = [[P[a_] if a_ < len(P) else TOTAL, P[b_] if b_ < len(P) else 99, m] for a_, b_, m in spec.MOODS]
head = open("head.html").read()
js = f"const DUR={TOTAL};\nconst T={json.dumps(T)},MO={json.dumps(MO)},SCR={open('screen.json').read()},GR={json.dumps(GR)},EM={json.dumps(EM)},SEC={json.dumps(SEC)},MOODS={json.dumps(MOODS)},CAPEND={P[spec.CAPEND_PHRASE] if spec.CAPEND_PHRASE is not None else 999};\n" + open("engine.js").read()
html = head + "\n".join(scenes) + '\n<div id="glow"></div><div id="pres"><img id="pf" src="fr/0001.jpg"></div><div id="scr"></div>\n</div><div id="flash"></div><div id="vig"></div><div id="grain"></div></div><script>' + js + "</script></body></html>"
open(f"{name}.html", "w").write(html)
json.dump({"dur": TOTAL, "P": P, "scenes": [s[1] for s in SEC], "pops": spec.POPS(P) if hasattr(spec, "POPS") else []}, open(f"{name}.meta.json", "w"))
print(name, "dur", TOTAL, "phrase starts", [round(x, 2) for x in P])
