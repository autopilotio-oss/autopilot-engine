# Integration inventory (masked)

Work package 01 of the Master Implementation Plan (Nov 3 2026). Audited 2026-11-03 09:50 to 10:40 ART by Claude in an authenticated session. No secret values are shown anywhere in this file; secrets are named only.

Status words: **VERIFIED** (tested end to end today), **WORKING** (ran successfully, not tested end to end), **PARTIAL**, **NOT SET UP**, **BROKEN**, **UNKNOWN** (no access to check).

| System | Why we need it | Access used | Secret name (GitHub) | Status | Last test and evidence | Failure mode / rollback |
| --- | --- | --- | --- | --- | --- | --- |
| GitHub repo + Actions | Jobs, site build, CI, ledger | gh CLI (repo scope), REST only | `GITHUB_TOKEN` (built in) | WORKING | 24 workflows; latest runs all success except `refresh.yml` (see below). CI 72 tests green on 2026-11-03 | Revert commit; disable a workflow in Actions; repo PAUSE convention |
| GitHub Pages (autopilotoi.app) | Site, landing pages, media | push to `docs/` | none | VERIFIED | CNAME autopilotoi.app; hourly health check `state/health/status.json` 0 failing pages | Revert commit; Pages redeploys in about 2 min |
| GitHub Actions secrets | Keys for jobs | names read from workflow files (the secrets API is blocked from this session) | `GUMROAD_TOKEN`, `KIT_PRIVATE_KEY`, `GOATCOUNTER_TOKEN`, `THREADS_TOKEN`, `THREADS_APP_SECRET`, `IG_TOKEN`, `IG_APP_SECRET`, `IG_USER_ID`, `X_API_KEY`, `X_API_SECRET`, `X_ACCESS_TOKEN`, `X_ACCESS_SECRET`, `ELEVENLABS_API_KEY`, `PEXELS_API_KEY` | UNKNOWN which are set | Owner, scopes and renewal dates can only be seen by Seb in GitHub Settings > Secrets | Revoke at the provider, delete the secret |
| Secret hygiene | No keys in public repo or media | git grep for token patterns | n/a | VERIFIED clean | 0 matches in text files (only binary font false positives). New CI test `tests/test_secrets.py` blocks future leaks | Rotate any leaked key at the provider |
| Gumroad API | Products, prices, orders, refunds, covers, offer codes | `GUMROAD_TOKEN` in Actions | `GUMROAD_TOKEN` | WORKING | `gumroad.yml` success 07:37Z; ledger sync 10:43Z `sales_api ok`, `products_api ok`. All 14 live prices match `config/offers.json` (health `gumroad_offer:*`, `library_price:*`) | Product edits are versioned in `products/*/product.json`; revert + resync |
| Gumroad checkout + delivery | Taking money, sending the kit | Seb's test order | n/a | PARTIAL | Seb bought Front Desk Kit with one use 100% code SEBTEST9089 on 2026-11-02; receipt and PDF arrived (screenshots in chat). **A $0 order is invisible to the Gumroad sales API** (ledger 0 events, product sales_count 0), so ledger, Kit and Pixel cannot be tested with a free order | Needs one small real paid order, then refund (approval requested) |
| Gumroad Ping (webhook) | Instant purchase callback | none | n/a | NOT SET UP (by design) | Site is static GitHub Pages; there is no server to receive Ping. The ledger polls the Gumroad sales API every 3 h (`revenue.yml`), deduplicated by sale id. Acceptable for current volume | If instant callbacks are needed: a small serverless endpoint (approval needed, may cost money) |
| Revenue ledger | Financial truth | `scripts/revenue/ledger.py` | `GUMROAD_TOKEN` | WORKING | Idempotent by `order_paid:<hash(sale id)>`; refunds and chargebacks are separate events; test and $0 orders excluded from sales. Covered by tests | Events are append only; rerun sync |
| Kit (email) | Leads, onboarding, purchase sequence | Kit connector (account API) | `KIT_PRIVATE_KEY` (Actions) | PARTIAL | 1 subscriber ever (Seb's own test, state **inactive**: never confirmed). 0 purchases, 0 tags, 0 webhooks. 4 sequences, all 0 subscribers. Form 10118407 used by the site | Sequences and emails are editable; unpublish to stop |
| Kit double opt in | Consent | Kit UI only | n/a | BLOCKS ONBOARDING (likely) | Seb's test signup stayed inactive, and the routing task only routes active subscribers, so a person who does not click the confirm email gets nothing | Seb: Kit > form 10118407 > Settings > Incentive: turn off double opt in, or keep it and accept the drop |
| Kit welcome routing | Puts form signups into the right sequence | scheduled task `AUTOPILOT.OI Kit welcome sync` every 3 h | Kit connector | WORKING (idle) | Last run 12:31Z ok, 0 routed (no active subscribers) | Disable the task |
| Kit + Gumroad purchase automation | Buyer onboarding | Kit UI only | n/a | NOT SET UP | `list_purchases` returns 0 and Kit shows no Gumroad source. Needs Seb: Kit > Settings > Integrations > Gumroad, then a Visual Automation (Purchase: Front Desk Kit > sequence 2954468) | Turn the automation off |
| Meta ad account | Optional paid tests | Adspirer connector | n/a (OAuth in Adspirer) | WORKING | Account `1615960133613424` active. Campaign `120248645551300265` (Instagram boost, $25/day) schedule ended Nov 1 17:15 ART; **PAUSED 2026-11-03 10:10 ART** with Seb's approval. Lifetime spend $49.89, 647 clicks, 0 sales | Owner should set it to paused so nobody can extend it (live ad change: approval requested) |
| Meta Pixel | Marketing signal (not accounting truth) | Adspirer `list_meta_pixels` | n/a | NOT SET UP | **0 pixels exist** on the ad account. `docs/assets/ap.js` has `PIXEL = ''` and fires nothing | Seb creates the pixel in Events Manager and pastes the ID in Gumroad Settings > Third party analytics; I add it to `ap.js` |
| GoatCounter | Visits, UTM, CTA clicks | script in `docs/assets/ap.js` on all 33 content pages | `GOATCOUNTER_TOKEN` | PARTIAL | Counting script installed and fires `checkout-click`, `optin`, demo picks. Reading the data is blocked: no API token (SALES.md "Visits: not connected") | Seb adds a read only API token as the repo secret `GOATCOUNTER_TOKEN` |
| Metricool | Scheduling and analytics | Metricool connector | n/a (OAuth) | VERIFIED | Brand 7761544. 4 posts published 2026-11-02 22:30 ART on IG, TikTok, Threads, X with public URLs; analytics returned for all 4 networks | Move posts to draft; no deletes |
| ManyChat | Instagram comment keyword to DM | none (no API) | n/a | UNKNOWN | Keyword list kept in `config/manychat.json` (Seb confirmed); DM link goes to /free/ | Seb manages in ManyChat |
| Threads direct API | `post.yml` approval issues, keyword replies | `THREADS_TOKEN` + encrypted `state/token.enc` | `THREADS_TOKEN`, `THREADS_APP_SECRET` | WORKING, renewal at risk | `post.yml` success today; but weekly `refresh.yml` failed 2026-11-01: "Invalid OAuth access token, cannot parse" (the `THREADS_TOKEN` secret is stale; posting uses the refreshed encrypted copy). Long lived tokens expire after 60 days | Seb pastes a fresh Threads token into `THREADS_TOKEN` |
| Instagram Graph API | Comment replies | `IG_TOKEN` | `IG_TOKEN`, `IG_APP_SECRET`, `IG_USER_ID` | WORKING | `daily.yml` success 12:03Z | Revoke in Meta |
| X API | Metrics | `X_*` | 4 secrets | WORKING (low value) | X impressions 0 in 7 days per Metricool | none |
| ElevenLabs | Voice for reels | `ELEVENLABS_API_KEY` | same | WORKING | `freel.yml` success 09:55Z. Paid usage: cap is 2 voiced renders a day by policy | Disable workflow |
| Pexels | Stock photos | `PEXELS_API_KEY` | same | WORKING | `photos.yml` success Nov 1 | none |
| Scheduled tasks (Claude) | Operators | claude.ai scheduled tasks | n/a | WORKING | 20+ tasks; last runs succeeded. Posting tasks refocused on the Front Desk funnel on Nov 2; ads blocked in their prompts | Disable a task |
| SMS | none | none | none | NOT SET UP (by plan) | Plan: email only for 30 days | n/a |

## Gate G0 (technically sellable): NOT PASSED yet

Passed: checkout opens at the right price, delivery works (free test order), prices match everywhere, pages and links healthy, no secrets exposed.

Missing (each needs an owner action or approval):
1. One paid order recorded by Gumroad, the ledger and Kit, then refunded and shown as refunded (needs Seb's approval for a small charge).
2. Meta Pixel created and receiving `PageView`, `ViewContent`, `InitiateCheckout` on the site and `Purchase` on the Gumroad receipt.
3. Kit Gumroad integration and the purchase automation.
4. GoatCounter read token, so landing sessions are measured.
