"""Voice an ink film (tools/ink/films/<stem>.json) with the factory voice -> tools/ink/out/<stem>.wav + words.json
python3 tools/ink/voice.py <stem> [--fake]"""
import os, sys, json
D = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(D))
sys.path.insert(0, os.path.join(ROOT, "tools", "series")); sys.path.insert(0, os.path.join(ROOT, "scripts"))
import tts_ts
ep = sys.argv[1]; E = json.load(open(f"{D}/films/{ep}.json")); os.makedirs(f"{D}/out", exist_ok=True)
tts_ts.script = lambda _: " ".join(b["say"].strip() for b in E["beats"]); tts_ts.D = f"{D}/out"; tts_ts.SPEED = float(E.get("voice_speed", 1.0))
(tts_ts.fake if "--fake" in sys.argv else tts_ts.real)(ep)
