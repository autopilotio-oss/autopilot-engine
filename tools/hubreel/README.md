# Hub reels (animated, no voice)

13.1 s vertical reels built from the hub carousels: 128 BPM, 28 beats (7 bars), so audio and video loop on the bar.
Frame 0 shows the full hook; the lime CTA slides off at the end to reveal that same frame, so the replay is seamless.
Key text stays inside the safe zone (x <= 940, y <= 1540 on 1080x1920).

Render: put Anton-Regular.ttf, Inter-Bold.otf, Inter-Medium.otf, JetBrainsMono.ttf next to the html, then
  node render.js $PWD/team_of_5.html out_ig full ig    (tt = TikTok ending with link in bio + URL)
  python3 music.py music.wav
  ffmpeg -framerate 30 -i out_ig/%04d.jpg -i music.wav -c:v libx264 -crf 17 -pix_fmt yuv420p -c:a aac -af loudnorm=I=-14:TP=-1.5 -t 13.125 out.mp4
Status: team_of_5 final (Nov 19) waiting for Seb's approval. Nothing scheduled.
