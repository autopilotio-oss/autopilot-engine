# Outbound Intelligence V3: infrastructure audit and status (2026-11-03)

Labels: **VERIFIED WORKING** (tested end to end today) · **BUILT, TESTED OFFLINE** (unit tests pass, not exercised live) · **PROPOSED** (not built) · **BLOCKED** (needs Seb or an account).

## What V3 needs vs what already existed (no duplicate systems)

| V3 component | Reused existing system | New code | Status |
| --- | --- | --- | --- |
| Scheduler | GitHub Actions `revenue.yml` (every 3 h) | adds `engine.py reconcile` step | BUILT; first live run checked after push (see below) |
| "Creator Demand Engine" | **Not found in the repo** (no code or data by that name). Nearest assets: `research/queue.jsonl` (competitor research), `sales/invites.md` (tester invites) | none | n/a |
| Intake adapter (permitted leads) | Claude research using public business websites; private CSV in the Claude Project `claude/outbound/leads.csv` | `scripts/outbound/engine.py process` | BUILT, TESTED OFFLINE; used on 10 real leads |
| Research audit trail | | required `source_url`, `need_evidence_url`, `fact_source_url`, `checked_at` | BUILT, TESTED |
| Deterministic scoring /100 | | `score()` (V3 weights; missing = 0) | BUILT, TESTED |
| Draft generator + claim checker | `config/offers.json` prices, claims, forbidden phrases | `draft()`, `claim_issues()` | BUILT, TESTED; **BLOCKED for use** until a business postal address is in `config/outbound.json` |
| $299 offer definition | `config/offers.json` | new `pilots` entry (not on sale, delivery hours UNKNOWN) | BUILT; checkout PROPOSED |
| Batch approval queue | the private Project doc `claude/outbound/leads-and-drafts.md` | `engine.py approve` writes APPROVED with the approver | BUILT, TESTED |
| Pipeline / CRM | `sales/outreach.csv` (existing, was empty; columns extended) | stage machine with gates | BUILT, TESTED |
| Opt out suppression | | `sales/suppression.csv` (domain hash) + checks before scoring, drafting and every stage | BUILT, TESTED |
| Sending | none | **no send code by design** | Seb sends 1:1 from his own email after approval |
| Follow ups | | `followups_due()`: 1 follow up max, after 4 days, listed in the daily report | BUILT, TESTED |
| Reply classification | Support agent task already reads Gmail (drafts only) | none yet | PROPOSED: extend that task to log INTERESTED/NOT_FIT/OPTED_OUT for known lead refs |
| Payment reconciliation | Gumroad ledger (`state/ledger`) | `reconcile()`: PAID only for a real, non test, non refunded order with `utm_content=<lead_ref>` | BUILT, TESTED OFFLINE; live attribution UNVERIFIED (Gumroad passing UTMs to the sale is untested until the $1 test order) |
| Reporting | `growth/report_daily.md` | outbound section + follow ups due | BUILT; live after push |
| Kit | Kit sequences | none (no buyer automation yet) | BLOCKED: Gumroad integration in Kit (Seb) |
| Email deliverability (SPF, DKIM, DMARC) | none | none | UNKNOWN: depends on the address Seb sends from; no bulk sending planned |
| Automated research schedule | Claude scheduled tasks | none yet | PROPOSED: a weekly research task (10 new leads, same rules) after the first batch is reviewed |

## Live checks done today
- 10 real businesses researched from their own websites; 2 leads had their key facts re-verified by Claude directly against the business website (details in the private Project doc).
- Engine run on the 10: 6 drafted (all held by the claim check for the missing postal address), 4 no authorised channel. Public log: 22 events, no names, no URLs. Re-running added 0 rows.
- Messages sent: **0**. Spend: **$0**.

## 14 day scorecard (fill as it happens; UNKNOWN stays UNKNOWN)

| Measure | Target | Now |
| --- | --- | --- |
| Leads researched with evidence | 10 | 10 |
| Qualified (score 55+, channel ok) | 5 | 6 |
| Drafts approved by Seb | 5 | 0 |
| Contacted (approved, sent by Seb) | 5 | 0 |
| Replies / qualified replies | record | 0 / 0 |
| Demos or calls | 3 | 0 |
| Offers sent ($299) | record | 0 |
| Paid (ledger verified) | 1 is a good early signal | 0 |
| Activation after purchase | record | 0 |
| Opt outs / complaints | 0 complaints | 0 / 0 |
| Founder minutes per contacted lead | measure | UNKNOWN |
| $299 delivery hours and cost | measure on first 2 | UNKNOWN |
| Contribution after fees, labour, support | positive | UNKNOWN |

Decision on day 14: GO (bigger approved batch of up to 15), HOLD, REWORK the offer, or STOP (any permission problem, complaint, wrong personalisation or opt out failure).
