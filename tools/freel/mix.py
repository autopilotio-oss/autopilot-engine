"""Sound design for factory reels -> tools/freel/<ep>_mix.wav
Voice on top; designed UI sfx synced to the screen (keys, ticks, row pops, stamps, whooshes, hook impacts); a dark minimal bed ducked under the voice."""
import sys, os, json, wave, numpy as np
D = os.path.dirname(os.path.abspath(__file__)); SR = 44100
EP = sys.argv[1]; M = json.load(open(f"{D}/{EP}.meta.json")); dur = M["dur"]; N = int(SR * (dur + .2)); rng = np.random.default_rng(7)
L = np.zeros(N); R = np.zeros(N)
def add(x, t, g=1., pan=0.):
    i = int(max(t, 0) * SR); n = min(len(x), N - i)
    if n > 0: L[i:i + n] += x[:n] * g * (1 - max(pan, 0)); R[i:i + n] += x[:n] * g * (1 + min(pan, 0))
ts = lambda d: np.arange(int(d * SR)) / SR
def env(t, a, d): return np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / d)
def lp(x, k):  # cheap one pole lowpass, k in (0,1]
    y = np.empty_like(x); s = 0.
    for i, v in enumerate(x): s += k * (v - s); y[i] = s
    return y
def hp(x, k): return x - lp(x, k)
def S(*xs):
    n = max(len(x) for x in xs); o = np.zeros(n)
    for x in xs: o[:len(x)] += x
    return o
def sat(x, d=2.): return np.tanh(x * d) / np.tanh(d)
# --- designed sounds ---
def impact(i):
    t = ts(1.1); f = 62 * np.exp(-t * 3) + 34; sub = np.sin(2 * np.pi * np.cumsum(f) / SR) * env(t, .002, .45)
    crack = hp(rng.standard_normal(len(t)), .35) * env(t, .0005, .025)
    body = lp(rng.standard_normal(len(t)), .08) * env(t, .001, .12)
    return sat(sub * 1.1 + crack * .5 + body * .6, 1.6) * (1 - i * .12)
def whoosh(d=.55, up=True):
    t = ts(d); n = rng.standard_normal(len(t)); sw = np.linspace(.02, .35, len(t)) if up else np.linspace(.35, .02, len(t))
    y = np.empty_like(n); s = 0.
    for i, v in enumerate(n): s += sw[i] * (v - s); y[i] = s
    e = np.sin(np.pi * np.clip(t / d, 0, 1)) ** 1.6; return hp(y, .02) * e * 1.6
def key(c):
    t = ts(.05); f = 1 + rng.uniform(-.15, .15)
    clack = hp(rng.standard_normal(len(t)), .5) * env(t, .0003, .006 * f)
    thock = np.sin(2 * np.pi * 170 * f * t) * env(t, .0005, .012)
    return clack * .55 + thock * .5
def tick(i):
    t = ts(.18); f = 1760 * (1 + .04 * (i % 4)); return (np.sin(2 * np.pi * f * t) + .25 * np.sin(2 * np.pi * f * 2.0 * t)) * env(t, .0008, .045) + hp(rng.standard_normal(len(t)), .6) * env(t, .0002, .003) * .4
def blip(i):
    t = ts(.12); f = 620 + 40 * i; return np.sin(2 * np.pi * f * t) * env(t, .001, .03) * .7
def row(i):
    t = ts(.14); f = 980 + 70 * (i % 6); return np.sin(2 * np.pi * f * (1 + .3 * np.exp(-t * 60)) * t) * env(t, .001, .035) + hp(rng.standard_normal(len(t)), .5) * env(t, .0002, .004) * .3
def chord(fs, d=1.2, dec=.4):
    t = ts(d); return sum(np.sin(2 * np.pi * f * t) * env(t, .003, dec) for f in fs) / len(fs)
def win(_): return S(chord([1046.5, 1318.5, 1568, 2093], 1.4, .5) * .9, impact(3) * .25)
def stamp_ok(_): return S(impact(2) * .55, chord([784, 988, 1175], 1.0, .35) * .6)
def stamp_no(_):
    t = ts(.5); bz = np.sign(np.sin(2 * np.pi * 110 * t)) * env(t, .002, .14); return S(impact(2) * .55, lp(bz, .2) * .5)
