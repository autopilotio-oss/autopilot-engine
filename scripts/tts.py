"""Voice a reel spec with ElevenLabs (Brian, sped to 1.2x). Usage: python scripts/tts.py <spec_name>
Reads PHRASES from tools/reel/<spec>.py, writes tools/reel/<spec>.wav (mono 44.1k 16 bit). Needs ELEVENLABS_API_KEY."""
import os, sys, json, subprocess, importlib, urllib.request
KEY = os.environ.get("ELEVENLABS_API_KEY", "").strip()
API = "https://api.elevenlabs.io/v1"
FALLBACK_BRIAN = "nPczCjzI2devNBz1zQrb"
def get(path):
    return json.loads(urllib.request.urlopen(urllib.request.Request(API + path, headers={"xi-api-key": KEY}), timeout=60).read())
def voice_id():
    try:
        for v in get("/voices").get("voices", []):
            if v.get("name", "").lower().startswith("brian"): return v["voice_id"]
    except Exception as e: print("voices lookup failed, using default Brian id:", str(e)[:120])
    return FALLBACK_BRIAN
def model_id():
    want = os.environ.get("ELEVEN_MODEL", "").strip()
    if want: return want
    try:
        ids = [m["model_id"] for m in get("/models") if m.get("can_do_text_to_speech")]
        for pref in ("v4", "v3", "multilingual_v2"):
            for i in ids:
                if pref in i and "flash" not in i and "turbo" not in i: return i
    except Exception as e: print("models lookup failed:", str(e)[:120])
    return "eleven_multilingual_v2"
def main(name):
    if not KEY: sys.exit("No ELEVENLABS_API_KEY")
    d = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "tools", "reel")
    sys.path.insert(0, d); spec = importlib.import_module(name)
    text = " ".join(t for t, _ in spec.PHRASES)
    vid, mid = voice_id(), model_id(); print("voice", vid, "model", mid)
    body = json.dumps({"text": text, "model_id": mid}).encode()
    req = urllib.request.Request(f"{API}/text-to-speech/{vid}?output_format=mp3_44100_128", data=body, method="POST",
                                 headers={"xi-api-key": KEY, "Content-Type": "application/json", "Accept": "audio/mpeg"})
    mp3 = os.path.join(d, name + "_raw.mp3"); open(mp3, "wb").write(urllib.request.urlopen(req, timeout=300).read())
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", mp3, "-af", "atempo=1.2", "-ac", "1", "-ar", "44100", "-sample_fmt", "s16", os.path.join(d, name + ".wav")], check=True)
    os.remove(mp3); print("voiced", name)
if __name__ == "__main__": main(sys.argv[1])
