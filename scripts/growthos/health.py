"""P1-12 Self healing operations: probes, incidents, alerts (section 12).

Runs hourly in GitHub Actions (.github/workflows/health.yml), which can reach the live site and Gumroad.
Each failed check opens one incident per check per day (idempotent) with a severity; a passing check resolves it.
Safe automatic recovery only: re-dispatch the Gumroad sync or the ledger sync. Nothing public is changed.
Alerts are written to state/health/alerts.jsonl as UNSENT; the daily chief of staff (or the next interactive
session) delivers them and marks them sent. We never claim the owner was notified when he wasn't.

python3 scripts/growthos/health.py run [--recover]"""
import datetime as dt, json, os, sys, urllib.request
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from events import Store, ROOT, now  # noqa: E402

PAGES = [("home", "https://autopilotoi.app/", "href=\"g/subs/\""), ("free", "https://autopilotoi.app/free/", "/g/subs/"),
         ("store", "https://autopilotoi.app/store/", "gumroad.com/l/"), ("workspace", "https://autopilotoi.app/workspace/", "gumroad.com/l/workspace"),
         ("guide_subs", "https://autopilotoi.app/g/subs/", "gumroad.com/l/subs-agent"), ("brain", "https://autopilotoi.app/brain/", "kit.com"),
         ("guide_refund", "https://autopilotoi.app/g/refund/", "gumroad.com/l/refund-agent"), ("guide_bill", "https://autopilotoi.app/g/bill/", "gumroad.com/l/bill-agent"),
         ("guide_shop", "https://autopilotoi.app/g/shop/", "gumroad.com/l/shop-agent"), ("guide_video", "https://autopilotoi.app/g/video/", "gumroad.com/l/video-agent"),
         ("guide_sell", "https://autopilotoi.app/g/sell/", "gumroad.com/l/sell-agent"), ("guide_raise", "https://autopilotoi.app/g/raise/", "gumroad.com/l/raise-agent")]
CHECKOUT = "https://autopilotoi.gumroad.com/l/{}"
HDIR = os.path.join(ROOT, "state", "health")


