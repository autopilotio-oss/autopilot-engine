# Sales logs (manual inputs to the dashboard)

No personal data in this public repo: use a short reference (e.g. `cleaner-NJ-01`), never names, emails or phone numbers.

| File | One row per | Who fills it |
| --- | --- | --- |
| `spend.csv` | Ad or tool spend that buys traffic (USD) | Claude, from Ads Manager, only spend Seb approved |
| `outreach.csv` | Invitation to an owner or partner (status: drafted, approved, sent, replied, demo, bought, declined) | Claude drafts, Seb approves and sends |
| `activations.csv` | Buyer or tester who reached (or failed to reach) a first useful draft | From buyer replies and usability tests |

`scripts/revenue/sales_dashboard.py` joins these with the Gumroad ledger (paid orders only; test and free orders excluded) into `SALES.md` and `state/dashboard/daily.csv`. Unknown sources stay `unknown`.
