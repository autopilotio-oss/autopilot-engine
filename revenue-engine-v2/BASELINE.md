# Revenue Engine 2.0: verified baseline (audited 2026-10-31, 14:30 to 15:30 America/Argentina/Buenos_Aires)

Every row was checked against the repo, the connected APIs or a live test during this audit.
- **VERIFIED**: checked.
- **UNVERIFIED**: no access, or no data yet.
- **BROKEN**: checked and not working.
- **RETIRED**: deliberately turned off.

## Numbers (as of the audit)
| Metric | Value | Source | Status |
|---|---|---|---|
| Verified paid orders | Not yet pulled. The ledger sync runs for the first time with this release. | Gumroad API via `state/ledger/summary.json` | UNVERIFIED until the first `Revenue ledger` run |
| Email subscribers | 0 (0 new in October) | Kit `get_growth_stats` | VERIFIED |
| Instagram followers | 34 (Oct 30) | Metricool IGEV01 | VERIFIED |
| Instagram, Oct 30 | 3 posts, 5 interactions, 34 accounts engaged, 10 reel views | Metricool | VERIFIED. Metricool also reports reach 12,500 / views 9,769 for that day, which is inconsistent with 10 reel views, so treat account level reach as unreliable. |
| Threads followers | 0. Oct 30: 3 posts, 9 views | Metricool THEV | VERIFIED |
| Website visits | Unknown | GoatCounter. The script is installed on every page, but there is no API token. | UNVERIFIED |
| ManyChat keyword replies | Unknown | No ManyChat API access. Seb reported setting up the keywords by hand. | UNVERIFIED |

**What this means.** The last reported baseline ("a handful of followers, no sales") still holds. The work right now is distribution and conversion, not more products.

## System inventory
| Area | What exists | Status |
|---|---|---|
| Site | Static HTML on GitHub Pages (`docs/`, custom domain autopilotoi.app). Built by hand plus `tools/guides/build.py` (guides and sitemap). No framework and no package manager. | VERIFIED |
| Deploy | Every push to `main` deploys via `pages-build-deployment`. There is no preview environment. A branch plus a local server is the preview. | VERIFIED |
| Free guides | 9 public: credit, bill, debt, subs, refund, raise, video, shop, sell. Plus deposit as a noindex draft. | VERIFIED. Sitemap test passes. |
| Money Leak Check quiz | `/quiz/` redirects to `/free/` | RETIRED (Seb rejected it Oct 31) |
| AI Front Desk | `/brain/` questionnaire | VERIFIED (page exists, keyword routes there) |
| Agent kits on Gumroad | 8 live: subs, bill, debt, refund, raise, shop, sell agents and the all-money-agents bundle ($39) | VERIFIED (`docs/live.json`) |
| Video Agent, TikTok bundle ($24) | Built in `products/`. Not created on Gumroad because the 10 new products per day limit was hit. | BROKEN for today, fixes itself on the next sync |
| THE WORKSPACE ($49, gumroad `ttdat`) | Linked 3 times from `/workspace/`, but not in Gumroad's published product list. All 3 buy buttons render "Coming soon" (tested in a browser). | **BROKEN. This is the only business offer, and BRAIN, AGENT and WORKSPACE all lead to it.** |
| Deposit Agent | Built today. Now a draft that needs approval. | DRAFT |
| Credit Agent, Lower Bills Agent, old Money bundle | Retired | RETIRED |
| Checkout analytics | `ap.js` adds UTMs to Gumroad links and sends GoatCounter events (checkout-click, optin, quiz-complete). It overwrote the inbound `utm_content`. | Partly working. Fixed on the branch. |
| Lead capture | One Kit form (10118407) on every page, with custom field `source` set to the guide slug. No UTM fields. | Partly working. UTM fields added on the branch, and Kit fields were created. |
| Email | 3 Kit sequences (3, 3 and 5 emails). Routed by the "Kit welcome sync" scheduled task, which runs every hour. | VERIFIED configured, never exercised (0 subscribers) |
| Consent | Opt-in is an explicit email submit ("Send me tips"). Kit handles unsubscribes. Double opt-in setting is unknown. | Partly verified |
| Publishing | Metricool (IG, Threads, TikTok, X connected). `post.yml` also posts the queue to Threads every 15 min via the Threads API. | VERIFIED. Two paths to Threads is a duplicate risk, de-duplicated only by `state/posted.json`. |
| Video | ElevenLabs (secret in Actions) plus Playwright/three.js renderers: series, reels, demo, office. | VERIFIED (3 renders succeeded today). Credit balance UNVERIFIED. |
| Gumroad sync | `gumroad.yml` on push and every 6h. Creates and updates products and writes `live.json`. | VERIFIED |
| Orders and refunds | Nothing recorded them before this release | BROKEN. Added `scripts/revenue/ledger.py`. |
| Tests | None before this release | Added 16 tests |
| Secrets | GitHub secrets: GUMROAD_TOKEN, KIT_PRIVATE_KEY, ELEVENLABS_API_KEY, plus Threads/IG tokens encrypted in `state/token.enc`. None in tracked files (test). | VERIFIED |
| Repo visibility | **Public.** Anything in `state/` can be read by anyone. | VERIFIED. This is why the ledger stores no personal data. |

## Scheduled jobs (as found)
**Claude scheduled tasks** (about 30 runs a day):

| Job | When | Notes |
|---|---|---|
| Kit welcome sync | hourly (24 a day) | Biggest cost line and over-frequent at 0 subscribers |
| Daily content upgrade | 03:47 ART | |
| Agent drop | 06:43 ART | Changed to fully automatic at 13:40 today |
| Morning trend scout | 08:41 ART | |
| IG + Threads loader | 09:23 ART | |
| Day series writer | 15:37 ART | |
| Voiced reels | Mon and Thu | |
| Newsletter | Sun | |
| TikTok Shop intel | Wed | |

**GitHub Actions** (free on a public repo):
- `post.yml` every 15 min
- `daily.yml` hourly (stats and comment replies)
- `gumroad.yml` every 6h
- `market.yml` daily
- plus render workflows triggered on push

## Ranked blockers (expected revenue impact divided by effort)
1. **The Workspace ($49) cannot be bought.** Every business owner CTA ends at "Coming soon". Needs Seb to publish or restore the Gumroad product. Approval item.
2. **0 subscribers and about 40 people reached.** Distribution is the constraint, not the catalog. Daily new SKUs are the wrong lever right now (the blueprint agrees).
3. **No order ledger and no web analytics access.** We can't see if anything converts. The ledger is added. GoatCounter needs a token.
4. **Attribution was lossy.** `utm_content` was overwritten and leads had no source fields. Fixed on the branch.
5. **ManyChat is a black box.** No API, so keyword to DM delivery can't be tested automatically.
6. **Cost.** The hourly Kit sync spends about 24 Claude runs a day routing 0 subscribers.