def http_get(url, timeout=20):
    req = urllib.request.Request(url, headers={"User-Agent": "autopilot-health/1"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.status, r.read(400000).decode("utf-8", "replace")


def _age_h(iso):
    t = dt.datetime.fromisoformat(iso.replace("Z", "+00:00"))
    return (dt.datetime.now(dt.timezone.utc) - t).total_seconds() / 3600


def check_pages(fetch=http_get):
    out = []
    for name, url, marker in PAGES:
        try:
            code, body = fetch(url)
            ok = code == 200 and marker in body
            out.append({"check": f"page:{name}", "ok": ok, "severity": "SEV-2", "detail": f"{code}, marker {'found' if marker in body else 'missing'}"})
        except Exception as e:
            out.append({"check": f"page:{name}", "ok": False, "severity": "SEV-2", "detail": str(e)[:120]})
    return out


def check_checkout(fetch=http_get, root=ROOT):
    """Every product the site sells (docs/live.json) must open a working Gumroad checkout page."""
    out = []
    try: live = json.load(open(os.path.join(root, "docs", "live.json")))["live"]
    except Exception as e: return [{"check": "checkout:live_json", "ok": False, "severity": "SEV-1", "detail": str(e)[:120]}]
    for slug in ["subs-agent", "refund-agent", "bill-agent"]:
        if slug not in live:
            out.append({"check": f"checkout:{slug}", "ok": False, "severity": "SEV-1", "detail": "flagship not live on Gumroad"})
    for slug in live:
        try:
            code, body = fetch(CHECKOUT.format(slug))
            out.append({"check": f"checkout:{slug}", "ok": code == 200 and "gumroad" in body.lower(), "severity": "SEV-1", "detail": f"{code}"})
        except Exception as e:
            out.append({"check": f"checkout:{slug}", "ok": False, "severity": "SEV-1", "detail": str(e)[:120]})
    return out


def approved_post_uuids(root=ROOT):
    """Metricool uuids and ids of posts Seb approved (factory reel queue, incl. the campaign standing approval)."""
    import glob
    ids = set()
    for f in glob.glob(os.path.join(root, "queue", "freel", "*.json")):
        q = json.load(open(f))
        if not (q.get("approval") or {}).get("quote"): continue
        for p in q.get("posts", []):
            for k in ("uuid", "metricool_id"):
                if p.get(k) is not None: ids.add(str(p[k]))
    try:
        for v in json.load(open(os.path.join(root, "viral", "staged.json"))).values(): ids.add(str(v.get("metricool_uuid")))
    except Exception: pass
    return ids


def check_files(root=ROOT):
    out = []
    try:
        live = json.load(open(os.path.join(root, "docs", "live.json")))
        out.append({"check": "gumroad_sync_fresh", "ok": _age_h(live["checked"]) < 8, "severity": "SEV-2", "detail": f"live.json {live['checked']}"})
    except Exception as e:
        out.append({"check": "gumroad_sync_fresh", "ok": False, "severity": "SEV-2", "detail": str(e)[:120]})
    try:
        s = json.load(open(os.path.join(root, "state", "ledger", "summary.json")))
        ok = _age_h(s["sync"]["ran"]) < 6 and str(s["sync"].get("sales_api", "")).startswith("ok")
        out.append({"check": "revenue_ledger_fresh", "ok": ok, "severity": "SEV-2", "detail": f"{s['sync']['ran']} {s['sync'].get('sales_api')}"})
    except Exception as e:
        out.append({"check": "revenue_ledger_fresh", "ok": False, "severity": "SEV-2", "detail": str(e)[:120]})
    try:
        dbg = json.load(open(os.path.join(root, "state", "gumroad_debug.json")))
        errs = [d for d in dbg if d and d[0] in ("fail", "crash", "update_fail", "cover_fail", "re_enable_fail", "offer_code_fail", "adopt_fail")]
        out.append({"check": "gumroad_errors", "ok": not errs, "severity": "SEV-3", "detail": f"{len(errs)} error(s)"})
    except Exception:
        pass
    return out


def check_fulfillment(store, products_state):
    """Paid but undelivered: every paid order must map to a published Gumroad product with an uploaded file.
    Gumroad itself delivers the file at checkout; this catches orders for products we can't confirm."""
    sys.path.insert(0, os.path.join(ROOT, "scripts", "revenue"))
    from ids import offer_id
    by_offer = {offer_id(k): v for k, v in products_state.items()}
    bad = []
    for e in store.of("order.paid"):
        p = e["payload"]
        if p.get("test"):
            continue
        st = by_offer.get(p["product_id"])
        if not st or not st.get("id") or not st.get("published"):
            bad.append(p["order_id"])
    return [{"check": "paid_but_undelivered", "ok": not bad, "severity": "SEV-2",
             "detail": f"{len(bad)} order(s) for products not confirmed live", "orders": bad}]


def check_integrity(store):
    out = []
    ok, n = store.verify()
    out.append({"check": "event_store_chain", "ok": ok, "severity": "SEV-1", "detail": f"{n}"})
    sys.path.insert(0, os.path.join(ROOT, "scripts", "viral"))
    try:
        import gate
        vok, vn = gate.verify_audit()
        out.append({"check": "viral_audit_chain", "ok": vok, "severity": "SEV-1", "detail": f"{vn} events"})
        q = gate.check_queue()
        if gate.POLICY.get("active"):
            out.append({"check": "viral_queue_guard", "ok": not q, "severity": "SEV-1", "detail": f"{len(q)} ungated item(s) after enforcement date"})
        else:
            out.append({"check": "viral_queue_guard", "ok": True, "severity": "SEV-1", "detail": f"not enforced yet (owner cutover pending): {len(q)} item(s) would be held"})
    except Exception as e:
        out.append({"check": "viral_audit_chain", "ok": False, "severity": "SEV-2", "detail": str(e)[:120]})
    return out


def check_jobs(queue):
    dl = queue.dead_letters()
    backlog = [j for j in queue.jobs().values() if j["status"] in ("QUEUED", "RETRY_WAIT")]
    return [{"check": "dead_letters", "ok": not dl, "severity": "SEV-3", "detail": f"{len(dl)} dead lettered"},
            {"check": "queue_backlog", "ok": len(backlog) < 50, "severity": "SEV-3", "detail": f"{len(backlog)} waiting"}]


def check_metricool(posts, approved_ids=None):
    """Run from a session with the Metricool connector: scheduled versus published, and (once the policy is active)
    any scheduled post without an approved content_id."""
    err = [p for p in posts if any(pr.get("status") == "ERROR" for pr in p.get("providers", []))]
    out = [{"check": "metricool_errors", "ok": not err, "severity": "SEV-3", "detail": f"{len(err)} post(s) in ERROR"}]
    if approved_ids is not None:
        rogue = [p.get("uuid") for p in p_pending(posts) if not any(cid in (p.get("text") or "") for cid in approved_ids)]
        out.append({"check": "metricool_unapproved", "ok": not rogue, "severity": "SEV-1", "detail": f"{len(rogue)} pending post(s) without approval"})
    return out


def p_pending(posts):
    return [p for p in posts if not p.get("draft") and any(pr.get("status") == "PENDING" for pr in p.get("providers", []))]


def record(store, results, day=None):
    """Open one incident per failing check per day; resolve when it passes. Returns new alerts."""
    day = day or dt.date.today().isoformat(); alerts = []
    open_inc = {}
    for e in store.of("incident.opened"):
        open_inc[e["payload"]["incident_id"]] = e
    for e in store.of("incident.resolved"):
        open_inc.pop(e["payload"]["incident_id"], None)
    for r in results:
        iid = f"inc:{r['check']}:{day}"
        active = [k for k in open_inc if k.startswith(f"inc:{r['check']}:")]
        if not r["ok"]:
            _, created = store.append("incident.opened", {"incident_id": iid, "severity": r["severity"], "check": r["check"], "detail": r["detail"]},
                                      "growthos.health", iid, "health")
            if created and not active:
                alerts.append({"incident_id": iid, "severity": r["severity"], "check": r["check"], "detail": r["detail"], "at": now(), "sent": False})
        else:
            for k in active:
                store.append("incident.resolved", {"incident_id": k, "by": "probe passed"}, "growthos.health", f"res:{k}", "health")
    if alerts:
        os.makedirs(HDIR, exist_ok=True)
        with open(os.path.join(HDIR, "alerts.jsonl"), "a") as f:
            for a in alerts:
                f.write(json.dumps(a) + "\n")
    return alerts


def recover(results, dispatch):
    """Safe automatic recovery only (re-run syncs). dispatch(workflow_file) triggers a GitHub workflow."""
    done = []
    for r in results:
        if not r["ok"] and r["check"] == "gumroad_sync_fresh":
            dispatch("gumroad.yml"); done.append("gumroad.yml")
        if not r["ok"] and r["check"] == "revenue_ledger_fresh":
            dispatch("revenue.yml"); done.append("revenue.yml")
    return done


if __name__ == "__main__":
    from jobs import Queue
    st = Store(); res = check_pages() + check_checkout() + check_files()
    ps = os.path.join(ROOT, "state", "products.json")
    res += check_fulfillment(st, json.load(open(ps)) if os.path.exists(ps) else {}) + check_integrity(st) + check_jobs(Queue())
    import heartbeat
    res += heartbeat.check()
    drill = os.environ.get("SIMULATE_FAILURE")
    res.append({"check": "simulated_failure", "ok": not drill, "severity": "SEV-2", "detail": ("drill: " + drill) if drill else "no drill running"})
    alerts = record(st, res)
    if os.environ.get("GITHUB_TOKEN"):
        try:
            print("github issues opened/closed:", heartbeat.push_alerts(os.path.join(HDIR, "alerts.jsonl"), st, os.environ.get("ALERT_ASSIGNEE", "autopilotio-oss")))
        except Exception as e:
            print("alert push failed:", str(e)[:150])
    os.makedirs(HDIR, exist_ok=True)
    json.dump({"at": now(), "results": res, "failing": [r["check"] for r in res if not r["ok"]], "new_alerts": len(alerts)},
              open(os.path.join(HDIR, "latest.json"), "w"), indent=1)
    # status.json has no timestamps, so git only sees a change when a check flips (keeps commits and Pages builds rare)
    json.dump({r["check"]: {"ok": r["ok"], "severity": r["severity"]} for r in res}, open(os.path.join(HDIR, "status.json"), "w"), indent=1, sort_keys=True)
    if "--recover" in sys.argv:
        def dispatch(wf):
            tok, repo = os.environ.get("GITHUB_TOKEN"), os.environ.get("GITHUB_REPOSITORY")
            if tok and repo:
                req = urllib.request.Request(f"https://api.github.com/repos/{repo}/actions/workflows/{wf}/dispatches", method="POST",
                                             data=b'{"ref":"main"}', headers={"Authorization": f"Bearer {tok}", "Accept": "application/vnd.github+json"})
                urllib.request.urlopen(req, timeout=20)
        print("recovery:", recover(res, dispatch))
    print(json.dumps({"failing": [r["check"] for r in res if not r["ok"]], "new_alerts": len(alerts)}))
