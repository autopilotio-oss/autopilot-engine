# How AUTOPILOT.OI runs without Seb, without an open chat and with his computer off

Two runners, both in the cloud. Neither needs a Claude chat open or Seb's computer on.

## Runner 1: GitHub Actions (deterministic code, free on a public repo)
| Job | Schedule (UTC) | Does | Evidence it runs on its own |
|---|---|---|---|
| Growth OS health checks | hourly :11 | live page probes, sync freshness, paid but undelivered, audit chains, job queue, worker heartbeats; incidents; safe re-dispatch of stale syncs; GitHub issue alerts | drill 2026-10-31 18:47: issue #2 opened, resolved and closed 18:51 by the next run |
| Revenue ledger + event store | every 3h :53 | Gumroad orders/refunds/fees, event store, reconciliation, catalog, quality gate | run 2026-10-31 18:36 success |
| Gumroad products | every 6h :23 | create/update products, docs/live.json | 2 scheduled runs observed (event=schedule) |
| Tests | every push | 59 tests | green on every Growth OS commit |

## Runner 2: Claude scheduled tasks (judgment work; run in Anthropic's cloud)
| Worker | Schedule (ART) | Side effects | Messages Seb |
|---|---|---|---|
| Daily Pulse | daily 08:13 | read only; one safe internal fix; dashboard refresh; sets unapproved new Metricool posts to draft | only critical, security, cost cap, authorization needed |
| Viral Content Lab | daily 03:47 | research, original concepts, gate, previews, Approval Queue | only when a concept is READY for him |
| Trend scout (research only) | daily 08:41 | research records, trend candidates | never |
| Publisher (approved only) | daily 09:23 | schedules ONLY what `publish.py plan` allows | only if an approved post fails after retry |
| Kit welcome sync | every 3h | adds active, opted in subscribers to their welcome sequence | only after 2 failures in a row |
| Weekly Growth Sprint | Mon 09:37 | one experiment, waste review, reliability audit | THE weekly report |
| Monthly Scale Review | 1st 10:17 | finance truth, portfolio, scale stage, next month plan | only with approval requests or red flags |
| Newsletter (draft) | Sun 11:13 | Kit DRAFT only | never (listed in weekly report) |
| TikTok Shop intel | Wed 11:13 | playbook updates; guide fixes proposed | never |
| Disabled at cutover | Day series, voiced reel maker, agent factory | cannot publish under NO PROOF, NO POST; re-enable from growth-os/rollback/ | |

Every Claude worker ends with `heartbeat.py beat <worker>`; the hourly GitHub job flags a late or failed worker
(config/growthos/workers.json) as an incident, so a dead worker is caught even if every Claude task is down.

## Alert paths
1. GitHub issue assigned to the repo owner (sent from GitHub Actions; works with no Claude session). Verified 2026-10-31 (issue #2). Seb must confirm he receives GitHub notifications on his phone/email.
2. Claude message from the Daily Pulse (SEV-1/SEV-2 not yet reported, security, cost cap, authorization).
Unsent alerts stay `sent: false` in state/health/alerts.jsonl; nothing claims Seb was told unless a channel accepted it.

## What still needs a human
Approving content (Approval Queue page or "approve <content_id>"), spend caps, any spending, price changes, new
products going live, deployments of customer facing changes, refunds and disputes, ManyChat keyword edits.
