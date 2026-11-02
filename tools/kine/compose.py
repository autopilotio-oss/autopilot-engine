"""Composite: plate clips (time mapped per scene) + alpha graphics layer + mix -> mp4.
python3 tools/kine/compose.py <stem> <overlay.mov> <out.mp4>"""
import sys, json, subprocess, os
D = os.path.dirname(os.path.abspath(__file__)); ep, ov, out = sys.argv[1:4]
M = json.load(open(f"{D}/out/{ep}.meta.json")); P = M["plates"]
import shutil
def has_audio(f): return bool(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "a", "-show_entries", "stream=index", "-of", "csv=p=0", f], capture_output=True, text=True).stdout.strip())
FOLEY = M.get("foley", 0) and all(has_audio(f"{D}/plates/{p['plate']}.mp4") for p in P)
ins, fc = [], []
for i, p in enumerate(P):
    ins += ["-i", f"{D}/plates/{p['plate']}.mp4"]
    L = p["e"] - p["s"]; N = round(p["e"] * 30) - round(p["s"] * 30)  # exact frame count from absolute boundaries: no drift
    S = int(p.get("shift", 0)); sh = (f",crop=1080:{1920 - S}:0:0,pad=1080:1920:0:{S}:color=0x050605" if S > 0 else f",crop=1080:{1920 + S}:0:{-S},pad=1080:1920:0:0:color=0x050605") if S else ""
    fc.append(f"[{i}:v]trim=start={p['off']}:duration={L * p['rate'] + .1},setpts=(PTS-STARTPTS)/{p['rate']},fps=30,scale=1080:1920{sh},tpad=stop_mode=clone:stop=60,trim=end_frame={N},setpts=PTS-STARTPTS[p{i}]")
    if FOLEY: fc.append(f"[{i}:a]atrim=start={p['off']}:duration={L},asetpts=PTS-STARTPTS,aformat=sample_rates=44100:channel_layouts=stereo,apad=whole_dur={L},afade=t=in:d=.08,afade=t=out:st={max(0, L - .12)}:d=.12[a{i}]")
n = len(P); fc.append("".join(f"[p{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=0[bg]")
ins += ["-i", ov, "-i", f"{D}/out/{ep}_mix.wav"]
fc.append(f"[bg][{n}:v]overlay=0:0:format=auto,format=yuv420p[v]")
amap = f"{n + 1}:a"
if FOLEY:
    fc.append("".join(f"[a{i}]" for i in range(n)) + f"concat=n={n}:v=0:a=1,volume={M['foley']}[fol]")
    fc.append(f"[{n + 1}:a][fol]amix=inputs=2:duration=first:normalize=0[aout]"); amap = "[aout]"
cmd = ["ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", ";".join(fc), "-map", "[v]", "-map", amap,
       "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-pix_fmt", "yuv420p", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11",
       "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-ac", "2", "-shortest", "-movflags", "+faststart", out]
subprocess.run(cmd, check=True); print("composed", out)
