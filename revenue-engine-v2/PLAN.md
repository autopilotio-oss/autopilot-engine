# Plan (ranked by expected revenue learning divided by cost and risk)

| # | Task | Expected measurable benefit | Depends on | Owner | Status |
|---|---|---|---|---|---|
| 1 | Make THE WORKSPACE ($49) purchasable again on Gumroad (`ttdat`) | Unblocks the only business offer: BRAIN, AGENT and WORKSPACE CTAs, plus 2 email sequences | Seb (publish or restore on Gumroad) | Seb | BLOCKED (approval) |
| 2 | Order ledger: Gumroad orders, refunds and products, PII-free, every 3h | First trustworthy revenue numbers, plus confirmation of point 1 | Merge back office to main | Claude | DONE (runs after merge) |
| 3 | Attribution in `ap.js`: keep inbound UTMs, first touch, Kit UTM fields | Join content → lead → order | Seb approves the site deploy | Claude | DONE on branch, tested in a browser |
| 4 | Daily Chief of Staff brief with verified numbers and 1 to 3 decisions | One honest daily view, and fewer messages | 2 | Claude | DONE (scheduled task) |
| 5 | Agent Factory: draft only, plus quality gate and release script | No unreviewed SKUs. Focus on selling the 9 kits. | — | Claude | DONE |
| 6 | Cut the Kit sync from hourly to every 3h | About 16 fewer Claude runs a day | — | Claude | DONE |
| 7 | GoatCounter API token as a repo secret | Landing visits and checkout clicks per source | Seb, 1 min | Seb | BLOCKED (credential) |
| 8 | Add 8 to 10 analogous accounts to Metricool Competitors | Benchmarked outliers instead of "unbenchmarked" | Seb (Metricool UI) | Seb | BLOCKED (access) |
| 9 | Two controlled content tests (`subs_hook_001`, `deposit_cta_001`) | First hook and CTA evidence | Seb approves captions; 7 for measuring | Claude | READY (draft) |
| 10 | ManyChat reply links with UTMs, plus DEPOSIT keyword | Attributable DM traffic | Seb (ManyChat UI) | Seb | BLOCKED (access) |
| 11 | Purchaser suppression in Kit (Gumroad → Kit) | Stop offering a kit to people who already bought it | Gumroad Kit integration or a webhook receiver | Seb / Claude | BLOCKED |
| 12 | Premium pilot (tier 1) page and delivery checklist | First high-ticket learning | Funnel proven, plus Seb's terms | Seb | DRAFT (`/pilot/` on branch) |
| 13 | Keep only one Threads publishing path (Metricool) | Removes the duplicate post risk | Seb OK | Claude | PROPOSED |

## 30 day roadmap (blueprint, adapted)
| Week | Focus | Status |
|---|---|---|
| 1 | Baseline plus instrumentation (this release). Exit gate: checkout and old automations still work, events are observable. | Tests pass. Production site untouched until approval. |
| 2 | Research and creative. The scout fills `research/queue.jsonl`, 10 sourced candidates. Run tests 9 and 10. | |
| 3 | Lead conversion. ManyChat UTMs, purchaser suppression, 3 end-to-end funnels green (Workspace fixed). | |
| 4 | Revenue dashboard plus pilot decision. Weekly SKU funnel report. Pilot launch only on approval. | |
