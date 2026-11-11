# FIRST SALES MODE: final report (Nov 1 to Nov 10 2026)

Written 2026-11-11 12:20 UTC by the scheduled final report run. Goal: 10 verified customers (Gumroad orders, not refunded). Labels: OBSERVED (read from a source this run or a committed record), CALCULATED (math on observed numbers), MISSING (not readable; never treated as zero).

## Result: 0 of 10 verified customers. Goal missed.

## 1. Facts

### Sales (python3 scripts/growthos/orders.py sync, then report, 2026-11-11 ~12:20 UTC)
| Item | Value | Label |
|---|---|---|
| Verified orders Nov 1 to Nov 10 | 0 | OBSERVED (sync: 0 new events; Gumroad reconciliation ok, 10 products, 0 mismatches) |
| Gross | $0.00 | OBSERVED |
| Gumroad fees | $0.00 | OBSERVED |
| Refunds | $0.00 (0) | OBSERVED |
| Net receipts | $0.00 | CALCULATED (gross minus refunds minus fees) |
| Orders using LAUNCH30 | 0 | OBSERVED |
| Orders by product | none | OBSERVED |
| Orders by utm_source / utm_content | none (0 unattributed, 0 quarantined) | OBSERVED |

### Costs (python3 scripts/growthos/costs.py report, month 2026-11)
| Item | Value | Label |
|---|---|---|
| Meta ads, Nov 1 | $17.86 (boost 120248645551300265, pre-campaign IG boost) | OBSERVED (spend.recorded event, Adspirer read Nov 2) |
| Meta ads, Nov 2 to Nov 10 | $0 new spend; boost schedule ended Nov 1, set PAUSED Nov 3 (Seb: "Approve pause") | OBSERVED (decision-log Nov 3, daily scoreboard rows) |
| Meta ads, live re-check this run | Adspirer refused: 15 call monthly quota used, resets Nov 29 | MISSING |
| Meta results in window | Nov 1 day: not split out; lifetime of the boost Oct 30 to Nov 1: $49.89, 647 clicks, 0 conversions | OBSERVED (decision-log Nov 2, Adspirer) |
| Meta ad spend before the window (Oct 30 to 31) | $32.03, not counted in this window | OBSERVED |
| ElevenLabs (voice) | amount unknown; API key returns HTTP 401 since Nov 10 | MISSING |
| Kit subscription | $39/mo (owner statement) | OBSERVED |
| ManyChat, Metricool, Claude, Porkbun domain | amounts unknown | MISSING |
| GitHub | $0 (public repo) | OBSERVED |
| Known November costs | $56.86 (Kit $39.00 + Meta $17.86) | CALCULATED |
| Contribution | $0.00 - $56.86 = -$56.86, INCOMPLETE (5 unknown costs) | CALCULATED |

### Audience
| Item | Value | Label |
|---|---|---|
| Kit subscribers gained Nov 1 to 10 | 0 new, 0 cancellations, 0 total | OBSERVED (Kit get_growth_stats) |
| GoatCounter guide visits | not readable (no API token in the operator) | MISSING |
| GoatCounter checkout-click events | not readable | MISSING |
| Instagram followers | 85 on Nov 10 / Nov 11 (59 on Nov 1) | OBSERVED (Daily Pulse rows) |

### Factory reels posted Nov 1 to Nov 10 (Metricool brand 7761544, read this run, organic)
Instagram (IGRE). Metricool retention field returned empty for every reel, so retention = MISSING; average watch and 3 second view rate are shown instead. Timestamps are UTC; the first three went out the evening of Oct 31 ART.

| Reel | IG posted (UTC) | Reach | Views | Avg watch s | 3s view rate | Shares | Saves | Comments | Likes | Orders | Checkout clicks |
|---|---|---|---|---|---|---|---|---|---|---|---|
| late-night-reply | Nov 8 13:03 | 99 | 111 | 3.75 | 33.3% | 0 | 0 | 0 | 0 | 0 | MISSING |
| late-payer | Nov 9 13:04 | 60 | 62 | 3.43 | 30.5% | 0 | 0 | 0 | 0 | 0 | MISSING |
| subs-leak | Nov 2 13:04 | 37 | 42 | 2.98 | 25.6% | 0 | 1 | 0 | 2 | 0 | MISSING |
| refund-agent | Nov 1 01:02 | 15 | 14 | 6.50 | 36.4% | 0 | 0 | 0 | 1 | 0 | MISSING |
| quiet-quotes | Nov 7 13:04 | 49 | 54 | 3.97 | 18.7% | 0 | 0 | 0 | 0 | 0 | MISSING |
| quote-tonight | Nov 10 13:06 | 5 | 6 | 2.55 | 16.7% | 0 | 0 | 0 | 0 | 0 | MISSING |
| price-inquiry | Nov 5 13:05 | 50 | 56 | 2.02 | 16.0% | 0 | 0 | 0 | 1 | 0 | MISSING |
| shop-finder | Nov 1 00:15 | 61 | 74 | 2.86 | 12.7% | 0 | 0 | 0 | 1 | 0 | MISSING |
| ai-employees | Nov 1 02:02 | 58 | 69 | 2.44 | 10.0% | 0 | 0 | 0 | 0 | 0 | MISSING |
| review-agent | Nov 6 13:07 | 70 | 79 | 1.72 | 6.8% | 0 | 0 | 0 | 2 | 0 | MISSING |

TikTok (TKPO, views only; reach, watch time and full watch rate came back empty = MISSING): ai-employees 141 views (3 likes), raise-agent 118, refund-agent 99, subs-leak 84, shop-finder 44. 0 shares, 0 comments on all.

