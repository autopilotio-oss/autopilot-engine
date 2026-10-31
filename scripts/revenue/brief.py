"""Daily Revenue Chief of Staff brief.

python3 scripts/revenue/brief.py [--social state/social/<date>.json] [--ops ops.json] [--date YYYY-MM-DD]
-> prints the brief (markdown) and writes state/briefs/<date>.json

Inputs (all optional, missing ones are reported as gaps, never guessed):
  state/ledger/summary.json   verified Gumroad orders and refunds (ledger.py)
  config/catalog.json         offers and their live status (catalog.py)
  --social                    snapshot the Chief of Staff session pulls from Metricool + Kit (+ GoatCounter when a token exists)
  --ops                       failed GitHub runs / scheduled task problems
  config/approvals_queue.md   items waiting for Seb"""
import argparse, datetime, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TZ = "America/Argentina/Buenos_Aires"


def money(cents, cur):
    sym = {"usd": "$"}.get(cur, cur.upper() + " ")
    return f"{sym}{cents / 100:,.2f}"


def jload(p):
    try:
        return json.load(open(p))
    except Exception:
        return None


def revenue_lines(summary):
    if not summary:
        return ["Revenue: UNKNOWN (no ledger yet; the Gumroad ledger sync has not run)."], 0
    out = []
    for label, key in (("Yesterday", "last_1d"), ("Last 7 days", "last_7d")):
        w = summary.get(key) or {"orders": 0, "by_currency": {}}
        if not w["orders"]:
            out.append(f"{label}: 0 verified orders, $0.00 net.")
        else:
            parts = [f"{money(c['net_cents'], cur)} net ({money(c['gross_cents'], cur)} gross, {money(c['fee_cents'], cur)} fees, {money(c['refund_cents'], cur)} refunds)"
                     for cur, c in w["by_currency"].items()]
            out.append(f"{label}: {w['orders']} verified order(s), " + "; ".join(parts) + ".")
    cov = summary.get("attribution_coverage")
    out.append("Attribution coverage: " + ("n/a (no orders)" if cov is None else f"{cov:.0%} of orders have a known source"))
    sync = summary.get("sync", {})
    if sync and "ok" not in str(sync.get("sales_api", "")):
        out.append(f"Ledger warning: Gumroad sales API {sync.get('sales_api')}")
    return out, (summary.get("last_7d") or {}).get("orders", 0)


def pending_approvals():
    p = os.path.join(ROOT, "config", "approvals_queue.md")
    if not os.path.exists(p):
        return []
    txt = open(p).read()
    items = []
    for block in re.split(r"\n(?=## )", txt):
        if re.search(r"Status:\s*(AWAITING APPROVAL|DRAFT AWAITING)", block):
            items.append(block.splitlines()[0].lstrip("# ").strip())
    return items


def build(social=None, ops=None, date=None):
    date = date or datetime.datetime.utcnow().date().isoformat()
    summary = jload(os.path.join(ROOT, "state", "ledger", "summary.json"))
    cat = jload(os.path.join(ROOT, "config", "catalog.json")) or {"offers": []}
    rev, orders7 = revenue_lines(summary)
    not_live = [o["offer_id"] for o in cat["offers"] if o["status"] == "not_live"]
    live = [o["offer_id"] for o in cat["offers"] if o["status"] == "live"]
    s = social or {}
    lines = [f"# Revenue brief, {date} ({TZ})", "", "## Executive summary"] + [f"- {l}" for l in rev]
    kit = s.get("kit")
    lines.append(f"- Email leads: {kit.get('subscribers')} subscribers total, {kit.get('new_7d', 'unknown')} new in 7 days" if kit else "- Email leads: UNKNOWN (no Kit snapshot)")
    gc = s.get("goatcounter")
    lines.append(f"- Website: {gc.get('visits_7d')} visits in 7 days, {gc.get('checkout_clicks_7d')} checkout clicks" if gc else "- Website visits: UNKNOWN (GoatCounter API token not connected)")
    lines += ["", "## Funnel health"]
    if orders7 == 0:
        lines.append("- 0 verified orders in 7 days. Priority: reach, guide visits, opt ins and checkout click debugging, not new products.")
    if not_live:
        lines.append(f"- Not purchasable right now: {', '.join(not_live)} (buttons show 'Coming soon').")
    lines.append(f"- Live offers: {len(live)}.")
    lines += ["", "## Content outcomes"]
    soc = s.get("social") or {}
    if soc:
        for net, v in soc.items():
            lines.append(f"- {net}: " + ", ".join(f"{k} {v[k]}" for k in v))
    else:
        lines.append("- UNKNOWN (no Metricool snapshot)")
    pub = s.get("publishing")
    if pub:
        lines.append(f"- Publishing: {pub.get('published', 0)} published, {pub.get('queued', 0)} queued, {pub.get('failed', 0)} failed in the last 24h")
    lines += ["", "## Customer and product signals"]
    if summary and summary.get("by_offer"):
        for o, v in sorted(summary["by_offer"].items(), key=lambda x: -x[1]["orders"]):
            lines.append(f"- {o}: {v['orders']} orders, {v['refunds']} refunded")
    else:
        lines.append("- No SKU sales yet.")
    for q in s.get("top_requests", [])[:3]:
        lines.append(f"- Asked for: {q}")
    lines += ["", "## Operational issues"]
    probs = (ops or {}).get("problems", [])
    lines += [f"- {p}" for p in probs] or ["- None reported."]
    lines += ["", "## Owner decisions"]
    dec = list((s.get("decisions") or []))[:3]
    if not dec:
        pend = pending_approvals()
        dec = [f"Approve or reject: {p}" for p in pend[:3]]
    lines += [f"{i + 1}. {d}" for i, d in enumerate(dec)] or ["None today."]
    md = "\n".join(lines) + "\n"
    os.makedirs(os.path.join(ROOT, "state", "briefs"), exist_ok=True)
    json.dump({"date": date, "tz": TZ, "markdown": md, "orders_7d": orders7, "not_live": not_live},
              open(os.path.join(ROOT, "state", "briefs", f"{date}.json"), "w"), indent=1)
    return md


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--social"); ap.add_argument("--ops"); ap.add_argument("--date")
    a = ap.parse_args()
    print(build(jload(a.social) if a.social else None, jload(a.ops) if a.ops else None, a.date))
