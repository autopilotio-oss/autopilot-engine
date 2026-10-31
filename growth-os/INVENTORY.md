# P0-01 Inventory (observed 2026-10-31, repo SHA 7f20453)

Everything below was observed in this session (repo files, GitHub API, connector calls). "UNVERIFIED" means I could not see it.

## Repository and deployment
| Item | Observed |
|---|---|
| Repo | github.com/autopilotio-oss/autopilot-engine, **public**, default branch main, no branch protection (API 404 "Branch not protected") |
| Site | GitHub Pages from `docs/`, custom domain autopilotoi.app; every push to main deploys (no staging environment) |
| Size | .git 569 MB, docs 438 MB (media files) |
| Stack | Python 3 scripts + Node (Playwright/three.js renders) + GitHub Actions; no database; state in git as JSON/JSONL |
| Tests | pytest: tests/test_revenue_engine.py (16), tests/test_viral_gate.py (19); CI workflow `Tests` on push |

## GitHub Actions workflows (15)
| Workflow | Trigger | Does |
|---|---|---|
| post.yml Post to Threads | every 15 min + push queue/ | Threads API publisher. **Paused** by config/threads.json (Meta blocked the app) |
| daily.yml Collect stats and reply | hourly | Reads Threads API (blocked), comment replies |
| market.yml Daily stories | daily 12:00 UTC | Renders story images |
| gumroad.yml | every 6h + push products/ | Creates/updates Gumroad products, writes docs/live.json |
| revenue.yml | every 3h :53 | Gumroad ledger, catalog, quality gate |
| refresh.yml | weekly | Threads token refresh |
| ci.yml Tests | push | pytest + quality gate |
| demo, office, hq, reel, series | push/dispatch | Video renders (ElevenLabs voice) |
| connect, connect_ig, check_ig | manual | Meta app setup (blocked) |

Secrets referenced by name (values never read): ELEVENLABS_API_KEY, GUMROAD_TOKEN, GOATCOUNTER_TOKEN (not set: ledger says not connected), KIT_PRIVATE_KEY (kit file sealing key, not Kit email), IG_*, THREADS_*, X_*. The secrets list API is blocked from this session, so presence is inferred from workflow behavior only.

## Claude scheduled tasks (workers)
| Task | Schedule (ART) | Side effects today |
|---|---|---|
| Revenue chief of staff | daily 08:13 | read only + brief + dashboard |
| Morning trend scout | daily 08:41 | **schedules Threads posts + stories in Metricool** |
| Instagram + Threads loader | daily 09:23 | **schedules every queue item + cross posts to TikTok/YouTube/FB** |
| Daily content upgrade | daily 03:47 | **writes new posts into queue/** (loader publishes them) |
| Day series writer | daily 15:37 | **renders and schedules a reel in Metricool** |
| Voiced reel maker | Mon, Thu 13:47 | **renders and schedules IG reel + Threads** |
| Weekly email newsletter | Sun 11:13 | **creates and schedules a Kit broadcast to all subscribers** |
| Kit welcome sync | every 3h | adds new subscribers to one sequence |
| Agent factory (draft only) | daily 06:43 | drafts products, no publishing |
| TikTok Shop intel | Wed 11:13 | updates playbook and guides |
| AUTOPILOT.IO weekly intel | disabled | none |

**Finding:** 6 workers can put public content or email out without passing NO PROOF, NO POST or owner approval. That conflicts with policy priority 1. Cutover needs owner authorization (see RELEASE report).

## Providers (connector or token observed working this session)
| Provider | Access | Status |
|---|---|---|
| Gumroad | GUMROAD_TOKEN in Actions (sales + products API ok) | LIVE (polling every 3h; no webhook endpoint exists: static hosting) |
| Metricool | Claude connector, brand 7761544 (IG, Threads, TikTok, X) | LIVE |
| Kit | Claude connector | LIVE (0 subscribers) |
| GitHub | git + REST (repo scoped) | LIVE (no org endpoints, no secrets list) |
| ElevenLabs | key in Actions | LIVE (renders succeeded today) |
| ManyChat | none | **LIVE BLOCKED**: no API or connector; keyword list edited by Seb only |
| GoatCounter | script on site, no API token | **LIVE BLOCKED** for reads |
| Claude artifacts | connector (dashboard + DB) | LIVE |
| Meta Graph API (own app) | blocked by Meta | DEAD (Metricool replaces it) |
| Email inbox (support) | no Gmail connector | **LIVE BLOCKED**: buyer replies reach Seb's email only |

## Offers (products/ and docs/live.json)
Live and buyable (8): subs, refund, raise, bill, debt, sell, shop agents ($10), all-money-agents ($39).
Queued for Gumroad create (daily limit): workspace ($49), deposit-agent ($10), video-agent ($10), tiktok-agents ($24).
Retired: credit-agent, lower-agent, money-agents.
Free guides: 11 under docs/g/, plus /brain/ (AI Front Desk), /free/, /store/, /workspace/.

## Baseline numbers (observed)
0 Gumroad orders all time (ledger summary 2026-10-31T17:44Z). 0 Kit subscribers. Instagram 34 followers, Threads 0 (Metricool). Website traffic UNVERIFIED (no GoatCounter API).

## Unverified areas
GitHub secret presence (only inferred), ManyChat automation state, GoatCounter numbers, Gumroad refund policy setting, whether any buyer support email has arrived, TikTok/YouTube analytics beyond Metricool.
