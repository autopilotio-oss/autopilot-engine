"""Files for the private Revenue Dashboard (a Claude Dashboard artifact). The Chief of Staff uploads them daily.
python3 scripts/revenue/dashboard_data.py [state/social/<date>.json]  -> /tmp/dash/{revenue,offers,decisions}.json"""
import json, os, sys, datetime
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = "/tmp/dash"


def main():
    os.makedirs(OUT, exist_ok=True)
    s = json.load(open(os.path.join(ROOT, "state", "ledger", "summary.json")))
    rows = []
    for label, key in (("Last 1 day", "last_1d"), ("Last 7 days", "last_7d"), ("Last 30 days", "last_30d")):
        w = s.get(key) or {"orders": 0, "by_currency": {}}
        usd = w["by_currency"].get("usd", {"gross_cents": 0, "fee_cents": 0, "refund_cents": 0, "net_cents": 0})
        rows.append({"window": label, "orders": w["orders"], "gross_usd": usd["gross_cents"] / 100, "fees_usd": usd["fee_cents"] / 100,
                     "refunds_usd": usd["refund_cents"] / 100, "net_usd": usd["net_cents"] / 100,
                     "other_currencies": ", ".join(c for c in w["by_currency"] if c != "usd") or "none"})
    rows.append({"window": "All time", "orders": s["verified_orders_all_time"], "gross_usd": None, "fees_usd": None, "refunds_usd": None, "net_usd": None,
                 "other_currencies": "see ledger"})
    json.dump({"rows": rows, "as_of": s.get("generated"), "sales_api": s.get("sync", {}).get("sales_api")}, open(f"{OUT}/revenue.json", "w"), indent=1)
    cat = json.load(open(os.path.join(ROOT, "config", "catalog.json")))
    offers = [{"offer": o["name"], "offer_id": o["offer_id"], "price_usd": (o["price_cents"] or 0) / 100, "status": o["status"],
               "kind": o["kind"], "orders": (s.get("by_offer", {}).get(o["offer_id"], {}) or {}).get("orders", 0)}
              for o in cat["offers"] if o["status"] != "retired"]
    json.dump({"rows": offers}, open(f"{OUT}/offers.json", "w"), indent=1)
    social = json.load(open(sys.argv[1])) if len(sys.argv) > 1 else {}
    dec = [{"n": i + 1, "decision": d} for i, d in enumerate((social.get("decisions") or [])[:3])]
    json.dump({"rows": dec}, open(f"{OUT}/decisions.json", "w"), indent=1)
    print("dashboard files in", OUT, datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"))


if __name__ == "__main__":
    main()
