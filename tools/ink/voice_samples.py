"""Short ElevenLabs voice auditions for an ink film hook -> tools/ink/voice/samples/<voice>.mp3 (+ list of voices on the account)
python3 tools/ink/voice_samples.py "Chris,Eric,Liam,Jessica,Brian" """
import os, sys, json, urllib.request
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "scripts"))
import tts
KEY = os.environ.get("ELEVENLABS_API_KEY", "").strip(); tts.KEY = KEY
if not KEY: sys.exit("No ELEVENLABS_API_KEY")
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "voice", "samples"); os.makedirs(D, exist_ok=True)
TEXT = ("This doctor does not exist. An AI made her up in under a second... "
        "And it wasn't a glitch. It did exactly what it was built to do.")
voices = tts.get("/voices").get("voices", [])
open(f"{D}/voices.txt", "w").write("\n".join(f'{v.get("name")} | {v.get("category")} | {(v.get("labels") or {})}' for v in voices))
want = [w.strip().lower() for w in sys.argv[1].split(",")]
models = [m["model_id"] for m in tts.get("/models") if m.get("can_do_text_to_speech")]
print("models", models)
mid = next((m for m in [os.environ.get("ELEVEN_MODEL", ""), "eleven_v4", "eleven_v3", "eleven_multilingual_v2"] if m and m in models), "eleven_multilingual_v2")
for w in want:
    v = next((v for v in voices if v.get("name", "").lower().startswith(w)), None)
    if not v: print("missing voice", w); continue
    body = json.dumps({"text": TEXT, "model_id": mid, "voice_settings": {"stability": 0.4, "similarity_boost": 0.8, "style": 0.35, "use_speaker_boost": True}}).encode()
    req = urllib.request.Request(f"{tts.API}/text-to-speech/{v['voice_id']}?output_format=mp3_44100_128", data=body, method="POST",
                                 headers={"xi-api-key": KEY, "Content-Type": "application/json", "Accept": "audio/mpeg"})
    try:
        slug = w.split(" - ")[0].replace(" ", "_") + ("_" + w.split(" - ")[1].split()[0] if " - " in w else ""); data = urllib.request.urlopen(req, timeout=120).read(); open(f"{D}/{slug}_{mid.split('_')[-1]}.mp3", "wb").write(data); print("sample", w, mid, slug)
    except Exception as e: print("failed", w, str(e)[:200])
