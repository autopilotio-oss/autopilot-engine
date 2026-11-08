"""Voice an ink film (tools/ink/films/<stem>.json) -> tools/ink/out/<stem>.wav + words.json
Film keys: "voice" (ElevenLabs voice name, default Brian), "model", "voice_settings" (ElevenLabs settings), "voice_speed" (ffmpeg atempo after TTS, 1.0 = natural).
python3 tools/ink/voice.py <stem> [--fake]"""
import os, sys, json, base64, subprocess, urllib.request
D = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(D))
sys.path.insert(0, os.path.join(ROOT, "tools", "series")); sys.path.insert(0, os.path.join(ROOT, "scripts"))
import tts_ts, tts
ep = sys.argv[1]; E = json.load(open(f"{D}/films/{ep}.json")); os.makedirs(f"{D}/out", exist_ok=True)
text = " ".join(b["say"].strip() for b in E["beats"]); speed = float(E.get("voice_speed", 1.0))
if "--fake" in sys.argv:
    tts_ts.script = lambda _: text; tts_ts.D = f"{D}/out"; tts_ts.SPEED = speed; tts_ts.fake(ep); sys.exit()
key = os.environ.get("ELEVENLABS_API_KEY", "").strip(); tts.KEY = key
if not key: sys.exit("No ELEVENLABS_API_KEY")
name = E.get("voice", "Brian").lower()
vid = next((v["voice_id"] for v in tts.get("/voices").get("voices", []) if v.get("name", "").lower().startswith(name)), None) or sys.exit("voice not found: " + name)
body = {"text": text, "model_id": E.get("model") or tts.model_id()}
if E.get("voice_settings"): body["voice_settings"] = E["voice_settings"]
req = urllib.request.Request(f"{tts.API}/text-to-speech/{vid}/with-timestamps?output_format=mp3_44100_128", data=json.dumps(body).encode(), method="POST",
                             headers={"xi-api-key": key, "Content-Type": "application/json"})
res = json.loads(urllib.request.urlopen(req, timeout=300).read()); print("voice", name, vid, "model", body["model_id"])
mp3 = f"{D}/out/{ep}_raw.mp3"; open(mp3, "wb").write(base64.b64decode(res["audio_base64"]))
al = res.get("normalized_alignment") or res["alignment"]
w = tts_ts.words_from_chars(al["characters"], al["character_start_times_seconds"], al["character_end_times_seconds"])
w = [[x, round(a / speed, 3), round(b / speed, 3)] for x, a, b in w]
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", mp3, "-af", f"atempo={speed}", "-ac", "1", "-ar", "44100", "-sample_fmt", "s16", f"{D}/out/{ep}.wav"], check=True)
os.remove(mp3); json.dump(w, open(f"{D}/out/{ep}.words.json", "w")); print("voiced", ep, len(w), "words, ends", w[-1][2])
