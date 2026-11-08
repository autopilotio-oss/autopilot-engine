"""Sound for an ink film -> tools/ink/out/<stem>_mix.wav
Voice on top; pen scratch synced to every pen down stroke (fineliner vs marker), nib taps, room tone,
a low pulse under the twist and a quiet pad that darkens in the red section and resolves at the end.
python3 tools/ink/mix.py <stem>   (needs out/<stem>.wav and out/<stem>_v.tl.json from render.js)"""
import sys, os, json, wave, numpy as np
D = os.path.dirname(os.path.abspath(__file__)); SR = 44100
stem = sys.argv[1]; TL = json.load(open(f"{D}/out/{stem}_v.tl.json")); dur = TL["dur"]; N = int(SR * (dur + .3))
rng = np.random.default_rng(11)
def readwav(p):
    w = wave.open(p); x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float64) / 32768
    if w.getnchannels() == 2: x = x.reshape(-1, 2).mean(1)
    return x
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR)
    g = np.clip((f - lo * .7) / (lo * .3), 0, 1) * np.clip((hi * 1.3 - f) / (hi * .3), 0, 1)
    return np.fft.irfft(X * g, len(x))
voice = np.zeros(N); v = readwav(f"{D}/out/{stem}.wav"); voice[:min(N, len(v))] = v[:N]
# --- pen scratch ---
envF = np.zeros(N); envM = np.zeros(N); taps = np.zeros(N); pan = np.zeros(N)
for e in TL["ink"]:
    marker = e["c"] in ("g", "r") and e["w"] >= 3.2
    for s, t, down in e["seq"]:
        if not down or t - s < .02: continue
        i0, i1 = int(s * SR), min(N, int(t * SR)); n = i1 - i0
        if n <= 0: continue
        tt = np.arange(n) / SR; wob = 8 + rng.uniform(0, 6)
        a = (.55 + .45 * np.abs(np.sin(2 * np.pi * wob * tt + rng.uniform(0, 6)))) * np.minimum(1, tt / .015) * np.minimum(1, (n / SR - tt) / .02)
        (envM if marker else envF)[i0:i1] += a * (.9 + .2 * rng.random())
        k = np.arange(int(.012 * SR)); taps[i0:i0 + len(k)] += rng.standard_normal(len(k)) * np.exp(-k / (.0018 * SR)) * .5
wn = rng.standard_normal(N)
scratch = band(wn * envF, 2600, 8000) * 1.0 + band(rng.standard_normal(N) * envM, 900, 4200) * .8
taps = band(taps, 1500, 9000)
# --- room tone ---
room = band(rng.standard_normal(N), 60, 900) * .006
# --- twist pulse ---
pulse = np.zeros(N)
if TL.get("twist") is not None:
    t0 = TL["twist"] - .05; i0 = int(t0 * SR); tt = np.arange(int(3.2 * SR)) / SR
    p = np.sin(2 * np.pi * 46 * tt) * np.minimum(1, tt / .02) * np.exp(-tt / 1.1) * .55 + band(rng.standard_normal(len(tt)), 40, 200) * np.exp(-tt / .25) * .5
    pulse[i0:i0 + len(p)] += p[:max(0, N - i0)]
# --- pad: calm, darker after the twist, resolves at the end ---
tw = TL.get("twist") or dur * .45; tt = np.arange(N) / SR
def chord(fs, a, b):
    m = (tt >= a) & (tt < b); x = np.zeros(N)
    for f in fs: x += np.sin(2 * np.pi * f * tt + rng.uniform(0, 6)) * (1 + .3 * np.sin(2 * np.pi * .13 * tt))
    fade = np.clip((tt - a) / 1.8, 0, 1) * np.clip((b - tt) / 1.8, 0, 1); return x * fade * m / len(fs)
end = dur - 9.5
pad = chord([110, 164.8, 220, 261.6], 0, tw + .8) + chord([103.8, 155.6, 207.7, 246.9], tw - .8, end + .8) * 1.1 + chord([130.8, 196, 261.6, 329.6], end - .8, dur + .3)
pad = band(pad, 80, 1800) * .05
# --- duck the bed under the voice ---
ve = np.convolve(np.abs(voice), np.ones(2205) / 2205, "same"); duck = 1 - .45 * np.clip(ve / .04, 0, 1)
mix = voice * 1.0 + (scratch * .055 + taps * .05) * (1 - .35 * np.clip(ve / .04, 0, 1)) + room + pulse * .5 + pad * duck
mix = np.tanh(mix * 1.1) / 1.1
out = (np.clip(mix, -1, 1) * 32767).astype(np.int16)
w = wave.open(f"{D}/out/{stem}_mix.wav", "wb"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(out.tobytes()); w.close()
print("mix", stem, round(dur, 2), "s")
