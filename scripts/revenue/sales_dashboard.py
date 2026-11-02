"""Sales dashboard: verified Gumroad orders joined with spend, outreach and activation logs.
python3 scripts/revenue/sales_dashboard.py  -> state/dashboard/daily.csv + SALES.md
Rules: paid orders only (test and $0 orders excluded); refunds subtracted; unknown sources stay "unknown"; CAC only when spend exists."""
import csv, json, os, datetime as dt
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
COLS = ["date", "channel", "campaign", "visits", "verified_orders", "refunds", "gross_usd", "fees_usd", "ad_spend_usd", "cac_usd",
        "contribution_usd", "email_optins", "activated_customers", "objections"]


def rows(path):
    p = os.path.join(ROOT, path)
    return list(csv.DictReader(open(p))) if os.path.exists(p) else []


def build():
    ev = [json.loads(l) for l in open(os.path.join(ROOT, "state", "ledger", "events.jsonl")) if l.strip()] if os.path.exists(os.path.join(ROOT, "state", "ledger", "events.jsonl")) else []
    paid = {e["order"]: e for e in ev if e["type"] == "order_paid" and not e.get("test") and not e.get("free")}
    refunds = {e["order"]: e for e in ev if e["type"] == "refund_processed" and e["order"] in paid}
    agg = {}
    def cell(d, ch, ca):
        return agg.setdefault((d, ch or "unknown", ca or "unknown"), {c: 0 for c in COLS[3:]} | {"objections": []})
    for o, e in paid.items():
        c = cell(e["ts"][:10], e.get("utm_source"), e.get("utm_campaign"))
        c["verified_orders"] += 1; c["gross_usd"] += e["gross_cents"] / 100; c["fees_usd"] += e["fee_cents"] / 100
        if o in refunds: c["refunds"] += 1; c["gross_usd"] -= refunds[o]["refund_cents"] / 100
    for s in rows("sales/spend.csv"):
        cell(s["date"], s["channel"], s["campaign"])["ad_spend_usd"] += float(s["usd"] or 0)
    for a in rows("sales/activations.csv"):
        if a.get("activated", "").lower() in ("yes", "true", "1"): cell(a["date"], a.get("source"), "activation")["activated_customers"] += 1
    for r in rows("sales/outreach.csv"):
        if r.get("objection"): cell(r["date"], r["channel"], r["campaign"])["objections"].append(r["objection"])
    try:
        site = json.load(open(os.path.join(ROOT, "state", "ledger", "site.json")))
        visits_note = "connected" if "status" not in site else site["status"]
    except Exception: visits_note = "not connected"
    out = []
    for (d, ch, ca), c in sorted(agg.items()):
        spend = c["ad_spend_usd"]; n = c["verified_orders"]
        c["cac_usd"] = round(spend / n, 2) if spend and n else ""
        c["contribution_usd"] = round(c["gross_usd"] - c["fees_usd"] - spend, 2)
        c["visits"] = ""; c["email_optins"] = ""
        out.append({"date": d, "channel": ch, "campaign": ca, **{k: (round(v, 2) if isinstance(v, float) else v) for k, v in c.items() if k != "objections"}, "objections": "; ".join(c["objections"])})
    os.makedirs(os.path.join(ROOT, "state", "dashboard"), exist_ok=True)
    with open(os.path.join(ROOT, "state", "dashboard", "daily.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLS); w.writeheader(); [w.writerow({k: r.get(k, "") for k in COLS}) for r in out]
    tot = lambda k: round(sum(float(r[k] or 0) for r in out), 2)
    orders, spend = int(tot("verified_orders")), tot("ad_spend_usd")
    md = [f"# Sales dashboard", "", f"Updated {dt.datetime.now(dt.timezone.utc).strftime('%Y-%m-%d %H:%M UTC')} from the Gumroad ledger (paid orders only; test and $0 orders excluded) and the logs in `sales/`.", "",
          "| Verified orders | Refunds | Revenue net of refunds | Gumroad fees | Ad spend | CAC | Contribution | Activated customers |", "| --- | --- | --- | --- | --- | --- | --- | --- |",
          f"| {orders} | {int(tot('refunds'))} | ${tot('gross_usd'):.2f} | ${tot('fees_usd'):.2f} | ${spend:.2f} | {('$%.2f' % (spend / orders)) if spend and orders else 'n/a'} | ${tot('contribution_usd'):.2f} | {int(tot('activated_customers'))} |", "",
          f"Visits: {visits_note}. Email opt ins: tracked in Kit (not yet joined here).", ""]
    md += ["| " + " | ".join(COLS) + " |", "|" + " --- |" * len(COLS)] + ["| " + " | ".join(str(r.get(k, "")) for k in COLS) + " |" for r in out] if out else ["No verified orders, spend or activations recorded yet."]
    open(os.path.join(ROOT, "SALES.md"), "w").write("\n".join(md) + "\n")
    return out


if __name__ == "__main__":
    print(len(build()), "rows")
