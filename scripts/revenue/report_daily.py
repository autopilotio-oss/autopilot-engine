"""Daily revenue and growth report (Master Plan p13, tactic 10): growth/report_daily.md.

Financial truth = Gumroad ledger (state/ledger). Spend = sales/spend.csv (from the ad platform). Sessions come from
GoatCounter only when connected; otherwise they are MISSING, never 0. Small numbers are shown as numerator/denominator.
python3 scripts/revenue/report_daily.py"""
import csv, datetime, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def _json(p, default=None):
    try:
        return json.load(open(os.path.join(ROOT, p)))
    except Exception:
        return default


def _csv(p):
    try:
        return list(csv.DictReader(open(os.path.join(ROOT, p))))
    except Exception:
        return []


def money(c):
    return f"${c / 100:,.2f}" if c is not None else "MISSING"


def build(now=None):
    now = now or datetime.datetime.now(datetime.timezone.utc)
    led = _json("state/ledger/summary.json", {}) or {}
    events = []
    try:
        events = [json.loads(l) for l in open(os.path.join(ROOT, "state/ledger/events.jsonl")) if l.strip()]
    except Exception:
        pass
    paid = [e for e in events if e["type"] == "order_paid" and not e.get("test") and not e.get("free")]
    refunds = {e["order"]: e for e in events if e["type"] == "refund_processed"}
    gross = sum(e["gross_cents"] for e in paid); fees = sum(e["fee_cents"] for e in paid)
    ref = sum(r["refund_cents"] for o, r in refunds.items() if any(p["order"] == o for p in paid))
    net = gross - fees - ref
    spend = sum(round(float(r["usd"]) * 100) for r in _csv("sales/spend.csv") if r.get("usd"))
    attributed = [e for e in paid if e.get("utm_source", "unknown") != "unknown"]
    paid_ads_orders = [e for e in paid if e.get("utm_medium") in ("paid_social", "cpc", "paid")]
    acts = _csv("sales/activations.csv")
    activated = sum(1 for a in acts if str(a.get("activated", "")).lower() in ("1", "true", "yes"))
    health = _json("state/health/status.json", {}) or {}
    failing = sorted(k for k, v in health.items() if isinstance(v, dict) and v.get("ok") is False)
    site = _json("state/ledger/site.json", {}) or {}
    sessions = site.get("sessions_7d") if isinstance(site, dict) else None
    day = lambda e: str(e.get("ts", ""))[:10]
    today = now.date().isoformat(); y = (now.date() - datetime.timedelta(days=1)).isoformat()
    last24 = [e for e in paid if day(e) in (today, y)]
    cpa = f"{money(spend // len(paid_ads_orders))}" if paid_ads_orders else "n/a (0 paid ad orders)"
    conv = f"{len(paid)}/{sessions} sessions" if sessions else f"{len(paid)} orders / sessions MISSING (GoatCounter token not set)"
    lines = [
        "# Daily report", "",
        f"Generated {now.strftime('%Y-%m-%d %H:%M')} UTC by `scripts/revenue/report_daily.py`. Ledger synced {led.get('sync', {}).get('ran', 'MISSING')}.",
        "Financial truth is the Gumroad ledger. Test and $0 orders are excluded. Unknown attribution stays unknown.", "",
        "| Metric | Value | Source |", "| --- | --- | --- |",
        f"| Verified orders (24 h / all time) | {len(last24)} / {len(paid)} | Gumroad sales API |",
        f"| Gross revenue | {money(gross)} | sum of paid orders |",
        f"| Refunds | {len(refunds)} ({money(ref)}) | Gumroad refund state |",
        f"| Net receipts | {money(net)} | gross minus Gumroad fees minus refunds |",
        f"| Ad spend (all time) | {money(spend)} | sales/spend.csv (ad platform) |",
        f"| CAC / CPA | {cpa} | spend / orders with paid UTMs |",
        f"| Contribution | {money(net - spend)} | net receipts minus ad spend (support and commissions not yet tracked) |",
        f"| Landing conversion | {conv} | ledger + GoatCounter |",
        f"| Activation | {activated}/{len(paid)} buyers | sales/activations.csv |",
        f"| Attribution quality | {len(attributed)}/{len(paid)} orders with a source | ledger UTMs |",
        f"| System health | {'all checks passing' if not failing else 'failing: ' + ', '.join(failing)} | state/health/status.json |",
        "", "## Gates (Master Plan p17)",
        f"- G0 technically sellable: {'NOT PASSED' if 'meta_pixel_configured' in failing or not paid else 'check'} (needs a paid test order through ledger, Kit and pixel; see tests/e2e_purchase.md)",
        f"- G1 product activated: {activated}/3 outside users reached a useful draft",
        f"- G2 demand exists: {len(paid)}/3 paying buyers",
        "- G3 to G5: not started (no paid acquisition until G0 passes and Seb approves a cap)",
        "", "Escalations go to Seb only for: broken checkout, overspend, duplicate fulfilment, a message to an unsubscribed person.",
    ]
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    os.makedirs(os.path.join(ROOT, "growth"), exist_ok=True)
    out = build()
    open(os.path.join(ROOT, "growth", "report_daily.md"), "w").write(out)
    print(out)
