# Daily report

Generated 2026-11-03 13:57 UTC by `scripts/revenue/report_daily.py`. Ledger synced 2026-11-03T13:57:11Z.
Financial truth is the Gumroad ledger. Test and $0 orders are excluded. Unknown attribution stays unknown.

| Metric | Value | Source |
| --- | --- | --- |
| Verified orders (24 h / all time) | 0 / 0 | Gumroad sales API |
| Gross revenue | $0.00 | sum of paid orders |
| Refunds | 0 ($0.00) | Gumroad refund state |
| Net receipts | $0.00 | gross minus Gumroad fees minus refunds |
| Ad spend (all time) | $49.89 | sales/spend.csv (ad platform) |
| CAC / CPA | n/a (0 paid ad orders) | spend / orders with paid UTMs |
| Contribution | $-49.89 | net receipts minus ad spend (support and commissions not yet tracked) |
| Landing conversion | 0 orders / sessions MISSING (GoatCounter token not set) | ledger + GoatCounter |
| Activation | 0/0 buyers | sales/activations.csv |
| Attribution quality | 0/0 orders with a source | ledger UTMs |
| System health | failing: meta_pixel_configured | state/health/status.json |

## Gates (Master Plan p17)
- G0 technically sellable: NOT PASSED (needs a paid test order through ledger, Kit and pixel; see tests/e2e_purchase.md)
- G1 product activated: 0/3 outside users reached a useful draft
- G2 demand exists: 0/3 paying buyers
- G3 to G5: not started (no paid acquisition until G0 passes and Seb approves a cap)

Escalations go to Seb only for: broken checkout, overspend, duplicate fulfilment, a message to an unsubscribed person.
