# Outbound Intelligence V3 (draft only)

A small, reversible module that adds B2B prospect research, scoring, drafting and tracking on top of the existing sales system. It reuses `config/offers.json`, the Gumroad ledger, `sales/outreach.csv`, `revenue.yml` and the daily report. It does not send anything.

## Flow

```
Research (Claude, public business websites only)
  -> private leads CSV in the Claude Project (claude/outbound/leads.csv)
  -> engine.py score      scores, flags, drafts, claim check     -> private scored CSV (Project)
                          writes RESEARCHED / QUALIFIED / DRAFTED  -> sales/outreach.csv (public, pseudonymous)
  -> Seb reviews drafts in the Project doc
  -> engine.py approve <lead_ref> "Seb" "<his words>"            -> APPROVED row
  -> Seb sends 1:1 from his own business email (no bulk tool, no LinkedIn or social DM automation)
  -> engine.py stage <lead_ref> CONTACTED | INTERESTED | CALL_BOOKED | OFFER_SENT | NO_RESPONSE | NOT_FIT | CLOSED_LOST
  -> engine.py optout <website>                                  -> suppressed forever (hash only)
  -> revenue.yml every 3 h: ledger sync -> engine.py reconcile -> PAID only for a real, non test, non refunded
     Gumroad order whose utm_content is the lead_ref -> growth/report_daily.md
```

## Scoring (V3 weights, evidence only)
Niche fit 30 · observable need with URL 25 · authorised contact path 20 (owner relationship or opt in 20, public business contact page 10) · verified commercial fit 15 · research checked within 30 days 10. A missing field scores 0. The score is a research priority, not a prediction.

## Gates that cannot be skipped (all unit tested in `tests/test_outbound.py`)
- No send function and no network access in the module.
- CONTACTED and later stages need an APPROVED row with the approver's name.
- Drafts fail the claim check if they promise automatic sending, 24/7, guaranteed bookings, use a price not in `config/offers.json`, lack the opt out line, or lack the sender's postal address (CAN-SPAM). `config/outbound.json` `postal_address` is empty until Seb provides it.
- One company = one `lead_ref` (sha256 of the domain); duplicates are rejected; the same stage is never logged twice.
- Opt out is final and checked before scoring and drafting.
- A reply is never a sale; PAID comes only from the Gumroad ledger.
- The public repo holds only `lead_ref`s, stages and scores. Names, websites, facts and drafts stay in the private Project.

## Rollback
`git revert` the commits that added `scripts/outbound/`, `tests/test_outbound.py`, `config/outbound.json`, the `pilots` key in `config/offers.json`, the outbound lines in `scripts/revenue/report_daily.py` and the `engine.py reconcile` step in `.github/workflows/revenue.yml`. `sales/outreach.csv` and `sales/suppression.csv` are append only logs; keep the suppression list even after a rollback.
