"""Daily pulse, weekly sprint and monthly review reports (Continuous Improvement playbooks 01, 02, 03).

Deterministic: built only from the event store, ledger, health, heartbeats, viral register, experiments and the
latest social snapshot. Every line is labeled OBSERVED, CALCULATED or MISSING DATA. A missing source is never a 0.
Writes growth-os/operations/run-history/<date>-<kind>.md and prints it. The scheduled Claude runs add judgment
(the one change made, the experiment card, the portfolio memo) on top of these facts.

python3 scripts/growthos/reports.py daily|weekly|monthly [--date YYYY-MM-DD]"""
import datetime as dt, glob, json, os, sys, uuid
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from events import Store, ROOT, now  # noqa: E402
import orders, costs, commander, heartbeat  # noqa: E402

OPS = os.path.join(ROOT, "growth-os", "operations")


def _j(p, d=None):
    try:
        return json.load(open(p))
    except Exception:
        return d


def money_window(store, days, end):
    start = (dt.date.fromisoformat(end) - dt.timedelta(days=days - 1)).isoformat()
    sub = Store.__new__(Store); sub.path = store.path; sub._keys = None
    evs = [e for e in store.all() if start <= e["occurred_at_utc"][:10] <= end]
    class V:  # minimal view over a filtered list
        def of(self, *t):
            return [e for e in evs if e["type"] in t]
    return orders.money(V())


def fmt_money(m):
    if not m["by_currency"]:
        return "0 verified orders, $0.00 net receipts"
    return "; ".join(f"{b['orders']} orders, gross {b['gross_minor'] / 100:.2f} {c}, refunds {b['refunds_minor'] / 100:.2f}, fees {b['fees_minor'] / 100:.2f}, "
                     f"net receipts {b['net_receipts_minor'] / 100:.2f} {c} (unattributed {b['attributed']['unknown'] / 100:.2f})" for c, b in m["by_currency"].items())


def facts(store, date, days):
    led = _j(os.path.join(ROOT, "state", "ledger", "summary.json"), {})
    socials = sorted(glob.glob(os.path.join(ROOT, "state", "social", "*.json")))
    soc = _j(socials[-1], {}) if socials else {}
    kit = soc.get("kit") or {}
    site = _j(os.path.join(ROOT, "state", "ledger", "site.json"), {})
    hs = _j(os.path.join(ROOT, "state", "health", "status.json"), {})
    sys.path.insert(0, os.path.join(ROOT, "scripts", "viral"))
    import gate
    vc = gate.status()
    inc_open = {e["payload"]["incident_id"]: e for e in store.of("incident.opened")}
    for e in store.of("incident.resolved"):
        inc_open.pop(e["payload"]["incident_id"], None)
    since = (dt.date.fromisoformat(date) - dt.timedelta(days=days - 1)).isoformat()
    incidents_window = [e for e in store.of("incident.opened") if e["occurred_at_utc"][:10] >= since]
    return {
        "money": ("OBSERVED", fmt_money(money_window(store, days, date)) + f" · ledger synced {led.get('sync', {}).get('ran', 'MISSING')}"),
        "contribution": ("CALCULATED", costs.report(store, orders.money(store))["contribution_status"]),
        "leads": ("OBSERVED" if kit else "MISSING DATA", f"Kit subscribers {kit.get('subscribers')}, new {kit.get('new_subscribers', kit.get('new_7d'))} (snapshot {os.path.basename(socials[-1])[:10] if socials else 'none'})" if kit else "no Kit snapshot"),
        "visits": ("MISSING DATA", "website analytics not connected (GoatCounter API token missing)") if (not site or "not connected" in str(site.get("status", ""))) else ("OBSERVED", json.dumps(site)[:120]),
        "content": ("OBSERVED", f"{len(vc)} concepts in the evidence register: " + (", ".join(f"{c['content_id']} {c['state']}" for c in vc) or "none")),
        "reliability": ("OBSERVED", f"{sum(1 for v in hs.values() if not v['ok'])} failing checks now; {len(inc_open)} open incidents; {len(incidents_window)} opened in window" if hs else "MISSING DATA: no health status"),
        "workers": ("OBSERVED", ", ".join(f"{r['check'][7:]}={('waiting first run' if 'waiting' in r['detail'] else 'ok') if r['ok'] else 'LATE/FAILED'}" for r in heartbeat.check())),
        "budget": ("CALCULATED", costs.guard(store)["status"]),
    }


