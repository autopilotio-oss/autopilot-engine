"""Voice an ink film (tools/ink/films/<stem>.json) -> tools/ink/out/<stem>.wav + words.json
Film keys: "voice" (ElevenLabs voice name, default Brian), "model" (default best available), "voice_speed" (1.0 = natural).
python3 tools/ink/voice.py <stem> [--fake]"""
import os, sys, json
D = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(D))
sys.path.insert(0, os.path.join(ROOT, "tools", "series")); sys.path.insert(0, os.path.join(ROOT, "scripts"))
import tts_ts, tts
ep = sys.argv[1]; E = json.load(open(f"{D}/films/{ep}.json")); os.makedirs(f"{D}/out", exist_ok=True)
tts_ts.script = lambda _: " ".join(b["say"].strip() for b in E["beats"]); tts_ts.D = f"{D}/out"; tts_ts.SPEED = float(E.get("voice_speed", 1.0))
if E.get("voice"):
    def _vid(name=E["voice"].lower()):
        for v in tts.get("/voices").get("voices", []):
            if v.get("name", "").lower().startswith(name): return v["voice_id"]
        sys.exit("voice not found: " + name)
    tts.voice_id = _vid
if E.get("model"): tts.model_id = lambda: E["model"]
(tts_ts.fake if "--fake" in sys.argv else tts_ts.real)(ep)
