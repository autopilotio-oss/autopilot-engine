# Revenue Engine 2.0: Release Report

Date: 2026-10-31
Phase: **approved live** (Seb, Oct 31: "Figure out how to finish everything yourself")

## What shipped to main (no customer-facing change)

| Area | Files |
|---|---|
| Canonical IDs + UTM | scripts/revenue/ids.py |
| Offer catalog | scripts/revenue/catalog.py → config/catalog.json |
| Revenue ledger (Gumroad, no PII) | scripts/revenue/ledger.py → state/ledger/{products,events.jsonl,summary}.json |
| Site analytics adapter | scripts/revenue/goatcounter.py → state/ledger/site.json (reports "not connected" until token) |
| Daily brief | scripts/revenue/brief.py → state/briefs/<date>.json |
| Dashboard data | scripts/revenue/dashboard_data.py |
| Competitor research schema + scoring | scripts/revenue/research.py, research/queue.jsonl, research/registry.json |
| Experiments schema | scripts/revenue/experiments.py, experiments/experiments.jsonl (2 drafts) |
| Product quality gate | scripts/revenue/quality.py |
| Approval release path | scripts/revenue/release.py |
| Flow map | scripts/revenue/flows.py → FLOWS_MAP.md |
| Tests + CI | tests/test_revenue_engine.py (16 tests), .github/workflows/ci.yml |
| Scheduled sync | .github/workflows/revenue.yml (every 3h) |
| Agent factory | tools/daily/new_agent.py now writes drafts + approval queue entry |
| Deposit Agent | back to draft (product, guide noindex, out of sitemap) pending approval |
| Docs | BASELINE, PLAN, METRICS, AGENTS, CONTENT_SYSTEM, FLOWS, RUNBOOK, offers/PREMIUM_OFFERS_DRAFT, this report |

## Shipped after approval (Oct 31, second pass)

* THE WORKSPACE rebuilt as a real product: 18 page course (tools/workspace/), sealed in products/workspace, $49 (the advertised price), permalink /l/workspace, cover, top priority for Gumroad's daily create slots. The old ttdat link no longer existed on Gumroad.
* Workspace page: new checkout link; outdated claims fixed (scheduled tasks now run in the cloud, paid plan wording, refunds via Gumroad receipt).
* Deposit Agent released (guide indexed, on home and /free/, product queued).
* docs/assets/ap.js live: UTM + first touch per visit, carried to Gumroad and Kit (Playwright tested on real pages).
* Metricool: Deposit IG reel CTA changed to link in bio (DEPOSIT isn't a ManyChat keyword); 3 duplicate X posts (Nov 1 to 3) set to draft.
* One Threads path: Metricool only (GitHub API paused since Meta's block); trend scout now schedules through Metricool.
* Instagram CTA rule + config/manychat.json.

## Decisions taken (owner delegated)

* Premium pilot: shelved. Gumroad bans install/tech support services, and Seb doesn't want manual delivery. Page stays unpublished.
* Ledger stays in the public repo: no PII, only product totals. Revisit at the first $1,000.
* GoatCounter API: not required. Revenue attribution uses Gumroad url_params + Kit fields; page views stay in the GoatCounter dashboard.
* Competitor benchmarks: the trend scout logs real competitor posts to research/queue.jsonl daily instead of Metricool's UI only feature.

## Scheduled tasks changed

| Task | Change | Rollback |
|---|---|---|
| Daily agent factory (trig_015tEKz5vpiqz7PAtDmfV1rn) | Builds a draft + approval entry; no auto publish or auto posting | Restore earlier prompt from the Oct 30 session history |
| Kit welcome sync (trig_01JueAhYdT9qTGfjVDuCL8gm) | Hourly → every 3h (`31 */3 * * *`) | Set cron back to hourly |
| Morning trend scout (trig_01RjuAqCLMe4Mbk5qD6tewo7) | Adds competitor records, canonical IDs, UTM links; routine messages removed | Remove step 4 and the IDs line |
| NEW Revenue chief of staff (trig_01BS2kUkKkcYGCqHPR8tnCUW) | Daily 08:13 ART brief + dashboard refresh | Disable the task |

Estimated Claude runs: ~29.6/day → ~14.6/day.

## Acceptance tests

| # | Test | Result | Evidence |
|---|---|---|---|
| 1 | Canonical IDs + UTM builder deterministic | PASS | tests: test_ids_and_utm |
| 2 | Ledger stores no PII | PASS | test_ledger_no_pii, salted order hash |
| 3 | Ledger dedupes repeated syncs | PASS | test_dedupe |
| 4 | Refunds and fees net correctly | PASS | test_refunds |
| 5 | Zero sales reported honestly | PASS | test_zero_sales; live summary shows 0 |
| 6 | Multi currency kept separate | PASS | test_currencies |
| 7 | Attribution read from url_params; missing = unknown | PASS | test_url_params_attribution |
| 8 | Research opportunity score + unbenchmarked rule | PASS | test_research |
| 9 | Experiments refuse winners below sample | PASS | test_experiments |
| 10 | Product quality gate | PASS | 11/11 products pass |
| 11 | Guide build reproducible, sitemap excludes drafts | PASS | test_guide_build, test_sitemap |
| 12 | No secrets in repo | PASS | test_secrets_scan |
| 13 | Site attribution (ap.js) on real pages | PASS | Playwright: UTM + ft appended to /l/subs-agent, Kit body has utm_source + first_touch, 0 page errors |
| 14 | BRAIN → AGENT → WORKSPACE funnel buyable end to end | PENDING | Product built + sealed + quality gate pass; Gumroad 10/day create limit hit today, sync retries every 6h (next 00:23 UTC) |
| 15 | GoatCounter traffic in ledger | WAIVED | attribution comes from Gumroad + Kit instead |
| 16 | Competitor benchmarks | PASS (manual source) | trend scout appends verified records daily |
| 17 | ManyChat keyword flows | WORKAROUND | no API; captions only use confirmed keywords, others use link in bio |

## Risks

* Repo is public. Ledger has no PII but product revenue totals are visible. Option: private data repo.
* Every push to main deploys the site. There is no preview environment; site changes stay on the branch until approved.
* Gumroad allows 10 new products per day; Video Agent and TikTok bundle are still pending.

## Next 3 actions

1. Confirm THE WORKSPACE, Deposit Agent, Video Agent and TikTok bundle go live on the next Gumroad sync (check-in scheduled 00:50 UTC).
2. Run the first experiments (subs_hook_001, deposit_cta_001) once posts have reach.
3. Optional for Seb: add DEPOSIT, VIDEO, SHOP, SELL to the ManyChat keyword list, then add them to config/manychat.json.
