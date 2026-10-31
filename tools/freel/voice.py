"""Voice a factory reel with ElevenLabs Brian (1.2x) + word timings.
python tools/freel/voice.py <ep-stem> [--fake]"""
import os, sys, json
D = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(D))
sys.path.insert(0, os.path.join(ROOT, "tools", "series")); sys.path.insert(0, os.path.join(ROOT, "scripts"))
import tts_ts
ep = sys.argv[1]; E = json.load(open(f"{D}/eps/{ep}.json"))
tts_ts.script = lambda _: " ".join(b["say"].strip() for b in E["beats"]); tts_ts.D = D
(tts_ts.fake if "--fake" in sys.argv else tts_ts.real)(ep)
