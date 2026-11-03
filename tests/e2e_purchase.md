# End to end purchase test (Master Plan p5, WP03)

Checkout > paid order > delivery > Kit email > ledger > refund. Ground truth is the Gumroad order; everything else must agree with it.

## Run 1: free order (done 2026-11-02, Seb)

| Step | Result | Evidence |
| --- | --- | --- |
| Landing page buy button opens the right product | PASS | Seb's screenshot: Gumroad checkout "Front Desk Kit by AUTOPILOT.OI", US$39 |
| One use code applied | PASS | Code SEBTEST9089 (100% off, 1 use) created by `test_code.yml`, run success 2026-11-02 |
| Receipt and file delivered | PASS | Seb: "It works" with the receipt and PDF |
| Code removed after the test | PASS | `test_code.yml` log: "deleted SEBTEST9089" |
| Order appears in the ledger | NOT TESTABLE | A $0 order is not returned by the Gumroad sales API (ledger 0 events; product sales_count 0 on 2026-11-03 10:43Z) |
| Kit purchase automation fires once | NOT TESTABLE | Kit Gumroad integration not connected (`list_purchases` empty) |
| Meta Purchase event | NOT TESTABLE | No pixel exists on ad account 1615960133613424 |
| Refund shows as refunded, not double counted | NOT TESTABLE | No paid order to refund |

Logic covered offline by `tests/test_purchase_tracking.py` (5 tests, pass): one paid order counts once with its UTM; a repeated poll adds nothing; a refund is recorded once and net goes to minus the fee; $0 and test orders never count as sales; missing UTM stays `unknown`. Buyer email and name never reach the ledger.

## Run 2: small paid order, then refund (NEEDS SEB'S APPROVAL, about $1)

Do this after the Pixel and the Kit Gumroad integration are set up, so one purchase tests everything.

1. I create a one use code that takes the Front Desk Kit to $1 (`test_code.yml`, amount off, 1 use). No list price change.
2. Seb opens `https://autopilotoi.app/front-desk/?utm_source=test&utm_medium=qa&utm_campaign=e2e&utm_content=run2` on his phone, taps Buy, applies the code, pays $1 with his own card.
3. Checks (I run them and save the output here):
   - Gumroad: 1 sale, $1.00, correct product.
   - Ledger: after `gh workflow run revenue.yml`, exactly 1 `order_paid` event for `front_desk_kit` with `utm_campaign=e2e` (or `unknown` if Gumroad does not pass URL params, which is itself a finding).
   - Delivery: receipt email and PDF.
   - Kit: 1 purchase in `list_purchases`; the buyer enters sequence 2954468 once.
   - Meta Events Manager: 1 Purchase, value 1.00 USD, domain gumroad.com / autopilotoi.gumroad.com.
4. Seb refunds it in Gumroad (Sales > the order > Refund). After the next ledger sync: 1 `refund_processed`, orders still 1, net = minus the Gumroad fee, SALES.md shows the refund.
5. I delete the test code and label the order `test` in `sales/activations.csv` notes, and exclude it from acquisition metrics.

Cost: $1 charge, refunded; Gumroad may keep its fee (about $0.60). Rollback: refund in Gumroad; delete the code.
