"""Music bed + sfx under the voice -> tools/hq/hq_mix.wav"""
import sys, os, json, wave, numpy as np
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(D, "..", "reel")); import sfx
from sfx import add, kick, hat, note, whoosh, chime, pop, click, SR
M = json.load(open(f"{D}/hq.meta.json")); dur = M["dur"]; sfx.init(dur); np.random.seed(7)
b = 60 / 112; roots = [41.2, 41.2, 36.7, 49.0]
for i in range(int(dur / b) + 1):
    t = i * b; bar = i // 4
    if i % 2 == 0 or i % 8 == 7: add(kick(), t, .3)
    add(hat(), t + b / 2, .06, pan=.35); add(hat(), t + b * .75, .025, pan=-.35)
    if i % 16 == 0:
        r = roots[(i // 16) % 4] * 4
        for f in (r, r * 1.2, r * 1.5, r * 2): add(note(f, 16 * b, 'pad'), t, .028)
    if i % 2 == 0: add(note(roots[(bar // 4) % 4], b * 1.6, 'bass'), t, .11)
    if i % 4 == 2: add(pop(2400 + 400 * (i % 3)), t + b / 4, .035, pan=.5 - (i % 3) * .5)
for c in M["cuts"]:
    add(whoosh(.45), c - .1, .2); add(click(), c + .5, .25); add(pop(900), c + .55, .08)
add(chime(1318), M["cuts"][-1] + .1, .16); add(chime(1976), M["cuts"][-1] + .25, .08)
v = wave.open(f"{D}/hq.wav"); a = np.frombuffer(v.readframes(v.getnframes()), np.int16) / 32768; v.close()
voice = np.zeros(len(sfx.L)); n = min(len(a), len(voice)); voice[:n] = a[:n]
pk = np.max(np.abs(voice)) or 1; voice = voice / pk * .9
bed = np.stack([sfx.L, sfx.R], 1); bed = bed / (np.max(np.abs(bed)) or 1) * .3
env = np.convolve((np.abs(voice) > .02).astype(float), np.ones(4410) / 4410, 'same'); bed *= (1 - .45 * np.clip(env * 3, 0, 1))[:, None]
m = bed + voice[:, None]; m = m / max(1, np.max(np.abs(m)) / .97)
f = np.ones(len(m)); k = int(1.2 * SR); f[-k:] = np.linspace(1, 0, k); m *= f[:, None]
w = wave.open(f"{D}/hq_mix.wav", "wb"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((m * 32767).astype(np.int16).tobytes()); w.close(); print("mixed")
