"""P0-03 Orders, refunds, net receipts, attribution confidence and provider reconciliation (sections 05 and 06).

Input: the Gumroad ledger already pulled every 3h by scripts/revenue/ledger.py (state/ledger/events.jsonl, no PII).
Each ledger event becomes exactly one Growth OS event (source "gumroad", source_event_id = ledger event_id), so a
sale seen 5 times is one order. Money is integer minor units per currency, never mixed.

python3 scripts/growthos/orders.py sync     -> ingest ledger into the event store, print the money view
python3 scripts/growthos/orders.py report   -> money view + reconciliation against Gumroad product sales counts"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from events import Store, ROOT  # noqa: E402

LEDGER = os.path.join(ROOT, "state", "ledger", "events.jsonl")
PRODUCTS = os.path.join(ROOT, "state", "ledger", "products.json")


def known_content_ids():
    ids = set()
    vdir = os.path.join(ROOT, "viral", "concepts")
    if os.path.isdir(vdir):
        ids |= {f[:-5] for f in os.listdir(vdir) if f.endswith(".json")}
    qdir = os.path.join(ROOT, "queue")
    for f in os.listdir(qdir) if os.path.isdir(qdir) else []:
        if f.endswith(".json"):
            try:
                ids |= {p.get("content_id") for p in json.load(open(os.path.join(qdir, f))) if p.get("content_id")}
            except Exception:
                pass
    return ids


def ingest_ledger(store, ledger_events):
    """Map ledger events to Growth OS events. Returns number of new events."""
    n = 0
    for e in ledger_events:
        if e["type"] == "order_paid":
            p = {"order_id": e["order"], "provider": "gumroad", "product_id": e.get("offer_id") or "unknown",
                 "amount_minor": int(e.get("gross_cents", 0)), "currency": e.get("currency", "usd").upper(),
                 "fee_minor": int(e.get("fee_cents", 0)), "test": bool(e.get("test")), "free": bool(e.get("free")),
                 "utm_source": e.get("utm_source"), "utm_campaign": e.get("utm_campaign"), "utm_content": e.get("utm_content")}
            _, created = store.append("order.paid", p, "gumroad", e["event_id"], "ledger", occurred_at=e.get("ts"))
        elif e["type"] == "refund_processed":
            p = {"order_id": e["order"], "provider": "gumroad", "refund_minor": int(e.get("refund_cents", 0)),
                 "currency": e.get("currency", "usd").upper(), "reason": e.get("reason")}
            _, created = store.append("order.refunded", p, "gumroad", e["event_id"], "ledger", occurred_at=e.get("ts"))
        else:
            continue
        n += created
    return n


def attribution(p, content_ids):
    c = p.get("utm_content")
    if c and c in content_ids:
        return "verified", f"utm_content={c}"
    if p.get("utm_source") or c or p.get("utm_campaign"):
        return "partial", "campaign parameters present but not linked to a registered content_id"
    return "unknown", "no campaign link on the order"


def money(store, content_ids=None):
    content_ids = known_content_ids() if content_ids is None else content_ids
    orders, quarantine = {}, []
    for e in store.of("order.paid"):
        p = e["payload"]
        if p["order_id"] in orders:
            quarantine.append({"order_id": p["order_id"], "why": "duplicate provider order id"}); continue
        if p.get("test") or p.get("free"):
            quarantine.append({"order_id": p["order_id"], "why": "test or free order (not revenue)"}); continue
        conf, method = attribution(p, content_ids)
        orders[p["order_id"]] = {**p, "refund_minor": 0, "attribution": conf, "method": method, "at": e["occurred_at_utc"]}
    for e in store.of("order.refunded"):
        p = e["payload"]; o = orders.get(p["order_id"])
        if not o:
            quarantine.append({"order_id": p["order_id"], "why": "refund for unknown order"}); continue
        if p["currency"] != o["currency"]:
            quarantine.append({"order_id": p["order_id"], "why": "refund currency mismatch"}); continue
        o["refund_minor"] = min(o["amount_minor"], o["refund_minor"] + p["refund_minor"])
    by = {}
    for o in orders.values():
        b = by.setdefault(o["currency"], {"orders": 0, "gross_minor": 0, "fees_minor": 0, "refunds_minor": 0,
                                          "attributed": {"verified": 0, "partial": 0, "unknown": 0}})
        b["orders"] += 1; b["gross_minor"] += o["amount_minor"]; b["fees_minor"] += o["fee_minor"]
        b["refunds_minor"] += o["refund_minor"]; b["attributed"][o["attribution"]] += o["amount_minor"] - o["refund_minor"]
    for b in by.values():
        b["net_receipts_minor"] = b["gross_minor"] - b["refunds_minor"] - b["fees_minor"]
    return {"orders": len(orders), "by_currency": by, "quarantined": quarantine,
            "unattributed_orders": sum(1 for o in orders.values() if o["attribution"] == "unknown"),
            "note": "Gross = completed order amounts. Net receipts = gross minus refunds minus provider fees. Contribution needs costs (see costs.py)."}


def reconcile(store, provider_products):
    """Compare our order count per product with Gumroad's own sales_count. Any mismatch is reported, never 'fixed'."""
    ours = {}
    for e in store.of("order.paid"):
        p = e["payload"]
        if not p.get("test"):
            ours[p["product_id"]] = ours.get(p["product_id"], 0) + 1
    from collections import defaultdict
    theirs = defaultdict(int)
    sys.path.insert(0, os.path.join(ROOT, "scripts", "revenue"))
    from ids import offer_id
    for pr in provider_products:
        theirs[offer_id(pr["permalink"])] += int(pr.get("sales_count") or 0)
    keys = set(ours) | set(theirs)
    mism = [{"product": k, "ours": ours.get(k, 0), "provider": theirs.get(k, 0)} for k in sorted(keys) if ours.get(k, 0) != theirs.get(k, 0)]
    return {"checked_products": len(keys), "mismatches": mism, "ok": not mism}


if __name__ == "__main__":
    st = Store()
    if len(sys.argv) > 1 and sys.argv[1] == "sync":
        led = [json.loads(l) for l in open(LEDGER) if l.strip()] if os.path.exists(LEDGER) else []
        print("new events:", ingest_ledger(st, led))
    out = money(st)
    if os.path.exists(PRODUCTS):
        pp = json.load(open(PRODUCTS)); pp = pp if isinstance(pp, list) else pp.get("products", [])
        out["reconciliation"] = reconcile(st, pp)
    print(json.dumps(out, indent=1))
