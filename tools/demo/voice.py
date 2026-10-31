"""python tools/demo/voice.py <ep> [--fake]  ->  tools/demo/<ep>.wav + <ep>.words.json"""
import os, sys, json, wave
D = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(D))
sys.path.insert(0, os.path.join(ROOT, "tools", "series")); sys.path.insert(0, os.path.join(ROOT, "scripts"))
import tts_ts
ep = sys.argv[1]; S = json.load(open(f"{D}/eps/{ep}.json"))
tts_ts.script = lambda _: " ".join(b["say"].strip() for b in S["beats"]); tts_ts.D = D
def fake():
    t, w = 0.25, []
    for x in tts_ts.script(ep).split():
        d = 0.10 + 0.04 * len(x); w.append([x, round(t, 3), round(t + d, 3)]); t += d + (0.25 if x[-1] in ".,:!?" else 0.03)
    n = int((t + 0.5) * 44100); f = wave.open(f"{D}/{ep}.wav", "wb"); f.setnchannels(1); f.setsampwidth(2); f.setframerate(44100); f.writeframes(b"\0\0" * n); f.close()
    json.dump(w, open(f"{D}/{ep}.words.json", "w")); print("fake timings", len(w), round(t, 1))
fake() if "--fake" in sys.argv else tts_ts.real(ep)
