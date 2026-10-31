"""Worker heartbeats and the out-of-band alert path (Continuous Improvement 05, Growth OS 12).

Every scheduled worker (Claude scheduled task or GitHub workflow) ends its run with
    python3 scripts/growthos/heartbeat.py beat <worker> ok|failed ["note"]
which appends to state/heartbeats.jsonl. The hourly GitHub health job checks each worker against its SLA in
config/growthos/workers.json and opens an incident when a worker is late or failed.

Alerts that must reach Seb even if every Claude task is down go out from GitHub Actions itself: an issue in the
repo, assigned to the repo owner (GitHub notifies the owner by email and in the GitHub app). One issue per incident
id (deduplicated); it is closed automatically when the incident resolves.

python3 scripts/growthos/heartbeat.py beat <worker> <status> [note]
python3 scripts/growthos/heartbeat.py check            -> late/failed workers (json)"""
import datetime as dt, json, os, sys, urllib.request
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from events import ROOT, now  # noqa: E402

HB = os.path.join(ROOT, "state", "heartbeats.jsonl")
WORKERS = os.path.join(ROOT, "config", "growthos", "workers.json")


def beat(worker, status, note="", path=HB):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    rec = {"worker": worker, "status": status, "at": now(), "note": (note or "")[:200]}
    with open(path, "a") as f:
        f.write(json.dumps(rec) + "\n")
    return rec


def last_beats(path=HB):
    out = {}
    for l in (open(path) if os.path.exists(path) else []):
        if l.strip():
            r = json.loads(l); out[r["worker"]] = r
    return out


def check(path=HB, workers_path=WORKERS, at=None):
    at = at or dt.datetime.now(dt.timezone.utc)
    W = json.load(open(workers_path))["workers"]; lb = last_beats(path); res = []
    for w, cfg in W.items():
        if not cfg.get("enabled", True):
            continue
        b = lb.get(w)
        if not b:
            since = dt.datetime.fromisoformat(cfg["since"]) if cfg.get("since") else None
            late = since is not None and (at - since).total_seconds() / 3600 > cfg["max_gap_hours"]
            res.append({"check": f"worker:{w}", "ok": not late, "severity": cfg.get("severity", "SEV-3"),
                        "detail": "no heartbeat yet" + (" (overdue)" if late else " (waiting for first run)")})
            continue
        age = (at - dt.datetime.fromisoformat(b["at"])).total_seconds() / 3600
        ok = b["status"] == "ok" and age <= cfg["max_gap_hours"]
        res.append({"check": f"worker:{w}", "ok": ok, "severity": cfg.get("severity", "SEV-3"),
                    "detail": f"last {b['status']} {age:.1f}h ago (limit {cfg['max_gap_hours']}h) {b.get('note', '')}"[:160]})
    return res


# ---------- GitHub issue alerts (works without any Claude session) ----------
def _gh(method, path, body=None):
    tok, repo = os.environ.get("GITHUB_TOKEN"), os.environ.get("GITHUB_REPOSITORY")
    if not tok or not repo:
        raise RuntimeError("no GITHUB_TOKEN/GITHUB_REPOSITORY (only inside GitHub Actions)")
    req = urllib.request.Request(f"https://api.github.com/repos/{repo}{path}", method=method, data=json.dumps(body).encode() if body else None,
                                 headers={"Authorization": f"Bearer {tok}", "Accept": "application/vnd.github+json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read() or "null")


def push_alerts(alerts_path, store, owner, gh=_gh):
    """Open one GitHub issue per unsent SEV-1/SEV-2 alert; close issues of resolved incidents.
    Marks an alert sent only when GitHub accepted the issue. Returns (opened, closed)."""
    if not os.path.exists(alerts_path):
        return 0, 0
    rows = [json.loads(l) for l in open(alerts_path) if l.strip()]
    resolved = {e["payload"]["incident_id"] for e in store.of("incident.resolved")}
    opened = closed = 0
    for a in rows:
        if a.get("issue") is None and not a.get("sent") and a["severity"] in ("SEV-1", "SEV-2") and a["incident_id"] not in resolved:
            try:
                r = gh("POST", "/issues", {"title": f"[{a['severity']}] AUTOPILOT.OI: {a['check']}",
                                           "body": f"{a['detail']}\n\nIncident `{a['incident_id']}` at {a['at']}.\nRunbook: growth-os/RUNBOOKS.md\n"
                                                   "This issue closes itself when the check passes again.",
                                           "assignees": [owner]})
                a["issue"] = r.get("number"); a["sent"] = True; a["sent_at"] = now(); a["channel"] = "github_issue"; opened += 1
            except Exception as e:
                a["send_error"] = str(e)[:120]
        if a.get("issue") and a["incident_id"] in resolved and not a.get("issue_closed"):
            try:
                gh("PATCH", f"/issues/{a['issue']}", {"state": "closed", "state_reason": "completed"})
                gh("POST", f"/issues/{a['issue']}/comments", {"body": "Resolved: the check passes again."})
                a["issue_closed"] = now(); closed += 1
            except Exception as e:
                a["close_error"] = str(e)[:120]
    with open(alerts_path, "w") as f:
        for a in rows:
            f.write(json.dumps(a) + "\n")
    return opened, closed


if __name__ == "__main__":
    if sys.argv[1] == "beat":
        print(json.dumps(beat(sys.argv[2], sys.argv[3], " ".join(sys.argv[4:]))))
    elif sys.argv[1] == "check":
        print(json.dumps(check(), indent=1))
