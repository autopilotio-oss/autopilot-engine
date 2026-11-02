# Kinetic editor

Full screen motion graphics cut of a factory reel episode. Built Nov 2 2026 after the factory reel test read
(subs reel: 78 IG views but 2.1s average watch, 13.5% past 3s). Style reference: kinetic type reels
(one idea per screen, giant slammed words, neon highlights, light streak wipes, typed prompt panel, counters).

## What it does
- **Cold open**: the payoff (e.g. `$1,756 a year`) is fully on screen at frame 0, before the voice starts (`cold_open`, default 0.85s). Always labeled sample data.
- **Hook as kinetic type**: every sentence of beat 1 except the last is slammed word group by word group, synced to the voice word timings. Numbers and starred hook words go neon.
- **One full screen card per agent step**: prompt typing (key words highlight as typed), agent step chain with checks and a progress bar, table rows with a counter to the total, letter with a READY TO SEND stamp, checklist with a verdict stamp, DM bubbles, CTA with the ManyChat keyword.
- Light streak + flash between steps, camera punch and shake on slams, chromatic split on entrances, burst particles on payoffs, grain, word captions with the spoken word highlighted.
- Sound: the factory reel sound design plus a slam hit; the voice is delayed by the cold open.

## Use
```
bash tools/kine/make.sh 001-subs-agent      # local, needs node+playwright, ffmpeg, numpy
gh api -X POST repos/autopilotio-oss/autopilot-engine/actions/workflows/kine.yml/dispatches -f ref=main -f "inputs[eps]=001-subs-agent"
```
Output: `docs/media/kine/<id>.mp4` + poster. Reuses `tools/freel/voice/<stem>.wav` so there is no voice spend.

Optional episode fields: `payoff` `{big, lines[], tag}` (lines support `*neon*`), `emph` (extra words to highlight), `cold_open` (seconds).

Not wired into the daily factory autopost. Switching the factory to this cut needs Seb's OK.
