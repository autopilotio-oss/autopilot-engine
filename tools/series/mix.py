"""Music bed + sound effects for a series episode, mixed under the voice -> <ep>_mix.wav"""
import sys, os, json, wave, numpy as np
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(D, "..", "reel")); import sfx
from sfx import add, kick, hat, note, whoosh, click, chime, pop, SR
ep = sys.argv[1]; M = json.load(open(f"{D}/{ep}.meta.json")); dur = M["dur"]; sfx.init(dur)
b = 60 / 96; roots = [55.0, 46.25, 41.2, 49.0]
for i in range(int(dur / b)):
    t = i * b
    if i % 4 == 0: add(kick(), t, .35)
    add(hat(), t + b / 2, .07, pan=.3)
    if i % 8 == 0:
        r = roots[(i // 8) % 4] * 4
        for f in (r, r * 1.19, r * 1.5): add(note(f, 8 * b, 'pad'), t, .035)
        add(note(roots[(i // 8) % 4], 8 * b, 'bass'), t, .12)
for c, ty in zip(M["cuts"], M["types"][1:]):
    add(whoosh(.35), c - .28, .22)
    if ty in ("white", "tip", "cta"): add(chime(), c + .05, .12)
    else: add(pop(), c + .1, .1)
for s, e in M["typing"]:
    ty = max(.9, (e - s) * .42)
    for k in np.arange(s + .25, s + .25 + ty, .07): add(click(), float(k), .12)
v = wave.open(f"{D}/{ep}.wav"); a = np.frombuffer(v.readframes(v.getnframes()), np.int16) / 32768; v.close()
voice = np.zeros(len(sfx.L)); n = min(len(a), len(voice)); voice[:n] = a[:n]
pk = np.max(np.abs(voice)) or 1; voice = voice / pk * .9
bed = np.stack([sfx.L, sfx.R], 1); bed = bed / (np.max(np.abs(bed)) or 1) * .28
env = np.convolve((np.abs(voice) > .02).astype(float), np.ones(4410) / 4410, 'same'); bed *= (1 - .45 * np.clip(env * 3, 0, 1))[:, None]
m = bed + voice[:, None]; m = m / max(1, np.max(np.abs(m)) / .97)
f = np.ones(len(m)); k = int(.8 * SR); f[-k:] = np.linspace(1, 0, k); m *= f[:, None]
w = wave.open(f"{D}/{ep}_mix.wav", "wb"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((m * 32767).astype(np.int16).tobytes()); w.close(); print("mixed", ep)
