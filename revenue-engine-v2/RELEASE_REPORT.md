# Revenue Engine 2.0: Release Report

Date: 2026-10-31
Phase: **build** (back office live on main; site changes held on a branch for approval)

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

## Held for approval (branch `feat/revenue-engine-v2`, not deployed)

* docs/assets/ap.js: first touch + UTM persistence, UTM on Gumroad links, named GoatCounter events, UTM/first_touch fields on Kit opt ins.
* docs/pilot/: noindex draft page for the premium pilot offer.

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
| 13 | Site attribution (ap.js) on real pages | PASS (branch only) | Playwright: UTM kept, appended to Gumroad links, Kit fields set |
| 14 | BRAIN → AGENT → WORKSPACE funnel buyable end to end | **FAIL** | gumroad.com/l/ttdat does not exist; /workspace/ shows "Coming soon" |
| 15 | GoatCounter traffic in ledger | BLOCKED | needs GOATCOUNTER_TOKEN secret |
| 16 | Competitor benchmarks | BLOCKED | competitors must be added in Metricool UI; scout logs manual records meanwhile |
| 17 | ManyChat keyword flows verified | BLOCKED | no ManyChat access from here |

## Risks

* Repo is public. Ledger has no PII but product revenue totals are visible. Option: private data repo.
* Every push to main deploys the site. There is no preview environment; site changes stay on the branch until approved.
* Gumroad allows 10 new products per day; Video Agent and TikTok bundle are still pending.

## Next 3 actions

1. Create THE WORKSPACE on Gumroad (or approve a new permalink) so the top tier can sell.
2. Approve or reject the Deposit Agent and the site attribution branch.
3. Add GOATCOUNTER_TOKEN and 5 competitor accounts in Metricool.
