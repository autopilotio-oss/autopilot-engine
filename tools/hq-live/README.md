# AUTOPILOT.OI Chicago HQ (live)

Published as a Claude artifact (private to Seb). Single file, three.js r170 from jsdelivr.

## What is real
- Agents = your Claude scheduled tasks (list_triggers). States: WORKING, COMPLETED, IDLE, FAILED, PAUSED. Only states the scheduler reports.
- Posts today = Metricool getScheduledPosts (brand 7761544). Kit subscribers = get_growth_stats.
- Run now / Pause / Resume act on the real scheduled task, always after a confirm.
- Activity log = changes this page observed since it was opened. Replay walks the camera through them.

- ANALYST feed (hourly scheduled task): runs `python3 scripts/growthos/hq_feed.py` and writes the result to the page database at `status/hub`: GitHub Actions workers (RELAY post.yml, REELS freel.yml, STORIES market.yml, REPLY daily.yml, TILL revenue.yml, SYNC gumroad.yml, HEALTH health.yml, CI ci.yml), verified revenue from state/ledger/summary.json, approvals waiting. Older than 2.5h shows STALE.

## NOT CONNECTED (shown as such, never estimated)
Meta ad spend, Metricool analytics, per step progress, 7 day performance, revenue per agent.

## DEMO MODE
Add `#demo` to the address. Separate test dataset, red banner, never mixed with live data.

## Characters
Procedural placeholders, labeled as such. Upload a rigged GLB as `assets/agent.glb` (clips named Idle, Walk, Typing, Sit) and the page swaps it in for every agent.
Licensed sources: Adobe Mixamo, Reallusion ActorCore / Character Creator (check export license), Sketchfab Store, CGTrader, TurboSquid (check real time / web use), or a custom ArtStation commission.

## Profiles and keys
Settings: High end desktop, Standard desktop, Mobile (auto detected). Keys: 1 to 7 cameras, / search, [ ] cycle agents, A W T L views, R replay, Esc close.
