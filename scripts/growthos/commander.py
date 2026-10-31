"""Growth Commander (section 08): the brain, not the bank.

Daily: read health -> read verified funnel -> pick ONE bottleneck -> propose up to 3 actions with evidence,
hypothesis, expected benefit, rollback and whether owner approval is needed. It executes nothing customer facing;
proposals land in the owner's decisions list (brief + dashboard) and internal low tier work can be queued as jobs.

priority = (impact x confidence x reversibility) / (effort x risk)   (illustrative, inputs shown, never hidden)
Broken checkout, wrong billing, privacy and fraud issues always outrank growth experiments.

python3 scripts/growthos/commander.py [--write]"""
import glob, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from events import Store, ROOT, now  # noqa: E402
import orders, costs  # noqa: E402


def _j(p, d=None):
    try:
        return json.load(open(p))
    except Exception:
        return d


def snapshot(store):
    hs = _j(os.path.join(ROOT, "state", "health", "status.json"), {})
    health = {"failing": [k for k, v in hs.items() if not v["ok"]],
              "results": [{"check": k, "ok": v["ok"], "severity": v["severity"]} for k, v in hs.items()]}
    cat = _j(os.path.join(ROOT, "config", "catalog.json"), {})
    offers = cat.get("offers", cat if isinstance(cat, list) else [])
    not_live = [o.get("offer_id") for o in offers if isinstance(o, dict) and o.get("status") in ("not_live", "missing")]
    social = sorted(glob.glob(os.path.join(ROOT, "state", "social", "*.json")))
    soc = _j(social[-1], {}) if social else {}
    kit = soc.get("kit") or {}
    site = _j(os.path.join(ROOT, "state", "ledger", "site.json"), {})
    m = orders.money(store)
    sys.path.insert(0, os.path.join(ROOT, "scripts", "viral"))
    import gate
    concepts = gate.status()
    waiting = [c for c in concepts if c["state"] == "QUALITY_PASSED"]
    aq = open(os.path.join(ROOT, "config", "approvals_queue.md")).read() if os.path.exists(os.path.join(ROOT, "config", "approvals_queue.md")) else ""
    return {"at": now(), "health_failing": health.get("failing", []),
            "critical": [r["check"] for r in health.get("results", []) if not r["ok"] and r.get("severity") == "SEV-1"],
            "not_live_offers": not_live, "subscribers": kit.get("subscribers") if isinstance(kit, dict) else None,
            "site_connected": bool(site) and site.get("status") != "not connected",
            "orders": m["orders"], "unattributed_orders": m["unattributed_orders"], "budget": costs.guard(store),
            "viral_waiting_owner": [c["content_id"] for c in waiting], "viral_concepts": len(concepts),
            "approvals_waiting": aq.count("AWAITING APPROVAL"),
            "ungated_publishers": _j(os.path.join(ROOT, "config", "growthos", "cutover.json"), {}).get("ungated_publishers", [])}


def proposals(s):
    P = []
    def add(pid, title, why, action, impact, conf, rev, effort, risk, approval, rollback, metric):
        P.append({"id": pid, "title": title, "evidence": why, "action": action, "needs_owner": approval, "rollback": rollback,
                  "success_metric": metric, "inputs": {"impact": impact, "confidence": conf, "reversibility": rev, "effort": effort, "risk": risk},
                  "priority": round(impact * conf * rev / (effort * risk), 2)})
    if s["critical"]:
        add("recover_critical", "Fix critical health checks first", f"SEV-1 failing: {', '.join(s['critical'])}", "run recovery runbook; pause dependent outbound",
            10, .9, 1, 1, 1, True, "n/a", "checks pass")
    if s["not_live_offers"]:
        add("checkout_live", "Make queued products buyable", f"not purchasable: {', '.join(s['not_live_offers'])}",
            "re-run the Gumroad sync after the daily create limit resets (automatic every 6h)", 8, .9, 1, 1, 1, False, "set draft true", "offers in docs/live.json")
    if s["ungated_publishers"]:
        add("gate_publishers", "Route every publisher through NO PROOF, NO POST", f"{len(s['ungated_publishers'])} workers can post without the gate",
            "owner authorizes cutover (config/growthos/cutover.json)", 7, .9, .9, 2, 1.5, True, "restore previous task prompts (growth-os/rollback/)", "0 ungated scheduled posts")
    if s["viral_waiting_owner"]:
        add("review_concepts", "Review concepts ready for you", f"{len(s['viral_waiting_owner'])} passed the gate", "approve or reject on the Approval Queue page",
            6, .7, 1, .5, 1, True, "reject", "approved concept queued")
    if s["subscribers"] in (0, None) and not s["site_connected"]:
        add("measure_funnel", "Turn on page view tracking reads", "0 email leads and website traffic is unknown (GoatCounter API not connected)",
            "owner adds GOATCOUNTER_TOKEN secret (read only)", 5, .8, 1, .5, 1, True, "delete the secret", "site.json shows visits")
    if s["orders"] == 0 and s["subscribers"] == 0:
        add("first_funnel", "Prove one funnel: Subscription Leak", "0 orders, 0 leads: volume is not the bottleneck, proof is",
            "one gated Subscription video -> /g/subs/ -> opt in -> $10 kit; trace every step", 6, .5, 1, 2, 1, True, "pause the concept", "first traced order or lead")
    if s["budget"]["status"].startswith("UNCAPPED"):
        add("set_caps", "Set AI and service spend caps", "no owner approved caps; costs are recorded but unbounded", "owner picks daily soft/hard caps",
            4, .9, 1, .3, 1, True, "edit budget.json", "caps enforced")
    if s["approvals_waiting"] >= 2:
        add("clear_queue", "Decide the waiting drafts", f"{s['approvals_waiting']} items AWAITING APPROVAL", "approve or reject in config/approvals_queue.md",
            3, .6, 1, .3, 1, True, "n/a", "queue empty")
    # broken checkout, billing, privacy and fraud outrank everything; then policy/safety; then growth
    CLASS = {"recover_critical": 0, "checkout_live": 1, "gate_publishers": 2, "set_caps": 2, "review_concepts": 3,
             "first_funnel": 3, "measure_funnel": 3, "clear_queue": 4}
    P.sort(key=lambda p: (CLASS.get(p["id"], 5), -p["priority"]))
    return P


def run(store=None, write=False):
    store = store or Store(); s = snapshot(store); props = proposals(s)
    out = {"at": s["at"], "snapshot": s, "bottleneck": props[0]["title"] if props else "none found", "top3": props[:3], "all": props}
    if write:
        d = os.path.join(ROOT, "state", "commander"); os.makedirs(d, exist_ok=True)
        json.dump(out, open(os.path.join(d, s["at"][:10] + ".json"), "w"), indent=1)
    return out


if __name__ == "__main__":
    o = run(write="--write" in sys.argv)
    print(json.dumps({"bottleneck": o["bottleneck"], "top3": [(p["title"], p["priority"], p["needs_owner"]) for p in o["top3"]]}, indent=1))