def deny(i):
    t = ts(.2); return np.sin(2 * np.pi * 240 * t) * env(t, .001, .05) * .8
def drop(i):
    t = ts(.25); f = 300 * np.exp(-t * 12) + 120; return S(np.sin(2 * np.pi * np.cumsum(f) / SR) * env(t, .001, .06), row(i) * .5)
def send(_):
    t = ts(.35); f = 500 + 900 * t / .35; return S(np.sin(2 * np.pi * np.cumsum(f) / SR) * env(t, .002, .09) * .6, whoosh(.3) * .3)
def msg(i):
    t = ts(.25); return (np.sin(2 * np.pi * 1318 * t) * env(t, .001, .05) + np.sin(2 * np.pi * 1976 * t) * env(np.maximum(t - .06, 0), .001, .07) * (t > .06)) * .7
def cta(_): return S(chord([659, 988, 1318, 1976], 2.0, .7) * .8, whoosh(.6, False) * .3)
def trans(_): return S(whoosh(.5) * .6, impact(4) * .18)
G = {"impact": (impact, .55), "whoosh": (lambda _: whoosh(.6), .45), "trans": (trans, .45), "key": (key, .16), "send": (send, .3),
     "drop": (drop, .3), "blip": (blip, .14), "tick": (tick, .22), "row": (row, .2), "win": (win, .3), "stamp_ok": (stamp_ok, .42),
     "stamp_no": (stamp_no, .42), "deny": (deny, .22), "msg": (msg, .28), "cta": (cta, .3)}
for k, t, i in M["events"]:
    f, g = G[k]; add(f(i), t, g, pan=(((len(k) * 3 + i) % 7) - 3) * .06)
sfx = np.stack([L, R], 1)
# --- bed: dark pulse, 96 bpm, enters after the hook ---
B = np.zeros((N, 2)); b = 60 / 96; root = 43.65
def put(x, t, g, pan=0.):
    i = int(t * SR); n = min(len(x), N - i)
    if n > 0: B[i:i + n, 0] += x[:n] * g * (1 - max(pan, 0)); B[i:i + n, 1] += x[:n] * g * (1 + min(pan, 0))
k = 0; t0 = 2.5
while t0 + k * b < dur:
    t = t0 + k * b; ph = ts(b * .95)
    put(np.sin(2 * np.pi * root * ph) * env(ph, .01, .35) + .2 * np.sin(2 * np.pi * root * 2 * ph) * env(ph, .01, .2), t, .5)
    if k % 2 == 1: put(hp(rng.standard_normal(int(.05 * SR)), .6) * env(ts(.05), .0005, .012), t, .12, .3)
    put(hp(rng.standard_normal(int(.04 * SR)), .7) * env(ts(.04), .0005, .008), t + b / 2, .07, -.3)
    if k % 8 == 0:
        pd = ts(8 * b); pad = sum(np.sin(2 * np.pi * f * ph2) for f, ph2 in [(root * 4, pd), (root * 4 * 1.189, pd), (root * 4 * 1.498, pd)]) / 3
        put(lp(pad * np.minimum(1, pd / 1.2) * np.minimum(1, (8 * b - pd) / 1.2).clip(0), .15), t, .22)
    k += 1
# --- voice + ducking ---
v = wave.open(f"{D}/{EP}.wav"); a = np.frombuffer(v.readframes(v.getnframes()), np.int16) / 32768; v.close()
voice = np.zeros(N); n = min(len(a), N); voice[:n] = a[:n]; voice = voice / (np.max(np.abs(voice)) or 1) * .92
envv = np.convolve((np.abs(voice) > .02).astype(float), np.ones(4410) / 4410, 'same')
duck = (1 - .55 * np.clip(envv * 3, 0, 1))[:, None]
bed = B / (np.max(np.abs(B)) or 1) * .22 * duck
s = sfx / (np.max(np.abs(sfx)) or 1) * .5 * (1 - .25 * np.clip(envv * 3, 0, 1))[:, None]
m = bed + s + voice[:, None]; m = m / max(1, np.max(np.abs(m)) / .97)
f = np.ones(N); kk = int(.8 * SR); f[-kk:] = np.linspace(1, 0, kk); m *= f[:, None]
w = wave.open(f"{D}/{EP}_mix.wav", "wb"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((m * 32767).astype(np.int16).tobytes()); w.close(); print("mixed", len(M["events"]), "sfx events")
