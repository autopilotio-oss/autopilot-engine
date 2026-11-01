# MONTHLY SCALE REVIEW · October 2026 · run 2026-11-01 13:20 UTC

Window: system went live Oct 30, so "October" is 2 days of operation (Oct 30 to Nov 1). Labels: OBSERVED (provider or log), CALCULATED, MISSING (source not connected, never shown as 0). Nothing here is a projection unless marked SCENARIO. Raw generated report: run-history/2026-11-01-monthly.md.

**Stage: A (Validate).** 0 verified orders, 0 Kit subscribers, visits MISSING. Expansion is blocked.

## Finances (October)
| Line | Value | Label |
|---|---|---|
| Gross (all currencies) | $0.00 (0 orders) | OBSERVED, Gumroad ledger synced 2026-11-01 10:25 UTC |
| Refunds / fees | $0.00 / $0.00 | OBSERVED |
| Net receipts | $0.00 | OBSERVED |
| Reconciliation vs Gumroad | OK, 10 products checked, 0 mismatches, 0 quarantined | OBSERVED |
| Known costs | $71.03 = Kit $39.00 (plan, owner statement) + Meta Ads $32.03 | OBSERVED |
| Meta Ads | $9.56 Oct 30 + $22.47 Oct 31, boost "If you answer the same customer...", 30,158 impressions, 406 link clicks, 0 conversions, status ACTIVE, paid from a $50 prepaid balance | OBSERVED (Meta receipts + Adspirer). **Was not in the ledger or the scoreboard ($0); recorded this run.** |
| Unknown costs | ManyChat, Metricool, ElevenLabs, Claude, Porkbun (domain) | MISSING amounts |
| Contribution / net operating result | at most -$71.03; **INCOMPLETE** while 5 costs are unknown | CALCULATED |

## Portfolio (15 catalog agents)
Sessions MISSING for every product (GoatCounter token not set). Opt-ins 0 (Kit), buyers 0, refunds 0, activation n/a, support burden 0 cases.

| Group | Products | Class |
|---|---|---|
| Live, no verified orders (12) | all_money_agents, bill, debt, deposit, raise, refund, sell, shop, subs, tiktok_agents, video, workspace | VALIDATE (all checkouts pass health checks) |
| Retired (3) | credit_agent (Meta special ad category, Gumroad list), lower_agent, money_agents | RETIRE (done) |

Of the 15 concepts: 12 are still candidates, 0 tested (both experiments are drafts, none ran), 0 have verified orders. No KEEP or IMPROVE is possible without sessions or orders.

## Channels (qualified visits, conversion, contribution)
| Channel | Reach (OBSERVED) | Qualified visits | Opt-ins / orders | Contribution |
|---|---|---|---|---|
| Meta paid boost | 30,158 impr, 406 clicks | MISSING | 0 / 0 | -$32.03 |
| Instagram organic | 98 reel views 7d, 59 followers | MISSING | 0 / 0 | n/a (tool costs unknown) |
| Threads (via Metricool) | 19 views 7d | MISSING | 0 / 0 | n/a |
| TikTok | not in Metricool; no stats collected | MISSING | 0 / 0 | n/a |
| Email (Kit) | 0 subscribers | n/a | 0 / 0 | -$39.00 |
No channel can be ranked: without visit data, raw reach is the only number and it is not the decision metric.

## Experiments
Weekly runs so far: 1 (Oct 31). Experiments subs_hook_001 and deposit_cta_001 are both DRAFT; deposit_cta_001 is blocked on the GoatCounter token. No results, no failures to learn from yet. The unplanned Meta boost is the only paid test that ran, and it had no hypothesis, cap or measurement.

## Reliability (Oct 30 to Nov 1)
| Integration | Incidents | Recovery | Recurrence | Alert |
|---|---|---|---|---|
| Viral queue guard | 1 SEV-1 (daily stories wrote 5 ungated items) | contained this run, about 35 min after alert | daily until fixed | GitHub issue #4 in 1 s |
| Gumroad checkout (bill) | 1 SEV-1 | 30 min | none | issue #3 in 1 s |
| Site (home marker) | 1 SEV-2 | 2 min | none | not sent (resolved first) |
| Metricool / Instagram | 2 SEV-2 (IG restricted Oct 30; 2 Threads media errors Nov 1) | retried same day | 2 in 3 days | email intake only |
| Meta ads | 2 SEV-2 (same credit ad rejection, IG and FB copies) | n/a, product retired | none | email intake only |
| Support worker | 1 SEV-3 (heartbeat 16.5h vs 16h) | ran 13:15 UTC | first | by design not sent |
Open: 3 Oct 30 email incidents never closed (stale), SEV-3 support, SEV-1 guard (closes on the next hourly probe). Flaky automations: direct Threads API workflow (token unparseable, already paused: keep it circuit broken), market data fetch for the 8:30 story (no retry), test_guide_pages_build_reproducibly fails on main.

## Keep doing
- Gumroad reconciliation and checkout probes: both caught and closed real issues within 30 min.
- NO PROOF, NO POST gate and approval-only publishing.

## Stop doing
- Spend outside the tracked plan (the Meta boost ran 2 days at $16/day with no cap, no UTM read, no hypothesis).
- Generators writing straight into queue/. Fixed this run: daily_stories.py now writes to queue/hold/ (drafts), and today's 5 stories moved there.

## Improve
- Measurement first: GoatCounter token, so visits, checkout clicks and opt-ins per source exist.
- Daily Pulse reads Meta spend (Adspirer or receipts) into the scoreboard; close stale email incidents.

## Explore (hypothetical, needs evidence)
- Whether the 406 boost clicks reached a guide at all (needs the visit data first).

## Approval requests (none acted on)
1. Meta boost "If you answer the same customer..." is ACTIVE: $32.03 spent, 0 orders, prepaid balance about $18 left. Pause it, or count it against the campaign's $60 ad cap?
2. Add the GOATCOUNTER_TOKEN repo secret ($0) and tell us the monthly amounts for ManyChat, Metricool, ElevenLabs, Claude and Porkbun.
3. Confirm the containment change (daily stories go to queue/hold/ as drafts, not queue/). Applied under the standing NO PROOF rule; say "revert" to undo.

## Next month (November) scenarios, not promises
| Scenario | Assumptions | Verified orders | Net receipts |
|---|---|---|---|
| Low | organic reach stays under 1k views/week, no tracking fix | 0 to 2 | under $20 |
| Base | tracking live by Nov 4, flagship reels go out Nov 3 to 4, guide to checkout 1% | 3 to 10 | $20 to $100 (mostly $7 LAUNCH30 kits) |
| High | one reel passes 10k views and the subs funnel converts 2% | 10 to 25 | $100 to $300 |

## Next month scoreboard (max 3 priorities)
| Priority | Target metric | Baseline | Budget cap | Stop loss | Owner | Due |
|---|---|---|---|---|---|---|
| 1. Measure the funnel | visits, checkout clicks, opt-ins per utm_source readable daily | MISSING | $0 | n/a | Seb (token), system (reports) | Nov 4 |
| 2. First verified customers via Subscription Leak (FIRST SALES MODE) | verified orders | 0 | ads $60 total incl. the $32.03 already spent, only if Seb approves | stop any ad after $15 with 0 checkout clicks | operator; Seb approves spend | Nov 10 |
| 3. Reliability clean | SEV-1 recurrences 0; stale incidents closed; main tests green | 2 SEV-1, 1 red test | $0 | n/a | system | Nov 8 |

Quarterly expansion checkpoint (paid acquisition, affiliates, membership, localization, white label): not due; first one with the January review. All stay hypothetical at Stage A.
