#!/usr/bin/env python3
"""Build the HQ live page feed (status/hub) from real sources only.

Sources: GitHub Actions runs (gh run list), the Gumroad ledger summary
(state/ledger/summary.json) and approvals waiting on Seb (queue/viral files with
status "awaiting_seb" plus "Awaiting approval" sections in next-actions.md).
Missing data stays null. No customer data, no secrets.

Usage: python3 scripts/growthos/hq_feed.py > /tmp/hub.json
"""
import json, re, subprocess, sys, glob, datetime as dt
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WORKFLOWS = ["post.yml", "freel.yml", "market.yml", "daily.yml", "revenue.yml", "gumroad.yml", "health.yml", "ci.yml"]


def now():
    return dt.datetime.now(dt.timezone.utc)


def iso(t):
    return t.strftime("%Y-%m-%dT%H:%M:%SZ") if t else None


def parse(s):
    return dt.datetime.fromisoformat(s.replace("Z", "+00:00")) if s else None


def github():
    out = {}
    for wf in WORKFLOWS:
        try:
            r = subprocess.run(["gh", "run", "list", "--workflow", wf, "-L", "100", "--json",
                                "status,conclusion,createdAt,updatedAt,startedAt"], capture_output=True, text=True, timeout=60, cwd=ROOT)
            runs = json.loads(r.stdout or "[]") if r.returncode == 0 else None
        except Exception:
            runs = None
        if runs is None:
            out[wf] = None
            continue
        if not runs:
            out[wf] = {"status": "none", "conclusion": None, "started": None, "finished": None, "runs24h": 0, "fails24h": 0}
            continue
        last = runs[0]
        day = now() - dt.timedelta(hours=24)
        recent = [x for x in runs if parse(x["createdAt"]) >= day]
        done = last["status"] == "completed"
        out[wf] = {
            "status": last["status"], "conclusion": last.get("conclusion") or None,
            "started": last.get("startedAt") or last["createdAt"], "finished": last["updatedAt"] if done else None,
            "runs24h": len(recent), "fails24h": sum(1 for x in recent if x.get("conclusion") in ("failure", "timed_out")),
        }
    return out


def revenue():
    p = ROOT / "state/ledger/summary.json"
    if not p.exists():
        return None
    s = json.loads(p.read_text())
    net = {}
    for cur, v in (s.get("last_7d", {}).get("by_currency") or {}).items():
        if isinstance(v, dict):
            val = v.get("net", v.get("net_receipts"))
            if val is not None:
                net[cur] = round(float(val), 2)
    return {
        "orders_all_time": s.get("verified_orders_all_time"),
        "orders_7d": (s.get("last_7d") or {}).get("orders"),
        "net_7d": net,
        "refunds_all_time": s.get("refunds_all_time"),
        "ledger_synced": (s.get("sync") or {}).get("ran") or s.get("generated"),
    }


def approvals():
    items = []
    for f in glob.glob(str(ROOT / "queue/**/*.json"), recursive=True) + glob.glob(str(ROOT / "viral/**/*.json"), recursive=True):
        try:
            d = json.loads(Path(f).read_text())
        except Exception:
            continue
        if isinstance(d, dict) and d.get("status") == "awaiting_seb":
            items.append(Path(f).stem)
    na = ROOT / "growth-os/operations/next-actions.md"
    if na.exists():
        sec = None
        for line in na.read_text().splitlines():
            if line.startswith("## "):
                sec = line[3:].lower().startswith("awaiting approval")
            elif sec and re.match(r"^\s*[-*] ", line):
                items.append(re.sub(r"^\s*[-*] ", "", line)[:80])
    return {"count": len(items), "items": items[:8]}


if __name__ == "__main__":
    json.dump({"at": iso(now()), "by": "ANALYST", "github": github(), "revenue": revenue(), "approvals": approvals()}, sys.stdout)
