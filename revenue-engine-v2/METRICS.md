# Metrics, IDs and attribution

## North star
**Monthly attributed net revenue** from kits, bundles and approved implementations. It is reported with:
- gross revenue
- refunds
- Gumroad fees
- known variable costs
- attribution coverage

Followers and views are inputs, not success.

## Definitions (Gumroad is the source of truth)
| Metric | Definition |
|---|---|
| Verified order | A Gumroad sale. Price above 0, not a test purchase. |
| Gross | Sum of `price` (cents) for verified orders, per currency. |
| Fees | Sum of `gumroad_fee`. |
| Refunds | Full refunds or chargebacks count the whole price. Partial refunds count `amount_refunded_cents` when Gumroad provides it. |
| Net | Gross minus fees minus refunds. Sales tax is not included (Gumroad handles tax). Currencies are never added together. |
| Contribution | Net minus known variable costs (ElevenLabs characters, paid tools). Reported separately, and only when the costs are known. |
| Qualified lead | A Kit subscriber (explicit opt-in) that is not cancelled. |
| Attribution coverage | Verified orders with a known `utm_source` divided by verified orders. "n/a" when there are 0 orders. |

Zero sales is reported as "0 verified orders, $0.00 net". Revenue is never extrapolated.

## Canonical IDs (`scripts/revenue/ids.py`)
| ID | Format | Example |
|---|---|---|
| offer_id | Gumroad permalink with `_` instead of `-` | `subs_agent`, `all_money_agents`, `workspace` (Gumroad `ttdat`) |
| campaign_id | `<topic>_<year>w<iso week>` | `subscription_leak_2026w45` |
| content_id | `<platform>_<format>_<offer short>_<NNN>[_<variant>]` | `ig_reel_subs_003_b` |

Platforms: ig, tt, th, x, yt, em, site.
Formats: reel, carousel, post, story, video, text, card, email, demo.

## UTM protocol
Every link we control carries all four:

```
utm_source=instagram  utm_medium=organic_social  utm_campaign=subscription_leak_2026w45  utm_content=ig_reel_subs_003_b
```

Build links with `ids.utm_url(url, platform, campaign_id, content_id)`.

**Where the parameters go**
- **Instagram and TikTok** captions can't hold clickable links. Their UTMs go on the ManyChat reply link and the bio link (Seb sets those). Without them, those visits arrive with no source and stay "unknown".
- **Threads, X and email** links carry UTMs directly.

## Event contract
| Event | Where it's recorded | Fields |
|---|---|---|
| content_published | Metricool post id. The Chief of Staff snapshot stores the counts. | content_id (caption or queue id), platform, external_post_id, campaign_id, ts |
| landing_view | GoatCounter page view (no cookies) | path, referrer, UTM in path query |
| lead_opted_in | Kit subscriber | fields: `source` (guide), `utm_source`, `utm_campaign`, `utm_content`, `first_touch`. Consent is the explicit submit. |
| guide_delivered | Implicit: the guide is the page itself. ManyChat DM delivery is UNVERIFIED. | |
| checkout_started | GoatCounter event `checkout-click/<offer_id>/<page>/<source>` | |
| order_paid | `state/ledger/events.jsonl` | event_id `order_paid:<hash>`, offer_id, gross_cents, fee_cents, currency, ts, utm_* from Gumroad `url_params` (or `unknown`), referrer path only |
| refund_processed | `state/ledger/events.jsonl` | event_id `refund_processed:<hash>`, refund_cents, reason |
| implementation_inquiry | Kit subscriber with `source=pilot` and the `inquiry` field (draft page `/pilot/`) | |

## Joining (best effort, never invented)
- **Site and checkout.** `ap.js` keeps the visit's UTMs in sessionStorage and the first known touch in localStorage (`ap_first`). It appends them to every Gumroad link (plus `ft=<source>:<campaign>`). Gumroad stores the query string on the sale as `url_params`, and the ledger reads them.
- **Opt-in.** `ap.js` adds the same values to every Kit form post as custom fields.
- **No match.** Missing values stay `unknown`. Nothing is inferred across devices, and emails are never matched to orders in the public repo.

## Privacy and data quality
- **Public repo.** The ledger stores no email, name, address, card, IP or license key. Sale ids are salted and hashed. A test fails if an email address ever lands in `state/ledger/`.
- **De-duplication.** Every event has a deterministic `event_id`. Syncing the same sales again adds nothing (test).
- **Time.** UTC internally. Briefs are dated in America/Argentina/Buenos_Aires and say so.

## Known limits
- Instagram and TikTok in-app browsers sometimes drop the referrer and sessionStorage between app and browser.
- Gumroad's sales API may not return `url_params` for every purchase type. Sales without them stay unknown.
- GoatCounter numbers need `GOATCOUNTER_TOKEN`.
- ManyChat has no API in this stack.
