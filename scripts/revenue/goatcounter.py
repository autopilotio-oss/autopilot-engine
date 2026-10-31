"""Website numbers from GoatCounter (aggregate counts only, no visitor data).
python3 scripts/revenue/goatcounter.py   (needs GOATCOUNTER_TOKEN; without it writes status "not connected")
-> state/ledger/site.json: visits and top pages for 1 and 7 days, checkout clicks, opt ins, quiz completions per path."""
import json, os, sys, urllib.request, urllib.parse, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "state", "ledger", "site.json")
BASE = "https://autopilotoi.goatcounter.com/api/v0"


def get(path, params):
    req = urllib.request.Request(f"{BASE}{path}?{urllib.parse.urlencode(params)}",
                                 headers={"Authorization": "Bearer " + os.environ["GOATCOUNTER_TOKEN"].strip(), "Content-Type": "application/json"})
    return json.loads(urllib.request.urlopen(req, timeout=60).read().decode())


def window(days):
    end = datetime.datetime.now(datetime.timezone.utc).replace(minute=0, second=0, microsecond=0)
    start = end - datetime.timedelta(days=days)
    p = {"start": start.strftime("%Y-%m-%dT%H:%M:%SZ"), "end": end.strftime("%Y-%m-%dT%H:%M:%SZ")}
    total = get("/stats/total", p)
    hits = get("/stats/hits", p | {"limit": 100}).get("hits", [])
    events = {h["path"]: h.get("count", 0) for h in hits if h.get("event")}
    pages = sorted(((h["path"], h.get("count", 0)) for h in hits if not h.get("event")), key=lambda x: -x[1])[:15]
    def sum_prefix(pre): return sum(v for k, v in events.items() if k.startswith(pre))
    return {"visits": total.get("total") or total.get("total_events"), "top_pages": pages,
            "checkout_clicks": sum_prefix("checkout-click/"), "optins": sum_prefix("optin/"), "quiz_completions": sum_prefix("quiz-complete"),
            "events": events}


if __name__ == "__main__":
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    if not os.environ.get("GOATCOUNTER_TOKEN"):
        json.dump({"status": "not connected: add a GoatCounter API token as the GOATCOUNTER_TOKEN repo secret"}, open(OUT, "w"), indent=1)
        print("GoatCounter not connected"); sys.exit(0)
    try:
        d = {"status": "ok", "checked": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"), "last_1d": window(1), "last_7d": window(7)}
    except Exception as e:
        d = {"status": "error: " + repr(e)[:160]}
    json.dump(d, open(OUT, "w"), indent=1); print(d["status"])
