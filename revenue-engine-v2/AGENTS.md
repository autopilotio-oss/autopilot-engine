# Agent roster: blueprint roles mapped to the jobs that already exist

Rule: merge duplicates, don't add workers. One job can hold several roles.

| # | Blueprint role | Who does it now | Autonomy | Change in this release |
|---|---|---|---|---|
| 01 | Revenue Chief of Staff | **New** scheduled task "AUTOPILOT.OI revenue chief of staff" (daily 08:13 ART) | Read only, plus alerts | Replaces the many separate daily status messages with one brief |
| 02 | Competitor Intelligence | "Morning trend scout" (daily) plus "TikTok Shop intel" (weekly) | Draft only | The scout now also writes sourced records to `research/queue.jsonl` (schema in `scripts/revenue/research.py`) |
| 03 | Creative Strategist | "Daily content upgrade" | Draft only | Every test is logged in `experiments/experiments.jsonl` with one variable, an objective and a minimum sample |
| 04 | Script + Compliance | "Day series writer", "Voiced reels", the content upgrade | Draft and review | Unchanged. Content uses canonical content_ids and UTM links. |
| 05 | Production Studio | GitHub render workflows: series, reel, demo, office, hq | Stage and review | Unchanged (demo pacing fixed today) |
| 06 | Publisher | "IG + Threads loader" (Metricool) plus `post.yml` (Threads API) | Approved items only | Unchanged. Duplicate Threads path flagged in RUNBOOK. |
| 07 | Community + Lead Router | ManyChat (manual, UNVERIFIED), `daily.yml` comment replies, "Kit welcome sync" | Scoped approved | Kit sync every 3h instead of hourly. Kit now gets UTM fields. |
| 08 | Lifecycle + Email | Kit sequences plus "Weekly newsletter" | Scoped approved | Unchanged |
| 09 | Attribution Analyst | **New** `revenue.yml` GitHub workflow (every 3h, no Claude cost) | Read only | Gumroad ledger, product inventory, GoatCounter totals, catalog |
| 10 | Product Quality Gate | **New** `scripts/revenue/quality.py`, run in CI and before every release | Blocks release | All 11 active products pass |
| 11 | Agent Factory | "Daily agent drop", renamed "agent factory (draft only)" | No auto-publish | Drafts with `draft: true`, then asks Seb. `scripts/revenue/release.py` publishes after his yes. |
| 12 | Operations Monitor | CI `ci.yml` plus Chief of Staff (`gh run list` failures) | Safe maintenance | 16 acceptance tests on every relevant push |

## Cost change (Claude scheduled task runs per day)
| | Before | After |
|---|---|---|
| Kit welcome sync | 24 | 8 |
| Daily tasks (upgrade, scout, loader, series, factory) | 5 | 5 |
| Chief of Staff | 0 | 1 |
| Weekly tasks, averaged per day | about 0.6 | about 0.6 |
| **Total** | **about 29.6** | **about 14.6 (-51%)** |

GitHub Actions are free on a public repo, so `revenue.yml` adds no cost.
