"""python tools/master_film/voice.py <cut> [--fake]  -> <cut>.wav + <cut>.words.json (ElevenLabs Brian via tools/series/tts_ts, existing credits)"""
import os, sys, json, wave
D = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(D))
sys.path.insert(0, os.path.join(ROOT, "tools", "series")); sys.path.insert(0, os.path.join(ROOT, "scripts"))
import tts_ts
cut = sys.argv[1]; S = json.load(open(f"{D}/script.json"))["cuts"][cut]
tts_ts.script = lambda ep: " ".join(b["say"].strip() for b in S)
tts_ts.D = D; tts_ts.SPEED = 1.04   # calmer than the 1.2x reels: this is a brand film
def fake():
    t, w = 0.6, []
    for x in tts_ts.script(cut).split():
        d = 0.12 + 0.045 * len(x); w.append([x, round(t, 3), round(t + d, 3)]); t += d + (0.32 if x[-1] in ".,:!?" else 0.035)
    n = int((t + 0.5) * 44100); f = wave.open(f"{D}/{cut}.wav", "wb"); f.setnchannels(1); f.setsampwidth(2); f.setframerate(44100); f.writeframes(b"\0\0" * n); f.close()
    json.dump(w, open(f"{D}/{cut}.words.json", "w")); print("fake timings", cut, len(w), "words", round(t, 1), "s")
if __name__ == "__main__":
    fake() if "--fake" in sys.argv else tts_ts.real(cut)
