# Content system: research, tests, approvals

## 1. Research queue (`research/queue.jsonl`)
**Sources:** Metricool Competitors (Instagram and Threads give interactions, not views). Once the accounts in `research/registry.json` are added in Metricool, the scout pulls them through the API. Public pages read by hand are also allowed, with provenance. No scraping, no logins.

**Each record holds:**
- account and post URL
- capture date and post date
- topic, format, hook type and CTA
- metric and post value
- creator median, with its sample size and window
- provenance
- 4 judgment scores (0 to 5)
- the offer it would feed
- **our own angle** (never their words)

**Outlier:** post value divided by the creator's median over the last 10 to 20 comparable posts. With fewer than 5 posts the record is `unbenchmarked` and never gets a score.

**Score** (`python3 scripts/revenue/research.py rank`):
`0.35 outlier (log normalised) + 0.25 audience fit + 0.20 offer relevance + 0.10 evidence + 0.10 ease`.
The weights are test assumptions, not facts.

**Output:** a weekly top 10 brief in the Chief of Staff message on Mondays, and hooks that work go to LEARNINGS.md under "Winning hooks".

## 2. Experiments (`experiments/experiments.jsonl`, `scripts/revenue/experiments.py`)
- **One objective per item:** reach, guide_visit, optin, quiz_complete, purchase or inquiry. No objective means it stays a draft.
- **One variable per test:** hook, opening, cta, landing_headline, cover, post_time or format. Same offer and same route in both variants.
- **Predeclared before posting:** `min_sample` and `review_date`. Declaring a winner below `min_sample` fails validation.
- **No false A/B claims:** Trial Reels are used where Metricool supports them. Otherwise two ordinary posts, with the exposure difference written down as a limitation.
- **Commercial score:** attributed net revenue per 1,000 qualified views, or per 100 landing visits. Secondary: CTR, opt-in rate, checkout clicks, saves and shares.
- **First month mix (hypothesis):** 60% proven education, 25% new hooks and angles, 15% product demos (the robot demo videos). Reviewed weekly.

## 3. Approval criteria (QA gate before anything is queued)
1. One useful lesson a stranger would save. One CTA, from the catalog.
2. Facts about money, law, health or platforms have a source and a review date. Legal, medical and credit specifics get an extra accuracy pass and are not auto-published.
3. Voice rules: no dashes, no hype, no income or outcome promises, no fake scarcity or testimonials. Product wording: a "Claude prompt kit you run".
4. Brand: black and lime, condensed headlines, robot mascot, faceless.
5. Canonical `content_id`, plus UTM links where a link is possible.
6. State tracked: draft, approved, published, failed, measured.

**Who approves:** new formats, offers and products need Seb. Existing formats follow the content upgrade task's rules. Agent Factory products always need Seb.