No IG reel row returned for content-machine, money-agents, raise-agent (IG), debt-agent, refund-fighter, charged-twice, bill-coach: these were thinned, parked or drafted (Nov 1 thinning, Nov 3 money agent park, Nov 4 IG row switch). MISSING, not zero.

Threads and X per reel: MISSING (Threads disconnected from Metricool since about Nov 6 23:30 ART; X analytics 403).

viral/evidence.jsonl: 3 reference entries, all views "not verifiable". No external evidence backed a format.

## 2. Winning content
Ranking rule: attributed orders, then checkout clicks, then retention. Orders were 0 for every reel and checkout clicks are MISSING, so the ranking falls to retention (3 second view rate and average watch, IG, reach 30 or more).

1. late-night-reply (Front Desk Kit, after hours message): 33.3% view rate, 3.75 s average watch, 99 reach, best reach of the campaign. Why: the hook is a concrete moment every service owner knows (customer messages late at night) and the payoff is shown on screen.
2. late-payer (Invoice Chaser, $9.99): 30.5% view rate, 3.43 s, 60 reach. Why: names a person and a feeling ("Dave is a week late and you hate the awkward text"), pain first, product second.
3. subs-leak (Subscription Leak Hunter): 25.6% view rate, 2.98 s, the only reel with a save (1) and 2 likes. Why: universal money pain (forgotten subscriptions). Parked after Nov 3 with the money agents.

Note: refund-agent had the best retention (36.4%, 6.5 s) but on 15 reach, too small to call.

Formats to stop:
- Instruction first hooks that open with "Type X..." (review-agent 6.8% view rate, 1.72 s; price-inquiry 16.0%).
- Multi agent overview lists (ai-employees "Seven AI agents": 10.0% view rate).
- "Comment AGENTS" as the only conversion path: 0 comments on every reel, 0 Kit subscribers.

Across all reels: 0 shares and 0 attributed orders. Nothing is a verified sales winner.

## 3. Improvements made (git log Nov 1 to Nov 10, decision-log.md)
- Nov 1: /quiz/ and /g/lower/ redirects keep UTMs; reel template holds the final number about 1 s.
- Nov 1: daily story batch moved to drafts (cleared SEV-1 viral_queue_guard); stats workflow push race fixed; guide pages build reproducibly.
- Nov 2: canonical offer manifest with CI rules; stale offer copy fixed across keyword replies, /brain/, /free/, support KB.
- Nov 2: Gumroad covers showing stale prices replaced; price recorded when the list API omits a product.
- Nov 2: LAUNCH30 taken off Office Autopilot while on hold; sync deletes withdrawn codes.
- Nov 2: health marker test added so every page probe matches the committed page.
- Nov 2: paid ads withdrawn until a Meta Pixel exists (Seb: "Fix it"); Nov 3 the leftover boost was paused (Seb approved).
- Nov 2 to 3: Front Desk Starter renamed and made the /free/ lead; UTM source kept from /brain/ through to checkout.
- Nov 3: offer simplified for owners new to AI (4 tools, $24 Owner Toolkit); false "most popular" label removed.
- Nov 3: Master Plan WP01 to 05: CI secret scan, events schema, purchase tracking tests, true ad spend, daily report.
- Nov 4: site redesign v5 and $9.99 tools shipped (Seb); TikTok Agent v5; $39 Your AI Team bundle; platform cadence per network.
- Nov 4: approved posts restored after the Pulse wrongly drafted 12 chat scheduled posts.
- Nov 5 to 8: false worker alerts stopped; kit_sync health limit fixed; disabled workers resolve stale incidents.
- Nov 6: IG reels review-agent and quiet-quotes restored from draft; 3 questions an hour on Threads and X (Seb).
- Nov 7 to 10: honesty fixes on Sales Agent, Subscription Agent, library hero, /brain/, video guide headline; "tap for sound" pill removed from silent demos.

## 4. Housekeeping (no spending, pricing or publishing action taken)
- Meta campaign: the only campaign that spent (120248645551300265) was set PAUSED Nov 3 and its schedule ended Nov 1 (OBSERVED, decision-log). The Nov 5 ad test was never launched; campaign.json ads.status is "off" with no campaign id. Live confirmation this run: MISSING (Adspirer quota used up until Nov 29).
- LAUNCH30: state/gumroad_debug.json (committed 2026-11-11 07:42 UTC) shows offer_code_deleted for all 11 products in campaign.json offer_code.products. Workflow dispatch not needed. 10 site pages still carry a hidden ("display:none") LAUNCH30 banner line; harmless but worth removing in the next site pass.
- Posting mode: config still holds Seb's Nov 4 01:39 ART approval "yes" to keep autopost on after Nov 10 for gated posts (campaign.json approvals.autopost_after_nov10, MANAGER.md). flags.json outbound_publishing is true. This run's brief expects approval based posting after Nov 10. Not changed here; the operator or Seb decides which instruction stands.

## 5. Next (ranked)
1. Make the funnel measurable before anything else: GoatCounter read token for the operator, a live Meta Pixel, Threads reconnected in Metricool, and a working ElevenLabs key (401 since Nov 10). NEEDS YOUR OK only if the ElevenLabs fix means paying for a plan.
2. Only pain first owner reels in the late-night-reply and late-payer pattern (named person, real moment, result on screen); stop "Type X" openers and agent lists; add the Kit opt in to /free/ so the DM link captures emails. No spend.
3. Decide posting mode after Nov 10: keep autopost (your Nov 4 "yes") or go back to approval based. NEEDS YOUR OK.
