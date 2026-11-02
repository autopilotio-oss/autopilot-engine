"""Composite: plate clips (time mapped per scene) + alpha graphics layer + mix -> mp4.
python3 tools/kine/compose.py <stem> <overlay.mov> <out.mp4>"""
import sys, json, subprocess, os
D = os.path.dirname(os.path.abspath(__file__)); ep, ov, out = sys.argv[1:4]
M = json.load(open(f"{D}/out/{ep}.meta.json")); P = M["plates"]
ins, fc = [], []
for i, p in enumerate(P):
    ins += ["-i", f"{D}/plates/{p['plate']}.mp4"]
    L = p["e"] - p["s"]
    fc.append(f"[{i}:v]trim=start={p['off']}:duration={L * p['rate'] + .05},setpts=(PTS-STARTPTS)/{p['rate']},fps=30,scale=1080:1920,trim=duration={L},setpts=PTS-STARTPTS[p{i}]")
n = len(P); fc.append("".join(f"[p{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=0[bg]")
ins += ["-i", ov, "-i", f"{D}/out/{ep}_mix.wav"]
fc.append(f"[bg][{n}:v]overlay=0:0:format=auto,format=yuv420p[v]")
cmd = ["ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", ";".join(fc), "-map", "[v]", "-map", f"{n + 1}:a",
       "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-pix_fmt", "yuv420p", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11",
       "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-ac", "2", "-shortest", "-movflags", "+faststart", out]
subprocess.run(cmd, check=True); print("composed", out)
