"""Voice the HQ video with ElevenLabs Brian (1.2x) + word timings.
python tools/hq/voice.py          -> tools/hq/hq.wav + hq.words.json   (needs ELEVENLABS_API_KEY)
python tools/hq/voice.py --fake   -> silent wav + estimated timings (local previews only)"""
import os, sys, json, wave
D = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(D))
sys.path.insert(0, os.path.join(ROOT, "tools", "series")); sys.path.insert(0, os.path.join(ROOT, "scripts"))
import tts_ts
S = json.load(open(f"{D}/script.json"))
tts_ts.script = lambda ep: " ".join(b["say"].strip() for b in S["beats"])
tts_ts.D = D
def fake():
    t, w = 0.25, []
    for x in tts_ts.script("hq").split():
        d = 0.10 + 0.04 * len(x); w.append([x, round(t, 3), round(t + d, 3)]); t += d + (0.25 if x[-1] in ".,:!?" else 0.03)
    n = int((t + 0.5) * 44100); f = wave.open(f"{D}/hq.wav", "wb"); f.setnchannels(1); f.setsampwidth(2); f.setframerate(44100); f.writeframes(b"\0\0" * n); f.close()
    json.dump(w, open(f"{D}/hq.words.json", "w")); print("fake timings", len(w), "words", round(t, 1), "s")
if __name__ == "__main__":
    fake() if "--fake" in sys.argv else tts_ts.real("hq")
