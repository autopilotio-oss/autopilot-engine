"""Score for a story ad: ElevenLabs Music from the ad's music_prompt, fitted to the ad length.
python3 tools/kine/music.py <stem> -> tools/kine/out/<stem>_music.wav (falls back to a synthesized piano score)"""
import os, sys, json, urllib.request, subprocess, wave, numpy as np
D = os.path.dirname(os.path.abspath(__file__)); ep = sys.argv[1]
E = json.load(open(f"{D}/ads/{ep}.json")); M = json.load(open(f"{D}/out/{ep}.meta.json")); dur = M["dur"]
out = f"{D}/out/{ep}_music.wav"; key = os.environ.get("ELEVENLABS_API_KEY", "").strip()
def eleven():
    body = json.dumps({"prompt": E["music_prompt"].replace("{dur}", str(round(dur))), "music_length_ms": int((dur + 1.5) * 1000)}).encode()
    for path in ("/v1/music", "/v1/music/compose"):
        try:
            r = urllib.request.urlopen(urllib.request.Request("https://api.elevenlabs.io" + path, data=body, method="POST",
                headers={"xi-api-key": key, "Content-Type": "application/json", "Accept": "audio/mpeg"}), timeout=600).read()
            if len(r) > 20000:
                open(out + ".mp3", "wb").write(r); subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", out + ".mp3", "-ac", "2", "-ar", "44100", out], check=True)
                print("music: elevenlabs", path, len(r)); return True
        except Exception as e: print("music", path, "failed:", str(e)[:200])
    return False
def synth():
    SR = 44100; n = int(SR * (dur + 1.5)); L = np.zeros(n); R = np.zeros(n); t0 = np.arange(SR * 4) / SR
    turn = E.get("music_turn", 11.0); warm = E.get("music_warm", 19.0)
    def note(f, t, g, d=3.5, pan=0):
        i = int(t * SR); m = min(len(t0), n - i)
        if m <= 0: return
        x = t0[:m]; e = np.minimum(1, x / .01) * np.exp(-x / (d / 3))
        y = (np.sin(2 * np.pi * f * x) + .35 * np.sin(4 * np.pi * f * x) * np.exp(-x * 2) + .12 * np.sin(6 * np.pi * f * x) * np.exp(-x * 3)) * e * g
        L[i:i + m] += y * (1 - max(pan, 0)); R[i:i + m] += y * (1 + min(pan, 0))
    A = [(220, 261.6, 329.6), (174.6, 220, 261.6), (196, 246.9, 293.7), (164.8, 196, 246.9)]   # Am F G Em
    B = [(261.6, 329.6, 392), (196, 246.9, 293.7), (220, 261.6, 329.6), (174.6, 220, 261.6)]   # C G Am F
    t = .2; k = 0
    while t < dur:
        prog = A if t < turn else B; ch = prog[k % 4]; g = .16 if t < turn else (.22 if t < warm else .26)
        note(ch[0] / 2, t, g * .9, 5); [note(f, t + j * .18, g * .6, 3.5, (j - 1) * .3) for j, f in enumerate(ch)]
        if t >= turn:
            for j in range(4): note(ch[j % 3] * 2, t + .5 + j * .5, g * .35, 1.2, (j % 2 - .5) * .4)
        t += 2.6 if t < turn else 2.0; k += 1
    pad = np.zeros(n); x = np.arange(n) / SR; fade = np.clip((x - turn) / 3, 0, 1) * np.clip((dur + 1 - x) / 2, 0, 1)
    for f in (130.8, 196, 261.6): pad += np.sin(2 * np.pi * f * x + np.sin(x * .7) * 2) * .05
    L += pad * fade; R += pad * fade
    m = np.stack([L, R], 1); m = m / (np.max(np.abs(m)) or 1) * .8
    w = wave.open(out, "wb"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((m * 32767).astype(np.int16).tobytes()); w.close(); print("music: synthesized fallback")
if not (key and eleven()): synth()