def render(kind, date, store=None):
    store = store or Store(); days = {"daily": 1, "weekly": 7, "monthly": 30}[kind]
    run_id = f"{kind}-{date}-{uuid.uuid4().hex[:6]}"
    f = facts(store, date, days); cmd = commander.run(store)
    lines = [f"# {kind.upper()} REPORT · {date} · run {run_id}", f"Generated {now()} UTC. Window: last {days} day(s) ending {date}. Reporting timezone America/Argentina/Buenos_Aires.", ""]
    for k, (label, v) in f.items():
        lines.append(f"- **{k.upper()}** [{label}] {v}")
    lines += ["", f"**BOTTLENECK** [CALCULATED] {cmd['bottleneck']}", "", "**TOP PROPOSALS** (needs owner = approval required)"]
    for p in cmd["top3"]:
        lines.append(f"- {p['title']} · priority {p['priority']} · needs owner: {p['needs_owner']} · evidence: {p['evidence']}")
    if kind == "weekly":
        exp = os.path.join(ROOT, "experiments", "experiments.jsonl")
        ex = [json.loads(l) for l in open(exp) if l.strip()] if os.path.exists(exp) else []
        lines += ["", "**EXPERIMENTS** [OBSERVED] " + (", ".join(f"{e.get('id')} {e.get('status')}" for e in ex) or "none")]
        lines.append("**SAMPLE RULE** No winner is declared below an experiment's min_sample; small samples are INCONCLUSIVE.")
    if kind == "monthly":
        cat = _j(os.path.join(ROOT, "config", "catalog.json"), {})
        m = orders.money(store)
        lines += ["", "**PORTFOLIO** [CALCULATED] (KEEP needs verified orders; without orders a live product is VALIDATE)"]
        per = {}
        for e in store.of("order.paid"):
            if not e["payload"].get("test"):
                per[e["payload"]["product_id"]] = per.get(e["payload"]["product_id"], 0) + 1
        for o in cat.get("offers", []):
            if o.get("status") == "retired":
                continue
            n = per.get(o["offer_id"], 0)
            verdict = "NOT LIVE" if o["status"] != "live" else ("VALIDATE (no verified orders)" if n == 0 else "KEEP or IMPROVE (check refunds, activation)")
            lines.append(f"- {o['offer_id']}: {o['status']} · verified orders {n} · {verdict}")
        stage = "Stage A (Validate): no verified end to end funnel yet" if m["orders"] == 0 else "Stage A/B: check repeat sales and refunds"
        lines += ["", f"**SCALE STAGE** [CALCULATED] {stage}. Red flags stop expansion: missing budget caps = {costs.guard(store)['status'].startswith('UNCAPPED')}."]
    lines += ["", "Labels: OBSERVED = read from a provider or log; CALCULATED = computed from observed data; MISSING DATA = source not connected (never shown as 0)."]
    txt = "\n".join(lines)
    d = os.path.join(OPS, "run-history"); os.makedirs(d, exist_ok=True)
    open(os.path.join(d, f"{date}-{kind}.md"), "w").write(txt + "\n")
    return txt


if __name__ == "__main__":
    kind = sys.argv[1]
    date = sys.argv[sys.argv.index("--date") + 1] if "--date" in sys.argv else dt.date.today().isoformat()
    print(render(kind, date))
