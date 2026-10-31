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
    sys.path.insert(0, os.path.join(ROOT, "scripts", "growthos"))
    import commander, costs, adapters
    from events import Store
    st = Store(); cmd = commander.run(st)
    dec = [d if isinstance(d, str) else (d.get("decision") or d.get("title") or json.dumps(d)) for d in (social.get("decisions") or [])]
    dec += [f"{p['title']}: {p['action']}" for p in cmd["top3"] if p["needs_owner"]]
    seen = []
    [seen.append(d) for d in dec if d not in seen]
    json.dump({"rows": [{"n": i + 1, "decision": d} for i, d in enumerate(seen[:3])]}, open(f"{OUT}/decisions.json", "w"), indent=1)
    # Growth OS operations: health checks, controls, integrations
    hs = {}
    try:
        hs = json.load(open(os.path.join(ROOT, "state", "health", "status.json")))
    except Exception:
        pass
    json.dump({"rows": [{"check": k, "status": "ok" if v["ok"] else "FAILING", "severity": v["severity"]} for k, v in sorted(hs.items())]},
              open(f"{OUT}/ops_health.json", "w"), indent=1)
    flags = json.load(open(os.path.join(ROOT, "config", "growthos", "flags.json")))
    g = costs.guard(st); vp = json.load(open(os.path.join(ROOT, "viral", "policy.json")))
    rows = [{"item": "Publishing", "value": "ON" if flags["outbound_publishing"] else "STOPPED", "note": "kill switch"},
            {"item": "Messaging (email, DMs)", "value": "ON" if flags["messaging"] else "STOPPED", "note": "kill switch"},
            {"item": "Paid services", "value": "ON" if flags["paid_services"] else "PAUSED", "note": "kill switch"},
            {"item": "AI spend caps", "value": g["status"], "note": f"spent today ${g['spent_today_minor'] / 100:.2f} recorded"},
            {"item": "NO PROOF, NO POST", "value": "ENFORCED" if vp.get("active") else "REPORT ONLY", "note": "publishers cut over only with your OK"},
            {"item": "Bottleneck today", "value": cmd["bottleneck"], "note": "Growth Commander"}]
    rows += [{"item": f"Integration: {k}", "value": v["status"], "note": v["how"][:90]} for k, v in adapters.matrix().items()]
    json.dump({"rows": rows}, open(f"{OUT}/ops_controls.json", "w"), indent=1)
    print("dashboard files in", OUT, datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"))


if __name__ == "__main__":
    main()
