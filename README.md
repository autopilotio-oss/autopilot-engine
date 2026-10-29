# AUTOPILOT.IO engine

Posts to Threads on a schedule through the official Threads API.

- `queue/*.json` posts to publish, written by Claude each morning
- `media/` images and videos for those posts (public, so Threads can load them)
- `state/` what was posted, views, comments and replies sent
- Drop a file named `PAUSE` in the repo root to stop all posting instantly. Delete it to resume.

Secrets (Settings, Secrets and variables, Actions): `THREADS_TOKEN` required, `GH_PAT` optional (lets the weekly job renew the key by itself).

Safety limits: at most 6 posts a day, 3 per run, nothing older than 6 hours gets posted late, and comment replies are capped at 20 per run.
