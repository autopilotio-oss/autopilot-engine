"""Pulls Instagram stats, merges them with Threads stats, and writes SCOREBOARD.md:
which series and posts are winning, so the daily upgrade can double down on them."""
import os, sys, json, glob, re, datetime as dt
sys.path.insert(0, os.path.dirname(__file__))
import instagram
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def load(p, d):
    try: return json.load(open(os.path.join(ROOT, p)))
    except Exception: return d

def series(pid, kind):
    if pid.startswith("ig-l") or pid == "ig-c03": return "IG lesson carousel"
    if pid.startswith("ig-c"): return "IG list carousel"
    m = re.search(r"-(market|tip|quiz|answer|fact|poll)$", pid)
    if m: return "IG story: " + {"fact": "everyday fix"}.get(m.group(1), m.group(1))
    return "Threads " + kind

def ig_metrics(mid, kind, token):
    sets = (["reach", "replies", "navigation", "views"], ["reach", "replies"]) if kind == "story" else \
           (["reach", "views", "likes", "comments", "saved", "shares"], ["reach", "likes", "comments", "saved", "shares"])
    for m in sets:
        try:
            r = instagram._req("GET", f"/{mid}/insights", {"metric": ",".join(m)}, token)
            out = {}
            for x in r.get("data", []):
                v = x.get("values", [{}])[0].get("value", x.get("total_value", {}).get("value", 0))
                out[x["name"]] = v if isinstance(v, (int, float)) else sum(v.values()) if isinstance(v, dict) else 0
            return out
        except Exception as e:
            err = e
    print("skip", mid, err); return None

def collect_ig():
    token = instagram.get_token()
    ins = load("state/insights_ig.json", {})
    if not token: return ins
    cut = dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=14)
    for pid, v in load("state/posted_ig.json", {}).items():
        if not v.get("media_id") or dt.datetime.fromisoformat(v["at"]) < cut: continue
        m = ig_metrics(v["media_id"], v.get("kind", ""), token)
        if m: ins[pid] = {**ins.get(pid, {}), **m, "kind": v.get("kind"), "at": v["at"]}
    json.dump(ins, open(os.path.join(ROOT, "state/insights_ig.json"), "w"), indent=1)
    return ins

def score(m):
    views = m.get("views") or m.get("reach") or 0
    act = m.get("likes", 0) + 3 * (m.get("replies", 0) + m.get("comments", 0)) + 4 * (m.get("saved", 0) + m.get("shares", 0) + m.get("reposts", 0) + m.get("quotes", 0))
    return views, act, round(100 * act / views, 1) if views else 0.0

def main():
    ig = collect_ig()
    th = load("state/insights.json", {})
    posted = load("state/posted.json", {})
    text = {}
    for f in glob.glob(os.path.join(ROOT, "queue", "*.json")):
        for p in load(f, []): text[p["id"]] = (p.get("text") or "").split("\n")[0][:90]
    rows = []
    for pid, m in th.items():
        rows.append(("Threads", pid, series(pid, posted.get(pid, {}).get("kind", "?")), *score(m)))
    for pid, m in ig.items():
        rows.append(("Instagram", pid, series(pid, m.get("kind", "?")), *score(m)))
    agg = {}
    for r in rows:
        a = agg.setdefault(r[2], [0, 0, 0]); a[0] += 1; a[1] += r[3]; a[2] += r[4]
    L = [f"# Scoreboard\n\nUpdated {dt.datetime.now(dt.timezone.utc):%Y-%m-%d %H:%M} UTC. Score = likes + 3×comments/replies + 4×saves/shares/reposts, per 100 views. Last 14 days.\n",
         "## By series (what to double down on)\n", "| Series | Posts | Avg views | Score per 100 views |", "|---|---|---|---|"]
    for k, (n, v, a) in sorted(agg.items(), key=lambda x: -(x[1][2] / x[1][1] if x[1][1] else 0)):
        L.append(f"| {k} | {n} | {v // n} | {round(100 * a / v, 1) if v else 0} |")
    L += ["\n## Top posts\n", "| Where | Post | Views | Score/100 | First line |", "|---|---|---|---|---|"]
    for r in sorted(rows, key=lambda r: (-r[5], -r[3]))[:10]:
        L.append(f"| {r[0]} | {r[1]} | {r[3]} | {r[5]} | {text.get(r[1], '')} |")
    L += ["\n## Bottom posts\n", "| Where | Post | Views | Score/100 | First line |", "|---|---|---|---|---|"]
    for r in sorted(rows, key=lambda r: (r[5], r[3]))[:5]:
        L.append(f"| {r[0]} | {r[1]} | {r[3]} | {r[5]} | {text.get(r[1], '')} |")
    open(os.path.join(ROOT, "SCOREBOARD.md"), "w").write("\n".join(L) + "\n")
    print("scoreboard rows", len(rows))

if __name__ == "__main__":
    main()
