"""Master plan p5 acceptance tests that can run without spending money (WP03/WP04).
The live versions (a real paid order, then a refund) need Seb's approval and are tracked in tests/e2e_purchase.md."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts", "revenue"))
import ledger

SALE = {"id": "S-TEST-1", "product_permalink": "autopilot", "price": 3900, "gumroad_fee": 520, "currency": "usd",
        "created_at": "2026-11-03T12:00:00Z", "email": "buyer@example.com", "full_name": "Buyer Name",
        "url_params": "utm_source=instagram&utm_medium=social&utm_campaign=front_desk&utm_content=fd_cards_1102"}


def test_paid_order_counts_once_with_attribution():
    evs, added = ledger.merge([], ledger.to_events(SALE))
    s = ledger.summarize(evs)
    assert added == 1 and s["verified_orders_all_time"] == 1
    e = evs[0]
    assert e["utm_source"] == "instagram" and e["utm_content"] == "fd_cards_1102"
    assert "buyer@example.com" not in str(evs) and "Buyer Name" not in str(evs)


def test_poll_retry_never_double_counts():
    evs, _ = ledger.merge([], ledger.to_events(SALE))
    evs, added = ledger.merge(evs, ledger.to_events(SALE))      # same sale seen on the next 3 h poll
    assert added == 0 and ledger.summarize(evs)["verified_orders_all_time"] == 1


def test_refund_after_order_is_one_refund_and_net_zero():
    evs, _ = ledger.merge([], ledger.to_events(SALE))
    refunded = dict(SALE, refunded=True, refunded_at="2026-11-04T12:00:00Z")
    evs, added = ledger.merge(evs, ledger.to_events(refunded))
    evs, again = ledger.merge(evs, ledger.to_events(refunded))  # retry
    s = ledger.summarize(evs)
    assert added == 1 and again == 0
    assert s["refunds_all_time"] == 1 and s["verified_orders_all_time"] == 1
    w = ledger.summarize(evs, today=__import__("datetime").date(2026, 11, 4))["last_30d"]
    assert w["by_currency"]["usd"]["net_cents"] == 3900 - 520 - 3900   # ledger is conservative: the fee is treated as not returned


def test_test_and_free_orders_are_not_sales():
    free = dict(SALE, id="S-FREE", price=0, gumroad_fee=0)      # e.g. a 100% off code like SEBTEST9089
    test = dict(SALE, id="S-T", test=True)
    evs, _ = ledger.merge([], ledger.to_events(free) + ledger.to_events(test))
    assert ledger.summarize(evs)["verified_orders_all_time"] == 0


def test_missing_attribution_stays_unknown():
    evs = ledger.to_events(dict(SALE, id="S-NOUTM", url_params=""))
    assert evs[0]["utm_source"] == "unknown" and evs[0]["utm_campaign"] == "unknown"
