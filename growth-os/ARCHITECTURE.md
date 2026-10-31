# Growth OS 3.0 architecture (as built, Oct 31 2026)

Minimum diff on the existing stack: Python scripts + GitHub Actions + Claude scheduled tasks + git as the durable
store (append only JSONL, hash chained). No new vendor, no database bill. Why no Postgres: zero orders and zero
subscribers today; a managed DB would add cost and a secret with nothing to store yet. The event schema is ready to
move into Postgres later without changing callers (Store is one class).

```
             CONTROL PLANE (deterministic code)                         EXECUTION PLANE (existing workers)
  ┌──────────────────────────────────────────────────┐        ┌──────────────────────────────────────────────┐
  │ policy.py   action registry, risk tiers, scoped   │◀──ask──│ Claude scheduled tasks (trend scout, loader,  │
  │             approvals, kill switches              │        │ day series, reel maker, newsletter, factory)  │
  │ viral/gate.py  NO PROOF, NO POST state machine    │        │ GitHub Actions (gumroad, revenue, renders)     │
  │ jobs.py     durable queue, retries, dead letter    │──run──▶│ adapters.py (Gumroad, Metricool, Kit: LIVE;   │
  │ costs.py    budget guard (caps set by owner)      │        │   ManyChat, GoatCounter, inbox: LIVE_BLOCKED) │
  │ health.py   hourly probes, incidents, alerts      │        └──────────────────────────────────────────────┘
  │ commander.py  daily bottleneck + proposals        │                         │ facts
  └──────────────────────────────────────────────────┘                         ▼
             LEARNING PLANE                                     ┌──────────────────────────────────────────────┐
  orders.py (money, attribution confidence, reconcile)  ◀──────│ events.py  state/events/events.jsonl          │
  consent.py (Kit consent, suppression)                         │ unique(source, source_event_id), hash chain,  │
  experiments.py, research.py (Revenue Engine 2.0)              │ schema checked, no PII                        │
  dashboard_data.py -> private dashboard artifact               └──────────────────────────────────────────────┘
```

## Stores
| Store | Where | Holds | PII |
|---|---|---|---|
| Event store | state/events/events.jsonl (public repo) | orders (hashed ids), refunds, incidents, approvals, flags, jobs failures, spend | none (emails rejected by schema) |
| Gumroad ledger | state/ledger/ (public repo) | raw normalized sales, salted order hashes | none |
| Viral register | viral/ (public repo) | references, concepts, hash chained audit | none |
| Job queue | state/jobs/ | job transitions, effect keys | none |
| Consent | Kit (system of record) + contact_ref events | consent scope, source, unsubscribe | Kit only |
| Support cases | private dashboard artifact DB (planned) | redacted case text | redacted |

## Approval flow
Owner words in chat or on the Approval Queue page -> `gate.py approve` (content) or `policy.py grant` (any high or
critical action). A grant is scoped to one action + resource + version hash + destination, expires within 72h,
and is used once. Editing the content changes the hash and voids it.

## Ticket map
| Ticket | Code | Status |
|---|---|---|
| P0-01 inventory | growth-os/INVENTORY.md | done |
| P0-02 event store | scripts/growthos/events.py | done, live in Actions |
| P0-03 Gumroad reconciliation | scripts/growthos/orders.py + revenue.yml | done, live (0 orders) |
| P0-04 consent | scripts/growthos/consent.py | done; ingest runs in the daily brief |
| P0-05 dashboard | private dashboard (ops sections) | done |
| P0-06 durable queue | scripts/growthos/jobs.py | done (library; workers adopt it gradually) |
| P0-07 policy and action registry | scripts/growthos/policy.py, config/growthos/policy.json | done |
| P0-08 viral gate on all publishers | scripts/viral/gate.py, scripts/growthos/publish.py | ACTIVE since 2026-10-31 (owner instruction); one Publisher worker, others draft only |
| P0-09 approval UX | Approval Queue page + chat approvals (publish.py approve) | built; page goes up with the first concept |
| P0-10 guide to delivery test | tests/test_growthos.py::test_P0_10 (synthetic) | synthetic PASS; live purchase test needs approval (spends $10) |
| P1-11 support | scripts/growthos/support.py, support_kb.json | triage done; inbound channel LIVE_BLOCKED |
| P1-12 health, alerts, kill switches | health.py, health.yml, flags.json | live hourly |
| P1-13 unit economics, caps | costs.py, budget.json | built; caps need owner numbers |
| P1-14 experiments | scripts/revenue/experiments.py (Revenue Engine 2.0) | exists; 2 drafts |
| P1-15 cutover, rollback, manual | RUNBOOKS.md, RELEASE.md, cutover.json | done |

## Continuous Improvement pack (6 PDFs)
Daily Pulse, Weekly Sprint, Monthly Review, Viral Content Lab and Reliability are scheduled workers; see growth-os/AUTONOMY.md. Shared state lives in growth-os/operations/ (decision log, experiment ledger, weekly priorities, next actions, run history).
