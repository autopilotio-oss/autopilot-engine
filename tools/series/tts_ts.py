"""Voice a series episode with ElevenLabs Brian (sped to 1.2x) and word timestamps.
python tools/series/tts_ts.py <ep>   -> tools/series/<ep>.wav + <ep>.words.json   (needs ELEVENLABS_API_KEY)
python tools/series/tts_ts.py <ep> --fake   -> silent wav + estimated timings (for local previews only)"""
import os, sys, json, base64, subprocess, urllib.request, wave
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "scripts"))
D = os.path.dirname(os.path.abspath(__file__)); SPEED = 1.2
def script(ep): return " ".join(b["say"].strip() for b in json.load(open(f"{D}/eps/{ep}.json"))["beats"])
def words_from_chars(chars, starts, ends):
    out, cur, s = [], "", None
    for c, a, b in zip(chars, starts, ends):
        if c.isspace():
            if cur: out.append([cur, s, last]); cur = ""
            continue
        if not cur: s = a
        cur += c; last = b
    if cur: out.append([cur, s, last])
    return out
def real(ep):
    import tts
    key = os.environ.get("ELEVENLABS_API_KEY", "").strip()
    if not key: sys.exit("No ELEVENLABS_API_KEY")
    tts.KEY = key; vid = tts.voice_id(); text = script(ep); res = None
    for mid in [tts.model_id(), "eleven_multilingual_v2"]:
        try:
            body = json.dumps({"text": text, "model_id": mid}).encode()
            req = urllib.request.Request(f"{tts.API}/text-to-speech/{vid}/with-timestamps?output_format=mp3_44100_128", data=body, method="POST",
                                         headers={"xi-api-key": key, "Content-Type": "application/json"})
            res = json.loads(urllib.request.urlopen(req, timeout=300).read()); print("voice", vid, "model", mid); break
        except Exception as e: print("model", mid, "failed:", str(e)[:200])
    if not res: sys.exit("TTS failed")
    mp3 = f"{D}/{ep}_raw.mp3"; open(mp3, "wb").write(base64.b64decode(res["audio_base64"]))
    al = res.get("normalized_alignment") or res["alignment"]
    w = words_from_chars(al["characters"], al["character_start_times_seconds"], al["character_end_times_seconds"])
    w = [[x, round(a / SPEED, 3), round(b / SPEED, 3)] for x, a, b in w]
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", mp3, "-af", f"atempo={SPEED}", "-ac", "1", "-ar", "44100", "-sample_fmt", "s16", f"{D}/{ep}.wav"], check=True)
    os.remove(mp3); json.dump(w, open(f"{D}/{ep}.words.json", "w")); print("voiced", ep, len(w), "words")
def fake(ep):
    t, w = 0.25, []
    for x in script(ep).split():
        d = 0.12 + 0.045 * len(x); w.append([x, round(t, 3), round(t + d, 3)]); t += d + (0.28 if x[-1] in ".,:!?" else 0.04)
    n = int((t + 0.5) * 44100); f = wave.open(f"{D}/{ep}.wav", "wb"); f.setnchannels(1); f.setsampwidth(2); f.setframerate(44100); f.writeframes(b"\0\0" * n); f.close()
    json.dump(w, open(f"{D}/{ep}.words.json", "w")); print("fake timings", ep, len(w))
if __name__ == "__main__":
    (fake if "--fake" in sys.argv else real)(sys.argv[1])
