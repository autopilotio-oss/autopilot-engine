# Runbook

## Secrets and config (GitHub repo secrets, never committed)
| Secret | Used by | Status |
|---|---|---|
| GUMROAD_TOKEN | gumroad.yml, revenue.yml | set. The sales scope is tested by the first `Revenue ledger` run. |
| KIT_PRIVATE_KEY | gumroad.yml (opens sealed kits) | set |
| ELEVENLABS_API_KEY | series, reel, demo and office renders | set |
| GOATCOUNTER_TOKEN | revenue.yml → `state/ledger/site.json` | **missing.** Create it in GoatCounter: Settings → API → New token (read statistics), then add it as a repo secret. |

Kit, Metricool and the scheduled tasks use the Claude connectors (no repo secrets).

## Jobs
| Job | Schedule | What to watch |
|---|---|---|
| `revenue.yml` | every 3h at :53, plus manual | Writes `state/ledger/{events.jsonl,summary.json,products.json,site.json}` and `config/catalog.json`. If `summary.json.sync.sales_api` starts with "error", check the token scope (needs `view_sales`). |
| `ci.yml` | on push to scripts, guides, products or config | 16 tests plus the quality gate. A red run means don't release. |
| `gumroad.yml` | on push to products, plus every 6h | 10 new products a day max. Drafts are skipped. |
| `demo.yml` | on push of an episode | Renders in 5 parallel chunks (about 10 min), then queues the next episode without a video. |
| Revenue chief of staff (Claude) | daily 08:13 ART | Sends the brief. Silence means it failed: check the scheduled task history. |

## Common tasks
- **Release a drafted agent (after Seb says yes):** `python3 scripts/revenue/release.py <slug> --approved-by "Seb, <date>, <channel>"`, then commit and push.
- **Rebuild the catalog and the funnel map:** `python3 scripts/revenue/catalog.py && python3 scripts/revenue/flows.py`
- **Make a tracked link:** `python3 -c "import sys;sys.path.insert(0,'scripts/revenue');import ids;print(ids.utm_url('https://autopilotoi.app/g/subs/','threads','subscription_leak_2026w45','th_text_subs_004'))"`
- **Run the tests:** `python3 -m pytest -q tests/`

## Failure modes
| Symptom | Likely cause | Fix |
|---|---|---|
| Buy button shows "Coming soon" | The permalink is not published on Gumroad (`live.json`) | Publish it on Gumroad, or wait for the sync. This is a fail-safe by design. |
| Ledger shows 0 orders but Gumroad shows sales | Token lacks sales scope, or the API errored | Check `summary.json.sync` and re-run `revenue.yml` |
| Duplicate Threads post | Both `post.yml` and the Metricool loader picked up a queue item | Check `state/posted.json`. Long term, keep only one Threads path (recommend Metricool). |
| Kit lead in no sequence | The Kit sync task failed, or `source` is empty | It now runs every 3h. Check the scheduled task history. |
| Demo video stuck | A render chunk failed | Re-run `demo.yml` with input `ep=<slug>` |

## Rollback
- **Site** (`ap.js`, guides, pilot page). These are only on the `feat/revenue-engine-v2` branch until approved. After a merge, run `git revert <merge sha>` and push. Pages redeploys the previous files in about 1 min. Smoke test: open /g/subs/ and /store/ and check the buy links include `utm_source`.
- **Back office** (scripts, tests, workflows, docs). Delete or disable `revenue.yml` in the Actions tab. Nothing else depends on it.
- **Scheduled tasks.** The previous prompts are recorded in `revenue-engine-v2/RELEASE_REPORT.md`. Restore them with the update tool.
- **Deposit Agent.** It's a draft. Release it with `release.py`, or delete `products/deposit-agent` to drop it.

## Cost controls
- Claude scheduled runs are about 15 a day after this release (was about 30).
- ElevenLabs: about 450 characters per demo, about 900 per Day episode. The credit balance isn't visible to us. If renders fail at the voice step, the brief reports it.
- GitHub Actions are free (public repo). Metricool, Kit and Gumroad plans are unchanged. No new paid subscriptions.
