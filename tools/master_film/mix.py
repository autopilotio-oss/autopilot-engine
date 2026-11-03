"""python tools/master_film/mix.py <cut> -> <cut>_mix.wav: slow cinematic bed (no external audio) + soft transitions under the voice"""
import sys, os, json, wave, numpy as np
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(D, "..", "reel")); import sfx
from sfx import add, note, whoosh, chime, kick, SR
cut = sys.argv[1]; M = json.load(open(f"{D}/{cut}.meta.json")); dur = M["dur"]; sfx.init(dur); np.random.seed(11)
b = 60 / 76; prog = [[55.0, 82.4, 110.0, 130.8], [43.65, 65.4, 87.3, 130.8], [49.0, 73.4, 98.0, 123.5], [41.2, 61.7, 82.4, 123.5]]
fin = M["beats"][-1]["s"]
for i in range(int(dur / (8 * b)) + 1):
    t = i * 8 * b; ch = prog[i % 4]
    for f in ch: add(note(f * 2, 8 * b + .6, 'pad'), t, .035)
    add(note(ch[0], 8 * b, 'bass'), t, .10)
for i in range(int(dur / b)):
    t = i * b
    if 4 < t < fin + 1 and i % 2 == 0: add(kick(), t, .10)                     # soft heartbeat pulse
    if t > 8 and i % 4 == 3: add(note(880 * (1.5 if i % 8 == 7 else 1), .5, 'pad'), t, .010, pan=.4 - .8 * (i % 3) / 2)
for c in M["cuts"]:
    add(whoosh(.7), c - .45, .10)
add(chime(1318), fin + .2, .10); add(chime(1976), fin + 1.6, .06); add(chime(2637), fin + 3.0, .05)
v = wave.open(f"{D}/{cut}.wav"); a = np.frombuffer(v.readframes(v.getnframes()), np.int16) / 32768; v.close()
voice = np.zeros(len(sfx.L)); n = min(len(a), len(voice)); voice[:n] = a[:n]
pk = np.max(np.abs(voice)) or 1; voice = voice / pk * .9
bed = np.stack([sfx.L, sfx.R], 1); bed = bed / (np.max(np.abs(bed)) or 1) * .32
env = np.convolve((np.abs(voice) > .02).astype(float), np.ones(8820) / 8820, 'same'); bed *= (1 - .5 * np.clip(env * 3, 0, 1))[:, None]
m = bed + voice[:, None]; m = m / max(1, np.max(np.abs(m)) / .97)
f = np.ones(len(m)); k = int(2.0 * SR); f[-k:] = np.linspace(1, 0, k); f[:int(.6 * SR)] = np.linspace(0, 1, int(.6 * SR)); m *= f[:, None]
w = wave.open(f"{D}/{cut}_mix.wav", "wb"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((m * 32767).astype(np.int16).tobytes()); w.close(); print("mixed", cut)
